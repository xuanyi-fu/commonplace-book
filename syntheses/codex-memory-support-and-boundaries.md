---
type: synthesis
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# Codex Memory 的实现概览

截至 `2026-04-20`，如果只从实现上看，Codex memory 不是一个“模型自动记住一切”的黑盒能力，而是一条相当明确的本地 pipeline：先挑选合适的旧线程，再做单线程抽取，再把抽取结果落到 sqlite，随后同步成 memory 工作区文件，最后再由一个专门的 consolidation subagent 维护真正给未来线程使用的 `MEMORY.md` 和 `memory_summary.md`。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]]

## 工作判断

今天这套实现最重要的判断不是“Codex 支不支持 memory”，而是：

- 它已经有完整的 memory pipeline，但这条 pipeline 仍然很工程化，也很初级。
- 它依赖显式筛选、离线提取、文件中间层和二次 consolidation，而不是一个统一的、实时更新的长期记忆系统。
- 它真正成熟的部分是“可控的本地状态层”，而不是“强泛化的自动记忆能力”。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]

## 整体架构

从代码结构看，memory 的主体不在 `app-server`，而是在 `core` 和 `state`。

- `app-server`
  - 主要暴露控制接口，例如 `thread/memoryMode/set` 和 `memory/reset`
  - 更像控制面，不是 memory 抽取和合并本身 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]
- `state`
  - 负责线程筛选、job claim、sqlite 持久化、phase-2 选择快照、`polluted` 标记等状态管理 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]
- `core`
  - 负责 pipeline 调度、phase-1 模型调用、phase-2 文件同步、consolidation subagent 启动，以及未来线程里的 memory prompt 注入 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

这意味着，如果只看产品 UI，会以为 memory 是一个简单开关；但如果看实现，它其实是 `thread selection -> phase 1 extraction -> sqlite -> filesystem sync -> phase 2 consolidation -> prompt injection` 这样一条多阶段链路。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

## 触发与筛选

memory 不是在线程结束时立刻写盘。它是在一个新的 root session 启动时，异步触发 startup task，然后按顺序跑 `phase1::prune`、`phase1::run`、`phase2::run`。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

真正能进入这条链路的线程还要先过筛：

- 必须是 `memory_mode = enabled`
- 不能是当前线程
- 必须落在线程年龄窗口内
- 必须已经 idle 到足够久
- 已有的 stage-1 输出或 job watermark 不能已经覆盖这个线程的最新状态 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

所以更准确的理解不是“thread 结束后被记住”，而是“thread 在后续某次会话启动时，如果已经冷却且仍然 eligible，才会被后台抽取成 memory 源”。

## Phase 1：单线程抽取，而不是 agent

`Phase 1` 的职责是把单个 rollout 变成一个 stage-1 output。这里最容易误解的一点是：它不会起新的 agent，也不会创建新的 thread。[[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]]

实现上它更像一次内部的单轮结构化抽取调用：

- 读取 rollout `.jsonl`
- 过滤出 memory-relevant response items
- 用固定模板构造 prompt
- 不带 tools，要求输出命中固定 JSON schema
- 返回 `raw_memory`、`rollout_summary`、`rollout_slug`
- 做 secret redaction
- 把结果写回 sqlite 的 `stage1_outputs` [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]]

如果用更贴近产品的语言，它更像一次“summary / extraction 风格的 Responses 调用”，而不是 agent loop。[[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]]

## Stage-1 Output 是什么

通过 `Phase 1` 之后，每个合格线程会得到一个 stage-1 output。它可以被理解成一种中间层 structured data，但这个 structured data 不是纯 JSON 对象结束就完了，而是：

- sqlite 里有结构化字段
- `raw_memory` 自己又是一段有固定写作约束的 markdown 文本 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-stage-one-system|stage_one_system prompt]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-stage-one-input|stage_one_input prompt]]

因此，“memory 被沉淀成文件”之前，先发生的其实是“memory 被沉淀成 sqlite 里的 stage-1 outputs”。

## Phase 2：先同步文件，再起全局 consolidation agent

`Phase 2` 才是这套系统真正把中间层变成 durable memory 的地方。这里也有一个关键澄清：它不是把 `stage1_outputs` 简单拼成一段输入文本，然后直接丢给 agent。[[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]]

它实际分两步：

- Rust 先把 sqlite 里的 stage-1 outputs 同步成文件系统里的 `raw_memories.md` 和 `rollout_summaries/*.md`
- 然后再起一个全局 consolidation subagent，让它在 memory root 这个目录里工作，去维护 `MEMORY.md`、`memory_summary.md` 和可选 `skills/` [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|consolidation prompt]]

也就是说，phase-2 agent 看到的是一个已经准备好的 memory 工作区，而不是一条平面的文本输入。

## 四层 memory 文件各干什么

这套实现里真正容易被低估的，是它故意保留了多层文件，而不是只写一个 `MEMORY.md`。

- `raw_memories.md`
  - 机械合并的 stage-1 raw memories
  - 是 phase-2 的临时输入层，不是给未来线程直接默认消费的成品 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|consolidation prompt]]
- `rollout_summaries/*.md`
  - 每个 retained rollout 一份 recap
  - 保留 thread 级别的来源、证据和路径，用来给 consolidation 和后续检索提供中间证据层 [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]
- `MEMORY.md`
  - 真正的详细知识库 / searchable registry
  - 是 task-grouped 的 durable handbook，不追求被直接整页注入，而追求可检索、可 grep、可复用 [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|consolidation prompt]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-read-path|read_path prompt]]
- `memory_summary.md`
  - 顶层路由层
  - 这是未来线程默认直接看到的 memory 首页，用来快速路由到 `MEMORY.md`、`skills/` 或 `rollout_summaries/` [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|consolidation prompt]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-read-path|read_path prompt]]

所以 `memory_summary.md` 和 `MEMORY.md` 的关系，不是“一个简略版，一个详细版”这么简单，而是“一个是默认注入的导航层，一个是主知识库”。

## 未来线程怎么用到 memory

未来线程并不是把旧聊天全文拼回上下文。实际做法是：在 developer instructions 里注入一段 memory prompt，而这段 prompt 的核心输入是 `memory_summary.md`。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-read-path|read_path prompt]]

这意味着：

- 默认直接进上下文的是 `memory_summary.md`
- `MEMORY.md` 是后续检索主库
- `rollout_summaries/*.md` 和 `skills/` 是再下一层的证据或程序层

这套设计本身就说明，Codex 团队没有把 memory 实现成“统一的一大段长期记忆文本”，而是实现成了“默认路由层 + 主检索层 + 中间证据层”的分层结构。

## `app-server` 为什么看起来能力很少

如果从用户视角看，memory 相关功能好像就几个开关，这其实正反映了 `app-server` 的定位。它主要负责：

- 暴露线程级 `memory_mode` 控制
- 暴露 `memory/reset`
- 接收 UI 的实验 API 请求

它不负责：

- 挑线程
- 跑 phase 1
- 跑 phase 2
- 维护 `MEMORY.md`
- 注入 read-path prompt [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

所以从实现角度看，`app-server` 在这套系统里确实只是壳，不是核心。

## `Skip tool-assisted chats` 的实现含义

UI 里的 `Skip tool-assisted chats` 不是一个表层开关，它在实现上对应的是：当线程包含 MCP / web search 这类外部上下文时，线程会被标成 `polluted`，并且在必要时触发一次全局 consolidation 去移除旧基线里受污染的 memory。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

这说明 Codex 团队对 memory 的一个核心约束是：它宁可少记，也不想把带外部上下文污染的线程直接推进 durable memory。

## Chronicle 在这套实现里的位置

`Chronicle` 仍然是 memory 体系的一部分，但不应该拿来替代 ordinary memory 的实现理解。ordinary memory 的主体实现，是上面这条 `selection -> phase 1 -> sqlite -> filesystem sync -> phase 2 -> prompt injection` pipeline。[[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]]

`Chronicle` 更像一个上游增强层：它通过屏幕上下文为 memory 生成补充输入，但它解决的第一问题还是“近期上下文恢复”，不是这条 ordinary memory pipeline 本身。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]

## 一个更准确的结论

如果把今天的 Codex memory 用一句话概括，我会写成：

`Codex memory 已经有一条完整但仍然初级的本地实现链路：它会筛选旧线程，用单轮抽取生成 stage-1 outputs，再同步成 memory 工作区，并通过一个全局 consolidation subagent 维护分层的 memory 文件；未来线程默认消费的是 memory_summary 这个路由层，而不是一份无结构的长期记忆全文。` [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|实现笔记]] [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|补充澄清]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|consolidation prompt]] [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-read-path|read_path prompt]]

## Sources

- [[sources/codex-memory-implementation-2026-04/source/local-code-reading-codex-memory-pipeline-2026-04-20|local-code-reading-codex-memory-pipeline-2026-04-20]]
- [[sources/codex-memory-implementation-2026-04/source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|local-followup-clarifications-codex-memory-pipeline-2026-04-20]]
- [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-stage-one-system|openai-codex-d62421d-memory-stage-one-system]]
- [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-stage-one-input|openai-codex-d62421d-memory-stage-one-input]]
- [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-consolidation|openai-codex-d62421d-memory-consolidation]]
- [[sources/codex-memory-implementation-2026-04/source/openai-codex-d62421d-memory-read-path|openai-codex-d62421d-memory-read-path]]
- [[sources/codex-memory-2026-04/source/official-doc-codex-memories|official-doc-codex-memories]]
- [[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|official-doc-codex-chronicle]]
