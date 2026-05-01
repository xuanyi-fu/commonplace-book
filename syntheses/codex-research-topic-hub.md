---
type: synthesis
status: draft
created: 2026-04-24
updated: 2026-05-01
---

# Codex Research Topic Hub

This page is a hub for Codex-related material currently covered in this wiki. It does not merge the source collections; it groups them by question so future reading starts from the right evidence type.

## Main Topics

### Codex memory

This topic has both product-level and implementation-level material. The product source covers current official docs, app UI, Chronicle, and local observations around whether memory is enabled or present. The implementation source covers the code-level pipeline across `app-server`, `core`, and `state`, including stage-one extraction, phase-two consolidation, prompt templates, `MEMORY.md`, and `memory_summary.md`. [[sources/codex-memory-2026-04/summary|codex-memory-2026-04]] [[sources/codex-memory-implementation-2026-04/summary|codex-memory-implementation-2026-04]]

Start from [[syntheses/codex-memory-support-and-boundaries|codex-memory-support-and-boundaries]] when the question is "how does Codex memory actually work?" Use the two source collections when checking product claims versus implementation details.

For a cross-agent implementation comparison, use [[sources/claude-code-auto-memory-2026-04/summary|claude-code-auto-memory-2026-04]] as the Claude Code side: it covers filesystem-based topic memory files, the `MEMORY.md` index, main-agent writes, `extractMemories`, `autoDream`, and relevant-memory recall in the local Claude Code snapshot. [[sources/claude-code-auto-memory-2026-04/summary|claude-code-auto-memory-2026-04]]

### Codex model context and prompt assembly

This topic is about what becomes model-visible context in a Codex turn. The primary implementation source is [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]], which analyzes how `openai/codex@d62421d` assembles model context inputs, including top-level `instructions`, `tools`, ordered `input`, developer-role context, contextual user fragments, skill injection, memory guidance, and later context diffs. [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]

Start from [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]] for the current working model: Codex context is best understood as top-level request controls plus an ordered `input` stream, not one flat prompt string. [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]

### Codex goals

This topic covers persisted `/goal` workflows: thread-scoped objective state, the `get_goal` / `create_goal` / `update_goal` model tools, TUI controls, and runtime continuation turns that inject developer-role messages into Responses `input`. [[sources/codex-goals-2026-05/summary|codex-goals-2026-05]]

Start from [[syntheses/codex-goal-system|codex-goal-system]] when the question is "how does Codex keep working toward a thread goal after the current turn ends?" Use [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]] for the broader `instructions` / `input` / `tools` framing.

### Codex compaction

This topic covers when compaction starts and what local compaction does. The current source collection maps manual triggers, pre-sampling automatic compaction, model-downshift compaction, post-sampling compaction, `needs_follow_up`, remote versus local compaction choice, local Responses-based summary generation, replacement history, context reinjection, and persistence. [[sources/codex-compaction-analysis-2026-04/summary|codex-compaction-analysis-2026-04]]

Start from [[sources/codex-compaction-analysis-2026-04/summary|codex-compaction-analysis-2026-04]] when the question is "when does Codex compact and what does it replace the old context with?"

### Codex V1 subagents

This topic covers the V1 subagent interface at `openai/codex@d62421d`: `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent`, model-callable input shapes, returned status shapes, parent awareness, spawn context, communication, and the return path back into the parent thread. [[sources/codex-v1-subagents-2026-04/summary|codex-v1-subagents-2026-04]]

Start from [[sources/codex-v1-subagents-2026-04/summary|codex-v1-subagents-2026-04]] when the question is about delegation mechanics rather than general prompt assembly.

### Codex computer use

This topic covers Codex desktop computer use as a GUI control loop. The source collection combines official docs, product rollout material, the API computer-use guide, a local tool-interface snapshot, and one concrete Slay the Spire 2 drag failure case. The current synthesis frames Codex computer use as screenshot plus accessibility-tree observation followed by discrete GUI actions, with limits around continuous low-latency control. [[sources/codex-computer-use-2026-04/summary|codex-computer-use-2026-04]] [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]]

Start from [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]] when the question is "what can computer use do today, and where does it break?"

## Supporting Background

### OpenAI Codex agent loop blog

[[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]] is useful background for the Codex agent loop, Responses API request shape, prompt caching, and compaction, but it should be used with caution because it contains outdated implementation details relative to `openai/codex@d62421d`. Treat it as supporting context for model context / prompt assembly, not as the primary current-code source. [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]] [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]

## Reading Order

If the question is broad, read in this order:

1. [[syntheses/codex-research-topic-hub|codex-research-topic-hub]]
2. [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]
3. [[syntheses/codex-goal-system|codex-goal-system]]
4. [[syntheses/codex-memory-support-and-boundaries|codex-memory-support-and-boundaries]]
5. [[sources/codex-compaction-analysis-2026-04/summary|codex-compaction-analysis-2026-04]]
6. [[sources/codex-v1-subagents-2026-04/summary|codex-v1-subagents-2026-04]]
7. [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]]

For code-level questions, prefer source collections pinned to a concrete `openai/codex` commit. Several older collections use `openai/codex@d62421d`; the goals collection uses the later `fe05acad` snapshot because `/goal` landed afterward. For product-surface questions, use the official-doc and local-observation collections. For older explanatory material, keep the "supporting background" boundary visible.

## Sources

- [[sources/codex-memory-2026-04/summary|codex-memory-2026-04]]
- [[sources/codex-memory-implementation-2026-04/summary|codex-memory-implementation-2026-04]]
- [[sources/claude-code-auto-memory-2026-04/summary|claude-code-auto-memory-2026-04]]
- [[syntheses/codex-memory-support-and-boundaries|codex-memory-support-and-boundaries]]
- [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]
- [[sources/codex-goals-2026-05/summary|codex-goals-2026-05]]
- [[syntheses/codex-goal-system|codex-goal-system]]
- [[sources/codex-compaction-analysis-2026-04/summary|codex-compaction-analysis-2026-04]]
- [[sources/codex-v1-subagents-2026-04/summary|codex-v1-subagents-2026-04]]
- [[sources/codex-computer-use-2026-04/summary|codex-computer-use-2026-04]]
- [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]]
- [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]]
