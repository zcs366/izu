# Hermes Agent 完整功能手册与操作指令集 v0.14.0

> **版本**: v0.14.0 (2026.5.16) · 代号: Foundation  
> **作者**: Nous Research · **协议**: MIT  
> **文档状态**: 基于本地部署环境整理（截至 2026-05-21）
> **一句话定义**: 开源、自改进、跨平台的 AI 代理框架，可运行于终端、消息平台和 IDE

---

## 目录

1. [概述与核心特性](#1-概述与核心特性)
2. [v0.14.0 版本亮点](#2-v0140-版本亮点)
3. [快速入门](#3-快速入门)
4. [CLI 指令全集](#4-cli-指令全集)
5. [会话中斜杠指令](#5-会话中斜杠指令)
6. [工具与工具集](#6-工具与工具集)
7. [配置详解](#7-配置详解)
8. [模型与提供商](#8-模型与提供商)
9. [Gateway 消息平台](#9-gateway-消息平台)
10. [Skills 技能系统](#10-skills-技能系统)
11. [Memory 记忆系统](#11-memory-记忆系统)
12. [Cron 定时任务](#12-cron-定时任务)
13. [Webhooks 与 ACP 集成](#13-webhooks-与-acp-集成)
14. [Profiles 多配置档案](#14-profiles-多配置档案)
15. [Kanban 多Agent看板](#15-kanban-多agent看板) ← **新**
16. [持久目标 /goal](#16-持久目标-goal) ← **新**
17. [安全与隐私](#17-安全与隐私)
18. [TUI 终端 UI](#18-tui-终端-ui)
19. [插件系统](#19-插件系统)
20. [MCP 服务器集成](#20-mcp-服务器集成)
21. **[工具生态图谱 — CLI · MCP · Skill 三件套](#21-工具生态图谱--cli--mcp--skill-三件套)** ← **🆕 本章**
22. [故障排除手册](#22-故障排除手册)
23. [未来展望](#23-未来展望) ← **新**
24. [附录：术语表](#附录：术语表)
---

## 1. 概述与核心特性

Hermes Agent 是 Nous Research 开发的开源 AI 代理框架，和 Claude Code、OpenAI Codex、OpenCode 属于同一品类——自主编码与任务执行代理，通过工具调用与系统交互。

### Hermes 的独特之处

| 特性 | 说明 |
|------|------|
| **自改进技能系统** | 解决复杂问题后自动保存流程为技能文档，下次自动加载，越用越好 |
| **跨会话持久记忆** | 记住你是谁、偏好、环境细节，支持 10+ 记忆后端（Holographic、Hindsight、RetainDB、Honcho、Mem0 等） |
| **多平台网关** | 同一代理在 Telegram、Discord、Slack、微信等 20 个平台运行，工具全功能 |
| **提供商无关** | 随时切换模型/提供商，凭据池自动轮换多个 API Key |
| **多配置档案** | 独立运行多个 Hermes 实例，各自持有隔离的配置、会话、技能、记忆 |
| **多Agent看板** | v0.13.0 新增：持久化看板，多个 Hermes 智能体协作完成复杂任务 |
| **持久目标** | v0.13.0 新增：跨轮锁定任务目标，Agent 不会跑偏 |
| **可扩展** | 插件、MCP 服务器、自定义工具、Webhook 触发器、Cron 调度、完整 Python 生态 |

### 核心架构速览

```
用户终端 / Telegram / Discord / Web / ...
         │
    ┌────▼─────────────────────┐
    │      Gateway 消息网关      │ ← 20个平台适配器
    └────────┬──────────────────┘
             │
    ┌────────▼──────────────┐
    │   AI Agent 核心循环      │ ← run_agent.py (AIAgent, ~12K LOC)
    │  - 工具调用调度          │
    │  - 上下文压缩           │
    │  - 记忆检索             │
    │  - 技能自动加载          │
    └────────┬──────────────┘
             │
    ┌────────▼──────────────┐     ┌────────────────────┐
    │  Tool Engine           │────▶│  插件系统           │
    │  工具调度/缓存/审批     │     │  记忆/提供商/平台/   │
    └────────┬──────────────┘     │  看板/图像生成等     │
             │                    └────────────────────┘
    ┌────────▼──────────────┐
    │  Terminal / Docker /   │
    │  SSH / Modal 执行环境    │
    └─────────────────────────┘
```

---

## 2. v0.14.0 版本亮点

> **代号**: Foundation（基石）—— 核心主题：**Hermes 安装即用，跑在任何地方**

**版本跨度**: 808 次提交 · 633 个合并 PR · 1393 个文件变更 · 545 个议题关闭（12 个 P0、50 个 P1） · 215 位社区贡献者

### 新特性一览

| 特性 | 一句话说明 | 适合谁 |
|------|-----------|--------|
| **PyPI 一键安装** | `pip install hermes-agent && hermes`，不用克隆仓库 | 新用户 |
| **xAI Grok OAuth** | SuperGrok 订阅直接登录，grok-4.3 升级到 1M 上下文 | Grok 用户 |
| **OpenAI 兼容本地代理** | `hermes proxy` 把 OAuth 提供商变 OpenAI 接口 | Claude Pro / ChatGPT Pro 用户 |
| **x_search 搜索工具** | 原生 X/Twitter 搜索工具 | 社媒运营/研究者 |
| **Microsoft Teams 全链路** | 从 Graph 认证到 Webhook 接收、双向通信完整打通 | 企业用户 |
| **LINE + SimpleX Chat** | 第21/22个消息平台，覆盖日韩台 | 跨国团队 |
| **冷启动提速 19 秒** | `hermes` 启动从等待变成秒开 | 所有用户 |
| **浏览器 eval 提速 180 倍** | CDP 持久连接替代每次重建会话 | 重度浏览器用户 |
| **LSP 语义诊断** | write_file/patch 后实时捕获类型错误、未定义符号 | 开发者 |
| **Native Windows 支持** | 原生支持 cmd.exe 和 PowerShell（早期 Beta） | Windows 用户 |
| **/handoff 实时会话移交** | 切换模型/人格时上下文不丢失 | 多模型用户 |

---

## 3. 快速入门

### 3.1 安装

Hermes Agent 支持多种安装方式（按难度排序）：

| 方法 | 难度 | 说明 |
|------|------|------|
| **PyPI 安装（推荐）** | ★☆☆ | `pip install hermes-agent && hermes` —— 官方推荐 |
| 一键脚本 | ★☆☆ | `curl -fsSL https://hermes.nousresearch.com/install.sh | sh` |
| 源码安装 | ★★★ | `git clone && cd hermes-agent && pip install -e .` |
| Windows 原生 | ★★☆ | 在 cmd.exe 或 PowerShell 中运行 `pip install hermes-agent`（早期 Beta） |

系统要求：

| 项目 | 最低 | 推荐 |
|------|------|------|
| OS | Linux / macOS / WSL2 / Windows (Beta) | Linux (Ubuntu 22.04+) |
| Python | 3.11+ | 3.11.10+ |
| 内存 | 512MB | 2GB+ |
| 磁盘 | 500MB | 5GB+（含模型缓存） |
| 网络 | 可访问 API 提供商 | 稳定的宽带连接 |

### 3.2 基础配置

```bash
# 运行初始化向导
hermes setup

# 设置 API Key（以 OpenRouter 为例）
hermes config set provider openrouter
hermes config set model openrouter/anthropic/claude-sonnet-4
export OPENROUTER_API_KEY="sk-or-PLACEHOLDERv1-..."

# 检查配置
hermes config show
```

### 3.3 启动交互会话

```bash
# CLI 模式（终端内直接对话）
hermes

# 启动 Gateway（连接消息平台）
hermes gateway start

# 启动 Dashboard（Web UI 管理界面）
hermes dashboard

# 启动 TUI（终端图形界面）
hermes --tui
```

### 3.4 第一个任务

```bash
# 进入 CLI 后
> 写一个 Python 脚本，计算斐波那契数列的前20项

# 或通过 Telegram 发送
/start
写一个 Python 脚本，计算斐波那契数列的前20项

# 用 /goal 锁定目标（v0.13.0 新特性）
/goal 完成一个 Flask 博客后端，包含 CRUD 和用户认证
```

---

## 4. CLI 指令全集

### 4.1 基础命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `hermes` | 启动交互式 CLI | `hermes` |
| `hermes --tui` | 启动终端 UI | `hermes --tui` |
| `hermes <指令>` | 直接执行单条指令后退出 | `hermes "列出当前目录"` |
| `hermes chat` | 同 `hermes`，启动 CLI | `hermes chat` |
| `hermes proxy` | 启动 OpenAI 兼容本地代理（v0.14.0 新） | `hermes proxy --port 8080` |

### 4.2 配置管理

| 命令 | 说明 |
|------|------|
| `hermes setup` | 交互式安装向导 |
| `hermes config show` | 显示当前配置 |
| `hermes config set <key> <value>` | 设置配置项 |
| `hermes config get <key>` | 读取配置项 |
| `hermes model` | 交互式模型选择器 |
| `hermes model list` | 列出可用模型 |
| `hermes model set <provider/model>` | 设置当前模型 |

### 4.3 会话管理

| 命令 | 说明 |
|------|------|
| `hermes sessions` | 列出所有会话 |
| `hermes resume <session_id>` | 恢复指定会话 |
| `hermes delete <session_id>` | 删除会话 |

### 4.4 Skills 管理

| 命令 | 说明 |
|------|------|
| `hermes skill list` | 列出所有已安装 skill |
| `hermes skill view <name>` | 查看 skill 内容 |
| `hermes skill create <name>` | 创建新 skill |
| `hermes skill edit <name>` | 编辑 skill |
| `hermes skill delete <name>` | 删除 skill |
| `hermes skills reset` | 重置所有 skill 到默认状态 |

### 4.5 Curator 技能整理（v0.13.0 增强）

| 命令 | 说明 |
|------|------|
| `hermes curator status` | 查看整理状态 |
| `hermes curator run` | 手动运行技能整理（v0.13.0 改为同步执行） |
| `hermes curator archive <name>` | 归档一个技能 |
| `hermes curator prune` | 修剪过时的技能 |
| `hermes curator list-archived` | 列出已归档的技能 |

### 4.6 Gateway 管理

| 命令 | 说明 |
|------|------|
| `hermes gateway start` | 启动 Gateway |
| `hermes gateway stop` | 停止 Gateway |
| `hermes gateway restart` | 重启 Gateway |
| `hermes gateway status` | Gateway 运行状态 |
| `hermes gateway list` | 跨 Profile 的 Gateway 状态（v0.13.0） |

### 4.7 更新与维护

| 命令 | 说明 |
|------|------|
| `hermes update` | 更新到最新版本 |
| `hermes update --yes` / `-y` | 静默更新（v0.13.0） |
| `hermes logs` | 查看日志 |
| `hermes logs --follow` | 实时日志 |
| `hermes debug share` | 分享调试信息（v0.13.0 自动脱敏） |

### 4.8 看板管理（新）

| 命令 | 说明 |
|------|------|
| `hermes kanban` | 看板管理入口 |
| `hermes kanban create <name>` | 创建新看板 |
| `hermes kanban list` | 列出所有看板 |
| `hermes kanban status` | 看板运行状态 |
| `hermes kanban specify <task-id>` | 用辅助 LLM 细化看板任务（v0.14.0） |
| `hermes kanban list` | 列出所有看板任务（v0.14.0） |
| `hermes kanban unblock <task-id>` | 手动解除卡住的任务（v0.14.0） |

### 4.9 其他

| 命令 | 说明 |
|------|------|
| `hermes doctor` | 诊断系统问题 |
| `hermes version` | 显示版本号 |
| `hermes help` | 显示帮助 |

---

## 5. 会话中斜杠指令

在 CLI / TUI / Gateway 会话中可使用以下 `/` 指令：

### 基础指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `/help` | 显示帮助 | `/help` |
| `/new` | 新会话（v0.13.0 可加名称） | `/new 项目研究` |
| `/reset` | 重置当前会话 | `/reset` |
| `/model` | 切换模型 | `/model claude-sonnet-4` |
| `/provider` | 切换提供商（v0.13.0 移除，改用 /model） | - |
| `/clear` | 清屏 | `/clear` |
| `/exit` | 退出 | `/exit` |

### 会话控制

| 指令 | 说明 |
|------|------|
| `/goal <目标>` | 设置持久目标（v0.13.0 新特性） |
| `/goal` | 查看当前目标 |
| `/goal clear` | 清除当前目标 |
| `/steer <指令>` | 引导当前运行的 Agent（ACP 模式） |
| `/queue <指令>` | 在 Agent 忙碌时排队任务 |
| `/stop` | 停止当前生成 |
| `/retry` | 重试最后一次生成 |
| `/save` | 保存当前会话 |
| `/branch` | 从当前会话分叉新会话 |
| `/history` | 显示历史记录 |
| `/handoff <model/profile>` | 实时移交会话给其他模型/人格（v0.14.0 新） |
| `/subgoal <条件>` | 给正在运行的 /goal 添加额外成功标准（v0.14.0 新） |
| `/platform` | 查看/切换消息平台（v0.14.0 新） |
| `/sessions` | 浏览和恢复历史会话（v0.14.0 新，TUI） |

### 工具控制

| 指令 | 说明 |
|------|------|
| `/tools` | 列出可用工具 |
| `/yolo` | 启用 YOLO 模式（跳过危险操作确认） |
| `/approve` | 批准待审批的工具调用 |

### 显示控制

| 指令 | 说明 |
|------|------|
| `/status` | 显示会话状态（模型、令牌数等） |
| `/tokens` | 显示令牌使用情况 |
| `/time` | 显示会话耗时 |
| `/info` | 显示系统信息 |

---

## 6. 工具与工具集

### 6.1 核心工具

| 工具 | 说明 | 类别 |
|------|------|------|
| `terminal` | 执行 shell 命令 | 执行 |
| `write_file` | 写入文件（v0.13.0 自动 lint） | 执行 |
| `read_file` | 读取文件 | 查询 |
| `patch` | 文件编辑（v0.13.0 自动 lint） | 执行 |
| `search_files` | 搜索文件内容/文件名 | 查询 |
| `web_search` | 网页搜索 | 查询 |
| `web_extract` | 网页内容提取 | 查询 |
| `vision_analyze` | 图像分析 | 多模态 |
| `video_analyze` | **视频分析（v0.13.0 新）** | 多模态 |
| `image_generate` | 图像生成 | 多模态 |
| `text_to_speech` | 文本转语音 | 媒体 |
| `delegate_task` | 派生子代理 | 编排 |
| `execute_code` | 执行 Python 代码 | 执行 |
| `memory` | 保存/读取记忆 | 记忆 |
| `todo` | 任务管理 | 编排 |
| `cronjob` | 定时任务管理 | 调度 |
| `process` | 后台进程管理 | 执行 |
| `skill_manage` | 技能管理 | 系统 |
| `fact_store` | 事实存储/查询 | 记忆 |
| `clarify` | 向用户提问 | 通信 |
| `send_message` | 跨平台发送消息 | 通信 |
| `browser_*` | 浏览器交互系列（导航、点击、截图等） | 浏览器 |

### 6.2 工具集

工具集是工具的命名分组，可按需启用/禁用：

| 工具集 | 包含工具 | 场景 |
|--------|---------|------|
| `web` | web_search, web_extract | 网络查询 |
| `terminal` | terminal, process | 系统操作 |
| `file` | read_file, write_file, patch, search_files | 文件操作 |
| `browser` | browser_* 系列 | 网页交互 |
| `x_search` | x_search | X/Twitter 搜索（v0.14.0 新） |
| `delegation` | delegate_task | 任务派发 |
| `vision` | vision_analyze, video_analyze, video_generate | 多模态分析/生成 |
| `image_gen` | image_generate | 图像生成 |
| `cronjob` | cronjob | 定时任务 |
| `kanban` | 看板相关 | 多Agent协作 |

---

## 7. 配置详解

### 7.1 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 主配置 | `~/.hermes/config.yaml` | YAML 格式，所有设置 |
| 环境变量 | `~/.hermes/.env` | API Key 等敏感信息 |
| 状态 | `~/.hermes/state.db` | SQLite 会话存储 |

### 7.2 核心配置项

```yaml
# ~/.hermes/config.yaml 示例
agent:
  provider: openrouter
  model: openrouter/anthropic/claude-sonnet-4
  max_iterations: 90
  quiet_mode: false
  save_trajectories: true

display:
  language: zh          # v0.13.0: 中文界面
  timezone: Asia/Shanghai

tools:
  enabled_toolsets: [web, terminal, file, browser, vision]
  disabled_toolsets: []
  
web:
  search_provider: searxng  # v0.13.0: 搜索/提取/浏览可分开配置
  extract_provider: firecrawl
  browse_provider: playwright

cron:
  enable: true

memory:
  provider: holographic   # 默认记忆后端

gateway:
  enable: true
  platforms:
    telegram:
      enabled: true
      bot_token: "..."
    discord:
      enabled: false
```

### 7.3 平台白名单（v0.13.0）

```yaml
gateway:
  platforms:
    telegram:
      allowed_chats: [-1001234567890]    # 仅允许指定群组
    slack:
      allowed_channels: [general, dev]   # 仅允许指定频道
    mattermost:
      allowed_rooms: [town-square]
```

---

## 8. 模型与提供商

### 8.1 支持提供商

| 提供商 | 模式 | 说明 |
|--------|------|------|
| OpenRouter | chat_completions | 统一接口，多模型可选 |
| Anthropic | chat_completions | Claude 系列 |
| OpenAI | chat_completions + responses | GPT 系列 |
| Google | chat_completions | Gemini 系列 |
| Nous Portal | chat_completions | Nous 自有 |
| xAI | chat_completions + OAuth | Grok 系列（v0.14.0 SuperGrok OAuth 登录，grok-4.3 1M 上下文） |
| NovitaAI | chat_completions | v0.14.0 新增：开源模型托管（Llama/Qwen/DeepSeek） |
| DeepSeek | chat_completions | DeepSeek 系列 |
| Qwen Cloud | chat_completions | 阿里通义千问（v0.14.0 更名） |
| Bedrock | chat_completions | AWS 托管 |
| 自定义 | chat_completions | 任意 OpenAI 兼容 API |

### 8.2 v0.14.0 新增模型/提供商

| 模型/提供商 | 说明 | 特点 |
|------------|------|------|
| `x-ai/grok-4.3` | SuperGrok OAuth | 1M 上下文窗口（v0.14.0） |
| `novitaai/*` | NovitaAI 提供商 | 开源模型托管 |
| `openrouter/pareto-code` | Pareto Code 路由器 | 自动选最便宜够用的模型 |

### 8.3 OpenRouter Pareto Code 路由器（v0.14.0 新）

自动选择成本最低但满足编码质量门槛的模型：

```yaml
openrouter:
  pareto_code:
    enabled: true
    min_coding_score: 0.7  # 0.0-1.0，越高越贵越聪明
```

### 8.4 OpenAI 兼容本地代理（v0.14.0 新）

`hermes proxy` 启动一个本地 HTTP 端点，把 Claude Pro、ChatGPT Pro、SuperGrok 等 OAuth 认证的提供商变成 OpenAI 兼容接口。Codex CLI、Aider、Cline、Continue 等工具可直接使用：

```bash
# 启动代理
hermes proxy --port 8080

# 其他工具现在可以通过 http://localhost:8080 调用
# 就像调用 OpenAI API 一样
```

### 8.5 凭据池

```yaml
credential_pools:
  my-pool:
    provider: openrouter
    keys:
      - sk-or-PLACEHOLDERv1-xxx
      - sk-or-PLACEHOLDERv1-yyy
    strategy: round_robin  # 自动轮换
```

---

## 9. Gateway 消息平台

### 9.1 支持平台（22个）

| 平台 | 状态 | 备注 |
|------|------|------|
| Telegram | ✅ 完整 | 含频道、群组、管理话题 |
| Discord | ✅ 完整 | 含角色白名单（v0.13.0 限定服务器） |
| Slack | ✅ 完整 | |
| WhatsApp | ✅ 完整 | v0.13.0 默认拒绝陌生人 |
| WeChat | ✅ 完整 | 微信个人号 |
| Signal | ✅ 完整 | |
| Matrix | ✅ 完整 | |
| Email | ✅ 完整 | IMAP/SMTP |
| SMS | ✅ 基础 | |
| Google Chat | ✅ **v0.13.0 新增** | 第19个平台 |
| QQBot | ✅ 完整 | v0.13.0 含审批键盘、分段上传 |
| 钉钉 | ✅ 完整 | |
| 飞书 | ✅ 完整 | |
| 企业微信 | ✅ 基础 | |
| Home Assistant | ✅ 基础 | |
| IRC | ✅ 基础 | |
| Teams | ✅ 基础 | v0.13.0 含侧栏+线程 |
| Webhook | ✅ 完整 | |
| API Server | ✅ 完整 | REST API |
| Mattermost | ✅ 完整 | |
| LINE | ✅ **v0.14.0 新增** | 日韩台主流 IM |
| SimpleX Chat | ✅ **v0.14.0 新增** | 隐私优先去中心化聊天 |
| Microsoft Teams | ✅ **v0.14.0 新增** | 全链路双向通信（Graph 认证+Webhook+双向） |

### 9.2 启动 Gateway

```bash
# 启动（前台）
hermes gateway start

# 查看状态
hermes gateway status

# 跨 Profile 状态（v0.13.0）
hermes gateway list

# 作为 systemd 服务
sudo systemctl start hermes-gateway
```

### 9.3 v0.14.0 Gateway 增强

| 特性 | 说明 |
|------|------|
| **Platform 电路断路器** | 单个平台故障不影响其他平台，自动隔离 |
| **`/platform` 命令** | 查看/切换当前消息平台 |
| **clarify 原生按钮** | Telegram 和 Discord 上选择题出现原生按钮，点一下就行 |
| **Discord 历史回溯** | 加入频道后自动读取近期消息历史，知道上下文 |
| **LINE 消息平台** | 第21个平台，覆盖日韩台用户 |
| **SimpleX Chat** | 第22个平台，去中心化无 ID 隐私聊天 |

### 9.4 会话中断自动恢复（v0.13.0）

Gateway 重启后（包括 `/update` 重启、源码重载），中断的会话自动恢复：

```yaml
# 无需额外配置
gateway:
  auto_resume: true  # 默认开启
```

### 9.5 国际化界面（v0.13.0）

Gateway + CLI 静态消息支持 16 种语言：

```yaml
display:
  language: zh  # zh (中文), ja (日语), de (德语), es (西班牙语), fr (法语), uk (乌克兰语), tr (土耳其语)
```

### 9.6 平台白名单

```yaml
gateway:
  platforms:
    telegram:
      allowed_chats: [聊天ID列表]     # 只响应指定聊天
    discord:
      allowed_roles: [角色ID列表]     # 限定服务器角色（v0.13.0 安全加固）
```

---

## 10. Skills 技能系统

### 10.1 什么是 Skill

Skill 是 Hermes Agent 最核心的独特特性——**可复用的流程文档**。完成复杂任务后，Agent 会自动将解决过程保存为 SKILL.md，下次遇到同类问题时自动加载。

### 10.2 Skill 格式

```yaml
---
name: my-skill
description: "技能描述"
version: 1.0.0
metadata:
  hermes:
    tags: [category, keyword]
    category: work-type
---

# Skill 名称

## When to Use
什么场景触发这个 Skill

## Steps
1. 第一步
2. 第二步

## Pitfalls
- 常见陷阱
```

### 10.3 Skill 管理

```bash
# 列出所有 Skill
hermes skill list

# 查看 Skill
hermes skill view my-skill

# 创建 Skill
hermes skill create my-skill

# 删除 Skill
hermes skill delete my-skill

# 重置内置 Skill
hermes skills reset
```

### 10.4 技能整理（Curator，v0.13.0 增强）

v0.13.0 新增归档和修剪子命令：

```bash
hermes curator run                     # 同步运行技能整理
hermes curator archive outdated-skill  # 归档不用的技能
hermes curator prune                   # 自动修剪
hermes curator list-archived           # 查看已归档
```

### 10.5 v0.14.0 Skills 增强

- **huggingface/skills 默认源** — 社区技能索引 huggingface.co/skills 自动可用，无需额外配置
- **9 个新可选技能** — Hyperliquid（交易）、Yahoo Finance（市场数据）、api-testing（API调试）、EVM 多链、darwinian-evolver（进化式提示优化）、osint-investigation（开源情报）、pinggy-tunnel（内网穿透）、watchers（RSS/HTTP/GitHub轮询）、Notion（开发者平台适配）
- **插件 `ctx.llm`** — 插件可以直接通过活跃提供商调用 LLM，无需手动连接客户端
- **插件 `tool_override`** — 插件可替换内置工具的实现

### 10.6 [[as_document]] 指令（v0.13.0 新）

Skill 可指定输出以文档形式发送，而非普通消息：

```markdown
---
name: report-skill
---

[[as_document]]

# 报告内容
...（输出将作为文件发送）
```

---

## 11. Memory 记忆系统

### 11.1 支持后端

| 后端 | 特点 | 适用场景 |
|------|------|---------|
| **Holographic** | 实体解析 + 可信度评分 | 默认推荐 |
| **Hindsight** | 跨进程探针去重（v0.13.0） | 高并发场景 |
| **RetainDB** | 持久化存储 | 需要长期记忆 |
| **Honcho** | 云端记忆 | 分布式部署 |
| **Mem0** | 智能记忆管理 | 进阶用户 |
| **Supermemory** | 企业级 | 大规模 |
| **Byterover** | 轻量级 | 嵌入设备 |
| **OpenViking** | 探索型 | 实验 |

### 11.2 配置

```yaml
memory:
  provider: holographic  # 默认
```

### 11.3 持久目标与记忆

v0.13.0 的 `/goal` 系统与记忆系统协同工作：目标信息保存在会话中，跨轮保持不丢失。

---

## 12. Cron 定时任务

### 12.1 基础用法

```bash
# 创建定时任务（当前会话自动交付）
hermes 创建定时任务，每天早上9点告诉我今日待办

# 或通过 cronjob 工具
/cron create "每日简报" "0 9 * * *" "读取今天的日历事件并总结"
```

### 12.2 no_agent 模式（v0.13.0 新）

纯脚本模式，不经过 LLM 代理，适合监控/检查：

```bash
# 创建 no_agent 看门狗任务
cronjob create \
  --schedule "*/5 * * * *" \
  --script ~/.hermes/scripts/disk_check.sh \
  --no-agent \
  --name "磁盘监控"
```

特点：
- 脚本 stdout 为空 → 静默（不发送任何消息）
- 脚本有输出 → 原样交付
- 脚本出错 → 发送错误通知
- 零令牌消耗

### 12.3 context_from 链式调用

```yaml
# Job A 收集数据 → Job B 处理数据
# 在 Job B 的 context_from 中引用 Job A
cron:
  jobs:
    - name: data-collector
      schedule: "0 */6 * * *"
      script: collect.py
      no_agent: true
    - name: data-analyzer
      schedule: "0 7 * * *"
      context_from: [data-collector]
      prompt: "分析上一份数据"
```

### 12.4 v0.14.0 Cron 增强

| 特性 | 说明 |
|------|------|
| **deliver=all** | 一个任务同时发送到所有已连接的消息平台 |
| **名称查找** | 支持按名称引用 cron 任务，不必记住 ID |
| **提示注入扫描** | 自动扫描组装后的 prompt（含 skill 内容）中的注入代码 |

---

## 13. Webhooks 与 ACP 集成

### 13.1 Webhook Server

```bash
# 启动 webhook 接收端
hermes webhook start --port 8080

# 配置 webhook
hermes webhook add --url https://example.com/hook --events message,tool_call
```

### 13.2 ACP (Agent Communication Protocol)

ACP 使 Hermes 能在 IDE 中作为编码助手运行：

| 集成方式 | 状态 |
|---------|------|
| VS Code | ✅ ACP Client 扩展 |
| Zed | ✅ 原生支持 |
| JetBrains | ✅ ACP 插件 |

v0.13.0 新增 `/steer` 和 `/queue` 指令：

- `/steer <提示>` — 在 Agent 忙碌时引导它
- `/queue <提示>` — 排队后续任务

### 13.3 API Server

```bash
hermes api-server start --port 8000
```

v0.13.0 新增 `X-Hermes-Session-Key` 请求头，为记忆提供商提供稳定的会话标识符。

---

## 14. Profiles 多配置档案

### 14.1 概念

Profile 是完全隔离的 Hermes 实例——不同 Profile 有各自的配置、会话、技能、记忆、凭据。

```bash
# 创建新 Profile
hermes profile create work

# 切换到指定 Profile
hermes --profile work

# 列出所有 Profile
hermes profile list

# 创建空 Profile（v0.13.0）
hermes profile create minimal --no-skills
```

### 14.2 Profile 隔离内容

| 项目 | 是否隔离 |
|------|---------|
| 配置文件 config.yaml | ✅ 完全隔离 |
| 会话记录 state.db | ✅ 完全隔离 |
| Skills | ✅ 完全隔离 |
| 记忆 | ✅ 完全隔离 |
| Cron 任务 | ✅ 完全隔离 |
| Gateway | ✅ 各 Profile 独立运行 |
| 凭据 | ✅ 完全隔离 |
| Nous OAuth | ❌ 跨 Profile 共享（v0.13.0） |

---

## 15. Kanban 多Agent看板 ← 新

> **v0.13.0 核心新特性**

Kanban 是 Hermes Agent 的**持久化多Agent协作看板系统**。你可以把一个大任务拆成多个小卡片，系统会启动多个 Hermes Worker 智能体并行处理。

### 15.1 核心功能

| 功能 | 说明 |
|------|------|
| **持久化看板** | 看板数据存在磁盘，重启不丢失 |
| **多Profile协作** | 不同 Profile 的 Worker 可共用一个看板 |
| **心跳检测** | Worker 定期报告存活状态 |
| **僵尸检测** | 自动检测并回收死掉的 Worker |
| **任务回收** | 失败的 Worker 自动重新调度 |
| **幻觉检测** | 检测 Worker 声称完成但实际未完成的任务 |
| **重试预算** | 每任务可设置最大重试次数 |
| **看板 Dashboard** | Web UI 管理看板 |

### 15.2 工作原理

```
用户创建任务
    │
    ▼
┌───────────────┐
│   Kanban Board  │  ← 持久化（SQLite）
│ ┌───┬───┬───┐ │
│ │待办│进行│完成│ │
│ └───┴───┴───┘ │
└───────┬───────┘
        │
    ┌───▼───┐
    │ Scheduler │ ← 调度 Worker
    └───┬───┘
        │
    ┌───▼──────┐
    │ Hermes Worker 1 │ ← 独立 AIAgent 实例
    │ Hermes Worker 2 │
    │ Hermes Worker n │
    └──────────────┘
        │
    ┌───▼───┐
    │ 结果合并  │ ← 汇总到看板
    └───────┘
```

### 15.3 使用方式

**CLI 中：**

```bash
# 创建看板
hermes kanban create "网站重构"

# 添加任务
hermes kanban add "设计数据库模型" --board "网站重构"

# 查看进度
hermes kanban status
```

**会话中：**

```
/kanban create "迁移项目"
/kanban add "迁移用户认证模块"
/kanban add "迁移数据库" --priority high
/kanban status
```

**通过 Skill 使用：**

Hermes 附带了两个 Kanban Skill：
- `kanban-orchestrator` — 编排者 Skill，负责分解任务并分配到看板
- `kanban-worker` — 工人 Skill，实际执行的具体任务

```skill
# 加载编排者 Skill
使用 kanban-orchestrator，将"开发博客系统"分解为看板任务并执行
```

### 15.4 配置

```yaml
kanban:
  heartbeat_interval: 30      # 心跳间隔（秒）
  zombie_timeout: 120         # 僵尸判定超时
  max_retries: 3              # 默认最大重试次数
  max_workers: 5              # 最大并行 Worker 数
  reclaim_tasks: true         # 自动回收失败任务
  specify_enabled: true       # 用辅助 LLM 自动细化粗略任务
```

### 15.5 看板 Dashboard 通知

v0.13.0 支持按平台设置通知开关：

```yaml
kanban:
  notifications:
    telegram:
      on_task_complete: true
      on_worker_failure: true
    discord:
      on_task_complete: false
```

### 15.6 v0.14.0 Kanban 增强

| 特性 | 说明 |
|------|------|
| **specify 辅助** | 辅助 LLM 把粗略的任务描述细化成可执行步骤 |
| **kanban_list** | 编排者 Agent 的看板工具：列出看板任务 |
| **kanban_unblock** | 编排者 Agent 的看板工具：手动解除卡住的任务 |
| **stranded_in_ready** | 诊断就绪状态但无人认领的任务 |
| **去重投递** | 原子认领 + 失败回滚，确保消息不重复 |
| **订阅存活** | 通知订阅跨越重试周期保持存活 |

---

## 16. 持久目标 /goal ← 新

> **v0.13.0 核心新特性**

`/goal` 让 Agent 记住你设定的目标，**跨轮保持专注**——即使你发了一大段不相关的内容，Agent 也不会跑偏。

### 16.1 基本用法

```
/goal 完成一个 Flask 博客系统，包含 CRUD + 用户认证

# 之后即使你聊别的，Agent 也知道最终目标
# 继续执行它的终极目标
```

### 16.2 命令

| 指令 | 说明 |
|------|------|
| `/goal <目标描述>` | 设置持久目标 |
| `/goal` | 查看当前目标 |
| `/goal clear` | 清除当前目标 |

### 16.3 工作原理

1. 设置目标后，目标文本被注入到后续每一轮的系统 prompt 中
2. Agent 每一轮都会检查目标完成状态
3. 可以设置轮数预算（默认不限），到达后自动停止

### 16.4 配置

```yaml
agent:
  goal_turn_budget: 50  # 最大目标轮数（0=不限，默认）
```

---

## 17. 安全与隐私

### 17.1 v0.14.0 安全加固（12个P0关闭）

| 漏洞 | 严重程度 | 修复 |
|------|---------|------|
| sudo 暴力破解 | P0 | 阻断 `sudo -S` 及 stdin/askpass 注入 |
| 危险命令绕过（3个） | P0 | 关闭已知绕过路径 |
| 工具错误注入 | P0 | 工具错误输出脱敏后注入模型，防止恶意文件/服务传递指令 |
| kanban_comment 作者伪造 | P0 | 禁止调用者覆盖作者信息 |
| SSRF 覆盖 | P0 | 补全 Skills Hub 中的 SSRF 路径 |
| 自定义端点凭据泄露 | P0 | 使用 credential_pool 探测模型列表 |
| Dashboard 插件 API | P0 | 需要认证才能访问插件路由 |
| 供应链依赖检查 | P0 | 安装时扫描不安全版本 |
| 减少不必要的 shell=True | P0 | 子进程调用安全加固 |

### 17.2 脱敏机制

v0.13.0 起，秘密脱敏**默认开启**：

```yaml
security:
  redaction:
    enabled: true     # 默认开启
    mode: aggressive  # aggressive | standard
```

支持脱敏的字段：
- API Keys (`sk-*`, `pk-*`)
- 令牌 (`eyJ*` JWT)
- 密码
- `.env` 中的所有值

### 17.3 其他安全措施

```yaml
security:
  redaction:
    enabled: true
  approval:
    dangerous_tools: [terminal, write_file]  # 危险操作需要确认
  browser:
    ssrf_protection: true                     # SSRF 防护
```

---

## 18. TUI 终端 UI

### 18.1 启动

```bash
hermes --tui
```

### 18.2 v0.14.0 增强

| 特性 | 说明 |
|------|------|
| `/sessions` 斜杠命令 | 浏览和恢复历史会话（@austinpickett） |
| 消息分段 | 非首条用户消息上方显示分割线 |
| 附加到现有 Gateway | TUI 连接到已运行的 Gateway |
| Markdown 链接解析 | 显示可读的页面标题 |
| 宽度自适应表格 | 表格过宽时自动切换为垂直布局 |
| 光标同步 | 实时打字写入时光标不跑偏 |
| 滚动 + Esc 支持 | 在审批/clarify/确认提示时可以滚动查看 |
| 人格切换保持会话 | 切换 Agent 人格时当前会话不丢失 |

---

## 19. 插件系统

### 19.1 插件类型

| 插件类型 | 存放位置 | 说明 |
|---------|---------|------|
| 记忆插件 | `plugins/memory/` | 各种记忆后端 |
| 提供商插件 | `plugins/model-providers/` | v0.13.0 新增：第三方推理提供商 |
| 平台插件 | `plugins/platforms/` | 消息平台适配器 |
| 图像生成 | `plugins/image_gen/` | 图像生成提供商 |
| 看板 | `plugins/kanban/` | 多Agent协作看板 |
| 可观测性 | `plugins/observability/` | 指标/跟踪/日志 |
| 成就系统 | `plugins/hermes-achievements/` | 游戏化成就 |
| 自定义 | `plugins/*/` | 任意自定义插件 |

### 19.2 v0.13.0 新Hook

```python
# transform_llm_output — 在 LLM 输出到达会话前拦截
class MyPlugin:
    def transform_llm_output(self, text: str) -> str:
        # 过滤或修改输出
        return text
```

### 19.3 插件管理（Dashboard）

v0.13.0 的 Dashboard 新增插件管理页面，支持：
- 查看已安装插件列表
- 启用/禁用插件
- 查看认证状态

---

## 20. MCP 服务器集成

### 20.1 什么是 MCP

Model Context Protocol (MCP) 是 AI 模型与外部工具/数据源的开放协议。Hermes 支持作为 MCP 客户端。

### 20.2 v0.14.0 增强

| 特性 | 说明 |
|------|------|
| **supports_parallel_tool_calls** | MCP 服务器可以并行处理多个工具调用 |
| **Codex MCP 预设** | 为 Codex CLI 配置专门的 MCP 服务器 |
| **停止重试认证失败** | MCP 服务器认证失败不再无限重试 |

### 20.3 配置

```yaml
mcp:
  servers:
    my-server:
      command: npx
      args: [-y, @modelcontextprotocol/server-filesystem, /path]
      transport: stdio  # 或 sse
      # SSE 配置（v0.13.0）
      sse_url: https://example.com/mcp
      oauth_token: ...
    another-server:
      transport: sse
      sse_url: https://api.example.com/mcp/sse
```

```bash
# 添加 MCP 服务器
hermes mcp add my-server --command "npx -y @modelcontextprotocol/server-filesystem /path"

# 查看已配置的 MCP 服务器
hermes mcp list
```

---

## 21. 工具生态图谱 — CLI · MCP · Skill 三件套

> **一句话定义**：CLI 是人机界面，MCP 是对外接口，Skill 是对内的经验沉淀——三者组成 AI Agent 的三层工具生态。**不要孤立地学每一件，要看它们怎么协同。**

### 21.1 为什么需要一张"生态图谱"

Hermes Agent 提供了大量工具和接口，新用户最容易犯的错误是：**把每样东西当独立功能学**——学 CLI 指令、学 MCP 配置、学 Skill 格式——结果学了三个月还是不知道怎么组合使用。

真实世界的工作流是三者交织的：

```
┌─── 用户发来消息 ─────────────────────────────┐
│ "帮我看一下服务器日志，找出报错规律，            │
│  下次遇到自动修复"                            │
└────────────────────┬─────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   CLI / Gateway 入口   │ ← 第一层：人机界面
         │   接收→理解→规划       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   MCP 工具调用         │ ← 第二层：对外接口
         │   读日志 → 分析 → 写脚本│
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Skill 经验沉淀        │ ← 第三层：对内经验
         │   保存"日志分析流程"     │
         │   下次遇到同类问题直接复用│
         └─────────────────────────┘
```

这张图谱回答三个核心问题：
- **用什么跟Agent说话？** → CLI / Gateway（消息平台）
- **Agent用什么跟世界交互？** → MCP（工具、数据、服务）
- **做过的事怎么不白做？** → Skill（流程、模板、规范）

### 21.2 CLI：人机界面层

**生态位置**：用户↔Agent 的交互协议。

CLI 不只是"敲命令的工具"，它是 Agent 世界的信息通道。在 Hermes 中，CLI 有三重身份：

| 身份 | 说明 | 场景 |
|------|------|------|
| **命令入口** | `hermes "写个Python脚本"` | 直接对话式编程 |
| **配置入口** | `hermes config set, hermes model, hermes setup` | 系统管理 |
| **管理入口** | `hermes sessions, hermes skill list, hermes gateway start` | 状态监控与维护 |

**关键洞察**：CLI 的价值不在"快"而在"可编排"。你可以在 shell 脚本中链式调用 CLI 命令，把 Hermes 嵌入到你的 CI/CD 流水线、定时任务、监控系统中：

```bash
# 把Hermes CLI嵌入日常流程
hermes "审查这个PR，列出所有安全问题" --output review.md
if [ $? -eq 0 ]; then
    hermes gateway restart  # 安全通过后重启网关
fi
```

**一句话定位**：CLI 是 Agent 的"听觉和嘴"——你通过它说话，Agent 通过它回答。

### 21.3 MCP：对外接口层

**生态位置**：Agent↔外部工具/数据/服务的连接协议。

MCP（Model Context Protocol）是 Anthropic 提出的开放标准，Hermes 作为 MCP 客户端，通过它连接文件系统、数据库、浏览器、API 等外部资源。

**为什么 MCP 是"USB-C"**：在 MCP 出现之前，每个工具都有自己的接入方式——写 Python 脚本、调 REST API、用 SDK——Agent 要"学"每种工具的语言。MCP 统一了接口规范，任何工具只要实现 MCP 协议，Agent 就知道怎么用它：

```
MCP 之前                       MCP 之后
┌────┐  ┌──────┐             ┌────┐  ┌──────────┐
│Agent│→→│Python脚本│         │Agent│→→│ MCP Server │
│    │  │REST API│             │    │  │(统一接口) │
│    │  │SDK调用 │             └────┘  └────┬─────┘
└────┘  └──────┘                         ┌──┼──┐
                                     ┌──┐│┌─┐│┌─┐
                                     │DB│││FS│││API│
                                     └──┘│└─┘│└─┘
                                          │
```

**Hermes 中的 MCP 生态**：

| MCP 服务器类型 | 示例 | 用途 |
|---------------|------|------|
| 文件系统 | `@modelcontextprotocol/server-filesystem` | 读写文件 |
| 数据库 | `@modelcontextprotocol/server-postgres` | SQL 查询 |
| 搜索 | `@modelcontextprotocol/server-web-search` | 联网搜索 |
| 浏览器 | `@modelcontextprotocol/server-puppeteer` | 网页交互 |
| 自定义 | 你自己写的 MCP Server | 连接公司内部系统 |

**一句话定位**：MCP 是 Agent 的"手和眼"——它通过 MCP 触摸世界、观察世界。

### 21.4 Skill：对内经验层

**生态位置**：Agent↔自身经验的持久化机制。

Skill 是 Hermes 最独特的设计。它不是配置文件，不是插件——它是一个**可复用的决策文档**，记录了"怎么做一件事"的完整流程。

**三个核心价值**：

| 价值 | 解释 | 类比 |
|------|------|------|
| **记忆** | 做完的事情不会被忘——流程以 skill 形式持久化 | 你的笔记系统 |
| **进化** | 多次执行后，skill 被 curator 自动整理优化 | 肌肉记忆 |
| **复用** | 下次遇到同类问题，不需要从零思考 | 菜谱 |

**Skill 的生命周期**：

```
完成复杂任务
    │
    ▼
┌─────────────────┐
│ Agent自动生成    │ ← 由 skill_manage 或 curator 触发
│ Skill 初稿       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 执行中修正/完善   │ ← 发现遗漏步骤或陷阱时 patch
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Curator 整理优化  │ ← 归档、修剪、分类
│（自动或手动）     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 下次任务自动加载   │ ← 遇到匹配的触发词时自动生效
│（配合 Skills list │
│   + 关联匹配）    │
└─────────────────┘
```

**一句话定位**：Skill 是 Agent 的"经验和直觉"——做过的事变成肌肉记忆，下次不用重新想。

### 21.5 三件套的关系矩阵

| 维度 | CLI | MCP | Skill |
|------|-----|-----|-------|
| **方向** | 用户→Agent | Agent→外部 | Agent→自身 |
| **协议** | 人机对话（自然语言+指令） | 机机对话（标准化协议） | 文档驱动（自描述流程） |
| **典型用户** | 所有使用者 | 开发者/集成者 | 重度使用者/管理者 |
| **学习成本** | 低（自然语言即可） | 中（需理解协议概念） | 中（需掌握格式规范） |
| **核心产出** | 一次性的执行结果 | 可扩展的能力边界 | 可复用的工作流程 |
| **复用性** | 低（每次重新输入） | 高（一次配置，多次使用） | 最高（自动加载，不断优化） |
| **维护方式** | 无需维护 | 配置文件变更 | `skill_manage` 或 curator |
| **失败影响** | 当前对话中断 | 工具调用失败 | 缺乏经验辅助，效率降低 |

### 21.6 实战场景：三件套如何协同

#### 场景一：日常编码任务

```
你说："修复这个bug"
  → CLI 接收指令，Agent 理解任务
  → MCP 连接文件系统读取代码 + 运行测试
  → Agent 分析后写修复代码
  → 完成后，Agent 自动生成/更新 Skill
  → 下次同类 bug，Skill 自动加载，减少一半时间
```

#### 场景二：运维监控流水线

```
cron 定时任务触发（CLI 层面配置）
  → Agent 通过 MCP 连接服务器监控系统
  → 发现问题后通过编程修复（MCP 写文件/重启服务）
  → 把这次故障处理流程沉淀为 Skill
  → 以后同类故障，Agent 自动按 Skill 流程走
```

#### 场景三：新人入职引导

```
管理员写好 5 个核心 Skill
  → 这些 Skill 在 Agent 启动时自动加载
  → 新用户通过 CLI 或 Gateway 发消息
  → Agent 依据 Skill 指导新人完成标准操作
  → 遇到 Skill 未覆盖的问题，Agent 现场解决并补充 Skill
```

### 21.7 生态位置总览图

```
                  ┌─────────────────────────────────────┐
                  │          用户（人类）                  │
                  └──────────────────┬──────────────────┘
                                     │
                          CLI / Gateway（消息平台）
                          ┌──────────┴──────────┐
                          │    自然语言交互指令    │
                          └──────────┬──────────┘
                                     │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
  ┌──────────────┐        ┌──────────────────┐       ┌──────────────┐
  │   推理引擎     │        │   MCP Server 池    │       │   Skill 库    │
  │  (LLM决策)    │◄──────►│  ┌────┬────┬────┐│       │  ┌──────────┐│
  │              │        │  │ FS │ DB │ Web││       │  │ 流程 A   ││
  │              │        │  └────┴────┴────┘│       │  │ 流程 B   ││
  │              │        │  ┌────┬────┐      │       │  │ 流程 C   ││
  │              │        │  │API │自定义│     │       │  └──────────┘│
  └──────────────┘        └──────────────────┘       └──────────────┘
          │
          ▼
  ┌──────────────────┐
  │  Kanban 多Agent    │
  │  /goal 持久目标     │
  │  cron 定时任务      │
  │  其他高级特性        │
  └──────────────────┘

  三层生态：
  ┌─────┐     ┌─────┐     ┌─────┐
  │ CLI │     │ MCP │     │Skill│
  │人机界面│     │对外接口│     │对内经验│
  └─────┘     └─────┘     └─────┘
```

### 21.8 选择指南：什么时候用什么

| 你想做什么 | 用什么 | 为什么 |
|-----------|--------|--------|
| 跟Agent对话 | **CLI** / Gateway | 这是默认的人机交互通道 |
| 让Agent操作文件 | **MCP** filesystem | Agent 通过 MCP 读写文件 |
| 让Agent搜索网页 | **MCP** web-search | Agent 通过 MCP 联网 |
| 让Agent记住怎么做事 | **Skill** | 一次学会，重复使用 |
| 把Agent接入微信 | **Gateway** + CLI | 用消息平台代替终端 |
| 批量处理100个文件 | **MCP** + **CLI脚本** | MCP 操作文件，CLI 控制流程 |
| 团队新人快速上手 | **Skill** + **CLI** | Skill 保证一致性 |
| 监控服务器自动修复 | **cron** + **MCP** + **Skill** | 全套配合 |
| 多个Agent协作干活 | **Kanban** + **Skill** | Kanban 调度，Skill 保证质量 |
| 让Agent自我进化 | **Skill** + **curator** | 经验自动沉淀、自动整理 |
| 搜索 X/Twitter 讨论 | **x_search**（v0.14.0） | 原生搜索工具，无需集成 skill |
| 生成 AI 视频 | **video_generate**（v0.14.0） | 统一接口，可插拔后端 |

---

## 22. 故障排除手册

### 22.1 常见问题

#### 问题：Gateway 无法启动
```
检查项：
1. 端口是否被占用：lsof -i :<port>
2. 配置文件语法：hermes config validate
3. 日志查看：hermes logs --level ERROR
```

#### 问题：Agent 无响应
```
1. 检查 API Key 是否有效
2. 查看配额：hermes model list | grep <your-model>
3. 重启 Gateway：hermes gateway restart
4. 查看完整日志：hermes logs --follow
```

#### 问题：会话中断后丢失
```
v0.13.0 已修复：Gateway 重启后自动恢复
如未恢复，手动恢复：
  hermes sessions        # 列出会话
  hermes resume <id>     # 恢复指定会话
```

#### 问题：工具调用超时
```
1. 增大超时：在配置中设置 tool_timeout: 300
2. 检查网络：ping 目标服务器
3. 使用代理（如在国内访问国外 API）
```

#### 问题：Firecrawl 额度用尽
```
方案一：切换到 SearXNG 自托搜索（v0.13.0）
  web:
    search_provider: searxng
    searxng_url: http://localhost:4000

方案二：使用 DuckDuckGo 搜索（ddgs Python 包）
方案三：使用 bing-search skill（见 wiki）
```

### 22.2 诊断命令

```bash
# 综合诊断
hermes doctor

# 查看版本
hermes version

# 查看配置
hermes config show

# 实时日志
hermes logs --follow

# 检查网络
python3 -c "import urllib.request; urllib.request.urlopen('https://openrouter.ai/api/v1/models', timeout=5).read()"
```

### 22.3 备份恢复

```bash
# 一键备份（v0.13.0 optional skill）
hermes skill enable hermes-user-data-pack
hermes user-data-pack backup

# 手动备份
cp -r ~/.hermes ~/.hermes.backup.$(date +%Y%m%d)

# 恢复
hermes user-data-pack restore
```

### 22.4 技能回滚

使用军师十策③提供的工具（本环境已部署）：

```bash
# 查看历史
~/.hermes/scripts/skill_backup.sh history <skill-name>

# 回滚到第2个版本
~/.hermes/scripts/skill_backup.sh rollback <skill-name> 2
```

### 22.5 会话回放

使用军师十策⑨提供的工具（本环境已部署）：

```bash
# 列出最近会话
~/.hermes/scripts/session_replay.py list

# 回放指定会话
~/.hermes/scripts/session_replay.py show <session-id>

# 会话统计
~/.hermes/scripts/session_replay.py stats <session-id>
```

---

## 23. 未来展望

### 23.1 从 Tenacity 到下一步

v0.13.0 "Tenacity" 解决的核心问题是 **Agent 的可信执行**。Kanban + /goal + Checkpoints v2 + 会话恢复，这一套组合拳让 Hermes 从一个"试一下"的工具变成了"能干活"的平台。

接下来几条可预见的演进路线：

### 23.2 Provider 生态化

v0.13.0 将推理提供商插件化（`plugins/model-providers/`），这意味着：
- **第三方提供商无需修改核心代码**即可集成
- 可能出现社区维护的提供商集市
- 最终用户能像装一个 pip 包一样添加推理后端

预测到 v0.15，provider 插件数量将从现在的 8 个增长到 20+，涵盖各种国产模型、自托管推理、边缘设备。

### 23.3 Kanban 的进化方向

当前看板是多Agent协作的起点而非终点。接下来：
- **Profile RPC**：不同 Profile 的 Worker 通过看板传递中间结果
- **跨机器看板**：Worker 运行在不同机器的 Hermes 实例上
- **人工审批节点**：在关键步骤暂停，等待人类确认后再继续

这在本质上是一个**分布式任务网格**，Hermes 的每一个实例都是网格中的一个节点。

### 23.4 记忆系统的统一

当前 Hermes 有多个记忆系统共存：
- Holographic Memory（事实存储）
- Hindsight（跨进程探针）
- RetainDB（持久化会话）
- wiki 知识库（llm-wiki）

未来可能统一为一个**分层记忆架构**：
```
短期记忆（当前会话）→ 中期记忆（Holographic facts）→ 长期记忆（wiki + RetainDB）
```

### 23.5 原生多模态

v0.13.0 新增了 `video_analyze` 工具，但目前多模态能力仍受限于底层模型。接下来的趋势：
- 将图像/视频/音频作为**一等公民**，而不是通过"工具"间接调用
- 跨模型自动降级：用 Gemini 做视觉理解，用 Claude 做文本推理，结果自动拼接
- 多模态消息在多平台之间的无损传输

### 23.6 自托管搜索的崛起

Firecrawl 的 API 额度限制（本环境已验证）正推动用户转向自托管方案。SearXNG 搜索支持（v0.13.0 新增）是第一步，接下来：
- 内置本地搜索引擎（类似 Elasticsearch 但更轻量）
- 搜索结果缓存共享（跨 Profile / 跨用户）
- 中文搜索深度优化（Bing + 百度 + 知乎的聚合）

### 23.7 对中国用户的实用建议

1. **搜索解决方案**：Firecrawl 额度紧张时，优先使用 `bing-search` skill（零成本）或部署 SearXNG
2. **Provider 选择**：DeepSeek V4 性价比高，可作主力；OpenRouter 作备用
3. **Kanban 实战**：先从小项目开始（2-3 个 Worker），熟悉后再扩展到复杂工程
4. **语言配置**：设置 `display.language: zh` 获得中文界面
5. **备份策略**：每周使用 `hermes user-data-pack backup`，同时手动备份 `~/.hermes/skills/`

---

## 附录：术语表

| 中文 | English | 使用场景 |
|------|---------|---------|
| 代理 | Agent | 核心概念，运行中的 AI 智能体实例 |
| 技能 | Skill | 复用流程文档，Hermes 的核心特性 |
| 看板 | Kanban | 多Agent协作的任务看板（v0.13） |
| 持久目标 | Goal | 跨轮不变的任务目标（v0.13） |
| 网关 | Gateway | 连接消息平台的服务 |
| 工具 | Tool | Agent 可调用的功能模块 |
| 工具集 | Toolset | 工具的命名分组 |
| 插件 | Plugin | 扩展 Hermes 功能的模块 |
| 记忆 | Memory | Agent 的持久化记忆系统 |
| 会话 | Session | 一次对话的完整记录 |
| 配置档案 | Profile | 完全隔离的 Hermes 实例配置 |
| 凭据池 | Credential Pool | 多 API Key 管理和自动轮换 |
| 检查点 | Checkpoint | 会话状态的快照和恢复 |
| 技能整理 | Curator | 自动整理优化技能库的系统 |
| 提供商 | Provider | AI 模型推理服务商 |
| 上下文窗口 | Context Window | Agent 能"看到"的最大令牌数 |
| 上下文压缩 | Context Compression | 用摘要代替旧消息以节约上下文 |
| 派生子代理 | Delegate Task | 启动子 Agent 处理子任务 |
| 定时任务 | Cron | 定期执行的自动化任务 |
| 看门狗 | Watchdog | no_agent 模式的脚本监控（v0.13） |
| 持久化 | Persistence | 数据在重启后不丢失 |
| 心跳 | Heartbeat | Worker 定期报告的存活信号 |
| 僵尸检测 | Zombie Detection | 自动发现并清理死掉的 Worker |
| 幻觉检测 | Hallucination Gate | 防止Worker声称完成但未实际完成 |
| 脱敏 | Redaction | 自动隐藏敏感信息（API Key等） |
| 终端UI | TUI | 基于终端的图形用户界面 |
| 仪表盘 | Dashboard | Web 管理界面 |
| ACP | Agent Communication Protocol | Agent 通信协议（IDE集成用） |
| MCP | Model Context Protocol | 模型上下文协议（工具集成标准） |
| SSE | Server-Sent Events | 服务端推送事件（v0.13 MCP） |
| 国际化 | i18n | 多语言界面支持（v0.13 共7语言） |
| X 搜索 | x_search | X/Twitter 原生搜索工具（v0.14.0） |
| 本地代理 | Proxy | OpenAI 兼容的 OAuth 代理（v0.14.0） |
| 语义诊断 | LSP Diagnostics | 文件写入时实时语言服务器错误检查（v0.14.0） |
| 文件变异验证 | File Mutation Verifier | 每次写文件后自动验证修改（v0.14.0） |
| Pareto 路由 | Pareto Router | 成本/质量最优平衡的模型路由（v0.14.0） |
| 提示缓存 | Prompt Cache | 跨会话 1 小时的 Claude prompt 前缀缓存（v0.14.0） |
| 电路断路器 | Circuit Breaker | 平台故障隔离机制（v0.14.0） |
| 实时移交 | Handoff | 不丢上下文的 Agent 转换（v0.14.0） |
| 子目标 | Subgoal | 主目标运行中附加额外成功标准（v0.14.0） |
| 计算机使用 | Computer Use | Agent 控制鼠标键盘操作 GUI（v0.14.0 支持非 Anthropic 模型） |
