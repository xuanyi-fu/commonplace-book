---
type: summary
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# openai-codex-agent-loop-2026-01

这个 source collection 收录 OpenAI Engineering blog `Unrolling the Codex agent loop`，发布于 2026-01-23，作者是 Michael Bolin。文章解释 Codex harness / Codex CLI 的 agent loop、Responses API 请求形态、`instructions` / `tools` / `input` 的分工、多轮 tool-call 循环、prompt caching、mid-conversation configuration changes，以及 compaction。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

## Structure

- `source/unrolling-the-codex-agent-loop-reader.md`: 通过 Jina Reader 从原网页 URL 取得的 next-best webpage artifact；本地 shell 直接抓取 raw HTML 时得到 Cloudflare challenge 页面，所以没有把 raw HTML 作为权威网页 artifact 保存
- `source/unrolling-the-codex-agent-loop-markdown.md`: 去掉导航和 related-article chrome 后的 Markdown derivative，保留正文顺序、原文链接和正文图片，并把正文图片改写为本地 assets 路径
- `source/assets/unrolling-the-codex-agent-loop/`: 本地化保存的五张正文 SVG 图，包括 agent loop、multi-turn loop 和三个 prompt snapshot 图
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/unrolling-the-codex-agent-loop-markdown.md`，它是更适合阅读、搜索和引用的正文版本
- 需要核对网页读取器输出的原始形态时，再看 `source/unrolling-the-codex-agent-loop-reader.md`
- 需要看图时，使用 `source/assets/unrolling-the-codex-agent-loop/` 中的本地 SVG；Markdown derivative 已经引用这些本地文件
- 使用这篇文章校准 Codex context / prompt 讨论时，要注意它是 2026-01-23 的 OpenAI blog，且聚焦 Codex CLI / harness；它可以补充本地 `openai/codex@d62421d` 代码阅读，但不自动覆盖后续 commit 或 Codex desktop app 的所有差异

## Summary

文章把 Codex agent loop 描述为 user input、model inference、tool call execution、tool observation append、再次 inference 的循环；一个 user-to-agent-response journey 是一个 turn，而一个 turn 内可以包含多次 inference/tool-call 迭代。新一轮对话会把之前 messages 和 tool calls 作为 prompt 的一部分带入，因此 prompt 会随着 conversation 增长。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

在 model inference 部分，文章把 Responses API 请求重点拆成 `instructions`、`tools` 和 `input` 三个字段：`instructions` 来自 `model_instructions_file` 或模型内置 base instructions，`tools` 是可调用工具的 schema 列表，`input` 是发送给模型的 item list。文章进一步说明，Codex 在添加用户消息前，会往 `input` 插入 developer-role permissions message、可选 developer instructions、可选 user-role user instructions / skill metadata、以及 user-role environment context。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

文章还强调 Responses API server 会用 JSON request 派生最终 prompt：server 决定 prompt 前三个 item 的顺序，但其中 `tools` 和 `instructions` 的内容由 client 决定，随后才接上 client 传入的 `input`。后续 SSE output 中的 reasoning 和 function call item，会被表示回下一次请求的 `input`；tool output 也追加进去，从而让旧 prompt 成为新 prompt 的 exact prefix。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

性能部分说明 Codex 目前不使用 `previous_response_id`，以保持请求 stateless 并支持 Zero Data Retention；prompt caching 依赖 exact prefix matches，因此 Codex 尽量把 mid-conversation configuration changes 表达为新的 `input` message，而不是修改旧 message。文章举例：sandbox / approval mode 变化追加新的 role=`developer` permissions message；cwd 变化追加新的 role=`user` environment context message。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

最后，文章把 compaction 描述为 context window management：超过阈值后，用更小、更有代表性的 item list 替换原 `input`，现在通过 Responses API `/responses/compact` endpoint 返回可继续对话的 compacted item list，其中包含 `type=compaction` 的 opaque `encrypted_content`。[[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]

## Sources

- [[source/unrolling-the-codex-agent-loop-reader|unrolling-the-codex-agent-loop-reader.md]]
- [[source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown.md]]
