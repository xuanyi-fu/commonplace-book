---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# ai-scientist-2026-04

这个 source collection 收集了截至 2026-04-21 可见的 AiScientist 一手材料，重点回答一个具体问题：`AiScientist` 的架构到底是怎样组织的，包括它的控制层、状态层、工作区、specialist / subagent 分层，以及这些概念在公开仓库里如何落地。

## Structure

- `source/arxiv-2604-13018-paper.pdf`: AiScientist 论文原始 PDF
- `source/arxiv-2604-13018-html.html`: arXiv HTML 版论文原文
- `source/official-repo-readme.md`: 官方仓库原始 README
- `source/src-aisci-app-cli.py`: 公开仓库 CLI 入口源码
- `source/src-aisci-core-runner.py`: 公开仓库 job runner 源码
- `source/src-aisci-domain-mle-orchestrator.py`: MLE orchestrator 源码
- `source/src-aisci-domain-mle-orchestrator-runtime.py`: MLE runtime paths / config 源码
- `source/src-aisci-domain-mle-subagents-configs.py`: MLE subagent 配置源码
- `source/src-aisci-domain-mle-tools-spawn-subagent-tool.py`: generic subagent tool 源码
- `source/config-paper-subagents.yaml`: paper 侧 subagent 配置原文
- `source/arxiv-paper-long-horizon-engineering-for-ml-research.md`: 基于论文原文整理的 architecture note
- `source/official-repo-readme-architecture-overview.md`: 基于官方 README 整理的 runtime shape note
- `source/official-repo-code-reading-module-layout-and-runtime.md`: 基于公开仓库代码整理的实现层笔记
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 想核对原始材料时，优先看 `pdf / html / md / py / yaml` 这些 raw source
- 想快速建立心智模型时，先读 3 份 cleaned notes：
  - `source/arxiv-paper-long-horizon-engineering-for-ml-research.md`
  - `source/official-repo-readme-architecture-overview.md`
  - `source/official-repo-code-reading-module-layout-and-runtime.md`
- 再回跳到对应 raw source，检查具体论断和实现细节
- 讨论时要把三层分开：
  - `architecture thesis`：论文里讲的系统原则
  - `product/runtime shape`：README 里公开承诺的运行方式
  - `public implementation surface`：当前仓库代码里已经清楚暴露出来的控制面、工作区和 subagent 结构

## Summary

截至 2026-04-21，这个 collection 现在同时保留了 raw source 和 cleaned notes 两层材料。公开材料支持一个相当清楚的架构判断：AiScientist 不是单个“科研 agent”，而是一个围绕 `durable project state` 组织起来的研究工程系统。它的核心原则是 `thin control over thick state`：Tier-0 `Orchestrator` 只保留阶段级控制、简短总结和 `workspace map`，不试图把完整项目历史塞进当前上下文；真正厚重的状态被外置到 permission-scoped workspace 里，并通过 `File-as-Bus` 在不同 agent 之间传递。论文把系统划成 Tier-0 orchestrator、Tier-1 specialists、Tier-2 scoped subagents 三层；README 则把这套设计具体化为 “stage workspace -> launch sandbox -> orchestrator dispatch -> specialists read/write artifacts -> leave inspectable run” 这条主流程。公开仓库进一步表明，系统至少已经分成 `aisci_app`、`aisci_core`、`aisci_agent_runtime`、domain adapter / orchestrator / subagents 这几层，并通过 `/home/data`、`/home/code`、`/home/submission`、`/home/agent`、`/home/logs` 这组共享路径把工作区变成运行时的系统记录。对理解 AiScientist 而言，最关键的不是“多 agent”四个字，而是它如何用 `workspace artifacts` 取代脆弱的 conversational handoff。

## Sources

- [[source/arxiv-2604-13018-paper|arxiv-2604-13018-paper.pdf]]
- [[source/arxiv-2604-13018-html|arxiv-2604-13018-html.html]]
- [[source/official-repo-readme|official-repo-readme.md]]
- [[source/src-aisci-app-cli|src-aisci-app-cli.py]]
- [[source/src-aisci-core-runner|src-aisci-core-runner.py]]
- [[source/src-aisci-domain-mle-orchestrator|src-aisci-domain-mle-orchestrator.py]]
- [[source/src-aisci-domain-mle-orchestrator-runtime|src-aisci-domain-mle-orchestrator-runtime.py]]
- [[source/src-aisci-domain-mle-subagents-configs|src-aisci-domain-mle-subagents-configs.py]]
- [[source/src-aisci-domain-mle-tools-spawn-subagent-tool|src-aisci-domain-mle-tools-spawn-subagent-tool.py]]
- [[source/config-paper-subagents|config-paper-subagents.yaml]]
- [[source/arxiv-paper-long-horizon-engineering-for-ml-research|arxiv-paper-long-horizon-engineering-for-ml-research.md]]
- [[source/official-repo-readme-architecture-overview|official-repo-readme-architecture-overview.md]]
- [[source/official-repo-code-reading-module-layout-and-runtime|official-repo-code-reading-module-layout-and-runtime.md]]
