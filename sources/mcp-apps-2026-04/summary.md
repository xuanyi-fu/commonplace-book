---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# mcp-apps-2026-04

This source collection captures official MCP Apps material across the proposal-to-launch arc: the official docs overview, the build guide, the stable 2026-01-26 spec text, and two official blog posts from proposal introduction to production rollout. [[source/official-doc-mcp-apps-overview-markdown]] [[source/official-doc-build-an-mcp-app-markdown]] [[source/official-spec-mcp-apps-2026-01-26-markdown]] [[source/official-blog-2025-11-21-mcp-apps-markdown]] [[source/official-blog-2026-01-26-mcp-apps-markdown]]

## Structure

- `source/official-doc-mcp-apps-overview.html`: raw published HTML capture of the official MCP Apps overview page
- `source/official-doc-mcp-apps-overview-markdown.md`: faithful markdown derivative from the official `ext-apps` repo overview source
- `source/official-doc-build-an-mcp-app.html`: raw published HTML capture of the official build guide
- `source/official-doc-build-an-mcp-app-markdown.md`: faithful markdown derivative from the official `ext-apps` repo quickstart source, with the quickstart image localized under `source/assets/`
- `source/official-spec-mcp-apps-2026-01-26.mdx`: raw versioned spec artifact from the official `ext-apps` repo
- `source/official-spec-mcp-apps-2026-01-26-markdown.md`: markdown-readable derivative of the stable 2026-01-26 spec text
- `source/official-blog-2025-11-21-mcp-apps.html`: raw published HTML of the proposal announcement blog post
- `source/official-blog-2025-11-21-mcp-apps-markdown.md`: faithful markdown derivative of the November 21, 2025 announcement post
- `source/official-blog-2026-01-26-mcp-apps.html`: raw published HTML of the production launch blog post
- `source/official-blog-2026-01-26-mcp-apps-markdown.md`: faithful markdown derivative of the January 26, 2026 launch post
- `source/assets/official-doc-build-an-mcp-app/`: localized image used by the quickstart markdown derivative
- `source/assets/official-blog-2025-11-21-mcp-apps/`: localized blog images from the proposal announcement
- `source/assets/official-blog-2026-01-26-mcp-apps/`: localized blog GIFs from the production launch post
- `summary.md`: this collection summary and usage guide

## How To Use

- Start with `source/official-blog-2025-11-21-mcp-apps-markdown.md` if you want the first public announcement and the initial explanation for why an official UI extension was needed.
- Read `source/official-spec-mcp-apps-2026-01-26-markdown.md` next for the stable normative shape: `ui://` resources, tool-UI linkage, JSON-RPC over `postMessage`, host context, display modes, and the security model.
- Use `source/official-doc-mcp-apps-overview-markdown.md` for the shortest official explanation of the architecture and lifecycle, and `source/official-doc-build-an-mcp-app-markdown.md` when you need the concrete server plus View registration flow.
- Use `source/official-blog-2026-01-26-mcp-apps-markdown.md` for the launch framing, client-support claims, and the point where MCP Apps is described as live and production-ready.
- Fall back to the paired raw `.html` captures when you need the exact published page framing or page metadata rather than the repo-readable markdown.

## Summary

The collected official material makes MCP Apps legible as both a protocol extension and a product surface. The proposal blog and the stable spec agree on the core shape: servers declare `ui://` resources, tools link to them through metadata, hosts render them in sandboxed iframes, and the UI talks back through JSON-RPC over `postMessage`. The docs overview and build guide then translate that into host/server/View lifecycle and concrete implementation steps. [[source/official-blog-2025-11-21-mcp-apps-markdown]] [[source/official-spec-mcp-apps-2026-01-26-markdown]] [[source/official-doc-mcp-apps-overview-markdown]] [[source/official-doc-build-an-mcp-app-markdown]]

The earliest dated official MCP Apps material collected here is November 21, 2025: the proposal announcement blog post is published that day, and the stable spec text itself carries `Created: 2025-11-21`. By January 26, 2026, the launch post describes MCP Apps as live and as the first official MCP extension. [[source/official-blog-2025-11-21-mcp-apps-markdown]] [[source/official-spec-mcp-apps-2026-01-26-markdown]] [[source/official-blog-2026-01-26-mcp-apps-markdown]]

## Sources

- [[source/official-doc-mcp-apps-overview.html|official-doc-mcp-apps-overview.html]]
- [[source/official-doc-mcp-apps-overview-markdown|official-doc-mcp-apps-overview-markdown.md]]
- [[source/official-doc-build-an-mcp-app.html|official-doc-build-an-mcp-app.html]]
- [[source/official-doc-build-an-mcp-app-markdown|official-doc-build-an-mcp-app-markdown.md]]
- [[source/official-spec-mcp-apps-2026-01-26.mdx|official-spec-mcp-apps-2026-01-26.mdx]]
- [[source/official-spec-mcp-apps-2026-01-26-markdown|official-spec-mcp-apps-2026-01-26-markdown.md]]
- [[source/official-blog-2025-11-21-mcp-apps.html|official-blog-2025-11-21-mcp-apps.html]]
- [[source/official-blog-2025-11-21-mcp-apps-markdown|official-blog-2025-11-21-mcp-apps-markdown.md]]
- [[source/official-blog-2026-01-26-mcp-apps.html|official-blog-2026-01-26-mcp-apps.html]]
- [[source/official-blog-2026-01-26-mcp-apps-markdown|official-blog-2026-01-26-mcp-apps-markdown.md]]
