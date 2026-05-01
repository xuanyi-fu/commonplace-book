---
type: summary
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# cursor-sdk-2026-04

This source collection preserves the official Cursor materials around the April 2026 Cursor SDK public beta, including the launch blog, changelog announcement, TypeScript SDK docs, current pricing pages, and self-hosted Cloud Agents changelog.

## Structure

- `source/cursor-sdk-blog.html`: original Cursor blog page for "Build programmatic agents with the Cursor SDK"
- `source/cursor-sdk-blog-markdown.md`: best-effort Markdown derivative of the launch blog's main content
- `source/cursor-sdk-release-changelog.html`: original Cursor changelog page for the SDK release
- `source/cursor-sdk-release-changelog-markdown.md`: best-effort Markdown derivative of the SDK release changelog
- `source/cursor-sdk-typescript-docs.html`: original Cursor TypeScript SDK docs page
- `source/cursor-sdk-typescript-docs-markdown.md`: best-effort Markdown derivative of the TypeScript SDK docs surface
- `source/cursor-models-pricing.html`: original Cursor Models & Pricing docs page
- `source/cursor-models-pricing-markdown.md`: best-effort Markdown derivative of the pricing docs surface
- `source/cursor-pricing.html`: original Cursor pricing page
- `source/cursor-pricing-markdown.md`: best-effort Markdown derivative of the pricing page
- `source/cursor-self-hosted-cloud-agents-changelog.html`: original Cursor self-hosted Cloud Agents changelog page
- `source/cursor-self-hosted-cloud-agents-changelog-markdown.md`: best-effort Markdown derivative of the self-hosted Cloud Agents changelog
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/cursor-sdk-blog-markdown.md` for the launch positioning: Cursor presents the SDK as access to the same coding-agent runtime, harness, and models used by Cursor itself. [[source/cursor-sdk-blog-markdown|cursor-sdk-blog-markdown.md]]
- Use `source/cursor-sdk-typescript-docs-markdown.md` for concrete API-surface questions such as `Agent.create`, `local`, `cloud`, `mcpServers`, `agents`, and run-stream events. [[source/cursor-sdk-typescript-docs-markdown|cursor-sdk-typescript-docs-markdown.md]]
- Use `source/cursor-sdk-release-changelog-markdown.md` for the Cloud Agents API lifecycle/event changes introduced with the SDK release. [[source/cursor-sdk-release-changelog-markdown|cursor-sdk-release-changelog-markdown.md]]
- Use the pricing files only for public pricing surface and plan-access claims; do not infer an unpublished per-VM runtime price from these pages. [[source/cursor-models-pricing-markdown|cursor-models-pricing-markdown.md]] [[source/cursor-pricing-markdown|cursor-pricing-markdown.md]]
- Use `source/cursor-self-hosted-cloud-agents-changelog-markdown.md` when distinguishing Cursor-hosted Cloud Agents from self-hosted workers that keep code and tool execution inside the user's own infrastructure. [[source/cursor-self-hosted-cloud-agents-changelog-markdown|cursor-self-hosted-cloud-agents-changelog-markdown.md]]

## Summary

Cursor SDK is a public-beta TypeScript interface for programmatically creating Cursor agents. The official launch framing is not "call a model from TypeScript"; it is access to Cursor's coding-agent runtime, harness, and model surface across local, cloud, and self-hosted execution modes. The cloud mode uses Cursor Cloud Agents and dedicated VMs; local mode points at local working directories; self-hosted workers preserve code and tool execution inside the user's own infrastructure. [[source/cursor-sdk-blog-markdown|cursor-sdk-blog-markdown.md]] [[source/cursor-sdk-typescript-docs-markdown|cursor-sdk-typescript-docs-markdown.md]] [[source/cursor-self-hosted-cloud-agents-changelog-markdown|cursor-self-hosted-cloud-agents-changelog-markdown.md]]

The harness surface includes codebase indexing, semantic search, grep, MCP server configuration, repo skills, hooks, subagents, model routing, and streamable agent runs. The SDK release also updated the Cloud Agents API around durable agents, per-prompt runs, SSE streaming, reconnect, lifecycle controls, and separate `agent` / `run` objects. [[source/cursor-sdk-blog-markdown|cursor-sdk-blog-markdown.md]] [[source/cursor-sdk-release-changelog-markdown|cursor-sdk-release-changelog-markdown.md]] [[source/cursor-sdk-typescript-docs-markdown|cursor-sdk-typescript-docs-markdown.md]]

For this wiki, the collection is most useful as evidence that Cursor is packaging a coding-agent harness plus runtime as a developer-facing API. It should be compared with broader managed-agent platforms such as [[entities/claude-managed-agents|Claude Managed Agents]], but the scope is narrower and more coding-workflow-specific.

## Sources

- [[source/cursor-sdk-blog|cursor-sdk-blog.html]]
- [[source/cursor-sdk-blog-markdown|cursor-sdk-blog-markdown.md]]
- [[source/cursor-sdk-release-changelog|cursor-sdk-release-changelog.html]]
- [[source/cursor-sdk-release-changelog-markdown|cursor-sdk-release-changelog-markdown.md]]
- [[source/cursor-sdk-typescript-docs|cursor-sdk-typescript-docs.html]]
- [[source/cursor-sdk-typescript-docs-markdown|cursor-sdk-typescript-docs-markdown.md]]
- [[source/cursor-models-pricing|cursor-models-pricing.html]]
- [[source/cursor-models-pricing-markdown|cursor-models-pricing-markdown.md]]
- [[source/cursor-pricing|cursor-pricing.html]]
- [[source/cursor-pricing-markdown|cursor-pricing-markdown.md]]
- [[source/cursor-self-hosted-cloud-agents-changelog|cursor-self-hosted-cloud-agents-changelog.html]]
- [[source/cursor-self-hosted-cloud-agents-changelog-markdown|cursor-self-hosted-cloud-agents-changelog-markdown.md]]

