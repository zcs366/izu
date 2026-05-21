---
source_url: file:///mnt/i/hermes/wiki_dropbox/Hermes_Agent_完整功能手册与操作指令集.md
ingested: 2026-05-11
sha256: f866131ec349fb1fab9a49288974110ae3507adc2da88997820b86add92b03ce
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: Hermes Agent 完整功能手册与操作指令集
---

# Hermes Agent 完整功能手册与操作指令集

> 来源: Hermes_Agent_完整功能手册与操作指令集.md（用户存入 wiki_dropbox）

# Hermes Agent 完整功能手册与操作指令集

> **版本**: v0.12.0 (2026.4.30) · 构建号: 7530ce04  
> **作者**: Nous Research · **协议**: MIT  
> **文档状态**: 基于本地部署环境整理（截至 2026-05-05）  
> **一句话定义**: 开源、自改进、跨平台的 AI 代理框架，可运行于终端、消息平台和 IDE

---

## 目录

1. [概述与核心特性](#1-概述与核心特性)
2. [近期版本更新亮点](#2-近期版本更新亮点)
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
15. [Credential Pools 凭据池](#15-credential-pools-凭据池)
16. [安全与隐私](#16-安全与隐私)
17. [TUI 终端 UI](#17-tui-终端-ui)
18. [插件系统](#18-插件系统)
19. [MCP 服务器集成](#19-mcp-服务器集成)
20. [故障排除手册](#20-故障排除手册)

---

## 1. 概述与核心特性

Hermes Agent 是 Nous Research 开发的开源 AI 代理框架，和 Claude Code、OpenAI Codex、OpenCode 属于同一品类——自主编码与任务执行代理，通过工具调用与系统交互。

### Hermes 的独特之处

| 特性 | 说明 |
|------|------|
| **自改进技能系统** | 解决复杂问题后自动保存流程为技能文档，下次自动加载，越用越好 |
| **跨会话持久记忆** | 记住你是谁、偏好、环境细节，支持多种记忆后端（内置、Honcho、Mem0 等） |
| **多平台网关** | 同一代理在 Telegram、Discord、Slack、微信等 15+ 平台运行，工具全功能 |
| **提供商无关** | 随时切换模型/提供商，凭据池自动轮换多个 API Key |
| **多配置档案** | 独立运行多个 Hermes 实例，各自持有隔离的配置、会话、技能、记忆 |
| **可扩展** | 插件、MCP 服务器、自定义工具、Webhook 触发器、Cron 调度、完整 Python 生态 |

### 核心架构速览

```
用户输入 → CLI/Gateway → AIAgent (run_agent.py)
  ├─ 构建 system prompt
  ├─ 加载技能、记忆、工具
  ├─ 循环：调用 LLM → 解析工具调用 → 分发执行 → 追加结果 → 继续
  └─ 直到 LLM 返回纯文本回复

关键组件：
  run_agent.py      # AIAgent 类，核心对话循环 (~12k LOC)
  model_tools.py    # 工具编排，discover_builtin_tools(), handle_function_call()
  toolsets.py       # 工具集定义，_HERMES_CORE_TOOLS 列表
  cli.py            # HermesCLI 类，交互式 CLI 编排 (~11k LOC)
  hermes_state.py   # SessionDB — SQLite 会话存储 (FTS5 全文搜索)
  gateway/          # 消息网关 — Telegram/Discord/微信等平台适配器
  cron/             # 定时任务调度器
  agent/            # 代理内部模块（提供商适配、记忆、缓存、压缩等）
  tools/            # 工具实现（自动发现）
  plugins/          # 插件系统（记忆提供商、上下文引擎等）
```

---

## 2. 近期版本更新亮点

本地环境版本演进：`v2026.3.30` → `v2026.4.8` → `v2026.4.13` → `v2026.4.16` → `v2026.4.23` → `v2026.4.30`

### v0.12.0 (2026.4.30) — 最新版本

**新增功能：**
- Microsoft Teams 平台适配器（插件形式）
- Piper 本地 TTS 提供商（纯离线语音合成）
- 命令型 TTS 提供商注册机制 `tts.providers.<name>`
- Gateway 音频路由中心化 + FLAC 支持 + Telegram 文档回退
- 仪表盘 Models 页面支持配置主模型 + 辅助模型
- 多图片发送（Telegram/Discord/Slack/Mattermost/Email/Signal）
- `hermes curator status` 技能使用统计（最常用/最少用）
- 技能使用计数追踪（`bump_use()` 集成到加载路径）
- Dashboard `--stop`/`--status` 标志

**重要修复：**
- Skills `.archive` 目录排除（不再污染索引）
- Gateway Ctrl+C 干净关闭
- `hermes config set` 保留 YAML 列表结构
- 上下文压缩后返回有效 `session_id`
- ACP 连接重放会话历史
- Cron 任务失败状态正确传递
- DeepSeek v4 reasoning_content 兼容性
- Kimi/Moonshot thinking-mode 填充

### v2026.4.23

**新增功能：**
- Ollama Cloud 内置提供商
- xAI Responses API 升级 + TTS 提供商
- Dashboard 主题系统（实时切换）
- Dashboard 插件系统（自定义标签页）
- Telegram `TELEGRAM_PROXY` 独立环境变量
- 工具网关（Tool Gateway）订阅制访问

**重要修复：**
- 拒绝启动时无提供商配置的静默 OpenRouter 回退
- MCP 工具处理器加入熔断器防止重试燃烧循环
- Gateway 线程上下文保持通知
- Telegram 冷启动重试预算增加

### v2026.4.16

**新增功能：**
- Ollama 自定义提供商 `think=false` 支持
- GitHub Copilot ACP 模式稳定化
- Claude Opus 4.7 API 迁移完成

**重要修复：**
- 上下文压缩保留最后一条用户消息
- Cron 空响应不再泄漏占位符
- Gateway 关闭临时代理防止泄漏
- 安静模式 `-Q` 仅输出原始响应文本
- CWD 来源统一为 `config.yaml`

### v2026.4.8

- 凭据池（Credential Pool）轮换
- 子代理 `delegate_task` 稳定性改进
- 浏览器工具本地 Chromium 回退
- 多项安全加固

### v2026.4.3 / v2026.3.30

- 初步凭据池支持
- 基础能力建立
- Memory 记忆后端扩展

---

## 3. 快速入门

### 安装

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 基本使用

```bash
hermes                      # 交互式对话
hermes chat -q "你好"       # 单次查询
hermes setup                # 运行设置向导
hermes model                # 切换模型/提供商
hermes doctor               # 健康检查
```

### 更新

```bash
hermes update               # 升级到最新版
```

---

## 4. CLI 指令全集

### 全局标志

```
hermes [flags] [command]

  --version, -V             # 显示版本
  --resume, -r SESSION      # 按 ID 或标题恢复会话
  --continue, -c [NAME]     # 按名称恢复，或最近的会话
  --worktree, -w            # 隔离 git worktree 模式（并行代理）
  --skills, -s SKILL        # 预加载技能（逗号分隔或重复使用）
  --profile, -p NAME        # 使用特定配置档案
  --yolo                    # 跳过危险命令确认
  --pass-session-id         # 在 system prompt 中包含 session ID
```

### 会话命令（chat）

```bash
hermes [chat] [flags]
  -q, --query TEXT          # 单次查询，非交互
  -m, --model MODEL         # 指定模型 (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       # 指定工具集（逗号分隔）
  --provider PROVIDER       # 强制提供商
  -v, --verbose             # 详细输出
  -Q, --quiet               # 抑制 banner、spinner、工具预览
  --checkpoints             # 启用文件系统检查点 (/rollback)
  --source TAG              # 会话源标签（默认: cli）
```

### 配置管理

```bash
hermes setup [section]      # 交互式向导 (model|terminal|gateway|tools|agent)
hermes model                # 交互式模型/提供商选择
hermes config               # 查看当前配置
hermes config edit          # 在 $EDITOR 中打开 config.yaml
hermes config set KEY VAL   # 设置配置值
hermes config path          # 打印 config.yaml 路径
hermes config env-path      # 打印 .env 路径
hermes config check         # 检查缺失/过时配置
hermes config migrate       # 用新选项更新配置
hermes login [--provider P] # OAuth 登录 (nous, openai-codex)
hermes logout               # 清除储存的认证
hermes doctor [--fix]       # 检查依赖和配置
hermes status [--all]       # 显示组件状态
```

### 工具与技能管理

```bash
hermes tools                # 交互式工具开关 (curses UI)
hermes tools list           # 显示所有工具和状态
hermes tools enable NAME    # 启用工具集
hermes tools disable NAME   # 禁用工具集

hermes skills list          # 列出已安装技能
hermes skills search QUERY  # 搜索技能市场
hermes skills install ID    # 安装技能（支持 URL）
hermes skills inspect ID    # 预览但不安装
hermes skills config        # 按平台启用/禁用技能
hermes skills check         # 检查更新
hermes skills update        # 更新过时技能
hermes skills uninstall N   # 移除市场安装的技能
hermes skills publish PATH  # 发布到注册表
hermes skills browse        # 浏览所有可用技能
hermes skills tap add REPO  # 添加 GitHub 仓库为技能源
```

### 会话管理

```bash
hermes sessions list        # 列出近期会话
hermes sessions browse      # 交互式选择器
hermes sessions export OUT  # 导出为 JSONL
hermes sessions rename ID T # 重命名会话
hermes sessions delete ID   # 删除会话
hermes sessions prune       # 清理旧会话 (--older-than N days)
hermes sessions stats       # 会话储存统计
```

### Cron 定时任务

```bash
hermes cron list            # 列出任务 (--all 包含禁用的)
hermes cron create SCHED    # 创建: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         # 编辑调度、提示、投递
hermes cron pause/resume ID # 控制任务状态
hermes cron run ID          # 立即触发一次
hermes cron remove ID       # 删除任务
hermes cron status          # 调度器状态
```

### Webhooks

```bash
hermes webhook subscribe N  # 在 /webhooks/<name> 创建路由
hermes webhook list         # 列出订阅
hermes webhook remove NAME  # 移除订阅
hermes webhook test NAME    # 发送测试 POST
```

### Gateway 消息平台

```bash
hermes gateway run          # 启动 gateway（前台）
hermes gateway install      # 安装为后台服务
hermes gateway start/stop   # 控制服务
hermes gateway restart      # 重启服务
hermes gateway status       # 检查状态
hermes gateway setup        # 配置平台
```

### Profiles 多配置档案

```bash
hermes profile list         # 列出所有档案
hermes profile create NAME  # 创建 (--clone, --clone-all, --clone-from)
hermes profile use NAME     # 设置默认
hermes profile delete NAME  # 删除
hermes profile show NAME    # 显示详情
hermes profile alias NAME   # 管理包装脚本
hermes profile rename A B   # 重命名
hermes profile export NAME  # 导出为 tar.gz
hermes profile import FILE  # 从归档导入
```

### 凭据池管理

```bash
hermes auth add             # 交互式凭据向导
hermes auth list [PROVIDER] # 列出池化凭据
hermes auth remove P INDEX  # 按提供商+索引移除
hermes auth reset PROVIDER  # 清除耗尽状态
```

### MCP 服务器

```bash
hermes mcp serve            # 将 Hermes 作为 MCP 服务器运行
hermes mcp add NAME         # 添加 MCP 服务器 (--url 或 --command)
hermes mcp remove NAME      # 移除
hermes mcp list             # 列出配置的服务器
hermes mcp test NAME        # 测试连接
hermes mcp configure NAME   # 切换工具选择
```

### 其他命令

```bash
hermes insights [--days N] # 使用分析
hermes update              # 更新到最新版
hermes pairing list/approve/revoke  # DM 授权管理
hermes plugins list/install/remove  # 插件管理
hermes honcho setup/status # Honcho 记忆集成
hermes memory setup/status/off  # 记忆提供商配置
hermes completion bash|zsh # Shell 补全
hermes acp                 # ACP 服务器 (IDE 集成)
hermes claw migrate        # 从 OpenClaw 迁移
hermes uninstall          # 卸载 Hermes
```

---

## 5. 会话中斜杠指令

在交互式会话中随时输入斜杠指令。

### 会话控制

| 指令 | 说明 |
|------|------|
| `/new` `/reset` | 新会话 |
| `/clear` | 清屏 + 新会话（CLI） |
| `/retry` | 重新发送最后一条消息 |
| `/undo` | 撤销最后一次交换 |
| `/title [name]` | 为会话命名 |
| `/compress` | 手动压缩上下文 |
| `/stop` | 终止后台进程 |
| `/rollback [N]` | 恢复文件系统检查点 |
| `/background <prompt>` | 后台运行提示 |
| `/queue <prompt>` | 排队到下一轮 |
| `/resume [name]` | 恢复指定名称的会话 |
| `/branch` `/fork` | 分支当前会话 |

### 配置控制

| 指令 | 说明 |
|------|------|
| `/config` | 显示配置（CLI） |
| `/model [name]` | 显示或切换模型 |
| `/personality [name]` | 设置人格 |
| `/reasoning [level]` | 设置推理层级（none/minimal/low/medium/high/xhigh/show/hide） |
| `/verbose` | 循环切换：off → new → all → verbose |
| `/voice [on/off/tts]` | 语音模式 |
| `/yolo` | 切换批准绕过 |
| `/skin [name]` | 切换主题（CLI） |
| `/statusbar` | 切换状态栏（CLI） |

### 工具与技能

| 指令 | 说明 |
|------|------|
| `/tools` | 管理工具（CLI） |
| `/toolsets` | 列出工具集（CLI） |
| `/skills` | 搜索/安装技能（CLI） |
| `/skill <name>` | 将会话加载技能 |
| `/cron` | 管理 cron 任务（CLI） |
| `/reload-mcp` | 重载 MCP 服务器 |
| `/plugins` | 列出插件（CLI） |

### Gateway 平台控制

| 指令 | 说明 |
|------|------|
| `/approve` | 批准待定命令（gateway） |
| `/deny` | 拒绝待定命令（gateway） |
| `/restart` | 重启 gateway |
| `/sethome` | 将当前聊天设为 home 频道 |
| `/update` | 更新 Hermes |
| `/platforms` `/gateway` | 显示平台连接状态 |

### 实用工具

| 指令 | 说明 |
|------|------|
| `/fast` | 切换优先/快速处理 |
| `/browser` | 打开 CDP 浏览器连接 |
| `/history` | 显示对话历史（CLI） |
| `/save` | 保存对话到文件（CLI） |
| `/paste` | 附加剪贴板图片（CLI） |
| `/image` | 附加本地图片文件（CLI） |

### 信息

| 指令 | 说明 |
|------|------|
| `/help` | 显示命令帮助 |
| `/commands [page]` | 浏览所有命令（gateway） |
| `/usage` | Token 用量 |
| `/insights [days]` | 使用分析 |
| `/status` | 会话信息（gateway） |
| `/profile` | 当前档案信息 |

### 退出

| 指令 | 说明 |
|------|------|
| `/quit` `/exit` `/q` | 退出 CLI |

---

## 6. 工具与工具集

当前启用状态（基于本地配置，CLI 平台）：

| 工具集 | 名称 | 状态 | 功能 |
|--------|------|------|------|
| `web` | 🔍 Web 搜索 | ✅ 启用 | 网络搜索与内容提取 |
| `browser` | 🌐 浏览器 | ✅ 启用 | 浏览器自动化（Browserbase/Camofox/本地 Chromium） |
| `terminal` | 💻 终端 | ✅ 启用 | Shell 命令与进程管理 |
| `file` | 📁 文件 | ✅ 启用 | 文件读写/搜索/修补 |
| `code_execution` | ⚡ 代码执行 | ✅ 启用 | 沙箱化 Python 执行 |
| `vision` | 👁️ 视觉 | ✅ 启用 | 图像分析 |
| `video` | 🎬 视频 | ❌ 禁用 | 视频分析 |
| `image_gen` | 🎨 图像生成 | ✅ 启用 | AI 图像生成 |
| `moa` | 🧠 混合代理 | ❌ 禁用 | Mixture of Agents |
| `tts` | 🔊 语音合成 | ✅ 启用 | 文字转语音 |
| `skills` | 📚 技能 | ✅ 启用 | 技能浏览与管理 |
| `todo` | 📋 任务规划 | ✅ 启用 | 会话内任务规划 |
| `memory` | 💾 记忆 | ✅ 启用 | 跨会话持久记忆 |
| `session_search` | 🔎 会话搜索 | ✅ 启用 | 搜索历史会话 |
| `clarify` | ❓ 澄清问题 | ✅ 启用 | 向用户提问 |
| `delegation` | 👥 任务委派 | ✅ 启用 | 子代理并行工作 |
| `cronjob` | ⏰ Cron | ✅ 启用 | 定时任务管理 |
| `messaging` | 📨 跨平台消息 | ✅ 启用 | 跨平台发送消息 |
| `rl` | 🧪 强化学习 | ❌ 禁用 | 强化学习工具 |
| `homeassistant` | 🏠 智能家居 | ❌ 禁用 | 智能家居控制 |
| `spotify` | 🎵 Spotify | ❌ 禁用 | Spotify 控制 |
| `yuanbao` | 🤖 元宝 | ❌ 禁用 | 腾讯元宝集成 |

### 工具使用要点

- **工具变更需 `/reset` 新建会话** 后才能生效，不会中途生效（保护 prompt caching）
- **每个工具返回 JSON 字符串**，通过 `tools/registry.py` 注册
- **`check_fn`** 机制确保工具仅在满足依赖条件时显示

---

## 7. 配置详解

### 配置文件路径

| 文件 | 路径 | 用途 |
|------|------|------|
| 主配置 | `~/.hermes/config.yaml` | 所有设置 |
| 密钥 | `~/.hermes/.env` | API 密钥和密钥（受文件保护，不能直接用工具写入） |
| 会话 | `~/.hermes/sessions/` | 会话记录 |
| 日志 | `~/.hermes/logs/` | 代理日志 + 错误日志 + Gateway 日志 |
| 技能 | `~/.hermes/skills/` | 已安装技能 |
| 认证 | `~/.hermes/auth.json` | OAuth Token 和凭据池 |
| 源码 | `~/.hermes/hermes-agent/` | Git 安装的源码 |

### 配置节

使用 `hermes config set section.key value` 设置。

| 配置节 | 关键选项 |
|--------|----------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement`, `reasoning_effort`, `gateway_timeout` (1800) |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/piper/elevenlabs/openai/minimax/mistral/neutts) 及自定义 `tts.providers.<name>` |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist`, `redact_secrets` |
| `delegation` | `model`, `provider`, `base_url`, `max_iterations` (50) |
| `checkpoints` | `enabled`, `max_snapshots` (50), `auto_prune`, `retention_days` (7) |
| `browser` | `inactivity_timeout` (120), `cdp_url`, `dialog_policy`, `camofox` |
| `approvals` | `mode` (manual/smart/off) |
| `privacy` | `redact_pii` |
| `auxiliary` | `vision`, `compression`, `curator` 各项子配置 |
| `tool_output` | `max_bytes` (50000), `max_lines` (2000) |
| `tool_loop_guardrails` | 工具循环防护（失败计数、相同工具失败计数等阈值） |
| `credential_pool_strategies` | 凭据池轮换策略（`fill_first` 等） |

### 本地关键配置

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
agent:
  max_turns: 90
  reasoning_effort: medium
compression:
  enabled: true
  threshold: 0.5
checkpoints:
  enabled: true
  max_snapshots: 50
terminal:
  backend: local
  timeout: 180
```

---

## 8. 模型与提供商

### 全部支持的提供商（20+）

| 提供商 | 认证方式 | 环境变量 | 本地状态 |
|--------|----------|----------|----------|
| OpenRouter | API Key | `OPENROUTER_API_KEY` | ✅ 已配置 |
| DeepSeek | API Key | `DEEPSEEK_API_KEY` | ✅ 当前使用 |
| Anthropic | API Key | `ANTHROPIC_API_KEY` | ❌ 未配置 |
| Nous Portal | OAuth | `hermes auth` | ❌ 未登录 |
| OpenAI Codex | OAuth | `hermes auth` | ❌ 未登录 |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` | ✅ Token 存在 |
| Google Gemini | API Key | `GOOGLE_API_KEY` / `GEMINI_API_KEY` | ❌ 未配置 |
| xAI / Grok | API Key | `XAI_API_KEY` | ❌ 未配置 |
| Hugging Face | Token | `HF_TOKEN` | ❌ 未配置 |
| Z.AI / GLM | API Key | `GLM_API_KEY` | ❌ 未配置 |
| MiniMax | API Key | `MINIMAX_API_KEY` | ❌ 未配置 |
| MiniMax CN | API Key | `MINIMAX_CN_API_KEY` | ✅ 已配置 |
| Kimi / Moonshot | API Key | `KIMI_API_KEY` | ❌ 未配置 |
| Alibaba DashScope | API Key | `DASHSCOPE_API_KEY` | ❌ 未配置 |
| Xiaomi MiMo | API Key | `XIAOMI_API_KEY` | ❌ 未配置 |
| NVIDIA NIM | API Key | `NVIDIA_API_KEY` | ✅ 已配置 |
| Ollama Cloud | API Key | (内置) | ❌ 未配置 |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` | ❌ 未配置 |
| 自定义端点 | Config | `model.base_url` + `model.api_key` | — |
| GitHub Copilot ACP | 外部 | `COPILOT_CLI_PATH` | — |

### 模型切换

```bash
# 交互式
hermes model

# 直接在会话中
/model anthropic/claude-sonnet-4

# 命令行指定
hermes chat -m deepseek-v4-flash --provider deepseek
```

### 凭据池（多个 API Key 轮换）

支持 `fill_first` 策略——先用第一个 Key，耗尽后自动切换到下一个。配合 `hermes auth add/list/remove` 管理。

---

## 9. Gateway 消息平台

### 支持的平台

| 平台 | 状态 | 主页频道 |
|------|------|----------|
| Telegram | ✅ 配置运行中 | 6512378453 |
| Discord | ✅ 配置运行中 | 1499356887945314376 |
| 微信（Weixin） | ✅ 配置运行中 | bot 身份 o9cq80-A2QetTJisKNUphB70rxhs |
| WhatsApp | ✅ 已配置 | — |
| Signal | ❌ 未配置 | — |
| Slack | ❌ 未配置 | — |
| Email | ❌ 未配置 | — |
| SMS | ❌ 未配置 | — |
| DingTalk | ❌ 未配置 | — |
| Feishu | ❌ 未配置 | — |
| WeCom | ❌ 未配置 | — |
| BlueBubbles (iMessage) | ❌ 未配置 | — |
| QQBot | ❌ 未配置 | — |
| Matrix | ❌ 未配置 | — |
| Mattermost | ❌ 未配置 | — |
| Microsoft Teams | ❌ 未配置（v0.12.0 新增插件） | — |
| Home Assistant | ❌ 未配置 | — |
| Yuanbao | ❌ 未配置 | — |

### Gateway 后台管理

```bash
# systemd 用户服务（推荐）
systemctl --user start hermes-gateway
systemctl --user restart hermes-gateway
systemctl --user status hermes-gateway
systemctl --user enable hermes-gateway
sudo loginctl enable-linger $USER   # 退出登录后保持运行

# 查看日志
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
journalctl --user -u hermes-gateway --since "5 min ago"
```

### Proxy 配置（中国大陆用户关键）

Gateway 作为 systemd 服务不继承 shell 代理变量，需在 service 文件中显式配置：

```ini
[Service]
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,::1,*.weixin.qq.com,*.qq.com,10.0.0.0/8,..."
```

⚠ **每次 `hermes gateway install` 会覆盖 service 文件自定义内容**，升级后需重新添加。

### Gateway 平台指令

```bash
# 平台配置
hermes gateway setup

# 平台启用
GATEWAY_ALLOW_ALL_USERS=true    # 首次测试设此变量

# Telegram 专属配置
TELEGRAM_PROXY=http://127.0.0.1:7890   # Telegram 独立代理
```

---

## 10. Skills 技能系统

**核心理念**：从经验中学习——每次解决复杂问题后，将流程保存为可复用的技能文档。

### 技能生命周期

```
发现 → 创建 → 安装 → 加载 → 使用 → 更新 → 归档/整合
```

### 当前已安装的本地技能

| 技能名称 | 分类 | 用途 |
|----------|------|------|
| `hermes-agent` | autonomous-ai-agents | Hermes 配置/扩展/贡献 |
| `claude-code` | autonomous-ai-agents | Claude Code 委派 |
| `codex` | autonomous-ai-agents | OpenAI Codex 委派 |
| `opencode` | autonomous-ai-agents | OpenCode 委派 |
| `wife-base-copywriter` | wife-business | 国防基地文案专员 |
| `wife-base-planner` | wife-business | 国防基地活动策划 |
| `document-typesetting` | creative | 报刊排版（Typst/WeasyPrint/Vivliostyle） |
| `plan` | software-development | 计划模式 |
| `spike` | software-development | 快速验证实验 |
| `daily-briefing-system` | productivity | 每日简报系统 |
| ... 以及更多技能 |

### 技能指令

```bash
# 查看所有
hermes skills list
hermes skills browse

# 安装
hermes skills install ID
hermes skills install https://.../SKILL.md --name my-skill

# 使用
hermes -s skill-name
# 或在会话中
/skill skill-name
```

### 编写技能的 SKILL.md 规范

```markdown
---
name: my-skill
description: "简短描述"
version: 1.0.0
author: 你的名字
---

# My Skill

## 触发条件
...

## 步骤
1. ...
2. ...

## 注意事项
- ...

## 验证
- ...
```

---

## 11. Memory 记忆系统

### 层级架构

| 层级 | 工具 | 持久性 | 用途 |
|------|------|--------|------|
| **会话搜索** | `session_search` | SQLite FTS5 | 跨会话全文搜索 |
| **用户画像** | `memory(target='user')` | 随会话注入 | 你是谁、偏好 |
| **个人笔记** | `memory(target='memory')` | 随会话注入 | 环境事实、约定 |
| **全息记忆** | `fact_store` | 实体关系图谱 | 结构化推理记忆 |

### 全息记忆（Holographic Memory）

- 基于实体的记忆系统，支持信任评分
- 24 个事实已存储（本地环境）
- 自动去重解析（Entity Resolution）

### 记忆提供商

8 个捆绑插件：`holographic`（内置）、`byterover`、`openviking`、`honcho`、`hindsight`、`retaindb`、`supermemory`、`mem0`

```bash
hermes memory setup     # 配置外部记忆提供商
hermes memory status    # 查看状态
hermes memory off       # 关闭记忆
```

---

## 12. Cron 定时任务

### 当前配置的任务

本地已配置 15 个 cron 任务——**七脉周报系统**（每周一至周日 + 下午 6 点提醒）：

| 任务名 | 调度 | 说明 |
|--------|------|------|
| 周一·诗歌与文学创作 | `0 9 * * 1` | 每周一早 9 点 |
| 周二·父亲角色与家庭教育 | `0 9 * * 2` | 每周二早 9 点 |
| 周三·军事热点与宏观视野 | `0 9 * * 3` | 每周三早 9 点 |
| 周四·计算机与人工智能 | `0 9 * * 4` | 每周四早 9 点 |
| 周五·古代学术与出版业 | `0 9 * * 5` | 每周五早 9 点 |
| 周六·自我管理与短板修补 | `0 9 * * 6` | 每周六早 9 点 |
| 周日·生活趣味与身心安顿 | `0 9 * * 0` | 每周日早 9 点 |
| 提醒（7 个） | `0 18 * * *` | 每天下午 6 点提醒 |
| Groq API Key 到期提醒 | `0 10 * * 1` | 每周一上午 10 点 |

### Cron 调度语法

| 格式 | 说明 | 示例 |
|------|------|------|
| `30m` | 每 30 分钟 | 简单周期 |
| `every 2h` | 每 2 小时 | 简单周期 |
| `0 9 * * *` | 标准 cron 表达式 | 每天早上 9 点 |
| ISO 时间戳 | 一次性任务 | 2026-05-05T09:00:00 |

### Cron 高级功能

- **脚本模式**：`script` 参数指定轮询脚本，`no_agent=true` 跳过 LLM，脚本 stdout 直接投递
- **上下文链**：`context_from` 将一个任务的输出注入另一个任务
- **`deliver` 控制**：可投递到当前会话、其他频道或仅存储
- **技能绑定**：任务可预加载一组技能
- **Workdir 隔离**：`workdir` 参数让任务在特定项目目录运行，自动注入 AGENTS.md 等上下文文件

---

## 13. Webhooks 与 ACP 集成

### Webhooks

```bash
# 创建 webhook 端点
hermes webhook subscribe my-hook

# 触发（POST 到 /webhooks/my-hook）
curl -X POST http://localhost:8000/webhooks/my-hook \
  -H "Content-Type: application/json" \
  -d '{"text": "处理这个"}'
```

### ACP（Agent Control Protocol）

ACP 是 Hermes 的 IDE 集成协议，支持 VS Code、Zed、JetBrains：

```bash
hermes acp                          # 作为 ACP 服务器启动
hermes chat -m codex --acp          # 在 ACP 模式下运行
```

ACP 特性：
- 会话历史重放（v0.12.0 修复）
- 图像提示转发
- 支持 `/rollback` 检查点恢复

---

## 14. Profiles 多配置档案

让多个 Hermes 实例带隔离配置独立运行。本地暂未使用 Profiles，但已正确配置。

```bash
# 创建
hermes profile create my-profile --clone-from default

# 使用
hermes --profile my-profile

# 设置默认
hermes profile use my-profile

# 导出/分享
hermes profile export my-profile   # 产生 tar.gz
hermes profile import my-profile.tar.gz
```

Profiles 储存在 `~/.hermes/profiles/<name>/`，结构完整克隆（config、.env、skills、sessions）。

---

## 15. Credential Pools 凭据池

单个提供商可以配置多个 API Key，自动轮换：

```bash
hermes auth add deepseek            # 添加第一个 Key
hermes auth add deepseek            # 添加第二个 Key
hermes auth list deepseek           # 查看
hermes auth remove deepseek 1       # 移除第二个

# 策略配置
credential_pool_strategies:
  deepseek: fill_first              # 先用第一个，耗尽后换下一个
```

---

## 16. 安全与隐私

### 命令审批

| 模式 | 说明 | 设置 |
|------|------|------|
| `manual` | 危险命令前提示（默认） | `hermes config set approvals.mode manual` |
| `smart` | 辅助 LLM 自动审批低风险命令 | `hermes config set approvals.mode smart` |
| `off` | 跳过所有审批（不推荐） | `hermes config set approvals.mode off` |

快捷绕过：`hermes --yolo` 或设 `HERMES_YOLO_MODE=1`

### 密钥脱敏

自动掩盖工具输出中的 API Key 等敏感信息：

```bash
hermes config set security.redact_secrets true   # 启用
hermes config set security.redact_secrets false  # 禁用（默认）
```

⚠ **需重启会话生效**（防止 LLM 自行关闭脱敏）

### PII 脱敏（Gateway）

```bash
hermes config set privacy.redact_pii true   # 启用，脱敏用户 ID/手机号
```

### 工具循环防护（Tool Loop Guardrails）

防止 LLM 陷入工具调用死循环的自动防护：

| 阈值 | 警告 | 硬停止 |
|------|------|--------|
| 精确错误 | 2 次 | 5 次 |
| 相同工具错误 | 3 次 | 8 次 |
| 无进展幂等调用 | 2 次 | 5 次 |

### 文件保护

`~/.hermes/.env` 受文件保护层保护，无法通过 `write_file`、`patch` 等工具直接写入。需通过 `sed` 或 `Python helper` 间接操作。

### Webhook 安全性

`hermes webhook subscribe` 创建的路由受签名验证保护。

---

## 17. TUI 终端 UI

Hermes 提供了基于 React Ink 的终端 UI：

```bash
hermes --tui       # 以 TUI 模式启动
```

TUI 特性（v0.12.0）：
- 迷你帮助菜单（输入 `?` 弹出）
- 鼠标模式自动恢复
- 扩展键盘模式重置
- 尊重 `max_turns` 配置
- Gateway 客户端集成

TUI 架构：
```
ui-tui/src/             # React/Ink 前端
  ├── app.tsx           # 主应用
  ├── entry.tsx         # 入口
  └── components/       # UI 组件
tui_gateway/            # Python JSON-RPC 后端
```

---

## 18. 插件系统

### 插件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 记忆提供商 | 外部记忆后端 | honcho, mem0, supermemory |
| 上下文引擎 | 上下文处理引擎 | — |
| 仪表盘 | Web UI 扩展 | dashboard-plugins |
| 平台适配器 | 消息平台 | Microsoft Teams |
| 工具 | 自定义工具集 | — |

### 插件命令

```bash
hermes plugins list              # 列出所有插件
hermes plugins install NAME      # 安装插件
hermes plugins remove NAME       # 移除插件
```

### v0.12.0 新插件

- **Microsoft Teams 平台适配器** — 支持消息收发、图片附件、卡片审批
- **hermes-achievements** — 扫描完整会话历史，追踪成就

---

## 19. MCP 服务器集成

Hermes 原生支持 MCP（Model Context Protocol）客户端和服务器模式。

### 客户端模式（连接外部 MCP 服务器）

```bash
# 添加 MCP 服务器（stdio 方式）
hermes mcp add my-server --command "npx @modelcontextprotocol/server-filesystem"

# 添加 MCP 服务器（HTTP 方式）
hermes mcp add my-server --url http://localhost:8080/mcp

# 测试
hermes mcp test my-server

# 配置启用哪些工具
hermes mcp configure my-server
```

MCP 注意事项：
- 工具处理器带熔断器（防止重试燃烧循环）
- 支持 keepalive 心跳（`_wait_for_lifecycle_event`）
- 重启：`/reload-mcp`

### 服务器模式（将 Hermes 作为 MCP 服务器提供）

```bash
hermes mcp serve                 # 其他 MCP 客户端可以连接使用 Hermes 的所有工具
```

---

## 20. 故障排除手册

### 语音不工作

```
1. 检查 stt.enabled: true
2. pip install faster-whisper 或设置 API Key
3. Gateway 中 /restart；CLI 中退出重进
```

### 工具不出现

```
1. hermes tools list — 检查工具集是否对当前平台启用
2. 检查 .env 是否有正确的环境变量
3. 启用后 /reset 新建会话
```

### 模型/提供商问题

```
1. hermes doctor — 检查配置和依赖
2. hermes login — 重新认证 OAuth 提供商
3. 检查 .env 中的 API Key
```

### 配置变更不生效

```
- 工具/技能：/reset 新建会话
- 配置变更（CLI）：退出重进
- 配置变更（Gateway）：/restart
- systemd service 文件：daemon-reload 后验证 Environment
```

### Gateway 不工作

```
1. 查日志: grep -i "failed\|error" ~/.hermes/logs/gateway.log
2. systemctl --user reset-failed hermes-gateway  # 清除崩溃状态
3. 检查代理配置（中国大陆用户）
4. sudo loginctl enable-linger $USER  # 保持退出登录后运行
```

### 微信相关

```
- iLink 身份 (@im.bot) 无法加入普通微信群，建议改用 Telegram 群
- 微信断开重连: 检查网络 + DNS 解析
- 微信家频道: WEIXIN_HOME_CHANNEL 环境变量
```

### WSL 专属问题

```
- npm install 卡住：--ignore-scripts 后手动执行 postinstall
- .npmrc 冲突：取消 Windows 侧 npm prefix 设置
- 中文字体缺失：安装文泉驿字体 (fonts-wqy-zenhei)
- systemd 必须：/etc/wsl.conf 中 [boot] systemd=true
```

### Windows HTTP 400 "No models provided"

`config.yaml` 编码问题（BOM）。确保保存为 UTF-8 without BOM。

### 浏览器工具不可用

```
1. npx agent-browser install
2. 建立符号链接:
   ln -sf ~/.agent-browser/browsers/chrome-<version> ~/.cache/ms-playwright/chromium-<version>
```

### .env 文件操作

`.env` 受保护，不能直接用工具写入。替代方案：
```python
# 替换已有行（可靠）
terminal("sed -i '42s|^OLD_KEY=.*|OLD_KEY=new_value|' ~/.hermes/.env")

# 追加新行（用 Python helper）
with open('/tmp/write_env.py', 'w') as f:
    f.write('''...''')
terminal("python3 /tmp/write_env.py")
```

---

## 附录 A：关键文件路径速查

| 要找什么 | 在哪里 |
|----------|--------|
| 主配置 | `~/.hermes/config.yaml` |
| API 密钥 | `~/.hermes/.env` |
| Gateway 日志 | `~/.hermes/logs/gateway.log` |
| 代理日志 | `~/.hermes/logs/agent.log` |
| 错误日志 | `~/.hermes/logs/errors.log` |
| 会话文件 | `~/.hermes/sessions/` |
| 技能文件 | `~/.hermes/skills/` |
| 认证 Token | `~/.hermes/auth.json` |
| Cron 任务 | `~/.hermes/cron/jobs.json` |
| 配置档案 | `~/.hermes/profiles/<name>/` |
| 系统服务 | `~/.config/systemd/user/hermes-gateway.service` |
| 检查点 | `~/.hermes/checkpoints/` |
| 缓存图片 | `~/.hermes/image_cache/` |
| 语音缓存 | `~/.hermes/audio_cache/` |
| 来源源码 | `~/.hermes/hermes-agent/` |

---

## 附录 B：本地环境摘要

| 项目 | 值 |
|------|-----|
| Hermes 版本 | v0.12.0 (2026.4.30) |
| Python | 3.11.15 |
| OpenAI SDK | 2.32.0 |
| 操作系统 | WSL (Ubuntu) |
| 当前模型 | deepseek-v4-flash (DeepSeek) |
| 已配置平台 | Telegram + Discord + 微信 + WhatsApp |
| Gateway 运行方式 | systemd 用户服务 |
| Cron 任务 | 15 个（七脉周报系统） |
| 安装技能 | 20+ 本地技能 |
| 会话记录 | 81 条 |

---

> **文档生成时间**: 2026-05-05  
> **工具**: Hermes Agent v0.12.0 + 军师祭酒

