---
type: synthesis
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Multica 的共享项目状态层，以及它和 AiScientist 的差别

如果只回答一句话，我会说：`是的，Multica 也在解决 agent 之间的“共享项目状态”问题；但它解决的层级，不是 AiScientist 那种 artifact-centric 的 File-as-Bus，而是 task platform / session resumption / execution-environment rehydration 这一层。`[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]]

## 先说结论：它们确实在解决同一个大问题

AiScientist 和 Multica 都在回答同一个根问题：

`当一个复杂任务不会在单轮对话里结束时，系统怎样让后续 agent 接得住前面的工作。`

只是两者选的“状态载体”完全不同。

- AiScientist 选的是 workspace 里的 durable artifacts，例如 `analysis/summary.md`、`impl_log.md`、`exp_log.md`、`submission_registry.jsonl`。[[syntheses/ai-scientist-file-as-bus-state-and-context-flow|AiScientist 的 File-as-Bus 状态层与上下文流动]]
- Multica 选的是平台对象和恢复指针，例如 `workspace`、`issue`、`comment`、`agent`、`skill`、`agent_task_queue.session_id/work_dir`、`chat_session.session_id/work_dir`，再加 daemon 每次为 agent 重建出来的 workdir。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/020_task_session.up.sql|020_task_session.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/033_chat.up.sql|033_chat.up.sql]]

所以如果非要类比：

- AiScientist 更像 `shared artifact state`
- Multica 更像 `shared platform state + resume state`

## 在 Multica 里，哪些东西算“共享项目状态”

从当前公开代码看，Multica 的共享项目状态至少有 4 层。

第一层是 `workspace` 级状态：

- `workspace.context`
- `workspace.repos`
- workspace 里的 `agents`
- workspace 里的 `skills`

这些东西决定了这个工作区里 agent 理论上能看到什么、能访问什么 repo、有哪些可复用技能。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/006_workspace_context.up.sql|006_workspace_context.up.sql]]

第二层是 `issue / collaboration object` 级状态：

- `issue`
- `comment`
- `activity_log`
- `issue_subscriber`
- `attachment`

这层才是“多个 agent 围绕同一个项目对象协作”的核心。SQL 里甚至明确写了：同一个 issue 上，不同 agent 可以并行工作；只是同一个 agent 不会在同一个 issue 上重复并发。[[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|001_init.up.sql]]

第三层是 `task / session continuation` 级状态：

- `agent_task_queue.session_id`
- `agent_task_queue.work_dir`
- `trigger_comment_id`
- `chat_session_id`
- `autopilot_run_id`
- chat 路径下的 `chat_session.session_id/work_dir`

这层不是项目内容本身，而是“这次执行怎样接上上次执行”。它解决的是 continuity，不是业务事实本身。[[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]]

第四层是 `execution environment` 级状态：

- `.agent_context/issue_context.md`
- provider-native `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
- provider-native skills 目录
- 本地 workdir 本身

这层是 daemon 把平台对象重新投影到 agent 本地工作现场之后的产物。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|context.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/execenv.go|execenv.go]]

## Multica 的状态流，不是“聊天总结成文件”，而是“平台状态重建成执行环境”

Multica 的关键流动大致是这样的：

1. 人或 agent 在平台上创建 / 更新 `issue`、`comment`、`chat_session` 这些 canonical objects。[[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|001_init.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/033_chat.up.sql|033_chat.up.sql]]
2. 这些对象触发 `agent_task_queue` 里的 task。issue assignment、`@agent` comment、chat message、autopilot 都会落到 task queue。[[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]]
3. daemon claim task 时，server 会把当前需要的上下文拼成一个 `Task` response：
   - `workspace_id`
   - `repos`
   - agent `instructions`
   - skills
   - `trigger_comment_content`
   - `chat_message`
   - `prior_session_id`
   - `prior_work_dir`[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/agent.go|agent.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/types.go|types.go]]
4. daemon 拿到这个 `Task` 以后，会：
   - 复用或新建 workdir
   - 写 `.agent_context/issue_context.md`
   - 写 provider-native runtime config
   - 安装 skill 文件
   - 把 `ResumeSessionID` 传给底层 CLI backend[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/execenv.go|execenv.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|context.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]]
5. 真正厚的业务信息并不全靠这份响应携带；prompt 反而很薄，明确要求 agent 先跑 `multica issue get ... --output json` 去平台读最新状态。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/prompt.go|prompt.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]]
6. task 完成或失败后，再把 `result`、`session_id`、`work_dir`、`task_message`、comment 写回平台对象层；chat 路径还会事务性更新 `chat_session.session_id/work_dir`。[[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]]

这条链路的重点是：

`Multica 不是把共享状态长期保存在 prompt 里，而是把共享状态长期保存在平台对象里，再在每次执行时重建最小必要执行环境。`

## 它和 AiScientist 最像的地方

两者最像的不是“都有 memory”，而是都不相信“把所有历史塞进单个 prompt”这条路。

AiScientist 的做法是：

- 厚状态落到文件工件
- 下游 agent 按需读这些工件
- orchestrator 只做轻控制[[syntheses/ai-scientist-file-as-bus-state-and-context-flow|AiScientist 的 File-as-Bus 状态层与上下文流动]]

Multica 的做法是：

- 厚状态落到平台对象和 session 指针
- agent 每轮通过 CLI 回平台取最新状态
- daemon 只做 workdir / skills / runtime config / resume 的重建[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/prompt.go|prompt.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]]

所以两者都在做一件反 prompt-centric 的事：

`把协作连续性外化到系统别处。`

只是外化到哪里不同。

## 它和 AiScientist 最不一样的地方

最不一样的是“系统把什么当成 system of record”。

AiScientist 里，system of record 更像是 workspace artifacts：

- `analysis/summary.md`
- `impl_log.md`
- `exp_log.md`
- `submission_registry.jsonl`

这些文件本身就是项目状态。[[syntheses/ai-scientist-file-as-bus-state-and-context-flow|AiScientist 的 File-as-Bus 状态层与上下文流动]]

Multica 里，system of record 更像是平台对象：

- issue 是任务事实
- comments 是协作事实
- skills 是 reusable process fact
- session_id / work_dir 是 continuation fact
- task_message 是执行流水

workdir 只是这些平台状态的本地执行投影，不是唯一真相源。[[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|001_init.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]]

所以更尖锐一点地说：

- AiScientist 更像 `artifact bus`
- Multica 更像 `workflow object bus`

## 一个很重要的保留意见

这次代码阅读里有两个点需要特别保守，不该说得过头。

第一，`workspace.context`。

它在 schema 和产品文档里都是明确存在的，官方文档也把它定义成“所有该 workspace 的 agent 都会感知到”的统一系统提示。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/006_workspace_context.up.sql|006_workspace_context.up.sql]]

但在当前公开代码里，我暂时只明确看到它被 CRUD 出来，还没有找到它被注入 daemon prompt、`Task` response、`execenv`、或 runtime config 的直接路径。[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/workspace.go|workspace.go]]

所以今天最严谨的表述只能是：

`workspace.context 是一个明确存在的 workspace-level state surface，但它在当前公开代码里的执行时注入路径，还不能仅凭这批 source 直接坐实。`

第二，`agent_task_queue.context`。

migration 明确加了这个字段，但当前 `EnqueueTaskForIssue` 代码又明确写着：issue task 不做 context snapshot，agent 运行时自己通过 CLI 去取数据。[[sources/multica-shared-project-state-2026-04/source/server/migrations/003_task_context.up.sql|003_task_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]]

在这份公开代码里，我目前只明确看到它被 `broadcastTaskDispatch` 当作 event payload 的底子来解。[[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]]

所以它更像：

- schema 上预留过
- 事件层还在读
- 但不是今天公开实现里的主执行上下文来源

## 一个更准确的类比

如果把两者压到同一张图里，我会这样写：

- AiScientist：`shared state = durable artifacts inside the project workspace`
- Multica：`shared state = durable workflow objects plus resume pointers, rehydrated into each local run`

所以你的直觉是对的：

`Multica 确实也在解决 agent 之间“共享项目状态”的问题。`

但如果继续往下精确区分，它更像是在解决：

- 任务对象共享
- 协作记录共享
- 会话连续性共享
- 执行环境重建

而不是像 AiScientist 那样，直接把研究过程本身变成一个文件总线。

## Sources

- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]
- [[syntheses/ai-scientist-file-as-bus-state-and-context-flow|ai-scientist-file-as-bus-state-and-context-flow]]
