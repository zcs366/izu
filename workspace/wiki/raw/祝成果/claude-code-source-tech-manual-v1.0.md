# Claude Code 源码深度技术手册 · v1.0

> **完整版**：基于 v2.1.88 泄露源码的架构分析
>
> 覆盖：Agent循环 · 工具系统 · 权限模型 · 上下文管理 · MCP集成 · 未发布功能
>
> 版本：v1.0 · 2026年5月 · 依据社区架构分析综合编写
>
> **数据来源**：Bits-Bytes-NN 架构分析、Reddit r/ClaudeAI 深度解读、Verdent AI、Layer5、HuggingFace 讨论、The Hacker News 报道
>
> ⚠️ 注意：本文基于2026年3月31日泄露的 npm v2.1.88 版本源码分析，当前版本已有变化。Anthropic 已弃用 npm 分发，转向原生二进制安装器。

---

# 第1章：概览与核心理念

## 1.1 源码泄露始末

2026年3月31日，安全研究员 Chaofan Shou 在 X 上披露：Claude Code 的 npm 包 `.map` 文件意外暴露了完整源码。帖子获 2880万+ 阅读。

| 关键事实 | 详情 |
|---------|------|
| **泄露文件** | `cli.js.map`（Source Map） |
| **源码规模** | 1,906个 TypeScript 文件，512,000+ 行代码 |
| **npm版本** | v2.1.88 |
| **技术栈** | Bun运行时 + React/Ink终端UI + TypeScript严格模式 |
| **首次暴露** | 2025年2月24日（Dave Shoemaker发现，未公开） |
| **二次泄露** | 2026年3月7日（`@anthropic-ai/claude-agent-sdk`） |
| **Anthropic回应** | "人为错误的发布打包问题，非安全漏洞，无客户数据泄露" |

> 后来发现，同一 Source Map 问题在13个月内发生了两次。非偶然失误，是发布流程的系统性漏洞。

## 1.2 官方"开源" vs 泄露代码

Anthropic 在 GitHub 上运营 `anthropics/claude-code` 仓库（12.3万 Star），但该仓库仅包含：

- **279个文件**：插件系统接口、Hook示例、配置模板、11个示例插件
- **不包含**：核心Agent引擎、工具实现、权限系统、MCP客户端

泄露代码揭示了完整引擎：

| 组件 | 官方仓库 | 泄露代码 |
|------|---------|---------|
| 核心Agent引擎 | ❌ | ✅ `query.ts` (785KB) |
| 40+ 工具实现 | ❌ | ✅ `tools/` 目录 |
| 8层权限系统 | ❌ | ✅ `permissions.ts` (52K) |
| MCP客户端 | ❌ | ✅ `client.ts` (119K) |
| 远程控制(Bridge) | ❌ | ✅ `bridge/` (33+文件) |
| 查询引擎 | ❌ | ✅ `QueryEngine.ts` |
| 108个未发布功能 | ❌ | ✅ `feature()` 门控代码 |

> 类比：苹果开源了 App Store 审核规则和开发者文档，但 iOS 内核一直闭源。Claude Code 的"开源"策略类似——开放插件生态，保留核心引擎。

## 1.3 为什么这个源码值得研究

Claude Code 是**少数几个真正跑在生产环境中、经受数百万用户实战检验的大型 AI Agent 工程**。不是论文里的概念验证，不是 Hackathon 的 Demo。512K 行代码中包含了：

1. **成本感知的工程设计**：每个决策都从"最便宜的方案"开始（压缩、恢复、工具加载）
2. **纵深防御安全模型**：8层安全防护，从编译时消除到服务器端 Kill Switch
3. **Prompt 缓存优化至上**：工具池排序策略、Microcompact pinning、只读投影——全都围绕 Anthropic 的 prompt 缓存机制设计
4. **从 CLI 工具到 Agent 平台的演进**：Bridge 远程控制、Coordinator 多代理、KAIROS 主动模式揭示了 Anthropic 的战略方向

---

## 1.4 竞品架构对比

| 维度 | Claude Code | Cursor | GitHub Copilot | Codex CLI (OpenAI) | Aider |
|------|------------|--------|----------------|-------------------|-------|
| **运行时** | Bun（启动快+原生TS） | Electron | VS Code扩展 | Node.js | Python |
| **Agent循环** | Async Generator统一流 | 聊天驱动 | 补全+聊天 | 顺序执行 | 线性循环 |
| **上下文管理** | 4层压缩（Snip→Micro→Collapse→Auto） | IDE索引 | 局部上下文 | 基础窗口管理 | 文件级 |
| **安全模型** | 8层洋葱防御 | IDE自然约束 | 有限 | 基础权限 | 基础 |
| **工具系统** | 40+工具+流式并发+动态搜索 | IDE内工具 | 有限工具 | 基础工具 | Git+Shell |
| **架构开放度** | 插件接口开放 / 核心闭源 | 闭源 | 闭源 | 开源 | 开源 |

---

# 第2章：技术栈与目录结构

## 2.1 技术栈全景

```
┌─────────────────────────────────────────────────┐
│                  运行时层                        │
│  Bun (启动<100ms, 原生TypeScript, DCE支持)       │
├─────────────────────────────────────────────────┤
│                  UI 层                           │
│  React 18 + Ink (终端React渲染)                  │
├─────────────────────────────────────────────────┤
│                 业务逻辑层                        │
│  TypeScript 严格模式 (4,600+文件)                 │
├─────────────────────────────────────────────────┤
│                 通信层                           │
│  @anthropic-ai/sdk  · @modelcontextprotocol/sdk │
├─────────────────────────────────────────────────┤
│                 基础设施层                        │
│  GrowthBook (特性开关) · Bun bundler (树摇优化)   │
└─────────────────────────────────────────────────┘
```

**为什么选 Bun 而不是 Node.js？**

- **启动速度**：Bun 启动 <100ms vs Node.js ~500ms+。对于 CLI 工具，每次键入命令的启动延迟至关重要
- **原生 TypeScript**：无需 ts-node 或预编译步骤
- **`feature()` 编译时函数**：Bun 的自定义插件机制允许 `feature('FLAG')` 返回常量，打包器据此进行死代码消除（DCE）。这是 Claude Code 隐藏108个内部功能的基石

## 2.2 完整目录树

```
src/
├── main.tsx                 # REPL 引导程序，4,683 行
├── QueryEngine.ts           # SDK/无头查询生命周期引擎 (1,295行)
├── query.ts                 # ★ 主代理循环 (785KB，最大文件，~1,729行核心逻辑)
├── Tool.ts                  # 工具接口 + buildTool 工厂
├── Task.ts                  # 任务类型、ID、状态基类
├── tools.ts                 # 工具注册、预设、过滤
├── commands.ts              # 斜杠命令定义
├── context.ts               # 用户输入上下文
├── cost-tracker.ts          # API 成本累积
├── setup.ts                 # 首次运行设置流程
│
├── bridge/                  # Claude Desktop / 远程桥接
│   ├── bridgeMain.ts        #   会话生命周期管理器
│   ├── bridgeApi.ts         #   HTTP 客户端
│   ├── bridgeConfig.ts      #   连接配置
│   ├── bridgeMessaging.ts   #   消息中继
│   ├── sessionRunner.ts     #   进程生成
│   ├── jwtUtils.ts          #   JWT 刷新
│   ├── workSecret.ts        #   认证令牌
│   └── capacityWake.ts      #   基于容量的唤醒
│
├── cli/                     # CLI 基础设施
│   ├── handlers/            #   命令处理器
│   └── transports/          #   I/O 传输 (stdio, structured)
│
├── commands/                # ~80 个斜杠命令 (/allow, /compact, /memory, ...)
├── components/              # React/Ink 终端 UI 组件
├── entrypoints/             # 应用入口点
├── hooks/                   # React hooks
├── services/                # 业务逻辑层
├── state/                   # 应用状态管理
├── tasks/                   # 任务实现
├── tools/                   # 40+ 工具实现（每个工具一个子目录）
├── types/                   # 类型定义
├── utils/                   # 工具函数库（最大目录）
└── vendor/                  # 原生模块源码存根
```

## 2.3 各层职责划分

| 层 | 职责 | 关键文件 |
|----|------|---------|
| **入口层** | 解析命令行参数、初始化UI、启动REPL | `cli.tsx`, `main.tsx`, `REPL.tsx` |
| **查询引擎层** | 管理会话生命周期、组装消息、跟踪用量 | `QueryEngine.ts` |
| **Agent循环层** | 多轮对话核心流程：压缩→API→恢复→工具→下一轮 | `query.ts` |
| **服务层** | 业务逻辑：遥测、会话、MCP客户端、成本跟踪 | `services/`, `cost-tracker.ts` |
| **工具层** | 文件操作、Shell执行、搜索、Web、Agent委托 | `tools/` (40+工具) |
| **命令层** | 用户交互命令：权限管理、内存管理、模式切换 | `commands/` (80+命令) |
| **UI层** | 终端界面渲染：进度条、权限弹窗、多面板 | `components/` |
| **基础设施层** | Bridge远程、MCP客户端、特性开关、认证 | `bridge/`, `MCP/`, GrowthBook |

---

# 第3章：Agent主循环深度剖析

## 3.1 核心设计：Async Generator模式

**文件**：`query.ts`（1,729行核心逻辑）

传统 CLI Agent 通常使用 EventEmitter 或回调模式处理事件流——将"流事件"、"终止处理"、"错误处理"分散到不同通道。Claude Code 使用 **异步生成器（async function\*）** 将三者统一：

```typescript
export async function* query(
  params: QueryParams,     // 不可变参数
): AsyncGenerator<
  StreamEvent | RequestStartEvent | Message | TombstoneMessage | ToolUseSummaryMessage,
  Terminal                  // 返回值：终止原因
>
```

**设计优势**：

1. 消费者通过 `for await...of` 自然接收事件流
2. 终止原因通过 `return` 值传递（而非额外回调）
3. 错误通过 `throw` 自然传播到调用者的 `try-catch`

> 类比：传统方案像"给不同部门分别打电话"——管事件的打A部门，管终止的打B部门，管错误的打C部门。Async Generator 像"专用热线"——一个号码处理所有情况。

## 3.2 不可变参数 + 可变状态（Continue Site 模式）

### QueryParams（每轮不改的参数）

```typescript
type QueryParams = {
  messages: Message[]
  systemPrompt: SystemPrompt
  canUseTool: CanUseToolFn          // 权限检查回调
  toolUseContext: ToolUseContext     // 工具执行上下文
  taskBudget?: { total: number }    // API task_budget (beta)
  maxTurns?: number                  // 最大轮次限制
  fallbackModel?: string            // 回退模型
  querySource: QuerySource          // 查询来源 (REPL, agent等)
}
```

### State（每轮更新的可变状态）

```typescript
type State = {
  messages: Message[]
  toolUseContext: ToolUseContext
  autoCompactTracking: AutoCompactTrackingState | undefined
  maxOutputTokensRecoveryCount: number
  hasAttemptedReactiveCompact: boolean
  maxOutputTokensOverride: number | undefined
  pendingToolUseSummary: Promise<ToolUseSummaryMessage | null> | undefined
  stopHookActive: boolean | undefined
  turnCount: number
  transition: Continue | undefined   // ★ 上一轮的继续原因
}
```

**Continue Site 模式**：源码注释写道 `// Continue sites write 'state = { ... }' instead of 9 separate assignments.` 每轮结束时整个 state 对象一次性重新赋值，保证状态转换的**原子性**和**可追踪性**。

> 类比：不是逐个改9个变量（容易出现"改了5个崩了，剩下4个是旧值"），而是一次性拍一张"状态快照"。`transition` 字段记录了"为什么走到这一步"。

## 3.3 6阶段流水线

每轮对话经过6个阶段：

```
┌─────────────────────────────────────────────────────────┐
│ Stage 1: 预请求压缩 (lines 365-548)              ~183行 │
├─────────────────────────────────────────────────────────┤
│  Tool Result Budget — 裁剪过大的工具结果                 │
│  Snip Compact — 丢弃旧消息块 (最便宜、最激进)            │
│  Microcompact — 选择性清除单个工具结果 (缓存感知)        │
│  Context Collapse — 分阶段缩减 (只读投影)               │
│  Auto-Compact — LLM全量摘要 (最贵但信息损失最小)         │
├─────────────────────────────────────────────────────────┤
│ Stage 2: API 调用 & 流式处理 (lines 659-863)     ~204行 │
│  StreamingToolExecutor — Claude生成时并行执行安全工具     │
├─────────────────────────────────────────────────────────┤
│ Stage 3: 错误恢复级联 (lines 1062-1256)         ~194行  │
│  免费方案→廉价方案→昂贵方案→最终抛错                      │
├─────────────────────────────────────────────────────────┤
│ Stage 4: Stop Hooks & Token Budget (lines 1267-1355)    │
│  用户定义的验证逻辑 + 收益递减检测                       │
├─────────────────────────────────────────────────────────┤
│ Stage 5: 工具执行 (lines 1363-1520)             ~157行  │
│  收集流式结果 + 顺序执行剩余工具                         │
├─────────────────────────────────────────────────────────┤
│ Stage 6: 处理后 & 下一轮转场 (lines 1547-1727)  ~180行  │
│  收割预取结果 (技能发现, 记忆附件)                       │
│  刷新MCP服务器工具列表                                   │
│  ★ Continue Site: state = { ... } 进入下一轮             │
└─────────────────────────────────────────────────────────┘
```

### 各阶段详解

**Stage 1（压缩）的核心原则**：**始终从最便宜的选项开始**。不必要时绝不做昂贵的 Auto-Compact（需要额外 API 调用）。

**Stage 2（API调用）的并发**：`StreamingToolExecutor` 在 Claude 还在生成响应时，就开始并行执行那些"并发安全"的工具（如 `FileReadTool`、`GlobTool`、`GrepTool`）。这显著减少了端到端延迟。

**Stage 6（转场）的预取系统**：在 Stage 1 中启动的技能发现和记忆加载预取，在 Stage 6 收割结果。非阻塞、异步、不增加关键路径延迟。

## 3.4 9种终止原因

| 退出原因 | 含义 | 触发条件 |
|---------|------|---------|
| `completed` | 正常完成 | 响应结束且无工具调用 |
| `blocking_limit` | 硬Token限制 | 上下文超过窗口减去3K tokens |
| `aborted_streaming` | 用户中断流式 | Ctrl+C 在Claude生成时 |
| `aborted_tools` | 用户中断工具执行 | Ctrl+C 在工具运行时 |
| `prompt_too_long` | 即使恢复后仍超限 | 压缩和恢复均失败 |
| `image_error` | 图像验证失败 | 用户提供的图像处理出错 |
| `model_error` | 意外的模型错误 | API返回非预期错误 |
| `hook_stopped` | Stop hook阻止继续 | 用户定义的验证逻辑判定停止 |
| `max_turns` | 超过最大轮次 | 配置的轮次上限被突破 |

## 3.5 QueryEngine.ts —— 会话级监督者

```typescript
class QueryEngine {
  mutableMessages: Message[]              // 完整对话历史
  permissionDenials: PermissionDenial[]   // 工具权限拒绝记录
  totalUsage: Usage                       // 累积Token用量
  readFileState: FileStateCache           // 文件状态缓存（防重复读取）
  discoveredSkillNames: Set<string>       // 已发现的技能
  loadedNestedMemoryPaths: Set<string>    // 已加载的记忆路径
}
```

**非对称转录策略**：

- **用户消息**：阻塞保存（`await recordTranscript`）——对 `--resume` 恢复会话至关重要
- **助手消息**：即发即忘（无 `await`）——不严格需要用于会话恢复

> 设计哲学：用户说的每个字都不能丢（丢了没法恢复对话），Claude自己说的话可以重新生成。非对称投入，精准使用有限资源。

---

# 第4章：工具系统设计

## 4.1 三层注册结构

`getAllBaseTools()` 将工具分为三层：

### 始终激活（约20个核心工具）

| 工具 | 功能 | 并发安全 |
|------|------|---------|
| `BashTool` | Shell命令执行 | ❌ |
| `FileReadTool` | 文件读取 | ✅ |
| `FileEditTool` | 文件编辑 | ❌ |
| `WriteTool` | 文件写入 | ❌ |
| `GlobTool` | 文件名匹配 | ✅ |
| `GrepTool` | 内容搜索 | ✅ |
| `WebSearchTool` | 网络搜索 | ❌ |
| `WebFetchTool` | 网页抓取 | ❌ |
| `TaskTool` | 子任务创建 | ❌ |
| `AgentTool` | 子代理生成 | ❌ |

### 条件激活

| 工具 | 条件 |
|------|------|
| `PowerShellTool` | 仅 Windows 平台 |
| `GlobTool/GrepTool` | 内部构建中用 BFS/ugrep 替代 |
| `LSPTool` | 需要环境变量显式激活 |

### Feature Flag 门控（未发布，15+个）

`WebBrowserTool`, `WorkflowTool`, `SleepTool`, `PushNotificationTool`, `SubscribePRTool`, `MonitorTool`, `DiscoverSkillsTool` 等。

## 4.2 工具池组装与缓存稳定性

```typescript
export function assembleToolPool(permissionContext, mcpTools): Tools {
  const builtInTools = getTools(permissionContext)
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext)

  // ★ 分别排序以保持prompt缓存稳定
  // 内置工具作为连续前缀，MCP工具排序后拼接
  const byName = (a: Tool, b: Tool) => a.name.localeCompare(b.name)
  return uniqBy(
    [...builtInTools].sort(byName).concat(allowedMcpTools.sort(byName)),
    'name',
  )
}
```

**为什么分别排序而不是统一排序？**

Anthropic 服务器在最后一个内置工具后放置**缓存断点**。如果统一排序，添加一个 MCP 工具可能打乱整个内置工具区域，导致缓存完全失效。分别排序保证了无论用户连接多少 MCP 服务器，内置工具的排序始终稳定——缓存命中率最大化。

> 类比：图书馆的"常备书架"永远按固定顺序排列（读者不需要重新找），新到的"流动图书"放在另一排。你不会因为来了新书就把常备书架打乱重排。

## 4.3 并发安全控制

```typescript
class StreamingToolExecutor {
  private canExecuteTool(isConcurrencySafe: boolean): boolean {
    const executingTools = this.tools.filter(t => t.status === 'executing')
    return (
      executingTools.length === 0 ||
      (isConcurrencySafe && executingTools.every(t => t.isConcurrencySafe))
    )
  }
}
```

**规则**：
- 只能同时运行**并发安全**的工具
- 一旦有一个非并发安全的工具在运行，其他所有工具等待
- 同一时刻只能有一个非并发安全工具在执行

**终止原因体系**：
```typescript
type AbortReason =
  | 'sibling_error'       // 兄弟工具出错 → 同时取消我
  | 'user_interrupted'    // 用户按下 Ctrl+C / ESC
  | 'streaming_fallback'  // 因模型回退而被丢弃
```

## 4.4 动态工具搜索 (Beta)

`tool-search-2025-10-16` 特性的问题场景：当工具超过20个内置 + 数十个 MCP 工具时，工具定义本身占用数千 tokens。

解决方案：
1. 只提供一个 `ToolSearchTool`（找工具的工具）
2. Claude 需要特定工具时通过它按需加载
3. 大幅减少每次 API 调用的工具定义 token 开销

> 类比：以前每次点菜都给你一本完整的800页菜谱（多数与你无关），现在只给一页"今日推荐"和一个服务员——想吃什么问他。

---

# 第5章：8层权限安全模型

## 5.1 洋葱模型全景

```
    ╭──────────────────────────────────────────────╮
    │  L8: 全局 Kill Switch (服务器端)              │
    │  ╭────────────────────────────────────────╮  │
    │  │ L7: 项目信任对话框                      │  │
    │  │ ╭──────────────────────────────────╮   │  │
    │  │ │ L6: 文件系统沙箱验证               │   │  │
    │  │ │ ╭────────────────────────────╮   │   │  │
    │  │ │ │ L5: 危险命令硬编码拦截       │   │   │  │
    │  │ │ │ ╭──────────────────────╮   │   │   │  │
    │  │ │ │ │ L4: YOLO分类器(AI监AI)│   │   │   │  │
    │  │ │ │ │ ╭────────────────╮   │   │   │   │  │
    │  │ │ │ │ │ L3: 8级权限规则  │   │   │   │   │  │
    │  │ │ │ │ │ ╭──────────╮   │   │   │   │   │  │
    │  │ │ │ │ │ │ L2: 特性开关│   │   │   │   │   │  │
    │  │ │ │ │ │ │ ╭──────╮ │   │   │   │   │   │  │
    │  │ │ │ │ │ │ │ L1: 编│ │   │   │   │   │   │  │
    │  │ │ │ │ │ │ │译时消除│ │   │   │   │   │   │  │
    │  │ │ │ │ │ │ ╰──────╯ │   │   │   │   │   │  │
    │  │ │ │ │ │ ╰──────────╯   │   │   │   │   │  │
    │  │ │ │ │ ╰────────────────╯   │   │   │   │  │
    │  │ │ │ ╰──────────────────────╯   │   │   │  │
    │  │ │ ╰────────────────────────────╯   │   │  │
    │  │ ╰──────────────────────────────────╯   │  │
    │  ╰────────────────────────────────────────╮  │
    ╰──────────────────────────────────────────────╯
```

## 5.2 Layer 1：编译时消除（安全通过"不存在"实现）

```typescript
const WebBrowserTool = feature('WEB_BROWSER_TOOL')
  ? require('./tools/WebBrowserTool/WebBrowserTool.js').WebBrowserTool
  : null
```

`feature()` 是 **Bun 编译时内建函数**。内部构建返回 `true` → 代码保留；发布构建返回 `false` → 被 DCE 完全消除。运行时不存在的代码不存在漏洞。

> 设计哲学：最好的安全防护不是"拦住攻击"，而是"攻击目标根本不存在"。

## 5.3 Layer 2：特性开关（服务器端 Kill Switch）

GrowthBook 特性标志（`tengu_` 前缀）：

| 标志 | 作用 | 机制 |
|------|------|------|
| `tengu_amber_quartz_disabled` | 语音模式 Kill Switch | 服务器端一键禁用 |
| `tengu_bypass_permissions_disabled` | 绕过权限模式 Kill Switch | 无需客户端更新 |
| `tengu_auto_mode_config.enabled` | 自动模式断路器 | 连续拒绝后回退 |
| `tengu_ccr_bridge` | 远程控制资格检查 | 按账户/组织门控 |
| `tengu_sessions_elevated_auth_enforcement` | 要求受信任设备令牌 | 高安全模式 |

**关键设计**：Kill Switch 不依赖客户端更新。Anthropic 可以在服务器端一键关闭任何功能，所有客户端即时生效。

## 5.4 Layer 3：8级权限规则优先级

```typescript
type PermissionRule = {
  source: PermissionRuleSource
  ruleBehavior: 'allow' | 'deny' | 'ask'
  ruleValue: { toolName: string; ruleContent?: string }
}
```

优先级（数字越小越高）：

| 优先级 | 来源 | 范围 | 可被覆盖？ |
|--------|------|------|-----------|
| 1 (最高) | `userSettings` — `~/.claude/settings.json` | 全局 | 否 |
| 2 | `projectSettings` — `.claude/settings.json` | 项目级 | 是（被1覆盖） |
| 3 | `localSettings` — `.claude/local.json` | 本地（不提交Git） | 是（被1-2覆盖） |
| 4 | `flagSettings` — GrowthBook特性标志 | 服务器端 | 是 |
| 5 | `policySettings` — 组织级策略 | 企业管理员 | 是 |
| 6 | `cliArg` — 命令行参数 | 单次会话 | 是 |
| 7 | `command` — 运行时规则更新 (`/allow`) | 单次会话 | 是 |
| 8 (最低) | `session` — 内存中仅会话规则 | 重启消失 | 是 |

> 设计亮点：用户全局设置是"天花板"——项目设置不能放宽用户设置的约束。组织策略不过度限制个人选择。

## 5.5 Layer 4：YOLO 分类器（AI 监控 AI）

**文件**：`yoloClassifier.ts`（52K）

自动模式下，额外的 Claude API 调用独立判断每次工具使用的安全性：

```
1. 工具使用请求发生
2. 白名单检查
   └ FileRead, Grep, Glob, Tasks等 (只读) → 跳过分类器，自动允许
3. 分类器 API 调用 → "allow" 或 "deny"
4. 拒绝跟踪：
   └ 连续3次拒绝 → 回退到 prompting 模式
   └ 总计20次拒绝 → 回退到 prompting 模式
5. 分类器自身失败 → 回退到 prompting（Fail Open：不自动拒绝）
```

- 环境变量 `CLAUDE_CODE_DUMP_AUTO_MODE=1` 可转储分类器请求/响应为 JSON

> Fail Open 原则：分类器不确定时，回退到"询问用户"模式，而非自动拒绝。宁可打扰用户，也不错杀合理操作。

## 5.6 Layer 5：危险命令硬编码拦截

```typescript
DANGEROUS_BASH_PATTERNS = [
  'python', 'node', 'ruby', 'perl', 'bash', 'sh', 'zsh', 'ksh',
  'exec', 'eval', 'source',
  'curl', 'wget', 'nc', 'ncat', 'socat',
  'dd', 'xxd', 'openssl',
  'ssh', 'scp', 'sftp',
  'sudo', 'su', 'chroot', 'unshare', 'docker', 'podman',
  'chmod', 'chown', 'chgrp', 'umask', 'mount', 'umount'
]
```

特别拦截 `python:*` 作为允许规则——因为通过解释器可以绕过所有 Bash 级安全检查。

## 5.7 Layer 6-8：文件沙箱 · 信任对话框 · Kill Switch

- **Layer 6**：绝对路径规范化、符号链接逃逸预防、安全 glob 展开、CWD-only vs 完全访问模式、Scratchpad 支持
- **Layer 7**：首次在项目中运行 Claude Code 时，显示信任对话框审阅 `.claude/settings.json`——防恶意项目配置
- **Layer 8**：`bypassPermissionsKillswitch.ts`——服务器端全局禁用绕过权限模式

## 5.8 安全设计原则总结

1. **默认拒绝** — 无显式允许规则则拒绝
2. **无法判断则提示，不自动拒绝** — Fail-Open（"通过"意味着"让用户决定"）
3. **纵深防御** — 无单点故障。突破某一层不意味着完全沦陷
4. **服务器端 Kill Switch** — 无需客户端更新即可禁用功能
5. **构建时消除** — 代码不在二进制中，漏洞也不存在

---

# 第6章：上下文管理机制

## 6.1 核心原则：从最便宜的开始

```
成本:     $0              $0           ~$0.001      ~$0.01+
         │               │               │             │
     Snip         Microcompact    ContextCollapse  AutoCompact
   (丢弃旧块)     (清过期结果)      (只读投影)     (AI摘要)
  信息损失高      信息损失中       信息损失中       信息损失低
```

## 6.2 四层压缩详解

| 层级 | 成本 | 信息损失 | 缓存影响 | 核心机制 |
|------|------|---------|---------|---------|
| **Snip** | 免费 | 高 | 无 | 直接丢弃旧消息块。主要用于无头会话 |
| **Microcompact** (530行) | 免费 | 中 | 通过"固定"最小化 | 选择性清除工具结果，替换为 `[Old tool result content cleared]` |
| **Context Collapse** | 低成本 | 中 | 最小（一次性重置） | 类似数据库视图的只读投影，原始消息永不修改 |
| **Auto-Compact** (351行) | 高 | 低 | 完全重置 | 发送整个历史给Claude请求摘要。断路器：3次失败即停 |

## 6.3 Microcompact 的"缓存编辑块固定"

这是整个压缩系统最精致的部分：

```
假设30轮对话 = 若干文件读取结果分散在消息中

缓存范围 = [消息0, 消息400]（Anthropic的prompt缓存在前400条消息）
候选清除 = 消息中所有旧的 file_read 结果
固定策略 = 不触碰缓存范围内的结果（清除它们会破坏缓存）
提交策略 = 下一轮缓存移动后，再清除之前固定的候选
```

> 类比：你正在用书签读一本厚书。笔（缓存编辑块）标记了"可删除的段落"。但你不会在读到那一页之前就把段落撕掉——那会弄丢页码。等翻过那一页了，再撕。

## 6.4 Context Collapse 的只读投影

```typescript
// 不产生输出 — 折叠视图是对 REPL 完整历史的只读投影
// 摘要消息存在于 collapse store 中，而非 REPL 数组中
// 这就是折叠在轮次间持久化的原因: projectView() 在每次入口重放提交日志
```

**两阶段模型**（类似 Git）：
- **预览阶段**：标记可折叠的消息块
- **提交阶段**：实际折叠

原始消息永不修改——折叠结果存储在独立的 `collapse store` 中，在发送给 API 时通过 `projectView()` 覆盖折叠视图。

> 类比：Git 的 commit 不修改原始文件。你的 repo 里文件没变，但你通过 `git log` 看到的是一个"折叠后"的历史视图。

## 6.5 Token 警告状态机

```
[正常] ← 绿色。一切正常
  ↓ 上下文窗口 - 20K tokens
[警告] ← 黄色。"对话正在变长"
  ↓ 上下文窗口 - 20K tokens
[错误] ← 橙色。"压缩即将触发"
  ↓ 上下文窗口 - 13K tokens
[自动压缩] ← Auto-Compact 触发。通知用户
  ↓ 上下文窗口 - 3K tokens
[阻塞限制] ← 红色。自动压缩不够，仅 /compact 可选
```

## 6.6 三层记忆架构

| 层级 | 存储位置 | 加载策略 | 用途 |
|------|---------|---------|------|
| 工作上下文 | `CLAUDE.md` / `MEMORY.md` | 始终加载 | 项目当前状态 |
| 项目笔记 | 独立结构化文件 | 按需搜索 | 长期知识积累 |
| 会话历史 | 过去对话日志 | 选择性搜索 | 跨会话记忆 |

在 Agent 循环的 Stage 1 中预取记忆附件，Stage 6 收割结果——不阻塞关键路径。

---

# 第7章：MCP 集成与 API 通信

## 7.1 MCP 客户端

**文件**：`client.ts`（119K）——泄露中确认的巨大 MCP 模块。

Claude Code 使用 `@modelcontextprotocol/sdk` 作为 MCP 客户端，连接到用户配置的外部工具服务器。MCP 客户端连接传递到 `ToolUseContext` 中：

```typescript
type ToolUseContext = {
  options: { 
    tools: Tools
    mainLoopModel: string
    mcpClients: MCPServerConnection[]  // MCP服务器连接列表
  }
}
```

## 7.2 MCP 工具集成流程

1. 用户配置 `.claude/mcp.json` 定义 MCP 服务器
2. 启动时建立 MCP 客户端连接
3. 每轮 Stage 6 刷新 MCP 工具列表（外部服务可能更新）
4. `assembleToolPool()` 合并内置工具和 MCP 工具
5. MCP 工具经过权限过滤（`filterToolsByDenyRules`）
6. 合并后的工具池发送给 Claude API

## 7.3 API 调用架构

```typescript
// 每次API调用的消息构建
for await (const message of deps.callModel(
  fullSystemPrompt,                                      // 系统提示词
  prependUserContext(messagesForQuery, userContext),     // 预处理后的消息
  toolUseContext,                                        // 工具上下文
  { taskBudget, taskBudgetRemaining,                     // 预算信息
    maxOutputTokensOverride, skipCacheWrite },           // 输出控制
)) { /* 处理流式事件 */ }
```

### 系统提示词组成

```
完整系统提示词 = 
  基础系统提示词
  + 内置工具定义 (JSON Schema)
  + MCP 工具定义 (追加在内置工具后)
  + CLAUDE.md 项目上下文
  + 当前技能发现结果
  + 记忆附件
```

### 模型回退与墓碑消息

```typescript
if (innerError instanceof FallbackTriggeredError && fallbackModel) {
  currentModel = fallbackModel
  // 为孤儿消息创建墓碑
  yield* yieldMissingToolResultBlocks(assistantMessages, 'Model fallback triggered')
}
```

**墓碑消息（Tombstone）**：从数据库借用的概念。当模型切换时，前一模型请求的工具调用不再有效。墓碑标记"此工具调用因模型回退被丢弃"，保持历史一致性。

## 7.4 Prompt 缓存策略

Anthropic 服务器使用 `claude_code_system_cache_policy`，在最后一个匹配的内置工具后放置**全局缓存断点**。工具列表的排序策略直接影响缓存命中率——这也是为什么 `assembleToolPool()` 要分别排序的原因。

---

# 第8章：错误处理与恢复机制

## 8.1 Prompt-Too-Long（413）3 级恢复

```
Stage 1: Context Collapse drain (成本: $0)
  └ 已准备的候选块立即提交以缩小上下文
  └ 无需额外 API 调用

Stage 2: Reactive Compact (成本: 1次API调用)
  └ 摘要整个对话，剥离图像，重试
  └ "strip retry" — 如果摘要过大，移除媒体重试

Stage 3: 抛错给用户
```

## 8.2 Max-Output-Tokens 3级恢复

```
Stage 1: Token上限升级 (成本: $0)
  └ 透明地从 8K → 64K (ESCALATED)

Stage 2: 恢复消息注入 (成本: API重调用, 最多3次)
  └ 注入: "Your previous response was truncated. Continue from where you left off."
  └ 最多尝试3次

Stage 3: 恢复耗尽 → 使用可用结果完成
```

## 8.3 收益递减检测

```typescript
function checkTokenBudget(tracker, budget, globalTurnTokens) {
  const isDiminishing = (
    continuationCount >= 3 &&        // 连续继续3次以上
    deltaSinceLastCheck < 500 &&     // 自上次检查少于500 tokens
    lastDeltaTokens < 500            // 上次检查也少于500 → "空转"
  )
  // 如果空转 → 停止
  // 如果正常 → 继续
}
```

**设计理念**：如果 Agent 连续3轮以上每次只产出 <500 tokens，说明它在"反复调整但没实质进展"——及时止损，告诉用户情况。

## 8.4 断路器模式汇总

| 位置 | 断路条件 | 后果 |
|------|---------|------|
| Auto-Compact | 连续3次摘要失败 | 停止重试，移交错误级联 |
| YOLO分类器 | 连续3次拒绝 | 回退到prompting模式 |
| YOLO分类器 | 总计20次拒绝 | 回退到prompting模式 |
| Max-Output恢复 | 3次恢复人仍失败 | 使用可用结果完成 |

---

# 第9章：未发布功能全景

## 9.1 Coordinator Mode — 多代理编排

**门控**: `COORDINATOR_MODE`（19K代码）

协调器不直接写代码——它是元编排器，生成多个 worker 代理并分配任务：

```typescript
COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  'AgentTool',           // 生成 worker
  'TaskStop',            // 终止 worker
  'SendMessage',         // 与 worker 通信
  'SyntheticOutput',     // 合并 worker 结果作为最终输出
])
```

协调器**不能执行 Bash**，不能读取文件——只能管理 worker。这是最小权限原则的极端应用。

> 类比：项目经理不自己写代码、不动服务器、不碰数据库。他只开会、分配任务、审阅结果、整合汇报。

## 9.2 KAIROS — 主动代理模式

KAIROS（希腊语"恰当时机"）是 Claude **先行动**的模式：

| 门控标志 | 工具 | 能力描述 |
|---------|------|---------|
| `KAIROS` | `SendUserFileTool` | 主动向用户发送文件 |
| `KAIROS` + `KAIROS_PUSH_NOTIFICATION` | `PushNotificationTool` | 移动/桌面推送通知 |
| `KAIROS_GITHUB_WEBHOOKS` | `SubscribePRTool` | GitHub PR webhook 订阅 |
| `PROACTIVE` + `KAIROS` | `SleepTool` | 后台等待（定时器），到点自动醒来 |
| `KAIROS_CHANNELS` | (未知) | 多渠道集成（Slack/Discord/邮件） |
| `KAIROS_BRIEF` | (未知) | 检查点/状态更新 |

`autoDream` 后台进程在空闲期间处理记忆合并，无需中断活动会话上下文。

## 9.3 Bridge — 远程控制系统（33+文件）

连接流程：
```
1. 用户 → OAuth 登录 claude.ai
2. CCR API → 订阅 + GrowthBook 门控检查
3. 本地 Claude Code → 获取 environment_id + environment_secret
4. WebSocket 认证隧道
5. 浏览器 → Bridge API → 本地工具执行 → 结果返回
```

安全层级：
- **Standard**：OAuth
- **Elevated**：OAuth + 受信任设备 JWT
- 会话通过 **Git worktree** 隔离（你的项目不会被其他会话污染）

## 9.4 其他未发布功能

| 功能 | 描述 |
|------|------|
| **Voice 语音模式** | `voice_stream` 端点，OAuth 认证，Kill Switch 控制 |
| **Web Browser 工具** | 基于 Bun WebView 的真正浏览器自动化 |
| **Agent Triggers** | Cron 创建/删除/列表工具，自调度代理 |
| **UDS Inbox** | 多设备消息传递（`ListPeersTool`） |
| **Workflow Scripts** | 预构建自动化脚本，带初始化系统，防递归执行 |
| **AFK 模式** | 用户离开时继续操作 |
| **Advisor 工具** | 额外推理/规划层（双模型架构） |
| **Redact Thinking** | 隐藏扩展思考痕迹 |

## 9.5 动物代号体系

| 代号 | 含义 |
|------|------|
| **Capybara** | 当前主版本 |
| **Tengu** | 项目代号（日语"天狗"，GrowthBook标志 `tengu_` 前缀） |
| **Numbat** | 下一代架构 |
| **Fennec** | Opus 4.6 代号 |

## 9.6 卧底模式（Undercover Mode）

源码中发现的独特安全机制：在某些场景下，Claude 使用 `UNDERCOVER` 系统提示词——防止 AI 在公开的 Git 提交信息中暴露 Anthropic 的内部代号。

> 这是针对 AI 编码工具特有安全威胁的创造性应对——AI 不知道什么该公开、什么不该。

## 9.7 虚假工具注入（Fake Tools）

主动防御模型蒸馏攻击——注入虚假工具定义，使试图偷取模型能力的攻击者获得被污染的数据。

---

# 第10章：业内评价与源码启示

## 10.1 关键专业人士评价

| 人物 | 身份 | 核心评价 |
|------|------|---------|
| **Chaofan Shou** | 安全研究员/首位披露者 | 2880万阅读的X帖子引爆全网关注 |
| **Rittika Jindal** | LinkedIn深度分析作者 | "构建AI Agent的人的金矿。卧底特工自己暴露了！" |
| **Alex Kim** | 技术分析师 | 特别关注了虚假工具、挫败正则表达式、卧底模式 |
| **Straiker** | AI安全公司 | "攻击者可以研究四阶段上下文管线，构造活过压缩的后门载荷" |
| **Violetta Bonenkamp** | Mean CEO Blog | "2026年的运营原则：假设你的代码会泄露" |
| **Clement Dumas** | 安全研究员 | 发现 npm typosquat 攻击：先占位等下载量，再推送恶意更新 |

## 10.2 安全漏洞（CVE）

| CVE | 描述 | 严重程度 | 状态 |
|-----|------|---------|------|
| CVE-2025-59536 | 通过恶意 project hooks 实现 RCE | 严重 | 已修复 |
| CVE-2026-21852 | 通过环境变量替换泄露 API 密钥 | 严重 | 已修复 |

均由外部研究人员用泄露代码发现。

## 10.3 供应链攻击

1. **同日 Axios 攻击**（2026年3月31日 UTC 00:21-03:29）：npm 安装可能拉取木马化 HTTP 客户端（含跨平台 RAT）
2. **Typosquatting**：用户 "pacifier136" 发布5个依赖混淆包
3. **假冒仓库**：Zscaler 发现 Vidar Stealer + GhostSocks；Huntress 发现 Bing 搜索重定向攻击

## 10.4 源码启示：构建 AI Agent 的要与不要

**要构建的**：
- 多语言支持、隐私遥测、明确安全约束
- 可扩展路由架构、工作流集成钩子
- 成本感知设计（从最便宜的方案开始）

**要避免的**：
- 未批准自动执行、模糊安全指南
- Source Map 发布（自动化剥离检查）
- 过度集中控制（Kill Switch 应该服务器端）

**工程教训**：
- "假设集成代码会公开。API 密钥绝不在源码中。"
- "假设代码会泄露。设计基础设施使泄露不影响用户数据。"

---

# 第11章：未来展望

## 11.1 Claude Code 的战略演进方向

从泄露源码中可见 Anthropic 的战略版图远不止"终端代码助手"：

### 从单 Agent 到多 Agent 编排

`Coordinator Mode` 的设计表明 Anthropic 正在建设**分层 Agent 架构**：顶层协调器负责任务分解和资源分配，底层 Worker 负责具体执行。这和 LangChain、AutoGPT 的"工具调用"模式有本质区别——Coordinator 是一等公民，有自己的工具集、安全边界和权限模型。

### 从被动响应到主动代理

`KAIROS` 模式的 Sleep Tool、Push Notification、Cron 调度揭示了方向：**Claude Code 不只是等你下指令，而是会在后台自主运行**。这个转变比"终端还是IDE"的讨论更重要——它意味着 AI Agent 从"工具"进化为"同事"。

### 从本地到云端/远程

`Bridge` 系统（33+文件）的 WebSocket 隧道和 OAuth 认证表明 Anthropic 在建设**跨设备的 Agent 基础设施**。你在浏览器里操控本地电脑上的 Claude Code，或者反过来——Claude Code 在服务器上运行但操作你本地文件。

### 从代码到通用 Agent

Voice、Web Browser、Multi-Channel 的能力表明 Claude Code 的终局不是"更好的 Copilot"——它是 Anthropic 的 **AI Agent 操作系统**。代码编辑只是第一个应用场景。

## 11.2 源码泄露对行业的影响

**短期（2026年内）**：
- 更多 AI 编码工具将借鉴 Claude Code 的架构模式（Async Generator、4层压缩、8层安全）
- 安全研究方向将转移到"针对 AI Agent 上下文窗口的攻击"
- Anthropic 可能加速原生二进制发布，减少 npm 依赖

**中期（2027-2028）**：
- "生产级 AI Agent"的工程标准将被建立（Claude Code 就是事实标准）
- 供应链安全将纳入 AI 工具的合规要求
- "开源接口、闭源核心"将成为 AI 工具的标准发布模式

**长期**：
- AI Agent 的操作系统级集成（类似 Claude Code 的 Bridge 模式但标准化）
- 安全模型的标准化：8层洋葱可能成为行业参考架构

## 11.3 对 Hermes / izu 的启示

1. **Async Generator 模式**值得借鉴——统一事件流、终止、错误处理
2. **4层压缩**中"从便宜到贵"的成本感知设计是通用原则
3. **Continue Site 模式**的状态原子更新适用于长对话 Agent
4. **失效分类器 + Fail Open** 的安全哲学值得学习——"不确定时问用户，不自动拒绝"
5. **工具池缓存稳定性**的设计揭示了 prompt 缓存实践的深层技巧
6. **编译时功能门控**（`feature()`）是管理功能演进的优雅方案

---

## 附录：术语表

| 中文 | English | 使用场景 |
|------|---------|---------|
| 异步生成器 | Async Generator | `query.ts` 主循环使用 `async function*` 模式 |
| 继续站点 | Continue Site | 每轮结束时的状态原子更新模式 |
| 墓碑消息 | Tombstone Message | 模型回退时标记无效工具调用 |
| 流式工具执行器 | StreamingToolExecutor | Claude响应时并行执行安全工具 |
| 只读投影 | Read-Time Projection | Context Collapse 的视图机制 |
| 缓存编辑块固定 | Cache Edit Block Pinning | Microcompact 中保护缓存范围内的结果 |
| 断路器 | Circuit Breaker | 连续失败3次后停止重试的模式 |
| 失效开放 | Fail Open | 分类器失败时回退到询问用户而非自动拒绝 |
| 死代码消除 | Dead Code Elimination (DCE) | `feature()` 编译时移除未发布功能 |
| 洋葱模型 | Onion Model | 8层纵深防御的安全架构 |
| 特性门控 | Feature Gate | 通过 `feature('FLAG')` 控制代码是否编译 |
| Kill Switch | Kill Switch | 服务器端一键禁用功能的机制 |
| 提示词缓存 | Prompt Cache | Anthropic API 的上下文缓存机制 |
| 工具池 | Tool Pool | `assembleToolPool()` 合并内置+MCP工具 |
| 上下文压缩 | Context Compaction | 4层压缩系统总称 |
| 微观压缩 | Microcompact | 选择性清除过期工具结果 |
| 上下文折叠 | Context Collapse | 类似Git的两阶段折叠（预览→提交） |
| 自动压缩 | Auto-Compact | LLM全量摘要压缩 |
| 收益递减检测 | Diminishing Returns Detection | 检测Agent是否在"空转" |
| 协调器模式 | Coordinator Mode | 多代理编排（未发布） |
| 主动代理 | KAIROS (Proactive Agent) | 不等用户指令自主行动 |
| 远程控制桥 | Bridge | WebSocket隧道连接浏览器与本地CLI |
| 梦境模式 | Dream Mode (autoDream) | 后台处理记忆合并 |
| 卧底模式 | Undercover Mode | 防止AI泄露内部代号到公开Git提交 |
| 虚假工具 | Fake Tools | 主动防御模型蒸馏攻击 |
| 依赖混淆 | Dependency Confusion | 供应链攻击：发布与内部包同名的公开包 |
| 打字抢注 | Typosquatting | 供应链攻击：发布名称相近的恶意包 |
| 受信任设备 | Trusted Device | Bridge高安全模式所需的设备JWT |
| Git worktree | Git Worktree | Bridge会话隔离机制 |
| 非对称转录 | Asymmetric Transcript | 用户消息阻塞保存，助手消息即发即忘 |
| 任务预算 | Task Budget | `task_budget` API参数控制Agent总token用量 |

---

## 参考文献

| # | 来源 | URL |
|---|------|-----|
| 1 | Bits-Bytes-NN 架构分析 | bits-bytes-nn.github.io/insights/agentic-ai/2026/03/31/claude-code-architecture-analysis.html |
| 2 | Reddit r/ClaudeAI 深度解读 | reddit.com/r/ClaudeAI/comments/1sa6ih3/ |
| 3 | Verdent AI 架构洞察 | verdent.ai/guides/claude-code-source-code-leak-architecture |
| 4 | Layer5 工程分析 | layer5.io/blog/engineering/the-claude-code-source-leak-512000-lines |
| 5 | The Hacker News 报道 | thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html |
| 6 | Mean CEO Blog 深度分析 | blog.mean.ceo/claude-codes-full-source-code-just-leaked/ |
| 7 | HuggingFace 社区讨论 | discuss.huggingface.co/t/claude-code-source-leak/174846 |
| 8 | LinkedIn Rittika Jindal 分析 | linkedin.com/posts/rittika-jindal...-7445148213378113537-95Cb |
| 9 | Augment Code 市场分析 | augmentcode.com/learn/anthropic-claude-code-github-stars |
| 10 | Claude Code 官方仓库 | github.com/anthropics/claude-code |
| 11 | Claude Code npm 页面 | npmjs.com/package/@anthropic-ai/claude-code |
| 12 | Claude Code 官方文档 | docs.anthropic.com/en/docs/claude-code |
| 13 | GitHub 源码收集 | github.com/chauncygu/collection-claude-code-source-code |
| 14 | GitHub 源码分析 | github.com/yangzhaoliu/claude-code-source-code |
