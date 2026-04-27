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
  - semantic position: under `## Does Prompting Help?`, before `## Does Reasoning Mean Overthinking and Over-Editing?`
  - next unread source span: explicit minimal-edit prompt experiment under `## Does Prompting Help?`
  - next boundary: `## Does Reasoning Mean Overthinking and Over-Editing?`
  - completed spans: opening framing block under `# Coding Models Are Doing Too Much`; `Over-Editing` definition and GPT-5.4 example; brown-field framing and tests-do-not-catch-it argument; compressed `## Measuring Over-Editing` chapter; `## Do Models Over-Edit?` model comparison results
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

### Over-Editing Definition And Example

- Source span label: `## Over-Editing` figure, caption, definition, and GPT-5.4 example, before the brown-field framing paragraph
- Quoted original span or citation: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^over-editing-definition]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^gpt54-over-editing-example]]
- Guiding question: `Over-editing` 在这里具体指什么？
- User recitation: 用户理解为：作者在这里明确定义了 `over-editing`，也就是功能正确但是结构性偏离太大的改动。例子中本来只改一行就能完成的事，GPT 却做了一些看起来能让代码更 reliable、但和这次 bug fix 不相干的事情；这些事情会成为 brown-field 的风险。
- Calibrated understanding: 这个复述准确。这里的判定标准是双重的：输出必须先是 functionally correct，然后才讨论它是否比 minimal fix 更大幅度地偏离原代码。GPT-5.4 的例子典型，是因为它把一个 off-by-one 单行修复扩展成整段函数 rewrite；这些新增检查和转换即使看似更稳健，也不是当前 bug fix 的必要条件。
- Missing points: 后文会进一步说明为什么这种风险在 brown-field codebase 中更严重，以及为什么 tests pass 不足以发现它。
- Open questions: 接下来需要看作者如何把 brown-field 的 review 风险和测试不可见性连接起来。

### Brown-Field Failure And Tests Limitation

- Source span label: final paragraphs under `## Over-Editing`, before `## Measuring Over-Editing`
- Quoted original span or citation: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^greenfield-brownfield-distinction]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^tests-miss-over-editing]]
- Guiding question: `green-field` 和 `brown-field` 有什么关键区别？为什么这个区别对 `Over-editing` 重要？
- User recitation: 用户理解为：test 只能检测正确性。作者想说的是，需要一个 metric 来衡量结构偏离。
- Calibrated understanding: 这个复述抓住了通往下一节的重点：如果 tests 只能确认功能正确，就需要额外度量来衡量模型到底改了多少、偏离了多少。需要补一层当前 span 的论证位置：作者先把 `over-editing` 定位成 `brown-field failure`，因为已有 codebase 的代码已经被团队理解并有意写成现在的样子；模型的职责是 fix the issue and nothing else。它不是 tests 能直接解决的 correctness failure，而是 review 面积、maintainability、change safety 和 codebase quality 层面的失败。
- Missing points: 下一节会把这个直觉落到 dataset 和 metrics 上，而不是只停留在工程原则。
- Open questions: 作者会选择哪些指标来近似“结构偏离”，以及这些指标是否真的对应 reviewer 感受到的 review burden。

### Measuring Over-Editing

- Source span label: compressed `## Measuring Over-Editing` chapter through the end of `### Metrics`
- Quoted original span or citation: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^measurement-dataset-construction]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^pass1-not-sufficient]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^token-levenshtein-relative-patch]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^added-cognitive-complexity-metric]]
- Guiding question: 作者是怎么把 `over-editing` 变成可测问题的？
- User recitation: 用户理解为：作者直接构建了一个数据集，把已有 benchmark 里的运算符、boolean 等弄坏；除了 `Pass@1` 之外，还增加两个新的 metrics，一个是 Python token edit distance，一个是 `Cognitive Complexity`，后者是 `Cyclomatic Complexity` 的改进版本。
- Calibrated understanding: 这个复述准确。更完整地说，作者通过 programmatic corruption 让每个样本的 ground truth minimal edit 变得明确：把 corruption 反转即可。`Pass@1` 只检查模型是否修对 bug；`Token-level Levenshtein Distance` 近似衡量模型相对 minimal patch 多改了多少 token；`Added Cognitive Complexity` 近似衡量模型是否引入了额外理解负担。因为 corruptions 只改 value 而不改 structure，faithful fix 理论上不应增加 complexity。
- Missing points: 这些 metrics 是 proxy，不是 review burden 本身；它们会偏向“局部、小改动”的定义。
- Open questions: 这个 synthetic simple-bugfix benchmark 能否代表更一般的 coding-agent 工作，仍然需要后续证据支持。

### Do Models Over-Edit

- Source span label: `## Do Models Over-Edit?` table and immediate interpretation, before `## Does Prompting Help?`
- Quoted original span or citation: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^model-overedit-comparison-table]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^gpt54-claude-opus-result]]
- Guiding question: 这一组实验结果说明哪些模型在 correctness 和 edit minimality 上同时表现好或差？
- User recitation: 用户提前总结为：观察到的现象是 GPT 不但做得差，还喜欢 `over-editing`；Claude Opus 不但做得好，还能在 `over-editing` 维度表现一枝独秀。
- Calibrated understanding: 这个总结抓住了这一节的核心对比。作者的直接结论是 GPT-5.4 在 frontier models 中 `over-edits the most`，同时 `Pass@1` 也偏低；Claude Opus 4.6 则同时拿到最高 `Pass@1` 和最小 `Levenshtein` diff。小校正是：Claude Opus 在 `Added Cognitive Complexity` 上也很低，但表中该列的 best 并不总是 Claude；reasoning 表里 Qwen 3.6 Plus 更低，non-reasoning 表里 GLM 5 更低。
- Missing points: 这一节只说明默认表现差异；还没有说明 prompt 能否改变这种行为，也没有解释 reasoning model 为什么会更容易或更不容易 over-edit。
- Open questions: 下一节需要看 explicit minimal-edit prompt 是否能降低 Levenshtein，并是否同时影响 correctness。

## Questions And Answers

## Reader Comments

### Measuring Over-Editing External Validity

- User comment: 这种构造的数据集确实能说明问题，但可能有偏差：作者想说明 LLMs generally 在任何 coding 任务上都有 `over-editing` 倾向，而这个实验更直接证明的是 LLM 在这种简单 bugfix 上有 `over-editing` 倾向。
- Cited supporting passage: [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^measurement-dataset-construction]]
- Note: 这个 critique 成立。该实验的内部有效性较强，因为 minimal fix 被构造得很清楚；但外部有效性有边界，因为它覆盖的是 programmatically corrupted、ground-truth 明确的 simple bugfix，而不是 feature work、large refactor、multi-file repo task 或 ambiguous product change。

## Candidate Concepts Entities

- `over-editing`: central term for the article's target failure mode; likely reusable beyond this source; no page checked yet; confidence high.

## Candidate Related Pages

- None yet.

## Sources

- [[sources/minimal-editing-2026-04/summary|minimal-editing-2026-04]]
- [[sources/minimal-editing-2026-04/source/minimal-editing-markdown|minimal-editing-markdown.md]]
