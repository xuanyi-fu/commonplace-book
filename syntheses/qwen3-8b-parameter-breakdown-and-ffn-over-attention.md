---
type: synthesis
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Qwen3-8B 的参数分解，以及为什么 Transformer 更愿意膨胀 FFN 而不是 attention

这页不是在讨论 `Qwen3-8B` 的产品能力，而是在把一个更基础的问题算清楚：如果把一个现代 dense LLM 的参数按模块拆开，attention 到底有多大，`SwiGLU` FFN 到底有多大，为什么大家常说参数大头在 FFN，以及为什么后续像 MoE 这样的结构更自然地先去改 FFN，而不是先去改 attention。[[sources/transformer-moe-2026-04/summary|transformer-moe-2026-04]]

## 先把 Qwen3-8B 的基本配置抄出来

按官方 `Qwen3-8B` model card 和 `config.json`，这次算账只用到下面这些量：

- `vocab_size = 151936`
- `d_model = 4096`
- `num_hidden_layers = 36`
- `num_attention_heads = 32`
- `num_key_value_heads = 8`
- `d_head = 128`
- `d_ff = 12288`
- `tie_word_embeddings = false`
- `attention_bias = false` [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B) [Qwen3-8B config](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json)

这意味着：

\[
32 \cdot 128 = 4096 = d_{\text{model}}
\]

所以 query 这边的总宽度正好等于 `d_model`。但 `Qwen3-8B` 用的是 GQA，不是标准 MHA，因此 key / value 的总宽度不是 \(32 \cdot 128\)，而是：

\[
8 \cdot 128 = 1024
\]

于是：

\[
Q \in \mathbb R^{B\times T\times 4096},\qquad
K,V \in \mathbb R^{B\times T\times 1024}
\]

这也意味着每 \(4\) 个 query heads 共用一套 KV heads，因为：

\[
\frac{32}{8} = 4
\]

## attention 这部分到底有多少参数

对单层 attention 而言，最主要的参数来自四个投影矩阵：

\[
Q = XW_Q,\qquad
K = XW_K,\qquad
V = XW_V,\qquad
Y = \operatorname{Concat}(O_1,\dots,O_{32})W_O
\]

其中：

\[
W_Q \in \mathbb R^{4096\times 4096}
\]

\[
W_K \in \mathbb R^{4096\times 1024}
\]

\[
W_V \in \mathbb R^{4096\times 1024}
\]

\[
W_O \in \mathbb R^{4096\times 4096}
\]

所以单层 attention 参数量就是：

\[
|W_Q| = 4096 \cdot 4096 = 16{,}777{,}216
\]

\[
|W_K| = 4096 \cdot 1024 = 4{,}194{,}304
\]

\[
|W_V| = 4096 \cdot 1024 = 4{,}194{,}304
\]

\[
|W_O| = 4096 \cdot 4096 = 16{,}777{,}216
\]

加起来得到：

\[
N_{\text{attn, layer}}
=
16{,}777{,}216
+ 4{,}194{,}304
+ 4{,}194{,}304
+ 16{,}777{,}216
= 41{,}943{,}040
\]

36 层总共就是：

\[
N_{\text{attn, all}}
=
36 \cdot 41{,}943{,}040
= 1{,}509{,}949{,}440
\]

也就是大约：

\[
1.51\text{B}
\]

如果 `Qwen3-8B` 不是 GQA，而是标准 MHA，那么 \(K/V\) 也会是 \(4096\) 维，单层 attention 参数会变成：

\[
4 \cdot 4096^2 = 67{,}108{,}864
\]

相比现在的 GQA：

\[
67{,}108{,}864 - 41{,}943{,}040 = 25{,}165{,}824
\]

也就是单层少了大约 \(37.5\%\) 的 attention 投影参数。

## `SwiGLU` FFN 为什么会一下子变得这么大

`Qwen3-8B` 的 FFN 不是简单的两层 MLP，而是 `SwiGLU`。对单层 block 而言，可以把它理解成三块大矩阵：

- `gate_proj: 4096 \to 12288`
- `up_proj: 4096 \to 12288`
- `down_proj: 12288 \to 4096`

公式上可以写成：

\[
h = \operatorname{SiLU}(xW_{\text{gate}})\odot (xW_{\text{up}})
\]

\[
y = hW_{\text{down}}
\]

因此每层 FFN 参数量是：

\[
N_{\text{ffn, layer}}
=
4096\cdot 12288
+ 4096\cdot 12288
+ 12288\cdot 4096
\]

\[
= 3\cdot 4096\cdot 12288
= 150{,}994{,}944
\]

也就是单层大约：

\[
0.151\text{B}
\]

36 层总共就是：

\[
N_{\text{ffn, all}}
=
36 \cdot 150{,}994{,}944
= 5{,}435{,}817{,}984
\]

也就是大约：

\[
5.44\text{B}
\]

这个数字第一次算出来时会显得离谱，但它并不是算错了，而是现代 LLM 的典型分布：只要 \(d_{\text{model}}\) 已经到了 \(4096\) 这种量级，再把中间维度膨胀到

\[
d_{ff}=12288 = 3\cdot d_{\text{model}}
\]

那么一层 FFN 本来就会是一个 \(10^8\) 量级的大块参数。

## 把整模型加起来

除了 block 内部的 attention 和 FFN 之外，`Qwen3-8B` 还有 embedding 与 output head。因为 `tie_word_embeddings = false`，两者不共享参数。

输入 embedding：

\[
N_{\text{embed}}
=
151936 \cdot 4096
= 622{,}329{,}856
\]

输出 head：

\[
N_{\text{lm\_head}}
=
151936 \cdot 4096
= 622{,}329{,}856
\]

norm 这部分很小。36 层、每层两个 RMSNorm，再加最后一个 final norm，总共只有：

\[
N_{\text{norm}} = 299{,}008
\]

所以全模型总参数是：

\[
N_{\text{total}}
=
N_{\text{embed}}
+ N_{\text{lm\_head}}
+ N_{\text{attn, all}}
+ N_{\text{ffn, all}}
+ N_{\text{norm}}
\]

\[
=
622{,}329{,}856
+ 622{,}329{,}856
+ 1{,}509{,}949{,}440
+ 5{,}435{,}817{,}984
+ 299{,}008
\]

\[
= 8{,}190{,}726{,}144
\]

也就是：

\[
8.19\text{B} \approx 8.2\text{B}
\]

这和官方 model card 对得上。对应占比大概是：

- 输入 embedding：\(7.6\%\)
- 输出 head：\(7.6\%\)
- attention：\(18.4\%\)
- FFN：\(66.4\%\)

所以如果只记一句话：

`Qwen3-8B` 这种 dense LLM 的参数大头，不在 attention，而在 `SwiGLU` FFN。

## FFN 为什么值得膨胀

FFN 变大，不是因为它干了 attention 那种 token-to-token 交互，而是因为它给每个 token 提供了更大的 channel-space 计算容量。

如果只看职责，可以粗略分成：

- attention：让 token 和别的 token 交互
- FFN：让单个 token 在 channel 维度上做更强的非线性变换

所以 attention 更像“通信层”，FFN 更像“计算层”或“容量层”。

把 FFN 从

\[
\mathbb R^{d_{\text{model}}}
\to
\mathbb R^{d_{ff}}
\to
\mathbb R^{d_{\text{model}}}
\]

做宽，本质上是在给每个 token 更多的中间工作空间，让它在固定上下文读取完成之后，能做更复杂的 channel mixing 和非线性加工。这也是为什么现代 dense LLM 的参数主要堆在 FFN，而不是 attention。

## 为什么不优先膨胀 attention

一个直接的工程原因是：attention 的麻烦不只在参数量，还在 KV cache。

对自回归推理来说，KV cache 的主要大小和下面这个量成正比：

\[
L \cdot T \cdot h_{kv} \cdot d_{\text{head}}
\]

其中：

- \(L\) 是层数
- \(T\) 是当前缓存的历史 token 数
- \(h_{kv}\) 是 KV heads 数
- \(d_{\text{head}}\) 是每个 KV head 的宽度

也就是说，如果你把 \(K/V\) 维度膨胀，或者把 KV heads 数量拉大，那么推理时的 KV cache、带宽和长上下文成本都会跟着近似线性膨胀。GQA 的一个核心好处，恰恰就是在尽量保留 query-side 表达能力的同时，把 \(K/V\) 维度压下来。[[sources/transformer-moe-2026-04/source/hugging-face-mixture-of-experts-explained|hugging-face-mixture-of-experts-explained.html]]

FFN 则不一样。FFN 再大，主要影响的是：

- 模型总权重有多大
- 每个 token 的前向 matmul 有多大

但它不会像 attention 一样，把每个历史 token 的 \(K/V\) 状态一直缓存下来。因此，从“增加参数容量”的角度看，膨胀 FFN 往往比膨胀 attention 更划算。

## 这也解释了为什么 MoE 优先改 FFN

如果 dense 模型里，参数大头本来就在 FFN，那最自然的 sparse 化路径就是：

- attention 先保持共享
- 把原来的 dense FFN 换成很多个 expert FFN
- 每个 token 只激活少数几个 experts

这正是 MoE 在 Transformer 里的典型落点。它不是随便挑了一块改，而是直接改了原本最肥、最适合做参数扩张、同时又不想把 KV cache 一起拉爆的那一层。[[sources/transformer-moe-2026-04/summary|transformer-moe-2026-04]] [[sources/transformer-moe-2026-04/source/rasbt-llms-from-scratch-ch04-07-moe-readme|rasbt-llms-from-scratch-ch04-07-moe-readme.md]] [[sources/transformer-moe-2026-04/source/hugging-face-mixture-of-experts-explained|hugging-face-mixture-of-experts-explained.html]]

## 一个更准确的结论

如果把今天这页压成一句话，我会写成：

`Qwen3-8B 这种现代 dense LLM 的参数分布说明，Transformer 的主要参数容量本来就堆在 FFN / SwiGLU 上；attention 更像负责 token 间交互的共享机制，而它的 KV cache 又让进一步膨胀变得昂贵，因此后续像 MoE 这样的结构，优先改 FFN 而不是优先改 attention，是一个很自然的设计选择。`

## Sources

- [[sources/transformer-moe-2026-04/summary|transformer-moe-2026-04]]
- [[sources/transformer-moe-2026-04/source/hugging-face-mixture-of-experts-explained|hugging-face-mixture-of-experts-explained.html]]
- [[sources/transformer-moe-2026-04/source/rasbt-llms-from-scratch-ch04-07-moe-readme|rasbt-llms-from-scratch-ch04-07-moe-readme.md]]
- [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B)
- [Qwen3-8B config](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json)
