---
source_url: https://mp.weixin.qq.com/s/6uCuiw34bzLRoMl1YzKo4w
sha256: 65244b6f75d926fbe1b1bf83145b6b0152682929a6b90df0970d9f1914c0cf9b
ingested: 2026-05-19
title: 手把手搭一个「AI 同事军团」—— Hermes Agent 多 Profile 实战
author: 烈焰之雨
source: 微信公众号"烈焰之雨空间"
content_type: tutorial
eval_level: 极大
tags: [Hermes Agent, Multi-Profile, 实战, Gateway, 省钱技巧]
---

# 手把手搭一个「AI 同事军团」—— Hermes Agent 多 Profile 实战

> 作者：烈焰之雨，2026年5月15日

## 核心痛点
开发中经常被突然打断。需要一个团队，而不是一个工具。

## 为什么不选 Claude Code / Codex / Cursor
Hermes Agent 的 Profile + Skill + 永久记忆 是其核心差异。

## 架构设计：同一台 Linux 服务器运行3个独立 Gateway
- 小爱马 🐴 — 全能助手（Profile: default）
- 虾仔 🦐 — 全栈开发（Profile: coder）
- 爱老师 🧬 — 研究分析（Profile: research）

三个关键设计：
1. 独立进程，共享基础设施
2. 自建模型网关（HQAI UAT）
3. 会话隔离 + 技能共享

## 省钱技巧：辅助模型白嫖
主模型用 DeepSeek V4 Flash / MiniMax M2.7
辅助模型全部走智谱 GLM 免费系列（glm-4v-flash, glm-4.5-flash, glm-4-flash）

## 目录结构
/media/mydata/linux_home/hermes/
├── .env
├── config.yaml
├── profiles/{default,coder,research}/ 各含 .env + config.yaml + SOUL.md
├── skills/ (共享)
└── memory/ (共享+隔离)

