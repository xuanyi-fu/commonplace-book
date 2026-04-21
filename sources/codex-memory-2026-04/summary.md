---
type: summary
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# codex-memory-2026-04

这个 source collection 收集了截至 2026-04-20 可见的 Codex memory 一手资料，包括官方产品发布、官方文档、app 设置页说明、用户提供的当前设置界面截图，以及本地状态观察。它的目标是回答一个很具体的问题：今天的 Codex memory 实际支持到什么程度，以及这些能力在产品里是怎样暴露出来的。

## Structure

- `source/blog-2026-04-16-codex-for-almost-everything-memory.md`: 官方产品发布里关于 memory 的公开定位和可用性说明
- `source/official-doc-codex-memories.md`: 官方 `Memories` 文档，覆盖开关、存储、线程级控制和配置项
- `source/official-doc-codex-chronicle.md`: 官方 `Chronicle` 文档，覆盖屏幕上下文增强 memory 的方式、限制和风险
- `source/official-doc-codex-app-settings-memory.md`: 官方 app `Settings` 文档里关于 `Memories` 和 `Context-aware suggestions` 的说明
- `source/user-screenshot-codex-memory-settings-2026-04-20.md`: 用户提供的当前 Codex memory 设置界面截图整理
- `source/local-observation-codex-memory-storage-2026-04-20.md`: 本地 `~/.codex` 状态观察，记录 memory 目录、空目录现状和当前配置表面
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/official-doc-codex-memories.md`，它是回答“memory 本体支持什么”的主文档
- 再读 `source/official-doc-codex-chronicle.md`，区分普通 memory 和 Chronicle 这个屏幕上下文增强层
- 用 `source/blog-2026-04-16-codex-for-almost-everything-memory.md` 看 memory 在产品发布里的外部承诺和 rollout 表述
- 用 `source/official-doc-codex-app-settings-memory.md` 和 `source/user-screenshot-codex-memory-settings-2026-04-20.md` 对照“文档说什么”和“当前 app UI 里实际露出什么开关”
- 用 `source/local-observation-codex-memory-storage-2026-04-20.md` 区分“目录已经存在”和“真的已经生成 memory 文件”这两件事
- 讨论实现边界时，优先区分“官方明确确认”与“从 UI / 配置表面推断”

## Summary

截至 2026-04-20，Codex memory 处于实验性或预览阶段，不是默认开启能力。官方文档确认它可以把过去线程里的有用上下文沉淀为本地 memory files，并在未来线程中注入使用；官方同时提供线程级控制、配置项覆盖，以及一个名为 Chronicle 的可选屏幕上下文增强层。用户提供的当前设置截图进一步表明，app 里除了 `Enable memories` 和 `Chronicle research preview` 之外，还存在 `Skip tool-assisted chats` 和 `Reset memories` 这类更细粒度的 UI 控制；本地观察则说明 `~/.codex/memories/` 目录的存在本身不等于已经生成了 ordinary memory files。

## Sources

- [[source/blog-2026-04-16-codex-for-almost-everything-memory|blog-2026-04-16-codex-for-almost-everything-memory.md]]
- [[source/official-doc-codex-memories|official-doc-codex-memories.md]]
- [[source/official-doc-codex-chronicle|official-doc-codex-chronicle.md]]
- [[source/official-doc-codex-app-settings-memory|official-doc-codex-app-settings-memory.md]]
- [[source/user-screenshot-codex-memory-settings-2026-04-20|user-screenshot-codex-memory-settings-2026-04-20.md]]
- [[source/local-observation-codex-memory-storage-2026-04-20|local-observation-codex-memory-storage-2026-04-20.md]]
