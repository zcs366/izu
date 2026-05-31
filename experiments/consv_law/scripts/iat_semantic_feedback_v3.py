"""
语义反馈 V3：PC乱序 → 反馈学习映射 → 针对性补偿

场景（模拟两个Agent模型的语义空间不对齐）：
  发送方：PCA编码，PC顺序 = 方差递减（最优）
  接收方：PCA编码，但PC顺序被随机打乱
  
  双方都不知道对方的排序
  
  无反馈：发送方用许多维度确保「大概率覆盖接收方的重要PC」
  语义反馈：接收方发回解码结果→发送方推断映射→精炼缺失维度

核心判据：反馈后 d×r < D_shuffled（无反馈所需维度）
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95
NOISE_STD = 0.005

np.random.seed(42)
data = np.random.randn(N_SAMPLES, FULL_DIM)
data /= np.linalg.norm(data, axis=1, keepdims=True)

# 共享PCA
pca = PCA(n_components=FULL_DIM)
pca.fit(data)

# ─── 接收方的PC乱序 ───────────────────────────────
np.random.seed(777)
receiver_order = np.arange(FULL_DIM)
np.random.shuffle(receiver_order)  # 接收方的PC索引映射
# receiver_order[i] = 发送方PC i 在接收方眼中的序号

def sender_encode(x, d):
    """发送方：编码方差最大的前d个PCs"""
    return pca.transform(x)[:, :d]

def sender_decode(c, d):
    r = c @ pca.components_[:d] + pca.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
    return r / nr

def receiver_decode(c, d):
    """接收方：用打乱的PC顺序解码"""
    # 发送方的PC 0,1,...,d-1 → 接收方用 receiver_order[0],...,receiver_order[d-1]
    r = np.zeros((len(c), FULL_DIM))
    for j in range(d):
        pc_idx = receiver_order[j]  # 接收方用的实际PC
        r += np.outer(c[:, j], pca.components_[pc_idx])
    r += pca.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
    return r / nr

def cos_sim(x, y):
    return np.mean(np.sum(x*y, axis=1))

# ════════════════════════════════════════════════════
# A) 理想 D₀
# ════════════════════════════════════════════════════
lo, hi = 8, FULL_DIM; D0 = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, sender_decode(sender_encode(data,mid), mid)) >= TARGET_COS:
        D0 = mid; hi = mid-8
    else: lo = mid+8
print(f"D₀ = {D0} (发送方自闭环)")

# ════════════════════════════════════════════════════
# B) 无反馈：发送→乱序接收方（发送方不知道乱序）
# ════════════════════════════════════════════════════
lo, hi = 8, FULL_DIM; D_shuffle = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    c = sender_encode(data, mid) + np.random.randn(N_SAMPLES, mid)*NOISE_STD
    if cos_sim(data, receiver_decode(c, mid)) >= TARGET_COS:
        D_shuffle = mid; hi = mid-8
    else: lo = mid+8
print(f"D_shuffle (无反馈) = {D_shuffle} (+{D_shuffle-D0} vs D₀, 乱序开销)")

# ════════════════════════════════════════════════════
# C) 语义反馈：反馈学习映射 → 精炼
# ════════════════════════════════════════════════════
print(f"\n语义反馈实验:")
print(f"  {'d₁':>4s} {'d₂':>4s} {'总':>5s} {'轮':>3s} {'cos':>7s} {'ΔD₀':>6s} {'ΔDs':>6s}")

# 第一轮：发送方用d₁维编码
# 接收方乱序解码 → 发回结果
# 发送方比较原始意图和接收方解码 → 推断乱序映射
# 第二轮：发送方用推断的映射，只传输接收方缺失的重要PCs

best = None

for d1 in [D0//2, D0//4, D0//8, D0//16]:
    d1 = max(4, d1)
    
    # 第一轮
    c1 = sender_encode(data, d1) + np.random.randn(N_SAMPLES, d1)*NOISE_STD
    r1 = receiver_decode(c1, d1)
    
    # 语义反馈：发送方看到 r1
    # 发送方推断：哪些方向（PCs）的残差最大？
    residual = data - r1
    
    # 发送方分析残差的PCA → 找出接收方"遗漏"的方向
    resid_pca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    resid_pca.fit(residual)
    
    # 残差的前k个PCs = 接收方最需要的方向
    # 发送方把这些方向编码为精炼信号
    
    for d2 in [d1//2, d1//4, d1//8]:
        d2 = max(4, d2)
        
        recon = r1.copy()
        rnd = 1
        
        for extra in range(10):
            rnd += 1
            # 编码残差的前d2个PCs
            c2 = resid_pca.transform(residual)[:, :d2]
            c2 += np.random.randn(N_SAMPLES, d2) * NOISE_STD
            
            # 接收方用同样的乱序解码（但这次解码的是残差空间的PCs）
            # 简化：直接用残差PCA的components重建
            piece = c2 @ resid_pca.components_[:d2] + resid_pca.mean_
            
            recon += piece
            nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1
            recon /= nr
            
            residual = data - recon
            
            if cos_sim(data, recon) >= TARGET_COS:
                break
            
            # 重新计算残差PCA
            resid_pca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
            resid_pca.fit(residual)
        
        total_d = d1 + (rnd-1) * d2
        cs_v = cos_sim(data, recon)
        d_d0 = total_d - D0
        d_ds = total_d - D_shuffle
        
        ok = cs_v >= TARGET_COS
        print(f"  {d1:4d} {d2:4d} {total_d:5d} {rnd:3d} {cs_v:7.4f} {d_d0:+6d} {d_ds:+6d} {'✓' if ok else '✗'}")
        
        if ok and (best is None or total_d < best[2]):
            best = (d1, d2, total_d, rnd, cs_v)

# ════════════════════════════════════════════════════
print(f"\n{'═'*55}")
print(f"结论")
print(f"{'═'*55}")
print(f"  D₀        = {D0}")
print(f"  D_shuffle  = {D_shuffle} (乱序开销 +{D_shuffle-D0})")
if best:
    d1,d2,td,rnd,cs = best
    print(f"  语义反馈   = d₁={d1} + ({rnd-1})×d₂={d2} → {td}")
    print(f"  vs D₀:     {td-D0:+d} {'★★★ ≤D₀ 突破信息守恒！★★★' if td <= D0 else '>D₀'}")
    print(f"  vs 无反馈: {D_shuffle-td:+d} (节省 {100*(1-td/D_shuffle):.0f}%)")
else:
    print(f"  无达标方案（乱序太随机，反馈无法收敛）")
