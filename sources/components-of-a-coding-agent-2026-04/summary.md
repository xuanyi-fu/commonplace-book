---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# components-of-a-coding-agent-2026-04

这个 source collection 收集了 Sebastian Raschka 于 2026-04-04 发布在 `Ahead of AI` 的文章 “Components of A Coding Agent” 的原始 Substack 网页和一个 best-effort markdown derivative。它主要用于保存作者对 coding agent / coding harness 组成部分的原始论述，便于后续做 source-backed 阅读、引用和概念拆分。

## Structure

- `source/components-of-a-coding-agent.html`: 从 Substack 抓取的原始网页 HTML；这是 authoritative source
- `source/components-of-a-coding-agent-markdown.md`: 从页面内嵌 `body_html` 提取并规范化得到的 markdown derivative，便于阅读、搜索和引用
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/components-of-a-coding-agent-markdown.md`，按原文顺序阅读文章正文、图注和代码块
- 需要核对页面原貌、图片链接、原始 HTML 结构或抓取局限时，回到 `source/components-of-a-coding-agent.html`
- 这个 collection 主要适合回答 coding agent / coding harness 包含哪些核心组件，以及 `repo context`、`prompt` cache、structured tools、context reduction、memory、subagents 之间如何分层
- 这次抓取不需要登录、滚动解锁或额外浏览器交互；原始 HTML 可以直接拿到正文，markdown derivative 基于页面内嵌 `body_html` 生成

## Summary

这篇文章把 `Claude Code`、`Codex CLI` 这类工具解释为“用 application layer 包住 LLM 的 coding harness”，核心不只是模型本身，而是围绕模型组织出来的上下文、工具、状态和控制流。作者把 coding agent 的主干拆成 6 个部分：live `repo context`、prompt shape and cache reuse、structured tools / validation / permissions、context reduction、structured session memory，以及 delegation and bounded subagents。对这个仓库后续如果要写概念页或综合页，这个 collection 更适合作为“原始论述入口”，先保留作者原话和图，再在别处做中文解释或实现层比较。

## Sources

- [[source/components-of-a-coding-agent|components-of-a-coding-agent.html]]
- [[source/components-of-a-coding-agent-markdown|components-of-a-coding-agent-markdown.md]]
