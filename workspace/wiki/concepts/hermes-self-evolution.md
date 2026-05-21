---
title: Hermes Agent 自进化机制
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [hermes, agent, evolution, learning]
sources:
  - raw/articles/hermes-agent-self-evolution-yiqi.md
  - raw/articles/hermes-agent-intro-kim-surely.md
confidence: medium
---

# Hermes Agent 自进化机制

[[Hermes Agent]] 的"自进化"通过两条并行路径实现：**在线经验沉淀**（上下文层）和**离线 RL 训练**（训练数据层）。前台即时响应，后台异步进化。

## 在线路径：越用越顺手

### 1. System Prompt 分层构建

`_build_system_prompt()` 构建稳定层（缓存前缀），按序装载：Agent 身份 → memory 指导 → skill 指导 → 冻结 memory 快照 → 冻结 user profile → skills 索引 → 项目上下文文件。

临时层只在当前 API 调用前注入（外部 memory recall 结果等），不回写消息历史。缓存前缀保持稳定，推理成本可控。

### 2. Memory 精选记忆机制

内建记忆系统维护两本文件：
- **MEMORY.md**（~800 Token）：环境事实、项目约定、工具怪癖、踩坑记录
- **USER.md**（~500 Token）：用户偏好、工作方式、沟通习惯、反复纠正过的要求

两者在 session 开始时冻结成快照。Mid-session 写入即时落地到磁盘，但不改变当前 system prompt——保持缓存前缀在整个 session 内稳定。

### 3. Skill 自动生成

复杂任务完成后，后台独立 Agent 自动复盘：哪些步骤走错了？可复用模式？固化为 SKILL.md 技能文件。下次类似任务直接调用，Token 消耗降低。

[[agent-skills-system]] 中的 skill_view/skill_manage/manage_skills 等 tool 支持模型在对话中查看、调用、管理技能。

### 4. Cron 周期性推动

内置 cron 调度器，Agent 可主动发消息：每日摘要、定期搜索、监控变化。比被动响应更进一步——Agent 有"日程意识"。

## 离线路径：深层进化

rollout 数据导出为 trajectory → verifier + reward 函数验收 → 带 token 级信号的数据送 Atropos 训练框架。实现"经验→模型权重"的深层进化。

## 双路径对比

| 维度 | 在线（Skill/Memory） | 离线（RL） |
|------|---------------------|-----------|
| 生效速度 | 即时 | 需训练周期 |
| 作用范围 | 单 session/技能级 | 模型权重级 |
| 透明性 | 用户可审阅编辑 | 黑盒优化 |
| 存储形式 | markdown 文件 | 模型参数 |

## 参见

- [[hermes-agent]] — Hermes Agent 主体
- [[hermes-agent-memory-system]] — 多层记忆架构（含冻结快照）
- [[agent-skills-system]] — 技能系统（含自动生成与复盘）
