---
type: synthesis
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# Codex Memory 目前支持什么，以及边界在哪里

截至 2026-04-20，Codex 的 memory 已经不是一句笼统的“会记住你”了，而是一个有明确开关、存储位置、线程级控制和扩展层的功能集合。更准确地说，今天的 Codex memory 至少包含两层：一层是普通的 thread-derived memories，另一层是用屏幕上下文增强 memory 生成的 `Chronicle`。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]] [[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]

## 工作判断

如果只回答“今天 Codex 支不支持 memory”，答案是支持；但如果问“它是不是默认就有、是不是无限制、是不是所有上下文都会自动记住”，答案都是否定的。它现在更像一个可配置、可局部关闭、默认关闭的本地记忆层，而不是一个总是隐式开启的全局人格记忆系统。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]] [[sources/codex-memory-2026-04/source/user-screenshot-codex-memory-settings-2026-04-20|用户设置截图]]

## 今天已经明确支持的部分

- `memory` 可以把过去线程里的有用上下文带到未来线程里使用。官方明确给出的例子包括稳定偏好、重复工作流、技术栈、项目约定和已知坑点。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- `memory` 不是默认开启的，需要在 app settings 里打开，或者在 `~/.codex/config.toml` 里设置 `[features] memories = true`。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- memory 是“从线程生成，再供未来线程使用”的结构，不是简单地把每轮对话原样拼接过去。官方文档明确写到，它会从符合条件的历史线程生成本地 memory files，而且会跳过活跃线程和短生命周期线程。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- memory 有线程级控制。官方文档明确写到，在 app 和 TUI 里可以用 `/memories` 控制当前线程是否能使用已有 memories，以及当前线程是否允许被拿去生成未来 memories。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- memory 有明确的本地存储位置。主 memory 文件默认放在 `~/.codex/memories/` 下，包含 summaries、durable entries、recent inputs 和 prior threads 的 supporting evidence。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- app 的当前 UI 还暴露了几个文档里不够显眼、但非常关键的控制项：`Skip tool-assisted chats` 和 `Reset memories`。这说明 memory 不只是“开/关”两档，还有“是否从用了 MCP / web search 的聊天中生成记忆”以及“一键全部清空”的控制面。[[sources/codex-memory-2026-04/source/user-screenshot-codex-memory-settings-2026-04-20|用户设置截图]]

## Chronicle 是什么

`Chronicle` 不是普通 memory 本身，而是一个给 memory 增强输入来源的研究预览层。它通过屏幕上下文来帮助 Codex 建 memory，从而减少用户重复解释自己刚刚在看什么、刚刚在做什么。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]

- 官方文档明确把 Chronicle 写成 `opt-in research preview`。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]
- 它只对 `ChatGPT Pro + macOS` 开放，而且在 `EU / UK / Switzerland` 不可用。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]
- 它要求先开启 Memories，再单独开启 Chronicle，还需要 `Screen Recording` 和 `Accessibility` 权限。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]
- 它当前会比较快地消耗 rate limits，并且会提高 prompt injection 风险。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]
- 它生成的 Chronicle memories 也是本地未加密 markdown 文件，默认放在 `$CODEX_HOME/memories_extensions/chronicle/`。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]

## 这说明今天的 memory 设计重点是什么

从这些资料看，Codex 团队目前对 memory 的设计重点不是“让模型尽可能多记住一切”，而是“让记忆成为一个可控的本地状态层”。这个判断主要有 4 个依据。

- 第一，它默认关闭，而不是默认打开。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- 第二，它把主存储位置明确放在本地目录里，而不是只把 memory 当成云端黑盒。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]] [[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]
- 第三，它把“能不能生成 memory”和“能不能使用 memory”拆成了可分别控制的行为。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- 第四，当前 UI 已经出现了 `Skip tool-assisted chats` 和 `Reset memories` 这种很偏治理、而不是偏炫技的控制项。[[sources/codex-memory-2026-04/source/user-screenshot-codex-memory-settings-2026-04-20|用户设置截图]]

## 今天还不该高估的部分

- 官方产品发布虽然把 memory 描述成可以记住偏好、纠正和耗时收集的信息，但这仍然是 `preview` 语境，不应该把它理解成“稳定、全面、总是命中”的长期个人知识库。[[sources/codex-memory-2026-04/source/blog-2026-04-16-codex-for-almost-everything-memory|官方发布文章]] 
- 官方文档明确提醒：必须长期生效的团队规范仍然应该写进 `AGENTS.md` 或版本库文档，而不是只依赖 memories。这个提醒很关键，它实际上是在承认 memory 目前更像 recall layer，而不是 policy layer。[[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]]
- Chronicle 虽然能让 Codex 用最近屏幕上下文来辅助建记忆，但它同时引入了更高的 prompt injection 风险，也会处理截图帧、OCR 文本、时间信息和本地路径。这意味着它不是一个“开了就更聪明”的纯增益功能，而是带来明显安全和隐私权衡的实验能力。[[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]]

## 一个更准确的结论

如果把今天的 Codex memory 用一句话概括，我会写成：

`Codex 已经支持可配置的跨线程 memory，而且这个 memory 已经细化到本地存储、线程级控制、筛选条件、重置入口和屏幕上下文增强层；但它仍然是实验性、预览性、带明确地域和套餐限制的能力，而不是一个默认开启、完全可靠、无治理成本的长期记忆系统。` [[sources/codex-memory-2026-04/source/blog-2026-04-16-codex-for-almost-everything-memory|官方发布文章]] [[sources/codex-memory-2026-04/source/official-doc-codex-memories|官方 Memories 文档]] [[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|官方 Chronicle 文档]] [[sources/codex-memory-2026-04/source/user-screenshot-codex-memory-settings-2026-04-20|用户设置截图]]

## Sources

- [[sources/codex-memory-2026-04/source/blog-2026-04-16-codex-for-almost-everything-memory|blog-2026-04-16-codex-for-almost-everything-memory]]
- [[sources/codex-memory-2026-04/source/official-doc-codex-memories|official-doc-codex-memories]]
- [[sources/codex-memory-2026-04/source/official-doc-codex-chronicle|official-doc-codex-chronicle]]
- [[sources/codex-memory-2026-04/source/official-doc-codex-app-settings-memory|official-doc-codex-app-settings-memory]]
- [[sources/codex-memory-2026-04/source/user-screenshot-codex-memory-settings-2026-04-20|user-screenshot-codex-memory-settings-2026-04-20]]
