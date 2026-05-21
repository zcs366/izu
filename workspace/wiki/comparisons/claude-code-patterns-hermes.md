---
title: "Claude Code 源码范式提取报告 —— 可直接复用的 Agent 设计模式"
source: "Claude Code v2.1.88 泄露源码 + 社区分析"
author: "军师"
date: 2026-05-20
tags: [claude-code, agent-pattern, architecture, memory, consolidation, hermes, izu]
status: comparison
---

> **本报告目的**：从 Claude Code 51.2万行泄露源码中，提取对 Hermes Agent 和 izu 系统**可直接复用的设计范式**，按优先级排列。

---

## 概览：六大范式

| # | 范式 | 复杂度 | 复用价值 | 优先级 |
|---|------|--------|---------|--------|
| 1 | **AutoDream 三重门** | ★★ | ★★★★★ | **P0 — 立即抄** |
| 2 | **Fork Subagent 隔离** | ★★★ | ★★★★★ | **P0 — 立即抄** |
| 3 | **MEMORY.md 索引制** | ★ | ★★★★ | **P0 — 立即抄** |
| 4 | **Prompt Cache 友好设计** | ★★★ | ★★★ | P1 |
| 5 | **9段式压缩摘要** | ★★ | ★★★★ | **P0 — 立即抄** |
| 6 | **四层权限链** | ★★★★ | ★★★ | P2 |

---

## 范式一：AutoDream 三重门

### 是什么

不是你想的"后台定时跑脚本"。Claude Code 的 autoDream 是一个**严格门控的后台子进程**，设计极其严谨。

```typescript
// 源码逻辑 (src/services/autoDream/autoDream.ts)
// 门顺序：最便宜的先
//   1. 时间门: hoursSinceLastConsolidation >= minHours (一次stat调用)
//   2. 会话门: transcriptCount > lastConsolidatedAt >= minSessions
//   3. 锁文件门: 文件级advisory lock
```

### 三个设计亮点

**① 递减成本门控**
- 时间门是一个 stat() 系统调用，几乎零成本
- 会话门是读一个计数器文件
- 锁文件门才真正 fork 子进程
- **原则**：先筛掉绝大多数"不够格"的情况，再花大成本

**② 锁文件即状态存储**
```
文件mtime = 最后一次consolidation时间
文件body  = 持有者的PID
过期时间  = 1小时（PID重用防护）
```
- 不需要单独的状态数据库
- mtime 天然是时间戳
- PID 防止误杀（1小时后锁自动过期）

**③ 手工命令 + 自动触发并存**
- 用户可手动输入 `/dream` 立即触发
- 自动触发走三重门
- **手动触发不检查门控**——用户说干就干

### 复用方案

```python
# Morning Consolidation cron job 设计草案
gate_1_time():       stat(lockfile).mtime > 24h ago
gate_2_sessions():   read(session_counter) >= 5 since last_consolidation
gate_3_lock():       try_lock(lockfile)  # mtime=now, body=PID, 1h expiry

if gate_1 and gate_2 and gate_3:
    fork_subagent(consolidation_prompt)
```

---

## 范式二：Fork Subagent 隔离

### 是什么

Claude Code 不是在一个上下文里硬塞——而是 fork 一个独立的子 Agent 跑探索性任务，结论回传、用完即毁。

```typescript
// Coordinator 只有3个工具:
// - Agent (派生子代理)
// - SendMessage
// - TaskStop

// 子Agent fork时继承父会话的 Prompt Cache
// 中间输出、错误信息全部局限在子上下文
// 完成后通过 <task-notification> 回传结论
```

### 三个设计亮点

**① Fork 继承 Prompt Cache**
- 子 Agent 起步成本极低（共享父会话的 KV 缓存）
- 不需要重新加载工具定义、系统规则

**② 隔离探索（上下文污染的解药）**
- 子 Agent 的中间输出不进主上下文
- 哪怕是探索失败、报错，都不影响主线程

**③ 结论压缩回传**
- 不是把子 Agent 对话全文传回去
- 通过 XML `<task-notification>` 传结构化结论
- 主 Agent 所见只有结论，没有推理过程

### 复用方案

Hermes 已有 `delegate_task` 工具——但与 Claude Code 的关键差距：

| 维度 | Claude Code | Hermes delegate_task |
|------|------------|---------------------|
| 缓存继承 | 继承父Prompt Cache | 无（从头开始） |
| 隔离度 | 完全隔离 | 完全隔离 ✅ |
| 结论格式 | XML结构化 | 自由文本（不够结构化） |
| 任务类型 | 6种（含dream） | 1种通用 |

**改进方向**：
1. delegate_task 增加结构化结论格式（XML/YAML）
2. 对于 memory consolidation 类任务，设计专用的 subagent 类型
3. 子 Agent 预热机制（预加载常用工具定义）

---

## 范式三：MEMORY.md 索引制（最重要）

### 是什么

不是把所有记忆塞进一个文件。核心设计：

```
~/.claude/projects/<project>/memory/
├── MEMORY.md              ← 索引文件（≤200行，每行≤150字符）
├── user_role.md           ← type: user
├── feedback_testing.md    ← type: feedback
├── project_auth_rewrite.md ← type: project
└── reference_linear.md    ← type: reference
```

**类比操作系统虚拟内存**：
- MEMORY.md = 页表（page table）
- Topic 文件 = 磁盘页面（disk pages）
- 上下文窗口 = 物理内存（physical memory）
- 按需加载 = 缺页中断（page fault）

### 四种记忆类型

| 类型 | 用途 | 示例 |
|------|------|------|
| user | 用户画像 | 编程偏好、命名习惯 |
| feedback | 纠正反馈 | "不要用var，用let/const" |
| project | 项目知识 | 架构决策、技术选型 |
| reference | 参考信息 | 依赖文档、API用法 |

### 关键约束

- **MEMORY.md 不超过 200 行**——硬性限制
- **每行不超过 150 字符**——一行就是一个指针
- **扫描上限 200 个文件**——不会扫整个目录
- **记忆是 hint，不是 fact**——System Prompt 要求 Claude 验证后再用

### 复用方案

我们当前的 wiki 体系已经类似，但缺了**索引层**：

| 维度 | Claude Code | 我们的 wiki |
|------|------------|-----------|
| 索引文件 | MEMORY.md (200行) | 无独立索引 |
| 文件组织 | 4种类型 + frontmatter | raw/research/ 按功能分 |
| 行数限制 | 硬性200行 | 无限制 |
| 加载策略 | 索引注入上下文，内容按需 | 全量或人工找 |
| 记忆地位 | "hint，不是fact" | 未声明 |

**改进方向**：
1. 为 wiki 引入索引层（类似 MEMORY.md），控制在 200 行以下
2. 每次会话自动注入索引到 context
3. 把 wiki 的 frontmatter 标准化（type, tags, status）
4. 明确"wiki 内容是 hint"——Agent 需要验证后使用

---

## 范式四：Prompt Cache 友好设计

### 是什么

Anthropic API 的 Prompt Cache 技术：如果请求的前缀与上次相同，直接复用 KV 缓存，大幅降低成本。Claude Code 整个架构围绕这个优化。

### 三个技巧

**① 静态/动态边界**
```
SYSTEM_PROMPT_DYNAMIC_BOUNDARY  # 硬编码分隔线
┌─ 静态段（全局缓存）────┐
│  身份、规则、行为准则    │ ← 几乎不变
├─ 边界 ─────────────────┤
│  动态段（会话内缓存）    │ ← 可能变化
│  MCP指令                │ ← 唯一不缓存的部分
└────────────────────────┘
```

**② 确定性排序**
- 工具描述**严格按字母表排序**
- 内置工具放前缀，MCP 工具放后缀
- 保证每次请求的 prompt 哈希一致

**③ 状态外置**
- Agent 列表从工具描述剥离，移到消息附件
- 减少约 **10.2%** 的 Cache Creation Tokens

### 复用方案

Hermes 目前没有做任何 prompt cache 优化。如果以后换到 Anthropic API，这就是巨大的成本节省。当前阶段：
- **记录在案**，等切换到 Anthropic API 时优先落地
- 当前可以用确定性排序提高缓存命中率

---

## 范式五：9段式压缩摘要

### 是什么

当对话超限时，Claude Code 触发压缩——不是简单摘要，而是**9段式结构化输出**：

```text
1. 会话目标
2. 已完成的任务
3. 未完成的任务
4. 关键决策和理由
5. 代码变更摘要
6. 发现的问题
7. 待验证的假设
8. 用户偏好
9. 上下文关键信息
```

### 复用方案

Hermes 的 session_search 已有 FTS5 检索，但没有"压缩摘要"这一层。可以：
1. 在长会话结束时自动生成 9 段式摘要
2. 摘要作为 session 的 metadata 存储
3. 后续检索时优先展示摘要而非全文

---

## 范式六：四层权限链

### 是什么

```text
Config Rules → Tool.checkPermissions → Classifier(小模型) → 用户确认
```

- **Config Rules**：用户自定义 allow/deny（.claude/settings.json）
- **Tool.checkPermissions**：每个工具自身的安全检查（BashTool 检查命令是否在白名单）
- **Classifier**：侧查询小模型（更便宜）判断操作安全性。Auto Mode 下静默调用
- **用户确认**：弹出 Allow/Deny

**关键设计**：
- 用小 AI 监管大 AI（比静态规则更灵活）
- Denial Tracking：同一个工具被频繁拒绝时自动降级
- Fail Open：分类器不确定时问用户，不直接拒绝

### 复用方案

当前 priority 不高，但有几个点可以借鉴：
1. "小模型监管大模型"的思路（用小模型做危险操作预判）
2. Denial Tracking（工具被频繁拒绝时的智能降级）
3. Fail Open 哲学

---

## 对照总表：Claude Code vs Hermes Agent

### 已对齐（自信保持）

| 范式 | Claude Code | Hermes | 差距 |
|------|------------|--------|------|
| 文件系统记忆 | Markdown 文件 | wiki/ 体系 | 小（缺索引层） |
| grep 式检索 | Grep/Glob 工具 | search_files | 小 |
| 子 Agent 隔离 | Coordinator + Fork | delegate_task | 中（缺缓存继承+结构化结论） |

### 需立即补齐（P0）

| 事项 | 价值 | 工作量 |
|------|------|--------|
| AutoDream 三重门 cron job | 自动记忆consolidation | 半天 |
| MEMORY.md 索引层 | 大幅降低每次context的噪声 | 半天 |
| 9段式压缩摘要 | 长对话可复用的结构化记忆 | 1天 |
| 锁文件设计模式 | 防重复运行+状态自存储 | 2h |

### 需中长期规划（P1-P2）

| 事项 | 价值 | 前置条件 |
|------|------|----------|
| Prompt Cache 优化 | Token 成本降低 | 切换到 Anthropic API |
| Four-layer permission | 安全性提升 | Agent 自主权扩大 |
| KAIROS 主动模式 | 从工具到同事 | 架构大版本升级 |

---

## 总结：三句话

1. **Claude Code 最强的不是算法，是工程约束**——200 行 cap、锁文件、三重门、硬性 deadline
2. **"做减法"比"做加法"更难**——MEMORY.md 不是存储工具，是**遗忘工具**
3. **没有完美的架构，只有诚实的取舍**——Claude Code 的 5 个已知瓶颈（200行cap、grep-only、无推理保留、层叠复杂度、锁定单工具）说明他们也在 trade-off

**后续行动**：
- 本报告已同步更新至 wiki
- 范式深入（7-11）详见 `comparisons/claude-code-patterns-deep.md`
- Morning Consolidation cron job 已创建（job_id: dd2bfeaf81f6，每天5:30）
