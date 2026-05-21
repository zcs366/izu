# 🔭 前沿实验室·每日论文扫描

**日期**: 2026-05-18（周一） · **扫描时段**: 00:00–09:00 UTC
**扫描范围**: arXiv / HuggingFace Daily Papers / Hacker News / Semantic Scholar / Reddit
**研究方向**: 三大支柱（Agent自我迭代 / 多Agent协作架构 / AI×人文社科）

---

## 一、今日值得关注论文

### 支柱1：Agent自我迭代（Self-Evolution / Metacognition）

| # | 标题 | 来源 | 核心方法 | 热度 | 星级 |
|---|------|------|---------|------|------|
| 1 | **MARS: Metacognitive Agent Reflective Self-improvement** (2601.11974) | arXiv Jan 2026 | 单周期自进化框架，模拟人类元认知：**原则反思**（抽象规则防错）+ **程序反思**（推导步骤策略），无需持续在线反馈 | — | ⭐⭐⭐⭐⭐ |
| 2 | **SDAR: Self-Distilled Agentic Reinforcement Learning** (2605.15155) | HF #2 今日（84票） | Sigmoid门控自蒸馏：RL主优化 + OPSD门控辅助损失，选择性强化正信号、弱化负信号 | ❤️84 · GitHub⭐73 | ⭐⭐⭐⭐⭐ |
| 3 | **EvolveMem: Self-Evolving Memory Architecture** (2605.13941) | HF 15日（21票） | **两级协同进化**：存储内容 + 检索机制同步调优，LLM诊断模块+带安全阀的元分析器，自动回滚/探索 | ❤️21 · GitHub开源 | ⭐⭐⭐⭐ |
| 4 | **LLMs Know When They Know, but Do Not Act on It** (2605.14186) | arXiv 13 May | 元认知控制具身化：监测(FOK/JOL信号)→控制(信任/重试/聚合)，+8.6精度点，无需参数更新 | — | ⭐⭐⭐⭐ |
| 5 | **Metis: Self-Evolving Metacognitive Policy Optimization** (2605.10067) | ICML 2026 | 红队攻防元认知策略：POMDP形式化攻防→因果诊断防御逻辑，ASR 89.2%，成本降低8.2× | — | ⭐⭐⭐ |
| 6 | **Beyond Individual Intelligence: Survey on MAS Self-Evolution** (2605.14892) | HF 15日（44票） | **LIFE框架**：能力奠基→协作集成→故障归因→自主进化，四阶段因果链接 | ❤️44 · GitHub开源 | ⭐⭐⭐⭐ |
| 7 | **STALE: Can Agents Know When Memories Are No Longer Valid?** (2605.06527) | HF 15日（39票） | 隐式冲突检测基准：400场景×3维度，最佳模型仅55.2%，提出CUPMem写时修正原型 | ❤️39 | ⭐⭐⭐ |

### 支柱2：多Agent协作架构

| # | 标题 | 来源 | 核心方法 | 热度 | 星级 |
|---|------|------|---------|------|------|
| 8 | **MPAC: Multi-Principal Agent Coordination Protocol** (2604.09744) | arXiv Apr 2026 | **多主体协调协议**：五层架构（会话/意图/操作/冲突/治理），冲突为一等对象，95%协调开销降低，4.8×加速 | 开源双语言实现 | ⭐⭐⭐⭐⭐ |
| 9 | **Orchard: Open-Source Agentic Modeling Framework** (2605.15040) | HF 15日（14票）·Microsoft | 统一环境层+三种Agent配方：SWE 67.5% SOTA、GUI 74.1%、个人助手 73.9%，数据效率极高 | ❤️14 · GitHub⭐31 | ⭐⭐⭐⭐ |
| 10 | **Multi-Agent Orchestration Survey (MCP+A2A)** (2601.13671) | arXiv Jan 2026 | 统一架构框架：规划/策略/状态/质量四层，MCP+A2A协议互补 | — | ⭐⭐⭐ |
| 11 | **ACP: Unified Agent Communication Protocol** (2602.15055) | arXiv Feb 2026 | 联邦编排模型：去中心化身份验证+语义意图映射+自动化SLA，零信任安全 | — | ⭐⭐⭐ |

### 支柱3：AI×人文社科

| # | 标题 | 来源 | 核心方法 | 热度 | 星级 |
|---|------|------|---------|------|------|
| 12 | **AI Can Persuade People to Take Political Actions** (2604.09200) | arXiv Apr 2026 | 大规模实验(N=17,950)：AI说服力+19.7pp签名率，态度≠行为，信息提供不能解释行为变化 | — | ⭐⭐⭐⭐ |

---

## 二、🚀 值得深挖TOP3（实战参考价值排序）

| 排名 | 论文 | 理由 | 关联项目 |
|------|------|------|---------|
| **🥇** | **MARS** (2601.11974) | 单周期元认知自进化，直接对标izu Agent的自我迭代能力升级，实现成本低，架构清晰 | 爱祝·Agent能力升级 |
| **🥈** | **MPAC** (2604.09744) | 多主体协调协议填补A2A空白，冲突即对象的设计对Hermes Agent的工具协调层有直接启发 | Hermes Agent·工具编排 |
| **🥉** | **SDAR** (2605.15155) | 高频社区验证(84票)，RL+自蒸馏门控，对izu的训练管线优化有实用参考 | 爱祝·训练管线 |

---

## 三、📡 今日热点信号

> **"An AI Hate Wave Is Here"** —— HN #1 今日（53 points, 43 comments）
>
> Axios报告显示AI反感情绪正在升温，公众对AI的信任度出现显著下滑。这是2026年第一次出现"AI仇恨浪潮"成为HN头条，值得关注社会情绪拐点。
>
> 另外，**Self-Evolving AI Agents** 话题在Medium/InfoSec连续发酵（5月14日文章爆火），"agent写自己协议"成为新 meme。

---

## 四、关联项目匹配

| 项目 | 匹配论文 | 具体对接点 |
|------|---------|-----------|
| **爱祝 (izu)** | MARS, SDAR, EvolveMem, Beyond Individual Intelligence | Agent自我迭代管线设计、元认知反思机制、记忆体系进化 |
| **Hermes Agent** | MPAC, Orchard, Multi-Agent Survey | 工具编排层协议、多Agent协调、冲突处理 |
| **Wiki知识系统** | EvolveMem, STALE | 记忆写时修正、传播感知搜索 |
| **论文skill/转录** | — | 可尝试Metacognitive Harness提升翻译质量 |
| **日常管理** | AI Persuasion | 了解AI对社会行为的影响趋势 |

---

> *扫描完成于 2026-05-18 09:01 UTC · 共扫描 12+ 篇论文 / 5+ 信息源 · 猎手（Scout）*
