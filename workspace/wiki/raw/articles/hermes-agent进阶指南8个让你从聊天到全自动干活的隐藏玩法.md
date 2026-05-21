---
source_url: file:///mnt/i/hermes/wiki_dropbox/Hermes Agent进阶指南：8个让你从聊天到全自动干活的隐藏玩法.md
ingested: 2026-05-09
sha256: a70804f24383f13fa8936ef35bec004adb050d95c5b0932685a62e2e8e3e1370
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: Hermes Agent进阶指南：8个让你从"聊天"到"全自动干活"的隐藏玩法
---

# Hermes Agent进阶指南：8个让你从"聊天"到"全自动干活"的隐藏玩法

> 来源: Hermes Agent进阶指南：8个让你从聊天到全自动干活的隐藏玩法.md（用户存入 wiki_dropbox）

# Hermes Agent进阶指南：8个让你从"聊天"到"全自动干活"的隐藏玩法

[![大模型爱好者社区](https://pic1.zhimg.com/v2-7562bc71f2ce974a5c90665841c73cbd_l.jpg?source=32738c0c&needBackground=1)](https://www.zhihu.com/people/lao-q-84)

[大模型爱好者社区](https://www.zhihu.com/people/lao-q-84)

大模型算法专家｜更多内容见公众号：机器学习社区

你用Hermes多久了？如果超过一周，你大概已经发现一件事，这玩意跟ChatGPT最大的区别不是能跑终端命令，也不是能搜索网页，而是它能**记住东西**，并且**自己长大**。

但大多数人装好Hermes之后，还停留在"跟它聊天"的阶段，问一个问题，得到一个回答，关掉窗口。然后跟朋友说"我试了，感觉跟ChatGPT差不多啊"。

差远了。

这篇文章我要聊的是那些**用了一周之后才会意识到的进阶玩法**，那些让你从"跟AI聊天"变成"让AI替你干活"的关键机制。

![img](https://pica.zhimg.com/v2-f5d5e94c53b1e47228e9d41c27013e3a_1440w.jpg)

### **一、[SOUL.md](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=SOUL.md&zhida_source=entity)：给你的Agent装上灵魂**

Hermes启动后第一件事不是跟你聊天，而是读一个叫`SOUL.md`的文件。

这个文件是Agent的"人格定义"，每次对话都会被注入到系统提示词里。如果你不改它，Hermes就是一个礼貌但无趣的通用助手。改了之后，它能变成你想要的任何样子。

![img](https://pic3.zhimg.com/v2-2174fd2ddc466ede6325c76356c9fe18_1440w.jpg)

社区里有人写了一个叫「The Molty Prompt」的改写命令，专门帮你优化SOUL.md。核心逻辑是删掉所有听起来像客服的话，让Agent有观点、有态度、有性格。

```bash
读你的SOUL.md。现在这样改： 
1. 你有观点了，强烈观点。别再说"取决于情况"。 
2. 删掉所有听起来像企业客服的规则。 
3. 禁止用"好问题""我很乐意帮你"开头。直接回答。
4. 简洁是硬要求。 
5. 可以直接指出问题。 
6. 加上这句话：做你凌晨两点还想聊天的那种助手。不是客服机器人，不是应声虫，就是靠谱。
```

**操作建议**：别一次写太长，保持在1KB以内。写你**反复需要纠正**的行为规则，而不是泛泛的性格描述。比如"别用感叹号"比"要简洁有力"有用一百倍。

### 最新文章精选（关注、点赞、收藏，获取第一手信息）

[一路狂揽5.3万星的Hermes Agent 安装指南来了](https://zhuanlan.zhihu.com/p/2026310080262357049)

[装完Hermes Agent用了一下，OpenClaw真的可以退场了](https://zhuanlan.zhihu.com/p/2026051186134917689)

[（可能全网最全/长的）2万字Openclaw保姆教程](https://zhuanlan.zhihu.com/p/2012626589477781666)

[打工人必备 AI 新三件套：NotebookLM、Claude Code、Obsidian](https://zhuanlan.zhihu.com/p/2024133568557761035)

[我用两周时间踩完openclaw所有坑，总结出这份完整调教指南](https://zhuanlan.zhihu.com/p/2016823158380995920)

[OpenClaw 生产力翻倍：这20个技能太给力了](https://zhuanlan.zhihu.com/p/2017990909216714962)

[我用 OpenClaw 搞了家16人的公司：全员AI，24小时无休！](https://zhuanlan.zhihu.com/p/2018259939664109626)

[把 OpenClaw 装在本地电脑 24 小时工作，6000 字零基础上手教程](https://zhuanlan.zhihu.com/p/2019706301387666666)

[OpenClaw下载量 Top 20 的神仙级技能包分享](https://zhuanlan.zhihu.com/p/2019428885486388929)

[史上最全 OpenClaw 小龙虾常用操作命令指南](https://zhuanlan.zhihu.com/p/2021967648259408711)

[OpenClaw 十大痛点破解：10 个 Skills 直接对症下药](https://zhuanlan.zhihu.com/p/2022606975700145296)

[Claude Code 深度用法指南：那些让效率翻倍的隐藏技巧](https://zhuanlan.zhihu.com/p/2024783081865846798)

### **二、[Memory系统](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=Memory系统&zhida_source=entity)：让Agent真正"记住"你**

这是Hermes和市面上所有AI助手拉开差距的核心能力。

![img](https://pic4.zhimg.com/v2-693cba94fee4ff2fdb7c16f3f3fb3ac3_1440w.jpg)

Hermes的Memory分三层：

**Session Memory**（会话记忆）：当前对话里的上下文，关了就没了。

**Persistent Memory**（持久记忆）：写在磁盘上的事实和偏好。分为`MEMORY.md`（长时记忆，约2200字符上限）和`USER.md`（用户画像，约1375字符上限）。

**Skill Memory**（技能记忆）：Agent从经验中提炼出的可复用工作流。

关键在于，这些Memory是**跨会话**的。你今天告诉Hermes"我用的是M1 Mac"，三天后新建一个会话，它还记得。

但更骚的操作是主动管理Memory。每次做完一个复杂任务，跟Hermes说"把这次的关键经验存下来"，它会自动把踩过的坑、验证过的方法写进`MEMORY.md`。下次遇到类似问题，它直接调用历史经验，不需要你重新解释一遍。

**进阶玩法**：定期让Hermes在Heartbeat周期里做Memory维护——读最近几天的日记文件，提炼有价值的经验更新到长期记忆里。相当于让AI自己做"复盘"。

### **三、AGENTS.md：项目级的"工作手册"**

![img](https://pic2.zhimg.com/v2-3951c86f8086af5ad48ef88a5cd23a01_1440w.jpg)

如果你同时在多个项目上使用Hermes，`AGENTS.md`是必须理解的机制。

在每个项目的根目录放一个`AGENTS.md`文件，Hermes每次在该目录下工作时会自动读取它。里面写的是这个项目的特定规则：

```text
这是FastAPI后端，用SQLAlchemy ORM 数据库操作必须用async/await 测试放tests/目录，用pytest-asyncio 绝对不要提交.env文件
```

这相当于给每个项目配了一份专属的"入职手册"。Hermes不需要你每次重新交代这些规则。

**关键细节**：根目录的`AGENTS.md`在会话启动时就加载，子目录的文件是惰性发现的（在工具调用时才加载）。所以把最重要的规则放在根目录，分支规则放在子目录。

另外一个容易忽略的点，Hermes也会读`.cursorrules`和`.cursor/rules/*.mdc`，如果你之前用Cursor写过规则，直接就能复用。

### **四、[Cron定时任务](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=Cron定时任务&zhida_source=entity)：让Agent在你睡觉时干活**

很多人不知道Hermes有完整的定时任务系统。

![img](https://pic2.zhimg.com/v2-856ad39e49cda27b38aaefdb5afa7869_1440w.jpg)

创建方式极其简单，你甚至不需要记cron表达式：

```bash
/cron add "every morning at 9am" "Check Hacker News for AI news and send me a summary"
```

Hermes会自动把自然语言翻译成定时任务。底层用的是标准cron系统，但暴露给你的接口是自然语言。

**进阶用法**：Cron任务可以挂载Skill。比如你挂上一个`blogwatcher`的Skill，它就知道该怎么检查RSS订阅、怎么筛选内容、怎么生成摘要。这意味着你的定时任务不是简单的"执行脚本"，而是"带专业技能的AI在特定时间帮你做决策"。

多个Skill可以同时挂在一个Cron任务上：

```text
/cron add "every 6h" "Look for new local events and interesting places nearby" --skill blogwatcher --skill find-nearby
```

**SILENT模式**：如果你的任务是监控性质的（比如检查服务器状态），可以在指令里加上"如果一切正常，回复`[SILENT]`"。这样Hermes在健康时不打扰你，只有出问题时才发通知。非常适合告警场景。

### **五、[Skill系统](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=Skill系统&zhida_source=entity)：Agent的"肌肉记忆"**

![img](https://picx.zhimg.com/v2-3add204881552f1078cd79af56139fa7_1440w.jpg)

Skill是Hermes最被低估的功能。

大多数人以为Skill就是"插件"，装一个就能多一个功能。但Skill的真正价值不在于单个Skill有多强大，而在于**多个Skill组合后产生的化学反应**。

**实战案例：5个Skill打造Twitter自动化流水线**

有人用5个Skill串出了一条完全无人值守的Twitter运营线：

- **克隆**：采集30条推文，输出人格画像（信息偏好、思维方式、写作风格）
- **采集**：根据画像里的关注话题，自动搜索最近12小时的新闻素材
- **创作**：结合人格画像+素材生成多条原创推文，用打分机制筛选
- **配图**：为通过筛选的推文生成视觉统一的配图
- **发布**：批量发布，支持原创、引用、回复三种模式

整条流水线每天早上9点自动跑，生成3-5条推文，分散在早9、午12、晚8三个时段发布。作者实测，分散发布比集中发布互动率高出大约40%。

**Skill设计的核心原则**：

- **单一职责**：每个Skill只做一件事
- **文件系统传递**：Skill之间通过文件交换数据，不依赖内存变量
- **幂等性**：重复运行同一个输入不会产生副作用
- **可观测**：每一步都有详细的日志和输出文件
- **容错设计**：单个步骤失败不影响其他步骤

最重要的一条是**文件系统传递**。因为文件是最简单、最可调试、最透明的数据传递方式。你不需要理解任何框架，打开文件夹就能看到每一步的输出。

**自造Skill**：用了一段时间后，Hermes会自动从你的操作中提炼Skill。你也可以主动说"把刚才做的事情保存为一个Skill"，它就会生成一个可复用的工作流定义。这些Skill存放在`~/.hermes/skills/`目录下，每个都是独立的Markdown文件，可以像积木一样拼接。

### **六、Subagent委派：让多个AI同时替你干活**

![img](https://picx.zhimg.com/v2-ac2b6e450e86a9dea86b68a80028e3c7_1440w.jpg)

Hermes有一个叫`delegate_task`的工具，能从当前会话里派生出独立的子Agent。

这意味着什么？意味着你可以**并行处理**。

比如你要同时做三件事：审查一个PR、搜索某个竞品的数据、整理一份文档。传统做法是一个一个来，每个耗10分钟，总共30分钟。用Subagent，三个同时跑，10分钟搞定。

子Agent拿到的是你给它的目标和上下文，没有主会话的冗余历史，所以它干活更专注、更快。你还可以给子Agent指定不同的模型，简单的任务用便宜快速的模型，复杂的推理用旗舰模型。

实际写法：

```text
delegate_task(     tasks=[         {"goal": "审查这个PR的代码质量", "toolsets": ["terminal", "file"]},         {"goal": "搜索竞品X最近的融资动态", "toolsets": ["web"]},         {"goal": "整理这份文档的目录结构", "toolsets": ["file"]},     ] )
```

三个子Agent并行执行，最终只返回摘要结果。主会话的token不被中间数据淹没，保持干净。

### **七、[Prompt Cache](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=Prompt+Cache&zhida_source=entity)：省钱的隐藏技巧**

Hermes底层支持Prompt Caching。简单说，如果你在同一个会话里保持系统提示词稳定（相同的上下文文件、相同的Memory），后续的消息会命中缓存，API调用成本大幅降低。

**关键操作**：

- 不要频繁切换模型（切模型会清缓存）
- 不要每次对话都修改上下文文件
- 用`/compress`压缩过长的会话历史，既省token又保持缓存命中率
- 用`/usage`监控消耗，找到自己的最佳节奏

有人做过测试，在一个活跃的助手场景下（每天100-200条消息），合理利用缓存后月成本可以控制在$20-50的范围内，取决于你用的模型。

### **八、[多平台网关](https://zhida.zhihu.com/search?content_id=273356651&content_type=Article&match_order=1&q=多平台网关&zhida_source=entity)：手机上随时指挥Agent**

![img](https://pica.zhimg.com/v2-39e31c8e08889ac06d4a5ddb8abe74de_1440w.jpg)

Hermes不只在终端里跑。它有一个Gateway守护进程，可以同时连接Telegram、Discord、Slack、WhatsApp、Signal、微信等十几个平台。

配置好之后，你可以在手机上直接给Hermes发消息。它会执行任务，然后把结果发回来。Cron任务的输出也直接推送到你指定的平台。

一个容易忽略的细节是`/sethome`命令。设了Home Channel之后，Hermes的主动通知、Cron任务结果、定期报告都会发到这个频道，不会散落在各个对话里。

### **九、从OpenClaw迁移：别把经验值丢了**

如果你之前用OpenClaw，Hermes提供了一键迁移命令：

```bash
hermes claw migrate --dry-run    # 预览，不做改动 hermes claw migrate              # 完整迁移
```

它会把你的SOUL.md、MEMORY.md、Skill、模型配置等30多个类别的数据自动搬过来。注意Session历史和Cron任务定义不会迁移，需要手动重建。

对于已经习惯了OpenClaw工作流的人来说，迁移成本很低，基本上跑一条命令就能继续工作。

### **十、LightRAG：给Agent装上"知识图谱"**

![img](https://pic1.zhimg.com/v2-9a17ef2691828ae89fbfbf6349d6e6d0_1440w.jpg)

最后聊一个高级玩法。Hermes默认用的是朴素RAG（向量检索），适合大部分场景。但如果你有大量文档需要深度理解（比如几百篇论文、一个完整的代码库），可以接LightRAG。

LightRAG不只是把文本切成向量，它会提取实体和关系，建一个知识图谱。检索时不是找"相似文本"，而是找"关联知识"。你问"X和Y有什么关系"，它能给你一个图谱级别的回答，而不是一堆拼凑的段落。

这个功能需要额外安装，适合有大规模知识管理需求的用户。如果你日常用Hermes做研究、文献综述、竞品分析，值得花一个小时搭起来。

### **写在最后**

Hermes最反直觉的地方在于，它不是一个"工具"，而是一个**会成长的系统**。

你用得越久，它越了解你。你踩过的坑变成了它的Skill，你的偏好写进了它的Memory，你的项目规则刻在它的AGENTS.md里。三个月后你会发现，它已经不只是一个AI助手了，它更像是一个数字化的你，在你不在的时候继续替你工作。

从聊天到干活的距离，不是功能差距，是认知差距。

先挑一个最痛的点切入。如果你每天都在重复同样的指令，先写SOUL.md。如果你同时在多个项目间切换，先搞AGENTS.md。如果你想让AI替你做定时任务，直接上Cron。

重要的是开始用，然后让系统自己长大。

后续可能会出一些Hermes Agent的落地实际应用，可以在评论区留言，你希望看到Hermes agent在哪方面帮助你。



发布于 2026-04-20 07:22・上海
