---
type: note
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# openai-codex-symphony-2026-04-reading-note

## Source

- source collection: [[sources/openai-codex-symphony-2026-04/summary|openai-codex-symphony-2026-04]]
- primary reading file: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown|openai-codex-symphony-markdown]]
- discussion language: Chinese

## Core Question

Symphony 这组材料想回答：团队怎样把 Codex 从需要人手动盯多个 session 的交互式工具，升级成以 issue tracker 为 control plane、能持续调度 coding agents 的 orchestration workflow？[[sources/openai-codex-symphony-2026-04/summary]]

Final takeaways:

- Symphony 的核心不是一个要长期维护的 standalone product，而是一个 reference pattern：用 issue tracker 作为 durable coordination store / human UI，用 Codex App Server 作为 headless execution interface，用 `SPEC.md` / `WORKFLOW.md` 把目标、runtime contract、repo workflow 和 handoff 规则写成 agent-readable harness。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-whats-next-reference-pattern|reference pattern]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-problem-automation-service|automation service]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-workflow-md-captures-workflow|WORKFLOW captures workflow]]
- 文章的管理视角比代码实现更重要：当 coding agents 变强，瓶颈从写代码迁移到管理 agentic work，人要从 session-level micromanagement 转向 issue / task / milestone / objective / harness 层面的 Engineering Management。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-human-attention-bottleneck|human attention bottleneck]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-deliverables-pivot|deliverables pivot]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-objectives-not-transitions|objectives not transitions]]
- 读这篇材料最有价值的 takeaway 是 harness-first / spec-driven development：不是只用 coding agent 写软件，而是和 coding agent 一起沉淀能让 coding agent 更稳定地写软件的 spec、workflow、tools、guardrails、tests、docs 和 validation surface。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-failures-to-harness|failures to harness]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-elixir-reference-spec-portability|spec portability]]

## Reading State

- source slug: `openai-codex-symphony-2026-04`
- primary reading file: `sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown.md`
- semantic cursor:
  - file: `sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown.md`
  - semantic position: `completed main article body before "### Community shoutouts"`
  - next unread source span: none for main article body; `### Community shoutouts` is social proof / postscript and was not read in detail
  - next boundary: none
  - completed spans:
    - opening framing under `# An open-source spec for Codex orchestration: Symphony`, before `### The ceiling of interactive coding agents`
    - `### The ceiling of interactive coding agents`
    - `### A shift in perspective`
    - `### Turning our issue tracker into an agent orchestrator` opening mechanism
    - `### Turning our issue tracker into an agent orchestrator` task DAG expansion
    - `### Turning our issue tracker into an agent orchestrator` agent-created work and cheap exploration
    - `### An increase in exploration from working this way`
    - `### Progress comes with new, different problems` ticket-level tradeoff and harness improvements
    - `### Progress comes with new, different problems` work-style boundary and objective-oriented management
    - `### Using Symphony to build Symphony` SPEC.md as steering and runtime contract
    - `### Using Symphony to build Symphony` Elixir reference implementation and spec portability
    - `### Using Symphony to build Symphony` prototype to app-server harness
    - `### What’s next`
- scout status:
  - `concept/entity scout`: refreshed locally through final takeaways; no subagents started
  - `related-pages scout`: refreshed locally through final takeaways; no subagents started
  - latest refresh point: after final takeaways

## Recall Log

### Opening framing

- source span: `# An open-source spec for Codex orchestration: Symphony`, opening body before `### The ceiling of interactive coding agents`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-agent-friendly-repo|agent-friendly repository]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-control-plane-framing|control plane framing]]
- guiding question: 作者为什么要引入 Symphony？它要解决什么问题？
- user recitation: 用户理解为：前提是这个 repo 已经被改造成 `agent friendly`，Codex 在里面可以很好运行；但现有 Codex 界面仍然偏 `single-agent-focus`，不适合同时管理多个 agents，所以在 agents 之间切换会很麻烦；Symphony 像是给 MAS 做一个 issue-tracker 风格的 control plane。
- calibrated understanding: 这个理解基本对。更精确地说，作者不是先在这里正式讨论 MAS 架构，而是在说“单个 Codex session 能工作以后，新的瓶颈变成人的 attention / context switching”。Symphony 的第一层动机是把 control surface 从多个 live sessions 迁移到 project-management board：每个 open task 对应一个 agent，agents 持续跑，人主要 review results。
- missing points:
  - opening 段落已经暗示上一阶段的 prerequisite：repo、tests、guardrails、workflow 都要先变得 agent-friendly，Symphony 不是替代这些基础设施，而是建在这些东西已经有效的前提上。
  - `issue tracker` 在这里不是普通任务列表，而是后续 orchestration 的 control plane。
- open questions:
  - 作者后面会不会把这个问题明确写成 MAS 问题，还是只用 orchestration / agent runs 的语言来描述？

### The ceiling of interactive coding agents

- source span: `### The ceiling of interactive coding agents`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-three-to-five-sessions|three to five sessions]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-human-attention-bottleneck|human attention bottleneck]]
- guiding question: interactive coding agents 在规模变大时的边界或失败模式是什么？
- user recitation: 用户理解为：随着 coding agent 越来越 capable，人可以同时操纵五六个 coding agents；但 context switching 一多，人就像操作系统 thrashing 一样变卡。再加上小事不断 `yield control back to human`，人就一直处在 micromanagement 位置，效果肯定不好。现在人的 attention 变成瓶颈，问题变成怎么让人管理更多 agents 干活；这其实是一个 Engineering Management 问题，issue tracker / Jira 这类项目管理工具自然会被 recall 出来。
- calibrated understanding: 这个理解很准确。这段的 ceiling 不是 model capability ceiling，而是 workflow / attention ceiling：interactive coding agent UI 把每个 agent run 变成一个需要人持续 assign、review、steer、debug 的 session。agent 越快、越多，人的 context switching 和 micromanagement 负担越明显，所以 bottleneck 从 coding throughput 转移到 work management throughput。
- missing points:
  - 原文给了一个经验边界：多数人舒适管理 `three to five sessions`，再多 productivity drops。
  - 这里的 `junior engineers` 类比强调 agent 很能干，但仍需要一个管理结构；所以后文转向 issue / task / ticket / milestone 并不是偶然，而是在把 agent operations 重新包装成工程管理问题。
- open questions:
  - Symphony 后面会怎样把传统 issue tracker 的人类项目管理语义改造成 agent orchestration 语义？

### A shift in perspective

- source span: `### A shift in perspective`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-deliverables-pivot|deliverables pivot]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-supervisor-spec|supervisor spec]]
- guiding question: 作者从 session / PR 转向 issue / task / ticket / milestone，这个 perspective shift 具体是什么？
- user recitation: 用户理解为：agent 现在足够 capable，能指挥一堆 agents 的人也变厉害了；所以人不该继续盯着 commit、merge pull request 这种低层 execution artifact，而应该进入 Engineering Manager 视角，思考更大的 work units：issue、tickets、tasks、milestones。
- calibrated understanding: 这个理解准确。作者在这里把 Codex work 的评价单位从 implementation surface 拉高到 deliverable surface：session 和 PR 是完成工作的手段，不是组织工作的根对象。Symphony 因此不是要优化“怎么开更多 sessions”，而是把 agents 接到已经承载工程管理语义的 task tracker 上，让它们从 issue / task / ticket / milestone 这类对象里 pull work。
- missing points:
  - `merged PRs` 也被作者降级为 means to an end；这说明 Symphony 不只是在替换 UI，而是在重新定义 agent work 的 primary object。
  - `written spec` 在这里首次出现，暗示 Symphony 首先是一套 supervisor/orchestration contract，而不只是一个现成产品。
- open questions:
  - 下一段会具体说明 issue tracker 怎样从 project management surface 变成 agent orchestrator。

### Turning our issue tracker into an agent orchestrator: opening mechanism

- source span: `### Turning our issue tracker into an agent orchestrator`, opening body through `Linear as a state machine`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-open-task-agent|open task agent]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-linear-issue-workspace|Linear issue workspace]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-linear-status-state-machine|Linear status state machine]]
- guiding question: Symphony 是怎么把 issue tracker 变成 agent orchestrator 的？输入、状态机、运行单元分别是什么？
- user recitation: 用户理解为：Symphony 相当于是一套围绕 Linear 来做的 MAS orchestrator；核心点是每个 Linear issue 都要有一个 active agent 去推进。
- calibrated understanding: 这个理解基本准确。更精确地说，在当前文章/spec 语境里，Linear issue 是 work object，dedicated agent workspace 是运行隔离单元，Linear ticket status 是 orchestration state machine；Symphony 负责持续 watch task board、确保 active task 有 agent running、并在 crash/stall 时 restart。它是围绕 Linear issue/status 建的 agent orchestration layer，但不是把所有业务逻辑都塞进 orchestrator。
- missing points:
  - `open task should get picked up and completed by an agent` 是这段最小原则；它不只是“issue 有 agent”，而是 active issue 应该持续有 agent loop 推进到 handoff/done。
  - spec 边界显示 Symphony 自身更像 `scheduler/runner and tracker reader`；ticket writes、comments、PR links 等通常由 coding agent 通过 workflow/tooling 完成。
- open questions:
  - 下一段会把 issue/workspace/session 的一对一映射继续放大成更大的 work unit：multi-PR、multi-repo、investigation、task DAG 和 blocked dependency。

### Turning our issue tracker into an agent orchestrator: task DAG expansion

- source span: paragraph beginning `In practice, Symphony decouples work from sessions and from pull requests.` through the React upgrade DAG example
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-decouple-work-from-prs|decouple work from PRs]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-larger-work-units|larger work units]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-task-tree-dependencies|task tree dependencies]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-dag-blocked-tasks|DAG blocked tasks]]
- guiding question: issue-level orchestration 是怎么把一个大 work unit 变成可并行执行的 task DAG 的？
- user recitation: 用户理解为：以前的 plan 多是从单个 agent、单个任务角度做 plan；现在视野要放宽，让模型把一个大任务逐步梳理成尽量可以多线并行的 DAG。每条线可以近似理解成 milestone，每个 milestone 下有很多 task，每个 task 对应 agent 去干活。这相比随便开几个 Codex sessions，多了两层 topology：一是 agents 之间通过 Linear 这个平台沟通形成 communication topology，二是任务本身有 dependency topology，而不是随便几个并行任务。
- calibrated understanding: 这个理解抓住了结构增量。源文直接支持的是 task topology：ticket 可以代表更大的 work unit，agent 先生成 implementation plan，再生成 task tree，task 被 stages 和 dependencies 组织成 DAG，未 blocked 的 task 才并行启动。用户说的 communication topology 是合理推断：因为 agents 不是直接在聊天窗口里互相喊话，而是通过 Linear issue/status/dependency/comment/PR 等平台对象间接协调；不过这段原文还没有正式展开 agent-to-agent communication，只展开了 work dependency graph。
- missing points:
  - 原文明确把 work 从 PR/session 中解耦：一个 issue 可以产出多个 PR、跨 repos，也可以是纯 investigation/analysis 而不改代码。
  - `milestone` 是一个有帮助的管理类比，但原文当前 span 更精确的词是 `tree of tasks`、`stages`、`dependencies` 和 `DAG`。
- open questions:
  - 下一段会说明 agents 不只是消费任务，还能在实现或 review 中发现新的 work，并把 follow-up issue 写回 Linear。

### Turning our issue tracker into an agent orchestrator: agent-created work and cheap exploration

- source span: paragraph beginning `Agents can also create work themselves.` through the devbox/phone example
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-agent-created-work|agent-created work]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-ambiguous-work-cheap-exploration|cheap ambiguous exploration]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-always-on-devbox|always-on devbox]]
- guiding question: agent 自己创建 follow-up work 和 always-on orchestrator，分别怎样降低人启动 ambiguous work 的成本？
- user recitation: 用户最喜欢的是 ambiguous work 变得成本更低：探索成本一下子变低了，当然前提是能付 token 成本。团队不必 active 地参与每一个 exploration，而是让 agent plan 出几个可能方向，再 plan 每个方向怎么 explore，然后创建 task 去执行。
- calibrated understanding: 这个理解准确。这段的核心不是简单提高 output，而是降低 exploration 的 activation energy：agent 在实现/review 中发现 out-of-scope opportunities 后可以 file follow-up issues；人只需要 evaluate/schedule，而不必把所有想法立即塞进当前任务或亲自开 session 探索。Always-on devbox orchestrator 则让任务入口变轻，人可以随时把 ambiguous idea ticket 化，让 agent prototype/explore，失败结果也只是便宜的信息。
- missing points:
  - 原文仍然保留 human oversight：follow-up issue 是 `we can evaluate and schedule later`，不是 agent 完全自治排期。
  - `near zero cost` 是相对 human effort / cognitive cost 而言；用户补充的 token cost caveat 很重要。
- open questions:
  - 下一节会把这种 cheap exploration 进一步上升为团队行为变化：more output、more speculative tasks、更宽的 initiator group。

### An increase in exploration from working this way

- source span: entire `### An increase in exploration from working this way` section
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-500-percent-output-deeper-shift|500 percent output and deeper shift]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-change-economics-human-effort|change economics]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-speculative-tasks|speculative tasks]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-nonengineer-review-packet|non-engineer review packet]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-monorepo-last-mile|monorepo last mile]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-engineers-focus-exploratory|engineers focus exploratory]]
- guiding question: 这一节给了什么 evidence/result？这些结果说明 Symphony 怎样改变团队对 work 的经济学和组织方式？
- user recitation: 用户聚焦技术团队成员：工程师被解放了，原来要在 Codex sessions 之间切换、效率不高；现在不难的活交给 agents，人主要做探索性工作。
- calibrated understanding: 这个复述抓住了技术团队视角的核心。文章表面 evidence 是 landed PR 增加 500%，但作者说 deeper shift 是 work economics：工程师不再亲自驱动 implementation，change 的 perceived cost 下降，routine implementation 和 PR landing pipeline 被代理出去，人从 session supervisor 变成 allocator/reviewer，并把注意力转向 harder, more exploratory tasks。
- missing points:
  - 这一节还扩展了 who can initiate work：PM/designer 不需要 checkout repo 或管理 Codex session，也能直接提交 feature request 并拿到 review packet / product video walkthrough。
  - 在 large monorepo 里，Symphony 也处理 PR landing 的 last mile：watch CI、rebase、resolve conflicts、retry flaky checks，把 `Merging` 前后的 babysitting 成本降下来。
- open questions:
  - 下一个大标题会讲这种模式的新 tradeoffs：少了 mid-flight nudging，ticket-level delegation 会带来新的失败模式。

### Progress comes with new problems: ticket-level tradeoff and harness improvements

- source span: section opening from `Operating at this level comes with tradeoffs.` through `clarified what good looks like.`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-ticket-level-tradeoff|ticket-level tradeoff]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-failures-to-harness|failures to harness]]
- guiding question: ticket-level delegation 的代价是什么？作者怎样把 agent 失败转化成 harness / system 改进？
- user recitation: 用户概括为：这一段主要观点不是用 coding agent 去开发软件，而是用 coding agent 去开发能让 coding agent 自己开发软件的 harness。
- calibrated understanding: 这个概括抓住了本段的 meta-engineering 含义，但要稍微收窄：作者不是说 coding agent 不用于开发软件，而是说当 agent output miss the mark 时，高杠杆动作不是人手动 patch 这个结果，而是把失败反馈到 guardrails、skills、tests、Chrome DevTools workflow、QA smoke tests、docs 和 `what good looks like` 里。也就是让 coding agent 的失败推动 harness 变强，使下一次 coding agent 更能自己开发软件。
- missing points:
  - 这一段的前提代价是：从 interactive steering 变成 ticket-level assignment 后，人失去 mid-flight nudge / course-correct 能力，所以失败会更像系统性 gap，而不是一次局部操作失误。
  - 这和 Anthropic harness reading note 互相支持：每个 `agent harness` component 都是在编码当前模型做不到什么；Symphony 这里则把 agent failure 转译成新的 harness components / docs / criteria。[[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic harness reading note]]
- open questions:
  - 下一段会划清边界：哪些任务不适合 Symphony style，仍需要 engineer 直接用 interactive Codex session。

### Progress comes with new problems: work-style boundary and objective-oriented management

- source span: paragraph beginning `Not every task fits the Symphony style of work.` through `let them cook.`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-boundary-exploratory-work|boundary for exploratory work]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-routine-work-focus|routine work focus]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-agents-not-rigid-nodes|agents not rigid nodes]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-objectives-not-transitions|objectives not transitions]]
- guiding question: 这段分别说明 Symphony style 的适用边界，以及 team 应该怎样管理越来越 capable 的 Codex agents？
- user recitation: 用户纠正：这两个点没有强连接。第一点是 task-oriented MAS 能把人从一个个 Codex session 中解放出来，让人去做更困难、更令人兴奋的 exploratory work；第二点是团队之前把 Codex 看扁了，Codex 可以做更多事情，所以人的工作应该像好 manager 一样给资源、context、工具，弄好 harness，而不是 micromanage 每个 transition。
- calibrated understanding: 这个纠正准确。这里应读成两个并列 lessons：一是 Symphony 不适合所有任务，ambiguous / judgment-heavy / expertise-heavy work 仍适合 engineer 直接用 interactive Codex session，但 routine implementation 可以交给 task-oriented MAS，从而减少 session-level context switching；二是 agent capability 已经超出“只 implement 一个 feature task”的窄盒子，系统应该提供 `gh` CLI、CI log skills 等 tools 和足够 context，让 Codex 处理 PR、review feedback、CI、old PR cleanup、reporting 等更宽 workflow。
- missing points:
  - `Not every task fits` 不是在否定 Symphony，而是在划清分工：routine implementation 进入 orchestrator，hard exploratory work 留给人集中注意力。
  - `objectives instead of strict transitions` 的重点是 management style：把 agent 当作会 reasoning 的 direct report，给目标、资源、context、tools，而不是把它锁进过细的 state machine。
- open questions:
  - 下一节会展示作者怎样用这种 spec / objective / harness 思路反过来建设 Symphony 本身。

### Using Symphony to build Symphony: SPEC.md as steering and runtime contract

- source span: opening paragraph of `### Using Symphony to build Symphony` plus the linked `SPEC.md` snapshot excerpt
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-spec-as-steering|SPEC.md as steering]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-problem-automation-service|long-running automation service]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-normalized-issue-fields|normalized issue fields]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-dispatch-eligibility|dispatch eligibility]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-workspace-reuse|workspace reuse]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-workflow-prompt-template|WORKFLOW prompt template]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-worker-continuation|worker continuation]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-app-server-thread-turn|app-server thread/turn reuse]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-tracker-writes-boundary|tracker writes boundary]]; [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown#^codex-agent-loop-turn-thread-history|Codex thread/turn history]]
- guiding question: `SPEC.md` 在 Symphony 里到底定义了什么，哪些逻辑属于 Symphony daemon，哪些逻辑属于 repo 的 `WORKFLOW.md` 和 Codex worker？
- user recitation: 用户结合另一个 thread 的研究总结：Symphony 只借用 Linear issue-tracker surface 的一小部分，如 issue、state、priority、labels、blockers、comments/links；Linear 更像 durable coordination store 和 human UI，而不是 Symphony 采纳 Linear 的 cycle/milestone/project/initiative 方法论。Symphony daemon polling Linear issue list，过滤 eligible active issues，为每个 issue 创建或复用 deterministic workspace，并启动 per-issue Codex worker。worker 在 Codex thread 上把按 `WORKFLOW.md` 渲染出的 prompt 作为首个消息推入；多轮 turn 之间靠 workspace、workpad comment、issue state、PR artifacts 和 thread history 续接。agent 可通过 Linear tool/skill 操作 issue；只要 issue 仍 eligible active，daemon 就持续 nudge 新 turn，直到 agent 把 issue 状态改成 noneligible。`SPEC.md` 定义 Symphony 的逻辑；项目自己的 `WORKFLOW.md` 定义 agent 怎么工作、workspace 怎么 setup。
- calibrated understanding: 这个总结基本是本段真正的 runtime reading。原文说 `SPEC.md` 给 agents high-level steering，spec 里具体落成了几层 contract：orchestrator 负责 poll、candidate selection、claim/running/retry、workspace lifecycle 和 app-server launch；normalized Linear issue 只保留调度和 prompt rendering 需要的字段，不等于把 Linear 全套项目管理方法论搬进来；`WORKFLOW.md` 是 repo-owned policy layer，既包含 runtime config，也包含 per-issue prompt template；Codex worker 的执行延续依赖同一 workspace、同一 live thread 的 continuation turns、tracker state re-check 和 workflow/tooling 写回 tracker。Codex agent loop source 可支撑 thread/turn 续接的背景：一个 Codex thread 的后续 turn 会带入历史 messages 和 tool calls，turn 内也可多次 inference/tool-call 迭代。
- missing points:
  - 当前 public spec 直接写到的 agent-side Linear tool 是 optional `linear_graphql` client-side tool extension；如果说 `linear skill` 或 `workpad comment`，应标为另一个 thread 的 implementation research / local terminology，而不是这篇文章 opening paragraph 自己已经完整展开的术语。
  - `comments/links` 更稳妥地归到 tracker writes / workflow tooling：spec 明确 orchestrator 不内建 ticket mutation business logic，state transition、comments、PR metadata 这类写入通常由 coding agent 通过工具完成。
- open questions:
  - 下一段会说明为什么作者选择 Elixir reference implementation，以及为什么鼓励读者把 spec 交给 coding agent 自己实现一版。

### Using Symphony to build Symphony: Elixir reference implementation and spec portability

- source span: paragraph beginning `The reference implementation is written in Elixir` through `have it implement its own version.`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-elixir-reference-spec-portability|Elixir reference and spec portability]]
- guiding question: 这一段里 `Elixir reference implementation` 和 Markdown `SPEC.md` 分别承担什么角色？
- user recitation: 用户理解为：这个项目不是主要拿来给你直接使用的，而是展示一种 `spec driven dev` 思路；软件实现不重要，重要的是能用来做出软件的 agent harness。换句话说，不是和 coding agent 一起开发软件，而是和 coding agent 一起开发“开发软件的 harness”。
- calibrated understanding: 这个复述抓住了这段的 meta-point。Elixir reference implementation 是 proof / demo：当 code is effectively free 时，implementation 可以按 runtime strengths 选择语言；但 OpenAI 真正要开源和传播的是可被 coding agent 消化的 `SPEC.md`，也就是问题定义、系统 contract 和 harness shape。读者不一定应该部署这份 Elixir implementation，而是应该把 spec 当作 prompt / steering artifact，让自己的 coding agent 在自己的环境里生成合适版本。
- missing points:
  - “实现不重要”更稳妥地说是“实现不是主要可复用资产”；实现仍然验证 spec 是否足够清楚、是否能落成可运行系统。
  - 这一段强化了前面的 manager/harness 视角：人类的高杠杆产物不是每一行代码，而是能让 agent 稳定产出代码的 spec、workflow、tools、context 和 validation surface。
- open questions:
  - 下一段会回到历史演进：从 `tmux` 里的 Codex session，到内嵌主 repo，再到用 Symphony build Symphony。

### Using Symphony to build Symphony: prototype to app-server harness

- source span: paragraph beginning `The first version of Symphony was just a Codex session running in tmux` through the Codex App Server / dynamic tools paragraph
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-tmux-to-main-repo-harness|tmux to main repo harness]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-dogfood-build-itself|dogfood build itself]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-spec-implementation-pressure|spec implementation pressure]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-core-invariant|core invariant]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-workflow-md-captures-workflow|WORKFLOW captures workflow]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-app-server-headless-api|App Server headless API]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-app-server-dynamic-tools-linear|dynamic tools for Linear]]
- guiding question: Symphony 是怎样从脆弱 prototype 沉淀成可复用 spec / workflow / app-server harness 的？
- user recitation: 用户表示这一段没有必要继续总结，要求直接进入下一段。
- calibrated understanding: 低细节记录即可。这段补充了演进路线：早期 `tmux` + polling Linear + sub-agents 能跑但不可靠；放到 agent-friendly 主 repo 后，Symphony 连接已有 harness；dogfooding 之后，团队把内部系统抽成 standalone `SPEC.md`，用多语言 implementation 压力测试 spec 歧义；最后把核心 invariant 简化为每个 open task 都有独立 workspace 里的 agent running，并用 `WORKFLOW.md` 显式记录人类原本隐性的开发流程。Codex App Server 则把交互面从 CLI / live `tmux` 换成 headless JSON-RPC API，并通过 dynamic tool calls 暴露 `linear_graphql`，避免把 Linear token 暴露给 containers。
- missing points:
  - 用户已明确低兴趣，不需要在主线讨论中展开。
- open questions:
  - `What’s next` 会把本文定位为 reference implementation / demonstration，而不是长期维护的 standalone product。

### What's next

- source span: entire `### What’s next` section before `### Community shoutouts`
- source citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-whats-next-reference-pattern|reference pattern]]; [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-bottleneck-agentic-work-management|agentic work management bottleneck]]
- guiding question: 作者最后怎样定位 Symphony 的 open-source 价值，以及他认为下一阶段的瓶颈会迁移到哪里？
- user recitation: 用户确认主文已读完。
- calibrated understanding: 这一节把 Symphony 明确降格为 intentionally minimal orchestration layer / reference implementation，而不是 OpenAI 打算长期维护的 standalone product。真正的 power 来自 Codex 和 Codex App Server；Symphony 只是把 Codex、Linear 和 workflow tools 连接起来解决 work management problem。作者预计其他公司也会遇到同样的瓶颈迁移：当 coding agents 更会 reasoning 和 following instructions，瓶颈会从 writing code 转向 managing agentic work。
- missing points:
  - `Community shoutouts` 之后主要是社区引用 / social proof，不影响主文 argument；本 reading note 将主文读到 `What’s next` 结束视为完成。
- open questions:
  - 后续可考虑把本文和 Anthropic harness / Multica synthesis 合成一个更高层概念页：`harness-first agent work management` 或 `issue tracker as agent control plane`。

## Questions And Answers

### Is Symphony built on Linear?

- user question: 用户质疑 “Symphony 只是监听 Linear，然后把 active issue 映射成 workspace/session” 这个说法是否准确；是否应该说 Symphony 是建立在 Linear 之上的？
- answer: 更准确的说法是：在这篇文章和当前 spec 版本里，Symphony 的具体 issue tracker adapter 是 Linear，所以它确实把 Linear issue/status 当作当前 control plane；但 Symphony 不是 Linear 内置功能，也不应该被说成只等于 Linear。spec 把它定义为 long-running automation service：持续从 issue tracker 读取 work，给每个 issue 创建 isolated workspace，并在 workspace 里运行 coding agent session。当前 spec 支持 `tracker.kind == "linear"`，但同时明确 non-Linear implementation 可以改变 transport，只要 normalized issue domain model 匹配。因此 “建立在 Linear 之上” 对当前实现/文章语境成立；作为架构抽象，更准确是 “建立在 issue tracker adapter 之上，当前版本是 Linear-compatible”。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-control-plane-framing|control plane framing]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec|symphony-spec]]
- supporting citation: [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-control-plane-framing|article framing]]; [[sources/openai-codex-symphony-2026-04/source/symphony-spec|spec problem statement and Linear-compatible tracker contract]]

### Which Anthropic harness article supports the harness-gap interpretation?

- user question: 用户问 “agent 做错不是只修结果，而是问当前 harness 没把什么能力/约束编码进去” 这个类比来自哪篇文章，并要求在 Symphony reading note 里 link 起来。
- answer: 对应本库的 [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]] 和 [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic-harness-design-long-running-apps-2026-04-reading-note]]。该 reading note 的 final takeaway 明确写到：每个 `agent harness` component 都是在编码一个“当前模型做不到什么”的假设，因此 harness 必须随着模型变强不断调整。这个观点和 Symphony 本段互为佐证：Symphony 中 agent miss the mark 后，团队没有只 patch result，而是加入 guardrails、skills、e2e tests、Chrome DevTools workflow、QA smoke tests、docs 和 clearer definition of good，从而把失败沉淀回 system / harness。[[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic harness reading note]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^harness-components-encode-model-assumptions|harness components encode assumptions]]
- supporting citation: [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic harness reading note]]; [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^harness-components-encode-model-assumptions|harness components encode model assumptions]]

## Reader Comments

- 用户指出：这段 Symphony 的动机很像 Multica。两者都把多 agent 工作从单个 chat/session UI 抽到一个平台化 work object 层：Symphony 说用 issue tracker / Linear 作为 coding agents 的 `control plane`，Multica 则把共享状态放在 `workspace`、`issue`、`comment`、`agent`、`skill`、`agent_task_queue`、`chat_session` 等平台对象里，再由 daemon 重建 agent 执行环境。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-control-plane-framing|Symphony control plane framing]] [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]
- 用户把 `context switching` 类比成操作系统 thrashing：当人同时盯太多 agent sessions，并且小事都需要 `yield control back to human`，人的注意力调度会变成系统瓶颈。用户进一步指出，这把 coding-agent scaling 问题推回了 Engineering Management / project management 领域，所以 Jira / issue tracker 这类工具会自然成为可 recall 的管理界面。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-three-to-five-sessions|three to five sessions]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-human-attention-bottleneck|human attention bottleneck]]
- 用户指出：当 agent 和 agent manager 都更 capable 以后，人应该停止把注意力放在 commit / merge PR 这些低层交付动作上，而是像 Engineering Manager 一样从 issue、tickets、tasks、milestones 这些更大的 work units 组织 agent work。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-deliverables-pivot|deliverables pivot]]
- 用户评论：从当下视角看，Symphony 之所以可行，是因为模型已经比较能完成 long-running agentic tasks；若放在更早模型时代，agentic long task 没有被充分优化，issue-level delegation 很难成立。这呼应 Anthropic harness reading 里的结论：`harness` components encode current-model capability assumptions，模型变强后一些 scaffold 会过时；例如 Opus 4.6 后作者移除了 `sprint construct`，因为模型更能维持 long-running task coherence。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^harness-components-encode-model-assumptions|harness components encode model assumptions]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^remove-sprint-construct|remove sprint construct]]
- 用户的 forward-looking speculation：如果模型能力继续提高，也许未来连 agent 之间的协作拓扑都不需要人手动管理，agent 能自己组建小队并组织 topology。这个方向可以用 Sakana Fugu / Conductor 作为外部参考：Sakana Fugu 官方介绍把它描述为会自动处理 model-pool coordination、建立 collaboration topology、分配 roles 和 subtasks 的 multi-agent orchestration system；Conductor 论文摘要进一步说，Conductor 学习为 agent-to-agent collaboration 设计 targeted communication topologies。这里目前只能作为相邻研究信号，不应写成 Symphony 本文已经证明的结论。[Sakana Fugu official post](https://sakana.ai/fugu-beta/) [Conductor arXiv](https://arxiv.org/abs/2512.04388)
- 用户指出：这段相比“随手开几个 Codex sessions”的关键增量，是同时出现两种 topology：任务 dependency topology，以及通过 Linear 平台对象形成的 agent coordination / communication topology。前者由原文的 task tree / dependencies / DAG 直接支持；后者是对 Linear 作为 control plane 的合理抽象。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-task-tree-dependencies|task tree dependencies]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-dag-blocked-tasks|DAG blocked tasks]]
- 用户指出：这一节最有价值的是 ambiguous work 的探索成本变低。团队不必 active 地参与每个 exploration，可以让 agent 先 plan 多个可能方向，再为每个方向 plan exploration task 并执行；人保留 evaluate / schedule / discard 的决策角色。用户同时补充：这个低成本是相对人类注意力成本而言，仍然要付 token 成本。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-ambiguous-work-cheap-exploration|cheap ambiguous exploration]]
- 用户从技术团队成员角度总结：Symphony 把工程师从多个 Codex sessions 之间的 context switching 中解放出来，不难的 routine implementation / landing work 交给 agents，人主要转向 harder, more exploratory tasks。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-change-economics-human-effort|change economics]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-engineers-focus-exploratory|engineers focus exploratory]]
- 用户要求把 Symphony 的 failure-to-harness-improvement 观点与 Anthropic harness reading note 互相 link：两者都支持一种工程方法，即 agent 失败后不只 patch output，而是把失败转化为 guardrails / skills / tests / docs / clearer criteria 等 system-level scaffold。[[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic harness reading note]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^harness-components-encode-model-assumptions|harness components encode assumptions]]
- 用户将本段进一步压缩为：高杠杆工作不是只用 coding agent 开发软件，而是用 coding agent 的失败和运行反馈来开发能让 coding agent 自己更好开发软件的 harness。更稳妥表述是：routine software work 仍由 agent 做，但团队把失败优先沉淀成 guardrails / skills / tests / docs / criteria，而不是一次性 patch output。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-failures-to-harness|failures to harness]]
- 用户纠正：`Not every task fits Symphony` 和 `objectives instead of strict transitions` 不应被强行连成一个问题。更准确读法是两个并列 lessons：task-oriented MAS 把人从 Codex session-level context switching 中解放出来，让人集中做 exploratory work；同时，Codex 不应被看成只会 implement task 的状态机节点，好的 manager/harness 应该给资源、context、tools 和 objective，减少 micromanagement。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-boundary-exploratory-work|boundary for exploratory work]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-objectives-not-transitions|objectives not transitions]]
- 用户补充了另一个 thread 的 runtime research：Symphony 的核心不是 Linear 方法论，而是用 Linear 的有限 issue surface 作为 durable coordination store / human UI；daemon polling eligible active issues，创建或复用 deterministic workspace，启动 per-issue Codex worker，并通过 `WORKFLOW.md` 渲染 prompt。这个总结由 public `SPEC.md` 的 scheduler/runner、candidate eligibility、workspace reuse、prompt template、app-server thread/turn reuse 和 tracker-write boundary 支撑；其中 `workpad comment` 和 `linear skill` 的具体叫法应作为另一个 thread 的实现研究术语保留边界。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-problem-automation-service|long-running automation service]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-workflow-prompt-template|WORKFLOW prompt template]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-app-server-thread-turn|app-server thread/turn reuse]]
- 用户总结 Elixir/spec portability 段：Symphony 不是主要作为可直接采用的软件交付，而是在展示 `spec driven dev` 和 harness-first 方法；高杠杆不是和 coding agent 一起开发软件本身，而是和 coding agent 一起开发能让 coding agent 开发软件的 harness。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-elixir-reference-spec-portability|Elixir reference and spec portability]]

## Candidate Concepts Entities

- `issue tracker as control plane`: central because Symphony's first move is to turn Linear-style work items into the operating surface for coding agents; existing page: none found yet; confidence: 0.85
- `Codex orchestration`: central because the source is about moving from individual Codex sessions to continuously managed agent work; existing page: no dedicated concept found yet; confidence: 0.82
- `agent-friendly repository`: relevant prerequisite but already partly covered through existing `agent-harness` material; existing page: [[concepts/agent-harness|agent-harness]] may partially cover it; confidence: 0.72
- `human attention bottleneck`: central to the article's diagnosis of why interactive coding agents stop scaling; existing page: no dedicated page found yet; confidence: 0.84
- `agent work management`: useful umbrella for the shift from coding execution to assigning, tracking, retrying, and reviewing agent work; existing page: no dedicated page found yet; confidence: 0.78
- `deliverable surface`: useful term for the article's move from sessions and PRs to issue / task / ticket / milestone as the primary unit of agent work; existing page: none found yet; confidence: 0.76
- `model-era scaffold`: useful term for harness or orchestration components that encode current model limitations and may become obsolete as models improve; existing page: [[concepts/agent-harness|agent-harness]] partially covers this; confidence: 0.83
- `learned agent topology`: external research signal from Sakana Fugu / Conductor where coordination topology is learned or selected by a coordinator model rather than hand-designed by humans; existing page: none found yet; confidence: 0.74
- `tracker-backed MAS orchestrator`: useful local term for Symphony's current shape as Linear-backed multi-agent work orchestration; existing page: none found yet; confidence: 0.8
- `task dependency topology`: central to the article's move from parallel sessions to staged, dependency-aware issue DAGs; existing page: none found yet; confidence: 0.84
- `platform-mediated agent communication`: useful inference for how agents coordinate through tracker objects instead of direct chat; existing page: [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] is a strong related source; confidence: 0.72
- `cheap ambiguous exploration`: central behavioral shift where speculative work can be ticketed, prototyped, and discarded with low human attention cost; existing page: none found yet; confidence: 0.86
- `agent-created follow-up work`: important mechanism where agents surface out-of-scope performance/refactor/architecture tasks as new issues; existing page: none found yet; confidence: 0.8
- `agentic work economics`: central to the article's claim that perceived change cost drops when implementation-driving labor moves to agents; existing page: none found yet; confidence: 0.86
- `PR landing automation`: relevant mechanism for large monorepos where CI/rebase/conflict/flaky-check handling becomes agent-shepherded last-mile work; existing page: none found yet; confidence: 0.76
- `harness-first agent improvement`: useful concept for treating agent failures as signals to improve guardrails, skills, tests, docs, and criteria rather than manually patching one output; existing page: [[concepts/agent-harness|agent-harness]] partially covers it; confidence: 0.84
- `objective-oriented agent management`: useful concept for managing capable coding agents by giving objectives, context, and tools rather than micromanaging every state transition; existing page: [[concepts/agent-harness|agent-harness]] partially adjacent; confidence: 0.84
- `spec-as-steering`: central to this section because `SPEC.md` is both a human-readable system definition and an agent-readable objective/context artifact for implementing Symphony variants; existing page: none found yet; confidence: 0.86
- `repo-owned workflow contract`: central because `WORKFLOW.md` moves implicit human development procedure into versioned prompt/config that Symphony can use to guide Codex workers; existing page: [[concepts/agent-harness|agent-harness]] partially adjacent; confidence: 0.84
- `harness-first software development`: central meta-pattern where humans and agents co-develop the specs, workflows, tools, and validation surfaces that let agents produce software repeatedly; existing page: [[concepts/agent-harness|agent-harness]] partially covers this; confidence: 0.87

## Candidate Related Pages

- [[concepts/agent-harness|agent-harness]] | relation: `extends` | opening framing says Symphony builds on a repo already redesigned with tests, guardrails, and agent-friendly workflow; this extends the harness layer into orchestration | confidence: 0.78
- [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]] | relation: `extends` | Symphony starts from Codex sessions but shifts the management layer upward from session-level agent loops to issue-level orchestration | confidence: 0.74
- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] | relation: `supports` | Multica is a close local comparison for the same move from individual agent sessions to platform/work-object-mediated agent execution; Symphony externalizes this through an issue tracker control plane, while Multica stores shared project state in platform objects and rehydrates execution environments | confidence: 0.9
- [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]] | relation: `extends` | useful synthesis for naming the shared abstraction: durable workflow objects plus resume/execution-environment state, rather than everything living in prompt or chat history | confidence: 0.86
- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]] | relation: `supports` | supports the broader pattern that orchestration scaffolds encode model-era assumptions and should be simplified when frontier models can carry longer tasks themselves | confidence: 0.88
- [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic-harness-design-long-running-apps-2026-04-reading-note]] | relation: `supports` | the final takeaway that each harness component encodes a current-model limitation directly supports reading Symphony failures as signals for guardrails, skills, tests, docs, and clearer criteria rather than one-off result patching | confidence: 0.9
- [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]] | relation: `supports` | provides the thread/turn and prompt-history background for understanding how Symphony workers can continue Codex work across multiple turns while preserving conversation state; use with its own outdated-source caveat | confidence: 0.76

## Sources

- [[sources/openai-codex-symphony-2026-04/summary|openai-codex-symphony-2026-04]]
- [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown|openai-codex-symphony-markdown]]
- [[sources/openai-codex-symphony-2026-04/source/symphony-spec|symphony-spec]]
- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]
- [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- [[notes/anthropic-harness-design-long-running-apps-2026-04-reading-note|anthropic-harness-design-long-running-apps-2026-04-reading-note]]
- [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]]
- [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]
- external reference, not yet ingested: [Sakana Fugu official post](https://sakana.ai/fugu-beta/)
- external reference, not yet ingested: [Learning to Orchestrate Agents in Natural Language with the Conductor](https://arxiv.org/abs/2512.04388)
