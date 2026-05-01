---
type: summary
status: draft
created: 2026-04-30
updated: 2026-04-30
---

# openai-responses-websockets-2026-04

This source collection preserves OpenAI's April 22, 2026 engineering post "Speeding up agentic workflows with WebSockets in the Responses API." It is meant to support implementation-oriented research on Responses API WebSocket mode, Codex agent-loop latency, `previous_response_id` state reuse, and transport-level optimization around faster inference.

## Structure

- `source/openai-responses-websockets-reader-capture.md`: reader-captured webpage artifact for the OpenAI post
- `source/openai-responses-websockets-markdown.md`: best-effort Markdown derivative of the article body, with global site navigation/footer removed and the two main article diagrams localized
- `source/assets/openai-responses-websockets/`: localized copies of the two OpenAI-hosted article diagrams referenced by the Markdown derivative
- `summary.md`: collection summary and usage guide

## How To Use

- Start with `source/openai-responses-websockets-markdown.md` for a readable and searchable copy of the article body.
- Use `source/openai-responses-websockets-reader-capture.md` when you need the captured page text, original source URL, article metadata, or residual webpage context.
- Use this collection when researching Responses API transport design, Codex agent-loop latency, WebSocket state caching, `previous_response_id`, rendered-token reuse, safety/validation incrementalization, and the effect of faster inference on surrounding API services.
- Direct raw HTML capture from `openai.com` was not practical during ingest because direct `curl` returned HTTP 403. No login was needed; the collection therefore preserves a reader capture as the practical webpage artifact.

## Summary

The post explains why faster model inference made Responses API service overhead visible in Codex-style agent loops: Codex repeatedly asks the API for the model's next action, executes local tools, returns tool outputs, and continues until the task is done. OpenAI frames the resulting work as reducing end-to-end agent-loop latency by 40%, while allowing users to experience a jump from roughly 65 tokens per second to nearly 1,000 tokens per second. [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]

OpenAI describes the original structural problem as treating every Codex request independently: each follow-up request reprocessed conversation state and reusable context even when most of the conversation had not changed. Earlier single-request optimizations improved time to first token by nearly 45%, but the API stack was still too expensive relative to GPT-5.3-Codex-Spark's inference speed. [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]

The first WebSocket prototype modeled an agentic rollout as one long-running Response. After the model sampled a tool call, the Responses API blocked in the sampling loop, sent `response.done` to the client, then accepted a client `response.append` event with the tool result so sampling could continue. OpenAI compares this to treating a local tool call like a hosted tool call, except the tool executes on the client side. [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]

The launched version kept the familiar `response.create` shape and used `previous_response_id` to continue from previous response state. On a WebSocket connection, the server keeps connection-scoped in-memory state, including the previous response object, prior input/output items, tool definitions/namespaces, and reusable sampling artifacts such as rendered tokens. This lets validators, safety classifiers, token rendering, routing, and postinference work operate incrementally instead of rebuilding the full conversation each time. [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]

The launch section reports production adoption and downstream integrations: Codex ramped most Responses API traffic onto WebSockets, GPT-5.3-Codex-Spark hit the 1,000 TPS target with bursts up to 4,000 TPS, Vercel saw up to 40% latency decrease through AI SDK integration, Cline reported 39% faster multi-file workflows, and Cursor reported up to 30% faster OpenAI-model use. [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]

## Sources

- [[source/openai-responses-websockets-reader-capture|openai-responses-websockets-reader-capture.md]]
- [[source/openai-responses-websockets-markdown|openai-responses-websockets-markdown.md]]
