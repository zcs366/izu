# Claude Code autoDream 详细基准

> 基于 v2.1.88 泄露源码分析 | 2026-05-20
> 关联视频：硅谷温差 Ep2「Agent 记忆系统 = AGI ?」(BV13WRGBoEU3)

## 源码位置

`src/services/autoDream/autoDream.ts` — 约200行 TypeScript

## 完整触发逻辑

autoDream 不是一个常驻后台进程，而是一个**惰性检查+按需fork**的模式：

```
每次对话开始 → 检查是否满足consolidation条件
  ├── 不满足 → 继续对话
  └── 满足 → fork subagent，在后台跑 /dream prompt
```

## 三重门逐级分析

### Gate 1: 时间门
- 检查项：`(now - lastConsolidatedAt) >= minHours`
- 数据源：锁文件的 mtime（正是为此设计的双用途）
- 计算成本：一次 stat 系统调用
- minHours 值：24 小时（源码硬编码，非配置项）

### Gate 2: 会话门
- 检查项：累计新会话数 >= minSessions
- 数据源：从 session store 查询 lastConsolidatedAt 之后创建的会话数
- 计算成本：一次数据库查询
- minSessions 值：5 个（源码硬编码）

### Gate 3: 锁文件门
- 检查项：能否成功获取 consolidation lock
- 实现：`src/services/autoDream/consolidationLock.ts`
- 锁文件路径：`~/.claude/consolidation.lock`
- 锁文件内容：持有者的 PID
- 过期处理：如果 PID 对应的进程已不存在，认为锁已过期
- 防 PID 重用：检查 `/proc/{pid}/cmdline` 确认是 Claude Code 进程（Linux）或同等 OS 特定检查

## /dream prompt 内容

fork 出的 subagent 收到以下指令（来自 `dreamPrompt.ts`）：

> "You are performing a dream — a reflective pass over your memory files.
> Replace vague time references with exact dates.
> Resolve contradictions (keep the current truth version).
> Delete stale entries (files that no longer exist, tasks that are complete).
> Keep MEMORY.md under 200 lines."

## 200 行上限

MEMORY.md 被设计为 index 文件，每行一条记忆指针。200 行上限意味着：
- 每个条目必须足够精炼（一行能说清楚的事，不说两行）
- 当超过 200 行时，dream 进程必须做取舍：合并或删除
- 这强制了「记忆质量 > 记忆数量」的原则

## 四个记忆文件

```
~/.claude/projects/{project_id}/memory/
├── MEMORY.md              ← 索引，最多200行
├── user_role.md           ← 用户角色信息
├── feedback_testing.md    ← 用户纠正/反馈
└── project_auth_rewrite.md ← 项目关键决策
```

## 与 izu 遗忘引擎的互补

| 场景 | Claude Code 做法 | izu 做法 | 互补价值 |
|------|-----------------|----------|---------|
| 判断记什么 | AI 自己判断，写入 MEMORY.md | 规则提取（关键词+正则） | izu 更可控，Claude Code 更灵活 |
| 何时清理 | 24h + 5 sessions 后自动 | 手动触发 | 抄自动触发模式 |
| 怎么清理 | fork subagent 跑 /dream | 遗忘引擎+回收站 | 抄后台执行模式 |
| 清理依据 | 检查文件是否存在、任务是否完成 | Ebbinghaus 曲线+冲突检测 | izu 更科学 |
| 容量控制 | 硬性 200 行 | 无硬性上限 | 抄硬上限 |
| 安全措施 | 锁文件+pid 防护 | 无 | 抄锁文件 |

## 参考源

1. Claude Code v2.1.88 泄露源码（npm source map）
2. Sabrina.dev 源码分析：https://www.sabrina.dev/p/claude-code-source-leak-analysis
3. Milvus Blog 记忆系统分析：https://milvus.io/blog/claude-code-memory-memsearch.md
4. 硅谷温差 Ep2「Agent 记忆系统 = AGI ?」：https://www.bilibili.com/video/BV13WRGBoEU3
