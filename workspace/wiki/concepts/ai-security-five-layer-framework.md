---
title: AI 安全五层结构
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [ai, security, framework, architecture]
sources:
  - raw/articles/ai-anquan-gongfang-kb-v1.2.md
confidence: medium
---

# AI 安全五层结构

[[AI 安全工坊]] 提出的 AI 安全分层框架，将 AI 系统安全从"模型输出"扩展到"系统行为"，覆盖从模型层到组织治理层的五层结构。

## 五层结构

### 第一层：模型层
越狱（Jailbreak）、幻觉（Hallucination）、对齐（Alignment）、欺骗（Deception）、能力隐藏（Capability Hiding）、推理链可监控性、模型记忆、训练数据泄露。

### 第二层：应用层
Prompt Injection、RAG 污染、Insecure Output Handling、Function Calling 滥用、LLM-mediated SSRF / SQLi / XSS、用户确认边界。

### 第三层：Agent 和协议层
MCP 安全、A2A 安全、Tool Poisoning、跨 server 工具影子、STDIO 本地子进程风险、OAuth Resource Indicator、token audience、marketplace 供应链。

### 第四层：工程和供应链层
数据摄取安全、评估集污染检测、模型注册表安全、AIBOM / ML-BOM、模型签名与溯源、依赖包投毒、HuggingFace 模型审计。

### 第五层：组织和治理层
红队评估、蓝队监控、事件响应、隐私合规、EU AI Act、中国 AI 备案、NIST AI RMF、ISO/IEC 42001、行业垂直风险。

## 核心洞察

这些层不是互相独立的。一次真实 AI 安全事故往往会跨越好几层。关键事故链举例：

> 恶意网页污染 RAG 内容 → 诱导 Agent 调用工具 → 工具读取敏感文件 → 模型把内容总结进外部工单 → 日志里只留下"用户请求已完成"

## 与 Hermes 安全模型的关联

[[hermes-security-model]] 的 7 层纵深防御与该框架高度对应，尤其在第三层（Agent 和协议层）和第五层（组织治理层）有直接映射。

## 应用场景

- **安全研究员** — 从第三层（Agent 安全）切入
- **红队工程师** — 从第一到三层串联攻击链
- **蓝队/SOC** — 从第三到五层构建检测体系
- **AI 工程师** — 从第二到四层排查工程风险
- **合规治理** — 从第五层入手建立制度

## 参见

- [[ai-security-workshop]] — AI 安全工坊与知识库
- [[hermes-security-model]] — Hermes Agent 7 层纵深防御
- [[agent-web-capability]] — Agent 互联网能力与安全
