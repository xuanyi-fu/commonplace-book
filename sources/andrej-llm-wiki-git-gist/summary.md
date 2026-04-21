---
type: summary
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# andrej-llm-wiki-git-gist

This source collection contains Andrej's gist about the LLM wiki pattern. The main content is a short idea document that explains the core concept, architecture, operations, indexing/logging, and optional tooling for a persistent LLM-maintained wiki.

## Structure

- `source/gist.md`: the raw gist text
- `summary.md`: the collection summary and usage guide

## How To Use

- Read `source/gist.md` first to understand the original proposal
- Use this collection as the canonical raw source when deriving summaries, concepts, and implementation rules for the wiki
- Treat the text as a high-level pattern description, not as an implementation spec

## Summary

The gist argues that an LLM should maintain a persistent markdown wiki between the user and the raw documents. Instead of re-deriving answers from raw files every time, the system should continuously update summaries, concept pages, entity pages, and syntheses as new sources are added.

## Sources

- [[source/gist|gist.md]]
