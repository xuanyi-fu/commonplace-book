---
type: concept
status: draft
created: 2026-05-14
updated: 2026-05-14
---

# MLA Multi-head Latent Attention

MLA（Multi-head Latent Attention）是 DeepSeek-V2 引入、DeepSeek-V3 继续采用的一种 attention 架构。它的核心不是 sparse attention，而是把每个历史 token 的 multi-head K/V cache 联合压缩成一个更小的 latent 表示，再在 attention 需要时通过训练好的 projection 生成各 head 所需的 key/value，从而降低长 context autoregressive inference 的 KV cache 内存和带宽压力。[[sources/mla-multihead-latent-attention-2026-05/summary|mla-multihead-latent-attention-2026-05]]

## 机制

普通 MHA 会为每个历史 token 存多组 head-specific key/value。MLA 改成先把 attention input `h_s` 通过 down-projection 压成 compressed latent vector `c_s^KV`，再通过 key/value up-projection 生成 content key/value；DeepSeek 的公式还单独保留一段携带 RoPE 的 decoupled key，因此生成时实际 cache 的不是完整 K/V，而是 `c_s^KV` 加上 RoPE key part。[[sources/mla-multihead-latent-attention-2026-05/source/deepseek-v3-technical-report-text|deepseek-v3-technical-report-text.txt]]

用简化形式写：

```text
h_s -> W_DKV -> c_s
c_s -> W_UK  -> k_s_content
c_s -> W_UV  -> v_s
h_s -> W_KR  -> k_s_rope

cache_s = { c_s, k_s_rope }
```

这里的 `W_DKV`、`W_UK`、`W_UV`、`W_KR` 是训练得到的模型参数；训练结束后，它们在 inference 时是固定的。MLA 的压缩不是无损压缩，也不是额外套一个 Transformer encoder/decoder，而是 attention 模块内部的可学习低秩 projection。[[sources/mla-multihead-latent-attention-2026-05/source/deepseek-v2-paper-text|deepseek-v2-paper-text.txt]]

## 和 MHA / MQA / GQA 的区别

MHA 为每个 query head 配一套独立 K/V，表达力强但 KV cache 大。MQA 让所有 query heads 共用一套 K/V；GQA 让一组 query heads 共用一套 K/V，所以它们主要靠减少 KV heads 来省 cache。MLA 则不是直接让 heads 共用同一套 K/V，而是让多个 heads 共享一个 compressed latent cache，再由 head-specific up-projection 从 latent 中生成各 head 的 K/V 子空间。DeepSeek-V2 论文把 MLA 和 MHA 做了 ablation，结论是 MLA 在保持性能的同时显著减少 KV cache。[[sources/mla-multihead-latent-attention-2026-05/source/deepseek-v2-paper-text|deepseek-v2-paper-text.txt]]

这个差别可以压成一句话：

```text
MQA/GQA: 少存几份 K/V
MLA: 存一份低维母体，再还原各 head 的 K/V
```

本库已有的 Qwen3-8B 参数分解页给出了 GQA 的本地对照：Qwen3-8B 通过 `num_key_value_heads = 8`、`num_attention_heads = 32` 让每 4 个 query heads 共用一组 KV heads，并指出 KV cache 会随层数、历史 token 数、KV heads 数和 head dimension 线性增加。这个页面支持把 Qwen3 主线理解为 GQA 路线，而不是 DeepSeek-style MLA 路线。[[syntheses/qwen3-8b-parameter-breakdown-and-ffn-over-attention|qwen3-8b-parameter-breakdown-and-ffn-over-attention]]

## 省什么，增加什么

MLA 省的是 KV cache 的存储量和读取带宽。长 context decoding 时，服务端每生成一个新 token 都要反复读取历史 token 的 cache；当 context 很长或 batch 很大，显存容量和 HBM bandwidth 往往比额外矩阵计算更紧张。DeepSeek-V2 官方 README 报告 DeepSeek-V2 相比 DeepSeek 67B reduced the KV cache by 93.3% and boosted maximum generation throughput to 5.76 times，这说明 DeepSeek 把 MLA 当成 serving cost 的核心优化，而不是只做结构美学。[[sources/mla-multihead-latent-attention-2026-05/source/deepseek-v2-readme|deepseek-v2-readme.md]]

MLA 增加的是 projection 与实现复杂度。概念上，模型需要从 cached latent 生成 key/value；工程上，优秀实现会把一部分 projection 与 query/output 计算合并，避免每一步把所有历史 K/V 完整 materialize。无论实现怎么优化，它的基本 tradeoff 都是：少搬运和少保存 KV cache，换取更多结构化矩阵计算与更复杂的 serving kernel。

## 不是 sparse attention

MLA 不决定当前 token 看哪些历史 token；它决定历史 token 的 K/V 以什么形式存。普通 dense MLA 仍然可以让当前 token attend 到完整历史前缀，只是历史 token 的 K/V cache 是 latent-compressed 的。

Sparse attention 解决的是另一个问题：当前 query token 是否要 attend 所有历史位置。DeepSeek-V3.2 这类后续 sparse attention 路线可以叠在 MLA 上：先用 MLA 把每个历史 token 的 cache 存便宜，再用 sparse selector 只让 core attention 看被选中的历史位置。也就是说：

```text
MLA: 压缩每个历史 token 怎么存
sparse attention: 选择当前 token 看哪些历史 token
```

## 采用边界

DeepSeek-V2 官方材料明确把 MLA 作为模型架构的一部分；DeepSeek-V3 technical report 继续采用 MLA；DeepSeek-R1 论文说明 R1/R1-Zero 是在 DeepSeek-V3-Base 上继续 RL / SFT 得到，因此 R1 线更适合理解为 V3-Base 架构的后训练延伸。[[sources/mla-multihead-latent-attention-2026-05/summary|mla-multihead-latent-attention-2026-05]]

MLA 不是一个已经训练好的 MHA/GQA 模型在 inference 时随手打开的开关。MHA2MLA 论文把从 MHA/GQA 到 MLA 的转换明确表述为需要专门 fine-tuning 的架构迁移问题，并提出 partial-RoPE 与 low-rank approximation 来让已有模型转成 MLA。这个边界也解释了为什么 Qwen 这类 GQA 模型不会因为 MLA 好用就自动变成 MLA：要原生使用 MLA，最好从预训练架构和 serving stack 就一起设计。[[sources/mla-multihead-latent-attention-2026-05/source/mha2mla-paper-text|mha2mla-paper-text.txt]] [[syntheses/qwen3-8b-parameter-breakdown-and-ffn-over-attention|qwen3-8b-parameter-breakdown-and-ffn-over-attention]]

## Sources

- [[sources/mla-multihead-latent-attention-2026-05/summary|mla-multihead-latent-attention-2026-05]]
- [[syntheses/qwen3-8b-parameter-breakdown-and-ffn-over-attention|qwen3-8b-parameter-breakdown-and-ffn-over-attention]]
