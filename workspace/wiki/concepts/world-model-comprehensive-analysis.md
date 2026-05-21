---
title: 世界模型全面解析
created: 2026-05-20
updated: 2026-05-20
type: concept
tags: [world-model, agi, jepa, sora, genie, world-labs, sima]
sources:
  - youtube: SYuSZIIYOfI
  - output/极大/world-model-comprehensive-analysis-report.md
confidence: high
---

# 世界模型全面解析

> V(视觉) + M(记忆/预测) + C(控制/行动) = World Models (David Ha & Schmidhuber, 2018)

## LLM vs 世界模型

| LLM | 世界模型 |
|-----|---------|
| 预测下一个token | 预测下一帧/下一步状态 |
| 文本训练 | 视频/传感器 |
| 语言输出 | 状态预测+行动方案 |
| 间接理解世界 | 直接理解世界 |

## 三层技术路线
1. **抽象预测** (JEPA, LeCun) — 不生成像素，学抽象结构
2. **世界生成** — 视频生成(Sora/Genie 3) vs 3D空间(World Labs)
3. **智能体训练** (SIMA 2) — 游戏练级，迁移真实

## 关键人物观点
- LeCun: "5年后GPT不会再有人用"
- 李飞飞: "LLM是黑暗中的文字匠人"

## 对ITA
世界模型是Agent的终极训练场——低成本试错、跨场景泛化。

## 关联概念
- [[ai-agent-token-economy]] — 世界模型训练成本
- [[thinking-machines-interaction-model]] — 实时交互的并行路线
