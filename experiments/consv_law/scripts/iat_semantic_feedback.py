"""
语义反馈实验：非对称编解码 → 测试 d×r < D₀ 是否可能

核心设计：
  发送方使用 PCA（最优线性压缩）
  接收方使用 RANDOM PROJECTION（次优，制造可控失真）
  双方共享随机投影矩阵
  
  无反馈：发送方需冗余编码对抗接收方差解码 → D_noisy > D₀
  有反馈：接收方发回解码结果 → 发送方只需精炼误差 → 总维度应更少

  关键测试：d₁(首轮) + d₂(精炼) < D₀？  （不是 < D_noisy，而是 < D₀！）
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95
NOISE_STD = 0.01

np.random.seed(42)
data = np.random.randn(N_SAMPLES, FULL_DIM)
data /= np.linalg.norm(data, axis=1, keepdims=True)

# ─── 发送方：PCA ──────────────────────────────────
pca_sender = PCA(n_components=FULL_DIM)
pca_sender.fit(data)

# ─── 接收方：随机投影矩阵 ─────────────────────────
np.random.seed(99)
R = np.random.randn(FULL_DIM, FULL_DIM) * 0.3  # 失真矩阵
# 接收方的"解码"= 直接逆投影（伪逆）+ R的扰动
# 简化：receiver_decode(c) = pca_decode(c) + R @ pca_decode(c) 的一部分
# 即：接收方看到的是发送方意图经过 R 扭曲后的版本

def sender_encode(x, d):
    return pca_sender.transform(x)[:, :d]

def sender_decode(c, d):
    r = c @ pca_sender.components_[:d] + pca_sender.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
    return r / nr

def receiver_decode(c, d):
    """接收方解码：PCA解码 + 随机扰动"""
    # 先正常PCA解码
    clean = sender_decode(c, d)
    # 加随机扰动（模拟模型不对齐）
    perturbed = clean + (clean @ R) * 0.15  # 15%的失真
    nr = np.linalg.norm(perturbed, axis=1, keepdims=True); nr[nr==0]=1
    return perturbed / nr

def cos_sim(x, y):
    return np.mean(np.sum(x * y, axis=1))

# ════════════════════════════════════════════════════
# A) 发送方自闭环 D₀（发送方用自己的解码器）
# ════════════════════════════════════════════════════
print("A) 发送方自闭环 D₀（理想情况）")
lo, hi = 8, FULL_DIM; D0 = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, sender_decode(sender_encode(data, mid), mid)) >= TARGET_COS:
        D0 = mid; hi = mid-8
    else: lo = mid+8
print(f"  D₀ = {D0}")

# ════════════════════════════════════════════════════
# B) 无反馈：发送→接收方差解码（单轮）
# ════════════════════════════════════════════════════
print(f"\nB) 无反馈：发送方编码 → 接收方差解码（单轮）")
def receiver_single_ok(d):
    c = sender_encode(data, d) + np.random.randn(N_SAMPLES, d)*NOISE_STD
    r = receiver_decode(c, d)
    return cos_sim(data, r) >= TARGET_COS

lo, hi = 8, FULL_DIM; D_noisy_r = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if receiver_single_ok(mid): D_noisy_r = mid; hi = mid-8
    else: lo = mid+8
print(f"  D_noisy_receiver = {D_noisy_r} (vs D₀={D0}, +{D_noisy_r-D0})")

# ════════════════════════════════════════════════════
# C) 语义反馈：接收方发回解码→发送方精炼误差
# ════════════════════════════════════════════════════
print(f"\nC) 语义反馈（接收方发回解码 → 发送方精炼残差）")

def semantic_feedback(x, d_per, max_r=30):
    """每轮：发送→接收方差解码→反馈→发送方编码残差"""
    recon = np.zeros_like(x)
    resid = x.copy()
    
    for rnd in range(max_r):
        # 发送方编码残差
        c = sender_encode(resid, d_per) + np.random.randn(len(x), d_per)*NOISE_STD
        # 接收方差解码
        piece = receiver_decode(c, d_per)
        recon += piece
        nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1
        recon /= nr
        
        # 语义反馈：发送方知道接收方解码结果，计算精确残差
        resid = x - recon  # 真正的语义差距
        
        if cos_sim(x, recon) >= TARGET_COS:
            return recon, rnd+1, True
    return recon, max_r, False

# 二分搜最优 d
best_total = 9999
best_config = None

for d in [D0//2, D0//4, D0//8, D0//16, D0//32, D0//64]:
    d = max(4, d)
    _, rnd, ok = semantic_feedback(data, d)
    total = rnd * d
    cs_v = cos_sim(data, semantic_feedback(data, d)[0])
    print(f"  d={d:4d} r={rnd:2d} d×r={total:5d} cos={cs_v:.4f} {'✓' if ok else '✗'} vsD₀={total-D0:+5d} vsDn={total-D_noisy_r:+5d}")
    if ok and total < best_total:
        best_total = total
        best_config = (d, rnd)

# 细搜
if best_config:
    print(f"\n  细搜最优d...")
    d_opt, _ = best_config
    for d in range(max(4, d_opt//2), min(D0, d_opt*2), 4):
        _, rnd, ok = semantic_feedback(data, d)
        if ok and rnd*d < best_total:
            best_total = rnd*d
            best_config = (d, rnd)

# ════════════════════════════════════════════════════
# 核心对比
# ════════════════════════════════════════════════════
print(f"\n{'═'*60}")
print(f"核心对比")
print(f"{'═'*60}")
print(f"  D₀ (理想自闭环)        = {D0}")
print(f"  D_noisy_receiver (无反馈) = {D_noisy_r}")

if best_config:
    d, r = best_config
    print(f"  语义反馈最佳: d={d}, r={r}, d×r={best_total}")
    print(f"    节省 vs 无反馈: {D_noisy_r - best_total} dims")
    print(f"    vs D₀:           {best_total - D0:+d} ", end="")
    if best_total <= D0:
        print("≤ D₀ ✓★★★ 突破信息守恒！★★★")
    elif best_total < D_noisy_r:
        print("< D_noisy (优于无反馈，未突破 D₀)")
    else:
        print("≥ D_noisy (无优势)")
else:
    print(f"  语义反馈: 无达标方案")
