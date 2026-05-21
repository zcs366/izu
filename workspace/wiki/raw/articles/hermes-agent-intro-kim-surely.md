---
source_url: https://mp.weixin.qq.com/s/E3J_pjFCmhDjXkNIyzyKEg
ingested: 2026-05-10
sha256: ae04f6afb3ad63f41fc06b9a463635ef20b149e7794f34ab5d9eec9a79adeb11
source: 微信公众号
author: Kim_Surely
original_pub: 微信公众号
description: Hermes Agent（爱马仕）核心特色介绍——越用越懂你的 AI 智能体
---

# Hermes Agent（爱马仕）核心特色介绍

## 一、自进化大脑：越用越聪明

### 1. 持久记忆系统
MEMORY.md（约800 Token）存储项目环境、踩坑记录、关键约定。USER.md（约500 Token）存储用户画像、偏好、沟通习惯。两个文件在每次会话开始时自动注入，历史会话存储在本地 SQLite，支持全文搜索。

### 2. 技能自生成机制
复杂任务完成后，后台 Agent 自动复盘：哪些步骤错了？可复用的模式？固化为 SKILL.md？下次遇到类似任务直接复用。

### 3. 双路径进化闭环
动态 Skill 生成（即时生效）+ RL 训练闭环（深度优化）。"前台即时响应、后台异步进化"。

## 二、无处不在的连接能力

### 全平台消息接入
原生支持 15+ 平台：飞书、钉钉、企业微信、Discord、Slack、Telegram、WhatsApp、Signal。微信通过 HermesClaw 桥接。

### 丰富工具调用
内置 40+ 基础技能，覆盖终端、文件、网页、浏览器、GitHub、MLOps 等。

### 子Agent 并行作战
复杂任务自动拆解派发，各自独立上下文互不干扰。

## 三、工程落地能力

### 低门槛部署
5美元/月 VPS 可跑。支持：本地/WSL2、Docker、SSH 远程、Modal 无服务器、腾讯云/阿里云一键镜像。

### 多模型切换
支持 20+ 模型商：OpenAI、Claude、Kimi、智谱GLM、MiniMax、通义千问、DeepSeek、Ollama、HuggingFace。国产模型无需代理。

### Cron 定时自动化
自然语言配置周期性任务："每天早上8点抓取技术新闻发到我的Telegram"。
