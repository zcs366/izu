---
title: 传统Agent框架已经被Skills取代——从代码编排到技能组合的范式革命
source: https://zhuanlan.zhihu.com/p/2039105611418308885
date: 2026-05-17
eval_level: 极大
contributors: 军师
tags: [skills-paradigm, agent-framework, openclaw, hermes, workflow-agent, paradigm-shift, skill-ecosystem]
author: Johnson7788 (知乎)
references:
  - "Anthropic: Stop building Agents, build Skills"
  - "Agent=Model+Harness (deephub)"
  - "周昌: Evolver Engineering"
  - "Agent自进化年度综述"
  - "Hermes Agent架构解析"
status: 已评估
trigger_consultation: true
---

# 传统Agent框架已被Skills取代 — 评估

## 一、核心论点

> **开发Agent不应该写代码，应该组合技能（Skills）。**

**代际划分**：
- **第一代（2023-2025）**: Workflow Agent — LangGraph、ADK、CrewAI。有状态函数编排引擎，请求-响应模式
- **第二代（2025-）**: Skills-Driven Agent — OpenClaw、Hermes。技能组合+持续运行+长期记忆+自我进化

## 二、传统框架的集体死刑

| 框架 | Stars | 致命缺陷 |
|---|---|---|
| **LangGraph** | 最高 | 检查点≠持久执行、Graph Explosion、学习曲线陡峭 |
| **Google ADK** | 新 | 持久性缺口、GCP隐性耦合、无内置限流 |
| **CrewAI** | 51.5K | 无限委派循环（最严重）、可观测性不足、单次~10分钟 |

**共同天花板**：长期记忆缺失、Agent Identity缺失、长期在线不支持、Persistent Orchestration缺失。

## 三、新范式的两强格局

### OpenClaw（37.2万⭐）

| 维度 | 数据 |
|---|---|
| 架构 | Model/Memory/Tools/Orchestrator 四层 |
| 技能市场 | **44,000+** 技能，月增18% |
| 月活 | 320万，92%留存 |
| 渠道 | WhatsApp/Discord/Telegram/Slack/Teams 等 |
| 初创公司 | 180家，月总$32万 |

**设计哲学**：配置优先、插件无关核心、本地优先、ClawHub技能市场。

### Hermes（14万⭐）

**五大支柱**：
1. **Memory** — 向量+结构键值，动态检索
2. **Skills** — **自动生成**（非人手写）：复杂任务完成、错误恢复、用户纠正、非常规解法 → 四条触发路径
3. **自我优化** — 运行时Patch + 后台审计(使用达10次触发) + GEPA离线进化(~$2-10/次)
4. **Soul** — SOUL.md防人格漂移
5. **Crons** — 自然语言调度定时任务

**与OpenClaw的本质区别**：
| | OpenClaw | Hermes |
|---|---|---|
| 技能来源 | 社区手动写 | Agent自动提炼 |
| 进化能力 | 靠社区更新 | 运行时patch+审计+GEPA |
| 类比 | npm包管理器 | 肌肉记忆 |

## 四、范式切换的三项核心驱动

文章提出的三项变革动力：

1. **Skills范式** — 任何人都可掌握，编程不再是必要条件
2. **Agent模型的RL训练** — 从代码编排到经验学习
3. **Token经济学** — 成本决定架构设计

这正好对应我们三天的积累：Skills体系(SKILL.md) + RL训练方向(MetaClaw等) + Token优化(Prompt Caching)。

## 五、对核战队的三层意义

### 第一层：方向验证（★★★★★）

> **核战队选择Skills驱动+自我进化，不是选了一个技术偏好——是站对了范式。**

文章明确宣告：Workflow Agent是上一代，Skills Agent是下一代。我们没有走错路。

### 第二层：竞争格局认知（★★★★★）

| 玩家 | 定位 | 核战队关系 |
|---|---|---|
| **OpenClaw** | 技能市场基础设施（44K技能） | 生态级对手/平台 |
| **Hermes** | 自进化Agent OS | 我们的宿主 |
| **核战队** | 核战队=Hermes之上的治理与进化引擎 | 上层差异化 |

**关键洞察**：OpenClaw有44K技能，但我们有**评估+进化+治理**——这是OpenClaw没有的。核战队不是另一个Agent框架，是**Agent框架之上的治理层**。

### 第三层：分岔路口（★★★★★）

两条路：
- **A. 融入OpenClaw生态** — 利用其44K技能市场，把核战队治理层做成OpenClaw上的元技能
- **B. 深耕Hermes+核战队** — Hermes的自动技能生成是OpenClaw没有的能力，核战队的治理+进化补上Hermes缺失的成熟度

**军师判断**：当前选B。Hermes+核战队的组合（自动生成+评估治理）比OpenClaw的生态（人手写+市场）更适合我们的定位。但需关注OpenClaw是否也在做治理层——如果也做了，竞争逻辑会变。

## 六、军师最终判断

**级别：极大。** 不是因为信息密度——是因为这篇文章宣告了一个**范式的正式完成**。

Workflow Agent时代结束了。Skills Agent时代已开始。这不是技术选型问题，是时代判断问题。

**一条建议**：把这篇文章和今天所有入库内容一起纳入核战队认知地图的**顶层**。它是坐标原点。
