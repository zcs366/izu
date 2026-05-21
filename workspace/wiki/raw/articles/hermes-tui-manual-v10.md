---
source_url: file:///mnt/i/hermes/wiki_dropbox/hermes-tui-manual-v1.0.md
ingested: 2026-05-11
sha256: 6a8795a2c4e9b861d404800259c01c8fbe1fae515a72a888d0be83449850efaa
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: ---
---

# ---

> 来源: hermes-tui-manual-v1.0.md（用户存入 wiki_dropbox）

---
title: Hermes TUI 完全手册
version: 1.0
date: 2026-05-09
author: 军师祭酒
tags: [hermes, tui, terminal-ui, ink, react]
---

# Hermes TUI 完全手册

> 从零掌握 Hermes Agent 的现代终端界面

---

## 第1章：概览与核心理念

### 1.1 什么是 Hermes TUI

Hermes Agent 是 Nous Research 开发的开源 AI 智能体框架。它提供两种终端交互方式：

| 模式 | 启动方式 | 技术栈 | 特点 |
|------|---------|--------|------|
| **经典 REPL** | `hermes`（默认） | Python prompt_toolkit | 轻量、稳定、功能完整 |
| **现代 TUI** | `hermes --tui` | Ink (React for Terminal) | 美观、交互丰富、实时反馈 |

**TUI = Terminal User Interface（终端用户界面）**。它不是 Web 界面，而是跑在终端里的 React 应用——用 `Ink` 框架在终端里渲染组件，像 React 在浏览器里渲染 DOM 一样。

### 1.2 为什么要用 TUI 而不是经典 REPL

用一个类比来解释：

> **经典 REPL 像手写便签**——功能足够，但每一个操作都是一次性的文字流，没有结构。
> **TUI 像带面板的办公桌**——聊天区、工具执行区、提示区各自占一块地方，你能同时看到多个信息层。

具体区别：

| 维度 | 经典 REPL | 现代 TUI |
|------|----------|----------|
| 渲染方式 | 纯文本流式输出 | 组件化渲染（Ink + React） |
| 工具执行 | 文字列表 | 动态面板，实时状态 |
| 模型推理 | 等待文字出现 | 动画指示器 + 思维链展示 |
| 命令输入 | 单行提示符 | 带自动补全的编辑器 |
| 主题皮肤 | 色彩+符号 | 完整主题系统 |
| 历史会话 | `/continue` 命令 | 会话选择器 |
| 架构 | 单进程 Python | TS (Ink) + Python 双进程 JSON-RPC |

### 1.3 架构总览

```
hermes --tui
  └─ Node.js (Ink/React)  ──stdio JSON-RPC──  Python (tui_gateway)
       │                                          └─ AIAgent + tools + sessions
       └─ 渲染: transcript, composer, prompts, activity
```

- **TypeScript 端**（`ui-tui/`）: 用 Ink 框架渲染屏幕。**TypeScript 拥有屏幕渲染权。**
- **Python 端**（`tui_gateway/`）: 处理会话、工具调用、模型推理、斜杠命令逻辑。**Python 拥有计算权。**
- **通信协议**：换行分隔的 JSON-RPC，通过 stdio 双向传输。

这种架构的好处是显而易见的：
- 画面渲染和业务逻辑解耦，互不阻塞
- 模型推理耗时不会卡死 UI
- 两端可以用各自最擅长的技术栈

### 1.4 与 Dashboard 的关系

Dashboard（`hermes dashboard` 启动的 Web UI，端口 9119）**嵌入的是真正的 Hermes TUI**，而不是重新实现了一遍聊天界面。

```
Dashboard (Web)
  └─ xterm.js Terminal
       └─ WebSocket /api/pty
            └─ PTY bridge
                 └─ hermes --tui (真正的 Ink 实例)
```

这意味着你在 Web Dashboard 里看到的聊天界面，和在终端里跑 `hermes --tui` 看到的是**同一个程序**，只是通过 WebSocket 代理到了浏览器。

---

## 第2章：安装部署全指南

### 2.1 前提条件

| 依赖 | 用途 | 检查命令 |
|------|------|---------|
| Node.js >= 18 | 运行 Ink TUI | `node --version` |
| npm | 安装依赖 | `npm --version` |
| Python >= 3.10 | Hermes 核心 | `python3 --version` |
| Hermes Agent | 本体 | `hermes --version` |

### 2.2 安装方式

**方式一：一键安装（推荐）**

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装完成后，直接启动 TUI：

```bash
hermes --tui
```

**方式二：源码安装（开发用）**

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
source .venv/bin/activate
uv pip install -e .

# 安装 TUI 依赖
cd ui-tui
npm install
npm run build    # 构建生产版本
```

**方式三：环境变量激活**

如果不想每次输入 `--tui` 参数，可以设置环境变量：

```bash
export HERMES_TUI=1
hermes   # 自动进入 TUI 模式
```

### 2.3 验证安装

```bash
# 检查版本
hermes --version        # 应显示 v0.13.0+

# 检查 TUI 是否可启动（会进入界面，按 Ctrl+C 退出）
hermes --tui --version  # 显示 TUI 相关信息

# 检查依赖
hermes doctor           # 检查所有组件状态
```

### 2.4 开发模式

如果你在开发 TUI 组件，用开发模式（热重载）：

```bash
cd ~/.hermes/hermes-agent/ui-tui
npm run dev
# 然后在新终端运行：
hermes --tui --dev
```

`--dev` 标志让 Hermes 使用 TypeScript 源码（通过 tsx 运行）而不是 `dist/` 下的构建产物。代码修改后自动重载。

---

## 第3章：界面与基础操作

### 3.1 界面布局

TUI 启动后，屏幕分为几个区域：

```
┌─────────────────────────────────────────────────────┐
│  对话标题 / 模型信息 / 配置状态         (状态栏)     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  对话记录区 (Transcript)                             │
│  ┌─────────────────────────────────────────────────┐│
│  │ User: 帮我查一下最新新闻                        ││
│  │ Assistant: 好的，我来搜索...                    ││
│  │  ┌─ 🔍 web_search ──────────────────────────┐  ││
│  │  │ 搜索中...                                 │  ││
│  │  └───────────────────────────────────────────┘  ││
│  │ 以下是今天的新闻摘要：                          ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
├─────────────────────────────────────────────────────┤
│ > /  输入你的问题...                    [模型名]     │
│   ┌── 命令提示区 ────────────────────────────────┐  │
│   │ /help  /model  /skin  /retry  /new  ...      │  │
│   └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 3.2 基本操作

**发送消息**：在底部输入框键入内容，按 `Enter` 发送。

**输入多行**：按 `Alt+Enter` 或 `Meta+Enter` 插入换行。

**自动补全**：
- 输入 `/` 触发斜杠命令自动补全
- 输入文件路径时自动补全路径

**滚动查看历史**：
- 方向键 `↑` `↓` 滚动对话
- `PageUp` `PageDown` 快速翻页

### 3.3 斜杠命令速查

斜杠命令是 TUI 的效率核心。输入 `/` 即可看到完整列表：

| 命令 | 作用 | 操作对象 |
|------|------|---------|
| `/new` 或 `/reset` | 开始新会话 | 会话控制 |
| `/clear` | 清屏+新会话（CLI） | 会话控制 |
| `/retry` | 重新发送上条消息 | 会话控制 |
| `/undo` | 撤回落幕 | 会话控制 |
| `/title [name]` | 命名当前会话 | 会话控制 |
| `/compress` | 手动压缩上下文 | 会话控制 |
| `/stop` | 终止后台进程 | 会话控制 |
| `/rollback [N]` | 回滚文件系统检查点 | 会话控制 |
| `/background <prompt>` | 后台运行提示 | 会话控制 |
| `/queue <prompt>` | 排队下一轮 | 会话控制 |
| `/resume [name]` | 恢复命名会话 | 会话控制 |
| `/model [name]` | 查看或切换模型 | 配置 |
| `/skin [name]` | 切换主题皮肤 | 配置 |
| `/reasoning [level]` | 设置推理级别 | 配置 |
| `/verbose` | 切换详细输出 | 配置 |
| `/voice [on/off/tts]` | 语音模式 | 配置 |
| `/yolo` | 绕过危险命令确认 | 配置 |
| `/tools` | 管理工具（CLI） | 工具 |
| `/skill <name>` | 加载技能 | 技能 |
| `/cron` | 管理定时任务 | 工具 |
| `/help` | 显示帮助 | 信息 |
| `/usage` | Token 使用统计 | 信息 |
| `/quit` 或 `/exit` | 退出 | 退出 |

### 3.4 状态栏解读

TUI 顶部状态栏显示：

```
Hermes Agent | deepseek-v4-flash | 会话: 新闻查询 | [○ 正常]
```

- **Agent 名称**：从左到右
- **当前模型**：如 `deepseek-v4-flash`
- **会话标题**：自动生成或手动命名
- **连接状态**：`○ 正常` / `◐ 推理中` / `● 工具执行中`

### 3.5 工具执行可视化

当模型调用工具时，TUI 会显示一个动态面板：

```
┌─ 🔍 web_search ─────────────────────────────────┐
│  ⚡ 正在搜索 "latest AI news 2026"...             │
│  进度: ████████░░ 80%                            │
└──────────────────────────────────────────────────┘
```

工具完成后，结果以折叠/展开形式显示，不会污染对话主区域。

---

## 第4章：实战——从零搭建第一条对话

### 4.1 场景：信息查询助手

假设你想搭建一个「每日 AI 资讯查询」助手，让它每天早上帮你搜索最新 AI 动态。

**第一步：启动 TUI**

```bash
hermes --tui
```

你会看到欢迎信息和底部的输入提示符。

**第二步：发送第一条消息**

在输入框输入：

```
帮我搜索今天最新的 AI 新闻，列出前5条
```

按 `Enter` 发送。你会看到：

1. 模型开始「思考」（状态栏显示推理指示器）
2. 模型调用 `web_search` 工具（面板动态出现）
3. 搜索结果返回（面板显示结果数）
4. 模型组织回答（逐字流式输出）

**第三步：切换模型**

如果觉得当前模型回答不够好：

```
/model
```

TUI 会显示可用的模型列表，让你交互式选择。

**第四步：命名会话**

```
/title AI资讯测试
```

方便以后按名字恢复。

**第五步：退出**

```
/quit
```

### 4.2 场景：代码审查

```
帮我审查下面这段 Python 代码的性能问题：

def process(data):
    result = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            result.append(data[i][j] * 2)
    return result
```

模型会分析代码，调用工具执行测试，然后在对话中给出优化建议。

### 4.3 场景：多轮深度研究

```
/background 帮我持续监控这个 GitHub 仓库的 release: https://github.com/NousResearch/hermes-agent
```

这条命令让任务在后台运行，你可以继续聊天。任务完成后会收到通知。

---

## 第5章：参数详解

### 5.1 启动参数

| 参数 | 示例 | 作用 | 类比 |
|------|------|------|------|
| `--tui` | `hermes --tui` | 启动 TUI 模式 | 像在浏览器里打开一个新标签页 |
| `--dev` | `hermes --tui --dev` | 使用源码而非构建产物 | 开发模式，改了代码立刻见效 |
| `-m MODEL` | `hermes --tui -m claude-sonnet-4` | 指定模型 | 换引擎不换车身 |
| `--provider P` | `hermes --tui --provider openrouter` | 指定提供商 | 选加油站 |
| `-t TOOLSETS` | `hermes --tui -t web,terminal` | 启用工具集 | 只带需要的工具箱 |
| `-r SESSION` | `hermes --tui -r abc123` | 恢复会话 | 打开上次没看完的书 |
| `-c [NAME]` | `hermes --tui -c` | 继续最近会话 | 翻开上次看到的那页 |
| `-s SKILLS` | `hermes --tui -s hermes-agent,github-auth` | 预加载技能 | 提前准备好工具书 |
| `--yolo` | `hermes --tui --yolo` | 跳过危险操作确认 | 拆掉安全护栏 |
| `--pass-session-id` | `hermes --tui --pass-session-id` | 传递会话 ID 给模型 | 让助手知道它在哪间办公室 |

### 5.2 配置参数

**显示相关配置（`display.*`）**

| 配置键 | 可选值 | 默认值 | 作用 |
|--------|--------|--------|------|
| `display.compact` | `true` / `false` | `false` | 紧凑模式，减少空白 |
| `display.skin` | `default` / `ares` / `mono` / `slate` / 自定义 | `default` | 主题皮肤 |
| `display.tui_status_indicator` | `kaomoji` / `text` / `simple` | `kaomoji` | 状态指示器风格 |
| `display.tui_auto_resume_recent` | `true` / `false` | `false` | 启动时自动恢复最近会话 |
| `display.show_reasoning` | `true` / `false` | `false` | 显示模型推理过程 |
| `display.streaming` | `true` / `false` | `true` | 流式输出 |
| `display.show_cost` | `true` / `false` | `false` | 显示每次调用的费用 |
| `display.language` | `en` / `zh` / `ja` 等 | `en` | 界面语言 |
| `display.bell_on_complete` | `true` / `false` | `false` | 任务完成时响铃 |
| `display.busy_input_mode` | `interrupt` / `queue` | `interrupt` | 忙时输入处理方式 |

**运行时底部栏配置（`display.runtime_footer`）**

```yaml
display:
  runtime_footer:
    enabled: true
    fields:
      - model        # 显示当前模型
      - context_pct  # 显示上下文使用百分比
      - cwd          # 显示当前工作目录
```

### 5.3 推理级别详解

`/reasoning` 命令控制模型展示「思考过程」的程度：

| 级别 | 效果 | 适用场景 |
|------|------|---------|
| `none` | 不展示推理过程 | 日常对话，追求简洁 |
| `minimal` | 仅显示推理结束标志 | 半信半疑时查看 |
| `low` | 简短推理摘要 | 调试简单问题 |
| `medium` | 中等长度推理 | 一般开发工作 |
| `high` | 详细推理过程 | 复杂问题分析 |
| `xhigh` | 完整推理链 | 深度研究、教学 |

---

## 第6章：进阶技术详解

### 6.1 自定义皮肤系统

Hermes TUI 的皮肤系统是数据驱动的——不需要写代码，只需要一个 YAML 文件。

**内置皮肤一览：**

| 皮肤名 | 风格 | 适合 |
|--------|------|------|
| `default` | 经典 Hermes 金色/可爱风 | 默认，所有人都适合 |
| `ares` | 深红/青铜战神主题 | 喜欢暗黑风格的开发者 |
| `mono` | 干净灰阶单色 | 极简主义者 |
| `slate` | 冷蓝色开发者主题 | 长时间使用，护眼 |

**创建自定义皮肤：**

在 `~/.hermes/skins/` 目录下创建一个 YAML 文件：

```yaml
# ~/.hermes/skins/cyberpunk.yaml
name: cyberpunk
description: 赛博朋克终端主题

colors:
  banner_border: "#FF00FF"     # 霓虹粉边框
  banner_title: "#00FFFF"      # 青色标题
  banner_accent: "#FF1493"     # 深粉高亮
  banner_dim: "#666666"        # 灰色次要信息
  banner_text: "#CCCCCC"       # 浅灰正文
  response_border: "#00FF88"   # 绿色回答框

spinner:
  waiting_faces: ["⟳", "⟲", "⟰"]
  thinking_faces: ["◐", "◓", "◑", "◒"]
  thinking_verbs: ["jacking in", "decrypting", "uploading"]
  wings:
    - ["⟨⚡", "⚡⟩"]

branding:
  agent_name: "Cyber Agent"
  welcome: "进入赛博空间..."
  response_label: " ⚡ Cyber "
  prompt_symbol: "⚡"

tool_prefix: "▏"
```

**激活皮肤：**

```bash
# 临时切换
/skin cyberpunk

# 永久设置
hermes config set display.skin cyberpunk
```

**可自定义的完整元素表：**

| 界面元素 | 配置键 | 归属 |
|---------|--------|------|
| 横幅边框 | `colors.banner_border` | banner.py |
| 横幅标题 | `colors.banner_title` | banner.py |
| 横幅分区标题 | `colors.banner_accent` | banner.py |
| 横幅灰色文字 | `colors.banner_dim` | banner.py |
| 横幅正文 | `colors.banner_text` | banner.py |
| 回答框边框 | `colors.response_border` | cli.py |
| 等待动画 | `spinner.waiting_faces` | display.py |
| 思考动画 | `spinner.thinking_faces` | display.py |
| 思考动词 | `spinner.thinking_verbs` | display.py |
| 动画翅膀 | `spinner.wings` | display.py |
| 工具输出前缀 | `tool_prefix` | display.py |
| 工具 emoji 映射 | `tool_emojis` | display.py |
| Agent 名称 | `branding.agent_name` | banner.py, cli.py |
| 欢迎语 | `branding.welcome` | cli.py |
| 回答框标签 | `branding.response_label` | cli.py |
| 提示符 | `branding.prompt_symbol` | cli.py |

### 6.2 状态指示器

`display.tui_status_indicator` 控制 TUI 的状态图标风格：

| 值 | 效果 | 示例 |
|-----|------|------|
| `kaomoji` | 颜文字风格 | `(◕‿◕)`, `(>_<)`, `(╯°□°)` |
| `text` | 纯文本 | `[OK]`, `[BUSY]`, `[ERROR]` |
| `simple` | 简单符号 | `●`, `◐`, `✕` |

### 6.3 紧凑模式

`display.compact: true` 会减少界面空白、缩短信息行距，适合在小屏幕终端中使用：

```yaml
display:
  compact: true
  tool_preview_length: 0      # 不显示工具预览
  tool_progress: minimal      # 最小化工具进度显示
```

### 6.4 后台任务管理

`/background` 命令是 TUI 的杀手级功能之一。它让模型在后台运行耗时任务（如大型代码审查、批量数据处理），而你可以在前台继续聊天。

```bash
/background 帮我重构这个项目中的 user_service.py 模块
```

后台任务的状态会显示在状态栏中，完成后会收到通知。

### 6.5 会话管理

TUI 的会话管理比经典 REPL 更直观：

**恢复特定会话：**
```bash
hermes --tui -r 20260509_083000_abc123
```

**自动恢复最近会话：**
```bash
# 配置
hermes config set display.tui_auto_resume_recent true
```

**会话选择器：**
在 TUI 中输入 `/resume` 不带参数，会显示交互式会话选择器，可以用方向键浏览和选择。

### 6.6 Dashboard 中的 TUI

访问 `http://localhost:9119/chat` 可以在浏览器中使用 TUI：

```
hermes dashboard --port 9119 --no-open --tui
```

浏览器中的 TUI 通过 WebSocket 连接到 Hermes 的 PTY 桥接，体验与终端一致，但多了：
- 可调整字体大小
- 支持复制粘贴
- 多标签页操作

---

## 第7章：社区资源精选

### 7.1 官方资源

**Hermes Agent GitHub**
- URL: https://github.com/NousResearch/hermes-agent
- 适合人群：所有用户
- 内容概览：源代码、Issue 跟踪、Release 说明、贡献指南
- 为什么值得看：获取最新功能文档，报告 Bug，了解开发进度
- 一句话评价：这是你了解 TUI 所有细节的第一站
- 学到的东西：项目结构、配置选项、开发模式

**Hermes Agent 官方文档**
- URL: https://hermes-agent.nousresearch.com/docs/
- 适合人群：所有用户
- 内容概览：安装指南、CLI 参考、技能系统、平台配置
- 为什么值得看：最权威的配置参数说明
- 一句话评价：遇到问题先查这里
- 学到的东西：配置参数详解、集成方案

### 7.2 教程资源

**元小二学 AI——Hermes 全套教程**
- URL: 微信公众号「元小二学AI」
- 适合人群：中文用户、Hermes 新手
- 内容概览：从入门到高级的 Hermes 使用教程，含实战案例
- 为什么值得看：中文内容中最系统的 Hermes 教程
- 一句话评价：国内最接地气的 Hermes 教程系列
- 学到的东西：实际部署经验、自动化配置技巧

**Ink 框架官方文档**
- URL: https://github.com/vadimdemedes/ink
- 适合人群：想自定义 TUI 的开发者
- 内容概览：React-in-Terminal 完整 API
- 为什么值得看：TUI 的底层渲染框架
- 一句话评价：理解了 Ink 就理解了 TUI 的工作原理
- 学到的东西：Ink 组件开发、终端渲染原理

### 7.3 技术分析

**NouResearch 官方 Blog**
- URL: https://nousresearch.com/
- 适合人群：深度用户
- 内容概览：Hermes Agent 设计理念、更新日志
- 为什么值得看：了解 TUI 设计决策背后的原因
- 一句话评价：开发者亲自解释为什么这么设计
- 学到的东西：架构设计思路、未来规划

### 7.4 社区讨论

**Discord 社区**
- URL: Nous Research Discord（GitHub 主页有邀请链接）
- 适合人群：所有用户
- 内容概览：用户互助、开发讨论、功能反馈
- 为什么值得看：提问最快得到回答的地方
- 一句话评价：活跃的开发者社区
- 学到的东西：最佳实践、避坑经验

**Reddit r/LocalLLaMA**
- URL: https://reddit.com/r/LocalLLaMA
- 适合人群：关注开源 AI 生态的用户
- 内容概览：Hermes Agent 讨论、对比评测
- 为什么值得看：了解 Hermes 在开源社区中的定位
- 一句话评价：开源 AI 领域的风向标
- 学到的东西：行业对比、真实使用反馈

---

## 第8章：业内评价与案例分析

### 8.1 与同类工具的对比

| 工具 | 启动方式 | UI 技术栈 | 独特优势 | 不足 |
|------|---------|-----------|---------|------|
| Hermes TUI | `hermes --tui` | Ink (React) | 架构分离、皮肤系统丰富 | 需 Node.js |
| Claude Code | `claude` | 内置 TUI | Anthropic 官方支持 | 封闭生态 |
| OpenAI Codex CLI | `codex` | 内置 TUI | OpenAI 推理能力 | 需 OAuth |
| OpenClaw | `claw` | Python prompt_toolkit | 轻量、无 Node 依赖 | UI 功能有限 |

### 8.2 典型场景分析

**场景一：个人自动化系统**

一位开发者用 Hermes TUI + cron 构建了一套每日资讯推送系统：
- TUI 中配置定时任务（`/cron create`）
- 每天早上自动搜索关键词
- 抓取摘要并推送到微信
- 效果：每天节省 30 分钟人工浏览时间

**场景二：代码开发助手**

团队使用 Hermes TUI 作为日常开发辅助：
- 代码审查（`/background` 后台审查）
- 文档生成
- Git 操作辅助
- 效果：代码审查效率提升约 40%

### 8.3 性能表现

- 启动时间：约 1-2 秒（含 Python + Node 双进程初始化）
- 内存占用：约 80-150MB（取决于会话长度）
- 响应速度：与底层模型 API 延迟一致，TUI 本身不增加显著延迟

---

## 第9章：避坑指南

### 9.1 安装问题

**问题 1：`hermes --tui` 启动失败，提示 "Ink not available"**

- 现象：启动 TUI 时闪退
- 原因：`ui-tui/dist/` 未构建或 Node.js 不可用
- 修复：
  ```bash
  cd ~/.hermes/hermes-agent/ui-tui
  npm install
  npm run build
  ```

**问题 2：TUI 显示乱码**

- 现象：界面出现奇怪的字符
- 原因：终端编码问题或字体不支持 Unicode
- 修复：检查终端设置为 UTF-8，或使用支持 Nerd Font 的终端模拟器

**问题 3：热重载不生效**

- 现象：修改了 `ui-tui/src/` 下的代码但界面没有变化
- 原因：没有使用 `--dev` 模式，或 `npm run dev` 没有在运行
- 修复：
  ```bash
  # 终端1：启动开发服务器
  cd ~/.hermes/hermes-agent/ui-tui && npm run dev
  # 终端2：以开发模式启动 TUI
  hermes --tui --dev
  ```

### 9.2 运行问题

**问题 4：TUI 响应迟钝**

- 现象：输入延迟、界面卡顿
- 原因：模型 API 响应慢，或终端性能不足
- 修复：
  - 切换更快的模型（`/model`）
  - 减少 `max_turns` 配置
  - 使用轻量级皮肤（`/skin mono`）

**问题 5：斜杠命令不显示在自动补全中**

- 现象：输入 `/` 后看不到某些命令
- 原因：命令在 TypeScript 前端有定义但 Python 端 `COMMAND_REGISTRY` 缺失
- 修复：检查 `hermes_cli/commands.py` 中是否有对应的 `CommandDef`

**问题 6：上下文压缩后丢失信息**

- 现象：长对话被压缩后模型忘记之前的内容
- 原因：压缩阈值太低
- 修复：
  ```bash
  hermes config set compression.threshold 0.6
  hermes config set compression.target_ratio 0.3
  ```

**问题 7：后台任务没有通知**

- 现象：`/background` 提交后没有收到完成通知
- 原因：`background_process_notifications` 未开启
- 修复：
  ```bash
  hermes config set display.background_process_notifications all
  ```

**问题 8：会话自动恢复不生效**

- 现象：设置了 `tui_auto_resume_recent` 但启动时还是新会话
- 原因：没有最近会话，或会话已被清理
- 修复：
  ```bash
  # 检查是否有可恢复的会话
  hermes sessions list
  ```

### 9.3 配置问题

**问题 9：皮肤修改后不生效**

- 现象：修改了 `~/.hermes/skins/*.yaml` 但 `/skin` 切换后没变化
- 原因：YAML 格式错误或皮肤名称不匹配文件名
- 修复：检查 YAML 缩进，确保文件名是 `<name>.yaml` 格式

**问题 10：Dashboard 中的 TUI 白屏**

- 现象：`hermes dashboard` 能打开但 `/chat` 页面空白
- 原因：PTY bridge 依赖 POSIX PTY，原生 Windows 不支持
- 修复：在 WSL 或 macOS/Linux 上运行

---

## 第10章：进阶技巧与最佳实践

### 10.1 工作效率提升

**技巧 1：为常用任务创建别名**

```bash
# 以特定模型和技能启动 TUI
alias hermes-tui-pro='hermes --tui -m claude-sonnet-4 -s github-auth,hermes-agent'

# 恢复特定项目的会话
alias hermes-project='hermes --tui -c my-project'
```

**技巧 2：一键加载工作环境**

结合 `--skills` 和 `--model`，为不同任务预配置环境：

```bash
# 代码开发环境
hermes --tui -s github-auth -m deepseek-v4-flash

# 写作环境
hermes --tui -s humanizer -m claude-sonnet-4

# 研究环境
hermes --tui -s wiki-project-study,llm-wiki -m claude-sonnet-4
```

**技巧 3：5 分钟规则**

如果一个问题 5 分钟找不到答案，就用 TUI 创建一个后台任务：

```
/background 帮我研究一下 xxx 问题，把关键信息整理成要点
```

继续手头的工作，等通知就好。

### 10.2 工作流组织

**单任务模式**：一个会话只处理一件事，用 `/title` 命名，方便以后检索。

**分叉会话**：用 `/branch`（或 `/fork`）从当前会话分叉出一个新分支，适合「如果换个方向会怎样」的场景。

**会话清理**：定期用 `hermes sessions prune --older-than 30` 清理过期会话。

### 10.3 学习路线图

| 时间 | 目标 | 学习内容 |
|------|------|---------|
| Day 1 | 上手 | 启动 TUI，发送第一条消息，掌握 `/help` |
| Day 2-3 | 高效输入 | 掌握全部斜杠命令，配置 `display` 参数 |
| Day 4-5 | 个性化 | 创建自定义皮肤，调整状态指示器 |
| Week 2 | 自动化 | 配置 cron 任务，使用 `/background` |
| Week 3 | 工作流 | 多会话管理，技能组合，模型切换 |
| Week 4 | 深度定制 | 源码修改，自定义 Ink 组件开发 |

### 10.4 自我学习方法

1. **读源码**：`ui-tui/src/app/app.tsx` 是入口，看它怎么组织渲染
2. **看测试**：`ui-tui/src/__tests__/` 里有针对各组件的测试用例
3. **改配置**：调 `display.*` 参数理解每个的作用
4. **建皮肤**：从复刻一个内置皮肤开始

---

## 第11章：未来展望

### 11.1 TUI 与桌面应用的边界正在模糊

Hermes TUI 的架构（TypeScript 渲染 + Python 计算 + JSON-RPC 通信）本质上是一个「终端原生」的富客户端架构。这种架构有一个有趣的推论：**TUI 到桌面原生应用之间的转换成本极低。**

目前的 Dashboard 嵌入模式（通过 PTY bridge 把 TUI 代理到浏览器）是第一步。下一步很可能是：
- **Electron/Tauri 原生壳**：用 Electron 或 Tauri 包裹 Ink 渲染层，直接变成桌面应用，去掉 PTY bridge 这个中间层
- **多窗口支持**：Ink 本身是单终端渲染，但 JSON-RPC 可以支持多实例，一个会话用 TUI，另一个用 Dashboard，数据互通
- **WebSocket 远程连接**：把 JSON-RPC 从 stdio 换成 WebSocket，TUI 就可以远程连接到运行在服务器上的 Hermes 实例

### 11.2 AI 原生终端的进化方向

传统终端（bash、zsh）是「命令驱动」的——你输入什么它就执行什么。AI 终端是「意图驱动」的——你说你想做什么，它帮你完成。

Hermes TUI 在这方面做了一个关键设计决策：**TypeScript 只负责渲染，不负责 AI 逻辑。** 这意味：
- 后端可以独立升级 AI 能力（新模型、新工具、新推理方式）
- 前端可以独立升级 UX（新布局、新动画、新交互方式）
- 两端通过 JSON-RPC 协议松耦合

这种「渲染-计算分离」的架构，在未来可能会成为 AI 工具的标准模式。Claude Code 和 Codex 的 TUI 也在往这个方向走。

### 11.3 对开发者生态的影响

TUI 架构降低了「为 AI 工具做 UI 定制」的门槛。一个开发者不需要学复杂的 GUI 框架，只需要懂一点 React+Ink，就可以：
- 开发自定义工具面板
- 为特定工作流定制 UI 组件
- 创建行业专属的皮肤主题

这可能会催生一个类似 VSCode 扩展市场的「TUI 插件生态」——目前 Hermes 已经有技能（skills）系统和插件系统，未来 TUI 组件插件可能是自然延伸。

### 11.4 局限与风险

坦率地说，TUI 模式也有一些内在局限：

1. **终端能力上限**：无论如何优化，终端终究不是浏览器。复杂的图形、丰富的交互、高清渲染都需要借道 Dashboard/Web
2. **双进程复杂度**：Node + Python 双进程带来了额外的启动时间、内存开销和调试复杂度
3. **Node.js 依赖**：对于不想安装 Node.js 的用户来说，经典 REPL 是更轻量的选择

Hermes 团队保持了两种模式并存（经典 REPL + 现代 TUI），说明他们意识到了这个平衡。未来可能的方向是：用更轻量的 Rust/Go 替代 Node.js 作为渲染层。

### 11.5 预测

1. **6-12 个月内**：Hermes TUI 将支持可拖拽的侧边面板（类似 VSCode 的侧栏），用于显示工具结果、会话历史、文件树
2. **12-18 个月内**：TUI 组件将可以通过插件系统热加载，社区将出现 TUI 组件市场
3. **18-24 个月内**：渲染-计算分离架构将成为 AI 工具的标准模式，不止 Hermes 一家采用

---

## 附录：术语表

| 中文 | English | 使用场景 |
|------|---------|---------|
| 终端用户界面 | Terminal User Interface (TUI) | 在终端中运行的图形化用户界面 |
| Ink | Ink | React for Terminal，Hermes TUI 的渲染框架 |
| JSON-RPC | JSON-RPC | TUI 中 TypeScript 和 Python 的通信协议 |
| 斜杠命令 | Slash Command | 以 `/` 开头的命令，在 TUI 输入框中触发 |
| 会话 | Session | 一次完整的对话记录，可命名、恢复、删除 |
| 皮肤 | Skin | 控制 TUI 颜色、动画、文字风格的主题配置 |
| 状态指示器 | Status Indicator | TUI 顶部或状态栏显示的连接状态图标 |
| 紧凑模式 | Compact Mode | 减少界面空白的小屏幕优化模式 |
| 推理级别 | Reasoning Level | 控制模型展示思考过程的详细程度 |
| 后台任务 | Background Task | 用 `/background` 提交的异步执行任务 |
| 技能 | Skill | 可复用的工作流知识，保存在 `~/.hermes/skills/` |
| 工具集 | Toolset | 一组工具的集合，如 `web`、`terminal`、`browser` |
| 渲染-计算分离 | Rendering-Computation Separation | TUI 架构中 TypeScript 渲染 + Python 计算的模型 |
| 流式输出 | Streaming | 模型逐 token 输出结果，实时显示 |
| 上下文压缩 | Context Compression | 长对话时压缩历史以节省 token |
| 检查点 | Checkpoint | 文件系统状态快照，可通过 `/rollback` 恢复 |
| 双进程架构 | Dual-process Architecture | TUI 同时运行 Node.js 和 Python 两个进程 |
| PTY 桥接 | PTY Bridge | Dashboard 中通过伪终端连接 TUI 的技术 |
| 自动恢复 | Auto Resume | 启动时自动载入最近会话的功能 |
| 开发模式 | Dev Mode | `--dev` 标志，使用 TypeScript 源码而非构建产物 |

