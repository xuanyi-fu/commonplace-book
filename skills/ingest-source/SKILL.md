---
name: ingest-source
description: Use this skill when adding a new source collection to this knowledge-base wiki. It explains how to normalize the collection name, place raw files under sources/<collection>/source/, write sources/<collection>/summary.md, update index.md, run uv run python scripts/lint.py, and commit the ingest in the repository's required format.
---

# Ingest Source

Use this skill when the task is to add a new source collection to this repository.

This skill is specific to the current repo layout and must follow [AGENTS.md](/Users/bytedance/Documents/knowledge-base/AGENTS.md:1).

## Target Layout

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
- All raw source files must live under `sources/<collection>/source/**`.
- Never place raw files directly under `sources/<collection>/`.
- Root `index.md` must link to `sources/<collection>/summary.md`, not to raw source files.

## Ingest Workflow

1. Choose the collection name.
   Use a short `kebab-case` slug that names the source collection clearly.

2. Create the collection layout.
   Create `sources/<collection>/source/` and place all raw source files there.

3. Preserve raw source as raw source.
   Do not rewrite, summarize, or restructure files under `source/` unless the task is explicitly to clean an imported snapshot.

4. Create `sources/<collection>/summary.md`.
   This is the only source-collection entry page.

5. Update root `index.md`.
   Add one entry that links to `[[sources/<collection>/summary|<collection>]]` and briefly explains what the collection is.

6. Run lint.
   Always run `uv run python scripts/lint.py` before commit.

7. Commit the ingest.
   The repo requires a Conventional Commit after each logical update.

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

## Source Links

Inside `sources/<collection>/summary.md`, source links should point to files under the local `source/` subtree, for example:

```md
- [[source/gist|gist.md]]
- [[source/official-help-cli|official-help-cli.md]]
```

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
- Do not put raw files at collection root.
- Do not skip `summary.md`.
- Do not skip `index.md` when introducing a new collection.
- Do not commit before `uv run python scripts/lint.py` passes.
