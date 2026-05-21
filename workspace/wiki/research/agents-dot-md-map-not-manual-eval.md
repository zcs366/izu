---
title: Harness工程原则——AGENTS.md是地图而非手册
source: https://mp.weixin.qq.com/s/thAtRIH9IhTHyQ_QKZMocw
date: 2026-05-17
eval_level: 大
contributors: 军师
tags: [harness-engineering, agents-dot-md, information-architecture, token-optimization, prompt-cache]
author: 未知（微信公众号）
references:
  - "Agent=Model+Harness (deephub)"
  - "Prompt Caching (Claude Code)"
  - "核战队SKILL.md体系"
status: 已评估
---

# AGENTS.md是地图而非手册 — 评估

## 核心论点

AGENTS.md应该是**地图而非手册**——索引+路由规则+少量全局约束。将具体规范分散到专业文档，按需读取。

## 与Prompt Caching文章的完美互补

| 原则 | 本文章 | Prompt Caching |
|---|---|---|
| 越不变越往前放 | AGENTS.md保持精简稳定 | 静态system prompt做缓存前缀 |
| 按需加载 | Read工具按需读专业文档 | defer_loading的MCP工具 |
| 分层 | AGENTS.md→MAP.md→具体规范 | 系统prompt→CLAUDE.md→会话 |

## 对核战队SKILL.md体系的启示

我们的SKILL.md整体设计已经符合"地图原则"——每个skill是自包含的，按需加载。但可以改进：

1. **检查SKILL.md是否过度臃肿** — 每个skill的SKILL.md应该像地图而非手册
2. **路由规则** — SKILL.md的triggers部分可以更场景化
3. **分层地图** — 考虑在核战队层面加一个"技能地图"（什么场景用什么技能）

## 军师判断

大。不是新发现，而是对已有实践的工程化原则提炼。建议作为核战队技能系统设计的参考准则。
