---
title: GenericAgent
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [agent, automation, enterprise, os-level]
sources:
  - raw/articles/genericagent-hermes-enterprise-combo.md
confidence: medium
---

# GenericAgent

一个专注于操作系统层面直接控制的轻量开源 AI Agent，核心代码约 3000 行。与 [[Hermes Agent]] 互补，组成从底层执行到顶层编排的企业自动化基座。^[raw/articles/genericagent-hermes-enterprise-combo.md]

## 核心设计

### 9 个原子工具

GenericAgent 通过 9 个原子工具实现 OS 级操控，不依赖 API 对接：

| 工具 | 能力 |
|------|------|
| 代码执行 | 在本地/远程环境运行脚本 |
| 文件读写 | 读取、写入、管理文件系统 |
| 浏览器注入 | 直接操控浏览器 DOM 和页面交互 |
| 键鼠控制 | 模拟鼠标点击、键盘输入 |
| 屏幕视觉识别 | 截图 + 视觉模型识别界面元素 |
| ADB 移动端控制 | 通过 ADB 控制 Android 设备 |

### 分层记忆架构（L0-L4）

上下文控制在 **30K 以内**，关键信息保留在当前层，历史知识下沉到长期记忆层，噪声主动过滤。相比动辄 200K-1M 上下文窗口的方案，幻觉更少、成本更低。^[raw/articles/genericagent-hermes-enterprise-combo.md]

### 自我进化

每完成一个新任务，自动将执行路径固化为 Skill 存入分层记忆系统。下次同类任务一句话即可调用。

## 与 Hermes 的互补关系

| 能力 | GenericAgent | Hermes Agent |
|------|-------------|-------------|
| 执行深度 | OS 级（浏览器/桌面/移动端） | 工具集 + MCP 生态 |
| 平台覆盖 | 无 API 的系统通过 GUI 兜底 | 15+ IM 平台统一网关 |
| 技能管理 | 自身 Skill 自动固化 | 全局技能图书馆 + 共享复用 |
| 上下文 | 30K 分层记忆 | 上下文压缩 + 智能模型路由 |
| 审批流 | ask_user 执行层断点 | 人机协作审批流 + 超时自动拒绝 |

**协作模式：** Hermes 负责需求拆解、任务分发、平台对接、技能沉淀——像项目经理；GenericAgent 负责直接操控操作系统执行——像一线工程师。^[raw/articles/genericagent-hermes-enterprise-combo.md]

## 核心优势

- **轻量**：~3000 行核心代码，不依赖重型框架
- **无 API 依赖**：通过 GUI 操控绕过接口限制
- **人机共融**：ask_user 工具在关键步骤主动暂停，等待人工确认
- **成本可控**：30K 上下文 + 分层记忆，Token 消耗低

## 相关条目

- [[hermes-agent]] — 上层编排与调度
- [[agent-skills-system]] — Hermes 的技能管理体系，与 GenericAgent 的自我进化互补
