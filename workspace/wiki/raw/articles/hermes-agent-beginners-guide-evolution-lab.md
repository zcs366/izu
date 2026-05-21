---
source_url: https://mp.weixin.qq.com/s/cBzdfaae43AvPfW3I8-MPw
ingested: 2026-05-07
sha256: 0373010db5a119166911cfe338e4f372f12c94545e3e49bf3f96b5affa7dfbc8
source: 微信公众号
author: 进化的实验室
description: 面向所有人的 Hermes Agent 安装、配置与实战教程，覆盖 CLI/Web UI/多平台接入/定时任务/技能系统
---

# Hermes Agent 零基础安装配置实战教程

作者：进化的实验室

## 什么是 Hermes Agent

Nous Research 开源的 AI Agent 框架。不是"问一句答一句"的普通助手——能记住你是谁、能执行代码、能操作文件、能浏览网页、能定时执行任务、能同时出现在 10+ 平台。

## 与同类对比

| 特性 | Hermes | Claude Code | OpenClaw | Codex |
|---|---|---|---|---|
| 跨会话记忆 | ✅ 自动 | ⚠️ 部分 | ✅ | ⚠️ 部分 |
| 定时任务 | ✅ | ❌ | ✅ | ❌ |
| 多平台消息 | ✅ 10+ | ⚠️ 预览中 | ✅ 15+ | ❌ |
| Web UI | ✅ | ❌ | ⚠️ | ❌ |
| 自我进化技能 | ✅ | ❌ | ⚠️ | ❌ |
| 多模型支持 | ✅ 20+ | ❌ 仅 Claude | ✅ | ✅ |

## 安装配置

### 一键安装
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 配置向导
```bash
hermes setup
```

## 推荐模型配置
- 日常 → Claude Sonnet（性价比最高）
- 编程 → Claude Opus（最强编程）
- 快速问答 → GPT-4o-mini（便宜快速）
- 中文优化 → DeepSeek Chat（效果好价格低）
- 本地运行 → Llama 3 via Ollama（免费隐私保护）

## Web UI
```bash
# 安装
hermes webui setup
# 启动
hermes webui start
```
三栏布局：左侧会话列表、中间聊天、右侧文件浏览。手机通过 Tailscale 可远程访问。

## 核心功能
- 持久化记忆（MEMORY.md + USER.md）
- 技能系统（自动创建和自我改进）
- 定时任务（自然语言描述 cron）
- 多平台消息（Telegram/Discord/Slack/微信等）
- 多 Agent 协作（调用 Claude Code 等子进程）
