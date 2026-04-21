---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# weak-to-strong-supervision-2026-04

这个 source collection 收集了 weak-to-strong supervision / weak-to-strong generalization 的几份核心一手资料，重点回答一个容易混淆的问题：它要解决的不是“能不能直接调用强模型”，而是“当监督者本身比模型弱时，怎样训练、评估、对齐或控制更强的模型”。

## Structure

- `source/blog-openai-weak-to-strong-generalization.md`: OpenAI 2023 年官方博文，最直接解释 weak-to-strong 的动机，也最直接回答“为什么不是直接用强模型就完了”
- `source/paper-openai-weak-to-strong-generalization.md`: OpenAI 原始论文整理，覆盖 formal setup、`performance gap recovered (PGR)` 指标、实证结果和局限
- `source/blog-anthropic-automated-w2s-researcher.md`: Anthropic 2026 年官方研究博文，展示 weak-to-strong supervision 如何被当作一个 outcome-gradable alignment research 问题来自动化推进
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/blog-openai-weak-to-strong-generalization.md`，建立问题意识：weak-to-strong 关心的是监督和可控性，不是单次调用强模型
- 再读 `source/paper-openai-weak-to-strong-generalization.md`，理解它的实验设定：`weak supervisor`、`strong student`、`ground-truth-supervised strong ceiling`、以及 `PGR`
- 最后读 `source/blog-anthropic-automated-w2s-researcher.md`，看这个问题在 2026 年如何被继续推进成一个可自动化研究的 alignment benchmark
- 讨论时要始终区分三件事：
  - `using a strong model`
  - `supervising / evaluating a strong model`
  - `aligning a stronger model when no stronger trusted judge exists`

## Summary

截至 2026-04-21，这组资料支持一个很清楚的结论：weak-to-strong supervision 不是在问“强模型能不能直接用”，而是在问“如果标签、反馈、评估和监督来自更弱的人或模型，强模型会不会只复制这些弱监督的错误，还是能被诱导去发挥它本来就有的更高能力”。这个问题之所以重要，是因为当模型比人更强时，真正困难的不再是“有没有强模型”，而是“谁来监督它、谁来判断它是否做对了、谁来把期望行为可靠地传达给它”。OpenAI 的原始工作把它定义成 superalignment 的一个可实验化类比；Anthropic 则进一步把它当成一个 outcome-gradable 的 alignment research testbed，用来评估自动化研究代理能否推进这个问题。

## Sources

- [[source/blog-openai-weak-to-strong-generalization|blog-openai-weak-to-strong-generalization.md]]
- [[source/paper-openai-weak-to-strong-generalization|paper-openai-weak-to-strong-generalization.md]]
- [[source/blog-anthropic-automated-w2s-researcher|blog-anthropic-automated-w2s-researcher.md]]
