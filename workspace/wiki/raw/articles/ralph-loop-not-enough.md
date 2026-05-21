---
title: "Ralph Loop 不够用：长时间 Agent 还缺这 3 件事"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/2ql-DDr2d4bemwq3dr0ElA"
author: "Jarrod Watts (Monad 首席AI工程师) / 高可用架构"
date: 2026-05-19
ingested: 2026-05-19
sha256: 4d0bcf9ef823441d130bf7cacb42b7b349a6b7dcaaa237a2bcea927398f6228b
type: article
tags: [long-running-agent, multi-agent, orchestrator, persistent-memory]
eval_level: 极大
---

# Ralph Loop 不够用

## 核心观点
长时间运行的agent有效是因为花了更多token（测试时计算扩展）。但在任务上下文超出上下文窗口容量时，简单循环策略失效。

## 3件缺失的事

### 1. 模糊性会复利增长
每一轮输出变成下一轮输入，错误决策在后续迭代中指数放大。
**解决**：前期使用 `/interview` 或 "grill-me" 技能。
- plan mode创建计划 → /interview命令 → Claude提出20-50个澄清问题 → 更新计划文件
- **核心洞察**：前期多投入时间，剪掉偏离目标的决策分支。

### 2. 多agent优势
orchestrator ↔ subagent 优于单一agent。
**引用Anthropic研究**（第39页）：多agent协作消耗更多token但显著改善结果。
**架构**：
```
主 orchestrator ⟶ subagent 小队
                    ├── 实现者
                    └── 评审者
```
**Boris（Claude Code创建者）**：独立上下文窗口的subagent有效，解释了为什么一个agent引入bug而另一个不会。

### 3. 跨上下文记忆
持久化文件：
| 文件 | 用途 |
|------|------|
| GOAL.md | 顶层目标 |
| STANDARDS.md | 代码质量标准 |
| IMPLEMENT.md | 工作流说明 |
| PROGRESS.md | 进展日志 |

**原则**：新agent必须阅读所有文件，以一致的方式行动。

## 优化工作流
```
设置阶段（interview） → 拆解为里程碑 → 主 orchestrator
    ↓
    ├── subagent 小队（实现者+评审者）
    ├── 持久化记忆文件
    └── git worktrees 并行化工作
```

**关键数据**：Sonnet 4.6在BrowseComp上多花10倍token，分数提高约10个百分点。

**GitHub**: https://github.com/jarrodwatts/long-running-agent-skill
