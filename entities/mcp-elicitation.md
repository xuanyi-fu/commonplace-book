---
type: entity
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# MCP elicitation

`MCP elicitation` 是 MCP 里让 `server` 在一次正在进行的交互里，经由 `client` 再向用户要补充信息的能力。它解决的不是“让 server 自己托管一段前端 UI”，而是“当 tool / workflow 走到一半还缺用户输入时，协议怎么把这次补充输入标准化，并且把最终控制权留在 `client` 手里”。官方 versioned spec 明确把它定义成 server 通过 client 向用户请求额外信息的标准流程，并把它拆成 `form` 与 `url` 两种 mode。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-definition]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-capability-modes]]

## 它是什么

从协议边界看，elicitation 是一种“嵌套在其他 MCP 能力里的用户补充输入”。spec 明确说，server 发的是 `elicitation/create`，而实现方可以用任何合适的交互方式把它暴露给用户，协议本身不强制某一种具体 UI。也就是说，标准化的是 server/client 之间的请求与安全边界，不是某个固定弹窗样式。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-definition]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-request-core]]

更具体地说，`form` mode 用来收集结构化但不敏感的数据，server 通过 `requestedSchema` 描述它想要的字段；`url` mode 则把用户引导到外部 URL 做 out-of-band 交互，适合 API key、OAuth、支付等不应该穿过 `client` 的敏感流程。spec 还明确要求：敏感信息不能走 `form` mode，涉及这类信息时必须使用 `url` mode。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-form-schema]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-sensitive-boundary]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-oauth-boundary]]

## 协议到底标准化了什么

官方 spec 标准化了几层东西。第一层是 capability negotiation：支持 elicitation 的 `client` 必须在初始化时声明 `elicitation` capability，并且至少支持一种 mode；`server` 不能发送超出该 `client` 已声明 mode 的请求。第二层是 request / response contract：`elicitation/create` 至少包含 `mode` 和 `message`，`form` mode 再加 `requestedSchema`，`url` mode 再加 `url` 与 `elicitationId`。第三层是 response action 语义：用户不是只有“提交”一种结果，而是明确区分 `accept`、`decline`、`cancel`。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-capability-modes]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-request-core]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-response-actions]]

第四层是为了让 `client` 容易实现而故意收紧的 schema 边界。`form` mode 的 schema 不是任意 JSON Schema，而是以 flat object + primitive properties 为主，目的是简化 `client` 侧表单生成与输入校验。第五层是安全规则：`client` 必须明确告诉用户是谁在请求信息、给出清楚的 decline / cancel 选项；如果是 `url` mode，还必须展示完整 URL、先征得用户同意、不能自动预取链接内容。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-form-schema]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-url-client-rules]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-form-security]]

## 它和 MCP Apps 有什么不同

`MCP Apps` 解决的是另一类问题。官方 MCP Apps overview 讲得很清楚：它标准化的是 server 如何声明 `ui://` 资源、`host` 如何把这些资源渲染进 sandboxed iframe、以及 `View` 如何通过 `postMessage` 与 `host` 双向通信。换句话说，MCP Apps 关心的是“可嵌入 UI 资源与 host/view 生命周期”。[[sources/mcp-apps-2026-04/source/official-doc-mcp-apps-overview-markdown]]

而 elicitation 不要求 server 提供 `ui://` 资源，也不定义 iframe、`View`、`postMessage`、display modes 这套 host-managed UI runtime。它只规定 server 如何请求补充输入、`client` 在什么安全边界内向用户展示请求、以及用户结果如何回到 server。可以把它理解成：elicitation 标准化的是一次“向用户再要数据”的协议动作；MCP Apps 标准化的是一整套“把 server 提供的 UI 嵌进 host 里运行”的 UI extension surface。两者都涉及用户交互，但抽象层级不同。[[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-definition]] [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown#^elicitation-request-core]] [[sources/mcp-apps-2026-04/source/official-doc-mcp-apps-overview-markdown]]

## 一个具体的 client-side support 例子

官方 `modelcontextprotocol/inspector` README 给了一个很实在的实现信号：Inspector 把 elicitation 当成需要用户交互的 client 行为来处理，所以文档明确提醒，遇到这类请求时要把 client-side timeout 设得足够长；否则 Inspector 这个 `client` 会先于 server 取消请求。README 还写了它对表单输入的处理准则，比如省略空的 optional fields，但保留 required fields 和显式 default values。也就是说，至少在官方 Inspector 这条实现线上，elicitation 不是“只有 spec 没有 client 行为”的纸面能力，而是已经落到具体 client 输入处理与超时策略上的功能面。[[sources/mcp-elicitation-2026-04/source/official-inspector-readme-markdown#^inspector-elicitation-timeout]] [[sources/mcp-elicitation-2026-04/source/official-inspector-readme-markdown#^inspector-form-input-omissions]] [[sources/mcp-elicitation-2026-04/source/official-inspector-readme-markdown#^inspector-form-input-required]]

## Sources

- [[sources/mcp-elicitation-2026-04/summary|mcp-elicitation-2026-04]]
- [[sources/mcp-elicitation-2026-04/source/official-spec-elicitation-2025-11-25-markdown|official-spec-elicitation-2025-11-25-markdown.md]]
- [[sources/mcp-elicitation-2026-04/source/official-inspector-readme-markdown|official-inspector-readme-markdown.md]]
- [[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]
- [[sources/mcp-apps-2026-04/source/official-doc-mcp-apps-overview-markdown|official-doc-mcp-apps-overview-markdown.md]]
