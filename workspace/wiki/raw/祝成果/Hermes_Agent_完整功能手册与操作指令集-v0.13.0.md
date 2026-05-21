# Hermes Agent 完整功能手册与操作指令集 v0.13.0

> **版本**: v0.13.0 (2026.5.7) · 代号: Tenacity  
> **作者**: Nous Research · **协议**: MIT  
> **文档状态**: 基于本地部署环境整理（截至 2026-05-08）  
> **一句话定义**: 开源、自改进、跨平台的 AI 代理框架，可运行于终端、消息平台和 IDE

---

## 目录

1. [概述与核心特性](#1-概述与核心特性)
2. [v0.13.0 版本亮点](#2-v0130-版本亮点)
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
21. [故障排除手册](#21-故障排除手册)
22. [未来展望](#22-未来展望) ← **新**

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

## 2. v0.13.0 版本亮点

> **代号**: Tenacity（坚韧）—— 核心主题：**Agent 不再半途而废**

**版本跨度**: 864 次提交 · 588 个合并 PR · 295 位社区贡献者 · 282 个议题关闭（含 13 个 P0、36 个 P1）

### 新特性一览

| 特性 | 一句话说明 | 适合谁 |
|------|-----------|--------|
| **多Agent Kanban** | 持久化协作看板，多个 Hermes 智能体分任务干活 | 团队协作、复杂工程 |
| **/goal 持久目标** | 设定了目标就不忘，跨轮保持专注 | 所有用户 |
| **video_analyze** | 原生视频理解（Gemini 等兼容模型） | 媒体工作者 |
| **xAI Custom Voice** | 语音克隆作为 TTS 提供商 | 内容创作者 |
| **7 语言国际化** | CLI + Gateway 静态消息支持中文/日文/德文/西文/法等 | 非英语用户 |
| **Google Chat 平台** | 第 20 个消息平台 | Google 用户 |
| **会话中断自动恢复** | Gateway 重启后自动续接中断的会话 | 所有用户 |
| **Checkpoints v2** | 状态持久化重写，自动修剪，磁盘保护 | 长时间任务用户 |
| **安全加固** | 8 个 P0 级别安全漏洞修复 | 所有用户 |
| **no_agent cron** | 脚本监控模式，不经过 Agent，纯脚本定时运行 | 运维/监控 |
| **Providers 插件化** | 第三方提供商可以不改核心代码集成 | 开发者 |
| **Dashboard 增强** | 插件管理、Profiles 管理、排序分析表 | 管理员 |
| **SearXNG 搜索后端** | 自托管搜索，不依赖外部 API | 隐私敏感用户 |
| **OpenRouter 缓存** | 模型响应缓存，省费用 | 频繁调用用户 |
| **MCP SSE + OAuth** | 服务端推送事件 + 授权转发 | MCP 集成者 |
| **代码自检** | write_file/patch 自动 lint 语法错误 | 开发者 |

---

## 3. 快速入门

### 3.1 安装

Hermes Agent 支持多种安装方式（按难度排序）：

| 方法 | 难度 | 说明 |
|------|------|------|
| 一键脚本 | ★☆☆ | `curl -fsSL https://hermes.nousresearch.com/install.sh | sh` |
| Homebrew | ★☆☆ | `brew install nousresearch/tap/hermes-agent` |
| pip 安装 | ★★☆ | `pip install hermes-agent` |
| 源码安装 | ★★★ | `git clone && cd hermes-agent && pip install -e .` |

系统要求：

| 项目 | 最低 | 推荐 |
|------|------|------|
| OS | Linux / macOS / WSL2 | Linux (Ubuntu 22.04+) |
| Python | 3.11 | 3.11.10+ |
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
| `delegation` | delegate_task | 任务派发 |
| `vision` | vision_analyze, video_analyze | 视觉分析 |
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
| xAI | chat_completions | Grok 系列 |
| DeepSeek | chat_completions | DeepSeek 系列 |
| Bedrock | chat_completions | AWS 托管 |
| 自定义 | chat_completions | 任意 OpenAI 兼容 API |

### 8.2 v0.13.0 新增模型

| 模型 | 提供商 | 特点 |
|------|--------|------|
| `deepseek/deepseek-v4-pro` | OpenRouter/Nous | 高性能推理 |
| `x-ai/grok-4.3` | OpenRouter/Nous | Grok 最新版 |
| `openrouter/owl-alpha` | OpenRouter | 免费层 |
| `tencent/hy3-preview` | OpenRouter | 国产大模型 |

### 8.3 提供商插件化（v0.13.0）

在 `plugins/model-providers/` 中，第三方提供商可通过 `ProviderProfile` ABC 集成，无需修改核心代码：

```python
# 自定义提供商插件示例
from plugins.model_providers import ProviderProfile

class MyProvider(ProviderProfile):
    name = "my-provider"
    def chat_completions(self, messages, **kwargs):
        # 实现你的 API 调用
        ...
```

### 8.4 凭据池

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

### 9.1 支持平台（20个）

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
| Google Chat | ✅ **v0.13.0 新增** | 第20个平台 |
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

### 9.3 会话中断自动恢复（v0.13.0）

Gateway 重启后（包括 `/update` 重启、源码重载），中断的会话自动恢复：

```yaml
# 无需额外配置
gateway:
  auto_resume: true  # 默认开启
```

### 9.4 国际化界面（v0.13.0）

Gateway + CLI 静态消息支持 7 种语言：

```yaml
display:
  language: zh  # zh (中文), ja (日语), de (德语), es (西班牙语), fr (法语), uk (乌克兰语), tr (土耳其语)
```

### 9.5 平台白名单

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

### 10.5 [[as_document]] 指令（v0.13.0 新）

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

### 17.1 v0.13.0 安全加固（8个P0关闭）

| 漏洞 | 严重程度 | 修复 |
|------|---------|------|
| 密钥泄露 | P0 | 默认启用秘密脱敏 |
| Discord 跨服务器 | P0 (CVSS 8.1) | 角色白名单限定到本服务器 |
| WhatsApp 陌生人 | P0 | 默认拒绝陌生人 |
| MCP OAuth TOCTOU | P0 | 关闭凭据写入竞态窗口 |
| 认证文件 TOCTOU | P0 | 关闭凭据写入竞态窗口 |
| 浏览器 SSRF | P0 | 云元数据端点加固 |
| 日志上传泄露 | P0 | `hermes debug share` 上传时自动脱敏 |
| Cron 注入 | P0 | 扫描组装后的 prompt 中的注入代码 |

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

### 18.2 v0.13.0 增强

| 特性 | 说明 |
|------|------|
| `/model` 选择器 | 匹配 `hermes model` 命今，内联认证（@austinpickett） |
| 启动横幅折叠 | Skills/System Prompt/MCP 可折叠（@kshitijk4poor） |
| 压缩计数器 | 状态栏显示上下文压缩次数 |
| 性能优化 | 减少重复渲染（@OutThisLife） |
| 语音 PuT | 恢复语音 PTT 功能（@OutThisLife） |
| Kanban 按钮 | 看板快速入口（@austinpickett） |

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

### 20.2 v0.13.0 增强

| 特性 | 说明 |
|------|------|
| **SSE 传输** | 服务端推送事件，代替轮询 |
| **OAuth 转发** | MCP 认证凭据可自动转发 |
| **断线重连** | 管道断开自动重试 |
| **图片结果** | MCP 返回的图片正确显示（不丢弃） |
| **生命周期保活** | 长期运行 MCP 任务的心跳保持 |

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

## 21. 故障排除手册

### 21.1 常见问题

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

### 21.2 诊断命令

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

### 21.3 备份恢复

```bash
# 一键备份（v0.13.0 optional skill）
hermes skill enable hermes-user-data-pack
hermes user-data-pack backup

# 手动备份
cp -r ~/.hermes ~/.hermes.backup.$(date +%Y%m%d)

# 恢复
hermes user-data-pack restore
```

### 21.4 技能回滚

使用军师十策③提供的工具（本环境已部署）：

```bash
# 查看历史
~/.hermes/scripts/skill_backup.sh history <skill-name>

# 回滚到第2个版本
~/.hermes/scripts/skill_backup.sh rollback <skill-name> 2
```

### 21.5 会话回放

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

## 22. 未来展望

### 22.1 从 Tenacity 到下一步

v0.13.0 "Tenacity" 解决的核心问题是 **Agent 的可信执行**。Kanban + /goal + Checkpoints v2 + 会话恢复，这一套组合拳让 Hermes 从一个"试一下"的工具变成了"能干活"的平台。

接下来几条可预见的演进路线：

### 22.2 Provider 生态化

v0.13.0 将推理提供商插件化（`plugins/model-providers/`），这意味着：
- **第三方提供商无需修改核心代码**即可集成
- 可能出现社区维护的提供商集市
- 最终用户能像装一个 pip 包一样添加推理后端

预测到 v0.15，provider 插件数量将从现在的 8 个增长到 20+，涵盖各种国产模型、自托管推理、边缘设备。

### 22.3 Kanban 的进化方向

当前看板是多Agent协作的起点而非终点。接下来：
- **Profile RPC**：不同 Profile 的 Worker 通过看板传递中间结果
- **跨机器看板**：Worker 运行在不同机器的 Hermes 实例上
- **人工审批节点**：在关键步骤暂停，等待人类确认后再继续

这在本质上是一个**分布式任务网格**，Hermes 的每一个实例都是网格中的一个节点。

### 22.4 记忆系统的统一

当前 Hermes 有多个记忆系统共存：
- Holographic Memory（事实存储）
- Hindsight（跨进程探针）
- RetainDB（持久化会话）
- wiki 知识库（llm-wiki）

未来可能统一为一个**分层记忆架构**：
```
短期记忆（当前会话）→ 中期记忆（Holographic facts）→ 长期记忆（wiki + RetainDB）
```

### 22.5 原生多模态

v0.13.0 新增了 `video_analyze` 工具，但目前多模态能力仍受限于底层模型。接下来的趋势：
- 将图像/视频/音频作为**一等公民**，而不是通过"工具"间接调用
- 跨模型自动降级：用 Gemini 做视觉理解，用 Claude 做文本推理，结果自动拼接
- 多模态消息在多平台之间的无损传输

### 22.6 自托管搜索的崛起

Firecrawl 的 API 额度限制（本环境已验证）正推动用户转向自托管方案。SearXNG 搜索支持（v0.13.0 新增）是第一步，接下来：
- 内置本地搜索引擎（类似 Elasticsearch 但更轻量）
- 搜索结果缓存共享（跨 Profile / 跨用户）
- 中文搜索深度优化（Bing + 百度 + 知乎的聚合）

### 22.7 对中国用户的实用建议

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
