---
source_url: https://mp.weixin.qq.com/s/FGOi7oPvThsq6hvasTuqbQ
ingested: 2026-05-10
sha256: d656232c86927dd23120286ca8c5098ac77d4a8b27e31523207a7b7e6fcb0c60
source: 微信公众号
author: 阿超
original_pub: 微信公众号
description: Hermes Agent 配置详解：从入门到生产部署——面向运维/开发场景的完整配置指南
---

# Hermes Agent 配置详解：从入门到生产部署

一份面向运维/开发场景的完整配置指南，从 Quick Setup 和 Full Setup 两个维度，系统梳理 Hermes Agent 核心配置项。

## 核心概念：两种启动模式

### Quick Setup
命令 `hermes setup` → 选第一项。适用首次安装、快速验证、普通聊天。配置三要素：Provider + Model + Messaging。

### Full Setup
命令 `hermes setup` → 选第二项。适用生产部署、服务器运维、高级集成。配置全部项。

## Quick Setup：三要素

1. **Provider（模型服务商）**：Nous Portal / OpenAI Codex / Anthropic / OpenRouter / Ollama / Custom Endpoint。主模型必须 ≥64K context。
2. **Model（具体模型）**：交互式选择或 `hermes config set model ...` 直接指定。
3. **Messaging（消息平台）**：Telegram / Discord / Slack / WhatsApp / Signal / Email / Home Assistant。`hermes gateway setup` 配置，务必配置 allowed_users。

## Full Setup 详解

### 配置文件结构
```
~/.hermes/
├── config.yaml     # 非敏感配置
├── .env            # API Keys / Tokens
├── auth.json       # OAuth 凭证
├── SOUL.md         # Agent 主身份定义
├── memories/       # 长期记忆
├── skills/         # 技能库
├── cron/           # 定时任务
├── sessions/       # Gateway 会话
└── logs/           # 日志（自动脱敏）
```
配置优先级：CLI 参数 → config.yaml → .env → 内置默认值

### Terminal Backend
local（本机测试）→ Docker（隔离）/ SSH（远程）/ Modal（无服务器）/ Daytona 五级推荐路径。

### Gateway（消息网关）
配置步骤：`hermes gateway setup` → 选平台 → 获取 Token → 配置安全规则。安全建议：allowed_users 白名单 + DM 配对 + DM-only 指令。
