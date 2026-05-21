---
title: "MCP安全"
type: "concept"
description: "围绕Anthropic提出的模型上下文协议（Model Context Protocol, MCP）的安全风险、攻击向量和防护机制。MCP是AI Agent连接外部工具的标准协议，其安全性直接影响AI Agent生态的安全边界。"
source: "系统"
tags: ["MCP", "协议安全", "AI Agent安全", "工具投毒", "攻击面分析"]
related_articles:
  - "mcp-a2a-agent-security-boundary"
  - "openai-anthropic-responses-api-agent-standard"
related_concepts:
  - "Agent安全"
  - "企业AI落地"
---

# MCP安全

## 概述
MCP（Model Context Protocol）是Anthropic提出的开放标准，为AI模型与外部工具之间建立安全、双向的连接。随着MCP成为AI Agent连接工具的事实标准，其安全问题日益受到关注。

## 已知安全缺陷

### 1. 工具投毒攻击（Tool Poisoning Attack - TPA）
2025年4月，安全公司Invariant Labs披露。攻击者在MCP工具描述中嵌入对用户不可见但对AI模型可见的恶意指令，操纵AI Agent执行未经授权的操作。

### 2. 地毯式骗局（Carpet Scam）
攻击者通过精心设计的工具返回结果，让AI Agent在无意识状态下泄露敏感信息。

### 3. 影子攻击（Shadow Attack）
利用MCP协议的开放性建立隐蔽通信通道，持续窃取用户数据。

## 攻击面
- MCP客户端（Cursor、Claude for Desktop等）
- MCP服务器端（权限管理、输入验证）
- 工具描述元数据注入
- 远程MCP服务器的供应链安全

## 防护建议
1. 仅从可信来源安装MCP工具
2. 限制MCP工具的访问权限（权限最小化）
3. AI Agent对工具描述和执行结果进行安全审查
4. 运行时监控AI Agent行为异常
5. 对AI Agent输出进行安全过滤
6. 建立MCP供应链安全评估机制

## 与A2A安全的关系
MCP安全与A2A安全构成了AI Agent安全的两大支柱：
- MCP：Agent⇔工具的安全
- A2A：Agent⇔Agent的安全

两者需要统一的跨协议安全框架。

## 关键文献
- [AI Agent破局：MCP与A2A定义安全新边界](../articles/mcp-a2a-agent-security-boundary.md)
- Invariant Labs: MCP Tool Poisoning Attack Disclosure (2025-04-06)
