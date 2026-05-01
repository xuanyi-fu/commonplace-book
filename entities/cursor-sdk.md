---
type: entity
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# Cursor SDK

`Cursor SDK` 是 Cursor / Anysphere 在 2026-04 推出的 TypeScript SDK，用来从开发者自己的代码里创建和管理 Cursor agents。它更适合被理解成 Cursor 把自己的 coding-agent harness 和 runtime 暴露成 API，而不是一个普通 model API wrapper：官方 launch framing 是让开发者使用 Cursor desktop app、CLI、web app 背后的同一套 runtime、harness 和 models。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-runtime]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown#^cursor-sdk-typescript-purpose]]

## 核心抽象

开发者侧的主入口是 `@cursor/sdk` 里的 `Agent.create`。当前 TypeScript docs 暴露的 `AgentOptions` 包括 `apiKey`、`model`、`local`、`cloud`、`mcpServers`、`agents`、`agentId` 等字段；其中 `local` 是本地 agent 配置，`cloud` 是 Cloud agent 配置，`mcpServers` 和 `agents` 分别把 MCP server 与 subagent 定义接到 agent surface 上。[[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown#^cursor-sdk-agent-options]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown#^cursor-sdk-local-cloud-options]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown#^cursor-sdk-tools-subagents-agentid]]

这个 API surface 不是一次性 completion。TypeScript docs 里列出的 run-stream event 类型包括 `message`、`reasoning`、`tool_call`、`tool_result`、`error`、`finish`、`file_change`、`status`、`task`、`request`，而 SDK release changelog 还把 Cloud Agents API 描述成 durable agents、per-prompt runs、run-scoped status / streaming / cancellation、SSE reconnect 和 lifecycle controls。[[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown#^cursor-sdk-event-stream]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-release-changelog-markdown#^cursor-cloud-agents-api-updates]]

## Runtime 模式

Cursor SDK 当前最重要的 runtime 区分是 `local`、`cloud` 和 self-hosted workers。`local` 模式让 agent 在本机 working directory 上运行；`cloud` 模式使用 Cursor Cloud Agents runtime，每个 cloud agent 有 dedicated VM、sandbox、repo clone 和 configured development environment；self-hosted workers 则把 code、tool execution、build outputs 和 secrets 留在用户自己的 network / internal machines 里。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-local-example]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-cloud-runtime]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-runtime-modes]] [[sources/cursor-sdk-2026-04/source/cursor-self-hosted-cloud-agents-changelog-markdown#^cursor-self-hosted-data-boundary]]

因此说它“提供运行环境”要分层：Cloud mode 里 Cursor 确实提供 VM/runtime；local mode 里运行环境主要是用户自己的机器；self-hosted mode 则是用户自备 infrastructure，但继续接入 Cursor 的 agent experience / harness 能力。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-cloud-runtime]] [[sources/cursor-sdk-2026-04/source/cursor-self-hosted-cloud-agents-changelog-markdown#^cursor-self-hosted-capabilities]]

## Harness 能力

Cursor SDK 的差异化在 `[[concepts/agent-harness|agent-harness]]` 层。官方 blog 明确把 SDK-launched agents 连接到 Cursor 的 full harness：codebase indexing、semantic search、instant grep、MCP servers、repo-local `.cursor/skills/`、`.cursor/hooks.json` hooks，以及可以由主 agent 通过 `Agent` tool 生成的 subagents。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-harness]]

这使它更像 coding-agent platform 的 API surface：开发者把 agent 放进 CI/CD、automation、internal app 或 customer-facing product，而不是只在 IDE 里手动触发 agent。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-use-cases]]

## Pricing Surface

官方 launch blog 和 release changelog 都把 Cursor SDK 说成 public beta，并说明它按 standard token-based consumption pricing 计费。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-billing]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-release-changelog-markdown#^cursor-sdk-release-billing]]

当前公开 pricing surface 主要落在 plan access 和 model usage 上：Pro 页面列出 `Cloud agents`、MCPs、skills、hooks 等能力；Pro+ 和 Ultra 提供更高 usage multiplier；Models & Pricing docs 说明 included monthly usage 用完后可以走 on-demand usage，Teams 侧还有 Cursor Token Rate。[[sources/cursor-sdk-2026-04/source/cursor-pricing-markdown#^cursor-pricing-pro-cloud-agents]] [[sources/cursor-sdk-2026-04/source/cursor-pricing-markdown#^cursor-pricing-pro-plus-ultra]] [[sources/cursor-sdk-2026-04/source/cursor-models-pricing-markdown#^cursor-models-pricing-on-demand]] [[sources/cursor-sdk-2026-04/source/cursor-models-pricing-markdown#^cursor-token-rate]]

## 和 Claude Managed Agents 的关系

`Cursor SDK` 和 [[entities/claude-managed-agents|Claude Managed Agents]] 很像的一点是：两者都把 agent 从单次 model call 往 harness + runtime + state + tools + billing surface 推。差别在于 Cursor SDK 是 coding-workflow-first，核心资产是 Cursor 的 repo 理解、代码编辑、MCP、skills、hooks、subagents 和 Cloud Agents runtime；Claude Managed Agents 则是更通用的平台对象模型，把 `Agent`、`Environment`、`Session`、`Events` 这些 runtime 资源明确做成官方主抽象。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-harness]] [[entities/claude-managed-agents]]

如果只抓一句话，Cursor SDK 是 Cursor 对 “agent runtime 变成可购买、可编排平台能力” 这条趋势的 coding-agent 版本：打包卖 Cursor coding-agent harness，加上 local / cloud / self-hosted runtime selection。[[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown#^cursor-sdk-runtime-modes]] [[sources/cursor-sdk-2026-04/source/cursor-sdk-release-changelog-markdown#^cursor-cloud-agents-api-updates]]

## Sources

- [[sources/cursor-sdk-2026-04/summary|cursor-sdk-2026-04]]
- [[sources/cursor-sdk-2026-04/source/cursor-sdk-blog-markdown|cursor-sdk-blog-markdown.md]]
- [[sources/cursor-sdk-2026-04/source/cursor-sdk-release-changelog-markdown|cursor-sdk-release-changelog-markdown.md]]
- [[sources/cursor-sdk-2026-04/source/cursor-sdk-typescript-docs-markdown|cursor-sdk-typescript-docs-markdown.md]]
- [[sources/cursor-sdk-2026-04/source/cursor-pricing-markdown|cursor-pricing-markdown.md]]
- [[sources/cursor-sdk-2026-04/source/cursor-models-pricing-markdown|cursor-models-pricing-markdown.md]]
- [[sources/cursor-sdk-2026-04/source/cursor-self-hosted-cloud-agents-changelog-markdown|cursor-self-hosted-cloud-agents-changelog-markdown.md]]
- [[entities/claude-managed-agents]]

