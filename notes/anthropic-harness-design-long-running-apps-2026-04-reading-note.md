---
type: note
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# anthropic-harness-design-long-running-apps-2026-04-reading-note

## Source

- Source collection: [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- Primary reading file: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown|harness-design-long-running-apps-markdown.md]]
- Discussion language: Chinese, with implementation terms such as `harness`, `agent`, `context reset`, `compaction`, `planner`, `generator`, and `evaluator` kept in English when translation would blur system structure.

## Core Question

Anthropic 这篇文章想回答的核心问题是：在 frontier agentic coding 里，哪些 `harness` 设计组件真正能让模型完成更长、更复杂的 frontend 与 full-stack application development，又该如何随着模型能力变化删减这些组件？[[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]

## Reading State

- Source slug: `anthropic-harness-design-long-running-apps-2026-04`
- Primary reading file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
- Semantic cursor:
  - file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
  - semantic position: under `## Why naive implementations fall short`, before the section setup that starts from the earlier long-running harness experiment
  - next unread source span: section setup explaining that earlier decomposition and handoff approaches helped but still left persistent long-task failure modes
  - next boundary: the first detailed failure mode beginning with context-window coherence and `context anxiety`
  - completed spans: opening framing block under `# Harness design for long-running application development`
- Scout status: background subagents not started in this turn; candidate concept/entity and related-page lists will be maintained locally in this note.

## Recall Log

### Opening Framing Block

- Source span label: `# Harness design for long-running application development` opening body, before `## Why naive implementations fall short`
- Quoted original span or citation: opening body in [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]], especially the passages on generator/evaluator design and the later three-agent architecture. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- Guiding question: 作者为什么要引入 `generator/evaluator` multi-agent structure？它要解决什么问题？
- User recitation: 用户理解为：作者想完成一个能 long-running 的 full-stack development 任务，所以先设计了 `generator + evaluator` 架构；`evaluator` 必须有明确、可靠、不 flaky 的评分系统，不能只问 "is this design good"；作者还把之前 harness 研究的两个经验带过来，即把大任务拆成可治理的小任务，以及让 `agent` 之间靠 `structured artifacts` 交换 `context`。
- Calibrated understanding: 这个复述抓住了主线。需要补一层范围校正：开头不是直接只从 full-stack coding 出发，而是从两个相连问题出发，即 frontend design 的主观质量问题和 long-running autonomous software engineering 的完整应用构建问题。`generator/evaluator` 最初解决的是“主观质量如何变成可评分、可迭代的反馈”；随后作者把同一分工模式迁移到 long-running coding，并结合任务分解与结构化 handoff，形成 `planner / generator / evaluator` 架构。
- Missing points: 注意后续阅读中的四个锚点：A criteria 怎样把主观判断变成明确评分；B evaluator 如何被校准到稳定可靠；C 大任务如何被拆成可治理的小任务或 sprint；D `structured artifacts` 如何在 `agent` 之间传递 `context`。
- Open questions: 后文是否能说明 A/B 是通过 prompt wording、few-shot calibration、Playwright interaction 还是 hard threshold 机制实现；C/D 是否最终是 load-bearing 组件，还是会随着 Opus 4.6 能力增强被删减。

## Questions And Answers

No questions recorded yet.

## Reader Comments

- 用户提出后续阅读应跟踪四个实现锚点：A 明确评分系统，B 可靠不 flaky 的 evaluator，C 大任务拆成可治理小任务，D 通过 `structured artifacts` 在 `agent` 之间交换 `context`。支撑段落见 opening framing block 中关于 generator/evaluator、criteria、decomposition、structured artifacts 和 three-agent architecture 的说明。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]

## Candidate Concepts Entities

- `harness design`: central to the article's argument; existing page likely exists at [[concepts/agent-harness|agent-harness]]; confidence: medium
- `generator/evaluator loop`: reusable pattern for separating production from judgment in agentic workflows; existing page unknown; confidence: medium
- `context reset`: recurring mechanism in long-running agent work; existing page unknown; confidence: medium
- `planner / generator / evaluator architecture`: reusable long-running coding harness shape; existing page unknown; confidence: medium
- `evaluator calibration`: reusable problem around making LLM-based QA skeptical, stable, and aligned with target criteria; existing page unknown; confidence: medium
- `sprint contract`: article-specific but potentially reusable harness artifact boundary; existing page unknown; confidence: low
- `file-based handoff`: reusable coordination pattern across long-running agents; existing page unknown; confidence: medium

## Candidate Related Pages

- [[concepts/agent-harness|agent-harness]]: supports; this article appears to give a concrete Anthropic case study for harness components around long-running coding; confidence: medium
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]: extends; this source collection can add a later Anthropic engineering example to the broader harness-origin trail; confidence: medium
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]: extends; the article's later simplification discussion may stress-test which harness components should stay load-bearing; confidence: low

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
