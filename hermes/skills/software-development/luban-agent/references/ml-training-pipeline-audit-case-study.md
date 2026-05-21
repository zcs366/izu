# ML Training Pipeline Audit Case Study: ITA Three-Stage Framework (2026-05-17)

> Source: 鲁班审计韩信 NLA→ITA 训练方案
> Context: Qwen2.5-Coder-1.5B冻结 + FSQ量化 + 离散codebook的ITA编码器训练方案

## Background

韩信提出ITM/ITA的三阶段训练框架：
1. SFT预热（AST→codebook映射监督训练）
2. GRPO强化重建（Actor生成离散code + reward = MSE+可编译性+CodeBLEU）
3. 对抗训练（判别器区分重建vs真实代码）

## Key Findings

### GRPO Framework Coupling

| 维度 | 韩信假设 | 实际代码状态 |
|------|---------|-------------|
| 目标RL框架 | TRL GRPOTrainer | TRL的GRPOTrainer假设actor是LLM（text completion），非通用encoder |
| Actor输出 | 离散code序列 | 不是text token → 不能用`GRPOTrainer(model=encoder)` |
| 替代方案 | — | 需要从零写自定义训练循环（~30-40h） |
| 结论 | ❌ 框架耦合检查不通过 | GRPOTrainer不直接支持ITA编码器 |

### Reward Engineering Hidden Cost

| Reward维度 | 韩信描述 | 实际成本 |
|-----------|---------|---------|
| MSE重建损失 | "简单MSE" | ✅ 5行代码，🟢低 |
| 可编译性 | "β系数" | ❌ 需要编译环境+安全性+超时，训练速度降10-100x |
| CodeBLEU | "γ系数" | 🟡 有现成库，但集成+调参需3-5h |
| 对抗判别器 | "GAN Loss" | ❌ GAN训练不稳定+需要生成器判别器双状态追踪 |

### 叠床架屋检测

- **阶段数**：3（SFT→GRPO→GAN）
- **GRPO在FSQ离散空间的价值**：🟡低。NLA的GRPO有value是因为AV输出自然语言（搜索空间~32K），ITA codebook是固定有限集（~16807码字），GRPO的exploration-利用平衡完全不同
- **对抗训练对M1的必要性**：🔴低。语义保真可通过CodeBLEU评估，MSE模型还没跑通就上对抗是典型的过度工程
- **结论**：❌ 严重叠床架屋。砍掉S2+S3后估时从80-100h降至15-22h（-78%）

### 框架假设差距

- **方案说的**："借鉴NLA的GRPO配方→直接移植到ITA编码器训练"  
- **代码里有的**：TRL GRPOTrainer只支持LLM；ITA编码器无代码存在；FSQ无代码存在
- **差距**：从零起步，且框架假设不匹配

## Audit Outcome

| 条目 | 结论 |
|------|------|
| GRPO集成复杂度 | 🔴高（30-40h），TRL框架不支持 |
| FSQ实现复杂度 | 🟢低（4-6h baseline），但集成到GRPO后变🔴 |
| 三阶段叠床架屋 | ✅严重，砍掉S2+S3 |
| 装备清单 | 砍后只需4件（原8件）：ita_encoder.py, ita_trainer.py, ita_eval.py, layer_scanner.py |
| 模型滥用风险 | GRPO reward中可编译性不应用模型判断，应用代码判断；但训练循环本身代码可控 |
| 总估时变化 | 80-100h → 15-22h（-78%） |

## Lessons for Future ML Pipeline Audits

1. **RL框架的隐式假设**：TRL/Axolotl/OpenRLHF都不是通用RL框架，它们假设特定的输入输出格式。在确认框架兼容性前，RL方案的估时需×2-3。
2. **Reward公式≠Reward工程**：公式写3行，工程实现可能3000行。逐维审计成本：编译环境、运行时、维护负担。
3. **GRPO在固定离散空间的价值衰减**：当action空间是有限集（VS开放文本）时，GRPO的exploration增益指数级下降。适合用简单对比学习替代。
4. **阶段数触发阈值**：≥3阶段的训练方案自动触发叠床架屋审查。不需要证明简单方案不可行就堆复杂度。
