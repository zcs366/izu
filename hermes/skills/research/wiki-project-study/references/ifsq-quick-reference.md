# iFSQ: Quick Reference

## Paper Info
- **Title**: iFSQ: Improving FSQ for Image Generation with 1 Line of Code
- **arXiv**: [2601.17124](https://arxiv.org/abs/2601.17124) (Jan 2026, v2)
- **Authors**: Bin Lin, Zongjian Li, Yuwei Niu, Kaixiong Gong, Yunyang Ge, Yunlin Long, Mingzhe Zheng, JianWei Zhang, Miles Yang, Zhao Zhong, Liefeng Bo, Li Yuan
- **Affiliation**: Tencent Hunyuan + Peking University
- **Code**: [github.com/Tencent-Hunyuan/iFSQ](https://github.com/Tencent-Hunyuan/iFSQ) (Apache 2.0, 101★)
- **License**: CC BY 4.0
- **Related Paper**: FSQ - [arXiv:2309.15505](https://arxiv.org/abs/2309.15505) (Mentzer et al., ICLR 2024)

## The One-Line Change
```python
# Original FSQ
z = torch.tanh(z)

# iFSQ (α=1.6 distribution-matching sigmoid)
z = 2.0 * torch.sigmoid(1.6 * z) - 1
```

## Why It Works
FSQ's equal-interval quantization assumes uniform input distribution, but neural activations are Gaussian-like. This causes **activation collapse** — center bins crowded (83.3% utilization), edge bins wasted. iFSQ transforms Gaussian activations into an approximately uniform distribution via the scaled sigmoid (α=1.6 minimizes both RMSE and KS distance to uniform).

## Three Key Findings
1. **4 bits/dim is the optimal equilibrium point** between discrete and continuous representations (neither 2 nor 8 bits improve overall quality)
2. **AR models converge faster, diffusion models reach higher quality ceiling** — strict sequential ordering limits AR's upper bound
3. **REPA alignment depth = 1/3 of total layers** for both AR and diffusion models (the "Golden Ratio" of representation alignment)

## Performance Summary

**DiT-Large (Diffusion)**:
| Tokenizer | CR | Bit | gFID | gFID+REPA |
|-----------|-----|-----|------|-----------|
| AE (16-bit) | 24× | 16 | 13.78 | 10.67 |
| FSQ | 96× | 4 | 13.38 | 11.04 |
| **iFSQ** | **96×** | **4** | **12.76** | **10.48** |
| iFSQ (2bit) | 192× | 2 | 18.52 | 14.97 |
| iFSQ (8bit) | 48× | 8 | 14.06 | 10.54 |

**LlamaGen-Large (AR)**:
| Tokenizer | Dim | Bit | gFID |
|-----------|-----|-----|------|
| VQ | 4 | 14 | 33.90 |
| **iFSQ** | **4** | **4** | **28.07** |
| iFSQ | 4 | 6 | 32.60 |

## Code Structure
```
iFSQ/
├── ifsq/          # iFSQ tokenizer (configs/ifsq_f16_d4_4bit/)
├── llamagen/      # LlamaGen-REPA (AR model)
├── dit/           # DiT-REPA (diffusion model)
├── assets/
└── requirements.txt
```

## Key Config
```json
{
  "z_channels": 4,
  "levels": [17, 17, 17, 17],   // 17^4 ≈ 83521 codes, ~4.09 bits/dim
  "act_fun": "scale_sigmoid_16",  // ★ iFSQ activation
  "hidden_size": 128,
  "hidden_size_mult": [1,1,2,4,4],
  "disc_start": 50000
}
```

## Requirements
- Python 3.10, PyTorch 2.7.1, CUDA 12.6
- 8× NVIDIA GPU (≥24GB each)
- ADM eval: separate env with CUDA 12.2, TensorFlow 2.15

## Comparison: Quantization Methods
- **VQ**: Learnable codebook → prone to collapse, needs auxiliary losses
- **FSQ**: Scalar quantization → simple, no collapse, but activation collapse
- **iFSQ**: Distribution-matching FSQ → fixes activation collapse with 1 line
- **LFQ**: Lookup-free (binary) → MAGVIT-v2, for video
- **BSQ**: Binary spherical → very high compression
- **FQ**: Factorized quantization → multi-sub-codebooks

## LlamaGen-REPA Extension
- First adaptation of REPA (Representation Alignment) to AR models
- Encoder: DINOv2-ViT-B at depth = total_layers/3
- proj_coef = 2.0 (AR) vs 0.5 (diffusion)

## Files Generated This Session
- `output/doc/ifsq-user-guide-v1.0.{md,html}` — 12.6KB user guide
- `output/doc/ifsq-tech-manual-v1.0.{md,html}` — 34.2KB tech manual
- `output/doc/ifsq-philosophy-v1.0.{md,html}` — 7.9KB philosophy essay
