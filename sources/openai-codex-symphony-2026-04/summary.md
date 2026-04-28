---
type: summary
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# openai-codex-symphony-2026-04

This source collection preserves OpenAI's April 27, 2026 engineering post "An open-source spec for Codex orchestration: Symphony" plus the linked Symphony `SPEC.md` snapshot. It is meant to preserve OpenAI's public framing of Symphony as a Codex App Server based orchestration pattern for turning issue trackers such as Linear into control planes for coding agents.

## Structure

- `source/openai-codex-symphony-reader-capture.md`: reader-captured webpage artifact for the OpenAI post
- `source/openai-codex-symphony-markdown.md`: best-effort Markdown derivative of the article body, with global site navigation/footer removed and the two main article diagrams localized
- `source/symphony-spec.md`: snapshot of the linked `openai/symphony` `SPEC.md` from GitHub `main` at commit `58cf97da06d556c019ccea20c67f4f77da124bf3`
- `source/assets/openai-codex-symphony/`: localized copies of the two OpenAI-hosted article diagrams referenced by the Markdown derivative
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/openai-codex-symphony-markdown.md` for a readable and searchable copy of the article body.
- Use `source/openai-codex-symphony-reader-capture.md` when you need the full captured page text, including social embeds and residual webpage chrome.
- Use `source/symphony-spec.md` for the linked Symphony service specification in readable form. Treat it as the GitHub `main` snapshot fetched during ingest, not as a guaranteed byte-for-byte reconstruction of the webpage's embedded code block.
- Use this collection when researching Codex orchestration, Codex App Server, issue-tracker-driven agent workflows, Linear-backed agent dispatch, and the shift from supervising coding sessions to managing work items.
- Direct raw HTML capture from `openai.com` was not practical during ingest because direct `curl` and headless Chrome attempts reached a Cloudflare challenge. No login was needed; the collection therefore preserves a reader capture as the practical webpage artifact.

## Summary

The post frames Symphony as OpenAI's answer to the context-switching ceiling of interactive coding agents: engineers could manage a few Codex sessions, but managing many sessions created a human-attention bottleneck. Symphony shifts the control surface from sessions and pull requests to issue-tracker work items: active Linear issues map to dedicated agent workspaces, an orchestrator keeps agents running, restarts stalled or crashed agents, and lets work decompose into larger units such as dependency-aware task DAGs. [[source/openai-codex-symphony-markdown|openai-codex-symphony-markdown.md]]

OpenAI reports that this workflow increased landed pull requests by 500% on some teams in the first three weeks, but the post treats the deeper change as economic and organizational: filing speculative tasks becomes cheap, non-engineers can initiate work through the tracker, and Symphony can shepherd long-running work through CI, rebases, conflicts, and review handoff. [[source/openai-codex-symphony-markdown|openai-codex-symphony-markdown.md]]

The article also records the tradeoff: moving from live session steering to ticket-level objectives reduces mid-flight nudging, so OpenAI added guardrails, skills, end-to-end tests, Chrome DevTools workflows, QA smoke tests, and clearer documentation. It argues that agents should receive objectives, tools, and context rather than being trapped in overly rigid state-machine transitions. [[source/openai-codex-symphony-markdown|openai-codex-symphony-markdown.md]]

The linked Symphony spec defines the orchestration layer as a scheduler/runner and tracker reader. It describes a service that polls the issue tracker, creates deterministic per-issue workspaces, loads a repo-owned `WORKFLOW.md`, launches a coding-agent app-server client, tracks retries and runtime state, and leaves ticket writes to the coding agent's tools or workflow environment. [[source/symphony-spec|symphony-spec.md]]

## Sources

- [[source/openai-codex-symphony-reader-capture|openai-codex-symphony-reader-capture.md]]
- [[source/openai-codex-symphony-markdown|openai-codex-symphony-markdown.md]]
- [[source/symphony-spec|symphony-spec.md]]
