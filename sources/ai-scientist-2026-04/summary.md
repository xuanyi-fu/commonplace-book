---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# ai-scientist-2026-04

这个 source collection 收集了截至 2026-04-21 可见的 AiScientist 一手材料，重点回答一个具体问题：`AiScientist` 的架构到底是怎样组织的，包括它的控制层、状态层、工作区、specialist / subagent 分层，以及这些概念在公开仓库里如何落地。

## Structure

- `source/arxiv-paper-long-horizon-engineering-for-ml-research.md`: arXiv 论文整理，重点记录方法部分对 `thin control over thick state`、`File-as-Bus`、分层编排和 evidence-driven loop 的定义
- `source/official-repo-readme-architecture-overview.md`: 官方仓库 README 的架构要点，重点记录 “How It Works”“Two Tracks”“What Lands On Disk” 这几部分
- `source/official-repo-code-reading-module-layout-and-runtime.md`: 直接根据官方仓库公开代码做的实现层笔记，重点对应 `CLI / core / agent runtime / domain adapter / orchestrator / subagents / workspace paths`
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/arxiv-paper-long-horizon-engineering-for-ml-research.md`，它最适合建立 AiScientist 的总体心智模型
- 再读 `source/official-repo-readme-architecture-overview.md`，把论文里的方法论对上公开系统的运行方式、双 track 设计和落盘工件
- 最后读 `source/official-repo-code-reading-module-layout-and-runtime.md`，看这些设计在公开仓库里分别落到了哪些模块和路径
- 讨论时要把三层分开：
  - `architecture thesis`：论文里讲的系统原则
  - `product/runtime shape`：README 里公开承诺的运行方式
  - `public implementation surface`：当前仓库代码里已经清楚暴露出来的控制面、工作区和 subagent 结构

## Summary

截至 2026-04-21，公开材料支持一个相当清楚的架构判断：AiScientist 不是单个“科研 agent”，而是一个围绕 `durable project state` 组织起来的研究工程系统。它的核心原则是 `thin control over thick state`：Tier-0 `Orchestrator` 只保留阶段级控制、简短总结和 `workspace map`，不试图把完整项目历史塞进当前上下文；真正厚重的状态被外置到 permission-scoped workspace 里，并通过 `File-as-Bus` 在不同 agent 之间传递。论文把系统划成 Tier-0 orchestrator、Tier-1 specialists、Tier-2 scoped subagents 三层；README 则把这套设计具体化为 “stage workspace -> launch sandbox -> orchestrator dispatch -> specialists read/write artifacts -> leave inspectable run” 这条主流程。公开仓库进一步表明，系统至少已经分成 `aisci_app`、`aisci_core`、`aisci_agent_runtime`、domain adapter / orchestrator / subagents 这几层，并通过 `/home/data`、`/home/code`、`/home/submission`、`/home/agent`、`/home/logs` 这组共享路径把工作区变成运行时的系统记录。对理解 AiScientist 而言，最关键的不是“多 agent”四个字，而是它如何用 `workspace artifacts` 取代脆弱的 conversational handoff。

## Sources

- [[source/arxiv-paper-long-horizon-engineering-for-ml-research|arxiv-paper-long-horizon-engineering-for-ml-research.md]]
- [[source/official-repo-readme-architecture-overview|official-repo-readme-architecture-overview.md]]
- [[source/official-repo-code-reading-module-layout-and-runtime|official-repo-code-reading-module-layout-and-runtime.md]]
