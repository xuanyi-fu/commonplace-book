# AGENTS

Supplementary rule documents live in `rules/`.

## Scope

These rules apply to wiki-layer pages in:

- `summaries/`
- `notes/`
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
- When an original raw source is available, preserve that raw source in `sources/<collection>/source/**` whenever practical, preferably in its native format such as PDF, HTML, exported email, or image capture.
- A cleaned markdown source note may accompany a raw source, but should not replace the raw source when the raw source can be preserved.
- That page must clearly cover:
  - what the source collection mainly contains
  - how the collection is structured
  - how the collection should be used

`notes/` rules:

- Canonical source reading notes live under `notes/`.
- Canonical source reading notes use the path shape `notes/<collection>-reading-note.md`.
- Reading notes may add minimal `^block-id` anchors to cleaned markdown source notes under `sources/*/source/*.md` when precise reusable citations are needed.
- Reading notes must not add `^block-id` anchors to raw source artifacts such as PDF, HTML, screenshots, or exported email.

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
- `note`
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
- A canonical source reading note page is `notes/<collection>-reading-note.md`.
- Use the same language as the discussion when recording wiki content, unless the user explicitly asks for a different language.
- When discussing implementations in Chinese, keep core implementation terms like `thread`, `raw memory`, `context`, `prompt`, and `agent` in their original form when translating them would blur the structure of the system; translate the surrounding explanation instead.

## Citation

- In wiki-layer pages, every non-trivial factual claim derived from a local source note should cite the supporting source note.
- `## Sources` lists which sources the page uses overall; it does not replace inline citations for specific claims.
- Whole-document citations are acceptable when the claim is supported broadly across the cited page.
- When a claim depends on one specific passage and that passage is likely to be reused, add a block id to the source note passage and cite it via `[[path/to/page#^block-id]]`.
- In this repo, paragraph-level reusable citations should be implemented with block ids.
- Do not rely on a whole-page link when the claim is only supported by one specific passage and a block-id citation is practical.
- Do not add block ids mechanically to every paragraph.
- `AGENTS.md` defines the repo-wide citation contract; `rules/markdown-conventions.md` remains the syntax and example reference.

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
- `transformer-moe-2026-04-reading-note.md`

## Index

`index.md` rules:

- Root `index.md` is the global index.
- Index pages only answer "what exists".
- Each entry should be a page link plus a one-line description.
- Root `index.md` must not index raw source files under `sources/**/source/**` directly.
- Source collections should be surfaced through `sources/<collection>/summary.md`.
- Canonical reading notes under `notes/` should be surfaced through their note pages when they exist.

## Git History

- Git history is the only change history. Do not use `log.md`.
- This repository has a configured GitHub remote at `origin`.
- The deterministic subset of these rules is enforced by `scripts/lint.py`.
- Install the repo-managed commit-time checks with `uv run pre-commit install`.
- Run the full hook suite manually with `uv run pre-commit run --all-files`.
- Every logical update must run `uv run python scripts/lint.py` before commit.
- Commit-time checks run full-repo `scripts/lint.py` plus page-scoped `scripts/check_links.py` on staged wiki-layer markdown pages.
- Commits must only be created from a passing `uv run python scripts/lint.py` run.
- Every logical update must end with one git commit.
- After each commit, push the current branch to `origin` unless the user explicitly asks you not to push.
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
- `note/<name>`
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
- `docs(note/transformer-moe-2026-04): add canonical reading note`
- `chore(rules): update source collection rules`
