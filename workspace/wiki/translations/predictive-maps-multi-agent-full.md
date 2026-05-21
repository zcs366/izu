---
title: "多Agent推理的预测地图 — 全文翻译"
source_url: "https://arxiv.org/abs/2605.11453"
authors: "Ethan David James Parks, Dalal Alharthi"
institution: "University of Arizona"
date: "2026-05-12"
translated_by: "izu 论文skill"
slug: "predictive-maps-multi-agent"
---

# 多Agent推理的预测地图：LLM通信拓扑的继承表征谱系

> **原文标题**：Predictive Maps of Multi-Agent Reasoning: A Successor-Representation Spectrum for LLM Communication Topologies
> **作者**：Ethan David James Parks, Dalal Alharthi（亚利桑那大学）
> **日期**：2026年5月12日

---

## 摘要 Abstract

**原文**
> Practitioners deploying multi-agent large language model (LLM) systems must currently choose between communication topologies (chain, star, mesh, and richer variants) without any pre-inference diagnostic for which topology will amplify drift, converge to consensus, or remain robust under perturbation. We introduce a structural diagnostic for multi-agent LLM communication graphs based on the successor representation M = (I - γP)^(-1) of the row-stochastic communication operator, and we connect three of its spectral quantities—the spectral radius ρ(M), the spectral gap Δ(M), and the condition number κ(M)—to three distinct failure modes. We derive closed-form spectra for the chain, star, and mesh under row-stochastic normalization, and validate the predictions on a 12-step structured state-tracking task with Qwen2.5-7B-Instruct over 100 independent trials. The condition number is a perfect rank-order predictor of empirical perturbation robustness (r_s = 1.0); the spectral gap partially predicts consensus dynamics (r_s = 0.5); and the spectral radius is perfectly inverted with respect to cumulative error (r_s = -1.0). We trace this inversion to a regime in which linear spectra are blind to non-contracting bias drift, and we propose an affine-noise extension of the predictive map that recovers the empirical ordering.

**译文**
> 部署多智能体大语言模型（Multi-Agent LLM，多个 LLM 实例通过固定通信图交换信息组成的系统）系统的实践者，目前必须在通信拓扑（Communication Topology，智能体之间的信息传递结构）——链式（Chain）、星形（Star）、网状（Mesh）及更丰富的变体——之间做选择，却没有任何**推理前诊断工具**来预判哪种拓扑会放大漂移、哪种会收敛到共识、哪种在扰动下保持鲁棒。我们引入一个基于**继承表征**（Successor Representation，简称 SR——将多步影响路径压缩为单一线性算子的数学工具）M = (I - γP)^(-1) 的结构性诊断工具，并将其三个谱量——**谱半径**（Spectral Radius）ρ(M)、**谱间隙**（Spectral Gap）Δ(M) 和**条件数**（Condition Number）κ(M)——与三种不同的失败模式建立联系。我们为链、星、网在行随机归一化下推导了闭式谱，并在一个 12 步结构化状态追踪任务上用 Qwen2.5-7B-Instruct 进行了 100 次独立试验验证。条件数是经验扰动鲁棒性的完美秩序预测器（Spearman r_s = 1.0）；谱间隙部分地预测了共识动力学（r_s = 0.5）；谱半径则与累积误差**完全反相关**（r_s = -1.0）。我们将这一反相关追溯到线性谱对非收缩性偏差漂移"失明"的机制，并提出了预测地图的仿射噪声扩展，恢复了经验排序。

---

## 1. 引言 Introduction

**原文**
> A recurring lesson across cognitive science, reinforcement learning, and systems neuroscience is that intelligent behavior is shaped as much by the structure of representation as by the computations that operate over it. An agent that carries a predictive map of its environment reasons differently from one that does not, even when both have access to the same local transitions. We bring this lens to a setting in which it has rarely been applied: multi-agent LLM systems, where a handful of language model instances exchange intermediate state through a fixed communication graph. The graph is the structure. Our question is whether an appropriate representation of that structure, taken before any inference is run, can predict how the system will reason.

**译文**
> 认知科学、强化学习和系统神经科学反复揭示的教训是：智能行为既由操作于其上的计算塑造，也由**表征的结构**同等地塑造。一个携带着环境预测地图（Predictive Map，压缩了多步转移信息的内部表征）的智能体，与一个没有的智能体推理方式不同——即使两者都能访问相同的局部转移。我们将这一视角带入一个它很少被应用的领域：**多智能体 LLM 系统**。在这里，多个语言模型实例通过固定的通信图交换中间状态。**图就是结构。** 我们的问题是：在推理运行之前，该结构的一个适当表征，是否能够预测系统将如何推理？

**原文**
> The practical motivation is concrete. A designer choosing between a 12-agent chain, a judge-and-leaves star, or a peer-deliberating mesh currently has no principled diagnostic for the question *which topology amplifies drift, which converges to consensus, and which is brittle under perturbation*. Existing evaluation protocols answer these questions only after the pipeline has been executed, and only for the specific task measured. A structural diagnostic would close this loop, in the same spirit in which predictive maps close the loop between a transition structure and the behavior it supports.

**译文**
> 实践动机非常具体。一个设计者在 12 智能体链、裁判-叶子星形、或同伴审议网状之间做选择时，目前没有任何原则性诊断工具来回答：**哪种拓扑放大漂移？哪种收敛到共识？哪种在扰动下脆弱？** 现有的评估协议只能在整个管线执行完成后，且仅对特定测量任务回答这些问题。结构性诊断工具将关闭这个回路——就像预测地图在转移结构和它支持的行为之间关闭回路一样。

**原文**
> We model a multi-agent LLM system as a directed graph whose nodes are agents and whose edges are information-passing channels, and we treat the row-normalized adjacency as a stochastic transition operator. The successor representation M = (I - γP)^(-1), introduced in reinforcement learning by Dayan (1993) and subsequently shown in computational neuroscience to describe a predictive cognitive map in hippocampal circuits, compresses all multi-step influence pathways into a single linear operator. Its eigenspectrum offers three scalar summaries with distinct mechanistic meaning.

**译文**
> 我们将多智能体 LLM 系统建模为有向图（Directed Graph），节点=智能体，边=信息通道，行归一化邻接矩阵（Row-Normalized Adjacency，将每行的加权出边除以该行的总和使其成为概率分布）作为随机转移算子。继承表征 M = (I - γP)^(-1)——由 Dayan (1993) 在强化学习中引入，后经计算神经科学证明能描述海马回路中的预测认知地图——将所有多步影响路径压缩为单一线性算子。其特征谱提供三个标量摘要，各具独特的机制含义。

---

## 2. 三个谱量与三种失败模式

| 谱量 | 定义 | 预测的失败模式 |
|------|------|-------------|
| **谱半径** ρ(M) | 最大特征值的绝对值 | 误差放大倾向 |
| **谱间隙** Δ(M) | 最大与次大特征值绝对值之差 | 共识收敛速度 |
| **条件数** κ(M) | 最大与最小奇异值之比 | 扰动敏感性 |

**原文**（核心预测）
> Our claim is local and precise. On the state-tracking task, and with the model and decoding parameters described, the rank ordering of the three empirical measurements across the three topologies should agree with the rank ordering of the corresponding spectral quantity, up to any inversion that the predictive-map view itself makes visible. The spectral-radius case is where we expect such an inversion, and it is where we find one.

**译文**
> 我们的主张是局部的和精确的。在状态追踪任务上，使用所述模型和解码参数，三种经验测量在三种拓扑上的秩排序应与对应谱量的秩排序一致——除了预测地图视角本身使之可见的任何反相关。谱半径正是我们预期出现反相关之处，也正是在此处我们发现了反相关。

---

## 3. 稳定性悖论与仿射噪声模型

### 稳定性悖论

**原文**
> Read naively, the spectral radius predicts that the chain (ρ=1) should be the most stable topology under repeated information flow. Empirically, the chain exhibits the largest cumulative error, roughly twice the mesh and star. The disagreement is not a numerical artifact; it is a consequence of which kind of stability the spectral radius encodes. The spectral radius governs the geometric growth of *deterministic* perturbations to a homogeneous linear flow. The cumulative error in our task is dominated instead by accumulation of *stochastic* per-agent deviations, which is invisible to the homogeneous spectrum.

**译文**
> 天真的解读下，谱半径预测链（ρ=1）在重复信息流下应该是最稳定的拓扑。经验上，链展现出**最大的累积误差**，约是网状和星形的两倍。这一矛盾不是数值伪影；它是谱半径所编码的是**哪种**稳定性的结果。谱半径控制的是对均匀线性流的**确定性**扰动的几何增长。我们任务中的累积误差则由**随机的**逐智能体偏差累积所主导——这在均匀谱中是完全不可见的。

> *术语注：确定性扰动（Deterministic Perturbation）——可以被精确建模和传播的误差；随机偏差（Stochastic Deviation）——每个智能体独立引入的不可预测误差，其方差而非均值决定累积效应。*

### 仿射噪声模型

**原文**
> At step t, agent i produces x̂_t^(i) = τ(x̂_{t-1}) + η_t^(i), where η_t^(i) ∼ D(0, σ²), iid across agents and steps. For a topology that aggregates k agents per step, the effective per-step noise has variance σ²/k. For the chain, k=1. This gives E[E_ceg] ∝ c·σ·T^(3/2)/√k. With k=4 leaves per star step and k=4 peer agents per mesh step, the predicted chain-to-aggregated ratio is √4=2, which matches the empirical ratios in our experiment.

**译文**
> 在第 t 步，智能体 i 产生 x̂_t^(i) = τ(x̂_{t-1}) + η_t^(i)，其中 η_t^(i) ∼ D(0, σ²)，跨智能体和步骤独立同分布。对于一个每步聚合 k 个智能体的拓扑，有效每步噪声具有方差 σ²/k。对于链，k=1。这给出 E[E_ceg] ∝ c·σ·T^(3/2)/√k。每星步 4 个叶子和每网步 4 个同伴时，预测的链与聚合拓扑之比为 √4=2，与我们实验中的比率匹配。

**漂移修正增益**：
> ρ̃(M; k) = ρ(M) · √((1/n)Σ_i 1/k_i)

此修正量将三个拓扑正确排序（链 > 星 ≈ 网），恢复了裸谱半径所缺失的预测有效性。

---

## 4. 实验

### 任务

12 步结构化 JSON 状态更新，三字段：
- **Value**（浮点数）——算术精度
- **Parity** ∈ {A, B}（二进制）——条件分支
- **Level** ∈ [1, 9]（有界整数）

三个规则耦合算术精度、条件分支和有界更新。Agent 上下文在步骤间重置，误差**仅通过显式通信通道传播**。

### 拓扑

| 拓扑 | 结构 | Agent数 |
|------|------|---------|
| **链（Chain）** | 12 个顺序 Agent，每步一个 | 12 |
| **星（Star）** | 每步 4 个叶子→裁判聚合 | 48 |
| **网（Mesh）** | 4 Agent 同伴审议→多数投票 | 48 |

### 谱预测（γ=0.9）

| 拓扑 | ρ(M) | Δ(M) | κ(M) |
|------|------|------|------|
| 链 | 1.00 | 0.00 | 9.95 |
| 星 | 10.00 | 9.00 | 28.61 |
| 网 | 10.00 | 9.23 | 13.00 |

### 实验结果

| 指标 | 链 | 星 | 网 | r_s（与预测） |
|------|-----|-----|-----|-------------|
| **累积误差** E_ceg | 2094.3 | 1184.2 | 1241.0 | **-1.00**（完全反相关） |
| **共识衰减** R_cdr | 0.27 | -3.44 | -1.66 | **+0.50**（部分一致） |
| **扰动敏感度** F_ps | 237.8 | 443.6 | 247.4 | **+1.00**（完美一致） |

### 核心发现

1. **条件数 κ 是完美的扰动鲁棒性预测器**（Spearman r_s = 1.0）。在实际应用中，κ 是作者最推荐的第一个诊断量
2. **谱间隙 Δ 部分预测共识动力学**（r_s = 0.5）。星形的裁判瓶颈加速了共识，但这种显式聚合算子的效应不在裸图谱中
3. **谱半径 ρ 与累积误差完全反相关**（r_s = -1.0）——**链表面最稳定但漂移最大**。这是"稳定性悖论"的核心。漂移修正增益 ρ̃ 恢复了正确排序
4. 对于链式拓扑——即大多数简单多步推理管线采用的默认结构——**最大的风险不是发散，而是累积漂移**。每个智能体贡献的小偏差顺序累积，因为链结构中没有任何聚合步骤对它们求平均

---

## 5. 实用分流规则

**原文**
> Compute κ(M) first: it was the cleanest predictor of perturbation sensitivity. Compute Δ(M) next, with the caveat that explicit aggregation operators introduce bottlenecks the raw gap does not see. For cumulative error, do not rely on ρ(M) alone; use ρ̃(M; k), which factors in the per-step aggregation count. The full computation requires only the row-stochastic adjacency and the in-degree profile of aggregation nodes, and runs in milliseconds for graphs of practical size.

**译文**
> **先算 κ(M)**：它是扰动敏感性最干净的预测器，单个标量即可对候选拓扑排序。**再算 Δ(M)**，但要注意显式聚合算子引入了裸图谱无法体现的瓶颈。**不要仅依赖 ρ(M)** 来判断累积误差；使用 ρ̃(M; k)，它纳入了每步聚合计数。完整计算仅需行随机邻接矩阵和聚合节点的入度概貌，对实用规模的图在毫秒内完成。

---

## 6. 讨论 Discussion

**原文**
> As LLM-based systems migrate from monolithic models to multi-agent architectures, the relevant failure modes become structural properties of the communication graph rather than purely behavioral properties of any single agent; pre-inference spectral diagnostics are one instantiation of that structural turn.

**译文**
> 随着 LLM 系统从单体模型迁移到多智能体架构，相关的失败模式变成了**通信图的结构属性**，而非任何单个智能体的纯行为属性。推理前谱诊断就是这一"结构转向"的一个实例。

三点自然延伸：
1. **扫参验证**：扫 γ（折扣因子）、Agent 数量和聚合计数，直接测试 √k 预测
2. **丰富噪声模型**：智能体间相关偏差（共享基础模型导致的相关误差）违反 iid 假设，应改变聚合增益
3. **加权图**：边权重编码信任、注意力或智能体可靠性，使算子 P 本身成为可学习的对象

---

## 术语汇总

| 术语 | 英文 | 解释 |
|------|------|------|
| **继承表征** | Successor Representation (SR) | 压缩多步转移信息的线性算子 M=(I-γP)^(-1)，源自 RL，在神经科学中被发现对应海马体预测地图 |
| **谱半径** | Spectral Radius ρ | 矩阵最大特征值的绝对值。在线性系统中度量"信号放大/衰减的极限速率" |
| **谱间隙** | Spectral Gap Δ | 最大与次大特征值绝对值之差。越大，马尔可夫链混合（信息均匀散布）越快 |
| **条件数** | Condition Number κ | 最大与最小奇异值之比。度量矩阵在输入扰动下输出的敏感度——κ 越大越脆弱 |
| **行随机归一化** | Row-Stochastic Normalization | 将邻接矩阵的每行除以其总和，使行和为 1，从而成为概率转移矩阵 |
| **仿射噪声模型** | Affine-Noise Model | 假设智能体输出 = 正确结果 + 随机偏差，用于解释"线性谱不可见的漂移累积" |
| **漂移修正增益** | Drift-Corrected Gain ρ̃ | 将聚合度纳入谱半径修正的衍生诊断量，正确排序了累积误差 |
| **稳定性悖论** | Stability Paradox | 链式拓扑谱半径最小（线性最稳定）但累积误差最大——因为线性谱对随机漂移"失明" |
| **共识动力学** | Consensus Dynamics | 多智能体系统随时间趋向一致状态的过程和速率 |
| **Spearman r_s** | Spearman Rank Correlation | 秩相关系数，度量两组排名的单调一致性（-1 到 +1） |

---

*翻译日期：2026-05-13 · 工具：izu 论文skill · 原文许可：CC BY 4.0*
