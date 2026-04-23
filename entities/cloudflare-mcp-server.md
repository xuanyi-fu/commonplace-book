---
type: entity
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# Cloudflare MCP server

这里说的 `Cloudflare MCP server`，具体指官方仓库 `cloudflare/mcp` 对应的 `Cloudflare API MCP server`，不是 Cloudflare 整个 MCP server catalog。它的定位是一个官方托管的 remote MCP server，把整个 Cloudflare API 暴露给 MCP client，但默认只暴露两个 tool：`search()` 和 `execute()`。[[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown#^api-mcp-two-tools]] [[sources/cloudflare-mcp-2026-04/source/official-repo-readme#^readme-agent-writes-code]]

## 它是什么

从官方 docs 和 blog 看，Cloudflare 想把这个 server 做成“整个 Cloudflare API 的 MCP 入口”，覆盖 DNS、Workers、R2、Zero Trust 等 2,500+ endpoints，同时把 agent 看到的 tool surface 固定成两个入口，而不是把每个 endpoint 都展开成一个 MCP tool。[[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown#^api-mcp-two-tools]] [[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown#^api-mcp-fixed-token-cost]] [[sources/cloudflare-mcp-2026-04/source/code-mode-mcp-markdown#^server-two-tools-fixed-footprint]]

## 它解决什么问题

它主要解决的是“大 API 面”在 MCP 里的 context 成本和维护成本问题。官方 README 直接说 Cloudflare OpenAPI spec 大约有 200 万 tokens，就算把 native MCP tool schema 压到只保留必需参数，也还有大约 24.4 万 tokens；而 Code Mode 版本把入口压成两个 tool，token footprint 约 1,000。换句话说，它不是为了让 agent “更会调 API”，而是为了不把整份 API surface 一次性塞进 model context。[[sources/cloudflare-mcp-2026-04/source/official-repo-readme#^readme-code-execution-pattern]] [[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown#^api-mcp-fixed-token-cost]] [[sources/cloudflare-mcp-2026-04/source/code-mode-mcp-markdown#^server-two-tools-fixed-footprint]]

## 它的代码执行模式

官方材料把执行模型说得很清楚：这不是 custom DSL，而是普通 JavaScript 加 sandbox。Cloudflare docs 明确说 model 是“writes JavaScript”去操作 typed OpenAPI representation 和 Cloudflare API client；Codemode API reference 也明确把 `openApiMcpServer` 定义成 `search` / `execute` 两个 tool，并说明 host-side `request` handler 会把 authentication 留在 sandbox 外面。[[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown#^api-mcp-js-sandbox]] [[sources/cloudflare-mcp-2026-04/source/code-mode-mcp-markdown#^codemode-write-code-safely]] [[sources/cloudflare-mcp-2026-04/source/codemode-doc-markdown#^openapi-mcp-server-host-auth]]

更具体地说，`search` 不是让 model 调一个预定义查询语言，而是让它写一个 JavaScript `async` 函数去遍历 `spec.paths`。`execute` 也不是让 model 填一个专门的动作 schema，而是让它写 JavaScript，调用 `cloudflare.request()`，在一次 execution 里自己处理分页、条件判断、链式调用和结果过滤。[[sources/cloudflare-mcp-2026-04/source/official-repo-readme#^readme-agent-writes-code]] [[sources/cloudflare-mcp-2026-04/source/code-mode-mcp-markdown#^server-dynamic-worker-sandbox]]

## sandbox 和 auth 边界

官方文档同时说明了 sandbox 边界：Codemode 的 generated code 跑在 isolated Worker sandbox 里，默认 external network access 是 blocked 的，而且当前实现只支持 JavaScript。Dynamic Workers docs 进一步说明这是一个可以执行 arbitrary code 的 secure sandboxed environment，并且宿主可以决定 binding、network access 和其他运行边界。[[sources/cloudflare-mcp-2026-04/source/codemode-doc-markdown#^codemode-security-boundary]] [[sources/cloudflare-mcp-2026-04/source/codemode-doc-markdown#^codemode-js-only]] [[sources/cloudflare-mcp-2026-04/source/dynamic-workers-markdown#^dynamic-workers-secure-sandbox]] [[sources/cloudflare-mcp-2026-04/source/dynamic-workers-markdown#^dynamic-workers-control-surface]]

repo 代码把这个边界落得更实。`src/executor.ts` 里，Cloudflare 用 `env.LOADER.get(...modules: { 'worker.js': ... })` 动态生成一个 Worker，把 model 传进来的 `code` 直接拼进 `await (${code})();` 这一执行路径里；`search` worker 拿到的是预处理后的 `spec.json`，并且 `globalOutbound` 是 `null`，而 `execute` worker 拿到的是 `cloudflare.request()` helper 和受控的 `globalOutbound`。[[sources/cloudflare-mcp-2026-04/source/official-repo-src-executor|official-repo-src-executor.ts]]

`src/index.ts` 则把 auth 明确留在 host 侧：`GlobalOutbound.fetch()` 只允许访问 `CLOUDFLARE_API_BASE` 的 hostname，并在 host 这一侧注入 `Authorization: Bearer ...` header，代码注释也直接写明 token “never enters the user code isolate”。所以更准确的理解不是“agent 学会了一门 Cloudflare DSL”，而是“agent 写普通 JavaScript，Cloudflare 在 server 端给它一个受限的执行环境和一个受控的 API helper”。[[sources/cloudflare-mcp-2026-04/source/official-repo-src-index|official-repo-src-index.ts]]

## 默认模式和回退模式

README 还给了一个很有用的对照：如果加 `?codemode=false`，server 会回退成“每个 endpoint 一个 tool”的传统模式，而且文档明确写了这种模式下是 direct API calls，`no code execution involved`。这说明 code execution 是 Cloudflare 为了压缩上下文和提升组合能力做的默认设计，不是 MCP 协议本身强制要求的交互形式。[[sources/cloudflare-mcp-2026-04/source/official-repo-readme#^readme-disable-codemode]] [[sources/cloudflare-mcp-2026-04/source/official-repo-readme#^readme-no-codemode-no-exec]]

## Sources

- [[sources/cloudflare-mcp-2026-04/summary|cloudflare-mcp-2026-04]]
- [[sources/cloudflare-mcp-2026-04/source/cloudflare-own-mcp-servers-markdown|cloudflare-own-mcp-servers-markdown]]
- [[sources/cloudflare-mcp-2026-04/source/code-mode-mcp-markdown|code-mode-mcp-markdown]]
- [[sources/cloudflare-mcp-2026-04/source/codemode-doc-markdown|codemode-doc-markdown]]
- [[sources/cloudflare-mcp-2026-04/source/dynamic-workers-markdown|dynamic-workers-markdown]]
- [[sources/cloudflare-mcp-2026-04/source/official-repo-readme|official-repo-readme]]
- [[sources/cloudflare-mcp-2026-04/source/official-repo-src-index|official-repo-src-index]]
- [[sources/cloudflare-mcp-2026-04/source/official-repo-src-executor|official-repo-src-executor]]
