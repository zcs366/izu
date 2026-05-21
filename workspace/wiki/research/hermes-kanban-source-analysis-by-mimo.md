---
title: "Hermes Kanban源码深度分析（MiMo V2.5 Pro产出）"
aliases: ["Kanban源码分析", "kanban_db.py分析", "Dispatcher源码"]
author: "MiMo V2.5 Pro (通过子代理)"
source: "Hermes Agent源码：tools/kanban_tools.py + hermes_cli/kanban_db.py + gateway/run.py"
created: "2026-05-20"
updated: "2026-05-20"
tags: [Kanban, 源码分析, Hermes, Dispatcher, SQLite, 状态机]
sources:
  - /home/zcs/.hermes/hermes-agent/tools/kanban_tools.py
  - /home/zcs/.hermes/hermes-agent/hermes_cli/kanban_db.py
  - /home/zcs/.hermes/hermes-agent/gateway/run.py
---

# Hermes Kanban 源码深度分析报告

> 由 MiMo V2.5 Pro 分析产出 | 2026-05-20

---

**一句话核心判断**：Kanban不是"又一个看板工具"，它是一个精心设计的三层门控+原子CAS+7步Tick调度器的持久化多Agent状态机。最值得izu抄的设计是**原子CAS Claim**和**结构化worker上下文传递机制**。

---

## 一、三层门控设计

工具层使用 **三层守卫** 控制哪些工具对什么上下文可见：

| 层 | 函数 | 逻辑 | 适用工具 |
|---|---|---|---|
| **全局门** | `_check_kanban_mode()` | `HERMES_KANBAN_TASK`已设置 **或** profile启用kanban toolset | kanban_show/complete/block/heartbeat/comment/create/link |
| **Orchestrator门** | `_check_kanban_orchestrator_mode()` | 非worker **且** profile有kanban toolset | kanban_list, kanban_unblock |
| **运行时守卫** | `_require_orchestrator_tool()` | Belt-and-suspenders——schema门失败后handler内部再检查 | kanban_list, kanban_unblock |

**关键设计**：`check_fn`在`registry.register()`时注册，运行时由`model_tools.py` TTL缓存（约30s）决定是否注入模型schema。Worker进程不会看到`kanban_list`/`kanban_unblock`。

## 二、所有权检查与任务隔离

`_enforce_worker_task_ownership(tid)`：Worker（`HERMES_KANBAN_TASK`已设置）调用complete/block/heartbeat时必须传入自己的task_id。传入其他task_id返回`tool_error`拒绝执行。

**例外**：`kanban_comment` **没有** 所有权检查——注释是有意设计的跨任务沟通通道（#19713）。

## 三、原子CAS Claim——Kanban最精髓的设计

核心代码（简化）：
```python
updated = db.execute(
    "UPDATE tasks SET status='running', current_run_id=?, started_at=? "
    "WHERE id=? AND status='ready'",
    [run_id, now, task_id]
)
if updated.rowcount == 0:
    return None  # claimed by someone else
```

**为什么重要**：单条SQL UPDATE + rowcount检查，零分布式锁。SQLite WAL模式保证串行化。这是Kanban能在单进程多Worker下无锁并发的根本。

## 四、Dispatcher 7步Tick循环

1. **僵尸回收** — PID不存在且TTL过期的任务回收
2. **TTL回收** — 存活但TTL耗尽的强制回收
3. **心跳检测** — 检查worker健康状态
4. **崩溃检测** — 检测意外退出的worker
5. **超时终止** — 运行超过max_duration的任务强制终止
6. **依赖解析** — 检查依赖链，Completed的上游触发下游Ready
7. **Ready/Review派发** — 从Ready队列取任务派生Worker

## 五、完整状态机

`triage → todo → scheduled → ready → running ↔ blocked → review → done | archived`

对比文章说的6列，实际有**8态**——多了`scheduled`（等待调度时间）和`review`（需要人工确认完成）。

## 六、电路断路器

`consecutive_failures` + 阈值检查。协议违规或系统性失败立即熔断，只在成功完成时重置。默认3次失败后进入`gave_up`。

## 七、Worker上下文构建

`build_worker_context()`的截断策略：
- attempts上限10条
- comments上限30条
- 每字段：summary 4KB / metadata 8KB / error 2KB

防止历史信息撑爆worker prompt。

## 八、SQLite Schema（关键表）

- **tasks** — id, title, body, assignee, status, priority, tenant, workspace_kind, workspace_path, created_by, created_at, started_at, completed_at, current_run_id, model_override, consecutive_failures, max_consecutive_failures
- **runs** — id, task_id, profile, status, outcome, summary, error, metadata (JSON), started_at, ended_at
- **events** — id, task_id, run_id, kind, payload (JSON), created_at
- **comments** — id, task_id, author, body, created_at
- **parents/children** — tasks_links表(pair_id, parent_id, child_id, created_at)

## 九、可直接复用的设计模式

1. **原子CAS Claim** — 单SQL UPDATE + rowcount检查，无锁并发
2. **结构化worker上下文传递** — build_worker_context()的截断策略
3. **三层门控** — check_fn TTL缓存决定模型可见性
4. **断路器** — consecutive_failures + gave_up
5. **kanban_comment无锁设计** — 故意绕过所有权检查

## 十、潜在坑点
- 单宿主局限（跨机PID检测不可用，只能等TTL）
- Gateway崩溃导致worker孤儿（依赖TTL过期恢复）
- SQLite写串行化在单board高并发时可能瓶颈
- 快速重试风暴 + 断路器阈值配置不当

---

*分析时间：2026-05-20 | 源码版本：Hermes Agent 基于当前安装*
