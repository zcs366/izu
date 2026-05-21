---
title: Hermes Agent 工具系统架构
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [hermes, agent, tools, architecture]
sources:
  - raw/articles/hermes-agent-tool-system-zhineng-sibian.md
confidence: medium
---

# Hermes Agent 工具系统架构

[[Hermes Agent]] 的工具系统从注册到执行经历完整的四阶段链路：注册→发现→过滤→调用。本文梳理其工程实现。

## 四层概念区分

1. **Tool** — 单个可执行能力，如 read_file、terminal、web_search。模型可直接调用。
2. **Toolset** — tool 的分组，如 file、terminal、browser。模型不能直接调用 toolset，只能调用具体的 tool。
3. **Plugin** — 运行时扩展机制，可注册 tool、hook、context engine、memory 等外部扩展。
4. **Skill** — 给模型看的操作知识、SOP、上下文材料。skill_view/skill_manage 本身是可调用的 tool。

## 工具注册机制

所有普通工具最终调用 `registry.register()`，注册发生在模块 import 时——每个 tools/*.py 自己在文件底部注册。注册表只做三件事：
- 收集 schema 和 handler
- 按 check_fn 过滤（结果缓存避免重复检查）
- 调用 dispatch 执行 handler，异常统一包装为 JSON 错误

## model_tools.py 三轮发现

1. `_discover_tools()` — import 内置工具模块
2. `discover_mcp_tools()` — 发现 MCP server 工具
3. `discover_plugins()` — 发现用户目录/项目目录/pip entry point 的 plugin

import 是 best-effort 的：某个 optional 工具失败只记日志，不影响整体。

## Toolset 解析

`resolve_toolset(name)` 流程：all/* 展开所有 → 静态 toolset 从 TOOLSETS 字典读 → registry 查 plugin 注册的 toolset。plugin toolset 无需写进静态字典。

## 平台默认工具

不同入口默认工具不同：
- CLI → hermes-cli
- ACP → hermes-acp
- Gateway → 按平台选（hermes-telegram 等）
- API server → 排除 clarify/send_message

最终可见工具取决于：平台默认值 + 用户配置 + MCP server + plugin + check_fn。

## Tool Schema 四步生成

`get_tool_definitions()` 完整逻辑：
1. 决定"想要哪些工具名"（enabled/disabled/all）
2. registry 过滤（check_fn 缓存）
3. 动态 schema 修正（execute_code 只列可用工具、浏览器工具描述修正）
4. 记录最终工具名到 `_last_resolved_tool_names`

## 参见

- [[hermes-agent]] — Hermes Agent 主体
- [[agent-skills-system]] — Hermes Agent 技能系统
- [[hermes-security-model]] — Hermes Agent 安全模型
