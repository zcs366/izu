# Phase 1A: ITA 6轮合议（Test-Time Scaling + Pre-Training Joint Optimization）

## Round 0 — 惠施：概念澄清

**核心概念体系：**

1. **Test-Time Scaling (TTS)** ≠ Inference Scaling：TTS特指通过增加推理阶段计算量（采样次数、搜索深度、推理轮次等）来提升LLM输出质量的策略家族。而Inference Scaling更宽泛，涵盖模型量化、KV-cache优化等降低推理成本的方法。

2. **T2T² (Train-to-Test)**：Nicholas Roberts等人2026年提出的联合scaling law框架，统一建模预训练计算（模型大小D、数据量T）和测试时计算（采样数K）。其核心突破是将pass@K测试时指标与预训练loss通过一个联合函数映射，而非传统Chinchilla只优化预训练loss。

3. **Overtraining Region**：当计入推理成本时，最优模型不再遵循Chinchilla的20 tokens/param比率，而是向"小模型+多tokens"方向移动（overtraining）。直觉：一个3B模型经过500B tokens训练，其单次推理成本低，可通过多次采样弥补单次能力不足。

4. **Pass@K 非线**：测试时scaling的收益不是线性的——pass@K = 1 - (1 - p)^K（独立同分布假设下），其中p是单次正确概率。p是模型大小和训练数据量的函数。因此联合优化需要在D、T、K三者间寻找最优曲面。

5. **RL Post-Training Coupling**：RL后训练（GRPO/PPO）改变模型的单次正确率p的分布特性，从而改变scaling曲线的形状。RL scaling law与TTS scaling law之间存在交叉耦合。

**关键模糊点：**
- p的独立同分布假设在overtrained小模型上是否成立？（可能出现正确/错误的聚类模式）
- 不同downstream task的pass@K函数形态差异有多大？
- 后训练如何与T2T²联合框架兼容——是加法因子还是乘法因子？

---

## Round 1 — 墨子：形式化验证

**T2T²核心形式框架：**

1. **联合优化问题**：
   ```
   给定总计算预算 C_total = C_train + C_test
   其中 C_train = 6 × D × T （FLOPs，假设训练data的每个token 6 FLOPs/param）
   C_test = K × C_infer = K × 2 × D （FLOPs，假设推理每个token约2 FLOPs/param)
   
   目标：在C_total约束下最大化pass@K
   pass@K = 1 - (1 - p(D, T))^K
   ```

2. **p(D, T) 的形式**：T2T²假设p可以表示为损失函数的单调变换：
   ```
   p(D, T) = σ(α - β × L(D, T))
   其中L(D, T) = L_∞ + A × D^(-a) + B × T^(-b) （经典scaling law形式）
   σ为sigmoid或类似函数
   ```

3. **关键形式化结果**：
   - 当K=1（单次推理），退化为Chinchilla优化
   - 当K→∞，最优D趋向0（极端overtraining：无限次采样补偿一切）
   - 实际最优位于两者之间，具体位置取决于β（p对loss的敏感度）
   - T2T²重要的形式突破是证明**overtraining是推理scaling的必然结果**而非巧合

4. **验证条件**：
   - 需要验证p(D,T)的单调变换假设是否成立
   - 八项downstream task上验证通过（论文报告），但多是推理密集型任务
   - 对非推理任务（翻译、摘要）的适用性未充分验证
   - 结论对post-training（RLHF/RL后训练）的鲁棒性——论文声称"survives post-training"，但仅测试了有限配置

**形式化挑战**：
- pass@K的独立同分布假设在LLM上不严格成立（采样间存在相关性）
- 缺乏跨任务类型的p(D,T)泛化形式
- 未形式化定义后训练对p(D,T)的修正函数

---

## Round 2 — 商鞅：实验设计

**关键实验一：联合边界测绘**
- 设C_total = 1e22 FLOPs（约等价于训练一个7B Chinchilla-optimal模型）
- 系统扫描D ∈ {1B, 3B, 7B, 13B}，T ∈ {Chinchilla推荐值, 2×, 4×, 8×}，K ∈ {1, 4, 16, 64, 256}
- 在MATH、GSM8K、HumanEval、MMLU-Pro、BIG-Bench Hard上测量pass@K
- 输出：3D Pareto前沿曲面，标注每个预算分配下的最优配置

**关键实验二：p(D,T)函数形式拟合**
- 从实验一数据反向拟合p(D,T) = σ(α - β × L_hat(D,T))
- 测量β的跨任务稳定性
- 检验σ函数的替代形式（如Gumbel、Probit）

**关键实验三：后训练修正实验**
- 对每个(D,T)配置做RL后训练（GRPO，budget固定）
- 测量后训练后p' = p + Δ(D,T, RL_budget)
- 验证Δ是否可表示为乘法因子（p' = γ × p）还是更复杂形式
- 检查不同RL算法（GRPO vs PPO）的Δ差异

**关键实验四：非独立采样检验**
- 对同一question生成K个答案，计算答案间的Bhattacharyya距离分布
- 如果距离分布集中在0附近（答案高度相似），则pass@K假设被违反
- 测量"有效多样性"H_eff = -Σ P(answer_i) log P(answer_i) / log K
- 比较不同overtraining程度下的H_eff差异

---

## Round 3 — 鲁班：工程可行

**可行性评估：**

1. **实验一（联合边界测绘）**：
   - 总计算量：约25个模型×推理评估 ≈ 2.5e23 FLOPs ≈ 250K GPU-hours (H100)
   - 耗时：若使用512 GPU并行，约20天
   - 现有基础设施可支持 ✅
   - 瓶颈：推理评估时的prompt工程和任务构建

2. **实验二（函数形式拟合）**：
   - 计算量小，数据分析为主
   - 需谨慎处理噪声：pass@K是随机变量，需多次复现 ✅
   - 现有工具（numpy/scipy/JAX自动微分）完全足够

3. **实验三（后训练修正）**：
   - 每个配置RL后训练需约10%额外预训练计算
   - 25×0.1×原始预算≈2.5e22 FLOPs
   - 关键风险：RL训练不稳定，可能需要在多个seed上运行
   - 中度可行 ⚠️

4. **实验四（多样性检验）**：
   - 计算量轻，分析密集型
   - 仅需存储K个生成的完整文本
   - 完全可行 ✅

**工程约束**：
- 最大挑战：25个不同(D,T)配置的训练管线需要强大的实验管理（W&B风格的tracking必需）
- 推理评估的标准化：不同任务的数据集格式、评估脚本的差异可能导致不可比
- 成本：整体实验约300K-500K GPU-hours，约为一个小型开源模型的训练预算

---

## Round 4 — 萧何：资源路径

**所需资源估算：**

| 资源项 | 需求 | 获取路径 | 时间线 |
|--------|------|----------|--------|
| GPU算力 | 500K H100-hours | 租赁（Lambda/火山引擎）约$300-500K | 随时 |
| 数据 | 覆盖8任务的评估集 | 开源（MATH、GSM8K等） | 已有 |
| 工程团队 | 2-3人（训练+评估+分析） | 内部调配或合作 | 2周 |
| 实验管理 | 1套W&B/MLflow | 现有 | 已有 |
| 论文写作 | 1-2周 | 内部 | 最后 |

**执行路线**：
1. Week 1-2：训练管线搭建，验证基础模型质量
2. Week 3-6：实验一（联合边界测绘）
3. Week 7：实验二（函数拟合）
4. Week 8-9：实验三（后训练），并行实验四（多样性）
5. Week 10：分析综合、论文撰写

**风险与缓解**：
- 算力成本超支 → 缩小扫描范围，锁定最有信息量的(D,T,K)组合
- RL训练不稳定 → 先在小规模验证GRPO实现正确性
- 结果不可发表（负结果）→ 负结果也有学术价值，关于scaling law的假设检验文献稀少

---

## Round 5 — 张仪：最强攻击

**攻击一：Overtraining的边界——计算资源分配的根本谬误？**
T2T²的核心论点是"计入推理成本后最优配置向overtraining偏移"，但这个结论隐含了一个关键假设：**推理计算成本与训练计算成本是同质的**。实际上，推理计算需要使用低延迟、高可靠性的部署硬件（在线服务），而训练计算可以使用高延迟、可容错的批处理硬件。如果推理计算的实际货币成本是训练的2-3倍（由于SLA要求），则最优偏移量会大幅缩小。T2T²论文默认假设1 FLOP = 1 FLOP，这是廉价的。

**攻击二：Pass@K 假设的脆弱性**
pass@K = 1 - (1-p)^K 假设每次采样**独立同分布**。但实际的LLM推理中：
- 使用相同的prompt和采样参数，两次生成的答案高度相关（温度低时更甚）
- 模型存在"自信回路"：对某些问题无论采样多少次都产生同样错误
- T2T²声称的pass@K增益在实际部署中可能被严重高估，因为"有效独立采样数"远小于K
- 论文中未报告采样的实际多样性指标（如self-BLEU、distinct n-grams）

**攻击三：p(D,T)→Loss映射的非平凡性**
将pass@K通过σ(α - βL)与loss关联，假设了p是loss的单调递减函数。但已知：
- 同loss不同架构的模型有不同推理能力
- RLHF后loss可能增加但推理能力提升
- 不同任务对loss下降的敏感度不同（某些任务存在"threshold"效应）
这个映射假设是整个T2T²大厦的基石，但论文对其验证不够充分——仅在8个任务上做相关性检验，而非因果检验。

**攻击四：Chinchilla重现性危机的回声**
Hoffmann等人的Chinchilla scaling已被后续研究质疑（如Kaplan vs Chinchilla的冲突）。T2T²的预测是否重蹈覆辙？论文自己承认"forecasts are robust over distinct modeling approaches"，但未说明scaling参数的置信区间。如果在近期模型（如Llama 4、Gemini 3）上复现失败，则T2T²可能成为又一个过度泛化的scaling law。

**攻击五：实用性——后训练的"存活"声称空洞**
论文声称T2T²结论"survives the post-training stage"，但仅测试了少量post-training配置。现实中的SOTA模型经过了RLHF、DPO、GRPO等多阶段复杂后训练，每阶段都改变p(D,T)的分布。T2T²能否在真正的"production pipeline"中存活是未回答的问题。
