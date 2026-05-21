---
title: OpenAI CodeX CLI 完全手册
version: 1.0
date: 2026-05-09
author: 军师祭酒
tags: [codex, openai, coding-agent, cli, terminal]
---

# OpenAI CodeX CLI 完全手册

> 从零掌握 OpenAI 的终端原生 AI 编程智能体

---

## 第1章：概览与核心理念

### 1.1 什么是 CodeX CLI

CodeX CLI 是 OpenAI 推出的**开源 AI 编程智能体**，直接运行在你的终端里。它不是一个 IDE 插件，而是一个独立的命令行工具——你告诉它你想做什么，它自己读代码、写代码、跑测试、提 PR。

用一个类比来理解：

> **Copilot 像打字时的自动补全**——你写一个字，它猜下一个字。
> **CodeX 像一个坐在你旁边的初级工程师**——你跟他说"把这个模块重构了"，他起身去干活，干完回来给你看结果。

CodeX CLI 的定位是 **agent-first（智能体优先）**，区别于 cursor 的 IDE-first 路线。它的核心哲学是：**你描述目标，它执行过程。**

### 1.2 与同类工具的定位

| 工具 | 类型 | 哲学 | 技术栈 | 价格 |
|------|------|------|--------|------|
| **CodeX CLI** | 终端智能体 | Agent-first，自主执行 | Rust + GPT 模型族 | ChatGPT Plus ($20/月) 起 |
| **Claude Code** | 终端智能体 | Agent-first，自主执行 | Python + Claude 模型 | $20/月起 |
| **Cursor** | AI IDE | IDE-first，渐进式辅助 | TypeScript + 多模型 | $20/月起 |
| **Hermes Agent** | 通用智能体 | 工具调用，多平台 | Python + 任意模型 | 开源免费 |
| **GitHub Copilot** | IDE 插件 | 补全优先，辅助为主 | TypeScript + GPT | $10/月起 |

### 1.3 核心能力一览

CodeX CLI 能做什么：

- **编写功能**：从自然语言描述生成完整代码
- **大型重构**：跨文件、跨模块的重构
- **代码审查**：用独立 reviewer agent 审查 diff
- **调试修复**：读错误日志，定位 Bug，修代码
- **Web 搜索**：搜索最新文档和 API
- **图片生成/编辑**：直接在终端生成 UI 素材
- **子智能体**：并行处理复杂任务
- **MCP 集成**：接入第三方工具
- **Cloud 任务**：远程执行并返回 diff

### 1.4 架构概览

```
你 (终端)
  │
  ▼
CodeX CLI (Rust 核心)
  │
  ├── Sandbox (安全沙箱)
  │     ├── 文件系统隔离
  │     ├── 网络访问控制
  │     └── 命令审批系统
  │
  ├── Reviewer Agent (独立审查)
  │     └── 在另一个进程里审查 diff
  │
  ├── Sub-agents (子智能体)
  │     └── 并行执行子任务
  │
  ├── MCP (工具扩展)
  │     └── 第三方工具集成
  │
  └── Cloud Runner (云端执行)
        └── 远程服务器执行代码
```

---

## 第2章：安装部署全指南

### 2.1 系统要求

| 平台 | 支持情况 | 备注 |
|------|---------|------|
| macOS | ✅ 完整支持 | Intel 和 Apple Silicon |
| Linux | ✅ 完整支持 | 主流发行版 |
| Windows | ✅ 支持 | 原生运行（不是 WSL），设置 sandbox.mode 为 wsl 或 none |

其他要求：
- **Node.js >= 18**（npm 安装方式需要）
- **Git**（CodeX 需要在 git 仓库中运行）
- **OpenAI 账号**：ChatGPT Plus / Pro / Business / Edu / Enterprise

### 2.2 安装方式

**方式一：npm 全局安装（推荐）**

```bash
npm install -g @openai/codex
```

验证安装：

```bash
codex --version
```

**方式二：Homebrew（macOS）**

```bash
brew install --cask codex
```

**方式三：GitHub Release 二进制**

从 https://github.com/openai/codex/releases 下载对应平台的二进制文件，解压后放入 PATH。

### 2.3 认证配置

CodeX 支持两种认证方式：

**方式 A：ChatGPT OAuth（推荐个人用户）**

```bash
codex
# 首次运行会自动打开浏览器，要求登录 OpenAI 账号授权
```

**方式 B：API Key**

```bash
codex --config preferred_auth_method="apikey"
# 然后设置 OPENAI_API_KEY 环境变量
```

切换回 ChatGPT 认证：

```bash
codex --config preferred_auth_method="chatgpt"
```

如果账号额度用完了，可以直接切换到 API Key 方式继续使用。

### 2.4 快速启动

```bash
cd your-project   # 必须是一个 git 仓库
codex
```

你会看到一个交互式界面，输入提示词即可开始。

---

## 第3章：界面与基础操作

### 3.1 界面概览

CodeX CLI 启动后界面分为几个区域：

```
┌──────────────────────────────────────────────────────────┐
│  CodeX v2.x  |  gpt-5-codex  |  project-name            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  对话记录区                                        │   │
│  │  User: 帮我给这个 API 添加分页功能                  │   │
│  │                                                    │   │
│  │  CodeX: 好的，我来分析一下当前的 API 结构...        │   │
│  │  ┌─ 正在读取 user_service.py ─────────────────┐    │   │
│  │  │  ✓ 分析完成                                  │   │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │  ┌─ 正在修改 user_service.py ─────────────────┐    │   │
│  │  │  + 添加 page 和 page_size 参数              │   │   │
│  │  │  + 添加分页逻辑                             │   │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │                                                     │   │
│  │  [等待审批] codex 想要运行: pip install fastapi     │   │
│  │  批准? (Y/n) >                                      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ > 输入你的任务...                                        │
│   /help  /review  /status  /undo                         │
└──────────────────────────────────────────────────────────┘
```

### 3.2 基本操作

**发送任务**：在底部输入框直接键入自然语言描述。

**多行输入**：用 `Alt+Enter` 或 `Shift+Enter` 换行。

**审批命令**：CodeX 执行危险操作前会暂停等待审批：
- `y` 或 `Enter`：批准
- `n`：拒绝
- `s`：跳过

### 3.3 斜杠命令

| 命令 | 作用 |
|------|------|
| `/help` | 显示帮助信息 |
| `/review` | 审查当前代码差异 |
| `/status` | 显示当前任务状态 |
| `/undo` | 撤销上一次操作 |
| `/retry` | 重试上一条指令 |
| `/clear` | 清屏 |
| `/model` | 切换模型 |
| `/settings` | 打开设置 |
| `/quit` 或 `/exit` | 退出 |

### 3.4 审批模式

CodeX 有几种审批策略，适应不同的使用场景：

| 审批模式 | 行为 | 适合场景 |
|---------|------|---------|
| `untrusted`（默认） | 每次执行命令前询问 | 新项目、重要代码库 |
| `trusted` | 信任项目内命令 | 自己维护的项目 |
| `--dangerously-bypass-approvals-and-sandbox` | 跳过所有审批和沙箱 | 一次性脚本、完全信任的环境 |

---

## 第4章：实战——从零到一

### 4.1 场景1：给现有 API 添加分页功能

假设你有一个 FastAPI 应用，用户列表接口没有分页。

**第一步：进入项目并启动 CodeX**

```bash
cd ~/projects/my-api
codex
```

**第二步：输入任务**

```
帮我给 GET /users 接口添加分页功能，每页默认 20 条，支持 page 和 page_size 参数
```

**你会看到 CodeX 依次：**
1. 读取 `user_service.py` 和路由文件
2. 分析现有查询逻辑
3. 修改代码添加分页
4. 暂停等待你审批（`pip install fastapi` 等命令）
5. 运行测试验证

**第三步：审查修改**

```bash
/review
```

CodeX 会开一个独立的 reviewer agent，审查刚才的 diff，输出结构化反馈。

### 4.2 场景2：大规模重构

```
把这个项目的认证模块从 JWT 迁移到 OAuth 2.0，涉及 auth_service.py、middleware.py、config.py
```

CodeX 可以跨文件理解依赖关系，一次性完成迁移。如果任务很大，可以用子智能体并行处理：

```bash
codex --subagents 3 "重构 auth 模块"
```

### 4.3 场景3：修复 Bug

```
用户报告创建订单时偶尔会抛出 "Duplicate entry" 错误，帮我定位并修复
```

CodeX 会读错误日志、追踪代码路径、找到竞态条件，然后修复。

### 4.4 创建临时项目

如果想在空目录中测试：

```bash
cd $(mktemp -d) && git init && codex "用 Python 写一个命令行天气查询工具，调用 wttr.in API"
```

---

## 第5章：参数详解

### 5.1 命令行参数

| 参数 | 示例 | 作用 | 类比 |
|------|------|------|------|
| `exec` | `codex exec "添加日志"` | 非交互式执行，执行完退出 | 像发一封邮件而不是打电话 |
| `-m, --model` | `codex -m gpt-5-codex` | 指定模型 | 换引擎 |
| `-c, --config` | `codex -c key=value` | 临时配置覆盖 | 临时改设置 |
| `--search` | `codex --search "..."` | 启用 Web 搜索 | 给 CodeX 装上网 |
| `--subagents N` | `codex --subagents 3` | 并行子智能体数 | 叫几个帮手 |
| `--review` | `codex --review` | 启用审查模式 | 写完后找人看 |
| `--dangerously-bypass-approvals-and-sandbox` | `codex --yolo "..."` | 跳过所有安全措施 | 拆掉安全护栏 |
| `-v` | `codex -v` | 详细输出 | 看每一步在干嘛 |
| `--version` | `codex --version` | 显示版本 | — |

### 5.2 配置参数（config.toml）

CodeX 从多个层次读取配置（优先级从高到低）：

1. 命令行 `-c` 参数
2. 项目级 `codex.toml`（项目根目录）
3. 用户级 `~/.config/codex/config.toml`
4. 全局默认值

**常用配置项：**

| 配置键 | 可选值 | 默认值 | 说明 |
|--------|--------|--------|------|
| `model` | `gpt-5-codex`, `gpt-5`, `gpt-4o` 等 | `auto` | 默认模型 |
| `approval_policy` | `untrusted`, `trusted` | `untrusted` | 审批策略 |
| `model_reasoning_effort` | `low`, `medium`, `high` | `auto` | 推理深度 |
| `model_reasoning_summary_format` | `standard`, `experimental` | `standard` | 推理摘要格式 |
| `sandbox.mode` | `native`, `wsl`, `none` | `native` | 沙箱模式 |
| `sandbox.filesystem` | `readwrite`, `readonly`, `blocked` | `readwrite` | 文件系统权限 |
| `sandbox.network` | `auto`, `blocked`, `unrestricted` | `auto` | 网络访问 |
| `preferred_auth_method` | `chatgpt`, `apikey` | `chatgpt` | 认证方式 |
| `review_model` | 模型名 | 当前模型 | 审查专用模型 |
| `web_search` | `cached`, `live`, `off` | `cached` | 网页搜索模式 |

### 5.3 使用别名简化

```bash
# 配置默认参数
alias codex='codex -m gpt-5-codex -c model_reasoning_effort="high" -c model_reasoning_summary_format=experimental --search'
```

加到 `~/.zshrc` 或 `~/.bashrc` 中永久生效。

---

## 第6章：进阶技术详解

### 6.1 沙箱模式

CodeX 的沙箱是它的核心安全机制。它控制 CodeX 能做什么、不能做什么。

**三种沙箱模式：**

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `native`（默认） | 操作系统原生沙箱，限制文件系统和网络 | 日常使用 |
| `wsl` | WSL 兼容模式 | Windows 用户 |
| `none` | 无沙箱，全权限 | 完全信任的环境 |

**文件系统权限：**

```
readwrite   → CodeX 可以读写任何文件（默认）
readonly    → CodeX 只能读，不能写
blocked     → CodeX 不能访问文件系统
```

**网络权限：**

```
auto          → 根据任务自动判断（默认）
blocked       → 禁止网络访问
unrestricted  → 完全开放
```

### 6.2 子智能体（Sub-agents）

CodeX 支持启动多个子智能体并行处理任务。适合大型重构或多文件修改。

```bash
codex --subagents 3 "重构 payment 模块的三个核心服务"
```

每个子智能体：
- 运行在独立的进程中
- 有独立的安全沙箱
- 可以并行读写不同的文件
- 最终结果汇总到主会话

### 6.3 独立审查者（Reviewer）

CodeX 内置一个独立的 reviewer agent，在 diff 提交前进行审查：

```bash
# 在交互式会话中
/review

# 或命令行模式
codex review --base origin/main
```

Reviewer 的特点：
- 使用独立的模型（`review_model` 配置）
- 专注审查，不和主任务互相干扰
- 输出结构化的审查报告：严重问题 → 建议 → 小细节

### 6.4 Web 搜索

CodeX 支持搜索网页获取最新信息。三种模式：

```yaml
web_search = "cached"   # 默认：使用 OpenAI 缓存的搜索结果，减少 prompt injection 风险
web_search = "live"     # 实时搜索，获取最新内容
web_search = "off"      # 禁用搜索
```

启用 Web 搜索后，CodeX 可以：
- 查询最新的 API 文档
- 查找 npm/PyPI 包的版本信息
- 搜索 Stack Overflow 上的解决方案

### 6.5 MCP 集成

CodeX 支持 Model Context Protocol（MCP），可以接入第三方工具：

```bash
# 添加 MCP 服务器
codex mcp add my-tools --command npx --args my-mcp-server

# 列出已配置的 MCP
codex mcp list
```

常用 MCP 工具：
- **文件系统操作**：更精细的文件读写控制
- **数据库查询**：直接查询数据库获取 schema
- **API 调用**：调用外部服务

### 6.6 Cloud 任务

对于需要远程执行的任务（例如需要特定环境的编译、测试）：

```bash
codex cloud "编译并测试这个 Rust 项目"
```

CodeX 会在云端执行任务，完成后将 diff 返回本地。

### 6.7 图片生成与编辑

CodeX 可以在终端中生成和编辑图片：

```
帮我生成一个简单的登录页面 UI 草图，蓝色主题
```

CodeX 会生成图片，并可以在后续对话中根据反馈修改。

### 6.8 配置文件示例

**用户级配置文件 `~/.config/codex/config.toml`：**

```toml
[default]
model = "gpt-5-codex"
approval_policy = "trusted"
web_search = "cached"

[features]
review = true
subagents = true
cloud = true

[profiles]
  [profiles.quick]
  model = "gpt-4o-mini"
  approval_policy = "untrusted"

  [profiles.deep]
  model = "gpt-5-codex"
  model_reasoning_effort = "high"
  model_reasoning_summary_format = "experimental"
  web_search = "live"
```

使用 profile：

```bash
codex --profile quick "修复这个拼写错误"
codex --profile deep "重构整个数据库层"
```

---

## 第7章：社区资源精选

### 7.1 官方资源

**GitHub 仓库**
- URL: https://github.com/openai/codex
- 适合人群：所有用户
- 内容概览：源代码（Rust）、Release 发布、Issue 跟踪
- 为什么值得看：获取最新版本、查看 Roadmap、报告 Bug
- 一句话评价：CodeX 的大本营，所有一手信息都在这
- 学到的技能点：项目结构、贡献方式

**OpenAI 开发者文档**
- URL: https://developers.openai.com/codex/cli
- 适合人群：所有用户
- 内容概览：详细的功能指南、配置说明、命令参考
- 为什么值得看：最权威的官方配置文档
- 一句话评价：遇到参数问题先查这里
- 学到的技能点：完整命令参考、配置技巧

**OpenAI 官网 CodeX 页**
- URL: https://openai.com/codex/
- 适合人群：新用户
- 内容概览：功能宣传、案例展示、定价信息
- 为什么值得看：快速了解 CodeX 能做什么
- 一句话评价：从宏观了解 CodeX 的价值
- 学到的技能点：产品定位、定价方案

### 7.2 教程资源

**Blog 园 CodeX 技巧系列（Java技术栈）**
- URL: https://www.cnblogs.com/javastack/p/19113665
- 适合人群：中文开发者、新手
- 内容概览：16 个 CodeX 实用技巧，从别名校验到配置优化
- 为什么值得看：实战经验总结，非官方教程
- 一句话评价：博主用 CodeX 替代 Claude Code 后的实战心得
- 学到的技能点：别名配置、认证切换、模型选择

**腾讯云开发者社区——万字 CodeX 安装配置全攻略**
- URL: https://cloud.tencent.com/developer/article/2630702
- 适合人群：新手、国内用户
- 内容概览：超详细的安装配置教程，含踩坑记录
- 为什么值得看：国内环境下的完整部署指南
- 一句话评价：一篇上万字的 CodeX 百科全书
- 学到的技能点：国内环境配置、常见问题

**知乎国内使用 CodeX 教程**
- URL: https://zhuanlan.zhihu.com/p/1972655407605520311
- 适合人群：国内用户、零基础
- 内容概览：国内注册、支付、安装、配置完整流程
- 为什么值得看：解决了国内用户访问 OpenAI 服务的最大痛点
- 一句话评价：零基础友好的国内专属教程
- 学到的技能点：国内支付方案、代理配置

### 7.3 对比评测

**Particula Tech——CodeX vs Claude Code 对比**
- URL: https://particula.tech/blog/codex-vs-claude-code-cli-agent-comparison
- 适合人群：在两种工具间犹豫的用户
- 内容概览：功能、性能、工作流适配的全面对比
- 为什么值得看：客观中立的技术对比
- 一句话评价：帮你决定选哪个工具
- 学到的技能点：决策框架、场景匹配

**Beam——AI 编程工具终极对比 2026**
- URL: https://getbeam.dev/blog/ai-coding-agents-comparison-2026.html
- 适合人群：深度使用者
- 内容概览：Claude Code vs Cursor vs CodeX 三足鼎立格局分析
- 为什么值得看：分析的是三种不同哲学，不只是功能对比
- 一句话评价：agent-first vs IDE-first 的底层逻辑分析
- 学到的技能点：工具选择决策树

### 7.4 社区讨论

**Reddit r/OpenAI**
- 适合人群：关注 OpenAI 生态的用户
- 内容概览：CodeX 使用经验分享、问题求助
- 为什么值得看：最活跃的 CodeX 用户社区
- 一句话评价：遇到奇怪的 Bug，这里往往有人遇到过

**Discord OpenAI 社区**
- 适合人群：深度用户、开发者
- 内容概览：官方团队在线答疑、功能讨论
- 为什么值得看：可以直接和官方团队交流
- 一句话评价：获取第一手更新信息的地方

---

## 第8章：业内评价与案例分析

### 8.1 行业格局

2026 年初的 AI 编程工具市场形成了三足鼎立的格局：

- **Claude Code**（Anthropic）：终端原生智能体，年化收入已达 25 亿美元
- **Cursor**（Anysphere）：AI 增强 IDE，开发者社区最大的 AI 编辑器
- **CodeX CLI**（OpenAI）：终端智能体，GPT 模型族

### 8.2 典型案例

**案例一：从 JWT 到 OAuth 2.0 迁移**

某金融科技公司使用 CodeX 完成了一次大型认证模块迁移。使用 `--subagents 3` 并行处理三个核心服务，整个项目从计划到完成用了 3 天，而团队估计人工需要 2 周。

**案例二：Code Review 自动化**

一位开发者将 CodeX 的 review 功能集成到 CI 流程中：
- 每次 PR 创建时自动触发 `codex review --base origin/main`
- Reviewer 输出结构化报告，直接 comment 到 PR
- 结果：代码审查效率提升 40%，小问题不再漏掉

**案例三：爬坑实录**

一位中文开发者记录了从 Claude Code 切换到 CodeX 的经历：
> "CodeX = 一个愿意花 10+ 分钟思考、一次性给你写出生产级代码的狠角色"

主要痛点：CodeX 需要 ChatGPT Plus/Pro 订阅才能使用，免费用户无法体验。

### 8.3 性能对比

| 维度 | CodeX CLI | Claude Code | Cursor |
|------|-----------|-------------|--------|
| 自动执行能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 上下文理解 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 性价比 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| IDE 集成 | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 安全性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 开源程度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### 8.4 定价对比

| 方案 | 月费 | 适用人群 |
|------|------|---------|
| ChatGPT Plus | $20 | 个人开发者 |
| ChatGPT Pro | $200 | 重度使用者 |
| ChatGPT Business | $25/人 | 团队 |
| API Key 方式 | 按量计费 | 灵活使用 |

---

## 第9章：避坑指南

### 9.1 安装问题

**问题 1：`codex: command not found`**

- 现象：安装后找不到命令
- 原因：npm 全局安装路径不在 PATH 中
- 修复：
  ```bash
  # 检查 npm 全局 bin 路径
  npm root -g
  # 添加到 PATH
  export PATH=$(npm root -g)/bin:$PATH
  ```

**问题 2：首次认证失败**

- 现象：浏览器打开了但认证页面报错
- 原因：网络代理问题或 OpenAI 账号问题
- 修复：切换 API Key 方式：
  ```bash
  codex --config preferred_auth_method="apikey"
  export OPENAI_API_KEY="sk-..."
  ```

**问题 3：Windows 上沙箱报错**

- 现象：CodeX 启动时提示 sandbox 错误
- 原因：Windows 原生沙箱不支持
- 修复：
  ```bash
  codex -c sandbox.mode=wsl
  # 或在 config.toml 中设置
  # sandbox.mode = "wsl"
  ```

### 9.2 运行问题

**问题 4：CodeX 说"not a git repository"**

- 现象：拒绝在非 git 目录中运行
- 原因：CodeX 设计上要求 git 仓库
- 修复：
  ```bash
  git init  # 或在临时目录创建
  ```

**问题 5：命令审批太频繁**

- 现象：每一步都停下来问"是否允许"
- 原因：默认审批策略是 `untrusted`
- 修复：
  ```bash
  codex --config approval_policy="trusted"
  ```

**问题 6：CodeX 改错了文件**

- 现象：修改不符合预期
- 原因：提示词不够精确
- 修复：
  ```bash
  /undo     # 撤销
  # 重新描述，更精确
  ```

**问题 7：搜索功能不返回实时结果**

- 现象：CodeX 搜索结果过时
- 原因：默认使用缓存搜索（`web_search = "cached"`）
- 修复：
  ```bash
  codex --search --config web_search="live"
  ```

### 9.3 性能问题

**问题 8：执行速度慢**

- 现象：一个简单的修改要等很久
- 原因：模型推理时间 + 审批流程
- 修复：
  - 使用 `--dangerously-bypass-approvals-and-sandbox`（注意安全风险）
  - 切换到轻量模型：`-m gpt-4o-mini`
  - 降低推理深度：`-c model_reasoning_effort=low`

**问题 9：大项目中上下文不够**

- 现象：长对话后 CodeX 记不住之前的内容
- 原因：上下文窗口满了
- 修复：分割任务，每个会话处理一个模块

### 9.4 中国特色问题

**问题 10：国内无法访问 OpenAI**

- 现象：认证失败、API 超时
- 原因：网络限制
- 修复：
  - 使用 API Key + 代理方案
  - 参考知乎教程配置国内环境
  - 考虑试用国内的替代工具

---

## 第10章：进阶技巧与最佳实践

### 10.1 效率技巧

**技巧 1：为不同任务创建 Profile**

```toml
# ~/.config/codex/config.toml
[profiles]
  [profiles.quick]         # 快速修改
  model = "gpt-4o-mini"
  approval_policy = "trusted"

  [profiles.deep]          # 深度重构
  model = "gpt-5-codex"
  model_reasoning_effort = "high"
  web_search = "live"

  [profiles.review]        # 代码审查
  model = "gpt-5-codex"
  web_search = "off"
```

**技巧 2：用 exec 模式做自动化**

```bash
# CI/CD 中集成 CodeX 审查
codex exec --review "修复所有 ESLint 警告"

# 批量任务
for dir in services/*/; do
  codex exec --workdir "$dir" "更新依赖到最新版本"
done
```

**技巧 3：5 分钟规则**

如果一个手动操作预计超过 5 分钟，就交给 CodeX：

```bash
codex "把这个 JSON 文件转成 TypeScript 类型定义，输出到 types.ts"
```

### 10.2 提示词工程

好的提示词 = 好的结果。几个原则：

1. **明确目标**：不要说"优化代码"，要说"把 users API 的响应时间优化到 200ms 以下"
2. **限定范围**：指出要修改哪些文件，避免涉及无关模块
3. **提供上下文**：粘贴相关的错误日志或需求文档
4. **分步描述**：复杂任务拆成多个小步骤

### 10.3 安全最佳实践

1. **始终使用沙箱**：除非完全信任环境，否则保持默认沙箱
2. **审查所有 diff**：合并前用 `/review` 审查
3. **敏感信息隔离**：不要在提示词中包含 API Key 和密码
4. **使用 untrusted 策略**：在生产环境代码上保持 untrusted

### 10.4 学习路线图

| 时间 | 目标 | 学习内容 |
|------|------|---------|
| Day 1 | 上手 | 安装、认证、第一条 prompt |
| Day 2-3 | 交互 | 掌握审批流程、`/review`、`/undo` |
| Day 4-5 | 配置 | 学习 config.toml 配置、创建 profile |
| Week 2 | 工作流 | 使用 exec 模式、集成到 CI |
| Week 3 | 高级 | 子智能体、MCP 集成、Cloud 任务 |
| Week 4 | 深度 | 多工具配合（CodeX + Claude Code + Cursor） |

---

## 第11章：未来展望

### 11.1 Agent-first 编程的范式转换

CodeX CLI 代表的不是"又一个新的开发者工具"，而是一次编程范式的根本转变。传统上，开发者与代码的关系是**直接操作**——你写每一行、改每一行、看每一行。Agent-first 工具把这种关系变成了**间接委托**——你描述意图，AI 执行实现。

这个转变的深远影响在于：**它把编程从"手艺"变成了"管理"**。你不再是一个用手写代码的工匠，而是一个用语言指挥 AI 的架构师。这意味着：

1. **入门门槛大幅降低**：不会写具体实现的细节语法，但能描述清楚需求的人，也能"编程"了
2. **开发效率的天花板被重新定义**：过去衡量效率看"你一天能写多少行"，未来看"你能管理多少个 agent"
3. **代码质量的责任边界变了**：每一行代码不是人写的，但每一行代码都是人批准的

### 11.2 终端 vs IDE 之争

2026 年 AI 编程工具最有趣的格局是：**终端智能体（CodeX、Claude Code）和 AI 编辑器（Cursor）代表了两种完全不同的哲学。**

Cursor 的 IDE-first 路线假设：**你仍然在写代码，AI 只是在帮你写得更快。**
CodeX 的 Agent-first 路线假设：**你写的代码越来越少，AI 替你写的越来越多。**

这不是渐进式改进，而是根本分歧。就像自动档和手动档——不是手动档更好或更差，而是自动档改变了你开车时的注意力和体验。CodeX 的信徒认为，未来十年，大多数"寻常"的编程工作都将由 agent 完成，人类开发者转向更高级的架构决策和需求分析。

### 11.3 多 Agent 协作生态

目前 CodeX 的子智能体功能（`--subagents 3`）只是一个开始。可以预见的未来：

1. **Agent 之间的对话**：一个 agent 写完代码，另一个 agent 审查，第三个 agent 写测试——它们彼此之间可以直接沟通
2. **跨工具 agent 协作**：CodeX 写完代码 → Claude Code 审查 → Cursor 做最终编辑，每个工具用自己最强的能力
3. **持久化 agent 角色**：团队成员的角色（architect、reviewer、tester）被 agent 长期扮演

### 11.4 风险与隐忧

需要清醒地认识到几个风险：

1. **过度依赖**：当 agent 承担了太多编码工作，开发者的"代码免疫力"会下降——长期不亲手写代码，会失去对代码的直觉判断
2. **安全边界**：agent 越强大，出错的破坏力越大。一句模糊的 prompt 可能导致带着安全漏洞的代码上线
3. **锁定效应**：如果团队从工具层面深度耦合了某个 agent，切换成本会极高

### 11.5 预测

1. **6 个月内**：CodeX 将支持多模型并行调用（不同子任务由不同模型执行，最优的模型做最适合的事）
2. **12 个月内**：Agent-first 和 IDE-first 将互相融合——终端 agent 会嵌入编辑器，编辑器会扩展 agent 能力
3. **18 个月内**："软件工程师"的角色将从"写代码的人"重新定义为"管理 AI 开发者的人"——代码产出不再是能力的主要衡量标准

---

## 附录：术语表

| 中文 | English | 使用场景 |
|------|---------|---------|
| 智能体优先 | Agent-first | 描述 CodeX/Claude Code 这类工具的设计哲学 |
| 审批策略 | Approval Policy | 配置 CodeX 何时需要人类批准后才能执行命令 |
| 沙箱 | Sandbox | CodeX 运行时的安全隔离环境 |
| 子智能体 | Sub-agent | CodeX 并行启动的独立工作进程 |
| 审查者 | Reviewer | 独立审查代码 diff 的 AI agent |
| MCP | Model Context Protocol | CodeX 接入第三方工具的标准化协议 |
| Cloud 任务 | Cloud Task | 在远程服务器上执行 CodeX 任务 |
| 配置文件 | Config TOML | CodeX 的配置格式，使用 TOML 语言 |
| Profile | Profile | 一组预定义的配置参数集合 |
| 推理深度 | Reasoning Effort | 控制模型思考的深入程度 |
| 非交互模式 | Exec Mode | `codex exec` 执行完就退出的模式 |
| 缓存搜索 | Cached Search | 使用预索引的搜索结果，避免实时网络请求 |
| 实时搜索 | Live Search | 实时搜索互联网获取最新内容 |
| 提示词 | Prompt | 用户向 CodeX 描述任务的文字 |
| Diff | Diff | 代码修改前后的差异 |
| 沙箱模式 | Sandbox Mode | `native` / `wsl` / `none` 三种沙箱运行方式 |
| 认证方法 | Auth Method | `chatgpt`（OAuth）或 `apikey`（API Key） |
| 项目级配置 | Project Config | 项目根目录下的 `codex.toml` |
| 用户级配置 | User Config | `~/.config/codex/config.toml` |
| 命令审批 | Command Approval | CodeX 执行每条命令前的暂停等待确认机制 |
