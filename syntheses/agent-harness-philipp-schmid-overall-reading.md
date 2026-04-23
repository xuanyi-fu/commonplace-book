---
type: synthesis
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Agent Harness：对 Philipp Schmid 2026-01 这篇文章的整体理解

围绕 `The importance of Agent Harness in 2026` 这篇文章，一个可以站得住脚的整体理解是：Philipp Schmid 说的不是某个具体 agent，而是包在 LLM 外面的 `agent harness`。它是一层运行基础设施，目标是让 agent 能可靠地完成 long-running tasks。原文明确说 `Agent Harness` 是 “the infrastructure that wraps around an AI model to manage long-running tasks”，并且强调它 “is not the agent itself”，而是 governs how the agent operates 的那层系统。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-definition|definition]]

## 第一层理解：它是 long-running task 的运行层

如果按这篇文章自己的定义来读，`agent harness` 的核心职责不是替模型做推理，而是让模型在真实环境中持续工作。也就是说，它关心的不是一次性回答，而是长时间 tool use、持续执行、持续遵守指令时的 `reliability`。这也是为什么文章一开始就强调，真正拉开差距的不是单步 benchmark，而是复杂任务中长期运行的稳定性。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-definition|definition]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-durability|durability]]

## 第二层理解：它必须暴露 trajectory，而且不只是为了“看过程”

这篇文章里一个很重要的要求是，`agent harness` 必须把多步 agent workflow 变成可 `log and grade` 的 structured data。这样做的目的不只是可观测，而是让系统变得可比较、可验证、可评分，并且让失败轨迹可以用于后续 hill climbing，甚至进一步反哺训练。也就是说，trajectory 的价值不是“我们能看到 agent 每一步在干嘛”这么简单，而是它让 harness 同时变成 measurement layer 和 data layer。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-log-and-grade|log and grade]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

## 第三层理解：不要把任务智能写死成 rigid workflow

围绕 `Bitter Lesson` 和最后的三条 builder principles，文章还在强调另一件事：`agent harness` 不应该主要靠僵硬、预先写死的 workflow 承载任务智能。更好的方向是提供 robust atomic tools，把高层 planning 留给 model / agent，同时由 harness 提供 guardrails、retries、verifications 这类治理能力。作者直接写的是：不要 build massive control flows，要 provide robust atomic tools，并且 let the model make the plan。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

## 第四层理解：build to delete

这篇文章还要求 `agent harness` 的架构保持 lightweight、modular、ready to delete。这里真正要删的，主要不是 atomic tools 本身，而是那些随着模型变强会迅速过时的 hand-coded control logic、rigid assumptions 和过度设计的 workflow。作者直接写的是：new models will replace your logic，developers must be ready to rip out code。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

## 一个更完整的综合结论

如果把整篇文章压成一句比较完整的话，可以这样说：

`agent harness` 是包在 LLM 外面的运行基础设施，它的作用是让 agent 能可靠地完成 long-running tasks。一个好的 harness 一方面要把真实运行中的 trajectory 结构化地记录下来，使系统可观察、可比较、可评分，并能据此改进 harness 甚至反哺模型训练；另一方面又不能把任务智能过多固化成 rigid workflow，而应该提供 robust atomic tools、必要的 guardrails / retries / verifications，并尽量让 model 自己去 plan。与此同时，harness 的架构还要保持 lightweight、modular、build-to-delete，因为随着模型变强，很多手写 control logic 都应该随时准备被删掉。` [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## Sources

- [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- [[concepts/agent-harness|Agent Harness]]
