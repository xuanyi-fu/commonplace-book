# Newsletter Worker Task

Read this file before scoring any newsletter item.

You are a worker subagent for the `read-newsletter` skill. Your job is to score assigned newsletter items against the current knowledge-base index. You do not produce the final user-facing checklist.

## Inputs

You will receive:

- `worker_id`
- one or more newsletter items
- a concrete `Current Source Exclusion` block naming entries that must not count as matches
- for each item:
  - `item_id`
  - title
  - section path
  - full item text
  - links or image references if present

Use root `index.md` as the primary map of existing knowledge entries. If a match is ambiguous, use narrow search over wiki-layer pages to confirm it. Do not edit files.

The current newsletter source is never an eligible match. The main agent must pass a concrete block like:

```text
Current Source Exclusion:
- sources/<collection>/summary.md
- sources/<collection>/source/**
```

For a standalone markdown file outside `sources/`, the block contains that exact file path.

If the assignment does not include a concrete `Current Source Exclusion` block, do not score items. Return only:

```md
## Worker Result: <worker-id>

Missing Current Source Exclusion. Cannot score assigned items.
```

## Rubrics

### Index Connection

Score the number of distinct eligible existing wiki entries matched by the item.

```text
0 = no existing wiki entry matched
1 = 1 existing wiki entry matched
2 = 2 existing wiki entries matched
3 = 3 or more existing wiki entries matched
min = 1
```

### Relation Coverage

Score the number of distinct eligible matched entries for which you can explain one allowed relation.

```text
0 = no matched entry has an explainable relation
1 = at least 1 matched entry has an explainable relation
2 = at least 2 matched entries have explainable relations
3 = 3 or more matched entries have explainable relations
min = 1
```

`Possibly Interesting` is `yes` only when:

```text
Index Connection >= 1
and Relation Coverage >= 1
```

## Relation Labels

Use only these labels:

- `repeat`: the item repeats a fact or judgment already present in an existing page.
- `support`: the item adds evidence, an example, or a citation for an existing judgment.
- `extend`: the item connects an existing theme to a new object, scenario, or implementation.
- `challenge`: the item may require revising an existing page's judgment, boundary, or wording.

An item can have multiple matched relations. Do not force a single global relation for the whole item.

## Matching Rules

- Prefer existing entries from root `index.md`.
- Ignore every entry in the `Current Source Exclusion` block, even if it appears in `index.md` or is an obvious keyword match.
- A weak keyword overlap is not enough; there must be an explainable relation.
- If a page exists but the item only shares a generic term with it, do not count it.
- Do not verify newsletter claims against primary sources.
- Do not add a value judgment such as "high value" or "low value"; just report the relation.
- Keep each `why` sentence short and concrete.
- Pick one `Most Relevant Entry` from the matched relations for the main agent's final comment.
- For `Original Paragraph`, copy the most relevant original paragraph or shortest faithful excerpt from the assigned item text; do not paraphrase it.
- For `Comment`, write one concise sentence that explains why the original paragraph may interest the user through the `Most Relevant Entry`.

## Output Structure

Return fixed Markdown, not JSON.

Use exactly this structure:

```md
## Worker Result: <worker-id>

Current Source Exclusion:
- <excluded path or glob>

### Item: <item-id>
Title: <title>
Section: <section path>
Index Connection: <0-3> / min 1
Relation Coverage: <0-3> / min 1
Possibly Interesting: yes|no

Matched Relations:
- <wiki entry> | <repeat|support|extend|challenge> | <one sentence why>

Most Relevant Entry:
<single wiki entry, or "none">

Original Paragraph:
<one relevant original paragraph or short excerpt from the newsletter item, or "none">

Comment:
<one concise sentence, or "No clear connection to the current index.">
```

Constraints:

- Copy the received `Current Source Exclusion` block exactly once under `## Worker Result`.
- Emit one `### Item:` block for every assigned item.
- `Index Connection` must equal the count of distinct eligible matched wiki entries, capped at 3.
- `Relation Coverage` must equal the count of distinct eligible matched entries with an explainable relation, capped at 3.
- If there are no matched relations, write exactly `- none`.
- `Most Relevant Entry` must name only one wiki entry, even when multiple entries matched.
- `Original Paragraph` must come from the item text and should be the shortest relevant original paragraph or excerpt that supports the comment.
- `Comment` must be exactly one sentence and should mention only the `Most Relevant Entry`.
- Do not output a global ranking.
- Do not output final `可能关注` / `暂不关注` groups.
