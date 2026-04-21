---
type: synthesis
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Auto-Diagnose：先把简单的 triage 做好，比着急做大而全的自动修复更重要

`Auto-Diagnose` 最值得记住的，不是它用了什么新模型，也不是它已经会自动修 bug；恰恰相反，它公开展示的是一条相当朴素的生产流水线：先把 integration test 失败后的日志收齐并排好序，再做一次受 prompt 强约束的单轮 LLM 诊断，最后把结果直接发回 code review 工作流。就公开论文看，这不是 agent loop，不是多轮工具探索，也不是自动修复系统。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026.pdf]]

## 简单工作流

这套系统的大体流程可以压缩成 4 步：

1. 某个 integration test 失败后，系统自动触发 Auto-Diagnose。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]]
2. 它收集 `test driver` 和 `SUT` component 的 `INFO` 及以上日志，把跨 `data center / process / thread / logging level` 的文本按时间戳 join 成单一日志流。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026.pdf]]
3. 它把这条日志流放进 `<LOGS=>`，再把 component metadata 放进 `<CONTEXT=>`，然后对 `Gemini 2.5 Flash` 做一次单轮调用；公开参数是 `temperature = 0.1`、`top-p = 0.8`。prompt 会强约束模型只能依据相关 component 的日志下结论，缺日志时不许瞎猜。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026.pdf]]
4. 模型返回后，系统把结果后处理成 markdown，把相关日志行转成可点击链接，并把一条 structured finding 直接发进 `Critique`。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/arxiv-abstract-auto-diagnose-google|arXiv 摘要整理]]

这里最关键的判断是：`Auto-Diagnose` 的“智能部分”并不是一个会来回调查、反复试探的 agent，而更像一次大上下文、强约束、单轮完成的 diagnosis call。前面的日志汇总是规则式预处理，后面的结果落地是规则式后处理；真正的模型推理被压缩在中间这一枪里。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026.pdf]]

## 它真正的贡献

如果把这篇工作当成“新算法”来看，它并不新；但如果把它放回软件工程和生产工具这个语境里，它的贡献很明确。

第一，它证明了一个很朴素的系统设计已经足够解决高价值 bottleneck。`integration test triage` 的难点本来就不是“会不会写代码”，而是人要在大量异构日志里找出真正的 root cause。Auto-Diagnose 做的不是把整个 debugging 全自动化，而是先把最费脑力、最耗时的第一步切下来。[[sources/auto-diagnose-2026-04/source/arxiv-abstract-auto-diagnose-google|arXiv 摘要整理]] [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]]

第二，它提供的是 `deployment evidence`，不是 benchmark 幻觉。公开材料里真正有价值的数字包括：71 个真实失败案例上的 `90.14%` root-cause diagnosis 成功率、Google 范围内 `52,635` 个 distinct failing tests、`p50 56 秒` 把 finding 发进 Critique、以及 `5.8%` 的 `Not helpful` 反馈率。它的说服力不在“模型有多聪明”，而在“这套简单流程上线后有没有真被人用、真节省时间、真没有惹怒开发者”。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/arxiv-abstract-auto-diagnose-google|arXiv 摘要整理]] [[sources/auto-diagnose-2026-04/source/icse-2026-session-page-auto-diagnose|ICSE 页面整理]]

第三，它给了一个很重要的工程判断：不要太早把目标设成 `full autonomous repair`。在今天的生产环境里，自动修复要面对的风险远大于 triage，因为它涉及代码修改、状态影响、测试重跑和责任边界；而 triage 先天更适合做成“高价值、低侵入”的 LLM 工具。Auto-Diagnose 的成功，本质上是在提醒：先把 `deterministic log funnel -> single-shot diagnosis -> workflow-native surfacing` 这种简单链路做到可靠，再谈大而全的 autonomous repair。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/icse-2026-session-page-auto-diagnose|ICSE 页面整理]]

## 一个更准确的结论

`Auto-Diagnose` 的主要贡献，不是提出了花哨的新 agent 架构，而是证明了：在一个很真实、很痛、很贵的生产问题上，规则式日志汇总加上一轮受强约束的 LLM 诊断，已经能稳定创造价值。它的启发不是“LLM 已经会自动修系统”，而是“别急着做大而全的自动修复，先把 triage 做到快、准、嵌入现有工作流”。[[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|论文整理]] [[sources/auto-diagnose-2026-04/source/arxiv-abstract-auto-diagnose-google|arXiv 摘要整理]] [[sources/auto-diagnose-2026-04/source/icse-2026-session-page-auto-diagnose|ICSE 页面整理]]

## Sources

- [[sources/auto-diagnose-2026-04/summary|auto-diagnose-2026-04]]
- [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026|paper-auto-diagnose-google-icse-2026]]
- [[sources/auto-diagnose-2026-04/source/paper-auto-diagnose-google-icse-2026.pdf]]
- [[sources/auto-diagnose-2026-04/source/arxiv-abstract-auto-diagnose-google|arxiv-abstract-auto-diagnose-google]]
- [[sources/auto-diagnose-2026-04/source/icse-2026-session-page-auto-diagnose|icse-2026-session-page-auto-diagnose]]
