# Book PDF Ingest

Use this file when the source is a book, monograph, or other book-length PDF.

## What Counts

- books distributed as PDF
- book-length monographs
- handbooks or textbooks whose primary artifact is a book-style PDF
- long-form PDFs that are better navigated by chapters than by full-text extraction

If the PDF is a research paper, use `paper-pdf.md` instead.
If the PDF is a report, manual, or slide deck rather than a book, use `pdf.md` instead.

## Required And Preferred Artifacts

- Preserve the raw PDF whenever practical.
- Do not create a full-book text derivative by default.
- Add a TOC or chapter-map file when it materially improves navigation.
- The raw PDF is the authoritative source.
- The TOC or chapter-map file is a structural navigation aid and does not replace the raw PDF.

## Allowed Normalization

- extraction of the PDF outline when one exists
- reconstruction of a table of contents from the printed TOC pages
- manual chapter and page-range mapping when the PDF has no reliable embedded outline
- structural listing of parts, chapters, section labels, and page ranges when available

The TOC or chapter-map file should stay structural. It may help readers find the right part of the book, but it should not become a content summary.

## Prohibited Interpretation

Do not let the TOC or chapter-map file become:

- a summary of the book's arguments
- chapter-by-chapter interpretation
- a rewritten explanation of the book
- a partial full-text extract presented as the default companion artifact
- personal reading notes or conclusions

If the PDF is image-only or difficult to inspect, keep the raw PDF authoritative and note the limitation in `summary.md`.

## Naming Guidance

- Prefer `source/<book-slug>.pdf` for the raw PDF.
- Prefer `source/<book-slug>-toc.md` for the TOC or chapter-map file.
- Do not create a full-book Markdown conversion by default.

## `summary.md` Expectations

In `summary.md`:

- identify the raw PDF clearly
- identify the TOC or chapter-map file if one exists
- state that no full-book text derivative is maintained by default
- explain how to use the TOC file to navigate the PDF
- include edition, version, or language metadata when known
- keep the `## Summary` section collection-level rather than interpretive book notes

## Example

```md
## Structure

- `source/example-book.pdf`: authoritative raw PDF
- `source/example-book-toc.md`: structural TOC and chapter map for navigation
- `summary.md`: the collection summary and usage guide

## Sources

- [[source/example-book|example-book.pdf]]
- [[source/example-book-toc|example-book-toc.md]]
```
