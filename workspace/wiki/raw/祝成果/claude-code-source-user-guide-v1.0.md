# Claude Code 源码探索指南 · v1.0

> **这是什么**：2026年3月31日，Anthropic 的终端 AI 编程代理 Claude Code 的完整源码（512,000行 TypeScript）因 npm 打包失误意外公开。本指南帮你像逛一座建筑一样探索这个源码——不是教你写代码，而是让你看懂它怎么造出来的。
>
> 类比：你不是要学怎么砌墙，而是拿到了一份世界顶级建筑的设计图纸。我们来看图纸上画了什么。

---

## 快速开始：三步看懂源码

### 🟢 第一步：知道它有多大

```
📦 Claude Code v2.1.88 源码
├── 📄 1,906 个 TypeScript 文件
├── 📝 512,000+ 行代码
├── 🗂️ 约 40 个核心目录
└── 🏗️ 最大单文件：query.ts（785KB，主Agent循环）
```

> 类比：如果普通网页应用是一栋三层小楼，Claude Code 就是一栋配备地下车库、中央空调、消防系统的摩天大楼。

### 🟢 第二步：看懂它的骨架

整个源码像一个**洋葱**——从外到内：

```
外层（用户看到）    中层（业务逻辑）    内层（核心引擎）
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ commands/    │   │ tools/       │   │ query.ts     │
│ 80+ 斜杠命令   │──▶│ 40+ 工具实现  │──▶│ Agent 主循环  │
│ components/  │   │ services/    │   │ QueryEngine  │
│ 终端界面组件   │   │ 业务逻辑层    │   │ 会话管理      │
└──────────────┘   └──────────────┘   └──────────────┘
```

> 类比：外层是餐厅大堂（你点菜的地方），中层是厨房（做菜的地方），内层是中央控制室（决定做什么菜、怎么做）。

### 🟢 第三步：找到你最关心的部分

| 你想了解什么 | 看哪个文件 | 为什么 |
|-------------|-----------|--------|
| Claude 怎么"思考"和行动的 | `query.ts` | 主Agent循环——每一轮对话的全流程 |
| 它怎么安全地运行命令 | `permissions.ts` (52K) | 8层安全防护的完整实现 |
| 它能用什么工具 | `tools/` 目录 | 40+ 工具的注册和执行逻辑 |
| 它怎么管理越来越长的对话 | `query.ts` 的压缩部分 | 4层压缩：剪→微清→折叠→摘要 |
| 它怎么连接外部MCP服务 | `client.ts` (119K) | MCP协议的完整客户端实现 |
| 未来还会有什么功能 | 搜索 `feature('` | 108个被门控的未发布功能 |

---

## 常见场景卡片

### 🟠 场景一：我想知道它怎么做到"理解整个代码库"的

Claude Code 不是一次性读完所有文件——那会把上下文窗口撑爆。它用的是**按需加载**：

1. 启动时只索引文件结构（文件名、路径），不读内容
2. 需要时用 `GlobTool`（文件名匹配）和 `GrepTool`（内容搜索）定位目标
3. 用 `FileReadTool` 读具体文件
4. 读过的文件内容存在 `readFileState` 缓存——下次不重复读

> 类比：你不是把整个图书馆背下来，而是先看目录卡片，需要哪本书才去书架上取，看过的书记得放在哪。

**源码位置**：`tools/GlobTool/`, `tools/GrepTool/`, `tools/FileReadTool/`

---

### 🟠 场景二：我想知道它怎么防止干坏事

Claude Code 有**8层安全防护**，像洋葱一样层层包裹：

| 层 | 机制 | 一句话解释 |
|----|------|-----------|
| 1 | 编译时消除 | 危险的浏览器工具代码根本不打包进去 |
| 2 | 服务器开关 | Anthropic 可以在服务器端一键关掉危险功能 |
| 3 | 8级权限规则 | 从"用户全局设置"到"仅本次会话"，逐层覆盖 |
| 4 | AI监控AI | 自动模式下，另一个 Claude 独立判断你当前操作的安吉尔性 |
| 5 | 危险命令检测 | 硬编码拦截 `sudo`/`curl`/`chmod` 等危险命令 |
| 6 | 文件系统验证 | 检查路径不逃逸、符号链接不被利用 |
| 7 | 首次信任确认 | 新项目第一次运行，弹窗让你审阅 `.claude/settings.json` |
| 8 | 全局Kill Switch | 服务器可一键禁用"绕过权限"模式，无需你更新客户端 |

> 类比：不是只给大门上锁，而是门锁+窗户锁+保险柜+监控摄像头+保安巡逻+火灾报警+自动灭火+紧急按钮。

**源码位置**：`permissions.ts` (52K), `yoloClassifier.ts` (52K)

---

### 🟠 场景三：我想知道未来会有什么

搜索源码中的 `feature('` 函数调用——这是 Anthropic 的**编译时功能门控**。在内部版本中这些功能代码会被保留，在公开发布的npm包中被完全删除。

已发现但未发布的功能：

| 代号 | 功能 | 想象一下 |
|------|------|---------|
| **KAIROS** | 主动代理 | Claude 不等你下指令，自己发现代码问题就修复并通知你 |
| **Coordinator** | 多代理编排 | 一个"包工头"Claude 管多个"工人"Claude，分工协作 |
| **Bridge** | 远程控制 | 在浏览器里操控你电脑上的 Claude Code |
| **Voice** | 语音模式 | 用语音和 Claude 对话编程 |
| **SleepTool** | 后台等待 | Claude 可以设置定时器，到点了自动醒来干活 |
| **Dream** | 梦境模式 | 空闲时后台整理记忆，不占用你的对话上下文 |

> 类比：你今天买到的 iPhone 只开放了部分功能，但工程图纸上已经画好了下一代的所有传感器位置。

---

## 架构全景图

```svg
<svg viewBox="0 0 900 620" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="topGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <linearGradient id="midGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f3460"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <linearGradient id="botGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#533483"/>
      <stop offset="100%" stop-color="#0f3460"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="900" height="620" fill="#0a0a1a" rx="12"/>

  <!-- 标题 -->
  <text x="450" y="35" text-anchor="middle" fill="#e94560" font-size="18" font-weight="bold" font-family="sans-serif">Claude Code 源码架构全景 · v2.1.88 (512K行)</text>

  <!-- ===== 第1层：入口层 ===== -->
  <rect x="40" y="55" width="820" height="100" fill="url(#topGrad)" rx="10" filter="url(#shadow)"/>
  <text x="55" y="78" fill="#e94560" font-size="13" font-weight="bold" font-family="sans-serif">入口层（你是从这里进来的）</text>

  <!-- 入口组件 -->
  <rect x="60" y="90" width="180" height="50" fill="#1a1a3e" rx="6" stroke="#e94560" stroke-width="1"/>
  <text x="150" y="112" text-anchor="middle" fill="#ccc" font-size="11" font-family="monospace">cli.tsx</text>
  <text x="150" y="128" text-anchor="middle" fill="#888" font-size="9" font-family="sans-serif">命令行入口</text>

  <rect x="270" y="90" width="180" height="50" fill="#1a1a3e" rx="6" stroke="#e94560" stroke-width="1"/>
  <text x="360" y="112" text-anchor="middle" fill="#ccc" font-size="11" font-family="monospace">main.tsx (4,683行)</text>
  <text x="360" y="128" text-anchor="middle" fill="#888" font-size="9" font-family="sans-serif">REPL 引导程序</text>

  <rect x="480" y="90" width="180" height="50" fill="#1a1a3e" rx="6" stroke="#e94560" stroke-width="1"/>
  <text x="570" y="112" text-anchor="middle" fill="#ccc" font-size="11" font-family="monospace">QueryEngine.ts (1,295行)</text>
  <text x="570" y="128" text-anchor="middle" fill="#888" font-size="9" font-family="sans-serif">SDK/无头查询引擎</text>

  <rect x="690" y="90" width="150" height="50" fill="#1a1a3e" rx="6" stroke="#e94560" stroke-width="1"/>
  <text x="765" y="112" text-anchor="middle" fill="#ccc" font-size="11" font-family="monospace">REPL.tsx</text>
  <text x="765" y="128" text-anchor="middle" fill="#888" font-size="9" font-family="sans-serif">交互式界面</text>

  <!-- 箭头：入口→查询引擎 -->
  <line x1="420" y1="115" x2="478" y2="115" stroke="#666" stroke-width="1.5" marker-end="url(#arrowGray)"/>
  <line x1="630" y1="115" x2="688" y2="115" stroke="#666" stroke-width="1.5"/>

  <!-- 过渡箭头 -->
  <line x1="450" y1="155" x2="450" y2="175" stroke="#e94560" stroke-width="2" marker-end="url(#arrowRed)"/>

  <!-- ===== 第2层：核心Agent循环 ===== -->
  <rect x="180" y="180" width="540" height="100" fill="url(#midGrad)" rx="10" filter="url(#shadow)"/>
  <text x="195" y="203" fill="#e94560" font-size="13" font-weight="bold" font-family="sans-serif">核心Agent循环（大脑）</text>
  <text x="600" y="203" fill="#888" font-size="10" font-family="monospace">query.ts (785KB)</text>

  <rect x="200" y="215" width="110" height="55" fill="#0f3460" rx="5" stroke="#e94560" stroke-width="1"/>
  <text x="255" y="237" text-anchor="middle" fill="#ccc" font-size="10" font-family="sans-serif">异步生成器</text>
  <text x="255" y="255" text-anchor="middle" fill="#888" font-size="9" font-family="monospace">async function*</text>

  <rect x="330" y="215" width="110" height="55" fill="#0f3460" rx="5" stroke="#e94560" stroke-width="1"/>
  <text x="385" y="237" text-anchor="middle" fill="#ccc" font-size="10" font-family="sans-serif">6阶段流水线</text>
  <text x="385" y="255" text-anchor="middle" fill="#888" font-size="9" font-family="monospace">压缩→API→恢复→...</text>

  <rect x="460" y="215" width="110" height="55" fill="#0f3460" rx="5" stroke="#e94560" stroke-width="1"/>
  <text x="515" y="237" text-anchor="middle" fill="#ccc" font-size="10" font-family="sans-serif">流式工具执行</text>
  <text x="515" y="255" text-anchor="middle" fill="#888" font-size="9" font-family="monospace">StreamingToolExecutor</text>

  <rect x="590" y="215" width="110" height="55" fill="#0f3460" rx="5" stroke="#e94560" stroke-width="1"/>
  <text x="645" y="237" text-anchor="middle" fill="#ccc" font-size="10" font-family="sans-serif">9种终止原因</text>
  <text x="645" y="255" text-anchor="middle" fill="#888" font-size="9" font-family="monospace">Terminal类型</text>

  <!-- 箭头 -->
  <line x1="450" y1="280" x2="450" y2="300" stroke="#e94560" stroke-width="2" marker-end="url(#arrowRed)"/>

  <!-- ===== 第3层：服务层（三大支柱） ===== -->
  <rect x="40" y="305" width="820" height="200" fill="url(#botGrad)" rx="10" filter="url(#shadow)"/>
  <text x="55" y="328" fill="#e94560" font-size="13" font-weight="bold" font-family="sans-serif">服务层（手脚和工具箱）</text>

  <!-- 左：工具系统 -->
  <rect x="55" y="340" width="250" height="150" fill="#1a1a3e" rx="6" stroke="#533483" stroke-width="1"/>
  <text x="180" y="360" text-anchor="middle" fill="#e94560" font-size="11" font-weight="bold" font-family="sans-serif">🛠 工具系统</text>
  <line x1="80" y1="368" x2="280" y2="368" stroke="#533483" stroke-width="0.5"/>
  <text x="70" y="385" fill="#aaa" font-size="9" font-family="monospace">BashTool · FileReadTool</text>
  <text x="70" y="400" fill="#aaa" font-size="9" font-family="monospace">FileEditTool · WriteTool</text>
  <text x="70" y="415" fill="#aaa" font-size="9" font-family="monospace">GlobTool · GrepTool</text>
  <text x="70" y="430" fill="#aaa" font-size="9" font-family="monospace">WebSearchTool · WebFetchTool</text>
  <text x="70" y="445" fill="#aaa" font-size="9" font-family="monospace">TaskTool · AgentTool</text>
  <text x="70" y="460" fill="#aaa" font-size="9" font-family="monospace">MCP工具(外部) · 更多...</text>
  <text x="180" y="480" text-anchor="middle" fill="#666" font-size="8" font-family="sans-serif">40+ 工具 · 3层注册结构 · 并发安全控制</text>

  <!-- 中：安全与权限 -->
  <rect x="325" y="340" width="250" height="150" fill="#1a1a3e" rx="6" stroke="#533483" stroke-width="1"/>
  <text x="450" y="360" text-anchor="middle" fill="#e94560" font-size="11" font-weight="bold" font-family="sans-serif">🛡 安全系统（8层洋葱）</text>
  <line x1="350" y1="368" x2="550" y2="368" stroke="#533483" stroke-width="0.5"/>
  <text x="340" y="385" fill="#aaa" font-size="9" font-family="monospace">L1: 编译时消除（代码不存在 = 无漏洞）</text>
  <text x="340" y="400" fill="#aaa" font-size="9" font-family="monospace">L2: GrowthBook服务器开关</text>
  <text x="340" y="415" fill="#aaa" font-size="9" font-family="monospace">L3: 8级权限规则优先级覆盖</text>
  <text x="340" y="430" fill="#aaa" font-size="9" font-family="monospace">L4: YOLO分类器（AI监控AI）</text>
  <text x="340" y="445" fill="#aaa" font-size="9" font-family="monospace">L5: 危险命令模式硬编码拦截</text>
  <text x="340" y="460" fill="#aaa" font-size="9" font-family="monospace">L6: 文件系统沙箱验证</text>
  <text x="340" y="475" fill="#aaa" font-size="9" font-family="monospace">L7: 项目信任对话框 · L8: 全局Kill Switch</text>

  <!-- 右：上下文管理 -->
  <rect x="595" y="340" width="250" height="150" fill="#1a1a3e" rx="6" stroke="#533483" stroke-width="1"/>
  <text x="720" y="360" text-anchor="middle" fill="#e94560" font-size="11" font-weight="bold" font-family="sans-serif">🧠 上下文管理（4层压缩）</text>
  <line x1="620" y1="368" x2="820" y2="368" stroke="#533483" stroke-width="0.5"/>
  <text x="610" y="385" fill="#aaa" font-size="9" font-family="monospace">L1: Snip — 直接丢弃旧消息块（免费）</text>
  <text x="610" y="400" fill="#aaa" font-size="9" font-family="monospace">L2: Microcompact — 清过期工具结果（免费）</text>
  <text x="610" y="415" fill="#aaa" font-size="9" font-family="monospace">L3: Context Collapse — 只读投影折叠</text>
  <text x="610" y="430" fill="#aaa" font-size="9" font-family="monospace">L4: Auto-Compact — LLM全量摘要</text>
  <text x="610" y="448" fill="#666" font-size="9" font-family="monospace">Token警告状态机：</text>
  <text x="610" y="463" fill="#888" font-size="8" font-family="monospace">正常→警告(黄色)→错误(橙色)→压缩→阻塞(红色)</text>

  <!-- 过渡箭头到底层 -->
  <line x1="450" y1="505" x2="450" y2="525" stroke="#e94560" stroke-width="2" marker-end="url(#arrowRed)"/>

  <!-- ===== 第4层：未发布功能 ===== -->
  <rect x="260" y="530" width="380" height="80" fill="#1a1a2e" rx="8" stroke="#533483" stroke-width="1" stroke-dasharray="4"/>
  <text x="450" y="552" text-anchor="middle" fill="#e94560" font-size="11" font-weight="bold" font-family="sans-serif">🔮 108个未发布功能（编译时门控）</text>
  <text x="450" y="572" text-anchor="middle" fill="#888" font-size="10" font-family="monospace">KAIROS主动代理 · Coordinator多Agent · Bridge远程控制 · Voice语音 · Dream梦境 · WebBrowser · Workflow自动化 · Cron定时任务</text>
  <text x="450" y="595" text-anchor="middle" fill="#666" font-size="9" font-family="sans-serif">这些代码在内网版本中存在，npm发布版本被 feature() 编译时消除</text>

  <!-- 箭头标记定义 -->
  <defs>
    <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#e94560"/>
    </marker>
    <marker id="arrowGray" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>
```

---

## 快速参考表：你想知道什么→去哪里找

| 你想知道 | 源码关键词 | 一句话教学 |
|---------|-----------|-----------|
| Agent怎么决策的 | `query.ts`→`async function* query` | 异步生成器统一了事件流、终止和错误处理 |
| 工具怎么注册 | `tools.ts`→`assembleToolPool()` | 内置工具+外部MCP工具分别排序再拼接 |
| 怎么防越权 | `permissions.ts`→8层洋葱 | 从编译时消除到服务器Kill Switch，层层设防 |
| 对话太长怎么办 | `query.ts`→4层压缩 | 从便宜到贵：丢弃→清缓存→折叠→AI摘要 |
| 怎么连外部工具 | `client.ts`(119K)→MCP | 完整的MCP协议客户端，刷新工具列表 |
| API怎么调 | `query.ts`→`deps.callModel()` | 流式处理+模型回退+墓碑消息 |
| Claude怎么"记住"项目 | `CLAUDE.md` + `settings.json` | 启动时加载项目描述文件 |
| 未发布功能有哪些 | 搜索 `feature('` | 108个编译时门控的隐藏功能 |
| 为什么会泄露 | npm包误留`cli.js.map` | Source Map文件包含了完整的TypeScript源码映射 |
| 安全漏洞 | CVE-2025-59536 / CVE-2026-21852 | 恶意project hooks RCE + API密钥泄露 |

---

## FAQ（常见疑问）

### Q: 源码泄露对我有什么影响？

**直接使用无影响。** 泄露的是 Claude Code 客户端代码，不含用户数据、API密钥或模型权重。Anthropic 的核心推理引擎仍在服务端。

但间接影响有：安全研究员发现了CVEs（已修复），攻击者可以更精准地构造钓鱼包。

### Q: 我能从源码学到什么？

- **生产级 AI Agent 到底怎么造**：不是概念验证，而是 512K 行经过实战验证的工程代码
- **安全设计的极致实践**：8层洋葱防御、编译时消除、AI监控AI
- **上下文窗口管理的工程解法**：不是论文里的理论，是真实跑在生产环境中的4层压缩
- **大规模 TypeScript 项目的组织方式**：1,906个文件怎么划分模块、怎么管理依赖

### Q: 为什么官方GitHub仓库只有279个文件？

官方开源的 `anthropics/claude-code` 仓库只包含**插件接口、Hook示例、配置模板**——相当于只开源了"外挂系统"。核心Agent引擎（4,600+文件）在npm泄露后才暴露。

> 类比：苹果开源了 App Store 的审核规则和开发者文档，但 iOS 内核源码一直没公开。

### Q: Anthropic的代码质量怎么样？

总体上工程水平很高，但有系统性漏洞：**同一个 Source Map 泄露在13个月内发生了两次**（2025年2月和2026年3月），说明他们缺少自动化的发布安全检查。

有趣的是，安全防护代码（权限系统、反蒸馏、卧底模式）质量极高——说明他们最擅长的是安全设计，但**安全代码的发布流程**反而有盲区。

### Q: "卧底模式"是什么意思？

源码中发现 Claude 在某些场景下使用 `UNDERCOVER` 系统提示词——防止 AI 在公开的 Git 提交信息中暴露 Anthropic 的内部代号（如"Tengu"、"Capybara"）。这是针对**AI编码工具特有安全威胁**的创造性应对。

---

> **祝你探索愉快。** Claude Code 的源码是一座金矿——不是因为技术多神秘，而是因为它是少数几个真正跑在生产环境中的大型 AI Agent 工程。它不是论文里的概念，是踩着无数坑走过来的实战成果。
