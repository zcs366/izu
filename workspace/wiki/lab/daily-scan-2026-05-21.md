# 🔭 每日前沿扫描 · 2026-05-21

> 猎手：Scout · 来源：arXiv cs.AI / cs.CL / cs.LG
> 三大支柱覆盖：✅ Agent自我迭代 · ✅ 多Agent协作 · ✅ AI×人文社科
> 关联项目：爱祝(izu) / Hermes Agent / Wiki知识系统

---

## 📊 全源扫描总览

### 支柱一：Agent自我迭代（Self-Evolution / Self-Improvement）

| # | 论文 | 核心方法 | 星级 |
|---|------|---------|------|
| 1 | **Library Drift** (arXiv:2605.19576) | 诊断自进化技能库的"库漂移"失败模式，提出outcome-driven治理方案 | ⭐⭐⭐⭐⭐ |
| 2 | **DMPO: Distribution-Matching Policy Optimization** (arXiv:2605.19461) | 用前向KL散度替代反向KL，解决GRPO的mode collapse问题 | ⭐⭐⭐⭐⭐ |
| 3 | **MOCHA: Multi-Objective Chebyshev Annealing** (arXiv:2605.19330) | Chebyshev标量化+指数退火优化Agent技能，覆盖Pareto非凸区域 | ⭐⭐⭐⭐⭐ |
| 4 | **SERL: Selective Hindsight Distillation** (arXiv:2605.19447) | 环境反馈驱动的选择性蒸馏，解决长程信用分配 | ⭐⭐⭐⭐ |
| 5 | **How Far Are We From True Auto-Research?** (arXiv:2605.19156) | ResearchArena: 117篇agent生成论文系统性评估 | ⭐⭐⭐⭐ |

### 支柱二：多Agent协作架构（Multi-Agent Orchestration）

| # | 论文 | 核心方法 | 星级 |
|---|------|---------|------|
| 1 | **Trustworthy Agent Network** (arXiv:2605.19035) | A2A网络信任架构，四大设计支柱 | ⭐⭐⭐⭐⭐ |
| 2 | **Discoverable Agent Knowledge** (arXiv:2605.19186) | Agentic KG Affordance Profile (AAP) 框架 | ⭐⭐⭐⭐⭐ |
| 3 | **Formal Skill** (arXiv:2605.19604) | 可编程运行时Skill抽象，FairyClaw实现 | ⭐⭐⭐⭐⭐ |
| 4 | **Learning to Hand Off** (arXiv:2605.19140) | IC-Q: 异步去中心化Q-learning，首个有限样本保证 | ⭐⭐⭐⭐⭐ |
| 5 | **DecisionBench** (arXiv:2605.19099) | 23,375实例的长程委托基准 | ⭐⭐⭐⭐ |
| 6 | **SIGMA** (arXiv:2605.19418) | 符号图建模Agent间冲突关系，冲突感知消息传递 | ⭐⭐⭐⭐ |

### 支柱三：AI×人文社科（AI for Social Science）

| # | 论文 | 核心方法 | 星级 |
|---|------|---------|------|
| 1 | **A-TLM: LLMs for Survey Research** (arXiv:2605.19229) | 保护动机理论约束的知识图谱，缺失数据填补新SOTA | ⭐⭐⭐⭐ |
| 2 | **DECOR** (arXiv:2605.19270) | 基于信息操纵理论的多Agent欺骗审计框架 | ⭐⭐⭐⭐ |
| 3 | **Literary Primitives via SAEs** (arXiv:2605.18808) | SAE发现LLM内部的文学原语（自我/风格/情感） | ⭐⭐⭐⭐ |
| 4 | **Progressive Autonomy as Preference Learning** (arXiv:2605.19151) | GP后验的信任校准，工具使用的渐进自治 | ⭐⭐⭐ |

---

## 🏆 今日TOP3值得深挖

### 🥇 arXiv:2605.19576 — Library Drift
> **库漂移：自进化LLM技能库的静默失败模式**

**为什么是TOP1**：直接关联izu项目！自进化技能库正是izu的核心机制之一。本文系统性地确诊了"库漂移"——技能无限累积但没有outcome-driven生命周期管理导致检索退化、误注入、性能停滞。给出了可复现触发条件、trace级诊断工具、已验证的修复方案（outcome-driven退役+bounded active-cap+元技能创作先验），把held-out pass@1从0.258提升到0.584。

### 🥈 arXiv:2605.19186 — Discoverable Agent Knowledge
> **可发现Agent知识：Agentic KG能力的正式框架**

**为什么是TOP2**：直接关联izu的KG+Agent融合路线。从语义Web服务（OWL-S/WSMO）的遗产出发，提出Agentic Affordance Profile (AAP)——在VoID和DCAT之上的语义层，让Agent在规划时就能基于形式化描述选择、组合KG，诊断失败。方法论和形式化深度都极高，直接指导izu的知识发现模块设计。

### 🥉 arXiv:2605.19035 — Trustworthy Agent Network
> **可信Agent网络：Agent网络中的信任必须内建而非外挂**

**为什么是TOP3**：A2A网络（Agent-to-Agent）正在成为下一波范式，但现有安全对齐技术无法解决异质Agent协作中的系统性漏洞（对抗组合、语义错位、级联故障）。本文提出四大设计支柱：身份与认证、行为契约、运行时监控、争议仲裁。对Hermes Agent的多Agent编排设计有直接参考价值。

---

## 📡 今日热点信号

| 信号 | 详情 |
|------|------|
| 🔥 **Self-Evolving Agents** 成为今日最大热点 | 同一日arXiv出现Library Drift、MOCHA、SERL、DMPO四篇相互呼应的Agent自我进化论文，方向感极强 |
| 🔥 **Formalization浪潮** | Discoverable Agent Knowledge、Formal Skill、Learning to Hand Off三篇不约而同走向形式化——Agent能力正在从"写prompt"走向"定义协议" |
| 🔥 **A2A网络安全** | Trustworthy Agent Network是第一批系统讨论A2A网络安全的工作，信号明确 |
| ⚡ **Mode Collapse成RL训练新焦点** | DMPO系统性地指出GRPO的mode collapse问题并提供可落地方案 |

---

## 💬 军师的话

今日arXiv cs.AI新论文中，Agent自我进化方向出现"集中爆发"——Library Drift + MOCHA + SERL + DMPO 恰好覆盖了技能管理、多目标优化、信用分配、探索-利用四个子问题。这不是巧合，说明Agent生产化已经进入"补课阶段"：先造轮子（Agent框架），再修轮子（Agent治理）。izu选择在这个时间点入局，恰逢其时。

另一信号：形式化（Formalization）正在从"学术界孤芳自赏"变成"工程界刚需"。Learning to Hand Off给出了第一个有限样本保证，Discoverable Agent Knowledge把KG选择形式化为可计算的affordance matching。Hermes Agent和izu都应该注意这一趋势——未来6-12个月，"prompt工程"将让位于"协议工程"。

> 📅 下次扫描：2026-05-22 08:00
