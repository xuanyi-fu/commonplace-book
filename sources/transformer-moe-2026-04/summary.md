---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# transformer-moe-2026-04

这个 source collection 不是在泛泛整理所有后来的 MoE 变体，而是围绕一个更具体的学习问题来收材料：Transformer 里的 MoE 层究竟是什么，它替换了 Transformer block 里的哪一部分，router 每个 token 到底在做什么，以及为什么它能把总参数做大、但又不要求每个 token 都跑完整个参数集。

## Structure

- `source/hugging-face-mixture-of-experts-explained.html`: Hugging Face 的 MoE 入门文章原始 HTML，用来先建立直觉和术语
- `source/paper-shazeer-2017-outrageously-large-neural-networks-sparsely-gated-moe.pdf`: 2017 年经典论文，讲稀疏 gated MoE 的基本机制
- `source/paper-gshard-2020-scaling-giant-models-with-conditional-computation.pdf`: GShard 论文，展示 MoE 如何嵌入 Transformer 并引入 capacity / overflow 等工程约束
- `source/paper-switch-transformers-2021.pdf`: Switch Transformers 论文，展示 top-1 routing 如何把 MoE 在 Transformer 里的路由做得更简单
- `source/rasbt-llms-from-scratch-ch04-07-moe-readme.md`: rasbt 的 `LLMs-from-scratch` 中 MoE 目录 README
- `source/rasbt-gpt-with-kv-ffn.py`: rasbt 的 dense FFN 版 GPT 对照实现
- `source/rasbt-gpt-with-kv-moe.py`: rasbt 的 MoE 版 GPT 对照实现
- `summary.md`: 这个 collection 的导读、范围说明和使用方法

## How To Use

- 第一遍先读 `source/hugging-face-mixture-of-experts-explained.html`。
  这一步的目标不是追求最严谨，而是先把几件事看顺：`expert` 不是整模型，通常是替换 FFN 的一组子网络；`router` / `gate` 是按 token 决定激活哪些 expert；MoE 的收益来自 sparse activation，而不是“所有参数都一起算”。
- 然后读 `source/paper-shazeer-2017-outrageously-large-neural-networks-sparsely-gated-moe.pdf`。
  这篇还不是 Transformer 里的最终形态，但它把最核心的 MoE 机械结构讲清楚了：一个可训练 gating network、多个 expert、稀疏激活、load balancing 问题，以及“把容量做大但不线性增加计算”的基本思路。
- 接着读 `source/paper-gshard-2020-scaling-giant-models-with-conditional-computation.pdf`。
  这里开始进入 “Transformer 里的 MoE 层” 这个具体问题。重点看：MoE 在 Transformer 中通常是替换 FFN 子层，而不是 attention；以及为了大规模训练，需要引入 `top-2 gating`、expert capacity、overflow token 处理、并行切分这些更工程化的约束。
- 再读 `source/paper-switch-transformers-2021.pdf`。
  这篇的价值在于把前一阶段相对复杂的 routing 简化成更容易训练和扩展的 `top-1` / switch routing。它能帮助你理解：MoE 在 Transformer 里不只是“多几个 FFN”，关键还在于路由策略怎么简化、通信怎么降低、训练怎么稳定。
- 最后读 rasbt 这一组代码：
  - `source/rasbt-llms-from-scratch-ch04-07-moe-readme.md`
  - `source/rasbt-gpt-with-kv-ffn.py`
  - `source/rasbt-gpt-with-kv-moe.py`
  这一组材料最适合把论文里的抽象概念落回实现。建议直接对照 dense FFN 版和 MoE 版来看，重点观察 “原来 block 里的 FFN 在代码里长什么样” 以及 “换成多个 experts + 一个 router 之后，forward path 多了哪些步骤”。
- 这轮 collection 有意不展开 Mixtral、DeepSeekMoE、Qwen-MoE 等较新的变体。
  它们当然重要，但如果第一轮学习目标是搞清楚 Transformer 里的 MoE 层“是什么”，那么先把经典机制、Transformer 化、以及一个可读实现串起来更重要。

## Summary

Transformer 里的 MoE 层，本质上是把原本每个 token 都会经过的 dense FFN 子层，替换成“多个 expert FFN + 一个 router”的稀疏层。attention 子层通常保持共享不变，MoE 主要发生在 feed-forward 这一段。所以，MoE 不是把整个 Transformer block 都变成多个分支，而是把其中最吃参数的 FFN 子层改造成条件激活结构。

router 的作用是按 token 做选择。给定某一层的 hidden state，router 会为每个 token 计算应该送去哪些 expert，常见做法是选 `top-k` 个 expert，再把 token 分发过去并聚合结果。Shazeer 2017 奠定了这种稀疏 gated 结构；到了 GShard，这个结构被系统性地嵌进 Transformer；到了 Switch Transformers，又进一步把 routing 简化成更激进的 `top-1` 选择，从而降低通信和训练复杂度。

MoE 能把总参数做大而 active compute 仍然保持稀疏，关键在于“总参数量”和“单个 token 激活参数量”被拆开了。一个层里可以放很多 expert，于是总参数显著增加；但一次前向时，每个 token 只经过很少几个 expert，而不是全部 expert，所以每个 token 实际使用的参数和计算量只对应其中一个小子集。这也是 MoE 常被说成“用 sparse activation 换更高 capacity”的原因。

MoE 从早期的通用 conditional computation 进入 Transformer 设计之后，发生的主要变化不是概念名字变了，而是它开始被明确地当作 Transformer FFN 的替代件来设计，并且不得不面对 Transformer 大规模训练的具体工程问题：token 到 expert 的分发、expert 负载是否均衡、每个 expert 的容量上限、溢出 token 怎么办、跨设备通信如何控制，以及 routing 复杂度是否会抵消稀疏计算带来的收益。这个 collection 收的 3 篇论文加 1 组代码，正好对应这条演化链。

## Sources

- [[source/hugging-face-mixture-of-experts-explained|hugging-face-mixture-of-experts-explained.html]]
- [[source/paper-shazeer-2017-outrageously-large-neural-networks-sparsely-gated-moe|paper-shazeer-2017-outrageously-large-neural-networks-sparsely-gated-moe.pdf]]
- [[source/paper-gshard-2020-scaling-giant-models-with-conditional-computation|paper-gshard-2020-scaling-giant-models-with-conditional-computation.pdf]]
- [[source/paper-switch-transformers-2021|paper-switch-transformers-2021.pdf]]
- [[source/rasbt-llms-from-scratch-ch04-07-moe-readme|rasbt-llms-from-scratch-ch04-07-moe-readme.md]]
- [[source/rasbt-gpt-with-kv-ffn|rasbt-gpt-with-kv-ffn.py]]
- [[source/rasbt-gpt-with-kv-moe|rasbt-gpt-with-kv-moe.py]]
