---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# windsurf-position-2026-04

这个 source collection 收集了截至 2026-04-21 用来判断 Windsurf 市场位置的直接材料。它不试图全面覆盖 Windsurf 的所有产品能力，而是聚焦两个问题：Windsurf 官方如何描述自己的规模，以及公开 survey 信号里它大概处在什么位置。

## Structure

- `source/official-windsurf-editor-page.md`: Windsurf 官网编辑器页面里关于 active users 和产品定位的公开表述
- `source/sonarsource-state-of-code-developer-survey-2026.md`: SonarSource 2026 开发者调查里与 Windsurf 使用率相关的摘录
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/official-windsurf-editor-page.md`，看 Windsurf 官方自己公开主张的规模信号
- 再读 `source/sonarsource-state-of-code-developer-survey-2026.md`，把官网自述和第三方 survey 代理指标放在一起看
- 讨论“市场占有率”时，优先把它理解成公开可见的代理指标，而不是精确份额

## Summary

截至 2026-04-21，Windsurf 至少不是边缘产品。官网宣称 `1M+ active users`，说明它已经有相当规模；但 SonarSource 的 2026 survey 里，Windsurf 在“过去一年用于软件开发任务的 AI 工具”这一口径下只有 `8%`，明显低于 Copilot、ChatGPT、Claude / Claude Code、Cursor 等第一梯队工具。所以更稳妥的判断是：Windsurf 不是头部，但也不是没人用，它更像 AI coding 工具里的第二梯队或腰部玩家。

## Sources

- [[source/official-windsurf-editor-page|official-windsurf-editor-page.md]]
- [[source/sonarsource-state-of-code-developer-survey-2026|sonarsource-state-of-code-developer-survey-2026.md]]
