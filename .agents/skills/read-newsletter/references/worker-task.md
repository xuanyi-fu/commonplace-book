# Newsletter Worker Task

Read this file before scoring any newsletter item.

You are a worker subagent for the `read-newsletter` skill. Your job is to score assigned newsletter items against the current knowledge-base index. You do not produce the final user-facing checklist.

## Inputs

You will receive:

- `worker_id`
- one or more newsletter items
- for each item:
  - `item_id`
  - title
  - section path
  - full item text
  - links or image references if present

Use root `index.md` as the primary map of existing knowledge entries. If a match is ambiguous, use narrow search over wiki-layer pages to confirm it. Do not edit files.

## Rubrics

### Index Connection

Score the number of distinct existing wiki entries matched by the item.

```text
0 = no existing wiki entry matched
1 = 1 existing wiki entry matched
2 = 2 existing wiki entries matched
3 = 3 or more existing wiki entries matched
min = 1
```

### Relation Coverage

Score the number of distinct matched entries for which you can explain one allowed relation.

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
- A weak keyword overlap is not enough; there must be an explainable relation.
- If a page exists but the item only shares a generic term with it, do not count it.
- Do not verify newsletter claims against primary sources.
- Do not add a value judgment such as "high value" or "low value"; just report the relation.
- Keep each `why` sentence short and concrete.

## Output Structure

Return fixed Markdown, not JSON.

Use exactly this structure:

```md
## Worker Result: <worker-id>

### Item: <item-id>
Title: <title>
Section: <section path>
Index Connection: <0-3> / min 1
Relation Coverage: <0-3> / min 1
Possibly Interesting: yes|no

Matched Relations:
- <wiki entry> | <repeat|support|extend|challenge> | <one sentence why>

One Sentence Reason:
<one sentence reason, or "No clear connection to the current index.">
```

Constraints:

- Emit one `### Item:` block for every assigned item.
- `Index Connection` must equal the count of distinct matched wiki entries, capped at 3.
- `Relation Coverage` must equal the count of distinct matched entries with an explainable relation, capped at 3.
- If there are no matched relations, write exactly `- none`.
- `One Sentence Reason` must be exactly one sentence.
- Do not output a global ranking.
- Do not output final `可能关注` / `暂不关注` groups.
