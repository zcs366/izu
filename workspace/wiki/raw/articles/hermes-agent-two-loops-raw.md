---
source_url: "https://mp.weixin.qq.com/s/6vzpCymHVGOSkoWa3VBbDg"
title: "Hermes Agent 中的两套 Agent Loop"
author: "钱sir AIGC"
source: "微信公众号"
ingested: 2026-05-17
sha256: "pending"
---

# Hermes Agent 中的两套 Agent Loop

## 核心要点

Hermes Agent 源码中同时存在两套 Agent Loop：

- **`AIAgent`**（位于 `run_agent.py`）——面向用户实时交互
- **`HermesAgentLoop`**（位于 `agent_loop.py`）——面向 RL rollout（由 Atropos 调用）

两者都执行"模型调工具→继续推理"的基本循环，但服务的运行场景和控制逻辑完全不同。作者明确指出：**"拆分不是为了拆分而拆分，根本是因为两个场景本来就不是同一个问题。"**

## 设计原则

> "用户交互系统优化的是体验、鲁棒性和可恢复性；RL rollout 优化的是吞吐、并发和训练信号精度。它们都叫 Agent Loop，但回答的不是同一个工程问题。"

> "更具参考价值的做法，反而是把系统拆成两层：
> - **上层按场景定义各自的循环控制策略**
> - **下层复用工具调度、结果存储和共享基础设施**"

## AIAgent（用户交互路径）

- **入口**：CLI、Gateway、Telegram、Discord 等直接面向人的接口
- **关注点**：交互过程的健壮性与用户体验
- **包含**：流式输出、Provider 容错、上下文压缩、用户中断、预算耗尽后的 Grace Call、子 Agent 委派、插件钩子
- **复杂度**：数千行代码

## HermesAgentLoop（RL rollout 路径）

- **调用者**：Atropos（训练框架），不面向用户
- **关注点**：高性能、低开销、训练信号精确
- **必须满足**：
  - `async` 实现，支持并发大量 rollout
  - 获取真实 `token`、`logprobs`、`masks`，供 GRPO 训练使用
  - 工具执行与 reward 验证在同一个 sandbox 上下文中
  - 循环本身足够轻，避免交互分支干扰训练路径

## 为什么不合成一个超级 Loop？

- 若将 `AIAgent` 的交互逻辑放入训练 rollout，无用且增加开销
- 若将 `HermesAgentLoop` 的轻量控制流用于用户交互，缺少错误恢复和用户体验逻辑
- **强行融合会导致 Loop 复杂度极高、可靠性降低**

## 复用策略

- **不复用**：循环体本身（loop policy）
- **复用**：底层工具调度层（如 `handle_function_call()`）、预算控制、持久化等基础设施

## 设计启示

| 层面 | 做法 |
|------|------|
| 上层（场景层） | 定义各自的循环控制策略，按目标函数优化 |
| 下层（基础设施） | 共享工具调度、结果存储、预算管理等 |

**核心思想**：只要场景的目标函数已经变了，循环层通常就不该强行共用。
