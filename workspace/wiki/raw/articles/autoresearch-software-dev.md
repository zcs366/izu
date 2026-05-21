---
source_url: https://mp.weixin.qq.com/s/JFvYo9RCn9Xm8ilx1Chd6g
ingested: 2026-05-14
sha256: 75920e91036a2266
title: 我把 Karpathy 的 AutoResearch 搬到了软件开发领域，效果炸了
author: 鸟窝
source: 微信公众号
---

点击蓝字，关注我们

作者 | 鸟窝

本项目成功将Karpathy在AI研究领域的AutoResearch方法迁移到软件开发领域，通过多AI Agent交叉审核、5维度量化评分和反馈驱动迭代三大改进，构建了一个全自动的软件开发系统。该系统以program.md为规则核心，实现从GitHub Issue识别、代码实现、测试验证到审核合并的完整闭环，仅在少数情况下需要人工介入。实践表明，该系统能在约10分钟内自主完成中等复杂度的开发任务，并达到9.0/10的代码质量标准。

## 什么是 Karpathy AutoResearch？

2026 年 3 月，Andrej Karpathy 发布了 autoresearch 项目，几天内 GitHub 5 万+ 星标。核心思想：把 AI 研究本身也交给 AI 来自主完成。

具体做法：给 AI Agent 一个真实的小型 LLM 训练环境（单 GPU，5 分钟训练预算），让它自主修改 train.py、跑实验、检查结果——只有 val loss 确实降低了才保留修改，否则回滚。循环往复。

核心理念：只保留可测量的改进，其余全部回滚。

这个循环极简但极强：提出想法→实现→运行实验→测量结果→保留或回滚→继续。

## 迁移到软件开发

鸟窝把同样的思想搬到了软件开发领域，项目地址：https://github.com/smallnest/autoresearch

核心循环：识别 Issue → Agent1 实现 → Agent2 审查打分 → 通过就合并，不通过就反馈给 Agent1 重做。

三大改进：
1. **多 Agent 交叉审核**：支持 1-3 个 Coding Agent（Codex/Claude Code/OpenCode）任意组合，互相审查
2. **5 维度量化评分**：代码正确性、代码风格、测试覆盖、安全性、性能，每项 0-10 分
3. **反馈驱动迭代**：审查不通过时，评分报告作为反馈输入，Agent 据此修改，直到达标或达到最大重试次数

以 program.md 为规则核心，定义项目的编码规范、审查标准、评分阈值。

## 实际效果

中等复杂度的开发任务（如添加一个带测试的 API 端点）能在约 10 分钟内自主完成，代码质量评分 9.0/10。

关键设计决策：
- 多 Agent 对抗：Codex 实现 + Claude 审核，交叉验证减少盲区
- 量化一切：不靠"我觉得可以"，靠打分
- 退火重试：API 不稳定时脚本自动退避重试，无需人工干预
- 只保留可测量的改进：评分不达标就回滚，不积累技术债务

## 底层工具链

- acpx — Agent 控制工具，让 Codex/Claude 在命令行中协作
- imclaw — 鸟窝自己的项目，微信/飞书操控 Claude Code/Codex/Gemini CLI/Pi Agent 蜂群
- OpenCode — 开源 Coding Agent
