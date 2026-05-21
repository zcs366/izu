---
tags:
  - personal-ai-server
  - architecture
  - infrastructure
related_entities:
  - qinlao-shulan-tongxue
  - Hermes Agent
related_concepts:
  - agent-skills-system
  - hermes-agent-memory-system
status: active
created: 2026-05-20
---

# 个人AI工作站（Personal AI Workstation）

## 核心定义

个人AI工作站是一套**软硬一体的、个人专属的、可远程访问的AI计算系统**，核心架构为：
- **移动端（操作层）**：笔记本/手机——发号施令、编写代码、远程控制
- **固定端（执行层）**：常驻在家的mini主机/服务器——跑Agent、长任务、自动流程
- **网络层**：VPN/ZeroTier/Tailscale——安全远程访问
- **Agent引擎**：Codex / Hermes Agent / OpenCLI——负责具体干活
- **网关/调度层**：OpenClaw / 飞书机器人 / webhook——消息入口和任务分发

## 核心理念

**分层不是功能分层，而是时空分层。** 移动端管人在哪里，固定端管任务跑哪里，网关管消息从哪里来。三者不需要在一起，甚至不需要同时在线。

## 发展历程

### 第一代：单机方案（2024以前）
所有工作在一台电脑上完成。问题：关机断网所有Agent停摆。代表：直接跑在笔记本上的各种AI工具。

### 第二代：双机分布式（2025-2026）
移动端控制 + 固定端执行。代表：
- **Mac方案（勤劳的树懒同学）**：MacBook（操作）+ Mac mini（执行）+ Tailscale（网络）
- **WSL方案（张成市）**：Windows笔记本/台式（操作）+ WSL Linux（执行）+ Hermes Gateway（调度）

### 第三代：多云/多端（未来）
多个执行节点，异地备份，自动容错。

## 代表方案比较

| 维度 | Mac方案（勤劳的树懒） | WSL方案（张成市） |
|------|-------------------|----------------|
| 操作端 | MacBook | Windows笔记本/台式 |
| 执行端 | Mac mini | WSL / LM Studio |
| 网络 | Tailscale | Tailscale（计划中）/ 直连 |
| Agent引擎 | Codex CLI | Hermes Agent |
| 网关 | OpenClaw（龙虾） | Hermes Gateway（多平台） |
| 任务保持 | tmux | terminal(background=true) |
| 项目规范 | AGENTS.md | _workspace.md / AGENTS.md |
| 记忆系统 | OpenClaw memory | Hermes Memory + Holographic Memory |
| GPU | Mac mini内置GPU | 22GB VRAM NVIDIA |
| 模型推理 | 云端API为主 | 本地LM Studio + 云端API |

## 关键洞察

两个方案殊途同归：**AI系统需要物理层的时空分离**才能持续运转。人带着笔记本移动是不可避免的物理限制，但AI work不能随着人移动而中断。解决方案不是造更好的笔记本，而是把"控制"和"执行"分开，用网络连起来。

这与分布式系统的古老智慧一脉相承：分离关注点（Separation of Concerns）。在AI时代，分离的是**人的所在位置**与**计算的发生地点**。

## 与izu的关系

izu的哲学基础（明学七则）天然支持这种架构：
- **「辨」** — 辨明控制端与执行端的不同职责
- **「时中」** — 移动端做移动端的事，固定端做固定端的事
- **「以乐为终」** — 人不被固定在一台机器前，AI在后台自主运转

## 实践建议

### 对WSL用户的借鉴
1. **AGENTS.md → _workspace.md** 的映射：每个项目建立行为规范文件，让Agent进入即知规矩
2. **tmux → terminal(background)**：Hermes原生支持后台进程，无需tmux
3. **Tailscale零信任网络**：关闭公网端口，全部走VPN
4. **双机思维**：Windows做操作界面，WSL/LM Studio做计算后端——你已经有了这个架构，只是没命名

## 参考
- [[personal-ai-server-mac-mini-codex]] — raw原文
- [[qinlao-shulan-tongxue]] — 作者
- [[hermes-agent-memory-system]] — 记忆系统对比
