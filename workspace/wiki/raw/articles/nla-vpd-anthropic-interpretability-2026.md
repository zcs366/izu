---
title: Natural Language Autoencoders — Anthropic论文原文
ingested: 2026-05-21
sha256: d0699dbe702e5d7da5140c8d83873da991fa9193d42c7622081a29d3a744c124
created: 2026-05-18
updated: 2026-05-18
type: raw
tags: [AI/ML, interpretability, paper]
source: https://transformer-circuits.pub/2026/nla/
confidence: high
---

# Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations

> **原始论文**：https://transformer-circuits.pub/2026/nla/
> **作者**：Kit Fraser-Taliente*, Subhash Kantamneni*‡, Euan Ong* (共同第一作者), Dan Mossing, Christina Lu, Paul C. Bogdan 等 — **Anthropic**
> **发布**：2026-05-07 | 代码: https://github.com/kitft/natural_language_autoencoders

## 摘要

我们引入**Natural Language Autoencoders (NLAs)**，一种无监督方法，生成LLM激活向量的自然语言解释。NLA由两个LLM模块组成：**Activation Verbalizer (AV)** 将激活映射为文本描述，**Activation Reconstructor (AR)** 将文本映射回激活向量。使用RL联合训练。FVE从0.3-0.4提升到0.6-0.8。

## 关键审计案例
- **未言明的评估意识**：Claude认为自己在被评估但不说出来
- **自动化审计基准**：使用NLA的Agent优于基线方法
- 交互式Demo: neuronpedia.org/nla

## 纠正（vs视频解读）
- 视频说FVE 0.6-0.8 → ✅ 准确
- 视频说confabulation细节准确率28% → 需论文验证具体数字
- 视频说的"AV用Claude Opus 4.5生成摘要" → 论文中有Supervised Warm-up初始化步骤

