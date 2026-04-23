# Webpage Ingest

Use this file when the source is a webpage or a browser-rendered page.

## What Counts

- static documentation pages, blog posts, landing pages, changelog pages, and other web-native pages
- pages that require JavaScript rendering, login state, scrolling, expansion, or browser interaction before their full content is visible
- saved local HTML archives of webpages

If the source is primarily a PDF, return to the main skill and route it to `paper-pdf`, `book-pdf`, or the generic `pdf` fallback.
If the material is only an excerpt copied from a known webpage, do not use `short-text.md`; route to this webpage flow instead.

## Required And Preferred Artifacts

- Preserve two source artifacts whenever practical:
  - the original webpage artifact
  - a best-effort Markdown derivative
- The original webpage artifact is the authoritative source.
- The Markdown derivative is a convenience view for reading, search, and quoting. It does not replace the original artifact.
- Prefer raw `html` for the original webpage artifact whenever practical.
- If raw `html` is not practical, save the next-best original webpage artifact and explain the limitation briefly in `summary.md`.

## Allowed Normalization

- deterministic HTML-to-Markdown conversion
- LLM-assisted normalization
- hybrid pipelines that combine browser capture, extraction, and cleanup
- removal of obvious webpage chrome such as navigation, cookie banners, subscription widgets, comment sections, and other non-content UI
- preservation of the page's original title, section order, headings, paragraphs, lists, tables, code blocks, links, footnotes, and citation cues whenever practical
- downloading article-body images or diagrams into `source/**` and rewriting the Markdown derivative to point to those local files when practical

`browser-use` may be used when browser automation is needed to access or fully render the page before saving it. Do not require `browser-use` when a simpler capture path is sufficient.

## Prohibited Interpretation

Do not let the Markdown derivative become:

- a summary
- a rewrite of the author's meaning
- a selective extraction based on model judgment of importance
- a reordered argument
- an explanation, conclusion, or interpretation

If fidelity and readability conflict, keep the original artifact authoritative and prefer preserving source structure over aggressive cleanup.

## Images And Embedded Assets

- Do not leave article-body images as dead site-relative paths such as `/static/...` in the Markdown derivative.
- When the original page includes meaningful images, diagrams, or figures, download them into the same source collection under `source/**` whenever practical.
- Prefer a stable local layout such as `source/assets/<page-slug>/<filename>`.
- Rewrite image references in the Markdown derivative to repo-local relative paths, for example `![diagram](assets/<page-slug>/diagram.png)`.
- If an image cannot be downloaded practically, keep the original source URL and note the limitation in `summary.md`.
- Decorative site chrome images, icons, avatars, and unrelated footer graphics do not need to be localized unless they are part of the source content.

## Naming Guidance

- Prefer `source/<page-slug>.html` for the original webpage artifact when `html` is practical to preserve.
- Prefer `source/<page-slug>-markdown.md` for the Markdown derivative.
- If the original artifact is not `html`, keep the original format and still use `-markdown.md` for the derivative.

## `summary.md` Expectations

In `summary.md`:

- identify which file is the original webpage artifact
- identify which file is the Markdown derivative
- identify any localized image or asset subdirectories if the Markdown derivative depends on them
- state whether browser interaction or rendering was needed before capture
- note any limitation if the original artifact is not raw `html`
- tell the reader which file to start with

## Example

```md
## Structure

- `source/example-page.html`: original webpage artifact
- `source/example-page-markdown.md`: best-effort Markdown derivative for reading and search
- `source/assets/example-page/`: localized images used by the Markdown derivative
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/example-page|example-page.html]]
- [[source/example-page-markdown|example-page-markdown.md]]
```
