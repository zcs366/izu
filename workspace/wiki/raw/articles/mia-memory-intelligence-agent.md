---
title: "MIA：强化学习驱动的自进化记忆智能体"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/nmzirr1ddrKBfK6CegfkuQ"
author: "MindChain.AI"
date: 2026-04-16 (原发) / 2026-05-19 (摄入)
ingested: 2026-05-19
sha256: 5401fa9fd905c81622a4b97a380fc2185f5ff0129f3fb0e2bb96232c64a2a773
type: article
tags: [mia, memory-intelligence, rl, self-evolution, deep-research]
eval_level: 极大
---

# MIA：Memory Intelligence Agent

**论文**: https://arxiv.org/abs/2604.04503
**GitHub**: https://github.com/ECNU-SII/MIA

## 一句话
MIA结合参数记忆与非参数记忆，通过强化学习实现自进化，显著提升深度研究任务中的多步推理与工具交互能力。

## 背景问题
当前LLM记忆系统三方面关键局限：
1. 依赖长上下文存储，易噪声导致推理退化
2. 仅相似性检索历史轨迹，忽略质量与价值
3. 缺乏持续进化机制

## 方法：三模块架构
**Manager → Planner → Executor** 闭环

- **非参数记忆**（轨迹存储）+ **参数记忆**（模型内化）双向转换
- **交替强化学习（alternating RL）**：Planner与Executor协同优化
- **test-time learning**：Planner在推理过程中持续更新
- **反思 + 无监督评估**：开放环境下的自进化

## 实验结果
- 相比GPT-5.4：LiveVQA提升9%，HotpotQA提升6%
- Qwen2.5-VL-7B上平均提升31%，超过32B模型18%
- 无监督设置下提升约7%
- 超越现有memory-based agent方法约5%，SOTA

## 启示
Agent的核心不再是更大模型，而是可持续进化的 memory intelligence。
