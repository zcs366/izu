---
title: 图灵奖得主杨立昆最新访谈：LLM时代即将落幕？
source: https://mp.weixin.qq.com/s/HYfqHn068A88Aj8ttuEGAA
date: 2026-05-17
eval_level: 大
contributors: 军师
tags: [lecun, jepa, world-model, llm-limitation, ami-labs]
author: 杨立昆 (Yann LeCun)
references:
  - Unsupervised Learning Podcast 2026
  - LeCun JEPA papers
  - ILE (Bistriero)
status: 已评估
---

# 杨立昆最新访谈评估

## 一、核心论点

LLM虽伟大，但**不是通往人类级智能的路**，甚至不是动物级智能的路。

LeCun在LLM最如日中天时公开唱反调，押注**JEPA架构+世界模型**。

## 二、三个致命攻击

### 1. 语言≠世界
- 语言世界：离散符号，~10万token，LLM完美适用
- 现实世界：高维、连续、噪声、不确定
- **LLM只训练"给定文字下一token是什么"，不是"给定物理状态接下来会发生什么"**

### 2. LLM缺两个关键能力
- **无法预测行动后果** — 最大级模式匹配器，不知道自己说什么
- **没有真正规划能力** — 逐token预测≠搜索和优化

### 3. 给PhD的建议
> "不要搞LLM。学术界的LLM是描述性的——解释它为什么work。这不是创造性研究。**去研究下一代系统。**"

## 三、JEPA方案

核心：不在像素层预测未来，在**抽象表示空间**做预测。

| 组件 | 作用 |
|---|---|
| 双编码器 | 处理两个不同视角输入 |
| 预测器 | 从一个表示预测另一个 |
| SIGPreg正则化器 | 防表示崩溃，强制各向同性高斯分布 |

最大挑战：表示崩溃（Representation Collapse）— 用SIGPreg解决。

## 四、Meta内部战争

LeCun离开管理岗的原因：FAIR被告知帮Llama → 长期探索优先级降低 → 2023年GenAI成立抽人去做Llama → Llama 4让Zuckerberg失望 → FAIR与GenAI断层。

**他唯一贡献**：推动Llama 2开源，内部法律/政策部门反对，他力排众议。

## 五、AMI Labs

新公司AMIE（Advanced Machine Intelligence），副标题"AI for the Real World"。融资顺利。态度：极度自信+极度诚实。

## 六、军师判断

**级别：大**

**三条启示**：
1. **LLM天花板争论不影响我们** — izu不是LLM替代方案，是LLM的上层框架。LLM能做的用LLM做，LLM做不了等新架构
2. **JEPA的表示空间概念 → ITA的compact encoding** — 将高维信息压缩到低维表示空间，两方向一致
3. **LeCun说的"描述性研究vs创造性研究"** — 核战队的定位是创造性研究（造东西），不是描述性研究（解释为什么），方向正确

**与主流矛盾的处理**：
- 我们的实践仍以Hermes/LLM为中心——这是现在能用的东西
- JEPA是未来可能的方向——记一笔，等成熟了再评估
- 不因为LeCun唱反调就动摇现有路线

**一句话**：LeCun可能在AI的终点是正确的，但明天的活儿还得用LLM干。
