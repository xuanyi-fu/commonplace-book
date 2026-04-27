---
type: summary
status: draft
created: 2026-04-27
updated: 2026-04-27
---

# minimal-editing-2026-04

This source collection preserves Nrehiew's blog post "Coding Models Are Doing Too Much" as raw HTML, a best-effort Markdown derivative, and localized copies of the article-body figures. It is meant to support later source-backed work on AI coding models, over-editing, minimal code editing, prompting effects, and training methods for faithful code edits.

## Structure

- `source/minimal-editing.html`: original webpage artifact captured directly from `https://nrehiew.github.io/blog/minimal_editing/`; this is the authoritative source
- `source/minimal-editing-markdown.md`: best-effort Markdown derivative of the article body, preserving heading order, links, tables, code blocks, footnotes, and figure captions
- `source/assets/minimal-editing/`: localized copies of the three article-body figures referenced by the Markdown derivative
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/minimal-editing-markdown.md` for a readable and searchable copy of the article.
- Use `source/minimal-editing.html` as the authoritative source for exact page structure, original HTML, original image references, and rendering details that the Markdown conversion may simplify.
- Use this collection when comparing model behavior around minimal bug fixes, reasoning vs non-reasoning editing style, explicit minimal-edit prompting, and RL-style training for minimal editing.
- No browser interaction was required before capture; the page was retrievable directly over HTTP.

## Summary

The post frames over-editing as a brown-field coding failure mode: a model can fix the bug while rewriting more of the surrounding code than the minimal patch requires, making review harder even when tests pass. It uses programmatically corrupted BigCodeBench problems to measure correctness and edit size, with token-level Levenshtein distance and added cognitive complexity as the main minimality metrics. [[source/minimal-editing-markdown]]

The article reports that frontier models vary widely in how much they over-edit. In the author's benchmark, Claude Opus 4.6 is both high on Pass@1 and low on diff size, while GPT-5.4 and GPT-5 High show much larger edits. Explicit prompting to preserve original code improves all models on edit minimality and is especially helpful for reasoning models. [[source/minimal-editing-markdown]]

The training section compares SFT, rejection-sampled SFT, DPO, and RL on a Qwen3 4B base model. The key result is that in-domain SFT looks very strong but fails out-of-domain, while RL produces more faithful edits without degrading LiveCodeBench performance; the article also reports LoRA and Qwen3 14B follow-up experiments. [[source/minimal-editing-markdown]]

## Sources

- [[source/minimal-editing|minimal-editing.html]]
- [[source/minimal-editing-markdown|minimal-editing-markdown.md]]
