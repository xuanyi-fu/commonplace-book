---
type: concept
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# Over-Editting

这里的 `over-editting` 对应源文里的 `Over-Editing`：模型能修对 bug、tests 也能过，但改动超过 minimal fix 所需范围，导致输出在结构上比必要修复更偏离原代码。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^over-editing-definition]]

它主要是 brown-field code review 问题，不是普通 correctness failure。已有 codebase 的代码通常已经被团队理解并有意写成当前形态；如果模型顺手 rewrite、加检查、改结构，tests 可能仍然通过，但 reviewer 需要重新理解更多变化，change safety 和长期 maintainability 都会变差。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^greenfield-brownfield-distinction]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^tests-miss-over-editing]]

## Observations

- `over-editting` 可以被度量，但这些度量只是 proxy：`Token-level Levenshtein Distance` 近似衡量相对 minimal patch 多改了多少 token，`Added Cognitive Complexity` 近似衡量是否引入额外理解负担。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^token-levenshtein-relative-patch]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^added-cognitive-complexity-metric]]
- 在这篇文章的实验里，GPT-5.4 是 correctness 和 edit minimality 的双差样本；Claude Opus 4.6 则同时拿到最高 `Pass@1` 和最小 `Levenshtein` diff。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^gpt54-claude-opus-result]]
- `over-editting` 更像可被 steer 的 default behavior，而不是纯 capability limitation：显式提示模型保留原代码和原逻辑后，所有模型的 `Levenshtein Distance` 都下降，reasoning models 的改善尤其明显。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^explicit-prompt-results]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^reasoning-overedit-overridable]]
- RL 可以把 minimal-edit behavior 内化成更 faithful 的 editing policy；在 Qwen3 4B 和 14B 实验中，这种改进没有损害 general coding ability。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^rl-no-lcb-degradation]] [[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^rl-improves-without-degradation]]
- 当前证据的边界是 isolated function bugfix：它能说明简单 bugfix 场景里的 `over-editting` 可以被测、被 steer、被训练改善，但不能直接外推到 repo-level、多文件、feature work 或 ambiguous product-change tasks。[[sources/minimal-editing-2026-04/source/minimal-editing-markdown#^isolated-function-benchmark-boundary]] [[notes/minimal-editing-2026-04-reading-note]]

## Sources

- [[sources/minimal-editing-2026-04/summary|minimal-editing-2026-04]]
- [[sources/minimal-editing-2026-04/source/minimal-editing-markdown|minimal-editing-markdown.md]]
- [[notes/minimal-editing-2026-04-reading-note|minimal-editing-2026-04-reading-note]]
