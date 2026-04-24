---
type: synthesis
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# Ralph Wiggum Loop vs Planner Generator Evaluator

`Ralph Wiggum method` 和 Anthropic 的 `planner / generator / evaluator` 架构都属于 [[concepts/agent-harness|agent harness]] 问题，但它们补的是不同层的能力缺口。`RW loop` 更像轻量的 long-running execution scaffold：反复启动一个主 coding agent，让它读取 repo 里的 durable artifacts，并用 tests、build、static analysis 这类 `backpressure` 把明显坏掉的代码压回去。`planner / generator / evaluator` 则是更强的分工式 harness：`planner` 防 under-scope，`generator` 负责实现，`evaluator` 负责独立验收和 skeptical QA。[[entities/ralph-wiggum-method|Ralph Wiggum method]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-pure-bash-loop]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-backpressure]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-personas]]

## RW loop 补的是执行连续性

RW 的最小形态是一个 Bash loop，但实际有效的不是“无限重复 prompt”本身，而是同一个 repo、同一个 process、每轮只做一个 task，并且每轮都重新分配同一组 plan / spec / project files。也就是说，RW 的连续性主要不靠同一个 `context window` 长时间保存所有东西，而靠 filesystem 把状态外化：`fix_plan.md` 记录当前 backlog 和发现的问题，`AGENT.md` 记录怎么 build / test / run，repo 本身记录已经完成的代码状态。[[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-monolithic-one-task]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-one-thing-per-loop]] [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-deterministic-stack]]

这也是为什么 `fix_plan.md` 不应该直接等同于 Anthropic 的 `sprint construct`。它更像一个 durable plan / state ledger，可以由人先写，也可以让 agent 在 planning mode 里读 specs、src、examples 后生成或刷新。它给下一轮 agent 一个继续工作的入口，但它本身不包含独立验收、done criteria negotiation 或 per-sprint QA gate。[[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^sprint-contract]]

## PGE 补的是 scope 和 judgment

Anthropic 的 `planner / generator / evaluator` 架构是在 `generator/evaluator` loop 上继续扩展出来的。文章先从 frontend design 里引出 generator 和 evaluator：要把 subjective taste 变成可评分 criteria，并把 generation 和 grading 分开，让 generator 接收外部 feedback。随后它把这个模式迁移到 full-stack coding，把 code review 和 QA 当作 evaluator 的结构角色。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-harness-two-insights]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^full-stack-generator-evaluator-transition]]

PGE 的关键不是“多几个 agents”本身，而是把三个容易互相污染的职责拆开。`planner` 把 1-4 句话 raw prompt 扩成 product spec，但避免过早写死细节；`generator` 按 feature / sprint 做实现；`evaluator` 用 Playwright MCP 实测 UI、API 和 database state，并用 hard threshold 把 vague review 变成 pass/fail feedback。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-personas]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^hard-threshold-evaluator]]

## 最关键差距是 self-evaluation

RW 对 compile、unit test、typecheck、lint 这类明确 pass/fail 的任务比较适合，因为这些检查可以作为 `backpressure` 拒绝坏代码生成。Huntley 明确把 tests、build、static analysers、security scanners 这类东西放进 backpressure，并强调 loop 的速度要足够快。[[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-backpressure]]

但 RW 对模糊 criteria 的防护弱。Anthropic 文章指出，agent 评价自己产出的 work 时容易自信地夸奖 mediocre work，尤其在 design 这种没有 binary test 的任务里更明显；把做事的 agent 和判断的 agent 分开，是更可调的工程杠杆。这个点正好解释了 RW 的边界：RW 能防止一部分“代码明显坏掉”，但不擅长防止“方向看似前进、实际质量很差”。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^self-evaluation-bias]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^external-evaluator-skeptical-tuning]]

因此，`fresh context evaluator` 的价值不只是 fresh context，而是 role separation、skeptical tuning、rubric / hard threshold 三件事叠加。Anthropic 也承认 evaluator 不是天然可靠：Claude out of the box 作为 QA agent 会偏宽松、测试浅，必须读 evaluator logs，找出 judgment 和人类判断不一致的地方，再迭代 QA prompt。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^few-shot-evaluator-calibration]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^evaluator-qa-tuning]]

## Opus 4.6 后 RW 还剩什么意义

Anthropic 后来移除了 `sprint construct`，理由是 Opus 4.6 更能维持 long-running task coherence；但这不是说所有 scaffold 都没用了。文章里 `planner` 和 `evaluator` 仍被保留，因为 raw prompt 会让 generator under-scope，而 evaluator 的价值取决于任务是否落在当前模型 reliable solo 能力边界之外。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^remove-sprint-construct]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^planner-prevents-under-scoping]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^evaluator-load-bearing-boundary]]

所以 RW 在 SOTA 模型下的意义不再是“模型无法连续工作两小时，所以要强行循环”。它更像一种低成本 persistence / recovery pattern：处理中断、rate limit、上下文丢失、长期 backlog、重复 build/test 反馈，以及 greenfield bootstrapping 中大量明确可验证的小步推进。Huntley 自己也把边界收得很窄：Ralph 最适合 greenfield bootstrapping，预期把项目推到大约 90%，而不是接管既有代码库的高质量长期维护。[[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown#^ralph-greenfield-boundary]] [[entities/ralph-wiggum-method|Ralph Wiggum method]]

## 更稳定的组合方式

更稳的结论不是在 RW 和 PGE 之间二选一，而是把它们看成两层可组合 scaffold：

- RW 提供 outer loop：持续启动、读取 durable plan、跑 deterministic checks、更新 repo state。
- `planner` 提供 scope expansion：把 raw prompt 变成更完整但不过度实现化的 spec。
- `evaluator` 提供 independent judgment：对 product completeness、UX、visual design、edge cases、code quality 做 skeptical review。
- `sprint construct` 只是可选的更重执行协议；当模型足够强时可以删，但 durable plan、logs、tests 和 evaluator 未必能删。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^harness-components-encode-model-assumptions]] [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]

压成一句话：RW 是 `one worker agent + persistent files + deterministic backpressure`；PGE 是 `scope expansion + implementation + independent judgment`。RW 适合把可验证工程任务往前滚，PGE 适合处理需要明确 scope 和独立质量判断的复杂任务。两者都应该遵守 [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent harness 不要把任务智能过度写死成 rigid workflow]] 这个原则：只保留当前模型能力边界上仍然 load-bearing 的 scaffold。[[concepts/agent-harness|Agent Harness]]

## Sources

- [[sources/ralph-wiggum-method/summary|ralph-wiggum-method]]
- [[sources/ralph-wiggum-method/source/ralph-wiggum-method-markdown|ralph-wiggum-method-markdown.md]]
- [[entities/ralph-wiggum-method|Ralph Wiggum method]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown|harness-design-long-running-apps-markdown.md]]
- [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic-harness-design-long-running-apps-2026-04-reading-note]]
- [[concepts/agent-harness|Agent Harness]]
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]
