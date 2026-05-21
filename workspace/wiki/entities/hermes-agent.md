---
title: Hermes Agent
created: 2026-05-06
updated: 2026-05-14 2026-05-10
type: entity
tags: [model, agent, tool, open-source]
sources:
  - raw/articles/hermes-15-overlooked-capabilities.md
  - raw/articles/hermes-agent-docs-overview-2026-05-06.md
  - raw/articles/hermes-agent-soulmd-tony-simons.md
  - raw/articles/hermes-agent-kanban-feature.md
  - raw/articles/tinyfish-free-search-fetch-api-yuanxiaoer.md
  - raw/articles/hermes-auto-wiki-workflow-yutou.md
  - raw/articles/hermes-agent-deep-dive-series-agent-observer.md
  - raw/articles/hermes-agent-profile-guide-muse.md
  - raw/articles/hermes-comfyui-skill-wechat.md
  - raw/articles/hermes-agent-config-guide-achao.md
  - raw/articles/hermes-agent-tool-system-zhineng-sibian.md
  - raw/articles/hermes-agent-self-evolution-yiqi.md
  - raw/articles/hermes-agent-intro-kim-surely.md
  - raw/articles/hermes-memory-tuning-practical.md
  - raw/articles/hermes-agent-deep-analysis-yugong.md
  - raw/articles/hermes-agent-per-provider-proxy.md
  - raw/articles/hermes-agent-v0.13.0-tenacity.md
  - raw/articles/hermes-agent-practical-guide.md
  - raw/articles/hermes-memory-three-rules.md
  - raw/articles/supply-chain-attack-mistralai-hermes-20260513.md
  - raw/articles/hermes-v0.13.0-tenacity-20260509.md
confidence: high
updated: 2026-05-11
---

# Hermes Agent

Hermes Agent 是由 [[Nous Research]] 构建的自主 AI 代理，具备内置的学习循环。与普通的编码助手或聊天机器人封装不同，它是一个随时间推移不断增长能力的**自主代理**。

## 关键特性

- **闭环学习**：Agent 策划的记忆、周期性推动、自主技能创建、使用过程中的技能自我改进、基于 FTS5 的跨会话召回（含 LLM 摘要）以及 Honcho 辩证用户建模
- **运行于任何环境**：6 种终端后端 — local、Docker、SSH、Daytona、Singularity、Modal。Daytona 和 Modal 支持无服务器持久化（空闲时休眠，成本趋近于零）
- **无处不在的消息通道**：CLI、Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Mattermost、Email、SMS、DingTalk、Feishu、WeCom、BlueBubbles、Home Assistant、Microsoft Teams — 单个网关覆盖 15+ 平台
- **68+ 内置工具** — 包含搜索、提取、浏览、视觉、图像生成、TTS 等
- **MCP 集成** — 连接任何 MCP 服务器以扩展工具集
- **外部搜索/抓取** — 通过 [[tinyfish]] 等 MCP Server 补足互联网信息获取能力，实现自主搜索和网页内容抓取 ^[raw/articles/tinyfish-free-search-fetch-api-yuanxiaoer.md]
- **语音模式** — CLI、Telegram、Discord、Discord VC 中的实时语音
- **多媒体生成（ComfyUI Skill）** — 通过 [[comfyui-skill]] 实现文生图、图生图、视频生成、音频生成、链式工作流编排。一句话驱动 ComfyUI 的全部能力 ^[raw/articles/hermes-comfyui-skill-wechat.md]
- **定时自动化** — 内置 Cron 调度，支持投递到任意平台
| 子代理并行 — 生成隔离的子代理处理并行工作流。通过 `execute_code` 实现程序化工具调用，将多步管道压缩为单次推理调用
|- **开放标准技能** — 兼容 agentskills.io，技能可移植、可共享，通过 Skills Hub 社区贡献
|- **视频分析**（v0.13.0）— `video_analyze` 工具，支持通过 Gemini 等多模态大模型原生视频解析
|- **语音克隆**（v0.13.0）— 接入 xAI Custom Voices 作为 TTS 提供商，原生支持语音克隆
|- **国际化**（v0.13.0）— CLI 和网关提示信息支持 7 种语言（含简体中文），官方文档新增中文版
|- **20 个接入平台**（v0.13.0）— 新增 Google Chat，Provider 插件化接口
|- **Cron 看门狗模式**（v0.13.0）— `no_agent` 模式，纯后台监控巡检脚本

## SOUL.md：核心身份文件

SOUL.md 是 Hermes Agent 实例的**核心身份文件**，定义了代理的语气、个性、沟通方式、直接程度、分歧处理和模糊问题的默认处理方式。独立开发者 [[tony-simons]] 将其实践总结为七大模块：

### 1. 身份定义
> "You are Hermes, Tony's autonomous operator and thought partner."

定义角色不是客服或秘书，而是**参与工作的人**（自主操作者和思考伙伴）。

### 2. 主动性
> "You don't wait for orders. Surface opportunities, flag problems, push work forward."

不等命令，主动发现机会、标记问题、推动工作。

### 3. 反驳规则（Pushback）
> "Push back aggressively when it makes sense. Every objection comes with evidence."

必须反驳但不能为反驳而反驳。每次反对带证据（数据、例子、推理）。

### 4. 责任闭环
> "If Tony isn't acting on what you surface, the feedback loop is broken."

输出未被行动接住时，要么提醒人，要么改进产出。防止 AI 产出变成"内容垃圾场"。

### 5. 场景化语气
- **私下**：Casual, authoritative, unfiltered（直接、不加修饰）
- **公开**：Write like someone who builds things（像一个真正做事的人写的）

### 6. 任务地图
维护当前目标、优先级、活跃项目、停滞项目的状态。Agent 不需要每次追问"我们现在在做什么"。

### 7. 授权边界
> "Never without explicit approval: posting, publishing, purchasing, destructive changes. Everything else: move."

红线极简单：发布/购买/不可逆破坏必须批准。其他事有事实依据就直接行动。

详见：[[soulmd-core-identity]] 及原始文章 `raw/articles/hermes-agent-soulmd-tony-simons.md`。

## Kanban：多 Agent 任务流水线

v0.12.0 推出的持久化看板系统，将多 Agent 协作从"子任务分发"升级为"有状态、有依赖、有历史、可重试的任务流水线"。

**v0.13.0 增强（Tenacity Release）：**
- **防幻觉网关（Hallucination gate）**：审查 Worker 提交的任务成果，防止"糊弄"完成
- **心跳监控 + 僵尸节点检测**：Heartbeats / Zombie detection / Reclaim 机制
- **Cron 看门狗模式**：`no_agent` 模式，纯后台监控脚本不唤醒 Agent
- **/goal 持久目标锁定**：Agent 硬性锁定在一个目标上，Ralph Loop 作为一级原语

详见 [[hermes-kanban-workflow]]。^[raw/articles/hermes-agent-v0.13.0-tenacity.md]

## 多 Profile 机制

Hermes Agent 支持通过 **profile** 创建多个独立 Agent 实例，每个拥有独立的配置、记忆、技能和任务边界。详见 [[hermes-profile-system]]。

## 典型用例：自动知识库工作流

Hermes Agent 可与 [[AutoCLI（OpenCLI）]]、[[llm-wiki]] skill、微信渠道组合，构建全自动知识库流水线：定时抓取信息 → 编译入库（Karpathy LLM Wiki） → 微信日报推送。详见 [[hermes-auto-wiki-workflow]]。

## 与 OpenClaw 的关系

[[OpenClaw]] 与 Hermes Agent 同属开源 AI Agent 生态，在 Skill 体系（SKILL.md / agentskills.io）、多平台网关、浏览器操作等方向理念相似。Hermes Agent 的 Skills Hub 与 OpenClaw 的 [[ClawHub]] 互为参照。

## 架构

六种终端后端、统一消息网关、技能系统、记忆系统、MCP 集成、子代理委派和基于 Cron 的调度。

## 部署选项

- $5 VPS
- GPU 集群
- 无服务器基础设施（Daytona、Modal）— 空闲时几乎零成本

## 组织背景

由 [[Nous Research]]（Hermes、Nomos、Psyche 模型团队）构建。支持 Nous Portal、OpenRouter、OpenAI 或任何兼容端点。

## 深度技术拆解

[[Agent 观察者]] 撰写了目前公开渠道最完整的 Hermes Agent 第三方技术分析（23 讲专栏），涵盖：

**基础篇**：三层架构、200+ 模型统一接入（4 路 Provider / Smart Model Routing / 故障转移 / 凭证池轮换）、工具系统 Registry 模式、Agent 主循环（IterationBudget / 并行工具调用 / 空响应恢复）

**核心篇**：[[hermes-agent-memory-system]]（冻结快照 + 8 种 Memory Provider + Nudge 机制）、[[agent-skills-system]]（SKILL.md 格式 + 4 级信任 + _spawn_background_review）、[[soulmd-core-identity]]、[[hermes-kanban-workflow]]

**安全篇**：[[hermes-security-model]]（7 层防线 + 120 条威胁正则 + 智能审批 + 6 种沙箱后端 + 供应链投毒事件分析 [[supply-chain-attack-mistralai-hermes]]）

**多平台篇**：[[hermes-gateway-architecture]]（gateway/run.py + session_key + home channel）

**进阶篇**：MCP 集成（2500+ 行 mcp_tool.py + OAuth 2.1 PKCE + OSV 扫描）、长会话治理（上下文压缩 + Token 追踪）

详见 `raw/articles/hermes-agent-deep-dive-series-agent-observer.md`。

## 配置体系

Hermes Agent 提供两套配置路径：**Quick Setup**（三要素：Provider + Model + Messaging）和 **Full Setup**（全部配置项）。配置存储于 `~/.hermes/` 目录下，遵循 CLI 参数 → config.yaml → .env → 内置默认值的优先级链。

核心配置结构：`config.yaml`（非敏感）、`.env`（API Keys）、`auth.json`（OAuth）、`SOUL.md`（身份定义）、`memories/`、`skills/`、`cron/`、`sessions/`、`logs/`。

Terminal Backend 五级推荐路径：local → Docker → SSH → Modal → Daytona。Gateway 多平台接入需配置 allowed_users 白名单。

详见 [[achao]] 的配置指南。

### 按 Provider 独立配置代理

Hermes Agent 支持在 `config.yaml` 中按 Provider 独立设置代理，解决 OpenAI/OpenRouter（需走代理）与 MiniMax 等国内 API（直连更快）共存的网络需求。^[raw/articles/hermes-agent-per-provider-proxy.md]

**配置方式：** 在 `~/.hermes/config.yaml` 中添加 `model_providers:` 节点：

```yaml
model_providers:
  openai-codex: http://127.0.0.1:7897   # OpenAI 走代理
  openrouter: http://127.0.0.1:7897     # OpenRouter 走代理
  # 未配置的 Provider（如 minimax-cn）自动直连
```

**支持的代理协议：** HTTP、HTTPS、SOCKS5。

**架构链路：** `config.yaml` → `config.py`（读取 model_providers）→ `run_agent.py`（_create_openai_client() 中 15 行注入逻辑）→ `httpx.Client`（proxy 参数）。保存配置后直接使用，无需重启。

**Clash Verge Rev 注意：** 默认端口 HTTP=7897，SOCKS=7891（非 7890）。

## 工具系统架构

Hermes Agent 的工具系统分为四层：**Tool**（单个能力）、**Toolset**（分组）、**Plugin**（运行时扩展）、**Skill**（操作知识）。每层职责分离，通过 registry 注册、model_tools.py 发现、get_tool_definitions() 过滤并暴露给模型。

工具注册发生在模块 import 时（每个 tools/*.py 自注册），三轮发现（内置→MCP→Plugin）保证容错。详见 [[hermes-tool-system]]。

## 自进化机制

Hermes Agent 的"自进化"通过在线（上下文层）和离线（RL 训练层）两条路径实现。在线路径包括：system prompt 分层构建（稳定缓存前缀+临时注入）、Memory 冻结快照（MEMORY.md/USER.md）、Skill 自动生成（后台复盘→固化为 SKILL.md）、Cron 周期性推动。离线路径将 rollout 导出为 trajectory 经 verifier + reward 验收后送 Atropos 训练。详见 [[hermes-self-evolution]]。

## 研究与可扩展性

支持批处理、轨迹导出、使用 Atropos 进行强化学习训练。

## 行业框架：Harness Engineering 视角

2026 年 AI 行业提出 **Harness Engineering（线束工程）** 理念——大模型已非瓶颈，约束与环境才是关键。Hermes Agent 被视为首款"出厂自带缰绳"的智能体，将五大组件自动化、产品化：^[raw/articles/hermes-agent-deep-analysis-yugong.md]

| 组件 | Hermes 实现 |
|------|------------|
| 指令层 | Skill 自动生成与迭代 |
| 约束层 | 工具权限 + 沙箱隔离 + 7 层安全防线 |
| 反馈层 | 自学习闭环自动复盘 |
| 记忆层 | 三层记忆（会话/持久/技能）+ Honcho 用户建模 |
| 编排层 | 子智能体委派 + Cron 定时调度 |

### 与 OpenClaw 的核心差异

| 维度 | Hermes Agent | OpenClaw |
|------|-------------|----------|
| 核心理念 | 自改进学习循环 | 配置即行为 |
| 技能维护 | 自动创建 + 自我优化 | 人工编写维护 |
| 记忆体系 | 三层自进化记忆 | 人工维护为主 |
| 运行模式 | 24h 后台常驻 | 按需启动 |
| 生态 | 自研 Skill + 通用标准 | ClawHub 海量 Skill |

**一句话概括：** OpenClaw 是被驯养的助手（"你养 AI"），Hermes 是会自我成长的伙伴（"AI 自我成长"）。三者（含 [[Claude Code]]）并非替代关系——Claude Code 专注实时编码，OpenClaw 适合标准化部署，Hermes 适合长期自动化与个性化需求。^[raw/articles/hermes-agent-deep-analysis-yugong.md]

### 社区数据

| 截至 2026 年 5 月，Hermes Agent GitHub 星标已突破 **117,000+**（逼近 14 万），内置工具 **68+**，接入平台 **20+**（含微信、飞书、QQ、Telegram、Google Chat 等），通过 MCP 协议可联动 **6,000+** 外部应用。内存占用低于 500MB，MIT 协议完全开源。^[raw/articles/hermes-agent-deep-analysis-yugong.md] ^[raw/articles/hermes-agent-v0.13.0-tenacity.md]

### 实战使用原则

[[求索深思]] 撰写了 Hermes Agent 实战应用指南，总结出高效使用的核心原则 ^[raw/articles/hermes-agent-practical-guide.md]：

- **前置上下文，减少来回**：一次说清问题（路径、错误信息、预期效果），胜过三轮追问
- **让 Agent 用自己的工具**：告诉它「找到并修复失败的测试」而非「打开 test_foo.py 看第 42 行」
- **善用 AGENTS.md**：反复告知的约定（缩进风格、测试框架、API 路径）写进文件，一劳永逸
- **主动触发技能创建**：复杂任务完成后用「把你刚才做的保存为 skill X」
- **选对模型做对事**：`/model` 随时切换，复杂推理用 Claude Sonnet/Opus，简单任务用 Gemini Flash
- **用 delegate_task 处理并行**：多个调研方向用委派并行，子 Agent 只返回摘要

此外还提供了四个实战案例（自动日报、GitHub Issue 监控、内容创作助手、代码审查）和详细的费用对比。Hermes 月费约 5-10 美元，比 OpenClaw 便宜 30%-60%，记忆调用成本稳定不递增。^[raw/articles/hermes-agent-practical-guide.md]


## v0.13.0 韧性版更新（2026-05）

代号「Tenacity」。解决两大痛点：任务中途卡死、多轮对话跑偏。四大模块：Kanban 多智能体看板（心跳检测+僵尸检测+幻觉门控）、/goal Ralph Loop 目标锁定、Recovery Checkpoints v2 崩溃恢复、8个P0安全修复（含敏感信息自动脱敏、提示词注入扫描）。详见 [[hermes-v0.13.0-tenacity]]。^[raw/articles/hermes-v0.13.0-tenacity-20260509.md]

## 安全事件：MistralAI 供应链投毒（2026-05）

2026年5月11-12日，PyPI 包 `mistralai` 2.4.6 被植入 credential stealer，`import` 即触发，窃取所有环境变量凭据。属于 Mini Shai-Hulud 供应链攻击一部分，同期PyPI 3个包+npm 170+包受影响。攻击者打穿的是发布链路而非终端用户——恶意版本无对应 GitHub tag/commit，却挂载在 PyPI 官方包名之下。核心教训：Agent 自动化安装变成攻击高速公路；环境变量全暴露是致命弱点。详见 [[supply-chain-attack-mistralai-hermes]]。^[raw/articles/supply-chain-attack-mistralai-hermes-20260513.md]

## 高级能力（来自王二的15项总结）

- **SOUL.md + /personality**：长期人格配置，非一次性Prompt
- **MEMORY.md + USER.md**：跨会话记忆，FTS5+LLM摘要检索
- **/insights**：Agent使用行为可观测性
- **/snapshot**：配置版本管理，可回滚
- **多模型路由**：按任务选模型，成本优化
- **多平台触达**：Telegram/微信/Discord/Slack等15+渠道
- **Cron + Webhook**：定时主动执行 + 事件驱动
- **Skills as slash commands**：把重复工作沉淀为可复用命令

详见 [[wanger]] 的深度总结。
