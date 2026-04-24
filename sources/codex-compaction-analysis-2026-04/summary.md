---
type: summary
status: draft
created: 2026-04-24
updated: 2026-04-24
---

# codex-compaction-analysis-2026-04

This source collection contains two Codex code-reading notes about compaction at [`openai/codex@d62421d32299aa5fdc30b131471eb06f03f1c91a`](https://github.com/openai/codex/tree/d62421d32299aa5fdc30b131471eb06f03f1c91a). Both source artifacts are normalized so code citations use pinned GitHub blob URLs instead of local relative Codex paths. [[source/compaction-trigger-analysis|compaction-trigger-analysis.md]] [[source/local-compaction-analysis|local-compaction-analysis.md]]

## Structure

- `source/compaction-trigger-analysis.md`: normalized Markdown source note on manual and automatic compaction trigger paths
- `source/local-compaction-analysis.md`: normalized Markdown source note on the local Responses-based compaction implementation
- `summary.md`: this collection summary and usage guide

## How To Use

- Start with `source/compaction-trigger-analysis.md` to understand when compaction is started manually, pre-sampling, and post-sampling.
- Then read `source/local-compaction-analysis.md` for the local compaction implementation path, including request construction, summary extraction, replacement history, context reinjection, and persistence.
- Treat this collection as code-reading evidence for the pinned Codex commit, not as official product documentation.
- Preserve the existing GitHub blob URLs when deriving wiki claims from this collection; do not translate them back into local relative Codex paths.
- If a later wiki page needs paragraph-level reuse, add minimal block ids to the specific source-note passages being cited.

## Summary

`compaction-trigger-analysis.md` maps the compaction entry points. Manual compaction can enter through app-server `thread/compact/start` or the TUI `/compact` command. Automatic compaction belongs to regular `codex-core` turn execution: it checks token usage before sampling, can also compact during model downshift, and can compact after sampling when the token limit is reached and follow-up work is still needed. [[source/compaction-trigger-analysis|compaction-trigger-analysis.md]]

The trigger note also defines `needs_follow_up`: model tool calls and some tool-call error paths create model-side follow-up work, while pending input can also keep the turn active. It ends by distinguishing the execution choice between remote compaction and local inline compaction. [[source/compaction-trigger-analysis|compaction-trigger-analysis.md]]

`local-compaction-analysis.md` follows the local `CompactionImplementation::Responses` path. It shows that local compaction builds a normal streaming Responses request from cloned history plus the compact prompt, retries by dropping oldest cloned-history items on context-window errors, extracts the last assistant output text as the summary, and stores replacement history as retained recent user messages plus a synthetic user-role summary message. [[source/local-compaction-analysis|local-compaction-analysis.md]]

The local implementation note also covers context reinjection differences between pre-turn/manual and mid-turn compaction, persistence through `CompactedItem` and `RolloutItem::Compacted`, token-usage recomputation, client-session reset, and the warning emitted after compaction completes. [[source/local-compaction-analysis|local-compaction-analysis.md]]

## Sources

- [[source/compaction-trigger-analysis|compaction-trigger-analysis.md]]
- [[source/local-compaction-analysis|local-compaction-analysis.md]]
