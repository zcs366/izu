# iFSQ 研究者实操手册

> **一行代码，统一离散与连续图像生成的量化桥**
>
> 版本：v1.0 | 日期：2026-05-20
>
> 论文：[iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124) (arXiv:2601.17124)
>
> 代码：[github.com/Tencent-Hunyuan/iFSQ](https://github.com/Tencent-Hunyuan/iFSQ)
>
> 作者：Bin Lin, Zongjian Li, Yuwei Niu et al. (腾讯混元 + 北京大学)

---

## 1. 这东西是什么？一句话告诉你

**iFSQ 是一行代码改进 FSQ（有限标量量化）的方法**，让图像生成的离散模型（AR）和连续模型（扩散）可以在同一个公平平台上比较。

> **打个比方**：VQ-VAE 像用一套固定乐高积木拼图——积木用完就没办法，还会丢零件（codebook collapse）。FSQ 换成了在纸上画格子填充颜色。iFSQ 则改进填色方式——让颜料分布更均匀，每个格子都充分利用，不浪费。

---

## 2. 三分钟快速上手

### 你只需要改一行代码

原始 FSQ 的量化激活：
```python
# 原始 FSQ (tanh 激活)
z = torch.tanh(z)
```

iFSQ 的改进：
```python
# iFSQ (分布匹配激活)——唯一改了这行
z = 2.0 * torch.sigmoid(1.6 * z) - 1
```

就这。剩下所有代码不变。

### 三步流程

```text
┌─────────────────────────────────────────────────────────┐
│  Step 1: 训练 iFSQ Tokenizer                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  cd ifsq && bash configs/ifsq_f16_d4_4bit/run.sh  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Step 2: 选择生成模型训练                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  AR (LlamaGen-REPA): cd llamagen && train.py      │  │
│  │  扩散 (DiT-REPA):    cd dit && train.py           │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Step 3: ADM 评估                                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  python tools/evaluator.py ref.npz gen.npz        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 常见场景卡片

### 🟦 场景一：我想了解 iFSQ 到底解决了什么问题

**读论文**：原 FSQ 用等间隔量化（每个格子一样大），但神经网络激活值呈高斯分布（中间多两边少）。这就造成一个两难：

| 策略 | 保真度 | 效率 | 问题 |
|------|--------|------|------|
| 等间隔 (tanh) | 高 | 83.3% | 边缘格子浪费 |
| 等概率强制 | 低 | 100% | 格子边界扭曲，精度下降 |
| **iFSQ (α=1.6)** | **高** | **100%** | **两全其美** |

**一句话**：iFSQ 通过一个激活函数替换，让格子大小匹配数据分布，既没有浪费格子也不损失精度。

### 🟩 场景二：我想训练自己的 iFSQ Tokenizer

**环境要求**：
- 8× NVIDIA GPU（每卡 ≥ 24GB）
- CUDA 12.6 + PyTorch 2.7.1
- 准备 ImageNet-1K 和 COCO 2017 验证集

**启动训练**：
```bash
conda create -n ifsq python=3.10 -y
conda activate ifsq
pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt

cd ifsq
# 编辑 run.sh 中数据路径为自己本地的路径
bash configs/ifsq_f16_d4_4bit/run.sh
```

**评估**：
```bash
torchrun --nproc_per_node=8 eval_ddp.py \
  --imgnet_eval_path ${IMAGENET_VAL} \
  --model_name ImageFSQVAE \
  --ckpt_path results/ifsq_f16_d4_4bit/checkpoint-10000.ckpt \
  --model_config configs/ifsq_f16_d4_4bit/run.json \
  --resolution 256 --eval_batch_size 64 \
  --eval_lpips --eval_psnr --eval_ssim --eval_fid --ema
```

### 🟧 场景三：我想对比 AR vs Diffusion 模型

这是 iFSQ 论文最巧妙的设计——**用同一个 tokenizer 作为公平基准**：

```text
iFSQ Tokenizer (同一个权重)
       │
       ├──→ AR (LlamaGen-REPA): 收敛快，上限低
       │     训练: cd llamagen && torchrun train.py --config ...
       │
       └──→ 扩散 (DiT-REPA): 收敛慢，上限高
             训练: cd dit && accelerate launch train.py --config ...
```

**关键发现**：
1. **4 bits/dim** 是离散vs连续表示的最优平衡点
2. AR 收敛快但质量天花板低——**严格序列顺序限制了生成质量上限**
3. 扩散模型最终性能更优

### 🟥 场景四：我想复现论文核心表格

论文 Table 2（DiT-Large 扩散生成）：

| Tokenizer | CR | Bit | gFID ↓ | gFID+REPA ↓ |
|-----------|-----|-----|--------|--------------|
| AE (16-bit) | 24 | 16 | 13.78 | 10.67 |
| FSQ | 96 | 4 | 13.38 | 11.04 |
| **iFSQ** | 96 | 4 | **12.76** | **10.48** |
| iFSQ (2 bit) | 192 | 2 | 18.52 | 14.97 |
| iFSQ (8 bit) | 48 | 8 | 14.06 | 10.54 |

论文 Table 3（LlamaGen-Large AR 生成）：

| Tokenizer | Dim | Bit | gFID ↓ |
|-----------|-----|-----|--------|
| VQ | 4 | 14 | 33.90 |
| iFSQ | 4 | 2 | 31.09 |
| iFSQ | 4 | 4 | **28.07** |
| iFSQ (6 bit) | 4 | 6 | 32.60 |

---

## 4. 可视化：iFSQ 在做什么

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" font-family="sans-serif">
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">iFSQ 的激活坍缩修复原理</text>

  <!-- Left: FSQ (tanh) -->
  <text x="200" y="65" text-anchor="middle" font-size="14" font-weight="bold" fill="#c0392b">FSQ (tanh): 等间隔 = 格子浪费</text>
  <!-- Gaussian curve -->
  <path d="M 60 200 Q 100 80, 130 130 Q 160 100, 200 80 Q 240 100, 270 130 Q 300 80, 340 200" fill="none" stroke="#c0392b" stroke-width="2"/>
  <!-- Bins -->
  <line x1="60" y1="210" x2="340" y2="210" stroke="#c0392b" stroke-width="3"/>
  <line x1="95" y1="200" x2="95" y2="220" stroke="#c0392b" stroke-width="1"/>
  <line x1="130" y1="200" x2="130" y2="220" stroke="#c0392b" stroke-width="1"/>
  <line x1="200" y1="200" x2="200" y2="220" stroke="#c0392b" stroke-width="1"/>
  <line x1="270" y1="200" x2="270" y2="220" stroke="#c0392b" stroke-width="1"/>
  <line x1="305" y1="200" x2="305" y2="220" stroke="#c0392b" stroke-width="1"/>
  <!-- Density labels -->
  <text x="200" y="240" text-anchor="middle" font-size="11" fill="#c0392b">中间太挤 ↑</text>
  <text x="200" y="255" text-anchor="middle" font-size="11" fill="#c0392b">两边太空 ↓</text>
  <text x="200" y="270" text-anchor="middle" font-size="11" fill="#888">利用率: 83.3%</text>

  <!-- Arrow -->
  <text x="400" y="155" text-anchor="middle" font-size="24" fill="#8B5E3C">→ 一行代码 →</text>

  <!-- Right: iFSQ (sigmoid 1.6) -->
  <text x="600" y="65" text-anchor="middle" font-size="14" font-weight="bold" fill="#27ae60">iFSQ (σ(1.6x)): 均匀分布 = 全利用</text>
  <!-- Uniform distribution -->
  <rect x="410" y="95" width="190" height="105" rx="3" fill="#27ae60" opacity="0.15"/>
  <line x1="410" y1="200" x2="600" y2="200" stroke="#27ae60" stroke-width="3"/>
  <line x1="437" y1="190" x2="437" y2="210" stroke="#27ae60" stroke-width="1"/>
  <line x1="464" y1="190" x2="464" y2="210" stroke="#27ae60" stroke-width="1"/>
  <line x1="491" y1="190" x2="491" y2="210" stroke="#27ae60" stroke-width="1"/>
  <line x1="518" y1="190" x2="518" y2="210" stroke="#27ae60" stroke-width="1"/>
  <line x1="545" y1="190" x2="545" y2="210" stroke="#27ae60" stroke-width="1"/>
  <line x1="572" y1="190" x2="572" y2="210" stroke="#27ae60" stroke-width="1"/>
  <text x="505" y="240" text-anchor="middle" font-size="11" fill="#27ae60">所有格子均匀利用</text>
  <text x="505" y="255" text-anchor="middle" font-size="11" fill="#27ae60">利用率: 100%</text>

  <!-- Key formula -->
  <text x="400" y="320" text-anchor="middle" font-size="13" fill="#555">Z_iFSQ = 2.0 × σ(1.6 × Z_input) − 1</text>
  <text x="400" y="340" text-anchor="middle" font-size="11" fill="#888">每维度约4 bits，4维共16 bits → 17⁴ = 83521个离散码</text>

  <!-- Results box -->
  <rect x="150" y="370" width="500" height="110" rx="8" fill="#f0f4f8" stroke="#ddd"/>
  <text x="400" y="395" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">iFSQ 核心成果</text>
  <text x="170" y="418" font-size="11" fill="#555">• 一行代码：tanh → 2·σ(1.6x)−1</text>
  <text x="170" y="435" font-size="11" fill="#555">• 4 bits/dim 是最优离散-连续平衡点</text>
  <text x="170" y="452" font-size="11" fill="#555">• AR 收敛快，扩散上限高</text>
  <text x="170" y="469" font-size="11" fill="#555">• REPA 最优对齐深度 = 总层数 × 1/3（黄金比例）</text>
</svg>
```

---

## 5. 快速参考表

| 你想做什么 | 终端命令 | 或者直接跟我说 |
|-----------|---------|--------------|
| 训练 iFSQ tokenizer | `bash configs/ifsq_f16_d4_4bit/run.sh` | 军师，帮我训练 iFSQ tokenizer |
| 训练 AR 生成模型 | `cd llamagen && torchrun train.py --config fsq17x4_.../config.yaml` | 军师，启动 LlamaGen-REPA 训练 |
| 训练扩散生成模型 | `cd dit && accelerate launch train.py --config fsq17x4_.../run.yaml` | 军师，启动 DiT-REPA 训练 |
| 评估 tokenizer | `torchrun --nproc_per_node=8 eval_ddp.py ...` | 军师，评估 tokenizer |
| 计算 FID | `python tools/evaluator.py ref.npz gen.npz` | 军师，算 FID |
| 改一行代码测试 | `act_fun = scale_sigmoid_16` | 军师，把激活改成 iFSQ |

---

## 6. 常见疑问 (FAQ)

### Q: iFSQ 比原始 FSQ 好多少？
rFID 从 13.38 → 12.76（降低 4.6%），bin 利用率从 83.3% → 100%，且不需要任何额外参数。

### Q: 我能在自己的项目里用 iFSQ 吗？
可以，Apache 2.0 协议，改一行代码就行。注意需要 PyTorch 2.7.1+ 和 CUDA 12.6。

### Q: iFSQ 只能用于 ImageNet 256×256 吗？
论文主要验证了这个设定，但方法完全通用——任何使用 FSQ 的场景都可以用 iFSQ 替换。

### Q: iFSQ 和 LFQ、BSQ 有什么区别？
| 方法 | 本质 | 特点 |
|------|------|------|
| FSQ | 标量量化 | 简单但等间隔不匹配分布 |
| **iFSQ** | **分布匹配标量量化** | **一行代码修复 FSQ** |
| LFQ | 无查找量化 | 用于视频 tokenizer |
| BSQ | 二值球面量化 | 压缩率极高但质量有损 |

### Q: 我只有单卡能跑吗？
可以但慢。论文所有实验使用 8×GPU。单卡可以尝试减小 batch size（如从 16→4 每卡）。

### Q: REPA 对齐深度为什么是 1/3 总层数？
论文发现对 AR 和扩散模型都适用——浅层对齐欠抽象，深层对齐过语义，1/3 处恰好是视觉语义与生成目标的黄金平衡点。

---

## 7. 学习路径

```text
Day 1:  读原 FSQ 论文 (arXiv:2309.15505) → 理解 VQ→FSQ 的动机
Day 2:  读 iFSQ 论文 (arXiv:2601.17124) → 理解一行代码的原理
Day 3:  配置环境 → 跑通 eval_ddp.py
Day 4:  训练自己的 iFSQ tokenizer
Day 5:  对比 LlamaGen-REPA vs DiT-REPA
Day 6:  尝试不同 bits/dim 配置
Day 7:  在自己的数据集上实验
```

---

## 来源汇总

1. Lin B et al. (2026). *iFSQ: Improving FSQ for Image Generation with 1 Line of Code*. arXiv:2601.17124.
2. Mentzer F et al. (2024). *Finite Scalar Quantization: VQ-VAE Made Simple*. ICLR 2024. arXiv:2309.15505.
3. GitHub: Tencent-Hunyuan/iFSQ. Apache 2.0 License.
4. Hugging Face Papers: papers/2601.17124.
5. Yu J et al. (2024). *MAGVIT-v2: Language Model Beats Diffusion — Tokenizer is Key to Visual Generation*. ICLR 2024.
6. Lu H et al. (2024). *Representation Alignment for Diffusion Models*.
