---
title: Ground Truth：AI时代最被低估的竞争力
source: https://mp.weixin.qq.com/s/N1IPbmN50gj8tGUyR3HpqQ
date: 2026-05-17
eval_level: 大
contributors: 军师
tags: [ground-truth, verification, harness-engineering, deterministic-validation, agent-pipeline]
author: johnsonlee.io
references:
  - "Harness Engineering系列: 从LLM到高效沟通, RAG既死什么才是Ground Truth"
status: 已评估
---

# Ground Truth：AI时代最被低估的竞争力

## 一、核心论点

> **没有Ground Truth，你连"错了"都不知道。**

LLM是概率性的，这不是缺点，是本质。它不保证正确，只保证"像正确"。

大多数团队的兜底手段有一个共同特征：**都在用人脑当ground truth**。人工review、人工判断PR质量、人工抽查通过率——这不scale，跟没用AI之前的效率瓶颈是同一个瓶颈。

## 二、关键洞察

### 1. Ground Truth必须是确定性的

> 用概率性的工具去验证概率性的输出，等于没验证。

作者用AB实验清理Agent举例：基于SootUp的字节码静态分析工具Graphite，先跑出call graph。哪个方法调用了实验API、哪些分支依赖实验状态——全是确定性的结果。

**分工：**
- 确定性工具做**发现**（call graph、静态分析）
- LLM做**解释**（这个逻辑该保留还是移除？commit message怎么写？）

这不是偏好，是**工程约束**。

### 2. 护城河不在Prompt，在验证

> 大多数人在优化prompt，少数人在优化验证。后者才是真正的杠杆。

有ground truth就能：自动验证每次输出、量化每次prompt调整的真实效果、做closed-loop（生成→验证→反馈→重试）。

### 3. Build Ground Truth是一种能力

需要两层能力：
1. **识别**什么该成为ground truth——高错误代价的环节、可用确定性手段验证的环节
2. **造出来**——像作者基于SootUp搭Graphite并暴露为MCP Server

## 三、对izu的启示（★★★★☆）

### 核战队验证引擎的理论根基

这篇文章提供了核战队验证引擎缺失的**理论层**——我们一直知道需要验证，但没想清楚验证的哲学是什么。

**核心三点：**
1. **验证必须确定性工具做，LLM只做解释**——我们目前全靠LLM判断"这个评估好不好"，这是错误做法
2. **Ground Truth需要工程化造出来**——不能指望LLM自己产出ground truth
3. **Closed-loop验证**——生成→验证→反馈→重试，我们已经有这个框架但缺少确定性验证环节

### 可立即执行的行动

| 行动 | 当前 | 目标 |
|---|---|---|
| 核战队评审标准 | 军师/子贡LLM判断 | 加入确定性检查项 |
| ITA编码器验证 | 纯LLM评估 | 加入静态分析验证层 |
| Skill效果评估 | 主观判断 | 定量指标+确定性检查 |

### 军师判断

这篇文章比第一眼看起来重要。它补上了核战队架构的**短板**：我们的验证引擎全部基于LLM的"像对的"判断，缺少确定性的ground truth层。

**建议**：不急着全面铺开，选一个高价值小场景做POC（ITA编码器的compact encoding验证？），跑通后再扩展。

## 四、与Evolver Engineering的关联

上周昌的文章讲**Evolver Engineering**（进化工程），核心是量化SKILL/Memory贡献、删减负能力要素。这篇文章补上了"用什么量化"——用确定性的ground truth，而不是用LLM自我评价。

两篇合在一起读，才是完整的：
- **周昌**：进化工程的方向（压缩、量化、成本）
- **Johnsonlee**：进化的度量方法（Ground Truth）

核战队的进化引擎 = 周昌的方向 + Johnsonlee的方法。
