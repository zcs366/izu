---
title: AG-UI 协议
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [protocol, agent, frontend, standard]
sources:
  - raw/articles/ag-ui-protocol-intro.md
confidence: high
---

# AG-UI 协议

AG-UI 是一个开源的、基于事件流的轻量协议，专门用于连接 AI Agent 和用户界面。由 [CopilotKit](https://github.com/CopilotKit) 发起并主导维护。

## 定位：Agent 三层协议的"前端层"

AI Agent 生态正在形成三层协议格局，三者互补而非竞争：

| 协议 | 发起方 | 解决什么问题 |
|------|--------|-------------|
| **MCP**（Model Context Protocol） | Anthropic | Agent 怎么用工具和数据源 |
| **A2A**（Agent to Agent） | Google | Agent 之间怎么通信协作 |
| **AG-UI**（Agent - User Interface） | CopilotKit | Agent 怎么跟人打交道 |

一个 Agent 可以同时运行这三个协议，各管各的层，互不冲突。^[raw/articles/ag-ui-protocol-intro.md]

## 为什么需要 AG-UI

传统 REST/GraphQL API 在 Agent 场景下有四个硬伤：^[raw/articles/ag-ui-protocol-intro.md]

1. **长时运行** — Agent 可能跑十分钟、半小时持续输出中间结果，"请求-响应"模型无法处理持续数据流
2. **输出不确定性** — 每次运行可能给出不同结果甚至生成不同 UI，前端无法写死界面
3. **混合 IO** — 文字、语音、工具调用、状态更新同时在跑，格式完全不同
4. **人类参与** — Agent 需要暂停下来让用户确认、修改、拒绝，然后继续

AG-UI 在这条缝隙里立了一套标准化的事件流协议。

## 16 种标准事件类型

| 分类 | 事件 | 说明 |
|------|------|------|
| 生命周期 | RunStarted, RunFinished, RunError, StepStarted, StepFinished | Agent 在干什么、做完了没、出错了没 |
| 文本消息 | TextMessageStart, TextMessageContent, TextMessageEnd | "Agent 在说话"的基础事件流 |
| 工具调用 | ToolCallStart, ToolCallArgs, ToolCallEnd, ToolCallResult | 前端实时看到 Agent 调了什么工具、传了什么参数、返回了什么结果 |
| 状态管理 | StateSnapshot, StateDelta | Agent 和前端共享状态，前端实时同步内部状态 |
| 推理 | ReasoningStart, ReasoningMessageContent, ReasoningEnd | 把 Agent 思考过程可视化，不暴露原始思维链 |
| 特殊 | Raw, Custom | 自定义场景的扩展口 |

这套事件体系建立在 **HTTP 和 WebSocket** 之上，支持 SSE（Server-Sent Events）流式传输和 Webhook 等多种传输方式。

## 生态支持

### 三大云厂商原生支持

- **Google** — ADK（Agent Development Kit）原生支持 AG-UI，有文档和 demo
- **Microsoft** — Agent Framework（MIT 协议）将 AG-UI 作为官方推荐的前端交互协议
- **AWS** — Strands Agents 和 Bedrock AgentCore 两个产品线均集成

### 主流框架支持

LangGraph、CrewAI、Mastra、Pydantic AI、Agno、LlamaIndex、AG2、Oracle Agent Spec 等框架均在支持列表中。OpenAI Agent SDK 和 Cloudflare Agents 正在适配中（标注为"进行中"）。

### SDK 语言覆盖

TypeScript、Python、Kotlin、Go、Dart、Java、Rust 已发布；.NET 和 Nim 开发中。

## Generative UI（生成式 UI）

AG-UI 提出的一个前沿概念——让 Agent 自己决定在界面上展示什么组件，而非前端把所有界面写死。借助 AG-UI 的状态同步和事件机制，这一概念正在变得可行。当前仍在 Draft 提案阶段。^[raw/articles/ag-ui-protocol-intro.md]

## 项目状态

| 指标 | 数据 |
|------|------|
| GitHub Stars | 13,400+ |
| 提交数 | 1,600+ |
| 首次开源 | 2025 年 5 月 |
| 首个正式 release | 2026 年 3 月 28 日 |
| 发布节奏 | 8 个版本 / 约 1 个月（三五天一新版） |
| 资金背景 | CopilotKit 获 2700 万美元 A 轮（Glilot Capital / NFX / SignalFire） |

协议仍在快速演进中，Generative UI、Meta Events、A2UI 等处于 Draft 阶段，尚未完全定型。^[raw/articles/ag-ui-protocol-intro.md]

## 值得关注的争议点

- **OpenAI 态度暧昧** — Agent SDK 标为"进行中"，以 OpenAI 自有前端方案来看，接受程度可能没那么无条件
- **前端协议天生困难** — 后端协议（MCP）工具调用格式可标准化，但前端交互需求差异巨大（客服 Agent vs 编程助手的界面完全不同），AG-UI 能在多大程度上真正统一"Agent 和人之间的交互"有待观察

## 相关条目

- [[hermes-agent]] — 已集成 MCP，是 AG-UI 的潜在应用场景
- [MCP 协议](https://modelcontextprotocol.io/) — Agent 工具层协议
- [A2A 协议](https://github.com/google/A2A) — Agent 协作层协议
