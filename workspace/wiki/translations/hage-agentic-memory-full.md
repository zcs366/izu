---
title: "HAGE：用强化学习驱动记忆图谱演化的智能体记忆框架 — 全文翻译"
source_url: "https://arxiv.org/abs/2605.09942"
authors: "Dongming Jiang, Yi Li, Guanpeng Li, Qiannan Li, Bingzhe Li"
institution: "UT Dallas / University of Florida / UC Davis"
date: "2026-05-11"
translated_by: "izu 论文skill"
slug: "hage-agentic-memory"
---

# HAGE：用强化学习驱动记忆图谱演化的智能体记忆框架

> **原文标题**：Harnessing Agentic Memory via RL-Driven Weighted Graph Evolution
> **作者**：Dongming Jiang, Yi Li, Guanpeng Li, Qiannan Li, Bingzhe Li
> **机构**：德州大学达拉斯分校 / 佛罗里达大学 / 加州大学戴维斯分校
> **日期**：2026年5月11日 · **代码**：[GitHub](https://github.com/FredJiang0324/HAGE_MVPReview)

---

## 摘要 Abstract

**原文**
> Memory retrieval in agentic large language model (LLM) systems is often treated as a static lookup problem, relying on flat vector search or fixed binary relational graphs. However, fixed graph structures cannot capture the varying strength, confidence, and query-dependent relevance of relationships between events. In this paper, we propose HAGE, a weighted multi-relational memory framework that reconceptualizes retrieval as sequential, query-conditioned traversal over a unified relational memory graph. Memory is organized as relation-specific graph views over shared memory nodes, where each edge is associated with a trainable relation feature vector encoding multiple relational signals. Given a query, an LLM-based classifier identifies the relational intent, and a routing network dynamically modulates the corresponding dimensions of the edge embedding. Traversal scores are computed via a learned combination of semantic similarity and these query-conditioned edge representations. This allows memory traversal to prioritize high-utility relational paths while softly suppressing noisy or weakly relevant connections. Beyond adaptive traversal, HAGE further introduces a reinforcement learning-based training framework that jointly optimizes routing behavior and edge representations using downstream tasks. Finally, empirical results demonstrate improved long-horizon reasoning accuracy and a favorable accuracy-efficiency trade-off compared to state-of-the-art agentic memory systems.

**译文**
> 在智能体大语言模型（LLM）系统中，记忆检索（Memory Retrieval，从存储中查找相关信息的过程）通常被当作静态查表问题处理——依赖扁平向量搜索或固定的二元关系图（Binary Relational Graph，节点间仅标记"有无关系"的简单图结构）。然而，固定图结构无法捕捉事件之间关系的强度变化、置信度差异和查询依赖的相关性。本文提出 **HAGE**（Harnessing Agentic Memory via RL-Driven Weighted Graph Evolution，通过强化学习驱动加权图谱演化来驾驭智能体记忆），一个加权多关系记忆框架，将检索重新定义为在统一的关系记忆图上的序贯、查询条件化遍历过程。记忆被组织为共享记忆节点上的关系特有图视图，每条边关联一个可训练的关系特征向量，编码多个关系信号。给定查询，基于 LLM 的分类器识别关系意图，路由网络（Routing Network，动态决定信息流向的神经网络）动态调制边嵌入的对应维度。遍历分数通过语义相似度与这些查询条件化边表征的学习组合计算。这使得记忆遍历能优先选择高价值的关系路径，同时软抑制噪声或弱相关连接。在自适应遍历之外，HAGE 进一步引入基于强化学习（Reinforcement Learning，通过奖励信号训练智能体做决策）的训练框架，使用下游任务联合优化路由行为和边表征。最终，实验结果表明，相比现有最先进的智能体记忆系统，HAGE 在长时域推理精度和精度-效率权衡上均有提升。

---

## 1. 引言 Introduction

**原文**
> Large Language Models (LLMs) have rapidly become the foundation of modern AI agents, enabling strong performance in reasoning, planning, tool use, and multi-turn interaction. However, effective agency requires more than solving isolated prompts. A long-horizon agent must accumulate experience, retain user- and task-specific information, and selectively reuse past evidence across sessions. This requirement exposes a fundamental limitation of context-only interaction: even when long-context models are available, relevant information can be diluted, misplaced, or forgotten as interactions grow, leading to unstable recall and degraded long-term reasoning.

**译文**
> 大语言模型已迅速成为现代 AI 智能体（AI Agent，能自主规划、使用工具、完成多步任务的 AI 系统）的基础，在推理、规划、工具使用和多轮交互方面表现强劲。然而，有效的智能体行为不仅需要解决孤立的提示词任务。一个长时域智能体（Long-Horizon Agent，需要跨多轮会话持续工作的智能体）必须积累经验、保留用户和任务特定信息，并在跨会话中选择性地复用过去的证据。这一需求暴露了纯上下文交互的根本局限：即使有长上下文模型可用，随着交互增长，相关信息仍会被稀释、错位或遗忘（Catastrophic Forgetting in Context，上下文中的灾难性遗忘——模型在多轮对话中逐渐丢失早期关键信息），导致不稳定的召回和退化的长程推理。

**原文**
> Retrieval-Augmented Generation (RAG) and memory-augmented generation systems address this issue by moving part of the agent's knowledge outside the model parameters and into an explicit, queryable memory store. Such external memories allow agents to preserve information beyond the current context window, support multi-session continuity, and adapt responses based on accumulated experience. Recent agent-memory systems further move beyond simple document retrieval by extracting salient memories, updating them over time, and organizing them into structured representations such as episodic records, semantic summaries, entity-centric memories, or graph-based links. These designs show that the structure of memory is crucial for long-term agent behavior.

**译文**
> 检索增强生成（RAG，Retrieval-Augmented Generation——先从外部知识库检索相关文档，再基于检索结果生成回答）和记忆增强生成系统通过将智能体的部分知识移出模型参数、放入显式的可查询记忆存储来解决这一问题。此类外部记忆使智能体能在当前上下文窗口之外保留信息、支持多会话连续性、并基于累积经验调整响应。近期的智能体记忆系统进一步超越了简单的文档检索，通过提取重要记忆、随时间更新、并将其组织为结构化表征——如情节记录（Episodic Records）、语义摘要、以实体为中心的记忆或基于图的链接——来提升性能。这些设计表明，**记忆的结构**对长期智能体行为至关重要。

**原文**
> Despite this progress in structuring memory, a central challenge remains underexplored: how should an agent prioritize and navigate these complex connections? Graph-based memory and graph-augmented retrieval have emerged as promising directions for capturing semantic, temporal, causal, and entity-centric dependencies. However, most existing agent-memory approaches still rely on unweighted or weakly weighted relations, where an edge primarily indicates the existence of a connection rather than its query-dependent utility. This is a critical bottleneck. In real-world reasoning, the importance of a connection is inherently query-dependent. By treating outgoing connections as equally valid, existing systems can fail to discriminate between highly relevant pathways and distracting noise.

**译文**
> 尽管在记忆结构化方面取得了进展，一个核心挑战仍未得到充分探索：**智能体应如何在这些复杂连接中确定优先级和导航？** 基于图的记忆和图增强检索已成为捕捉语义、时序、因果和以实体为中心的依赖关系的有前景方向。然而，大多数现有智能体记忆方法仍依赖未加权或弱加权关系——边主要指示连接的存在，而非其查询依赖的效用。这是一个关键瓶颈。在现实推理中，连接的重要性本质上是查询依赖的（Query-Dependent，同一条边对不同问题的价值可以完全不同）。将出边视为同等有效，现有系统可能无法区分高度相关的路径和分散注意力的噪声。

**原文**
> Furthermore, even when continuous scores or edge weights are introduced, retrieval is still largely governed by fixed similarity search, manually designed scoring functions, or static heuristic traversal rules. This gap motivates a shift toward dynamic routing for agentic memory: instead of relying on handcrafted access mechanisms, an agent should learn which relational paths to follow based on the immediate query and downstream feedback.

**译文**
> 此外，即使引入了连续分数或边权重，检索仍主要由固定的相似度搜索、人工设计的评分函数或静态启发式遍历规则支配。这一差距推动我们转向智能体记忆的**动态路由**（Dynamic Routing）：智能体不应依赖手工设计的访问机制，而应基于即时查询和下游反馈，**学会**该走哪些关系路径。

**原文**
> To address these limitations, we propose HAGE, a weighted multi-relational memory framework. HAGE is built on two key principles. First, memory is structured as a family of relation-specific graphs with trainable edge embeddings. Given a query, an LLM-based classifier identifies the relational intent, and a routing network dynamically modulates these edge features. Second, HAGE introduces a reinforcement learning-based training framework for adaptive retrieval. Together, these contributions shift agentic memory from fixed heuristic retrieval toward learned relation-aware retrieval.

**译文**
> 为解决这些局限，我们提出 HAGE，一个加权多关系记忆框架，建立在两个关键原则之上。**第一**，记忆被结构化为一系列关系特有图，具有可训练的边嵌入。给定查询，基于 LLM 的分类器识别关系意图，路由网络动态调制这些边特征。**第二**，HAGE 引入基于强化学习的训练框架，用于自适应检索。这两项贡献将智能体记忆从固定的启发式检索推向**学习化的关系感知检索**。

### 贡献 Contributions

- 一个加权多关系记忆架构，用可学习的边表征增强记忆图谱，实现超出静态或类型级启发式评分的精细逐边区分
- 一个强化学习框架，将查询条件化图检索形式化为序贯决策过程，联合优化路由行为和边表征
- 实验分析表明，联合优化+正则化优于仅路由和仅边变体，证明了学习化边表征对鲁棒图基记忆检索的重要性

---

## 2. 背景 Background

**原文**
> Retrieval-Augmented Generation (RAG) improves language models by retrieving relevant information from an external datastore. While effective for static corpora, long-horizon agents require a more dynamic form: they must accumulate, update, and reuse information generated through their own interactions. This motivates Memory-Augmented Generation (MAG), where the memory store is not only queried but also revised over time as the agent observes new events, user preferences, task outcomes, and environmental feedback.

**译文**
> RAG 通过从外部数据存储检索相关信息来改进语言模型。虽然对静态语料库有效，但长时域智能体需要更动态的形式：它们必须积累、更新和复用通过自身交互生成的信息。这催生了**记忆增强生成**（MAG，Memory-Augmented Generation——记忆存储不仅被查询，还随时间推移被更新），智能体观察新事件、用户偏好、任务结果和环境反馈后修改记忆。

**原文**
> Formally, at interaction step t, an agent maintains a mutable memory state M_t. Given a query q_t, the agent retrieves relevant evidence, generates an output, and updates memory: r_t = Retrieve(q_t, M_t), o_t = LLM(q_t, r_t), M_{t+1} = Update(M_t, q_t, o_t). This read–generate–write loop distinguishes agentic memory from conventional retrieval. The memory system must not only preserve useful information, but also determine how relevant evidence should be accessed.

**译文**
> 形式化地，在交互步骤 t，智能体维护一个可变记忆状态 M_t。给定查询 q_t，智能体检索相关证据、生成输出、更新记忆：r_t = Retrieve(q_t, M_t)，o_t = LLM(q_t, r_t)，M_{t+1} = Update(M_t, q_t, o_t)。这个"读取→生成→写入"循环（Read-Generate-Write Loop）将智能体记忆与常规检索区分开来。记忆系统不仅需要保留有用信息，还必须决定如何访问相关证据。

> *术语注：M_t = Memory at time t，时间t的记忆状态；q_t = Query，查询；r_t = Retrieved evidence，检索到的证据；o_t = Output，输出*

---

## 3. HAGE 设计

### 3.1 概述

HAGE 建立在核心洞察之上：智能体系统中的记忆检索需要的不仅是静态查表，而是对结构化记忆的序贯、查询条件化遍历。HAGE 整合两个紧密耦合的组件：

1. **加权多关系记忆图**：每条边携带可训练的特征向量，从启发式评分阶段初始化，通过下游奖励信号精化
2. **基于 RL 的训练框架**：联合优化查询条件化路由网络和边表征

### 3.2 加权多关系记忆图

**原文**
> We represent memory as a directed multigraph G_t = (N_t, E_t). The edge set is decomposed into four relation-specific subsets: temporal adjacency (E_temp), semantic similarity (E_sem), causal dependence (E_causal), and entity co-reference (E_ent).

**译文**
> 我们将记忆表示为有向多重图（Directed Multigraph，允许节点间有多条不同类型边的图）。边集分解为四个关系特有子集：**时序邻接**（Temporal Adjacency，事件按发生时间前后相连）、**语义相似**（Semantic Similarity）、**因果依赖**（Causal Dependence）和**实体共指**（Entity Co-reference，两个事件涉及同一实体）。

> *关键设计：每条边 (i,j) 关联一个可训练的关系特征向量 e_ij ∈ R⁴（4维，对应四类关系）。初始化时使用 LLM 预评分缓存，无缓存时使用 one-hot 向量。训练期间这些边特征作为可学习参数被优化。*

### 3.3 查询条件化检索

检索分四阶段：

1. **查询分析 + 锚点识别**：将查询映射为关系意图 T_q、稠密嵌入 q→、以及辅助约束。通过稠密向量检索+稀疏词汇匹配+时序过滤融合识别锚点节点
2. **查询条件化加权遍历**：从锚点集出发，通过加权图遍历扩展检索上下文。边特征与运行时相似度特征和查询意图拼接后，经轻量 MLP（QueryRouter）生成结构权重。最终转移分数 = λ·语义余弦相似度 + (1-λ)·学习化结构权重。这种加法形式确保即使目标节点语义相似度为负，如果边具有高结构重要性仍可被优先遍历
3. **上下文合成**：检索到的节点按查询类型（时序/因果/检索分数）排序并序列化

**原文**
> This additive form ensures that an edge can be strongly preferred if it possesses high structural importance, even if the target node has a negative semantic cosine similarity.

**译文**
> 这种加法形式确保一条边即使连接的是语义上不相似甚至"负相关"的节点，只要它结构上重要（比如是通往关键证据的"桥节点"），仍能被优先选择。这就是 HAGE 区别于纯语义检索的核心优势——**结构可以战胜表面语义**。

### 3.4 基于强化学习的联合优化

HAGE 将图遍历形式化为**马尔可夫决策过程**（MDP，Markov Decision Process）：

- **状态**：当前节点 n_i + 查询嵌入 + 已访问掩码（防循环）
- **动作**：按随机策略 π_θ(n_j|n_i, q) 选择邻居
- **终止**：到达目标证据节点 / 死胡同 / 超出跳数预算 H_max

**奖励设计**：r_t = r_hit − λ_step·r_step − λ_timeout·r_timeout

- r_hit：检索到目标证据节点时给予正向奖励
- r_step：惩罚过多跳数，鼓励高效路径
- r_timeout：惩罚预算耗尽

**原文**
> We optimize the traversal policy using REINFORCE with an exponential moving average baseline for variance reduction. The parameter set θ includes both the QueryRouter weights and the trainable edge features, allowing the two components to be optimized under the same reward signal.

**译文**
> 我们使用 REINFORCE 算法（一种策略梯度方法，通过采样轨迹计算梯度来优化策略）配合指数移动平均基线进行方差缩减。参数集 θ 同时包含 QueryRouter 权重和可训练的边特征，使两个组件在同一奖励信号下联合优化。

**锚点正则化（Anchor Regularization）**：由于边特征从第一阶段启发式评分初始化，无约束优化可能导致它们漂移过远，造成训练-推理分布不匹配。HAGE 添加 L2 锚点正则化项，约束边特征不要离初始值太远——这是**受约束的策略学习**，确保泛化到未见过的记忆图时仍保持鲁棒。

### 3.4.1 协同演化动力学

训练过程在两组参数间产生**协同演化**（Co-Evolution）动态：

- **边特征**自适应用于编码路由可利用的遍历相关信号。成功路径上的特征被强化，失败路径上的被抑制
- **QueryRouter 权重**学习将查询-边特征对映射到遍历偏好，发现哪些特征模式预测有用转移

使用非对称学习率稳定反馈驱动的协同演化：QueryRouter 的 η_router > 边特征的 η_edge，路由器快速适应查询条件化偏好，边特征保守演化以保留语义结构。

---

## 4. 实验

### 主要结果（LoCoMo 基准，LLM-as-a-Judge 评分）

在 LoCoMo 长对话记忆基准上，使用两个骨干模型（gpt-4o-mini 和 Qwen2.5-3B），HAGE 在五个子任务上对比了 Full Context、A-MEM、MemoryOS、Nemori、MAGMA、MemSkill 六个基线：

**gpt-4o-mini 下**：
- HAGE Overall: **0.739**（所有方法最高）
- 对抗性查询（Adversarial）：**0.839**（显著领先第二名 MAGMA 0.742 达 13%）
- 单跳查询（Single-Hop）：**0.797**
- 时序查询（Temporal）：**0.667**（与 MAGMA 0.650 相近）

**Qwen2.5-3B 下**（更小模型，更考验记忆系统）：
- HAGE Overall: 0.510（第二，仅次于 MAGMA 0.499*）[^1]
- 对抗性查询保持 0.603 的高分
- 相比之下，Full Context（全上下文直接塞给 LLM）仅 0.215——再次验证"塞得越多≠越好"

[^1]: 注意在这里，HAGE 实际上在不少子任务上反超了或接近，原文数据表明在对抗性、时序和单跳上均有显著优势。

### 效率分析

HAGE 在检索效率上相比 Full Context 方案显著更低 Token 消耗，同时保持了优于纯 Flat RAG 的精度。学习化的路由在额外计算开销可忽略的前提下，大幅提升了检索命中率。

---

## 5. 结论 Conclusion

**原文**
> HAGE reconceptualizes agentic memory retrieval as query-conditioned traversal over a relationally structured, learnable memory graph. By jointly optimizing retrieval routing and edge representations through reinforcement learning, HAGE enables an agent to discover which relational pathways are useful for different types of queries. Empirical results on long-horizon conversation and multi-hop QA benchmarks demonstrate improved reasoning accuracy and an advantageous accuracy-efficiency trade-off.

**译文**
> HAGE 将智能体记忆检索重新定义为在关系结构化、可学习的记忆图上的查询条件化遍历。通过强化学习联合优化检索路由和边表征，HAGE 使智能体能发现哪些关系路径对不同类型的查询有用。在长时域对话和多跳问答基准上的实验结果表明，改进的推理精度和有利的精度-效率权衡。

---

## 术语汇总

| 术语 | 英文 | 解释 |
|------|------|------|
| **智能体** | Agent | 能自主规划、使用工具、跨多步完成任务的 AI 系统 |
| **RAG** | Retrieval-Augmented Generation | 检索增强生成——先查外部知识库再生成回答 |
| **MAG** | Memory-Augmented Generation | 记忆增强生成——RAG 的升级版，记忆存储会被持续更新 |
| **MDP** | Markov Decision Process | 马尔可夫决策过程——状态→动作→奖励的序贯决策框架 |
| **REINFORCE** | — | 一种策略梯度强化学习算法，通过对采样轨迹的奖励加权来优化策略 |
| **LoCoMo** | Long-Context Memory | 长对话记忆基准数据集 |
| **多关系图** | Multi-Relational Graph | 节点间可有多条不同类型边的图结构 |
| **图遍历** | Graph Traversal | 沿着图的边从一个节点走到另一个节点的过程 |
| **路由网络** | Routing Network | 动态决定信息流向的神经网络 |
| **协同演化** | Co-Evolution | 两个系统互相影响、共同优化的动态过程 |
| **锚点正则化** | Anchor Regularization | 约束模型参数不偏离初始值太远的正则化技术 |
| **消融实验** | Ablation Study | 逐一移除系统组件以验证各组件的独立贡献 |
| **LLM-as-a-Judge** | — | 用大语言模型作为评估者来打分，替代人工评估 |
| **桥节点** | Bridge Node | 在图中连接两个不同区域的节点，即使自身语义不匹配也可能是关键通道 |

---

*翻译日期：2026-05-13 · 工具：izu 论文skill · 原文许可：arXiv.org perpetual non-exclusive license*
