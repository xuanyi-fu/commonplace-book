---
type: synthesis
status: draft
created: 2026-04-29
updated: 2026-04-29
---

# Issue Tracker 作为 Coding Agents 的 Control Plane

这次围绕 Symphony / Linear / Beads / GitHub Issues 的讨论，核心不是“哪一个 tracker 更好”，而是要把 agentic software work 拆成几个不同的 control plane。Symphony 的重要性在于它把管理面从多个 live Codex sessions 转移到 issue / ticket / task / milestone 这些 work objects 上：当 agent 够 capable 以后，人的瓶颈不再只是写代码，而是 attention、context switching 和 Engineering Management。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-control-plane-framing|Symphony control plane framing]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-human-attention-bottleneck|human attention bottleneck]]

## 三层状态不要混在一起

第一层是 `code workspace`。这一层天然适合 git / branch / worktree：多个 agent 可以在不同 workspace 里并行探索，代码 conflict 可以通过 diff、review、merge、rebase 来解决。代码 artifact 大、可分支、可比较，所以允许多个版本现实是合理的。

第二层是 `issue / project state`。这里记录的是谁在做、做到哪一步、blocked by 谁、下一步交给谁、acceptance criteria 是什么。这些是 coordination metadata，不是代码 artifact。它们更适合 centralized single source of truth，而不是让多个 workspace 各自写出局部现实以后再靠 git merge reconciliation。Symphony 用 Linear 的主要价值也在这里：不是完整采纳 Linear 的 PM 哲学，而是借一个 central issue state + human UI + comments / labels / blockers。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-normalized-issue-fields|normalized issue fields]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-dispatch-eligibility|dispatch eligibility]]

第三层是 `agent run control plane`。这里管 live thread、active turn、nudge、interrupt、restart、lease、heartbeat、token budget、workspace mapping。这个层不应该完全塞进 issue tracker，也不应该靠 worker workspace 自己抢写。Codex App Server 已经提供了 thread / turn 这种 live execution surface；更合理的是让薄 orchestrator 保存 `issue_id -> role -> workspace -> codex_thread_id` 的映射，再把 nudge / interrupt / continuation 转成 Codex thread 操作。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-app-server-thread-turn|app-server thread/turn reuse]]

## Symphony 做对了什么

Symphony 的 reference pattern 很清楚：daemon poll tracker，找 active issues，为每个 issue 创建或复用 deterministic workspace，加载 repo-owned `WORKFLOW.md`，启动 per-issue coding-agent session，并在 issue 仍 active 时继续推进。它不是主 agent，也不是通用 workflow engine，而是 rule-based scheduler / runner / tracker reader。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-problem-automation-service|long-running automation service]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-workspace-reuse|workspace reuse]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-workflow-md-captures-workflow|WORKFLOW captures workflow]]

这个 design 把 Codex 的 inner loop 扩展了一层。单个 Codex turn 仍然是模型推理、tool calls、observations；Symphony 在外层加上 `while(issue_needs_proceed)`：如果 worker turn 结束后 issue 仍在 active state，就继续同一 thread / workspace 的后续 turn，直到 issue 进入 handoff / non-active / terminal state。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-worker-continuation|worker continuation]] [[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-app-server-thread-turn|thread reuse]]

但 Symphony 的边界也很重要：ticket writes、state transitions、comments、PR metadata 通常由 coding agent 通过 workflow tool 完成，而不是 orchestrator 自己内建业务逻辑。也就是说，Symphony 不是“懂项目管理的 manager agent”，它只是把 agent 放进一个 issue-level long-running loop 里。[[sources/openai-codex-symphony-2026-04/source/symphony-spec#^symphony-spec-tracker-writes-boundary|tracker writes boundary]]

## Tracker 选择的真正差异

Linear 的意义不是它的 cycle / initiative / roadmap 方法论。Symphony 当前主要吃到的是 issue、state、priority、labels、blockers、comments 和 project scope。Linear 作为 baseline 的理由是 centralized state、好用 UI、权限、通知、搜索和 workflow states，而不是因为 Symphony 深度依赖 Linear 的完整 PM model。

GitHub Issues 也可以承担很多 topology。GitHub 已经有 `blocked_by` / `blocking` issue dependencies，也有 sub-issues；所以用 GitHub Issues 做 `issue graph` 并不荒谬。[GitHub issue dependencies](https://docs.github.com/en/enterprise-cloud@latest/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) [GitHub sub-issues](https://docs.github.com/en/issues/managing-your-tasks-with-tasklists/creating-a-tasklist) 它的问题是 workflow state 不像 Linear 那样是 issue 的一等字段，往往要在 issue labels、Projects status field、issue fields 之间选一个 source of truth。

Beads 的价值在另一边：它是 agent-friendly、repo-native、CLI-first 的 local issue graph。但 Beads 的 git-backed / JSONL sync 模型更像 durable backlog，不适合让很多 worker workspaces 高频直接更新同一个 issue state。hash IDs、append-only JSONL、merge driver、Dolt backend 都是在缓解 sync / merge 问题；它们不能替代 `claim / lease / running / heartbeat / nudge queue` 这种 runtime coordination primitive。[Beads JSONL sync](https://steveyegge.github.io/beads/core-concepts/jsonl-sync) [Beads architecture](https://steveyegge.github.io/beads/architecture)

所以一个稳妥边界是：

- `code repo` 可以 branch / conflict / merge。
- `issue tracker` 应该尽量 centralized，用来表达 project state 和 task graph。
- `agent run control plane` 应该单独保存 runtime lease、thread、turn、nudge、heartbeat。

## Manager Agent 可以有，但要受 kernel 约束

可以让一个 manager agent 读取 Beads / GitHub / Linear snapshot，然后决定要开什么 worker、建什么 follow-up issue、怎样调整 dependency graph。但 manager agent 不应该直接 shell out 或任意 spawn Codex。更稳的形态是：

```text
daemon builds world snapshot
-> manager agent returns structured JSON actions
-> deterministic kernel validates actions
-> kernel creates workspace / starts Codex thread / writes tracker update
```

这样 topology 和 task decomposition 可以变得更 agentic，但 lease、workspace、budget、permissions、process lifecycle 仍然是 deterministic runtime 负责。这个设计比 Symphony 更接近“agentic scheduling”，但不会把系统安全性完全交给一个 manager model。

## Nudge 是 Symphony 当前缺的一块

Symphony 把人从多个 live sessions 里解放出来，但代价是 live intervention 变差。agent 做得不好时，人通常只能改 issue/comment/state，等下一轮 agent 自己读到，或者杀掉 worker 等 retry。这不是舒服的 nudge。

更好的 operator surface 应该长这样：

```text
symctl runs
symctl tail ISSUE-123
symctl nudge ISSUE-123 "先别重构，先跑最小 reproducer"
symctl interrupt ISSUE-123
symctl restart ISSUE-123 --with "从当前 workspace 继续，优先处理 QA 第 2 点"
```

如果 active turn 正在跑，nudge 应该变成 live steer；如果 thread idle，就变成下一轮 `TurnStart`；如果 worker 已死，就写入 run DB / workpad，在 restart prompt 里注入。换句话说，issue tracker 是 project-management surface，Codex thread 是 live run surface，中间需要一个薄 operator bridge。

## 什么时候不需要 Symphony

项目刚开始时，通常不需要 Symphony。早期最稀缺的是问题定义、架构判断、产品边界、数据模型、接口形状和 exploratory spike。这个阶段如果过早把工作 ticket 化，反而会把人和 agent 都绑到未成熟流程里。

更合理的节奏是：

- `0 -> 1`：人和少量 interactive Codex sessions，重点是探索和垂直切片。
- `1 -> N`：任务模式稳定，出现清晰 backlog，再引入 issue tracker 和 lightweight orchestrator。
- `N -> scale`：任务可以被拆成 DAG，routine implementation / testing / review / landing work 足够多，才值得上 Symphony-style per-issue autonomous runs。

这也解释了为什么 Symphony 适合 routine implementation、CI babysitting、PR landing、探索性 ticket fan-out，却不适合所有 ambiguous / judgment-heavy work。好的 harness 应该让 routine work 自动化，把人释放到更难、更探索性的工作上；agent 失败也不应只手动 patch result，而要反过来改 guardrails、skills、tests、docs、QA workflow 和 success criteria。[[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-task-tree-dependencies|task tree dependencies]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-ambiguous-work-cheap-exploration|cheap ambiguous exploration]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-boundary-exploratory-work|boundary for exploratory work]] [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown#^symphony-failures-to-harness|failures to harness]]

## 结论

这条讨论最后得到的判断是：不要急着复刻 Linear，也不要把 Beads 当 runtime scheduler，更不要把 Polyphony 这种大平台直接当基座。更小、更稳的组合是：

```text
centralized issue tracker = durable work graph / human UI
thin orchestrator kernel = claim / workspace / Codex thread mapping
Codex app-server = live run control plane
git worktrees = code execution isolation
operator CLI/UI = nudge / interrupt / restart / observe
```

Symphony 是一个 reference pattern，不是终点。它真正留下来的问题是：当 coding agent 越来越 capable，软件团队需要的不是更多 chat windows，而是一个能把 work topology、agent runtime、human intervention 分层管理起来的 harness。

## Sources

- [[sources/openai-codex-symphony-2026-04/source/openai-codex-symphony-markdown|OpenAI Codex Symphony article]]
- [[sources/openai-codex-symphony-2026-04/source/symphony-spec|Symphony SPEC]]
- [[notes/openai-codex-symphony-2026-04-reading-note|openai-codex-symphony-2026-04-reading-note]]
- [GitHub issue dependencies](https://docs.github.com/en/enterprise-cloud@latest/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)
- [GitHub sub-issues](https://docs.github.com/en/issues/managing-your-tasks-with-tasklists/creating-a-tasklist)
- [Beads JSONL sync](https://steveyegge.github.io/beads/core-concepts/jsonl-sync)
- [Beads architecture](https://steveyegge.github.io/beads/architecture)
