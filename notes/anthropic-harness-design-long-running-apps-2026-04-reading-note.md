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
- Discussion language: Chinese, while preserving core implementation terms such as `harness`, `generator`, `evaluator`, `planner`, `context reset`, `compaction`, `sprint contract`, and `agent`.

## Core Question

这篇 source 的核心问题是：在 frontier agentic coding 里，哪些 `harness` 设计组件真正能提升长时应用开发质量，哪些只是随模型能力变化而需要被重新评估或删减的 scaffold？[[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]

## Reading State

- Source slug: `anthropic-harness-design-long-running-apps-2026-04`
- Primary reading file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
- Semantic cursor:
  - file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
  - semantic position: under `# Harness design for long-running application development`, before `## Why naive implementations fall short`
  - next unread source span: opening dek and author attribution
  - next boundary: `## Why naive implementations fall short`
  - completed spans: none
- Scout status: no background subagents used in this turn; candidate lists will be maintained locally in this note at review boundaries.

## Recall Log

No spans completed yet.

## Questions And Answers

No questions recorded yet.

## Reader Comments

No reader comments recorded yet.

## Candidate Concepts Entities

- `agent-harness`
  - why it matters: central existing concept for model-wrapping infrastructure and long-running agent execution
  - existing page? yes, [[concepts/agent-harness]]
  - confidence: high
- `context reset`
  - why it matters: article treats it as a specific long-running harness mechanism distinct from `compaction`
  - existing page? not checked
  - confidence: medium
- `evaluator`
  - why it matters: article uses evaluator agents as the load-bearing boundary between generation and judgment
  - existing page? not checked
  - confidence: medium

## Candidate Related Pages

- [[concepts/agent-harness]]
  - relation: extends
  - rationale: this source provides Anthropic engineering evidence about which harness components matter for long-running coding tasks
  - confidence: high
- [[syntheses/components-of-a-coding-agent-layer-mismatch-and-state-resumption]]
  - relation: extends
  - rationale: this source adds an Anthropic experiment-driven view of harness/runtime components and model-boundary-dependent scaffolding
  - confidence: medium

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
