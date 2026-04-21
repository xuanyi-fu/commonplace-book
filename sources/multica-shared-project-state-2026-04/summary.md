---
type: source
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Multica 共享项目状态 source collection

这组 source 主要收录 `multica-ai/multica` 官方公开仓库里，和“agent 之间怎样共享项目状态、怎样恢复会话、怎样把平台状态重新注入执行环境”直接相关的 raw source。重点不在产品宣发，而在 schema、query、handler、daemon、execenv 这几层的实际实现。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]]

## Structure

这个 collection 只保留 raw source，按 upstream repo 的原始路径分层：

- `source/docs/`
  公开产品全景文档，给出概念词典和模块地图。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]]
- `source/server/migrations/`
  schema 演化，说明 `workspace.context`、`agent_task_queue.context`、`session_id`、`work_dir`、`chat_session` 等字段是什么时候进入系统的。[[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|001_init.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/003_task_context.up.sql|003_task_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/006_workspace_context.up.sql|006_workspace_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/020_task_session.up.sql|020_task_session.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/033_chat.up.sql|033_chat.up.sql]]
- `source/server/pkg/db/queries/`
  sqlc query 层，给出任务 claim、会话恢复、chat fallback、chat session resume pointer 的数据库真相。[[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]]
- `source/server/internal/handler/`
  daemon claim response 是怎样把 issue、workspace、agent、repos、trigger comment、prior session 拼到同一个任务响应里的。[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/agent.go|agent.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]]
  `workspace.go` 则补了 `workspace.context` 和 `workspace.repos` 的 CRUD 侧证据。[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/workspace.go|workspace.go]]
- `source/server/internal/service/`
  task enqueue / complete / fail / chat resume pointer 更新的服务层逻辑。[[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]]
- `source/server/internal/daemon/`
  daemon 侧怎样把平台状态重建成 workdir、prompt、provider-native config、skills、resume 指针。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/types.go|types.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/prompt.go|prompt.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|daemon.go]]
- `source/server/internal/daemon/execenv/`
  workdir 内部到底写了什么文件，以及这些文件怎样让不同 CLI agent 读到同一份任务上下文。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/execenv.go|execenv.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|context.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]]

## How To Use

建议按下面的顺序读：

1. 先看 `docs/product-overview.md`，建立术语表和产品层心智模型。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]]
2. 再看 migrations 和 queries，确认哪些“共享状态”是真的落在 schema 里的，而不是文案表述。[[sources/multica-shared-project-state-2026-04/source/server/migrations/003_task_context.up.sql|003_task_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/020_task_session.up.sql|020_task_session.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]]
3. 再看 `handler/daemon.go` 和 `daemon/daemon.go`，理解“平台状态如何进入 agent 执行现场”。[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]]
4. 最后看 `execenv/*`，确认共享状态最终以什么文件和配置形式出现在 workdir 里。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|context.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]]

这组 source 最适合回答 3 类问题：

- Multica 里哪些对象才算“共享项目状态”
- 这些状态怎样从平台对象流到 agent workdir
- 它和 AiScientist `File-as-Bus` 到底像在哪里，又不像在哪里

## Summary

当前这组 raw source 支持 5 个关键判断：

- Multica 确实在解决 agent 之间的“共享项目状态”，但它主要把状态放在平台对象层：`workspace`、`issue`、`comment`、`agent`、`skill`、`agent_task_queue`、`chat_session`、`task_message`。[[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]] [[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|001_init.up.sql]]
- 真正驱动连续性的核心不是 prompt 本身，而是 `prior_session_id` + `prior_work_dir`，以及 chat 路径上的 `chat_session.session_id/work_dir`。[[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|agent.sql]] [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|chat.sql]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]]
- daemon claim 任务时，会把 `workspace_id`、`repos`、`agent instructions`、`skills`、`trigger comment content`、`chat message`、`prior session/workdir` 组装成一个 `Task` 响应，再由本地 daemon 重建执行环境。[[sources/multica-shared-project-state-2026-04/source/server/internal/handler/agent.go|agent.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|daemon.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/types.go|types.go]]
- daemon 在 workdir 里写入 `.agent_context/issue_context.md` 和 provider-native `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`，并把 skills 放到各家 CLI 的原生发现路径里；真正厚的业务状态仍然要求 agent 通过 `multica` CLI 回平台去读。[[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/prompt.go|prompt.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|context.go]] [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|runtime_config.go]]
- 需要特别谨慎区分两个“看起来像共享状态”的字段：
  - `workspace.context` 在 schema 和产品文档里是明确存在的，但在当前公开代码里，我还没有找到它被注入 daemon prompt 或 execenv 的明确路径。[[sources/multica-shared-project-state-2026-04/source/server/migrations/006_workspace_context.up.sql|006_workspace_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/docs/product-overview|product-overview.md]]
  - `agent_task_queue.context` 也真实存在，但当前 issue task enqueue 代码明确写着“不做 context snapshot”；我目前只看到它被用来承载 `task:dispatch` 事件 payload，而不是执行时的主上下文来源。[[sources/multica-shared-project-state-2026-04/source/server/migrations/003_task_context.up.sql|003_task_context.up.sql]] [[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|task.go]]

## Sources

- [[sources/multica-shared-project-state-2026-04/source/docs/product-overview|docs/product-overview.md]]
- [[sources/multica-shared-project-state-2026-04/source/server/migrations/001_init.up.sql|server/migrations/001_init.up.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/migrations/003_task_context.up.sql|server/migrations/003_task_context.up.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/migrations/006_workspace_context.up.sql|server/migrations/006_workspace_context.up.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/migrations/020_task_session.up.sql|server/migrations/020_task_session.up.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/migrations/033_chat.up.sql|server/migrations/033_chat.up.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/agent.sql|server/pkg/db/queries/agent.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/pkg/db/queries/chat.sql|server/pkg/db/queries/chat.sql]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/agent.go|server/internal/handler/agent.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/daemon.go|server/internal/handler/daemon.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/handler/workspace.go|server/internal/handler/workspace.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/service/task.go|server/internal/service/task.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/types.go|server/internal/daemon/types.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/prompt.go|server/internal/daemon/prompt.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/daemon.go|server/internal/daemon/daemon.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/execenv.go|server/internal/daemon/execenv/execenv.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/context.go|server/internal/daemon/execenv/context.go]]
- [[sources/multica-shared-project-state-2026-04/source/server/internal/daemon/execenv/runtime_config.go|server/internal/daemon/execenv/runtime_config.go]]
