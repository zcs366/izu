---
title: SOUL.md
created: 2026-05-07
updated: 2026-05-07
type: concept
tags: [agent, tool, configuration]
sources: [raw/articles/hermes-agent-soulmd-tony-simons.md]
confidence: medium
---

# SOUL.md

SOUL.md 是 [[Hermes Agent]] 实例的核心身份文件（core identity file），定义了代理的**身份、语气、个性、沟通方式、直接程度、分歧处理和模糊问题的默认处理方式**。Hermes 官方文档将其定位为实例的灵魂文件。

## 起源

由独立开发者 [[tony-simons]] 在其 170 行的 SOUL.md 实践中系统化。他认为"大部分 AI 提示词写'你是一个有帮助的助手'——'有帮助'太模糊了"，需要一份明确界定角色和协作规则的文件。

## 七大核心模块

| 模块 | 核心要求 | 英文原文摘录 |
|---|---|---|
| **身份定义** | 自主操作者和思考伙伴 | "autonomous operator and thought partner" |
| **主动性** | 不等命令，主动推动 | "surface opportunities, flag problems, push work forward" |
| **反驳规则** | 强硬反驳但带证据 | "push back aggressively... every objection with evidence" |
| **责任闭环** | 输出无行动则改进 | "feedback loop is broken" |
| **场景化语气** | 私下直接，公开克制 | 私下：unfiltered / 公开：like someone who builds things |
| **任务地图** | 明确当前目标与优先级 | 列出活跃/停滞项目清单 |
| **授权边界** | 红线极简，其他自主执行 | 发布/购买/破坏需批准，其余直接行动 |

## 核心哲学

> AI Agent 的差距不在模型能力，而在**协作协议的清晰度**。一份写清楚身份、边界、任务地图和反驳规则的文件，可能比多接三个 API 更有用。

## 相关条目

- [[hermes-agent]] — 承载 SOUL.md 的 Agent 系统
- [[tony-simons]] — SOUL.md 实践的系统化推动者
