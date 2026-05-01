---
type: summary
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# codex-goals-2026-05

这个 source collection 收录 Codex `goal` system 的两类证据：一份基于 `openai/codex@fe05acad23cb30fabcd942fbaabac358c32afd8b` 的本地代码阅读笔记，以及 GitHub `rust-v0.128.0` release note 中对 persisted `/goal` workflows 的发布说明。[[source/codex-goals-code-reading|codex-goals-code-reading]] [[source/codex-goals-release-note|codex-goals-release-note]]

## Structure

- `source/codex-goals-code-reading.md`: 代码阅读证据，覆盖 feature flag、持久化 state、model-visible tools、TUI `/goal` 入口、runtime continuation、Responses API request placement。
- `source/codex-goals-release-note.md`: 官方 GitHub release-note 证据，记录 `rust-v0.128.0` 对 persisted `/goal` workflows 的发布描述。
- `summary.md`: 这个 collection 的摘要和使用说明。

## How To Use

- 需要理解 Codex `goal` system 的实现路径时，先读 `source/codex-goals-code-reading.md`。
- 需要确认这个能力是官方 release note 中发布的功能时，读 `source/codex-goals-release-note.md`。
- 写 synthesis 时，把这个 collection 和 [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]] 一起使用：前者说明 goal 的具体功能，后者说明 Codex `instructions` / `input` / `tools` 的一般 request assembly 模型。

## Summary

代码阅读支持的核心判断是：Codex `goal` 是 thread-scoped 的持久目标状态，保存在 `thread_goals` 表里，模型侧暴露 `get_goal`、`create_goal`、`update_goal` 三个 tools；其中 `update_goal` 只能把 goal 标为 `complete`。[[source/codex-goals-code-reading#^goal-persistent-state]] [[source/codex-goals-code-reading#^goal-tool-schemas]] [[source/codex-goals-code-reading#^goal-complete-only]]

这个 goal 不进入 Responses API 顶层 `instructions`。当 thread 空闲、没有 pending input、goal 仍为 `active` 时，runtime 会创建 continuation turn，并把一个 `role: "developer"` 的 message 推入 Responses `input`，让模型继续朝当前 objective 工作。[[source/codex-goals-code-reading#^goal-responses-placement]] [[source/codex-goals-code-reading#^goal-continuation-input]]

GitHub `rust-v0.128.0` release note 把这组能力概括为 persisted `/goal` workflows，并点名包含 app-server APIs、model tools、runtime continuation、TUI controls。[[source/codex-goals-release-note#^goal-release-note]]

## Sources

- [[source/codex-goals-code-reading|codex-goals-code-reading]]
- [[source/codex-goals-release-note|codex-goals-release-note]]
