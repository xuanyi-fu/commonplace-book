---
type: summary
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# fire-pdf-2026-04

这个 source collection 收集了截至 2026-04-21 可见的 Fire-PDF 一手资料，重点回答两个具体问题：`Fire-PDF` 到底是 agent、单独模型，还是一条专门的 PDF 解析管线；以及它目前在 Firecrawl 里是如何计费的。

## Structure

- `source/official-blog-fire-pdf-launch-2026-04-14.md`: Firecrawl 官方发布文章，直接描述 Fire-PDF 的整体架构和五阶段流水线
- `source/official-doc-document-parsing.md`: Firecrawl 官方文档，说明 PDF 解析模式、默认行为和对外 API 形态
- `source/official-repo-pdf-inspector-readme.md`: Firecrawl 官方开源仓库 `pdf-inspector` 的 README，解释文本类 PDF 的 Rust 分类与提取组件
- `source/official-doc-billing-pdf-pricing.md`: Firecrawl 官方 billing 文档，给出更细的 PDF credit 计费口径
- `source/official-pricing-page-firecrawl-plans.md`: Firecrawl 官方 pricing 页，给出套餐价格和较粗粒度的 PDF 计费 FAQ
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/official-blog-fire-pdf-launch-2026-04-14.md`，它最直接回答 Fire-PDF 的架构问题
- 再读 `source/official-repo-pdf-inspector-readme.md`，区分“Rust 文本解析组件”与“OCR / 布局模型”这两层
- 用 `source/official-doc-document-parsing.md` 看 Fire-PDF 在对外产品接口里是如何暴露的
- 用 `source/official-doc-billing-pdf-pricing.md` 和 `source/official-pricing-page-firecrawl-plans.md` 对照“精细 credit 规则”和“套餐页 FAQ 说法”
- 讨论时要区分 `Fire-PDF` 整体管线、`pdf-inspector` 这个开源 Rust 组件、以及扫描页上用到的模型层

## Summary

截至 2026-04-21，公开资料支持一个很清楚的结论：`Fire-PDF` 不是 agent，也不是单一模型。它是一条专门的 PDF 解析管线。对文本型页面，它主要依赖开源 Rust 组件 `pdf-inspector` 做分类和原生提取；对扫描页或图像密集页，它再走渲染、神经布局检测和 OCR / vision-language extraction。也就是说，它是一个混合式解析系统，而不是“一个 agent 在读 PDF”。计费上，官方资料同时给出了两套口径：pricing 页 FAQ 写的是 `1 credit per PDF page`，但更细的 billing 页写的是 `Scrape 1 credit / page` 加上 `PDF parsing +1 credit / PDF page`，两页存在口径差异；如果按 billing 页的精细规则理解，当前应按 `2 credits / PDF page` 估算。

## Sources

- [[source/official-blog-fire-pdf-launch-2026-04-14|official-blog-fire-pdf-launch-2026-04-14.md]]
- [[source/official-doc-document-parsing|official-doc-document-parsing.md]]
- [[source/official-repo-pdf-inspector-readme|official-repo-pdf-inspector-readme.md]]
- [[source/official-doc-billing-pdf-pricing|official-doc-billing-pdf-pricing.md]]
- [[source/official-pricing-page-firecrawl-plans|official-pricing-page-firecrawl-plans.md]]
