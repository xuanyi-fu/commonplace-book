---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# axi-agent-experience-interface-2026-04

这个 source collection 收录 `AXI: Agent eXperience Interface` 的主站原始网页、`TOON` 规范原始网页与官方 Markdown，以及 `axi` / `gh-axi` / `chrome-devtools-axi` 官方仓库里最关键的 README、benchmark 文档和 skill 定义。它的用途是把 AXI 关于 `agent-first interface design`、`TOON`、benchmark 方法和参考实现的原始材料集中保存下来，供后续 source-backed 阅读、引用和概念拆分使用。

## Structure

- `source/axi-agent-experience-interface.html`: 从本地 weekly archive 保留下来的 AXI 主站原始网页 HTML；这是 landing page 的 authoritative webpage artifact
- `source/axi-agent-experience-interface-markdown.md`: 基于保存下来的 AXI 主站 HTML 做的 best-effort Markdown derivative，便于阅读、搜索和引用
- `source/toon-spec.html`: 从本地 weekly archive 保留下来的 TOON 规范原始网页 HTML
- `source/toon-spec-official.md`: TOON 官方规范 Markdown 原文
- `source/axi-readme.md`: `kunchenguid/axi` 官方 README
- `source/axi-bench-browser-report.md`: AXI browser benchmark 的公开结果汇总
- `source/axi-bench-github-study.md`: AXI GitHub benchmark 的公开 study 文档
- `source/axi-skill.md`: AXI 官方 skill 定义
- `source/gh-axi-readme.md`: `kunchenguid/gh-axi` 官方 README
- `source/chrome-devtools-axi-readme.md`: `kunchenguid/chrome-devtools-axi` 官方 README
- `summary.md`: 这个 collection 的摘要和使用说明

## How To Use

- 先读 `source/axi-agent-experience-interface-markdown.md`，用它快速恢复 AXI 主站的论证顺序、10 条原则、benchmark 设置和结论性表述。
- 需要核对 landing page 的原始渲染、页面结构或 conversion 局限时，回到 `source/axi-agent-experience-interface.html`。
- 需要核对 AXI 第 1 条原则背后的格式前提时，先读 `source/toon-spec-official.md`；需要对照网页版本时，再看 `source/toon-spec.html`。
- 需要确认 benchmark 条件、结果表和任务设计时，分别读 `source/axi-bench-browser-report.md` 和 `source/axi-bench-github-study.md`。
- 需要看 AXI 如何落成具体 agent-facing CLI 时，读 `source/gh-axi-readme.md`、`source/chrome-devtools-axi-readme.md` 和 `source/axi-skill.md`。
- 这次 ingest 不需要额外浏览器交互：AXI 主站和 TOON 规范页来自已有的本地 HTML 存档；仓库 README、benchmark 文档和 skill 定义是在 ingest 时直接从官方 GitHub raw 端点补抓的，因为原 weekly workspace 中说明提到的 repo clones 当时并不在磁盘上。

## Summary

这组材料把 AXI 的核心主张拆成了几层一手来源。AXI 主站和官方 README 给出项目自己的 framing：问题不是单纯比较 `CLI` 和 `MCP`，而是为 agent 设计怎样的 interface 才更省 token、更少回合、更易发现下一步。`TOON` 规范页与官方 Markdown 说明了它在 `Token-efficient output` 里依赖的具体结构化表示。两份 benchmark 文档把浏览器和 GitHub 两个 domain 的条件、成本、turn 数、成功率和局限写得更细。`gh-axi`、`chrome-devtools-axi` README 与 `axi-skill.md` 则把这 10 条原则落到了实际命令面、session hook、combined operations 和 contextual suggestions 这些实现层接口上。

## Sources

- [[source/axi-agent-experience-interface|axi-agent-experience-interface.html]]
- [[source/axi-agent-experience-interface-markdown|axi-agent-experience-interface-markdown.md]]
- [[source/toon-spec|toon-spec.html]]
- [[source/toon-spec-official|toon-spec-official.md]]
- [[source/axi-readme|axi-readme.md]]
- [[source/axi-bench-browser-report|axi-bench-browser-report.md]]
- [[source/axi-bench-github-study|axi-bench-github-study.md]]
- [[source/axi-skill|axi-skill.md]]
- [[source/gh-axi-readme|gh-axi-readme.md]]
- [[source/chrome-devtools-axi-readme|chrome-devtools-axi-readme.md]]
