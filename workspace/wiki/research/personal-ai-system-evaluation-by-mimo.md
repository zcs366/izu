---
title: "个人专属超级AI系统搭建教程评估（MiMo V2.5 Pro产出·极大）"
aliases: ["Mac mini Codex龙虾搭建评估"]
author: "MiMo V2.5 Pro (通过子代理)"
source_article: "微信公众号：个人专属超级AI系统搭建教程"
created: "2026-05-20"
updated: "2026-05-20"
tags: [Codex, 龙虾, OpenClaw, Tailscale, Mac mini, AI服务器, 架构评估]
sources:
  - https://mp.weixin.qq.com/s/wKOdibbEyYU8WbHmgsiLQw
---

# 个人专属超级AI系统搭建教程 — 深度评估

> 由 MiMo V2.5 Pro 评估产出 | 2026-05-20 | 等级：极大

---

**一句话核心判断**：文章提出了正确的四层抽象（用户交互→网关/调度→执行→硬件），但在具体实现上过度简化，对izu用户的价值在于架构思路的启发而非技术细节。

---

## 一、架构评估

### 四层抽象模型（正确之处）

| 层 | 组件 | 职责 |
|----|------|------|
| 用户交互 | 飞书/微信 | 消息入口 |
| 网关/调度 | 龙虾/OpenClaw | 接入、路由、调度 |
| 执行 | Codex CLI/App | 真正干活 |
| 硬件 | Mac mini | 在线主机 |

这个四层拆解**方向是对的**——把"调度"和"执行"分开是规模化Agent系统的必要条件。

### 问题出在哪

**"龙虾只做调度不做执行"的分离设计过于绝对。** 现实中轻任务（查天气、回消息）由网关/龙虾直接处理效率更高，不需要每次都启动一个Codex进程。更合理的应该是"执行能力分层"：轻任务近端处理，重任务远程执行。

## 二、与izu体系的对比

| 维度 | 本文方案 | izu方案 | 谁优 |
|------|---------|--------|------|
| Agent框架 | Codex CLI | Hermes Agent | izu（开源+更灵活） |
| 网关 | 龙虾/OpenClaw | Hermes Gateway（内置） | izu（无需额外组件） |
| 硬件 | Mac mini专用服务器 | WSL（非Mac也可） | izu（更便宜） |
| 安全网络 | Tailscale | Tailscale（通用） | 平手 |
| 模型 | Codex内置 | MiMo V2.5 Pro + DeepSeek | izu（可选更多） |
| 调度 | 手动tmux | Kanban/Dispatcher（自动） | izu |

izu的Hermes Agent + MiMo方案更适合非Mac环境，且组件更内聚。

## 三、批判性分析

### 六大盲区
1. **单点故障** — Mac mini挂了全停，没有备选降级方案
2. **隐性成本** — Mac mini+电费+网络+Codex订阅，长期不比云服务器便宜
3. **安全漏洞** — Tailscale解决了暴露端口问题但没解决Agent本身被攻击
4. **可维护性** — 出错时排障链路长（龙虾→Codex→Mac mini→网络）
5. **用户门槛** — 需要对Mac/SSH/tmux/node都很熟悉的用户
6. **未经验证的假设** — "Codex做执行最佳""龙虾只做调度"都是作者的个人偏好

## 四、izu可直接借鉴的点
1. **AGENTS.md用法** — 给每个项目写说明书
2. **tmux多窗口布局** — codex/gateway/logs/dev/monitor的分屏设计
3. **任务优先级分流** — 轻任务近端处理，重任务远程执行

---

*评估时间：2026-05-20*
