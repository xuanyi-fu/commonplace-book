---
type: synthesis
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# AiScientist 的 File-as-Bus 状态层与上下文流动

AiScientist 的 `File-as-Bus` 不应该被理解成“把聊天记录保存成几个 markdown 文件”。更准确的说法是：它把长程研究工程里的关键项目状态对象化、文件化、角色化，然后让不同 agent 围着这些 durable artifacts 协作。论文把这套方法概括成 `thin control over thick state`，公开仓库则把它具体落实成 `/home/data`、`/home/code`、`/home/submission`、`/home/agent`、`/home/logs` 这组共享路径，以及一套明确的 specialist / subagent 写入与读取约定。[[sources/ai-scientist-2026-04/source/arxiv-paper-long-horizon-engineering-for-ml-research|AiScientist 论文整理]] [[sources/ai-scientist-2026-04/source/official-repo-readme-architecture-overview|README 架构整理]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]

## 先分清两种“总结”

AiScientist 里至少有两种完全不同的总结机制。

第一种是 `workspace artifacts`。这是真正的 `File-as-Bus`。它由业务角色显式写入，例如 `analysis/summary.md`、`prioritized_tasks.md`、`impl_log.md`、`exp_log.md`、`submission_registry.jsonl`。这些文件是共享项目状态，不是临时压缩聊天。[[sources/ai-scientist-2026-04/source/official-repo-readme-architecture-overview|README 架构整理]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]

第二种是 `conversation summarization`。当主 agent 或 subagent 命中 `ContextLengthError` 时，运行时会把较早的完整 turn 总结成一段 `Essential Information`，再把这段 summary 作为新的 user message 塞回当前 message list 里继续推理。这是消息裁剪策略，不是 workspace 本体。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-subagents-configs|subagents/configs.py]]

所以如果抓一句话：

`File-as-Bus 是项目状态层；conversation summary 是上下文压缩层。`

## File-as-Bus 里到底有哪些状态

当前公开实现里，MLE 路径最关键的状态文件主要有这些：

- `/home/agent/analysis/summary.md`
  数据分析总结，是后续 planning、implementation、experiment 的共同输入。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]] [[sources/ai-scientist-2026-04/source/official-repo-code-reading-module-layout-and-runtime|代码阅读整理]]
- `/home/agent/prioritized_tasks.md`
  优先级执行契约，定义 P0-P3 任务顺序。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]] [[sources/ai-scientist-2026-04/source/official-repo-code-reading-module-layout-and-runtime|代码阅读整理]]
- `/home/agent/impl_log.md`
  实现变更日志，记录每轮改动摘要、文件、commit 和额外说明。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]
- `/home/agent/exp_log.md`
  实验结果日志，记录 status、metrics、error、diagnosis、log path。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]
- `/home/agent/experiments/<task_id>/<run_id>.log`
  长实验的原始输出日志。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- `/home/submission/submission.csv`
  当前有效提交文件。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]
- `/home/submission/candidates/`
  每次 `implement` 或 `run_experiment` 之后的 immutable snapshot。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- `/home/submission/submission_registry.jsonl`
  snapshot registry 和 candidate metadata。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- `/home/agent/summary.json`
  run 结束时写出的轻量统计摘要，例如 runtime、token、impl/exp 调用次数、submission 是否存在。它不是 bus 的核心工件，但属于系统保留下来的运行状态。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]] [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]

README 对 paper track 还暴露了 `paper_analysis/*`、`final_self_check.md/json`、`reproduce.sh` 这类更偏复现流程的工件，说明 File-as-Bus 不是只服务 MLE，而是服务两个长程 workload。[[sources/ai-scientist-2026-04/source/official-repo-readme-architecture-overview|README 架构整理]]

## 这些状态不是“自动记下来”的，而是被角色化写出来的

AiScientist 的关键不是后台自动做 memory extraction，而是每个 specialist 的 prompt 和 tool interface 直接规定了它要留下什么文件。

- `analysis` subagent 的任务就是分析 competition data，并把结果写到 `/home/agent/analysis/summary.md`。[[sources/ai-scientist-2026-04/source/official-repo-code-reading-module-layout-and-runtime|代码阅读整理]]
- `prioritization` subagent 明确以 `description.md` 和 `analysis/summary.md` 为输入，产出 `/home/agent/prioritized_tasks.md`。[[sources/ai-scientist-2026-04/source/official-repo-code-reading-module-layout-and-runtime|代码阅读整理]]
- `implementation` subagent 的主要输出当然是代码，但它还被显式要求调用 `add_impl_log` 把关键实现变化追加写入 `/home/agent/impl_log.md`。这不是可选优化，而是 prompt 里写明的工作协议。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- `experiment` subagent 同样被要求调用 `add_exp_log` 把实验结果写入 `/home/agent/exp_log.md`，并把长实验原始输出落到 `/home/agent/experiments/`。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- 主 orchestrator 则在每次 `implement` / `run_experiment` 后自动 snapshot `submission.csv` 到 `candidates/`，再把 snapshot metadata append 到 `submission_registry.jsonl`。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]

因此这条链路更像：

`角色获得上下文 -> 在本地 horizon 内工作 -> 通过专用 tool 把结果写成 durable file -> 文件成为下一轮共享状态`

而不是：

`系统自动把整段历史总结成一个 memory blob`

## 这些状态怎样重新进入别的 agent 的 context

File-as-Bus 的另一个关键不是“写出来”，而是“怎么读回去”。AiScientist 在这里做的是 `targeted reinjection`，而不是让下游 agent 继承所有历史。

- `prioritization` 会显式读取 `analysis/summary.md` 来形成任务合同。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- `implementation` 会读取 `prioritized_tasks.md` 来做 breadth-first 实现。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- 当 `implementation` 进入 `fix` 路径时，它会从 `exp_log.md` 里只截取**最近一段 experiment session**注入自己的 context，而不是把全部实验历史读进来。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]
- 对称地，`experiment` 会从 `impl_log.md` 里只截取**最近一段 implementation session**作为验证上下文。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|orchestrator.py]]

这意味着它的状态流动并不是“所有 agent 共享一个超级大 context”，而是：

`共享状态持久落盘 -> orchestrator 选择相关片段 -> 只把当前阶段最相关的一段 reinject 到下游 agent`

这正是论文说的 `progressive disclosure`：顶层控制始终保持轻量，只有在需要时才展开厚状态。[[sources/ai-scientist-2026-04/source/arxiv-paper-long-horizon-engineering-for-ml-research|AiScientist 论文整理]]

## permission-scoped 的含义不是抽象口号，而是路径和职责约束

在公开常量表里，不同 agent 能看到的 workspace reference 其实是不同的：

- 主 orchestrator 看到完整状态面，包括 `analysis`、`prioritized_tasks`、`impl_log`、`exp_log`、`submission_registry`、`candidates`。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]
- implementation 视角里，`/home/code/` 是“你的工作区”，`impl_log.md` 是“你 via add_impl_log 维护的 changelog”，而 `exp_log.md` 是 experiment subagent 维护的结果日志。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]
- experiment 视角里，`impl_log.md` 是它要先读的上游改动记录，`exp_log.md` 则是它自己继续 append 的实验日志。[[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|orchestrator_runtime.py]]

这说明 `permission-scoped workspace` 在实现上不是一个抽象哲学，而是“不同角色有不同的工作参考表、不同的主要写入文件、不同的协作边界”。

## 为什么它比普通 chat summary 更适合长程闭环

单纯的 chat summary 最大的问题是：它倾向于把“过程”压成“叙述”。但研究工程真正需要传递的，往往不是一句“我们试过 X 失败了”，而是：

- 改了哪些文件
- 用了哪条命令
- 跑了哪个 experiment
- 指标是多少
- 失败发生在哪个阶段
- 下一轮 fix 应该针对什么

AiScientist 的 `impl_log.md` 和 `exp_log.md` 之所以有用，正是因为它们不是普通 narrative summary，而是面向协作闭环设计的结构化工件：

- `impl_log.md` 保留 code-side decision lineage
- `exp_log.md` 保留 executable evidence 和 diagnosis
- `submission_registry.jsonl` 保留 candidate lineage
- `experiments/*.log` 保留可追溯原始输出

所以它真正保存下来的不是“说过什么”，而是“项目状态如何演化”。这也是论文把它称作 `system of record` 的原因。[[sources/ai-scientist-2026-04/source/arxiv-paper-long-horizon-engineering-for-ml-research|AiScientist 论文整理]] [[sources/ai-scientist-2026-04/source/official-repo-readme-architecture-overview|README 架构整理]]

## 一个更准确的结论

如果把这套机制压成一句话，我会写成：

`AiScientist 的 File-as-Bus 不是“把上下文存下来”，而是“把长程研究工程里的关键状态做成可写、可读、可追溯、可定向重注入的共享文件层”。`

这套设计真正解决的不是 memory 容量问题，而是长程协作里的三个更难的问题：

- 状态怎样跨 agent 持续存在
- 状态怎样避免被一次次 message handoff 压扁
- 状态怎样只在需要时被相关角色重新拉回 context

## Sources

- [[sources/ai-scientist-2026-04/source/arxiv-paper-long-horizon-engineering-for-ml-research|arxiv-paper-long-horizon-engineering-for-ml-research]]
- [[sources/ai-scientist-2026-04/source/official-repo-readme-architecture-overview|official-repo-readme-architecture-overview]]
- [[sources/ai-scientist-2026-04/source/official-repo-code-reading-module-layout-and-runtime|official-repo-code-reading-module-layout-and-runtime]]
- [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator-runtime|src-aisci-domain-mle-orchestrator-runtime.py]]
- [[sources/ai-scientist-2026-04/source/src-aisci-domain-mle-orchestrator|src-aisci-domain-mle-orchestrator.py]]
