---
type: summary
status: draft
created: 2026-04-25
updated: 2026-04-25
---

# claude-code-scratchpad-2026-04

This source collection preserves a 2026-04-25 local Claude Code code-reading note about the `scratchpad` feature. The analyzed checkout is `/Users/bytedance/claude-code/claude-code` at commit `0a0498cf6a04d144aba289366a55b1edf328a797`; this is implementation evidence from a local source snapshot, not official Anthropic product documentation. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]

## Structure

- `source/original-claude-code-scratchpad.md`: original local Markdown snapshot from `/Users/bytedance/claude-code/claude-code/claude-code-scratchpad.md`
- `source/claude-code-scratchpad.md`: normalized Markdown derivative that preserves the original structure and replaces Claude Code source-code footnotes with fixed links to `heshan.pro/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797`
- `summary.md`: the collection summary and usage guide

## How To Use

- Start with `source/claude-code-scratchpad.md` when checking what the local source snapshot shows about `scratchpad` boundaries, path construction, prompt exposure, permission handling, and coordinator-worker context. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]
- Compare against `source/original-claude-code-scratchpad.md` if you need to verify that the normalized derivative did not change the original wording.
- Re-check the local checkout before turning this collection into a current-product claim, because the evidence is pinned to `0a0498cf6a04d144aba289366a55b1edf328a797`.
- Use this alongside [[sources/claude-code-context-assembly-2026-04/summary|claude-code-context-assembly-2026-04]] when the question is how Claude Code inserts implementation-specific state into model-visible context.

## Summary

The note describes `scratchpad` as a current-session temporary workspace for Claude Code agents: it is isolated from the user's project, scoped by project and `sessionId`, exposed through a `systemPrompt` section, and handled by the permission layer as a low-friction read/write area. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]

The core design claim is boundary management. Instead of writing agent working files into the user repo or a global `/tmp`, Claude Code gives the agent a bounded session-local place for intermediate data, temporary scripts, generated artifacts, and multi-agent coordination files. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]

Implementation-wise, the feature is gated by `tengu_scratch`, derives its path from Claude Code's temp root, sanitized original working directory, and `sessionId`, creates the directory with owner-only permissions, and lets the prompt tell Claude to prefer that directory for temporary file needs. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]

The note also records the enforcement side: scratchpad paths are normalized before matching, current-session scratchpad reads and writes are allowed by internal permission checks, shell path validation reuses those checks, and coordinator mode can expose the same directory as shared worker context. [[source/claude-code-scratchpad|claude-code-scratchpad.md]]

## Sources

- [[source/claude-code-scratchpad|claude-code-scratchpad.md]]
- [[source/original-claude-code-scratchpad|original-claude-code-scratchpad.md]]
- Local checkout: `/Users/bytedance/claude-code/claude-code@0a0498cf6a04d144aba289366a55b1edf328a797`
