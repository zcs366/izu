---
title: "军师中枢工作模式变更记录"
created: "2026-05-20"
updated: "2026-05-20"
tags: [中枢模式, 架构变更, skill化]
---

# 军师中枢工作模式

## 变更内容（2026-05-20）

**背景**：delegate_task在执行长任务时，用户发新消息会导致子代理被静默中断（exit_reason=interrupted），浪费大量token。

**解决方案**：军师角色从"执行者"变为"中枢"
- 不再亲自做评估分析/读源码/搜索等耗时任务
- 所有子代理任务通过cronjob独立进程执行
- cronjob提供100%进程隔离，用户发新消息不打断
- 军师只做：理解意图→分发任务→汇总反馈

**skill化**：`devops/deferred-task-worker` v2.0

**已派出的Deferred Worker**：
1. `134204eddaa6` — 压缩器源码分析+工作集恢复实现方案
2. `77be435a88e8` — Fiverr搞钱可行性评估

**核心原则**：
- 所有delegate_task→cronjob+deliver=local
- prompt必须自包含（不依赖对话上下文）
- 用户不问就不查结果，问了才查
- 短任务（<10秒）保持直接执行
