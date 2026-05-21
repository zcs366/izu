---
source_url: https://mp.weixin.qq.com/s/MMqwW9IVSFueg8jpmLldwg
ingested: 2026-05-14
sha256: 6100fd10917410ffc04e40eb4fa66bcec8f6c4f3b9e8e29cd8ed007bc047c17e
title: "Skill Graphs超越SKILL.md:结构化知识网络才是AI智能体的未来"
author: 峥嵘岁月AI (译介)
original_author: Heinrich (@arscontexta)
source: 微信公众号
original_source: X/Twitter, Heinrich @arscontexta
---

Skills即技能包。简单地来说：它是AI通过调用特定流程、知识或工具来完成复杂任务的可复用能力模块。想必大家都不陌生了吧！？即使自己没有写过，也应该用过，即使没有用过，也应该听说过，诸如：离职的同事人不在了，但"蒸馏"他做成的Skill技能包继续完成他的事儿，他的工作一点没耽误等段子。不过，关于Skills，只知道这些，恐怕就有些out,落伍了。因为我们现在玩起Skill Graphs技能图谱了。

人们低估了结构化知识的力量。它能催生出全新类别的应用。

这是Heinrich在X平台上发布的一篇关于Skill Graphs的长文，标题就叫《Skill Graphs > SKILL.md》。Heinrich是Claude Code插件arscontexta的开发者，这篇文章获得了超过405万次浏览和8839个赞——是Skill Graph这个话题下传播最广的文章之一。

Heinrich回答的是一个深层次的问题：为什么一个文件装不下真正的专业能力，以及知识应该如何被结构化才能让Agent真正理解一个领域。

一、一个文件为什么装不下真正的专业能力
我们先承认一个现实。现在大家写技能文件的方式是什么？通常是：

一个 SKILL.md 文件
包含一种能力
总结某件事 → 一个技能
代码审查 → 一个技能

一个文件，一个能力。

这对简单任务来说是可以的。但当你想构建真正的深度能力时，这就碰到了天花板。Heinrich用了一个让人印象深刻的例子：

想象一个治疗（therapy）技能，它需要提供关于认知行为模式、依恋理论、积极倾听技术、情绪调节框架……的各种相关信息。

一个文件根本装不下这些东西。

这个例子精准地说明了问题：真正的专业能力，不是单一的技能，而是相互关联的知识网络。 你不能把认知行为心理学、依恋理论、倾听技术、情绪调节框架塞进一个 Markdown 文件里还保持可用性。

二、Skill Graph是什么
Heinrich给出了 Skill Graph 的定义：

Skill Graph是一个由技能文件组成的网络，用Wiki链接(Wiki-Link)相互连接。

关键词：不是一个大文件，而是许多小的、可组合的碎片，每个碎片是一个完整的想法、技术或技能，它们之间用 [[双向链接]] 织成一张可遍历的图。

这个定义里有几个重要细节：

不是一个大文件
→ 许多小文件，每个是一个完整单元
→ Wiki 链接把它们连接起来
→ Wiki 链接嵌入在 prose（自然段落）中
→ 所以链接携带语义，不只是「引用」
→ Agent 顺着相关路径遍历，跳过不相关的部分

这让人想到 Zettelkasten——那个用卡片笔记构建知识网络的方法。但这一次，Skill Graph是专门为AI智能体设计的知识网络。

三、Skill Graph的三层结构
第一层：渐进式披露（Progressive Disclosure）
Heinrich 认为，Skill Graph 之所以比单一文件更强，是因为它实现了渐进式披露：

第一层：索引（Index）
  → Agent 可以扫描所有节点描述而不读取完整文件

第二层：描述（YAML frontmatter）
  → 每个节点有 YAML 描述，Agent 扫描而不读全文

第三层：链接（Links）
  → Wiki 链接嵌入 prose 中，携带语义

第四层：段落（Sections）
  → 内容的子结构

第五层：完整内容（Full Content）
  → 全文在需要时才深入读取

最关键的洞察：大多数决定在读取任何一个完整文件之前就已经发生了。Agent 先扫描所有描述，理解全局，找到相关路径，然后才深入具体内容。

第二层：原子元素（The Primitives）
Skill Graph 的建筑模块并不新奇，你可能已经有了：

① Wiki 链接（Wikilinks）
  → 嵌入在句子里的链接
  → 携带意义，不只是引用
  → Agent 可以顺着它们找到相关上下文

② YAML frontmatter
  → 每个文件顶部的描述
  → Agent 可以扫描而不读全文

③ MOCs（Map of Content，内容地图）
  → 把相关技能的集群组织成可导航的子主题
  → 当图变大时管理复杂度

关键是这些元素如何被组合使用，而不是它们本身有多新奇。

四、arscontexta插件：Skill Graph的具体实现
Heinrich用自己的插件作为具体案例——arscontexta。

arscontexta 是一个技能图谱，它教会你的 Agent 如何构建技能图谱。

arscontexta 是一个包含 ~250 个相互连接的 Markdown 文件的 Claude Code 插件。这 ~250 个文件教 Agent 如何为用户构建一个超大型知识库（也就是 Skill Graph）。一个技能文件做不到这件事，但用图谱就可以。

这是Skill Graph理念的完美体现：要教会 Agent 构建知识系统，最好的方式不是写一个超大的技能说明，而是用一张由相互关联的研究声明（技能）组成的图。每个碎片链接到其他碎片，每个都可组合，整个图可遍历。

五、Skill Graph的应用场景
Heinrich列举了三个不可能用单一文件实现、但用 Skill Graph 可以完美覆盖的场景：

场景一：交易技能图谱
├── 风险管理（头寸大小计算、回撤控制）
├── 市场心理学（从众效应、损失厌恶）
├── 技术分析（支撑阻力、趋势识别）
└── 各节点相互链接，上下文在各节点间流动

场景二：法律技能图谱
├── 合同模式
├── 合规要求
├── 司法辖区细节
├── 先例链条
└── 从一个入口点可遍历全部

场景三：公司知识图谱
├── 组织结构
├── 产品知识
├── 流程文档
├── 入职上下文
├── 企业文化
└── 竞争格局

这些东西没有一个能装进一个文件，但它们全都可以用图谱来实现。

六、如何构建一个Skill Graph
方法一：简单方式（用 arscontexta 插件）
① 安装 arscontexta Claude Code 插件
② 选择 research preset（研究预设）
③ 指定任意话题
④ 插件帮你建立 Markdown 文件夹结构
⑤ 然后用 /learn 和 /reduce 来填充内容

方法二：手动方式
关键原则：Skill Graph 不需要活在你的 .claude/skills/ 文件夹里。关键是有一个索引文件告诉 Agent 什么存在以及如何遍历它。

索引文件的设计：索引不是一个查找表，而是一个注意力入口点。Agent 读取它，理解全局，然后顺着与当前对话相关的链接走。

索引中的每个链接文件本身就是一个独立的方法论声明（= 技能）。

七、从"注入上下文"到"理解领域"
这是最有哲理的一段话，也是Skill Graph相比SKILL.md 的最本质区别：

技能是上下文工程，本质上是在需要的地方注入精心的知识。
技能图谱是下一步——不是一次注入，而是让 Agent 遍历一个知识结构，精确拉入当前情境所需的东西。

SKILL.md 模式：给你一段上下文，你照着执行
Skill Graph 模式：Agent 理解整个领域的知识网络，根据当前情境精确选择相关路径，拉入所需内容，动态构建上下文

这就是"遵循指令的 Agent"和"理解领域的 Agent"之间的差别。

八、核心设计原则速查
Skill Graph 的三个原子元素：
  ① Wiki 链接嵌入 prose → 携带语义，不只是引用
  ② YAML frontmatter 描述 → Agent 可扫描而不读全文
  ③ MOCs（内容地图） → 组织子主题，管理复杂度

渐进式披露的读取顺序：
  索引 → 节点描述 → Wiki 链接 → 段落 → 全文

Skill Graph 的构建原则：
  ① 不需要活在 .claude/skills/ 里
  ② 关键是有一个索引告诉 Agent 什么存在
  ③ 索引是注意力入口点，不是查找表
  ④ 每个节点是一个完整的方法论声明

两种 Agent 的本质区别：
  遵循指令的 Agent：收到一段上下文，执行
  理解领域的 Agent：遍历知识网络，动态拉取所需

十、一句话总结
Heinrich的Skill Graph框架，本质上在回答一个问题：智能体理解一个领域，和智能体只是被注入一段上下文，区别在哪里？

区别在于：真正的理解，是能够在一个相互关联的知识网络里自主导航，根据当前情境找到相关路径，而不是等着被告知"该做什么"。

Skill Graph把知识从"注入的指令"变成了"可遍历的网络"。智能体从中推导出的本地知识系统，才是真正贴合你工作流的东西。

原文来自 Heinrich @arscontexta Note Tweet《Skill Graphs > SKILL.md》

