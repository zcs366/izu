---
title: "Claude Code 范式深入（续）：压缩/协调器/缓存/Circuit Breaker"
source: "Claude Code v2.1.88 泄露源码 + 腾讯云/知乎深度分析"
author: "军师"
date: 2026-05-20
tags: [claude-code, compression, coordinator, prompt-cache, circuit-breaker, hermes, izu]
status: comparison
---

> **本报告承接** `comparisons/claude-code-patterns-hermes.md`，补完之前未展开的四大范式。

---

## 范式七：4层压缩管线 — 成本感知设计的教科书

Claude Code 的上下文压缩不是"满了就摘要"——而是一个从最便宜到最贵的**阶梯式管线**。

```
成本:      $0              $0           ~$0.001      ~$0.01+
         │               │               │             │
     Snip         Microcompact    ContextCollapse  AutoCompact
   (丢弃旧块)     (清过期结果)      (只读投影)     (AI摘要)
  信息损失高      信息损失中       信息损失中       信息损失低
```

### 每层详解

| 层级 | 成本 | 信息损失 | 机制 | 触发条件 |
|------|------|---------|------|---------|
| **Snip** | $0 | 高 | 直接丢弃最旧的消息块 | Token超预算时 |
| **Microcompact** | $0 | 中 | 选择性清除旧工具结果，替换为 `[Old tool result content cleared]` | 超预算，需要更多空间 |
| **Context Collapse** | ~$0.001 | 中 | 类似数据库**只读投影**——原始消息不修改，发送时覆盖折叠视图 | Microcompact不够 |
| **Auto-Compact** | ~$0.01+ | 低 | 发送整个历史给Claude请求摘要（9段式） | Collapse不够 |

### 两点最精致的设计

**① Microcompact 的"缓存编辑块固定"**
```
缓存范围 = [消息0, 消息400]（Anthropic的prompt缓存区）
策略   = 不触碰缓存范围内的工具结果（清除会破坏缓存）
提交   = 下一轮缓存移动后，再清除之前固定的候选
```
类比：你用书签读厚书。笔标记了"可删除的段落"。但你不会在读到那一页之前就撕掉——等翻过去了再撕。

**② Context Collapse 的只读投影**
```typescript
// 摘要消息存在于 collapse store 中，而非消息数组中
// 这就是折叠在轮次间持久化的原因:
// projectView() 在每次入口重放提交日志
```
原始消息永不修改。两阶段模型（类似Git）：预览 → 提交。

### 对 Hermes 的启示

我们的 session 管理目前只有"全量保存"和"session_search检索"两个极端。缺少中间的**压缩阶梯**：

| 当前 | 应补充 |
|------|--------|
| 全量保存 | + Microcompact：清理过期工具输出 |
| session_search 全库检索 | + Context Collapse：为长会话建立折叠视图 |
| 无摘要 | + Auto-Compact：超长会话自动生成9段式摘要 |

---

## 范式八：Coordinator 最小权限 — 项目经理模式

### 核心设计

Coordinator（协调者）只有 **3 个工具**：

```typescript
COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  'AgentTool',      // 生成 worker 子代理
  'TaskStop',       // 终止 worker
  'SendMessage',    // 与 worker 通信
  // 没有 BashTool！没有 FileReadTool！没有 FileWriteTool！
])
```

**Coordinator 不能执行 Bash，不能读/写文件**——只能管理 worker。这是最小权限原则的极端应用：
> 项目经理不自己写代码、不动服务器、不碰数据库。他只开会、分配任务、审阅结果。

### 6种任务类型

| 类型 | 说明 | 场景 |
|------|------|------|
| `local_bash` | Shell命令执行 | 编译、测试 |
| `local_agent` | 本地代码修改 | 重构、修Bug |
| `remote_agent` | 远程执行 | 服务器操作 |
| `in_process_teammate` | 平行唤醒多个Agent | 大规模并行探索 |
| `local_workflow` | 预定义工作流 | CI/CD |
| `dream` | 记忆整合 | Memory consolidation |

### 三个关键机制

**① Fork 继承 Prompt Cache**
- 子 Agent fork 时继承父会话的 KV 缓存
- 起步成本极低——不需要重新加载工具定义、系统规则

**② 隔离探索**
- 子 Agent 在独立上下文窗口运行
- 所有中间输出、错误信息局限在子上下文
- 不会污染主对话

**③ 结论回传（XML 结构化）**
```xml
<task-notification>
  <task_id>...</task_id>
  <conclusion>提炼后的关键结论</conclusion>
  <artifacts>[文件路径列表]</artifacts>
</task-notification>
```
不是把子 Agent 对话全文传回去——只传结构化结论。

### in_process_teammate 的 AppleScript 联动

Claude Code 源码集成了 iTerm2/Terminal.app 的 AppleScript 控制，自动切分窗格：

```applescript
tell application "iTerm2"
  tell current window
    split vertically with default profile
  end tell
end tell
```

这展示了 Anthropic 对**用户工具体验**的极致追求——不是只在命令行里塞文字，而是利用操作系统API改善体验。

### 对 Hermes 的启示

我们的 `delegate_task` 已经实现了"fork 子 Agent"的基本功能，但有四个关键差距：

| 维度 | Claude Code | Hermes delegate_task |
|------|------------|---------------------|
| 最小权限 | Coordinator 只有3个工具 | 没有 Coordinator 层 |
| 缓存继承 | 继承父 Prompt Cache | 无（从头创建） |
| 结论格式 | XML结构化 | 自由文本 |
| 任务类型 | 6种专用类型 | 1种通用 |

**建议**：
1. 为 delegate_task 引入任务类型（`type: "research" | "code" | "consolidation" | "exploration"`）
2. 实现结构化结论格式化
3. 研究"继承缓存"的可能性

---

## 范式九：Prompt Cache 三个优化技巧

### ① 分段缓存 + 硬编码边界

```
SYSTEM_PROMPT_DYNAMIC_BOUNDARY   # 硬编码分隔符
┌─ 静态段（全局缓存）──────────┐
│  身份、规则、行为准则           │ ← 几乎不变，高缓存命中
├─ 边界 ─────────────────────┤
│  动态段（会话内缓存）          │ ← 可能变化
│  MCP指令（唯一不缓存部分）      │ ← 真正的变量
└──────────────────────────────┘
```

### ② 确定性排序

工具描述**严格按字母表排序**。内置工具放前缀，MCP 工具放后缀。保证每次请求的 prompt 哈希一致：
```
BashTool < FileReadTool < FileWriteTool < GrepTool
```
任何非确定性排序（如按工具名自然顺序而非字母顺序、按注册顺序）都会导致缓存每次失效。

### ③ 状态外置

将 Agent 列表从工具描述中剥离，转移到**消息附件（Attachments）**：
- 工具描述不再携带"可用 Agent 列表"
- 附件在系统提示之外独立缓存
- 减少约 **10.2%** 的 Cache Creation Tokens

### 对 Hermes 的启示

我们目前用 DeepSeek API（MiniMax），暂时不涉及 prompt cache。但两个设计原则是通用的：

1. **确定性排序** —— 所有列表（工具列表、skills列表、配置项）都应该按稳定顺序排列，不管是字母表还是别的
2. **不变量外置** —— 频繁变化的部分与稳定部分分离，不混在同一个结构里

---

## 范式十：Circuit Breaker 模式集

Claude Code 源码中散布着多种断路器模式：

| 位置 | 断路条件 | 后果 |
|------|---------|------|
| Auto-Compact | 连续3次摘要失败 | 停止重试，移交错误级联 |
| YOLO 分类器 | 连续3次拒绝 | 回退到 prompting 模式 |
| YOLO 分类器 | 总计20次拒绝 | 回退到 prompting 模式 |
| Max-Output 恢复 | 3次恢复仍失败 | 使用可用结果完成 |

### 收益递减检测（Diminishing Returns Detection）

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

**核心思想**：如果 Agent 连续3轮以上每轮只产出 <500 tokens，说明它在"反复调整但没实质进展"——及时止损。

### Max-Output-Tokens 三级恢复

```text
Stage 1: Token 上限升级 (成本: $0)
  └ 透明地从 8K → 64K (ESCALATED)

Stage 2: 恢复消息注入 (成本: API重调用, 最多3次)
  └ 注入: "Your previous response was truncated. Continue from where you left off."

Stage 3: 恢复耗尽 → 使用可用结果完成
```

### 对 Hermes 的启示

我们目前在 `delegate_task` 中没有 Circuit Breaker。如果一个子 Agent 空转了，用户可能等到超时才知道。建议补充：

1. Token 产出监控——如果子 Agent 连续N轮产出极少，主动中断
2. 断路器模式——API调用连续失败N次后降级，不无限重试
3. Fail Open 哲学——分类器不确定时问用户，不直接拒绝

---

## 范式十一：ToolSearch 按需加载（Code Splitting for Tools）

### 是什么

Claude Code 有 40+ 内置工具 + 任意数量 MCP 工具。全部加载到 prompt 中会膨胀上下文。解决方案：

- 核心工具（BashTool, FileReadTool, FileWriteTool, GrepTool, GlobTool）——始终加载
- 非核心工具标记 `defer_loading: true`——模型只知道有 `ToolSearch` 可用
- 需要时调用 `ToolSearch(keyword)` → 动态加载对应工具定义
- 类似 Web 开发的 Code Splitting

```text
默认加载 (~20个核心工具)    按需加载 (20+个非核心工具)
┌────────────────────┐    ┌────────────────────┐
│ BashTool            │    │ WebFetchTool        │ ← 用户说"去查官网"时才加载
│ FileReadTool        │    │ DockerTool          │ ← 用户说"跑docker"时才加载
│ FileWriteTool       │    │ MCPTool_xxx         │ ← 按需
│ GrepTool            │    │ ...                 │
│ GlobTool            │    └────────────────────┘
│ AgentTool           │
│ ...                 │
└────────────────────┘
```

此外还有一个极简模式 `CLAUDE_CODE_SIMPLE` —— 只保留 3 个基础工具（Bash/Read/Write）。

### 对 Hermes 的启示

我们目前所有工具都加载到所有会话中。可以考虑：

1. 工具分级：核心工具（始终加载） vs 扩展工具（按需加载）
2. 工具池根据当前任务动态组装
3. 为简单任务提供精简工具集

当前所有工具都可用，是因为 Hermes 的 toolsets 机制本身就是按需分组 —— 但 cron job 的 enabled_toolsets 做得很好，主会话还没来得及。

---

## 对照总表：Claude Code 关键范式评级

| # | 范式 | 当前 Hermes 状态 | 采纳价值 | 工作量 |
|---|------|-----------------|---------|--------|
| 7 | 4层压缩管线 | 无（全量保存或检索） | ★★★★ | 3天 |
| 8 | Coordinator 最小权限 | delegate_task 无类型区分 | ★★★★★ | 1天 |
| 9 | Prompt Cache 优化 | 不适用（非Anthropic API） | ★★ | 记录在案 |
| 10 | Circuit Breaker | 无 | ★★★★ | 0.5天 |
| 11 | ToolSearch 按需加载 | cron job 有 toolsets，但主会话无 | ★★★ | 1天 |

**最优先**：Circuit Breaker（半天，立即提升稳定性，可先加在 morning_consolidation cron job 里）
**次优先**：Coordinator 任务类型（引入类型区分，让 delegate_task 更智能）
**再次**：压缩管线（深改，需要 session 管理重构）

---

## 参考源

1. 腾讯云开发者社区：Claude Code 源码泄露5个Agent设计模式拆解
2. 知乎专栏：Claude Code 源码深度解析
3. 知乎专栏：当AI学会了"做梦"
4. Sabrina.dev：Comprehensive Analysis of Claude Code Source Leak
