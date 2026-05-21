---
title: Hermes Agent v0.13.0 韧性版（Tenacity Release）
created: 2026-05-15
type: concept
tags: [hermes, version, kanban, goal, recovery, security]
sources:
  - raw/articles/hermes-v0.13.0-tenacity-20260509.md
confidence: high
---

# Hermes Agent v0.13.0 · 韧性版

2026年5月，[[Hermes Agent]] 发布 v0.13.0，代号「韧性（Tenacity）」。核心理念：**Agent now finishes what it starts.** 解决两大痛点：任务中途卡死、多轮对话跑偏。

## 四大模块

### 1. Kanban · 多智能体看板（核心）

持久化多 AI 协作看板，多个 Worker 并行领任务、分工合作。

**三层保障机制：**

| 机制 | 作用 |
|------|------|
| **心跳检测** | Worker 定期上报状态，死亡自动感知 → 任务回收重分配 |
| **僵尸检测** | 卡死 Worker 直接踢出，不阻塞队列 |
| **幻觉门控** | Worker 声称"完成"但无证据 → 拦截要求补充 |
| **独立重试配额** | 每任务单独配置最大重试，不无限消耗 |

**理想场景**：Orchestrator 拆需求 → 创建任务 → 多个 Worker 并行 → 汇总。原本靠大量手工协调的流程被标准化。

### 2. /goal · Ralph Loop 目标锁定

`/goal 目标` 锁定一个任务目标。无论中间聊多少岔路，Agent 持续追踪目标状态。从"一次性回答问题"变成"持续跟进一个项目"。

**微信场景特有价值**：用户在微信上灵感闪现频繁打断 Agent，/goal 让 Agent 不被带跑。

### 3. Recovery · Checkpoints v2

- Gateway 崩溃 → 重启后对话自动续上
- `/update` 重启 → 保留 pending 状态
- 线程路由 restart 前后一致
- 检查点剪枝 + 磁盘用量上限

### 4. 8 个 P0 安全修复

- 敏感信息自动脱敏（API key/password/token 运行时过滤）— 默认开启
- Discord 角色白名单修复（CVSS 8.1）
- WhatsApp 默认拒绝陌生人
- Cron 任务提示词注入扫描

## 对张成市的价值

**Kanban → izu Pipeline 天然适配**：探×2→搜×2→织→审的七智能体流水线可直接用 Kanban 编排。当前靠 `delegate_task` 手动协调，升级到 Kanban 可得：自动重试、幻觉门控、崩溃恢复。

**/goal → 微信场景刚需**：用户常在微信上打断 Agent。Ralph Loop 让 Agent 不被带跑。

**Recovery → WSL 环境稳定器**：WSL 偶发崩溃，自动恢复省掉反复解释上下文。

**安全加固 → 结合供应链投毒事件**：敏感信息自动脱敏 + 提示词注入扫描，对当前威胁态势有直接价值。

## 升级命令

```bash
hermes update
```

## 相关

- [[hermes-kanban-workflow]] — Kanban 工作流详解
- [[hermes-security-model]] — 安全模型
- [[hermes-agent]] — 承载系统
- [[song-jingze]] — 来源作者
