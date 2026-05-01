---
type: synthesis
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# Codex Goal System

Codex `goal` system 可以理解成 thread-scoped persistent objective：它把一个长期 objective 挂到 thread 上，由 runtime 在 thread 空闲时启动 continuation turn，并由模型在确认 objective 达成后通过受限 tool 标记完成。这个能力在 Codex `0.128.0` release note 里作为 persisted `/goal` workflows 发布，范围包括 app-server APIs、model tools、runtime continuation 和 TUI controls。[[sources/codex-goals-2026-05/source/codex-goals-release-note#^goal-release-note]]

## 核心机制

模型侧会看到三个 goal tools：`get_goal` 读当前 goal，`create_goal` 在明确要求时创建 goal，`update_goal` 只允许把 goal 标成 `complete`。`create_goal` 接收 `objective` 和可选 `token_budget`；`update_goal` 的 schema 只有一个 `status` 字段，而且 enum 只有 `complete`。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-tool-schemas]] [[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-complete-only]]

人用 `/goal <objective>` 设置目标时，TUI 会把它解析成 `SetThreadGoalObjective` app event；这条路径直接进入 thread goal state，不走普通 user message。底层持久化状态保存在 `thread_goals` 表里，除了 `objective`，还记录 `status`、budget、usage 和 timestamps。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-slash-entrypoint]] [[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-persistent-state]]

## Request 位置

goal 不进入 system prompt。Codex 构造 Responses request 时，顶层 `instructions` 仍然只来自 base instructions；goal system 影响的是顶层 `tools` 和后续 `input` stream。这个边界和 [[syntheses/codex-context-ordered-input-stream|Codex context 是有序 input stream]] 的一般模型一致：`instructions`、`tools`、`input` 是不同 request 面。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-responses-placement]] [[syntheses/codex-context-ordered-input-stream]]

自动续跑发生在 runtime 层。当 thread 没有 active turn、没有 pending input、goal 仍是 `active` 时，runtime 会创建 continuation candidate，把一条 `role: "developer"` 的 message 推入 Responses `input`，再启动一个新 turn。这条 developer message 的任务是让模型继续朝当前 objective 工作，并在真正完成前做 completion audit。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-continuation-input]] [[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-continuation-prompt]]

## 完成边界

`update_goal` 名字看起来像通用更新接口，但当前暴露给模型的能力很窄：模型只能把 goal 标成 `complete`。`paused` 由用户或 app 控制，`budget_limited` 由 runtime 根据预算状态控制，模型不能自己随意设置这些状态。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-complete-only]]

因此完整循环是：创建或设置 goal，runtime 在空闲时用 developer-role continuation message 推动模型继续工作，模型确认 objective 已达成且没有剩余工作后调用 `update_goal({ "status": "complete" })`，完成后 continuation candidate 会跳过 inactive goal，不再自动开新 turn。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-continuation-input]] [[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-complete-only]]

## 和其他 Codex 状态层的关系

`goal` 和 Codex memory 容易都被叫成“长期状态”，但它们解决的是不同问题。`goal` 是当前 thread 的执行目标和续跑调度信号；[[syntheses/codex-memory-support-and-boundaries|Codex Memory]] 是跨 thread 的知识沉淀和未来检索层。前者把一个 active objective 变成 continuation turn，后者把旧 thread 经验整理成可复用 memory。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-persistent-state]] [[syntheses/codex-memory-support-and-boundaries]]

它也可以看作 [[syntheses/codex-context-ordered-input-stream|ordered input stream]] 模型的一个新例子：runtime 不回写 system prompt，而是在合适时机追加 developer-role `input` item。理解这个点，比把 goal 当成“自动发一条 user message”更准确。[[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-responses-placement]] [[sources/codex-goals-2026-05/source/codex-goals-code-reading#^goal-continuation-input]]

## Sources

- [[sources/codex-goals-2026-05/summary|codex-goals-2026-05]]
- [[sources/codex-goals-2026-05/source/codex-goals-code-reading|codex-goals-code-reading]]
- [[sources/codex-goals-2026-05/source/codex-goals-release-note|codex-goals-release-note]]
- [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- [[syntheses/codex-context-ordered-input-stream|codex-context-ordered-input-stream]]
- [[syntheses/codex-memory-support-and-boundaries|codex-memory-support-and-boundaries]]
