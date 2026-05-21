---
title: Lessons from Building Claude Code: Prompt Caching is Everything
source: https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything
date: 2026-05-17
eval_level: 极大
contributors: 军师
tags: [prompt-caching, claude-code, architecture, cost-optimization, thariq-shihipar, agent-design, constraint-driven]
references:
  - Chinese summary: https://mp.weixin.qq.com/s/2Qs5gRlhe7qSVYCd9r8t1g
  - Thariq Shihipar: "The Unreasonable Effectiveness of HTML" (same author, companion insight)
  - Karpathy: "Structure response as HTML" (same week trend)
status: 已评估
trigger_consultation: true
---

# 构建Claude Code的教训：Prompt Caching是一切

## 一、核心论点

> **Prompt Caching不是优化手段，而是架构约束。**

Anthropic将Cache命中率作为**基础设施级指标监控**，地位等同服务器uptime。命中率下降触发oncall告警，须像处理线上事故一样排查。

一句话总结7条经验：

> **Prompt Caching是前缀匹配，所有设计围绕这一约束展开。**

## 二、七条经验逐条拆解

### 1. 排好队形（内容顺序）

缓存依赖前缀匹配，**内容排列顺序至关重要**。

```
1. 静态system prompt + 工具定义（全局缓存，所有session共享）
2. CLAUDE.md（项目级缓存，同一项目内共享）
3. Session上下文（会话级缓存）
4. 对话消息（逐轮增长）
```

**原则**：越不容易变的东西，越往前放。

**常见陷阱**：
- ❌ 静态prompt嵌入时间戳 → 每秒变，缓存废掉
- ❌ 工具定义排序不确定（dict/set） → 前缀对不上
- ❌ 工具参数字段更新 → 整条缓存链断裂

### 2. 别动Prompt

处理过时信息时：
> **别去改prompt，把更新塞进下一轮的消息里。**

用`<system-reminder>`标签，将更新放入user message或tool result。**System prompt保持"不可变的基础设施"，消息是"流动的信息层"**。

### 3. 别换模型

缓存与模型绑定。**切换模型使所有缓存作废，从头重建。**

> 100K token的Opus对话，切到Haiku的成本高于直接用Opus回答，因为要重建缓存。

**正确做法**：用子Agent。子Agent有独立上下文和缓存，不污染主对话缓存链。

### 4. 别碰工具

**session期间工具集不动**。加一个、减一个 → 缓存断裂。

**Plan Mode设计模式**：
- ❌ 离开Plan Mode移除/加回执行工具 → 破坏缓存
- ✅ **保留所有工具，增加两个特殊工具**：`EnterPlanMode`和`ExitPlanMode`
- 模型在system message中知道"规划模式不能执行操作"

**额外收益**：模型可自主判断何时进入Plan Mode。

### 5. 延迟加载

大量MCP工具的平衡方案：
- 初始仅放轻量stub，标记`defer_loading: true`
- 模型仅看到工具名和一句话描述
- 需要时通过Tool Search拉取完整schema

> 像图书馆目录：先翻索引，找到书再去书架取。

### 6. Cache-Safe Forking（压缩）

长对话填满context window时，需压缩摘要。

**常见错误**：另起API调用做压缩，用不同system prompt → 缓存完全对不上。

**正确方案**：压缩请求使用与主对话**完全相同**的system prompt + 工具定义。将主对话消息作为历史带上，末尾追加压缩指令。

> 从API视角，这个请求与主对话的上一个请求几乎一模一样 → 缓存前缀被复用。

Anthropic已将Compaction功能**内置到API**中。

### 7. 缓存命中率当uptime监控

小失误就可以引起大规模缓存失效。

## 三、对izu/ITA的直接启示（★★★★★ 极高）

### 启示1：ITA的压缩方案应走Cache-Safe Forking路线

ITA的核心是把代码压缩为LLM可读的compact encoding。这篇文章告诉我们三件事：

| ITA现有设计 | Prompt Caching约束 | 是否对齐 |
|---|---|---|
| 代码压缩为compact encoding | 压缩要用Cache-Safe Forking | ✅ 方向一致 |
| 三语交互（自然语言↔代码↔AI内部编码） | 保持前缀稳定勿轻易切换模型/工具 | ⚠️ 需检查 |
| M1编码器v0.1 | 从第一天就设计缓存友好 | 🔴 需检查设计 |

**建议**：ITA的compact encoding格式应考虑prompt caching的前缀匹配约束。不要设计成"每次编码结果不同"的结构——缓存前缀必须稳定。

### 启示2：核战队子Agent模式已对齐Claude Code设计

我们已经在用子Agent做五人合议、izu-pipeline等。Claude Code团队告诉我们：这就是正确的做法。

**但需要注意**：
- 每个子Agent的system prompt + 工具集必须稳定（不要每次调用动态生成）
- 子Agent设计时就要考虑缓存复用（同一个Agent反复调用vs一次性调用差别巨大）

### 启示3：我们的SKILL.md = CLAUDE.md

Claude Code用CLAUDE.md做项目级缓存共享。我们的SKILL.md机制完全对应——项目级静态上下文。

**可以改进**：
- 每个skill加一个`cache_priority`字段，标注哪些部分最不应该变
- 频繁变动的部分（动态数据、时间戳）放到消息层而非skill定义层

### 启示4：ITAPrompt Caching抑制Token成本

你极度在意模型成本。这篇文章告诉你——**Prompt Caching是控制成本的第一杠杆**，不是模型选择、不是量化、不是API价格对比。

**成本等式重写**：
```
实际成本 = API价格 × (1 - 缓存命中率)
```

缓存命中率90% → 实际成本10%。缓存命中率降到60% → 实际成本涨到40%。

**4倍差距**。比任何模型价格差异都大。

## 四、检查清单（第二天可执行）

### 针对our setup的检查项

| 检查项 | 当前状态 | 建议变更 |
|---|---|---|
| 子Agent system prompt是否稳定 | ✅ 基本稳定 | 检查有无动态插入时间戳 |
| 工具定义排序是否确定 | ⚠️ 未检查 | 用有序dict固定工具顺序 |
| 是否同一session内切换模型 | ❌ 目前不换 | 保留现有模式 |
| 文件变更是否通过消息更新而非改prompt | ⚠️ 需确认 | 确认cron job的上下文更新方式 |
| 缓存命中率是否监控 | ❌ 未监控 | 考虑接入prompt caching metrics |

### 针对ITA的检查项

| 检查项 | 建议 |
|---|---|
| Compact encoding格式设计 | 考虑prompt cache前缀匹配，避免每次编码结果不同 |
| M1编码器v0.1 | 架构中加入cache-aware设计 |
| RTCE+2Steering | 确认steering切换时是否破坏缓存 |
| 编码器v1.0 | 设计文档加入prompt caching章节 |

## 五、军师判断

**级别：极大。** 这不是一篇"有趣的文章"——这是**架构层面的约束原理**。

原因：
1. **直接决定ITA方向**：ITA的compact encoding必须考虑prompt caching兼容性，否则上线后成本爆炸
2. **重塑成本模型**：缓存命中率是成本的第一杠杆，比模型选择更重要
3. **验证我们已有做法**：子Agent模式、SKILL.md体系→Claude Code已验证这是正确路径
4. **可立即执行**：检查清单里的项目，很多是改一行配置、加一个注释的事

### 合议建议

建议启动**五人合议**（极大级标准流程）：
- **子产**：断这个话题是否值得投入深度设计
- **韩信**：画ITA缓存架构的终局图
- **鲁班**：审现有子Agent和skill体系的缓存兼容性
- **萧何**：算如果不改，成本会多出多少
- **子贡**：调调度，确定优先级

但你刚才说"开干"——那就先执行检查清单里的可立即行动项，同时启动合议。
