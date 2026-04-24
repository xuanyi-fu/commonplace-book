---
type: summary
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# kenhuang-harness-paradigm-claude-hermes-2026-04

这个 source collection 保存 Ken Huang 2026-04-18 的 Substack 文章 “Chapter 1: The Harness Paradigm (Claude Code vs. Hermes Agent)”，内容围绕 `harness` 如何把 raw language model 包装成可控、可审计、可中断、可预算约束的 production agent，并用 Claude Code 与 Hermes Agent 的实现风格做对比。[[source/chapter-1-the-harness-paradigm-claude-markdown]]

## Structure

- `source/chapter-1-the-harness-paradigm-claude-fullpage.png`: 登录后的整页 rendered screenshot，是这次 capture 里最接近原网页视觉状态的原始网页 artifact
- `source/chapter-1-the-harness-paradigm-claude-dom-snapshot.txt`: `browser-use` 从登录后页面取得的 browser-rendered DOM/accessibility snapshot
- `source/chapter-1-the-harness-paradigm-claude-text.txt`: `article` 容器的 rendered text capture，包含标题区与正文
- `source/chapter-1-the-harness-paradigm-claude-body-text.txt`: 正文 `.markup` 容器的 rendered text capture
- `source/chapter-1-the-harness-paradigm-claude-markdown.md`: best-effort Markdown derivative，保留文章标题顺序、段落、代码块和正文图片引用
- `source/chapter-1-the-harness-paradigm-claude-metadata.json`: capture 元数据，包括 URL、时间、登录态说明、限制和原始图片 URL
- `source/assets/chapter-1-the-harness-paradigm-claude/comparison-table.png`: 本地化的正文比较表图片
- `summary.md`: 这个 collection 的导读、结构说明和使用建议

## How To Use

- 先读 `source/chapter-1-the-harness-paradigm-claude-markdown.md`，它最适合顺序阅读、搜索和后续做 reading note。
- 需要核对原网页渲染状态、付费墙解锁后的页面上下文或图片位置时，看 `source/chapter-1-the-harness-paradigm-claude-fullpage.png`。
- 需要核对 `browser-use` 实际读取到的页面结构时，看 `source/chapter-1-the-harness-paradigm-claude-dom-snapshot.txt`。
- 需要最小噪音的正文文本时，看 `source/chapter-1-the-harness-paradigm-claude-body-text.txt`。
- 这篇文章是付费 Substack 页面；本次抓取需要用户已登录的 in-app browser。raw HTML 没有通过当前 `browser-use` API 取得，所以本 collection 用 rendered screenshot、DOM snapshot、text capture 和 Markdown derivative 作为替代 artifact。

## Summary

文章先把 `harness` 定义成包在 model 外面的控制层：model 提供 intelligence，harness 提供 control；这个控制层负责 typed tools、conversation state、permission system、failure handling 和 resource consumption tracking。[[source/chapter-1-the-harness-paradigm-claude-markdown]]

Claude Code 一侧，文章把 TypeScript `QueryEngine` 描述为 harness core：它持有 session mutable state、abort controller、permission denials 和 usage tracker，并通过 `submitMessage()` async generator 把 token、tool start、tool finish 等事件流式交给 UI 或下游消费者。[[source/chapter-1-the-harness-paradigm-claude-markdown]]

Hermes Agent 一侧，文章把 Python `AIAgent`、thread-safe `IterationBudget`、同步 `run_conversation()` loop 和 registry-based tool system 放在一起说明，重点对比它和 Claude Code 在 streaming、typed tool interface、runtime flexibility、platform routing 与 runaway-loop cap 上的取舍。[[source/chapter-1-the-harness-paradigm-claude-markdown]]

文章最后给出一个 defensive cyber agent 示例，把 Hermes 的 `IterationBudget`、Claude Code 的 async generator streaming 和 immutable audit log 组合起来，说明在有 destructive remediation action 的安全场景里，harness 应该让 model 决定想做什么，但由 harness 决定是否允许执行。[[source/chapter-1-the-harness-paradigm-claude-markdown]]

## Sources

- [[source/chapter-1-the-harness-paradigm-claude-fullpage|chapter-1-the-harness-paradigm-claude-fullpage.png]]
- [[source/chapter-1-the-harness-paradigm-claude-dom-snapshot|chapter-1-the-harness-paradigm-claude-dom-snapshot.txt]]
- [[source/chapter-1-the-harness-paradigm-claude-text|chapter-1-the-harness-paradigm-claude-text.txt]]
- [[source/chapter-1-the-harness-paradigm-claude-body-text|chapter-1-the-harness-paradigm-claude-body-text.txt]]
- [[source/chapter-1-the-harness-paradigm-claude-markdown|chapter-1-the-harness-paradigm-claude-markdown.md]]
- [[source/chapter-1-the-harness-paradigm-claude-metadata|chapter-1-the-harness-paradigm-claude-metadata.json]]
- [[source/assets/chapter-1-the-harness-paradigm-claude/comparison-table|comparison-table.png]]
