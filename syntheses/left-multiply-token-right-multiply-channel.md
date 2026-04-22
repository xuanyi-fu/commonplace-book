---
type: synthesis
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# 左乘混 token，右乘混 channel

这页是一个用于防止记混的线性代数记号笔记。核心前提只有一个：在这里采用的约定是“行 = token，列 = channel”。在这个约定下，左乘会在行之间做线性组合，所以是 mix token；右乘会在列之间做线性组合，所以是 mix channel。

## 约定

设 hidden state 矩阵为

\[
V \in \mathbb R^{N\times E}
\]

其中：

- 第 \(i\) 行 \(V_i\) 表示第 \(i\) 个 token 的 hidden state
- \(N\) 是 token 数
- \(E\) 是 channel 数

也就是说：

- 行 = token
- 列 = channel

## 左乘：\(H = AV\)

设

\[
A \in \mathbb R^{N\times N}
\]

则第 \(i\) 行输出是

\[
H_i = \sum_{j=1}^N A_{ij} V_j
\]

这说明：

- 第 \(i\) 个输出 token，会把所有输入 token 的 \(V_j\) 按权重 \(A_{ij}\) 加起来
- 所以 \(H_i\) 一般依赖很多个 \(V_j\)
- 因而左乘是在行之间做 mixing，也就是 mix token

更直白地说，左边这个矩阵决定“每个输出 token 要看哪些输入 token，以及各自占多少权重”。

## 右乘：\(H = VW\)

设

\[
W \in \mathbb R^{E\times D}
\]

则第 \(i\) 行输出是

\[
H_i = V_i W
\]

如果写到单个元素，就是

\[
H_{ik} = \sum_{j=1}^E V_{ij} W_{jk}
\]

这说明：

- 第 \(i\) 个输出 token 只依赖第 \(i\) 个输入 token 的向量 \(V_i\)
- 不依赖别的 token 的 \(V_j\)
- 它只是把 \(V_i\) 自己的各个 channel 按 \(W\) 重新组合
- 因而右乘是在列之间做 mixing，也就是 mix channel

更直白地说，右边这个矩阵决定“同一个 token 内部，各个 channel 怎么重新线性组合成新的 channel”。

## 不要记反的关键

这个结论依赖当前的矩阵约定：

- 行 = token
- 列 = channel

所以：

- 左乘作用在行空间上，改变的是 token 之间的组合关系
- 右乘作用在列空间上，改变的是 channel 之间的组合关系

如果你换了约定，例如改成“列 = token，行 = channel”，那这句话就要跟着反过来，不能脱离约定单独背。

## 一句话记忆

在“行 = token，列 = channel”这个约定下：

- 左乘矩阵：作用在行上，所以 mix token
- 右乘矩阵：作用在列上，所以 mix channel

## Sources

- 本页整理自 2026-04-21 当前线程中的用户数学笔记。
