---
type: source
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# codex-memory-implementation-2026-04

这个 source collection 收集了截至 `2026-04-20` 对 Codex memory 实现的第一手代码级材料，基于本地仓库 `/Users/bytedance/codex/codex-latest/codex` 中的 `openai/codex@d62421d32299aa5fdc30b131471eb06f03f1c91a` 快照整理。它关注的不是产品文案，而是 memory 在 `app-server`、`core`、`state` 三层里究竟如何触发、抽取、落盘、注入，以及对应 prompt 模板长什么样。

## Structure

- `source/local-code-reading-codex-memory-pipeline-2026-04-20.md`: 代码阅读笔记，按触发时机、Phase 1、Phase 2、注入路径、`app-server` 接口和 `polluted` 线程治理来整理
- `source/local-followup-clarifications-codex-memory-pipeline-2026-04-20.md`: 对同一实现的二次澄清，重点补 `Phase 1` 是否起 agent、`Phase 2` 的真实输入形态，以及 `memory_summary.md` / `MEMORY.md` 的分工
- `source/openai-codex-d62421d-memory-stage-one-system.md`: [`openai/codex@d62421d.../codex-rs/core/templates/memories/stage_one_system.md`](https://github.com/openai/codex/blob/d62421d32299aa5fdc30b131471eb06f03f1c91a/codex-rs/core/templates/memories/stage_one_system.md) 的直接拷贝
- `source/openai-codex-d62421d-memory-stage-one-input.md`: [`openai/codex@d62421d.../codex-rs/core/templates/memories/stage_one_input.md`](https://github.com/openai/codex/blob/d62421d32299aa5fdc30b131471eb06f03f1c91a/codex-rs/core/templates/memories/stage_one_input.md) 的直接拷贝
- `source/openai-codex-d62421d-memory-consolidation.md`: [`openai/codex@d62421d.../codex-rs/core/templates/memories/consolidation.md`](https://github.com/openai/codex/blob/d62421d32299aa5fdc30b131471eb06f03f1c91a/codex-rs/core/templates/memories/consolidation.md) 的直接拷贝
- `source/openai-codex-d62421d-memory-read-path.md`: [`openai/codex@d62421d.../codex-rs/core/templates/memories/read_path.md`](https://github.com/openai/codex/blob/d62421d32299aa5fdc30b131471eb06f03f1c91a/codex-rs/core/templates/memories/read_path.md) 的直接拷贝
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/local-code-reading-codex-memory-pipeline-2026-04-20.md`，它回答“memory 具体怎么实现”的主问题
- 再读 `source/local-followup-clarifications-codex-memory-pipeline-2026-04-20.md`，它补充几个最容易混淆的点
- 如果你只关心“什么时候开始沉淀 memory”，重点看那页里的 `启动入口与触发时机`
- 如果你只关心“沉淀格式是什么”，重点看 `Phase 1`、`Phase 2` 和 `落盘产物`
- 如果你只关心 `Phase 1` 是不是 agent、以及 `memory_summary.md` 和 `MEMORY.md` 的关系，直接从 follow-up note 开始
- 如果你要核对 prompt 约束，直接打开四个 prompt 拷贝文件；它们是这个 repo snapshot 下的原文
- 讨论产品能力时，把这个 collection 当作“实现层证据”，不要和官方产品文档或 UI 文案混在一起

## Summary

这组材料显示，Codex memory 的主体实现并不在 `app-server`，而是在 `core/src/memories/` 和 `state/src/runtime/memories.rs`。`app-server` 暴露的是控制接口，例如线程级 `memory_mode` 开关和 `memory/reset`；真正的 pipeline 则是在 root session 启动时异步触发。进一步说，`Phase 1` 不是 subagent，而是一次内部的结构化抽取调用，先把满足条件的旧线程提取成 sqlite 里的 stage-1 outputs；`Phase 2` 再把这些 stage-1 输出同步成 `raw_memories.md` / `rollout_summaries/*.md`，随后起一个内部 consolidation subagent 生成 `MEMORY.md`、`memory_summary.md` 和可选 `skills/`。未来线程并不是直接读旧聊天，而是先通过 `read_path.md` 模板消费 `memory_summary.md` 这个默认注入的路由层，再按需检索 `MEMORY.md` 这个详细知识库。

## Sources

- [[source/local-code-reading-codex-memory-pipeline-2026-04-20|local-code-reading-codex-memory-pipeline-2026-04-20.md]]
- [[source/local-followup-clarifications-codex-memory-pipeline-2026-04-20|local-followup-clarifications-codex-memory-pipeline-2026-04-20.md]]
- [[source/openai-codex-d62421d-memory-stage-one-system|openai-codex-d62421d-memory-stage-one-system.md]]
- [[source/openai-codex-d62421d-memory-stage-one-input|openai-codex-d62421d-memory-stage-one-input.md]]
- [[source/openai-codex-d62421d-memory-consolidation|openai-codex-d62421d-memory-consolidation.md]]
- [[source/openai-codex-d62421d-memory-read-path|openai-codex-d62421d-memory-read-path.md]]
