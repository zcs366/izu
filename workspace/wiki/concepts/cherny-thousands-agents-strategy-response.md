---
title: Cherny"数千Agent"模式——izu战略回应（五人合议）
type: evaluation
evaluated: 2026-05-15
verdict: 窄做Loop合约，不追求并发规模
priority: high
related: [izu, cronjob, loop-contract, agent-safety-net, five-agent-consultation]
---

# Cherny"数千Agent"模式——izu战略评估

## 背景

2026年5月4日，Anthropic Claude Code缔造者Boris Cherny在红杉资本AI Ascent访谈中自述：每晚用手机管理5-10个会话，每个会话里跑多个Agent，总计每晚运行"数千个AI Agent"替他写代码。核心技术：`/loops`（cron本地触发循环指令）和`Routines`（服务器端周期任务）。

## 核实

| 文章声称 | 核实结果 | 证据 |
|---------|---------|------|
| Cherny"每晚数千Agent" | ✅ 属实 | Business Insider 2026.5.13报道、Sequoia YouTube视频 SlGRN8jh2RI、Cherny X帖子(2026.1.2, 810万浏览) |
| `/loops` 和 `Routines` 是核心功能 | ✅ 属实 | Cherny第二次X分享(2026.5)专门介绍了这两个功能 |
| 独立开发者3天交付小程序 | ⚠️ 文章作者自述案例，无法独立核实 | 逻辑上合理但无法验证 |

## 五人合议结论

### 子产判断：窄做
- 张成市在L1（6-20个cron agent），Cherny在L5（1000-5000+全天候）
- 不该全量铺开"数千并发Agent"，但该做Loop合约体验升级
- 关键差距不在"能不能做"，在"好不好用"——Hermes cronjob功能等效但创建体验差

### 韩信终局：2026年8月体验
- Loop Contract DSL + 安全网 → /loops Telegram管理 → Dashboard可视化
- 三句话定调：不是cron的UI升级，是Agent从"玩具"到"员工"的授权契约

### 鲁班审计：砍至骨头
- 从韩信28-44天压缩到7.5-12天
- P0只做三件事：安全网(max_attempts+auto-pause+通知) + 语法糖(/loops命令) + stop_condition评估
- 砍掉：费用核算、预算控制、自然语言创建、模板、Dashboard、可视化、归档

### 萧何路径：12天/¥0边际成本
- 4阶段、9h工时 → 12天含缓冲（张成市日均1h）
- 边际成本：¥0-10/年（安全网零API调用，诊断每日<¥0.01）
- 关键路径：安全网→语法糖→评估，纯串行

### 子贡调度：子Agent自动执行
- 3个编码子Agent + 1个写作Agent，张成市只验收
- 变通预案覆盖0小时到7天失联
- 包装三层：自用→元宝群→公众号

## 军师终裁

✅ **签核。窄做Loop合约。即刻开工。**

核心原因：
1. Hermes已有基础设施（cronjob/delegate_task/context_from/gateway），差距只在合约层
2. 边际成本趋近于零——不是"要不要做"的选择，是做起来几乎不要钱
3. Cherny的核心洞见不是"数千Agent"，是"敢让Agent在睡觉时替你工作"——我们已经在做了，只是少了护栏
4. 安全网一旦就位，现有的35个cron job自动受益，无需逐个改造

## 已产出

- 韩信终局画像：`output/doc/hanxin-loop-contract-endgame-2026Q3.md`
- 本文为五人合议完整记录
