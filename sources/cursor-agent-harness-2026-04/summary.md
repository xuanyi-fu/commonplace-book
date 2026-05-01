---
type: summary
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# cursor-agent-harness-2026-04

This source collection preserves Cursor's April 30, 2026 research post "Continually improving our agent harness." The post explains Cursor's agent-harness engineering process around context-window management, online and offline evals, degradation repair, model-specific harness tuning, mid-chat model switching, and future multi-agent orchestration. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

## Structure

- `source/continually-improving-agent-harness.html`: original Cursor blog HTML artifact
- `source/continually-improving-agent-harness-markdown.md`: best-effort Markdown derivative of the article's main content, with navigation and related-post chrome removed
- `source/assets/continually-improving-agent-harness/`: localized light and dark variants of the article's three body diagrams
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/continually-improving-agent-harness-markdown.md` for source-order reading and quoting. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]
- Use `source/continually-improving-agent-harness.html` when checking the original Cursor page structure, metadata, or exact rendered asset references. [[source/continually-improving-agent-harness|continually-improving-agent-harness.html]]
- The original webpage was available as raw HTML; no logged-in or browser-rendered fallback capture was needed.
- Use this collection as primary Cursor evidence for harness iteration, measurement, error taxonomy, model-specific tool/prompt customization, and multi-agent orchestration claims.
- Compare with `cursor-sdk-2026-04` when separating Cursor's programmable agent API surface from Cursor's internal harness-improvement process. [[sources/cursor-sdk-2026-04/summary|cursor-sdk-2026-04]]

## Summary

The post frames Cursor's agent harness as a product that is improved through hypotheses, experiments, quantitative and qualitative signals, evals, and real usage. Cursor says model early-access work converges on weeks of harness customization until a model in Cursor's tuned harness becomes faster, smarter, and more efficient than the raw model experience. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

The context-window section says Cursor's early coding agent used heavier static context and guardrails because late-2024 models were worse at choosing context. Cursor now keeps only some static context, removes many older guardrails, and emphasizes dynamic context that agents can fetch while working. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

The evaluation section distinguishes public/offline benchmarks from online product measurements. Cursor tracks metrics like latency, token efficiency, tool call count, cache hit rate, and "Keep Rate" for agent-generated code, and also uses a model to read user responses as a semantic satisfaction signal. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

The degradation section treats unknown tool-call errors as harness bugs, classifies expected errors by cause, computes per-tool and per-model baselines, runs anomaly alerts, and uses weekly automations plus Cloud Agents / Linear to investigate and fix regressions. The model-specific section says Cursor customizes tool formats and prompts by provider and model version, and even mitigated one model's `context anxiety` with prompt changes. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

The final sections make mid-chat model switching explicitly a harness problem: Cursor switches prompts and tools when the user switches models, adds instructions for taking over another model's conversation, summarizes to reduce cache penalty, and points to subagents as a cleaner way to get a fresh context window. Cursor closes by arguing that future AI-assisted software engineering will be multi-agent, and that deciding which specialized agent to dispatch and how to stitch results together will live in the harness. [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]

## Sources

- [[source/continually-improving-agent-harness|continually-improving-agent-harness.html]]
- [[source/continually-improving-agent-harness-markdown|continually-improving-agent-harness-markdown.md]]
