---
type: summary
status: draft
created: 2026-04-25
updated: 2026-04-25
---

# claude-code-advisor-strategy-context-2026-04

这个 source collection 收录一份 2026-04-25 的本地 Claude Code code-reading 文档，主题是 `advisor strategy` 如何进入 Anthropic Messages API 的 model-visible context：`system` 策略指令、`tools` server tool schema、`betas`、以及 `messages[]` 里的 `server_tool_use` / `advisor_tool_result` 历史块。[[source/advisor-strategy-context|advisor-strategy-context.md]]

## Structure

- `source/original-claude-code-advisor-strategy-context.md`: 原始本地 Markdown 快照，来自 `/Users/bytedance/claude-code/claude-code/claude-code-advisor-strategy-context.md`
- `source/advisor-strategy-context.md`: 规范化 Markdown derivative，保留原文结构，并把 Claude Code 源码脚注改成指向 `heshan.pro/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797` 的固定代码链接
- `summary.md`: 这个 collection 的导读、范围说明和与既有 `advisor strategy` 材料的连接

## How To Use

- 如果问题是“Anthropic 公开的 `advisor strategy` 到底是什么、和 `routing` / `cascading` / `shepherding` 有什么关系”，先读 [[sources/claude-advisor-strategy-2026-04/summary|claude-advisor-strategy-2026-04]]。
- 如果问题是“Claude Code 里这件事怎么进 request/context”，从 `source/advisor-strategy-context.md` 开始；它把公开 API 形态落实到 Claude Code 的 `system`、`tools`、`betas` 和 `messages[]` 四个位置。[[source/advisor-strategy-context|advisor-strategy-context.md]]
- 如果需要确认这份导入有没有改写原始 wording，对照 `source/original-claude-code-advisor-strategy-context.md`；规范化版只加 provenance note 并把本地源码脚注换成固定代码链接。
- 这份 source 是本地源码快照研究，不是 Anthropic 官方产品文档；把它用于当前实现判断前，应重新检查 `/Users/bytedance/claude-code/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797` 或更新后的 checkout。

## Summary

已有 [[sources/claude-advisor-strategy-2026-04/summary|claude-advisor-strategy-2026-04]] 把 `advisor strategy` 放在公开 API 与学术谱系里：它不是普通 prompt pattern，而是 Anthropic Platform 里一个 executor-led、hint-like、mid-generation 的 server-tool 机制。这个 collection 补上实现侧的连接点：Claude Code 不是把 advisor 当成本地 side channel，而是把它插进同一个 `/v1/messages` context surface。[[source/advisor-strategy-context|advisor-strategy-context.md]]

实现上，这份文档把 `advisor strategy` 拆成三个 model-visible 面：`system` 里追加 `ADVISOR_TOOL_INSTRUCTIONS`，这是策略；`tools` 里追加 `advisor_20260301` server tool schema，并通过 beta header 让 API 接受 advisor blocks，这是可用性；`messages[]` 里保留 `server_tool_use` 和 `advisor_tool_result`，这是后续 turn 能继续看到 advisor 建议的历史 context。[[source/advisor-strategy-context|advisor-strategy-context.md]]

它还指出两个边界条件：第一，Claude Code 会在没有 advisor beta header 时剥离 advisor blocks，也会清理中断 stream 留下的 orphaned server-side tool-use blocks；第二，advisor tool schema 和 system-side 策略都被放在较晚的 suffix 位置，以减少 `/advisor` 开关对 prompt cache 前缀的影响。[[source/advisor-strategy-context|advisor-strategy-context.md]]

## Sources

- [[source/advisor-strategy-context|advisor-strategy-context.md]]
- [[source/original-claude-code-advisor-strategy-context|original-claude-code-advisor-strategy-context.md]]
- Related public/API collection: [[sources/claude-advisor-strategy-2026-04/summary|claude-advisor-strategy-2026-04]]
