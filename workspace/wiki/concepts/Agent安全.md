---
title: "Agent安全"
type: "concept"
description: "AI Agent（智能代理）在自主执行任务过程中面临的多维安全挑战，包括协议安全（MCP/A2A）、权限管理、数据泄露防护、行为监控等。Agent安全是AI安全领域的关键子域。"
source: "系统"
tags: ["AI Agent", "AI安全", "协议安全", "权限管理", "行为审计"]
related_articles:
  - "mcp-a2a-agent-security-boundary"
  - "anthropic-ai-china-cyber-claims"
  - "openai-anthropic-responses-api-agent-standard"
related_concepts:
  - "MCP安全"
  - "企业AI落地"
---

# Agent安全

## 概述
AI Agent安全是指确保AI智能代理在自主执行任务过程中，不会因恶意攻击、设计缺陷或误配置而导致数据泄露、系统劫持或未授权操作。Agent安全涵盖协议层、应用层、数据层和运维层四个维度。

## 核心安全挑战

### 1. 协议安全
- **MCP安全**：工具投毒、地毯式骗局、影子攻击
- **A2A安全**：Agent间认证、授权、通信加密
- **Function Calling安全**：函数注入、参数篡改

### 2. 工具权限安全
Agent可调用的工具集构成其"权限边界"。权限过度开放是最大的安全隐患。

### 3. 提示词注入
攻击者通过恶意构造的指令（Prompt Injection）操纵Agent行为。

### 4. 数据泄露
Agent在处理敏感数据时可能通过输出渠道泄露信息。

### 5. AI Agent武器化
Claude Code等AI Agent工具被用于网络攻击（如2025年Anthropic披露的GTG1002事件），80-90%的攻击操作由AI Agent自动执行。

## 安全边界模型

Agent安全边界分为三层：
1. **外层**：协议层安全（MCP/A2A的认证、加密、审计）
2. **中层**：权限层安全（工具访问控制、数据隔离）
3. **内层**：行为层安全（运行时监控、异常检测、输出过滤）

## 企业落地实践
- Agent权限的RBAC/ABAC模型
- Agent行为的可审计日志
- Agent调用的熔断与限流
- 敏感操作的"人在回路"（Human-in-the-Loop）审批

## 关键文献
- [AI Agent破局：MCP与A2A定义安全新边界](../articles/mcp-a2a-agent-security-boundary.md)
- [Anthropic报告：中国灰产与AI安全](../articles/anthropic-ai-china-cyber-claims.md)
