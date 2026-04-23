---
type: summary
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# ralph-wiggum-method

This source collection preserves Geoffrey Huntley's article "Ralph Wiggum as a software engineer", which defines Ralph as a technique that runs an AI coding agent in a repeated Bash loop and then tunes the surrounding prompt, repository artifacts, tests, and feedback pressure over time. [[source/ralph-wiggum-method-markdown#^ralph-pure-bash-loop]] [[source/ralph-wiggum-method-markdown#^ralph-one-thing-per-loop]] [[source/ralph-wiggum-method-markdown#^ralph-backpressure]]

## Structure

- `source/ralph-wiggum-method.html`: original webpage HTML captured from `https://ghuntley.com/ralph/`; this is the authoritative source artifact.
- `source/ralph-wiggum-method-markdown.md`: best-effort Markdown derivative for reading, search, and reusable citations.
- `source/assets/ralph-wiggum-method/`: localized article assets used by the Markdown derivative, including the featured image, article screenshots, the Ralph process diagram, and the embedded MP4 plus thumbnail.
- `summary.md`: collection summary and usage guide.

## How To Use

- Start with `source/ralph-wiggum-method-markdown.md` for source-order reading, search, and citation.
- Return to `source/ralph-wiggum-method.html` when checking the original Ghost page structure, metadata, external embeds, or raw link targets.
- Use this collection as the evidence base for pages about the Ralph Wiggum method, single-loop AI coding workflows, greenfield agentic development, prompt/spec/test feedback loops, and context-window management.
- This capture did not require login or browser interaction. The derivative preserves the article's section order and localizes meaningful article assets; third-party YouTube and social embeds remain as external links or quoted embed text.

## Summary

The article defines Ralph in its simplest form as a Bash loop that repeatedly pipes `PROMPT.md` into an uncapped coding agent, but the method is not just "run a prompt forever". Huntley's operational pattern is monolithic: one repository, one process, one task per loop, and a deterministic stack of context artifacts such as the plan and specifications. [[source/ralph-wiggum-method-markdown#^ralph-pure-bash-loop]] [[source/ralph-wiggum-method-markdown#^ralph-monolithic-one-task]] [[source/ralph-wiggum-method-markdown#^ralph-one-thing-per-loop]] [[source/ralph-wiggum-method-markdown#^ralph-deterministic-stack]]

The article also frames Ralph as an engineering-feedback system. The main context should act like a scheduler while subagents handle expensive work; tests, type systems, static analysis, security scanners, and similar checks become backpressure that rejects bad code generation; and tests should record why they matter so later loops have useful local memory. [[source/ralph-wiggum-method-markdown#^ralph-primary-context-scheduler]] [[source/ralph-wiggum-method-markdown#^ralph-backpressure]] [[source/ralph-wiggum-method-markdown#^ralph-tests-as-memory]]

The stated boundary is narrow: Huntley argues Ralph is most suitable for greenfield bootstrapping and explicitly says he would not use it in an existing codebase. The piece also emphasizes that senior engineering judgment is still required to tune prompts, judge broken states, and decide when to rescue or restart the loop. [[source/ralph-wiggum-method-markdown#^ralph-greenfield-boundary]] [[source/ralph-wiggum-method-markdown]]

## Sources

- [[source/ralph-wiggum-method|ralph-wiggum-method.html]]
- [[source/ralph-wiggum-method-markdown|ralph-wiggum-method-markdown.md]]
