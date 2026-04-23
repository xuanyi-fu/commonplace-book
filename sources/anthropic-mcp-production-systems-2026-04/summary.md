---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# anthropic-mcp-production-systems-2026-04

This source collection preserves Anthropic's April 22, 2026 blog post "Building agents that reach production systems with MCP" as both raw HTML and a best-effort Markdown derivative. It is meant to preserve Anthropic's own framing of why production agents converge on MCP and which server, client, auth, and skill patterns Anthropic currently recommends.

## Structure

- `source/building-agents-that-reach-production-systems-with-mcp.html`: original webpage artifact captured directly from the Claude blog
- `source/building-agents-that-reach-production-systems-with-mcp-markdown.md`: best-effort Markdown derivative of the article body, preserving headings, links, and in-article figures
- `source/assets/building-agents-that-reach-production-systems-with-mcp/`: localized copies of the two in-article figures referenced by the Markdown derivative
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/building-agents-that-reach-production-systems-with-mcp-markdown.md` for a readable and searchable copy of the article.
- Use `source/building-agents-that-reach-production-systems-with-mcp.html` as the authoritative source for exact rendering, original link targets, and any formatting detail that the Markdown cleanup may simplify.
- Use this collection when you need Anthropic's public framing of direct API calls vs CLIs vs MCP, remote MCP server design, context-efficient MCP clients, and the pairing of MCP with skills.
- No browser interaction was required before capture; the page was retrievable directly over HTTP.
- The saved Markdown derivative preserves one visible source-page quirk from the original HTML: the anchor text `Canva` points to `https://claude.com/connectors/atlassian`.

## Summary

The article argues that agents usually connect to external systems through one of three surfaces: direct API calls, CLIs, or MCP. Anthropic's core claim is that direct API calls are fine for narrow integrations and CLIs are effective in local shell-based environments, but production agents increasingly run in cloud or cross-platform settings where MCP becomes the reusable common layer.

The recommended MCP server patterns in this article are: prefer remote servers for maximum client reach, group tools around user intent instead of mirroring raw endpoints, fall back to code-execution surfaces when the underlying API is very large, ship richer protocol semantics such as MCP Apps and elicitation when they help, and use standardized OAuth flows such as CIMD plus Vaults for credential reuse in cloud-hosted agents.

On the client side, the article recommends context-efficiency patterns such as tool search and programmatic tool calling. It closes by arguing that MCP and skills are complementary: MCP exposes external capabilities, while skills provide the procedural knowledge for using those capabilities effectively.

## Sources

- [[source/building-agents-that-reach-production-systems-with-mcp|building-agents-that-reach-production-systems-with-mcp.html]]
- [[source/building-agents-that-reach-production-systems-with-mcp-markdown|building-agents-that-reach-production-systems-with-mcp-markdown.md]]
