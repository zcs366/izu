---
source_url: https://mp.weixin.qq.com/s/Qi68ptxQRyiA932JU49SYQ
sha256: 3fc211165156a3a3e3bdf78b4be67d70f9a9b5702b5e69f61011abd0b0177a81
ingested: 2026-05-19
title: 深入源码：Hermes Agent 如何实现 "Self-Improving"
author: 阿里云开发者
source: 微信公众号
content_type: technical_deepdive
eval_level: 极大
tags: [Hermes Agent, Self-Improving, Memory, Skill, Nudge Engine]
---

# Hermes Agent 的 Self-Improving：深入源码解析

> 来源：微信公众号「阿里云开发者」
> 核心：Hermes Agent 通过 Memory、Skill、Nudge Engine 三子系统实现"越用越强"的自我进化闭环。

## 1. 背景：Agent 的"学习"方式分野
- OpenClaw：Skill 是手写 Markdown 文件，Agent 不会自动增长知识。
- Hermes Agent（GitHub 106k+ Star）：Agent 完成工作后自动将踩坑经验提炼为可复用 Skill。

## 2. 总览：三个子系统，一个闭环
| 子系统 | 类比 | 作用 |
|--------|------|------|
| Memory | 助理的小本子 | 记事实（环境、用户偏好） |
| Skill | 操作手册 | 记过程（怎么做某事） |
| Nudge Engine | 定时闹钟 | 提醒 Agent 回顾与提炼 |

## 3. Memory：越用越懂你
文件结构：~/.hermes/memories/MEMORY.md (2200 chars) + USER.md (1375 chars)
- 容量有限强制信息压缩，淘汰过时内容
- 冻结快照机制：会话内注入的快照冻结，不变动 → 共享前缀缓存，节省 API 计费
- 声明式事实 vs 命令式指令

## 4. Skill：把做过的事变成会做的事
- Skill 目录结构：~/.hermes/skills/{category}/{skill-name}/SKILL.md
- 典型 SKILL.md：YAML frontmatter + Markdown 步骤 + Pitfalls 部分
- 何时创建：工具调用 > 5次、踩过坑、用户纠正过
- Self-Improving 体现：Pitfalls 是踩坑后 Agent 追加的
- Skill 的自我修补：局部 patch（fuzzy_find_and_replace），非全量重写

