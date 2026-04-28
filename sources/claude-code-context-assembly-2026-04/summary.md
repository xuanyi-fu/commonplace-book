---
type: summary
status: draft
created: 2026-04-24
updated: 2026-04-28
---

# claude-code-context-assembly-2026-04

This source collection records implementation-level evidence for how the local Claude Code source snapshot assembles model-visible context. The analyzed checkout is `/Users/bytedance/claude-code/claude-code` at commit `0a0498cf6a04d144aba289366a55b1edf328a797`. The main evidence is a line-cited map over the local TypeScript source; it should not be treated as official product documentation. [[source/source-code-evidence|source-code-evidence]]

## Structure

- `source/source-code-evidence.md`: normalized evidence map with file paths and line ranges from the local Claude Code checkout
- `summary.md`: source collection summary and usage guidance

## How To Use

- Use `source/source-code-evidence.md` first when checking a claim about request assembly, context bucket ordering, or state-change delta behavior.
- Re-check the local checkout before turning this into current-product claims, because the source snapshot is pinned to `0a0498cf6a04d144aba289366a55b1edf328a797`.
- Use [[sources/claude-code-frc-2026-04/summary|claude-code-frc-2026-04]] as the focused supplement when the question is how `microcompact` relates to old `tool_result` clearing, `cache_reference`, `cache_edits`, and public Anthropic context editing.
- Use this alongside [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]] only as a comparison frame; the Claude Code evidence does not use Codex's Responses `input` stream terminology.

## Summary

The normal Claude Code turn path starts with `fetchSystemPromptParts()`, which fetches `systemPrompt`, `userContext`, and `systemContext` as the API cache-key prefix pieces; `QueryEngine.submitMessage()` then builds the final `systemPrompt`, processes the user input, and appends produced messages/attachments to the conversation state. `/Users/bytedance/claude-code/claude-code/src/utils/queryContext.ts:30-73` `/Users/bytedance/claude-code/claude-code/src/QueryEngine.ts:286-325` `/Users/bytedance/claude-code/claude-code/src/QueryEngine.ts:410-434`

Before the model call, `query()` applies pre-API context transforms, appends `systemContext` into the system prompt, and calls the model with `messages: prependUserContext(messagesForQuery, userContext)`, the full system prompt, tools, thinking config, and request options. `/Users/bytedance/claude-code/claude-code/src/query.ts:430-451` `/Users/bytedance/claude-code/claude-code/src/query.ts:659-675`

At the Anthropic API boundary, Claude Code normalizes messages through `normalizeMessagesForAPI()`, adds attribution and CLI prompt prefix to the system prompt, builds prompt-cache-aware `system` blocks, constructs request fields including `model`, `messages`, `system`, `tools`, `max_tokens`, `thinking`, and optional `context_management`, then sends `anthropic.beta.messages.create({ ...params, stream: true })`. `/Users/bytedance/claude-code/claude-code/src/services/api/claude.ts:1260-1379` `/Users/bytedance/claude-code/claude-code/src/services/api/claude.ts:1699-1728` `/Users/bytedance/claude-code/claude-code/src/services/api/claude.ts:1797-1832`

The major context buckets are separate until late assembly: `systemPrompt` comes from `getSystemPrompt()` and registry-managed prompt sections; `systemContext` is memoized separately and appended into the system prompt; `userContext` is memoized separately and prepended as an `isMeta` user message wrapped in `<system-reminder>`; user input and attachments are collected through `processUserInput()` and normalized later; tool schemas are generated separately by `toolToAPISchema()`. `/Users/bytedance/claude-code/claude-code/src/constants/prompts.ts:444-577` `/Users/bytedance/claude-code/claude-code/src/context.ts:113-189` `/Users/bytedance/claude-code/claude-code/src/utils/api.ts:437-474` `/Users/bytedance/claude-code/claude-code/src/utils/processUserInput/processUserInput.ts:495-514` `/Users/bytedance/claude-code/claude-code/src/utils/api.ts:119-266`

The code-backed ordering model is: final `system` blocks are built from attribution, CLI prefix, `systemPrompt`, appended `systemContext`, and prompt-cache splitting; `messages` starts from the conversation after compaction/collapse/microcompact transforms, with `userContext` prepended as a meta user reminder, then normalized before API send. For the old `tool_result` clearing branch inside this area, use the focused FRC collection. `/Users/bytedance/claude-code/claude-code/src/query.ts:449-451` `/Users/bytedance/claude-code/claude-code/src/query.ts:659-661` `/Users/bytedance/claude-code/claude-code/src/utils/api.ts:321-435` `/Users/bytedance/claude-code/claude-code/src/services/api/claude.ts:1265-1379` [[sources/claude-code-frc-2026-04/summary|claude-code-frc-2026-04]]

State-change handling is domain-specific rather than one proved generic state-diff pass in the inspected path. The confirmed date path memoizes the date for prompt-cache stability, intentionally leaves the original prefix stale after midnight, emits a `date_change` tail attachment, and renders it as a meta user `<system-reminder>`. `/Users/bytedance/claude-code/claude-code/src/constants/common.ts:17-24` `/Users/bytedance/claude-code/claude-code/src/utils/attachments.ts:1402-1444` `/Users/bytedance/claude-code/claude-code/src/utils/messages.ts:4162-4169`

Other confirmed state-change paths are also specialized attachments: `deferred_tools_delta` reconstructs prior announcements from old attachments and diffs the current deferred-tool pool; `agent_listing_delta` reconstructs prior agent announcements and diffs current filtered agent types; `mcp_instructions_delta` diffs connected instruction-bearing MCP servers against prior announcements and falls back to a volatile system prompt section when the delta path is off. `/Users/bytedance/claude-code/claude-code/src/utils/toolSearch.ts:624-705` `/Users/bytedance/claude-code/claude-code/src/utils/attachments.ts:1454-1556` `/Users/bytedance/claude-code/claude-code/src/utils/mcpInstructionsDelta.ts:29-130` `/Users/bytedance/claude-code/claude-code/src/constants/prompts.ts:508-520`

Those attachment deltas become model-visible user-role context through the attachment rendering path: computed attachments are yielded as `AttachmentMessage`; later `date_change`, `deferred_tools_delta`, `agent_listing_delta`, and `mcp_instructions_delta` each render into `isMeta` user messages wrapped in `<system-reminder>`. `/Users/bytedance/claude-code/claude-code/src/utils/attachments.ts:2940-2970` `/Users/bytedance/claude-code/claude-code/src/utils/messages.ts:3097-3134` `/Users/bytedance/claude-code/claude-code/src/utils/messages.ts:4162-4230`

Prompt-cache stability is an explicit implementation concern: normal system prompt sections are cached until `/clear` or `/compact`, volatile sections are marked with `DANGEROUS_uncachedSystemPromptSection()`, deferred-tool and MCP-instruction fallback paths are described as cache-busting, and compaction/resume/worktree-change paths clear relevant context caches. `/Users/bytedance/claude-code/claude-code/src/constants/systemPromptSections.ts:16-68` `/Users/bytedance/claude-code/claude-code/src/services/api/claude.ts:1327-1355` `/Users/bytedance/claude-code/claude-code/src/services/compact/postCompactCleanup.ts:51-76` `/Users/bytedance/claude-code/claude-code/src/utils/sessionRestore.ts:360-389`

The `/context` and prompt-dump code are validation surfaces, not primary behavior definitions: `/context` says it mirrors query pre-API transforms for token accounting, while `createDumpPromptsFetch()` is debug tooling for recording request/response snapshots. `/Users/bytedance/claude-code/claude-code/src/commands/context/context-noninteractive.ts:16-69` `/Users/bytedance/claude-code/claude-code/src/services/api/dumpPrompts.ts:146-220`

## Sources

- [[source/source-code-evidence|source-code-evidence.md]]
- Related focused supplement: [[sources/claude-code-frc-2026-04/summary|claude-code-frc-2026-04]]
- Local checkout: `/Users/bytedance/claude-code/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797`
- Supporting comparison: [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- Supporting comparison: [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]
