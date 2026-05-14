---
type: summary
status: draft
created: 2026-05-14
updated: 2026-05-14
---

# mla-multihead-latent-attention-2026-05

这个 source collection 收集 MLA（Multi-head Latent Attention）的几份 primary evidence，重点回答三个问题：DeepSeek 最初怎样定义 MLA，它怎样通过 low-rank key-value joint compression 降低 inference-time KV cache，DeepSeek-V3 / R1 线如何继承这条架构，以及 MHA2MLA 为什么把 MLA 当成模型架构迁移目标而不是 inference-time flag。

## Structure

- `source/deepseek-v2-paper.pdf`: DeepSeek-V2 论文原始 PDF，MLA 的主要定义来源
- `source/deepseek-v2-paper-text.txt`: DeepSeek-V2 PDF 的 `pdftotext` 衍生文本，用于搜索和快速定位公式
- `source/deepseek-v2-readme.md`: DeepSeek-V2 官方 GitHub README 快照，包含官方对 MLA、KV cache reduction、SGLang MLA optimization 的产品化描述
- `source/deepseek-v3-technical-report.pdf`: DeepSeek-V3 technical report 原始 PDF
- `source/deepseek-v3-technical-report-text.txt`: DeepSeek-V3 technical report 的 `pdftotext` 衍生文本
- `source/deepseek-r1-paper.pdf`: DeepSeek-R1 论文原始 PDF，用于确认 R1/R1-Zero 建立在 DeepSeek-V3-Base 上
- `source/deepseek-r1-paper-text.txt`: DeepSeek-R1 PDF 的 `pdftotext` 衍生文本
- `source/mha2mla-paper.pdf`: MHA2MLA 论文原始 PDF，用于确认 MLA 是需要架构迁移/微调的 attention 机制
- `source/mha2mla-paper-text.txt`: MHA2MLA PDF 的 `pdftotext` 衍生文本
- `summary.md`: 这个 collection 的结构和使用说明

## How To Use

- 先读 `source/deepseek-v2-paper-text.txt` 或 `source/deepseek-v2-readme.md`，确认 MLA 的核心定义：low-rank key-value union / joint compression，用来降低 autoregressive inference 的 KV cache bottleneck。
- 再读 `source/deepseek-v3-technical-report-text.txt` 的 architecture / Multi-Head Latent Attention 小节，确认 DeepSeek-V3 继续采用 MLA，并且只需要 cache compressed latent vector 与 decoupled RoPE key。
- 需要判断 R1 是否属于同一架构线时，读 `source/deepseek-r1-paper-text.txt` 中 DeepSeek-R1 / R1-Zero 建立在 DeepSeek-V3-Base 上的说明。
- 需要区分 MLA 和普通 MHA/GQA 的迁移边界时，读 `source/mha2mla-paper-text.txt`；该文把 MHA/GQA 模型迁移到 MLA 描述成需要专门 fine-tuning 的问题。
- PDF 是公式、表格和图示的 authoritative source；`.txt` 只是扫描和全文检索用的 convenience view。

## Summary

DeepSeek-V2 官方材料把 MLA 描述为 attention 侧的 low-rank key-value union compression，用来消除 inference-time KV cache bottleneck；DeepSeek-V2 README 同时报告，相比 DeepSeek 67B，DeepSeek-V2 reduced the KV cache by 93.3% and boosted maximum generation throughput to 5.76 times。DeepSeek-V2 论文正文和附录给出完整计算形式：attention input `h_t` 被 down-projection 成 compressed latent vector `c_t^KV`，再通过 key/value up-projection 生成 content key/value，同时保留一段携带 RoPE 的 decoupled key；生成时只需要 cache compressed latent vector 和 RoPE key。[[source/deepseek-v2-paper-text|deepseek-v2-paper-text.txt]] [[source/deepseek-v2-readme|deepseek-v2-readme.md]]

DeepSeek-V3 technical report 继续采用 MLA 和 DeepSeekMoE，并明确说这两者已经在 DeepSeek-V2 中验证。它的 MLA 小节再次把 MLA 的核心定义为 low-rank joint compression for attention keys and values to reduce KV cache during inference，并说明只 cache `c_t^KV` 与 `k_t^R` 可以显著降低 KV cache，同时维持 comparable to standard MHA 的性能。DeepSeek-R1 论文则说明 DeepSeek-R1-Zero 和 DeepSeek-R1 建立在 DeepSeek-V3-Base 上，因此 R1 线应理解为 V3-Base architecture 的 post-training / RL 延伸，而不是单独引入一套新的 MLA 证据。[[source/deepseek-v3-technical-report-text|deepseek-v3-technical-report-text.txt]] [[source/deepseek-r1-paper-text|deepseek-r1-paper-text.txt]]

MHA2MLA 论文从另一个角度确认了 MLA 的边界：它把 MLA 称为 DeepSeek proposed 的 architecture，目标是把已经训练好的 MHA/GQA 模型 transition 到 MLA，而不是在 inference server 上临时压缩普通 KV cache。该文也强调，MHA/GQA 到 MLA 的 zero-shot transfer 并不自然，需要 partial-RoPE 和 low-rank approximation 等专门迁移步骤。[[source/mha2mla-paper-text|mha2mla-paper-text.txt]]

## Sources

- [[source/deepseek-v2-paper|deepseek-v2-paper.pdf]]
- [[source/deepseek-v2-paper-text|deepseek-v2-paper-text.txt]]
- [[source/deepseek-v2-readme|deepseek-v2-readme.md]]
- [[source/deepseek-v3-technical-report|deepseek-v3-technical-report.pdf]]
- [[source/deepseek-v3-technical-report-text|deepseek-v3-technical-report-text.txt]]
- [[source/deepseek-r1-paper|deepseek-r1-paper.pdf]]
- [[source/deepseek-r1-paper-text|deepseek-r1-paper-text.txt]]
- [[source/mha2mla-paper|mha2mla-paper.pdf]]
- [[source/mha2mla-paper-text|mha2mla-paper-text.txt]]
