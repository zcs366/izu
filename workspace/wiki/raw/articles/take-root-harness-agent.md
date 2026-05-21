---
title: "take-root：6 Persona Harness Agent"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/3IjrEl82AAJZ_vbZW-ke9w"
author: "高可用架构"
date: 2026-05-19
ingested: 2026-05-19
sha256: ecdc21440e454a93bfcbc47a62bcd9c0d86c65243366cabe1e3ca7536b89c00e
type: article
tags: [take-root, harness-agent, multi-persona, code-review, convergence]
eval_level: 极大
---

# take-root：6 Persona Harness Agent

**GitHub**: https://github.com/gokeshenzhen/take-root

## 核心问题
项目越大Agent越乱——修好A悄悄坏掉B。根因不是模型智能不足，而是缺乏工程纪律：评审机制、收敛指标、角色边界。

## 6个Persona
| Persona | 角色 | Provider | 方式 |
|---------|------|----------|------|
| Jeff | 架构师，出方案 | Claude official | 交互式 |
| Robin | 独立评审+定稿 | Claude official | review-only |
| Neo | 对抗性评审（攻击者） | Kimi | review-only |
| Lucy | 实现者，编码 | Codex | 非交互 |
| Peter | 代码评审 | Qwen | 非交互 |
| Amy | 全量测试 | Codex | 非交互 |

**原则**：评审与实现使用不同厂商模型，消除单模型路径依赖。

## Plan阶段：对抗中收敛
```
Jeff提案 → Robin R1 + Neo R1
    → Robin R2 ↔ Neo R2（看过对方后重新评审）
    → 最多5轮 → 双方frontmatter status均为converged→提前结束
    → Robin finalize → final_plan.md
```
- Neo的硬规则：若说"看起来不错"，即失职
- 收敛判定：检查artifact中的status字段

## 权限隔离：三层
1. **工具权限**：review-only persona物理上无法修改代码
2. **上下文扫描**：检测指令覆盖、凭证窃取、权限升级
3. **工作区快照+自动回滚**：SHA256 + mtime_ns快照，越权自动回滚

## Code阶段
Lucy读final_plan.md → 非交互编码 → Peter代码评审
三种结局：converged / exhausted_stop / exhausted_advance

## Test阶段
Amy按验收标准全量测试 → 结构化状态 all_pass

## 设计哲学
> 真正缺的不是智力，是纪律。评审、对抗、收敛指标、角色边界——这些东西不会随着模型变聪明而自动出现，它们需要被设计进工作流里。
