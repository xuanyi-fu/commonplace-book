---
type: synthesis
status: draft
created: 2026-05-01
updated: 2026-05-01
---

# OpenAI Responses WebSockets 的 40% 提升更像产品口径，不是干净 benchmark

OpenAI 这篇 WebSocket mode 文章里的 `40%`，最稳妥的读法不是“所有 Codex / agent task 的完整 wall-clock 都会减少 40%”，也不是“WebSocket 协议本身让 inference 快了 40%”。它更像一个产品 / 集成口径：在快模型、多轮短请求、API overhead 占比较高的 agentic workflow 里，WebSocket mode 这组改动能带来最高约 40% 的 observed latency improvement。原文用的是 `40% faster end-to-end` 和 alpha users reported `up to 40% improvements`，但没有给任务集、分位数、baseline 配置、耗时拆分或复现实验定义。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-40-percent-framing|40% faster end-to-end]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-alpha-40-percent|up to 40% improvements]]

## 它到底优化了什么

文章真正有证据支撑的机制是：Codex-style agent loop 会产生很多 back-and-forth Responses API requests；当 inference 变快后，API services 的 validation / request processing、conversation state 处理、client-side context building 等非 inference 开销会变得更显眼。OpenAI 说他们过去把每个 Codex request 当成 independent，follow-up request 仍要处理 conversation state 和 reusable context，即使大部分 conversation 没变，conversation 越长这个重复处理越贵。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-codex-loop|Codex loop]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-api-overhead-visible|API overhead visible]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-independent-request-structure|independent request structure]]

WebSocket mode 的关键不是单独替换 HTTP，而是把 familiar API shape 保留下来：继续用 `response.create`，再用 `previous_response_id` 从前一个 response state 继续；同时在 WebSocket connection 上保留 connection-scoped in-memory cache。这个 cache 包含 previous response object、prior input/output items、tool definitions / namespaces、以及 rendered tokens 这类 reusable sampling artifacts。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-response-create-shape|response.create shape]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-previous-response-cache|previous response cache]]

因此这里的优化应该理解成“把 agent loop 里的重复 API work 做成增量处理”：部分 safety classifiers / validators 只处理新 input，rendered token cache 继续 append，model resolution / routing 结果可以复用，billing 这类 postinference work 可以和后续 request overlap。原文没有说 validation / routing 完全不做了，而是说某些环节变成只处理新增部分或复用已有结果。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-incremental-stack-optimizations|incremental optimizations]]

## 为什么不能把 40% 往大了读

完整 agent task 的耗时通常不只包括 API service overhead，还包括 model inference total time、本地 tool runtime、test / build / file IO、client-side context construction 等。WebSocket mode 主要打的是多轮请求之间的重复 state processing 和服务端固定开销；如果一个任务的大头仍然是长 inference、慢测试或本地工具执行，那么仅靠这个 transport/state cache 改动，不可能稳定把完整 task wall-clock 降低 40%。

原文自己的数字也说明了口径需要分开：`45%` 是此前 single-request sprint 对 `TTFT` 的 improvement；`40%` 是 agent loop / agentic workflow 的 reported improvement；`1,000 TPS` 和 `4,000 TPS bursts` 是 GPT-5.3-Codex-Spark 推理吞吐相关结果。这几个数字不是同一个指标，不能混成“WebSocket 让 TTFT 或完整 task 快 40%”。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-ttft-sprint|TTFT sprint]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-launch-results|launch results]]

## 更准确的结论

这篇文章有价值的地方，是说明当 model inference 足够快以后，agent harness / API stack 周围的固定开销会成为新的瓶颈；WebSocket mode 用 `previous_response_id` 加 connection-scoped state cache，把多轮 agent loop 里重复处理的 conversation state、rendered tokens、validation/safety 和 routing 工作尽量变成增量。[[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-spark-tps-goal|Spark TPS goal]] [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown#^responses-websockets-previous-response-cache|previous response cache]]

但 `40%` 这个数本身应该保守看待：它是一个 `up to` 的产品 / 集成观察值，不是公开定义清楚的 benchmark。可以用它来说明方向：fast model 时代，Responses API path 的 repeated overhead 值得优化；不能用它来断言一般软件工程 agent run 的完整耗时都会下降 40%。

## Sources

- [[sources/openai-responses-websockets-2026-04/summary|openai-responses-websockets-2026-04]]
- [[sources/openai-responses-websockets-2026-04/source/openai-responses-websockets-markdown|openai-responses-websockets-markdown]]
