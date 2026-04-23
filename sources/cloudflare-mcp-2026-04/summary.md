---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# cloudflare-mcp-2026-04

This source collection captures primary-source material for the official `cloudflare/mcp` Cloudflare API MCP server: the public Cloudflare docs and blog that define its two-tool `search` / `execute` shape, the Codemode and Dynamic Workers docs that explain the execution model, and the official repo files that show how the sandbox and auth boundary are implemented. [[source/cloudflare-own-mcp-servers-markdown#^api-mcp-two-tools]] [[source/cloudflare-own-mcp-servers-markdown#^api-mcp-js-sandbox]] [[source/code-mode-mcp-markdown#^server-two-tools-fixed-footprint]] [[source/codemode-doc-markdown#^openapi-mcp-server-host-auth]]

## Structure

- `source/cloudflare-own-mcp-servers.html`: raw HTML capture of Cloudflare's official docs page for Cloudflare's own MCP servers
- `source/cloudflare-own-mcp-servers-markdown.md`: faithful markdown derivative of that docs page, with block ids on the core API-server passages
- `source/code-mode-mcp.html`: raw HTML capture of Cloudflare's official Code Mode launch blog post
- `source/code-mode-mcp-markdown.md`: faithful markdown derivative of the Code Mode blog post, with block ids on the two-tool and sandbox passages
- `source/codemode-doc.html`: raw HTML capture of the official Codemode API reference
- `source/codemode-doc-markdown.md`: faithful markdown derivative of the Codemode API reference, including the `openApiMcpServer` and security sections
- `source/dynamic-workers.html`: raw HTML capture of the official Dynamic Workers docs page
- `source/dynamic-workers-markdown.md`: faithful markdown derivative of the Dynamic Workers docs page
- `source/official-repo-readme.md`: raw README from the official `cloudflare/mcp` repository
- `source/official-repo-src-index.ts`: raw `src/index.ts` from the official `cloudflare/mcp` repository
- `source/official-repo-src-server.ts`: raw `src/server.ts` from the official `cloudflare/mcp` repository
- `source/official-repo-src-executor.ts`: raw `src/executor.ts` from the official `cloudflare/mcp` repository
- `summary.md`: this collection summary and usage guide

## How To Use

- Start with `source/cloudflare-own-mcp-servers-markdown.md` to confirm what Cloudflare publicly says the Cloudflare API MCP server is: a managed remote server that exposes the whole Cloudflare API through `search()` and `execute()`.
- Read `source/code-mode-mcp-markdown.md` next for the product rationale: why the server exists, what context-window problem it addresses, and how Cloudflare describes server-side Code Mode in plain language.
- Use `source/codemode-doc-markdown.md` and `source/dynamic-workers-markdown.md` to answer execution-model questions precisely, especially whether the model writes ordinary JavaScript, where auth lives, and what the sandbox blocks by default.
- Use `source/official-repo-readme.md` for the public repo-level interface, including `?codemode=false` as the non-code-mode fallback.
- Use `source/official-repo-src-index.ts`, `source/official-repo-src-server.ts`, and `source/official-repo-src-executor.ts` when you need implementation evidence about `globalOutbound`, auth-header injection, and how generated code is actually run.

## Summary

The official material converges on a consistent picture: the Cloudflare API MCP server is a token-efficient remote MCP server for the entire Cloudflare API, designed around a fixed two-tool surface instead of one tool per endpoint. The execution model is not a custom DSL. Cloudflare's docs and Codemode reference say the model writes ordinary JavaScript against a typed OpenAPI representation and a `cloudflare.request()` helper; that generated code runs inside isolated Dynamic Workers / Worker sandboxes, with auth kept on the host side and network access constrained by sandbox configuration. [[source/cloudflare-own-mcp-servers-markdown#^api-mcp-js-sandbox]] [[source/code-mode-mcp-markdown#^codemode-write-code-safely]] [[source/code-mode-mcp-markdown#^server-dynamic-worker-sandbox]] [[source/codemode-doc-markdown#^openapi-mcp-server-host-auth]] [[source/codemode-doc-markdown#^codemode-security-boundary]] [[source/codemode-doc-markdown#^codemode-js-only]]

## Sources

- [[source/cloudflare-own-mcp-servers.html|cloudflare-own-mcp-servers.html]]
- [[source/cloudflare-own-mcp-servers-markdown|cloudflare-own-mcp-servers-markdown.md]]
- [[source/code-mode-mcp.html|code-mode-mcp.html]]
- [[source/code-mode-mcp-markdown|code-mode-mcp-markdown.md]]
- [[source/codemode-doc.html|codemode-doc.html]]
- [[source/codemode-doc-markdown|codemode-doc-markdown.md]]
- [[source/dynamic-workers.html|dynamic-workers.html]]
- [[source/dynamic-workers-markdown|dynamic-workers-markdown.md]]
- [[source/official-repo-readme|official-repo-readme.md]]
- [[source/official-repo-src-index|official-repo-src-index.ts]]
- [[source/official-repo-src-server|official-repo-src-server.ts]]
- [[source/official-repo-src-executor|official-repo-src-executor.ts]]
