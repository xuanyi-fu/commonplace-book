---
name: ingest-source
description: Use this skill when adding a new source collection to this knowledge-base wiki. It explains the shared ingest contract, how to route different source types to type-specific guidance, how to write sources/<collection>/summary.md, how to update index.md, and how to validate and commit the ingest in the repository's required format.
---

# Ingest Source

Use this skill when the task is to add a new source collection to this repository.

This skill is repo-specific and must follow [AGENTS.md](/Users/bytedance/Documents/knowledge-base/AGENTS.md:1).

## Shared Contract

Every ingested source collection must end up in this shape:

```text
sources/
  <collection-kebab-case>/
    summary.md
    source/
      ...
```

Rules:

- The collection folder name must use `kebab-case`.
- The collection root must contain exactly `summary.md` and `source/`.
- Original source artifacts and faithful normalized derivatives must live under `sources/<collection>/source/**`.
- Do not place source artifacts directly under `sources/<collection>/`.
- Files under `source/` are for source material only. Do not use `source/` for summaries, rewrites, conclusions, or personal understanding.
- `summary.md` is the only source-collection entry page.
- Root `index.md` must link to `sources/<collection>/summary.md`, not to raw source files.

## Workflow

1. Choose the collection name.
   Use a short `kebab-case` slug that names the source collection clearly.

2. Route the material to the right source type.
   Read the matching file under `types/` before ingesting the source.

3. Create the collection layout.
   Create `sources/<collection>/source/` and place the source artifacts there.

4. Create `sources/<collection>/summary.md`.
   This is the only source-collection entry page.

5. Update root `index.md`.
   Add one entry that links to `[[sources/<collection>/summary|<collection>]]` and briefly explains what the collection is.

6. Run lint.
   Always run `uv run python scripts/lint.py` before commit.

7. Commit the ingest.
   The repo requires a Conventional Commit after each logical update.

## Type Routing

- `webpage`: a webpage or browser-rendered page. Read `types/webpage.md`.
- `short-text`: standalone pasted text with no stable webpage, PDF, or email original. Read `types/short-text.md`.
- `paper-pdf`: a research paper, preprint, proceedings paper, or other paper-like academic PDF. Read `types/paper-pdf.md`.
- `book-pdf`: a book, monograph, or other book-length PDF. Read `types/book-pdf.md`.
- `pdf`: other PDF-first source material such as reports, manuals, or slide decks. Read `types/pdf.md`.
- `ai-daily-news`: one issue from the Daily AI Newsletter mail workflow. Read `types/ai-daily-news.md`.
- `ai-weekly-news`: one issue from the AI Agents Weekly mail workflow. Read `types/ai-weekly-news.md`.

If the material is only an excerpt from a known webpage, PDF, or email, do not use `short-text`. Route it to the underlying source type instead.

## `summary.md` Requirements

`sources/<collection>/summary.md` must include this frontmatter:

```md
---
type: summary
status: draft
created: 2026-04-20
updated: 2026-04-20
---
```

It must contain these sections:

- `## Structure`
- `## How To Use`
- `## Summary`
- `## Sources`

Recommended shape:

```md
---
type: summary
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <collection>

One short opening paragraph describing what this source collection contains.

## Structure

- `source/<file>`: what it is
- `summary.md`: the collection summary and usage guide

## How To Use

- how to read the source collection
- which raw file to start with
- how this collection should be used in the wiki

## Summary

A compact summary of the source collection's main content.

## Sources

- [[source/<file>|<display-name>]]
```

Inside `sources/<collection>/summary.md`, source links should point to files under the local `source/` subtree.

In root `index.md`, only link the collection summary page, for example:

```md
- [[sources/obsidian-cli/summary|obsidian-cli]]: summary page for the `sources/obsidian-cli/` collection
```

Do not link `sources/<collection>/source/...` from root `index.md`.

## Validation

Before committing:

```bash
uv run python scripts/lint.py
```

Useful extra check:

```bash
uv run python scripts/lint.py --list-rules
```

If lint fails, fix the reported rule violation before committing. The linter output maps each failure back to the corresponding `AGENTS.md` rule and gives a concrete next step.

## Commit Format

After a successful ingest, create one commit for the logical update.

Use a Conventional Commit such as:

```text
docs(source/<collection>): ingest source collection
```

If the change is mostly structural or repo-wide rather than content ingest, use the scope that best matches [AGENTS.md](/Users/bytedance/Documents/knowledge-base/AGENTS.md:1).

## Do Not Do

- Do not create `sources/<collection>/index.md`.
- Do not place source artifacts at the collection root.
- Do not put interpretation into files under `source/`.
- Do not skip `summary.md`.
- Do not skip `index.md` when introducing a new collection.
- Do not commit before `uv run python scripts/lint.py` passes.
