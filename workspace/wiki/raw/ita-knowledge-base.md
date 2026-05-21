# ITA 技术知识体系 · 核战队补充资料

> 2026-05-17 | 综合4篇大模型分析 + 核战队合议
> 目标：补充核战队在ITA项目中需要的计算机软硬件知识

---

## 一、FSQ（有限标量量化）

### 基本概念
FSQ = Finite Scalar Quantization（Mentzer et al., Google, 2023）
- 将高维连续向量映射到离散格子
- 每维独立量化到固定值集 → 所有维的笛卡尔积构成码本
- 不需要VQ-VAE那样的可学习码本 + 辅助损失

### 与VQ-VAE对比
| 特性 | VQ-VAE | FSQ |
|------|--------|-----|
| 码本 | 可学习嵌入向量 | 隐式固定（各维度量化值的笛卡尔积）|
| 码本坍缩 | 常见（50-80%码字未用） | **不会发生经典坍缩** |
| 辅助损失 | commitment + codebook loss | 不需要 |
| 梯度传递 | argmin + 梯度复制 | STE（Straight-Through Estimator）|
| 实现复杂度 | 高（码本更新逻辑） | 低 |

### iFSQ关键发现（Lin et al., Tencent, 2026）
- FSQ虽然不会VQ式坍缩，但存在"激活坍缩"——等间隔量化与神经网络激活的非均匀分布不匹配
- 表现：部分bin利用率极低
- 修复：1行代码——用tanh映射替代线性缩放

### ITA中的应用
- Qwen-Coder-1.5B的1536维隐状态 → 投影层 → FSQ（目标~8维×N级）
- 关键参数：每维级数、总维度数、缩放因子

---

## 二、代码离散表示

### 现有方法
| 方法 | 年份 | 特点 |
|------|------|------|
| CodeBERT | 2021 | 双编码器（代码+自然语言），连续嵌入 |
| GraphCodeBERT | 2021 | 加入数据流图，捕捉变量依赖 |
| CodeT5 | 2021-2022 | Encoder-Decoder架构，支持生成 |
| Latent Programmer (Google) | 2021 | **最相关**：离散latent code → 程序合成 |
| Qwen-Coder-1.5B | 2025 | 当前ITA基座，28层，1536 hidden |

### Latent Programmer核心贡献（Hong et al., ICML 2021）
- 离散自编码器给代码变成紧凑向量（几百字节）
- 证明了"代码可以被压缩并恢复"的可行性
- **仅单向**（自然语言→代码），未做可逆（代码→latent→恢复）→ ITA补的就是这个口

---

## 三、Steering与表示工程

### 基础
- Activation Steering：向残差流隐状态添加方向向量，使输出偏向目标
- CAA（Contrastive Activation Addition, Rimsky et al. 2024）

### ITA中的特殊性
- 不是在推理时steer，而是在离散latent空间中做
- 离散空间中的"方向"不再是连续 → 每个steering step都产生量化误差
- 关键问题：漂移累积模型（线性/亚线性/指数？）

### 已知风险
- "Steering Off Course" (ACL 2025)：36个模型上测试，大量模型steering无改善甚至退化
- 跨层语义漂移是steering失效主因（GER-steer, 2026）

---

## 四、RTCE评测体系

### 现有基准
| 基准 | 测什么 | ITA相关性 |
|------|--------|----------|
| HumanEval | 代码生成正确性 | 可用于恢复验证 |
| HumanEval-X | 多语言扩展 | 后续 |
| RoundTripCodeEval (ACL 2026) | **双向一致性** | 核心基准 |
| KoLMogorov Test (ICLR 2025) | 压缩即智能 | 理论支撑 |

### ITA需要造的评测维度
1. **执行等价**：恢复代码与原代码在相同输入下输出一致
2. **语义相似**：隐状态的余弦距离
3. **编辑距离**：恢复代码与原代码的文本差异
4. **AST结构相似**：抽象语法树的结构对比

---

## 五、预算与算力

### GPU选项
| 选项 | 成本 | 适用阶段 |
|------|------|---------|
| Colab免费 | $0 | 原型验证 |
| Colab Pro (~$10/月) | $0.3-0.5/h | 实验迭代 |
| Kaggle | $0 | 数据处理 |
| RunPod/A100租赁 | $0.5-1.0/h | 训练调优 |
| 自有显卡 | 一次性投入 | 长期 |

### 推荐预算分配（$200-400）
| 项目 | 预算 | 说明 |
|------|------|------|
| GPU（Colab Pro × 3月） | $30-50 | 前3个月原型期 |
| GPU（RunPod × 20h） | $50-100 | 训练窗口 |
| Demo部署 | $50 | 非优先，晚些再花 |
| 开源模型相关（HuggingFace等） | $0-30 | 基本免费 |
| 缓冲 | $50-120 | 防翻车 |

---

## 六、执行工具链

| 工具 | 用途 | 成本 |
|------|------|------|
| PyTorch | 训练框架 | 免费 |
| FSQ-pytorch | FSQ量化实现 | 免费开源 |
| HuggingFace Transformers | 加载Qwen-Coder | 免费 |
| W&B（免费版） | 实验追踪 | 免费 |
| GitHub | 版本控制+分发 | $0/月 |
| RTCE GitHub | 评测基准fork | 免费 |

---

## 七、与已有系统的关系

| 系统 | 关系 | 说明 |
|------|------|------|
| izu | ITA 50%, izu 30% | izu继续运行日报+管弦乐队 |
| 核战队 | 不动 | 25人不调整，知识在此补充 |
| ITA语言编码研究室 | 新建 | 8人，不占核战队名额 |

---

*参考：4篇大模型分析 + [FSQ原论文](https://arxiv.org/abs/2309.09747) + [iFSQ](https://arxiv.org/abs/2601.17124) + [Layer by Layer (ICML 2025)](https://arxiv.org/abs/2405.14875) + [Steering Off Course (ACL 2025)](https://arxiv.org/abs/2501.13649)*
