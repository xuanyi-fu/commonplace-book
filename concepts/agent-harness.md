---
type: concept
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Agent Harness

`agent harness` 在 Philipp Schmid 2026-01 这篇文章里的核心定义是：它是包在 AI model 外面的基础设施，用来管理 long-running tasks。原文强调它“不是 agent 本身”，而是 governs how the agent operates 的那层软件系统，目标是让 agent 的运行更 `reliable`、`efficient`、`steerable`。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-definition|definition]]

## 帮助理解的类比

- `Model = CPU`
- `Context Window = RAM`
- `Agent Harness = Operating System`
- `Agent = Application`  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-computer-analogy|computer analogy]]

这个类比对应的意思是：`agent harness` 更像运行环境和治理层，负责 context、boot sequence 和 `tool handling`；上层具体 agent 更像跑在这层环境上的 application。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-computer-analogy|computer analogy]]

## 原文里的要求

- 它应该提供一套比 `agent framework` 更完整的运行能力，例如 prompt presets、tool-call handling、lifecycle hooks、planning、filesystem access、sub-agent management。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-vs-framework|framework contrast]]
- 它应该实现 `context engineering` 策略，例如 context compaction、state offloading、task isolation。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-implements-context-engineering|implements context engineering]]
- 它应该把长任务 agent workflow 变成可 `log and grade` 的 structured data，让系统能被记录、验证和持续优化。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-benchmark-gap|benchmark gap]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-log-and-grade|log and grade]]
- 它应该保持 lightweight，并允许开发者删掉旧的“smart logic”，避免把任务智能过多固化成僵硬 workflow。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-bitter-lesson|bitter lesson]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-start-simple|start simple]]

## Sources

- [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]
