---
type: synthesis
status: draft
created: 2026-05-14
updated: 2026-05-14
---

# Outcomes API vs Generator Evaluator Pattern

`outcomes` 是 Claude Managed Agents 把 `generator-evaluator loop` 产品化之后的一种 opinionated API：开发者向 session 发送 `user.define_outcome`，给出 `description`、必需的 `rubric`，以及可选的 `max_iterations`；Managed Agents harness 会自动 provision 一个独立 `grader`，用独立 context window 按 rubric 评估 artifact，再把逐项 feedback 交回主 agent 继续迭代。[[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]

它有意思的地方不只是“多了一个 grader”，而是把原本需要应用自己写的 outer loop 压成了 session-level protocol。outcome-oriented session 会在 event stream 里暴露 `agent.*` 进展事件和 `span.outcome_evaluation_*` 评估事件；一次 session 同时只支持一个 outcome，但可以在前一个 outcome 终止后继续 chain 下一个；终态结果包括 `satisfied`、`needs_revision`、`max_iterations_reached`、`failed` 和 `interrupted`。[[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]

## 它继承的是 generator-evaluator 模式

Anthropic 在 long-running app harness 文章里讲的底层模式，是把做事的 `generator` 和判断质量的 `evaluator` 分开。这个模式最早在 frontend design 里被用来把 subjective taste 变成可评分 criteria，然后让 generator 接收 evaluator feedback 反复迭代；迁移到 full-stack coding 后，`evaluator` 又承担 code review、QA、UI/API/database 实测和 hard threshold gate。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-harness-two-insights]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^full-stack-generator-evaluator-transition]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^hard-threshold-evaluator]]

这个分离真正解决的是 self-evaluation bias。文章里明确说，agent 评价自己生成的 work 时容易自信地夸奖 mediocre work；把执行 agent 和 judging agent 拆开，不能自动让 evaluator 可靠，但可以把 evaluator 单独调成更 skeptical，并让 generator 拿到外部 feedback。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^self-evaluation-bias]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^external-evaluator-skeptical-tuning]]

所以 `outcomes` 可以理解为 Managed Agents 对这个模式的一种平台化 preset：`description` 是 generator 要追的 target，`rubric` 是 grader 的 criteria，`max_iterations` 是 loop budget，`span.outcome_evaluation_*` 是 loop 状态面，独立 grader context 是 role separation 的实现边界。[[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]] [[syntheses/ralph-wiggum-loop-vs-planner-generator-evaluator|ralph-wiggum-loop-vs-planner-generator-evaluator]]

## 你的评论：pattern 对，API 未必该这么抽

更稳的判断是：`generator-evaluator loop` 是一个有用的 harness pattern，但不一定应该被强行抽象成所有场景都用的 `description + rubric` API。很多任务确实可以这样表达，尤其是 artifact 明确、验收标准稳定、迭代成本可接受的场景；但也有很多任务的 success definition 会在探索中变化，或者需要 evaluator 调用特定工具、跑特定实验、读特定 domain state，甚至需要人类在中间重新定义问题。

Anthropic 自己的 harness-design 文章也支持这个谨慎边界：frontend evaluator 需要 few-shot calibration 才能和人的偏好对齐；criteria 的措辞会直接 steer generator 的输出；迭代质量也不是单调变好，作者甚至会偏好中间某一轮而不是最后一轮。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^few-shot-evaluator-calibration]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^criteria-wording-steers-output]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^iteration-pattern-not-linear]]

因此，`outcomes` 最适合被记成“Anthropic 把 generator-evaluator loop 做成 Managed Agents 内置协议”的产品信号，而不是 generator-evaluator loop 的唯一正确形态。真实应用里更重要的是保留 loop 的结构原则：独立 judgment、明确 feedback path、可观察 iteration state、可中断和可恢复；至于 criteria 是 markdown rubric、自动测试、Playwright 实测、domain-specific checker，还是人类 approval，应该由任务自己决定。[[concepts/agent-harness|Agent Harness]] [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]

## Sources

- [[sources/claude-managed-agents-2026-04/summary|claude-managed-agents-2026-04]]
- [[sources/claude-managed-agents-2026-04/source/managed-agents-define-outcomes-markdown|managed-agents-define-outcomes-markdown.md]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown|harness-design-long-running-apps-markdown.md]]
- [[syntheses/ralph-wiggum-loop-vs-planner-generator-evaluator|ralph-wiggum-loop-vs-planner-generator-evaluator]]
- [[concepts/agent-harness|Agent Harness]]
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]
