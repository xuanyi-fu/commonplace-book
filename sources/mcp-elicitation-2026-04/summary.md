---
type: summary
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# mcp-elicitation-2026-04

This source collection keeps a lightweight primary-source pack for MCP elicitation: the official versioned elicitation specification page and source text from the official MCP docs repo, plus the official `modelcontextprotocol/inspector` README passages that show one real client implementation handling elicitation-shaped user interaction. [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-definition]] [[source/official-inspector-readme-markdown#^inspector-elicitation-timeout]]

## Structure

- `source/official-spec-elicitation-2025-11-25.html`: raw published HTML capture of the official 2025-11-25 elicitation specification page
- `source/official-spec-elicitation-2025-11-25.mdx`: raw source MDX from the official `modelcontextprotocol/modelcontextprotocol` repository for the same versioned spec page
- `source/official-spec-elicitation-2025-11-25-markdown.md`: faithful markdown derivative of the versioned spec text, with reusable block ids on the main normative passages
- `source/official-inspector-readme.md`: raw README snapshot from the official `modelcontextprotocol/inspector` repository
- `source/official-inspector-readme-markdown.md`: faithful markdown derivative of the Inspector README, with block ids on the elicitation-relevant client-behavior passages
- `summary.md`: this collection summary and usage guide

## How To Use

- Start with `source/official-spec-elicitation-2025-11-25-markdown.md` for the protocol contract: what elicitation is, how capability negotiation works, the `elicitation/create` request shape, form versus URL mode, response actions, and the client/server security boundary.
- Use `source/official-inspector-readme-markdown.md` when you need one concrete official client-side example rather than only the abstract spec. The saved README passages show that Inspector treats elicitation as a user-interaction case for timeout handling and documents client-side form-input behavior. [[source/official-inspector-readme-markdown#^inspector-elicitation-timeout]] [[source/official-inspector-readme-markdown#^inspector-form-input-omissions]] [[source/official-inspector-readme-markdown#^inspector-form-input-required]]
- Fall back to `source/official-spec-elicitation-2025-11-25.html`, `source/official-spec-elicitation-2025-11-25.mdx`, and `source/official-inspector-readme.md` when you need the exact raw published artifact instead of the normalized markdown note.

## Summary

The official elicitation spec defines elicitation as a standardized way for an MCP server to request more information from the user through the client during an ongoing interaction. It standardizes capability declaration, the `elicitation/create` request, two modes (`form` and `url`), restricted form schemas, explicit `accept` / `decline` / `cancel` response actions, and client-side safety requirements around consent, review, and URL handling. [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-definition]] [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-capability-modes]] [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-request-core]] [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-form-schema]] [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-response-actions]] [[source/official-spec-elicitation-2025-11-25-markdown#^elicitation-url-client-rules]]

The Inspector material adds one concrete implementation datapoint from an official client: the Inspector README explicitly treats elicitation as a user-interaction case that may require longer client-side timeouts, and its input-validation guidance shows how the client handles schema-shaped form inputs before they go back to the server. [[source/official-inspector-readme-markdown#^inspector-elicitation-timeout]] [[source/official-inspector-readme-markdown#^inspector-form-input-omissions]] [[source/official-inspector-readme-markdown#^inspector-form-input-required]]

## Sources

- [[source/official-spec-elicitation-2025-11-25.html|official-spec-elicitation-2025-11-25.html]]
- [[source/official-spec-elicitation-2025-11-25.mdx|official-spec-elicitation-2025-11-25.mdx]]
- [[source/official-spec-elicitation-2025-11-25-markdown|official-spec-elicitation-2025-11-25-markdown.md]]
- [[source/official-inspector-readme|official-inspector-readme.md]]
- [[source/official-inspector-readme-markdown|official-inspector-readme-markdown.md]]
