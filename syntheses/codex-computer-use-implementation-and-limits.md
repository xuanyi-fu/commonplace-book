---
type: synthesis
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# codex-computer-use-implementation-and-limits

This synthesis is about the current shape of Codex computer use, not the entire Codex product. The direct public record supports a screenshot-driven GUI control loop with macOS permissions, app approvals, and a bounded action surface. The strongest extra implementation signal comes from the local Computer Use tool interface in this desktop session, which explicitly exposes `get_app_state` as screenshot plus accessibility tree and pairs it with element-index and coordinate-based actions.

## Working Thesis

Codex computer use currently looks like a perception-action loop over desktop GUIs, not a deep semantic integration with arbitrary Mac apps. It appears good enough for discrete, inspectable flows, but still early for continuous, timing-sensitive, or semantically opaque interaction.

## Direct Signals

- Public Codex app docs confirm that computer use depends on Screen Recording so Codex can see the target app and Accessibility so Codex can click, type, and navigate.
- Public Codex app docs also confirm that Codex may process screenshots and interact with windows, menus, keyboard input, and clipboard state in the target app.
- Public OpenAI computer-use docs describe a screenshot loop: see the current UI, return structured actions, execute them, capture a new screenshot, and repeat.
- The local desktop tool surface adds a stronger implementation clue than the public docs do: in this session, `get_app_state` returns both a screenshot and an accessibility tree, and the action set includes element-based operations plus coordinate clicks and drags.

## What That Likely Means

- Codex does not need a bespoke app API in order to do useful work in a GUI.
- At the same time, it also does not appear to have rich app-native semantics by default.
- The practical control stack looks closer to:
  - visual inspection of the current app state
  - optional structure from the accessibility layer
  - synthetic mouse and keyboard actions
  - another screenshot to verify what changed
- This is a strong fit for GUI QA, bug reproduction, settings changes, browser tasks, and multi-app knowledge workflows.
- It is a weaker fit for interfaces where the accessibility layer is poor, the UI state changes quickly, or success depends on continuous cursor control rather than discrete steps.

## Reading The STS2 Failure

The user's Slay the Spire 2 test is a good stress case. Codex failed at dragging an attack card onto the intended target. That outcome is consistent with the current architecture for three reasons.

- First, many game interfaces expose little useful accessibility structure. Even if Codex has access to an accessibility tree, the important game objects may still be custom-rendered surfaces with weak or meaningless semantics.
- Second, the documented computer-use loop is screenshot, act, screenshot, act. That is well matched to buttons, menus, text fields, and stepwise flows, but worse for a live drag interaction that depends on continuous feedback and precise hover state.
- Third, dragging a card onto a target in a game is not just a path-planning problem. It often requires low-latency correction against transient visual feedback, which a generic desktop agent surface does not obviously expose.

## Practical Conclusion

- Today, Codex computer use looks mature enough for scoped GUI workflows and exploratory app QA.
- It still looks early for games, drawing tools, highly dynamic canvases, and any task that depends on fast closed-loop cursor control.
- When an app has a dedicated plugin, MCP server, CLI, or stable API, those integrations should usually be preferred over computer use.

## Open Questions

- Public OpenAI docs do not explicitly state the exact native macOS APIs used under the hood.
- Public docs also do not explain the full OCR or vision stack, event injection path, or fallback behavior when accessibility structure is weak.
- The accessibility-tree signal is direct in this local session's tool interface, but that is still different from an official public implementation note from OpenAI.

## Sources

- [[sources/codex-computer-use-2026-04/source/official-doc-codex-app-computer-use|official-doc-codex-app-computer-use]]
- [[sources/codex-computer-use-2026-04/source/blog-2026-04-16-codex-for-almost-everything|blog-2026-04-16-codex-for-almost-everything]]
- [[sources/codex-computer-use-2026-04/source/official-guide-api-computer-use|official-guide-api-computer-use]]
- [[sources/codex-computer-use-2026-04/source/local-session-computer-use-tool-interface-2026-04-20|local-session-computer-use-tool-interface-2026-04-20]]
- [[sources/codex-computer-use-2026-04/source/user-test-sts2-drag-failure-2026-04-20|user-test-sts2-drag-failure-2026-04-20]]
