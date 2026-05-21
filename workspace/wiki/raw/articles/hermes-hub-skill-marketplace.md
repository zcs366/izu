---
source_url: https://mp.weixin.qq.com/s/LpHBQ4UT3lfJRIGizxjxVw
ingested: 2026-05-10
sha256: 2adf370c4b13d41f2ec921f30d1376f42227c3dbc4ac9306a4bf11c57ba56612
title: Hermes Agent 上线 Skill Hub：647个技能，直接用
author: 寒哥AI
description: HermesHub 技能市场上线，647个技能，4个注册源，兼容OpenClaw
---
Hermes Agent 的技能市场正式开张了。

5月6日，Nous Research 官方宣布 HermesHub 技能市场正式上线。目前已收录 647个技能，横跨4个注册源，动动手指就能安装。
先说 Hermes Agent 是什么
Hermes Agent 是 Nous Research 推出的 AI Agent 产品。

和 OpenClaw 一样，Hermes 能通过自然语言指令操控电脑、完成复杂任务——帮你管文件、发消息、操作软件、跑自动化流程。

它最大的特点：技能（Skill）系统。

你可以通过写一个 SKILL.md 文件，把任何工作流程封装成可复用的技能，让 AI 在执行任务时调用。

OpenClaw 的技能系统，其实就是从 Hermes 这套思路借鉴来的。
HermesHub 是什么
HermesHub 就是 Hermes 的技能市场。

网址：https://github.com/amanning3390/hermeshub

核心特点：
• 647个技能，持续增加中• 4个注册源聚合（包括 skills.sh、GitHub 等社区源）• 安全扫描：每个技能都经过安全检测• 开放标准：技能用 SKILL.md 格式，完全开放• 一键安装：通过 CLI 命令直接安装怎么安装技能
在 Hermes Agent 里安装技能，命令很简单：

    
    
    
  # 搜索某个技能
hermes skill search <关键词>

# 安装
hermes skill install <技能名>

# 查看已安装列表
hermes skill list
技能装好之后，在对话里直接提需求，Hermes 会自动调用对应技能执行。
技能市场意味着什么
AI Agent 刚出来的时候，大家都在拼模型能力——谁的模型强，谁的 Agent 就强。

但真正的战场，正在从"模型"转向"技能生态"。

就像手机的价值不在于芯片，而在于 App Store。AI Agent 的价值，也在于背后有多少人帮你写好了技能。

HermesHub 上线，意味着：

技能可以流通了。

以前你花三天写的一个自动化脚本，现在可以打包成技能发布到市场，别人一键安装就能用。你不用重复造轮子，AI 也不用每次从零学起。
和 OpenClaw 的关系
这里有个有意思的事。

OpenClaw 的技能格式 SKILL.md，和 Hermes 的技能格式几乎一模一样。两套系统可以互相兼容——在 HermesHub 上找到的技能，很多可以直接装到 OpenClaw 里。

前面我们演示过，把李继刚的 ljg-skills 迁移到 OpenClaw 全程不到一分钟，靠的就是这套格式的通用性。

技能生态正在形成合力。
最后说一句
AI Agent 这条路，走到今天，模型能力的差距已经在缩小。

真正的护城河，是谁家的技能更多、更好用、更好找。

HermesHub 上线，算是给这个趋势按了一个加速键。

想试 Hermes Agent 的，现在可以直接去 GitHub 逛逛，647个技能里，总有几个能解决你实际问题的。

关注我的公众号，

关注我的公众号，

限时获取《Openclaw和Hermes部署手册》

每日还有AI前沿资讯、实操技巧与行业干货～

