---
name: mcp-action-bridge
description: >
  动作型 MCP 桥接服务——让 AI Agent 通过 MCP 协议触发外部自动化工作流
  （Make webhook / n8n / 本地脚本）。注册于 config.yaml 的 mcp_servers 中。
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    category: mcp
    tags:
      - MCP
      - Action
      - Webhook
      - Automation
      - Make
      - Workflow
    related_skills:
      - native-mcp
---

# MCP Action Bridge — 动作型 MCP 桥接

> **一句话概括**：让 Agent 能触发外部工作流——发 webhook、跑本地脚本、调用 Make/n8n
> **触发词**：通过 MCP 工具调用，无需用户手动触发

## 1. 概述

传统的 MCP 连接是"数据型"的（搜索、读取文件、查询 GitHub）。动作型 MCP 让 Agent **触发**外部工作流——这是从"读到"到"做到"的关键一跃。

**能力矩阵**：

| 工具名 | 功能 | 典型场景 |
|--------|------|---------|
| trigger_webhook | 触发预注册的 webhook | 发布公众号、发送通知 |
| custom_webhook | 触发任意自定义 URL | 开发调试、临时调用 |
| run_script | 执行预注册的本地脚本 | 自动备份、生成日报 |
| list_hooks | 列出所有可用 hook/script | 了解当前配置 |

## 2. 配置

### 注册 Webhook

编辑 `/mnt/i/hermes/scripts/mcp-action-bridge.py` 中的 `WEBHOOKS` 字典。

### 注册脚本

编辑 `SCRIPTS` 字典。

### 重启生效

添加/修改后需重启 Hermes Agent。

## 3. 注意事项

1. **Webhook 是异步的**：trigger_webhook 立即返回 HTTP 状态码，不等待工作流完成。
2. **URL 和 token 保密**：WEBHOOKS 中的 URL 直接暴露在脚本中，生产环境建议用环境变量。
3. **预注册 vs 自定义**：预注册更简短，自定义更灵活。
4. **需要重启**：修改 WEBHOOKS 后需重启 Hermes。
