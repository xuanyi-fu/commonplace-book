---
type: synthesis
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# Codex context 是有序 input stream

这页记录一个关于 Codex model context 的修正：它不应该被画成“instructions / tools / developer instructions / contextual user instructions / history”几个静态层依次堆叠。更准确的模型是：`instructions` 和 `tools` 是 request 顶层字段；真正的 conversation material 进入一个有顺序的 `input` stream，developer-role items、contextual user fragments、普通 user message、assistant message、tool call/output、reasoning、compaction summary、后续 context diff 都会按 turn 生命周期追加进去。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]

## 核心判断

Codex 的 top-level `instructions` 是一个被选中的 base-instruction string，不是所有 instruction 来源的总拼接。`tools` 是另一个顶层字段，承载当前模型可见的 tool schemas。`AGENTS.md`、environment context、skills、plugins、memory guidance、collaboration mode、hooks 等材料多数作为 `input` 中的 developer-role message 或 user-role contextual fragments 注入，而不是拼到 top-level `instructions` 里。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]

所以最容易错的不是“少分了一类 context”，而是把这些类别画成了固定前置分区。真实顺序更像一个 append-only stream：每一轮开始时，Codex 先按需要记录 context update，再记录当前 user prompt，再记录 hook-added developer contexts、显式 skill/plugin 注入、pending input 等，然后从更新后的 history 克隆出本轮要采样的 prompt input。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]

## 不要这样画

下面这种图会误导，因为它暗示所有 context diff 都会在 history 之前统一加载：

```text
instructions
tools
developer instructions
contextual user instructions
history
  user
  assistant
  tool call
  tool output
  reasoning
```

它的问题是：后续 `environment_context` diff、collaboration-mode diff、model-switch instruction、hook prompt、显式 skill body 等，不是一个永远位于 history 前面的静态区块。它们会在具体 turn 的生命周期里，作为新的 `response_item` 插到已有 conversation stream 后面。

## 更好的模型

更好的画法是把 request 分成顶层字段和有序 `input`：

```text
top-level request fields:
  instructions = selected base instructions
  tools        = current tool schemas

ordered input stream:
  developer message: initial developer context bundle
  user message: initial AGENTS.md / environment context bundle
  user message: actual user prompt
  user message: explicit <skill>...</skill> body, if invoked
  reasoning item, if retained
  assistant message
  function_call
  function_call_output
  ...
  user message: later <environment_context> diff
  user message: later actual user prompt
  ...
```

这也解释了几个容易混淆的边界：

- `developer instructions` 不是等同于 top-level `instructions`；developer-role context bundle 是 `input` 里的 message。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]
- `contextual user fragments` 是 role=`user` 的 model-visible context item，但不是普通人类 user turn；普通 user-message parsing 会跳过这些 contextual user messages。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]
- `skills` 有两层：available skills metadata 进入 developer bundle；显式提到的 full `SKILL.md` body 作为 per-turn user-role `<skill>...</skill>` fragment 注入。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]
- `reasoning`、tool calls、tool outputs、compaction summary 都可能成为 history 的一部分；history 不只是 user/assistant 两类自然语言消息。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]

## 本机例子一：skill body 的位置

在本机当前 ingest 线程的 rollout 里，开头顺序是：

```text
/Users/bytedance/.codex/sessions/2026/04/23/rollout-2026-04-23T21-51-57-019dbdd4-8e9c-7a13-a721-47a8afb7849c.jsonl

1  session_meta.base_instructions = "You are Codex..."
3  response_item message developer = permissions / app-context / memory / collaboration / skills
4  response_item message user      = AGENTS.md + environment_context
6  response_item message user      = actual user prompt: ingest source request
8  response_item message user      = <skill> ingest-source ... </skill>
11 response_item reasoning
13 response_item message assistant
14 response_item function_call
19 response_item function_call_output
```

这个例子说明，显式调用的 `ingest-source` skill body 不是在所有 history 之前作为一个全局 instruction 预加载，而是在当前真实 user prompt 之后，作为新的 user-role `response_item` 被追加进 stream。

## 本机例子二：environment diff 插在中间

另一个更能说明“context diff 会穿插在 history 中间”的例子来自一个旧 thread：

```text
/Users/bytedance/.codex/sessions/2026/04/18/rollout-2026-04-18T22-51-31-019da44b-4d53-76a2-975c-c790f9d3c904.jsonl

520 user: 打赢了复活赛
525 assistant: 对，`tule elk` 这波确实算...
529 user: <environment_context>
       <shell>zsh</shell>
       <current_date>2026-04-19</current_date>
       <timezone>America/Los_Angeles</timezone>
     </environment_context>
531 user: 把他们的小故事也记录在另一个markdown吧
```

这里第 529 行的 `<environment_context>` 是一个日期变化后的 user-role contextual item。它出现在已经存在的 user/assistant history 后面，又出现在下一条真实 user message 前面。这就是为什么不能把 diff 画成“加载 history 之前的一整块 context”。

## 代表性伪 request

下面是一个顺序语义更接近真实情况的代表性伪例子。它不是原始 wire dump，而是把上面的代码阅读结论和本机 rollout 观察压成一个可读模型：

```jsonc
{
  "instructions": "You are Codex, a coding agent based on GPT-5...",
  "tools": [
    { "name": "exec_command", "schema": "..." },
    { "name": "apply_patch", "schema": "..." },
    { "name": "web.run", "schema": "..." }
  ],
  "input": [
    {
      "role": "developer",
      "content": [
        "<permissions instructions>...</permissions instructions>",
        "<app-context>...</app-context>",
        "<collaboration_mode>Default...</collaboration_mode>",
        "<skills_instructions>available skill metadata...</skills_instructions>"
      ]
    },
    {
      "role": "user",
      "content": "# AGENTS.md instructions for /repo\n<INSTRUCTIONS>...</INSTRUCTIONS>\n<environment_context>...</environment_context>"
    },
    {
      "role": "user",
      "content": "$ingest-source 帮我 ingest 这个文件..."
    },
    {
      "role": "user",
      "content": "<skill>\n<name>ingest-source</name>\n<path>.../SKILL.md</path>\n...full skill body...\n</skill>"
    },
    {
      "type": "reasoning",
      "summary": "retained reasoning item, if present"
    },
    {
      "role": "assistant",
      "content": "我会按 ingest-source 工作流处理..."
    },
    {
      "type": "function_call",
      "name": "exec_command",
      "arguments": { "cmd": "sed -n '1,160p' ..." }
    },
    {
      "type": "function_call_output",
      "output": "SKILL.md contents..."
    },
    {
      "role": "user",
      "content": "<environment_context>\n  <current_date>2026-04-24</current_date>\n</environment_context>"
    },
    {
      "role": "user",
      "content": "下一轮真实 user message..."
    }
  ]
}
```

## 一句话结论

Codex 的 model context 不应该理解成“几类 instruction 先拼好，再接完整 history”。更准确的理解是：`instructions` 和 `tools` 是 request 顶层控制面；`input` 是一个按时间和 turn 生命周期维护的有序 item stream，context update 和 diff 本身也是 stream 里的 item。这个顺序很重要，因为模型看到的不只是“有哪些内容”，还包括这些内容在 conversation history 里的相对位置。

## Sources

- [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- [[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]
- Local rollout observation: `/Users/bytedance/.codex/sessions/2026/04/23/rollout-2026-04-23T21-51-57-019dbdd4-8e9c-7a13-a721-47a8afb7849c.jsonl`
- Local rollout observation: `/Users/bytedance/.codex/sessions/2026/04/18/rollout-2026-04-18T22-51-31-019da44b-4d53-76a2-975c-c790f9d3c904.jsonl`
