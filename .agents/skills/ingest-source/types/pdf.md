# PDF Ingest

Use this file when the source is primarily a PDF document that is not best treated as `paper-pdf` or `book-pdf`.

## What Counts

- reports whose primary artifact is a PDF
- manuals, whitepapers, and product documentation distributed as PDF
- slide decks whose primary artifact is a PDF
- other PDF-first materials that are neither research papers nor books

If the PDF is a research paper, use `paper-pdf.md` instead.
If the PDF is a book or other book-length document, use `book-pdf.md` instead.
If the source is primarily a webpage that happens to mention a PDF, use `webpage.md` unless the PDF itself is the material being ingested.

## Required And Preferred Artifacts

- Preserve the raw PDF whenever practical.
- Add a lightweight normalized derivative only when it materially improves reading, search, or quoting.
- The raw PDF is the authoritative source.
- A derivative is a convenience view and does not replace the raw PDF.

## Allowed Normalization

- native text extraction from the PDF
- `pdftotext` as the default lightweight extraction tool for text derivatives
- `pdftotext -layout` when preserving spacing materially improves readability
- best-effort preservation of page order, headings, bullets, links, and other source cues when a derivative is created
- notation in `summary.md` about major extraction limitations when the derivative quality is uneven

## Prohibited Interpretation

Do not let the derivative become:

- a summary
- a paraphrase of the document
- a selective extraction of only the "important" pages or sections
- a rewritten explanation of claims or visuals

If extraction quality is poor, keep the raw PDF authoritative and note the extraction limitation in `summary.md`.

## Naming Guidance

- Prefer `source/<pdf-slug>.pdf` for the raw PDF.
- Prefer `source/<pdf-slug>-text.txt` for a `pdftotext` derivative.
- If a different lightweight derivative format is more practical for the material, keep the naming close to the same slug and explain the format briefly in `summary.md`.

## `summary.md` Expectations

In `summary.md`:

- identify the raw PDF clearly
- identify the derivative if one exists
- state whether the derivative came from `pdftotext` or another lightweight extraction path
- note any major fidelity limitation, such as broken layout or low-value extraction from slide-like pages
- tell the reader which file to start with for reading and which file remains authoritative

## Example

```md
## Structure

- `source/example-report.pdf`: authoritative raw PDF
- `source/example-report-text.txt`: best-effort `pdftotext` derivative
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/example-report|example-report.pdf]]
- [[source/example-report-text|example-report-text.txt]]
```
