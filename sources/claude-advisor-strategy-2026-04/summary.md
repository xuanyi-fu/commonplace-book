---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# claude-advisor-strategy-2026-04

这个 source collection 收集了 2026-04-13 左右为理解 Anthropic `advisor strategy` 而整理的直接材料：两份 Anthropic 官方网页，以及四篇用来判断它和 `routing`、`cascading`、`hierarchical inference`、`shepherding` 关系的论文。collection 的目标不是给出最终结论，而是把“官方到底公开了什么”和“它在学术谱系里更接近什么”这两层材料放在一起。

## Structure

- `source/anthropic-advisor-strategy.html`: Anthropic 官方博客原始 HTML
- `source/anthropic-advisor-strategy-markdown.md`: 上述博客页的 best-effort Markdown derivative，便于检索和引用
- `source/anthropic-advisor-tool.html`: Anthropic `Advisor tool` API 文档原始 HTML
- `source/anthropic-advisor-tool-markdown.md`: 上述文档页的 best-effort Markdown derivative；正文已抽出，但部分站点 chrome 和格式噪音仍保留，原始 HTML 仍是网页权威版本
- `source/llm-cascades-mixture-of-thoughts-2310.03094.pdf`: 2023 `LLM cascades` 论文原始 PDF
- `source/llm-cascades-mixture-of-thoughts-2310.03094-text.txt`: 对该 PDF 的 `pypdf` 文本抽取，便于快速搜索
- `source/routing-and-cascading-2410.10347.pdf`: 2025 `routing` / `cascading` 统一框架论文原始 PDF
- `source/routing-and-cascading-2410.10347-text.txt`: 对该 PDF 的 `pypdf` 文本抽取
- `source/llm-shepherding-2601.22132.pdf`: 2026 `LLM Shepherding` 论文原始 PDF
- `source/llm-shepherding-2601.22132-text.txt`: 对该 PDF 的 `pypdf` 文本抽取
- `source/multi-llm-routing-hierarchical-survey-2506.06579.pdf`: 多模型 `routing` / hierarchical inference survey 原始 PDF
- `source/multi-llm-routing-hierarchical-survey-2506.06579-text.txt`: 对该 PDF 的 `pypdf` 文本抽取
- `summary.md`: 这个 collection 的导读、范围说明和使用建议

## How To Use

- 先读 `source/anthropic-advisor-strategy-markdown.md`，建立 Anthropic 自己对 `advisor strategy` 的产品叙述：executor / advisor 分工、单请求 handoff、成本与 benchmark 口径。
- 再读 `source/anthropic-advisor-tool-markdown.md`，把公开 API 形态看实：`advisor_20260301`、`server_tool_use`、`advisor_tool_result`、`usage.iterations[]`、multi-turn 约束、streaming 行为。
- 如果你要精确确认网页里的代码块、表格、或某些格式细节，以原始 HTML 为准：
  - `source/anthropic-advisor-strategy.html`
  - `source/anthropic-advisor-tool.html`
- 接着用论文建立分类边界：
  - `source/llm-cascades-mixture-of-thoughts-2310.03094-text.txt`：看经典 `cascading` 的 `all-or-nothing` 升级语义。
  - `source/routing-and-cascading-2410.10347-text.txt`：看 `routing` 和 `cascading` 的统一定义。
  - `source/llm-shepherding-2601.22132-text.txt`：看 “Pay for hints, not answers” 这种更像 advisor 的提示式协作。
  - `source/multi-llm-routing-hierarchical-survey-2506.06579-text.txt`：看更大的多模型推理分类框架。
- 讨论细节时，PDF 仍然是论文权威版本。文本抽取版适合扫标题、摘要、术语和关键段落，但公式、表格、图示和版面仍以原始 PDF 为准。

## Summary

从 Anthropic 官方材料看，`advisor strategy` 不是一个泛泛的 prompt pattern，而是已经进入 Claude Platform 的平台能力：顶层仍然是 executor model，advisor 通过 `tools` 里的 `advisor_20260301` 声明为一个 server-side tool，在单个 `/v1/messages` 请求中完成 handoff。公开文档明确给出了 `server_tool_use`、`advisor_tool_result`、`usage.iterations[]`、multi-turn conversation 约束和 streaming 行为，因此这套能力已经有相当具体的 runtime 形态，而不只是营销描述。

从学术对照材料看，Anthropic 的做法和传统 `query-level` `cascading` 有明显亲缘关系，但并不等同。经典 `routing` / `cascading` 多半关注“这条 query 该交给哪一层模型”或“是否整体升级到更强模型”；而 `advisor strategy` 更像 executor 在执行中途向强模型请求一个 hint / plan / correction，然后继续由 executor 产出最终结果。按这批材料来看，它更接近 `hint-based`、`mid-generation`、`executor-led` 的 hierarchical inference / shepherding 风格变体。

这个 collection 因此最适合回答两类问题：第一，Anthropic 在公开 API 层到底暴露了哪些实现约束；第二，把它放到已有多模型成本优化文献里时，更准确的分类位置是什么。若要继续写 entity 或 synthesis，这一组 source 足够作为第一层证据基础。

## Sources

- [[source/anthropic-advisor-strategy|anthropic-advisor-strategy.html]]
- [[source/anthropic-advisor-strategy-markdown|anthropic-advisor-strategy-markdown.md]]
- [[source/anthropic-advisor-tool|anthropic-advisor-tool.html]]
- [[source/anthropic-advisor-tool-markdown|anthropic-advisor-tool-markdown.md]]
- [[source/llm-cascades-mixture-of-thoughts-2310.03094|llm-cascades-mixture-of-thoughts-2310.03094.pdf]]
- [[source/llm-cascades-mixture-of-thoughts-2310.03094-text|llm-cascades-mixture-of-thoughts-2310.03094-text.txt]]
- [[source/routing-and-cascading-2410.10347|routing-and-cascading-2410.10347.pdf]]
- [[source/routing-and-cascading-2410.10347-text|routing-and-cascading-2410.10347-text.txt]]
- [[source/llm-shepherding-2601.22132|llm-shepherding-2601.22132.pdf]]
- [[source/llm-shepherding-2601.22132-text|llm-shepherding-2601.22132-text.txt]]
- [[source/multi-llm-routing-hierarchical-survey-2506.06579|multi-llm-routing-hierarchical-survey-2506.06579.pdf]]
- [[source/multi-llm-routing-hierarchical-survey-2506.06579-text|multi-llm-routing-hierarchical-survey-2506.06579-text.txt]]
