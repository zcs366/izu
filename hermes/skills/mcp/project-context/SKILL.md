---
name: project-context
description: >
  项目上下文自动加载——进哪个项目目录就自动加载哪个项目的 _context.md / AGENTS.md / CLAUDE.md。
  类似 Claude Code 的 CLAUDE.md 自动读取机制。注册于 config.yaml 的 mcp_servers 中。
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    category: mcp
    tags:
      - MCP
      - Context
      - Project
      - Workspace
      - Auto-Load
    related_skills:
      - native-mcp
      - mcp-action-bridge
---

# Project Context — 项目上下文自动加载

> **一句话概括**：进哪个项目目录，就自动加载哪个项目的上下文——不再靠 memory 和全局 prompt 硬扛所有项目
> **触发词**：通过 MCP 工具调用，建议在会话启动时自动调用 `get_context`

## 1. 概述

**问题**：当前 Hermes 每次会话都从 memory 和全局 prompt 中获取上下文。如果同时维护多个项目（izu、Hermes Agent、佉馘博客等），会出现"上下文污染"——izu 的规则干扰 Hermes Agent 的工作，反之亦然。

**方案**：项目级 _context.md 文件 + MCP 服务自动检测。

**搜索顺序**（从当前目录逐级向上搜索 5 层）：

```
_context.md → AGENTS.md → CLAUDE.md → .cursorrules → _workspace.md
```

**就近原则**：找到的第一个文件即为项目上下文。上层目录的 context 文件不会覆盖下层。

## 2. 可用工具

| 工具 | 功能 | 典型场景 |
|------|------|---------|
| `get_context` | 检测 cwd 及父目录的 context 文件，返回合并上下文 | 会话启动时调用 |
| `init_context` | 在当前项目目录创建 _context.md | 新项目初始化 |
| `list_projects` | 列出所有已有 context 文件的项目 | 项目管理 |

## 3. 使用方式

### 新项目初始化

```
调用 init_context:
  cwd: /path/to/project
  description: 项目描述
  rules: 项目关键约定
```

### 会话启动时获取上下文

```
调用 get_context:
  cwd: /mnt/i/hermes   # 或当前工作目录
```

如果检测到 _context.md，其内容会自动作为项目上下文注入。

## 4. _context.md 模板

```markdown
# 项目名 — 项目上下文

> 创建于：YYYY-MM-DD

## 项目描述
一句话说明

## 关键约定
1. 规则1
2. 规则2

## 目录结构
```


## 5. 注意事项

1. **文件命名统一**：全部用 `_context.md`（前缀下划线，不干扰其他工具）
2. **就近优先**：子目录的 _context.md 优先于父目录
3. **每层只取一个**：同层目录按 `_context.md → AGENTS.md → CLAUDE.md → .cursorrules → _workspace.md` 优先级取
4. **最大 5 层**：向上搜索不超过 5 层目录
5. **单文件 2K**：context 文件内容限 2000 字符
