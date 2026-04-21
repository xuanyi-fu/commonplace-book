---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# auto-diagnose-2026-04

这个 source collection 收集了截至 2026-04-21 公开可见的 `Auto-Diagnose` 一手资料，重点回答三个问题：它到底是什么系统、它在 Google 内部是怎么接进开发工作流的、以及公开材料对它的方法和效果做了哪些明确披露。

## Structure

- `source/paper-auto-diagnose-google-icse-2026.pdf`: 原始论文 PDF，保留原始版式、图表和表格
- `source/arxiv-abstract-auto-diagnose-google.md`: arXiv 摘要页整理，适合快速抓 headline 和官方对外摘要口径
- `source/paper-auto-diagnose-google-icse-2026.md`: 论文正文整理，覆盖系统流程、提示设计、模型选择、部署方式和评估数字
- `source/icse-2026-session-page-auto-diagnose.md`: ICSE 2026 session page 整理，补 publication status 和公开会务摘要
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/paper-auto-diagnose-google-icse-2026.md`，它最直接回答 Auto-Diagnose 的方法问题
- 需要看图表、原始排版、表格和论文上下文时，回到 `source/paper-auto-diagnose-google-icse-2026.pdf`
- 再读 `source/arxiv-abstract-auto-diagnose-google.md`，快速回看对外摘要里的定位和 headline 数字
- 用 `source/icse-2026-session-page-auto-diagnose.md` 确认这项工作已经被 ICSE 2026 SEIP 接收，而不只是 arXiv 预印本
- 讨论时要区分三层：
  - `integration-test failure diagnosis`
  - `root-cause suggestion`
  - `full autonomous bug fixing`

## Summary

截至 2026-04-21，公开资料支持一个很清楚的结论：`Auto-Diagnose` 不是一个通用 coding agent，也不是自动修复系统；它是 Google 内部一个面向 integration test failure triage 的 LLM 诊断工具。它会在测试失败后自动收集 test driver 和 SUT component 的日志，把跨数据中心、进程、线程和日志级别的文本按时间戳 join 成单一日志流，再配上上下文元数据送给 `Gemini 2.5 Flash`。模型输出随后被后处理成带可点击日志链接的结构化 finding，并直接发进 `Critique`。公开论文报告的核心数字包括：71 个真实失败案例上的 90.14% root-cause diagnosis 成功率，Google 范围内部署后覆盖 52,635 个 distinct failing tests，median 56 秒把 finding 发进 Critique，`Not helpful` 反馈率为 5.8%。

## Sources

- [[source/paper-auto-diagnose-google-icse-2026.pdf]]
- [[source/arxiv-abstract-auto-diagnose-google|arxiv-abstract-auto-diagnose-google.md]]
- [[source/paper-auto-diagnose-google-icse-2026|paper-auto-diagnose-google-icse-2026.md]]
- [[source/icse-2026-session-page-auto-diagnose|icse-2026-session-page-auto-diagnose.md]]
