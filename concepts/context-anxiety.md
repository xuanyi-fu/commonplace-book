---
type: concept
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# Context Anxiety

`context anxiety` 指 long-running agent 在 context window 接近，或者它以为自己接近 context limit 时，开始过早收尾的一种失稳现象。Anthropic 的 harness 文章把它放在长任务失败模式里：随着 context window 填满，模型会失去 coherence；某些模型还会在接近“自己相信的 context limit”时提前 wrap up work。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-anxiety-first-failure-mode]]

## 现象

这种现象不是简单的“token 不够了”或 API 直接报错，而是 agent 的任务策略提前被 context 压力改变：它本来还应该继续实现、排查、迭代或验证，却开始转向总结、交接、声明完成，或者把没有真正收束的问题包装成接近完成的状态。换句话说，context limit 还没有以硬错误形式出现，agent 已经把“快到 limit”理解成“该结束了”。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-anxiety-first-failure-mode]]

Anthropic 文章里，`context reset` 被用来处理这个问题：清空 context window，启动 fresh agent，再用 structured handoff 携带 previous state 和 next steps。它和 `compaction` 的关键差别是，`compaction` 在原 conversation 里把早期内容 summarize in place，让同一个 agent 继续跑在 shortened history 上；这保留 continuity，但不给 agent 一个 clean slate，所以 `context anxiety` 仍可能持续。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]

在 reading note 里的评论里，这个差别还可以用一个模型架构层面的类比理解：`compaction` 和 `context reset + handoff` 的差别，像是旧 thread 的 KV Cache hidden state 是否继续影响后续生成。但这只是机制类比，不是源文直接声明的 runtime 事实；更稳妥的说法是，`compaction` 倾向于保留旧 thread 的语义轨迹和连续性，而 `reset + handoff` 用显式 artifact 替换隐式连续性，从而降低旧状态继续支配新 agent 的风险。[[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note#^context-anxiety-kv-cache-inference]]

## GPT-5 系列和相邻证据

目前不要写成“GPT-5 系列有 `context anxiety`”。更准确的判断是：公开材料里还没有直接实验能说明 GPT-5 系列存在 Anthropic 定义的这种“接近自己以为的 context limit 所以提前收尾”的行为。Anthropic 的原始说法明确来自 Claude Sonnet 4.5 / Opus 4.5 的 harness 经验，不应直接外推到 GPT-5。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-anxiety-first-failure-mode]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]

GPT-5 系列有 long-context degradation 的相邻证据，但这不是 `context anxiety` 的直接证据。一个 GPT-5 对比实验发现，在 high-volume social media task 中，输入超过 5K posts / 70K tokens 后，包含 GPT-5 在内的模型准确率明显下降；不过该实验测的是大量短片段聚合任务，不是 long-running agent 提前结束任务。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/gpt-5-long-short-context-performance-text#^gpt-5-long-short-context-abstract]]

最接近 `context anxiety` 的相邻证据是 `Reasoning Shift`：该论文在 Qwen3.5-27B、GPT-OSS-120B、Gemini 3 Flash Preview、Kimi K2 Thinking 上观察到，长 irrelevant context、多轮对话或 subtask 会让同一问题的 reasoning trace 最多少 50%，并减少 self-verification / uncertainty management。这更像“context 变大后模型更快停止深入推理”，但仍不等同于“模型意识到快到 context limit 所以提前收尾”。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/reasoning-shift-context-shortens-reasoning-text#^reasoning-shift-abstract]]

open-source / open-weight 模型上，类似的长上下文失稳证据更明确：Qwen2.5-7B paper 把 40%-50% maximum context length 附近识别为 critical threshold，F1 从 0.55-0.56 掉到 0.3，属于 long-context intelligence degradation，而不是严格的 `context anxiety`。[[sources/gpt-5-context-anxiety-evidence-2026-04/source/qwen-long-context-intelligence-degradation-text#^qwen-critical-threshold-abstract]]

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown|Harness design for long-running application development]]
- [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic-harness-design-long-running-apps-2026-04-reading-note]]
- [[sources/gpt-5-context-anxiety-evidence-2026-04/summary|gpt-5-context-anxiety-evidence-2026-04]]
