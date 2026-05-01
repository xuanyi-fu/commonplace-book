# Latent.Space AINews Ingest

Use this file when the source is one Latent.Space / AINews issue page, especially a daily issue page whose title starts with `[AINews]`.

## What Counts

- one public or subscriber Latent.Space / AINews issue page
- one dated AINews daily issue, preserved as a single source collection
- issue pages that combine an opening essay or editorial frame with the AINews roundup structure
- browser-rendered or logged-in issue pages when raw page capture needs browser state

Do not use this flow for arbitrary Latent.Space essays, interviews, podcasts, or blog posts that are not AINews issue pages. Use `webpage.md` for those.

Do not merge multiple AINews issue dates into one collection.

## Required And Preferred Artifacts

- Preserve raw `html` for the issue page whenever practical.
- Preserve a cleaned Markdown derivative for reading, search, and quoting.
- The raw `html` artifact is the authoritative source when it is available.
- The Markdown derivative is a convenience view and does not replace the original issue artifact.
- If raw `html` is not practically available from a logged-in or browser-rendered page, preserve the strongest rendered evidence set available:
  - rendered DOM snapshot
  - rendered article text
  - extracted links
  - full-page screenshot
  - localized body images or diagrams
- When raw `html` is not available, state the capture limitation clearly in `summary.md` and identify which fallback artifacts should be used for audit.

Treat AINews as a curated secondary source. Important claims should still be verified against primary sources before promoting them into stable wiki pages.

## Allowed Normalization

- deterministic or browser-assisted HTML-to-Markdown conversion
- cleanup of page chrome, subscription widgets, navigation, comments, and footer material
- preservation of the issue title, date, section order, headings, paragraphs, bullets, links, images, and source-order roundup items whenever practical
- extraction of link targets into a companion links file when the Markdown derivative cannot preserve them reliably
- downloading issue-body images or diagrams into `source/assets/<issue-slug>/` and rewriting Markdown image references to local paths
- light repair of extraction noise when the goal is faithful normalization rather than rewriting

## Prohibited Interpretation

Do not let the Markdown derivative or rendered text become:

- a summary of the issue
- a translated or rewritten edition
- a reordered list of only the items that seem important
- a merged document across multiple issue dates
- an explanation of whether the issue's claims are correct

Interpretation belongs in `summary.md` or later wiki pages, not in files under `source/`.

## Naming Guidance

- Prefer collection slugs like `latent-space-daily-ai-news-YYYY-MM-DD`.
- Prefer `source/<issue-slug>.html` for the raw webpage artifact when raw `html` is practical.
- Prefer `source/<issue-slug>-markdown.md` for the cleaned Markdown derivative.
- If raw `html` is not practical, prefer fallback names shaped like:
  - `source/<issue-slug>-rendered-dom.txt`
  - `source/<issue-slug>-text.txt`
  - `source/<issue-slug>-links.md`
  - `source/<issue-slug>-full-page.png`
  - `source/assets/<issue-slug>/`
- Keep one issue date per collection and keep the same `<issue-slug>` across companion artifacts.

## `summary.md` Expectations

In `summary.md`:

- identify the issue date and Latent.Space / AINews identity
- identify which file is the raw webpage artifact, if one exists
- identify the cleaned Markdown derivative
- identify rendered fallback artifacts and localized asset directories when raw `html` was not practical
- state whether browser rendering, login state, or subscriber access was needed before capture
- remind the reader that AINews is a curated secondary source and not a primary source bundle
- tell the reader which file to start with for source-order reading and which artifacts to use for audit

## Example

```md
## Structure

- `source/ainews-example-issue.html`: raw issue webpage artifact
- `source/ainews-example-issue-markdown.md`: cleaned Markdown derivative for reading and search
- `source/assets/ainews-example-issue/`: localized body images used by the Markdown derivative
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/ainews-example-issue|ainews-example-issue.html]]
- [[source/ainews-example-issue-markdown|ainews-example-issue-markdown.md]]
```

Rendered fallback example:

```md
## Structure

- `source/ainews-example-issue-markdown.md`: cleaned Markdown derivative from browser-rendered content
- `source/ainews-example-issue-rendered-dom.txt`: rendered DOM snapshot used as the closest available structural artifact
- `source/ainews-example-issue-text.txt`: rendered article text snapshot
- `source/ainews-example-issue-links.md`: extracted link targets from the rendered page
- `source/ainews-example-issue-full-page.png`: full-page screenshot for boundary and completeness checks
- `source/assets/ainews-example-issue/`: localized body images used by the Markdown derivative
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/ainews-example-issue-markdown|ainews-example-issue-markdown.md]]
- [[source/ainews-example-issue-rendered-dom|ainews-example-issue-rendered-dom.txt]]
- [[source/ainews-example-issue-text|ainews-example-issue-text.txt]]
- [[source/ainews-example-issue-links|ainews-example-issue-links.md]]
- [[source/ainews-example-issue-full-page.png|ainews-example-issue-full-page.png]]
```
