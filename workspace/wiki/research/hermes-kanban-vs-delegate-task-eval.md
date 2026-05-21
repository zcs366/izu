---
title: 评估：Hermes Kanban vs delegate_task
source: wiki/raw/articles/hermes-kanban-vs-delegate-task.md
date: 2026-05-19
eval_level: 大
tags: [评估, Hermes, Kanban, delegate_task]
---

## 核心判断
**这是你日常工作中最实用的工具选择指南。** 区分了"搭基础设施"和"临时调用"两个问题——很多人混用导致任务丢失。

## 关键提炼
- Kanban=基础设施（持久化/多角色/失败恢复）
- delegate_task=临时工（快/无状态/内存级）
- 推荐互补：Kanban管协作，delegate_task管推理中的临时子问题

## 对张成市的价值
**高。** 你核战队的"五人合议"流程正好是Kanban的典型使用场景——多Agent协作、需人工审批（军师终裁）、跨会话持久化。而delegate_task适合在合议流程中拉起临时子Agent查资料。

## 连接点
→ 核战队架构：五人合议 = Kanban多角色协作流程
→ cat Wu专访：Kanban≈Evergreen Launch Room的协作管道
