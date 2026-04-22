# Short-Text Ingest

Use this file when the source is standalone pasted text and there is no stable webpage, PDF, or email original available.

## What Counts

- a short pasted paragraph or note provided directly in chat
- a copied statement whose only available artifact is the pasted text itself
- a brief standalone text snippet that needs to be preserved as a source collection

Do not use this flow for:

- excerpts from a known webpage
- excerpts from a known PDF
- excerpts from a known email or newsletter

If a higher-fidelity original artifact exists or later becomes available, route to the underlying source type instead.

## Required And Preferred Artifacts

- Preserve one faithful text snapshot under `source/`.
- The text snapshot is the authoritative source because no better original artifact is available.
- If useful context exists and can be preserved without interpretation, an additional raw artifact such as a screenshot may accompany the text snapshot.

## Allowed Normalization

- converting the pasted text into a simple `.md` or `.txt` file
- normalizing line endings and obvious paste noise
- preserving paragraph order, list structure, and quote markers from the original pasted text
- adding a minimal provenance note only when needed to explain where the pasted text came from

## Prohibited Interpretation

Do not turn the pasted text into:

- a summary
- a rewritten note
- a cleaned-up argument with new headings or bullets that were not present in the original
- an explanatory memo about what the text means

The goal is preservation, not improvement.

## Naming Guidance

- Prefer `source/<text-slug>.md` for the faithful text snapshot.
- Use `.txt` only when Markdown would add unnecessary structure.
- If an accompanying raw artifact exists, name it semantically and keep it alongside the text snapshot.

## `summary.md` Expectations

In `summary.md`:

- state that this collection is based on standalone pasted text
- explain that no stable webpage, PDF, or email original was available
- identify the faithful text snapshot as the authoritative artifact
- tell the reader whether any additional raw artifact was preserved

## Example

```md
## Structure

- `source/model-announcement-snippet.md`: faithful standalone text snapshot
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/model-announcement-snippet|model-announcement-snippet.md]]
```
