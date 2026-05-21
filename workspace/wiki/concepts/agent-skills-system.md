---
title: Agent Skills System
created: 2026-05-06
updated: 2026-05-10
type: concept
tags: [agent, tool, training]
sources:
  - raw/articles/hermes-agent-docs-overview-2026-05-06.md
  - raw/articles/hermes-agent-deep-dive-series-agent-observer.md
  - raw/articles/hermes-comfyui-skill-wechat.md
  - raw/articles/hermes-agent-self-evolution-yiqi.md
  - raw/articles/hermes-agent-intro-kim-surely.md
  - raw/articles/hermes-agent-89-builtin-skills-overview.md
  - raw/articles/hermes-hub-skill-marketplace.md
confidence: high
---

# Agent Skills System

技能系统是 [[Hermes Agent]] 的核心功能之一，代表其程序性记忆。Agent 能够从经验中自主创建技能，在使用过程中自我改进，并通过 Skills Hub 共享社区贡献的技能。

## 核心机制

- **自主技能创建** — Agent 根据经验自动生成新技能
- **技能自我改进** — 使用过程中不断优化已有技能
- **开放标准** — 兼容 agentskills.io 标准格式
- **技能可移植性** — 技能可在不同 Agent 实例间共享

## GEPA 自进化闭环

技能系统的核心驱动力是 **GEPA Loop**（Generate → Evaluate → Persist → Adapt）：

1. **Generate** — Agent 在复杂任务完成后被触发，生成新技能的候选方案
2. **Evaluate** — 后台独立审查 Agent 评估技能质量、安全性和可复用性
3. **Persist** — 通过 `skill_manage` 工具写入 `~/.hermes/skills/`，成为持久化技能
4. **Adapt** — 后续对话中自动加载和适配，并可根据使用反馈继续优化

GEPA Loop 是 Hermes 区别于普通 Agent 助手的关键——它不是"装插件"，而是**让 Agent 自己长出技能**。^[raw/articles/hermes-agent-89-builtin-skills-overview.md]

## 技能自动生成与后台复盘

复杂任务完成后，Hermes 会启动一个后台独立审查 Agent（`_spawn_background_review()`），自动复盘整个过程：

- 哪些步骤走错了？后来怎么修正的？
- 有没有可复用的模式？
- 这套流程能否固化为一个标准操作？

审查通过后，经验自动打包成 SKILL.md 技能文件，存放在 `~/.hermes/skills/` 目录。下次遇到类似任务，Agent 可直接调用该技能，实现"用完即复用"，Token 消耗也大幅降低。

这是一种**即时生效**的进化路径——与离线 RL 训练的深层优化互补，详见 [[hermes-self-evolution]]。

## 创建触发机制

- `_skill_nudge_interval = 10`：每 10 轮对话触发一次技能审查 nudge
- `_spawn_background_review()`：命中条件后 fork 一个轻量 review Agent，在响应完成后**异步非阻塞写入**
- 注入 `_SKILL_REVIEW_PROMPT` 进行创建评估

## SKILL.md 文件格式

每个 Skill 是一个文件夹，包含 YAML 前置元数据 + Markdown 正文。Agent 通过 `skills_list` / `skill_view` / `skill_manage` 三件套进行分级管理（列表 → 元数据 → 完整内容 → 创建/更新/删除）。

## 四层信任等级

| 等级 | 策略字段 | 说明 |
|---|---|---|
| builtin | INSTALL_POLICY | 内置技能，不可删除 |
| trusted | INSTALL_POLICY | 用户信任的技能 |
| community | INSTALL_POLICY | 来自社区市场（agentskills.io） |
| agent-created | INSTALL_POLICY | Agent 自主创建的技能，最高风险 |

配合安全扫描：120 条威胁正则（12 大类）+ 不可见 Unicode 检测 + safe/caution/dangerous 三级裁决。

## 与记忆系统的关系

技能系统属于程序性记忆（know-how），与 [[Memory System]]（事实性记忆和用户建模）互补。两者共同构成 [[Hermes Agent]] 的闭环学习回路。

## Skills Hub

2026 年 5 月 6 日，Nous Research 正式上线 **HermesHub** 技能市场（[GitHub](https://github.com/amanning3390/hermeshub)），聚合 **647 个社区技能**（4 个注册源），加上 **89 个官方内置技能**，可在 Skills Hub 中搜索、浏览、安装、分享。^[raw/articles/hermes-agent-89-builtin-skills-overview.md]^[raw/articles/hermes-hub-skill-marketplace.md]

**与 OpenClaw 的格式兼容：** Hermes 的 SKILL.md 格式与 OpenClaw 几乎一致，两套系统可互相安装——HermesHub 上的技能可直接装到 OpenClaw 中使用，反之亦然。技能生态正在形成合力。^[raw/articles/hermes-hub-skill-marketplace.md]

### 18 大技能分类概览

官方内置技能覆盖以下领域（按类别分组）：

| 类别 | 核心技能示例 |
|------|-------------|
| Apple 生态 | apple-notes, apple-reminders, findmy, imessage |
| Creative 创作 | comfyui, manim-video, baoyu-comic, baoyu-infographic, excalidraw, p5js, ascii-art, humanizer, claude-design, sketch |
| DevOps & Kanban | kanban-orchestrator, kanban-worker, webhook-subscriptions |
| GitHub 自动化 | github-pr-workflow, github-code-review, github-issues, github-repo-management, codebase-inspection |
| MLOps / AI 工程 | 微调（Axolotl/Unsloth/TRL）、推理（vLLM/Ollama/llama.cpp）、评估（lm-eval-harness）、实验追踪（W&B） |
| Productivity | Notion, Linear, Google Workspace, arXiv, Blogwatcher, Email/Himalaya |
| Research | bing-search, arxiv, blogwatcher, wiki-project-study |
| Gaming | minecraft-modpack-server, pokemon-player |
| Media | gif-search, spotify, songsee |
| MCP | native-mcp |
| 其他 | dogfood (QA)、data-science、note-taking、parenting、wife-business、yuanbao |

每个 Skill 都是带 YAML frontmatter 的 Markdown runbook，支持 **progressive disclosure**（按需加载省 token），能被 Agent 自动改进、记忆、组合。

## 技能管理：hermes skills 命令全家桶

用户通过 `hermes skills` 命令进行完整技能生命周期管理：

| 命令 | 功能 |
|------|------|
| `list` | 列出已安装技能（轻量摘要） |
| `search` | 在 Skills Hub + 注册表中全文搜索 |
| `browse` | 分页交互式 TUI 浏览器 |
| `install` | 安装技能（official/社区ID/URL） |
| `inspect` | 预览技能完整内容（无需安装） |
| `config` | 交互式配置面板（启用/禁用/权限/参数） |
| `check` | 检查 Hub 技能是否有更新 |
| `update` | 一键更新所有 Hub 技能 |
| `audit` | 扫描验证技能完整性与安全 |
| `uninstall` | 卸载 Hub 技能 |
| `reset` | 恢复被修改的内置技能为官方默认 |
| `publish` | 发布本地技能到 Skills Hub |
| `tap` | 管理自定义技能源（私有仓库） |

### 聊天界面快捷调用

在 `hermes chat` 或任何消息平台直接输入：
- `/skills` — 直接唤起技能管理 TUI
- `/skill-name` — 直接调用已安装技能（如 `/comfyui`、`/baoyu-comic`）

所有已安装技能自动注册为 slash 命令，零学习成本调用。^[raw/articles/hermes-agent-89-builtin-skills-overview.md]

## 示例：ComfyUI Skill

[[comfyui-skill]] 是一个典型的多媒体生成 Skill，封装了 [[ComfyUI]] 的完整交互链路（生命周期管理、API 调用、工作流参数映射、多实例路由）。详见 `raw/articles/hermes-comfyui-skill-wechat.md`。
