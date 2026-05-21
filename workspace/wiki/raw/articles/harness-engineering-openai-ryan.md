---
title: "什么才是 Harness Engineering？OpenAI Ryan 伦敦演讲: Code is free, Agent 时代的软件工程分工"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/3Il92Szr1z4nf-u3Ur4Y-g"
author: "高可用架构 (译自 OpenAI Ryan Lopopolo 伦敦演讲)"
date: 2026-05-19
ingested: 2026-05-19
sha256: f1f12970444622c5167405e7393a1c10c7465774ebbab745126d2960b5084f12
type: article
tags: [harness-engineering, agent-orchestration, code-is-free, guardrails, openai]
eval_level: 极大
---

# 什么才是 Harness Engineering？OpenAI Ryan 伦敦演讲

## 核心论点
**代码是免费的（Code is Free）。** 软件工程分工已变。真正稀缺的不再是实现能力，而是人类时间/注意力、模型上下文窗口。工程师角色从 implementer 转向 orchestrator。

## 12个核心要点
1. 代码正在变便宜——生成代码不再是最贵环节
2. 模型已能胜任完整软件工程——尤其真实仓库里的真实问题
3. 工程师角色转变：从 implementer → orchestrator
4. 三种新稀缺资源：人类时间、人类与模型的注意力、模型上下文窗口
5. Harness 本质：把团队经验写成智能体可读的运行说明
6. 仓库 = Agent 唯一事实源
7. 渐进式上下文注入：按阶段给正确约束
8. Guardrails > Prompt：把人的 taste 变成机器可执行的 lint/规则
9. 自验证工作流：写代码不是终点，能自己验证、修正、通过才算完成
10. Review 重点转移：从"看代码"转向"看系统为什么让它走偏"
11. Skill 重质不重量：核心 skill 仅 5-10 个
12. 最终目标：Agent 7×24 工作，人只做判断、排序、验收

## 五层解读
1. **不是 Prompt 技巧，而是运行系统**：Prompt Engineering（怎么说）→ Context Engineering（给它看什么）→ Harness Engineering（让它在什么系统里工作）
2. **核心不是"更聪明"，而是"更可完成"**
3. **真正值钱的资产是 Guardrails**：lint、结构测试、依赖规则、review agents、QA plans
4. **重写软件工程分工**：定义 success criteria 的人 > 写代码的人
5. **最小闭环实践路径**：选高频任务→补入口地图→写一条guardrail→给自验证路径→每周回写一条规则

## 关键引述
- "代码是免费的。限制团队的因素已经只剩 GPU 容量和 token 预算。"
- "工程师真正的职责，是为智能体团队清除障碍。"
- "每次你必须与代理交互，都是失败。"
- "文件系统里的代码本身也是文本，而文本本质上就是你给编码智能体的提示。"

## 三种稀缺对比
| 旧稀缺 | 新稀缺 |
|--------|--------|
| 编写代码的能力 | 人类时间 |
| 工程师数量 | 人类和模型的注意力 |
| 部署速度 | 模型的上下文窗口 |
