---
title: Hermes Kanban 工作流
created: 2026-05-07
updated: 2026-05-10
type: concept
tags: [agent, tool, workflow, kanban]
sources: 
  - raw/articles/hermes-agent-kanban-feature.md
  - raw/articles/hermes-agent-kanban-v0.13-practice.md
confidence: high
---

# Hermes Kanban 工作流

[[Hermes Agent]] 推出的持久化看板系统，将多 Agent 协作从"子任务分发"（`delegate_task`）升级为**有状态、有依赖、有历史、可重试的任务流水线**。

- **v0.12.0**：核心看板系统，SQLite 持久化，六列状态机，父子依赖链
- **v0.13.0**：Gateway 调度器自动拾取、Fleet 舰队视图、熔断器和崩溃恢复、`/goal` 持久目标

## 核心原理

每个任务是 SQLite 数据库（`~/.hermes/kanban.db`）中的一行，状态持久化。多个命名 Agent 各自认领、执行、写结果。**你、脚本、Agent 三方读写同一块看板**，互不干扰。

## 六列状态机

| 列 | 说明 | 流转 |
|---|---|---|
| **Triage** | 原始想法，未整理 | → Todo |
| **Todo** | 有依赖未完成，或未分配 | → Ready（依赖满足后自动） |
| **Ready** | 可被 dispatcher 认领 | → In Progress |
| **In Progress** | worker 正在执行 | → Done / Blocked |
| **Blocked** | worker 卡住或熔断 | ← 人工 unblock |
| **Done** | 完成 | 终态 |

## 依赖链

`--parent` 参数创建任务间的父子依赖。依赖引擎自动管理：
- 父任务完成 → 子任务从 **Todo 自动提升到 Ready**
- 不等待人工触发，不担心乱序执行

典型场景：设计 Schema → 实现 API → 写测试。

## Fleet 模式

多 Worker 并行消耗任务队列。`hermes gateway start` 后内置 dispatcher 自动调度所有 profile。In Progress 列按 Assignee 分组显示。

## 熔断器（Circuit Breaker）

连续 3 次失败 → 任务进入 Blocked（`gave_up`），不再重试。
- 查看失败日志：`hermes kanban runs $TASK_ID`
- 修复后恢复：`hermes kanban unblock $TASK_ID`
- `gave_up` 事件自动推送到 Telegram/Discord

## Worker 工具调用

| 工具 | 作用 |
|---|---|
| `kanban_show()` | 读取任务描述、父任务结果、历史 run 记录 |
| `kanban_heartbeat(note)` | 状态心跳，汇报进度 |
| `kanban_complete(summary, metadata)` | 完成任务，summary 和 metadata 是给下游的结构化交接数据 |
| `kanban_block(reason)` | 标记阻塞并说明原因 |

## 适合场景

- **工程流水线**：设计 → 实现 → review → 上线
- **内容批处理**：转写 → 翻译 → 校对
- **任何需要跨 Agent 交接结果、知道每一步决策原因的场景**

## 不适合场景

单次对话能搞定的任务，不需要跨 Agent 交接结果 → 用 `delegate_task` 即可。

## 实战指南（v0.13.0+）

[[悟果AI]] 撰写了完整的实战指南，以**用户认证系统**为贯穿案例，覆盖四大场景。^[raw/articles/hermes-agent-kanban-v0.13-practice.md]

### 环境准备

```bash
pip install hermes-agent --upgrade   # 升级到 v0.13.0+
hermes kanban init                    # 初始化看板数据库
hermes dashboard                      # 启动看板仪表盘（http://127.0.0.1:9119）
```

### 场景一：功能交付（父子依赖）

将大任务拆成子任务，通过 `--parent` 指定依赖链，调度器自动控制子任务的 Ready 时机：

```bash
# 创建父任务→子任务链
SCHEMA_ID=$(hermes kanban create "Design auth schema" --assignee backend-dev --body "用户表、会话表、令牌表" --json | jq -r .id)
API_ID=$(hermes kanban create "Implement auth API" --assignee backend-dev --parent $SCHEMA_ID --body "注册/登录/刷新/登出" --json | jq -r .id)
hermes kanban create "Write integration tests" --assignee qa-dev --parent $API_ID
```

关键机制：父任务 `complete` 后子任务自动从 **Todo→Ready**，调度器随即拾取。下游 worker 通过 `kanban_show()` 自动读取上游的 `summary` 和 `metadata`，无需人工传文档。

### 场景二：批量任务（Fleet 舰队视图）

多个 worker 并行处理独立任务池，适合翻译、转录、数据清洗等场景：

```bash
for lang in Spanish French German; do
    hermes kanban create "Translate homepage to $lang" --assignee translator --tenant content-ops
done
hermes gateway start   # 一键启动调度
```

- 多个 worker 按角色分道（"进行中"列按 Assignee 分组）
- 任务完成后自动调度下一个就绪任务
- `hermes kanban watch` 实时监控运行状态

### 场景三：多角色流水线（阻塞与重试）

PM→工程师→审查者的标准交付流水线：

1. PM complete 规格，写入验收标准（`--metadata '{"acceptance": [...]}'`）
2. 工程师 claim 实现
3. 审查者 `kanban block` 发现缺陷
4. 工程师 `kanban unblock` → 重新 claim → 迭代完成

每次运行记录在 `task_runs` 表中，审查者可查看完整迭代历史。

### 场景四：熔断器与崩溃恢复

- **熔断器**：连续 3 次失败（默认）→ 任务进入 `gave_up` 态，不再重试。`hermes kanban runs $TASK_ID` 查看失败日志
- **崩溃恢复**：Worker 意外死亡（OOM/kill）→ 调度器通过 `kill(pid, 0)` 检测 → 任务自动回到 `ready` 重试。重试 worker 能看到上次崩溃原因

### 持久目标（/goal）

v0.13.0+ 支持 `hermes /goal` 设定持久目标，看板调度器据此决定任务优先级和分配策略。详见 [官方文档](https://hermes-doc.aigc.green/user-guide/features/goals)。

### 核心配置与命令速查

| 项目 | 说明 |
|------|------|
| 数据库位置 | `~/.hermes/kanban.db`（默认），`$HERMES_KANBAN_DB` 可自定义 |
| 仪表盘端口 | 9119（默认） |
| 熔断阈值 | `--failure-limit N`（默认 3） |
| 通知 | `hermes kanban notify-subscribe <ID> --platform telegram --chat-id <ID>` |

```bash
hermes kanban create "任务" --assignee xxx   # 创建
hermes kanban claim <ID>                     # 认领
hermes kanban complete <ID> --summary xxx    # 完成 + 交接数据
hermes kanban block <ID> "原因"              # 阻塞
hermes kanban unblock <ID>                   # 解封
hermes kanban show <ID>                      # 详情
hermes kanban runs <ID>                      # 运行历史
hermes kanban watch                          # 实时监控
hermes gateway start                         # 启动调度器
```

## 相关条目

- [[hermes-agent]] — 承载 Kanban 的 Agent 系统
- [[soulmd-core-identity]] — 配合 Kanban 使用，定义 Worker 角色的身份和边界
- [[wuguo-ai]] — 实战指南作者
