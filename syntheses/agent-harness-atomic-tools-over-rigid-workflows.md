---
type: synthesis
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Agent Harness：与其把任务智能写死成 workflow，不如提供原子能力

围绕 Philipp Schmid 的 `The "Bitter Lesson" of building Agents` 这一节，一个很自然的综合判断是：`agent harness` 不应该主要靠僵硬、预先写死的 workflow 来承载任务智能，而应该尽量提供轻量、稳健、可组合的原子能力，把更多 planning 空间留给 model / agent。这个判断不是对原文的逐句复述，而是把两段内容合起来读出的结论：一方面，作者明确说 Manus 重构 harness 是为了移除 `rigid assumptions`，并且强调 harness 必须 `lightweight`；另一方面，他又说开发者需要能够把昨天写进去的 “smart logic” 拆掉，因为下一代模型会改变 agent 的最优结构。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]]

## 这个判断是怎么推出来的

原文先借 `Bitter Lesson` 说，一般方法长期会打败大量手工写进去的人类先验。然后他举的例子都指向同一个方向：不是不断叠加结构，而是删掉那些把系统绑死的结构。Manus 六个月里改了五次 harness，LangChain 一年里重构了多次 agent，Vercel 删掉了大量 tools，带来的结果反而是更少步骤、更少 token、更快响应。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]]

如果把这些例子放在一起看，作者真正反对的不是一切流程控制，而是把任务完成路径预先写死在 harness 里面。因为一旦 harness 太依赖固定 workflow、过度细化的 control flow、或者某一代模型刚好需要的手工“聪明逻辑”，下一代模型出现以后，这些结构就会迅速从资产变成负担。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]]

## 对 agent harness 更准确的要求

从这个角度看，一个更好的 `agent harness` 应该具备的是：

- 原子能力，而不是把大任务路径提前写成固定 workflow
- 可组合性，让不同能力能被 model 在运行时重新编排
- 可删性，让昨天的 control logic 可以随着模型变强而被移除
- 轻量 guardrails，而不是厚重、强耦合、难以替换的 orchestration layer  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

这也能和文章最后 `What Comes Next?` 里的建议对上：`Start Simple`、`Provide robust atomic tools`、`Let the model make the plan`。虽然这些话出现在下一节，但它们其实正好把前一节 `Bitter Lesson` 的含义说得更直白。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

## 一个更稳定的综合结论

如果把这条线索压成一句话，就是：

`agent harness` 的设计重点不应该是把“如何完成任务”提前冻结成重 workflow，而应该是提供稳健、原子、可组合的能力面，让 model 在运行时自己规划；而 harness 只负责必要的边界、执行、记录和治理。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

这个结论对 coding 场景尤其有用，因为它意味着像 `computer use`、filesystem、search、planning 这类东西，更适合作为 harness 暴露出的原子能力，而不是被提前编排成一串固定步骤的“万能自动流程”。[[concepts/agent-harness|Agent Harness]]

## Sources

- [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- [[concepts/agent-harness|Agent Harness]]
