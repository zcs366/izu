---
source_url: https://mp.weixin.qq.com/s/LZ20JQng7d92XMvuwnslqg
ingested: 2026-05-07
sha256: c5be39aa8d2c333e1af9aa00cf70ff244bc9b047a70de20c8d908e1b1cf65efd
source: 微信公众号
author: AI 产品 Muke
description: Hermes Agent 安装后前十分钟最值得尝试的十件事，涵盖命令、技能、定时任务、平台接入、人格定制等
---

# Hermes Agent 上手 10 分钟速通指南

作者：Muke（AI 产品 Muke）

## 核心理念

Hermes 是 Nous Research 出品的"会自我进化"的 AI Agent。你用得越久，它越懂你，越能干。安装只要一行命令，但真正发挥威力需要这些技巧。

## 上手十件事

### 1. 让它操作你的电脑
装好后别只聊天：`What's my disk usage? Show the top 5 largest directories.` 它直接跑终端命令、解析结果、给报告。

### 2. 斜杠命令（/）
输入 `/` + Tab 查看所有命令：`/help` `/tools` `/model` `/personality` `/save` `/skills` `/voice` `/compress`

### 3. 多行输入：Alt+Enter
粘贴代码、写邮件时按 Alt+Enter 换行，整段发送不拆条。

### 4. Ctrl+C 中断
按一次中断当前任务，两秒内按两次强制退出。AI 跑偏是常态，能随时打断才是真生产力。

### 5. 跨会话延续
```bash
hermes -c              # 恢复最近对话
hermes -r "研究项目"   # 按标题恢复
```

### 6. 图片直接粘贴
Ctrl+V 从剪贴板直贴图片，不需要先保存再上传。用于调试 bug、看 UI 设计图、解析图表。

### 7. 接入消息平台
```bash
hermes gateway setup
```
交互式配置，选平台、填 token，5 分钟搞定。支持 15+ 平台。可用手机调度服务器上的 Hermes。

### 8. 定时自动化任务
自然语言描述定时任务：`Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.` 自动配置 cron + 跨平台推送。

### 9. 安装技能
```bash
hermes skills search react
hermes skills install official/security/1password
```
或在对话中让 AI 搜。技能是它的第二记忆，自动学习和复用流程。

### 10. AGENTS.md 项目上下文
在项目根目录建 AGENTS.md，注入项目规则到每次对话的系统提示：
```markdown
- 这是 FastAPI 后端项目
- 数据库用 async SQLAlchemy
- 测试用 pytest-asyncio
```

### 11. 编写个性化人格（Personality）
创建人格文件，用 `/personality 我的助手` 切换。定义说话风格、优先级、行为准则。

## 核心理念

记忆系统、技能系统、用户模型都是为长期使用设计——越用越强。
