---
title: Agent = Model + Harness：模型决定上限，Harness决定下限
source: https://zhuanlan.zhihu.com/p/2039471612370626449
date: 2026-05-17
eval_level: 大
contributors: 军师
tags: [harness, agent-architecture, governance, execution-hooks, orchestration]
author: deephub (知乎)
references:
  - "周昌: Harness工程→Evolver工程"
  - "Johnsonlee: Ground Truth"
  - "Claude Code Prompt Caching文章"
status: 已评估
---

# Agent = Model + Harness — 评估

## 一、核心公式

> **Agent = Model + Harness**
> 模型决定上限，Harness决定下限。

Harness不是聊天界面，是AI工作的**操作系统**。模型是CPU，Harness是OS——没有OS，CPU干不了任何事。

## 二、Harness的七层

| 层 | 定义 | 核战队对应 |
|---|---|---|
| **上下文加载** | CLAUDE.md/项目规则/架构约束 | ✅ SKILL.md, AGENTS.md |
| **工具层** | read/write/edit/search/execute | ✅ 工具集+MCP |
| **编排** | 子Agent/并行任务/结果合成 | ✅ 五人合议+izu-pipeline |
| **执行钩子** | 模型动作前运行的确定性代码 | ❌ **缺失** |
| **权限层** | 能做什么/不能做什么 | ⚠️ sandbox profile |
| **记忆与状态** | 持久化/压缩/跨会话 | ⚠️ MEMORY.md+SQLite |
| **会话生命周期** | 开始/交接/完成/恢复 | ⚠️ session管理 |

## 三、最值得提取的洞察

### 1. 执行钩子（Execution Hooks）— 我们唯一缺失的组件

> 钩子不是建议，不是指南，是**强制执行**的确定性代码。

一个钩子可以拦截文件写入 → 按Schema校验输出 → 失败时阻止动作 → 返回结构化错误。

**这正好是Ground Truth那篇文章的工程实现**：确定性工具做验证，LLM只做解释。

**对我们来说**：当前核战队没有"模型行动前强制验证"的机制——全靠事后LLM评判。

### 2. 治理层与Harness可分离

> 治理层不关心是哪一个Harness在读它。

这意味着：**一套核战队治理体系，可在不同Agent框架之间迁移**。Claude Code也好、Hermes也好、未来的工具也好——治理层不变。

这是核战队作为"Agent之上的治理层"定位的终极理论验证。

### 3. Harness决定下限

> 带治理的Harness+中等模型，持续胜于无治理的Harness+更强模型。

直接解释了我们为什么选择不追最前沿的模型——把现有Harness的七层做扎实，收益大于追模型。

## 四、军师判断

这篇文章是**框架定义级**的——不是新发现，而是把我们已经直觉在做的事情变成了结构化的理论。

**最大的价值**：帮我们看清了核战队当前的"欠账清单"：

| 组件 | 优先级 | 行动 |
|---|---|---|
| **执行钩子** | P1 | 在关键决策点（文件修改/MCP调用前）加确定性校验层 |
| **治理层可分离** | P0 | 确保SKILL.md/AGENTS.md不绑定Hermes特定语法 |
| **权限层** | P1 | 完善sandbox profile的权限定义 |

**一句话**：核战队已经有了Harness的5/7层。缺的两层（执行钩子+完善权限）补上后，就是完整的Harness实现。
