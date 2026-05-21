---
title: 近一年Agent自进化的两大方向和四大趋势——年度综述
source: https://zhuanlan.zhihu.com/p/2022259769969255910
date: 2026-05-17
eval_level: 大
contributors: 军师
tags: [self-evolution, survey, agent-learning, skill-accumulation, rl-training, safety]
author: 硅基捕手维克托 (知乎)
references:
  - "周昌: Evolver Engineering"
  - "Agent记忆全景综述 (arxiv:2602.06052)"
  - "MemMA: 多智能体记忆自进化"
  - "CASCADE, STELLA, AutoSkill, MetaClaw, SWE-RL等"
status: 已评估
---

# Agent自进化年度综述 — 评估

## 一、框架：两条主线

| 路线 | 方法 | 代表 | 核战队对齐 |
|---|---|---|---|
| **经验与技能积累**（不改模型） | 失败→提炼技能→复用 | CASCADE, STELLA, AutoSkill, SkillWeaver, EvoSkill | ✅ 直接对齐 |
| **RL训练**（改模型权重） | 奖励信号→参数更新 | EvolveR, OpenClaw-RL, MetaClaw, SWE-RL | ❌ 未涉足 |

## 二、哪些论文直接映射核战队

### 已对齐（我们已经做了类似的事）

| 论文 | 核战队对应 | 对齐度 |
|---|---|---|
| **AutoSkill** — 识别重复模式→抽象为技能→评估→精炼/废弃 | SKILL.md体系+定期审查 | ★★★★★ |
| **SkillWeaver** — Agent自己写API（工具调用=调API，SkillWeaver=写API） | SKILL.md的自创建 | ★★★★★ |
| **EvoSkill** — 分析失败轨迹触发新技能生成 | 军师终裁+评估回馈 | ★★★★ |
| **CASCADE** — 两个元技能（持续学习+自我反思） | 核战队进化引擎概念 | ★★★★ |

### 待改进（有差距但方向一致）

| 论文 | 差距 | 优先级 |
|---|---|---|
| **STELLA** — 独立的Tool Creation Agent自动发现并集成新工具 | 我们没有自动化工具发现机制 | P2 |
| **MemSkill** — 记忆管理本身作为可进化技能 | 记忆管理链路为空 | P1 |
| **Skill全生命周期** — AutoSkill强调"只增不减的技能库迟早变负担" | 我们就是只增不减 | P1 |

### 未涉足（需要时再研究）

| 方向 | 代表 | 为什么没碰 |
|---|---|---|
| **RL训练改模型权重** | MetaClaw, SWE-RL, EvolveR | 需要GPU+大量数据，超出当前范围 |
| **零数据自学习** | Absolute Zero, Tool-R0 | 学术探索，非工程需求 |
| **多智能体协同进化** | Self-Challenging, SiriuS | 与核战体重叠但有不同 |

## 三、五大趋势 × 核战队

| 趋势 | 核战队状态 | 行动 |
|---|---|---|
| **零标注数据** | ✅ 我们在做（自动化评估） | 持续推进 |
| **过程奖励>结果奖励** | ⚠️ 有评估但不够细粒度 | 可改进 |
| **奖励模型要一起进化** | ❌ 无奖励模型 | 暂无需求 |
| **安全是新问题** | ⚠️ Misevolution警示 | P2关注 |
| **Agent不应静止** | ✅ 核战队核心信念 | 保持 |

## 四、最大收获——一张地图

这篇文章最大的价值不是任何单个发现，而是**把零散碎片拼成了一张地图**。

我们今天看的所有文章，在这张图里各自有位置：

| 文章 | 在地图上的位置 |
|---|---|
| **周昌Evolver工程** | 理论框架层 |
| **Agent=Model+Harness** | 系统架构层 |
| **Agent记忆综述** | 记忆子系统 |
| **Ground Truth** | 验证子系统 |
| **Prompt Caching** | 成本优化层 |
| **MemMA** | 记忆进化实现案例 |
| **本综述** | 全景地图 |

### 军师判断

**今天这轮"开干"的全部产出，可以画成一条完整的逻辑链：**

> **Evolver理论** → **Harness架构7层**（含执行钩子） → **记忆全景3维框架** → **Ground Truth验证方法** → **Prompt Caching成本约束** → **年度综述全局验证方向正确**

这不是偶然——这是核战队进化引擎的理论根基在一天之内从零散碎片变成完整体系的过程。

**建议下一步**：把这张图固化到wiki knowledge graph中，作为核战队的顶层认知地图。
