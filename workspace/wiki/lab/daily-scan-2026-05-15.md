# 🔬 izu 前沿实验室 · 每日扫描

**日期**：2026-05-15（周五） · 扫描窗口：05-14 ~ 05-15
**猎手**：Scout · **呈**：张成市

---

## 📊 今日论文清单

### 一、Agent 自我迭代（Self-Evolution）

| # | 论文 | 来源 | 核心方法（一句话） | 热度 | 评级 |
|---|------|------|-------------------|------|------|
| 1 | **HAGE: Harnessing Agentic Memory via RL-Driven Weighted Graph Evolution** | arXiv 2605.09942 / HF ❤️10 💬1 | 将Agent记忆建模为多关系加权图（语义/时序/因果/实体），用RL联合优化路由网络和边特征，实现查询条件化的自适应记忆检索 | HF trending score 10 | ⭐⭐⭐⭐ |
| 2 | **ActGuide-RL: Learning Agentic Policy from Action Guidance** | arXiv 2605.12004 / HF ❤️11 💬1 | 利用人类日常交互产生的Action Data作为参考引导，替代昂贵的SFT冷启动；GAIA +10.7pp, XBench +19pp（Qwen3-4B） | HF trending score 11 | ⭐⭐⭐⭐⭐ |
| 3 | **Revisiting DAgger in the Era of LLM-Agents** | arXiv 2605.12913 / Georgia Tech / HF ❤️5 | 将DAgger算法引入多轮LLM Agent训练，学生策略与教师策略逐轮插值，同时享受SFT的密集监督+RL的在线交互纠正covariate shift | HF trending score 5 | ⭐⭐⭐⭐⭐ |
| 4 | **Context Training with Active Information Seeking** | arXiv 2605.13050 / DeepMind / HF ❤️4 | 上下文优化器+Wikipedia搜索+浏览器工具主动获取信息，搜索式训练+候选上下文剪枝；覆盖翻译/医疗/推理/人类最后的考试 | HF trending score 4 | ⭐⭐⭐ |
| 5 | **Many-Shot CoT-ICL: Making In-Context Learning Truly Learn** | arXiv 2605.13511 / HF ❤️1 | 研究many-shot链式思考上下文学习，揭示标准many-shot规则不能直接迁移，提出新的示例选择策略 | HF trending score 26 | ⭐⭐⭐ |

### 二、多Agent协作架构

| # | 论文 | 来源 | 核心方法（一句话） | 热度 | 评级 |
|---|------|------|-------------------|------|------|
| 6 | **MAP: A Map-then-Act Paradigm for Long-Horizon Interactive Agent Reasoning** | arXiv 2605.13037 / HF ❤️4 | 三阶段"先建图再行动"：全局探索→任务特定映射→知识增强执行，解决Agent的延迟环境感知和认知瓶颈 | HF trending score 4 | ⭐⭐⭐ |
| 7 | **AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation** | arXiv 2605.12925 / Microsoft / HF ❤️2 | 揭示10.7%的SWE-bench通过轨迹是"侥幸通过"（盲目重试/回归循环/验证缺失），提出过程级评估框架 | HF trending score 2 | ⭐⭐⭐⭐ |
| 8 | **EVA-Bench: End-to-end Framework for Evaluating Voice Agents** | arXiv 2605.13841 / ServiceNow / HF ❤️114 💬2 | 首个语音Agent端到端评估框架，模拟真实对话，双复合指标EVA-A（准确性）+ EVA-E（体验） | HF ❤️114 | ⭐⭐⭐ |
| 9 | **Predicting Decisions of AI Agents from Limited Interaction** | arXiv 2605.12411 / Technion / HF ❤️1 | 表格基础模型+LLM文本表示，从有限交互回合预测Agent在谈判博弈中的决策 | HF trending score 42 | ⭐⭐⭐ |

### 三、AI × 人文社科

| # | 论文 | 来源 | 核心方法（一句话） | 热度 | 评级 |
|---|------|------|-------------------|------|------|
| 10 | **BenCSSmark: Making the Social Sciences Count in LLM Research** | arXiv 2605.04886 | 立场论文：社会科学任务在LLM基准测试中严重缺席，提出跨学科基准设计框架 | 新发布 | ⭐⭐⭐ |
| 11 | **Grounded Satirical Generation with RAG** | arXiv 2605.10853 | RAG+时事新闻→讽刺性词典定义生成（芬兰语境），首个"有事实基础的AI讽刺"流水线 | 新发布 | ⭐⭐⭐ |
| 12 | **APSA AI & Politics Task Force Report** | APSA官方报告 / 2026-05 | 60位社会科学家×8个月×11章：AI与政治学的全面交叉审视（选举/治理/舆论/伦理） | 重大发布 | ⭐⭐⭐⭐ |
| 13 | **From Faces to Politics: VLMs Link Visual Demographics to Ideological Labels** | Political Analysis (Cambridge) | 视觉语言模型在分析政治内容时是否用人口特征作为意识形态归属的捷径？ | 期刊发表 | ⭐⭐⭐ |

---

## 🏆 值得深挖 TOP 3

| 排名 | 论文 | 理由 |
|------|------|------|
| 🥇 | **ActGuide-RL** (2605.12004) | 对Hermes Agent训练最有实战价值：用人机交互的Action Data替代昂贵的SFT冷启动，Agent自我迭代的新范式。Qwen3-4B+ActGuide不输SFT+RL流水线 |
| 🥈 | **Revisiting DAgger** (2605.12913) | 4B Agent打8B系统（SWE-bench 27.3%），训练方法可直接迁移至Hermes Agent的多轮工具调用训练 |
| 🥉 | **HAGE** (2605.09942) | 加权多关系记忆图是Agent长期记忆的核心基础设施，与izu知识管理系统直接相关 |

---

## 📡 今日热点信号

> **🔴 主信号**：**Agent训练范式正在从前SFT+RL的"烧钱冷启动"转向数据高效的新路径**——ActGuide-RL用人类交互数据替代SFT、DAgger用在线插值统一SFT和RL，两篇同天出现在HF Daily Papers，正在重塑Agent训练的经济学。这是"Agent自我迭代"从口号走向落地的关键转折。

> **🟡 辅信号**：社区对"AI Agent是否赚钱"的讨论白热化（HN 100+ comments），同时"Agent侥幸通过率10.7%"（AgentLens）打脸了以pass rate为唯一指标的Agent评估体系，评估方法论正在经历信任危机。

---

> 💡 **猎手点评**：今天的三篇TOP论文构成了一个完整链条——**记忆（HAGE）→ 训练（ActGuide-RL + DAgger）→ 评估（AgentLens）**。Agent自我迭代不再是一个孤立的技术点，而是正在形成一个完整的技术栈。注意这个栈的每一层都在昨天（5/14）同步出现了新工作，这不是巧合。
>
> 📌 **明日关注**：A2A Protocol生态地图（97M MCP下载量 vs 50+ A2A合作方）的协议之战，预计将有新的互操作标准发布。

---

*扫描覆盖：HuggingFace Daily Papers (56篇) · HN front page · Reddit r/MachineLearning / r/LocalLLaMA · arXiv cs.AI/cs.CL/cs.LG · APSA · Political Analysis*
*下次扫描：2026-05-16 08:00*
