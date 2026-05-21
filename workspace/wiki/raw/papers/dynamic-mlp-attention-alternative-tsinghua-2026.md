---
title: WeightFormer — 清华黄高团队论文原文
created: 2026-05-18
updated: 2026-05-18
type: raw
tags: [AI/ML, paper, architecture]
source: https://arxiv.org/abs/2605.01711
confidence: high
---

# Linear-Time Global Visual Modeling without Explicit Attention

> **原始论文**: https://arxiv.org/abs/2605.01711
> **作者**: Ruize He, Dongchen Han, **Gao Huang** (清华大学)
> **日期**: 2026-05-03 (v1), 2026-05-06 (v2)
> **代码**: https://github.com/LeapLabTHU/WeightFormer

## 摘要

证明注意力可以在数学上重新表述为一个配备了**动态预测参数的多层感知器（MLP）**。全局建模能力不是显式token间聚合，而是隐式过程：动态生成的参数充当全局上下文的**压缩表示**。设计了多种动态参数预测策略，在视觉模型上验证有效性。

## 纠正（vs知乎解读）

- 知乎说"线性复杂度实现Transformer级别建模" → ✅ 准确
- "压缩表示"概念与ITA理念一致 ✅
- 实验限于视觉模型（cv.CV），非LLM。视频未提这个限制
