---
title: Trace2Skill — 阿里巴巴Qwen团队论文原文
ingested: 2026-05-21
sha256: 672c84dab64775c417a5c389b90817490411c23fb64da26d76ab14bf368a3f98
created: 2026-05-18
updated: 2026-05-18
type: raw
tags: [AI/ML, paper, agent, skill]
source: https://arxiv.org/abs/2603.25158
confidence: high
---

# Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills

> **原始论文**: https://arxiv.org/abs/2603.25158
> **代码**: https://github.com/Qwen-Applications/Trace2Skill
> **作者**: Jingwei Ni†(ETH), Yihao Liu†(北大), Xinpeng Liu†(北大), Yutao Sun†(浙大) 等 — 阿里巴巴Qwen团队
> **日期**: 2026-03-31 (v4: 2026-04-27)

## 摘要

手动编写技能有严重可扩展性瓶颈，自动生成往往产生脆弱结果。Trace2Skill模拟人类专家编写技能的方式：**整体分析广泛的执行经验**，然后提炼成单一、全面的指南。派出并行子Agent分析多样化轨迹池→提取轨迹特定教训→**归纳推理**整合成统一、无冲突的skill目录。

## 关键实验数据

- **跨LLM规模迁移**：Qwen3.5-35B演化的技能使Qwen3.5-122B在WikiTableQuestions上提升**高达57.65个绝对百分点**
- **无需参数更新**，无需外部检索模块，仅需35B参数的开源模型
- 支持深化已有技能和从零创建新技能

## 纠正（vs视频解读）

- 视频说"小模型写的手册让大模型飙升" → ✅ 准确，跨模型迁移是核心卖点
- 视频没提的具体数据：Qwen3.5-35B→122B跨模型迁移提升57.65pp
- "防呆操作手册(skill.md)" → 论文中称为"声明式技能(Declarative Skill)"，纯文本存储，不绑定模型参数
