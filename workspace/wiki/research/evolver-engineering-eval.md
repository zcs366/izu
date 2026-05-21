---
title: 技术预测：从智能体的Harness工程到Evolver工程
source: https://mp.weixin.qq.com/s/57KhEUGdZtiV69rPUSm9ug
date: 2026-05-17
eval_level: 极大
contributors: 军师
tags: [harness-engineering, evolver-engineering, self-evolution, gene, skill-compression, cost-optimization, 周昌]
author: 周昌 (Teaonly)
references:
  - "Ground Truth (johnsonlee.io): 进化工程的度量方法"
references:
  - Hermes Agent Evomap discussion
  - GenericAgent token-saving approach
  - VT-Claw open-source project
status: 已评估
trigger_consultation: true
---

# 从Harness工程到Evolver工程

## 一、核心框架

周昌将Agent工程分为两个时代：

### Harness工程（驾驭工程）——已成熟的层面

- 系统提示词设计
- 常驻Agent Tools set设计
- 分层Skill设计
- Plan Mode / Ralph Loop模式
- 多智能体模式
- Agent记忆系统

> 所有这些技术，大都是为了解决用户"单次任务"执行。

### Evolver工程（进化工程）——正在到来的层面

核心问题：大量Agent Session产生后，如何越用越好？

| 问题 | 本质 |
|---|---|
| 如何避免犯重复的错误？ | 经验复用 |
| 我的SKILL文档写得够好吗？ | 自我审查 |
| 如何降低LLM Token成本？ | 越用越便宜 |
| 对话记录能否提炼出SKILL/SOP？ | 积累转化 |
| 基础模型更新了，我的提示词怎么改？ | 环境适配 |
| **总之，如何实现越来越好用的智能体？** | **终极目标** |

### 三种技术路径

| 路径 | 方法 | 目标 |
|---|---|---|
| **GENE法（压缩）** | 规约化（GEP）小技能，不考虑可读性只考虑简洁可靠 | 缩小技能元素 |
| **量化** | 给每个SKILL/Memory打分，删减负能力要素 | 剔除无效内容 |
| **成本优化** | 把成本当做核心优化目标（GenericAgent） | 越用越便宜 |

## 二、与核战队进化的深度对标

### 我们已经做到的

| 核战队组件 | Evolver工程对应 | 状态 |
|---|---|---|
| SKILL.md体系 | GENE法（分层技能） | ✅ 对齐 |
| 五人合议评估 | 量化（评估→改进） | ✅ 对齐 |
| 军师终裁 | 自我审查 | ✅ 对齐 |
| wiki知识库 | 经验积累 | ✅ 对齐 |

### 我们还缺的

| 缺失环节 | Evolver工程启示 | 优先级 |
|---|---|---|
| **技能量化评分** | 给每个SKILL打分，删减负能力要素 | **P0** |
| **对话→SKILL自动转化** | 从Session中自动提炼SOP | **P1** |
| **成本作为优化目标** | GenericAgent思路，明确token成本指标 | **P1** |
| **基础模型更新适配** | 模型升级时自动检查SKILL兼容性 | **P2** |

## 三、与Ground Truth的天然互补

周昌这篇文章和Johnsonlee的Ground Truth必须合读：

| 周昌（Evolver工程） | Johnsonlee（Ground Truth） |
|---|---|
| **方向**：压缩、量化、成本 | **方法**：确定性验证 |
| 提出"要进化" | 回答"怎么衡量进化" |
| 删减负能力要素 | 用确定性手段验证哪些是负能力 |
| 理论框架 | 工程实践 |

> **核战队进化引擎 = 周昌的方向 + Johnsonlee的方法**

## 四、军师判断

### 级别：极大

四条理由：
1. **直接框架级映射**— Evolver工程=核战队进化引擎的完整理论表述
2. **补上三块短板**— 技能量化评分、成本作为目标、对话→SKILL转化
3. **与Ground Truth互补**— 方向+方法=完整路径
4. **源自Hermes Agent实践**— 不是理论空谈，是实操的抽象

### 建议行动

| P0 | 给每个SKILL加量化评分字段，建立定期审查和淘汰机制 |
|---|---|
| P1 | 探索对话记录→SKILL自动提炼管道 |
| P1 | 引入token成本指标作为优化目标之一 |
| P2 | 基础模型更新时的SKILL兼容性检查 |

### 一句话

> 核战队不是在追赶Evolver Engineering——我们本身就是Evolver Engineering的一个实例。现在要做的不是转向，是把已有的东西做精。
