---
type: concept
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Web Agent

`web agent` 指的是一种把浏览器网页当作主要工作环境的 agent：它不仅回答网页相关问题，还会自己在网页里观察、点击、输入、跳转、读取结果，并试图完成一个多步任务。这个定义和 `WebArena`、`WebVoyager`、`WebXSkill` 这些研究线索是一致的：它们都把 agent 放进真实或半真实的 web environment 中，要求它通过网页交互完成目标，而不是只做离线问答。[WebArena](https://arxiv.org/abs/2307.13854) [WebVoyager](https://aclanthology.org/2024.acl-long.371/) [WebXSkill](https://arxiv.org/abs/2604.13318)

## 核心特征

- 它的主要工作空间是浏览器网页，而不是终端、IDE 或整个操作系统。[WebArena](https://arxiv.org/abs/2307.13854) [WebVoyager](https://aclanthology.org/2024.acl-long.371/)
- 它通常需要同时具备 3 类能力：
  - 观察页面状态，例如 DOM、accessibility tree、截图或页面文本
  - 操作页面元素，例如点击、输入、滚动、切标签页、提交表单
  - 规划多步任务，例如决定先去哪页、下一步搜什么、失败后如何重试
- 它的目标不是“解释网页”，而是“在网页上完成任务”。[WebVoyager](https://aclanthology.org/2024.acl-long.371/)

## 和相邻概念的区别

- 它不同于普通 chat assistant：
  - 普通 assistant 告诉你“该怎么做”
  - `web agent` 自己去网页里做
- 它也不同于更广义的 `computer-use agent` 或 `desktop agent`：
  - `web agent` 的操作边界主要在浏览器和网页
  - `desktop agent` 的边界是整个桌面和多个 app
- 因此，`web agent` 更适合被看作 `computer-use agent` 的一个更窄子类。

## 常见任务形态

- 在招聘、工单、SaaS 后台或电商网站里完成一串多步操作
- 根据多个页面的信息做比对、筛选、填表和提交
- 在文档站、搜索引擎、论文页和产品页之间来回跳转，生成报告或结论
- 在网页环境里执行可复用操作套路，而不是每次都从零摸索。`WebXSkill` 研究的就是如何把这类轨迹沉淀成 skill。[WebXSkill](https://arxiv.org/abs/2604.13318)
- 在工程实现上，这类 agent 往往还需要一层专门的浏览器执行层。`[[browser-use]]` 就是一个很典型的例子：它把浏览器变成 agent 可持续操作的环境，而不是只提供一次性网页抓取。[[entities/browser-use|Browser Use]]

## 为什么它容易翻车

- 网页信息往往分散在多个页面、多个标签和多种模态里
- 页面会变化，DOM 结构和视觉布局也可能不稳定
- 任务经常包含隐含约束，而不是清晰、单步、可验证的指令
- agent 不仅要“看懂页面”，还要在执行过程中保持状态、记住目标，并在失败时调整策略

这也是为什么 `web agent` 往往被单独研究和单独 benchmark，而不是直接等同于一般意义上的“会用工具的 LLM”。[WebArena](https://arxiv.org/abs/2307.13854) [WebVoyager](https://aclanthology.org/2024.acl-long.371/)

## 暂定判断

`web agent` 最好不要被理解成“会访问网页的聊天机器人”，而应该理解成“以浏览器为执行环境的任务代理”。它真正困难的地方，不只是信息检索，而是把观察、操作、规划和状态维护连成一个可持续的网页任务闭环。

## Sources

- [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)
- [WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models](https://aclanthology.org/2024.acl-long.371/)
- [WebXSkill: Skill Learning for Autonomous Web Agents](https://arxiv.org/abs/2604.13318)
- [[sources/ai-agent-weekly-2026-04-18/summary|ai-agent-weekly-2026-04-18]]
