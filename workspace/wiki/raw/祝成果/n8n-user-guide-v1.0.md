# n8n 用户操作指南 v1.0

> **一句话**：n8n 是一个「积木式 AI 工作流搭建台」——你把不同软件像乐高一样拼在一起，让它们自动干活，你躺着收结果。

---

## 这是什么？

想象你有一堆积木：微信、邮箱、日历、AI 聊天、Excel 表格、网页抓取……每块积木各干各的活。n8n 就是那张**底板**——你把积木按顺序卡上去，设定好"什么时候开始、做什么、做完通知谁"，然后你就可以去泡茶了。

它最大的特点三句话：
1. **免费**（你自己装一台就能免费用，不限量）
2. **开源的**（代码公开，不会被厂商锁定）
3. **AI 原生**（内置 AI 大脑，能自己思考决策）

---

## 你会在什么场景用上它？

| 你遇到的问题 | n8n 怎么帮你 |
|------------|------------|
| "每天手动复制粘贴数据到 Excel" | 定时自动抓取 → 整理 → 填入表格 |
| "微信消息太多，重要信息漏了" | 关键消息自动提取 → 汇总 → 发到邮箱 |
| "想用 AI 但不知道从哪开始" | 拖拽搭建一个 AI 助手，自动回答/处理问题 |
| "每个平台发同样的内容太累" | 写一次 → 自动发到公众号/微博/小红书 |
| "别人推荐的自动化工具太贵" | 自己装一个，服务器费一个月 30 块 |

---

## 快速上手：三步跑起来

### 第一步：安装（选你最舒服的方式）

#### 🟢 方式一：一条命令安装（推荐）

打开终端（就是那个黑窗口），输入：

```bash
npx n8n
```

你会看到：
```
n8n ready on http://localhost:5678
```

> **或者对我说**：「军师，帮我装一下 n8n」

#### 🟡 方式二：Docker 安装（生产用）

```bash
docker run -it --rm --name n8n -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

> **⚠️ 国内用户注意**：Docker 拉取镜像可能很慢。试试换成国内镜像源，或者直接用方式一。
>
> **或者对我说**：「军师，帮我在 Docker 里装 n8n」

#### 🔵 方式三：云端直接用（零安装）

访问 [n8n.cloud](https://n8n.cloud/signup)，注册即用。免费额度 2,500 次执行/月。

### 第二步：打开界面

浏览器打开 `http://localhost:5678`

你会看到这样的画面：

```
┌──────────────────────────────────────────┐
│  📁 Workflows    ＋ New Workflow          │
│                                          │
│     ┌──────────────────────┐             │
│     │   ＋ Add first step  │             │
│     │                      │             │
│     │   (一个大大的 + 号)   │             │
│     └──────────────────────┘             │
│                                          │
│  📋 Templates     🔌 Credentials         │
└──────────────────────────────────────────┘
```

点击 **"＋ Add first step"**，你就进入了工作流的搭建画布。

### 第三步：搭一个「Hello World」

我们来做一个最简单的：**定时到点了，AI 给你写一首打油诗，发到你的微信/邮箱。**

```
  ⏰ 定时触发
     │
     ▼
  🤖 AI 对话 (ChatGPT / DeepSeek)
     │
     ▼
  📧 发送结果
```

#### 具体操作（跟着做）：

1. 点击 **＋** → 搜索 "Schedule" → 选择 **Schedule Trigger**
2. 设置：每天 08:00 触发
3. 再点 **＋** → 搜索 "AI" → 选择 **AI Agent**（或 Basic LLM）
4. 在 "User Message" 里写：`请写一首关于清晨的五言打油诗`
5. 再点 **＋** → 搜索 "Email" → 选择 **Email (Send)**
6. 填上你的邮箱地址
7. 点右上角 **▶ Test Workflow** 试试看！

> **或者对我说**：「军师，帮我搭一个每天早上给我写诗发邮箱的工作流」

---

## 🗺️ 工作流全景图

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" font-family="sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="4" flood-opacity="0.3"/>
    </filter>
  </defs>
  <rect width="800" height="500" fill="url(#bg)"/>

  <!-- Title -->
  <text x="400" y="40" text-anchor="middle" fill="#e0e0e0" font-size="20" font-weight="bold">n8n 工作流全景：从触发到完成</text>

  <!-- Trigger section -->
  <rect x="50" y="70" width="200" height="120" rx="12" fill="#2d6a4f" filter="url(#shadow)"/>
  <text x="150" y="100" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">⚡ 触发器 (Trigger)</text>
  <line x1="70" y1="115" x2="230" y2="115" stroke="#52b788" stroke-width="1"/>
  <text x="150" y="135" text-anchor="middle" fill="#b7e4c7" font-size="11">⏰ 定时执行</text>
  <text x="150" y="155" text-anchor="middle" fill="#b7e4c7" font-size="11">🌐 Webhook 接收</text>
  <text x="150" y="175" text-anchor="middle" fill="#b7e4c7" font-size="11">📧 收到邮件时</text>

  <!-- Arrow 1 -->
  <line x1="250" y1="130" x2="310" y2="130" stroke="#4fc3f7" stroke-width="2"/>
  <polygon points="310,125 320,130 310,135" fill="#4fc3f7"/>
  <text x="280" y="120" text-anchor="middle" fill="#4fc3f7" font-size="9">事件</text>

  <!-- Process Section -->
  <rect x="320" y="70" width="200" height="120" rx="12" fill="#1b5e20" filter="url(#shadow)"/>
  <text x="420" y="100" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">🔧 处理节点 (Action)</text>
  <line x1="340" y1="115" x2="500" y2="115" stroke="#66bb6a" stroke-width="1"/>
  <text x="420" y="135" text-anchor="middle" fill="#c8e6c9" font-size="11">🤖 AI Agent 思考决策</text>
  <text x="420" y="155" text-anchor="middle" fill="#c8e6c9" font-size="11">📊 数据处理/转换</text>
  <text x="420" y="175" text-anchor="middle" fill="#c8e6c9" font-size="11">🔌 调用第三方API</text>

  <!-- Arrow 2 -->
  <line x1="520" y1="130" x2="580" y2="130" stroke="#4fc3f7" stroke-width="2"/>
  <polygon points="580,125 590,130 580,135" fill="#4fc3f7"/>
  <text x="550" y="120" text-anchor="middle" fill="#4fc3f7" font-size="9">结果</text>

  <!-- Output Section -->
  <rect x="590" y="70" width="180" height="120" rx="12" fill="#283593" filter="url(#shadow)"/>
  <text x="680" y="100" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">📬 输出 (Output)</text>
  <line x1="610" y1="115" x2="750" y2="115" stroke="#5c6bc0" stroke-width="1"/>
  <text x="680" y="135" text-anchor="middle" fill="#c5cae9" font-size="11">📧 发邮件/企业微信</text>
  <text x="680" y="155" text-anchor="middle" fill="#c5cae9" font-size="11">📝 写入数据库/文档</text>
  <text x="680" y="175" text-anchor="middle" fill="#c5cae9" font-size="11">📢 推送到各平台</text>

  <!-- Lower Section: AI Agent Detail -->
  <rect x="50" y="240" width="720" height="230" rx="12" fill="#1a1a2e" stroke="#ff9800" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="410" y="270" text-anchor="middle" fill="#ff9800" font-size="16" font-weight="bold">🧠 AI Agent 工作流（核心进阶能力）</text>
  <line x1="70" y1="285" x2="750" y2="285" stroke="#ff9800" stroke-width="0.5" opacity="0.5"/>

  <!-- Sub-steps -->
  <rect x="80" y="300" width="150" height="70" rx="8" fill="#e65100"/>
  <text x="155" y="325" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold">1️⃣ 理解任务</text>
  <text x="155" y="345" text-anchor="middle" fill="#ffe0b2" font-size="10">用户说"帮我找XXX"</text>
  <text x="155" y="360" text-anchor="middle" fill="#ffe0b2" font-size="10">Agent 理解意图</text>

  <line x1="230" y1="335" x2="270" y2="335" stroke="#ff9800" stroke-width="1.5"/>
  <polygon points="270,331 278,335 270,339" fill="#ff9800"/>

  <rect x="280" y="300" width="150" height="70" rx="8" fill="#e65100"/>
  <text x="355" y="325" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold">2️⃣ 选择工具</text>
  <text x="355" y="345" text-anchor="middle" fill="#ffe0b2" font-size="10">自动判断用哪个</text>
  <text x="355" y="360" text-anchor="middle" fill="#ffe0b2" font-size="10">：搜索/计算/API</text>

  <line x1="430" y1="335" x2="470" y2="335" stroke="#ff9800" stroke-width="1.5"/>
  <polygon points="470,331 478,335 470,339" fill="#ff9800"/>

  <rect x="480" y="300" width="150" height="70" rx="8" fill="#e65100"/>
  <text x="555" y="325" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold">3️⃣ 执行操作</text>
  <text x="555" y="345" text-anchor="middle" fill="#ffe0b2" font-size="10">调用工具拿到结果</text>
  <text x="555" y="360" text-anchor="middle" fill="#ffe0b2" font-size="10">如果不满意，重试</text>

  <line x1="630" y1="335" x2="670" y2="335" stroke="#ff9800" stroke-width="1.5"/>
  <polygon points="670,331 678,335 670,339" fill="#ff9800"/>

  <rect x="680" y="300" width="70" height="70" rx="8" fill="#4caf50"/>
  <text x="715" y="335" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold">✅</text>
  <text x="715" y="355" text-anchor="middle" fill="#fff" font-size="10">完成</text>

  <!-- Memory note -->
  <text x="410" y="420" text-anchor="middle" fill="#81d4fa" font-size="11">💾 Agent 可以带「记忆」——记住之前的对话内容，越用越聪明</text>
  <text x="410" y="440" text-anchor="middle" fill="#81d4fa" font-size="11">🔧 Agent 可以调用工具——搜索引擎、数据库、API、代码执行器……</text>
  <text x="410" y="460" text-anchor="middle" fill="#81d4fa" font-size="11">👥 多个 Agent 可以协作——一个管搜索，一个管分析，一个管执行</text>
</svg>
```

---

## 常见场景速查卡

### 🟢 我卡住了，不知道下一步怎么搞

| 症状 | 排查方法 |
|------|---------|
| "点了 Test 没反应" | 检查上一个节点有没有输出数据。点节点 → 看右边 OUTPUT 面板 |
| "提示 Credential 错误" | 左侧栏 Credentials → 找到对应的服务（如 Gmail）→ 重新连接 |
| "AI 节点不工作" | 确认 API Key 填对了没。国内用 DeepSeek 的话，Base URL 填 `https://api.deepseek.com/v1` |
| "Docker 拉不下来镜像" | 换镜像源：`docker.n8n.io` 改成国内 CDN，或者直接用 `npx n8n` |

> **或者对我说**：「军师，我到了 XXX 这一步，报错说 YYY，怎么搞？」

### 🟡 我做完了，它好像在工作

检查方法：左侧栏点 **Executions**，能看到每次运行的记录：
- 🟢 绿色 = 成功
- 🟡 黄色 = 等待中
- 🔴 红色 = 出错了（点进去看详情）

### 🔵 我有新想法，想加功能

直接在画布上拖新节点，连上线就行。n8n 的改动**实时生效**，不需要"保存并发布"那一步。

### 🟠 我想把手上的事自动化掉

**判断标准**：这件事满足以下 3 条就可以用 n8n 搞定——
1. 有规律（每天/每周/每次收到XX时）
2. 步骤固定（每次做的差不多）
3. 涉及 2 个以上的软件/平台

---

## 快速参考表

| 我想干什么 | 要搜的节点名 | 难度 | 或者对我说 |
|-----------|------------|:---:|-----------|
| 定时触发 | **Schedule Trigger** | ⭐ | 「每天 8 点跑一次」 |
| 收到 Webhook 时触发 | **Webhook** | ⭐ | 「外部系统发数据来就触发」 |
| 用 AI 聊天 | **AI Agent** / **Basic LLM** | ⭐⭐ | 「让 AI 帮我回答这个问题」 |
| AI 读取我的文档 | **AI Agent + Vector Store** | ⭐⭐⭐ | 「让 AI 读我的文件然后回答」 |
| 发邮件 | **Email (Send)** | ⭐ | 「把结果发到 xxx@邮箱」 |
| 发企业微信/钉钉 | **Webhook** + 群机器人 URL | ⭐⭐ | 「发到企业微信群」 |
| 调用任何 API | **HTTP Request** | ⭐⭐ | 「调这个接口拿数据」 |
| 处理 Excel/CSV | **Spreadsheet** / **Code** | ⭐⭐ | 「把这个表格处理一下」 |
| 微信自动回复 | **Webhook** + wxauto/wechaty | ⭐⭐⭐ | 「微信接入比较复杂…」 |
| 写 Python 代码 | **Code (Python)** | ⭐⭐ | 「用 Python 处理这段数据」 |
| 写 JS 代码 | **Code (JavaScript)** | ⭐⭐ | 「用 JS 处理这段数据」 |
| 判断条件 | **IF** / **Switch** | ⭐ | 「如果 A 就做 B，否则做 C」 |
| 等待一段时间 | **Wait** | ⭐ | 「等 5 分钟再继续」 |
| 拆分多条数据 | **Split In Batches** | ⭐⭐ | 「每条记录单独处理」 |

---

## 新手常见困惑（FAQ）

### Q1：n8n 和 Zapier / Make 有什么区别？
**最简单说法**：Zapier 像共享单车——扫码就能骑，但贵（大规模用每月几百美元）。n8n 像你自己的自行车——得自己买（装），但骑一辈子不花钱。Make 在两者之间。

**另一个关键**：n8n 有 AI 大脑（AI Agent 节点），Zapier/Make 目前做不到这种程度的 AI 落地。

### Q2：我不会写代码能用吗？
**能**。80% 的日常自动化不需要写代码。那 20% 需要的时候，你可以：
- 让 AI 帮你写（直接在 Code 节点里描述你要什么）
- 或者对我说「军师，帮我写一段……」

### Q3：自托管安全吗？数据会泄露吗？
**数据全在你自己机器上**，不出门。这比用第三方云服务**更安全**——你不用信任任何公司。企业（Vodafone、BMW、微软）用 n8n 的一个重要原因就是这个。

### Q4：微信/企业微信怎么接入？
这是国内用户**最大的痛点**。微信生态封闭，目前有三个方案：
1. **企业微信**：用群机器人 Webhook（最简单，官方支持）
2. **个人微信**：用 wxauto（PC 端自动化脚本），需要一台 Windows 电脑常开
3. **wechaty**：开源微信机器人框架，部署最复杂但也最稳

> 具体操作比较复杂，直接对我说：「军师，帮我搭微信接入 n8n」

### Q5：汉化怎么做？
社区有汉化包（n8nzh.com），但**不推荐汉化**——每次 n8n 升级都可能冲突，而且翻译质量参差不齐。建议适应英文界面，节点名都是些常见英文词，一周就习惯了。

### Q6：免费版有什么限制？
**自托管社区版无任何功能限制**。无限工作流、无限用户、无限执行次数、所有 400+ 集成都能用。唯一的"限制"是你得自己维护服务器。

### Q7：我能用国产 AI 模型吗？
**完全支持**。n8n 的 LLM 节点支持 OpenAI 兼容接口，只要填对 Base URL + API Key：
- DeepSeek：`https://api.deepseek.com/v1`
- 通义千问：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 智谱 GLM：`https://open.bigmodel.cn/api/paas/v4`
- MiniMax：`https://aibasecamp.asia/v1`

---

## 📊 中文社区资源导航

| 资源 | 适合人群 | 一句话评价 |
|------|---------|-----------|
| [n8n.akashio.com](https://n8n.akashio.com/) | ⭐⭐⭐ 国内最佳入门站 | 中文教程最全，有论坛+微信群，站长「汐笺」持续更新 |
| B站 UP「秋芝2046」 | ⭐⭐ AI Agent 实操派 | 「草履虫教程」系列，从零做 Agent，7万+播放 |
| B站 UP「技术爬爬虾」 | ⭐⭐⭐ 从入门到高级 | 10万+播放，部署→界面→API→数据结构→实战 |
| YouTube「柚智夫妻」 | ⭐⭐ 效率/生活黑客 | 11万订阅，n8n 教学融入生活场景 |
| GitHub [eleven-h/n8n](https://github.com/eleven-h/n8n) | ⭐⭐⭐ 中文技术手册 | 高质量实战手册，核心概念+节点详解+调试技巧 |
| [n8n 官方模板库](https://n8n.io/workflows/) | ⭐⭐ 找模板直接改 | 2,500+ 模板，搜关键词直接拿来用 |
| [n8n 官方文档](https://docs.n8n.io/) | ⭐⭐ 查参数/查节点 | 英文，但全面准确，不懂的对我说 |
| [VIBE 论坛](https://vibe.akashio.com/) | ⭐⭐ 提问交流 | AI 机器人自动回答，80% 问题能解决 |

---

## 🚀 进阶路线图

```
第 1 天：装好 + 跑通「定时 + AI + 发邮件」
    │
第 3 天：学会用 IF/Switch 做条件判断
    │
第 1 周：接入一个你常用的工具（飞书/钉钉/数据库）
    │
第 2 周：搭一个 AI Agent，给它装工具（搜索/读文件）
    │
第 1 月：日常有 3-5 个自动化在跑，每周节省 5+ 小时
    │
第 3 月：多个 Agent 协作，形成自己的「AI 自动化中台」
```

---

## 来源汇总

- n8n 官网：https://n8n.io/
- GitHub：https://github.com/n8n-io/n8n（~187K stars, v2.21.0）
- 定价：https://n8n.io/pricing/
- 安装文档：https://docs.n8n.io/hosting/installation/
- 中文社区：https://n8n.akashio.com/
- B站「技术爬爬虾」n8n 终极入门教学
- B站「秋芝2046」草履虫教程
- n8n Series C 融资公告：blog.n8n.io/series-c/（2025-10, $180M, $2.5B 估值）

---

*手册版本：v1.0 | 生成日期：2026-05-13 | 适用 n8n 版本：v2.19+*
