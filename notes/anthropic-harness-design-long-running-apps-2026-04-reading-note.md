---
type: note
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# anthropic-harness-design-long-running-apps-2026-04-reading-note

## Source

- Source collection: [[sources/anthropic-harness-design-long-running-apps-2026-04/summary|anthropic-harness-design-long-running-apps-2026-04]]
- Primary reading file: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown|harness-design-long-running-apps-markdown.md]]
- Discussion language: Chinese, with implementation terms such as `harness`, `agent`, `context reset`, `compaction`, `planner`, `generator`, and `evaluator` kept in English when translation would blur system structure.

## Core Question

Anthropic 这篇文章想回答的核心问题是：在 frontier agentic coding 里，哪些 `harness` 设计组件真正能让模型完成更长、更复杂的 frontend 与 full-stack application development，又该如何随着模型能力变化删减这些组件？[[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]

## Reading State

- Source slug: `anthropic-harness-design-long-running-apps-2026-04`
- Primary reading file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
- Semantic cursor:
  - file: `sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown.md`
  - semantic position: under `## Frontend design: making subjective quality gradable`, before the paragraph beginning `Across runs`
  - next unread source span: frontend loop outcomes: evaluator assessments improved before plateauing, with both incremental refinements and sharp aesthetic turns
  - next boundary: the paragraph beginning `The wording of the criteria steered the generator`
  - completed spans: opening framing block under `# Harness design for long-running application development`; `Why naive implementations fall short` setup span; first failure mode on `context anxiety`, `context reset`, and `compaction`; second failure mode on self-evaluation and external evaluator tuning; frontend design motivation span; frontend harness two-insights span; four frontend grading criteria; criteria weighting toward model weak spots; evaluator few-shot calibration; frontend generator/evaluator loop implementation
- Scout status: concept/entity scout and related-pages scout completed after the opening span; candidate lists refreshed in this note.

## Recall Log

### Opening Framing Block

- Source span label: `# Harness design for long-running application development` opening body, before `## Why naive implementations fall short`
- Quoted original span or citation: opening body in [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]], especially the passages on generator/evaluator design and the later three-agent architecture. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- Guiding question: 作者为什么要引入 `generator/evaluator` multi-agent structure？它要解决什么问题？
- User recitation: 用户理解为：作者想完成一个能 long-running 的 full-stack development 任务，所以先设计了 `generator + evaluator` 架构；`evaluator` 必须有明确、可靠、不 flaky 的评分系统，不能只问 "is this design good"；作者还把之前 harness 研究的两个经验带过来，即把大任务拆成可治理的小任务，以及让 `agent` 之间靠 `structured artifacts` 交换 `context`。
- Calibrated understanding: 这个复述抓住了主线。需要补一层范围校正：开头不是直接只从 full-stack coding 出发，而是从两个相连问题出发，即 frontend design 的主观质量问题和 long-running autonomous software engineering 的完整应用构建问题。`generator/evaluator` 最初解决的是“主观质量如何变成可评分、可迭代的反馈”；随后作者把同一分工模式迁移到 long-running coding，并结合任务分解与结构化 handoff，形成 `planner / generator / evaluator` 架构。
- Missing points: 注意后续阅读中的四个锚点：A criteria 怎样把主观判断变成明确评分；B evaluator 如何被校准到稳定可靠；C 大任务如何被拆成可治理的小任务或 sprint；D `structured artifacts` 如何在 `agent` 之间传递 `context`。
- Open questions: 后文是否能说明 A/B 是通过 prompt wording、few-shot calibration、Playwright interaction 还是 hard threshold 机制实现；C/D 是否最终是 load-bearing 组件，还是会随着 Opus 4.6 能力增强被删减。

### Why Naive Implementations Fall Short Setup

- Source span label: `## Why naive implementations fall short` opening setup, before the first detailed failure mode
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^persistent-long-task-failure-modes]]
- Guiding question: earlier decomposition/handoff harness 的边界或失败模式是什么？
- User recitation: 用户理解为：之前的 harness 做法是把大任务拆成多个小 task，让 `agent` 一个个实现；每个 `agent` 完成后把 handoff artifacts 交给下一个 `agent`，后者用这些 artifacts 影响自己的 `context`。但作者这一段还没有具体解释复杂任务中怎么失败，只是说时间一长 `agent` 会 `go off the rails`，具体表现会在接下来的两个 failure modes 里展开。
- Calibrated understanding: 这个复述准确。这段的论证位置是承认旧 harness 有效：它解决了任务组织、feature-by-feature 实现、以及跨 session 的 `context` handoff。但它同时指出这些机制还没有解决更长复杂任务里 `agent` 随时间失稳的问题。这里的 `go off the rails` 还只是总括，不是机制解释；机制解释就是后面两个 failure modes。
- Missing points: 注意这里没有否定 decomposition 和 handoff artifacts；作者是在说它们是必要但不充分的 scaffold。
- Open questions: 接下来两个 failure modes 是否分别对应 `context` 管理问题和 judgment/evaluation 问题；它们会怎样映射回用户标记的 C/D 与 A/B 四个锚点。

### Context Anxiety, Context Reset, And Compaction

- Source span label: first detailed failure mode under `## Why naive implementations fall short`, before the self-evaluation failure mode
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-anxiety-first-failure-mode]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^sonnet45-context-resets-essential]]
- Guiding question: `context reset` 和 `compaction` 有什么关键区别？为什么这个区别对 `context anxiety` 重要？
- User recitation: 用户理解为：表面看 `compaction` 和把当前任务总结成 handoff artifacts 差别不大，但从 KV Cache 角度看，`compaction` 仍然沿着旧历史继续，可能继承旧状态中的 `context anxiety`；而新的 `agent` 会扔掉旧 KV Cache，让 handoff artifact 在没有旧 KV Cache 影响的情况下进入新的 `context`，因此更难继承旧的 anxiety。但代价是失去大量旧 KV Cache hidden space 里的隐式信息，handoff artifact 不可能完美覆盖所有细节，所以 continuation 会弱于保留旧状态的 compacted continuation。
- Calibrated understanding: 源文直接支持的部分是：`compaction` 保留 continuity，但没有 clean slate，所以 `context anxiety` 仍可能持续；`context reset` 清空 context window，启动 fresh agent，并通过 structured handoff 传递 previous state 和 next steps；在 Sonnet 4.5 上，作者观察到 `compaction` 不足以解决 long task performance，因此 reset 成为 harness 的 essential 组件。用户的 KV Cache 解释是一个合理的机制类比，但不是源文直接声明，也不应写成必然的 runtime 事实：具体系统是否物理复用旧 KV Cache、怎样生成 compact summary、以及 prompt cache 如何参与，取决于实现。更稳妥的说法是：`compaction` 倾向于保留旧 thread 的语义轨迹和连续性，`reset + handoff` 则用显式 artifact 换掉隐式连续性，从而降低旧状态继续支配新 agent 的风险。
- Missing points: `context reset` 的代价不仅是信息损失，还包括 source span 明说的 orchestration complexity、token overhead、latency；而 handoff artifact 的质量变成 reset 能否成功的 load-bearing boundary。
- Open questions: 后文的 architecture 是否把 handoff artifact 做成文件、contract 或 QA artifact，从而补偿 reset 造成的隐式状态损失。

### Self-Evaluation Bias And External Evaluator

- Source span label: second detailed failure mode under `## Why naive implementations fall short`, before `## Frontend design: making subjective quality gradable`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^self-evaluation-bias]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^external-evaluator-skeptical-tuning]]
- Guiding question: 作者观察到 `self-evaluation` 有什么现象，为什么 separate `evaluator` 是更可调的工程杠杆？
- User recitation: 用户指出，不应把问题问成“为什么 self-evaluation 会失败”，因为源文没有给出根因解释，而模型自评偏宽松可能混合了训练信号、语言行为、哲学层面的自信与行动关系等问题。这里足够重要的是承认现象：做事的模型评价自己的输出时会倾向于自信和宽松。Separate `evaluator` 的优势在于可以从一开始就被调成 skeptical 的角色，并且不会被被评价模型先前的生成状态牵引，所以作为工程杠杆更好。
- Calibrated understanding: 这个校正准确。源文不是在解释 self-evaluation bias 的深层成因，而是在确认一个稳定工程现象：agents 自评时会 confidently praise mediocre work，主观 design 场景尤其明显；即使有可验证结果，poor judgment 也可能影响任务完成。作者的 actionable claim 是：把 generator 和 evaluator 分开，比让 generator 对自己的 work 变 skeptical 更 tractable。
- Missing points: Separate `evaluator` 不是天然客观。源文明确说 evaluator 仍然是 LLM，仍倾向于 generous；separation 只是让 skeptical tuning 更可行，并给 generator 一个可迭代的 external feedback target。
- Open questions: 后文会怎样把 skeptical tuning 具体化为 criteria、few-shot calibration、Playwright interaction、hard thresholds 或 QA prompt changes。

### Frontend Design Motivation

- Source span label: opening motivation paragraph under `## Frontend design: making subjective quality gradable`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-design-self-evaluation-testbed]]
- Guiding question: 作者为什么先在 frontend design 上实验？它暴露了什么问题？
- User recitation: 用户理解为：frontend design 的评分主观性很强，不像 unit tests 那样 pass/fail 清楚；主观评分任务会放大并暴露 self-evaluation 的问题。简单软件任务可能不太需要 generator/evaluator 模式，因为单个 agent 自己运行 tests 就够了；但评分主观性极强的任务，更能体现 generator/evaluator 模式的优势。
- Calibrated understanding: 这个复述准确。这里 frontend design 的实验价值在于它把“technically functional”与“visually unremarkable”分开了：Claude baseline 不是完全不会做页面，而是容易产出 safe、predictable、能用但平庸的 layout。正因为没有简单 binary check，external evaluator 的价值更容易被看见。
- Missing points: 这段还没进入 criteria 的具体设计；它只是在说明为什么 frontend design 是 self-evaluation issue 最明显的 testbed。
- Open questions: 下一段会如何把 subjective taste 转成可评分 criteria，以及 generation/grading 分离如何形成反馈循环。

### Frontend Harness Two Insights

- Source span label: `Two insights shaped the harness` paragraph under `## Frontend design: making subjective quality gradable`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-harness-two-insights]]
- Guiding question: frontend design harness 的两个关键机制是什么？它们分别解决什么问题？
- User recitation: 用户理解为：这两个 insight 就是前面标记的文章主线 A 和 B。A 是把模糊的好坏变成详细评分标准；B 是把实现的 `agent` 和评分的 `agent` 分开，否则会有 `self-evaluation bias`。
- Calibrated understanding: 这个复述准确。第一点把 aesthetics 从不可直接评分的 “is this beautiful?” 改写成 criteria-based judgment，也就是“是否符合我们定义的 good design principles”；第二点把 generation 和 grading 分开，让 generator 接收外部 feedback，而不是依赖自己的 self-evaluation。
- Missing points: 这里还没有说四个 criteria 分别是什么，也没有说明各项权重；它只是在给 criteria list 和 generator/evaluator loop 做概念铺垫。
- Open questions: 下一段的四个 criteria 会怎样覆盖 subjective quality、originality、technical craft 与 usability；哪些 criteria 会被作者强调，哪些只是 baseline competence check。

### Frontend Four Grading Criteria

- Source span label: four grading criteria list under `## Frontend design: making subjective quality gradable`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-four-grading-criteria]]
- Guiding question: 这四个 grading criteria 分别在评什么？它们怎样把 frontend design 的主观好坏拆成可操作维度？
- User recitation: 用户选择不逐条复述设计细节，指出这一段的关键不是掌握设计术语，而是看到评分标准设计时应强调模型做不好的那些标准。
- Calibrated understanding: 这个判断应和下一段合起来看。当前 list 本身把 frontend quality 拆成四类：整体设计质量、原创性、craft 基本功、功能可用性。用户指出的重点是 criteria 不只是分类清单，还会服务于后续 weighting：如果模型本来就容易做好 craft 和 functionality，那么评价系统应该更用力地压在模型容易失败的 design quality 与 originality 上。
- Missing points: 当前 span 只列 criteria，还没明说 weighting；“强调模型做不好的标准”是对下一段的提前概括。
- Open questions: 下一段会如何说明 design quality 和 originality 被赋予更高权重，以及这种 weighting 如何推动模型承担更多 aesthetic risk。

### Frontend Criteria Weighting Toward Model Weak Spots

- Source span label: paragraph beginning `I emphasized design quality and originality`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-weighting-model-weaknesses]]
- Guiding question: 作者为什么更强调 `design quality` 和 `originality`，而不是平均强调四个 criteria？
- User recitation: 用户上一轮已经概括了这一段：设计评分标准时，要强调模型做不好的那些标准。
- Calibrated understanding: 这个概括准确。作者把 `design quality` 和 `originality` 权重放在 `craft` 与 `functionality` 前面，因为 Claude 默认已经更容易做好技术执行和可用性；真正容易失败的是 bland、generic、AI slop 式的 design quality 和 originality。Rubric 在这里不是中立分类，而是用权重把模型推向 aesthetic risk-taking。
- Missing points: 这段说明了 criteria weighting，但还没说明 evaluator 怎样被校准得稳定。
- Open questions: 下一段 few-shot calibration 怎样减少 score drift，并让 evaluator judgment 对齐作者偏好。

### Evaluator Few-Shot Calibration

- Source span label: paragraph beginning `I calibrated the evaluator`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^few-shot-evaluator-calibration]]
- Guiding question: `few-shot examples` 和 `detailed score breakdowns` 在这里怎样让 evaluator 更可靠？
- User recitation: 用户把这和之前给 Lynx 做 Oncall 总结 rubrics 的实践类比：对着 few-shot examples 一直修改 rubrics，直到结果不再总是漂移。
- Calibrated understanding: 这个类比准确。这里的 few-shot calibration 不是抽象地告诉 evaluator “稳定一点”，而是用具体样例和 detailed score breakdowns 调整 evaluator 的判断边界，让它的输出更贴近作者偏好，并减少跨 iteration 的 score drift。和 Oncall rubrics 类似，rubric 的可靠性来自反复用样例校准，而不是只写一条原则。
- Missing points: 源文没有展开 few-shot examples 的具体内容；这里只能记录校准机制和目标。
- Open questions: 下一段会说明 calibrated evaluator 如何被接入实际 loop，以及 Playwright MCP 如何让 evaluator 从静态评分变成可交互 QA。

### Frontend Generator Evaluator Loop Implementation

- Source span label: paragraph beginning `I built the loop on the Claude Agent SDK`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-generator-evaluator-loop]]
- Guiding question: frontend `generator/evaluator loop` 是怎么工作的？输入、步骤、输出分别是什么？
- User recitation: 用户理解为：作者用这一段说明 `generator-evaluator loop` 的工作方式。一开始让 `generator` 写一个实现，然后 `evaluator` 评价这个实现；评价结果回流到 `generator`，`generator` 根据之前评分的 trend 决定继续 refine 还是 pivot 到新方向，如此循环往复。
- Calibrated understanding: 这个复述准确。完整机制是：user prompt 进入 `generator`，生成 HTML/CSS/JS frontend；`evaluator` 通过 Playwright MCP 直接操作 live page、截图、观察，再按 criteria 打分并写 critique；feedback 作为下一轮 `generator` 输入。Loop 通常跑 5 到 15 轮，并且每轮之后 `generator` 需要根据 score trend 做 refine-or-pivot 决策。
- Missing points: 这段还说明了成本来源：evaluator 不是静态截图评分，而是 live interaction，所以每轮有真实 wall-clock time，完整 run 可达四小时。
- Open questions: 下一段会说明这种 loop 的实际 outcome 是逐步改善、plateau，还是可能出现突然的 aesthetic turn。

## Questions And Answers

No questions recorded yet.

## Reader Comments

- 用户提出后续阅读应跟踪四个实现锚点：A 明确评分系统，B 可靠不 flaky 的 evaluator，C 大任务拆成可治理小任务，D 通过 `structured artifacts` 在 `agent` 之间交换 `context`。支撑段落见 opening framing block 中关于 generator/evaluator、criteria、decomposition、structured artifacts 和 three-agent architecture 的说明。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- 用户提出一个模型架构层面的解释：`compaction` 和 `context reset + handoff` 的差别可以理解为是否让旧 thread 的 KV Cache hidden state 继续影响后续生成；这个解释有助于理解 clean slate 与 continuation 的 tradeoff，但需要标注为推断，因为源文只讨论 `context window`、`compaction`、`clean slate` 与 handoff artifact，没有直接说明 KV Cache 复用机制。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- 用户修正 reading prompt：self-evaluation bias 这一段不该追问根因，而应问作者观察到什么现象，以及 separate `evaluator` 为什么是更可调的 harness component。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^self-evaluation-bias]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^external-evaluator-skeptical-tuning]]
- 用户把 evaluator few-shot calibration 类比到 Lynx Oncall 总结 rubrics：对着 few-shot examples 反复修改 rubric，直到输出不再总是漂移。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^few-shot-evaluator-calibration]]

## Candidate Concepts Entities

- `harness design`: central concept for the article's claim that surrounding orchestration can materially change frontier agentic coding performance; existing page likely exists at [[concepts/agent-harness|agent-harness]]; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `generator/evaluator loop`: reusable pattern for separating production from judgment in agentic workflows, first introduced here through the GAN-inspired frontend design setup; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]]
- `context reset`: recurring mechanism in long-running agent work where the context window is cleared and a fresh agent resumes from a structured handoff; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `compaction`: contrasting mechanism where earlier conversation is summarized in place so the same agent can continue on shortened history; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `context anxiety`: named failure mode where an agent starts wrapping up prematurely as it approaches its perceived context limit; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `structured handoff`: load-bearing artifact pattern for carrying prior state and next steps across context resets or agent sessions; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]]
- `self-evaluation bias`: failure mode where agents praise their own mediocre work, especially when quality is subjective and lacks binary tests; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `external evaluator`: reusable harness role that judges a generator's work separately from the agent that produced it, making skeptical evaluation easier to tune; existing page unknown; confidence: high. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `planner / generator / evaluator architecture`: reusable long-running coding harness shape for turning a prompt into a spec, implementing feature chunks, and testing/evaluating the result; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- `evaluator calibration`: reusable problem around making LLM-based QA skeptical, stable, and aligned with target criteria; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
- `sprint contract`: article-specific but potentially reusable harness artifact boundary for agreeing on what a feature chunk means before implementation; existing page unknown; confidence: low. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^sprint-contract]]
- `file-based handoff`: reusable coordination pattern where agents communicate through files rather than shared conversational state; existing page unknown; confidence: medium. [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^file-based-agent-communication]]

## Candidate Related Pages

- [[concepts/agent-harness|agent-harness]]: supports; this article is a concrete Anthropic case study for the same layer defined there: model-external infrastructure that manages long-running tasks through planning, tool use, context strategy, handoff artifacts, and evaluation rather than treating the model alone as the whole agent system; confidence: high
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]: extends; the Anthropic article adds a later 2026 engineering example to the broader origin trail, moving from general `agent harness` / `context engineering` framing into a specific long-running application-development harness with planner, generator, evaluator, context reset, and file-based handoff components; confidence: high
- [[syntheses/components-of-a-coding-agent-layer-mismatch-and-state-resumption|components-of-a-coding-agent-layer-mismatch-and-state-resumption]]: supports; the current `Why naive implementations fall short` section gives a concrete mechanism for that synthesis's state-resumption claim: compaction and transcript continuity are not always enough, while context resets require a durable handoff artifact carrying state and next steps; confidence: high
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]: extends; the article's later simplification discussion stress-tests the same design principle by asking which planner, sprint, evaluator, context-reset, and handoff components remain load-bearing as model capability improves; confidence: medium

## Sources

- [[sources/anthropic-harness-design-long-running-apps-2026-04/summary]]
- [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown]]
