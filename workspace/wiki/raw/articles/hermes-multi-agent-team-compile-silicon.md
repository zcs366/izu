---
source_url: https://mp.weixin.qq.com/s/xU2S7bTJGKpLoprgxq0g2Q
ingested: 2026-05-07
sha256: 40c8e5b959661ed050d0d403b1887b945eeab513974f1007e779a135bb4985c0
source: 微信公众号
author: 编译硅基
description: 从零搭建多 Agent 小队：Profile 机制原理、安装配置、调教过程，实战构建副官/coder/军师/老司机四个独立 Agent
---

# 从 0 搭建自己的多 Agent 小队：四大 Profile 实战

作者：编译硅基

## 核心理念

> 一套配置服务不了所有需求。术业有专攻，每个角色给独立的 profile、独立的配置、独立的模型、独立的人设、独立的记忆空间。

## Profile 文件结构（实战示例）

```
~/.hermes/
  .env                     ← main profile 的 token
  config.yaml              ← main 模型配置
  SOUL.md                  ← main 人格定义
  profiles/
    coder/
      .env / config.yaml / SOUL.md / gateway.pid / logs/
    master/
      .env / config.yaml / SOUL.md / gateway.pid / logs/
    olddriver/
      .env / config.yaml / SOUL.md / gateway.pid / logs/
```

每个 profile 有完整的配置副本，跑在物理级别隔离的 gateway 进程里。不同 profile 使用**不同的 Telegram bot token**，用 `--clone` 参数一键复制基础配置。

## 四大 Agent 角色设计

### 1. 副官（日常管家）
- 职责：日常消息、提醒、信息整理、调研、查资料
- 人设：口语化、反应快、靠谱的朋友
- 用法：随手问问题、记想法、文章链接丢给它解析存 Obsidian

### 2. Coder（代码 Agent）
- 职责：代码实现、debug、代码审查、技术方案、git 工作流
- 人设：资深软件工程师，严格遵循软件工程范式
- 核心：先做 plan，后实现，充分单元测试，多步提交发 PR review
- 模型推荐：Codex、Claude Opus

### 3. Master（古风军师）
- 职责：奇门遁甲、八字分析、运势参考、择吉
- 人设：卧龙先生转世，精通天文地理、梅花易数
- 模型推荐：DeepSeek / Qwen（古文理解好）或 Opus / Gemini（解卦稳）

### 4. Old Driver（深夜老司机）
- 职责：深夜陪聊、成人话题、情感释放
- 人设：深夜伴侣，会讲情话
- 模型推荐：**Grok**（成人话题自由度远超其他模型）

## 关键步骤

1. BotFather 创建 N 个独立 bot，拿到 N 个 token
2. `hermes profile create <name> --clone` 创建 profile
3. `<name> setup` 分别配置（token 必须一一对应）
4. 验证 token：`grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/profiles/<name>/.env`
5. `<name> gateway start` 各自启动
6. 配置各自的 SOUL.md 定义人设

## 注意事项

- `--clone` 会复制主 profile 全部配置含 skill 软链接，可能卡住需排查
- 不同 profile 必须对应不同 bot token（Hermes 有 token 锁机制）
- 每个 profile 跑独立的 gateway 进程
