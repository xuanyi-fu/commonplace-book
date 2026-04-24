---
type: summary
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# codex-model-context-inputs-2026-04

这个 source collection 收录了一份本地 Codex 代码阅读分析，主题是 Codex 在一次模型调用前如何构造 model context inputs。分析对象固定为 [`openai/codex@d62421d32299aa5fdc30b131471eb06f03f1c91a`](https://github.com/openai/codex/tree/d62421d32299aa5fdc30b131471eb06f03f1c91a)，归一化版本把原文里的相对代码引用改成了固定到该 commit 的 `github.com/openai/codex/blob/...` 链接。[[source/model-context-inputs-github-links|model-context-inputs-github-links.md]]

## Structure

- `source/model-context-inputs-local.md`: 从 `/Users/bytedance/codex/codex-latest/codex/codex-rs/docs/model-context-inputs.md` 复制出来的原始本地 Markdown 快照
- `source/model-context-inputs-github-links.md`: 同一份分析的归一化版本，只把 `../...` 代码引用改为固定到 `d62421d32299aa5fdc30b131471eb06f03f1c91a` 的 GitHub blob 链接
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/model-context-inputs-github-links.md`，它的每个代码引用都可以直接跳到 GitHub 上对应 commit 的具体行
- 需要核对这份分析在 ingest 前的原始形态时，再看 `source/model-context-inputs-local.md`
- 把这个 collection 当作 Codex model-visible context 构造路径的代码阅读证据；它不是官方产品文档，也不应该替代对目标 commit 源码的核对
- 后续写 entity、concept 或 synthesis 时，优先引用 `source/model-context-inputs-github-links.md`，因为它的 evidence 链接已经固定到 `openai/codex@d62421d32299aa5fdc30b131471eb06f03f1c91a`

## Summary

这份分析把一次 Codex 模型请求拆成几层：Responses API 顶层 `instructions`、请求里的 `input` / `tools`，developer-role context bundle，contextual user fragments，baseline context，后续 turn 的 context diff，以及 `reasoning`、`prompt_cache_key`、`service_tier` 这类非文本 request controls。核心结论是：Codex 的 top-level `instructions` 是一个被优先级规则选中的 base-instruction string；`AGENTS.md`、environment context、skills、plugins、memory guidance、collaboration mode、hooks 等材料多数作为 `input` 中的 developer 或 contextual user messages 注入，而不是拼进 top-level `instructions`。[[source/model-context-inputs-github-links|model-context-inputs-github-links.md]]

它还区分了几个容易混淆的输入面：skills 列表作为 developer bundle 的 metadata 出现，显式调用的 full `SKILL.md` body 则作为 user-role `<skill>...</skill>` fragment 注入；environment context 是 contextual user fragment；memory read path 是 prompt-plus-files 机制，而不是专门的 Responses tool schema；普通 user message 解析会跳过 contextual user messages。[[source/model-context-inputs-github-links|model-context-inputs-github-links.md]]

## Sources

- [[source/model-context-inputs-local|model-context-inputs-local.md]]
- [[source/model-context-inputs-github-links|model-context-inputs-github-links.md]]
