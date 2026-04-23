---
type: summary
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# gpt-5-context-anxiety-evidence-2026-04

这个 source collection 保存了用于判断 GPT-5 系列是否有 `context anxiety` 相邻问题的论文材料，重点覆盖 long-context degradation、reasoning shift、GPT-5 high-volume context task、以及 open-source Qwen 的 long-context critical threshold。

## Structure

- `source/reasoning-shift-context-shortens-reasoning.pdf`: arXiv 2604.01161 原始 PDF，讨论长 context 如何缩短 reasoning traces
- `source/reasoning-shift-context-shortens-reasoning-text.txt`: `pdftotext` derivative，带少量 block id 方便引用
- `source/context-length-alone-hurts-performance.pdf`: arXiv 2510.05381 原始 PDF，讨论 perfect retrieval 下 context length 本身仍会伤害表现
- `source/context-length-alone-hurts-performance-text.txt`: `pdftotext` derivative，带少量 block id 方便引用
- `source/gpt-5-long-short-context-performance.pdf`: arXiv 2602.14188 原始 PDF，比较 GPT-5 等模型在 high-volume long short-context 任务上的表现
- `source/gpt-5-long-short-context-performance-text.txt`: `pdftotext` derivative，带少量 block id 方便引用
- `source/qwen-long-context-intelligence-degradation.pdf`: arXiv 2601.15300 原始 PDF，讨论 Qwen2.5-7B 的 long-context critical threshold
- `source/qwen-long-context-intelligence-degradation-text.txt`: `pdftotext` derivative，带少量 block id 方便引用
- `source/lost-in-the-middle.pdf`: arXiv 2307.03172 原始 PDF，long-context position sensitivity 的经典论文
- `source/lost-in-the-middle-text.txt`: `pdftotext` derivative，带少量 block id 方便引用
- `summary.md`: 这个 collection 的导读、范围说明和使用建议

## How To Use

- 需要快速判断 GPT-5 系列与 `context anxiety` 的关系时，先读 [[entities/gpt-5-series|gpt-5-series]]。
- 需要最接近 `context anxiety` 的相邻实验证据时，优先看 `reasoning-shift-context-shortens-reasoning-text.txt` 的 `^reasoning-shift-abstract`。
- 需要 GPT-5 相关 high-volume context 证据时，看 `gpt-5-long-short-context-performance-text.txt` 的 `^gpt-5-long-short-context-abstract`。
- 需要 open-source / open-weight 类比时，看 `reasoning-shift` 的 GPT-OSS-120B 结果和 Qwen critical-threshold paper。
- OpenAI 官方 GPT-5 / GPT-5.5 网页是这次 brief 的重要背景，但 raw HTML 抓取被 403 阻止，因此未本地化到本 collection；引用官方发布数据时应回到 live OpenAI 页面复核。

## Summary

这些材料共同支持一个谨慎判断：公开材料里还没有直接实验能证明 GPT-5 系列存在 Anthropic 定义的 `context anxiety`，但 GPT-5 和 open-weight reasoning models 都有 long-context degradation 或 reasoning compression 的相邻证据。

`Reasoning Shift` 是最接近这次问题的论文：它发现多个 reasoning model 在长 irrelevant context、多轮对话或 subtask 条件下，会对同一个问题生成显著更短的 reasoning trace，最多减少 50%，并伴随 self-verification 与 uncertainty management 减少。[[source/reasoning-shift-context-shortens-reasoning-text#^reasoning-shift-abstract]]

GPT-5 专项对比论文则显示，在 20K social media posts 的 high-volume task 中，当输入超过 5K posts / 70K tokens 后，包含 GPT-5 在内的模型表现明显下降；这支持 long-context degradation，但不是 `context anxiety` 的直接证据。[[source/gpt-5-long-short-context-performance-text#^gpt-5-long-short-context-abstract]]

Qwen2.5-7B 的 long-context threshold paper 显示，开源 Qwen 模型在约 40%-50% 最大 context length 附近出现明显性能崩塌；这说明 open-source 模型上有类似的长上下文失稳现象，但仍应和“提前收尾”的 `context anxiety` 区分。[[source/qwen-long-context-intelligence-degradation-text#^qwen-critical-threshold-abstract]]

## Sources

- [[source/reasoning-shift-context-shortens-reasoning|Reasoning Shift: How Context Silently Shortens LLM Reasoning]]
- [[source/reasoning-shift-context-shortens-reasoning-text|reasoning-shift-context-shortens-reasoning-text.txt]]
- [[source/context-length-alone-hurts-performance|Context Length Alone Hurts LLM Performance Despite Perfect Retrieval]]
- [[source/context-length-alone-hurts-performance-text|context-length-alone-hurts-performance-text.txt]]
- [[source/gpt-5-long-short-context-performance|GPT-5 vs Other LLMs in Long Short-Context Performance]]
- [[source/gpt-5-long-short-context-performance-text|gpt-5-long-short-context-performance-text.txt]]
- [[source/qwen-long-context-intelligence-degradation|Intelligence Degradation in Long-Context LLMs]]
- [[source/qwen-long-context-intelligence-degradation-text|qwen-long-context-intelligence-degradation-text.txt]]
- [[source/lost-in-the-middle|Lost in the Middle]]
- [[source/lost-in-the-middle-text|lost-in-the-middle-text.txt]]
