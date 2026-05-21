---
title: Thinking Machines互动模型
created: 2026-05-20
updated: 2026-05-20
type: concept
tags: [thinking-machines, interaction-model, realtime-ai, mira-murati, harness]
sources:
  - youtube: 9Qc0Of4_BGA
  - output/极大/thinking-machines-interaction-model-report.md
confidence: high
---

# Thinking Machines互动模型

> **核心**: 全球首个原生实时交互AI模型，200ms微回合+时间感知First Citizen
> **公司**: Mira Murati创立，种子轮20亿(A16Z)，估值120亿
> **困境**: 6位联合创始人已走3位，发布主要为了安抚投资人

## 核心技术

| 特性 | 说明 |
|------|------|
| 200ms微回合 | 持续交错处理输入输出，不等待"用户说完" |
| 时间感知 | 时间作为First Citizen，可记忆30秒前对话准时提醒 |
| 双模型架构 | 互动模型(200ms) + 背景模型(搜索/工具调用) |
| 原生向量 | 所有输入输出直接编码，无外部STT/TTS管线 |

## 对你的价值

**Harness工程宿命论**：针对模型做harness，3-6个月后淘汰。正确方向是**模型无关的底层能力**。^[output/极大/thinking-machines-interaction-model-report.md]

## 关联概念
- [[ai-agent-token-economy]] — 成本结构决定做什么层面的能力
- [[world-model-comprehensive-analysis]] — 世界模型是底层能力的极致
