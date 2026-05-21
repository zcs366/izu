# Deep Research 用户操作指南 v1.0

> **呈：张成市** | 2026年5月13日
>
> Deep Research不是搜索引擎，也不是聊天机器人。它是一个**会自己上网查资料、交叉验证、写出完整研究报告的AI助手**。
>
> 打个比方：普通AI对话像是问路人怎么走，Deep Research像是雇了一个专职研究员，他先去图书馆翻几十本书，打几十个电话确认，然后回来给你一份有引用来源的完整报告。

---

## 快速上手：三步搞定

### 第一步：问个好问题

不要问「帮我查一下AI」，而要像给真人研究员下任务一样：

| ❌ 太模糊 | ✅ 好问题 |
|-----------|----------|
| 「查一下电动车」 | 「对比2026年中国市场比亚迪、特斯拉、蔚来的电池技术路线，分析各自优劣和未来三年趋势，引用行业报告和财报数据」 |
| 「量子计算怎么样」 | 「量子计算在药物研发领域的实际应用案例，哪些药企已经开始用，效果如何，离商业化还有多远」 |
| 「AI Agent现状」 | 「2026年AI Agent创业公司融资情况全景：哪些赛道最热、头部公司估值、投资人最关心的问题」 |

**诀窍**：好问题有五个要素——**主题 + 范围 + 角度 + 时间 + 输出形式**。

### 第二步：看它干活（别急）

Deep Research启动后，你会看到它在「思考中」。它会：

1. **拆解问题** → 把大问题分成几个子问题
2. **搜索网页** → 自动翻几十甚至上百个网页
3. **交叉验证** → 发现不同来源的数据对不上会标注
4. **写报告** → 最终输出一份带引用来源的结构化报告

整个过程 **2到30分钟** 不等（取决于工具和问题复杂度）。

> 🟠 **卡住了？** 如果等了很久没反应，检查网络连接，或者换一个工具试试——不同工具的稳定性不一样。

### 第三步：读报告、追问

拿到报告后，不用从头读到尾。这样用：

- **先看结论** → 通常在报告开头
- **看表格/对比** → Deep Research擅长结构化对比
- **点引用链接** → 验证关键数据的来源
- **追问** → 报告不是终点。「帮我展开第三点」「这个数据是哪一年的」「用表格形式重新整理」

> 🔵 **军师，帮我把这份报告读一下，挑出最关键的三个结论。**

---

## 四款主流工具怎么选

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" font-family="sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <linearGradient id="openai" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10a37f"/>
      <stop offset="100%" stop-color="#0d8a6a"/>
    </linearGradient>
    <linearGradient id="google" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4285f4"/>
      <stop offset="100%" stop-color="#3367d6"/>
    </linearGradient>
    <linearGradient id="perplexity" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
    <linearGradient id="claude" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>

  <rect width="800" height="420" fill="url(#bg)" rx="12"/>

  <text x="400" y="38" text-anchor="middle" fill="#e2e8f0" font-size="18" font-weight="bold">选工具决策树</text>
  <text x="400" y="58" text-anchor="middle" fill="#94a3b8" font-size="12">从你的需求出发，按这个路线走</text>

  <!-- Start node -->
  <rect x="300" y="75" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="1"/>
  <text x="400" y="97" text-anchor="middle" fill="#e2e8f0" font-size="13">你的需求是什么？</text>

  <!-- Line from start to branches -->
  <line x1="400" y1="111" x2="400" y2="130" stroke="#475569" stroke-width="1"/>
  <line x1="155" y1="130" x2="645" y2="130" stroke="#475569" stroke-width="1"/>
  <line x1="155" y1="130" x2="155" y2="145" stroke="#475569" stroke-width="1"/>
  <line x1="320" y1="130" x2="320" y2="145" stroke="#475569" stroke-width="1"/>
  <line x1="480" y1="130" x2="480" y2="145" stroke="#475569" stroke-width="1"/>
  <line x1="645" y1="130" x2="645" y2="145" stroke="#475569" stroke-width="1"/>

  <!-- Branch 1: 速度和成本优先 -->
  <rect x="35" y="148" width="240" height="30" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="155" y="167" text-anchor="middle" fill="#94a3b8" font-size="12">速度和成本优先</text>

  <line x1="155" y1="178" x2="155" y2="195" stroke="#475569" stroke-width="1"/>

  <rect x="45" y="198" width="220" height="52" rx="8" fill="url(#perplexity)" opacity="0.9"/>
  <text x="155" y="218" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Perplexity Deep Research</text>
  <text x="155" y="238" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11">$20/月 · 2-5分钟出报告</text>

  <!-- Branch 2: 深度和质量 -->
  <rect x="200" y="148" width="240" height="30" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="320" y="167" text-anchor="middle" fill="#94a3b8" font-size="12">深度和质量最重要</text>

  <line x1="320" y1="178" x2="320" y2="210" stroke="#475569" stroke-width="1"/>

  <!-- Sub-branch: 需要超深度 -->
  <text x="240" y="202" fill="#64748b" font-size="10">预算有限</text>
  <text x="400" y="202" fill="#64748b" font-size="10">预算充足</text>
  <line x1="240" y1="210" x2="240" y2="223" stroke="#475569" stroke-width="1"/>
  <line x1="400" y1="210" x2="400" y2="223" stroke="#475569" stroke-width="1"/>

  <rect x="150" y="226" width="180" height="52" rx="8" fill="url(#google)" opacity="0.9"/>
  <text x="240" y="246" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Gemini Deep Research Max</text>
  <text x="240" y="266" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11">$20/月 · 顶级分析深度</text>

  <rect x="310" y="226" width="180" height="52" rx="8" fill="url(#openai)" opacity="0.9"/>
  <text x="400" y="246" text-anchor="middle" fill="white" font-size="14" font-weight="bold">OpenAI Deep Research</text>
  <text x="400" y="266" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11">$200/月(Pro) · 综合最强</text>

  <!-- Branch 3: 需要联网 + 多步推理 -->
  <rect x="360" y="148" width="240" height="30" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="480" y="167" text-anchor="middle" fill="#94a3b8" font-size="12">需要联网+分析文档</text>

  <line x1="480" y1="178" x2="480" y2="195" stroke="#475569" stroke-width="1"/>

  <rect x="370" y="198" width="220" height="52" rx="8" fill="url(#claude)" opacity="0.9"/>
  <text x="480" y="218" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Claude (Opus 4.7)</text>
  <text x="480" y="238" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11">$20/月 · 长文档分析最强</text>

  <!-- Bottom summary bar -->
  <rect x="35" y="310" width="730" height="90" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>

  <text x="60" y="332" fill="#38bdf8" font-size="12" font-weight="bold">一句话总结</text>

  <circle cx="60" cy="350" r="3" fill="#8b5cf6"/>
  <text x="70" y="354" fill="#cbd5e1" font-size="11">Perplexity — 快但浅，适合日常</text>

  <circle cx="60" cy="370" r="3" fill="#4285f4"/>
  <text x="70" y="374" fill="#cbd5e1" font-size="11">Gemini Max — 深且新，分析最透彻（2026年多位评测者共识）</text>

  <circle cx="60" cy="390" r="3" fill="#10a37f"/>
  <text x="70" y="394" fill="#cbd5e1" font-size="11">OpenAI — 稳而全，生态最完整（MCP支持、文件上传、自定义网站限制）</text>

  <circle cx="370" cy="350" r="3" fill="#d97706"/>
  <text x="380" y="354" fill="#cbd5e1" font-size="11">Claude — 没有专门的Deep Research产品，但多步推理+长文档能力极强</text>

  <circle cx="370" cy="370" r="3" fill="#64748b"/>
  <text x="380" y="374" fill="#94a3b8" font-size="11">NotebookLM — Google的免费「研究笔记本」，适合个人知识整理而非开放式调研</text>
</svg>
```

---

## 常见情境速查

### 🟢 做完了——下一步？

| 你手里有 | 你可以这样用 |
|----------|-------------|
| 一份报告 | 发给同事前，先追问AI：「这个报告有哪些漏洞或偏见？」 |
| 一堆引用 | 挑3-5个最关键的来源自己读一遍原文，别只信AI的摘要 |
| 多个竞品报告 | 把它们喂给同一个AI，让它做横向对比 |
| 想发表 | ⚠️ **引用规范**：APA格式标注AI工具和日期。不同期刊对AI辅助写作有不同规定 |

### 🟠 卡住了怎么办

| 问题 | 可能原因 | 解决 |
|------|---------|------|
| 报告一直在转圈 | 问题太复杂或服务拥堵 | 换一个工具、或者把大问题拆成2-3个小问题分别问 |
| 报告质量差、像在糊弄 | 问题不够具体 | 加上「引用至少5个来源」「用表格对比」「包含2024-2026年数据」等具体指令 |
| 引用的链接打不开 | AI可能引用了过期页面 | 用链接中的关键词重新搜索 |
| 数据互相矛盾 | AI在不同来源间没做好仲裁 | 手动追问：「你引用了两个矛盾的数据，哪个更可信？为什么？」 |

### 🔵 不同场景的模板

**场景1：竞品分析**
> 「帮我做[产品A]和[产品B]的深度对比。维度包括：定价、核心功能、用户口碑（引用App Store评分和Reddit讨论）、技术架构、融资情况、团队背景。输出表格+文字分析。时间范围：2024-2026。」

**场景2：行业研究**
> 「[行业名称]在2026年的全景分析。覆盖：市场规模与增速（引用Gartner/IDC等第三方报告）、主要玩家和市场份额、技术趋势、监管政策变化、未来两年预测。要求至少引用8个来源。」

**场景3：学术调研**
> 「关于[研究主题]的文献综述。总结近3年核心论文的主要发现、方法论争议、和未解决问题。按学派或方法论分组呈现。」

**场景4：购买决策**
> 「我要买[品类]，预算是[X]。对比三个主流选项，从性能、可靠性、售后服务、长期使用成本四个维度分析。引用真实用户评价和专业评测数据。」

---

## 快速参考表

| 我想…… | 用什么 | 花费 | 一句话理由 |
|--------|--------|------|-----------|
| 快速了解一个话题 | Perplexity Deep Research | $20/月 | 2-5分钟出结果，够用 |
| 写深度行业报告 | Gemini Deep Research Max | $20/月 | 分析深度和来源广度在2026领先 |
| 最完整的生态体验 | OpenAI Deep Research | $200/月(Pro) | MCP连接、文件上传、自定义来源 |
| 分析几十页PDF | Claude Opus 4.7 | $20/月 | 长文档理解无人能及 |
| 整理个人笔记/文档 | NotebookLM | 免费 | 上传你的文件，AI帮你找关联 |
| 完全免费 | Perplexity Free 或 Bing Copilot | $0 | 功能受限，但日常够用 |

---

## FAQ：你最可能问的

**Q：这玩意儿能替代我自己做研究吗？**

不能，也不应该。它是加速器，不是替代品。你仍需判断：这个问题值得深究吗？AI引用的来源可信吗？结论有没有遗漏关键视角？**Deep Research帮你从「找资料」跳到「审资料」，但审的能力在你手里。**

**Q：报告能直接发表或交作业吗？**

取决于场景。公司内部分析——可以，注明AI辅助。学术发表——查你所在期刊的规定，多数要求披露AI使用。学校作业——问你的老师，每个老师标准不同。无论如何，**你至少需要验证关键数据和核心论点**。

**Q：为什么我用的和别人用的结果不一样？**

三个变量影响最大：①你的问题写得多好 ②你用的是哪个工具 ③你追问了几轮。**同一个人用同一个工具，好问题是差问题产出的10倍差距。**

**Q：Deep Research会编造数据吗？**

会。这是所有AI的通病（幻觉）。Deep Research的优势在于它引用了来源，你可以逐条验证。但它引用的来源本身可能有问题。**花2分钟抽查3个关键数据来源，这2分钟的ROI是全流程最高的。**

**Q：信息安全吗？我上传的敏感文件会被用来训练吗？**

- OpenAI ChatGPT Plus/Pro/Enterprise：默认不用于训练（需在设置中确认）
- Google Gemini Advanced：不用于训练（Google官方声明）
- Anthropic Claude：不用于训练
- Perplexity Pro：不用于训练

但不建议上传高度敏感的商业机密，无论哪家。

---

## 🟢 完成信号

当你读完这份指南，下一步不是从头到尾记住它——而是**立刻拿一个问题去试**。

打开你手机上任何一个有Deep Research功能的AI，问一个你最近真正需要答案的问题。看看它给你什么。然后回来告诉我体验。

---

*军师的话：工具都是锤子，钉子在你脑子里。钉子越清晰，锤子越有力。*

---

## 来源汇总

1. OpenAI, "Introducing deep research," openai.com, Feb 2026 update
2. Google, "Deep Research Max: a step change for autonomous research agents," blog.google, 2026
3. Perplexity, "Deep Research" product documentation, 2026
4. Glasp, "OpenAI vs Perplexity vs Gemini vs Claude (2026 Guide)," glasp.co, 2026
5. AwesomeAgents, "Best AI Deep Research Tools 2026," awesomeagents.ai, 2026
6. ClickIT Tech, "Perplexity vs OpenAI Deep Research," clickittech.com, 2026
7. Finout, "Perplexity Pricing in 2026," finout.io, 2026
8. Tactiq, "Comparing Prices: ChatGPT, Claude AI, DeepSeek, and Perplexity," tactiq.io, 2026
9. Reddit r/GeminiAI, "For Deep Research and heavy reading, Gemini is currently miles ahead," 2026
10. GitConnected/LevelUp, "I Tested Google's New Deep Research vs Deep Research Max," 2026
