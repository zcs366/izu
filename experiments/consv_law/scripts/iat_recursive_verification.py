"""
验证: 压缩维度 × 递归轮次 = 常数

两层验证：
  A) 递进式 —— 每轮追加下一批PCs（平凡情况，作为基线）
  B) 残差重编码 —— 每轮对残差重新PCA编码（非平凡，测试递归压缩增益）

目标：给定保真度阈值 τ，单轮所需维度 D₀ 应约等于 d×r。
"""

import torch
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import json

# ─── 配置 ──────────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "answerdotai/ModernBERT-base"
FULL_DIM = 768
TARGET_COS_SIM = 0.95
NN_ACCURACY_TARGET = 0.90
DIMS_TO_TEST = [384, 256, 192, 128, 96, 64, 48, 32, 24, 16, 12, 8]

# ─── 20个意图 ──────────────────────────────────────
INTENTS = [
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

print(f"设备: {DEVICE}")
print(f"目标 cos_sim ≥ {TARGET_COS_SIM}")
print(f"目标 NN准确率 ≥ {NN_ACCURACY_TARGET}")
print()

# ─── 加载模型 ──────────────────────────────────────
print("加载 ModernBERT-base...")
model = SentenceTransformer(MODEL_NAME, device=DEVICE)
print("✓ 模型加载完成\n")

# ─── 编码意图 ──────────────────────────────────────
print(f"编码 {len(INTENTS)} 个意图...")
embeddings = model.encode(INTENTS, normalize_embeddings=True)
embeddings_tensor = torch.tensor(embeddings, device=DEVICE)
n = len(INTENTS)
print(f"Shape: {embeddings.shape}\n")

# ─── 全局PCA ──────────────────────────────────────
print("计算全局PCA (所有20个意图)...")
pca_full = PCA(n_components=min(FULL_DIM, n))
pca_full.fit(embeddings)
print(f"✓ {pca_full.n_components_} 个主成分\n")

# ─── 辅助函数 ──────────────────────────────────────
def compress_decompress(x, pca, n_components):
    """用PCA压缩到n_components维并解压回原始空间"""
    compressed = pca.transform(x)[:, :n_components]
    reconstructed = np.zeros_like(x)
    for i in range(len(x)):
        for j in range(n_components):
            reconstructed[i] += compressed[i, j] * pca.components_[j]
    reconstructed += pca.mean_
    # 归一化
    norms = np.linalg.norm(reconstructed, axis=1, keepdims=True)
    norms[norms == 0] = 1
    reconstructed = reconstructed / norms
    return compressed, reconstructed

def evaluate_fidelity(original, reconstructed):
    """计算保真度指标"""
    cos_sims = []
    for i in range(len(original)):
        sim = np.dot(original[i], reconstructed[i])
        cos_sims.append(sim)
    avg_cos = np.mean(cos_sims)
    
    # NN准确率
    correct = 0
    for i in range(len(original)):
        sims = np.dot(reconstructed[i:i+1], original.T)[0]
        if np.argmax(sims) == i:
            correct += 1
    nn_acc = correct / len(original)
    
    return avg_cos, nn_acc, cos_sims

# ════════════════════════════════════════════════════
# A) 递进式递归 (平凡情况：每轮追加下一批PCs)
# ════════════════════════════════════════════════════
print("═" * 60)
print("A) 递进式递归 (每轮追加 d 个PCs)")
print("═" * 60)

results_progressive = []

for d in DIMS_TO_TEST:
    x_current = embeddings.copy()
    x_reconstructed = np.zeros_like(embeddings)
    rounds = 0
    pc_offset = 0
    
    while True:
        rounds += 1
        # 取下一批 d 个PCs
        end_pc = min(pc_offset + d, pca_full.n_components_)
        actual_d = end_pc - pc_offset
        
        if actual_d == 0:
            break
        
        # 用这批PCs压缩残差
        compressed, recon_piece = compress_decompress(
            x_current, pca_full, end_pc
        )
        # 修正：只取新增PCs的贡献
        # 用前end_pc个PCs重建，减去前pc_offset个PCs的贡献
        recon_full = recon_piece  # 这是用前end_pc个PCs重建的
        
        if pc_offset > 0:
            _, recon_old = compress_decompress(x_current, pca_full, pc_offset)
            recon_delta = recon_full - recon_old
        else:
            recon_delta = recon_full
        
        x_reconstructed += recon_delta
        # 归一化
        norms_r = np.linalg.norm(x_reconstructed, axis=1, keepdims=True)
        norms_r[norms_r == 0] = 1
        x_reconstructed = x_reconstructed / norms_r
        
        x_current = embeddings - x_reconstructed
        
        avg_cos, nn_acc, _ = evaluate_fidelity(embeddings, x_reconstructed)
        
        # 检查是否达标
        if avg_cos >= TARGET_COS_SIM and nn_acc >= NN_ACCURACY_TARGET:
            break
        
        pc_offset = end_pc
        
        if pc_offset >= pca_full.n_components_:
            break
    
    total_dims = rounds * d
    avg_cos_final, nn_acc_final, _ = evaluate_fidelity(embeddings, x_reconstructed)
    
    results_progressive.append({
        'd': d,
        'rounds': rounds,
        'd_x_r': total_dims,
        'cos_sim': round(avg_cos_final, 4),
        'nn_acc': round(nn_acc_final, 4),
        'converged': avg_cos_final >= TARGET_COS_SIM and nn_acc_final >= NN_ACCURACY_TARGET
    })
    
    status = "✓ 达标" if results_progressive[-1]['converged'] else "✗ 未达标"
    print(f"  d={d:3d} → {rounds}轮 → d×r={total_dims:4d} | cos={avg_cos_final:.4f} nn={nn_acc_final:.4f} {status}")

# ════════════════════════════════════════════════════
# B) 残差重编码 (非平凡：每轮对残差独立PCA)
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print("B) 残差重编码 (每轮对残差独立PCA)")
print("═" * 60)

results_residual = []

for d in DIMS_TO_TEST:
    residual = embeddings.copy()
    x_reconstructed = np.zeros_like(embeddings)
    rounds = 0
    
    while True:
        rounds += 1
        
        # 对当前残差做PCA
        n_comp = min(d, n, residual.shape[1])
        pca_local = PCA(n_components=n_comp)
        pca_local.fit(residual)
        
        compressed = pca_local.transform(residual)
        recon_piece = pca_local.inverse_transform(compressed)
        
        x_reconstructed += recon_piece
        # 归一化
        norms_r = np.linalg.norm(x_reconstructed, axis=1, keepdims=True)
        norms_r[norms_r == 0] = 1
        x_reconstructed = x_reconstructed / norms_r
        
        residual = embeddings - x_reconstructed
        
        avg_cos, nn_acc, _ = evaluate_fidelity(embeddings, x_reconstructed)
        
        if avg_cos >= TARGET_COS_SIM and nn_acc >= NN_ACCURACY_TARGET:
            break
        
        # 防止无限循环
        if rounds >= 20:
            break
    
    total_dims = rounds * d
    avg_cos_final, nn_acc_final, _ = evaluate_fidelity(embeddings, x_reconstructed)
    
    results_residual.append({
        'd': d,
        'rounds': rounds,
        'd_x_r': total_dims,
        'cos_sim': round(avg_cos_final, 4),
        'nn_acc': round(nn_acc_final, 4),
        'converged': avg_cos_final >= TARGET_COS_SIM and nn_acc_final >= NN_ACCURACY_TARGET
    })
    
    status = "✓ 达标" if results_residual[-1]['converged'] else "✗ 未达标"
    print(f"  d={d:3d} → {rounds:2d}轮 → d×r={total_dims:4d} | cos={avg_cos_final:.4f} nn={nn_acc_final:.4f} {status}")

# ════════════════════════════════════════════════════
# 综合对比
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print("综合对比")
print("═" * 60)
print(f"{'d':>4s} | {'递进轮次':>8s} {'递进d×r':>8s} | {'残差轮次':>8s} {'残差d×r':>8s} | {'差值':>6s}")
print("-" * 60)

for i, d in enumerate(DIMS_TO_TEST):
    rp = results_progressive[i]
    rr = results_residual[i]
    diff = rr['d_x_r'] - rp['d_x_r']
    marker = ""
    if diff < 0:
        marker = " ← 残差更优!"
    elif diff > 0:
        marker = " (残差更差)"
    print(f"{d:4d} | {rp['rounds']:8d} {rp['d_x_r']:8d} | {rr['rounds']:8d} {rr['d_x_r']:8d} | {diff:+5d}{marker}")

# ─── 求常数C ──────────────────────────────────────
print()
print("═" * 60)
print("常数C估计 (d × r 达标时的平均值)")
print("═" * 60)

for label, results in [("递进式", results_progressive), ("残差重编码", results_residual)]:
    converged = [r for r in results if r['converged']]
    if converged:
        c_values = [r['d_x_r'] for r in converged]
        c_mean = np.mean(c_values)
        c_std = np.std(c_values)
        print(f"  {label}: C = {c_mean:.1f} ± {c_std:.1f} (N={len(converged)}, 值: {c_values})")
    else:
        print(f"  {label}: 无达标配置")

print()
print("结论:")
print("  若 d×r 在两种方案下均收敛到接近的常数 → 公式成立")
print("  若残差重编码的 d×r 显著更小 → 递归反馈有净增益")
