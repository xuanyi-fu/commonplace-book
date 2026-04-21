---
type: entity
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Fire-PDF

Fire-PDF 当前更适合被理解成 Firecrawl 里的一个专门 PDF 解析子系统，而不是 agent，也不是单一模型。它的目标是把 text-based、scanned 和 mixed PDF 都转换成结构化 markdown，同时尽量保住阅读顺序、表格、公式和多栏结构。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]] [[sources/fire-pdf-2026-04/source/official-doc-document-parsing|Firecrawl 文档解析文档]]

## 功能

如果只看当前公开资料，Fire-PDF 的主要功能可以概括成 4 个点：

- 把 PDF 转成结构化 markdown，而不是只抽纯文本。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]] [[sources/fire-pdf-2026-04/source/official-doc-document-parsing|Firecrawl 文档解析文档]]
- 同时支持 text-based PDF 和 scanned PDF。[[sources/fire-pdf-2026-04/source/official-doc-document-parsing|Firecrawl 文档解析文档]]
- 尽量保住复杂版面信息，包括阅读顺序、表格、公式、段落和多栏结构。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]]
- 作为 Firecrawl 的默认 PDF 解析路径自动运行，不需要单独配置。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]]

## 大概实现

目前公开资料支持一个相当清楚的分层实现图，而不是“一个模型端到端完成所有事情”。

- 第一层是 `pdf-inspector`：
  - 这是一个开源 Rust 组件
  - 负责分类 PDF 类型
  - 对 text-based PDF 做原生提取和 markdown 转换
  - 它明确不是 OCR，也不是 ML 模型。[[sources/fire-pdf-2026-04/source/official-repo-pdf-inspector-readme|pdf-inspector README]]
- 第二层是神经布局检测：
  - 对需要 OCR 的页面先渲染成图
  - 然后用 `neural document layout model` 产出区域框、元素类型和阅读顺序
  - 官方没有公开说明这个布局模型具体叫什么或是否开源。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]]
- 第三层是 OCR / vision-language extraction：
  - 扫描区域会送到 `GLM-OCR`
  - 不同区域类型会用不同 prompt 和参数处理。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]]
- 最后一层是 assembly：
  - 结果按阅读顺序拼成 markdown
  - 表格转 markdown table
  - 公式保留为 LaTeX。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]]

所以更准确的说法是：Fire-PDF 是一个混合式 parser pipeline，而不是 agent，也不是单模型产品。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]] [[sources/fire-pdf-2026-04/source/official-repo-pdf-inspector-readme|pdf-inspector README]]

## 收费

Fire-PDF 不是单独订阅，而是挂在 Firecrawl 的 credit 计费体系下面。[[sources/fire-pdf-2026-04/source/official-doc-billing-pdf-pricing|Billing 文档]] [[sources/fire-pdf-2026-04/source/official-pricing-page-firecrawl-plans|Pricing 页面]]

- `Pricing` 页 FAQ 的粗粒度说法是：`1 credit per PDF page`。[[sources/fire-pdf-2026-04/source/official-pricing-page-firecrawl-plans|Pricing 页面]]
- 但 `Billing` 页的细规则写的是：
  - `Scrape = 1 credit / page`
  - `PDF parsing = +1 credit / PDF page`
  - 而且 modifiers 会叠加。[[sources/fire-pdf-2026-04/source/official-doc-billing-pdf-pricing|Billing 文档]]

如果按更细的 `Billing` 页理解，当前处理 PDF 的总成本更像 `2 credits / PDF page`。但这里必须保留一个谨慎点：Firecrawl 官方自己的 pricing 和 billing 两页现在存在口径不完全一致的问题。[[sources/fire-pdf-2026-04/source/official-doc-billing-pdf-pricing|Billing 文档]] [[sources/fire-pdf-2026-04/source/official-pricing-page-firecrawl-plans|Pricing 页面]]

## 暂定判断

Fire-PDF 最值得记的，不只是“PDF 解析更快”，而是它代表了一种更务实的文档解析工程路线：

- 文本型页面尽量走便宜、快速的原生解析
- 扫描页和复杂版面才进入 GPU、布局模型和 OCR
- 对外仍然表现成一个简单的 parser 接口

这说明它的真正卖点不是 agent 智能，而是 ingestion stack 的工程质量。[[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|Fire-PDF 官方发布文]] [[sources/fire-pdf-2026-04/source/official-doc-document-parsing|Firecrawl 文档解析文档]]

## Sources

- [[sources/fire-pdf-2026-04/source/official-blog-fire-pdf-launch-2026-04-14|official-blog-fire-pdf-launch-2026-04-14]]
- [[sources/fire-pdf-2026-04/source/official-doc-document-parsing|official-doc-document-parsing]]
- [[sources/fire-pdf-2026-04/source/official-repo-pdf-inspector-readme|official-repo-pdf-inspector-readme]]
- [[sources/fire-pdf-2026-04/source/official-doc-billing-pdf-pricing|official-doc-billing-pdf-pricing]]
- [[sources/fire-pdf-2026-04/source/official-pricing-page-firecrawl-plans|official-pricing-page-firecrawl-plans]]
