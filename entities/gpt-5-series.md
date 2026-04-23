---
type: entity
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# GPT-5 Series

这里先只记录 GPT-5 系列和 [[concepts/context-anxiety|context anxiety]] 相关的当前判断：**没有看到公开证据能直接说明 GPT-5 系列存在 Anthropic 定义的 `context anxiety`**，也就是模型因为接近自己以为的 context limit 而提前收尾。Anthropic 的原始说法目前明确落在 Claude Sonnet 4.5 / Opus 4.5 的 harness 经验上，不应直接外推到 GPT-5。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-anxiety-first-failure-mode]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]

更稳妥的说法是：GPT-5 系列有 long-context degradation 的相邻证据，但这不是 `context anxiety` 的直接证据。一个 GPT-5 对比实验发现，在 high-volume social media task 中，输入超过 5K posts / 70K tokens 后，包含 GPT-5 在内的模型准确率明显下降；不过该实验测的是大量短片段聚合任务，不是长时 agent 提前结束任务。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/gpt-5-long-short-context-performance-text#^gpt-5-long-short-context-abstract]]

最接近 `context anxiety` 的相邻证据是 `Reasoning Shift`：该论文在 Qwen3.5-27B、GPT-OSS-120B、Gemini 3 Flash Preview、Kimi K2 Thinking 上观察到，长 irrelevant context、多轮对话或 subtask 会让同一问题的 reasoning trace 最多少 50%，并减少 self-verification / uncertainty management。这更像“context 变大后模型更快停止深入推理”，但仍不等同于“模型意识到快到 context limit 所以提前收尾”。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/reasoning-shift-context-shortens-reasoning-text#^reasoning-shift-abstract]]

open-source / open-weight 模型上，类似的长上下文失稳证据更明确：Qwen2.5-7B paper 把 40%-50% maximum context length 附近识别为 critical threshold，F1 从 0.55-0.56 掉到 0.3，属于 long-context intelligence degradation，而不是严格的 `context anxiety`。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/qwen-long-context-intelligence-degradation-text#^qwen-critical-threshold-abstract]]

## 当前判断

把 GPT-5 系列写进知识库时，应该避免说“GPT-5 有 context anxiety”。更准确的记录是：**GPT-5 系列是否有 Anthropic 意义上的 `context anxiety` 仍未公开坐实；但 GPT-5 和 open-weight reasoning models 都存在 long-context degradation / reasoning compression 这类相邻风险。**

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- [[sources/gpt-5-context-anxiety-evidence-2026-04/summary|gpt-5-context-anxiety-evidence-2026-04]]
