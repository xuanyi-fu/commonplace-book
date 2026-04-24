---
type: summary
status: draft
created: 2026-04-24
updated: 2026-04-24
---

# codex-v1-subagents-2026-04

This source collection contains a Codex code-reading note about the V1 subagent interface at [`openai/codex@d62421d32299aa5fdc30b131471eb06f03f1c91a`](https://github.com/openai/codex/tree/d62421d32299aa5fdc30b131471eb06f03f1c91a). The stored source note is normalized so code citations use pinned GitHub blob URLs instead of local relative paths. [[source/v1-subagents|v1-subagents.md]]

## Structure

- `source/v1-subagents.md`: normalized Markdown source note copied from the local Codex checkout, with relative code links rewritten to GitHub URLs pinned to `d62421d32299aa5fdc30b131471eb06f03f1c91a`
- `summary.md`: this collection summary and usage guide

## How To Use

- Start with `source/v1-subagents.md`; it is the usable source artifact for reading, search, and citation.
- Treat this collection as code-reading evidence for the pinned Codex commit, not as official product documentation.
- Preserve the existing GitHub blob URLs when deriving wiki claims from this collection; do not translate them back into local relative Codex paths.
- If a later wiki page needs paragraph-level reuse, add a minimal block id to `source/v1-subagents.md` at the specific passage being cited.

## Summary

The note documents the V1 subagent surface: `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`, including their model-callable inputs and returned status shapes. It also records when the V1 branch is selected relative to the `MultiAgentV2` branch, and highlights that V1 exposes `resume_agent`. [[source/v1-subagents|v1-subagents.md]]

The implementation walkthrough follows the lifecycle around parent awareness, subagent communication, spawn context, main-agent delegation instructions, and return routing. It explains how subagent state can appear in `<environment_context>`, how `send_input` submits `Op::UserInput`, how non-forked and forked spawns differ, where the V1 delegation policy text lives, and how the detached completion watcher injects `<subagent_notification>` fragments back into the parent thread. [[source/v1-subagents|v1-subagents.md]]

The final example records one observed local run where the parent spawned explorer agents, hit the six-agent thread limit on the seventh spawn, used `wait_agent` with timeouts and later completed statuses, and also received asynchronous completion notifications through the background watcher. [[source/v1-subagents|v1-subagents.md]]

## Sources

- [[source/v1-subagents|v1-subagents.md]]
