---
source_url: https://mp.weixin.qq.com/s/b1VL28GX5d17sKPfkSbIsw
sha256: 46b0165981bc13e944e76747120788e78cb84424bae6e3cd067ec3eace2f1d00
ingested: 2026-05-21
title: 从Prompt、Context到Harness，工程的三次进化与终局之战
author: 李伟山
source: 腾讯云开发者
source_type: 微信公众号
---

# AI 工程的三次进化：从 Prompt、Context 到 Harness

**来源**：腾讯云开发者（李伟山）

## 核心框架

AI 工程能力经历了三次进化——Prompt Engineering → Context Engineering → Harness Engineering。三者不是替代关系，而是层层嵌套。

## 第一次进化：Prompt Engineering

核心思想：模型是"极其擅长续写的系统"，加约束就是 Prompt Engineering 的本质。

主要技巧：零样本、少样本、思维链（CoT）、角色扮演、提示链。

**命运**：2023-2024 年一度是高薪职业，但模型本身语言理解能力快速提升后，精心设计 Prompt 的边际效益降低。

## 第二次进化：Context Engineering

核心思想：金鱼助理比喻——全世界最聪明的助理只有 7 秒记忆，每次见面你给他一份简报。

上下文窗口分层：系统提示 → 用户输入 → 检索到的知识（RAG）→ 历史对话 → 工具调用结果。

关键方法：RAG、滚动摘要、重要性评分、层次记忆。

**实战案例**：OpenAI 把巨型 agent.md 压缩至百行以内，仅作索引目录，动态加载子文档。

## 第三次进化：Harness Engineering

为什么需要：即使 Prompt 和 Context 都完美，Agent 仍可能跑偏、自评过度乐观、声称测试通过但没跑。

**公式**：AI Agent 系统 = 大模型 + Harness

**关键案例：OpenAI 百万行代码实验**
- 3-7 人团队，5 个月，AI 生成近 100 万行生产级代码
- 三大策略：上下文治理、验证闭环、技术债清理

**关键案例：Anthropic 的 F-Harness**
- Planner（规划者）→ Generator（生成者）→ Evaluator（评估者）
- 代价：单 Agent 20 分钟/$9 vs F-Harness 6 小时/$200
- 收益：逻辑完整的生产环境级别

## Harness 的衰变定律

模型能力越强，所需的 Harness 越简单。不要过度设计那些模型未来能自我解决的问题。

## 工程师的新角色

Human steer, agents execute. 三大职责：定方向（Steering）、搭架子（Harnessing）、做判别（Decision Making）。
