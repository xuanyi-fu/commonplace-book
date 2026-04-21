# AGENTS

Supplementary rule documents live in `rules/`.

## Scope

These rules apply to wiki-layer pages in:

- `summaries/`
- `entities/`
- `concepts/`
- `syntheses/`
- `sources/*/summary.md`
- root `index.md`

Raw source files under `sources/*/source/**` should remain read-only.

`sources/` rules:

- Everything directly under `sources/` must be a folder.
- Each `sources/<collection>/` folder must use `kebab-case`.
- Each `sources/<collection>/` folder must contain exactly:
  - `summary.md`
  - `source/`
- No raw source file may live directly under `sources/<collection>/`.
- Every raw source file must live under `sources/<collection>/source/**`.
- Git LFS tracks every file under `sources/<collection>/source/**`.
- Each `sources/<collection>/summary.md` must include:
  - `## Structure`
  - `## How To Use`
  - `## Summary`
  - `## Sources`
- When a source file is cleaned or normalized from another format, preserve inline citations, footnote markers, and inline links from the original whenever practical so readers can jump back to referenced material.
- That page must clearly cover:
  - what the source collection mainly contains
  - how the collection is structured
  - how the collection should be used

## Frontmatter

Every wiki page must start with this exact four-field frontmatter, in this exact order:

```md
---
type: concept
status: draft
created: 2026-04-20
updated: 2026-04-20
---
```

Rules:

- Only `type`, `status`, `created`, `updated` are allowed.
- No extra frontmatter fields.
- Dates must use `YYYY-MM-DD`.
- `updated` must not be earlier than `created`.
- `created` is the original page creation date.
- `updated` must change after each substantive edit.

Allowed `type` values:

- `source`
- `summary`
- `entity`
- `concept`
- `synthesis`
- `index`

Allowed `status` values:

- `draft`
- `stable`

## Page Content

- Page title is the H1, not a frontmatter field.
- Sources are listed in a `## Sources` section.
- Tags are written directly in the body, not in frontmatter.
- A source collection summary page is `sources/<collection>/summary.md`.
- Use the same language as the discussion when recording wiki content, unless the user explicitly asks for a different language.

## Links

- Use Obsidian wikilinks for internal links: `[[target-page]]`
- Use alias syntax when needed: `[[target-page|display text]]`
- Use block ids only for precise reusable references: `^block-id`

## File Naming

- Use `kebab-case` only.
- Allowed characters: lowercase letters, numbers, `-`.
- Do not use spaces, `_`, camelCase, or Chinese filenames.
- Filenames must be short and semantic.
- `summary` filenames must express both the summary target and the summary intent.
- Source collection summary pages are always named `summary.md`.

Examples:

- `andrej-llm-wiki-summary.md`
- `obsidian-cli-help-overview.md`
- `obsidian-search-cli-comparison.md`

## Index

`index.md` rules:

- Root `index.md` is the global index.
- Index pages only answer "what exists".
- Each entry should be a page link plus a one-line description.
- Root `index.md` must not index raw source files under `sources/**/source/**` directly.
- Source collections should be surfaced through `sources/<collection>/summary.md`.

## Git History

- Git history is the only change history. Do not use `log.md`.
- The deterministic subset of these rules is enforced by `scripts/lint.py`.
- Every logical update must run `uv run python scripts/lint.py` before commit.
- Commits must only be created from a passing `uv run python scripts/lint.py` run.
- Every logical update must end with one git commit.
- Commit format is:

```md
<type>(<scope>): <subject>
```

Allowed `type` values:

- `docs`
- `chore`
- `refactor`

Recommended `scope` values:

- `repo`
- `rules`
- `index`
- `source/<collection>`
- `summary/<name>`
- `entity/<name>`
- `concept/<name>`
- `synthesis/<name>`
- `structure`

`subject` rules:

- use lowercase english
- start with a verb
- keep it short
- do not end with a period

Examples:

- `chore(repo): initialize git repository`
- `docs(source/obsidian-cli): add official cli snapshots`
- `docs(summary/obsidian-cli): summarize source collection`
- `chore(rules): update source collection rules`
