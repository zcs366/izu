---
source_url: https://mp.weixin.qq.com/s/0RDWrRPY1PKzltBIkFxNJg
ingested: 2026-05-19
sha256: pending
title: LASM：Agent 安全的七层攻击面
author: 模安局
source: arXiv:2604.23338
---

# LASM 核心笔记

**论文**：LASM系统综述（2021.01-2025.04，94篇核心论文）

## 七层攻击面

L1 基础模型层 — jailbreak/对抗/后门/数据污染
L2 认知层 — 规划/推理被带歪
L3 记忆层 — 最危险也最被低估
L4 工具执行层 — 最危险层，信任倒置
L5 多Agent协同层 — 单点→网络风险
L6 生态与供应链层 — MCP server/插件/依赖
L7 治理层 — 日志/归因/审计

## 四类攻击时间性

T1 即时 → T2 单会话持久 → T3 跨会话累积 → T4 时间边界打散

## 核心结论

研究集中在L1/L2和T1/T2；高层、慢变量、跨会话风险研究远远不够。

## ABOM（Agent Bill of Materials）

记录：模型版本、工具权限、系统提示、外部服务、记忆来源
