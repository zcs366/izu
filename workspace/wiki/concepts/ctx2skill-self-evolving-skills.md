---
title: Ctx2Skill: From Context to Skills — 清华孙茂松团队论文原文
created: 2026-05-18
updated: 2026-05-18
type: raw
tags: [AI/ML, paper, skill]
source: https://arxiv.org/abs/2604.27660
confidence: high
---

# Ctx2Skill: From Context to Skills

> **原始论文**: https://arxiv.org/abs/2604.27660
> **代码**: https://github.com/S1s-Z/Ctx2Skill
> **标题**: From Context to Skills: Can Language Models Learn from Context Skillfully?
> **作者**: Shuzheng Si, Haozhe Zhao, Yu Lei 等 — 清华孙茂松团队 + UIUC + 复旦 + 港中文
> **日期**: 2026-04-30 (v1) | 52页 | arXiv:2604.27660

## 摘要

提出Ctx2Skill自演化框架，无需人工监督或外部反馈，自主发现、精炼和选择上下文特定技能。多Agent自我博弈循环：Challenger生成探测任务，Reasoner在技能集指导下解题，Judge提供二值反馈。Proposer和Generator分析失败案例合成技能更新。Cross-time Replay机制防止对抗性崩溃。

## 纠正（vs知乎解读）

- 知乎说"多种骨架模型稳定提升" → 实际：GPT-4.1 11.1%→16.5%(+5.4pp), GPT-5.1 21.2%→25.8%(+4.6pp)
- 论文52页，深度远超市面上大部分短文
- 核心作者序列：司書证(清华+DeepLang)为第一作者，孙茂松为通讯作者

## 实验数据

| 模型 | 基线 | Ctx2Skill | 提升 |
|------|:----:|:---------:|:----:|
| GPT-4.1 | 11.1% | 16.5% | +5.4pp |
| GPT-5.1 | 21.2% | 25.8% | +4.6pp |

四个上下文学习任务：产品文档理解、科学论文推理、复杂指令执行等
