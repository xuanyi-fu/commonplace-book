---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# claude-managed-agents-2026-04

这个 source collection 保存了 2026-04-22 当天 Anthropic `Claude Managed Agents` 官方文档里与 runtime 抽象和能力面最直接相关的一组页面，包括 `overview`、`agent setup`、`environments`、`sessions`、`events and streaming`、`permission policies`、`MCP connector`、`skills`、`memory`、`multi-agent`、`define outcomes`。它的目标是把“Anthropic 公开把 agent runtime 抽象成什么对象”以及“这个 runtime 目前具体提供哪些能力”这两层材料保留下来，便于后续写 entity、concept 或 synthesis。 [[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]] [[source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]]

## Structure

- `source/managed-agents-overview.html`: Claude Managed Agents overview 原始网页 HTML
- `source/managed-agents-overview-markdown.md`: 上述 overview 页的 best-effort Markdown derivative
- `source/managed-agents-agent-setup.html`: Define your agent 文档原始网页 HTML
- `source/managed-agents-agent-setup-markdown.md`: 上述 agent setup 页的 best-effort Markdown derivative
- `source/managed-agents-environments.html`: Cloud environment setup 文档原始网页 HTML
- `source/managed-agents-environments-markdown.md`: 上述 environments 页的 best-effort Markdown derivative
- `source/managed-agents-sessions.html`: Start a session 文档原始网页 HTML
- `source/managed-agents-sessions-markdown.md`: 上述 sessions 页的 best-effort Markdown derivative
- `source/managed-agents-events-and-streaming.html`: Session event stream 文档原始网页 HTML
- `source/managed-agents-events-and-streaming-markdown.md`: 上述 events 页的 best-effort Markdown derivative
- `source/managed-agents-permission-policies.html`: Permission policies 文档原始网页 HTML
- `source/managed-agents-permission-policies-markdown.md`: 上述 permissions 页的 best-effort Markdown derivative
- `source/managed-agents-mcp-connector.html`: MCP connector 文档原始网页 HTML
- `source/managed-agents-mcp-connector-markdown.md`: 上述 MCP 页的 best-effort Markdown derivative
- `source/managed-agents-skills.html`: Skills 文档原始网页 HTML
- `source/managed-agents-skills-markdown.md`: 上述 skills 页的 best-effort Markdown derivative
- `source/managed-agents-memory.html`: Using agent memory 文档原始网页 HTML
- `source/managed-agents-memory-markdown.md`: 上述 memory 页的 best-effort Markdown derivative
- `source/managed-agents-multi-agent.html`: Multiagent sessions 文档原始网页 HTML
- `source/managed-agents-multi-agent-markdown.md`: 上述 multi-agent 页的 best-effort Markdown derivative
- `source/managed-agents-define-outcomes.html`: Define outcomes 文档原始网页 HTML
- `source/managed-agents-define-outcomes-markdown.md`: 上述 outcomes 页的 best-effort Markdown derivative
- `summary.md`: 这个 collection 的导读、范围说明和使用建议

## How To Use

- 先读 `source/managed-agents-overview-markdown.md`，建立 Anthropic 对 Claude Managed Agents 的总定位：它不是普通 `Messages API`，而是一个托管式 agent harness / runtime。[[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]]
- 再按 runtime 主干读四页：
  - `source/managed-agents-agent-setup-markdown.md`
  - `source/managed-agents-environments-markdown.md`
  - `source/managed-agents-sessions-markdown.md`
  - `source/managed-agents-events-and-streaming-markdown.md`
  这四页基本覆盖了 `Agent`、`Environment`、`Session`、`Events` 四个核心对象及其关系。[[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]] [[source/managed-agents-sessions-markdown|managed-agents-sessions-markdown.md]]
- 然后按能力面补读五页：
  - `source/managed-agents-permission-policies-markdown.md`
  - `source/managed-agents-mcp-connector-markdown.md`
  - `source/managed-agents-skills-markdown.md`
  - `source/managed-agents-memory-markdown.md`
  - `source/managed-agents-multi-agent-markdown.md`
  这几页分别回答权限 gating、外部工具接入、可复用技能、跨 session memory、以及多 agent 编排。[[source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]] [[source/managed-agents-mcp-connector-markdown|managed-agents-mcp-connector-markdown.md]] [[source/managed-agents-memory-markdown|managed-agents-memory-markdown.md]] [[source/managed-agents-multi-agent-markdown|managed-agents-multi-agent-markdown.md]]
- 最后读 `source/managed-agents-define-outcomes-markdown.md`，把 `outcome + rubric + grader + iteration loop` 这条 research preview 扩展面补齐。[[source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]
- 讨论具体 wording、表格、字段名和代码示例时，以对应 `html` 为准；`-markdown.md` 更适合检索、引用和快速阅读。
- 这次抓取不需要登录、滚动解锁或额外浏览器交互，原始 HTML 可以直接通过 HTTP 获取。

## Summary

从这组官方文档看，Claude Managed Agents 当前最核心的公开抽象仍然是四个对象：`Agent`、`Environment`、`Session`、`Events`。但只停在这四个词上会低估它的实际产品面，因为现在 docs 已经把一些关键扩展面写得很明确了，包括 versioned `agent` 配置、session-level 事件协议和 checkpoint/resume、server-executed tool permissions、MCP + vault、filesystem-based skills、workspace-scoped memory stores、shared-container-but-thread-isolated multi-agent orchestration，以及带 grader 的 `outcomes` 迭代闭环。[[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]] [[source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]] [[source/managed-agents-memory-markdown|managed-agents-memory-markdown.md]] [[source/managed-agents-multi-agent-markdown|managed-agents-multi-agent-markdown.md]] [[source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]

因此，这个 collection 最适合回答的不是“Claude 能不能做 agent”，而是更具体的两类问题：第一，Anthropic 在官方平台里到底把 agent runtime 暴露成了哪些资源和协议；第二，这个 runtime 现在已经原生接管了哪些能力，哪些仍然属于 preview 或需要应用侧自己参与的控制面。若后续要写 `Claude Managed Agents` 的 entity，这一组 source 已经足够作为第一层证据基础。 [[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]] [[source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]] [[source/managed-agents-mcp-connector-markdown|managed-agents-mcp-connector-markdown.md]]

## Sources

- [[source/managed-agents-overview|managed-agents-overview.html]]
- [[source/managed-agents-overview-markdown|managed-agents-overview-markdown.md]]
- [[source/managed-agents-agent-setup|managed-agents-agent-setup.html]]
- [[source/managed-agents-agent-setup-markdown|managed-agents-agent-setup-markdown.md]]
- [[source/managed-agents-environments|managed-agents-environments.html]]
- [[source/managed-agents-environments-markdown|managed-agents-environments-markdown.md]]
- [[source/managed-agents-sessions|managed-agents-sessions.html]]
- [[source/managed-agents-sessions-markdown|managed-agents-sessions-markdown.md]]
- [[source/managed-agents-events-and-streaming|managed-agents-events-and-streaming.html]]
- [[source/managed-agents-events-and-streaming-markdown|managed-agents-events-and-streaming-markdown.md]]
- [[source/managed-agents-permission-policies|managed-agents-permission-policies.html]]
- [[source/managed-agents-permission-policies-markdown|managed-agents-permission-policies-markdown.md]]
- [[source/managed-agents-mcp-connector|managed-agents-mcp-connector.html]]
- [[source/managed-agents-mcp-connector-markdown|managed-agents-mcp-connector-markdown.md]]
- [[source/managed-agents-skills|managed-agents-skills.html]]
- [[source/managed-agents-skills-markdown|managed-agents-skills-markdown.md]]
- [[source/managed-agents-memory|managed-agents-memory.html]]
- [[source/managed-agents-memory-markdown|managed-agents-memory-markdown.md]]
- [[source/managed-agents-multi-agent|managed-agents-multi-agent.html]]
- [[source/managed-agents-multi-agent-markdown|managed-agents-multi-agent-markdown.md]]
- [[source/managed-agents-define-outcomes|managed-agents-define-outcomes.html]]
- [[source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]
