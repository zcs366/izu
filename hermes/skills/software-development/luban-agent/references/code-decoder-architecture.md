# 代码解码器架构 · 从隐空间生成代码

> **适用场景**：需要从连续/离散隐空间表示重建代码文本时
> **实战验证**：ITA v1.2.0 (2026-05-19)，Transformer Decoder 2层，10步训练后 loss 下降
> **设计约束**：零外部依赖（仅 torch），生成时延 ≤500ms/函数 (A100)

## 核心架构

```
Latent Vector (1, seq_len, d_model)
    ↓
ITADecoder.decode_latent()
    ├── mock模式 → 直接返回原始代码（开发调试用）
    ├── 未训练状态 → 返回原始代码 + untrained=True 标记
    └── 已训练状态 → 委托给 CodeDecoder.generate()
                            ↓
              CodeDecoder (nn.TransformerDecoder)
                ├── Token Embedding (vocab_size → d_model)
                ├── Positional Encoding (正弦位置编码)
                ├── Transformer Decoder (2层, 4头, 256维)
                ├── Linear Head (d_model → vocab_size)
                └── 自回归生成 (greedy, <bos> 起, <eos> 止)
                            ↓
              Token IDs 序列
                            ↓
              PythonTokenizer.decode() → 代码文本
```

## 关键组件

### 1. 词表设计 (PythonTokenizer)

| 类别 | 内容 | 大小 |
|------|------|------|
| 特殊标记 | `<pad>` `<bos>` `<eos>` `<unk>` `<indent>` `<dedent>` `<nl>` | 7 |
| 关键字 | `def` `if` `else` `return` ... (Python 35个) | 35 |
| 运算符 | `+` `-` `*` `**` `/` `//` `==` `!=` ... | ~34 |
| 分隔符 | `(` `)` `[` `]` `{` `}` `,` `:` `;` `.` ... | ~9 |
| 标识符占位 | `<id>` — 所有变量/函数名 | 1 |
| 字面量占位 | `<lit>` — 数字/字符串 | 1 |
| 保留位 | `<extra_N>` — 填充至 4096 | ~128 |

**分词的实现**：用正则匹配，按最优先匹配关键字（整词）→ 运算符 → 分隔符 → 字符串 → 数字 → 标识符 → 空白。

**关键设计决策**：标识符和字面量用占位符 `<id>` 和 `<lit>`，而非全词表。原因：
- 词表保持小（~200定长），decoder参数少
- 训练关注的是代码结构（def/if/return等控制流），不是具体变量名
- 解码时 `<id>` 恢复为 `x`，`<lit>` 恢复为 `0`

### 2. Transformer Decoder (CodeDecoder)

```
CodeDecoder(
  d_model=256,          # 隐空间维度，与编码器 latent_dim 对齐
  nhead=4,              # 注意力头数
  num_layers=2,         # 解码器层数（足够验证收敛性）
  dim_feedforward=1024, # FFN中间层
  max_seq_len=512,      # 最大生成长度
)
```

**前向传播**：
```
tgt_tokens → Embedding (×√d_model) → Positional Encoding → TransformerDecoder(memory) → Linear → Logits
```

**自回归生成**：
```
<bos> → decoder → token₁
<bos>, token₁ → decoder → token₂
<bos>, token₁, token₂ → decoder → token₃
...直到 <eos> 或 max_len
```

**关键设计**：
- `batch_first=True` — 批维在第一位，与 HuggingFace 风格一致
- `norm_first=True` — Pre-LN 结构，训练更稳定
- 因果掩码 (causal mask) 由 `generate_square_subsequent_mask` 自动生成
- `padding_idx=0` — 填充位置不学习梯度

### 3. 状态管理

| 状态 | 判断依据 | decode() 行为 |
|------|---------|--------------|
| mock | `mock=True` | 恒等返回原始代码 |
| 未训练 | `trained=False` | 返回原始代码 + `untrained=True` 标记 |
| 已训练 | `trained=True` | 执行真实 transformer 生成 |

**重要性**：未训练状态返回原始代码 + untrained标记，是军规一（不造假）的落实。metric消费者看到 `untrained=True` 就不会误信 edit_similarity=1.0。

### 4. 验证方法

最小验证（不依赖预训练模型）：
```
def test_loss_decreases():
    # 1. 计算初始 loss
    loss_before = F.cross_entropy(decoder(memory, tgt_input), tgt_labels)
    # 2. 训练 10 步
    for _ in range(10):
        optimizer.zero_grad()
        loss = F.cross_entropy(decoder(memory, tgt_input), tgt_labels)
        loss.backward(); optimizer.step()
    # 3. 验证 loss 下降
    loss_after = F.cross_entropy(decoder(memory, tgt_input), tgt_labels)
    assert loss_after < loss_before
```

## 集成模式

解码器不独立存在，而是编码器 (`ITAEncoder`) 的一个组件：

```
ITAEncoder
  ├── HiddenStateExtractor → ProjectionLayer → FSQQuantizer
  └── ITADecoder  ← 新增组件
       └── CodeDecoder (Transformer)
```

`encode()` 产出 `LatentCode` (含 `continuous` 和/或 `codes/indices`)
`decode(latent)` 调用 `ITADecoder.decode_latent(latent)` 得到代码文本
`round_trip(code)` = `decode(encode(code))` → 指标对比

## 实战数据

| 指标 | 数值 |
|------|------|
| 代码行数 | 544行 (src/decoder.py) |
| 测试用例 | 22测 (test_decoder.py) |
| 初始loss | ~4.2 (vocab_size=256, 随机初始化) |
| 10步优化后loss | ~3.8 (Adam, lr=0.01) |
| 生成速度 | <100ms/函数 (CPU, greedy, max_len=512) |

## 参考

- ITA 解码器实现：`/mnt/i/hermes/ita/src/decoder.py`
- ITA 解码器测试：`/mnt/i/hermes/ita/tests/test_decoder.py`
- 原理解读：原始 code tokenizer 从源文本提取 token，位置编码注入结构信息，transformer decoder 以 latent 为条件逐 token 生成。本质是条件语言模型。
