# 智能体（AI Agent）用户操作指南 v1.0

> **呈：张成市** | 2026年5月13日
>
> 读完这篇，你会知道：智能体是什么、能帮你做什么、怎么开始用、遇到问题怎么办。
> 不需要懂代码。不需要懂技术。就像学用手机一样。

---

## 一、一句话说清楚：智能体是什么？

**智能体就是一个能自己动手干活的 AI。**

普通 AI 聊天机器人：你问一句，它答一句。像打电话问朋友"怎么去火车站"——朋友告诉你路线，但你自己走。

智能体：你跟它说"帮我订一张明天去上海的火车票"，它自己去查班次、比价格、下单、把电子票发到你手机上。**你只需要说你要什么，它自己想办法干完。**

> 📌 **类比**：普通 AI 是你的「顾问」，只给建议不动手。智能体是你的「助理」，给建议还帮你把事办了。

---

## 二、3 步快速上手

### 🟢 第 1 步：选一个智能体

现在市面上有很多智能体产品，选哪个取决于你想干什么：

| 你想干什么 | 推荐用这个 | 怎么开始 |
|-----------|-----------|---------|
| 写代码、做项目 | **Claude Code** / **Hermes Agent** | 在电脑上安装，终端里对话 |
| 查资料、写报告、做表格 | **ChatGPT Agent** / **Manus** | 打开网页或 App，直接说话 |
| 自动化办公流程 | **扣子（Coze）** / **Dify** | 注册账号，拖拽搭建 |
| 个人生活助理 | **手机自带 AI 助手** (Siri/小爱) | 手机已经在了，直接喊它 |

**🔹 新手建议**：先从 **Manus** 或 **ChatGPT Agent** 开始。不需要安装，打开网页就能用。等你熟悉了，再试更专业的工具。

### 🟢 第 2 步：学会「下命令」

对智能体说话和跟人说话不太一样。好的命令有三个要素：

```
❌ 不好的命令："帮我做点分析"
✅ 好的命令："分析这份销售数据，找出上个月销量下降最多的三个产品，并建议改进方案"
```

**好命令三要素（3W 法则）**：

1. **What（干什么）**：说清楚具体任务
2. **With what（用什么）**：给材料——文件、数据、链接
3. **What result（要什么）**：说清楚输出格式——"做成表格""写500字报告""画一张图"

```
📋 好命令模板：
"请帮我【做什么】，参考【这个文件/数据】，最终输出【什么格式】，要求【有什么要求】"

例：
"请帮我整理这周的会议记录，参考附件里的三份录音文字稿，
 最终输出一份500字以内的周报摘要，重点突出待办事项和风险点。"
```

### 🟢 第 3 步：检查和修正

智能体第一次做出来的东西，不一定是你要的。就像新助理第一天上班——你需要「调教」。

**三步检查法**：

1. **看结果对不对**：数据有没有算错？引用的信息准不准？
2. **看风格合不合适**：语气对不对？太啰嗦还是太简略？
3. **不满意就直接说**：

```
"第三段太啰嗦了，压缩到三句话"
"把这个表格改成柱状图"
"不要用'赋能''抓手'这种词，用大白话"
```

> 💡 把它当成真实助理来沟通。它不会烦，你越改它越懂你。

---

## 三、常见场景速查卡

### 🟠 场景 1：帮我写东西

| 你的需求 | 怎么跟智能体说 |
|---------|--------------|
| 写工作周报 | "这是我这周的工作记录（粘贴），帮我整理成周报，500字以内，分三个部分：完成事项、进行中、下周计划" |
| 写邮件 | "帮我写一封邮件给客户王总，确认下周三的会议时间，语气正式但不生硬" |
| 写方案 | "根据这个产品介绍（上传文件），帮我写一份市场推广方案，包括目标用户、推广渠道、预算估算" |

### 🟠 场景 2：帮我查东西

| 你的需求 | 怎么跟智能体说 |
|---------|--------------|
| 查行业信息 | "2025年中国新能源汽车销量前五的品牌是哪些？各占多少市场份额？" |
| 对比产品 | "对比 iPhone 17 Pro 和华为 Mate 80 Pro 的相机性能，做成对比表" |
| 解读政策 | "用大白话解释这个新政策对餐饮小企业的影响（附政策文件）" |

### 🟠 场景 3：帮我整理东西

| 你的需求 | 怎么跟智能体说 |
|---------|--------------|
| 整理会议记录 | "这是三个小时的会议录音文字稿（粘贴），帮我提炼出10条关键决策和对应的执行人" |
| 整理数据 | "把这个 Excel 里 500 条客户反馈分类，按：产品质量、物流、客服、价格 四个类别统计占比" |
| 整理知识 | "把我最近三个月收藏的这 30 篇文章（粘贴链接），按主题分类，每篇写一句话摘要" |

### 🟠 场景 4：帮我看东西

| 你的需求 | 怎么跟智能体说 |
|---------|--------------|
| 审合同 | "帮我审一下这份合同，重点看违约责任条款有没有坑，用红笔标注有问题的地方" |
| 改文章 | "这篇文章帮我润色，保持原意但让句子更流畅，删掉重复的话" |
| 翻译 | "把这封英文邮件翻译成中文，保留原文格式，专业术语不要翻错" |

---

## 四、智能体怎么「干活」——可视化流程图

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 620" font-family="sans-serif">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="400" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1a1a2e">智能体工作流程</text>

  <!-- Step 1: 用户输入 -->
  <rect x="280" y="60" width="240" height="50" rx="8" fill="#4a90d9" stroke="#3a7bc8" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" fill="white" font-size="14" font-weight="bold">🧑 你下达任务</text>
  <text x="400" y="102" text-anchor="middle" fill="#e0e0e0" font-size="11">"帮我分析这份数据"</text>

  <line x1="400" y1="110" x2="400" y2="140" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 2: 理解 -->
  <rect x="280" y="145" width="240" height="50" rx="8" fill="#8b5cf6" stroke="#7c3aed" stroke-width="2"/>
  <text x="400" y="170" text-anchor="middle" fill="white" font-size="14" font-weight="bold">🧠 理解任务</text>
  <text x="400" y="187" text-anchor="middle" fill="#e0e0e0" font-size="11">拆解成小步骤</text>

  <line x1="400" y1="195" x2="400" y2="225" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 3: 规划 -->
  <rect x="280" y="230" width="240" height="50" rx="8" fill="#f59e0b" stroke="#d97706" stroke-width="2"/>
  <text x="400" y="255" text-anchor="middle" fill="white" font-size="14" font-weight="bold">📋 制定计划</text>
  <text x="400" y="272" text-anchor="middle" fill="#fff" font-size="11">决定用什么工具、分几步做</text>

  <line x1="400" y1="280" x2="400" y2="310" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Loop box -->
  <rect x="230" y="315" width="340" height="130" rx="12" fill="#1e293b" stroke="#475569" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="400" y="338" text-anchor="middle" fill="#94a3b8" font-size="12">🔄 循环执行（直到任务完成）</text>

  <!-- Sub-steps inside loop -->
  <rect x="250" y="350" width="90" height="40" rx="6" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
  <text x="295" y="368" text-anchor="middle" fill="white" font-size="11" font-weight="bold">🔍 搜索</text>
  <text x="295" y="382" text-anchor="middle" fill="#d1fae5" font-size="9">查资料</text>

  <rect x="355" y="350" width="90" height="40" rx="6" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
  <text x="400" y="368" text-anchor="middle" fill="white" font-size="11" font-weight="bold">💻 执行</text>
  <text x="400" y="382" text-anchor="middle" fill="#d1fae5" font-size="9">写代码/算数据</text>

  <rect x="460" y="350" width="90" height="40" rx="6" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
  <text x="505" y="368" text-anchor="middle" fill="white" font-size="11" font-weight="bold">👀 检查</text>
  <text x="505" y="382" text-anchor="middle" fill="#d1fae5" font-size="9">自检结果</text>

  <line x1="340" y1="370" x2="353" y2="370" stroke="#6ee7b7" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="445" y1="370" x2="458" y2="370" stroke="#6ee7b7" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Loop back arrow -->
  <path d="M 400 445 L 400 465 L 570 465 L 570 370 L 552 370" fill="none" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#arrow)" stroke-dasharray="5,3"/>
  <text x="575" y="420" fill="#f59e0b" font-size="10">不满意→重来</text>

  <line x1="400" y1="445" x2="400" y2="480" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 5: Output -->
  <rect x="280" y="485" width="240" height="50" rx="8" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
  <text x="400" y="510" text-anchor="middle" fill="white" font-size="14" font-weight="bold">📤 交付结果</text>
  <text x="400" y="527" text-anchor="middle" fill="#fecaca" font-size="11">报告/图表/代码/分析</text>

  <line x1="400" y1="535" x2="400" y2="560" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 6: Feedback -->
  <rect x="280" y="565" width="240" height="45" rx="8" fill="#ec4899" stroke="#db2777" stroke-width="2"/>
  <text x="400" y="588" text-anchor="middle" fill="white" font-size="14" font-weight="bold">💬 你给反馈</text>
  <text x="400" y="603" text-anchor="middle" fill="#fce7f3" font-size="11">"第三段改短一点"</text>

  <!-- Loop back to Step 3 -->
  <path d="M 280 588 L 70 588 L 70 255 L 278 255" fill="none" stroke="#ec4899" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow)"/>
  <text x="65" y="430" fill="#ec4899" font-size="10" transform="rotate(-90, 65, 430)">不满意可以一直改</text>

  <!-- Legend -->
  <rect x="20" y="55" width="200" height="20" rx="4" fill="none"/>
  <text x="30" y="50" fill="#94a3b8" font-size="10">🔵 蓝色 = 你做的事  🟣 紫色 = 它思考  🟠 橙色 = 它规划</text>
  <text x="30" y="63" fill="#94a3b8" font-size="10">🟢 绿色 = 它干活  🔴 红色 = 交付结果  🩷 粉色 = 迭代改进</text>
</svg>
```

---

## 五、快速对照表

| 你想做什么 | 用什么工具 | 一句话怎么说 |
|-----------|-----------|------------|
| 写报告 | 任何智能体 | "根据这些材料写一份 2000 字的分析报告" |
| 做表格 | ChatGPT Agent / Manus | "把这个数据整理成表格，按月份汇总" |
| 写代码 | Claude Code / Hermes Agent | "帮我写一个自动发邮件的 Python 脚本" |
| 做 PPT | Gamma / Beautiful.ai | "用这个大纲生成一份 10 页的演示文稿" |
| 查资料 | ChatGPT Agent / Perplexity | "2025 年 AI 行业的五大趋势是什么？" |
| 翻译 | 任何智能体 | "把这篇文章翻译成中文，保持原意" |
| 审合同 | Claude / ChatGPT | "帮我审这份合同，标注所有风险条款" |
| 读论文 | Claude / NotebookLM | "用大白话总结这篇论文的核心发现" |
| 自动发邮件 | Make + AI / Dify | "每天早上 9 点自动汇总未读邮件发到微信" |
| 学新东西 | ChatGPT / Claude | "用我听得懂的话解释什么是量子计算" |

> 💡 **"Just talk to me" 模式**：如果你不想自己折腾这些工具，可以直接跟我说：**"军师，帮我做 XX"**，我来帮你选工具、下命令、检查结果。

---

## 六、常见问题（FAQ）

### 😰 "我不敢用，怕出错怎么办？"

**先从不重要的任务开始。** 别第一次就让智能体帮你写重要合同。先让它帮你：
- 整理会议记录 → 你核对
- 写邮件草稿 → 你改改再发
- 查资料 → 你验证关键数据

用两周，你就知道它哪里靠谱、哪里需要盯着。就像新助理，磨合期很正常。

### 🤔 "它老是不理解我的意思？"

**不是你笨，是说的方法不对。** 三个技巧：

1. **像给实习生布置任务一样说**：不是"帮我搞一下那个"，而是"帮我把上周的销售数据按地区分类，做成柱状图"
2. **给例子**：说"像这样的格式"，然后贴一个你满意的样本
3. **一次只说一件事**：别一口气给五个任务，一个一个来

### 😤 "它做出来的东西质量不行啊"

**智能体第一次给的结果 = 草稿，不是成品。** 正常用法是：

```
第 1 轮：你给任务 → 它出初稿
第 2 轮："第三段太长了，压缩" → 它改
第 3 轮："这个数据不对，用 2025 年的" → 它修正
第 4 轮：差不多了，你自己微调一下
```

好的结果往往是 3-5 轮对话改出来的。

### 💸 "太贵了怎么办？"

不同产品的价格差很大。从便宜到贵：

| 产品 | 大概费用 | 适合 |
|------|---------|------|
| 扣子（Coze） | 免费 | 轻度使用、搭简单机器人 |
| Dify 社区版 | 免费（自己部署） | 有一定动手能力 |
| ChatGPT Plus | $20/月 | 日常写作、查资料、分析 |
| Claude Pro | $20/月 | 写作、分析、编程 |
| Manus | 按用量计费 | 复杂多步骤任务 |
| Claude Code | 按 token 计费 | 专业开发者 |

**省钱技巧**：先用免费版试试，确定真的需要再付费。日常任务用 ChatGPT/Claude 的免费额度就够。

### 🔒 "数据安全吗？我的文件会不会泄露？"

**看你怎么用**：

- ❌ **不要做的事**：把公司机密文件、客户隐私数据、身份证号直接粘贴到公共 AI 产品里
- ✅ **可以做的事**：脱敏后再用（把真实人名、金额替换成"A公司""X万元"）
- ✅ **更安全的做法**：用企业版（有数据隔离协议）或本地部署版本（数据不出你的电脑）

---

## 七、进阶：智能体的五种形态

当你用熟了基础功能，可以了解智能体的不同「级别」：

### 🌱 Level 1：简单助手
你问，它答。ChatGPT 最早就是这样。

### 🌿 Level 2：工具使用者
它能调用工具——搜索网页、运行代码、读取文件。现在的 ChatGPT Agent、Claude 都属于这个级别。

### 🌳 Level 3：规划执行者
它能自己拆任务、定计划、分步执行。比如你让它"写一份竞品分析报告"，它会自己：查竞品资料 → 整理对比表 → 写分析 → 排版输出。

### 🌲 Level 4：多智能体协作
多个智能体像团队一样配合。一个负责查资料，一个负责写，一个负责审。**CrewAI** 就是这种模式。2026 年这个级别正在快速成熟。

### 🏔️ Level 5：自主智能体
完全独立运作，不需要你一步步盯着。设定目标，它自己想办法达成。这还处于早期探索阶段。

> 目前（2026年5月），主流产品在 **Level 2-3**，多智能体协作（Level 4）正在快速进入实用阶段。Level 5 还没到来——别信那些"AI 完全取代人类"的营销话术。

---

## 八、一张图看生态

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" font-family="sans-serif">
  <!-- Background -->
  <rect width="800" height="500" fill="#0f172a" rx="12"/>

  <!-- Title -->
  <text x="400" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#e2e8f0">2026 AI 智能体生态地图</text>

  <!-- Layer 1: Infrastructure -->
  <rect x="30" y="365" width="740" height="55" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="60" y="390" fill="#64748b" font-size="13">🖥️ 基础设施层</text>
  <text x="200" y="390" fill="#94a3b8" font-size="11">OpenAI · Anthropic · DeepSeek · 通义千问 · 文心一言</text>
  <text x="60" y="410" fill="#64748b" font-size="10">模型提供商（LLM API）</text>

  <!-- Layer 2: Frameworks -->
  <rect x="30" y="260" width="740" height="95" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="60" y="285" fill="#64748b" font-size="13">🔧 框架层</text>

  <rect x="60" y="298" width="150" height="45" rx="6" fill="#312e81" stroke="#4338ca" stroke-width="1"/>
  <text x="135" y="318" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="bold">LangChain</text>
  <text x="135" y="335" text-anchor="middle" fill="#818cf8" font-size="10">瑞士军刀</text>

  <rect x="225" y="298" width="150" height="45" rx="6" fill="#312e81" stroke="#4338ca" stroke-width="1"/>
  <text x="300" y="318" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="bold">CrewAI</text>
  <text x="300" y="335" text-anchor="middle" fill="#818cf8" font-size="10">多Agent协作</text>

  <rect x="390" y="298" width="150" height="45" rx="6" fill="#312e81" stroke="#4338ca" stroke-width="1"/>
  <text x="465" y="318" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="bold">AutoGen</text>
  <text x="465" y="335" text-anchor="middle" fill="#818cf8" font-size="10">微软出品</text>

  <rect x="555" y="298" width="150" height="45" rx="6" fill="#312e81" stroke="#4338ca" stroke-width="1"/>
  <text x="630" y="318" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="bold">Dify / 扣子</text>
  <text x="630" y="335" text-anchor="middle" fill="#818cf8" font-size="10">低代码平台</text>

  <!-- Layer 3: Products -->
  <rect x="30" y="130" width="740" height="120" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="60" y="155" fill="#64748b" font-size="13">📱 产品层（你直接用的）</text>

  <rect x="60" y="168" width="150" height="70" rx="6" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
  <text x="135" y="192" text-anchor="middle" fill="#bbf7d0" font-size="13" font-weight="bold">ChatGPT Agent</text>
  <text x="135" y="210" text-anchor="middle" fill="#86efac" font-size="10">全能型 · 有工具调用</text>
  <text x="135" y="226" text-anchor="middle" fill="#86efac" font-size="9">适合日常+办公</text>

  <rect x="225" y="168" width="150" height="70" rx="6" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
  <text x="300" y="192" text-anchor="middle" fill="#bbf7d0" font-size="13" font-weight="bold">Claude Code</text>
  <text x="300" y="210" text-anchor="middle" fill="#86efac" font-size="10">编程专用 · 终端运行</text>
  <text x="300" y="226" text-anchor="middle" fill="#86efac" font-size="9">开发者首选</text>

  <rect x="390" y="168" width="150" height="70" rx="6" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
  <text x="465" y="192" text-anchor="middle" fill="#bbf7d0" font-size="13" font-weight="bold">Manus</text>
  <text x="465" y="210" text-anchor="middle" fill="#86efac" font-size="10">长任务 · 自主执行</text>
  <text x="465" y="226" text-anchor="middle" fill="#86efac" font-size="9">复杂多步任务</text>

  <rect x="555" y="168" width="150" height="70" rx="6" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
  <text x="630" y="192" text-anchor="middle" fill="#bbf7d0" font-size="13" font-weight="bold">Hermes Agent</text>
  <text x="630" y="210" text-anchor="middle" fill="#86efac" font-size="10">开源 · 可编程</text>
  <text x="630" y="226" text-anchor="middle" fill="#86efac" font-size="9">极客·深度定制</text>

  <!-- Layer 4: Task Types -->
  <rect x="30" y="60" width="740" height="60" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="60" y="85" fill="#f59e0b" font-size="13">🎯 你能让它做什么？</text>
  <text x="200" y="85" fill="#fcd34d" font-size="11">写代码 ｜ 写文章 ｜ 数据分析 ｜ 自动操作 ｜ 客户服务 ｜ 知识管理 ｜ 翻译 ｜ 研究 ｜ 教育</text>
  <text x="60" y="108" fill="#fbbf24" font-size="10">从简单问答到自主规划执行，覆盖几乎所有知识工作场景</text>

  <!-- Arrows between layers -->
  <line x1="200" y1="190" x2="200" y2="258" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="400" y1="190" x2="400" y2="258" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="600" y1="190" x2="600" y2="258" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>

  <line x1="300" y1="355" x2="300" y2="363" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="500" y1="355" x2="500" y2="363" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>

  <!-- Right sidebar: Maturity -->
  <text x="690" y="460" fill="#64748b" font-size="10">成熟度：L2-L3 主流</text>
  <text x="690" y="478" fill="#64748b" font-size="10">L4 多Agent 快速成熟中</text>
</svg>
```

---

## 九、现在就开始

**第一步（今天就做）**：打开 [ChatGPT](https://chatgpt.com) 或 [Claude](https://claude.ai)，注册一个免费账号。

**第二步**：把这篇指南里的任何一个「好命令」复制粘贴进去，看看它怎么回答。

**第三步**：改一下，"这样改一下""再短一点"，体验迭代的感觉。

> 🔥 **一个让你立刻感受到价值的任务**：
>
> 粘贴你最近一次的工作周报或笔记，对它说：
> *"帮我整理成三个要点，每条不超过两句话，语气专业但不生硬。"*

试完回来告诉我感觉如何。这就是智能体的起点。

---

## 📚 推荐阅读（如果你想深入了解）

| 资料 | 适合谁 | 一句话 |
|------|-------|--------|
| [Google: Introduction to Agents](https://www.kaggle.com/whitepaper-agents) | 想了解原理的产品经理 | Google 2025年发布的系统化指南，从概念到生产 |
| [吴恩达: AI Agentic Design Patterns](https://www.deeplearning.ai/) | 技术入门者 | 四种 Agent 设计模式，视频短小精悍 |
| [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/) | 进阶开发者 | OpenAI 研究员的系统综述，经典必读 |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 实践者 | Anthropic 官方指南，讲的都是实战经验 |

---

> 💬 **军师的话**：智能体不是魔法，它不会取代你，而是放大你。就像一个永远不累、什么都愿意学的实习生——用好了，你的一天能有 28 个小时。用不好，就是个昂贵的聊天机器人。差别在哪？在于你会不会「带人」。这篇指南就是你的「带人手册」。
