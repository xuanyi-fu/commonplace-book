---
type: synthesis
status: draft
created: 2026-04-23
updated: 2026-04-23
---

# Codex context 是有序 input stream

这页记录 Codex model context 的正确模型：`instructions` 和 `tools` 是 request 顶层字段；真正的 conversation material 进入一个有顺序的 `input` stream，developer-role items、user-role context items、普通 user message、assistant message、tool call/output、reasoning、compaction item、后续 context diff 都会按 turn 生命周期追加进去。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

## 核心判断

Codex 的 top-level `instructions` 是一个被选中的 base-instruction string，不是所有 instruction 来源的总拼接。`tools` 是另一个顶层字段，承载当前模型可见的 tool schemas。`AGENTS.md`、environment context、skills、plugins、memory guidance、collaboration mode、hooks 等材料多数作为 `input` 中的 developer-role message 或 user-role context message 注入，而不是拼到 top-level `instructions` 里。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

关键是保留 item 的相对顺序。真实顺序更像一个 append-only stream：每一轮开始时，Codex 先按需要记录 context update，再记录当前 user prompt，再记录 hook-added developer contexts、显式 skill/plugin 注入、pending input 等，然后从更新后的 history 克隆出本轮要采样的 prompt input。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]

## 正确模型

正确画法是把 request 分成顶层字段和有序 `input`。OpenAI blog 还补了一层边界：Responses API server 会把 request 派生成最终 prompt，server 决定 prompt 前几个 server-side items 的顺序；`tools` 和 `instructions` 的内容由 client 决定，随后接上 client 提供的 `input`。[[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

```text
top-level request fields:
  instructions = selected base instructions
  tools        = current tool schemas

server-derived prompt prefix:
  server-side system/tool/instruction framing

client-provided ordered input stream:
  developer message: initial permissions / developer context / skill metadata in d62421d
  user message: user instructions / AGENTS.md
  user message: environment context
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
- `skills` 至少有两层：在 `openai/codex@d62421d` 的 `codex-core` 里，available skills metadata 进入 developer-role `<skills_instructions>` bundle；显式提到的 full `SKILL.md` body 作为 per-turn user-role `<skill>...</skill>` fragment 注入。OpenAI blog 的 2026-01 Codex CLI 描述把 skill metadata 放在 user instructions 下面，这一点对 `d62421d` 已经过时。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]
- `reasoning`、tool calls、tool outputs、compaction item 都可能成为 history / subsequent input 的一部分；history 不只是 user/assistant 两类自然语言消息。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

## Blog 校准

OpenAI 的 `Unrolling the Codex agent loop` blog 支持这页的主结论：`instructions`、`tools`、`input` 是 Responses API request 的不同字段，`input` 是 item list；模型返回的 reasoning / function_call item 和 tool output 会进入后续请求的 `input`，旧 prompt 成为新 prompt 的 exact prefix；mid-conversation configuration changes 会优先通过追加新 message 来表达，而不是回改旧 message。[[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

这篇 blog 不能覆盖 `openai/codex@d62421d` 的细节。它描述的 2026-01 Codex CLI 初始 `input` 是：role=`developer` permissions message、可选 role=`developer` `developer_instructions`、可选 role=`user` user instructions / skill metadata、role=`user` environment context，然后才追加真实 user message。到 `d62421d`，代码阅读证据显示 skills guidance 已经进入 developer bundle；因此 blog 在 `skills metadata` 的 role/分组上应视为历史描述。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

因此这页的稳定结论是 ordered `input` stream 和 append-on-change 策略；对当前收录的 `d62421d` 代码阅读来说，`skills metadata` 的具体位置也可以更精确地写成 developer-role bundle。

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

这个例子是 Codex desktop 本机 rollout 的实际形态，不是 OpenAI blog 里 Codex CLI 初始 prompt 的规范形态。它给出显式 skill body 的实际位置：`ingest-source` 的 full `SKILL.md` body 跟在当前真实 user prompt 之后，作为新的 user-role `response_item` 被追加进 stream。

## 本机例子二：environment diff 插在中间

另一个展示 `context diff` 实际位置的例子来自一个旧 thread：

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

这里第 529 行的 `<environment_context>` 是一个日期变化后的 user-role contextual item。它出现在已经存在的 user/assistant history 后面，又出现在下一条真实 user message 前面。因此这个 diff 的模型位置是 conversation stream 中的一个新 item。

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
        "optional developer_instructions...",
        "<skills_instructions>available skill metadata...</skills_instructions>"
      ]
    },
    {
      "role": "user",
      "content": "# AGENTS.md instructions for /repo\n<INSTRUCTIONS>...</INSTRUCTIONS>"
    },
    {
      "role": "user",
      "content": "<environment_context>...</environment_context>"
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

Codex 的 model context 可以理解为：`instructions` 和 `tools` 是 request 顶层控制面；`input` 是一个按时间和 turn 生命周期维护的有序 item stream，context update 和 diff 本身也是 stream 里的 item。OpenAI blog 提供了 agent-loop 和 Responses API 层面的背景；`openai/codex@d62421d` 的具体 role 分组则以本地代码阅读为准。[[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]] [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop]]

## Sources

- [[sources/codex-model-context-inputs-2026-04/summary|codex-model-context-inputs-2026-04]]
- [[sources/codex-model-context-inputs-2026-04/source/model-context-inputs-github-links|model-context-inputs-github-links]]
- [[sources/openai-codex-agent-loop-2026-01/summary|openai-codex-agent-loop-2026-01]]
- [[sources/openai-codex-agent-loop-2026-01/source/unrolling-the-codex-agent-loop-markdown|unrolling-the-codex-agent-loop-markdown]]
- Local rollout observation: `/Users/bytedance/.codex/sessions/2026/04/23/rollout-2026-04-23T21-51-57-019dbdd4-8e9c-7a13-a721-47a8afb7849c.jsonl`
- Local rollout observation: `/Users/bytedance/.codex/sessions/2026/04/18/rollout-2026-04-18T22-51-31-019da44b-4d53-76a2-975c-c790f9d3c904.jsonl`
