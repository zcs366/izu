---
source_url: https://mp.weixin.qq.com/s/jAxu3dG4KFfc78X2CL9M-A
sha256: 08da96d5afbaf7fddf9543ab25bcc33d562874c14c29be9b6da82af4eee1df2c
ingested: 2026-05-19
title: Hermes的多agent协作：Kanban vs delegate_task
author: 赛博生命虾酱
source: 微信公众号
eval_level: 大
tags: [Hermes Agent, Kanban, delegate_task, 多任务协作]
---

# Hermes的多agent协作：Kanban vs delegate_task

> 作者：赛博生命虾酱 (2026-05-06)

## Kanban — 任务协作框架
- 持久化 SQLite 数据库，跨进程存活
- 多 profile 并发，真多进程
- 支持 block 等待人工输入
- events 日志可追踪每个节点

## delegate_task — 函数调用
- 同一推理链条里快速拉起子 agent 并行干活
- 结果只存内存，父会话结束即消失
- 极低 overhead，同步返回

## 核心对比（Kanban 5维度领先）
Kanban优势：持久性、角色协作、失败恢复、可观测性、人工干预
delegate_task优势：速度（极低overhead）

## 决策指南
1. 需人工审核？→ Kanban
2. 需跨会话持久化？→ Kanban
3. 需多角色协作？→ Kanban
4. >5分钟？→ Kanban
5. 短时子问题<2分钟？→ delegate_task

## 推荐互补用法
在 Kanban 任务内部调用 delegate_task 是最稳定的用法。
