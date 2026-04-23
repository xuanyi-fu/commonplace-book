---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# agent-harness-origins-2023-2026

这个 source collection 按时间线收集了 `agent harness` 这个概念从早期公开用词，到被 Manus / Philipp Schmid 明确命名、再到作为长期运行 agent 基础设施被系统化表述的关键网页材料。它适合用来回答两个问题：这个词最早在公开材料里怎么出现，以及今天大家说的 `agent harness` 是怎样从 `agent loop` / `context engineering` / long-running system 这些更早的工程问题里长出来的。

## Structure

- `source/agent-harness-pypi.html`: 2026-04-22 直抓的 PyPI 项目页 HTML；由于 PyPI 挑战页限制，这个文件没有稳定返回正文
- `source/agent-harness-pypi-metadata.json`: 同日抓取的 PyPI JSON metadata；包含 package summary、homepage 和 release history，是该节点的可验证元数据补充
- `source/agent-harness-pypi-markdown.md`: 基于 PyPI 可读页面内容与 JSON metadata 整理的 best-effort markdown derivative
- `source/context-engineering-for-ai-agents-lessons-from-building-manus.html`: Manus 2025-07-18 原始网页 HTML；这是“概念前驱”节点的 authoritative source
- `source/context-engineering-for-ai-agents-lessons-from-building-manus-markdown.md`: Manus 文章正文的 best-effort markdown derivative
- `source/assets/context-engineering-for-ai-agents-lessons-from-building-manus/`: 上一篇 markdown derivative 依赖的本地化正文图片
- `source/context-engineering-for-ai-agents-part-2.html`: Philipp Schmid 2025-12-04 原始网页 HTML；这是显式定义 `Agent Harness` 的关键节点
- `source/context-engineering-for-ai-agents-part-2-markdown.md`: 对应正文的 markdown derivative
- `source/assets/context-engineering-for-ai-agents-part-2/`: 上一篇 markdown derivative 依赖的本地化正文图片
- `source/importance-of-agent-harness-in-2026.html`: Philipp Schmid 2026-01-05 原始网页 HTML；这是把该概念单独系统化展开的关键节点
- `source/importance-of-agent-harness-in-2026-markdown.md`: 对应正文的 markdown derivative
- `source/assets/importance-of-agent-harness-in-2026/`: 上一篇 markdown derivative 依赖的本地化正文图片
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先按时间顺序读：`agent-harness-pypi-markdown.md` -> `context-engineering-for-ai-agents-lessons-from-building-manus-markdown.md` -> `context-engineering-for-ai-agents-part-2-markdown.md` -> `importance-of-agent-harness-in-2026-markdown.md`
- 如果你要回答“最早是谁提出来的”，先看 PyPI 节点；它更像是可验证的早期公开用词，而不是今天这套成熟定义的完整发明时刻
- 如果你要回答“这个概念是怎么衍生出来的”，重点看 Manus 2025 那篇和 Philipp Schmid 2025-12 / 2026-01 两篇：前者提供实践问题和设计压力，后者把这些问题抽象成 `Agent Harness`
- 需要核对原始页面结构、发布时间、链接、图片和 HTML 局限时，回到对应 `.html`；需要做顺序阅读、搜索和引用时，先读对应 `-markdown.md`
- 这三个网页 derivative 的正文图片已经本地化到 `source/assets/**`，所以在 Obsidian 里直接打开 markdown 也能看到图，不必再依赖站外相对路径
- `agent-harness-pypi.html` 由于 PyPI 的挑战页限制，没有稳定返回项目正文；这个节点应与 `agent-harness-pypi-metadata.json` 和 `agent-harness-pypi-markdown.md` 结合使用
- 读完这个 collection 后，如果你要继续看 2026 年 spring 语境里 `coding harness` 被如何拆成具体组件，再接着读 [[sources/components-of-a-coding-agent-2026-04/summary|components-of-a-coding-agent-2026-04]]

## Summary

这组材料显示，`agent harness` 不是一个单点突然发明出来的概念，而是逐步收敛出来的工程语言。2023-08-25 的 PyPI package `agent-harness` 说明这个词在 AI agent 语境里已经公开出现，但当时更像一个项目名或包装层叫法。到 2025-07-18，Manus 的文章虽然主要谈 `context engineering`，但已经把长期 tool loop、KV-cache、action space、file system external memory、error traces 这些后来被归入 `agent harness` 的核心职责讲清楚。随后 Philipp Schmid 在 2025-12-04 明确写出 “Agent Harness is the software that wraps the model”，把它与 `Context Engineering`、`Context Rot`、sub-agent coordination 放进同一套词汇表；到 2026-01-05，这个概念又被进一步推广成一个独立主题，用来解释为什么 frontier agent 的差异越来越多地来自模型外部的系统层，而不只是模型本身。

## Sources

- [[source/agent-harness-pypi|agent-harness-pypi.html]]
- [[source/agent-harness-pypi-metadata|agent-harness-pypi-metadata.json]]
- [[source/agent-harness-pypi-markdown|agent-harness-pypi-markdown.md]]
- [[source/context-engineering-for-ai-agents-lessons-from-building-manus|context-engineering-for-ai-agents-lessons-from-building-manus.html]]
- [[source/context-engineering-for-ai-agents-lessons-from-building-manus-markdown|context-engineering-for-ai-agents-lessons-from-building-manus-markdown.md]]
- [[source/context-engineering-for-ai-agents-part-2|context-engineering-for-ai-agents-part-2.html]]
- [[source/context-engineering-for-ai-agents-part-2-markdown|context-engineering-for-ai-agents-part-2-markdown.md]]
- [[source/importance-of-agent-harness-in-2026|importance-of-agent-harness-in-2026.html]]
- [[source/importance-of-agent-harness-in-2026-markdown|importance-of-agent-harness-in-2026-markdown.md]]
