---
source_url: https://mp.weixin.qq.com/s/bDpc6sCwCY5oBXyTceITcA
sha256: 5f135b5a8935088329e37a690c4dfe8c69f162e511a7f6d6d1cb5a295bfc2ef7
ingested: 2026-05-21
title: "AI红队工具怎么选？6类18款对比"
author: AI安全工坊
source: 微信公众号
tags: [AI安全, 红队, 工具选型, LLM, Agent安全]
---

# AI红队工具怎么选？6类18款对比

AI红队选型决策矩阵 — 6类18款 + 5场景

## 核心观点

市面上AI红队工具分类混乱（OWASP、NIST、CSA、Gartner各家口径不同），本文自定义6大类、18款工具的选型对比。

## 为什么分类乱：4家权威分了4套

- **OWASP**：LLM Top 10 (2025) + GenAI Red Teaming Guide，4个测试维度
- **NIST**：AI 600-1 + ARIA体系，三层评估（模型测试→对抗性红队→实地测试）
- **CSA**：Agentic AI Red Teaming Guide (2025-05)，12类Agent威胁
- **Gartner**：AIUC + AIAC两大支柱，预测2026后由"合并平台"主导

## 6大类分类体系

| 类别 | 定位 |
|------|------|
| A 提示注入测试 | 漏洞类型层（OWASP LLM01） |
| B 越狱+综合红队 | 漏洞类型层（多漏洞综合扫） |
| C Agent/MCP安全 | 架构层（CSA 12威胁） |
| D LLM Gateway/Guardrail | 安全控制层（实时拦截） |
| E 可观测/Eval | 质量层（事后评估） |
| F 综合AI红队平台 | 工程层（一站式） |

### D vs E 关键区分

- **D类（消防员）**：实时干预流量，发现prompt injection直接拒绝
- **E类（验房师）**：事后评估，记录日志、token、回答质量供复盘

混用后果：以为langfuse能拦住攻击，结果它只能告诉你"刚才那条攻击成功了"。

## 18款工具按类对比

### A类：提示注入测试
- **microsoft/PyRIT** ★3,805 — 微软工业级，首选
- **cyberark/FuzzyAI** ★1,360 — 自动化LLM fuzzing
- **utkusen/promptmap** ★1,189 ⚠️维护减弱

### B类：越狱+综合红队
- **promptfoo/promptfoo** ★20,965 — 事实工业标准，首选
- **msoedov/agentic_security** ★1,864
- **confident-ai/deepteam** ★1,683

### C类：Agent/MCP安全
- **snyk/agent-scan** ★2,364 — 首选
- **splx-ai/agentic-radar** ★966 ⚠️维护减弱
- **slowmist/MCP-Security-Checklist** ★828 — spec类型，低频更新正常

### D类：LLM Gateway/Guardrail
- **BerriAI/LiteLLM** ★46,122 — 首选（注意CVE加固）
- **Portkey-AI/gateway** ★11,638
- **protectai/llm-guard** ★2,931 ⚠️维护减弱

### E类：可观测/Eval
- **langfuse/langfuse** — LLM可观测首选
- **explodinggradients/deepeval** — 评估框架
- **arize-ai/phoenix** — 可观测平台

### F类：综合AI红队平台
- 综合平台类工具，一站式覆盖

## 选型决策矩阵

文章提供5个典型场景对应推荐工具组合，可直接抄作业。
