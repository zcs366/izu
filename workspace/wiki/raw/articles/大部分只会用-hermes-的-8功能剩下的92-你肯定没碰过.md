---
source_url: file:///mnt/i/hermes/wiki_dropbox/大部分只会用 Hermes 的 8%功能，剩下的92% 你肯定没碰过.md
ingested: 2026-05-08
sha256: b2db44bebaea59223a71441dc0a33addcfa43cba8de33fa10b6422bd262e7e38
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: **大部分只会用 [Hermes](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Hermes&zhida_source=entity) 的 8%功能，剩下的92% 你肯定没碰过**
---

# **大部分只会用 [Hermes](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Hermes&zhida_source=entity) 的 8%功能，剩下的92% 你肯定没碰过**

> 来源: 大部分只会用 Hermes 的 8%功能，剩下的92% 你肯定没碰过.md（用户存入 wiki_dropbox）

# **大部分只会用 [Hermes](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Hermes&zhida_source=entity) 的 8%功能，剩下的92% 你肯定没碰过**

安装好Hermes之后，接入飞书、选好了模型、打几个 prompt，得到答案，然后就关掉标签页了，完事。

我相信大部分人就是这样使用Hermes的，这么使用的话、说实在的连 **Hermes 的 8%的功能都没发挥出来**。你只是把一个全副武装的 AI Agent，当成了“稍微聪明一点的 ChatGPT”而已

另外 **92%高级功能** — 持久记忆、会话分支、文件回滚、语音模式、17 个平台全覆盖、自定义斜杠命令……全都在那里闲置着。

今天我花了一晚上把**Hermes的这些功能清单，4部分15个功能点，进行了细致的整理，**毫无保留的奉献给大家，让大家充分的挖掘**Hermes 的潜能和价值**。

### **第一部分：你跳过的初始设置**

**1. /personality + [SOUL.md](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=SOUL.md&zhida_source=entity)**
Hermes 启动时会读取 SOUL.md 文件，里面写的内容会永久成为你Agent的“灵魂”和语气。
`/personality` 命令可以随时切换预设人格。
别再每次聊天都打“你是一位资深 X 专家”了，一次性写进 SOUL.md 就行。

**2. MEMORY.md + [USER.md](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=USER.md&zhida_source=entity)**
两个持久化文件，每次会话都会自动读取。

- • MEMORY.md = 项目笔记本
- • USER.md = 关于你的一切信息
  通过 [FTS5](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=FTS5&zhida_source=entity) + LLM 摘要索引，8 周前的记忆也能自动在今天弹出。
  从此不用反复自我介绍。

**3. /insights [天数]**
跨会话分析：消耗了多少 token、用了哪些模型、哪里卡住了、你最常问什么。
输入 `/insights 30` 就能看到过去一个月全貌。



![img](https://pic2.zhimg.com/v2-ccb30d3474f68f2042b8b41e27895e87_1440w.jpg)





**4. /snapshot**
在做高风险操作前保存完整 Hermes 状态。
玩脱了？直接 `/snapshot restore <id>` 回滚。
Agent自己的“时光机”。

### **第二部分：飞行中实时控制**

**5. /branch（别名 /fork）**
像 [Git](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Git&zhida_source=entity) 一样分支会话。想尝试更激进的路径，又不想污染当前上下文？直接分支，不行就切回来。



![img](https://pic2.zhimg.com/v2-d3c9d1f701b4680d08e2b09d9f8820d5_1440w.jpg)

**6. /rollback**
文件系统检查点。Agent把你的代码搞崩了？不用 git，直接 `/rollback` 秒恢复。

**7. /btw**
临时旁白问题，只用当前会话上下文，不调用工具，不保存记录。
真正的“快速确认”命令。

![img](https://picx.zhimg.com/v2-c5c00ef3c1ddec6b1c1c1f14b17e2d09_1440w.jpg)



**8. /steer 和 /queue**
正在跑 3 个工具调用时，突然发现它在生产环境而不是 staging？不用杀进程，直接 `/steer use staging not prod`，下一条工具调用就会看到这条指令，缓存依然是热的。`/queue` 还能排队下一轮而不中断当前流程。

![img](https://pic4.zhimg.com/v2-0958576b89afbdfff37edf1e29b3b5bf_1440w.jpg)



**9. /yolo、/fast、/reasoning**
三个功率开关：

- • `/yolo` 跳过危险命令审批
- • `/fast` 切换到 OpenAI 优先或 [Anthropic](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Anthropic&zhida_source=entity) 极速模式
- • `/reasoning` 调节推理模型的思考深度
  大多数人永远用默认设置，然后抱怨会话慢。

### **第三部分：彻底摆脱供应商锁定**

**10. /model [--provider] [--global]**
一条命令切换模型，无需重启。
支持 Anthropic、OpenAI、OpenRouter、NVIDIA NIM、Kimi、Gemini、AWS Bedrock 等十几家。
可以让重活用 [Opus](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Opus&zhida_source=entity)，轻活用 Kimi，状态无缝继承。

![img](https://pica.zhimg.com/v2-83ee527fbabd9cd5d5ae2372e9790946_1440w.jpg)



**11. 辅助模型**
上下文压缩、会话摘要、标题生成、视觉任务……都可以单独指定不同模型。
主脑用 Opus 4.7，压缩用 [Haiku](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=Haiku&zhida_source=entity) 4.5，标题用小模型。
别再为 Haiku 级别的工作付 Opus 的钱。

### **第四部分：你从未激活的超大触达**

**12. 17 平台网关**
Telegram、Discord、Slack、[WhatsApp](https://zhida.zhihu.com/search?content_id=274391284&content_type=Article&match_order=1&q=WhatsApp&zhida_source=entity)、Signal、Email、SMS、Matrix、飞书、企业微信、钉钉、QQBot、Home Assistant……
一个 Hermes 进程全部搞定。

**13. /voice 实时语音**
支持 CLI、Telegram、Discord 文字/语音频道。
打字 `/voice` 就能直接说话，走路、开车、手上有事时也能用。

![img](https://picx.zhimg.com/v2-68e29ba01cdd65bb212fbdcc67ed619f_1440w.jpg)



**14. Cron + Webhook 订阅**
内置定时任务（支持自然语言）：
“每周五下午 5 点，总结本周 GitHub 提交，发布到 Slack #standups”
配合 webhook 可实现 GitHub、Vercel、Stripe 等事件零延迟推送。
完全免费，不用再花钱买 Zapier。

### **第五部分：把游客和真用户区分开的秘密**

**15. 技能 = 斜杠命令**
100+ 内置技能，全部是 `/` 命令，输入 `/` 自动补全。
你还可以自己写技能。我自己写了 `/sage`，它能自动发现我领域里的异常值、追踪趋势、用我的语气起草推文和线程。
写一次，任何会话、任何平台，永久可用。
游客一周用一次斜杠命令，真用户把整个工作流都写成了斜杠命令。

```text
/architecture-diagram, 
/excalidraw, /manim-video, 
/research-paper-writing, 
/linear, /google-workspace, 
/imessage, /youtube-content, 
/codex, /claude-code, 
/test-driven-development, 
/systematic-debugging.
```

**一句话**：
你花钱买了一个拥有持久记忆、100+ 技能、文件回滚、会话分支、飞行中纠偏、17 平台、实时语音、多模型路由、定时任务、Webhook 和自定义技能的超级Agent……

结果你只把它当成了一个稍微高级一点的 ChatGPT机器人。

**工具没有辜负你，是你从来没有给它真正的指令。**
