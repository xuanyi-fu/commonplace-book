---
type: entity
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# Ralph Wiggum method

The `Ralph Wiggum method` is Geoffrey Huntley's name for a repeated AI-coding loop whose minimal form is `while :; do cat PROMPT.md | claude-code ; done`. In practice, the method depends on more than the loop: the article describes a single-repository, single-process workflow that asks the agent to do one task per loop and repeatedly allocates the same plan/specification context. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-pure-bash-loop]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-monolithic-one-task]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-one-thing-per-loop]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-deterministic-stack]]

## What It Is

Ralph is a greenfield-oriented coding-agent operating pattern, not a standalone tool or model. The loop keeps restarting the agent with a prompt and local project artifacts, while the operator tunes the prompt, specs, `fix_plan.md`, `AGENT.md`, tests, and validation pressure based on what the loop does wrong. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-pure-bash-loop]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-greenfield-boundary]]

The central design choice is to avoid multi-agent orchestration as the primary shape. Huntley describes Ralph as monolithic: one repository, one process, and one task per loop. Subagents still appear, but the primary context acts more like a scheduler that delegates expensive work instead of carrying every intermediate allocation itself. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-monolithic-one-task]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-primary-context-scheduler]]

## Operating Pattern

The method relies on a small set of repeatable controls:

- Keep the loop's task narrow; if outcomes degrade, return to one item per loop. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-one-thing-per-loop]]
- Reallocate the same core project artifacts each loop, especially plan and specification files. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-deterministic-stack]]
- Use subagents for expensive search, comparison, and summarization work so the primary context stays smaller. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-primary-context-scheduler]]
- Wire in fast backpressure such as tests, type checks, static analysis, and other validators that can reject invalid code generation. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-backpressure]]
- Ask tests and documentation to capture why behavior matters, so future loops can reason about whether a test should be kept, changed, or removed. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-tests-as-memory]]

## Boundary

The article's strongest boundary is that Ralph is for bootstrapping greenfield work, with an expectation that it can get a project substantially complete but not necessarily clean or final. Huntley explicitly says he would not use Ralph in an existing codebase, and the article repeatedly treats senior engineering judgment as necessary for tuning, validation, and rescue decisions. [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-greenfield-boundary]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown]]

## Sources

- [[sources/ralph-wiggum-method/summary|ralph-wiggum-method]]
- [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown|ralph-wiggum-method-markdown.md]]
