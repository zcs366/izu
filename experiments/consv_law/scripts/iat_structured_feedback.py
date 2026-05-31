"""
语义反馈突破 V4：精确构造的结构化不对齐

发送方：完整PCA（768 PCs）
接收方：PCs 0-49 完全共享，PCs 50-99 被旋转矩阵R扭曲，PCs 100+ 也共享

数据：2000样本，方差集中在50个信号PC（正好对应共享区域）

场景：
  D₀ ≈ 50（信号PC数）
  接收方前50PC完美对齐 → d₁=50 就接收方自闭环达标
  但接收方PCs 50-99 旋转了 → 发送方用d₁=50传过去，接收方解码有偏差
  反馈：发送方发现残差集中在50-99区域 → d₂=50 精炼 → total=100
  无反馈：发送方需要更多维度覆盖整个旋转区域 → D_mis > D₀

核心判据：反馈 total = d₁+d₂，能否 < D_mis？能否 ≤ D₀？
  正常情况下 d₁+d₂ = 50+50 = 100 > D₀=50
  但如果反馈让发送方"聪明地"重传——只传旋转导致的误差方向(非全部50PC)
  → d₂ < 50 → total < 100，甚至可能 < D₀ ？？
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
SHARED_PCS = 20      # PC0-19 完全共享
ROTATED_PCS = 50     # PC20-69 被旋转（在D₀≈48的临界区内！）
ROT_START = SHARED_PCS
TARGET_COS = 0.95

np.random.seed(42)

# ─── 数据：方差集中在前50个PC ────────────────────
# 生成50个强信号方向
signal_basis = np.linalg.qr(np.random.randn(FULL_DIM, SHARED_PCS + ROTATED_PCS))[0].T
coeffs = np.random.randn(N_SAMPLES, SHARED_PCS + ROTATED_PCS) * 5.0
noise = np.random.randn(N_SAMPLES, FULL_DIM) * 0.2
data = coeffs @ signal_basis + noise
data /= np.linalg.norm(data, axis=1, keepdims=True)

# ─── 发送方PCA ───────────────────────────────────
pca_s = PCA(n_components=FULL_DIM)
pca_s.fit(data)

# ─── 接收方PCA：前50共享，50-99旋转 ──────────────
R = np.linalg.qr(np.random.randn(ROTATED_PCS, ROTATED_PCS))[0]  # 随机旋转矩阵
pca_r_comps = pca_s.components_.copy()  # (768, 768)
pca_r_comps[ROT_START:ROT_START+ROTATED_PCS] = R @ pca_r_comps[ROT_START:ROT_START+ROTATED_PCS]

# 验证重叠
ol_shared = abs(np.dot(pca_s.components_[0], pca_r_comps[0]))
ol_rot = abs(np.dot(pca_s.components_[ROT_START], pca_r_comps[ROT_START]))
ol_after = abs(np.dot(pca_s.components_[ROT_START+ROTATED_PCS], pca_r_comps[ROT_START+ROTATED_PCS]))
print(f"PC对齐: PC0(共享)={ol_shared:.4f}, PC{ROT_START}(旋转)={ol_rot:.4f}, PC{ROT_START+ROTATED_PCS}(后)={ol_after:.4f}")

def encode(x): return pca_s.transform(x)
def decode_s(c, d):
    r = c[:,:d] @ pca_s.components_[:d] + pca_s.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1; return r/nr
def decode_r(c, d):
    r = c[:,:d] @ pca_r_comps[:d] + pca_s.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1; return r/nr
def cos_sim(x,y): return np.mean(np.sum(x*y, axis=1))

# ════════════════════════════════════════════════════
# 基线
# ════════════════════════════════════════════════════
c_full = encode(data)

# D₀：接收方自闭环（用自己的旋转PCA）
lo, hi = 8, FULL_DIM; D0_r = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, decode_r(c_full, mid)) >= TARGET_COS:
        D0_r = mid; hi = mid-8
    else: lo = mid+8
print(f"D₀(接收方自闭环) = {D0_r}")

# D₀：发送方自闭环  
lo, hi = 8, FULL_DIM; D0_s = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, decode_s(c_full, mid)) >= TARGET_COS:
        D0_s = mid; hi = mid-8
    else: lo = mid+8
print(f"D₀(发送方自闭环) = {D0_s}")

# D_mis：发送编码→接收解码（无反馈）
lo, hi = 8, FULL_DIM; D_mis = FULL_DIM
while lo <= hi:
    mid = ((lo+hi)//2//8)*8; mid = max(8,mid)
    if cos_sim(data, decode_r(c_full, mid)) >= TARGET_COS:
        D_mis = mid; hi = mid-8
    else: lo = mid+8
print(f"D_misalign = {D_mis} (+{D_mis-D0_s} vs 发送D₀)")

# ════════════════════════════════════════════════════
# 语义反馈
# ════════════════════════════════════════════════════
print(f"\n{'='*55}")
print(f"语义反馈（旋转区已知/自适应）")
print(f"{'='*55}")

# 策略：第1轮传d₁维 → 反馈 → 分析残差 → 第2轮只传残差主方向
# 关键：残差集中在旋转区 → d₂ 可以远小于 d₁

best = None

for d1 in [SHARED_PCS, SHARED_PCS + ROTATED_PCS//2, SHARED_PCS + ROTATED_PCS, D0_r]:
    d1 = max(8, min(d1, FULL_DIM))
    
    # 第1轮
    r1 = decode_r(c_full, d1)
    resid = data - r1
    
    # 残差PCA
    rpca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    rpca.fit(resid)
    
    # 残差方差分析：前k个PC覆盖多少方差？
    cumvar = np.cumsum(rpca.explained_variance_ratio_)
    
    for cov_target in [0.5, 0.7, 0.85, 0.9, 0.95]:
        d2 = int(np.searchsorted(cumvar, cov_target) + 1)
        d2 = max(2, min(d2, FULL_DIM//4))
        
        rc = rpca.transform(resid)
        piece = rc[:,:d2] @ rpca.components_[:d2] + rpca.mean_
        recon = r1 + piece
        nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1; recon/=nr
        cs = cos_sim(data, recon)
        total = d1 + d2
        
        if cs >= TARGET_COS:
            vs = total - D0_s
            marker = "★★★ ≤D₀！！" if total <= D0_s else ("< D_mis" if total < D_mis else "")
            print(f"  d₁={d1:4d} d₂={d2:3d}(cov{cov_target:.0%}) total={total:5d} cos={cs:.4f} vsD₀={vs:+5d} {marker}")
            if best is None or total < best['total']:
                best = {'d1': d1, 'd2': d2, 'total': total, 'cos': cs, 'vsD0': vs}

# ─── 细搜最优d₂ ──────────────────────────────────
if best:
    d1 = best['d1']
    r1 = decode_r(c_full, d1)
    resid = data - r1
    rpca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    rpca.fit(resid)
    
    for d2 in range(2, min(100, D0_s), 2):
        rc = rpca.transform(resid)
        piece = rc[:,:d2] @ rpca.components_[:d2] + rpca.mean_
        recon = r1 + piece
        nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr==0]=1; recon/=nr
        cs = cos_sim(data, recon)
        total = d1 + d2
        if cs >= TARGET_COS and total < best['total']:
            best = {'d1': d1, 'd2': d2, 'total': total, 'cos': cs, 'vsD0': total-D0_s}

# ════════════════════════════════════════════════════
print(f"\n{'='*55}")
print(f"结论")
print(f"{'='*55}")
print(f"  D₀(发送自闭环)  = {D0_s}")
print(f"  D₀(接收自闭环)  = {D0_r}")
print(f"  D_misalign       = {D_mis}")
if best:
    print(f"  语义反馈: d₁={best['d1']} + d₂={best['d2']} = {best['total']}")
    print(f"  vs D₀(发送): {best['vsD0']:+d}", end="")
    if best['total'] <= D0_s:
        print(" ★★★ 突破信息守恒！★★★")
    elif best['total'] < D_mis:
        print(f" < D_misalign")
    print(f"  cos = {best['cos']:.4f}")
    print(f"\n  解读: 第1轮传{best['d1']}维 → 接收方解码有偏差(旋转区)")
    print(f"        反馈定位 → 第2轮只传{best['d2']}维残差主方向 → 达标")
    print(f"        总成本 {best['total']} vs 发送D₀={D0_s}")
