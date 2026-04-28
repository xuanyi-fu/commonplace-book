---
type: summary
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# claude-code-frc-2026-04

这个 source collection 保存一份 2026-04-25 的本地 Claude Code code-reading note，主题是 FRC / Function Result Clearing 以及 Claude Code、first-party cache-editing、Anthropic public context editing 三者在清理旧 `tool_result` 时的边界。它来自 standalone local Markdown，没有稳定网页、PDF 或 email 原件；原始快照保存在 `source/original-claude-code-frc.md`。[[source/claude-code-frc|claude-code-frc.md]]

## Structure

- `source/original-claude-code-frc.md`: 原始本地 Markdown 快照，来自 `/Users/bytedance/claude-code/claude-code/claude-code-frc.md`
- `source/claude-code-frc.md`: 规范化 Markdown derivative，保留原文结构，并把 Claude Code 源码脚注改成指向 `heshan.pro/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797` 的固定代码链接
- `summary.md`: 这个 collection 的导读、范围说明和用法说明

## How To Use

- 如果问题是 “FRC 在 Claude Code 里到底指什么”，从 `source/claude-code-frc.md` 开始；它把 model-facing instruction surface、client-side clearing、first-party cache-editing path 和 public Anthropic context editing 分开。[[source/claude-code-frc|claude-code-frc.md]]
- 如果需要确认导入没有改写原始 wording，对照 `source/original-claude-code-frc.md`；规范化版只加 provenance note，并把本地源码脚注换成固定代码链接。
- 这份 source 是本地源码快照研究，不是 Anthropic 官方产品文档；把它用于当前实现判断前，应重新检查 `/Users/bytedance/claude-code/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797` 或更新后的 checkout。
- 和 [[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]] 一起使用时，把本 collection 视为 `tool_result` clearing / cache-editing 的专项补充，而不是通用 request assembly 总览。

## Summary

这份 note 把 FRC 定义成 Claude Code 中准备、触发或委托清理旧 `tool_result` content 的 feature area；`frc` 和 `summarize_tool_results` 只是 system prompt 里的 model-facing guidance，不是清理机制本身。[[source/claude-code-frc|claude-code-frc.md]]

它区分三条机制：`time-based microcompact` 在 client side 直接把旧 `tool_result.content` 替换成 cleared placeholder；`cache-edit microcompact` / `cached microcompact` 走 first-party cache-editing path，在最终 `messages[]` 里通过 `cache_reference` 和 `cache_edits` 删除旧结果但保留本地 transcript；public `context editing (tool result clearing)` 走 Anthropic top-level `context_management.clear_tool_uses_20250919`。[[source/claude-code-frc|claude-code-frc.md]]

核心边界是 prompt cache tradeoff：time-based microcompact 假设 cache 已冷，所以直接缩短 outgoing messages；cached microcompact 的目标是删除 referenced tool results 同时不 invalidate warm cached prefix；public context editing 是 documented server-side path，但官方文档说明 clearing 会 invalidate affected cached prompt prefixes。[[source/claude-code-frc|claude-code-frc.md]]

证据边界也被明确拆开：Claude Code source snapshot 支持 FRC prompt sections、microcompact call sites、`cache_reference` / `cache_edits` request-local insertion、feature gating 和 API context-management request construction；Anthropic public docs 支持 `context_management` / `clear_tool_uses_20250919` 形态；三者被归纳成 parallel mechanisms 是 implementation inference。[[source/claude-code-frc|claude-code-frc.md]]

## Sources

- [[source/claude-code-frc|claude-code-frc.md]]
- [[source/original-claude-code-frc|original-claude-code-frc.md]]
