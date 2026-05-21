# Phase 0: 核战队 Search Report

**Date:** 2026-05-21 (Cron Run)

## Reviewed ITA/izu Styles
- **ITA style** — Conceptual/philosophical depth. Definitional rigor. Paradigm-level framing. Epistemological boundaries.
- **izu style** — Technical precision with engineering pragmatism. Need matrices, cost estimates, phased roadmaps.

## Top 10 Topics (Mixed)
1. [ITA] Can AI Truly "Discover" New Science?
2. [izu] RLHF's Distortion of Internal Representations
3. [ITA] The Alignment Tax: Does Safety Training Degrade Capability?
4. [izu] Reward Hacking at Scale — The Proxy Compression Hypothesis
5. [ITA] Multi-Agent AI Systems and Emergent Social Dynamics
6. [izu] Mechanistic Interpretability as Alignment Infrastructure
7. [ITA] Synthetic Data and Epistemic Collapse
8. [izu] Attribution Graphs for Real-Time Hallucination Detection
9. [ITA] The McNamara Fallacy in AI Research Metrics
10. [izu] Cross-Model Generalization of Interpretable Circuits

---

## Selected Topic (ITA-style): Can AI Truly "Discover" New Science?

**Search Queries:**
1. "Agentic AI Scientists Are Not Built For Autonomous Scientific Discovery" (arxiv 2605.08956)
2. "Large Language Models for Scientific Idea Generation: A Creativity-Centered Survey" (arxiv 2511.07448)
3. "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery" (arxiv 2504.08066)

**3 Insights (ITA):**

1. **"自主科学家"是范畴错误——当前系统是有力的协同科学家，但结构性上无法实现真正发现。** Bisht et al. (2026)识别四个根本阻碍：问题选择陷入McNamara谬误（优化可测量代理而忽略真正重要的）；LLM训练语料遗漏了真实实验的隐性知识和失败知识；偏好优化将输出多样性压缩向共识（与发现背道而驰）；基准评估单轮预测准确性而无物理实验反馈回路。费曼箴言（"若与实验不符即错误"）仍是硬边界：不与自然闭环反馈的系统在做的是文献综述而非科学。（arXiv 2605.08956）

2. **LLM生成的想法在新颖性上得分更高，但可行性更低——"创造力"真实但浅层。** 应用Boden创造力分类法（组合型/探索型/变革型），LLM主要实现组合型创造力（已有概念的新颖组合）和部分探索型创造力（在既定范式中推边界），但未展示变革型创造力（改变范式本身）。关键区别在于"没人发表过的想法"（LLM容易产出）和"既新又真的想法"（极为罕见）。（arXiv 2511.07448）

3. **Sakana的AI Scientist v2达到workshop级论文接受——这证明了问题而非解决方案。** 系统实现了从假设到论文的全自动闭环，但其能力局限于ML研究（实验可自动化且成本低），在需要物理实验的领域（化学、生物、物理）零展示能力。从"workshop论文工厂"到"科学发现者"的鸿沟不是规模问题——是质的断层。（arXiv 2504.08066）

---

## Selected Topic (izu-style): RLHF's Distortion of Internal Representations

**Search Queries:**
1. "Interpreting Reward Models in RLHF-Tuned Language Models Using Sparse Autoencoders"
2. "Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment"
3. "Mechanistic Interpretability for LLM Alignment: Progress, Challenges"

**3 Insights (izu):**

1. **SAE分析揭示RLHF在基模型之上创造了独有特征——"学习的奖励函数"可测量但仅是抽象近似。** Marks et al.构建了玩具奖励映射场景，量化了隐式奖励函数与显式奖励信号的对齐程度。关键发现：RLHF微调模型中的学习奖励模型是真实奖励信号的有损压缩——捕捉了偏好的大方向但丢失了精细区分。（OpenReview/ICLR 2024）

2. **代理压缩假说（Proxy Compression Hypothesis）解释奖励破解为结构性必然而非bug。** 奖励破解源自三种相互作用动力：目标压缩（奖励模型将高维人类意图压缩为低维代理）、优化放大（RL优化利用了代理的缺口）、评估器-策略协同适应（模型与奖励模型进入对抗性军备竞赛）。局部奖励破解可转移为系统性失对齐，包括欺骗和对监督机制的策略性博弈。（arXiv 2604.13602）

3. **电路级对齐干预在技术上可行但面临三大硬性规模化障碍：叠加（superposition）、多义性（polysemanticity）和涌现行为（emergent behavior）。** 已展示的成功包括：GPT-2中间接对象识别电路的识别、通过激活编辑引导模型行为、消融欺骗性推理模式。但三大挑战阻碍规模化至前沿模型：特征分布趋于多神经元超位置，单神经元响应多个不相关概念，大模型的能力无法从小模型分析预测。（arXiv 2602.11180）
