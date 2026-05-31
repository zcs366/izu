"""
语义反馈 V2：未知稀疏失真 → 反馈学习 → 针对性补偿

场景：
  发送方：PCA编码（全部768维可用）
  接收方：PCA编码，但随机盲化30%的PCs（模拟模型不对齐）
  发送方不知道哪些PCs被盲化
  
  无反馈：发送方必须用高维编码确保「大概率覆盖未被盲的PCs」
  语义反馈：接收方反馈解码结果 → 发送方推断盲化维度 → 二次精炼

核心判据：反馈后的总维度 < D_no_blind（无反馈时所需维度）
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95
NOISE_STD = 0.005
BLIND_FRAC = 0.30  # 接收方随机盲化30%的PCs

np.random.seed(42)
data = np.random.randn(N_SAMPLES, FULL_DIM)
data /= np.linalg.norm(data, axis=1, keepdims=True)

# 共享PCA
pca = PCA(n_components=FULL_DIM)
pca.fit(data)

def encode(x, d):
    return pca.transform(x)[:, :d]

def decode(c, d):
    r = c @ pca.components_[:d] + pca.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
    return r / nr

def cos_sim(x, y):
    return np.mean(np.sum(x*y, axis=1))

# ─── 接收方：随机盲化30%的PCs ─────────────────────
np.random.seed(123)
all_pcs = np.arange(FULL_DIM)
np.random.shuffle(all_pcs)
blind_pcs = set(all_pcs[:int(FULL_DIM * BLIND_FRAC)])
visible_pcs = sorted(set(range(FULL_DIM)) - blind_pcs)
print(f"接收方盲化: {len(blind_pcs)} PCs, 可见: {len(visible_pcs)}")

def receiver_decode(c, d):
    """接收方解码：盲化PC的系数被清零"""
    recon = np.zeros((len(c), FULL_DIM))
    sender_pc_idx = 0  # 发送方按0,1,2,...顺序编码PCs
    rcvr_pc_idx = 0     # 接收方只使用可见PCs
    
    for sender_j in range(d):
        if sender_pc_idx in visible_pcs:
            # 这个PC接收方能解码
            recon += np.outer(c[:, sender_j], pca.components_[sender_pc_idx])
            rcvr_pc_idx += 1
        # else: 盲化 → 系数丢失，跳过
        sender_pc_idx += 1
        if sender_pc_idx >= FULL_DIM:
            break
    
    recon += pca.mean_
    nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1
    return recon / nr

# ════════════════════════════════════════════════════
# A) 理想 D₀
# ════════════════════════════════════════════════════
lo, hi = 8, FULL_DIM; D0 = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, decode(encode(data,mid), mid)) >= TARGET_COS:
        D0 = mid; hi = mid-8
    else: lo = mid+8
print(f"\nD₀ = {D0}")

# ════════════════════════════════════════════════════
# B) 无反馈：发送方不知道哪些PC被盲 → 冗余编码
# ════════════════════════════════════════════════════
lo, hi = 8, FULL_DIM; D_blind = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    c = encode(data, mid) + np.random.randn(N_SAMPLES, mid)*NOISE_STD
    if cos_sim(data, receiver_decode(c, mid)) >= TARGET_COS:
        D_blind = mid; hi = mid-8
    else: lo = mid+8
print(f"D_blind (无反馈) = {D_blind} (+{D_blind-D0} vs D₀, 盲化开销)")

# ════════════════════════════════════════════════════
# C) 语义反馈：接收方反馈 → 发送方推断盲化维度 → 精炼
# ════════════════════════════════════════════════════
print(f"\n语义反馈实验:")
print(f"  {'d₁':>4s} {'d₂':>4s} {'总d':>5s} {'r':>3s} {'cos':>7s} {'vsD₀':>6s} {'vsDb':>6s}")

best_config = None

for d1 in [D0//2, D0//4, D0//8]:
    d1 = max(4, d1)
    
    # 第一轮：发送方编码（高维）
    c1 = encode(data, d1) + np.random.randn(N_SAMPLES, d1)*NOISE_STD
    r1 = receiver_decode(c1, d1)  # 接收方解码（有盲化）
    
    # 语义反馈：接收方发回解码结果
    # 发送方看到 r1，知道哪些维度被丢失了
    residual = data - r1
    
    # 发送方推断：残差中能量较大的方向=接收方盲化的PC方向
    # （在实际系统中，发送方会分析残差的PCA来推断盲化维度）
    # 简化：发送方直接编码残差
    for d2_ratio in [0.25, 0.5, 1.0]:
        d2 = max(4, int(d1 * d2_ratio))
        
        # 第二轮到第N轮：精炼残差
        recon = r1.copy()
        resid = residual.copy()
        rounds = 1  # 已经进行了一轮
        
        for extra in range(5):  # 最多额外5轮
            rounds += 1
            c = encode(resid, d2) + np.random.randn(N_SAMPLES, d2)*NOISE_STD
            piece = receiver_decode(c, d2)
            recon += piece
            nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1
            recon /= nr
            resid = data - recon
            
            if cos_sim(data, recon) >= TARGET_COS:
                break
        
        total_d = d1 + (rounds-1) * d2
        cs_v = cos_sim(data, recon)
        vs_d0 = total_d - D0
        vs_db = total_d - D_blind
        
        ok = cs_v >= TARGET_COS
        print(f"  {d1:4d} {d2:4d} {total_d:5d} {rounds:3d} {cs_v:7.4f} {vs_d0:+6d} {vs_db:+6d} {'✓' if ok else '✗'}")
        
        if ok and (best_config is None or total_d < best_config[2]):
            best_config = (d1, d2, total_d, rounds, cs_v)

# ════════════════════════════════════════════════════
print(f"\n{'═'*55}")
print(f"核心结论")
print(f"{'═'*55}")
print(f"  D₀       = {D0}  (理想情况)")
print(f"  D_blind  = {D_blind}  (无反馈，盲化开销 +{D_blind-D0})")
if best_config:
    d1,d2,td,rnd,cs = best_config
    print(f"  语义反馈  = d₁={d1} + {rnd-1}×d₂={d2} → {td}")
    print(f"  vs D₀:    {td-D0:+d} {'≤D₀ ★★★突破信息守恒！★★★' if td <= D0 else '>D₀'}")
    print(f"  vs 无反馈: {D_blind-td:+d} ({100*(1-td/D_blind):.0f}% 节省)")
else:
    print(f"  语义反馈: 无达标方案")
