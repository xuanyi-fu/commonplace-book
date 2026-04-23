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
  - semantic position: under `## Why naive implementations fall short`, before the first detailed failure mode beginning with context-window coherence and `context anxiety`
  - next unread source span: first failure mode: context-window coherence loss, `context anxiety`, `context reset`, and the distinction from `compaction`
  - next boundary: the second detailed failure mode beginning with self-evaluation
  - completed spans: opening framing block under `# Harness design for long-running application development`; `Why naive implementations fall short` setup span
- Scout status: concept/entity scout and related-pages scout completed after the opening span; candidate lists refreshed in this note.

## Recall Log

### Opening Framing Block

- Source span label: `# Harness design for long-running application development` opening body, before `## Why naive implementations fall short`
- Quoted original span or citation: opening body in [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]], especially the passages on generator/evaluator design and the later three-agent architecture. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- Guiding question: 作者为什么要引入 `generator/evaluator` multi-agent structure？它要解决什么问题？
- User recitation: 用户理解为：作者想完成一个能 long-running 的 full-stack development 任务，所以先设计了 `generator + evaluator` 架构；`evaluator` 必须有明确、可靠、不 flaky 的评分系统，不能只问 "is this design good"；作者还把之前 harness 研究的两个经验带过来，即把大任务拆成可治理的小任务，以及让 `agent` 之间靠 `structured artifacts` 交换 `context`。
- Calibrated understanding: 这个复述抓住了主线。需要补一层范围校正：开头不是直接只从 full-stack coding 出发，而是从两个相连问题出发，即 frontend design 的主观质量问题和 long-running autonomous software engineering 的完整应用构建问题。`generator/evaluator` 最初解决的是“主观质量如何变成可评分、可迭代的反馈”；随后作者把同一分工模式迁移到 long-running coding，并结合任务分解与结构化 handoff，形成 `planner / generator / evaluator` 架构。
- Missing points: 注意后续阅读中的四个锚点：A criteria 怎样把主观判断变成明确评分；B evaluator 如何被校准到稳定可靠；C 大任务如何被拆成可治理的小任务或 sprint；D `structured artifacts` 如何在 `agent` 之间传递 `context`。
- Open questions: 后文是否能说明 A/B 是通过 prompt wording、few-shot calibration、Playwright interaction 还是 hard threshold 机制实现；C/D 是否最终是 load-bearing 组件，还是会随着 Opus 4.6 能力增强被删减。

### Why Naive Implementations Fall Short Setup

- Source span label: `## Why naive implementations fall short` opening setup, before the first detailed failure mode
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^persistent-long-task-failure-modes]]
- Guiding question: earlier decomposition/handoff harness 的边界或失败模式是什么？
- User recitation: 用户理解为：之前的 harness 做法是把大任务拆成多个小 task，让 `agent` 一个个实现；每个 `agent` 完成后把 handoff artifacts 交给下一个 `agent`，后者用这些 artifacts 影响自己的 `context`。但作者这一段还没有具体解释复杂任务中怎么失败，只是说时间一长 `agent` 会 `go off the rails`，具体表现会在接下来的两个 failure modes 里展开。
- Calibrated understanding: 这个复述准确。这段的论证位置是承认旧 harness 有效：它解决了任务组织、feature-by-feature 实现、以及跨 session 的 `context` handoff。但它同时指出这些机制还没有解决更长复杂任务里 `agent` 随时间失稳的问题。这里的 `go off the rails` 还只是总括，不是机制解释；机制解释就是后面两个 failure modes。
- Missing points: 注意这里没有否定 decomposition 和 handoff artifacts；作者是在说它们是必要但不充分的 scaffold。
- Open questions: 接下来两个 failure modes 是否分别对应 `context` 管理问题和 judgment/evaluation 问题；它们会怎样映射回用户标记的 C/D 与 A/B 四个锚点。

## Questions And Answers

No questions recorded yet.

## Reader Comments

- 用户提出后续阅读应跟踪四个实现锚点：A 明确评分系统，B 可靠不 flaky 的 evaluator，C 大任务拆成可治理小任务，D 通过 `structured artifacts` 在 `agent` 之间交换 `context`。支撑段落见 opening framing block 中关于 generator/evaluator、criteria、decomposition、structured artifacts 和 three-agent architecture 的说明。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]

## Candidate Concepts Entities

- `harness design`: central concept for the article's claim that surrounding orchestration can materially change frontier agentic coding performance; existing page likely exists at [[concepts/agent-harness|agent-harness]]; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `generator/evaluator loop`: reusable pattern for separating production from judgment in agentic workflows, first introduced here through the GAN-inspired frontend design setup; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]]
- `context reset`: recurring mechanism in long-running agent work where the context window is cleared and a fresh agent resumes from a structured handoff; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `compaction`: contrasting mechanism where earlier conversation is summarized in place so the same agent can continue on shortened history; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `context anxiety`: named failure mode where an agent starts wrapping up prematurely as it approaches its perceived context limit; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `structured handoff`: load-bearing artifact pattern for carrying prior state and next steps across context resets or agent sessions; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `self-evaluation bias`: failure mode where agents praise their own mediocre work, especially when quality is subjective and lacks binary tests; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `external evaluator`: reusable harness role that judges a generator's work separately from the agent that produced it, making skeptical evaluation easier to tune; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `planner / generator / evaluator architecture`: reusable long-running coding harness shape for turning a prompt into a spec, implementing feature chunks, and testing/evaluating the result; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- `evaluator calibration`: reusable problem around making LLM-based QA skeptical, stable, and aligned with target criteria; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `sprint contract`: article-specific but potentially reusable harness artifact boundary for agreeing on what a feature chunk means before implementation; existing page unknown; confidence: low. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^sprint-contract]]
- `file-based handoff`: reusable coordination pattern where agents communicate through files rather than shared conversational state; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^file-based-agent-communication]]

## Candidate Related Pages

- [[concepts/agent-harness|agent-harness]]: supports; this article is a concrete Anthropic case study for the same layer defined there: model-external infrastructure that manages long-running tasks through planning, tool use, context strategy, handoff artifacts, and evaluation rather than treating the model alone as the whole agent system; confidence: high
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]: extends; the Anthropic article adds a later 2026 engineering example to the broader origin trail, moving from general `agent harness` / `context engineering` framing into a specific long-running application-development harness with planner, generator, evaluator, context reset, and file-based handoff components; confidence: high
- [[syntheses/components-of-a-coding-agent-layer-mismatch-and-state-resumption|components-of-a-coding-agent-layer-mismatch-and-state-resumption]]: supports; the current `Why naive implementations fall short` section gives a concrete mechanism for that synthesis's state-resumption claim: compaction and transcript continuity are not always enough, while context resets require a durable handoff artifact carrying state and next steps; confidence: high
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]: extends; the article's later simplification discussion stress-tests the same design principle by asking which planner, sprint, evaluator, context-reset, and handoff components remain load-bearing as model capability improves; confidence: medium

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
