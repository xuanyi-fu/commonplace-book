---
type: summary
status: draft
created: 2026-04-27
updated: 2026-04-27
---

# kimi-agent-swarms-2026-04

这个 source collection 收集 Kimi K2.6 Agent Swarm、Kimi K2.5 Agent Swarm / PARL、Kimi Code subagent harness、Kimi API agent / thinking 文档，以及若干二级解读材料。它的重点是给后续研究“模型层、训练层、agent harness 层分别为大规模 parallel sub-agents 做了什么”提供可搜索、可引用的原始资料包。

## Structure

- `source/kimi-k2-6-tech-blog.html` 和 `source/kimi-k2-6-tech-blog-markdown.md`: Kimi K2.6 官方技术博客的原始 HTML 和清理版 Markdown，包含 300 sub-agents、4,000 coordinated steps、long-horizon coding、proactive agents、document-to-skills、Claw Groups 等 K2.6 官方表述。
- `source/kimi-k2-6-model-page.html` 和 `source/kimi-k2-6-model-page-markdown.md`: Kimi K2.6 官方模型页面快照。
- `source/kimi-k2-6-hugging-face-model-card.html` 和 `source/kimi-k2-6-hugging-face-model-card-markdown.md`: Hugging Face 上的 Kimi K2.6 model card，包含模型架构、context length、agent benchmark 设置、preserve thinking、interleaved thinking / multi-step tool call、coding agent framework 等信息。
- `source/kimi-k2-5-tech-blog.html` 和 `source/kimi-k2-5-tech-blog-markdown.md`: Kimi K2.5 官方技术博客，包含 Agent Swarm、PARL、trainable orchestrator、frozen subagents、serial collapse、spurious parallelism、Critical Steps 等训练机制说明。
- `source/kimi-k2-5-visual-agentic-intelligence.pdf` 和 `source/kimi-k2-5-visual-agentic-intelligence-text.txt`: Kimi K2.5 arXiv paper 原始 PDF 和文本抽取版，用于核对技术博客里的 PARL 和 swarm 训练细节。
- `source/kimi-agent-swarm-blog.html` 和 `source/kimi-agent-swarm-blog-markdown.md`: Kimi 官方 Agent Swarm 介绍文章，偏产品化说明，覆盖 K2.5 时代 100 sub-agents 的使用场景和早期 research preview 限制。
- `source/kimi-code-agents-and-subagents.html` 和 `source/kimi-code-agents-and-subagents-markdown.md`: Kimi Code 官方 Agents and Subagents 文档，覆盖 YAML agent 定义、built-in subagent types、isolated context、session state、foreground / background execution 等 public harness surface。
- `source/kimi-api-use-kimi-k2-6-to-setup-agent.html` 和 `source/kimi-api-use-kimi-k2-6-to-setup-agent-markdown.md`: Kimi API agent setup 指南，覆盖 tool selection、official tools、自定义 tool、multi-step tool handling 等 API harness 使用方式。
- `source/kimi-api-thinking-models.html` 和 `source/kimi-api-thinking-models-markdown.md`: Kimi API thinking model 指南，覆盖 `kimi-k2.6` thinking 开关、`reasoning_content`、multi-step tool call、Preserved Thinking / `thinking.keep` 等上下文连续性机制。
- `source/github-kimi-cli-main-sha.txt` 和 `source/github-kimi-cli-*.{md,py,yaml}`: Kimi CLI GitHub 源码快照，固定在 `fe60a9d04829f0e054b37afce0c042c104f0f5c3`，用于研究公开 CLI harness 中的 subagent 配置、运行、context 存储、runner 和 registry。
- `source/verdent-kimi-k2-6-agent-swarm.html` / `source/verdent-kimi-k2-6-agent-swarm-markdown.md`, `source/awesome-agents-kimi-k2-6.html` / `source/awesome-agents-kimi-k2-6-markdown.md`, `source/lushbinary-kimi-k2-6-agent-swarm.html` / `source/lushbinary-kimi-k2-6-agent-swarm-markdown.md`: 外部二级解读文章，用于收集行业解读和传播说法；它们不应替代官方文档或源码作为 primary evidence。
- `source/assets/`: Markdown derivative 使用的本地化图片资源。
- `summary.md`: 当前 collection 的目录和使用说明。

## How To Use

- 要查 K2.6 对 Agent Swarm 的官方能力声明，先读 `source/kimi-k2-6-tech-blog-markdown.md`，再用 `source/kimi-k2-6-hugging-face-model-card-markdown.md` 核对 model card 中的架构、context 和 agent benchmark 设定。
- 要查 PARL / Parallel-Agent Reinforcement Learning 的技术细节，优先读 `source/kimi-k2-5-tech-blog-markdown.md`，然后回到 `source/kimi-k2-5-visual-agentic-intelligence.pdf` 或 `source/kimi-k2-5-visual-agentic-intelligence-text.txt` 核对论文表述。
- 要查 agent harness 怎么暴露 subagents，先读 `source/kimi-code-agents-and-subagents-markdown.md`，再看 `source/github-kimi-cli-subagents-*.py`、`source/github-kimi-cli-default-*.yaml` 和 `source/github-kimi-cli-tools-agent-*.md`。
- 要查 API 层的 tool use、thinking、Preserved Thinking 和 multi-step tool call 约定，使用 `source/kimi-api-thinking-models-markdown.md` 和 `source/kimi-api-use-kimi-k2-6-to-setup-agent-markdown.md`。
- 外部二级解读文章适合用来理解市场传播、第三方口径和潜在问题清单；涉及“模型/训练/harness 到底做了什么”的事实判断时，应回到官方博客、paper、model card、API docs 或 CLI source snapshot。
- `.html` 和 `.pdf` 是更接近原始来源的 artifact；`-markdown.md` 和 `-text.txt` 主要用于搜索、阅读和后续引用。
- DataCamp 的 `kimi-k2-agent-swarm-guide` 在本次抓取中返回 HTTP 403，未能保存到 collection。

## Summary

K2.6 官方资料把 Agent Swarm 描述为从 K2.5 research preview 演进而来的横向扩展能力：K2.6 技术博客称其架构扩展到 300 sub-agents 和 4,000 coordinated steps，并把它放在 long-horizon coding、复杂文档分析、网站 / slides / spreadsheet 输出、proactive agents、document-to-skills 等端到端 autonomous run 场景里讨论。[[source/kimi-k2-6-tech-blog-markdown]]

关于“为什么模型会学会有效并行，而不是乱开 agent 或退化成串行”，最相关的一手技术资料仍主要来自 K2.5。K2.5 技术博客和 paper 将 PARL 描述为 trainable orchestrator + dynamically instantiated frozen subagents 的训练设置，并显式讨论 serial collapse、spurious parallelism、`rparallel`、`rfinish` 和 Critical Steps 这类偏 wall-clock latency / critical path 的约束。[[source/kimi-k2-5-tech-blog-markdown]] [[source/kimi-k2-5-visual-agentic-intelligence-text]]

K2.6 model card 补充了模型侧和推理侧使用条件：Kimi K2.6 是 MoE 架构，标称 256K context，并在 agent benchmark 设置里描述了工具配置、context management、preserve thinking mode、interleaved thinking / multi-step tool call、以及推荐的 coding agent framework。[[source/kimi-k2-6-hugging-face-model-card-markdown]]

公开 Kimi Code / Kimi CLI harness 资料展示的是可见的 subagent interface，而不是 Kimi.com 托管 Agent Swarm 的完整 300-agent scheduler。Kimi Code 文档描述 YAML agent 配置、built-in `coder` / `explore` / `plan` subagents、root agent 通过 `Agent` tool 启动 subagent、subagent 拥有 isolated context 并在 session directory 下维护自己的 history 和 metadata；CLI 源码快照则提供了这些 public harness 机制的具体实现入口。[[source/kimi-code-agents-and-subagents-markdown]] [[source/github-kimi-cli-subagents-store]] [[source/github-kimi-cli-subagents-runner]]

## Sources

- [[source/kimi-k2-6-tech-blog|kimi-k2-6-tech-blog.html]]
- [[source/kimi-k2-6-tech-blog-markdown|kimi-k2-6-tech-blog-markdown.md]]
- [[source/kimi-k2-6-model-page|kimi-k2-6-model-page.html]]
- [[source/kimi-k2-6-model-page-markdown|kimi-k2-6-model-page-markdown.md]]
- [[source/kimi-k2-6-hugging-face-model-card|kimi-k2-6-hugging-face-model-card.html]]
- [[source/kimi-k2-6-hugging-face-model-card-markdown|kimi-k2-6-hugging-face-model-card-markdown.md]]
- [[source/kimi-k2-5-tech-blog|kimi-k2-5-tech-blog.html]]
- [[source/kimi-k2-5-tech-blog-markdown|kimi-k2-5-tech-blog-markdown.md]]
- [[source/kimi-k2-5-visual-agentic-intelligence|kimi-k2-5-visual-agentic-intelligence.pdf]]
- [[source/kimi-k2-5-visual-agentic-intelligence-text|kimi-k2-5-visual-agentic-intelligence-text.txt]]
- [[source/kimi-agent-swarm-blog|kimi-agent-swarm-blog.html]]
- [[source/kimi-agent-swarm-blog-markdown|kimi-agent-swarm-blog-markdown.md]]
- [[source/kimi-code-agents-and-subagents|kimi-code-agents-and-subagents.html]]
- [[source/kimi-code-agents-and-subagents-markdown|kimi-code-agents-and-subagents-markdown.md]]
- [[source/kimi-api-use-kimi-k2-6-to-setup-agent|kimi-api-use-kimi-k2-6-to-setup-agent.html]]
- [[source/kimi-api-use-kimi-k2-6-to-setup-agent-markdown|kimi-api-use-kimi-k2-6-to-setup-agent-markdown.md]]
- [[source/kimi-api-thinking-models|kimi-api-thinking-models.html]]
- [[source/kimi-api-thinking-models-markdown|kimi-api-thinking-models-markdown.md]]
- [[source/github-kimi-cli-main-sha|github-kimi-cli-main-sha.txt]]
- [[source/github-kimi-cli-readme|github-kimi-cli-readme.md]]
- [[source/github-kimi-cli-docs-agents|github-kimi-cli-docs-agents.md]]
- [[source/github-kimi-cli-default-agent|github-kimi-cli-default-agent.yaml]]
- [[source/github-kimi-cli-default-coder|github-kimi-cli-default-coder.yaml]]
- [[source/github-kimi-cli-default-explore|github-kimi-cli-default-explore.yaml]]
- [[source/github-kimi-cli-default-plan|github-kimi-cli-default-plan.yaml]]
- [[source/github-kimi-cli-tools-agent-init|github-kimi-cli-tools-agent-init.py]]
- [[source/github-kimi-cli-tools-agent-description|github-kimi-cli-tools-agent-description.md]]
- [[source/github-kimi-cli-subagents-builder|github-kimi-cli-subagents-builder.py]]
- [[source/github-kimi-cli-subagents-core|github-kimi-cli-subagents-core.py]]
- [[source/github-kimi-cli-subagents-models|github-kimi-cli-subagents-models.py]]
- [[source/github-kimi-cli-subagents-registry|github-kimi-cli-subagents-registry.py]]
- [[source/github-kimi-cli-subagents-runner|github-kimi-cli-subagents-runner.py]]
- [[source/github-kimi-cli-subagents-store|github-kimi-cli-subagents-store.py]]
- [[source/verdent-kimi-k2-6-agent-swarm|verdent-kimi-k2-6-agent-swarm.html]]
- [[source/verdent-kimi-k2-6-agent-swarm-markdown|verdent-kimi-k2-6-agent-swarm-markdown.md]]
- [[source/awesome-agents-kimi-k2-6|awesome-agents-kimi-k2-6.html]]
- [[source/awesome-agents-kimi-k2-6-markdown|awesome-agents-kimi-k2-6-markdown.md]]
- [[source/lushbinary-kimi-k2-6-agent-swarm|lushbinary-kimi-k2-6-agent-swarm.html]]
- [[source/lushbinary-kimi-k2-6-agent-swarm-markdown|lushbinary-kimi-k2-6-agent-swarm-markdown.md]]
