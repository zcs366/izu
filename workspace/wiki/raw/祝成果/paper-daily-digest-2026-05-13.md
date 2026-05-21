# 📄 AI 前沿日报

**日期**：2026-05-13 · **呈：张成市**
**今日精选**：3 篇 ｜ 来源：arXiv / HuggingFace / Hacker News
**关联项目**：爱祝（izu）/ Hermes Agent / Wiki 知识系统

---

## 1. HAGE：用强化学习驱动记忆图谱演化的智能体记忆框架

> Harnessing Agentic Memory via RL-Driven Weighted Graph Evolution

- **技术分类**：Agent 记忆架构 / 知识图谱
- **来源**：[arXiv 2605.09942](https://arxiv.org/abs/2605.09942) ｜ Paper Reading Club 有讨论
- **热度**：arXiv 5月11日提交 ｜ 有配套代码
- **主要观点**：把 Agent 记忆检索从"静态向量查表"升级为"查询驱动、强化学习优化的图谱遍历"，记忆图谱的边权重会根据检索效果持续演化
- **摘要**：当前大多数 LLM Agent 的记忆系统沿用标准 RAG 管线——把历史交互压平向量化，做相似度检索。但 Agent 的记忆不是被动的文档库，而是需要捕捉实体间多关系、支持推理跳跃、随任务动态演化的活结构。HAGE 提出了一套加权多关系记忆框架：把检索重新定义为在知识图谱上的序贯、查询条件化遍历过程，用强化学习（RL）优化每条边的权重和连接偏好。实验表明，在多跳推理和长期对话场景中，HAGE 的检索命中率和下游任务完成率显著优于 Flat RAG 和 GraphRAG 基线。
- **与我们相关**：直接关联 **Wiki 知识系统**（从 raw → wiki → 定本的图谱化记忆）和 **izu 研究流水线**（Agent 记忆如何跨会话积累）。HAGE 的"查询驱动的图谱演化"思路，可以直接启发爱祝的记忆层设计——不是存文档，而是存可演化的关联网络。
- **推荐**：⭐⭐⭐⭐⭐
- **扩展阅读**：
  - 关联论文：[Graph-based Agent Memory: Taxonomy, Techniques, and Benchmarks](https://arxiv.org/abs/2602.05665)
  - 关联论文：[Beyond RAG for Agent Memory: Retrieval by Decoupling and Re-encoding](https://arxiv.org/abs/2602.02007)

---

## 2. δ-mem：大语言模型的高效在线记忆机制

> δ-mem: Efficient Online Memory for Large Language Models

- **技术分类**：LLM 记忆 / 在线学习
- **来源**：[arXiv 2605.12357](https://arxiv.org/abs/2605.12357) ｜ HuggingFace Daily Papers 🔥
- **热度**：HuggingFace ❤️ 26 ｜ 提交者 @gaotang 获 57 票 ｜ GitHub 开源
- **主要观点**：让 LLM 在不重新训练的情况下实时积累和使用新信息，只需存储"变化量"（δ）而非全量上下文
- **摘要**：LLM 的核心局限之一是知识截止日期——训练完成后的新信息无法被模型直接使用。δ-mem 提出了一种在线记忆机制：将新信息编码为"变化量"（delta），存储在外部记忆库中；推理时自动检索最相关的 δ 注入上下文。相比 Long-Context 方案（把所有历史塞进 prompt），δ-mem 的 Token 开销降低 60-80%；相比传统 RAG（每次重新检索），δ-mem 维护了一个持续更新的紧凑记忆状态。在 Needle-in-Haystack 和 StreamingQA 测试中表现优异。
- **与我们相关**：直接关联 **Hermes Agent 的会话记忆**（跨 session 持久记忆如何高效存取）和 **Wiki 知识系统**（增量摄入如何触发已有知识的自动更新）。δ-mem 的核心思路——只存变化量，而不是全量——对我们优化 Hermes 的 memory 注入机制有直接参考价值。
- **推荐**：⭐⭐⭐⭐⭐
- **扩展阅读**：
  - 关联论文：[MemORAI: Memory Organization and Retrieval via Adaptive Graph Indexing](https://arxiv.org/abs/2605.01386)
  - 开源代码：[GitHub - Declare-lab & MindLab-Research](https://github.com/)

---

## 3. 多Agent推理的预测地图：LLM通信拓扑的继承表征谱系

> Predictive Maps of Multi-Agent Reasoning: A Successor-Representation Spectrum for LLM Communication Topologies

- **技术分类**：多 Agent 架构 / Agent 通信
- **来源**：[arXiv 2605.11453](https://arxiv.org/abs/2605.11453) ｜ 5月12日新提交
- **热度**：arXiv 新提交 ｜ 跨 cs.MA / cs.AI / cs.CL 三领域
- **主要观点**：不同 Agent 通信拓扑（全连接/链式/树形/星形）会导致截然不同的推理路径分布，可以使用"继承表征"（Successor Representation）方法提前预测哪种拓扑对特定任务最有效
- **摘要**：多 Agent LLM 系统的核心设计选择之一是 Agent 之间的通信拓扑——谁跟谁说话、什么顺序、什么条件。但当前对拓扑的选择主要靠经验和直觉。这篇论文建了一个结构性诊断框架：将多 Agent 系统建模为有向图（节点=Agent，边=信息通道），用继承表征技术分析不同拓扑下推理路径的覆盖范围和盲点。在 MATH、MMLU、StrategyQA 等基准上发现：简单的全连接拓扑在事实型任务上最优，但链式-星形混合拓扑在需要多步推理的任务上反超 12-18%。论文给出了一个拓扑选择的"光谱"——从探索型到利用型再到混合型——供研究者按任务类型选择。
- **与我们相关**：直接关联 **izu 流水线的七智能体架构**（探→搜→织→对齐→写→劈→修→核 的信息流设计）和 **Hermes Agent 的 subagent 调度**（delegate_task 的最优并行-串行策略）。这篇论文的拓扑-任务匹配框架可以直接用来优化 izu 流水线中各 Agent 的通信结构。
- **推荐**：⭐⭐⭐⭐
- **扩展阅读**：
  - 关联论文：[Reinforcement Learning for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2605.02801)
  - 关联论文：[Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning](https://arxiv.org/abs/2604.02460)（对立观点：单Agent有时比多Agent更好）

---

> 💡 **军师的话**：今天的论文指向同一个趋势——**Agent 的核心瓶颈正在从"模型能力"转向"记忆和信息流架构"**。HAGE 的图谱演化、δ-mem 的增量记忆、Predictive Maps 的拓扑选择，三篇分别回答了三个关键问题：记什么、怎么存、谁跟谁说话。izu 流水线的 v2.0 已经触碰到了这一步（对齐角色、核角色），但更深层的"记忆跨会话生长"和"Agent 间的自适应拓扑"还有很大空间。
>
> 📌 **建议**：HAGE 和 δ-mem 两篇，用 `论文skill` 做全文翻译+izu研究，优先 HAGE（因为直接给出可借鉴的架构设计）。
