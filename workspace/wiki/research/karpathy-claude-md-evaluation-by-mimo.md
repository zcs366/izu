---
title: "Karpathy CLAUDE.md四规则评估（MiMo V2.5 Pro产出）"
aliases: ["Karpathy四条规则", "CLAUDE.md行为准则", "Think Before Coding"]
author: "MiMo V2.5 Pro (通过子代理)"
source_article: "最佳Claude Code配置：Andrej Karpathy的CLAUDE.md"
created: "2026-05-20"
updated: "2026-05-20"
tags: [Karpathy, CLAUDE.md, AGENTS.md, 行为准则, 提示词工程]
sources:
  - https://mp.weixin.qq.com/s/q7nuyMeB7AzECSQ11FfaTA
---

# Karpathy CLAUDE.md 四规则深度评估

> 由 MiMo V2.5 Pro 评估产出 | 2026-05-20

---

**一句话核心判断**：134k Star = 30k（规则本身价值）+ 104k（Karpathy品牌+反差叙事）。规则本质是工程常识的精确编码，但**把工程智慧编码为AI可执行的系统指令**是范式级创新。

---

## 一、逐条规则评估

### 规则1：Think Before Coding（先想清楚再动手）

痛点命中率极高——AI编程最常见的失败模式就是"自信猜测"。但有个问题没解决：**Confidence Threshold在哪**？如果模型对所有不确定都"停下来问"，会进入无穷Q&A循环，用户体验比猜错了更差。

### 规则2：Simplicity First（能简单别复杂）

与LLM训练分布有**根本矛盾**——AI的训练数据中，复杂代码="更专业"的信号。你要让AI写简单代码，是在对抗它的训练本能。这条规则需要很强的模型遵从能力才能生效。

### 规则3：Surgical Changes（只动该动的地方）

"每行改动都能追溯回用户请求"——小项目合理，复杂系统中会因联级效应难以严格执行。但作为理想标准是对的。

### 规则4：Goal-Driven（目标可验证）

**四条中实践价值最高**。具体模板（[Step]→verify:[check]）提供了内建反馈循环，是唯一一条可以直接在prompt工程中量化的规则。

---

## 二、与izu体系的关系

MiMo还读了我们的AGENTS.md和SOUL.md，发现：

| 维度 | 我们有的 | Karpathy的 | 缺口 |
|------|---------|-----------|------|
| 身份定义 | SOUL.md（军师祭酒） | — | 互补 |
| 项目规范 | AGENTS.md | CLAUDE.md | 同质 |
| 行为准则 | — | 四条规则 | ❌ 缺决策框架 |
| 反模式 | — | 文章提到但未展开 | ❌ 缺ANTI-PATTERNS.md |

AGENTS.md指导"怎么做"（技术规范、文件结构），Karpathy的规则指导"怎么想"（决策框架、对抗LLM本能）。**我们缺一层行为准则层的指令。**

---

## 三、可操作建议

1. **在AGENTS.md或SOUL.md中注入Karpathy四条规则**——直接加在behavioral guidelines段
2. **配一个ANTI-PATTERNS.md**——Karpathy规则的反面案例，让AI知道"不要怎么做"
3. **在izu coordinator的system prompt层注入决策原则**

---

*评估时间：2026-05-20*
