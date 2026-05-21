---
title: "MCP Gateway"
aliases: [MCP网关, 中枢网关]
tags: [MCP, AI Agent, 架构, 网关]
---

# MCP Gateway

由小米架构师张平提出的MCP协议企业级生产化解决方案，旨在弥合MCP协议与企业级生产需求间的鸿沟。

## 三大核心设计
1. **协议融合**: MCP会话式/流式协议转换为RPC/HTTP标准请求
2. **生产级能力注入**: 可观测性三支柱 + 服务治理四要素
3. **智能路由**: 基于语义检索的自然语言工具发现

## 与相关概念的关系
- **MCP协议**: 标准化的工具/模型交互协议（下层基础）
- **Agent Infra**: MCP Gateway属于Agent Infra的核心组件
- **语义路由**: 通过向量嵌入实现智能工具路由

## 代表文章
- InfoQ《MCP Gateway：构建下一代AI Agent的"中枢网关"》
