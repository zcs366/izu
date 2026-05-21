---
source_url: https://mp.weixin.qq.com/s/LdIZNotd2yPsaI7XdiN_CA
ingested: 2026-05-10
sha256: be4f5baf384b8cf86aa5810cfae6eeec877fb2171a17c1607192ebcca21f635d
source: 微信公众号
author: 智能思辨录
original_pub: 微信公众号
description: Hermes Agent Tool 深度梳理——从注册到执行的完整工程链路
---

# Hermes Agent Tool 深度梳理

本文面向理解 Hermes Agent 工具系统的读者，把一个 tool 从注册、暴露、执行的完整工程链路讲清楚。

## 整体流程

工具模块被 model_tools.py 导入。每个工具在 import 时向 tools.registry 注册 schema、handler、toolset、可用性检查。toolsets.py 决定哪些工具属于哪些分组。AIAgent 初始化时调用 get_tool_definitions()，按平台、配置、环境变量、check_fn 过滤出当前模型可见的工具 schema。模型只能从这批 schema 里发起 tool_call。run_agent.py 收到 tool_call 后，先判断并行还是串行，再分别路由到不同处理器。工具返回 JSON 字符串后，做展示、回调、超长结果持久化、目录规则懒加载、每轮结果预算控制。

## Tool / Toolset / Plugin / Skill 区别

1. **Tool**：单个可执行能力，如 read_file、terminal
2. **Toolset**：tool 的分组，如 file、terminal、browser
3. **Plugin**：运行时扩展机制，可注册 tool、hook、context engine、memory
4. **Skill**：给模型看的操作知识、SOP、上下文材料

## 工具注册机制

所有工具最终调用 `registry.register()`，注册发生在模块 import 时——每个 tools/*.py 自己在文件底部注册。注册表只做三件事：收集 schema 和 handler、按 check_fn 过滤、调用 dispatch 执行。

## model_tools.py 发现流程

三轮发现：_discover_tools() import 内置工具模块 → discover_mcp_tools() 发现 MCP server 工具 → discover_plugins() 发现插件工具。import 是 best-effort，某个工具失败不影响整体。

## Toolset 解析

由 resolve_toolset(name) 完成：all/* 展开所有 → 静态 toolset 从 TOOLSETS 读 → 查 registry plugin 注册的 toolset。

## 平台默认工具

不同入口默认工具不同：CLI → hermes-cli，ACP → hermes-acp，Gateway 按平台选，API server 排除 clarify/send_message。最终可见工具取决于：平台默认值 + 用户配置 + MCP server + plugin + check_fn。

## Tool Schema 生成四步

1. 决定"想要哪些工具名"
2. registry 过滤（check_fn 缓存）
3. 动态 schema 修正
4. 记录最终工具名到 _last_resolved_tool_names
