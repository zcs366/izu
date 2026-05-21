---
source_url: https://mp.weixin.qq.com/s/dDkVA9mfNbJWTwkVKN1AOQ
ingested: 2026-05-19
sha256: placeholder
title: 让Skill自己训练自己：8阶段Loop、3层评测、5维AND门控，从此实现自进化
author: 张思宇
source: 腾讯云开发者
note: curl_cffi完整抓取，11428字。Skill Evolver系统——Skill自训练/自迭代/自评测/自回归。
---

# 让Skill自己训练自己

> 作者：张思宇
> 来源：腾讯云开发者公众号
> 相关：Meta-Harness (arXiv:2603.28052) + skill-creator (Anthropic)

## 核心思想

Skill可以像神经元参数一样被训练——授它以渔，给他一本书、一个目标，让他自己实践、碰壁、改错。

## 系统架构：8阶段Loop

(详见完整评估)

## 关键组件

- **3层评测**：quick_validate + grader + comparator
- **5维AND门控**：分层mutation的质量控制
- **Meta-Harness trace 架构**
- **Workspace git 隔离**
- **meta-evolution 自证**：19轮自进化验证

## 依赖

- Meta-Harness (arXiv:2603.28052) — 原始trace喂proposer (+44%)
- skill-creator (Anthropic) — 硬依赖，quick_validate + grader + comparator + GT生成

## 增量贡献

5维AND门控 + 分层mutation + Meta-Harness trace架构 + workspace git隔离 + meta-evolution自证

## 结论

"它不完美，但我还是试着相信它"——适用边界明确，如果想试，作者给出了起点。
