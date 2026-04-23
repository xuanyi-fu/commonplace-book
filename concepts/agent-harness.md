---
type: concept
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Agent Harness

`agent harness` 在 Philipp Schmid 2026-01 这篇文章里的核心定义是：它是包在 AI model 外面的基础设施，用来管理 long-running tasks。原文强调它“不是 agent 本身”，而是 governs how the agent operates 的那层软件系统，目标是让 agent 的运行更 `reliable`、`efficient`、`steerable`。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## 这个定义主要在说什么

- 它不是 model。本体推理能力仍然来自 model；`agent harness` 是包在 model 外面的运行层。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- 它也不是 agent 本身。原文明确写的是 “It is not the agent itself.” 更准确地说，它是治理 agent 如何运行的系统层。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- 它关注的不是单次回答，而是 long-running task 中的持续运行质量，例如长时间 tool use 后还能否维持稳定、可控和高效。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## Philipp Schmid 给出的类比

这篇文章把几层东西类比成一台计算机：

- `Model = CPU`
- `Context Window = RAM`
- `Agent Harness = Operating System`
- `Agent = Application`  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

这个类比最重要的含义不是修辞，而是边界：

- `agent harness` 更像运行环境和治理层，而不是某个具体任务目标
- 它负责 `curates the context`、boot sequence、`tool handling` 这类更像 OS 的职责
- 上层具体 agent 更像跑在这层环境上的 application  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## 它通常包含什么

按照 Philipp Schmid 这篇文章的说法，`agent harness` 比 `agent framework` 更高一层。后者更像 building blocks 或 agentic loop 的基础实现；前者则额外提供：

- prompt presets
- opinionated handling for tool calls
- lifecycle hooks
- planning
- filesystem access
- sub-agent management  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

因此像 `computer use`、网页浏览 skill、filesystem access 这种能力，本身更适合看成 harness 提供给上层 agent 的 capability / tool surface，而不是 agent 本身。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]] [[sources/agent-harness-origins-2023-2026/source/context-engineering-for-ai-agents-part-2-markdown|Context Engineering for AI Agents: Part 2]]

## 它和 Context Engineering 的关系

在这个概念下，`context engineering` 不是 `agent harness` 的同义词。更接近的关系是：

- `context engineering` 是一组用来组织信息、工具和状态的策略
- `agent harness` 是把这些策略真正实现并施加到 agent 运行过程中的系统载体

Philipp Schmid 在 2026-01 这篇里直接写的是：`The Agent harness implements Context Engineering strategies`，例如 context compaction、把 state offload 到 storage、把任务隔离到 sub-agent。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## 它还需要可记录和可优化

如果继续按 Philipp Schmid 2026-01 这篇往下读，`agent harness` 还有一个很重要的要求：它不只是让 agent 能跑起来，还要把长任务中的行为变成可记录、可验证、可评分的结构化对象。文章在 `The Benchmark Problem and the need for Agent Harnesses` 这一节里强调，传统 benchmark 很难测出第 50 次、第 100 次 tool call 之后的 `reliability` 问题，因此 harness 的价值之一，就是把原本模糊的 multi-step workflow 变成可以 `log and grade` 的 structured data。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

这意味着，一个好的 `agent harness` 不只是运行层，也应该提供足够的可观测性和结构化反馈面，让开发者可以：

- 记录 agent 在长任务里的真实行为轨迹
- 验证结果是否满足约束
- 比较不同模型或不同系统配置的表现
- 把失败轨迹反过来作为后续优化 harness 的依据  
  [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## 暂定判断

如果只按这个 source 来定义，`agent harness` 最好不要被理解成“一个会调用工具的 agent”，而应该理解成“包在 model 外面的运行基础设施”。它负责把单纯会输出 token 的 model，变成能够在有限 `context window`、真实工具和长任务约束下持续工作的 agent system。[[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

在这个意义上，`Claude Code`、`Codex CLI` 这类 coding CLI 更接近 specialized agent harness，而不是这里所说的上层 agent 本身。这个判断主要来自 Philipp Schmid 在文中的表述：“Currently, general-purpose harnesses are rare. Claude Code is a prime example ... all coding CLIs are, in a way, specialized agent harnesses designed for specific verticals.” [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]

## Sources

- [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown|The importance of Agent Harness in 2026]]
- [[sources/agent-harness-origins-2023-2026/source/context-engineering-for-ai-agents-part-2-markdown|Context Engineering for AI Agents: Part 2]]
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]
