---
name: read-newsletter
description: Use this skill when reading, pre-reading, triaging, or screening an AI daily/weekly newsletter issue with the user. It first partitions newsletter items into likely-interesting and not-currently-interesting groups by comparing each item against the current knowledge-base index, then gives the user a concise source-order checklist. Use for AI Agents Weekly, Daily AI Newsletter, and similar already-ingested newsletter source collections; do not use for single-article source-span reading, where the read skill is a better fit.
---

# Read Newsletter

Use this skill to screen a daily or weekly AI newsletter before live discussion.

This skill is repo-specific and must follow [AGENTS.md](/Users/bytedance/Documents/knowledge-base/AGENTS.md:1).

## Purpose

- Partition all newsletter items into:
  - `可能关注`
  - `暂不关注`
- Keep both groups in the newsletter's original order.
- Give the user one concise sentence per `可能关注` item explaining why it connects to the current knowledge base.
- Do not create reading notes, update wiki pages, verify the newsletter's claims, or chase primary sources unless the user separately asks.

## Accepted Inputs

The user can anchor the workflow with either:

- a source collection slug, such as `ai-agent-weekly-2026-04-25`
- a path to `sources/<collection>/summary.md`
- a path to a cleaned newsletter markdown file

If multiple inputs are present, prefer the explicit file path.

## Main Workflow

1. Resolve the newsletter issue.
   - If given a collection slug or summary page, read `sources/<collection>/summary.md`.
   - Choose the cleaned markdown issue snapshot named or implied by the summary.
   - Do not use `In today's issue` as item content; it is a table of contents.
2. Extract newsletter items in source order.
   - Under `## Top Stories`, each `###` heading is one item.
   - Under `## Top Picks`, each `####` heading is one item when the issue uses heading-form items.
   - Under `## Top Picks`, each top-level bullet with a linked title is one item when the issue uses bullet-form items.
   - Preserve each item's title, section path, full item text, links, and local image references if present.
3. Read root `index.md` as the primary map of existing knowledge entries.
   - Use index entries as the main matching surface.
   - If a possible match is unclear, use narrow search over wiki-layer markdown pages to confirm the relationship.
   - Do not treat raw newsletter source text as a stable wiki judgment.
4. Split items into worker batches.
   - Start 6 worker subagents for normal newsletter issues.
   - If there are fewer than 6 items, start only non-empty worker batches.
   - Assign every item to exactly one worker.
   - Give every worker the path `.agents/skills/read-newsletter/references/worker-task.md` and require it to read that file before scoring items.
5. Merge worker outputs.
   - Worker output is fixed-structure Markdown, not JSON.
   - Merge by item id and original newsletter order.
   - `possibly_interesting = yes` only when both rubric scores meet their minimums.
6. Present the result.
   - `可能关注`: one bullet per item, one sentence each, naming the knowledge-base relation.
   - `暂不关注`: list item titles only unless a short note is needed to explain no clear index connection.
   - Do not rank items inside either group.

## Rubrics

Use exactly these two rubrics.

### Index Connection

```text
0 = no existing wiki entry matched
1 = 1 existing wiki entry matched
2 = 2 existing wiki entries matched
3 = 3 or more existing wiki entries matched
min = 1
```

### Relation Coverage

```text
0 = no matched entry has an explainable relation
1 = at least 1 matched entry has an explainable relation
2 = at least 2 matched entries have explainable relations
3 = 3 or more matched entries have explainable relations
min = 1
```

Allowed relation labels:

- `repeat`: the item repeats a fact or judgment already present in an existing page.
- `support`: the item adds evidence, an example, or a citation for an existing judgment.
- `extend`: the item connects an existing theme to a new object, scenario, or implementation.
- `challenge`: the item may require revising an existing page's judgment, boundary, or wording.

## Worker Prompt Requirements

For each worker, include:

- the worker id
- the assigned item ids, titles, section paths, and full item text
- the relevant `index.md` entries or a clear instruction to read `index.md`
- this required instruction:

```text
Before analyzing items, read .agents/skills/read-newsletter/references/worker-task.md and follow its output structure exactly.
```

Workers must not edit files and must not decide the final user-facing grouping.

## Final User Output

Use this shape:

```md
## 可能关注

- <Item title>: <one sentence explaining why this item connects to the user's current knowledge base>.

## 暂不关注

- <Item title>
```

Keep the result concise. If the user wants to discuss, start from the first `可能关注` item in newsletter order and wait for `下一话题` before advancing.
