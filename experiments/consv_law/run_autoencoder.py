#!/usr/bin/env python3
"""
§3.7 非线性 Autoencoder 验证：d×r×log₂(L) 守恒在非线性压缩下是否成立？

这是对论文最关键的补充实验——当前所有实验都基于 PCA（线性压缩），
批评者可攻击为"PCA恒等式"。Autoencoder 使用非线性激活函数（ReLU），
若守恒律仍成立，则大幅强化论文普适性声明。

设计：
  - 编码器：768 → 512 → ReLU → d（瓶颈）
  - 解码器：d → 512 → ReLU → 768
  - 训练：2000 随机高斯 + 20 语义意图，MSE重建
  - 量化：训练后对瓶颈层做 FSQ
  - 验证：d×r×log₂(L) ≈ 常数？
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import json
import os
os.environ["HF_HUB_OFFLINE"] = "1"
from datetime import datetime
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

# ─── 配置 ──────────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FULL_DIM = 768
N_RANDOM = 2000
N_INTENTS = 20
TARGET_COS = 0.95
SEED = 42
EPOCHS = 200
BATCH_SIZE = 64
LR = 1e-3

np.random.seed(SEED)
torch.manual_seed(SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DATA_DIR = os.path.join(BASE_DIR, "data")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def cos_sim_np(x, y):
    return float(np.mean(np.sum(x * y, axis=1)))

# ════════════════════════════════════════════════════
# 数据生成
# ════════════════════════════════════════════════════
print("═" * 65)
print("§3.7 非线性 Autoencoder 验证")
print("═" * 65)

# 随机高斯数据
data_random = np.random.randn(N_RANDOM, FULL_DIM)
data_random /= np.linalg.norm(data_random, axis=1, keepdims=True)

# 语义意图数据
model_st = SentenceTransformer("answerdotai/ModernBERT-base", device=DEVICE, local_files_only=True)
intents = [
    "我需要你帮我分析这篇论文的方法论缺陷",
    "请用三句话总结今天的所有讨论",
    "帮我在wiki里搜索关于语言压缩的所有文章",
    "将这段代码从Python翻译成Rust",
    "生成一份关于上周工作的总结报告",
    "对比分析GPT-4和Claude在代码生成上的差异",
    "用通俗的语言解释反向传播算法",
    "设计一个实验来验证压缩维度乘以递归轮次等于常数",
    "帮我找出项目中所有未完成的TODO项",
    "写一封邮件给合作者讨论论文修改意见",
    "分析这组数据的统计特征并画图",
    "解释为什么语言是认知压缩的最佳工具",
    "规划下周的工作安排和优先级",
    "将这篇中文文章翻译成英文并保持学术风格",
    "审查这段代码的安全漏洞",
    "用三个比喻解释什么是嵌入向量",
    "生成一个Python脚本来批量处理这些文件",
    "总结Chomsky和Hinton在语言本质上的分歧",
    "帮我设计数据库的表结构",
    "分析当前Agent系统的瓶颈并提出优化方案",
]
data_semantic = model_st.encode(intents, normalize_embeddings=True)
print(f"随机高斯: {data_random.shape}, 语义意图: {data_semantic.shape}")

# ════════════════════════════════════════════════════
# Autoencoder 模型
# ════════════════════════════════════════════════════
class NonlinearAE(nn.Module):
    def __init__(self, input_dim, bottleneck_dim, hidden=512):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, bottleneck_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(bottleneck_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, input_dim),
        )

    def encode(self, x):
        return self.encoder(x)

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        return self.decode(self.encode(x))


def train_ae(data_np, bottleneck_dim, epochs=EPOCHS):
    """训练 autoencoder，返回训练好的模型"""
    data_t = torch.tensor(data_np, dtype=torch.float32).to(DEVICE)
    n = len(data_np)
    
    model = NonlinearAE(FULL_DIM, bottleneck_dim).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs)
    criterion = nn.MSELoss()
    
    best_loss = float("inf")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        perm = torch.randperm(n)
        for i in range(0, n, BATCH_SIZE):
            idx = perm[i:i + BATCH_SIZE]
            batch = data_t[idx]
            optimizer.zero_grad()
            recon = model(batch)
            loss = criterion(recon, batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        scheduler.step()
        
        if total_loss < best_loss:
            best_loss = total_loss
    
    model.eval()
    return model


def fsq_quantize_torch(z, L):
    """FSQ 量化（Torch 版本）"""
    bound = (L - 1) / 2
    z_norm = torch.tanh(z) * bound
    z_quant = torch.round(z_norm)
    z_quant = torch.clamp(z_quant, -bound, bound)
    # Straight-through estimator: detach quantized, keep gradient on original
    z_ste = z_norm + (z_quant / bound - z_norm).detach()
    return z_ste


# ════════════════════════════════════════════════════
# 实验：多瓶颈维度 × FSQ 量化
# ════════════════════════════════════════════════════
BOTTLENECKS = [384, 256, 192, 128, 96, 64, 48, 32, 24, 16, 8]
FSQ_LEVELS = [3, 5, 7, 9, 15, 31]

all_results = {"random_gaussian": [], "semantic_intent": []}

for dataset_name, data_np in [("random_gaussian", data_random), ("semantic_intent", data_semantic)]:
    print(f"\n{'─' * 55}")
    print(f"数据集: {dataset_name} ({data_np.shape[0]} 样本)")
    print(f"{'─' * 55}")
    
    data_t = torch.tensor(data_np, dtype=torch.float32).to(DEVICE)
    
    for d_bn in BOTTLENECKS:
        d_bn = min(d_bn, data_np.shape[0] - 1, data_np.shape[1])
        if d_bn < 2:
            continue
        
        print(f"\n  瓶颈维度 d={d_bn}:")
        
        # 训练 autoencoder
        model = train_ae(data_np, d_bn)
        
        with torch.no_grad():
            z_full = model.encode(data_t)
            recon_full = model.decode(z_full)
            recon_full_np = recon_full.cpu().numpy()
            nr = np.linalg.norm(recon_full_np, axis=1, keepdims=True)
            nr[nr == 0] = 1
            recon_full_np /= nr
        
        fp32_cos = cos_sim_np(data_np, recon_full_np)
        fp32_bytes = d_bn * 4
        print(f"    FP32: cos={fp32_cos:.4f}, {fp32_bytes} bytes, {'✓达标' if fp32_cos >= TARGET_COS else '✗未达标'}")
        
        # FSQ 量化
        best_fsq = None
        z_mean = z_full.mean(dim=0, keepdim=True)
        z_std = z_full.std(dim=0, keepdim=True) + 1e-8
        z_norm = (z_full - z_mean) / z_std
        
        for L in FSQ_LEVELS:
            with torch.no_grad():
                z_q = fsq_quantize_torch(z_norm, L)
                z_r = z_q * z_std + z_mean
                recon = model.decode(z_r)
                recon_np = recon.cpu().numpy()
                nr = np.linalg.norm(recon_np, axis=1, keepdims=True)
                nr[nr == 0] = 1
                recon_np /= nr
            
            cs = cos_sim_np(data_np, recon_np)
            bpd = np.log2(L)
            tbytes = d_bn * bpd / 8
            ratio = fp32_bytes / tbytes if tbytes > 0 else 0
            ok = cs >= TARGET_COS
            
            print(f"    FSQ-{L:2d}: {bpd:.1f}bit/dim {tbytes:.1f}B cos={cs:.4f} {ratio:.1f}x {'✓' if ok else ''}")
            
            entry = {"d": d_bn, "L": L, "bits_per_dim": round(bpd, 1), "bytes": round(tbytes, 1),
                     "cos_sim": round(cs, 4), "fp32_cos": round(fp32_cos, 4), "compression_ratio": round(ratio, 1), "达标": ok}
            all_results[dataset_name].append(entry)
            
            if ok and (best_fsq is None or tbytes < best_fsq["bytes"]):
                best_fsq = {"d": d_bn, "L": L, "bytes": round(tbytes, 1), "cos_sim": round(cs, 4),
                           "ratio": round(ratio, 1), "fp32_cos": round(fp32_cos, 4)}
        
        if best_fsq:
            print(f"    ★ 最佳: d={best_fsq['d']} FSQ-{best_fsq['L']} {best_fsq['bytes']}B cos={best_fsq['cos_sim']:.4f}")

# ════════════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("汇总")
print("═" * 65)

for dataset_name in ["random_gaussian", "semantic_intent"]:
    results = all_results[dataset_name]
    # 找各瓶颈维度的最优 FSQ
    best_by_d = {}
    for r in results:
        d = r["d"]
        if r["达标"]:
            if d not in best_by_d or r["bytes"] < best_by_d[d]["bytes"]:
                best_by_d[d] = r
    
    print(f"\n{dataset_name}:")
    print(f"  {'d':>5s} {'最佳L':>6s} {'bytes':>7s} {'cos':>7s} {'dxlog2(L)':>10s}")
    print(f"  {'─' * 42}")
    
    dL_vals = []
    for d in sorted(best_by_d.keys()):
        r = best_by_d[d]
        dL = d * np.log2(r["L"])
        dL_vals.append(dL)
        print(f"  {d:5d} FSQ-{r['L']:<3d} {r['bytes']:7.1f} {r['cos_sim']:7.4f} {dL:10.1f}")
    
    if dL_vals:
        C_mean = np.mean(dL_vals)
        C_std = np.std(dL_vals)
        print(f"  C(d×log₂(L)) = {C_mean:.1f} ± {C_std:.1f}")
        print(f"  变异系数 CV = {C_std / C_mean:.3f}" if C_mean > 0 else "  无有效数据")

# 保存结果
result_path = os.path.join(RESULTS_DIR, f"{TIMESTAMP}_autoencoder_results.json")
with open(result_path, "w") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False, default=float)
print(f"\n📦 结果已保存: {result_path}")
print(f"⏰ 完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
