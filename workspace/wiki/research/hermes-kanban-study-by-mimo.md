---
title: "Hermes Kanban 学习研究报告（MiMo V2.5 Pro产出）"
aliases: ["Kanban学习报告", "izu+Kanban", "Kanban落地izu"]
author: "MiMo V2.5 Pro (通过子代理)"
source_article: "原文阅读于微信公众号（歪斯Wise → Hermes Kanban 看板）"
created: "2026-05-20"
updated: "2026-05-20"
tags: [Kanban, Hermes, izu, 多Agent协作, 工作流, SQLite, 状态机]
sources:
  - https://mp.weixin.qq.com/s/tx4QhbuUIWdmmkL5ijOJag
---

# Hermes Kanban 学习研究报告：izu多Agent协作的下一步

> 由 MiMo V2.5 Pro 评估产出 | 2026-05-20

---

**核心判断**：Kanban不是在和izu的pipeline竞争，而是在补pipeline的缺——持久化状态、失败恢复、人为介入这三个缺口正是izu当前多Agent协作中真实存在的痛点。

---

## 1. Kanban vs izu现状：差距在哪

| 维度 | izu当前（izu-pipeline + delegate_task） | Hermes Kanban | 差距 |
|------|-----------------------------------------|---------------|------|
| 任务持久化 | 内存中，上下文压缩后丢失 | SQLite永久存储 | 🔴 |
| 父Agent状态 | delegate_task阻塞等待子Agent | fire-and-forget | 🟡 |
| 失败恢复 | 失败即失败，无重试 | block→unblock→重新派生 + 断路器 | 🔴 |
| 人为介入 | 不支持（需重新发起对话） | 随时评论/解封/干预 | 🔴 |
| 审计轨迹 | 上下文压缩后丢失 | SQLite每次run完整记录 | 🔴 |
| 协作模式 | 层级式（军师delegate到子Agent） | 对等式（任何Profile读写任何任务） | 🟡 |
| 数据传递 | 手动拼接上下文 | kanban_show()自动看到上游summary | 🟡 |
| 依赖链 | 需手动编排顺序 | --parent字段自动依赖驱动 | 🟡 |

核心结论：**izu目前的编排是"脆弱的单线"**——依赖链是人脑维持的，失败是全损的，审计是依赖上下文日志的。Kanban的三个核心设计（持久化、恢复机制、结构化传递）正好补这个缺。

---

## 2. 四个场景在izu的映射

### 场景一：依赖链 → 核战队合议

核战队五人合议的典型流程是：
```
子产（诊断）→ 韩信（终局画像）→ 鲁班（架构/砍成本）→ 萧何（评估/锚点）→ 子贡（调度）→ 军师（终裁）
```

**这天然就是一个Kanban依赖链。** 每个Agent完成后，下一个Agent自动Ready，不需要军师手动说"子产完了，韩信上"。

更重要的是**数据传输**：目前每个Agent的输出是手动拼接成上下文的，经常丢东西。如果每个Agent通过`kanban_complete()`写summary/metadata，下游Agent通过`kanban_show()`自动读取，信息传递就变成了结构化契约，而不是靠prompt模板硬拼。

**差距分析**：izu切得很细（五人各司其职），但没有持久化状态。一个Agent跑了40分钟后崩溃（delegate_task超时），就全部重来。Kanban的block+重派能解决这个问题。

### 场景二：并行舰队 → 每日论文日报

izu的每日论文日报需要同时搜索多个来源、多个关键词。目前的做法是串行或手动并行。Kanban的批量创建+同Profile自动调度可以直接套用。

### 场景三：角色Pipeline + 重试 → 萧何审计

萧何审计系统目前的流程是：生成报告→萧何审计→打回→重做。但打回后没有机制确保二次尝试的Agent知道为什么被驳回。

Kanban的`kanban_block(reason=...)` + `worker_context`携带前一次block原因——**这正是萧何审计缺失的"失败反馈回路"**。目前的实现是让Agent重新读一遍审计报告，但Agent可能没读到关键段落。有了`worker_context`，断路器签名直接传给下一个Worker，不需要Agent自己去理解长文本。

### 场景四：断路器 + 崩溃恢复

izu目前对子Agent（delegate_task）的失败处理是：超时→重试（在代码层），但如果3次都失败，没有"放弃"信号，也没有通知机制。子Agent静默失败的情况时有发生。

Kanban的3次→gave_up→通知Telegram/Discord——这个模式可以直接抄。

---

## 3. 设计精华：哪些应该"抄"

### 3.1 SQLite持久化 + 双接口设计（P0级设计模式）

这不是一个"可有可无"的设计，这是Kanban真正的架构灵魂：

```
┌─────────────┐     ┌──────────────┐
│  人类接口    │     │  Agent接口    │
│ (CLI/Web)   │     │ (kanban_*)   │
└──────┬──────┘     └──────┬───────┘
       │                   │
       └───────┬───────────┘
               ▼
       ┌───────────────┐
       │  SQLite        │
       │  kanban.db     │
       │  (单一数据源)  │
       └───────────────┘
```

两套接口走同一套数据库代码，数据永不漂移。人类在Web Dashboard上Unblock一个任务，Agent在Terminal上kanban_show()看到的block状态是一致的——不需要通过Hermes消息总线传递状态。这一点对izu的多Agent编排非常有价值。

### 3.2 kanban_complete()的传递契约（P0级设计模式）

```python
kanban_complete(
  summary="...",  # 供下游Agent可读
  metadata={      # 供下游Agent程序化处理
    "changed_files": [...],
    "decisions": [...],
    "confidence_score": 0.85
  }
)
```

这不是"发一条消息"，而是**结构化状态转移**。下游Agent的kanban_show()直接拿到的是：
- summary（自然语言概览）
- metadata（结构化数据，可编程消费）

izu目前的问题是：每个Agent的输出格式不统一，下游Agent依赖prompt模板去理解上游说了什么。如果采用这个契约，每个Agent只需承诺输出固定的metadata结构，下游Agent可以直接解析。

### 3.3 kanban_block() + worker_context 失败传递（P1级）

失败不是"报个错就完"，而是：
1. 明确谁驳回、为什么驳回（block reason）
2. 下游Agent拿到前一次的失败原因（worker_context）
3. 仪表盘显示完整失败链

这也是izu目前缺失的——萧何审计驳回后，被驳回的Agent只能去读审计报告全文，没有结构化"驳回原因"传递给下一次尝试。

### 3.4 断路器（P2级）

连续失败3次→gave_up→Telegram通知手机。简单但有效。可以在izu的delegate_task外层包装一个类似的计数器。

---

## 4. 动手路线图

### 第一步（学习）：读Hermes Kanban源码

**目标文件**：
- `~/.hermes/...` 下的 `kanban.py` 或 `kanban/` 目录
- 重点关注：`kanban_show()`、`kanban_complete()`、`kanban_block()` 的实现
- Dispatcher的逻辑：如何检测Ready任务、如何派生Worker

**时间**：1小时阅读。不是改代码，是理解设计。

### 第二步（实验）：核战队走SQLite状态机原型

不直接启用Hermes Kanban，而是在izu的核战队pipeline中做一个**最小原型**：

1. 建一个`izu_kanban.py`，用SQLite存4个字段：`session_id, agent_name (子产/韩信/鲁班/萧何/子贡/军师), status (pending/ready/in_progress/done/blocked), output_summary`
2. 在每个Agent执行完写入output_summary
3. 下游Agent启动前先查SQLite读上游的output_summary
4. 不需要Dispatcher——手动触发

**目标**：验证"持久化状态+结构化传递"这个核心模式是否适合izu。
**时间**：半天到一天。

### 第三步（评估）：判断是否启用Hermes原装Kanban

如果第二步验证成功（状态持久化有价值、结构化传递减少了上下文噪音），评估是否切换到Hermes原装Kanban。

**切换条件判断**：
- 是否已经有多个Profile（izu目前只有一个军师Profile，子Agent通过delegate_task跑）
- 是否需要人类Unblock（izu目前是军师手动重派）
- 是否需要Dashboard可视化（izu目前不需要）

**评估结论预测**：izu目前可能不需要完整的Kanban（因为本质上是一个单人系统，军师既是指挥又是执行），但需要**Kanban的数据模型**。

---

## 5. 陷阱与注意事项

| 问题 | 风险等级 | 说明 |
|------|---------|------|
| Kanban依赖Hermes Agent | 高 | 没有Hermes跑不了Dispatcher。izu如果不用Hermes Gateway，自己实现状态机更可行 |
| Dispatcher需要Gateway | 中 | 文章没说但Dispatcher是Gateway内置的，Gateway不启动则无自动派发 |
| kanban_*工具函数需要skill支持 | 中 | 这些是Hermes的内置工具，izu的子Agent（通过delegate_task）拿不到。如果需要izu子Agent用Kanban，需要额外bridge |
| SQLite并发写入 | 低 | SQLite WAL模式支持并发读，但多个Worker同时kanban_heartbeat()可能有写锁。Hermes的实现应该已处理，但izu自己的原型需要注意 |
| 单Profile vs 多Profile | 中 | Kanban的核心是"多个Profile读写同一个看板"。izu目前只有一个军师Profile，子Agent是匿名的。要发挥Kanban的协作价值，需要先把核战队五人做成独立Profile |
| 审计日志膨胀 | 低 | SQLite存储每次run，长期运行会膨胀。Hermes应该有清理机制，izu原型也要考虑 |

---

## 6. 最终结论

**Kanban的价值不在于"又一个看板工具"，而在于它提供了一个经过验证的数据模型——持久化状态 + 双接口访问 + 结构化传递 + 失败恢复。**

izu当前的多Agent编排（核战队五人各司其职）架构方向是对的，但在**状态持久化**和**失败恢复**上存在真实缺口。不需要直接启用Kanban，但应该学习它的核心设计模式：尤其是`kanban_complete()`的参数契约和block→unblock→重试的失败处理模式。

**建议行动顺序**：
1. 读Hermes Kanban源码（1h）
2. 做izu最小原型验证（半天）
3. 评估是否启用原装Kanban（决策）

---

*报告生成时间：2026-05-20 | 由 MiMo V2.5 Pro 评估产出*
