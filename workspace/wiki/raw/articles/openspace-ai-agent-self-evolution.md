---
source_url: https://mp.weixin.qq.com/s/rTNZ7O-IyPpmfCgLUKzkNw
sha256: c99be2307391118e5795942b35816a843034d44d5437245380ecb0f80b9cacc3
ingested: 2026-05-19
title: OpenSpace：AI Agent自进化引擎
author: 智能时代指南针
source: 微信公众号
eval_level: 大
tags: [OpenSpace, 自进化, Skill Engine, Agent框架]
---

# OpenSpace：AI Agent自进化引擎

核心定位：让AI Agent从"单次执行"变为"持续学习"。一个Agent学习，所有Agent升级。

## 三大核心能力
- Self-Evolution：技能自动修复、改进、学习
- Collective Intelligence：一个Agent学习→所有Agent升级
- Token Efficiency：复用成功方案，减少推理开销（46% Token节省）

## GDPVal基准
- 收入：$11,484（vs ClawWork $2,750）
- 价值捕获：72.8%（vs ClawWork 40.8%）
- Token节省：-45.9%

## 系统架构
五层：接入层（MCP/CLI/Dashboard）→ 编排层（tool_layer.py）→ 智能层（Skill Engine + Grounding Agent）→ 后端层（Grounding Client）→ 外部层

## Skill Engine：技能生命周期管理
DISCOVER → MATCH → APPLY → MONITOR → EVOLVE → STORE
