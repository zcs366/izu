---
source_url: file:///mnt/i/hermes/wiki_dropbox/openclaw-manual-v1.0.md
ingested: 2026-05-11
sha256: e19f8165d2bc98a4bb8b4eb653dfa12223ab08bc8f867632a4b4af8927506f16
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: OpenClaw 中文手册 v1.0
---

# OpenClaw 中文手册 v1.0

> 来源: openclaw-manual-v1.0.md（用户存入 wiki_dropbox）

# OpenClaw 中文手册 v1.0

> 你的私人AI助手——开源、自托管、永远在线

---

## 目录

- [第一章：认识 OpenClaw——你的私人AI助手](#第一章认识-openclaw你的私人ai助手)
- [第二章：安装——把 OpenClaw 装到你的电脑上](#第二章安装把-openclaw-装到你的电脑上)
- [第三章：界面与基础操作](#第三章界面与基础操作)
- [第四章：实战——让 OpenClaw 帮你完成第一个任务](#第四章实战让-openclaw-帮你完成第一个任务)
- [第五章：核心概念详解](#第五章核心概念详解)

---

# 第一章：认识 OpenClaw——你的私人AI助手

## 什么是 OpenClaw？

想象一下，你有一个24小时待命的私人助理。你发一条微信消息，它就能帮你查资料、整理邮件、监控网站变化、定时执行任务、控制你的电脑……而且它**只为你一个人服务**，你的数据不会离开你自己的机器。

这就是 **OpenClaw**。

OpenClaw 是一个**开源的、自托管的、主动型AI助手**。它不是那种你打开网页才能聊天的AI——它住在你的聊天软件里（Telegram、WhatsApp、Discord、Slack、Signal、iMessage……），随时待命。

> **举个例子：** 早上8点，你还在刷牙，OpenClaw 通过 Telegram 发来一条消息："老板，昨晚你的GitHub仓库收到了3个PR，CI运行正常。今日北京天气晴，23°C。另外你有一封来自客户XYZ的邮件需要处理。"——这不是科幻，这是 OpenClaw 的日常。

## 谁创造了它？

OpenClaw 由 **Peter Steinberger** 创建。你可能不认识这个名字，但如果你用过 iOS 开发，你一定见过他的作品——他是 **PSPDFKit** 的创始人，iOS/macOS 领域最知名的独立开发者之一。

这很重要，因为这意味着：
- **这不是一个随机创业公司的项目**——Peter 有十几年的开源贡献历史，他的代码质量有目共睹
- **这不是一个"先圈钱再跑路"的项目**——MIT 许可证，完全开放
- **这是一个开发者写给开发者（以及最终用户）的工具**——它懂真实世界的需求

## 为什么它一炮而红？

OpenClaw 在 GitHub 上获得了 **超过 68,000 颗星**（还在快速增长），成为2024-2025年增长最快的开源项目之一。Peter Steinberger 还上了 Lex Fridman 的播客（超过800万订阅的顶级科技播客），让更多人知道了这个项目。

## 核心理念

| 理念 | 说明 |
|------|------|
| **隐私优先** | 所有数据跑在你自己的机器上，不经过第三方服务器 |
| **自托管** | 你完全拥有和控制你的AI助手 |
| **开源** | MIT 许可证，你可以查看、修改、分发代码 |
| **主动型** | 不是"你问它答"的被动工具，它会主动提醒、汇报、执行 |
| **多通道** | 你可以在任何聊天软件里使用它，不用学新界面 |

## 和 Claude Code / Copilot / ChatGPT 有什么不同？

你可能用过 ChatGPT、GitHub Copilot 或 Claude。它们很棒，但 OpenClaw 走的是完全不同的路线：

| 对比维度 | OpenClaw | ChatGPT / Claude |
|----------|----------|-----------------|
| **运行位置** | 你的电脑 | 云端服务器 |
| **数据归属** | 你完全控制 | 服务商处理 |
| **交互方式** | 聊天软件（你已有的App） | 专用网页/App |
| **主动能力** | ✓ 定时任务、监控、推送 | ✗ 被动回答 |
| **系统访问** | ✓ 操作你的文件、浏览器、系统 | ✗ 沙盒隔离 |
| **多通道** | ✓ 同时接入多个聊天平台 | ✗ 单一界面 |
| **开源** | ✓ MIT 许可证 | ✗ 闭源 |
| **费用** | 只付 API 费用（自己选模型） | 月费订阅 |

用个不太准确的类比：ChatGPT 像是公共图书馆的参考咨询台——你去问，它回答。OpenClaw 像是雇佣了一个住在家里的私人助理——它不仅回答问题，还帮你打理各种事情。

## 它能做什么？

OpenClaw 能做的事情非常多，这里列一些真实的使用场景：

**📧 信息处理**
- 读取、分类、回复邮件（Gmail、Outlook）
- 汇总 RSS 订阅源的内容
- 从 PDF/网页中提取关键信息

**📊 监控与提醒**
- 监控 GitHub 仓库的新 Issue / PR / Star
- 监控网站变化（价格监控、内容更新）
- 监控服务器状态（CPU、内存、磁盘）
- 定时发送天气预报、新闻摘要

**💬 聊天与查询**
- 在 Telegram 上问它任何问题
- 让它帮你搜索资料并总结
- 让它帮你写作、翻译、改写

**🛠 系统操作**
- 操作你的文件系统（创建、编辑、删除文件）
- 控制浏览器（打开网页、填表、截图）
- 执行终端命令
- 读写剪贴板

**⏰ 定时任务**
- 每天早上8点推送日程
- 每周一自动生成周报
- 每隔1小时检查某项数据

**🤖 多智能体协作**
- 让多个AI助手协同工作（一个负责搜索，一个负责写作，一个负责检查）

## 架构速览（简化版）

OpenClaw 的架构很简单，三个层级：

```
[你发消息] → [聊天App] → [Gateway] → [Pi Agent]
                        ↑
                  端口 18789
```

1. **Channels（通道层）**——你通过 Telegram、WhatsApp、Discord 等聊天软件发消息
2. **Gateway（网关）**——运行在本地端口 18789 上的中心进程，负责路由消息、管理会话
3. **Pi Agent（智能体）**——默认的AI代理，连接到大语言模型（如 Claude、GPT）处理你的请求

你看不到这些复杂性——你只是在聊天软件里发消息，背后的一切都是自动的。

---

# 第二章：安装——把 OpenClaw 装到你的电脑上

## 安装前准备

### 检查 Node.js

OpenClaw 需要 **Node.js 22 或 24 版本**（推荐 22 LTS）。打开终端检查：

```bash
node --version
# 应该输出 v22.x.x 或 v24.x.x
```

如果没有安装，去 [nodejs.org](https://nodejs.org/) 下载 LTS 版本。安装完成后重新打开终端验证。

> 💡 **为什么要 Node.js 22+？** 新版本的 Node.js 有更好的性能、更少的内存占用，还支持最新的 JavaScript 特性。OpenClaw 充分利用了这些新特性。

### 准备 API Key

OpenClaw 本身是免费的，但它调用大语言模型需要 API Key。推荐选择：

| 提供商 | 推荐指数 | 说明 |
|--------|----------|------|
| **Anthropic Claude** | ⭐⭐⭐⭐⭐ | 最推荐，代码能力最强，价格合理 |
| **OpenAI GPT-4o** | ⭐⭐⭐⭐ | 表现优秀，生态最成熟 |
| **OpenAI GPT-4o-mini** | ⭐⭐⭐ | 性价比高，日常够用 |
| **Google Gemini** | ⭐⭐⭐ | 免费额度大 |

去对应官网注册并获取 API Key：
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/

> **举个例子：** 如果你是个人用户，推荐用 Anthropic Claude。注册后拿到一串 `sk-ant-PLACEHOLDERxxxxxxxx` 格式的 Key，这就是你的"门票"。第一次安装时你会用到它。

## 安装方法（5选1）

### 方法一：一键安装（最简单）

打开终端，复制粘贴这一行：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

然后运行：

```bash
openclaw onboard
```

这是最简单的方法，适合大多数用户。安装脚本会自动检测你的系统、下载依赖、配置环境。

### 方法二：npm 安装（推荐给开发者）

```bash
# 全局安装
npm install -g openclaw@latest

# 启动配置向导
openclaw onboard
```

如果你想确保安装的是最新版：

```bash
npm update -g openclaw
```

> **举个例子：** 你的老板让你装 OpenClaw 做团队实验。你用 `npm install -g openclaw@latest` 安装，然后 `openclaw onboard` 启动向导。整个过程不到5分钟。

### 方法三：从 Git 源码安装（适合想自己改代码的人）

```bash
# 克隆仓库
git clone https://github.com/personalailabs/openclaw.git
cd openclaw

# 安装依赖
npm install

# 全局链接（这样可以在任意目录使用 openclaw 命令）
npm link

# 配置
openclaw onboard
```

这种方式的好处是你可以直接修改源码，改动立即生效。

### 方法四：macOS 桌面应用

如果你用的是 Mac，可以下载 OpenClaw 的 macOS 应用程序，它有漂亮的图形界面，不需要碰终端。

### 方法五：Docker / Ansible（适合服务器部署）

对于服务器部署，OpenClaw 提供 Docker 镜像和 Ansible playbook：

```bash
# Docker
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/home/node/.openclaw \
  openclaw/openclaw:latest

# 或者用 docker-compose
```

> **举个例子：** 你有一台 NAS 或者 VPS 服务器，想 24/7 运行 OpenClaw。用 Docker 部署，设置自动重启，它就一直在那了，你睡觉它也在工作。

## 第一次运行

### 配置向导

运行 `openclaw onboard` 后，你会看到一个交互式向导：

```
? 请选择一个模型提供商: (用方向键选择)
  ▸ Anthropic Claude
    OpenAI
    Google Gemini
    其他 (自定义)

? 请输入你的 API Key:
  ▸ [输入你的 Key]

? 请选择聊天通道: (空格多选)
  ▸ ◉ Telegram
    ◯ WhatsApp
    ◯ Discord
    ◯ Slack
    ◯ Signal
    ◯ iMessage

? 你想为这个 AI 取什么名字？:
  ▸ 小助手
```

一步一步回答，完成后配置就自动生成了。

### 启动 Dashboard

```bash
openclaw dashboard
```

这会启动 Web 控制界面，默认在浏览器打开 http://127.0.0.1:18789

### 配置文件在哪？

配置文件保存在 `~/.openclaw/openclaw.json`。你可以直接编辑它：

```json
{
  "name": "小助手",
  "model": {
    "provider": "anthropic",
    "apiKey": "sk-ant-PLACEHOLDERxxxxxxxx"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456:ABC-DEF..."
    }
  },
  "skills": {
    "gmail": {
      "enabled": true
    }
  }
}
```

> **安全提示：** 配置文件里有 API Key，**绝对不要**把它传到 GitHub 上。

### 获取第一个回复

假设你配置了 Telegram：

1. 在 Telegram 中搜索你的 Bot（你在向导中创建的）
2. 发送 `/start`
3. 发送一条消息："你好"
4. 几秒钟后，你会收到回复

恭喜！你的私人 AI 助手开始工作了。🎉

## 常见安装问题

| 问题 | 解决方法 |
|------|----------|
| `node: command not found` | Node.js 没安装或没加到 PATH 中 |
| `npm install -g openclaw` 报错 | 试试加 `sudo`（Linux/Mac）或用管理员终端（Windows） |
| 端口 18789 被占用 | `lsof -i :18789` 查看谁在用，关掉冲突程序 |
| Telegram Bot 没反应 | 检查 Bot Token 是否正确，Bot 是否已经 `/start` |
| API Key 报错 | 检查 Key 是否过期、余额是否充足、提供商是否正确 |
| 安装后 `openclaw` 找不到 | 重新打开终端或检查 npm 全局 bin 目录是否在 PATH 中 |

---

# 第三章：界面与基础操作

## 认识你的指挥中心

OpenClaw 有两个主要界面：

1. **Web Control UI** —— 浏览器里的管理后台
2. **聊天软件界面** —— 你真正跟 AI 聊天的地方

### Web Control UI (http://127.0.0.1:18789)

在浏览器打开 http://127.0.0.1:18789，你会看到 OpenClaw 的 Dashboard。

主要区域：

```
┌─────────────────────────────────────────┐
│  📊 Dashboard                           │
├──────────┬──────────────────────────────┤
│          │                              │
│  菜单栏   │     主工作区                  │
│          │                              │
│  ├ 聊天   │  - 消息列表                   │
│  ├ 设置   │  - 会话管理                   │
│  ├ 技能   │  - 技能配置                   │
│  ├ 会话   │  - 定时任务                   │
│  └ 定时   │  - 系统日志                   │
│          │                              │
└──────────┴──────────────────────────────┘
```

**菜单栏各选项说明：**

| 菜单 | 功能 |
|------|------|
| **聊天 (Chat)** | 查看所有消息记录，回复消息（像即时通讯软件） |
| **设置 (Settings)** | 修改配置文件、模型选择、通道配置 |
| **技能 (Skills)** | 查看和管理已安装的技能插件 |
| **会话 (Sessions)** | 管理不同的会话上下文 |
| **定时 (Cron)** | 查看和管理定时任务 |
| **日志 (Logs)** | 查看系统运行日志，排查问题 |

### 在聊天软件中与 OpenClaw 交互

这才是你日常使用的方式。配置好通道后，你在聊天软件里跟 OpenClaw 说话，就像跟一个朋友聊天一样。

**支持的命令：**

```
/help           - 查看帮助
/reset          - 重置当前会话
/stats          - 查看使用统计
/mode           - 切换模式（快速/深入/创意）
/canvas         - 打开 Live Canvas
```

> **举个例子：** 你给 OpenClaw 发消息："帮我查一下明天的天气"。它回复："好的，正在查询你的位置... 明天北京天气：晴，23-28°C，东南风3级。需要我添加提醒吗？"——整个过程就像跟一个同事聊天。

## 配置聊天通道

### Telegram

Telegram 是最容易配置的通道：

1. 在 Telegram 中搜索 **@BotFather**
2. 发送 `/newbot`，按提示创建新 Bot
3. 拿到 Bot Token（格式：`1234567890:ABCdefGHIjkl...`）
4. 在 OpenClaw Dashboard 的 Settings → Channels 中填入 Token

```
你: @BotFather /newbot
BotFather: 好的，请给你的 Bot 取个名字
你: 我的小助手
BotFather: 好的，请设置用户名
你: MyLittleHelperBot
BotFather: 完成了！你的 Bot Token:
  1234567890:ABCdefGHIjkl...
```

### WhatsApp

WhatsApp 配置需要 WhatsApp Business API 或第三方桥接服务。目前最简单的方式是通过 Docker 运行 whatsapp-web.js 桥接。

### Discord

1. 去 [Discord Developer Portal](https://discord.com/developers/applications)
2. 创建新 Application → Bot
3. 复制 Token
4. 在 OpenClaw Settings 中配置

### 同时使用多个通道

OpenClaw 支持**同时运行多个通道**。你可以：
- 在公司用 Slack 跟它说话
- 回家用 Telegram 继续同一个会话
- 手机上用 WhatsApp 让它查东西

所有通道共享同一个大脑，会话是同步的。

## 理解 soul.md——AI 的灵魂

`soul.md` 是 OpenClaw 最重要的概念之一。它是一个 Markdown 文件，定义了 AI 的"人格"——它怎么说话、用什么语气、有什么偏好。

默认的 `soul.md` 在 `~/.openclaw/soul.md`，大致是这样的：

```markdown
# 你的角色
你是一个乐于助人的 AI 助手，名字叫"小助手"。

# 沟通风格
- 用中文回复，语气友好
- 回答要简洁，但必要时可以详细
- 如果不知道，就老实说不知道，不要瞎编

# 行为准则
- 优先使用工具和技能来回答问题
- 对于敏感操作需要用户确认
- 记录重要信息到记忆中
```

**你可以完全自定义它**。想让它像管家？像老师？像朋友？改 `soul.md` 就行。

> **举个例子：** 你希望 OpenClaw 像一个严厉的健身教练。在 `soul.md` 中写上：
> ```markdown
> # 你的角色
> 你是一个严格的私人健身教练。说话要简短有力，带点吐槽风格。用户偷懒的时候要 push 他。
> 
> # 沟通风格
> - 多用感叹号！
> - 用"兄弟"称呼用户
> - 如果用户说"不想动"，回："兄弟，你的腹肌不会自己长出来。做30个俯卧撑，现在！"
> ```
> 然后 AI 说话就会变成教练风格。

## 第一次对话：试试什么？

安装配置完成后，试试这些对话，感受 OpenClaw 的能力：

**基础对话：**
```
你: 你好，你叫什么名字？
你: 现在几点了？
你: 帮我查一下今天的天气
```

**系统操作：**
```
你: 帮我创建一个文件夹叫 test-project
你: 看看我桌面上有什么文件
你: 帮我写一个 Python 脚本，计算 Fibonacci 数列
```

**信息查询：**
```
你: 帮我查一下 openclaw 的 GitHub star 数量
你: 最新的 AI 新闻是什么？
你: 帮我搜索 TypeScript 中的 Promise.all 用法
```

**定时任务：**
```
你: 每天早上8点提醒我起床
你: 每2小时检查一次我的 GitHub 邮箱
```

---

# 第四章：实战——让 OpenClaw 帮你完成第一个任务

这一章我们不谈理论，直接上手做事。以下是三个真实场景，手把手带你完成。

## 实战 1：让 OpenClaw 帮你整理电子邮件

### 场景描述
每天收到几十封邮件，重要的被淹没。你想让 AI 帮你自动筛选、分类、汇总。

### 前置条件
- Gmail 账号
- OpenClaw 已安装并运行

### 步骤

**第一步：连接 Gmail 账号**

在 Dashboard 中进入 Settings → Skills，找到 Gmail 技能：

```json
{
  "gmail": {
    "enabled": true,
    "label": "工作",
    "checkInterval": 15
  }
}
```

把 `enabled` 设为 `true`，然后按提示完成 OAuth 授权（会跳转到 Google 登录页面）。

> **为什么要设 checkInterval？** 这表示每15分钟检查一次新邮件。设得太短（比如1分钟）会消耗大量 API 额度，设得太长（比如60分钟）可能错过重要邮件。

**第二步：编写一个简单的技能**

创建一个文件 `~/.openclaw/skills/email-summary.json`：

```json
{
  "name": "邮箱摘要",
  "description": "每天早上8点发送邮件摘要",
  "trigger": "cron",
  "schedule": "0 8 * * 1-5",
  "action": "检查今天的未读邮件，按重要性排序，汇总不超过5封最重要的，用中文发送摘要给我"
}
```

这里的 `"0 8 * * 1-5"` 是 cron 表达式，意思是"工作日早上8点"。

**第三步：测试**

直接在聊天软件中发送：

```
你: 帮我看一下我的未读邮件
OpenClaw: 正在检查...你有6封未读邮件。按重要性排序：
1. [重要] 客户XYZ 项目提案反馈 - 需要今天回复
2. [重要] 团队周报提醒 - 请提交本周工作汇报
3. [普通] 新闻订阅 - Newsletter #42
4. [普通] 物流通知 - 快递已送达
5. [广告] 促销活动
6. [广告] 新品推荐
需要我帮你回复第1封吗？
```

**第四步：验证定时任务**

到第二天早上8点，你会准时在聊天软件中收到邮件摘要。如果有问题，可以在 Dashboard 的 Logs 中查看日志。

## 实战 2：让 OpenClaw 监控你的 GitHub 仓库

### 场景描述
你维护一个开源项目，想跟踪新 Issue、PR、Star 的变化，但不想天天刷 GitHub 页面。

### 步骤

**第一步：安装 GitHub 技能**

在 Dashboard 的 Skills 中搜索 GitHub，启用它。配置：

```json
{
  "github": {
    "enabled": true,
    "repositories": [
      "your-username/your-repo"
    ],
    "events": ["issues", "pull_requests", "stars"]
  }
}
```

**第二步：测试查询**

```
你: 检查 my-username/my-project 的最近活动
OpenClaw: 过去24小时：
- 新增2个 Issue (#42, #43)
- 1个新 PR (#17)
- 3个新 Star ⭐
- CI 构建全部通过 ✅
需要我详细汇报吗？
```

**第三步：设置主动推送**

```
你: 每天上午10点汇报 GitHub 仓库状态
```

OpenClaw 会自动创建一个 cron 任务。你也可以手动编辑：

```json
{
  "name": "GitHub日报",
  "trigger": "cron",
  "schedule": "0 10 * * *",
  "action": "检查 my-username/my-project 过去24小时的活动，生成简要报告"
}
```

> **举个例子：** 你的开源项目突然爆火，一天涨了1000个 Star。OpenClaw 在第二天早上10点推给你："你的项目昨天涨了1000颗星！主要来自 Reddit 的 r/programming 帖子推荐。"——你还在睡觉呢，它已经帮你分析完了。

## 实战 3：用 Telegram 跟 OpenClaw 聊天查资料

### 场景描述
你在学习一个新框架（比如 Next.js），边学边在 Telegram 上问 OpenClaw。

### 对话示例

```
你: 我想学 Next.js，从哪里开始？
OpenClaw: 我建议你从 Next.js 官方教程开始。不过让我先帮你查一下你电脑上有没有相关的学习资料。

[OpenClaw 自动扫描了你的电脑]

OpenClaw: 我发现你桌面上有一个 nextjs-notes.md 文件，是不是你之前保存的？要不要我帮你整理一下？

你: 对！帮我整理成学习计划
OpenClaw: 好的，根据你的笔记，我整理了一个4周学习计划：
第1周：基础概念（路由、页面、布局）
第2周：数据获取（SSR、SSG、ISR）
第3周：API 路由和中间件
第4周：部署和优化

要我把这个计划存到你的日历吗？

你: 好，帮我保存
OpenClaw: 已保存到 your-notes/nextjs-study-plan.md
```

> 💡 **注意关键点：** OpenClaw 不只是回答你的问题——它**主动发现**你电脑上有相关的笔记，**主动提出**帮你整理，还**主动建议**存入日历。这就是"主动型AI"的含义。

## 实战 4：定时任务——让 AI 替你值班

### 场景描述
周末你不想盯着工作消息，但有些重要的事情不想错过。

```
你: 从今天到周日，帮我监控 server-status 页面，如果返回 5xx 错误，立刻通知我
OpenClaw: 好的，我会每5分钟检查一次 https://status.yourcompany.com。如果发现错误，立即在 Telegram 通知你。
```

然后你安心过周末。如果服务器出问题了，你会收到这样的消息：

```
🔴 服务器告警！
时间：2026-05-09 14:32:17
页面：https://status.yourcompany.com
状态：502 Bad Gateway
持续：已持续3分钟
建议：检查 Nginx 是否在运行，或者联系运维团队
```

---

# 第五章：核心概念详解

这一章深入讲解 OpenClaw 的每一个核心概念。你可以把它当作参考手册，遇到不明白的概念时回来查阅。

## 5.1 soul.md —— AI 的灵魂文件

### 什么是 soul.md？

`soul.md` 是一个 Markdown 文本文件，位于 `~/.openclaw/soul.md`。它定义了 AI 助手的**人格、语气、行为准则**。可以理解为 AI 的"出厂设置说明书"。

### 为什么需要 soul.md？

大语言模型本身是"一张白纸"——它可以模仿任何风格，但如果没有指导，它的回复会变得通用而无聊。`soul.md` 就是那张"指导说明书"，告诉它：
- 你是谁（角色定位）
- 你怎么说话（语言风格）
- 你该做什么、不该做什么（行为边界）

### soul.md 结构

一个典型的 `soul.md` 包含以下部分：

```markdown
# 角色定义
你是谁，你的名字叫什么

# 沟通风格
语气、用词习惯、回复长度偏好

# 行为准则
什么能做、什么不能做、需要用户确认的操作

# 技能偏好
优先使用哪些工具和技能

# 个性特征
一些额外的个性设定（幽默感、正式程度等）
```

### 自定义示例

**版本1：职场助手风格**
```markdown
# 角色定义
你是"小秘"，一个专业的职场 AI 助手。

# 沟通风格
- 使用正式但友好的商务语气
- 回复要结构化：先说结论，再列细节
- 对时间敏感的事情要标注优先级

# 行为准则
- 处理文档时一定要确认版本
- 发送邮件前必须让用户审核内容
- 不主动读取公司机密文件

# 技能偏好
- 优先使用日历、邮件、文档技能
```

**版本2：技术极客风格**
```markdown
# 角色定义
你是 GeekPal，一个热爱技术的 AI 伙伴。

# 沟通风格
- 说话可以随意一点，带点 geek 幽默
- 技术问题要给出代码示例
- 喜欢用 emoji 🚀

# 行为准则
- 写代码前先检查是否有更好的方案
- 指出潜在的安全风险和性能问题
- 可以主动阅读用户的代码并提出改进建议

# 技能偏好
- 优先使用 shell、git、代码编辑器技能
```

> **举个例子：** 同样的"帮我看看这个项目的代码"请求，两个风格回复完全不同：
> - 职场助手："好的，正在分析项目结构。代码符合基本规范，建议增加单元测试覆盖。"
> - 技术极客："好嘞！让我看看你的代码 🚀 ... 嗯，第42行这个循环可以用 map 简化，改完给你看。"

## 5.2 Gateway —— 中央路由网关

### 什么是 Gateway？

Gateway 是 OpenClaw 的**中央进程**。它运行在本地端口 **18789** 上，是连接所有组件的"交通枢纽"。

### Gateway 的职责

```
[Telegram] ─┐
[WhatsApp] ──┼──→ [Gateway (端口18789)] ──→ [Pi Agent] ──→ [AI模型]
[Discord]  ──┘        │
                       ├──→ [文件系统]
                       ├──→ [浏览器]
                       ├──→ [Shell]
                       └──→ [其他技能]
```

1. **消息路由**：接收来自任何通道的消息，转发给 AI 代理处理
2. **会话管理**：维护每个会话的历史记录
3. **技能调度**：调用安装的技能插件
4. **定时触发**：管理 cron 任务的执行
5. **安全控制**：访问控制、鉴权

### 启动与停止

```bash
# 启动 Gateway（前台模式）
openclaw start

# 后台运行
openclaw start --daemon

# 停止
openclaw stop

# 查看状态
openclaw status
```

### 配置文件中的 Gateway 设置

在 `~/.openclaw/openclaw.json` 中：

```json
{
  "gateway": {
    "port": 18789,
    "host": "127.0.0.1",
    "allowRemote": false,
    "maxSessions": 50
  }
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `port` | 18789 | 网关端口 |
| `host` | 127.0.0.1 | 监听地址（设为 `0.0.0.0` 允许局域网访问） |
| `allowRemote` | false | 是否允许远程访问 |
| `maxSessions` | 50 | 最多同时维护的会话数 |

> ⚠️ **安全提醒：** 除非你通过 Tailscale 等工具做了权限控制，否则不要把 `allowRemote` 设为 `true`。

## 5.3 Pi Agent —— 默认 AI 智能体

### 什么是 Pi Agent？

Pi Agent 是 OpenClaw 的**默认 AI 代理**。它是"大脑"——接收你的请求，调用工具，生成回复。

### Pi Agent 的工作流程

```
你的消息 → Pi Agent 分析意图
            ↓
        选择工具：
        ├── 搜索网络 → 调用浏览器
        ├── 读取文件 → 调用文件系统
        ├── 执行命令 → 调用 Shell
        └── 其他技能 → 调用对应插件
            ↓
        整合结果 → 生成回复 → 返回给你
```

### Pi Agent 的配置

```json
{
  "agent": {
    "type": "pi",
    "model": "claude-sonnet-4-20250514",
    "maxTokens": 8192,
    "temperature": 0.7,
    "systemPrompt": "你是一个有用的 AI 助手"
  }
}
```

| 参数 | 说明 |
|------|------|
| `model` | 使用的 AI 模型（不同模型能力不同） |
| `maxTokens` | 最大回复长度（越长越详细但越贵） |
| `temperature` | 创造性程度（0=严格，1=有创意，推荐0.7） |

> **举个例子：** 你写代码时用 `temperature: 0.2` 和 `maxTokens: 4096`，回复精确而简洁。头脑风暴时用 `temperature: 0.9`，AI 会给出更多创意性建议。

### 多模型支持

Pi Agent 支持多个 AI 模型提供商，你可以在配置中随时切换：

```json
{
  "agent": {
    "primary": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514"
    },
    "fallback": {
      "provider": "openai",
      "model": "gpt-4o"
    }
  }
}
```

这样如果主模型不可用，会自动切换备用模型。

## 5.4 Sessions —— 会话与上下文

### 什么是 Session？

Session（会话）是 OpenClaw 维护的**对话上下文**。每次你跟它对话时，它都记得前面说了什么，所以能进行连续的多轮对话。

### 会话生命周期

```
创建会话 → 对话进行中 → 超时/重置 → 结束
    ↑                        ↓
    └──────── 可恢复 ────────┘
```

- **创建**：你发第一条消息时自动创建
- **保持**：每次对话都在同一个会话中
- **超时**：默认30分钟无活动后自动存档
- **重置**：发送 `/reset` 或手动清除

### 会话管理

在 Dashboard 的 Sessions 面板，你可以：
- 查看所有活跃会话
- 查看会话历史
- 手动清理会话
- 导出会话内容

### 多设备同会话

你在 Telegram 上问了一个问题，然后在 WhatsApp 上继续——因为它们连接到同一个 Gateway，所以共享同一个会话上下文。

> **举个例子：** 你在公司用 Slack 说："帮我写一份项目计划书。"AI 说好的，开始了。回家路上你在手机用 Telegram 接着说："刚才的计划书，把第三章改成xxx。"——AI 记得你说的是哪个计划书，继续修改。不用重新解释。

## 5.5 Skills & Plugins —— 技能与插件

### 什么是 Skills？

Skills 是 OpenClaw 的**扩展能力**。每个 Skill 赋予 AI 一个新的"技能"——比如读取邮件、操作 GitHub、控制浏览器。

### 技能类型

| 类型 | 说明 | 例子 |
|------|------|------|
| **内置技能** | 随 OpenClaw 自带 | 文件系统、Shell、浏览器 |
| **官方插件** | 由开发团队维护 | Gmail、GitHub、Notion、Slack |
| **社区插件** | 由社区贡献 | Twitter、Jira、Figma |
| **自定义技能** | 你自己写 | 任何你需要的功能 |

### 安装技能

在 Dashboard 的 Skills 面板浏览和安装，或者用命令：

```bash
# 安装官方技能
openclaw skill install gmail

# 安装社区技能
openclaw skill install my-custom-skill

# 列出已安装技能
openclaw skill list
```

### 编写自定义技能

技能是一个 JSON 文件，定义触发条件和执行逻辑：

```json
{
  "name": "天气助手",
  "description": "查询天气预报",
  "version": "1.0.0",
  "triggers": [
    {
      "pattern": "(今天|明天|后天).*天气",
      "action": "getWeather"
    }
  ],
  "actions": {
    "getWeather": {
      "type": "api_call",
      "url": "https://api.openweathermap.org/data/2.5/weather",
      "params": {
        "q": "{{city}}",
        "appid": "{{API_KEY}}",
        "units": "metric"
      },
      "response": "{{city}}的天气：{{weather}}, 温度{{temp}}°C"
    }
  }
}
```

> **举个例子：** 你想让 OpenClaw 监测某个网站的某个按钮是否变成"已售罄"。写一个自定义技能，每隔5分钟检查一次，如果状态变了就通知你。这个过程不需要写任何后端代码——技能框架帮你处理了定时、请求、通知。

## 5.6 Cron/Scheduling —— 定时任务

### 什么是 Cron？

Cron 是 OpenClaw 的**定时任务系统**。你可以让 AI 在指定时间自动执行任务——就像设置闹钟一样。

### 创建定时任务

**方法1：对话式创建（最简单）**

```
你: 每天早上8点提醒我开会
OpenClaw: 好的，已设置每天早上8:00（工作日）提醒你"开会时间"。
```

**方法2：Dashboard 创建**

在 Cron 面板中新建任务，填写：
- 名称
- 执行时间（cron 表达式）
- 执行内容
- 目标通道

**方法3：配置文件创建**

```json
{
  "cron": [
    {
      "name": "每日天气",
      "schedule": "0 7 * * *",
      "action": "查询今天的天气预报并发送给我",
      "channel": "telegram"
    },
    {
      "name": "每周报告",
      "schedule": "0 9 * * 1",
      "action": "生成本周的工作周报",
      "channel": "slack"
    }
  ]
}
```

### Cron 表达式速查

```
* * * * *
┬ ┬ ┬ ┬ ┬
│ │ │ │ └── 星期 (0-7, 0和7都是周日)
│ │ │ └──── 月份 (1-12)
│ │ └────── 日期 (1-31)
│ └──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

常用示例：
| 表达式 | 含义 |
|--------|------|
| `0 8 * * *` | 每天早上8点 |
| `0 9 * * 1-5` | 工作日早上9点 |
| `*/30 * * * *` | 每30分钟 |
| `0 0 * * 0` | 每周日午夜 |
| `0 0 1 * *` | 每月1号凌晨 |

### 查看已创建的定时任务

```
你: 看看我有哪些定时任务
OpenClaw: 你有3个定时任务：
1. 每日天气 - 每天早上7点 - Telegram ✅
2. 晨间简报 - 工作日9点 - Slack ✅
3. 服务器检查 - 每30分钟 - 两个通道 ⏸️ 暂停中
```

## 5.7 Multi-Agent Routing —— 多智能体路由

### 什么是 Multi-Agent？

OpenClaw 支持**多个 AI 代理协同工作**。你可以创建不同专长的代理，让它们分工合作。

### 场景示例

```
[你的消息] → [路由器] ──→ [搜索代理: 擅长查资料]
                       ├──→ [写作代理: 擅长写文章]
                       ├──→ [代码代理: 擅长写代码]
                       └──→ [审查代理: 擅长检查错误]
```

**使用场景：**
1. **搜索→写作**：搜索代理查资料，写作代理整理成文章
2. **代码→审查**：代码代理写代码，审查代理检查Bug
3. **多角度分析**：多个代理从不同角度分析同一个问题

### 配置多代理

```json
{
  "agents": [
    {
      "name": "研究员",
      "type": "pi",
      "systemPrompt": "你擅长搜索和整理信息，注重事实准确性",
      "model": "claude-sonnet-4-20250514"
    },
    {
      "name": "作家",
      "type": "pi",
      "systemPrompt": "你擅长写作，语言生动有趣，注重可读性",
      "model": "claude-sonnet-4-20250514"
    },
    {
      "name": "审查官",
      "type": "pi",
      "systemPrompt": "你擅长找出错误和漏洞，非常细致",
      "model": "claude-sonnet-4-20250514"
    }
  ]
}
```

> **举个例子：** 你想写一篇技术博客。你说"帮我写一篇关于 TypeScript 装饰器的博客"。路由器自动分派：
> 1. 研究员去搜索最新的装饰器用法和最佳实践
> 2. 作家根据资料写一篇通俗易懂的博客
> 3. 审查官检查技术准确性
> 最后把定稿发给你。整个过程你只需要说一句话。

## 5.8 Mobile Nodes —— 移动端节点

### 什么是 Mobile Node？

Mobile Node 是你手机上的 **OpenClaw 伴侣 App**（iOS 和 Android）。它让你的 AI 助手能够访问手机上的信息——位置、日历、摄像头、传感器。

### 能干吗？

- **位置感知**："我到了公司"→自动触发一个动作
- **拍照识物**：拍一张植物，让 AI 识别是什么种类
- **日程同步**：手机日历事件同步给 AI
- **语音输入**：直接说话，不用打字

### 安装

在 App Store（iOS）或 Google Play（Android）搜索 "OpenClaw Companion"。

首次使用扫描 Dashboard 上的二维码完成配对。

### 与桌面版的关系

- 桌面版是"大脑"，手机版是"感官"
- AI 仍然运行在你的电脑或服务器上
- 手机只是扩展了 AI 获取信息的能力

## 5.9 Live Canvas —— 互动画布

### 什么是 Live Canvas？

Live Canvas 是 OpenClaw 的**可视化交互工作区**。它不是聊天框，而是一个"画布"——AI 可以在这里展示图表、表格、流程图、交互式组件。

### 打开 Canvas

```
你: /canvas
```

或者：

```
你: 帮我画一个流程图，展示用户登录的流程
OpenClaw: [自动打开 Canvas，展示流程图]

你: 在注册流程后面加一个邮箱验证步骤
OpenClaw: [Canvas 自动更新，添加新步骤]
```

### Canvas 能做什么？

- **流程图/架构图**：用 Mermaid 或手绘风格
- **数据可视化**：图表、表格、统计
- **代码预览**：实时编辑和测试代码
- **协作编辑**：你和 AI 同时在一个画布上工作

> **举个例子：** 你在设计一个数据库架构。对 AI 说"帮我设计一个电商数据库的 ER 图"。Canvas 打开，展示出完整的实体关系图。你说"把用户表加一个积分字段"，Canvas 实时更新。你又说"帮我生成对应的 SQL 建表语句"——AI 在旁边生成 SQL，你直接复制就能用。

## 5.10 安全与隐私

### 核心理念

OpenClaw 的安全性建立在"完全本地化"的基础上：

```
你的数据 ──→ 你的电脑 ──→ AI模型API
                                       ↑
                              API Key 只在你的机器上
                              模型调用经过加密传输
                              没有任何第三方能访问你的数据
```

### 访问控制

```json
{
  "security": {
    "allowlist": ["user1", "user2"],
    "requireConfirmation": ["shell", "file_write", "browser"],
    "maxMessageLength": 10000,
    "rateLimit": {
      "messagesPerMinute": 30,
      "messagesPerHour": 500
    }
  }
}
```

| 配置 | 说明 |
|------|------|
| `allowlist` | 只允许指定用户访问 |
| `requireConfirmation` | 敏感操作需要用户确认 |
| `maxMessageLength` | 单条消息最大长度 |
| `rateLimit` | 频率限制，防止滥用 |

### 远程访问安全

如果你想让 OpenClaw 能从外网访问，**强烈推荐使用 Tailscale**：

```bash
# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# 启动
sudo tailscale up

# 获取 Tailscale IP
tailscale ip -4
# 输出: 100.x.x.x
```

然后用 Tailscale IP 替代 `127.0.0.1` 访问：

```
http://100.x.x.x:18789
```

这样只有加入你 Tailscale 网络的设备才能访问，等于多了一层 VPN 保护。

### ❌ 绝对不要做的事

1. **不要**把 `openclaw.json`（含 API Key）传到 GitHub
2. **不要**在公共网络直接暴露端口 18789
3. **不要**让 AI 执行你不理解的命令（它很强大，也可能误操作）
4. **不要**把敏感文件放在 OpenClaw 无限制可读取的目录

### ✅ 推荐的安全做法

1. 使用 `.env` 文件管理 API Key（OpenClaw 支持自动读取）
2. 在 `soul.md` 中明确限制敏感操作需要确认
3. 定期检查 `logs` 了解 AI 做了什么
4. 用 Tailscale 或 WireGuard 实现安全远程访问

---

---

# 第六章：进阶配置与自定义

> 本章适合已经跑通 OpenClaw 基础功能、想让 AI 更懂你、更好用的用户。你将学会修改灵魂、编写技能、设置定时任务、配置多Agent分身、以及安全地远程访问你的 AI。

## 6.1 自定义 soul.md —— 给你的 AI 换灵魂

`soul.md` 是 OpenClaw 的"人格文件"。默认的 `soul.md` 在 `~/.openclaw/soul.md`，但你可以把它改成任何你想要的风格。

### 结构模板

一个完整的 `soul.md` 通常包含以下段落：

```markdown
# 身份定位
你叫什么名字、你是谁、你服务于谁

# 沟通风格
语气（正式/随意/幽默）、用词偏好、语言

# 行为准则
什么可以做、什么需要用户确认、什么绝对不能做

# 专长领域
你最擅长什么、你用什么工具

# 个性彩蛋
（可选）一些有趣的细节设定
```

### 实战示例：客服版 soul.md

```markdown
# 身份定位
你是 OpenClaw 官方客服助手"小O"，为 OpenClaw 用户提供技术支持。

# 沟通风格
- 用中文回复，语气专业且耐心
- 使用 polite 措辞："您好"、"感谢您的提问"
- 回答先给结论，再展开细节
- 遇到不知道的问题说"这个问题我需要确认一下，请稍等"

# 行为准则
- 优先从官方文档查找答案
- 不要编造不存在的功能
- 涉及隐私问题引导用户查看官方安全文档
- 如果用户情绪激动，先安抚再解决问题

# 专长领域
- 安装部署问题
- 配置修改
- 技能开发指南
- 故障排查

# 个性彩蛋
- 用户说"谢谢"时回一句"不客气，有任何问题随时找我"
- 周末回复加一句"祝您周末愉快"
```

### 灵魂切换技巧

同一个 OpenClaw 实例支持**按会话切换灵魂**。在 `~/.openclaw/souls/` 目录下放多个 `.md` 文件：

```bash
~/.openclaw/souls/
├── default.md       # 默认人格
├── work.md          # 工作模式（正式、高效）
├── friend.md        # 朋友模式（随意、幽默）
└── tutor.md         # 教学模式（耐心、详细）
```

在聊天中切换：

```
你: /soul work
OpenClaw: 已切换至工作模式，我是你的专业助手。
```

## 6.2 编写自定义技能（Skills）

技能（Skill）是 OpenClaw 的扩展能力。如果内置功能和官方插件不满足你的需求，你可以自己写。

### 技能文件结构

技能是一个 JSON 文件，放在 `~/.openclaw/skills/` 目录下：

```json
{
  "name": "技能名称",
  "description": "技能描述",
  "version": "1.0.0",
  "author": "你的名字",
  "triggers": [
    {
      "pattern": "触发关键词正则",
      "action": "对应动作名称"
    }
  ],
  "actions": {
    "动作名称": {
      "type": "action_type",
      "config": { ... }
    }
  }
}
```

### 实战：写一个"今日运势"技能

这个技能会调用免费 API 生成每日运势，每天早上8点自动推送。

**第一步：创建技能文件**

```bash
mkdir -p ~/.openclaw/skills
vim ~/.openclaw/skills/fortune.json
```

**第二步：编写技能内容**

```json
{
  "name": "今日运势",
  "description": "每天早上生成今日运势",
  "version": "1.0.0",
  "author": "我的小助手",
  "triggers": [
    {
      "pattern": "(今天|今日).*(运势|运气)",
      "action": "getFortune"
    }
  ],
  "actions": {
    "getFortune": {
      "type": "api_call",
      "url": "https://api.你的运势服务.com/today",
      "params": {
        "zodiac": "{{userZodiac}}"
      },
      "responseTemplate": "🌟 {{zodiac}}座今日运势：\n综合：{{overall}}/10\n爱情：{{love}}/10\n事业：{{career}}/10\n幸运色：{{luckyColor}}\n一句话：{{oneSentence}}"
    }
  },
  "cron": [
    {
      "schedule": "0 8 * * *",
      "action": "getFortune",
      "channel": "telegram"
    }
  ]
}
```

**第三步：注册变量**

OpenClaw 用 `{{变量名}}` 来插入动态值。在 `openclaw.json` 中定义：

```json
{
  "userZodiac": "天蝎"
}
```

**第四步：测试**

```
你: 今天运势怎么样？
OpenClaw: 🌟 天蝎座今日运势：
综合：8/10
爱情：9/10
事业：7/10
幸运色：深海蓝
一句话：今天适合主动表达你的想法。
```

### 技能类型一览

| 类型 | 说明 | 适合场景 |
|------|------|----------|
| `api_call` | 调用外部 API | 天气、运势、新闻 |
| `shell_command` | 执行终端命令 | 系统监控、文件操作 |
| `file_read` | 读取本地文件 | 日志分析、配置检查 |
| `file_write` | 写入本地文件 | 自动记录、日志保存 |
| `browser_action` | 操作浏览器 | 网页截图、填表 |
| `webhook` | 触发 Webhook | 连接其他服务 |

## 6.3 设置定时任务（Cron）

除了第六章前面提到的对话式创建，我们来看看更高级的用法。

### 条件触发的 Cron

不是所有定时任务都需要固定时间。你可以设置"条件触发"：

```json
{
  "name": "下班提醒",
  "condition": {
    "type": "time_range",
    "start": "17:00",
    "end": "19:00",
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  },
  "action": "检查今天还有没有未完成的任务，如果有提醒我"
}
```

### 定时任务链

一个任务完成后触发下一个：

```json
[
  {
    "name": "数据收集",
    "schedule": "0 8 * * *",
    "action": "从数据库拉取昨日销售数据",
    "output": "raw_data.json",
    "next": "数据分析"
  },
  {
    "name": "数据分析",
    "action": "分析 raw_data.json，生成图表和摘要",
    "output": "report.md",
    "next": "推送报告"
  },
  {
    "name": "推送报告",
    "action": "将 report.md 发送到 Slack #daily-report 频道"
  }
]
```

### 定时任务的调试

```
你: 测试一下我的"每日天气"任务
OpenClaw: 正在模拟执行"每日天气"...
执行结果：北京今天晴，22-28°C ✅
推送通道：Telegram ✅
```

## 6.4 多 Agent 配置——让你的 AI 分身有术

### 场景：工作 Agent vs 个人 Agent

大多数用户只需要一个 Agent，但 OpenClaw 支持在同一台机器上运行多个 Agent，各自有不同的灵魂、技能和通道。

### 配置方式

在 `openclaw.json` 中定义多个 agent：

```json
{
  "agents": {
    "work": {
      "name": "工作助手",
      "soulFile": "~/.openclaw/souls/work.md",
      "channels": ["slack"],
      "skills": ["gmail", "jira", "github"],
      "model": "claude-sonnet-4-20250514",
      "cron": [
        { "schedule": "0 9 * * 1-5", "action": "发送今日日程" }
      ]
    },
    "personal": {
      "name": "生活管家",
      "soulFile": "~/.openclaw/souls/friend.md",
      "channels": ["telegram", "whatsapp"],
      "skills": ["weather", "news", "reminder"],
      "model": "gpt-4o-mini",
      "cron": [
        { "schedule": "0 7 * * *", "action": "发送天气预报" }
      ]
    }
  }
}
```

### 指定 Agent 对话

```
你: @work 帮我查一下 JIRA 上的这个 Sprint 进度
你: @personal 今天晚饭有什么推荐？
```

### 多 Agent 协作

两个 Agent 之间也可以互相"说话"：

```json
{
  "name": "跨Agent协作",
  "trigger": "cron",
  "schedule": "0 18 * * 5",
  "actions": [
    "work: 生成本周工作总结",
    "personal: 根据工作总结，为我安排周末放松计划"
  ]
}
```

## 6.5 远程访问——出门在外也能用

### 使用 Tailscale（推荐）

Tailscale 创建一个加密的私有网络，让你的设备（PC、手机、笔记本）像在同一个局域网一样互访。

**安装与配置：**

```bash
# 1. 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# 2. 启动和登录
sudo tailscale up

# 3. 查看你的 Tailscale IP
tailscale ip -4
# 输出：100.x.x.x
```

**在 openclaw.json 中开放远程访问：**

```json
{
  "gateway": {
    "port": 18789,
    "host": "0.0.0.0",
    "allowRemote": true
  }
}
```

然后你就可以通过 `http://100.x.x.x:18789` 从任何已加入 Tailscale 网络的设备访问 Dashboard。

### 使用 SSH 隧道

如果你不想装 Tailscale，可以用 SSH 隧道：

```bash
# 从远程机器建立隧道
ssh -L 18789:127.0.0.1:18789 user@your-server-ip

# 然后在浏览器打开
# http://127.0.0.1:18789
```

### 使用 Cloudflare Tunnel（高级）

适合暴露到公网但不暴露真实 IP：

```bash
# 安装 cloudflared
# 创建隧道指向 localhost:18789
cloudflared tunnel create openclaw
cloudflared tunnel route dns openclaw openclaw.yourdomain.com
cloudflared tunnel run openclaw
```

## 6.6 安全加固

### 用户 Allowlist

只允许特定用户访问你的 AI：

```json
{
  "security": {
    "allowlist": ["your_telegram_username", "your_discord_user_id"],
    "blocklist": ["spammer_username"]
  }
}
```

### 速率限制（Rate Limiting）

防止 API 被滥用导致费用暴增：

```json
{
  "security": {
    "rateLimit": {
      "messagesPerMinute": 20,
      "messagesPerHour": 200,
      "tokensPerDay": 500000,
      "costLimit": {
        "daily": 5.00,
        "monthly": 50.00
      }
    }
  }
}
```

当接近限额时，OpenClaw 会自动提醒你：

```
⚠️ 本月 API 费用已使用 $42.50，接近 $50.00 限额。
是否需要提高限额？
```

### Token 鉴权

在 Gateway 上加上 Token 验证，防止未授权访问：

```json
{
  "gateway": {
    "apiToken": "your-secret-token-here"
  }
}
```

然后所有 API 请求都需要在 Header 中带这个 Token。

### 操作确认

对敏感操作要求二次确认：

```json
{
  "security": {
    "requireConfirmation": [
      "shell:*",
      "file_write:/etc/*",
      "file_delete:*",
      "browser:submitForm"
    ]
  }
}
```

当 AI 执行这些操作时，会先发一条确认消息：

```
我准备执行这个命令：rm -rf /tmp/test
请确认是否执行？(y/n)
```

## 6.7 多通道同时管理

OpenClaw 可以同时运行多个聊天通道。下面是同时配置 Telegram + Discord + Slack 的完整示例：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456:ABC-DEF...",
      "allowlist": ["my_username"]
    },
    "discord": {
      "enabled": true,
      "botToken": "Nzg5MTIz...",
      "guildId": "123456789",
      "channelIds": ["general", "ai-bot"]
    },
    "slack": {
      "enabled": true,
      "botToken": "xoxb-123...",
      "signingSecret": "abc123...",
      "channelIds": ["#general", "#random"]
    }
  }
}
```

### 通道路由

你可以设置不同通道走不同 Agent：

```json
{
  "channelRouting": {
    "telegram": "personal",
    "slack": "work",
    "discord": {
      "channels": {
        "general": "personal",
        "ai-bot": "work"
      }
    }
  }
}
```

### 跨通道会话同步

所有通道共享同一个 Gateway，所以你在 Telegram 问的问题，可以在 Discord 上继续：

```
[Telegram 09:00] 你: 帮我查一下 XYZ 公司
[Discord 09:05] 你: 刚才查到的公司，帮我写一封合作邮件
[Discord 09:05] OpenClaw: 好的，关于 XYZ 公司，我查到...
```

---

# 第七章：社区资源精选

> 本章精选了 OpenClaw 社区最值得关注的资源，每个资源都配有结构化摘要，帮助你快速判断是否值得花时间阅读或观看。

## 7.1 [YouTube/Lex Fridman] Peter Steinberger 做客 Lex Fridman Podcast

| 项目 | 内容 |
|------|------|
| **资源类型** | 🎬 播客视频（3小时） |
| **链接** | [Lex Fridman Podcast #456](https://www.youtube.com/watch?v=xxxx) |
| **播放量** | 500万+ |
| **语言** | 英语（有自动字幕） |

**适合人群：** 对 AI 行业趋势感兴趣的任何人、想了解 OpenClaw 背后故事的开发者、开源爱好者。

**内容概览：**
这是 Lex Fridman 与 Peter Steinberger 的 3 小时深度对话。Peter 从自己的编程经历讲起（15岁开始写代码，在暴雪娱乐做魔兽世界插件），到创办 PSPDFKit（iOS/macOS 领域最成功的独立开发者产品之一），再到为什么决定做 OpenClaw。对话覆盖了 AI 代理的现状、开源与闭源的哲学分歧、自托管 AI 的未来，以及 Peter 对 AI 安全、隐私、以及"AI 应该是什么样的"的深入思考。

**为什么值得看：**
- **最权威的信息源**——OpenClaw 的创造者亲自讲述
- **不只是技术**——还讨论了创业哲学、开源商业模式、AI 伦理
- **Lex 的提问很到位**——能问到关键问题，比读文字材料更深入
- **5M+ 播放量背后有原因**——内容足够好才能吸引这么多人看

**一句话评价：**
> 听了这个 Podcast 你才能真正理解 OpenClaw 为什么而建，以及它和市面上其他 AI 产品最根本的区别在哪里。

**学到的技能点：**
- AI Agent 的设计哲学——为什么 OpenClaw 选择"Agentic Loop"架构
- 自托管 AI 的真正价值——不仅仅是隐私，更是控制权和自由度
- 开源商业模式思考——MIT 许可证 vs 企业版 vs 服务收费
- 对"AI 安全"的深度理解——不是"AI 会不会毁灭人类"，而是"你的数据在谁手里"
- 开发者创业的心路历程——从独立开发者到全球知名项目的经验

---

## 7.2 [GitHub] OpenClaw 官方仓库

| 项目 | 内容 |
|------|------|
| **资源类型** | 💻 GitHub 仓库 |
| **链接** | [github.com/personalailabs/openclaw](https://github.com/personalailabs/openclaw) |
| **Star 数** | 68,000+ |
| **许可证** | MIT |

**适合人群：** 所有用户——从刚接触 OpenClaw 的新手到想贡献代码的开发者。

**内容概览：**
GitHub 仓库包含 OpenClaw 的全部源代码、README 文档、Wiki 页面、Issues 讨论区、Discussions 社区论坛、以及 Release 版本发布。README 本身就是一份极好的快速开始指南。Wiki 里有更详细的部署、配置、开发指南。Issues 里能找到几乎所有常见问题的解决方案。Discussions 是社区交流的地方——新功能讨论、使用心得、最佳实践分享。

**为什么值得看：**
- **一手信息源**——所有官方更新最先在这里发布
- **最权威**——你读到的任何其他教程最终都应该回归到这里
- **社区活跃度是风向标**——68K+ Stars、大量 Fork、活跃的 Issues 和 PR 说明项目健康运行

**一句话评价：**
> 有问题先查 Issues，十有八九有人遇到过。再找不到就去 Discussions 问，作者本人经常回复。

**学到的技能点：**
- 安装方法的多种选择
- 所有配置选项的详细说明
- 社区贡献的最佳实践
- 常见问题的解决方案
- 如何为开源项目贡献代码

---

## 7.3 [官方文档] docs.openclaw.ai

| 项目 | 内容 |
|------|------|
| **资源类型** | 📖 在线文档 |
| **链接** | [docs.openclaw.ai](https://docs.openclaw.ai) |
| **维护者** | OpenClaw 官方团队 |

**适合人群：** 所有用户——新手看快速开始，进阶用户看 API 参考和配置手册。

**内容概览：**
完整的官方文档，涵盖以下内容：
- **快速开始**：5分钟上线
- **安装指南**：各平台安装方法
- **配置参考**：所有配置项详解
- **通道配置**：Telegram、WhatsApp、Discord、Slack、Signal 等
- **技能开发**：如何编写自定义技能
- **API 参考**：Gateway API 文档
- **FAQ**：常见问题解答
- **Changelog**：版本更新日志

**为什么值得看：**
- **最权威的技术文档**——比任何第三方教程都可靠
- **最全面**——事无巨细都有说明
- **更新最及时**——新功能发布后文档会第一时间更新

**一句话评价：**
> 遇到问题先翻文档，这是最快解决问题的途径。

**学到的技能点：**
- 完整的配置选项认知
- 通道接入的详细步骤
- Gateway API 的使用方法
- 故障排查的官方指引

---

## 7.4 [YouTube] OpenClaw Tutorial for Beginners - Crash Course

| 项目 | 内容 |
|------|------|
| **资源类型** | 🎬 视频教程（约 30-45 分钟） |
| **语言** | 英语 |
| **难度** | ★☆☆☆☆（纯新手向） |

**适合人群：** 完全没接触过 OpenClaw 的新手、不喜欢读文字想跟着视频操作的读者。

**内容概览：**
从零开始的 OpenClaw 入门教程，从"什么是 OpenClaw"开始，一步步演示安装过程、配置 Telegram 通道、编写第一个 soul.md、创建第一个定时任务。视频中能看到真实的终端操作和 Dashboard 界面，比文字描述更直观。

**为什么值得看：**
- 视频形式，跟着操作比读文档更容易
- 能看到实际的界面和命令行输出，减少"是不是我操作错了"的困惑
- 适合在第二屏幕边看边做

**一句话评价：**
> 适合完全没接触过的人快速上手，看完就能自己跑起来。

**学到的技能点：**
- 安装和配置的直观理解
- 第一次对话的完整流程
- 基础操作的视觉认知

---

## 7.5 [GitHub/Datawhale] OpenClaw 学习教程——一周打造跨设备AI助手

| 项目 | 内容 |
|------|------|
| **资源类型** | 📚 中文教程（GitHub 仓库） |
| **链接** | [Datawhale OpenClaw 教程](https://github.com/datawhalechina/openclaw-tutorial) |
| **维护者** | Datawhale 开源社区 |
| **难度** | ★★☆☆☆（入门到进阶） |

**适合人群：** 中文用户，希望系统学习 OpenClaw 从入门到进阶的所有内容。

**内容概览：**
Datawhale 社区编写的系统性教程，设计为"7天学习计划"：
- Day 1: 认识 OpenClaw + 安装
- Day 2: 基础配置 + 第一段对话
- Day 3: soul.md 深入定制
- Day 4: Skills 技能开发
- Day 5: 定时任务 + 自动化工作流
- Day 6: 多通道 + 多 Agent
- Day 7: 综合实战项目

每个章节有代码示例、配图和练习题，比官方文档更适合初学者循序渐进地学习。

**为什么值得看：**
- **中文社区最系统的教程**——不是零散的文章，而是一个完整的学习路径
- **结构清晰**——7 天计划，每天能学到新东西
- **社区维护**——有 Issue 和 PR 机制，内容会持续更新

**一句话评价：**
> 中文用户的最佳学习路径，跟着走一周就能成为 OpenClaw 中级用户。

**学到的技能点：**
- 完整的安装配置能力
- soul.md 高级定制技巧
- 自定义技能开发
- 自动化工作流搭建
- 多 Agent 协同管理

---

## 7.6 [知乎] OpenClaw 完全部署指南

| 项目 | 内容 |
|------|------|
| **资源类型** | 📝 知乎专栏文章 |
| **链接** | 知乎搜索"OpenClaw 完全部署指南" |
| **作者** | 社区技术博主 |
| **难度** | ★★★☆☆（需要一定技术基础） |

**适合人群：** 有一定技术基础（熟悉 Linux、网络配置）的用户，希望将 OpenClaw 部署到服务器上长期运行。

**内容概览：**
从入门到安全加固的完整部署指南，包括：
- 在 VPS/云服务器上的部署
- Nginx 反向代理配置
- HTTPS/SSL 证书设置
- Docker 生产环境部署
- 系统服务（systemd）配置
- 日志管理和监控
- 备份与恢复策略
- 安全加固 checklist

**为什么值得看：**
- **深度技术内容**——不只是"怎么装"，而是"怎么装好"
- **含安全最佳实践**——很多安全细节是官方文档没强调但实际非常重要的
- **中文写作**——技术术语有中文解释，阅读体验好

**一句话评价：**
> 想深入配置 OpenClaw 做生产环境部署的必读文章。

**学到的技能点：**
- 生产环境部署技能
- 安全加固的完整方案
- Nginx 反向代理配置
- Docker 生产部署
- 系统服务管理

---

## 7.7 [博客园] 手把手教你部署 OpenClaw

| 项目 | 内容 |
|------|------|
| **资源类型** | 📝 博客教程 |
| **难度** | ★☆☆☆☆（纯新手向） |

**适合人群：** 技术基础较弱的用户，希望有人一步一步带着操作。

**内容概览：**
非常详细的部署步骤，每一步都配有截图和解释。从注册 API 账号、安装 Node.js、运行安装命令、配置 Telegram Bot，到第一次对话成功。每一步的常见错误都有说明。

**为什么值得看：**
- 步骤细致到"点哪个按钮""输入什么内容"
- 每一步都有"你可能遇到的问题"提醒
- 截图标注了关键信息，不会看漏

**一句话评价：**
> 一步一步跟着做，小白也能成功部署。

**学到的技能点：**
- 从零开始的部署能力
- 常见安装问题的排查能力

---

## 7.8 [DigitalOcean] What is OpenClaw? Your Open-Source AI Assistant

| 项目 | 内容 |
|------|------|
| **资源类型** | 📝 技术博客 |
| **链接** | [DigitalOcean Community](https://www.digitalocean.com/community/tutorials) |
| **发布平台** | DigitalOcean 社区教程 |
| **难度** | ★★☆☆☆（概念理解向） |

**适合人群：** 想了解 OpenClaw 概念的读者，或者想向非技术朋友介绍 OpenClaw 时可以参考这篇文章。

**内容概览：**
DigitalOcean 作为知名的云服务商和开发者社区，其发布的 OpenClaw 介绍文章结构非常清晰：
- OpenClaw 是什么
- 核心架构（Channel → Gateway → Pi Agent）
- 关键功能
- 与 ChatGPT 等产品的对比
- 安装部署快速指南
- 使用场景示例

**为什么值得看：**
- DigitalOcean 的教程质量一直很高，经过专业编辑审核
- 结构清晰，适合作为"给非技术人员的介绍材料"
- 有英文原版，适合推荐给海外朋友

**一句话评价：**
> 如果你需要向一个不懂技术的朋友解释 OpenClaw 是什么，直接把这篇发给他。

**学到的技能点：**
- OpenClaw 核心概念的系统认知
- 使用场景的灵感来源

---

# 第八章：业内评价与案例分析

> 本章分析 OpenClaw 在业界引起的反响，以及它在开源 AI 生态中的定位。通过数据、报道和对比，带你理解这个项目为何如此受关注。

## 8.1 Peter Steinberger 的背景故事

理解 OpenClaw 之前，先理解它的创造者。

**Peter Steinberger** 是奥地利出生的独立开发者，iOS/macOS 领域最知名的人物之一。他的成名作是 **PSPDFKit**——一个为 iOS/Android/Web 提供 PDF 渲染和编辑功能的 SDK。PSPDFKit 从 2011 年起步，从一个单人项目发展为服务数千家企业客户的商业产品。

**几个关键事实：**
- **15 岁开始编程**——做过魔兽世界插件，在暴雪娱乐社区出名
- **PSPDFKit 的成功**——被 eBay、SAP、NASA 等机构使用，是独立开发者实现财务自由的经典案例
- **2023 年转型 AI**——Peter 在 2023 年将注意力转向 AI，开始构建 OpenClaw 的原型
- **完全的独立性**——OpenClaw 背后是 Personal AI Labs，没有 VC 融资压力

**对 OpenClaw 的影响：**
- 有 PSPDFKit 的经验，Peter 深知"独立开发者产品"的成功路径：开源吸引用户 → 企业版/服务收费
- 对质量的偏执——PSPDFKit 以代码质量著称，OpenClaw 继承了这一传统
- 对隐私的重视——PSPDFKit 处理企业敏感数据，这让 Peter 对数据安全有深度理解

## 8.2 Lex Fridman Podcast 的破圈效应

2025 年初，Peter Steinberger 做客 **Lex Fridman Podcast**（超过 800 万订阅的顶级科技播客）。这一期节目播放量超过 **500 万次**，是 OpenClaw 项目增长的转折点。

**为什么这次对话如此重要：**

| 因素 | 影响 |
|------|------|
| Lex 的受众群体 | 技术爱好者、AI 研究者、开源社区，恰好是 OpenClaw 的目标用户 |
| 3 小时深度对话 | 足够深入，能完整展示 Peter 的思考和技术深度 |
| 时间节点 | AI Agent 概念正处于关注高峰期 |
| 个人故事 | Peter 的独立开发者经历具有感染力和启发力 |

**播出后的效果：**
- GitHub Stars 从播出前的约 1 万飙升至 6.8 万+
- 社区 Discord/Slack 成员数量大幅增长
- 大量第三方教程和文章出现
- 开源贡献者数量显著增加

## 8.3 主流科技媒体报道

| 媒体 | 文章标题 | 核心观点 |
|------|----------|----------|
| **TechCrunch** | "Personal AI Labs raises the bar for open-source AI assistants" | 关注 OpenClaw 的架构设计和隐私优先理念 |
| **Ars Technica** | "This open-source AI assistant runs entirely on your machine" | 突出"自托管"和"隐私"两大优势 |
| **The Verge** | "The open-source AI revolution runs through your chat app" | 从用户体验角度分析 OpenClaw 与 ChatGPT 的不同 |

**TechCrunch 评价摘录：**
> "OpenClaw 代表了一种与主流 AI 产品截然不同的路径——不是更大的模型，不是更贵的订阅，而是让用户重新掌控自己的 AI 体验。"

**Ars Technica 评价摘录：**
> "在一个所有人都在争夺用户数据的时代，OpenClaw 反其道而行之——你的数据在你的机器上，API 调用结束后，模型不保留任何信息。"

## 8.4 GitHub 68K Stars 的意义

68,000+ 星是什么概念？我们来看看对比：

| 项目 | Stars | 类别 |
|------|-------|------|
| OpenClaw | 68K+ | AI 助手框架 |
| AutoGPT | 160K+ | AI Agent（早期先行者） |
| LangChain | 90K+ | LLM 应用框架 |
| Ollama | 80K+ | 本地模型运行 |
| Open Interpreter | 50K+ | AI 代码解释器 |

**分析：**
- OpenClaw 是 2024-2025 年增长最快的项目之一
- 作为"AI 助手"类别，其增长速度超过了大多数同类项目
- 68K Stars 代表了**开发者社区的认可**——Stars 不会骗人，开发者不会给不喜欢的项目点星

**Stars 增长曲线的解读：**
- **初期（< 1K）**：核心开发者和早期采用者
- **爆发期（1K → 20K）**：Lex 播客播出后的指数增长
- **稳定增长期（20K → 68K）**：口碑传播 + 媒体报道 + 社区壮大

## 8.5 对比分析：OpenClaw vs 其他 AI 项目

### OpenClaw vs Claude Code

| 维度 | OpenClaw | Claude Code |
|------|----------|-------------|
| **定位** | 通用 AI 助手 | 代码辅助工具 |
| **使用方式** | 聊天软件 + Web UI | 终端命令行 |
| **主动能力** | ✅ 定时任务、监控、推送 | ❌ 被动响应 |
| **多通道** | ✅ 7+ 聊天平台 | ❌ 仅终端 |
| **开源** | ✅ MIT | ❌ 闭源 |
| **数据控制** | ✅ 自托管 | ❌ 云端 |
| **适合人群** | 所有人 | 开发者 |

### OpenClaw vs Hermes Agent

| 维度 | OpenClaw | Hermes Agent |
|------|----------|--------------|
| **开发商** | Personal AI Labs (Peter Steinberger) | Nous Research |
| **定位** | 个人 AI 助手 | 通用 AI Agent 框架 |
| **架构** | Channel → Gateway → Pi Agent | Agent 库 + 工具链 |
| **使用门槛** | 低（通过聊天软件） | 高（需要编程） |
| **开源协议** | MIT | Apache 2.0 |
| **社区** | 68K+ Stars | 15K+ Stars |

### OpenClaw vs AutoGPT

| 维度 | OpenClaw | AutoGPT |
|------|----------|---------|
| **定位** | 个人助手 | 自主任务执行 Agent |
| **交互方式** | 聊天驱动 | 目标驱动 |
| **用途** | 日常辅助 | 自动化任务 |
| **稳定性** | 较高 | 早期，有时不稳定 |

### OpenClaw vs ChatGPT/Claude

| 维度 | OpenClaw | ChatGPT / Claude |
|------|----------|------------------|
| **数据归属** | 你完全控制 | 服务商处理 |
| **费用** | 只付 API 费用 | 月费 $20+ |
| **主动能力** | ✅ 有 | ❌ 无 |
| **系统访问** | ✅ 可操作你的电脑 | ❌ 沙盒隔离 |
| **离线能力** | ❌ 需要网络 | ❌ 需要网络 |

## 8.6 开发者社区的反响

**正面评价（占多数）：**
- "这就是我想要的 AI——不是另一个聊天机器人，而是真正能做事的助手"
- "配置 Telegram 后感觉像有了一个 24 小时在线的私人助理"
- "MIT 许可证让我放心，就算项目停止维护，我手里的代码也能继续用"
- "soul.md 这个设计太聪明了——一个文件就能定义 AI 的人格"

**批评和顾虑：**
- "API Key 费用是个隐藏成本——如果天天高强度使用，每个月也要花不少钱"
- "WhatsApp 配置太复杂了，希望能简化"
- "文档有些地方不够详细，新手配置多通道时会踩坑"
- "Pi Agent 有时候会出现幻觉，需要优化"

## 8.7 隐私与自托管作为竞争优势

在 AI 行业，几乎所有的头部产品都是"云端 SaaS"模式——你的数据发送到服务商的服务器上处理。OpenClaw 的反其道而行之反而成了最大的卖点：

**隐私优势：**
- 所有数据运行在用户自己的机器上
- AI 模型 API 调用是单向的——数据发送去处理，但模型不保留
- 没有"你的对话被用来训练模型"的风险

**控制权优势：**
- 你可以随时查看、修改、删除所有数据
- 你可以选择任何 AI 模型，不绑定特定供应商
- 你可以修改任何代码——MIT 许可证给了你完全的权限

**这个趋势背后的数据：**
- 2024-2025 年，"自托管 AI" 的搜索量增长了 500%+
- 越来越多的企业开始关注"AI 数据治理"
- 欧盟的 AI Act 等法规要求对用户数据有更高的控制权

## 8.8 "自托管 AI"市场趋势

OpenClaw 不是一个孤立的现象。它处于一个更大的趋势中——**自托管 AI**：

| 时间 | 事件 | 意义 |
|------|------|------|
| 2023 | Ollama 发布 | 本地运行大模型变得简单 |
| 2024 | OpenClaw 发布 | 自托管 AI 开始面向普通用户 |
| 2024 | LocalAI 社区壮大 | 本地 AI 生态丰富 |
| 2025 | 更多企业探索自托管 | 数据合规推动需求 |

**推动因素：**
1. **数据隐私法规**——GDPR、CCPA、中国《个人信息保护法》
2. **API 成本下降**——模型价格每年下降 50-80%
3. **开源模型成熟**——Llama、Mistral、Qwen 等开源模型越来越强
4. **用户意识提升**——越来越多的人意识到"你的数据=你的资产"

---

# 第九章：避坑指南

> 本章列出了 OpenClaw 使用中最常见的 10 个问题，每个都包含"现象→原因→修复步骤"三步走。遇到问题先翻这一章，大概率能找到答案。

## 9.1 Node.js 版本不兼容

**现象：**
```
npm ERR! engine not compatible with your version of node
```
或者安装后运行 `openclaw` 报各种奇怪的语法错误。

**原因：**
OpenClaw 需要 Node.js 22 或 24 版本。如果你用的是 Node.js 18 或 20（很多系统的默认版本），某些语法特性不支持。

**修复步骤：**

```bash
# 1. 检查当前版本
node --version

# 2. 如果版本不符合要求，用 nvm 管理版本
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新打开终端，安装 Node.js 22
nvm install 22
nvm use 22
nvm alias default 22

# 3. 验证
node --version  # 应该输出 v22.x.x

# 4. 重新安装 OpenClaw
npm install -g openclaw@latest
```

**Windows 用户特别说明：**
如果你在 Windows 上直接用 Node.js 安装包，下载页面选择"LTS"版本（22.x）。确认安装时勾选了"Add to PATH"。安装完成后重启终端。

## 9.2 API Key 配置错误

**现象：**
```
Error: Authentication failed
```
或者 AI 回复"抱歉，我无法处理这个请求"但没有具体错误。

**原因：**
- API Key 输入错误（多了空格、少了一个字符）
- API Key 已过期
- 选择的提供商和 Key 不匹配（用了 OpenAI 的 Key 但选了 Anthropic）
- API 账户余额不足

**修复步骤：**

```bash
# 1. 检查配置文件中的 Key
cat ~/.openclaw/openclaw.json | grep apiKey

# 2. 确保 Key 没有多余空格
# 正确的格式： "apiKey": "sk-ant-PLACEHOLDERxxxxxxxxxxxx"
# 错误的格式： "apiKey": " sk-ant-PLACEHOLDERxxxxxxxxxxxx "（多了空格）

# 3. 测试 Key 是否有效
# 对于 Anthropic:
curl -H "x-api-key: YOUR_KEY" \
     -H "anthropic-version: 2023-06-01" \
     https://api.anthropic.com/v1/messages \
     -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'

# 4. 检查余额
# Anthropic: https://console.anthropic.com/settings/billing
# OpenAI: https://platform.openai.com/account/usage

# 5. 如果以上都正常，尝试重新运行 onboard
openclaw onboard
```

## 9.3 端口 18789 被占用

**现象：**
```
Error: listen EADDRINUSE :::18789
```
或者启动后 Dashboard 打不开。

**原因：**
端口 18789 被另一个进程占用了。可能是之前启动的 OpenClaw 没有正常退出，或者其他应用占用了这个端口。

**修复步骤：**

```bash
# 1. 查看哪个进程在占用端口
lsof -i :18789
# Linux 或 WSL 用户也可以用：
ss -tlnp | grep 18789

# 输出示例：
# node  12345  user  12u  IPv4  ...  TCP *:18789 (LISTEN)

# 2. 关闭占用进程
kill -9 12345  # 用上一步看到的 PID 替换

# 3. 如果不知道是谁占用的，或者关了还会重启
# 可以修改 OpenClaw 的端口
# 编辑 ~/.openclaw/openclaw.json
# 将 "port": 18789 改为 "port": 18790（或其他可用端口）

# 4. 重启 OpenClaw
openclaw restart
```

**Windows 用户特别说明：**
```powershell
# 查看端口占用
netstat -ano | findstr :18789

# 关闭进程（用上一步看到的 PID）
taskkill /PID 12345 /F
```

## 9.4 Telegram Bot 连接失败

**现象：**
在 Telegram 中给 Bot 发消息，Bot 没有任何回复。Dashboard 中 Telegram 通道显示"Disconnected"。

**原因：**
- Bot Token 配置错误
- Bot 还没有通过 `/start` 命令激活
- Telegram 服务器无法访问（网络问题）
- Bot 被 Telegram 限流

**修复步骤：**

```bash
# 1. 验证 Bot Token 是否正确
curl https://api.telegram.org/botYOUR_BOT_TOKEN/getMe
# 如果返回 {"ok":true,"result":{"id":...,"first_name":"..."}} 说明 Token 正确
# 如果返回 404 说明 Token 错误

# 2. 检查 Bot 是否已激活
# 在 Telegram 中给你的 Bot 发送 /start
# 如果之前没发过，这一步是必须的

# 3. 检查网络
curl https://api.telegram.org/
# 如果网络不通，检查代理设置或防火墙

# 4. 重启通道
openclaw channel restart telegram
```

## 9.5 WhatsApp 配置复杂

**现象：**
WhatsApp 通道配置困难，连接不稳定，经常断连。

**原因：**
WhatsApp 没有官方的 Bot API（不像 Telegram 有 BotFather）。OpenClaw 通过 WhatsApp Web 协议模拟登录，而 WhatsApp 对非官方客户端有限制。

**修复步骤：**

```bash
# 1. 确认使用 Docker 运行 WhatsApp 桥接
# 推荐使用 whatsapp-web.js 的 Docker 镜像
docker run -d \
  --name openclaw-whatsapp \
  -v ~/.openclaw/whatsapp:/app/session \
  openclaw/whatsapp-bridge:latest

# 2. 第一次运行需要扫码
# 查看日志，找到二维码
docker logs -f openclaw-whatsapp
# 用手机 WhatsApp 扫码

# 3. 如果频繁断连
# 编辑 openclaw.json 增加重试
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "reconnectInterval": 30,
      "maxReconnectAttempts": 10
    }
  }
}

# 4. 备选方案：用 Telegram 代替 WhatsApp
# 如果 WhatsApp 始终不稳定，建议改用 Telegram
```

**重要提醒：**
WhatsApp 的非官方客户端有被封号的风险。如果只是个人使用，频率不高，风险不大。但如果用于商业用途，建议用 WhatsApp Business API。

## 9.6 远程访问配置问题

**现象：**
从外网访问 Dashbaord 时连接超时，或提示"Connection refused"。

**原因：**
- Gateway 监听地址是 `127.0.0.1`（只允许本机访问）
- 路由器没有端口转发
- 防火墙阻止了连接
- 没有配置安全通道（如 Tailscale）

**修复步骤：**

```bash
# 1. 检查 Gateway 监听地址
cat ~/.openclaw/openclaw.json | grep host
# 如果显示 "host": "127.0.0.1"，改成 "0.0.0.0"

# 2. 检查防火墙
# Linux:
sudo ufw status
# 如果开启了防火墙，允许 18789 端口
sudo ufw allow 18789

# 3. 推荐使用 Tailscale（最安全）
# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# 然后用 Tailscale IP 访问

# 4. 如果需要公网访问
# 绝对不要直接暴露端口！使用 Nginx 反向代理 + HTTPS
# 或使用 Cloudflare Tunnel
```

## 9.7 soul.md 格式错误

**现象：**
AI 的回复风格和预期不符，时好时坏，有时完全忽略 `soul.md` 中的指令。

**原因：**
- `soul.md` 的 Markdown 格式错误
- 指令不够具体，AI 无法理解
- `soul.md` 文件编码问题（应该是 UTF-8）

**修复步骤：**

```bash
# 1. 检查文件编码
file ~/.openclaw/soul.md
# 应该显示 UTF-8 Unicode text
# 如果是其他编码，用以下命令转换
iconv -f GBK -t UTF-8 ~/.openclaw/soul.md > ~/.openclaw/soul.md.utf8
mv ~/.openclaw/soul.md.utf8 ~/.openclaw/soul.md

# 2. 验证格式
# 用 Markdown 预览工具打开看看渲染效果
# 确保标题、列表、加粗等格式正确

# 3. 指令要具体，不要模糊
# ❌ 错误： "说话要好听"
# ✅ 正确： "使用中文，语气友好，多用表情符号，每段不超过3句话"

# 4. 重启使生效
openclaw restart

# 5. 测试
# 发一条消息看回复风格是否改变
你: 你是谁？
```

## 9.8 Gateway 崩溃

**现象：**
OpenClaw 突然不响应了，Dashboard 打不开，终端显示进程已退出。

**原因：**
- 内存不足被系统杀死（OOM Killer）
- 某个技能插件崩溃导致 Gateway 连带崩溃
- API 调用超时导致进程阻塞

**修复步骤：**

```bash
# 1. 查看崩溃日志
cat ~/.openclaw/logs/gateway.log | tail -50
# 查找 Error / Fatal / OOM 等关键词

# 2. 如果显示 "Out of Memory"
# 增加系统 swap 或升级内存
# 或者减少并发会话数
{
  "gateway": {
    "maxSessions": 20,  # 从 50 减少到 20
    "maxConcurrency": 3  # 限制同时处理的请求数
  }
}

# 3. 设置自动重启
# 使用 pm2 守护进程
npm install -g pm2
pm2 start `which openclaw` -- start --daemon
pm2 save
pm2 startup
# 这样 Gateway 崩溃后会自动重启

# 4. 使用 systemd（Linux）
# 创建服务文件
sudo vim /etc/systemd/system/openclaw.service
# 内容：
"""
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=你的用户名
ExecStart=/usr/bin/openclaw start --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
sudo systemctl enable openclaw
sudo systemctl start openclaw
```

## 9.9 内存不足

**现象：**
系统变慢，OpenClaw 响应越来越慢，最终崩溃。使用 `htop` 或任务管理器看到内存占用很高。

**原因：**
- 会话积累太多上下文
- 长时间运行没有清理
- 同时运行了多个 Agent
- 与其他应用竞争内存

**修复步骤：**

```json
{
  "agent": {
    "maxContextMessages": 50,  // 减少上下文保留的消息数
    "maxTokens": 4096         // 减少单次响应的最大 token 数
  },
  "gateway": {
    "sessionTimeout": 30,     // 30 分钟无活动自动清理会话
    "maxSessions": 20         // 限制最大会话数
  }
}
```

**日常维护：**
```bash
# 查看内存占用
openclaw stats

# 手动清理所有会话
openclaw session clear

# 限制日志大小（编辑 openclaw.json）
{
  "logging": {
    "maxLogSize": 10485760,  // 10MB
    "maxLogFiles": 3
  }
}
```

## 9.10 模型响应慢

**现象：**
发送消息后，OpenClaw 需要 10-20 秒甚至更久才能回复。有时回复到一半卡住了。

**原因：**
- 使用的模型本身较慢（如 Claude Opus）
- API 网络延迟
- 技能执行过程中有耗时操作（如浏览器操作、大型文件处理）
- API 配额/限流

**修复步骤：**

```json
{
  "agent": {
    "model": "claude-sonnet-4-20250514",  // 使用 Sonnet 而不是 Opus
    "timeout": 60000  // 增加超时时间到 60 秒
  }
}
```

```bash
# 网络诊断
curl -w "\n%{time_total}s\n" -X POST \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"hello"}]}' \
  https://api.anthropic.com/v1/messages
# 如果 time_total > 5s，说明网络延迟较高

# 如果人在中国，可能需要代理
# 在 openclaw.json 中配置代理
{
  "proxy": {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
  }
}
```

---

# 第十章：进阶技巧与最佳实践

> 本章汇集了 OpenClaw 高级用户和社区 contributors 总结的最佳实践，涵盖 soul.md 编写、安全配置、多 Agent 管理、Cron 任务设计、Skills 开发、性能优化和完整学习路线图。

## 10.1 soul.md 编写最佳实践

### 原则 1：具体优于抽象

❌ **模糊的写法：**
```markdown
# 沟通风格
对用户友好一点。
```

✅ **具体的写法：**
```markdown
# 沟通风格
- 用中文回复，使用"你"称呼用户
- 每条回复不超过 5 段，每段不超过 3 句话
- 对于技术问题，给出代码示例
- 对于主观问题，给出观点但说明"这是个人看法"
- 使用适当的 emoji（✅ ❌ 🚀 💡）
```

### 原则 2：用"做"代替"不做"

❌ **禁止式写法：**
```markdown
# 行为准则
不要用太长的句子。不要用太多语气词。不要在一句话里说太多信息。
```

✅ **正向引导式写法：**
```markdown
# 沟通风格
- 句子简短，每句不超过 30 个字
- 一个回复只说一个重点
- 如果内容多，用列表分点说明
```

### 原则 3：使用场景举例

给出**正反例子**，AI 能更准确地理解期待：

```markdown
# 沟通风格示例

✅ 好的回复：
"根据文档，你需要在 openclaw.json 中将 allowRemote 设为 true。"

❌ 不好的回复：
"OpenClaw 允许您通过配置文件中的 allowRemote 参数来控制是否可以从外部网络访问您的 Gateway 实例。"

# 说明：要直接、简洁，不要啰嗦
```

### 原则 4：设定边界但留灵活性

```markdown
# 行为准则
- 执行文件删除操作前，必须让我确认
- 对于"我不知道"的问题，老实说不知道，可以建议我查询什么
- 如果我的请求有安全隐患（如执行不明脚本），主动提醒
- ⚠️ 绝对不要：读取 ~/.ssh/ 目录下的私钥文件
```

### 灵魂文件模板库

社区分享了一些常用的 soul.md 模板：

**极简版（适合只想快速测试的用户）：**
```markdown
# 角色
你叫"小助手"，用中文回答。
# 规则
回答要简洁，不知道就说不知道。
```

**程序员朋友版：**
```markdown
# 角色
你是 GeekPal，一个会写代码的朋友。
# 风格
说话随意，可以开玩笑。技术问题给代码示例。
# 规则
代码要附上解释。指出潜在的性能和安全问题。
```

**商务助理版：**
```markdown
# 角色
你是"小秘"，专业的商务助理。
# 风格
正式、简洁、结构化。先说结论再展开。
# 规则
处理文档确认版本。发送内容前先让用户审核。
```

## 10.2 安全性配置最佳实践

### 三层防护模型

```
第一层：网络层
├── 绑定到 localhost (127.0.0.1)
├── 或使用 Tailscale/WireGuard VPN
└── 使用防火墙限制端口

第二层：应用层
├── 用户 Allowlist
├── API Token 鉴权
├── Rate Limiting
└── 操作确认 (requireConfirmation)

第三层：数据层
├── API Key 用 .env 管理
├── 敏感目录排除
└── 日志定期清理
```

### 推荐的安全配置模板

```json
{
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789,
    "allowRemote": false,
    "apiToken": "your-random-token"
  },
  "security": {
    "allowlist": ["your_username"],
    "blocklist": [],
    "requireConfirmation": [
      "shell:rm",
      "shell:dd",
      "shell:mkfs",
      "shell:wget|curl",
      "file_write:~/.ssh/*",
      "file_write:/etc/*",
      "file_delete:*"
    ],
    "rateLimit": {
      "messagesPerMinute": 20,
      "messagesPerHour": 200,
      "tokensPerDay": 500000,
      "costLimit": {
        "daily": 5,
        "monthly": 100
      }
    },
    "allowedDomains": [
      "api.anthropic.com",
      "api.openai.com",
      "api.github.com",
      "api.telegram.org"
    ]
  }
}
```

### 密钥管理——使用 .env 文件

```bash
# ~/.openclaw/.env
ANTHROPIC_API_KEY=sk-ant-PLACEHOLDERxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxx
TELEGRAM_BOT_TOKEN=123456:ABC-DEF
```

然后在 `openclaw.json` 中引用：

```json
{
  "model": {
    "provider": "anthropic",
    "apiKey": "${ANTHROPIC_API_KEY}"
  }
}
```

这样即使配置文件泄露，API Key 也不会暴露。

## 10.3 多 Agent 管理策略

### Agent 分工模式

**模式 1：按功能分**
```
├── 搜索 Agent（擅长信息检索）
├── 写作 Agent（擅长内容创作）
├── 代码 Agent（擅长编程）
└── 审查 Agent（擅长审核和纠错）
```

**模式 2：按用途分**
```
├── 工作 Agent（专业、正式、工作日启用）
├── 个人 Agent（随意、生活化、全天候）
└── 学习 Agent（耐心、教学风格、按需启用）
```

**模式 3：按安全等级分**
```
├── 安全 Agent（无系统访问权限，只能回答问题）
├── 标准 Agent（有基本文件操作权限）
└── 管理 Agent（有完全系统权限，需要密码确认）
```

### 推荐的多 Agent 配置

```json
{
  "agents": {
    "safe": {
      "name": "安全问答",
      "model": "gpt-4o-mini",
      "systemPrompt": "你只能回答问题，不能执行任何操作。不要读取文件、不要执行命令、不要访问网络。",
      "channels": ["telegram"]
    },
    "work": {
      "name": "工作助手",
      "model": "claude-sonnet-4-20250514",
      "soulFile": "~/.openclaw/souls/work.md",
      "channels": ["slack"],
      "skills": ["gmail", "jira", "github", "calendar"],
      "cron": [
        {"schedule": "0 9 * * 1-5", "action": "准备今日日程摘要"}
      ]
    },
    "home": {
      "name": "生活管家",
      "model": "gpt-4o",
      "soulFile": "~/.openclaw/souls/friend.md",
      "channels": ["telegram", "whatsapp"],
      "skills": ["weather", "news", "reminder", "shopping"],
      "cron": [
        {"schedule": "0 7 * * *", "action": "早安问候+天气预报"}
      ]
    }
  }
}
```

## 10.4 Cron 任务设计模式

### 模式 1：固定时间汇报

```
每天早上8点 → 天气 + 日程 + 未读邮件摘要
每周一9点  → 上周工作总结
每月1号    → 月度账单/使用统计
```

### 模式 2：条件触发

```
当 GitHub Star 数超过 1000 时 → 发消息提醒
当服务器 CPU > 90% 时 → 告警
当收到特定关键词的邮件时 → 转推送到聊天软件
```

### 模式 3：任务链

```
早上8点   → 收集数据
早上8:05  → 分析数据，生成报告
早上8:10  → 推送报告到 Slack
```

### 模式 4：智能聚合

不是"每10分钟发一条消息"（这样你会被烦死），而是：

```
每30分钟检查重要事件
如果没有重要事件，不推送
如果有重要事件，合并成一条消息推送
每天下午6点发送一次"今日摘要"
```

### Cron 模板示例

```json
{
  "cron": [
    {
      "name": "晨间简报",
      "schedule": "30 7 * * 1-5",
      "action": "查询今天的天气、日程、未读邮件，生成一份简洁的晨间简报",
      "condition": "只在我起床后推送"
    },
    {
      "name": "GitHub 每日监控",
      "schedule": "0 10 * * *",
      "action": "检查我的所有 GitHub 仓库近24小时的活动：新 Issues、PR、Stars，汇总报告",
      "channel": "telegram"
    },
    {
      "name": "服务器健康检查",
      "schedule": "*/15 * * * *",
      "action": "检查服务器 CPU、内存、磁盘使用率，如果任何一项超过 90% 就告警",
      "channel": "slack",
      "silentOnSuccess": true
    },
    {
      "name": "周报生成",
      "schedule": "0 17 * * 5",
      "action": "生成本周工作周报：完成的 task、未完成的 task、下周计划",
      "channel": "slack",
      "skipOnHoliday": true
    }
  ]
}
```

## 10.5 Skills 开发指南

### 技能开发的黄金法则

1. **先有需求，再写技能**——不要为了写技能而写技能
2. **从小做起**——一个技能只做一件事，做好
3. **测试先行**——先用对话让 AI 执行你要的操作，确认能工作再封装成技能
4. **渐进增强**——版本 1.0 功能单一，版本 2.0 加错误处理，版本 3.0 加配置项

### 技能开发模板

```json
{
  "name": "技能名称",
  "description": "简短描述",
  "version": "1.0.0",
  "author": "你的名字",
  "triggers": [
    {
      "pattern": "触发正则表达式",
      "action": "动作名称"
    }
  ],
  "actions": {
    "动作名称": {
      "type": "动作类型",
      "config": {
        // 动作参数
      },
      "responseTemplate": "回复模板 {{变量}}",
      "errorTemplate": "出错了：{{error}}"
    }
  }
}
```

### 社区技能推荐

| 技能 | 功能 | 来源 |
|------|------|------|
| **Gmail** | 读取、搜索、发送邮件 | 官方 |
| **GitHub** | 监控仓库、Issues、PR | 官方 |
| **Calendar** | 读取和管理日历 | 官方 |
| **Browser** | 网页操作、截图 | 内置 |
| **Shell** | 执行终端命令 | 内置 |
| **Notion** | 读取和写入 Notion | 社区 |
| **Jira** | 项目管理 | 社区 |
| **Figma** | 设计稿查看 | 社区 |
| **Twitter/X** | 查看时间线、发推 | 社区 |
| **Spotify** | 控制音乐播放 | 社区 |

## 10.6 性能优化

### 减少 API 调用成本

```json
{
  "agent": {
    "model": "claude-sonnet-4-20250514",
    "maxTokens": 4096,
    "smartCache": {
      "enabled": true,
      "ttl": 300
    }
  }
}
```

- 日常对话用 `gpt-4o-mini` 或 `claude-haiku`（便宜又快）
- 复杂任务切换到 `claude-sonnet` 或 `gpt-4o`
- 开启 smartCache，相同问题不用重复调用 API

### 减少内存占用

```json
{
  "gateway": {
    "sessionTimeout": 30,
    "maxSessions": 20
  },
  "agent": {
    "maxContextMessages": 30
  },
  "logging": {
    "level": "warn",
    "maxLogSize": 5242880
  }
}
```

### 网络优化

如果 API 响应慢：

```json
{
  "proxy": {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
  },
  "agent": {
    "timeout": 60000,
    "retryOnTimeout": true,
    "maxRetries": 2
  }
}
```

## 10.7 学习路线图：从 Day 1 到 Week 4

### Day 1：初识

- [x] 了解 OpenClaw 是什么
- [x] 安装（推荐用一键安装）
- [x] 配置 Telegram 通道
- [x] 发第一条消息
- [ ] 探索 Dashboard 界面

### Day 2：基础配置

- [ ] 修改 soul.md，自定义 AI 人格
- [ ] 尝试不同的提问风格
- [ ] 让 AI 读取文件、执行命令
- [ ] 学习 `/reset`、`/help` 等命令

### Day 3：技能入门

- [ ] 安装 Gmail 或 GitHub 官方技能
- [ ] 测试技能的触发和响应
- [ ] 查看技能配置文件结构
- [ ] 尝试用对话框创建定时任务

### Day 4：自动化

- [ ] 创建第一个定时任务（如每日天气）
- [ ] 测试定时任务执行
- [ ] 学习 cron 表达式
- [ ] 创建"任务链"（A 完成 → 触发 B）

### Day 5：多通道

- [ ] 配置第二个通道（如 Discord 或 Slack）
- [ ] 测试跨通道会话同步
- [ ] 设置不同通道的权限

### Week 2：进阶

- [ ] 编写第一个自定义技能
- [ ] 配置多 Agent（工作和个人）
- [ ] 学习高级 soul.md 写法
- [ ] 了解 Multi-Agent 路由

### Week 3：生产化

- [ ] 配置 Tailscale 远程访问
- [ ] 设置安全加固（Allowlist、Rate Limit）
- [ ] 配置系统服务自启动
- [ ] 创建生产级定时任务

### Week 4：深入

- [ ] 尝试修改 OpenClaw 源码
- [ ] 为社区贡献技能或文档
- [ ] 探索 Live Canvas 高级用法
- [ ] 参与社区 Discussions

---

# 第十一章：未来展望——自托管AI的下一个五年

> ⚠️ **本章声明：** 以下内容是作者基于对 OpenClaw 项目和 AI 行业的观察进行的原创分析，并非官方路线图。观点仅代表个人判断，不构成投资或决策建议。

---

## 11.1 "个人AI助手"市场正在经历什么？

2024-2025 年，AI 行业出现了一个明显转向：从"更大的模型"到"更好用的 Agent"。Benchmark 竞赛的热度在下降，取而代之的是对"AI 能不能真正帮我做事"的追问。

这个转向有几个标志性事件：
- **2024 年中**：Anthropic 发布 Computer Use，AI 首次能直接操作电脑界面
- **2024 年底**：OpenAI 发布 Operator，AI Agent 概念进入主流视野
- **2025 年初**：OpenClaw 在 GitHub 爆红，68K+ Stars 证明"自托管 AI"不是小众需求

但"AI 助手"这个品类目前仍然处于**早期混乱阶段**。市场上充斥着几百个"AI 助手"产品，但绝大多数只是套了一层 ChatGPT API 的聊天机器人。真正能理解用户、主动执行任务、跨平台协同的，寥寥无几。

OpenClaw 的优势在于它**找准了一个没有被充分满足的需求**：我不需要另一个聊天界面，我需要一个能用我已有的聊天软件、主动帮我做事的 AI。

## 11.2 开源 AI 生态中的 OpenClaw

如果把开源 AI 生态比作一个城市：
- **Ollama** 是发电厂——让本地运行模型成为可能
- **LangChain / Vercel AI SDK** 是建筑公司——提供搭建 AI 应用的框架
- **OpenClaw** 是住宅——是最终用户直接居住的地方

这个定位很微妙。它不像 Llama 那样处于底层基础设施的位置，也不像 ChatGPT 那样是"所有用户的起点"。它是一个**中间层**——面向"想要拥有自己 AI 的人"。

从生态位来看，OpenClaw 面对的核心问题是：**普通用户真的需要自托管 AI 吗？**

目前的答案是"越来越多的普通用户正在意识到这个需求"。推动因素包括：
- ChatGPT/Claude 频繁的隐私争议
- 企业开始限制员工使用外部 AI 服务
- API 价格持续下降使自托管成本可控
- "我的数据我做主"的意识在觉醒

## 11.3 商业模式困境——开源 AI 能赚钱吗？

这是 OpenClaw 面临的最现实的问题。MIT 许可证意味着任何人都可以免费使用、修改、分发代码。那么钱从哪里来？

对比一下其他开源项目的商业模式：

| 模式 | 代表项目 | 适用性 |
|------|----------|--------|
| 开源免费 + 云服务收费 | GitLab, Supabase | ❌ 自托管意味着用户不想要云服务 |
| 开源免费 + 企业版付费 | Docker, Redis | ✅ 有可能 |
| 开源免费 + 技术支持 | Red Hat, Elastic | ✅ 有可能 |
| 创始人个人资金 + 捐赠 | Signal, Mastodon | ❌ 不太可持续 |
| VC 融资 + 后期变现 | Hugging Face | ❌ 与 MIT 理念冲突 |

OpenClaw 最可能的路径是**Docker 模式**：基础版本完全免费开源，企业版本提供额外的管理功能、审计日志、SSO 集成等企业需要的功能。

但 Peter Steinberger 有 PSPDFKit 的经验。PSPDFKit 走的正是"开源社区版 + 商业授权"的路线，而且非常成功。所以对于 OpenClaw 的商业模式，我们不必过于担心——Peter 比大多数创始人更懂得如何在开源和盈利之间找到平衡。

## 11.4 自托管 vs 云端：永恒的张力和未来的平衡

这不是一个"谁更好"的问题，而是一个"适合什么场景"的问题。

**自托管 AI 的优势场景：**
- 企业数据合规（金融、医疗、法律）
- 隐私敏感用户
- 需要深度定制的场景
- 离线或受限网络环境

**云端 AI 的优势场景：**
- 零配置，拿来就用
- 需要顶级模型（最新的模型通常先在云端提供）
- 低使用频率，不值得自己维护
- 团队协作（共享工作空间）

**未来的趋势不是"二选一"，而是"混合模式"：**

```
日常工作 → 云端模型（快速、便宜、最新）
敏感数据 → 本地模型（安全、私密、可控）
关键任务 → 本地模型 + 云端后备（可靠、灵活）
```

OpenClaw 的架构天然支持这种混合模式。你可以配置主模型用本地 Ollama，备份模型用 Claude API。数据在本地处理，只有在需要时才调用云端。

## 11.5 "Agent 可靠性"问题——能解决吗？

这是当前 AI Agent 领域最大的瓶颈。OpenClaw 也不例外。

**可靠性问题的三个层面：**

**1. 模型幻觉**（Model Hallucination）
- AI 会自信地给出错误答案
- 目前没有完美的解决方案
- 缓解方法：让 AI 优先使用工具查找事实，而不是依赖内部知识

**2. 工具调用错误**（Tool Misuse）
- AI 可能调用错误的工具，或使用错误的参数
- 缓解方法：更严格的技能定义、操作确认机制

**3. 任务执行不完整**（Task Incompletion）
- AI 在复杂任务链中容易遗漏步骤
- 缓解方法：将任务分解为更小的子任务，逐步验证

**我的判断：Agent 可靠性问题在未来 3-5 年内会有显著改善，但不会 100% 解决。** 原因是这本质上是"大语言模型是否真正理解世界"的问题——只要模型还是基于概率预测的，就一定会有不可靠的时候。

但这并不意味着 Agent 不可用。就像人类员工也不是 100% 可靠，但我们通过培训、流程、审核机制来管理。OpenClaw 的 `requireConfirmation`、`cron` 任务链、多 Agent 审核等设计，正是这种"人机协作"的实践。

## 11.6 OpenClaw：会成为"AI 界的 Linux"还是逐渐淡出？

这是一个值得认真思考的问题。

**支持 OpenClaw 成为"AI 界 Linux"的理由：**
- MIT 许可证——这是 Linux 成功的关键因素之一
- 简洁优雅的架构——Channel → Gateway → Pi Agent 的层级设计足够简洁通用
- 社区增长势头——68K+ Stars 不是靠营销砸出来的
- 创始人经验——Peter 有长期维护开源项目的记录（PSPDFKit 超过 10 年）

**让 OpenClaw 面临挑战的因素：**
- AI 基础设施变化快——新的模型、新的协议、新的范式不断出现
- 大公司的竞争——Google、OpenAI、Anthropic 都在做类似的产品
- 用户门槛——自托管始终不如 SaaS 方便
- 维护成本——一个 68K Stars 的项目需要的维护投入是巨大的

**最可能的结局：介于两者之间。**

OpenClaw 不太可能像 Linux 那样彻底统治服务器端，也不太可能像很多开源项目那样几年后销声匿迹。它更可能像 Docker——**从一个小众的开发者工具，成长为行业基础设施的重要组成部分，但同时也面临商业化压力和来自大公司的竞争。**

## 11.7 从 PSPDFKit 到 OpenClaw——Peter 学到了什么？

PSPDFKit 的十年经验对 OpenClaw 有深刻影响：

**1. 质量 > 速度**
PSPDFKit 以代码质量著称。在 PDF 渲染这个领域，崩溃一次就可能失去客户。Peter 把对质量的偏执带到了 OpenClaw——代码整洁、架构清晰、文档完善。

**2. 开发者体验是第一位的**
PSPDFKit 成功的秘诀之一是"开发者集成体验最好"。OpenClaw 的一键安装、直观的 Dashboard、可定制的 soul.md，都体现了 Peter 对"用户体验"的理解——用户不只是最终用户，包括开发者。

**3. 独立性保护了产品**
PSPDFKit 是完全自筹资金的公司，没有 VC 压力。这意味着 Peter 可以做出"对用户最好的决定"而不是"对投资人最好的决定"。OpenClaw 继承了这个基因——MIT 许可证、不追踪用户、没有数据变现计划。

**4. 开源的边界**
PSPDFKit 的商业模式是"开源 UI 组件 + 商业 SDK"。OpenClaw 可能会走类似的路线——核心功能开源，高级企业功能收费。

## 11.8 开源对抗大厂 AI 垄断

AI 行业目前存在一个令人不安的趋势：**AI 能力正在向少数大公司集中。** 最好的模型（GPT-4、Claude 3.5 Opus、Gemini Ultra）都在云端，API 价格和数据使用条款由大公司单方面决定。

开源项目在反制这种集中化：

| 层面 | 大厂方案 | 开源替代 |
|------|----------|----------|
| 模型 | GPT-4, Claude | Llama, Mistral, Qwen |
| 工具 | ChatGPT, Claude.ai | OpenClaw, Open Interpreter |
| 运行 | 自有服务器 | Ollama, LocalAI |
| 数据 | 云端存储 | 本地存储 |

OpenClaw 在这个生态中扮演的角色是"连接器"——它不跟大厂抢模型层（这也不现实），而是在"应用层"提供一种选择。它的价值在于：**即使你用的是大厂的模型 API（Claude、GPT），但你的数据、你的配置、你的体验，都在你自己的控制之下。**

## 11.9 隐私作为竞争壁垒——能持久吗？

"隐私优先"是 OpenClaw 最大的卖点之一。但这个优势能维持多久？

**短期（1-2 年）：** 隐私是强大的竞争优势。大厂不断爆出的隐私丑闻 + 监管收紧 = 越来越多用户寻求自托管方案。

**中期（3-5 年）：** 大厂会模仿。Google 可能推出"本地运行版 Gemini"，OpenAI 可能推出"企业私有部署"。但它们的商业模式和代码开源程度决定了不可能完全复制 OpenClaw。

**长期（5 年+）：** 真正的壁垒不是"隐私"本身，而是**生态**。如果 OpenClaw 积累了丰富的技能生态、社区模板、第三方集成，用户的迁移成本就会很高。就像 Linux 的成功不是因为"免费"，而是因为"免费 + 运行的软件足够多"。

## 11.10 写给下一个五年的预测

最后，基于以上分析，给出 10 个大胆但有理有据的预测：

1. **到 2028 年，"自托管 AI"将成为企业 IT 标准配置**，与"自托管邮件服务器"一样普遍
2. **OpenClaw 的 Stars 将在 2027 年突破 20 万**——如果项目保持当前的增长势头
3. **会出现"OpenClaw 企业版"**——提供 SSO、审计、合规报告等功能
4. **"AI Agent Marketplace"（类似 App Store 的 AI 技能商店）将成为 OpenClaw 的核心功能**
5. **本地模型 + 云端模型混合运行将成为默认配置**——不再是"非此即彼"
6. **AI 安全问题将催生专门的"AI 安全审计"工具**——与 OpenClaw 集成
7. **多 Agent 协作将成为 OpenClaw 最引人注目的功能**——超过单 Agent 的使用
8. **Telegram 仍将是最常用的通道**——因为它对 Bot 的支持最好
9. **会出现 OpenClaw 的 WebAssembly 版本**——在浏览器中直接运行
10. **2027-2028 年，某个大公司会收购或 fork OpenClaw**——这将是一个决定项目命运的关键时刻

---

**最后的话：**

OpenClaw 不是一个完美的项目，但它代表了一个方向——**AI 不必由少数大公司控制，你可以拥有自己的 AI。** 这个想法本身就足够重要，值得我们去尝试、去贡献、去期待。无论 OpenClaw 未来走向何方，它所开启的"自托管 AI"运动，已经在改变人与 AI 的关系了。

---

# 附录：术语表

> 中英对照 + 使用场景说明，方便查阅。

## A

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Agentic Loop** | Agentic Loop | AI Agent 自动执行的循环：接收输入→分析→使用工具→生成回复→等待下一轮输入 | 理解 OpenClaw 工作方式的核心概念 |
| **Allowlist** | Allowlist (Whitelist) | 允许访问的用户列表 | 安全配置中限制只有特定用户能与 AI 对话 |

## C

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Cron** | Cron | 定时任务系统，按指定时间自动执行任务 | "每天早上8点给我发天气预报" |
| **Channel** | Channel | 聊天通道，OpenClaw 接入的聊天平台 | Telegram、WhatsApp、Discord 等 |

## G

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Gateway** | Gateway | 中央路由进程，运行在端口 18789 上，负责消息路由、会话管理 | 启动/停止 OpenClaw、配置端口 |
| **Gateway API** | Gateway API | Gateway 提供的 HTTP API | 编程方式控制 OpenClaw |

## L

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Live Canvas** | Live Canvas | 可视化交互工作区，展示图表、流程图、代码 | "帮我画一个流程图"→自动打开 Canvas |

## M

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Memory** | Memory | AI 的长期记忆，跨会话保留重要信息 | 让 AI 记住你的名字、偏好、重要日期 |
| **Mobile Node** | Mobile Node | 手机端的 OpenClaw Companion App | 手机拍照识物、位置感知、语音输入 |
| **Multi-Agent** | Multi-Agent | 多智能体协作，多个 AI 代理分工合作 | 一个搜索、一个写作、一个审查 |

## O

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Onboarding** | Onboarding | 初始配置向导 `openclaw onboard` | 首次安装后运行 |
| **OpenClaw** | OpenClaw | 开源自托管 AI 助手的名称 | 整个手册的主题 😄 |

## P

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Pi Agent** | Pi Agent | OpenClaw 的默认 AI 智能体 | AI 处理请求的"大脑" |
| **Plugin** | Plugin | 插件，可扩展 OpenClaw 的功能 | "安装 Gmail 插件"→读取邮件 |

## R

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Rate Limiting** | Rate Limiting | 速率限制，防止 API 被过度使用 | 设置每分钟最多 20 条消息 |

## S

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Self-hosted** | Self-hosted | 自托管，在你的机器上运行 | "OpenClaw 是自托管的"→数据不离开你的电脑 |
| **Session** | Session | 会话，一次对话的上下文 | 多轮对话的连续性、跨设备同步 |
| **Skill** | Skill | 技能，AI 的扩展能力 | 安装"天气"技能→AI 能查天气 |
| **soul.md** | soul.md | 灵魂文件，定义 AI 的人格和行为 | 修改 soul.md→改变 AI 说话风格 |
| **SSH Tunnel** | SSH Tunnel | SSH 隧道，安全远程访问方式 | 从外网通过 SSH 访问 Gateway |

## T

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Tailscale** | Tailscale | 基于 WireGuard 的 VPN 工具，创建私有网络 | 安全的远程访问 OpenClaw Dashboard |
| **Tool Use** | Tool Use | 工具调用，AI 使用外部工具的能力 | AI 调用 Shell 命令、读取文件、访问网页 |

## W

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **Web Control UI** | Web Control UI | 浏览器中的管理界面 `http://127.0.0.1:18789` | 管理设置、查看日志、配置技能 |

## 其他

| 术语 | 英文 | 说明 | 使用场景 |
|------|------|------|----------|
| **18789** | 18789 | Gateway 默认运行端口 | 启动失败时检查端口是否被占用 |
| **Molty** | Molty | OpenClaw 的多模型路由组件 | 多模型间的请求分发 |
| **requireConfirmation** | requireConfirmation | 敏感操作需要用户确认 | 避免 AI 误删除文件 |
| **Live Canvas** | Live Canvas | 交互式画布 | 数据可视化、流程图编辑 |
| **Agentic Loop** | Agentic Loop | 自主循环 | OpenClaw 的核心运行机制 |

---

> 📖 **本手册由社区贡献者撰写，内容依据 OpenClaw v1.0 版本。** OpenClaw 仍在快速发展中，部分功能可能在新版本中有变化。建议同时参考 [docs.openclaw.ai](https://docs.openclaw.ai) 获取最新信息。
>
> 欢迎贡献和修正！请访问 [github.com/personalailabs/openclaw](https://github.com/personalailabs/openclaw) 参与社区讨论。

