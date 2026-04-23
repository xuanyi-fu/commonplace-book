---
type: note
status: draft
created: 2026-04-22
updated: 2026-04-22
---

# anthropic-mcp-production-systems-2026-04-reading-note

## Source

- source collection: [[sources/anthropic-mcp-production-systems-2026-04/summary|anthropic-mcp-production-systems-2026-04]]
- primary reading file: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown|building-agents-that-reach-production-systems-with-mcp-markdown]]
- discussion language: Chinese

## Keshav Lite

- Category: vendor-authored architecture and integration explainer arguing for MCP as the common production layer for cloud-hosted agents [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-three-connection-paths]]
- Context: the article compares direct API calls, CLIs, and MCP, then narrows to the cloud-hosted agent setting where a reusable common layer matters most [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]]
- Core Question: if the goal is to let production agents in the cloud reach external systems reliably, why does MCP become the compounding integration layer, and what server/client patterns make that choice actually work? [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-three-connection-paths]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-protocol-common-layer]]
- Claims:
  - narrow or local integrations can stay with direct API calls or CLIs, but cloud-hosted production agents increasingly converge on MCP [[sources/anthropic-mcp-production-systems-2026-04/summary]]
  - effective MCP servers emphasize remote reach, intent-grouped tools, rich semantics, and standardized auth [[sources/anthropic-mcp-production-systems-2026-04/summary]]
  - MCP and skills are complementary rather than competing layers [[sources/anthropic-mcp-production-systems-2026-04/summary]]
- Credibility: the post is strongest as Anthropic's current product and protocol guidance, with some adoption signals and links to specs and companion posts; it is not a neutral benchmark or comparative survey [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]] [[sources/anthropic-mcp-production-systems-2026-04/summary]]
- Clarity: the API vs CLI vs MCP framing is very crisp, and the server/client split is easy to follow; the tradeoffs are compressed, so many of the stronger claims will need follow-up discussion rather than one-pass acceptance [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]] [[sources/anthropic-mcp-production-systems-2026-04/summary]]
- very brief TOB:
  - connecting agents to external systems
  - production agents run in the cloud
  - building effective MCP servers
  - making MCP clients more context-efficient
  - pairing MCP servers with skills
  - the compounding layer

## Reading State

- source slug: `anthropic-mcp-production-systems-2026-04`
- primary reading file: `sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown.md`
- current section: `completed`
- completed sections:
  - `Connecting agents to external systems`
  - `Direct API calls`
  - `Command-line interface (CLI)`
  - `Model Context Protocol (MCP)`
  - `Production agents run in the cloud`
  - `Building effective MCP servers`
  - `Build remote servers for maximum reach`
  - `Group tools around intent, not endpoints`
  - `Design for code orchestration when your surface is large`
  - `Ship rich semantics where they help`
  - `Lean on standardized auth`
  - `Making MCP clients more context-efficient`
  - `Load tool definitions on demand with tool search`
  - `Process tool results in code with programmatic tool calling`
  - `Pairing MCP servers with skills`
  - `Bundle skills and MCP servers as a plugin`
  - `Distribute skills from an MCP server`
  - `The compounding layer`
- pending sections:
  - `none`
- top-level section: `completed`
- scout status:
  - `concept/entity scout`: refreshed through session end
  - `related-pages scout`: refreshed through session end
  - latest refresh point: after final article verdict and note closeout

## Section Queue

1. `Connecting agents to external systems`
2. `Direct API calls`
3. `Command-line interface (CLI)`
4. `Model Context Protocol (MCP)`
5. `Production agents run in the cloud`
6. `Building effective MCP servers`
7. `Build remote servers for maximum reach`
8. `Group tools around intent, not endpoints`
9. `Design for code orchestration when your surface is large`
10. `Ship rich semantics where they help`
11. `Lean on standardized auth`
12. `Making MCP clients more context-efficient`
13. `Load tool definitions on demand with tool search`
14. `Process tool results in code with programmatic tool calling`
15. `Pairing MCP servers with skills`
16. `Bundle skills and MCP servers as a plugin`
17. `Distribute skills from an MCP server`
18. `The compounding layer`

## Recall Log

- section: `Connecting agents to external systems`
  - guiding question: 作者为什么把 agent 连接外部系统的方式分成 direct API、CLI、MCP 三类？三者真正的区别是什么？
  - user recitation: 用户抓住了本文这节的核心轴是 `common layer` 的有无与稳定性；用户进一步指出 CLI 的关键差别不一定是“薄”，而更可能是它默认依赖 OS / shell / stdin / stdout 这一类运行面，并提出“一个严格的 CLI 完全可以把输入输出收束成类似 MCP 的 JSON 协议”这一反例。
  - calibrated understanding: 这个复述大体是对的，尤其是“看 common layer 的强弱”这一点抓得很准。需要补的约束是：作者这里说 CLI “thin”，更接近“它提供的通用语义和跨环境 reach 比 MCP 少”，而不是说 CLI 天生不能变得很 rigid。也就是说，CLI 和 MCP 的差别不主要在“能不能定义严格协议”，而在于这层通用接口是不是被标准化、是不是被多 client 直接消费、以及是否天然覆盖 cloud / web / mobile 这类 deployment surface。用户提出的“universal MCP adapter”反例成立，但那更像是在 CLI 之上重新发明一层协议，而作者的论点是 MCP 本身已经把这层协议标准化了。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-protocol-common-layer]]
  - missing points:
    - 作者强调的是 deployment reach，不只是协议 strictness
    - MCP 还把 auth、discovery、rich semantics 一起抬到了 common layer，而不只是定义了一组调用命令
    - “MCP 最好”这件事只在作者关心的 production cloud-agent 场景里成立，不是普适结论
  - open questions:
    - CLI 和 MCP 的关键差别，究竟应该表述为“标准化的协议层”还是“标准化协议层 + 不依赖 OS 的跨环境 reach”
    - 如果一个 CLI 被设计成严格的 JSON protocol adapter，它和 MCP 的剩余差别还会落在哪些能力上
- section: `Production agents run in the cloud`
  - guiding question: 作者为什么要单独强调 production agents run in the cloud？这个前提会怎样改变前一节里 direct API、CLI、MCP 的比较结果？
  - user recitation: 按用户要求跳过正式 recite。用户认为这一节写得很烂，当前论证站不住脚：即便以 Claude Managed Agents 为例，agent 也可能依赖某种 execution environment，也就是某种 OS 运行面，因此“production agents run in the cloud”并不能自动推出“应该往 MCP 靠拢”。
  - calibrated understanding: 这条批评是成立的。原文当前形态把 `cloud-hosted` 和“不适合依赖 OS / shell 运行面”贴得太近了，但这两件事不是同一件事；同时它用 adoption/download 作为推力，也更像 popularity appeal，而不是充分的 architecture argument。更稳的版本应该是：并非所有 client 都暴露通用 OS 运行面，因此在 web、mobile、hosted client 等场景下，MCP 作为 standardized remote protocol 的价值才真正凸显出来。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]]
  - missing points:
    - 这一节更像是在收窄适用场景，而不是证明“云上一定没有 OS 运行面”
    - adoption 证据最多支持 ecosystem momentum，不能单独推出架构优越性
  - open questions:
    - 如果不把“无 OS 运行面”当前提，MCP 在 cloud-hosted agents 上的剩余核心优势到底是什么
- section: `Building effective MCP servers`
  - guiding question: 作者在这里把问题切成什么了？他接下来到底准备教你“怎么做对”什么？
  - user recitation: 用户压缩为“开始吹牛逼了，啊我懂怎么做 MCP，现在我来教你们”，意思是这节本身更像 vendor authority 的转场，而不是新的技术论证。
  - calibrated understanding: 这个判断基本成立。这节主要是在把问题从 `whether MCP` 切到 `how to build MCP well`，即“如果你已经决定做 MCP server，什么样的 server 更容易被 agent 稳定使用”。它更像经验法则的立题，不是证明。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 这节更像转场，不是具体 pattern
  - open questions:
    - 后面列出的 pattern 到底哪些是真有普适性的，哪些只是 Anthropic 当前产品偏好
- section: `Build remote servers for maximum reach`
  - guiding question: 为什么作者说 remote server 才真正给你 distribution / maximum reach？
  - user recitation: 用户的压缩判断是：如果你做一个 stdio MCP，而 client 没有 OS 运行面，那根本没法用；所以 remote server 的 `maximum reach` 本质上就是不把本地进程、shell、filesystem 这些前提压给每个 client。
  - calibrated understanding: 这个理解是对的，而且很实。这里的 `maximum reach` 核心不是“remote 更高级”，而是它对 client 运行面的假设最少，因此更容易覆盖 web、mobile、hosted agents。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 作者这里默认 major clients 都更容易消费 remote MCP，这更像经验判断
  - open questions:
    - 哪些 deployment surface 真正支持 remote MCP 但不支持本地 stdio / CLI
- section: `Group tools around intent, not endpoints`
  - guiding question: 为什么作者反对把 API endpoint 一比一包成 MCP tools，而主张按 intent 来组织工具？
  - user recitation: 用户认为这一节是目前为止很中肯的一节，并把它和 `AXI` 的 agent-first interface 思路联系起来：都在反对 raw primitive / endpoint mirror，而在追求更 task-shaped 的 interface。
  - calibrated understanding: 这个对应很准。作者这里的核心是让 tool 边界贴着任务意图，而不是底层 API 资源边界，从而减少回合数、context 负担和中间失败点。AXI 在更一般的 agent interface 层面把同一类问题讲得更系统。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]] [[sources/axi-agent-experience-interface-2026-04/summary|axi-agent-experience-interface-2026-04]]
  - missing points:
    - intent-shaped tools 也会更 opinionated，更难设计
  - open questions:
    - 什么程度的 combined operation 才算帮 agent，什么程度会变成 workflow 写死
- section: `Design for code orchestration when your surface is large`
  - guiding question: 如果一个系统的 API surface 特别大，为什么作者反而不建议继续堆很多 MCP tools，而是建议只暴露一个很薄的“写代码 + 执行代码”表面？
  - user recitation: 用户认为这是到目前为止最有价值的一节，关键启发是：如果 client/agent 没有统一的 OS 运行环境，没关系，MCP server 可以自己提供一个受控的 code execution surface，让 agent 写代码、server 来运行。
  - calibrated understanding: 这条理解抓住了这一节的真正价值。作者并不反对 code execution，而是在说：对于超大 API surface，与其暴露上千个 tools，不如把 execution surface 下沉到 server 侧，以少量高层入口加 sandboxed code orchestration 的方式处理。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 关键区别不是“要不要 code execution”，而是 execution 在 client 侧还是 server 侧
  - open questions:
    - 这种 server-side execution 的权限边界、语言选择、审计方式应该怎么设计
- section: `Ship rich semantics where they help`
  - guiding question: 作者为什么觉得有些 MCP server 不该只返回 text result，而应该把 UI 和 mid-tool-call interaction 也做进协议层？
  - user recitation: 按用户要求跳过正式 recite。本节的讨论重点转成了两个澄清：`MCP Apps` 是把可交互 UI 标准化地嵌进 host，而 `elicitation` 则是把 tool call 中途向用户要结构化输入 / URL handoff 这件事情标准化。用户进一步意识到 `elicitation` 最神奇的点，在于它让 agent 可以阻塞在 tool call 里等用户输入，而不是只能在 final answer 里回头追问。
  - calibrated understanding: 这个总结是对的。`MCP Apps` 和 `elicitation` 不依赖彼此，是两层不同的扩展/能力：前者是 inline embedded app UI，后者是 mid-tool-call user input。真正新的地方不是“CLI 做不到”，而是 MCP 把这些 richer interaction 变成了被 host/client 明确协商和消费的协议层能力。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - `elicitation` 只要求支持的 client 至少实现一种 mode，不是所有 client 必须支持
  - open questions:
    - 各个 coding agent 对 `elicitation` 和 `MCP Apps` 的真实支持面目前到什么程度
- section: `Process tool results in code with programmatic tool calling`
  - guiding question: 为什么作者不想把每次 tool 调用的原始结果都直接喂回模型，而要先在 code execution sandbox 里处理？
  - user recitation: 用户的总结是：上一节 `tool search` 解决的是不需要的 tool definition 占用 context；这一节 `programmatic tool calling` 解决的是 tool 返回内容太多、只有一部分真正对 agent 有用，因此让 agent 写一个小脚本去处理返回结果。
  - calibrated understanding: 这个理解是对的，而且抓住了和上一节的对称关系：上一节在压 `tool definitions` 的 context 成本，这一节在压 `tool results` 的 context 成本。还可以再补一个关键点：这里不只是“从一个大结果里过滤出一小部分”，而是把多步 tool orchestration 里的 loop、filter、aggregate、join 这些中间脏活交给 code execution sandbox 处理，让模型只看最终的高价值结果。它也要和前面那节 `Design for code orchestration when your surface is large` 区分开：那一节主要是 server-side code orchestration；这一节是 client-side / agent-side 的 programmatic post-processing pattern。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 这里的 code execution 主要服务于 client-side context optimization
  - open questions:
    - 这种 client-side sandbox 更像 host 提供的标准能力，还是 agent 自带的执行面
- section: `Lean on standardized auth`
  - guiding question: 作者为什么把 standardized auth 单独拎出来？在 cloud-hosted agent 场景里，它解决了什么调用之外的问题？
  - user recitation: 用户的压缩理解是：这一节主要在说 MCP 对 OAuth 的支持很好，同时顺手宣传 Claude Managed Agents 对 MCP auth / 凭证复用也支持得很好，所以不要自己再造 auth 和 token plumbing 的轮子。
  - calibrated understanding: 这个复述是对的。更准确一点说，作者在推进的是“把 cloud-hosted OAuth lifecycle 标准化”这件事：从首次授权、client registration、减少 surprise re-auth，一直到运行时 token 注入、refresh、凭证复用，都希望被协议和平台一起承接。后半段明确是在把 `Vaults in Claude Managed Agents` 当成现成解决方案来推。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-managed-agents-auth-tiein]]
  - missing points:
    - 这一节不只是说 “OAuth 支持好”，而是在说 “cloud-hosted runtime 里的 credential lifecycle 也要被接住”
  - open questions:
    - MCP 自身的 auth 标准化边界，到哪里结束，哪里开始变成 Anthropic 平台能力
- section: `Making MCP clients more context-efficient`
  - guiding question: 作者为什么开始从 server 端切到 client 端？他觉得 MCP client 最大的问题是什么？
  - user recitation: 用户的判断是：这一节开始，作者要讲一些 Anthropic 自己的 agent / MCP client 是怎么优化 MCP 调用的小技巧。
  - calibrated understanding: 这个判断是对的。这一节不再主要讲协议本身，而是在讲 client-side orchestration：当 MCP server 和 tools 变多以后，client 怎么避免被 tool definitions 和 tool results 把 context 吃爆。更像 Anthropic 自己的 client optimization playbook，而不是 MCP spec 的强约束。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 这里开始明显从 protocol/design 转到 host/client implementation tricks
  - open questions:
    - 哪些 pattern 是 Anthropic host 特有的，哪些能被更一般的 MCP client 复用
- section: `Load tool definitions on demand with tool search`
  - guiding question: 为什么作者不想一开始就把所有 MCP tools 都塞进 context，而要让 agent 先 search，再按需加载？
  - user recitation: 用户把它总结成 tool 太多时的 progressive disclosure：一开始 context 里只放简短 description，不放完整 tool definition；agent 通过 `tool search` 找到要用的工具后，再把 definition load 进 context。
  - calibrated understanding: 这个总结是对的，而且已经抓到这节的关键。更精确地说，这里延迟展开的对象不是执行步骤，而是 `tool definitions / tool schema` 本身。`skill` 延迟展开的是 “怎么做”，`tool search` 延迟展开的是 “有哪些工具、每个工具怎么调用”。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
  - missing points:
    - 这节的目标是把 tools 从 “静态全量 prompt” 变成 “运行时按需检索的工具目录”
  - open questions:
    - 在 tool catalog 特别大时，tool search 的召回和 selection accuracy 会怎样影响 agent 的稳定性
- section: `Pairing MCP servers with skills`
  - guiding question: 为什么作者觉得 MCP server 还不够，必须再配 skills？这两者在他这里各自负责什么？
  - user recitation: 用户认为作者这里对 `skill` 的理解过于狭隘。按照更一般的抽象，`skill` 只是一个 `name + description + 按需展开 SKILL.md` 的 progressive disclosure 载体，不天然只等于 procedural playbook，因此把 “MCP 负责能力、skill 只负责 playbook” 说成普适原则是愚蠢的。用户同时接受了 plugin 这一小节比较务实的部分：如果一个 workflow 同时需要 MCP、skill、hooks、LSP、subagent，那么把它们作为一个 plugin 统一分发是合理的。用户对 “从 MCP server 分发 skills” 这一小节兴趣不高，直接压缩跳过。
  - calibrated understanding: 这个批评成立。文中这一节更像是在描述 Anthropic 自家 host/runtime 对 `MCP`、`skills`、`plugin` 的产品分工：`MCP` 提供 capability surface，`skills` 提供 procedural overlay，`plugin` 负责 bundling 和 distribution。作为他们自己的产品架构，这套分工可以成立；但把它上升成 `skill` 这个抽象的本体定义，就说过头了。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-plugin-packaging]]
  - missing points:
    - `plugin` 作为分发单位是务实建议，不等于 `skill` 的概念边界被固定
  - open questions:
    - 如果脱离 Anthropic host/runtime，`skill`、`MCP server`、`plugin` 的更一般边界应该怎么定义
- section: `The compounding layer`
  - guiding question: 为什么作者最后把 MCP 叫做 `the compounding layer`？这个“复利”到底从哪来？
  - user recitation: 按用户要求跳过正式 recite。用户在读到末尾时的整体判断是：这篇更像一篇给 MCP 带货的文章，而不是客观综述。
  - calibrated understanding: 这个定性是对的。最后一节的主张是：如果 production agents 越来越往 cloud 走、主要 client 持续收敛到 MCP，那么 MCP 就会因为 client 增长、extension 增长、integration 复用而形成“复利”。但这个前提本身就是强趋势判断，不是逻辑证明；再结合全文里反复出现的 adoption 数据、Anthropic 自身产品绑定、以及平台 tie-in，这一节更像生态战略收束，而不是中性比较。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-adoption-and-product-tiein]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-pattern-authority]]
  - missing points:
    - 这节的说服力主要取决于是否接受 Anthropic 对 cloud-agent 生态走向的判断
  - open questions:
    - 如果 future client 生态没有像作者预期那样持续收敛到 MCP，这个“compounding layer”论证还剩多少成立

## Questions And Answers

- question: `每个 agent × service 组合都要自己处理 auth、tool description、edge cases` 这真的是一个代价吗？如果 agent 有 OS 和代码运行环境，直接写一个 API 调用 script 或走 browser-use 这类执行层，很多任务可以很快跑通。
  - answer: 这是代价，但要把代价的层级说清楚。你的 `browser-use` / 小红书例子说明：对“单个 agent、单个任务、单个环境”的快速达成来说，这个代价常常不大，尤其当 agent 已经拥有 OS、sandbox、浏览器执行层或代码执行能力时。这个例子确实削弱了作者把 `agent × service` 问题讲得过于沉重的语气。[[entities/browser-use|Browser Use]] [[sources/browser-use-2026-04/summary|browser-use-2026-04]] 但作者真正想强调的代价，更像是“把一个临时可跑通的集成，变成可复用、可跨 client、可跨 deployment、可统一 auth 和 tool semantics 的 production integration”。也就是说，问题不在“能不能十分钟写出来”，而在“是不是每个 agent / client / environment 都要重新做一遍，且各自维护 auth、tool description、异常行为和兼容性”。这个区分很重要：你的例子说明 ad-hoc execution path 很强，而作者在推的是 reusable integration layer。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]]
- question: `MCP 的 rich semantics` 到底是什么意思？
  - answer: 这里的 `rich semantics` 不是泛指“协议更高级”，而是说 MCP 不只传一个工具名和字符串参数，而是把一些高层交互语义也标准化进协议层。就这篇文章给的具体例子，`MCP Apps` 允许 tool 返回内嵌 chart / form / dashboard 这种可交互界面；`elicitation` 允许 server 在 tool call 中途暂停，向用户要额外输入、确认危险操作，或者把用户交给浏览器继续 OAuth / payment / credential flow。也就是说，`rich semantics` 在这里基本等于：协议本身能表达的不只是“调用工具”，还包括“怎么在调用过程中与用户交互、怎么把 UI 带进 chat、怎么处理中途授权或补参”。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- question: `rich semantics` 这些事情 CLI 就不能做了吗？
  - answer: 能做。CLI 完全可以通过 stdout / stdin / TTY / URL handoff / structured JSON output 去模拟 inline UI、补参、确认危险操作，甚至让宿主渲染 form 或 dashboard。所以问题不在“CLI 有没有表达能力”，而在“这些语义是不是协议层的一等公民、是不是被标准化了、是不是能被不同 client 直接一致地消费”。更准确地说，MCP 的优势不是“只有它能做 rich semantics”，而是它把这些 rich semantics 标准化成了协议层能力；而 CLI 通常需要你和宿主额外约定 wire shape 和 lifecycle，等于在 CLI 之上再长出一层协议。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- question: 这篇第一节是不是主要站在“我是给很多 agent 开发工具的人，我要选什么 integration layer”这个角度在说？
  - answer: 这个理解大体是对的，而且已经很接近这节的真正视角。更准确地说，作者站的不是“单个 agent 能不能把任务做成”，而是“如果我是一个系统/工具提供方，我想让很多不同 client 和 deployment environment 里的 production agents 都能接到我的能力，我应该把哪一层做成公共 integration layer”。所以你的说法抓住了“给很多 agent 提供能力”这件事，但还可以再补一层：作者特别关心的是 cloud-hosted production agents，而不只是抽象意义上的“很多 agent”。也正因为这个前提成立，他才会把 direct API、CLI、MCP 的差别放在 common layer、跨环境 reach、标准化 auth/discovery/interaction semantics 上来讲，而不是放在“单次任务能不能做成”上。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-protocol-common-layer]]
- question: `MCP Apps` 是什么时候提出和正式发布的？
  - answer: 按官方材料看，`MCP Apps` 最早在 `2025-11-21` 作为 `SEP-1865` 进入正式提案流程；到了 `2026-01-26`，它成为 `Stable`，并作为第一个官方 MCP extension 对外宣布 live。也就是说，`2025-11-21` 是最早的官方出现时间，`2026-01-26` 是正式稳定发布时间。[[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]
- question: 支持 `elicitation` 的 coding agent 多吗？`Claude Code` / `Codex` 支持吗？
  - answer: 截至 `2026-04-22`，我能明确确认 `Claude Code` 支持 `elicitation`，而且同时支持 `form mode` 和 `URL mode`；官方文档还写了会自动显示交互 dialog。至于 `Codex`，我能确认它支持连接 MCP servers，但我没有找到 OpenAI 官方文档明确确认 `elicitation` dialog 或 `MCP Apps` 渲染支持，所以不建议把 `Codex` 当成已确认支持 `elicitation` 的 client 来依赖。[[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]] [[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]
- question: `elicitation` 依赖 `MCP Apps` 吗？是不是每个 MCP client 都得自己实现 form mode？
  - answer: 不依赖。`elicitation` 和 `MCP Apps` 是两层不同的能力。`elicitation` 是 client capability，用来标准化 tool call 中途的结构化 user input / URL handoff；`MCP Apps` 是单独的 UI 扩展，用来让 tool 带一个可嵌入的交互 UI。只有在初始化时声明了 `elicitation` capability 的 client，才需要至少支持一种 mode（`form` 或 `url`）；不支持这个 capability 的 client 不需要实现 form mode，server 也不能给它发 elicitation 请求。[[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]

## Reader Comments

- comment: 用户认为作者把 CLI 说成 “thin” 并不完全准确。更精确的说法可能是：CLI 可以很灵活，也可以很 rigid；它和 MCP 的关键差别不只是协议 strictness，而是 CLI 默认依赖 OS / shell 运行面，而 MCP 试图把 common layer 直接标准化为可被多 client 跨环境消费的协议。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]]
- comment: 用户用 browser-use 在登录态小红书上快速完成探索和提取，质疑 `agent × service` 在有 OS / sandbox / browser execution layer 时是否真的构成高代价。这条评论把“临时可跑通的 agent task”与“可复用的 production integration layer”区分开了，是后续继续读这篇文章时的重要对照点。
  - cited passage: [[entities/browser-use|Browser Use]] [[sources/browser-use-2026-04/summary|browser-use-2026-04]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^common-layer-distinction]]
- comment: 用户反驳本文对 `rich semantics` 的隐含优越叙事：CLI 当然也可以承载 richer interaction，但通常需要在 CLI 之上追加一层额外约定；因此更准确的对比不该是“CLI 做不到，MCP 做得到”，而应是“CLI 可以做，但 MCP 把它协议化、标准化了”。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- comment: 用户认为本节论证当前形态并不稳：即便以 Claude Managed Agents 这类 cloud product 为例，agent 也可能实际依赖某种 execution environment，也就是某种 OS 运行面，因此“production agents run in the cloud”并不能自动推出“应该往 MCP 靠拢”。用户进一步指出，文中用 MCP SDK 下载量和 adoption 作为推动论据，更像是在做 popularity appeal，而不是直接证明 MCP 在能力或架构上必然更优。用户认可的更强论证应当是：并非任何 agent/client 都拥有通用 OS 运行面，因此在缺少 shell / filesystem / sandbox 的 web、mobile、hosted client 上，MCP 作为 standardized remote protocol 的价值才真正凸显出来。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^cloud-hosted-agents-favor-mcp]]
- comment: 用户在 `Build remote servers for maximum reach` 这一小节给出的压缩判断是：如果你做的是 stdio MCP server，而 client/agent 没有 OS 运行面，那它根本没法用；所以 remote server 所谓的 `maximum reach`，本质上就是不把本地进程、shell、filesystem 这些前提压给每个 client。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- comment: 用户认为作者对 `skill` 的理解过于狭隘。更本质地看，`skill` 只是一个带 `name` 和 `description` 的文件化约定，真正的作用是通过 progressive disclosure 影响 context：初始上下文里只有简短描述，agent 真要用时才把完整 `SKILL.md` 读进来。至于 skill 是否只提供 playbook、是否不该碰外部信息能力，这更像 Anthropic 自己的产品约定或训练分工，而不是 `skill` 这个抽象本身的必然边界。用户因此反对把 “MCP 负责能力、skill 只负责 playbook” 当成普适本体论。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- comment: 把这篇文章定性为 `vendor-authored architecture advocacy` 而不是客观综述，是因为它反复把 ecosystem momentum、Anthropic 自身经验权威、以及 Claude 平台产品 tie-in 混在一起推进论证：一方面用 `300 million downloads`、`millions of people use MCP with Claude` 和 `Claude Cowork / Claude Managed Agents / Claude Code` 来提供 adoption 与产品绑定；另一方面用 “we have over 200 MCP servers” 来把后续 design advice 建立在 Anthropic 自己的经验 authority 上；到了 auth 段又直接把 `Vaults in Claude Managed Agents` 作为现成承接方案；而在 skills/plugin 段则把 Claude plugin 作为推荐分发抽象。这个写法更像站在 Anthropic 生态位置上的架构倡导文，而不是把 direct API、CLI、MCP 放在对称条件下做中立比较。
  - cited passage: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^mcp-adoption-and-product-tiein]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-pattern-authority]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-managed-agents-auth-tiein]] [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown#^anthropic-plugin-packaging]]

## Candidate Concepts Entities

- `Model Context Protocol (MCP)` | concept | 文章的核心抽象：作为 common layer，把 auth、discovery、semantics 和 cross-client reach 标准化 | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `intent-grouped tools` | concept | 文章最核心的 server-design 规则之一：不要镜像 endpoint，而要围绕任务意图组织工具 | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `MCP Apps` | concept | 官方协议扩展，用于把 interactive UI 带回 chat 界面 | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `elicitation` | concept | 文章里重要的 mid-tool-call user input primitive | existing page status: exists [[entities/mcp-elicitation|mcp-elicitation]] | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `CIMD (Client ID Metadata Documents)` | concept | 文章推荐的 OAuth client registration pattern | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `Vaults` | entity | Anthropic 在 cloud-hosted agents 里承接 OAuth token reuse 的产品表面 | existing page status: missing | confidence: medium-high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `tool search` | concept | client-side progressive disclosure pattern，控制 tool definitions 的 context cost | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]
- `programmatic tool calling` | concept | client-side pattern：在 code execution sandbox 里处理 tool results，而不是把中间结果都喂回模型 | existing page status: missing | confidence: high | source: [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown]]

## Candidate Related Pages

- [[syntheses/agent-harness-philipp-schmid-overall-reading|agent-harness-philipp-schmid-overall-reading]] | relation: `extends` | 把 `agent harness` 作为长运行任务与 tool handling 的 infra layer 来讨论，能把本文的 `common layer` 论点推得更一般化 | confidence: 0.79 | trigger: `Connecting agents to external systems`; `Building effective MCP servers`
- [[syntheses/agent-harness-atomic-tools-over-rigid-workflows|agent-harness-atomic-tools-over-rigid-workflows]] | relation: `supports` | 直接支持本文 “group tools around intent, not endpoints” 的 server 设计方向 | confidence: 0.92 | trigger: `Building effective MCP servers` -> `Group tools around intent, not endpoints`
- [[sources/axi-agent-experience-interface-2026-04/summary|axi-agent-experience-interface-2026-04]] | relation: `extends` | AXI 不是在讲 MCP server design，而是在更一般的 `agent-first interface design` 层面讲同一类问题：不要把 interface 做成 raw primitive / help-text shell，而要用 combined operations、pre-computed aggregates、contextual disclosure 这些设计把 agent 的任务步数和发现成本压下来。这和本文这一小节“按 intent 组织 tools，而不是镜像 endpoints”是同一方向上的更系统展开。 | confidence: 0.9 | trigger: `Building effective MCP servers` -> `Group tools around intent, not endpoints`
- [[syntheses/components-of-a-coding-agent-layer-mismatch-and-state-resumption|components-of-a-coding-agent-layer-mismatch-and-state-resumption]] | relation: `extends` | 可作为本文 client-side context efficiency 部分的本地对照材料 | confidence: 0.76 | trigger: `Making MCP clients more context-efficient`
- [[syntheses/codex-computer-use-implementation-and-limits|codex-computer-use-implementation-and-limits]] | relation: `supports` | 其中“有结构化 plugin / MCP / CLI / API 时优先不用 computer use”的结论，可以作为本文外部系统接入层次结构的一个本地支持例子 | confidence: 0.88 | trigger: `Connecting agents to external systems`; `Model Context Protocol (MCP)`
- [[entities/cloudflare-mcp-server|cloudflare-mcp-server]] | relation: `supports` | 它把本文 “当 surface 太大时，用一个很薄的 MCP surface + server-side code execution” 这条建议具体化成了真实实现，因此是 `Design for code orchestration when your surface is large` 这一节最强的本地支持材料之一。 | confidence: 0.95 | trigger: `Design for code orchestration when your surface is large`
- [[entities/mcp-elicitation|mcp-elicitation]] | relation: `supports` | 它把本文 `Ship rich semantics where they help` 里关于 mid-tool-call user input 的协议层能力拆得更细，能支持我们对 `elicitation` 与 `MCP Apps` 区别的判断。 | confidence: 0.94 | trigger: `Ship rich semantics where they help`
- [[entities/mcp-apps|mcp-apps]] | relation: `supports` | 它把本文 `Ship rich semantics where they help` 里关于 inline UI / app surface 的部分拆得更细，能支持我们对 `MCP Apps` 在 rich semantics 里所处位置的判断。 | confidence: 0.91 | trigger: `Ship rich semantics where they help`

## Sources

- [[sources/anthropic-mcp-production-systems-2026-04/summary|anthropic-mcp-production-systems-2026-04]]
- [[sources/anthropic-mcp-production-systems-2026-04/source/building-agents-that-reach-production-systems-with-mcp-markdown|building-agents-that-reach-production-systems-with-mcp-markdown]]
- [[sources/axi-agent-experience-interface-2026-04/summary|axi-agent-experience-interface-2026-04]]
- [[sources/browser-use-2026-04/summary|browser-use-2026-04]]
- [[sources/mcp-apps-2026-04/summary|mcp-apps-2026-04]]
- [[sources/mcp-elicitation-2026-04/summary|mcp-elicitation-2026-04]]
