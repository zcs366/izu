---
source_url: https://mp.weixin.qq.com/s/uq9GSVT36LqhaaiE7L33IQ
ingested: 2026-05-07
sha256: 642a95ee6c302bdabc9a39924f92cd2bf251867cc75055377cbaae285d5037cd
source: 微信公众号
author: 土著哥聊AI
description: Hermes 的 15 个被大多数人忽视的特性，按对产出的影响程度排名，涵盖 SOUL.md/MEMORY.md/insights/branch/rollback/voice/cron 等
---

# Hermes 15 个被忽视的特性：告别纯聊天，激活全部潜能

作者：土著哥聊AI

## 大多数人完全跳过的设置阶段

### 1. /personality + SOUL.md
Hermes 启动时固定读取 SOUL.md，跨越每一个会话。写一次，定义说话方式、拒绝什么、为谁工作。用 `/personality` 可在对话中途切换预命名人格。

### 2. MEMORY.md + USER.md
- MEMORY.md：Agent 的笔记本，自动记录项目重要信息
- USER.md：它对你的了解（角色、语气、决策偏好）
- FTS5 + LLM 摘要器可将 8 周前的记忆提取到今天的会话

### 3. /insights [days]
跨越所有会话的数据分析：哪个项目消耗最多 token、哪些模型花了多少钱、Agent 在哪里卡住。

### 4. /snapshot
在执行危险操作前保存整个 Hermes 配置和状态快照，可用 `/snapshot restore` 恢复。

## 很少人理会的执行控制权

### 5. /branch (别名 /fork)
对当前会话分支处理，探索不同路径而不丢失原始内容——"对话的 git"。

### 6. /rollback
文件系统检查点。Agent 破坏性编辑搞崩代码？直接用 `/rollback` 恢复，不用 git。

### 7. /btw
临时的附加问题，利用当前上下文但不调用工具、不持久化。快速直觉验证，不污染主线程。

### 8. /steer 与 /queue
- `/steer`：不中断当前回合的情况下修正方向
- `/queue`：将下一回合排入队列，保持提示词缓存热启动

### 9. /yolo、/fast、/reasoning
- `/yolo`：跳过所有危险命令审批（慎用）
- `/fast`：切换到快速模式获得更低延迟
- `/reasoning`：设置推理力度级别

## 模型无关

### 10. /model [--provider] [--global]
一个命令切换 Agent 背后的模型，状态无缝继承。支持 Anthropic / OpenAI / OpenRouter / Kimi / Gemini 等。

### 11. 辅助模型（Auxiliary models）
为主力、上下文压缩、标题生成分别分配不同模型。`hermes model` 配一次，辅助界面处理剩下的事。

## 无人激活的到达能力

### 12. 17 个平台的 Gateway
Telegram / Discord / Slack / WhatsApp / Signal / Email / SMS / Matrix / 飞书 / 微信 / 钉钉等。

### 13. /voice（4 个平台的实时语音）
CLI / Telegram DMs / Discord 语音频道中直接语音对话。

### 14. Cron + /webhook-subscriptions
自然语言编写定时任务，自动跨平台投递。搭配 webhook 订阅，外部服务直接推送到消息频道（零 token 成本）。

## 高阶用户的杀手锏

### 15. Skills = 斜杠命令
开箱 100+ skills，每个支持 `/` 自动补全。重度用户把整个工作流构建在斜杠命令中。
