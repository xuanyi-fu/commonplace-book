---
type: synthesis
status: draft
created: 2026-04-20
updated: 2026-04-20
---

# Codex Computer Use 的实现形态与当前边界

这页讨论的是 `Codex computer use` 当前公开可见的实现形态，不是整个 Codex 产品。就现有公开材料和本地工具界面来看，一个比较稳妥的判断是：它现在更像一个面向桌面 GUI 的感知-动作闭环，而不是任意 macOS app 的深层语义集成层。

## 工作判断

当前的 Codex computer use，核心上像是：

- 先看当前界面状态
- 再决定一组 GUI 动作
- 执行动作
- 再看一张新的界面快照确认结果

这套模式对“可离散分解、可逐步验证”的任务是成立的，但对“连续、低延迟、强依赖悬停和即时反馈”的交互仍然偏初级。

## 直接信号

- 官方 Codex app 文档明确要求 `Screen Recording` 和 `Accessibility` 权限。前者让 Codex 看见目标 app，后者让 Codex 点击、输入和导航。
- 同一份官方文档明确写到，computer use 会处理截图，并且会与窗口、菜单、键盘输入、剪贴板状态发生交互。
- 官方 computer-use guide 明确描述了一个截图驱动的循环：看当前 UI，返回结构化动作，执行这些动作，再回传新的截图，然后继续。
- 本地桌面会话里暴露出来的 Computer Use 工具界面，比公开文档给出了更直接的实现信号：`get_app_state` 明确返回 `screenshot + accessibility tree`，动作层同时支持按元素索引操作和按像素坐标点击、拖拽。

## 这意味着什么

- 它不需要目标 app 提供专门的 API，也能在很多 GUI 里完成任务。
- 但它看起来也没有默认获得“这个 app 里每个对象到底是什么”的深层语义理解。
- 更贴近现实的控制栈大概是：
  - 用截图理解当前视觉状态
  - 在能拿到时，借助 accessibility 结构补充界面信息
  - 用合成的鼠标和键盘动作去操作界面
  - 再用新的截图验证动作是否生效
- 这套架构很适合 GUI QA、图形界面 bug 复现、设置页操作、浏览器任务、跨多个 app 的知识工作流。
- 它不太适合 accessibility 很差、界面变化很快、或者成功高度依赖连续光标控制的交互。

## 如何理解 STS2 失败案例

你拿 `Slay the Spire 2` 做测试，其实很有代表性。Codex 没法稳定把一张攻击牌拖到正确目标上，这个结果和上面的实现判断是相符的。

- 第一，游戏 UI 往往几乎不给可用的 accessibility 语义。就算底层能拿到 accessibility tree，真正关键的交互对象也可能只是自绘画布里的视觉元素，而不是可稳定引用的语义节点。
- 第二，官方文档描述的主循环本质上还是“截图一次，动作一轮，再截图一次”。这种节奏适合按钮、菜单、输入框和分步骤流程，但不擅长需要持续观察拖拽过程的实时交互。
- 第三，把牌拖到目标上不是单纯的路径规划问题。它往往要求代理根据瞬时视觉反馈不断校正拖拽路径、停留位置和释放时机，而当前这层通用桌面代理接口并没有公开暴露出这种高频闭环能力。

所以，`STS2` 这个失败案例不是一个偶然 bug，它更像是在暴露当前 computer use 的能力边界：它能做“看一眼再动一下”的事，但还不擅长“边看边连续控制”的事。

## 实用结论

- 今天的 Codex computer use，已经足够用于范围明确的 GUI 工作流和探索式 app QA。
- 但它在游戏、绘图工具、高动态 canvas，以及任何依赖快速闭环光标控制的任务上，仍然显得偏早期。
- 当目标系统已经有专门的 plugin、MCP server、CLI 或稳定 API 时，通常仍然应该优先使用这些结构化接口，而不是退回 computer use。

## 还没被公开确认的部分

- 公开 OpenAI 文档并没有直接写明底层到底调用了哪些 macOS 原生 API。
- 公开材料也没有完整解释 OCR 或视觉栈、事件注入路径、以及 accessibility 结构不足时的回退策略。
- 当前桌面会话里的 `accessibility tree` 信号很直接，但它仍然只是本地工具界面快照，不等于 OpenAI 官方公开写过一份完整实现说明。

## Sources

- [[sources/codex-computer-use-2026-04/source/official-doc-codex-app-computer-use|official-doc-codex-app-computer-use]]
- [[sources/codex-computer-use-2026-04/source/blog-2026-04-16-codex-for-almost-everything|blog-2026-04-16-codex-for-almost-everything]]
- [[sources/codex-computer-use-2026-04/source/official-guide-api-computer-use|official-guide-api-computer-use]]
- [[sources/codex-computer-use-2026-04/source/local-session-computer-use-tool-interface-2026-04-20|local-session-computer-use-tool-interface-2026-04-20]]
- [[sources/codex-computer-use-2026-04/source/user-test-sts2-drag-failure-2026-04-20|user-test-sts2-drag-failure-2026-04-20]]
