---
source_url: https://mp.weixin.qq.com/s/vsCbmfP2gZ3l9itbDN_t1g
ingested: 2026-05-21
sha256: 4b547fc83dbe8b91
title: OpenHuman：赶超OpenClaw、Hermes的又一爆火智能体
author: 乔见
source: 微信公众号
level: standard
---

OpenHuman，上周三无意刷到过这个项目 ，当时应该仅有不到 4000 的 Star，今天又看了下，确实很惊人，不到一星期接近 2W 了。这两天网上也开始出现很多介绍这个项目的文章，标题也都非常的夸张、震惊。我的同事今天也在群里转发了，甚至说：有火过 OpenClaw、Hermes 的趋势，抓紧机会提前预研、布局。
所以，我们今天就来快速体验一下OpenHuman，结果确实很震惊！！！ !

先来张OpenHuman 的官方吉祥物，很Q很萌，一下子拉近了距离，而不是科技冰冷的生硬感。
一、项目介绍
项目地址是：https://github.com/tinyhumansai/openhuman

OpenHuman 是一个由 tinyhumansai 团队开源、采用 GPL-3.0 许可证发布的"代理型助手"，官方的介绍是：

OpenHuman 是第一款能在几分钟内快速了解你的智能体管理框架。其设计灵感源自卡帕西（Karpathy）的大语言模型知识库。

绝大多数智能体均为冷启动模式：Hermes通过观察你的工作行为进行学习，OpenClaw 则依靠插件来传递上下文信息。无论采用哪种方式，你都需要花费数天乃至数周时间，才能让智能体充分熟悉你的技术栈，真正发挥实用价值。

意思就是OpenHuman不同于现在市面上现在绝大多数智能体，比OpenClaw 、Hermes更牛逼，不需要花时间去养。它的设计理念是：

让OpenHuman 连接你的账户，自动拉取数据到本地，然后将所有内容压缩为 Markdown 文件，智能存储在一个 Karpathy 风格的 Obsidian wiki 中。仅需一次同步，智能体就拥有了你收件箱、日历、仓库、文档、消息的完整（压缩后的）上下文。正如它的口号： 个人 AI 超级智能。私密、简洁、极其强大。

Claude Cowork、OpenClaw、Hermes Agent、OpenHuman   对比如下：
二、安装配置
安装起来还是比较顺畅的

# Download DMG, EXEs over at https://tinyhumans.ai/openhuman or run in from your terminal

# For macOS or Linux x64
curl -fsSL https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.sh | bash

# For Windows
irm https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.ps1 | iex

安装好后，它的logo长这样，支持很多种语言，包括中文。

使用github的账号来登录

然后你可以选择$1 体验。

也可以自定义；自定义，竟然不支持输入model…… !

接下来选择语音模型，鉴权等，直接下一步。

然后就来到账户首页了 

工具的底部可以看到几个菜单

分别对应首页、助手、对话、记忆、渠道、社区、设置等。
三、正式体验
首先让它做个介绍，看看它能干什么？

它竟然还想管我的钱包……

助手页是下面这样的，可以进行语音对话。 

渠道页面，按照官方的说法，支持118+ 第三方集成 + 自动拉取 

它的左边菜单还可以添加微信

点击微信图标后就这样了

挂了…… 

我无意中切换到主页面，再回来，发现冒出了个二维码让我扫描。

 但是已经超时，页面不支持刷新…… 

只好把它从左边菜单栏先删除，再重新添加…… 

扫描扫描二维码后，授权登录成功。页面跳转提示： 

体验失败！

继续看看它的能力，跟他对话几次，经常没有反应，不知道是 model 的问题还是 agent loop 的问题？它自己也意识到了……。

继续，让它给我写首诗，还是正常的 

但是，但是，我让它把这首诗写到我的某个目录下，生成一个md文件，它竟然……

好吧，无了个大语。

继续体验别的功能吧。记忆模块，包含了潜意识、人物、梦境等

梦境系统，即将推出……。对梦境不了解的小伙伴，可以看看这篇文章 会做梦的AI，才能真正记住你——智能体"梦境系统"完全解析四、设计理念
OpenHuman有很多好的设计理念，比如：

简洁、UI 优先、人性化： 通过清爽的桌面体验和简短的入门流程让你轻松拥有一个桌面吉祥物智能体，会说话、能感知周围环境、可以帮你参加google会议，持续在后台帮你思考。

记忆树 +Obsidian Wiki：基于你的数据和活动构建本地优先知识库，将连接的所有内容都被规范化为不超过 3k token 的 Markdown 片段，兼容Obsidian 的仓库，你可以打开、浏览和编辑。

智能 Token 压缩（TokenJuice）： 每个工具调用、抓取结果等都会经过 token 压缩层进行预处理。比如HTML 被转换为 Markdown，长 URL 被缩短，规则层去重并摘要等等。通过这种方式，token 消耗仅为原来的几分之一。最多可降低 80% 的成本和延迟。

OpenHuman的README里写了一句"Just connect your accounts and let it learn"。但是设计理念归理念，当前的实际体验说实话不太行，体验过过程中遇到的一些问题不是"早期阶段的正常现象"能一笔带过的。

但有一点值得重视：OpenHuman的思路确实跟 OpenClaw、Hermes 不一样，它是"一次性灌入"，把你的邮件、日历、代码仓库、聊天记录一次性压缩成本地知识库，agent 直接拥有你的完整上下文，这确实解决了一个真实痛点：冷启动太慢。

所以我的建议是：
值得关注：它的架构设计和 Token 压缩思路，值得花半小时看看源码和文档，了解这个方向在做什么暂时别着急使用：集成稳定性差、agent 响应不可靠，现在用来当日常工具会经常卡你适合两类人提前布局：在做本地化 AI 助手产品的人，以及对 agent 知识库架构感兴趣的开发者
Star 涨到 2W 不代表产品好用，但确实代表这个方向有人关注。让子弹飞可以，但别闭着眼睛飞。

推荐阅读

100天，36万星，258个漏洞，67%卸载：OpenClaw的神话与裂痕

关于OPC（一人公司），程序员需要知道的9个真相

AI编程新范式| OpenSpec接入老项目完整实战+踩坑记录

