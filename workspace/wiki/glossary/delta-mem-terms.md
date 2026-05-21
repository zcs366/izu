# δ-mem 术语表

> 来源：arXiv 2605.12357
> 生成：2026-05-13

| # | 术语 | 英文 | 定义 | 使用场景 |
|---|------|------|------|---------|
| 1 | δ-mem | delta-mem | 一种轻量级LLM记忆机制，用紧凑的在线联想记忆状态增强冻结骨干 | 本文核心方法 |
| 2 | 在线联想记忆状态 | Online State of Associative Memory (OSAM) | 固定尺寸矩阵S∈R^{r×r}，通过delta规则在线更新以编码历史键-值关联 | δ-mem的核心数据结构 |
| 3 | Delta规则学习 | Delta-rule learning | 仅根据预测残差更新权重的在线学习算法，S_t = S_{t-1} + β(v_t − S_{t-1}k_t)k^⊤ | 状态更新的数学基础 |
| 4 | 低秩修正 | Low-rank correction | 通过r维向量经固定投影矩阵产生的对注意力Q/O的微调信号 | δ-mem引导注意力的方式 |
| 5 | 门控Delta更新 | Gated delta update | 引入逐维遗忘门λ_t和写入门β_t的delta规则变体 | 控制记忆保留/遗忘 |
| 6 | 记忆投影 | Memory projection | 将d维隐藏状态映射到r维（r≪d）联想记忆空间的可训练投影矩阵 | 形成记忆键/查询/值 |
| 7 | 写入粒度 | Writing granularity | 状态更新的基本单位（token/片段/多状态） | TSW/SSW/MSW的设计空间 |
| 8 | Token状态写入 | Token-State Write (TSW) | 每个token位置触发一次状态更新 | 最细粒度，噪声敏感 |
| 9 | 序列状态写入 | Sequence-State Write (SSW) | 以消息/片段为单位，片内平均隐藏状态后触发一次更新 | 平滑演化，丢失细节 |
| 10 | 多状态写入 | Multi-State Write (MSW) | 维护N个并行子状态各自独立读写 | 减少类型干扰，参数更多 |
| 11 | 上下文退化 | Context rot | 上下文长度增加导致信息利用效率降低的现象 | δ-mem的动机之一 |
| 12 | 上下文恢复 | Context recovery | 移除显式上下文后仅凭压缩状态恢复信息的能力 | 消融实验§5.1 |
| 13 | 冻结骨干 | Frozen backbone | 参数被冻结不参与训练的预训练Transformer模型 | δ-mem的基底 |
| 14 | 注意力头 | Attention head | 注意力计算中Q/K/V/O四组投影及其组合 | 消融实验§5.2中研究修正注入位置 |
| 15 | 插入深度 | Insertion depth | δ-mem模块插入到Transformer的哪些层 | §5.3消融显示中间层最优 |
| 16 | 监督微调 | SFT / Supervised Fine-Tuning | 在有标注数据上的自回归语言建模训练 | δ-mem的训练范式 |
| 17 | QASPER | — | 学术论文问答数据集 | δ-mem的训练数据（仅用2,219最短样本） |
| 18 | MemoryAgentBench | — | 含准确检索、测试时学习、长程理解、选择性遗忘四子类的记忆基准 | 主要评测集之一 |
| 19 | LoCoMo | — | 长期对话记忆评估基准（多跳/时序/开放域/单跳） | 主要评测集之一 |
| 20 | HotpotQA | — | 多跳问答基准（含Bridge和Comparison子类） | 通用+记忆评测 |
| 21 | Context2LoRA | — | 将上下文信息编码到LoRA参数中的参数化记忆基线 | 对比基线 |
| 22 | MLP Memory | — | 用独立MLP模块检索并融合外部记忆的基线 | 外部通道记忆基线 |
| 23 | MemGen | — | 生成式潜记忆方案 | 参数化记忆基线 |
| 24 | MemoryBank | — | 文本形式的连续交互记忆条目管理 | 文本记忆基线 |
