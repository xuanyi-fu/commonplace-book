---
type: summary
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# claude-code-auto-memory-2026-04

这个 source collection 收录一份 2026-04-27 的本地 Claude Code code-reading 文档，主题是 Claude Code `AutoMem` 的 storage、write path、read path、`extractMemories`、`autoDream` 和 relevant-memory recall。它来自 `/Users/bytedance/claude-code/claude-code/claude-code-auto-memory.md`，对应本地 checkout `0a0498cf6a04d144aba289366a55b1edf328a797`，不是 Anthropic 官方产品文档。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]

## Structure

- `source/original-claude-code-auto-memory.md`: 原始本地 Markdown 快照，来自 `/Users/bytedance/claude-code/claude-code/claude-code-auto-memory.md`
- `source/claude-code-auto-memory.md`: 规范化 Markdown derivative，保留原文结构，并把 Claude Code 源码脚注改成指向 `heshan.pro/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797` 的固定代码链接
- `summary.md`: 这个 collection 的导读、范围说明和与既有 Codex / Claude Code memory-context 材料的连接

## How To Use

- 如果问题是“Claude Code AutoMem 怎么存、怎么写、怎么进 context”，先读 `source/claude-code-auto-memory.md`；它把 default flow 和 experimental flows 分开，并把 `MEMORY.md` index、topic files、`extractMemories`、`autoDream`、relevant-memory recall 放到同一张实现图里。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]
- 如果需要确认这份导入有没有改写原始 wording，对照 `source/original-claude-code-auto-memory.md`；规范化版只加 provenance note 并把本地源码脚注换成固定代码链接。
- 如果问题是“Codex memory 和 Claude Code AutoMem 有什么结构差异”，把它和 [[sources/codex-memory-implementation-2026-04/summary|codex-memory-implementation-2026-04]] 一起读；前者是 Claude Code filesystem-based topic memory，后者是 Codex 的 staged extraction / consolidation pipeline。
- 如果问题是“这些 memory 内容在 Anthropic Messages request 里怎么出现”，同时参考 [[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]，因为 AutoMem 默认 consumption 走 `userContext` / `<system-reminder>` 这条 messages-side context path。
- 这份 source 是本地源码快照研究；把它用于当前 Claude Code 产品判断前，应重新检查 `/Users/bytedance/claude-code/claude-code` 或更新后的 checkout。

## Summary

这份文档把 Claude Code `AutoMem` 描述为 project-scoped、filesystem-based 的 memory system：实际 durable memory 存在 topic Markdown files 里，`MEMORY.md` 是 compact index，而 topic type 被约束为 `user`、`feedback`、`project`、`reference`。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]

写入侧分成 default 和 experimental：default path 是 main agent 通过 system prompt 学会在用户明确 remember / forget 时用普通 file tools 改 topic files 和 `MEMORY.md`；`extractMemories` 是 turn-end catch-up fork，跳过 main agent 已经写 memory 的 turn；`autoDream` 是后台 consolidation pass，用近期 transcripts 和已有 memory files 做去重、删旧、合并和 index 维护。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]

读取侧也分成 default 和 experimental：default path 不是把所有 topic files 塞进 context，而是把 `MEMORY.md` entrypoint 作为 `claudeMd` / `userContext`，最后以 user-role `<system-reminder>` 进入 `messages[]`；`tengu_moth_copse` 相关的 experimental recall 会跳过默认 index injection，改成每个 user turn 启动 relevant-memory prefetch，选中 topic files 后再作为 `relevant_memories` attachment 注入。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]

它还明确了 evidence boundary：这些结论来自 code-observed behavior 和少量 architectural inference，不应该直接等同于 Anthropic 官方 API schema 或当前产品承诺。[[source/claude-code-auto-memory|claude-code-auto-memory.md]]

## Sources

- [[source/claude-code-auto-memory|claude-code-auto-memory.md]]
- [[source/original-claude-code-auto-memory|original-claude-code-auto-memory.md]]
- Related Codex implementation collection: [[sources/codex-memory-implementation-2026-04/summary|codex-memory-implementation-2026-04]]
- Related Claude Code context collection: [[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]]
