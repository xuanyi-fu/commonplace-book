---
type: index
status: draft
created: 2026-04-20
updated: 2026-04-22
---

# index

- [[sources/ai-scientist-2026-04/summary|ai-scientist-2026-04]]: source collection for AiScientist architecture, File-as-Bus coordination, and the public runtime/module layout
- [[sources/components-of-a-coding-agent-2026-04/summary|components-of-a-coding-agent-2026-04]]: source collection for Sebastian Raschka's coding-agent article covering repo context, prompt caching, tools, memory, and subagents
- [[sources/axi-agent-experience-interface-2026-04/summary|axi-agent-experience-interface-2026-04]]: source collection for AXI's agent-first CLI principles, TOON dependency, benchmark docs, and reference implementation readmes
- [[sources/agent-harness-origins-2023-2026/summary|agent-harness-origins-2023-2026]]: source collection for the public emergence of `agent harness` from early naming through Manus and Philipp Schmid's explicit system-level framing
- [[syntheses/components-of-a-coding-agent-layer-mismatch-and-state-resumption|components-of-a-coding-agent-layer-mismatch-and-state-resumption]]: synthesis arguing that Sebastian Raschka's coding-agent component split mixes harness infra with coding-specific app-layer optimizations while making a fair point about resumable state
- [[syntheses/ai-scientist-file-as-bus-state-and-context-flow|ai-scientist-file-as-bus-state-and-context-flow]]: synthesis of how AiScientist turns research state into files and routes those artifacts back into later agent context
- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]: source collection for how Multica stores shared task state in platform objects, session pointers, and daemon-rehydrated execution environments
- [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]: synthesis comparing Multica's platform-state sharing model with AiScientist's File-as-Bus artifact layer
- [[sources/fire-pdf-2026-04/summary|fire-pdf-2026-04]]: source collection for Fire-PDF architecture, parser modes, and the role of pdf-inspector
- [[entities/fire-pdf|fire-pdf]]: entity page for Fire-PDF as a PDF parsing subsystem with mixed extraction architecture and credit-based pricing
- [[concepts/web-agent|web-agent]]: concept page for agents that treat the browser as an execution environment rather than only a reading surface
- [[concepts/agent-harness|agent-harness]]: concept page defining the infrastructure layer that wraps a model and governs long-running agent execution
- [[sources/browser-use-2026-04/summary|browser-use-2026-04]]: source collection for Browser Use's positioning, Python/CLI workflows, and one local logged-in-site trial
- [[entities/browser-use|browser-use]]: entity page for Browser Use as a browser execution layer inside the web-agent stack
- [[sources/weak-to-strong-supervision-2026-04/summary|weak-to-strong-supervision-2026-04]]: source collection for the motivation, formal setup, and current alignment-research framing of weak-to-strong supervision
- [[sources/windsurf-position-2026-04/summary|windsurf-position-2026-04]]: source collection for Windsurf scale claims and public usage signals
- [[entities/windsurf|windsurf]]: entity page for Windsurf as a multi-agent IDE product with current public positioning and market signals
- [[entities/qwen3-6-35b-a3b|qwen3-6-35b-a3b]]: entity page for the open-weight sparse multimodal model positioned for agentic coding
- [[sources/transformer-moe-2026-04/summary|transformer-moe-2026-04]]: source collection for learning what a Transformer MoE layer is, how routing works, and how FFN-to-expert replacement changes capacity versus active compute
- [[syntheses/left-multiply-token-right-multiply-channel|left-multiply-token-right-multiply-channel]]: 解释在“行 = token，列 = channel”的约定下，为什么左乘会 mix token、右乘会 mix channel
- [[syntheses/qwen3-8b-parameter-breakdown-and-ffn-over-attention|qwen3-8b-parameter-breakdown-and-ffn-over-attention]]: 用 Qwen3-8B 把 GQA、SwiGLU 参数分解，以及为什么 Transformer 更愿意膨胀 FFN 而不是 attention 算清楚
- [[sources/codex-memory-2026-04/summary|codex-memory-2026-04]]: source collection for current official docs and observed UI around Codex memory support
- [[sources/codex-memory-implementation-2026-04/summary|codex-memory-implementation-2026-04]]: source collection，收录 Codex memory 在 app-server、core、state 三层的实现笔记与 prompt 快照
- [[syntheses/codex-memory-support-and-boundaries|codex-memory-support-and-boundaries]]: synthesis of Codex memory's implementation pipeline, file layering, and control surfaces
- [[sources/codex-computer-use-2026-04/summary|codex-computer-use-2026-04]]: source collection for official docs, local interface notes, and one failure case around Codex computer use
- [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]]: synthesis of how Codex computer use appears to work and where it currently breaks down
- [[sources/ai-agent-weekly-2026-04-18/summary|ai-agent-weekly-2026-04-18]]: cleaned April 18, 2026 AI Agents Weekly issue covering agent models, tooling, and research updates
- [[sources/auto-diagnose-2026-04/summary|auto-diagnose-2026-04]]: source collection for Google Auto-Diagnose covering the paper, workflow integration into Critique, and reported evaluation metrics
- [[syntheses/auto-diagnose-simple-triage-over-full-repair|auto-diagnose-simple-triage-over-full-repair]]: synthesis arguing that Auto-Diagnose matters less as an agent novelty than as evidence that simple one-shot triage can deliver production value
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]]: synthesis arguing that a better agent harness exposes atomic capabilities instead of baking task intelligence into rigid workflows
- [[syntheses/agent-harness-philipp-schmid-overall-reading|agent-harness-philipp-schmid-overall-reading]]: synthesis summarizing one complete reading of Philipp Schmid's 2026-01 agent-harness argument
- [[sources/claude-advisor-strategy-2026-04/summary|claude-advisor-strategy-2026-04]]: source collection for Anthropic's advisor strategy public API shape and its relation to routing, cascading, and shepherding papers
- [[sources/claude-managed-agents-2026-04/summary|claude-managed-agents-2026-04]]: source collection for Anthropic's managed-agent runtime objects, event protocol, permissions, MCP, skills, memory, multi-agent, and outcomes
- [[entities/claude-managed-agents|claude-managed-agents]]: entity page for Claude Managed Agents as Anthropic's hosted agent runtime with versioned configs, stateful sessions, and preview orchestration layers
- [[sources/anthropic-mcp-production-systems-2026-04/summary|anthropic-mcp-production-systems-2026-04]]: source collection for Anthropic's April 22, 2026 MCP blog post on production agent connectivity, remote server design, context-efficient clients, and skills
- [[notes/anthropic-mcp-production-systems-2026-04-reading-note|anthropic-mcp-production-systems-2026-04-reading-note]]: canonical reading note for the Anthropic MCP production-systems article, initialized with Keshav-lite, reading state, and section queue
- [[sources/cloudflare-mcp-2026-04/summary|cloudflare-mcp-2026-04]]: source collection for Cloudflare's official Cloudflare API MCP server materials, including the two-tool Code Mode design and Dynamic Worker sandbox execution model
- [[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]: source collection for official MCP Apps docs, stable spec text, and proposal-to-launch announcement material
- [[entities/mcp-apps|mcp-apps]]: entity page for MCP Apps as the official MCP extension for interactive UI rendered inside compliant hosts
- [[sources/obsidian-cli/summary|obsidian-cli]]: summary page for the `sources/obsidian-cli/` collection
- [[sources/andrej-llm-wiki-git-gist/summary|andrej-llm-wiki-git-gist]]: summary page for the `sources/andrej-llm-wiki-git-gist/` collection
