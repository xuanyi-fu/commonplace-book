---
type: note
status: draft
created: 2026-04-27
updated: 2026-04-27
---

# minimal-editing-2026-04-reading-note

## Source

- Source collection: [[sources/minimal-editing-2026-04/summary|minimal-editing-2026-04]]
- Primary reading file: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown|minimal-editing-markdown.md]]
- Discussion language: Chinese, with source terms such as `over-editing`, `minimal editing`, `brown-field`, `Pass@1`, `Levenshtein Distance`, `Cognitive Complexity`, `SFT`, `DPO`, and `RL` kept in English when translation would blur the argument.

## Core Question

这篇文章想回答的核心问题是：coding models 为什么会在 brown-field bug fix 中做出超过必要范围的 rewrite，以及能否通过 prompt 或 training 让模型学会更 faithful 的 minimal editing？[[sources/minimal-editing-2026-04/summary]]

## Reading State

- Source slug: `minimal-editing-2026-04`
- Primary reading file: `sources/minimal-editing-2026-04/source/minimal-editing-markdown.md`
- Semantic cursor:
  - file: `sources/minimal-editing-2026-04/source/minimal-editing-markdown.md`
  - semantic position: under `## Over-Editing`, before the brown-field framing paragraph
  - next unread source span: figure, caption, definition, and concrete GPT-5.4 example under `## Over-Editing`
  - next boundary: paragraph beginning `It helps to think about this in terms of the kind of work being done.`
  - completed spans: opening framing block under `# Coding Models Are Doing Too Much`
- Scout status: deferred; candidate concept/entity and related-page lists are kept locally in this note.

## Recall Log

### Opening Framing Block

- Source span label: `# Coding Models Are Doing Too Much` opening body, before `## Over-Editing`
- Quoted original span or citation: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^opening-over-editing-problem]]
- Guiding question: 作者为什么要引入 `Over-Editing`？它要解决什么问题？
- User recitation: 用户理解为：作者观察到最近的 coding agent 在完成任务时，倾向于用功能正确但改动量更大的方式完成修复；这对 code review 是一个不小的问题，因为需要 review 的改动变多，review 自然变麻烦。
- Calibrated understanding: 这个复述准确。需要补一层边界：作者不是在说模型没有修好 bug，而是在说模型即使功能正确，也可能把不相关代码一起 rewrite，导致 reviewer 需要重新理解更多变化并判断这些变化是否安全。这里的伤害主要落在 brown-field code review 和 change safety 上，而不是测试正确性本身。
- Missing points: 后文会把这个现象形式化为 `functionally correct but structurally diverges from the original code more than the minimal fix requires`。
- Open questions: 作者会如何把“改太多”变成可测指标，以及 prompt 或 training 是否能稳定减少这种行为。

## Questions And Answers

## Reader Comments

## Candidate Concepts Entities

- `over-editing`: central term for the article's target failure mode; likely reusable beyond this source; no page checked yet; confidence high.

## Candidate Related Pages

- None yet.

## Sources

- [[sources/minimal-editing-2026-04/summary|minimal-editing-2026-04]]
- [[sources/minimal-editing-2026-04/source/minimal-editing-markdown|minimal-editing-markdown.md]]
