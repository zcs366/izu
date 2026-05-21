---
source: raw/articles/hermes-agent-devils-in-details.md
created: 2026-05-13
tags: [hermes, prompt-engineering, system-prompt, skill-authoring]
---

# Hermes Prompt 工程五原则

源自 Radon & Mimo 对 Hermes Agent 系统提示词的深度分析，提炼出五条可复用的提示词编写原则。

## 一、否定优先于肯定

当需要改变行为时，用 **Never/Do NOT/NEVER** 而非 **Please/You should**。

LLM 对否定指令的 token 概率影响比肯定指令更大——"Never" 直接抑制相关 token 的生成概率，而 "Please" 只是给正确 token 加一点权重。

**示例：**
- ❌ `Please try to use tools rather than describing plans`
- ✅ `Never end your turn with a promise — execute it now`

## 二、机器词汇优先于人类词汇

用 **tool call** 代替 action，用 **turn** 代替 response，用 **inject** 代替 add。

机器词汇在 LLM 的训练数据中更频繁地出现在"正确执行"的语境里，能引导模型生成更精确的行为，同时减少 LLM 的拟人化倾向。

**示例：**
- `mental computation` 代替 `thinking` / `reasoning`
- `liabilities` 代替 `outdated` / `bad`

## 三、先禁后放（三明治结构）

先给禁令 → 具体场景 → 合法出路。禁止建立边界，场景锚定理解，出路防止 agent 陷入瘫痪。

```
You MUST use your tools to take action.
do not describe what you would do.
Never end your turn with a promise.
↓
Every response should either (a) contain tool calls that make progress,
 or (b) deliver a final result to the user.
```

## 四、三层冗余

每条指令至少包含：**任务类别 + 工具名 + 示例**。三层信息冗余确保即使 LLM 注意力分散，也能从任一层恢复正确理解。

**示例：** `"Arithmetic, math, calculations → use terminal → sha256sum, base64"` 比 `"use tools for calculations"` 有效十倍。

## 五、把失败具象化

把抽象的"做得不好"转化为具体的、可感知的失败场景。

- ❌ `save important things`
- ✅ `The most valuable memory is one that prevents the user from having to correct or remind you again`

## 上下文压缩的处理要点

当对话压缩时，用以下结构确保 agent 不把旧摘要当新指令：

- `REFERENCE ONLY` — 大写标记
- `handoff from a previous context window` — 交接术语
- `NOT as active instructions` — active 是关键区分词
- `they were already addressed` — 消除补全欲
- 明确指向最新用户消息

## 关联

- [[hermes-agent]] — 自主 AI 代理
- [[hermes-agent-memory-system]] — 多层记忆系统
