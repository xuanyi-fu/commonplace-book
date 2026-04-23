---
type: entity
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Claude Managed Agents

`Claude Managed Agents` 更适合被理解成 Anthropic 在 `Claude Platform` 上提供的托管式 `[[concepts/agent-harness|agent-harness]]` / agent runtime，而不是一个“把 prompt 发给模型”的普通聊天 API。它把 agent 提升成一个有可复用配置、云端运行环境、状态化 session 和事件协议的远程对象，开发者不需要自己先搭 agent loop、sandbox、tool execution layer 和 runtime 再开始用。[[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]]

## 官方主抽象

官方 overview 把 Claude Managed Agents 的核心对象定成四个：`Agent`、`Environment`、`Session`、`Events`。其中 `Agent` 不是一次运行，而是一个 reusable、versioned 的能力定义，里面组合 model、system prompt、tools、MCP servers、skills；`Environment` 是容器模板，定义 packages 和 networking；`Session` 是某个 agent 在某个 environment 里的运行实例；`Events` 则是应用和 runtime 之间的交互协议。[[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]]

如果再往实现边界里看一步，Anthropic 现在实际上已经把这四个主抽象扩展成更具体的资源面了：`Agent` 还带 `version`、`archived_at`、`callable_agents` 等字段；`Session` 可以默认引用 latest agent version，也可以 pin 到特定 version；session 本身有 `idle`、`running`、`rescheduling`、`terminated` 这些生命周期状态，并支持 archive / delete。[[sources/claude-managed-agents-2026-04/source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-sessions-markdown|managed-agents-sessions-markdown.md]]

## 它提供的主要功能

最底层的一组能力是托管执行层。官方 baseline surface 已经包含 pre-built agent toolset，至少覆盖 `bash`、文件读写编辑 / glob / grep、`web_search` / `web_fetch`，而 `Agent` 里的 `tools` 还可以同时组合 pre-built agent tools、MCP tools 和 custom tools。也就是说，它不是只给你一个会“建议动作”的模型，而是给你一个能在托管 runtime 里实际执行动作的 agent surface。[[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]]

第二组能力是运行环境与权限控制。`Environment` 允许你预装 `apt`、`cargo`、`gem`、`go`、`npm`、`pip` 依赖，并在共享同一 environment 配置的 session 之间复用这些 package cache；但每个 session 仍然拿到自己的隔离容器实例。网络侧则支持 `unrestricted` 和 `limited` 两种模式，后者可以用 `allowed_hosts`、`allow_package_managers`、`allow_mcp_servers` 把出站访问收紧到最小权限。工具执行权限则单独走 permission policies：server-executed tools 支持 `always_allow` 和 `always_ask`，其中 agent toolset 默认更偏放行，MCP toolset 默认更偏确认。[[sources/claude-managed-agents-2026-04/source/managed-agents-environments-markdown|managed-agents-environments-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]]

如果把这个 `Environment` 再往“它到底像什么”这个问题上压一层，Anthropic 当前公开给开发者的抽象更接近托管的 `cloud container` / `configured container template`，而不是一个把 base distro 也当成 contract 暴露出来的完整 OS。docs 明确给了容器模板、预装 packages、network access、session 级隔离实例和 idle 后整容器 checkpoint 这些边界，所以实际使用心智会很像 Docker-like Linux container；但更稳妥的理解仍然是“托管容器 runtime”，不要把它直接等同成“我拿到了一台可默认按 Debian / Ubuntu 假设的机器”。[[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-environments|managed-agents-environments.html]]

第三组能力是 stateful session runtime。Claude Managed Agents 不是 request-response，而是 event-based protocol：应用侧发送 `user.message`、`user.interrupt`、`user.tool_confirmation`、`user.custom_tool_result` 这类 `user.*` 事件，runtime 通过 SSE / event stream 回传 `agent.*`、`session.*`、`span.*` 事件。session 在 idle 时会被 checkpoint，保存文件系统、已安装 packages 和 agent 生成的文件；history 会一直保留到 session 被显式 delete，而完整容器 checkpoint 默认保留到最后活动后 30 天。[[sources/claude-managed-agents-2026-04/source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-sessions-markdown|managed-agents-sessions-markdown.md]]

第四组能力是外部能力和知识层接入。对外部系统，Claude Managed Agents 原生支持 remote MCP：在 agent 创建时声明 `mcp_servers`，在 session 创建时通过 `vault_ids` 提供鉴权材料，MCP auth 失败不会直接炸掉整个 session，而是以 `session.error` 暴露出来。对 procedural knowledge，它还支持 filesystem-based `skills`，分 Anthropic 预置 skills 和组织自定义 skills 两类，并且会在相关任务上按需自动调用。[[sources/claude-managed-agents-2026-04/source/managed-agents-mcp-connector-markdown|managed-agents-mcp-connector-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-skills-markdown|managed-agents-skills-markdown.md]]

第五组能力是长期状态和高级编排。`memory stores` 把跨 session learnings 做成 workspace-scoped 文本记忆集合，挂到 session 后 agent 会自动在任务开始前检查、在任务结束后写回，并获得 `memory_list`、`memory_search`、`memory_read`、`memory_write`、`memory_edit`、`memory_delete` 这组 memory tools。再往上，research preview 里的 multi-agent 允许多个 agent 共享同一 container / filesystem，但各自运行在独立 session thread 和独立上下文里；`outcomes` 则把 session 从“对话”进一步提升成“朝 rubric-defined result 迭代的工作单元”，由单独的 grader 在独立上下文窗口里评估成果并驱动 revision loop。[[sources/claude-managed-agents-2026-04/source/managed-agents-memory-markdown|managed-agents-memory-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-multi-agent-markdown|managed-agents-multi-agent-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]

## 暂定判断

如果只抓一句话，Claude Managed Agents 的真正差异化不在“Claude 也能当 agent”，而在 Anthropic 已经把 agent runtime 的大块基础设施做成平台产品了：versioned capability definition、托管容器、server-executed tools、permission gating、stateful session / checkpoint、event stream、MCP + vault、skills、memory，以及 preview 状态下的 multi-agent 和 outcomes。开发者仍然要对 custom tool 执行、approval 决策和更高层应用逻辑负责，但不必再从零搭一整套 agent runtime。[[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]] [[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]

## Sources

- [[sources/claude-managed-agents-2026-04/summary|claude-managed-agents-2026-04]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-environments-markdown|managed-agents-environments-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-sessions-markdown|managed-agents-sessions-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-mcp-connector-markdown|managed-agents-mcp-connector-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-skills-markdown|managed-agents-skills-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-memory-markdown|managed-agents-memory-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-multi-agent-markdown|managed-agents-multi-agent-markdown.md]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]
