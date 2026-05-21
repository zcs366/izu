---
source_url: https://mp.weixin.qq.com/s/BB5t7GfjBA--Ef22tjjvbQ
ingested: 2026-05-07
sha256: d90c80e2173d7ab30516900fa14021092420999353d676d0110aaae60dbd7ab6
source: 微信公众号
author: (转载 Tony Simons 观点)
original_pub: x.com/@tonysimons_
---

# Hermes Agent 的 SOUL.md：一份让 AI 从"回答问题"变成"一起做事"的文件

本文转述独立开发者 Tony Simons 关于 Hermes Agent 核心身份文件 SOUL.md 的实践思考。原文发布于 X (Twitter)：https://x.com/tonysimons_/status/2051473178682118241

## 核心问题

很多人讲 AI Agent，开口就是模型、工具、MCP、记忆、workflow。但真用起来，AI "很会回答，但不太像一个能一起做事的人"。大多数 AI 变成"礼貌、顺从、没有风险、没有判断"的回复机器。

**Tony 的判断**："这不是有用，这是昂贵的认同。"

## 解决方案：SOUL.md

Tony 的答案不是秘密模型，也不是魔法框架，而是一份 **170 行的 Markdown 文件**——SOUL.md。Hermes 官方文档定义：SOUL.md 是 Hermes 实例的核心身份文件，适合放语气、个性、沟通方式、直接程度、分歧处理和模糊问题的默认处理方式。

### SOUL.md 七大核心模块

#### 1. 身份定义
> "You are Hermes, Tony's autonomous operator and thought partner."

开篇定义角色——不是客服、不是情绪陪伴、不是秘书，而是 **参与工作的人**。

#### 2. 反驳规则（Pushback）
> "Push back aggressively when it makes sense. Disagree openly and directly, but earn the right to push back. Every objection comes with evidence."

必须反驳，但不能为了反驳而反驳。每一次反对都要带证据：数据、例子、推理、证明。真正有用的反驳，是指出：
- 这个想法解决的问题不清楚
- 这个产品没人会在真实场景里使用
- 这个任务和当前目标没关系
- 这个计划太大，执行阻力太高

#### 3. 责任闭环
> "If Tony isn't acting on what you surface, the feedback loop is broken."

如果输出没有被行动接住：要么提醒人，要么改进输出。建立了"输出→行动"的闭环机制，防止 AI 产出变成"内容垃圾场"。

#### 4. 场景化语气（Tone）
- **私下**："Casual, authoritative, and unfiltered. Cuss like a motherfucking sailor — it's just us."
- **公开**："No em dashes. Profanity: tasteful, not G-rated, not hardcore. Write like someone who builds things, not someone who writes about building things."

同一个 AI 在不同场景使用不同声音——内部讨论是思考现场，公开发布是交付物。

#### 5. 任务地图（Task Map）
维护当前目标、优先级、活跃项目、停滞项目的状态。Hermes 不需要每次都问"我们现在在做什么"。
- 哪个新想法支持当前变现目标？
- 哪个项目被忽略太久？
- 哪个旧项目应该停掉？

#### 6. 授权边界（Authorization）
> "Never without explicit approval: posting, publishing, purchasing, or making destructive changes. Everything else: if confident and grounded in facts, move."

红线极简单：发布、购买、不可逆破坏性修改必须批准。其他事直接行动。

#### 7. 主动性（Proactive）
> "You don't wait for orders. You surface opportunities, flag problems, and push work forward on your own."

## 实践建议：写自己的 SOUL.md

按六块起步：
1. **身份**：到底是什么角色？
2. **语气**：私下和公开分别怎么写？
3. **反驳规则**：什么时候必须提醒？反驳带证据？
4. **授权边界**：哪些能直接做，哪些必须问？
5. **任务地图**：最重要的是什么，哪些在做，哪些该停？
6. **责任闭环**：用户忽略输出时怎么办？

## 原文链接
https://x.com/tonysimons_/status/2051473178682118241
