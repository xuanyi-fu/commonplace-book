# Paper PDF Ingest

Use this file when the source is a research paper, preprint, proceedings paper, or other paper-like academic PDF.

## What Counts

- research papers distributed as PDF
- preprints from archives or lab sites
- conference or workshop papers
- academic-style technical papers whose primary artifact is a PDF

If the PDF is a book or book-length monograph, use `book-pdf.md` instead.
If the PDF is a report, manual, or slide deck rather than a paper, use `pdf.md` instead.

## Required And Preferred Artifacts

- Preserve the raw PDF whenever practical.
- Add a plain-text derivative when it materially improves scanning, search, or quoting.
- The raw PDF is the authoritative source.
- The plain-text derivative is a convenience view and does not replace the raw PDF.
- Use `pdftotext` as the default extraction tool for the text derivative.

## Allowed Normalization

- native text extraction with `pdftotext`
- `pdftotext -layout` when preserving spacing or column structure materially improves readability
- best-effort preservation of page order, headings, paragraphs, lists, links, footnote markers, reference cues, figure captions, and table captions
- brief notation in `summary.md` about major extraction limitations

Figures, tables, equations, page layout, and other visual structure remain PDF-authoritative even when a text derivative exists.

## Prohibited Interpretation

Do not let the text derivative become:

- a summary
- a paraphrase of the paper
- a selective extraction of only the "important" sections
- a rewritten explanation of figures, tables, equations, or claims
- an interpretation of results or conclusions

If extraction quality is poor, keep the raw PDF authoritative and note the limitation in `summary.md`.

## Naming Guidance

- Prefer `source/<paper-slug>.pdf` for the raw PDF.
- Prefer `source/<paper-slug>-text.txt` for the `pdftotext` derivative.
- Do not create figure-by-figure image sidecars by default.

## `summary.md` Expectations

In `summary.md`:

- identify the raw PDF clearly
- identify the `pdftotext` derivative if one exists
- state that the PDF remains authoritative for figures, tables, equations, and layout
- note any major extraction limitation, such as broken columns, missing captions, or unreadable tables
- tell the reader whether to start with the text derivative for scanning or the raw PDF for exact reading

## Example

```md
## Structure

- `source/example-paper.pdf`: authoritative raw PDF
- `source/example-paper-text.txt`: best-effort `pdftotext` derivative for scanning and search
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/example-paper|example-paper.pdf]]
- [[source/example-paper-text|example-paper-text.txt]]
```
