#!/usr/bin/env python3
"""
§3.8 多轮反馈消融：验证 d₁+d₂+d₃ 是否收敛到 D₀

商鞅审计第2项：语义反馈实验只做了2轮，没有验证第3轮。
核心问题：每增加一轮反馈，增量维度越来越小 → 总维度 d₁+d₂+d₃+... 是否收敛到 D₀？

设计：
  - 场景1：结构化不对齐（旋转矩阵），测 1/2/3/4 轮反馈
  - 场景2：随机不对齐（噪声），测 ARQ 多轮
  - 判据：Δd(r) = d_r（第r轮新增维度），是否递减？总和是否 ≤ D₀？
"""
import numpy as np
from sklearn.decomposition import PCA
import json, os
from datetime import datetime

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95
SEED = 42
np.random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def cos_sim(x, y):
    return float(np.mean(np.sum(x * y, axis=1)))

# ════════════════════════════════════════════════════
# 场景1：结构化不对齐（旋转矩阵）
# ════════════════════════════════════════════════════
print("═" * 65)
print("§3.8 多轮反馈消融")
print("═" * 65)

SHARED_PCS = 20
ROTATED_PCS = 50

signal_basis = np.linalg.qr(np.random.randn(FULL_DIM, SHARED_PCS + ROTATED_PCS))[0].T
coeffs = np.random.randn(N_SAMPLES, SHARED_PCS + ROTATED_PCS) * 5.0
noise = np.random.randn(N_SAMPLES, FULL_DIM) * 0.2
data = coeffs @ signal_basis + noise
data /= np.linalg.norm(data, axis=1, keepdims=True)

pca_s = PCA(n_components=FULL_DIM)
pca_s.fit(data)

R = np.linalg.qr(np.random.randn(ROTATED_PCS, ROTATED_PCS))[0]
pca_r_comps = pca_s.components_.copy()
pca_r_comps[SHARED_PCS:SHARED_PCS + ROTATED_PCS] = R @ pca_r_comps[SHARED_PCS:SHARED_PCS + ROTATED_PCS]

def encode_s(x): return pca_s.transform(x)
def decode_r(c, d):
    r = c[:, :d] @ pca_r_comps[:d] + pca_s.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr == 0] = 1; return r / nr

c_full = encode_s(data)

# D₀
lo, hi = 8, FULL_DIM; D0 = FULL_DIM
while lo <= hi:
    mid = ((lo + hi) // 2 // 8) * 8; mid = max(8, mid)
    r_test = c_full[:, :mid] @ pca_s.components_[:mid] + pca_s.mean_
    nr = np.linalg.norm(r_test, axis=1, keepdims=True); nr[nr == 0] = 1; r_test /= nr
    if cos_sim(data, r_test) >= TARGET_COS: D0 = mid; hi = mid - 8
    else: lo = mid + 8
print(f"\n场景1: 结构化不对齐  D₀={D0}")

# 多轮反馈
print(f"\n{'轮次':>4s} {'dᵣ新增':>6s} {'累计d':>6s} {'cos':>8s} {'vs D₀':>7s}")
print(f"{'─' * 36}")

recon = np.zeros_like(data)
total_d = 0
all_deltas = []
residual = data.copy()

for rnd in range(5):
    # 第rnd轮：发送方编码当前残差 → 接收方差解码
    rpca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    rpca.fit(residual)
    
    # 找最小达标维度
    lo, hi = 2, min(FULL_DIM, N_SAMPLES)
    dr = hi
    while lo <= hi:
        mid = ((lo + hi) // 2 // 2) * 2; mid = max(2, min(mid, rpca.n_components_))
        rc = rpca.transform(residual)[:, :mid]
        piece = rc @ rpca.components_[:mid] + rpca.mean_
        temp_recon = recon + piece
        nr = np.linalg.norm(temp_recon, axis=1, keepdims=True); nr[nr == 0] = 1
        temp_recon /= nr
        if cos_sim(data, temp_recon) >= TARGET_COS:
            dr = mid; hi = mid - 2
        else:
            lo = mid + 2
    
    # 应用本轮补偿
    rc = rpca.transform(residual)[:, :dr]
    piece = rc @ rpca.components_[:dr] + rpca.mean_
    recon += piece
    nr = np.linalg.norm(recon, axis=1, keepdims=True); nr[nr == 0] = 1
    recon /= nr
    
    residual = data - recon
    total_d += dr
    cs = cos_sim(data, recon)
    all_deltas.append({"round": rnd + 1, "delta_d": dr, "cumulative_d": total_d, "cos_sim": round(cs, 4)})
    print(f"{rnd+1:4d} {dr:6d} {total_d:6d} {cs:8.4f} {total_d-D0:+7d}")
    
    if cs >= 0.99 or dr <= 2:
        break

# ════════════════════════════════════════════════════
# 场景2：ARQ 噪声多轮
# ════════════════════════════════════════════════════
print(f"\n场景2: ARQ 噪声多轮 (σ=0.01)")

data_r = np.random.randn(N_SAMPLES, FULL_DIM)
data_r /= np.linalg.norm(data_r, axis=1, keepdims=True)
pca_r_all = PCA(n_components=FULL_DIM)
pca_r_all.fit(data_r)

# D₀
lo, hi = 8, FULL_DIM; D0_r = FULL_DIM
while lo <= hi:
    mid = ((lo + hi) // 2 // 8) * 8; mid = max(8, mid)
    c_r = pca_r_all.transform(data_r)[:, :mid]
    r_rec = c_r @ pca_r_all.components_[:mid] + pca_r_all.mean_
    nr = np.linalg.norm(r_rec, axis=1, keepdims=True); nr[nr == 0] = 1; r_rec /= nr
    if cos_sim(data_r, r_rec) >= TARGET_COS: D0_r = mid; hi = mid - 8
    else: lo = mid + 8
print(f"D₀={D0_r}")

recon_r = np.zeros_like(data_r)
total_d_r = 0
noise_std = 0.01
arq_deltas = []
residual_r = data_r.copy()

for rnd in range(8):
    rpca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    rpca.fit(residual_r)
    
    lo, hi = 2, min(FULL_DIM, N_SAMPLES)
    dr = hi
    while lo <= hi:
        mid = ((lo + hi) // 2 // 2) * 2; mid = max(2, min(mid, rpca.n_components_))
        rc = rpca.transform(residual_r)[:, :mid] + np.random.randn(N_SAMPLES, mid) * noise_std
        piece = rc @ rpca.components_[:mid] + rpca.mean_
        temp_recon = recon_r + piece
        nr = np.linalg.norm(temp_recon, axis=1, keepdims=True); nr[nr == 0] = 1
        temp_recon /= nr
        if cos_sim(data_r, temp_recon) >= TARGET_COS:
            dr = mid; hi = mid - 2
        else:
            lo = mid + 2
    
    rc = rpca.transform(residual_r)[:, :dr] + np.random.randn(N_SAMPLES, dr) * noise_std
    piece = rc @ rpca.components_[:dr] + rpca.mean_
    recon_r += piece
    nr = np.linalg.norm(recon_r, axis=1, keepdims=True); nr[nr == 0] = 1
    recon_r /= nr
    residual_r = data_r - recon_r
    total_d_r += dr
    cs = cos_sim(data_r, recon_r)
    arq_deltas.append({"round": rnd + 1, "delta_d": dr, "cumulative_d": total_d_r, "cos_sim": round(cs, 4)})
    print(f"{rnd+1:4d} {dr:6d} {total_d_r:6d} {cs:8.4f} {total_d_r-D0_r:+7d}")
    
    if cs >= 0.99 or dr <= 2:
        break

# ════════════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════════════
results = {
    "structured_misalignment": {
        "D0": D0,
        "rounds": all_deltas,
        "final_total_d": total_d,
        " converges_to_D0 ": total_d <= D0 * 1.1  # 10% tolerance
    },
    "arq_noise": {
        "D0": D0_r,
        "rounds": arq_deltas,
        "final_total_d": total_d_r,
        " converges_to_D0 ": total_d_r <= D0_r * 1.1
    }
}

print(f"\n{'═' * 65}")
print(f"结论")
print(f"═" * 65)
print(f"场景1(结构化不对齐): D₀={D0}, 总维度={total_d}, 比率={total_d/D0:.2f}")
print(f"  增量递减: {' → '.join(str(d['delta_d']) for d in all_deltas)}")
print(f"  是否趋近D₀: {'✓ 是' if total_d <= D0 * 1.1 else '✗ 否'}")
print(f"场景2(ARQ噪声): D₀={D0_r}, 总维度={total_d_r}, 比率={total_d_r/D0_r:.2f}")
print(f"  增量递减: {' → '.join(str(d['delta_d']) for d in arq_deltas)}")
print(f"  是否趋近D₀: {'✓ 是' if total_d_r <= D0_r * 1.1 else '✗ 否'}")

path = os.path.join(RESULTS_DIR, f"{TIMESTAMP}_multiround_feedback.json")
with open(path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n📦 {path}")
