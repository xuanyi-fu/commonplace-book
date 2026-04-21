---
type: summary
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# codex-computer-use-2026-04

This source collection contains official OpenAI pages, a local tool-interface snapshot, and a user test note about Codex computer use as observed in April 2026. The collection is meant to support implementation-oriented reasoning about what Codex computer use appears to do today and where its current limits likely are.

## Structure

- `source/official-doc-codex-app-computer-use.md`: Codex app documentation for Computer Use, including permissions, approvals, and safety guidance
- `source/blog-2026-04-16-codex-for-almost-everything.md`: April 16, 2026 product post announcing background computer use in the Codex app
- `source/official-guide-api-computer-use.md`: official computer-use guide describing the screenshot and action loop behind OpenAI's computer-use tooling
- `source/local-session-computer-use-tool-interface-2026-04-20.md`: local snapshot of the Computer Use tool surface exposed in this Codex desktop session
- `source/user-test-sts2-drag-failure-2026-04-20.md`: neutral note capturing one concrete user test failure in Slay the Spire 2
- `summary.md`: the collection summary and usage guide

## How To Use

- Start with `source/official-doc-codex-app-computer-use.md` for the current public product contract of Codex computer use
- Use `source/blog-2026-04-16-codex-for-almost-everything.md` for the public rollout framing and availability claims
- Use `source/official-guide-api-computer-use.md` for the most explicit official description of the screenshot-action loop pattern
- Use `source/local-session-computer-use-tool-interface-2026-04-20.md` for direct evidence from the current Codex desktop environment about the available GUI-control primitives
- Use `source/user-test-sts2-drag-failure-2026-04-20.md` as one concrete failure case when reasoning about current boundaries
- Treat claims about specific native macOS internals as inference unless a public OpenAI source explicitly confirms them

## Summary

Taken together, these materials support a narrow but useful conclusion: as of April 2026, Codex computer use publicly presents as a screenshot-driven GUI agent with app approvals and a bounded action surface, not as a deep semantic integration with arbitrary apps. The official docs confirm Screen Recording and Accessibility permissions, screenshot handling, and GUI actions; the local tool surface adds direct evidence of app-state retrieval plus element-index and coordinate-based interaction.

## Sources

- [[source/official-doc-codex-app-computer-use|official-doc-codex-app-computer-use.md]]
- [[source/blog-2026-04-16-codex-for-almost-everything|blog-2026-04-16-codex-for-almost-everything.md]]
- [[source/official-guide-api-computer-use|official-guide-api-computer-use.md]]
- [[source/local-session-computer-use-tool-interface-2026-04-20|local-session-computer-use-tool-interface-2026-04-20.md]]
- [[source/user-test-sts2-drag-failure-2026-04-20|user-test-sts2-drag-failure-2026-04-20.md]]
