---
source_url: https://mp.weixin.qq.com/s/oLiadKMNnXzNYKOgsH4ibA
ingested: 2026-05-19
sha256: pending
title: Meta-Harness：从"调 Prompt"到"自动进化整套 Harness"
author: 微信公众号
source: arXiv:2603.28052
---

# Meta-Harness 核心笔记

**论文**：Meta-Harness: End-to-End Optimization of Model Harnesses
**作者**：Yoonho Lee (Stanford), Roshen Nair, Qizheng Zhang (Stanford), Kangwook Lee (KRAFTON), Omar Khattab (MIT), Chelsea Finn (Stanford)

## 方法

外循环：proposer（coding agent）读取历史文件系统 → 提出新harness代码 → 评测 → 在Pareto frontier上选解。

关键设计：全历史可检索文件系统，proposer 用 grep/cat 按需取证，而非一次性塞进 prompt。

每步反馈 token 量：~10,000,000（先前方法 ≤ 26,000）

## 实验结果

- 在线文本分类：+7.7 pts（48.6% vs 40.9%），4× 更少 tokens
- IMO数学推理（检索增强）：+4.7 pts，5个held-out模型平均
- TerminalBench-2：Opus 4.6 → 76.4%（超越 Terminus-KIRA 74.7%）
- 消融实验：全traces中位准确率50.0% vs 仅分数34.6%

## 与izu关系

- 进化引擎方向一致，但度更细
- 最大差距：缺执行轨迹作为反馈
- 建议：P1 让进化引擎能 grep 历史执行日志
