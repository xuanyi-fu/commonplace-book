---
type: synthesis
status: draft
created: 2026-04-24
updated: 2026-04-24
---

# Claude Code context assembly and state deltas

Analyzed Claude Code commit: `0a0498cf6a04d144aba289366a55b1edf328a797`.

Claude Code 的 model-visible context 不应该被理解成 Codex 那种 Responses API ordered `input` stream。更贴近源码的模型是：Claude Code 在 client 侧维护 `systemPrompt`、`userContext`、`systemContext`、conversation `messages`、`AttachmentMessage`、tool schemas 和 request controls，然后在 Anthropic Messages API 边界组装成 `system` blocks、`messages`、`tools`、`thinking`、可选 `context_management` 等字段。[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]

## 核心判断

Claude Code 的普通 turn 从 `QueryEngine.submitMessage()` 进入，先拿到 `systemPrompt` / `userContext` / `systemContext`，再处理 user input 和 attachments，随后 `query()` 对 messages 做 compact / collapse / microcompact 一类 pre-API transform，最后在 `claude.ts` 里 normalize messages、build `system` blocks、build tool schemas，并调用 `anthropic.beta.messages.create()`。这是一条 Anthropic Messages request assembly path，不是一个把所有材料拼成单一 prompt string 的路径。[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]

关键位置关系是：

```text
Anthropic Messages request:
  system:
    attribution / CLI prefix
    default or custom systemPrompt sections
    appended systemContext text
    prompt-cache block controls

  messages:
    prepended meta user <system-reminder> from userContext
    normalized conversation history
    normalized attachment-derived meta user reminders / tool-result messages

  tools:
    schemas from toolToAPISchema()

  controls:
    max_tokens, thinking, betas, output_config, optional context_management
```

这个模型里，`systemContext` 和 `userContext` 是不同通道：`systemContext` 被 append 到 `systemPrompt`，`userContext` 被 prepend 到 `messages` 作为 `isMeta` user `<system-reminder>`。这点和 Codex 的 `contextual user fragments` 有相似性，但不能直接套用 Codex 的 `input` stream 术语。[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]] [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]

## State-change 模型

和 Codex 的集中式 context diff 相比，Claude Code 在 inspected path 里更像是“冻结 cache prefix，然后用专门的 tail delta/attachment 补充变化”。这个判断是 implementation inference：源码明确展示了多个 domain-specific delta path，但这份研究没有证明仓库中不存在任何别的通用 diff helper。[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]

日期变化是最清楚的例子。`currentDate` 起初在 memoized `userContext` 里出现；午夜后，代码注释明确说不清空 cached prefix，而是 append 一个 `date_change` attachment 到 conversation tail。这个 attachment 之后被渲染为 `isMeta` user `<system-reminder>`，内容是“Today's date is now ...”。[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]

其他变化也走专门路径：

- `deferred_tools_delta`：扫描旧 attachment，重建已经宣布过的 deferred tools，再和当前 deferred-tool pool 做 added/removed diff。[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]
- `agent_listing_delta`：扫描旧 `agent_listing_delta`，重建已宣布 agent type，再和当前可用 agent type 做 diff。[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]
- `mcp_instructions_delta`：扫描旧 `mcp_instructions_delta`，把当前 connected MCP instructions 和已宣布 instructions 比较；如果 delta path 关闭，则回退到 volatile system prompt section，这条回退会牺牲 prompt cache 稳定性。[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]
- `systemPromptSection()`：默认 section 被缓存到 `/clear` 或 `/compact`；只有显式标成 `DANGEROUS_uncachedSystemPromptSection()` 的 section 才每 turn recompute。[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]

因此 Claude Code 的 state-change 管理更像一组 cache-preserving patches：能保存在 tail message/attachment 里的变化，就不要改 prompt-cache prefix；不能走 delta path 时，才使用会 cache-bust 的 volatile system prompt section。

## 和 Codex 的对照

Codex 的当前研究模型是：`instructions` 和 `tools` 是 request 顶层字段，conversation material 进入有序 `input` stream；context update 和 diff 本身也是 stream item，例如 date 变化可以成为新的 role=`user` `<environment_context>` item，插在下一条真实 user message 前。[[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]] [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]

Claude Code 的对照点是：它没有用 Responses `input` items 作为抽象层，而是用 Anthropic Messages `messages` 加 `system` blocks。类似 Codex “contextual user fragment”的东西通常表现为 `isMeta` user message 加 `<system-reminder>`，而不是 `<environment_context>` 这种统一 fragment family。日期变化在 Codex 里可以是 partial `<environment_context>` diff；在 Claude Code 里是 `date_change` attachment 渲染出的 tail reminder。[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]] [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]

这也解释了为什么研究 Claude Code 时要分清两个问题：

1. **What is the request shape?** `system` / `messages` / `tools` / controls.
2. **What changes after the prefix is cached?** targeted attachments and volatile sections.

如果把 Claude Code 强行解释成 Codex-style ordered `input` stream，会丢掉它最重要的实现取向：prompt cache 稳定性优先，变化尽量走 tail delta，而不是重建 prefix。

## Validation Scenarios

Normal first turn: the evidence path covers `fetchSystemPromptParts()`, user input processing, `appendSystemContext()`, `prependUserContext()`, `normalizeMessagesForAPI()`, `buildSystemPromptBlocks()`, and final `anthropic.beta.messages.create()`.[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]

Date rollover: the evidence path covers memoized date/cache-stability comments, `getDateChangeAttachments()`, and attachment rendering into `<system-reminder>`.[[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]

Late MCP/tool/agent changes: the evidence path covers `mcp_instructions_delta`, `deferred_tools_delta`, `agent_listing_delta`, fallback system-prompt behavior, and rendering into meta user reminders.[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]

Cache reset boundaries: the evidence path covers `clearSystemPromptSections()`, post-compact cleanup, memory-file cache clearing, and resume/worktree state changes.[[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]

## Sources

- [[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]
- [[sources/claude-code-context-assembly-2026-04/source/source-code-evidence|source-code-evidence]]
- [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]
