---
title: LeCun：大模型只是"语言的假象" — World Models + JEPA
ingested: 2026-05-21
sha256: 587fb605905629967c8ec7c0d2e7ef750ff77c034e4b901ceb4633d7261154e3
created: 2026-05-18
updated: 2026-05-18
type: summary
tags: [AI/ML, paradigm, AGI]
source: https://youtu.be/40VyfW3IeHY
confidence: medium
---

# LeCun揭穿硅谷最大谎言

> wow频道 | 2026-05-17 | 1135 views
> 基于LeCun关于World Models + JEPA的长期主张

## 核心论点

- **LLM局限**：仅是高级"文字接龙"（next-token prediction），不懂真实物理世界
- **认知天花板**："水瓶翻倒"、"洗车悖论"——纯语言模型无法理解物理因果
- **解决方案**：**JEPA**（Joint-Embedding Predictive Architecture）— 学会"忽略视觉噪音"，在抽象表示空间做预测
- **表示坍塌（Representation Collapse）**：对比学习的经典问题→SIGReg（显式正则化）解决
- **AI主权**：闭源大模型垄断→开源+联邦学习的"织锦计划"

## 与ITA的连接

| LeCun立场 | ITA对应 |
|-----------|---------|
| JEPA：在抽象表示空间预测，而非在原始数据空间 | ITA：在compact encoding空间操控代码，而非在原始token空间 |
| 表示坍塌→SIGReg正则化 | FSQ量化器→无codebook collapse（Select FSQ的原因之一） |
| "忽略视觉噪音" | 编码器的语义抽象—提取语义而非保留完整文本 |
| World Models：理解物理世界因果 | ITA：理解代码的语义因果 |

## 与今日其他内容的连接

LeCun的"LLM不懂物理世界"与Karpathy的"可验证性决定AI能力锯齿"形成互补：
- Karpathy指出**在哪里AI能力强**（高可验证领域）
- LeCun指出**为什么纯语言在这条路上有天花板**（无物理/因果理解）
- ITA夹在中间→通过代码（高可验证+有精确语义边界）作为起点

## 级别判断

🔴 极大。但偏立场/范式辩论，非工程参考。与ITA有哲学共鸣。
