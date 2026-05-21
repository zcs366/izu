# Claude Code 中文手册 · v1.0

> **完整版**：从入门到精通，从安装到未来展望
>
> 覆盖：Anthropic 终端 AI 编程代理的完整使用指南
>
> 版本：v1.0 · 2026年5月

---

# 第 1 章：概览与核心理念

## 1.1 什么是 Claude Code？

**Claude Code** 是 Anthropic 推出的一款**终端 AI 编程代理**（Terminal AI Coding Agent）。它不是聊天机器人，而是一个驻扎在你终端里的智能"编程搭档"——它能够理解整个代码库、读取文件、编辑代码、运行命令、操作 Git，甚至帮你部署和调试。

你可以这样理解：

> 别的 AI 工具像是帮你**写作文**的助手，而 Claude Code 是一个能**钻进你的工地、拿起工具、自己动手砌墙**的施工队长。

### 它不是：

| 误解 | 实际 |
|-------|-------|
| 聊天机器人 | 聊天只是交互方式，核心是**执行编程任务** |
| 代码补全插件 | 不是补全光标位置的下一行，而是理解整个项目后**跨文件重构** |
| 云端沙盒 | 代码在**你本地**运行，文件读写、命令执行都在你自己的机器上 |

### 它是：

- **深度代码库感知**（Codebase Awareness）：启动时自动索引项目结构、读取 `CLAUDE.md`、理解依赖关系。你不需要手动"喂"上下文。
- **交互式推理**（Interactive Reasoning）：能边思考边行动——先规划、再执行、遇到错误自动修正，整个过程你可以实时观察。
- **本地执行**（Local Execution）：Shell 命令、Git 操作、文件编辑都在你的终端里完成，不是远程沙盒。
- **权限系统**（Permission System）：每个危险操作都需要你授权——Claude 不能擅自 `rm -rf /`，除非你明确说"可以"。

---

## 1.2 为什么 Claude Code 值得关注？

想象一下这个场景：

```bash
# 你只需要说一句话：
claude "帮我写一个用户认证模块，包含注册、登录、JWT 签发和测试"
```

然后 Claude Code 会：

1. 扫描你现有的项目结构
2. 设计文件组织方案
3. 创建路由、控制器、中间件、模型文件
4. 安装依赖、配置数据库连接
5. 运行测试、修复失败的用例
6. 用 Git 提交所有变更

**你全程只需要审核和点头。**

### 核心价值总结

| 能力 | 说明 |
|-------|-------|
| 🧠 深度理解 | 读取数百个文件、建立上下文图，不是"只看光标前后三行" |
| 🔧 可操作 | 真正执行命令、写文件、改代码，不止是建议 |
| 🔁 迭代式 | 发现问题会自己回头修改，不是一次输出就完事 |
| 🛡 可控 | 每一步操作都可以征求你的同意 |
| 🧩 可扩展 | 通过插件、Skills、MCP 连接任何工具 |

---

## 1.3 竞品对比

> 💡 **类比**：如果说 AI 编程工具是"交通工具"，Claude Code 是**越野吉普车**，Cursor 是**特斯拉**，Copilot 是**电动自行车**，Aider 是**自己组装的改装车**。

| 维度 | Claude Code | Cursor | GitHub Copilot | Codex CLI (OpenAI) | Aider |
|------|-------------|--------|----------------|-------------------|-------|
| **形态** | 终端原生 CLI | IDE 集成 | IDE 扩展插件 | 终端 CLI | 终端 CLI |
| **代码感知** | 全项目索引 | 全项目索引 | 局部上下文 | 全项目索引 | 部分文件 |
| **执行能力** | Shell/Git/文件全权 | IDE 内操作 | IDE 内补全 | Shell/Git/文件 | Shell/Git/文件 |
| **推理模型** | Claude Sonnet/Opus | 可切换多个模型 | GPT-4o/Claude | o4-mini 等 | 可切换 API |
| **权限控制** | 完善的权限系统 | IDE 内自然约束 | 有限 | 基础 | 基础 |
| **插件生态** | Skills/MCP/Plugins | 扩展有限 | 扩展有限 | 无 | 无 |
| **多人协作** | CLAUDE.md 团队共享 | 无 | 无 | CLI 配置 | 无 |
| **开源** | ✓ (GitHub 121k ⭐) | 否 | 否 | ✓ | ✓ |
| **价格** | $20/月起订阅 | $20/月起 | $10/月起 | 按 API 用量 | 按 API 用量 |

### 简单选择指南

- **想要 IDE 内的一体化体验？** → 选 **Cursor**
- **只是想要代码补全和简单问答？** → 选 **Copilot**
- **想要终端里最强大的自主编程代理？** → 选 **Claude Code**
- **预算有限、愿意自己折腾？** → 选 **Aider** 或 **Codex CLI**
- **想要开源且自建？** → **Claude Code（开源）** 或 **Aider**

---

## 1.4 生态全景

Claude Code 不只是一个人工智能工具——它是一整个生态系统的核心。

```
┌─────────────────────────────────────────┐
│            Claude Code                   │
│        (终端 AI 编程代理核心)              │
├─────────────────────────────────────────┤
│  CLI 界面  │  VS Code 扩展  │  Web 版    │
│  Desktop   │  JetBrains    │  Cursor     │
├─────────────────────────────────────────┤
│  Skills     │  Plugins     │  MCP 服务    │
│  Hooks      │  Sub-agents  │  Agent SDK  │
│  CLAUDE.md  │  Auto Memory │  自定义配置  │
└─────────────────────────────────────────┘
```

### 关键资源速查

| 资源 | 地址 | 用途 |
|------|------|------|
| 📄 官方文档 | [code.claude.com/docs](https://code.claude.com/docs) | 完整参考 |
| 💻 GitHub 仓库 | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) | 121k ⭐ 开源代码 |
| 🔌 插件市场 | [code.claude.com/plugins](https://code.claude.com/plugins) | 社区插件 |
| 🛠 MCP 规范 | [modelcontextprotocol.io](https://modelcontextprotocol.io) | 工具连接标准 |
| 💬 Discord | [discord.gg/8nwwASB4dr](https://discord.gg/8nwwASB4dr) | 社区讨论 |

---

## 1.5 核心类比：乐高 vs 成品模型

> 理解 Claude Code 最好的方式，是理解**乐高（LEGO）和成品模型（Pre-built Model）的区别**。

| | 🧱 乐高（Claude Code） | 🚗 成品模型（其他 AI 工具） |
|--|------------------------|---------------------------|
| **控制权** | 每一块砖你都可以自己拼 | 只能按说明书开 |
| **灵活性** | 想搭什么搭什么 | 只能做预设的事 |
| **修改成本** | 随时拆了重来 | 改一下整个结构都受影响 |
| **学习曲线** | 一开始要读说明书 | 开箱即用 |
| **天花板** | 无限可能 | 取决于模型的设计上限 |

**Claude Code 的理念：** 给你工具和砖块（终端、文件系统、Shell、Git），然后你在上面搭建任何你想要的开发工作流。

> 它不是告诉你"答案"——它是和你一起**建造答案**。

---

# 第 2 章：安装部署全指南

## 2.1 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| **操作系统** | macOS 12+ / Linux (任意发行版) / Windows 10+ (WSL2) | macOS 14+ / Ubuntu 22.04+ / Windows 11 + WSL2 |
| **内存** | 4 GB RAM | 16 GB+ RAM |
| **存储** | 500 MB 空闲 | 2 GB+（用于缓存和会话） |
| **网络** | 需要互联网连接 | 宽带连接 |
| **Shell** | Bash / Zsh / PowerShell 5+ | 支持 Unicode 和 256 色的终端 |
| **Git** | Git 2.0+ | Git 2.30+ |
| **Node.js** | 不需要（原生安装） | 不需要（但如果用 npm 方式则需要 Node 18+） |

> ⚠️ **注意**：Claude Code 需要网络连接来调用 Anthropic 的 API。离线模式不适用。

---

## 2.2 安装方式全览（按推荐度排序）

### 🥇 方法一：原生二进制安装（推荐）

这是**官方推荐的安装方式**——独立二进制文件，不依赖 Node.js、Python 或其他运行时。

**macOS / Linux / WSL：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**这个命令做了什么：**
1. `curl -fsSL` — 从 `claude.ai` 下载安装脚本（-f 失败时静默，-s 静默模式，-S 显示错误，-L 跟随重定向）
2. `| bash` — 将下载的脚本传给 bash 执行
3. 脚本会自动检测你的操作系统和架构，下载对应版本的二进制文件
4. 安装到 `~/.claude/` 目录下
5. 自动配置 PATH，使 `claude` 命令全局可用

**Windows PowerShell（管理员）：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD：**

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> 💡 **小提示**：如果看到 `The token '&&' is not a valid statement separator` 的错误，说明你在 PowerShell 里而不是 CMD。

**优点：** 最快、最稳定、自动更新、无依赖冲突

---

### 🥈 方法二：Homebrew（macOS）

```bash
# 安装稳定版
brew install --cask claude-code

# 或者安装最新版（包含预发布功能）
brew install --cask claude-code@latest

# 更新
brew upgrade claude-code
```

**注意：** Homebrew 安装的版本**不会自动更新**——你需要定期运行 `brew upgrade`。

---

### 🥉 方法三：WinGet（Windows）

```powershell
# 安装
winget install Anthropic.ClaudeCode

# 更新
winget upgrade Anthropic.ClaudeCode
```

---

### 方法四：npm（已弃用，但仍可用）

```bash
npm install -g @anthropic-ai/claude-code
```

**⚠️ 重要：**
- 不要使用 `sudo npm install -g`
- 需要 Node.js 18+
- 不会自动更新

---

### 方法五：Linux 包管理器

**Debian / Ubuntu：**
```bash
apt update
apt install claude-code
```

**Fedora / RHEL：**
```bash
dnf install claude-code
```

---

### 方法六：npx 临时使用

```bash
npx @anthropic-ai/claude-code
```

---

## 2.3 Windows 安装选项对比

| 方案 | 体验 | 难度 | Shell 类型 | 推荐场景 |
|------|------|------|-----------|---------|
| **原生 Windows**（PowerShell） | ⭐⭐⭐ | 低 | PowerShell | 简单任务 |
| **原生 Windows**（CMD + Git Bash） | ⭐⭐⭐ | 中 | Bash (Git Bash) | 需要 Bash 工具链 |
| **WSL 2**（推荐） | ⭐⭐⭐⭐⭐ | 中 | 完整 Linux Bash | 严肃开发、全功能体验 |
| **WSL 1** | ⭐⭐⭐ | 中 | Linux Bash | 磁盘性能不如 WSL2 |

> **推荐所有 Windows 开发者使用 WSL2。**

---

## 2.4 身份验证与账户

| 账户类型 | 适用场景 | 获取方式 |
|---------|---------|---------|
| **Claude Pro** ($20/月) | 个人开发者、日常使用 | claude.com/pricing |
| **Claude Max** ($100-$200/月) | 重度用户 | claude.com/pricing |
| **Team** | 小型团队协作 | claude.com/team |
| **Enterprise** | 企业级部署 | 联系销售 |
| **Console (API)** | 按量付费 | console.anthropic.com |

### 登录方式

```bash
# 交互式浏览器登录（推荐）
claude

# API Key
export ANTHROPIC_API_KEY="sk-ant-PLACEHOLDERyour-api-key-here"

# SSO（企业）
claude auth login --sso

# Console
claude auth login --console
```

---

## 2.5 验证安装

```bash
# 查看版本
claude --version

# 健康检查
claude doctor
```

**`claude doctor` 会告诉你：**
- ✅ 安装类型
- ✅ 当前版本
- ✅ 认证状态
- ✅ 配置文件位置
- ✅ 环境变量状态
- ❌ 任何配置问题

---

## 2.6 更新方法

| 安装方式 | 更新命令 | 是否自动更新 |
|----------|---------|------------|
| 原生二进制 | `claude update` | ✅ 后台自动更新 |
| Homebrew | `brew upgrade claude-code` | ❌ 需手动 |
| WinGet | `winget upgrade Anthropic.ClaudeCode` | ❌ 需手动 |
| npm | `npm update -g @anthropic-ai/claude-code` | ❌ 需手动 |

**发布渠道：**

```bash
# 安装最新稳定版
claude install stable

# 安装最新版
claude install latest

# 安装特定版本
claude install 2.1.118
```

---

# 第 3 章：界面与基础操作

## 3.1 交互模式（Interactive Mode）

```bash
# 进入交互模式
cd your-project
claude
```

你会看到一个提示符，然后就可以开始自然语言对话。Claude 会扫描你的项目，读取文件，理解代码结构。

**交互模式的特点：**
- ✅ 可以持续对话，Claude 会记住上下文
- ✅ 每次操作前会征求你的许可
- ✅ 支持多轮交互——修改 → 验证 → 再修改
- ✅ 可以随时打断、纠正、追加需求

### 启动时带初始提示

```bash
claude "解释一下这个项目的架构"
```

---

## 3.2 打印模式（Print Mode）

用于**一次性查询**——Claude 执行任务后直接输出结果并退出。

```bash
# 基本用法
claude -p "这个函数是做什么的？"

# 带具体文件
claude -p "src/utils.ts 中有哪些导出函数？"
```

**适用场景：**
- 快速代码解释
- 单次代码审查
- CI/CD 流水线中的自动化检查

---

## 3.3 管道模式（Pipe Mode）

将其他命令的输出通过管道传给 Claude Code：

```bash
# 查看日志中的错误
cat production-error.log | claude -p "分析这些日志，找出最常见的错误类型"

# diff 审查
git diff main | claude -p "审查这些变更，找出潜在问题"

# 结合 curl
curl -s https://api.example.com/health | claude -p "检查这个 API 响应是否有异常"
```

> 💡 **类比**：管道模式就像你把一张**素描草稿**递给 Claude，说"帮我上色"。

---

## 3.4 会话管理

| 命令 | 用途 | 示例 |
|------|------|------|
| `claude -c` | 继续当前目录最近的会话 | `claude -c` |
| `claude -c -p "query"` | 继续最近会话 + 一次性查询 | `claude -c -p "检查类型错误"` |
| `claude -r "<name>"` | 按名称恢复指定会话 | `claude -r "auth-refactor"` |
| `--name "name"` | 给当前会话命名 | `claude --name "重构用户模块"` |

---

## 3.5 核心斜杠命令（Slash Commands）

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `/help` | 显示所有命令 | 新手入门、忘记命令时 |
| `/compact` | 压缩对话历史为摘要 | 上下文窗口快满时（**最重要的命令**） |
| `/cost` | 显示 token 用量和费用 | 监控预算 |
| `/doctor` | 健康检查 | 排查问题 |
| `/init` | 初始化项目配置 | 新项目首次使用 |
| `/model` | 切换 Sonnet/Opus/Haiku | 需要更强推理或更快响应时 |
| `/permissions` | 循环切换权限模式 | 临时放宽/收紧权限 |
| `/review` | 审查当前变更 | 提交前检查 |
| `/clear` | 清除所有对话历史 | 从头开始 |
| `/plan` | 只读探索模式 | 设计阶段先讨论不清除代码 |
| `/fast` | 快速响应模式 | 需要快速答案 |

### `/compact` — 上下文救星

```bash
You: /compact

Claude: 已压缩对话历史。
      从 15,234 tokens 压缩至 2,187 tokens。
      保留了关键上下文：项目结构、已做出的决策、待办事项。
```

> 💡 类比：`/compact` 就像**收拾房间**——东西太多时整理一下。

**何时使用：**
- 对话超过 20 轮后
- Claude 开始"忘记"早期上下文时
- 准备讨论新话题前
- 每次 `/cost` 显示 token 用量过高时

---

## 3.6 @ 引用：文件和目录

```bash
You: 帮我看看 @package.json 里的依赖版本对不对
You: 重构 @src/utils/ 目录下的所有工具函数
You: 对比 @src/old.ts 和 @src/new.ts 的区别
```

**规则：**
- `@filename` — 引用当前目录下的文件
- `@dirname/` — 引用目录
- `@./path/to/file` — 相对路径引用
- 可以使用 Tab 自动补全路径

---

## 3.7 ! Shell 命令

```bash
You: !node --version
# 输出: v20.11.0

You: !npm test
# 运行测试并在对话中查看结果
```

任何以 `!` 开头的行都被当作 Shell 命令执行。

---

## 3.8 模型切换详解

| 模型 | 特点 | 适用场景 | 费用 | 速度 |
|------|------|---------|------|------|
| **Sonnet 4.6** | 默认模型，速度与质量的绝佳平衡 | ✅ 日常编码、一般重构、代码审查 | 中等 | ⭐⭐⭐⭐ |
| **Opus 4.6** | 最强推理能力，深度分析 | ✅ 复杂架构设计、跨模块重构、疑难 Bug | 较高 | ⭐⭐⭐ |
| **Haiku 4.5** | 最轻量，最快响应 | ✅ 简单问答、格式化、批量注释 | 最低 | ⭐⭐⭐⭐⭐ |

> 💡 **类比**：Sonnet 是**日常通勤车**，Opus 是**越野探险车**（强但费油），Haiku 是**电动滑板车**（便宜灵活）。

```bash
# 命令行指定模型
claude --model opus
claude --model haiku
claude --model sonnet
```

---

# 第 4 章：实战——从零搭建第一个工作流

## 4.1 场景设定

> **任务：从零开始创建一个待办事项 API**
>
> 技术栈：Node.js + Express + SQLite
> 功能：创建待办、列表查看、标记完成、删除
> 要求：有测试、有 Git 提交

---

## 4.2 第一步：初始化项目

```bash
mkdir my-todo-api
cd my-todo-api
claude
```

**你的提示词：**

```
You: 我想创建一个 Todo API 项目，使用 Node.js + Express + SQLite。
请帮我初始化项目，包括：
1. 创建 package.json（包含必要的依赖）
2. 创建基本的项目目录结构
3. 初始化 Git 仓库
4. 创建 .gitignore
```

**Claude 会做什么：**

```
Claude: 好的，让我来初始化这个项目。

  ✓ 检测到当前目录为空
  ✓ 初始化 npm 项目
  ✓ 安装依赖：express, better-sqlite3, uuid
  ✓ 安装开发依赖：jest, supertest
  ✓ 创建目录结构：
      my-todo-api/
      ├── package.json
      ├── .gitignore
      ├── src/
      │   ├── index.js
      │   ├── db.js
      │   ├── routes/
      │   └── models/
      └── tests/
  ✓ 初始化 Git 仓库
  ✓ 创建 .gitignore
```

---

## 4.3 第二步：让 Claude 设计架构

```
You: 在开始写代码之前，我希望你先给我一个架构设计。
  我想了解：
  1. 数据库表结构（需要哪些字段）
  2. API 路由设计（有哪些端点）
  3. 文件组织方式
```

**Claude 会输出架构设计**——数据库表结构、API 端点列表、文件组织方案。你可以审查后说"好的，开始写"或者提出修改意见。

---

## 4.4 第三步：编写代码

```
You: 设计很好，开始写代码吧。先从数据库配置和数据模型开始。
```

Claude 会依次创建文件，边创建边解释：`src/db.js`（数据库配置）、`src/models/todo.js`（数据模型）、`src/routes/todos.js`（路由）、`src/app.js`（应用配置）、`src/index.js`（入口文件）。

整个过程中，Claude 会展示每个文件的**创建、修改、diff**。你可以随时说"这里改成..."来调整。

---

## 4.5 第四步：添加测试

```
You: 现在帮我写测试。使用 Jest 和 Supertest，
  覆盖所有 API 端点，包括正常情况和错误情况。
```

Claude 会创建测试文件，然后**自动运行测试**：

```
Claude: 测试文件已创建，让我运行一下看看：

  ✓ POST /api/todos - 创建待办
  ✓ POST /api/todos - 缺少标题返回 400
  ✓ GET /api/todos - 获取所有待办
  ✓ GET /api/todos/:id - 不存在的 ID 返回 404
  ...
  Tests: 7 passed, 7 total
```

---

## 4.6 第五步：Git 提交

```
You: 现在帮我把所有变更提交到 Git。
  写一个有意义的提交信息，包含本次做了什么。
```

Claude 会暂存文件、创建规范的提交信息。

---

## 4.7 完整流程总结

```
cd my-todo-api && claude

┌─────────────────────────────────────────────────────┐
│ Step 1: 初始化项目 → package.json, 目录结构, Git    │
├─────────────────────────────────────────────────────┤
│ Step 2: 让 Claude 设计架构 → 数据库, API, 文件组织   │
├─────────────────────────────────────────────────────┤
│ Step 3: 编写代码 → db.js, models, routes, app.js    │
├─────────────────────────────────────────────────────┤
│ Step 4: 添加测试 → 7 个测试用例, 全部通过 ✅          │
├─────────────────────────────────────────────────────┤
│ Step 5: Git 提交 → git add, git commit, 规范信息     │
└─────────────────────────────────────────────────────┘

总用时：约 5 分钟
传统手动开发估计用时：45-60 分钟
```

---

# 第 5 章：参数详解

## 5.1 CLAUDE.md：分层配置

`CLAUDE.md` 是 Claude Code 的项目配置文件。**它是一个 Markdown 文件**，放在项目根目录下。

> 💡 **类比**：CLAUDE.md 就像是**奶茶店的配方手册**——新员工（Claude）进来先看这个，就知道这家店的奶茶要加多少糖、用什么茶底。

### 分层结构

```
项目根目录/CLAUDE.md          ← 项目级配置（提交到 Git，团队共享）
├── .claude/CLAUDE.md         ← 子目录级配置（覆盖上级）
~/.claude/CLAUDE.md           ← 全局配置（个人偏好，不共享）
```

### 实际示例

```markdown
# Todo API 项目规范

## 技术栈
- Node.js 20+, Express 4.x, better-sqlite3
- Jest + Supertest

## 代码风格
- 使用 CommonJS 模块
- 2 空格缩进，使用分号

## 架构约定
- 路由放在 src/routes/
- 数据模型放在 src/models/

## Git 规范
- 提交信息格式：type: 简短描述
- 类型：feat/fix/test/docs/refactor
```

---

## 5.2 settings.json：三层配置结构

### 配置优先级

```
最高     Managed settings（企业 IT 管理）
              ↓
        CLI 参数（临时覆盖）
              ↓
   .claude/settings.local.json（个人本地，git 忽略）
              ↓
     .claude/settings.json（项目共享，提交到 Git）
              ↓
   ~/.claude/settings.json（全局默认）
最低
```

### 项目配置示例

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Read(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": { "tool": "Edit", "pattern": "src/**" },
        "command": "npx prettier --write {{filePath}}"
      }
    ]
  }
}
```

---

## 5.3 权限系统

| 模式 | 行为 | 安全级别 |
|------|------|---------|
| `default` | 每个操作都问你 | 🛡️🛡️🛡️ |
| `acceptEdits` | 自动接受文件编辑 | 🛡️🛡️ |
| `bypassPermissions` | 跳过权限检查 | ⚠️ 危险 |
| `plan` | 只读模式 | 🛡️🛡️🛡️🛡️🛡️ |

**工具类型：**

| 工具 | 匹配语法 | 示例 |
|------|---------|------|
| `Bash` | `Bash(命令模式)` | `Bash(npm run *)` |
| `Read` | `Read(路径模式)` | `Read(.env)` |
| `Edit` | `Edit(路径模式)` | `Edit(src/**)` |
| `Write` | `Write(路径模式)` | `Write(*.md)` |

---

## 5.4 Hooks：自动化钩子

> 💡 **类比**：Hooks 就像**自动洗手程序**——每次你摸完脏东西（编辑文件），洗手台会自动出水（运行格式化工具）。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": { "tool": "Edit", "pattern": "src/**/*.js" },
        "command": "npx prettier --write {{filePath}}"
      }
    ]
  }
}
```

**模板变量：** `{{filePath}}`（操作的文件路径）、`{{projectDir}}`（项目根目录）

---

## 5.5 模型配置

```json
{
  "model": "sonnet"     // 可选: "sonnet", "opus", "haiku"
}
```

**限制可用模型列表：**

```json
{
  "availableModels": [
    "claude-sonnet-4-20260507",
    "claude-haiku-4-20260507"
  ]
}
```

---

## 5.6 maxTokens

```json
{
  "maxTokens": 4096
}
```

| 值 | 效果 | 适用场景 |
|----|------|---------|
| 1024 | 简短快速 | 简单问答 |
| 4096 (默认) | 平衡模式 | 日常编码 |
| 8192 | 长输出 | 复杂设计、大段代码生成 |

---

## 5.7 环境变量

| 变量名 | 作用 | 示例值 |
|--------|------|--------|
| `ANTHROPIC_API_KEY` | API 密钥 | `sk-ant-PLACEHOLDER...` |
| `ANTHROPIC_MODEL` | 默认模型 | `claude-sonnet-4-20260507` |
| `ANTHROPIC_BASE_URL` | API 代理 URL | `https://your-proxy.com` |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Windows 上用 PowerShell | `1` |
| `CLAUDE_CODE_SIMPLE` | 极简模式 | `1` |

---

## 5.8 MCP 配置

MCP（Model Context Protocol）是 Claude Code 连接外部工具的**万能转接头**。

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_xxxxx" }
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/Users/me/data.db"]
    }
  }
}
```

---

# 第 6 章：进阶技术详解

## 6.1 Agent Teams：多个 Claude 并行作战

在默认模式下，Claude Code 是"单线程"的。**Agent Teams** 让你担任"Team Lead"，Claude Code 会自动拆解任务、分派给多个子 Agent 并行执行。

> **类比**：单 Agent 像是你一个人做一桌子菜。Agent Teams 像你有了一个后厨团队——同时进行。

| 项目 | 说明 |
|------|------|
| 可用模型 | **仅 Opus 4.6** |
| 最大并行数 | 通常 3-8 个 |
| 定价 | 每个子 Agent 独立计费 |

**实战场景**：重构大型 monorepo 的测试框架

```bash
> /team "将 monorepo/packages 下每个包的测试从 Jest 迁移到 Vitest，并行处理"
```

> **⚠️ 注意**：Agent Teams 消耗 token 很快。一个 5 个子 Agent 的任务可能在 10 分钟内消耗掉 Pro 计划一半的配额。

---

## 6.2 Custom Slash Commands：打造你的快捷指令

自定义命令是放在 `.claude/commands/` 中的 Markdown 文件。

**结构：**
```
你的项目/.claude/commands/
├── code-review.md        # /code-review → AI 代码审查
├── add-tests.md          # /add-tests → 自动补测试
└── deploy-staging.md     # /deploy-staging → 部署到预发布
```

**示例：`/code-review.md`**

```markdown
---
title: Code Review
---

请对当前分支中所有未提交的变更进行代码审查。重点关注：
1. 潜在的性能问题
2. 安全漏洞（SQL 注入、XSS）
3. 与项目编码规范不一致之处
4. 缺少的错误处理
```

> **最佳实践**：把自定义命令提交到 Git 仓库中，整个团队都能共享。

---

## 6.3 Hooks Automation

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `PostToolUse` | 工具调用成功后 | 自动格式化代码 |
| `PreToolUse` | 工具调用前 | 安全检查 |
| `SessionStart` | 会话开始 | 加载配置 |

**实战：每次编辑后自动 lint**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "cd $CLAUDE_PROJECT_DIR && npm run lint:staged"
      }]
    }]
  }
}
```

---

## 6.4 MCP（Model Context Protocol）

MCP 是 Anthropic 推出的开放协议，你可以把它理解为"AI 的 USB 接口"——插上不同的外设，Claude 就能获得新的能力。

| MCP 服务器 | 功能 | 场景 |
|-----------|------|------|
| `mcp-github` | 访问 GitHub Issues、PRs | AI 自动提 PR |
| `mcp-postgres` | 数据库查询 | AI 分析数据 |
| `mcp-slack` | Slack 消息 | 发送通知 |
| `mcp-filesystem` | 文件系统操作 | 跨项目文件管理 |

**在 MCP 的加持下，你可以这样说：**

```text
> "查一下 GitHub Issue #342 的状态，然后去 Jira 更新对应的 ticket，最后在 Slack 上通知 @zhang 说问题已修复"
```

---

## 6.5 Plugin 系统

| 官方预装插件 | 功能 |
|------|------|
| `code-review` | 提交 PR 时自动进行 AI Code Review |
| `learning-output-style` | 教学模式输出 |
| `prompt-eng` | Prompt Engineering 模板 |

```bash
# 启用插件
> /plugin:enable code-review
```

---

## 6.6 Remote Control 模式

从手机、平板控制正在运行的 Claude Code 会话。

```bash
# 启动 Remote Control
claude --remoteControl
```

**典型场景：** 路上调试、夜间运行、团队演示

---

## 6.7 Ultrareview：非交互式代码审查

```bash
# 审查当前分支与 main 的差异
claude /ultrareview

# 审查一个 PR
claude /ultrareview --pr 42
```

**在 CI/CD 中使用：**

```yaml
name: Claude Ultrareview
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Ultrareview
        run: claude /ultrareview --pr ${{ github.event.pull_request.number }}
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## 6.8 1M Token 上下文窗口（Opus Beta）

| 项目 | 标准窗口 | 1M 窗口 |
|------|---------|---------|
| Token 容量 | 200K | 1M |
| 可用模型 | Sonnet 4.6, Opus 4.6 | Opus 4.6 (Beta) |
| 适用计划 | 全部 | Max, Team, Enterprise |

```bash
> /model
# 选择 "Opus 4.6 1M"
```

---

## 6.9 CI/CD 集成

**GitLab CI/CD：**

```yaml
claude:
  stage: ai
  image: node:24-alpine3.21
  before_script:
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - claude -p "Review this MR and fix any issues" --permission-mode acceptEdits
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
```

---

# 第 7 章：社区资源精选

> 本章从海量资源中精选出 8 个最有价值的，每个附上"一句话评价"和"学到的技能点"。

---

## 7.1 Vincent's Blog Series

| 项目 | 内容 |
|------|------|
| **适合人群** | 中高级开发者、技术主管 |
| **内容概览** | 8 篇深度技术博客，从基础到高级工作流 |
| **为什么值得看** | 英文社区中技术深度最深的系列文章 |
| **一句话评价** | "如果要花钱读一个 Claude Code 教程，就花在这套博客上。" |
| **学到的技能点** | Skill 组件设计模式、CLAUDE.md 分层策略 |

**链接**：https://blog.fsck.com/2025/10/09/superpowers/

---

## 7.2 Shipyard Cheatsheet

| 项目 | 内容 |
|------|------|
| **适合人群** | 日常使用的开发者 |
| **内容概览** | 命令行速查表，涵盖所有 CLI flag 和 Slash Commands |
| **一句话评价** | "一张纸覆盖了 80% 的日常操作。" |
| **学到的技能点** | 不常用的 CLI 参数、权限模式切换 |

**链接**：https://shipyard.build/blog/claude-code-cheat-sheet/

---

## 7.3 知乎"Claude Code 超详细完整指南"

| 项目 | 内容 |
|------|------|
| **适合人群** | 中文读者、初学者 |
| **内容概览** | 从 WSL 安装到 MCP 集成，覆盖完整使用路径 |
| **一句话评价** | "中文世界里最全面的 Claude Code 指南，没有之一。" |
| **学到的技能点** | WSL 配置、国内网络安装技巧 |

**链接**：https://zhuanlan.zhihu.com/p/1971872808159141982

---

## 7.4 NxCode 新手教程

| 项目 | 内容 |
|------|------|
| **适合人群** | 编程新手、零基础小白 |
| **一句话评价** | "入门首选，真正的零基础友好。" |

**链接**：https://www.nxcode.io/zh/resources/news/claude-code-tutorial-beginners-guide-2026

---

## 7.5 掘金"国内上手教程"

| 项目 | 内容 |
|------|------|
| **适合人群** | 国内开发者、需要解决网络问题的用户 |
| **一句话评价** | "如果你在中国用 Claude Code，先看这篇。" |
| **学到的技能点** | API 代理配置、国内镜像源选择 |

**链接**：https://juejin.cn/column/7438994991613935625

---

## 7.6 CSDN 保姆级教程

| 项目 | 内容 |
|------|------|
| **适合人群** | 安装阶段的新手 |
| **一句话评价** | "安装遇到问题？看这篇就够了。" |

**链接**：https://gitcode.csdn.net/69c20fc254b52172bc63dca1.html

---

## 7.7 Reddit r/ClaudeAI 和 r/ClaudeCode

| 项目 | 内容 |
|------|------|
| **适合人群** | 所有用户 |
| **一句话评价** | "出了问题先别开 Issue——先上 Reddit 搜一搜。" |

**链接**：https://www.reddit.com/r/ClaudeAI/

---

## 7.8 GitHub anthropics/claude-code

| 项目 | 内容 |
|------|------|
| **适合人群** | 开发者、插件作者 |
| **一句话评价** | "官方源代码是最好的文档。"（121k ⭐） |

**链接**：https://github.com/anthropics/claude-code

---

# 第 8 章：业内评价与案例分析

> 数据不会说谎。本章汇总 Claude Code 在现实世界中的真实表现。

---

## 8.1 Solo Developer：350K LOC 代码库

一位独立开发者维护 35 万行代码库：

| 指标 | 使用前 | 使用后 | 变化 |
|------|--------|--------|------|
| 每周完成功能数 | 3-4 | 12-15 | **+300%** |
| Claude Code 生成代码占比 | 0% | **80%+** | — |
| 生产效率 | 基准 | +30-40% | 显著提升 |

---

## 8.2 "4 人 × 6 个月 → 2 个月"

| 项目 | 原计划 | 实际 | 倍率 |
|------|--------|------|------|
| 团队规模 | 4 人 | 2 人 | 50% |
| 时间 | 6 个月 | 2 个月 | 33% |
| **等效效率提升** | — | — | **12 倍** |

---

## 8.3 Anthropic 内部研究：生产力悖论

| 指标 | 变化 |
|------|------|
| 个人 PR 合并数 | **+67%** |
| PR 体积 | **+154%** |
| Code Review 时间 | **+91%** |
| 整体交付速度 | **持平** |

> **生产力悖论：** 个人产出大幅增加，但团队交付速度没有提升。瓶颈从"编写代码"转移到了"审查代码"。

---

## 8.4 Morph LLM：100K 行 C 编译器

- 团队使用 Claude Code 构建了约 10 万行 C 代码的编译器
- 动用了 16 个 Agent 并行工作
- 总计消耗约 **$20,000 API 费用**
- 结果：**可运行的 C 编译器**，通过 99% GCC torture 测试

---

## 8.5 Faros ROI 模型：50 人团队

| 项目 | 数值 |
|------|------|
| 年费 | 50 × $200 × 12 = **$120,000** |
| 增量 PR | 3,200 个/年 |
| 每增量 PR 成本 | $37.50 |
| **投资回报率** | **4:1** |

---

## 8.6 竞品对比总表

| 维度 | Claude Code | Cursor | Copilot | Codex CLI | Aider |
|------|-------------|--------|---------|-----------|-------|
| SWE-bench | **80.9%** | ~45% | ~35% | ~57% | ~48% |
| 上下文 | 200K/1M | ~64K | ~64K | 128K | ~16K |
| Agent Teams | ✅ | ❌ | ❌ | ❌ | ❌ |
| MCP | ✅ | ✅ | ❌ | ❌ | ❌ |
| 自动补全 | ❌ | ✅ | ✅ | ❌ | ❌ |
| 开源 | ✅ | 部分 | 部分 | ✅ | ✅ |

---

## 8.7 就业市场信号

截至 2026 年 5 月，**86+ 个活跃职位**明确要求或优先考虑 Claude Code 技能：

| 岗位类型 | 薪资范围 | 示例描述 |
|---------|---------|---------|
| 高级软件工程师 | $95K-$300K | "你的主要工具是 Claude Code，不是你自己的打字" |
| AI Engineering Lead | $160K-$260K | "用户界面已死…知识工作者将通过 Agent 接口工作" |
| Developer Experience | — | "设计基于 Claude Code 的开发者工作流" |

---

# 第 9 章：避坑指南

> 每个问题遵循 **现象 → 原因 → 修复步骤** 的结构。

---

## 9.1 Rate Limit / 配额危机

**现象**：刚发了两条消息，就提示达到使用限制。

**原因**：长对话消耗快、Agent Teams 消耗翻倍、缓存失效 bug。

**修复**：
1. `/compact` 压缩上下文
2. 升级到 Max 计划
3. 使用 API 模式按量付费
4. `/clear` 开启新会话

---

## 9.2 源代码泄露事件（2026 年 3 月）

**现象**：Claude Code 源代码通过 npm .map 文件泄露。

**原因**：构建配置错误，npm 包包含了 Source Map 文件。

**修复**：
1. 普通用户不需要恐慌——泄露的是源代码，不是你的数据
2. 更新到最新版本
3. 轮换 API Key

---

## 9.3 生产力悖论

**现象**：个人感觉快了，团队交付没变。

**原因**：瓶颈从"写代码"转移到"审查代码"。

**修复**：
1. 设立专职审查员
2. 使用 Ultrareview 作为第一道防线
3. 设定 PR 大小限制（不超过 400 行）

---

## 9.4 复合错误（Compounding Mistakes）

**现象**：Claude 在一个 bug 基础上继续开发，导致连锁反应。

**修复**：
1. 分步确认，每次小修改后审查
2. 编写测试优先
3. 使用 Plan Mode 预先审查设计
4. 遇到方向错误立即 `/clear`

---

## 9.5 过度复杂化

**现象**：Claude 写出的代码过度设计，用了复杂模式解决简单问题。

**修复**：
1. 在 CLAUDE.md 中明确要求简洁
2. 给 Claude "预算约束"——"最多 3 个文件、100 行"
3. 人工审查不可替代

---

## 9.6 Token 成本不可预测

**修复**：
1. 设置每月预算上限
2. 使用 `/compact` 控制上下文大小
3. 订阅 Max 计划而非 API（固定费用）

---

## 9.7 模型锁定

**修复**：
1. 保持 CLAUDE.md 的通用性
2. 关注开源替代品
3. 制定退出策略

---

## 9.8 没有自动补全

**修复**：
1. 配合 VS Code 使用
2. 同时使用 Cursor + Claude Code
3. 改变工作习惯：写"需求文档"而非逐行编码

---

## 9.9 学习曲线高

**修复**：
1. 先用 Web 版 Claude
2. 使用 VS Code 插件
3. 从模板项目开始
4. 社区求助

---

## 9.10 缓存 Bug 导致 Token 暴增

**现象**：2026 年 3-4 月，大量用户报告 token 消耗异常。

**修复**：
1. 更新 Claude Code
2. 清除本地缓存：`rm -rf ~/.claude/cache`
3. Anthropic 已部分补偿受影响用户

---

## 9.11 静默限制降低（"67% dumber"事件）

**现象**：响应质量突然下降，Claude 不再深入阅读文件。

**修复**：
1. 明确要求"请先阅读文件的完整内容"
2. 切换到 Opus 模型
3. 在 CLAUDE.md 中强制要求

---

# 第 10 章：进阶技巧与最佳实践

## 10.1 CLAUDE.md 优先策略

> **CLAUDE.md 是 Claude Code 的"宪法"。花 80% 的时间写好它，剩下 20% 的时间 Claude 会自动做对事。**

**分阶段优化：**

| 阶段 | 目标 | 操作 |
|------|------|------|
| Day 1 | 让 Claude 能干活 | 写 5 行：技术栈+项目结构 |
| Week 1 | 让 Claude 少犯错 | 添加编码规范+测试要求 |
| Week 2 | 让 Claude 融入团队 | 添加 git 规范 |
| Month 1 | 让 Claude 成为专家 | 添加业务规则+架构决策 |

---

## 10.2 80/20 模型选择法则

> **80% 的任务用 Sonnet，20% 用 Opus。前者省钱，后者攻坚。**

**策略：**
1. 日常用 Sonnet（写测试、修 bug、加小功能）
2. 困难用 Opus（架构决策、跨模块重构）
3. Opus 做 Plan，Sonnet 做 Execute

---

## 10.3 Plan Mode

```bash
> /plan "我需要将用户认证系统从 JWT 迁移到 Session-based"
```

Plan Mode 输出示例：影响范围列表、分步实施方案、风险评估、预计改动量。

**最佳实践：**
- 超过 3 个文件的改动先出计划
- 架构决策让 Opus Plan

---

## 10.4 会话管理

```bash
# 命名会话
claude --name "auth-refactor"

# 恢复会话
claude --resume "auth-refactor"

# 分叉会话
> /fork "我想尝试另一种实现方式"
```

---

## 10.5 权限白名单配置

```json
{
  "permissionMode": "acceptEdits",
  "allowedTools": ["Bash", "Read", "Edit", "Write"],
  "deniedCommands": ["rm -rf", "sudo", "chmod 777"]
}
```

---

## 10.6 调试循环

**核心公式：** 修改代码 → 跑测试 → 分析失败 → 修复 → 重新跑测试

```text
> 请在 src/services/payment.ts 中实现支付超时处理逻辑。
然后运行 npm run test:payment，
如果任何测试失败，分析失败原因并修复代码。
重复直到所有测试通过。
```

---

## 10.7 学习路线图：Day 1 → Week 4

| 时间 | 目标 | 核心技能 |
|------|------|---------|
| **Day 1** | 快速上手 | 安装、第一次对话、简单修改 |
| **Day 2-3** | 核心命令 | `/help`, `/compact`, `-p` 模式 |
| **Week 1** | 深入配置 | CLAUDE.md, Custom Commands, Plan Mode |
| **Week 2** | 自动化 | Hooks, MCP, Debug Loop |
| **Week 3** | 高级场景 | Agent Teams, Ultrareview, Plugins |
| **Week 4** | 生产就绪 | CI/CD 集成, ROI 追踪, 团队推广 |

---

# 第 11 章：未来展望

> **本章为原创分析，非现有文章的拼凑。**

## 11.1 市场规模：$12.8B 的起点

2026 年 AI 编码工具市场达 **$12.8B**，但仅占全球软件开发支出（约 $1.5 万亿）的 **0.85%**。99% 的预算还未被触及。

**三个阶段：**
1. **2024-2026：工具替换期** — AI 取代传统插件
2. **2026-2028：工作流重构期** — 企业重建流程
3. **2028-2032：范式转换期** — AI Agent 主导开发

---

## 11.2 生产力悖论的解决方案

**核心判断：** 组织变革才是答案。

历史上每一次生产力革命都伴随着组织变革：
- 工业革命：作坊 → 流水线
- 软件工程：单人编程 → 敏捷团队
- AI 编码：单人+AI → AI 团队+人类监管

**需要的变革：**
1. 审查角色专业化——设立专职"AI 审查员"
2. PR 大小标准化——不超过 200-400 行
3. 审查工具升级——自动化 + AI 审查组合
4. 度量体系重构——从"代码行数"转向"有效交付"

---

## 11.3 从个体工具到 Agent 生态系统

**MCP 作为"互联网的 AI 层"：**

| HTTP | MCP |
|------|-----|
| 统一的通信协议 | 统一的协议 |
| 浏览器访问网站 | Agent 访问工具/服务 |
| 催生了 Web 2.0 | 可能催生 Agent 生态 |

---

## 11.4 开发者分流："工匠 vs 架构师"

| 维度 | 工匠 | 架构师 |
|------|------|--------|
| 核心技能 | 编写高质量代码 | 设计系统、管理复杂度 |
| 与 AI 关系 | AI 是搭档 | AI 是执行者 |
| 稀缺性 | 逐渐降低 | 越来越高 |

> 不是"谁更重要"，而是比例在变化：2026 年 1:9 → 2028 年 1:3 → 2030 年 1:1+多个 Agent

---

## 11.5 质量危机

未经审查的 AI 代码 bug 密度比人工代码高 **23%**。

**这不是 AI 的问题，而是使用方式的问题。** 解决方案：AI 不仅要写代码，还要证明代码是正确的。

---

## 11.6 定价模式的未来

| 模式 | 适用群体 |
|------|---------|
| Token-based（当前 API） | 企业、高频用户 |
| Fixed Tier（Pro/Max） | 个人、小团队 |
| Value-based（新模式） | 按产出付费 |

---

## 11.7 Claude Code 的战略位置

**先发优势：** 数据飞轮、生态锁定、品牌信任、人才密度

**威胁：** OpenAI Codex CLI、开源替代品、云厂商集成

> **判断：** Claude Code 的技术领先窗口约 12-18 个月。护城河不是模型能力，而是生态深度（MCP、插件、企业集成）。

---

## 11.8 对软件工程教育的影响

AI 不会让初级开发者失业，但会**急剧扩大"优秀开发者"和"普通开发者"之间的差距**。

> 在 AI 时代，优秀的编程能力比以往任何时候都重要——因为你要审查 AI 的代码、引导 AI 解决问题、在 AI 犯错时纠正它。

---

## 11.9 写在最后

> **我们现在处于"AI 编码的早期 Netscape 时代"——功能原始但令人兴奋，没有人能准确预测终局。**
>
> **保持好奇，保持学习，保持怀疑。**

---

# 附录：术语表

## A

**Agent（智能体）** – Claude Code 就是一个 Agent，接收指令后自主决定使用哪些工具、按什么顺序执行任务。与聊天机器人的区别：可以**自主行动**。

**Agent Teams（Agent 团队）** – Opus 4.6 提供的功能，允许同时启动多个 Agent 并行处理子任务。

---

## C

**CLAUDE.md（项目配置文件）** – 放在项目根目录的 Markdown 文件，告诉 Claude Code 技术栈、编码规范、项目结构。

**CLI（命令行界面）** – Claude Code 的交互方式，没有图形界面。

**Context Window（上下文窗口）** – Claude 一次对话能"记住"的信息量。标准 200K tokens，Opus 1M。

**Custom Slash Commands（自定义斜杠命令）** – 在 `.claude/commands/` 中创建 Markdown 文件定义快捷命令。

---

## H

**Hooks（钩子）** – 在特定事件（文件编辑后、工具调用前）自动触发脚本。

---

## M

**MCP（模型上下文协议）** – 允许 Claude Code 与外部工具交互的开放协议，类似"AI 的 USB 接口"。

---

## P

**Plan Mode（规划模式）** – 让 Claude 先输出计划，确认后再执行。

**Print Mode（打印模式）** – 使用 `-p` flag，结果直接输出到 stdout。

**Permission System（权限系统）** – 控制 Claude Code 能执行哪些操作。

**Pipe Mode（管道模式）** – 通过 `|` 将内容传给 Claude Code。

---

## R

**REPL（交互式解释器模式）** – 运行 `claude` 进入的交互模式。

**Rate Limit（速率限制）** – Pro/Max 计划下的使用配额限制。

**Remote Control（远程控制）** – 从手机/平板控制正在运行的会话。

---

## S

**Session（会话）** – 从启动到关闭之间的所有交互，可命名、恢复、分叉。

**Settings.json（设置文件）** – 定义 hooks、MCP、权限等配置。

**Sonnet / Opus / Haiku** – Claude 模型系列：日常主力/攻坚专家/轻量级。

**Subagent（子代理）** – Agent Teams 模式下分派的子任务执行者。

**SWE-bench** – 衡量 AI 编码能力的行业标准测试。Claude Code 达 80.9%。

---

## T

**Token（令牌）** – AI 模型计费的基本单位。1 token ≈ 0.75 英文字词或 0.5 中文字符。

---

## U

**Ultraview / Ultrareview（超级审查）** – 非交互式代码审查模式，适合 CI/CD 集成。

---

## W

**Workflow（工作流）** – 使用 Claude Code 完成任务的完整过程。

---

## 其他

**One-Shot（一次性模式）** – 通过 `-p` flag 一次性执行后退出。

**Interactive Mode（交互模式）** – 直接运行 `claude` 进入的对话模式。

**Plugin（插件）** – 扩展 Claude Code 功能的模块。

---

*Claude Code 中文手册 v1.0 · 2026 年 5 月 · 自动生成，示例驱动*
