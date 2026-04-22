# AI Weekly News Ingest

Use this file when the source is one issue from the AI Agents Weekly mail workflow, typically from `nlpnews@substack.com`.

## What Counts

- one dated issue from the AI Agents Weekly email workflow
- a saved raw email artifact such as HTML or EML for that issue
- a cleaned Markdown issue snapshot that preserves the issue order

Do not use this flow for general weekly roundup webpages unless they are actually the newsletter issue being ingested.

## Required And Preferred Artifacts

- Preserve the raw email artifact whenever practical.
- Preserve a cleaned Markdown issue snapshot for reading, search, and quoting.
- The raw email artifact is the authoritative source.
- The cleaned Markdown issue snapshot is a convenience derivative and does not replace the original email artifact.
- If live mailbox access is unavailable but a saved local HTML archive exists, that archive is an acceptable original artifact.

## Allowed Normalization

- removing mailbox chrome and HTML-only artifacts
- preserving the original language
- preserving issue order, section flow, headings, bullets, and links as much as practical
- repairing extraction noise when the goal is faithful normalization rather than rewriting

## Prohibited Interpretation

Do not let the cleaned issue snapshot become:

- a summary of the issue
- a translated or rewritten edition
- a reordered list of only the items that seem important
- a merged document across multiple issue dates
- an explanation of whether the newsletter's claims are correct

Treat the newsletter as a curated secondary source. Important claims should still be verified against primary sources before promoting them into stable wiki pages.

## Naming Guidance

- Prefer `source/newsletter-email-YYYY-MM-DD.html` or `source/newsletter-email-YYYY-MM-DD.eml` for the original email artifact.
- Prefer `source/newsletter-issue-YYYY-MM-DD.md` for the cleaned Markdown issue snapshot.
- Keep one date per collection and avoid mixing multiple issue dates in the same artifact set.

## `summary.md` Expectations

In `summary.md`:

- identify the issue date
- identify the sender or newsletter identity
- identify the raw email artifact and the cleaned issue snapshot
- state whether the raw artifact is an email export, saved HTML archive, or another preserved mail artifact
- remind the reader that this is a curated secondary source and not a primary source bundle

## Example

```md
## Structure

- `source/newsletter-email-2026-04-18.html`: preserved raw email artifact
- `source/newsletter-issue-2026-04-18.md`: cleaned issue snapshot with original order preserved
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/newsletter-email-2026-04-18|newsletter-email-2026-04-18.html]]
- [[source/newsletter-issue-2026-04-18|newsletter-issue-2026-04-18.md]]
```
