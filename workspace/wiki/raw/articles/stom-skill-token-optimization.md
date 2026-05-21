---
source_url: https://mp.weixin.qq.com/s/iR_HZbs3FMJVB6cqOoS1xw
ingested: 2026-05-19
sha256: pending
title: STOM：让 Skill 消耗的每个 token 都有意义
author: 难得金圣叹
source: github.com/zhuang-HE/stom-methodology
---

# STOM 核心笔记

## 三层信息架构

L1 执行层 — SKILL.md ≤350行（80%任务）
L2 参考层 — references/（按需加载）
L3 外部层 — 实时搜索（API文档等）

## 三纯净原则

1. 无平台语法污染
2. 工具用能力描述
3. 路径不写死

## CI门禁（11项，P0/P1/P2/P3分级）

P0：语法污染/工具名未声明/绝对路径/缺元数据 → 阻断发布

## 六维度健康评分

CI通过(25%) + 触发词覆盖(20%) + Token效率(15%) + 版本同步(15%) + 活跃度(15%) + 踩坑经验(10%)

## 自进化

触发词自进化 + 踩坑经验积累 + CI闭环

## 改造数据

1,269行/34.4KB → 439行/15.0KB（56%节省，~20K tokens/次加载）
