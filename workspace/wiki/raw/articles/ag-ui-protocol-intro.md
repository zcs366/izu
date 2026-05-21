---
source_url: https://mp.weixin.qq.com/s/OmFQ55nLsNKwbJ5bB9XTnQ
ingested: 2026-05-10
sha256: 10c03275ec97e49daa27e319e98925b6789017bded0c130a523630940378d966
title: 三大巨头站台，AI Agent 前端标准要统一了？
author: i龙虾
description: AG-UI 协议深度解读——连接 AI Agent 和用户界面的开源协议，MCP/A2A/AG-UI 三层协议格局
---

今天刷到一条推文，说 Google ADK、Microsoft Agent Framework、AWS 三大巨头全部原生支持了一个叫 AG-UI 的协议。我当时的第一反应是：这什么来头，居然能让这三家同时站台？

于是我花了两天时间把 AG-UI 的文档、GitHub、博客、社区讨论全扒了一遍。说实话，越看越觉得这件事值得认真聊聊。因为如果你在做 AI Agent 相关的产品，AG-UI 很可能就是你绕不开的那个"最后一公里"。
先说清楚 AG-UI 到底是什么
简单一句话：AG-UI 是一个开源的、基于事件流的轻量协议，专门用来连接 AI Agent 和用户界面。

你可能用过 MCP（Model Context Protocol），Anthropic 搞的那个，让 Agent 能调用外部工具和数据源。你也可能听过 A2A（Agent to Agent），Google 推的，让 Agent 之间能互相通信。

AG-UI 补的是第三个缺口——Agent 和人之间的交互。

把这三个协议放一起看，画面就很清晰了：

• MCP 解决的是 Agent 怎么用工具

• A2A 解决的是 Agent 怎么跟别的 Agent 协作

• AG-UI 解决的是 Agent 怎么跟人打交道

这三个协议不是竞争关系，是互补的。一个 Agent 可以同时跑这三个协议，各管各的层。
谁搞的？CopilotKit
AG-UI 背后是 CopilotKit，一家做 Agent 前端基础设施的创业公司。5 月 5 号他们刚拿了 2700 万美元 A 轮融资。

但 AG-UI 不是 CopilotKit 的"自家玩具"。它在 2025 年 5 月开源，GitHub 上已经有 13,400 多颗星，1,600 多次提交。更重要的是，它最初是 CopilotKit 跟 LangGraph 和 CrewAI 合作搞出来的，然后才推向了更广泛的生态。

现在 AG-UI 的 SDK 已经有 TypeScript、Python、Kotlin、Go、Dart、Java、Rust 这几种语言版本，.NET 和 Nim 还在开发中。
为什么需要 AG-UI？传统 API 不够用
这个问题我之前也没细想。直到我去读了 AG-UI 的文档才意识到，传统 REST/GraphQL API 在 Agent 场景下确实有硬伤：

Agent 是长时运行的。你问它做一件事，它可能跑十分钟、半小时，中间一直在输出中间结果。传统的"请求-响应"模型根本没法处理这种持续的数据流。

Agent 的输出是不确定的。每次运行可能给出不同的结果，甚至生成不同的 UI。你没法像传统前端那样把界面写死。

Agent 同时混合结构化和非结构化的 IO。文字、语音、工具调用、状态更新，这些东西同时在跑，而且格式完全不同。

Agent 需要人类参与。不是说你丢个指令它就闷头干完了，很多时候它需要暂停下来，让你确认一下、改一下、甚至拒绝一下，然后继续。

这些需求堆在一起，靠传统的 API 就接不住了。AG-UI 做的事情，就是在这个"Agent 和用户之间"的缝隙里，立了一套标准化的事件流协议。
16 种事件类型，定义 Agent 和人怎么说话
AG-UI 定义了大约 16 种标准事件类型，按功能可以分成几大类：

生命周期事件：RunStarted、RunFinished、RunError、StepStarted、StepFinished。这些告诉你 Agent 在干什么、做完了没、出错了没。

文本消息事件：TextMessageStart、TextMessageContent、TextMessageEnd。这是最基础的"Agent 在说话"的事件流。

工具调用事件：ToolCallStart、ToolCallArgs、ToolCallEnd、ToolCallResult。Agent 在调工具的时候，前端可以实时看到调了什么工具、传了什么参数、返回了什么结果。

状态管理事件：StateSnapshot、StateDelta。Agent 和前端之间可以共享状态，前端能实时同步 Agent 的内部状态。

推理事件：ReasoningStart、ReasoningMessageContent、ReasoningEnd。你可以把 Agent 的思考过程可视化出来，但不会暴露原始的思维链。

另外还有 Raw、Custom 这类特殊事件，给自定义场景留了口子。

这套事件体系建立在 HTTP 和 WebSocket 之上，既可以用 SSE（Server-Sent Events）流式传输，也支持 Webhook 等其他传输方式。
三巨头为什么都选了 AG-UI
这才是最值得琢磨的部分。

微软在 2025 年 10 月开源了 Agent Framework（MIT 协议），支持 Python 和 .NET 两种语言。他们把 AG-UI 作为官方文档推荐的前端交互协议。

Google 的 ADK（Agent Development Kit）也原生支持 AG-UI，有文档和 demo。

AWS 更狠，Strands Agents 和 Bedrock AgentCore 两个产品线都集成了 AG-UI。Bedrock AgentCore 的 AG-UI 运行时文档在 AWS 官网上已经可以查到了。

除了这三大云厂商，LangGraph、CrewAI、Mastra、Pydantic AI、Agno、LlamaIndex、AG2、Oracle Agent Spec 这些框架也都在支持列表里。OpenAI 的 Agent SDK 和 Cloudflare Agents 正在适配中。

你看，连 OpenAI 都在"进行中"，还没做完。

这种"全行业跟进"的阵仗，上一次见到还是 MCP 刚出来的时候。只不过 MCP 解决的是 Agent 的工具层，AG-UI 解决的是 Agent 的用户层——前者在后端，后者在前端，两个都不可少。
AG-UI 和 MCP 到底是什么关系
很多人一看到"协议"就紧张，觉得是不是又要搞一个标准战争。

不是的。

AG-UI 已经加了"握手"机制，能让 AG-UI 的前端直接对接 MCP 和 A2A 支持的 Agent。也就是说，你用 AG-UI 做前端，Agent 后端可以同时走 MCP 接工具、走 A2A 跟其他 Agent 通信，三者完全不冲突。

打个比方的话——MCP 是让 Agent 拿起了螺丝刀和扳手，A2A 是让 Agent 之间能打电话协调，AG-UI 是给 Agent 和人之间装了一部双向对讲机。
对开发者意味着什么
如果你在做 AI Agent 的前端，AG-UI 最大的好处是：你不用为每个 Agent 框架单独写一套交互逻辑了。

以前你接 LangGraph 的 Agent，得按 LangGraph 的方式来；接 CrewAI 的，又得换一套。现在只要大家都走 AG-UI，前端代码基本可以复用。

AG-UI 的 TypeScript SDK 已经很成熟了，Python SDK 也能用。他们的快速启动命令就一行：

npx create-ag-ui-app my-agent-app

另外，AG-UI 还提出了一个"Generative UI"（生成式 UI）的概念——让 Agent 自己决定在界面上展示什么组件，而不是前端把所有界面写死。这件事以前听起来很科幻，但有了 AG-UI 的状态同步和事件机制，它正在变得可行。
几个值得注意的细节
CopilotKit 刚拿了 2700 万 A 轮，领投方是 Glilot Capital、NFX 和 SignalFire。钱到位了，意味着 AG-UI 的维护和迭代不会缺资源。

GitHub 13,400 星。这个数字不算炸裂（毕竟 MCP 出来的时候更快），但对于一个专注于"前端交互层"的协议来说，已经相当不错了。

发布节奏很快。从 2026 年 3 月 28 号第一个正式 release 到现在，一个多月时间已经发了 8 个版本，几乎每隔三五天就有一个新版本出来。

协议还在快速演进中。Generative UI、Meta Events、A2UI 这些概念目前还在 Draft 提案阶段。AG-UI 还没有完全定型，但方向已经很清楚了。
也有需要冷静看的地方
首先是 OpenAI 的态度。他们自己的 Agent SDK 在 AG-UI 的支持列表里标的是"进行中"，还没正式完成。考虑到 OpenAI 有自己的一套前端方案（ChatGPT 的界面和 API），他们对 AG-UI 的接受程度可能没那么无条件。

其次是"前端协议"这件事本身的挑战。后端协议（比如 MCP）的好处是，工具调用的格式是确定的，可以标准化。但前端交互的需求差异很大——一个客服 Agent 和一个编程助手的界面，几乎没什么共同之处。AG-UI 能在多大程度上真正统一"Agent 和人之间的交互"，还有待观察。

还有就是，这个领域变化太快。三个月前你可能觉得 CopilotKit 和 AG-UI 还只是一个小众项目，现在三大云厂商已经全部站台了。三个月后会怎样，谁也说不准。
最后说两句
AG-UI 目前是我见过的最合理的"Agent 前端标准"。它的定位精准（只管 Agent 到用户这一层），设计务实（基于现有 Web 基础设施），生态也够广（三大云厂商加十几个主流框架）。

它不像有些协议那样试图包揽一切，而是老老实实做好一个切面的事情。这种"各管一层、互相握手"的思路，反而可能走得更远。

如果你正在做 AI Agent 产品，我建议现在就开始关注 AG-UI。不是说马上就要用它——毕竟它还在快速迭代——但至少了解一下它的事件模型和架构思路，等到需要做 Agent 前端交互的时候，你会发现很多设计思路是通用的。

AI Agent 这个赛道还在早期。工具层有 MCP，协作层有 A2A，现在前端交互层也有了 AG-UI。三层协议各司其职，整个栈正在慢慢补齐。

