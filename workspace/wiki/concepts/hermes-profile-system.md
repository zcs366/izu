---
title: Hermes Agent Profile 系统
created: 2026-05-07
updated: 2026-05-10
type: concept
tags: [agent, configuration, workflow]
sources: 
  - raw/articles/hermes-agent-profile-guide-muse.md
  - raw/articles/hermes-profiles-codex-practice.md
  - raw/articles/hermes-profiles-shengjie-guide.md
confidence: high
---

# Hermes Agent Profile 系统

[[Hermes Agent]] 的多实例管理机制。每个 profile 是一个独立的 Hermes home 目录，拥有自己的配置、记忆、会话、技能、环境变量、定时任务和状态数据。

## 核心命令

```bash
hermes profile create <name>          # 创建（空配置）
hermes profile create <name> --clone  # 从 default 克隆配置创建
hermes profile list                   # 列出（* 标记默认）
hermes profile show <name>            # 查看详细配置
hermes profile use <name>             # 设默认
hermes -p <name> chat                 # 以指定 profile 运行
hermes profile export <name>          # 导出备份为 tar.gz
hermes profile import <file.tar.gz>   # 导入恢复
hermes profile rename <old> <new>     # 重命名，同步更新别名
hermes profile delete <name> --yes    # 删除
```

创建后自动生成包装脚本 `~/.local/bin/<name>`，可直接运行如 `<name> chat`。

## 每个 Profile 独立拥有的资源

- config.yaml / .env / SOUL.md
- memories/MEMORY.md + memories/USER.md
- skills/ / sessions/ / cron jobs / state database

## 三文件分工

| 文件 | 职责 | 维护者 |
|---|---|---|
| [[soulmd-core-identity\|SOUL.md]] | Agent 是谁：身份、人格、语气、工作风格 | 你（新会话生效） |
| MEMORY.md | 你告诉 Agent 的长期事实、环境、经验 | 你 + Agent |
| USER.md | Agent 对你使用习惯的自动推断画像 | Agent 自动维护 |

## 注意事项

- **非文件系统沙箱**：不同 profile 仍有同一系统用户的文件权限，真正隔离需 Docker/SSH/Modal
- **Profile ≠ 工作目录**：需单独配置 `terminal.cwd`
- **修改 SOUL.md 后需新开会话**：影响 system prompt，缓存不实时刷新

## 推荐的多 Profile 方案

| Profile | 使命 | 推荐模型 |
|---|---|---|
| default | 通用日常 | 性价比模型 |
| coder | 写代码/改 Bug/重构 | 编程强模型 |
| researcher | 搜资料/竞品分析 | 推理强模型 |
| tester | 写/跑测试 | 严谨模型 |
| docs | 文档编写 | 中文强模型 |
| ops | 服务器/定时任务 | 轻量模型 |

## 相关条目

- [[Hermes Agent]]
- [[soulmd-core-identity]]
- [[hermes-agent-memory-system]]

## 实战：双 Profile 分工（coder + assistant）

[[蝈蝈的AI笔记]] 提供了完整的双 Profile 搭建实战指南：一个 `coder` Profile 调度本地 CodeX 写代码，一个 `assistant`（默认）负责日报与知识库。^[raw/articles/hermes-profiles-codex-practice.md]

### 核心架构

```
coder (Hermes Profile)      assistant (Hermes Profile)
    │                            │
    │ 调度+审查                    │ 日报/知识库/日常
    │                            │
    ▼
CodeX / Claude Code
    │
    ▼
    实际编码执行
```

关键设计原则：**Hermes 不自己写代码**——CodeX 已积累大量专业 coding skill，Hermes 只需做"需求翻译"和"结果审查"，各取所长。

### 快速搭建

```bash
# 方式一：创建空 Profile（需从头配置）
hermes profile create coder

# 方式二：从 default 克隆（推荐，继承已有配置和模型设置）
hermes profile create coder --clone
hermes profile create writer --clone
```

创建后自动生成命令别名 `~/.local/bin/coder`，可直接运行 `coder chat`。

### 为 Profile 分配独立模型

建议将不同 Profile 的默认模型区分开——编码和写作对模型的要求不同。coder 更吃推理和工具调用，writer 更看重表达和结构。

```bash
coder model                              # 交互式选择模型
coder config set model.default gpt-5.4   # 或直接写入配置
```

### SOUL.md 示例

```markdown
# 身份
你是一位代码任务调度专家。你自己不直接编写代码，
而是通过调用 CodeX 或 Claude Code 来完成所有编码工作。

# 工作方式
- 收到需求时，先分析任务类型和复杂度
- 将任务清晰描述后，委派给 CodeX 或 Claude Code 执行
- 审查返回的代码质量，必要时要求修改
- 向用户汇报结果，而不是自己动手写

# 避免
- 自己生成大段代码
- 不加审查地直接转发工具返回结果
```

**注意区分：** SOUL.md 管"这个 Agent 是谁"；项目根目录的 AGENTS.md 管"在这个项目里做什么"。

### 连通本地 CodeX

1. 在 ChatGPT 配置中开启 CodeX 设备访问权限（"安全"设置）
2. coder Profile 向本地 CodeX 发起连接——自动获取验证码和 OpenAI 配对链接
3. 配对成功后，coder 会执行 `codex login status` → `codex exec resume` 的完整调度链路
4. Hermes 全程不生成代码，只做调度和验证

### 管理命令速查

```bash
hermes profile list              # 查看所有 Profile 状态
hermes profile show coder        # 查看 coder 详细配置
hermes profile export coder      # 导出备份为 coder.tar.gz
hermes profile rename coder dev  # 重命名，同步更新别名和服务
hermes update                    # 更新代码并同步所有 Profile 的内置技能
```

### 何时需要第三个 Profile（orchestrator）

两个 Profile 并行独立（互不知晓对方存在）在大多数场景下已够用。**只有当需要多 Profile 按顺序协作**（如 coder 完成代码后自动触发 assistant 生成文档）时，才需要 orchestrator Profile 来统筹调度。

建议：**不要过度设计**——等真正感受到"需要有人协调它俩"的那一天再加。^[raw/articles/hermes-profiles-codex-practice.md]

### 按角色分配 Skills

SOUL 管"怎么想"，Skills 管"会什么"。建议将技能库也按 Profile 分离。^[raw/articles/hermes-profiles-shengjie-guide.md]

**coder 常用技能：** frontend-design（页面/组件设计）、superpowers（工程能力强化）、git-commit（Conventional Commits）、github-issue、vercel-react-best-practices、dotnet-best-practices

```bash
coder skills search frontend-design
coder skills install frontend-design --yes
```

**writer 常用技能：** frontend-slides（课件 slides）、pretty-mermaid（Mermaid SVG 渲染）、humanizer-zh（去 AI 味）、baoyu-post-to-wechat（公众号发布）

### Gateway 与 Dashboard 隔离

每个 Profile 有独立 Gateway 状态与配置。可让 coder 对接飞书机器人、writer 对接微信，互不干扰。^[raw/articles/hermes-profiles-shengjie-guide.md]

**Dashboard 端口冲突：** 默认 9119 对应 default Profile。同时多开需错开端口：

```bash
coder dashboard --port 9120
writer dashboard --port 9121
```

### Profile vs Session vs Skill 决策

| 维度 | 用途 | 隔离范围 |
|------|------|---------|
| Session | 临时切换任务/话题 | 无（同一身份内） |
| **Profile** | **长期隔离的身份/模型/工具/记忆** | **全套配置 + 数据** |
| Skill | 复用流程/模板/套路 | 单一能力单元 |

- 临时换任务 → session（/new、/branch、/resume）
- 需要长期隔离的身份/模型/记忆 → Profile
- 需要复用的流程/模板 → Skill ^[raw/articles/hermes-profiles-shengjie-guide.md]
