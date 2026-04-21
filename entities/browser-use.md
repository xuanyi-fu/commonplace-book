---
type: entity
status: draft
created: 2026-04-21
updated: 2026-04-21
---

# Browser Use

`Browser Use` 更适合被理解成 `[[web-agent]]` 生态里的浏览器执行层，而不是一个完整的消费级浏览器助手。它的核心作用是让 LLM / agent 把浏览器当成执行环境：既可以走 Python `Agent(task=..., llm=...)` 这条路线，也可以走持久会话式的 `browser-use` CLI。[[sources/browser-use-2026-04/source/official-doc-introduction|官方介绍]] [[sources/browser-use-2026-04/source/official-doc-quickstart|官方 quickstart]] [[sources/browser-use-2026-04/source/official-doc-cli|官方 CLI 文档]]

## 它解决什么问题

如果只抓最核心的问题，Browser Use 解决的是：

- 怎么让 agent 真的去网页里做事，而不是只会回答“你应该怎么操作网页”。[[sources/browser-use-2026-04/source/official-doc-introduction|官方介绍]] [[sources/browser-use-2026-04/source/official-repo-readme|官方 README]]
- 怎么减少传统 Playwright / Selenium 那种 selector-first、易脆的脚本心智，把网页操作变成更适合 agent 的任务执行层。[[sources/browser-use-2026-04/source/official-doc-quickstart|官方 quickstart]] [[sources/browser-use-2026-04/source/official-doc-cli|官方 CLI 文档]]
- 怎么在生产里处理浏览器会话、登录态、cookies、profile、cloud browser、tunnel 这些实际工程问题。[[sources/browser-use-2026-04/source/official-doc-quickstart|官方 quickstart]] [[sources/browser-use-2026-04/source/official-doc-cli|官方 CLI 文档]] [[sources/browser-use-2026-04/source/official-repo-readme|官方 README]]

所以更准确地说，Browser Use 不是“会浏览网页的模型”，而是“给模型用的浏览器执行层”。[[sources/browser-use-2026-04/source/official-repo-readme|官方 README]]

## 主要用法

### Python agent

官方 quickstart 的主用法是：

- 安装 `browser-use`
- 选一个模型
- 构造 `Agent(task=..., llm=...)`
- 让 agent 在浏览器里完成任务。[[sources/browser-use-2026-04/source/official-doc-quickstart|官方 quickstart]]

这说明 Browser Use 的主心智模型是 `AI browser agent runtime`。[[sources/browser-use-2026-04/source/official-doc-quickstart|官方 quickstart]]

### CLI

CLI 则更像一个持久浏览器 shell。官方文档给出的核心流程是：

- `open` 页面
- `state` 读取带编号的元素
- `click` / `input` / `type` / `screenshot`
- 保持会话继续操作。[[sources/browser-use-2026-04/source/official-doc-cli|官方 CLI 文档]] [[sources/browser-use-2026-04/source/official-repo-readme|官方 README]]

这条路线特别适合：

- 半手动、半自动的网页探索
- 已登录站点的会话复用
- 快速试错式的网页操作任务

## 为什么它适合挂在 Web Agent 下面

Browser Use 和 `[[web-agent]]` 的关系，不是“它本身等于所有 web agent”，而是：

- `[[web-agent]]` 是概念层：把浏览器网页当作主要工作环境的 agent
- Browser Use 是工具层：给这类 agent 提供浏览器观察和操作能力

从这个角度看，Browser Use 更像：

- `web agent infrastructure`
- `browser execution layer`
- `browser shell for agents`

而不是最终用户直接使用的全能 agent 产品。[[sources/browser-use-2026-04/source/official-doc-introduction|官方介绍]] [[sources/browser-use-2026-04/source/official-doc-cli|官方 CLI 文档]]

## 本地试用信号

这次线程里的 `RedNote` 实测给了一个很直接的信号：Browser Use CLI 的价值不只是“打开页面”，而是能在同一持久会话里完成：

- 打开网站
- 保持登录弹层
- 用户扫码登录
- 登录后继续复用同一浏览器会话
- 搜索关键词
- 打开帖子
- 读取帖子详情和部分页面文字。[[sources/browser-use-2026-04/source/local-observation-rednote-session-2026-04-21|本地 RedNote 试用记录]]

同时，这次试用也暴露了一个真实边界：

- 正文和评论这类可见文本，`state` 读起来比较顺
- 但配方类信息如果写在图里，就仍然要结合截图读取

所以它更像“浏览器执行层 + 页面文本层”，而不是完整的结构化内容抽取器。[[sources/browser-use-2026-04/source/local-observation-rednote-session-2026-04-21|本地 RedNote 试用记录]]

## 暂定判断

Browser Use 现在最值得记的，不是它是不是最强的 browser agent，而是它把一个很重要的分层做清楚了：

- 模型负责规划和决策
- Browser Use 负责把浏览器变成一个可执行、可保持会话、可持续操作的环境

这也是为什么它和 `[[web-agent]]` 的关系很自然：它不是概念本身，而是让这个概念真正可用的一层具体基础设施。

## Sources

- [[sources/browser-use-2026-04/summary|browser-use-2026-04]]
- [[sources/browser-use-2026-04/source/official-doc-introduction|official-doc-introduction]]
- [[sources/browser-use-2026-04/source/official-doc-quickstart|official-doc-quickstart]]
- [[sources/browser-use-2026-04/source/official-doc-cli|official-doc-cli]]
- [[sources/browser-use-2026-04/source/official-repo-readme|official-repo-readme]]
- [[sources/browser-use-2026-04/source/local-observation-rednote-session-2026-04-21|local-observation-rednote-session-2026-04-21]]
