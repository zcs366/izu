# 成市守恒律 (Chengshi Conservation Law) 实验复现

## 核心公式

**d × r × log₂(L) ≈ C（常数）**

其中：
- **d** = 每轮传输的压缩维度
- **r** = 递归反馈轮次
- **L** = 每维度量化级数（FSQ）
- **C** = 在给定解码器权重 W 下的相对 Kolmogorov 复杂度 K_W(意图)

## 实验架构

```
experiments/consv_law/
├── scripts/        # 16个原始实验脚本（完整迭代审计轨迹）
├── data/           # 实验数据 (NPY)
├── results/        # 实验结果 (JSON)
└── run_all.py      # 全实验统一复现脚本
```

## 实验清单（按论文章节）

| 章节 | 实验 | 核心结论 | 对应脚本 |
|------|------|---------|---------|
| §3.1 | T-C2 同模型意图编码 | 384维断崖，ModernBERT有效语义维度 | `scripts/iat_tc2_experiment.py` |
| §3.2 | d×r=常数 平凡验证 | D₀=552, D_noisy=664, 噪声地板 | `scripts/iat_feedback_experiment.py` |
| §3.3 | Chomsky 层级实验 | 四层合成数据均坍缩到 D₀=8 | `scripts/iat_chomsky_experiment.py` |
| §3.3 | 语义复杂度实验 | L1-L4 真实句子语义维度 | `scripts/iat_semantic_complexity.py` |
| §3.4 | 语义反馈实验 | 结构化不对齐下反馈节省 91% 维度 | `scripts/iat_structured_feedback.py` |
| §3.5 | FSQ 量化压缩 | FSQ-7 700D cos=0.950, 比FP32压缩9x | `scripts/iat_fsq_experiment.py` |
| §3.6 | 递归联合实验 | 乘积守恒贯穿，8.2x压缩 | `scripts/iat_fsq_recursive.py` |
| §3.6 | 递归验证 | 递进式 + 残差重编码 d×r=常数 | `scripts/iat_recursive_verification.py` |

## 复现命令

```bash
cd experiments/consv_law
python3 run_all.py
```

### 环境要求

- Python 3.11+
- PyTorch 2.x + CUDA
- `pip install transformers sentence-transformers scikit-learn numpy`
- 模型：ModernBERT-base (`answerdotai/ModernBERT-base`)
- 随机种子：42

### 产物

- `data/` - 原始数据 NPY 文件
- `results/` - 结构化 JSON 结果 + 终端日志

## 命名权

公式 d×r×log₂(L)≈常数 已命名为 **"成市守恒律"** (Chengshi Conservation Law)，
待公开发表后锁定优先权。

## 版本

- v1: 2026-06-01 初始实验链
- 复现轮次: 2026-06-01 (本目录)
