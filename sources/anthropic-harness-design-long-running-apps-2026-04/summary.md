---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# anthropic-harness-design-long-running-apps-2026-04

这个 source collection 保存了 Anthropic 2026-03-24 的工程文章 “Harness design for long-running application development”，重点覆盖 frontend design 的 generator/evaluator 循环、长时 autonomous coding 的 planner-generator-evaluator 架构，以及 `context reset`、sprint contract、file-based handoff、evaluator load-bearing boundary 这些 harness 设计问题。[[source/harness-design-long-running-apps-markdown]] [[source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]] [[source/harness-design-long-running-apps-markdown#^three-agent-architecture]] [[source/harness-design-long-running-apps-markdown#^sprint-contract]] [[source/harness-design-long-running-apps-markdown#^file-based-agent-communication]] [[source/harness-design-long-running-apps-markdown#^evaluator-load-bearing-boundary]]

## Structure

- `source/harness-design-long-running-apps.html`: Anthropic 原始网页 HTML，作为 authoritative source 保存页面原始结构与链接
- `source/harness-design-long-running-apps-markdown.md`: 对正文做的 best-effort Markdown derivative，保留标题层级、表格、引用块、附录，并为后续复用加了少量 block ids
- `source/assets/harness-design-long-running-apps/`: markdown derivative 依赖的本地化正文资源，包括 8 张 PNG 截图和 2 个 MP4 demo
- `summary.md`: 这个 collection 的导读、范围说明和使用建议

## How To Use

- 先读 `source/harness-design-long-running-apps-markdown.md`，它最适合顺序阅读、搜索、摘引和后续做 reading note。
- 需要核对原始发布时间、链接目标、页面布局、原始嵌入资源和 HTML 细节时，回到 `source/harness-design-long-running-apps.html`。
- 如果你关注 Anthropic 怎么解释 `context reset` 与 compaction 的差别，以及为什么 Sonnet 4.5 时 reset 仍然是必要 harness 组件，优先看 `^context-reset-vs-compaction` 和 `^sonnet45-context-resets-essential`。[[source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]] [[source/harness-design-long-running-apps-markdown#^sonnet45-context-resets-essential]]
- 如果你关注长时 coding harness 的系统形状，重点看 `^three-agent-architecture`、`^sprint-contract`、`^file-based-agent-communication` 和 `^hard-threshold-evaluator`。[[source/harness-design-long-running-apps-markdown#^three-agent-architecture]] [[source/harness-design-long-running-apps-markdown#^sprint-contract]] [[source/harness-design-long-running-apps-markdown#^file-based-agent-communication]] [[source/harness-design-long-running-apps-markdown#^hard-threshold-evaluator]]
- 如果你关注模型升级后哪些 scaffold 还算 load-bearing，直接看 `^remove-sprint-construct` 和 `^evaluator-load-bearing-boundary`。[[source/harness-design-long-running-apps-markdown#^remove-sprint-construct]] [[source/harness-design-long-running-apps-markdown#^evaluator-load-bearing-boundary]]
- 这次抓取不需要登录或额外浏览器交互；正文图片和 mp4 demo 都已经本地化到 `source/assets/**`，所以在本仓库里打开 derivative 不依赖站外相对资源。

## Summary

这篇文章的核心不是先给出一个抽象 taxonomy，再把工程技巧往里塞；它是从两个实验路径反推“哪些 harness 设计真正在 frontier agentic coding 里起作用”。第一条路径是 frontend design：作者把主观审美判断拆成可评分 criteria，再用 generator/evaluator 循环做多轮迭代，借此把“设计好不好”变成一个更稳定的优化问题。[[source/harness-design-long-running-apps-markdown#^gan-generator-evaluator]]

第二条路径是 long-running autonomous coding：文章把这个模式扩展成 planner-generator-evaluator 三代理系统，并在 generator 与 evaluator 之间加入 sprint contract，再通过 file-based handoff 维持多轮实现与 QA 的衔接。作者同时明确区分了 `context reset` 与 compaction，并说明在 Claude Sonnet 4.5 上，compaction 还不足以解决 `context anxiety`，所以 reset 当时仍然是 harness 的关键组件。[[source/harness-design-long-running-apps-markdown#^three-agent-architecture]] [[source/harness-design-long-running-apps-markdown#^sprint-contract]] [[source/harness-design-long-running-apps-markdown#^file-based-agent-communication]] [[source/harness-design-long-running-apps-markdown#^context-reset-vs-compaction]] [[source/harness-design-long-running-apps-markdown#^sonnet45-context-resets-essential]]

文章最后给出的更强信号是：harness 组件不是固定配方，而是随模型边界移动的可删减 scaffold。到 Opus 4.6，这个实验里 sprint construct 已经可以去掉，而 evaluator 也不再是固定必需项；它是否值得保留，取决于任务是否已经超出当前模型单跑的可靠边界。[[source/harness-design-long-running-apps-markdown#^remove-sprint-construct]] [[source/harness-design-long-running-apps-markdown#^evaluator-load-bearing-boundary]]

## Sources

- [[source/harness-design-long-running-apps|harness-design-long-running-apps.html]]
- [[source/harness-design-long-running-apps-markdown|harness-design-long-running-apps-markdown.md]]
