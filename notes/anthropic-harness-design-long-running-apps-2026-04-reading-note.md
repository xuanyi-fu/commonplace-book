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
  - semantic position: under `### Iterating on the harness`, before the paragraph beginning `The first set of harness results was encouraging`
  - next unread source span: motivation for simplifying the harness after the first results, including cost, speed, bulk, and the principle that each harness component encodes an assumption about model limitations
  - next boundary: the paragraph beginning `In my first attempt to simplify`
  - completed spans: opening framing block under `# Harness design for long-running application development`; `Why naive implementations fall short` setup span; first failure mode on `context anxiety`, `context reset`, and `compaction`; second failure mode on self-evaluation and external evaluator tuning; frontend design motivation span; frontend harness two-insights span; four frontend grading criteria; criteria weighting toward model weak spots; evaluator few-shot calibration; frontend generator/evaluator loop implementation; compressed frontend loop outcome/example span through the Dutch museum example; full-stack transition span; architecture setup showing context resets removed for Opus 4.5; three-agent personas; sprint contract negotiation; file-based agent communication; retro game maker setup and solo run failure analysis; full harness run evidence; evaluator QA tuning
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

### Frontend Loop Outcomes And Dutch Museum Example

- Source span label: compressed outcome/example span from `Across runs` through the Dutch museum example, before `## Scaling to full-stack coding`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^frontend-loop-outcomes]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^criteria-wording-steers-output]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^iteration-pattern-not-linear]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^dutch-museum-creative-leap]]
- Guiding question: frontend loop 的实际效果是什么？它在进入 full-stack coding 前证明了什么？
- User recitation: 用户指出按目标应已读到 `## Scaling to full-stack coding`，所以这一段按低兴趣 outcome/example 压缩处理。
- Calibrated understanding: 这几段的共同作用是收束 frontend experiment：evaluator assessments 会随 iteration 改善后 plateau；generation 可能 incremental refine，也可能 sharp aesthetic turn；criteria wording 本身会塑造输出分布；improvement 不总是线性，复杂度会随 feedback 上升，甚至第一轮 criteria prompt 就能把模型从 generic defaults 推开。Dutch art museum 例子只是把这个效果具体化：第十轮从普通 dark-themed landing page pivot 成 spatial 3D gallery experience。
- Missing points: 这些段落主要是结果与例子，不再新增 harness 组件；对后文最重要的是 generator/evaluator loop 已经被证明能把 subjective design 从 generic baseline 推向更大胆方向。
- Open questions: 下一节会说明同一 generator/evaluator pattern 如何迁移到 full-stack coding，以及 code review / QA 如何承担 design evaluator 的结构角色。

### Scaling To Full-Stack Coding Transition

- Source span label: opening paragraph under `## Scaling to full-stack coding`, before `### The architecture`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^full-stack-generator-evaluator-transition]]
- Guiding question: 作者怎样把 frontend 的 `generator/evaluator` pattern 迁移到 full-stack development？
- User recitation: 用户概括为：frontend design 里的 `evaluator` 到 full-stack coding 里变成了 QA 和 code review。
- Calibrated understanding: 这个复述准确。这段只是迁移桥：frontend 里 evaluator 的结构角色是评价实现、给 feedback；full-stack development 里天然有 code review 和 QA 承担类似角色，所以 generator/evaluator loop 可以映射到软件开发生命周期。
- Missing points: 这里还没有 architecture 细节；planner、generator、evaluator 角色会在下一段展开。
- Open questions: 下一段会说明 context reset 是否还需要、三代理系统各自补什么 gap，以及 full-stack harness 怎样继承前面 frontend loop 的 evaluator 逻辑。

### Architecture Setup: Dropping Context Resets

- Source span label: first paragraph under `### The architecture`, before the three-agent personas introduction
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^architecture-drop-context-resets]]
- Guiding question: 从 earlier harness 到这版 full-stack harness，`context reset` 发生了什么变化？为什么？
- User recitation: 用户概括为：前文花了很大篇幅说明 `context anxiety` 和 `context reset`，到这里作者说新模型基本没这个问题了，所以可以 drop `context reset`。
- Calibrated understanding: 这个复述准确。早期 Sonnet 4.5 harness 需要 context resets 来处理 `context anxiety`，让模型保持在 task 上；但 Opus 4.5 基本移除了这种 behavior，所以作者把 resets 从这个 harness 里删掉，改成 agents 在整个 build 里作为 one continuous session 运行，由 Claude Agent SDK automatic compaction 处理 context growth。
- Missing points: 这段不是否定 earlier reset 机制，而是在说明 harness component 是否 load-bearing 会随模型能力变化而移动。
- Open questions: 下一段三代理 personas 会说明作者保留了哪些组件：planner、generator、evaluator 分别补哪个 prior-run gap。

### Three-Agent Personas

- Source span label: three-agent personas list under `### The architecture`, before sprint contract negotiation
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-personas]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^hard-threshold-evaluator]]
- Guiding question: `planner`、`generator`、`evaluator` 三个 personas 分别补的是 prior runs 里的什么 gap？
- User recitation: 用户理解为：这一段用 full-stack 例子展开 `planner-generator-evaluator` 架构。`planner` 把三四句话扩成 spec，但不能把实现细节写太细，因为它的信息不足，错误实现判断会 cascade 到 `generator`；正确路线应让 `generator` 和 `evaluator` 在实践中发现。`generator` 一个 feature 一个 feature 地做，每个 sprint 结束先 self-evaluate，再交给 `evaluator`。`evaluator` 的新信息是每个标准都有 hard threshold，低于 threshold 就 fail，并给明确 feedback 让 `generator` 修改。
- Calibrated understanding: 这个复述准确。三 personas 分别补三个 gap：`planner` 补 upfront spec gap，但通过限制 implementation detail 避免上游错误固化；`generator` 补 scoped implementation gap，用 sprint/feature 粒度控制复杂度；`evaluator` 补 QA/judgment gap，用 Playwright MCP 实测 UI/API/database state，并用 hard thresholds 把 vague review 变成 pass/fail 反馈。
- Missing points: `planner` 还被要求把 AI features weave into specs；`generator` 使用具体 stack 并有 git；这些是实现细节，不改变三角色分工。
- Open questions: 下一段 sprint contract 会说明 `generator` 与 `evaluator` 如何在写代码前先对 done / success criteria 达成一致。

### Sprint Contract Negotiation

- Source span label: paragraph beginning `Before each sprint`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^sprint-contract]]
- Guiding question: `sprint contract` 是怎么工作的？输入、步骤、输出分别是什么？
- User recitation: 用户理解为：`planner` 把大任务拆成小任务，但不要对小任务写过多 implementation details；`sprint contract` 是 `generator` 和 `evaluator` 通过多轮对话把小任务的 deliverables 和 success metrics 定下来；`evaluator` 要确保这些 deliverables / success metrics 符合 plan，避免 `generator` 因 self-evaluation bias 或自我解释而做偏。
- Calibrated understanding: 准确，但需要小校正：当前 paragraph 的重点不是 `planner` 继续细拆小任务，而是 high-level product spec / user stories 到 testable implementation 之间的 bridge。`generator` proposes what to build and how success will be verified；`evaluator` reviews that proposal before code；双方 iterate until agreement。
- Missing points: `sprint contract` happens before code；它同时避免 `planner` 过早 over-specify implementation，也避免 `generator` 单方面定义 done。
- Open questions: 下一段会说明 contract 和 QA handoff 如何通过 files 在 agents 之间传递。

### File-Based Agent Communication

- Source span label: paragraph beginning `Communication was handled via files`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^file-based-agent-communication]]
- Guiding question: file-based communication 是怎么工作的？它怎样维持 spec fidelity without over-specifying implementation？
- User recitation: 用户理解为：这一段大致是在说 `evaluator` 和 `generator` 是通过文件系统来沟通的。
- Calibrated understanding: 准确。源文说的是 agents 通过 files 进行 turn-by-turn communication：一个 `agent` 写文件，另一个 `agent` 读后在同一文件或新文件里回应。`generator` 随后按已协商的 contract 开发，再 hand off 给 QA。这里的重点是把 contract、reply、handoff 变成显式、可读、可复查的 artifact。
- Missing points: 这不是让 `planner` 写更多实现细节，而是让 spec fidelity 通过 files 和 agreed contract 保持住；implementation 仍然留给 `generator` 在 sprint 内完成。
- Open questions: 下一节 `### Running the harness` 会用 retro game maker 对比 solo run 和 full harness 的实际输出差异。

### Retro Game Maker Setup And Solo Run Failure

- Source span label: `### Running the harness` opening comparison through the solo run screenshots, before `After evaluating the solo run`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^retro-maker-cost-comparison]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^solo-run-surface-ok-broken-runtime]]
- Guiding question: 这一段给了什么对比证据？这些证据先支持了什么结论？
- User recitation: 用户理解为：solo run 表面上看着还行，好像符合 retro game maker 的基本期待；但一深入点击就经不起推敲，workflow 僵硬、空间浪费，最关键是 game runtime 根本玩不了。
- Calibrated understanding: 准确。这段先建立同题对照：同一个 one-sentence retro game maker prompt，solo run 成本和时间更低，full harness 更贵更久；然后作者先打开 solo output，说明它的第一眼 impression 没有立刻失败，但真实使用暴露了 implementation wiring 与 product workflow 的问题。核心结论不是 solo run 完全不会生成 UI，而是它容易生成“看起来像 app、实际核心 loop broken”的结果。
- Missing points: 这里的对比还只是 solo side；full harness 的质量差异要到下一段才展开。成本差异也很重要：作者在承认 full harness expensive 的前提下论证质量收益。
- Open questions: 下一段会说明 full harness 的优势来自哪些具体机制：planner-expanded spec、visual design language、sprint contracts、以及更完整的 editor/AI features。

### Full Harness Run Evidence

- Source span label: paragraph beginning `After evaluating the solo run` through the evaluator findings table, before `Getting the evaluator to perform at this level took work`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^full-harness-expanded-spec]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^full-harness-play-mode-worked]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^evaluator-contract-playwright-findings]]
- Guiding question: full harness run 相比 solo run 改善在哪里？这些改善分别来自 `planner`、`sprint contract`、`evaluator`，还是只是 UI polish？
- User recitation: 用户理解为：这一段其实是在用一个实际例子证明前文的 `planner-generator-evaluator` 架构优于 single agent，证明 `harness` 确实有用。
- Calibrated understanding: 准确。这是一个 case-study evidence，而不是严格 benchmark：同一个 prompt 下，full harness 通过 `planner` 扩成 16-feature spec / ten sprints，通过 frontend design skill 形成 visual design language，通过 per-sprint contract 让 `generator` 和 `evaluator` 对 testable behaviors 达成一致。结果上，它不只是 UI 更 polished，还真的让 play mode 跑起来；`evaluator` 又通过 Playwright 按 contract criteria 找到具体 bug，把 implementation 拉回 spec。
- Missing points: 这段也保留了边界：full harness 仍然 expensive，workflow 仍有 product intuition gap，AI-generated level 也有 common-sense / edge-case 问题；所以作者证明的是 clear lift，不是完美解决。
- Open questions: 下一段会把重点从“harness 有用”转到“evaluator 不是天然有用”：Claude out of the box 作为 QA agent 会偏宽松、测试浅，需要通过日志和 prompt iteration 调。

### Evaluator QA Tuning

- Source span label: paragraph beginning `Getting the evaluator to perform at this level took work`, before `### Iterating on the harness`
- Quoted original span or citation: [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^evaluator-qa-tuning]]
- Guiding question: `evaluator` 为什么也需要 tuning？作者是怎么把它从 weak QA agent 调成可用的？
- User recitation: 用户理解为：让模型当这种 app 的 QA agent 并不天然称职，很多 edge cases cover 不到，并且评价太慷慨；作者的解决方式是看 evaluator logs，找 judgment 和自己不一致的地方，然后持续改 QA prompt。用户补充认为，语言模型本身对视觉和细粒度交互不一定敏感，例如 layout、1-pixel 差异等可能在模型 hidden space 里很难被稳定注意到；这可以和此前 Codex computer use 玩 `STS2` 的失败案例互相支持。[[syntheses/codex-computer-use-implementation-and-limits|Codex Computer Use 的实现形态与当前边界]]
- Calibrated understanding: 准确。源文直接说的失败模式有两类：第一，Claude 会发现 legitimate issues 后又说服自己问题不大，最后 approve；第二，测试太 superficial，没有充分 probe edge cases。作者的 tuning loop 是读 logs，挑出 evaluator judgment 与作者判断 diverge 的例子，再更新 QA prompt，重复几轮直到 grading reasonable。用户的视觉 hidden-space 解释是合理推断，但不是源文直接断言；更稳妥地说，视觉、布局、动态交互和细粒度 affordance 都是 LLM-based QA 的高风险区域。
- Missing points: 这段最后仍然承认 QA 能力有上限：small layout issues、unintuitive interactions、deeply nested features 里的 undiscovered bugs 仍会漏掉。但和 solo run 的 central feature broken 相比，lift 仍然明显。
- Open questions: 下一段会转向 harness simplification：如果 full harness 有用但 bulky、slow、expensive，哪些组件是真正 load-bearing 的？

## Questions And Answers

No questions recorded yet.

## Reader Comments

- 用户提出后续阅读应跟踪四个实现锚点：A 明确评分系统，B 可靠不 flaky 的 evaluator，C 大任务拆成可治理小任务，D 通过 `structured artifacts` 在 `agent` 之间交换 `context`。支撑段落见 opening framing block 中关于 generator/evaluator、criteria、decomposition、structured artifacts 和 three-agent architecture 的说明。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^three-agent-architecture]]
- 用户提出一个模型架构层面的解释：`compaction` 和 `context reset + handoff` 的差别可以理解为是否让旧 thread 的 KV Cache hidden state 继续影响后续生成；这个解释有助于理解 clean slate 与 continuation 的 tradeoff，但需要标注为推断，因为源文只讨论 `context window`、`compaction`、`clean slate` 与 handoff artifact，没有直接说明 KV Cache 复用机制。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]] ^context-anxiety-kv-cache-inference
- 用户修正 reading prompt：self-evaluation bias 这一段不该追问根因，而应问作者观察到什么现象，以及 separate `evaluator` 为什么是更可调的 harness component。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^self-evaluation-bias]] [[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^external-evaluator-skeptical-tuning]]
- 用户把 evaluator few-shot calibration 类比到 Lynx Oncall 总结 rubrics：对着 few-shot examples 反复修改 rubric，直到输出不再总是漂移。[[sources/anthropic-harness-design-long-running-apps-2026-04/source/harness-design-long-running-apps-markdown#^few-shot-evaluator-calibration]]
- 用户把当前 evaluator QA tuning 段和两个已有知识点连接起来：一是 `STS2` / Codex computer use 失败案例，说明视觉、连续控制和细粒度 GUI 判断不是 LLM agent 默认擅长的能力；二是 Philipp Schmid 的 `agent harness` 要求，即把多步 agent workflow 变成可 `log and grade` 的 structured data，方便后续验证和 hill-climbing。[[syntheses/codex-computer-use-implementation-and-limits|Codex Computer Use 的实现形态与当前边界]] [[sources/codex-computer-use-2026-04/source/user-test-sts2-drag-failure-2026-04-20|STS2 测试记录]] [[sources/agent-harness-origins-2023-2026/source/importance-of-agent-harness-in-2026-markdown#^agent-harness-log-and-grade|log and grade]]

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
