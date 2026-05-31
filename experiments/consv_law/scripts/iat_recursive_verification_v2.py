"""
验证: 压缩维度 × 递归轮次 = 常数  (V2 — 大样本)

问题: 20个意图时有效秩≤19，d≥20即完美重建
修正: 256个多样意图 + 随机高斯噪声撑开高维结构

两层验证：
  A) 递进式 —— 每轮追加下一批PCs（基线）
  B) 残差重编码 —— 每轮对残差独立PCA（测试递归增益）
"""

import torch
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import json, random

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "answerdotai/ModernBERT-base"
FULL_DIM = 768
TARGET_COS_SIM = 0.95

# 生成256个多样意图
def generate_diverse_intents(n=256):
    verbs = ["分析","总结","设计","审查","优化","生成","翻译","搜索",
             "解释","对比","评估","预测","规划","调试","重构","部署",
             "监控","记录","归档","提取","转换","合并","分割","计算",
             "模拟","验证","校准","加密","解密","压缩","解压","索引"]
    domains = ["代码","数据","论文","报告","文档","日志","配置","数据库",
               "API","前端","后端","网络","安全","性能","内存","存储",
               "模型","算法","图表","测试","部署","运维","用户界面","消息队列"]
    objects = ["Python脚本","Rust程序","SQL查询","Docker镜像","配置文件",
               "日志文件","测试用例","API文档","用户手册","技术方案",
               "系统架构","数据管道","机器学习模型","神经网络","特征工程",
               "错误日志","性能报告","安全审计","代码审查","部署清单"]
    modifiers = ["高效地","自动地","批量地","增量地","安全地","并发地",
                 "异步地","实时地","离线地","分布地","并行地","串行地",
                 "精确地","近似地","保守地","激进地","优雅地","鲁棒地"]
    
    intents = []
    for i in range(n):
        patterns = [
            f"请{random.choice(verbs)}{random.choice(domains)}相关的{random.choice(objects)}",
            f"帮我{random.choice(verbs)}这个{random.choice(domains)}问题，用{random.choice(modifiers)}的方式",
            f"需要{random.choice(verbs)}一份关于{random.choice(domains)}的{random.choice(objects)}",
            f"用{random.choice(verbs)}的方法处理{random.choice(domains)}中的{random.choice(objects)}",
            f"{random.choice(modifiers)}{random.choice(verbs)}这个{random.choice(domains)}{random.choice(objects)}",
            f"针对{random.choice(domains)}领域，{random.choice(verbs)}一个{random.choice(objects)}",
        ]
        intents.append(random.choice(patterns))
    return intents

print(f"设备: {DEVICE}")
print(f"目标 cos_sim ≥ {TARGET_COS_SIM}")
print()

# ─── 生成意图并编码 ────────────────────────────────
print("生成256个多样意图...")
intents = generate_diverse_intents(256)

print("加载 ModernBERT-base...")
model = SentenceTransformer(MODEL_NAME, device=DEVICE)

print("编码...")
embeddings = model.encode(intents, normalize_embeddings=True)
n = len(embeddings)
print(f"Shape: {embeddings.shape}")

# 注入微量噪声以撑满高维结构（模拟真实场景中信息不完全落在低维流形）
np.random.seed(42)
noise = np.random.randn(n, FULL_DIM) * 0.001
embeddings = embeddings + noise
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings = embeddings / norms
print(f"+ 噪声 (σ=0.001) 注入完成\n")

# ─── 单轮基线：找出达标所需最小维度D₀ ─────────────
print("═" * 60)
print("单轮基线：寻找 D₀...")
print("═" * 60)

# 用全维度PCA（＞样本数的PCs方差为零，但允许访问高维索引）
pca_full = PCA(n_components=FULL_DIM)
pca_full.fit(embeddings)
effective_dim = min(n, FULL_DIM)  # 实际有效维度

def compress_decompress_single(x, pca, n_comp):
    compressed = pca.transform(x)[:, :n_comp]
    recon = np.zeros_like(x)
    for i in range(len(x)):
        for j in range(n_comp):
            recon[i] += compressed[i, j] * pca.components_[j]
    recon += pca.mean_
    norms_r = np.linalg.norm(recon, axis=1, keepdims=True)
    norms_r[norms_r == 0] = 1
    return compressed, recon / norms_r

D0 = None
for d in [384, 256, 192, 128, 96, 64, 48, 32, 24, 20, 16, 12, 8]:
    _, recon = compress_decompress_single(embeddings, pca_full, d)
    cos_sims = [np.dot(embeddings[i], recon[i]) for i in range(n)]
    avg_cos = np.mean(cos_sims)
    print(f"  d={d:3d} → cos={avg_cos:.4f}", end="")
    if avg_cos >= TARGET_COS_SIM:
        D0 = d
        print(f" ✓ D₀={D0}")
        break
    print()

if D0 is None:
    D0 = FULL_DIM
    print(f"  → 未达标，D₀={D0}")

print(f"\n单轮最小达标维度 D₀ = {D0}")

# ─── 多轮实验维度范围 ─────────────────────────────
DIMS_TO_TEST = []
d = D0
while d >= 8:
    DIMS_TO_TEST.append(d)
    d = d // 2
if 8 not in DIMS_TO_TEST:
    DIMS_TO_TEST.append(8)
DIMS_TO_TEST = sorted(DIMS_TO_TEST, reverse=True)
print(f"多轮测试维度: {DIMS_TO_TEST}\n")

# ════════════════════════════════════════════════════
# A) 递进式递归
# ════════════════════════════════════════════════════
print("═" * 60)
print("A) 递进式递归 (每轮追加 d 个PCs)")
print("═" * 60)

results_progressive = []

for d in DIMS_TO_TEST:
    x_current = embeddings.copy()
    x_recon = np.zeros_like(embeddings)
    rounds = 0
    pc_offset = 0
    
    while True:
        rounds += 1
        end_pc = min(pc_offset + d, pca_full.n_components_)
        
        if end_pc <= pc_offset:
            break
        
        # 用前end_pc个PCs重建
        _, recon_full = compress_decompress_single(x_current, pca_full, end_pc)
        
        if pc_offset > 0:
            _, recon_old = compress_decompress_single(x_current, pca_full, pc_offset)
            recon_delta = recon_full - recon_old
        else:
            recon_delta = recon_full
        
        x_recon += recon_delta
        norms_r = np.linalg.norm(x_recon, axis=1, keepdims=True)
        norms_r[norms_r == 0] = 1
        x_recon = x_recon / norms_r
        
        cos_sims = [np.dot(embeddings[i], x_recon[i]) for i in range(n)]
        avg_cos = np.mean(cos_sims)
        
        if avg_cos >= TARGET_COS_SIM:
            break
        
        pc_offset = end_pc
        x_current = embeddings - x_recon
        
        if pc_offset >= pca_full.n_components_:
            break
    
    total_dims = rounds * d
    cos_sims_final = [np.dot(embeddings[i], x_recon[i]) for i in range(n)]
    avg_cos_final = np.mean(cos_sims_final)
    
    results_progressive.append({
        'd': d, 'rounds': rounds, 'd_x_r': total_dims,
        'cos_sim': round(avg_cos_final, 4),
        'converged': avg_cos_final >= TARGET_COS_SIM
    })
    
    status = "✓" if results_progressive[-1]['converged'] else "✗"
    print(f"  d={d:3d} → {rounds:2d}轮 → d×r={total_dims:4d} | cos={avg_cos_final:.4f} {status}")

# ════════════════════════════════════════════════════
# B) 残差重编码
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print("B) 残差重编码 (每轮对残差独立PCA)")
print("═" * 60)

results_residual = []

for d in DIMS_TO_TEST:
    residual = embeddings.copy()
    x_recon = np.zeros_like(embeddings)
    rounds = 0
    
    while True:
        rounds += 1
        n_comp = min(d, n)
        pca_local = PCA(n_components=n_comp)
        pca_local.fit(residual)
        
        compressed = pca_local.transform(residual)
        recon_piece = pca_local.inverse_transform(compressed)
        
        x_recon += recon_piece
        norms_r = np.linalg.norm(x_recon, axis=1, keepdims=True)
        norms_r[norms_r == 0] = 1
        x_recon = x_recon / norms_r
        
        residual = embeddings - x_recon
        
        cos_sims = [np.dot(embeddings[i], x_recon[i]) for i in range(n)]
        avg_cos = np.mean(cos_sims)
        
        if avg_cos >= TARGET_COS_SIM:
            break
        if rounds >= 50:
            break
    
    total_dims = rounds * d
    cos_sims_final = [np.dot(embeddings[i], x_recon[i]) for i in range(n)]
    avg_cos_final = np.mean(cos_sims_final)
    
    results_residual.append({
        'd': d, 'rounds': rounds, 'd_x_r': total_dims,
        'cos_sim': round(avg_cos_final, 4),
        'converged': avg_cos_final >= TARGET_COS_SIM
    })
    
    status = "✓" if results_residual[-1]['converged'] else "✗"
    print(f"  d={d:3d} → {rounds:2d}轮 → d×r={total_dims:4d} | cos={avg_cos_final:.4f} {status}")

# ════════════════════════════════════════════════════
# 综合对比
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print(f"综合对比 (D₀={D0})")
print("═" * 60)
print(f"{'d':>4s} | {'递进轮次':>8s} {'递进d×r':>8s} | {'残差轮次':>8s} {'残差d×r':>8s} | {'ΔvsD₀':>6s} 备注")
print("-" * 75)

for i, d in enumerate(DIMS_TO_TEST):
    rp = results_progressive[i]
    rr = results_residual[i]
    diff_prog = rp['d_x_r'] - D0
    diff_res = rr['d_x_r'] - D0
    
    prog_note = ""
    res_note = ""
    if diff_prog == 0: prog_note = "=D₀"
    elif diff_prog < 0: prog_note = f"<D₀({abs(diff_prog)})!"
    else: prog_note = f"+{diff_prog}"
    
    if diff_res == 0: res_note = "=D₀"
    elif diff_res < 0: res_note = f"<D₀({abs(diff_res)})!"
    else: res_note = f"+{diff_res}"
    
    print(f"{d:4d} | {rp['rounds']:8d} {rp['d_x_r']:8d} | {rr['rounds']:8d} {rr['d_x_r']:8d} | {diff_prog:+5d} 递进:{prog_note} 残差:{res_note}")

# ─── 常数C ────────────────────────────────────────
print()
print("═" * 60)
print("常数C估计")
print("═" * 60)

for label, results in [("递进式", results_progressive), ("残差重编码", results_residual)]:
    converged = [r for r in results if r['converged']]
    if converged:
        c_vals = [r['d_x_r'] for r in converged]
        mean_c = np.mean(c_vals)
        std_c = np.std(c_vals)
        print(f"  {label}: C = {mean_c:.1f} ± {std_c:.1f} (值: {c_vals})")
        print(f"          相对D₀偏差: {(mean_c - D0):+.1f} ({(mean_c/D0 - 1)*100:+.1f}%)")

print()
print("─" * 60)
print("结论判据:")
print(f"  1. d×r 在不同 d 下是否稳定 (低方差) → 公式近似成立")
print(f"  2. 残差重编码的 d×r 是否 ≤ 递进式     → 递归反馈有净增益")
print(f"  3. d×r 平均值是否接近 D₀={D0}       → 常数=单轮下限")
