---
source_url: https://mp.weixin.qq.com/s/_nGsAxStGxP9pLO1gmOgzw
ingested: 2026-05-07
sha256: 00e8d35e7961548246c42fa5a99eb1099f213f305918270bb5c20504304e759e
source: 量子智元（微信公众号）
author: 量子智元
description: Hermes Agent v0.12.0 Kanban：AI 多智能体协作新方式
---

# Hermes Agent v0.12.0 Kanban：AI 多智能体协作新方式

本文介绍 Hermes Agent v0.12.0 新推出的 Kanban（看板）功能，实现了有状态、有依赖、有历史、可重试的多 Agent 任务流水线。

## 解决的问题

原来 Hermes 多 Agent 协作靠 `delegate_task`——主 Agent 分发子任务，等结果回来再继续。问题在于：任务状态全在当前对话里，Agent 一死就没了。

**Kanban 的思路**：每个任务是数据库里的一行（`~/.hermes/kanban.db`，SQLite），状态持久化；多个命名 Agent（backend-dev、qa-dev、translator……）各自认领、执行、写结果。三方（你、脚本、Agent）可读写同一块看板。

## 六列看板

| 列 | 说明 |
|---|---|
| **Triage** | 原始想法，未整理成可执行任务 |
| **Todo** | 有依赖未完成，或未分配 Assignee |
| **Ready** | 可被 dispatcher 认领执行 |
| **In Progress** | 某个 worker 正在跑（按 Assignee 分组） |
| **Blocked** | worker 卡住，需人工介入或熔断器触发 |
| **Done** | 完成 |

**打开方式**：
```
hermes kanban init   # 可选，首次自动初始化
hermes dashboard     # HTTP://127.0.0.1:9119 → 左侧 Kanban
```

Agent worker 通过专用工具调用操作看板：`kanban_show`、`kanban_complete`、`kanban_block`、`kanban_heartbeat` 等。

## 依赖链

典型场景：设计 Schema → 实现 API → 写测试。

```
# 创建有依赖关系的任务链
SCHEMA=$(hermes kanban create "Design auth schema" --assignee backend-dev --priority 2)
API=$(hermes kanban create "Implement auth API" --assignee backend-dev --parent $SCHEMA)
hermes kanban create "Write auth tests" --assignee qa-dev --parent $API
```

依赖引擎自动管理状态流转：父任务完成后，子任务从 Todo → Ready，不乱序执行。

## Fleet 模式

多 Worker 并行消耗任务队列。启动 `hermes gateway start` 后内置 dispatcher 自动调度所有 profile。In Progress 列按 Assignee 分组显示，一目了然。

## 熔断器（Circuit Breaker）

连续 3 次失败 → 任务进入 Blocked（outcome = gave_up），不再重试，等待人工 `hermes kanban unblock $TASK_ID`。`gave_up` 事件会主动推送到 Telegram/Discord。

## Worker 工具调用序列

```
kanban_show()                # 读取任务描述、父任务结果、历史记录
# 执行具体工作...
kanban_heartbeat(note="...") # 状态心跳
kanban_complete(
    summary="...",           # 给下游的结构化数据
    metadata={"changed_files": [...], "decisions": [...]}
)
```

`summary` 和 `metadata` 是给下游 worker 的结构化交接数据，不用重新读设计文档。

## 适合场景 vs 不适合场景

**适合**：任务有依赖、多 Agent 角色分工、需要知道每一步为什么这么做。
- 工程流水线：设计 → 实现 → review → 上线
- 内容批处理：转写 → 翻译 → 校对

**不适合**：单次对话能搞定的任务，不需要跨 Agent 交接结果。用 `delegate_task` 即可。
