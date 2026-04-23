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
  - semantic position: under `# Harness design for long-running application development`, before `## Why naive implementations fall short`
  - next unread source span: opening framing block from the tagline through the three introductory paragraphs ending with the three-agent architecture result
  - next boundary: `## Why naive implementations fall short`
  - completed spans: none
- Scout status: background subagents not started in this turn; candidate concept/entity and related-page lists will be maintained locally in this note.

## Recall Log

No spans reviewed yet.

## Questions And Answers

No questions recorded yet.

## Reader Comments

No reader comments recorded yet.

## Candidate Concepts Entities

- `harness design`: central to the article's argument; existing page likely exists at [[concepts/agent-harness|agent-harness]]; confidence: medium
- `generator/evaluator loop`: reusable pattern for separating production from judgment in agentic workflows; existing page unknown; confidence: medium
- `context reset`: recurring mechanism in long-running agent work; existing page unknown; confidence: medium
- `sprint contract`: article-specific but potentially reusable harness artifact boundary; existing page unknown; confidence: low
- `file-based handoff`: reusable coordination pattern across long-running agents; existing page unknown; confidence: medium

## Candidate Related Pages

- [[concepts/agent-harness|agent-harness]]: supports; this article appears to give a concrete Anthropic case study for harness components around long-running coding; confidence: medium
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]: extends; this source collection can add a later Anthropic engineering example to the broader harness-origin trail; confidence: medium
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]: extends; the article's later simplification discussion may stress-test which harness components should stay load-bearing; confidence: low

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
