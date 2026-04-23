---
name: read
description: Use this skill when reading an already-ingested source collection in this knowledge-base repo source span by source span. It creates or resumes a canonical note at `notes/<collection>-reading-note.md`, starts by identifying the source's single Core Question, uses a semantic cursor as the reading state, quotes the current source span before explaining it, requires the user to recite each span in their own words before advancing, and keeps candidate concept/entity and related-page lists without auto-creating wiki pages.
---

# Read

Use this skill when the task is to read one already-saved source collection in this repository with the user, in source order, one source span at a time.

This skill is repo-specific and must follow [AGENTS.md](/Users/bytedance/Documents/knowledge-base/AGENTS.md:1).

## Shared Contract

- Source collections stay in the existing shape:

```text
sources/
  <collection-kebab-case>/
    summary.md
    source/
      ...
```

- Reading notes do not live inside `sources/<collection>/`.
- The canonical note path is:

```text
notes/<collection>-reading-note.md
```

- There is exactly one canonical reading note per source collection.
- If the canonical note already exists, resume it instead of creating a second note.
- When the note is first created, add a root `index.md` entry that points to the note page.
- Cleaned markdown source notes under `sources/*/source/*.md` may receive minimal `^block-id` anchors when precise reusable citations are needed.
- Raw source artifacts must remain read-only. Do not add block ids to PDF, HTML, screenshots, exported mail, or other non-markdown raw artifacts.
- Do not create `concept`, `entity`, or `synthesis` pages from this skill. This skill only produces or updates the canonical reading note.

## Accepted Inputs

The user can anchor the reading workflow with either of:

- a collection slug such as `transformer-moe-2026-04`
- a path to `sources/<collection>/summary.md`

If both are present, trust the explicit path.

## First Run vs Resume

1. Resolve the collection slug and the note path `notes/<collection>-reading-note.md`.
2. Read `sources/<collection>/summary.md` first.
3. Choose the primary reading file.
   Prefer the user-named file if they gave one. Otherwise choose the best "start here" file from the collection summary's guidance.
4. If the note does not exist:
   - create it with the exact section layout below
   - initialize `## Core Question`
   - initialize `## Reading State` with the semantic cursor fields below
   - add the note to root `index.md`
5. If the note already exists:
   - read `## Reading State`
   - resume from the semantic cursor recorded there
   - if the note has no semantic cursor yet, derive one from the existing reading state and any legacy `## Section Queue`; use that legacy queue only as a recovery hint and migrate the note to the semantic cursor shape on the next note update
   - preserve the existing note content and append updates

## Canonical Note Layout

The note must use this exact section set:

```md
---
type: note
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <collection>-reading-note

## Source

## Core Question

## Reading State

## Recall Log

## Questions And Answers

## Reader Comments

## Candidate Concepts Entities

## Candidate Related Pages

## Sources
```

Recommended content for each section:

- `## Source`
  - source collection link
  - primary reading file
  - discussion language
- `## Core Question`
  - one sentence naming the main question the whole source is trying to answer
  - supporting source citation
- `## Reading State`
  - source slug
  - primary reading file
  - semantic cursor:
    - file
    - semantic position, such as `under "# H1", before "## H2"` or `under "## X", before "### Y"`
    - next unread source span
    - next boundary
    - completed spans
  - scout status
- `## Recall Log`
  - source span label
  - quoted original span or citation to it
  - guiding question
  - user recitation
  - calibrated understanding
  - missing points
  - open questions
- `## Questions And Answers`
  - user question
  - answer
  - supporting citation
- `## Reader Comments`
  - user comment
  - cited supporting passage
- `## Candidate Concepts Entities`
  - term
  - why it matters
  - existing page?
  - confidence
- `## Candidate Related Pages`
  - page
  - relation: `supports` / `contradicts` / `extends`
  - rationale
  - confidence
- `## Sources`
  - source collection summary
  - primary reading file
  - any cleaned markdown source notes used for precise citations

## Core Question Kickoff

Before source-span reading, always give exactly one `Core Question`: the main question the whole source is trying to answer.

Keep it to one sentence. Prefer a broad citation to `sources/<collection>/summary.md`, unless one cleaned markdown source note clearly supports the question more precisely.

## Semantic Cursor

The `semantic cursor` is the single source of truth for reading progress.

- Do not infer progress from headings, recall logs, or legacy queues.
- Line numbers may be recorded as convenience hints, but they must not replace the semantic position.
- The semantic position must say where the cursor sits in the document structure, such as `under "# H1", before "## H2"`.
- A source span is a contiguous unread semantic passage from the cursor: the smallest block that completes one local argumentative or rhetorical move and can be answered by one guiding question.
- Do not split a span mechanically by sentence or paragraph boundaries. Sentences and paragraphs are only physical boundaries; the decision boundary is the source's local argumentative function.
- A span may be a paragraph group, continuous list item group, table, code block, or heading-intro block when that whole block performs one local function such as framing, motivation, overview, definition, or evidence.
- Headings only describe cursor position and boundaries. They are not the reading unit.
- Body text between a heading and its first child heading must be read as a semantic span when it jointly performs one local function. For example, an opening block after `# H1` and before `## H2` that frames the article's scope should be read as one span, not as isolated sentences.
- If a candidate span is too long or contains multiple unrelated moves, split it into smaller contiguous semantic spans instead of reading the whole heading scope at once.

## SQ3R Loop

The reading loop is always:

1. `Survey`
2. `Question`
3. `Read`
4. `Recite`
5. `Review`

### 1. Survey

- Locate the next unread source span from the semantic cursor.
- Start the user-facing reply with a `Current Source Span` block that quotes the full original span before any guiding question or explanation.
- The quoted text must match the semantic cursor, the guiding question, and the explanation scope. Do not quote only one sentence as a proxy for a larger span.
- If splitting a long passage for length, state the selected span boundary and ensure the split still forms one complete local argumentative move.
- Preserve the original language and core source terms in the quoted span.
- Lock to the current source span only.
- Restate the semantic position before explaining.
- Do not pull in later spans early unless a tiny amount of future context is strictly required to make the current span intelligible; if used, label it as inference/context.

### 2. Question

Derive exactly one `guiding question` for the current source span.

- The guiding question must cover the whole span, not only its first sentence.
- If one guiding question cannot cover the candidate span without becoming vague or mixing unrelated targets, the candidate span is too broad; split it by semantic move before reading.

Do not free-form brainstorm. Use rule-based rewrite:

1. Classify the source span as one of:
   - `definition`
   - `motivation`
   - `mechanism`
   - `comparison`
   - `evidence/result`
   - `limitation/tradeoff`
   - `history`
2. Apply the matching template:
   - `definition`: `X 在这里具体指什么？`
   - `motivation`: `作者为什么要引入 X？它要解决什么问题？`
   - `mechanism`: `X 是怎么工作的？输入、步骤、输出分别是什么？`
   - `comparison`: `X 和 Y 有什么关键区别？为什么这个区别重要？`
   - `evidence/result`: `这一段给了什么证据？这些证据支持了什么结论？`
   - `limitation/tradeoff`: `X 的代价、边界或失败模式是什么？`
   - `history`: `从 A 到 B 发生了什么变化？为什么会这样变？`
3. Keep original source terms whenever translation would blur meaning.

Fallback only when the source span is too vague:

- `这一段在整篇论证里起什么作用？`
- `作者在这一段真正想让读者明白什么？`

The `guiding question` is the acceptance target for the source span. It is not decorative.

### 3. Read

- Explain only what is needed to answer the guiding question.
- Stay anchored to the current source span and the user's current confusion point.
- Separate documented source facts from your own inference.
- Keep the explanation compact enough that the user can realistically restate it.

### 4. Recite

The user must answer the guiding question in their own words before the assistant may advance.

Rules:

- Do not advance automatically after your explanation.
- Ask the user to restate the source span in their own words.
- Accept short prose or a few bullets.
- If the user asks a clarification question instead of reciting, answer the clarification and then return to the recite gate.

### 5. Review

After the user recites:

- confirm what is correct
- fix what is off
- add any missing constraint that matters
- write the result into `## Recall Log`
- advance the semantic cursor to the next unread source span

Only after the note is updated and the user explicitly says `继续`, `下一段`, `下一节`, or equivalent may you move to the next source span.

## Strict Advancement Policy

- Never proactively say "let's move to the next source span" and then move on by yourself.
- Never treat one `继续` as permission to skip multiple spans.
- Each continuation only unlocks the next semantic source span.
- Do not skip unheaded body text.
- Do not cross the cursor's `next boundary` while explaining the current span.

## Background Scouts

If the current turn allows subagents and the user wants the full reading workflow, start two quiet background scouts automatically at session start:

- `concept/entity scout`
- `related-pages scout`

If subagents are unavailable in the current turn, keep these candidate lists locally in the canonical note and continue the workflow without blocking.

### Shared Scout Rules

- Scouts must never interrupt the main explanation.
- Scouts only update candidate lists in the canonical note.
- Scouts must never create `concept`, `entity`, or `synthesis` pages automatically.

### `concept/entity scout`

Refresh:

- at session start
- after every source span that passes the recite gate and has its review written into the note

Threshold:

- the concept/entity is central to the source's argument
- it is reusable beyond this one source
- the knowledge base either has no page for it or the existing page is materially underdeveloped

### `related-pages scout`

Refresh:

- at session start
- after completion of a top-level heading scope
- after the current source span review if a strong signal appeared in that span

Top-level heading scope means the first heading tier below the source title in the active source file.

Strong signal means any of:

- a new source-backed strong claim added to the note
- a new user comment tied to a cited passage
- a new `^block-id` added to a cleaned markdown source note
- a novel user question that clearly generalizes beyond the current span's surface wording

Coalesce scout refreshes to the source span `Review` boundary. Never refresh in the middle of active explanation.

Relation threshold:

- only `supports`, `contradicts`, or `extends`
- start from root `index.md`
- read candidate pages only when needed to verify the relation
- do not add loose "same topic" links

## Citation Policy

- In reading notes, cite non-trivial factual claims.
- Each active reading reply must quote the current original source span before explaining it.
- Prefer `[[...#^block-id]]` when one specific passage supports a reusable claim.
- Prefer cleaned markdown source notes under `sources/*/source/*.md` for block-id citations.
- If a cleaned markdown note lacks a needed block id, add the minimal stable readable `^block-id` to the supporting passage.
- Do not add block ids mechanically to every paragraph.
- If the only available artifact is raw HTML/PDF/image/email, keep it read-only and fall back to a whole-document citation or the collection summary, plus a note-local TODO if precision should be improved later.

## Do Not Do

- Do not create a second reading note for the same source collection.
- Do not place reading notes under `sources/<collection>/`.
- Do not advance to the next source span before the user recites and explicitly continues.
- Do not let background scouts dominate the session.
- Do not mutate raw source artifacts.
- Do not auto-create downstream wiki pages from candidate lists.
