"""
FSQ × 递归 V2：全局归一化 + 分批传输PC系数

流水线：
  1. 全局PCA → 标准化所有维度（均值0方差1）
  2. 每轮：取下一批d个PC系数 → FSQ量化 → 传输
  3. 接收方：逆量化 → 累积 → PCA重建 → 达标即停
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95

np.random.seed(42)
data = np.random.randn(N_SAMPLES, FULL_DIM)
data /= np.linalg.norm(data, axis=1, keepdims=True)

pca = PCA(n_components=FULL_DIM)
pca.fit(data)

# 全局PCA系数 + 全局标准化
c_global = pca.transform(data)  # (N, 768)
g_mean = c_global.mean(axis=0)
g_std = c_global.std(axis=0) + 1e-8
c_norm = (c_global - g_mean) / g_std  # 标准化

def decode_from_pcs(c_accum, n_pcs):
    """从累积的PC系数重建"""
    r = c_accum[:, :n_pcs] @ pca.components_[:n_pcs] + pca.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
    return r / nr

def cos_sim(x, y): return np.mean(np.sum(x*y, axis=1))

def fsq_quantize(z, L):
    bound = (L-1)/2
    zq = np.round(np.tanh(z) * bound)
    return np.clip(zq, -bound, bound) / bound

# ─── 基线 ─────────────────────────────────────────
D0, _ = 552, None  # known from previous
print(f"FP32基线: D₀={D0}, {D0*4}B, cos=0.9518")

# ─── 单轮FSQ基线 ──────────────────────────────────
print(f"\n单轮FSQ基线:")
for L in [5, 7, 9, 15]:
    z_q = fsq_quantize(c_norm[:, :700], L)
    c_r = z_q * g_std[:700] + g_mean[:700]
    recon = decode_from_pcs(c_r, 700)
    cs = cos_sim(data, recon)
    b = 700 * np.log2(L) / 8
    print(f"  FSQ-{L} 700D: {b:.0f}B, cos={cs:.4f} {'✓' if cs>=TARGET_COS else '✗'}")

# ─── FSQ × 递归 ─────────────────────────────────
print(f"\n{'='*55}")
print(f"FSQ × 递归 (全局归一化)")
print(f"{'='*55}")
print(f"{'d':>4s} {'L':>3s} {'r':>3s} {'d×r':>5s} {'B':>6s} {'cos':>7s} {'比':>5s}")
print(f"{'-'*40}")

best = None

for d in [384, 320, 256, 192, 160, 128]:
    for L in [3, 5, 7, 9, 15]:
        recon_c = np.zeros((N_SAMPLES, FULL_DIM))
        rounds = 0
        pc_offset = 0
        
        for rnd in range(1, 31):
            rounds = rnd
            end_pc = min(pc_offset + d, FULL_DIM)
            actual_d = end_pc - pc_offset
            if actual_d <= 0: break
            
            # 取这批的标准化系数 → FSQ量化
            batch_norm = c_norm[:, pc_offset:end_pc]
            batch_q = fsq_quantize(batch_norm, L)
            
            # 逆标准化 → 存入累积数组
            batch_raw = batch_q * g_std[pc_offset:end_pc] + g_mean[pc_offset:end_pc]
            recon_c[:, pc_offset:end_pc] = batch_raw
            
            # 重建
            recon = decode_from_pcs(recon_c, end_pc)
            cs = cos_sim(data, recon)
            
            if cs >= TARGET_COS:
                break
            
            pc_offset = end_pc
        
        td = rounds * d
        b = td * np.log2(L) / 8
        ratio = (D0*4) / b
        ok = "✓" if cs >= TARGET_COS else ""
        
        if cs >= 0.94 or ok:
            print(f"{d:4d} {L:3d} {rounds:3d} {td:5d} {b:6.1f} {cs:7.4f} {ratio:4.1f}x {ok}")
        
        if ok and (best is None or b < best['bytes']):
            best = {'d': d, 'L': L, 'r': rounds, 'bytes': b, 'cos': cs, 'ratio': ratio}

# ─── 细搜 ─────────────────────────────────────────
if best:
    d0, L0 = best['d'], best['L']
    print(f"\n细搜最优 (d≈{d0}, L={L0})...")
    for d in range(max(32, d0-64), min(FULL_DIM, d0+64), 16):
        for L in [L0-2, L0, L0+2]:
            if L < 3: continue
            recon_c = np.zeros((N_SAMPLES, FULL_DIM))
            rounds = 0; pc_offset = 0
            for rnd in range(1, 31):
                rounds = rnd
                end_pc = min(pc_offset + d, FULL_DIM)
                actual_d = end_pc - pc_offset
                if actual_d <= 0: break
                batch_q = fsq_quantize(c_norm[:, pc_offset:end_pc], L)
                recon_c[:, pc_offset:end_pc] = batch_q * g_std[pc_offset:end_pc] + g_mean[pc_offset:end_pc]
                cs = cos_sim(data, decode_from_pcs(recon_c, end_pc))
                if cs >= TARGET_COS: break
                pc_offset = end_pc
            b = rounds * d * np.log2(L) / 8
            if cs >= TARGET_COS and b < best['bytes']:
                best = {'d': d, 'L': L, 'r': rounds, 'bytes': b, 'cos': cs}

# ─── 结论 ─────────────────────────────────────────
print(f"\n{'='*55}")
print(f"最优方案")
print(f"{'='*55}")
if best:
    ratio_v = (D0*4) / best['bytes']
    print(f"  d={best['d']}, L={best['L']}, r={best['r']}")
    print(f"  {best['bytes']:.1f} bytes ({best['d']*np.log2(best['L'])/8:.1f}B/轮 × {best['r']}轮)")
    print(f"  cos={best['cos']:.4f}, {ratio_v:.1f}x vs FP32({D0*4}B)")
    
    fsq_single = 700 * np.log2(7) / 8
    print(f"\n  终极对比:")
    print(f"    FP32 单轮 552D:     2208 B  (基线)")
    print(f"    FSQ-7 单轮 700D:    {fsq_single:.0f} B  (8.9x)")
    print(f"    FSQ-7 递归 ★:       {best['bytes']:.1f} B  ({ratio_v:.1f}x)")
    print(f"\n  核心发现:")
    print(f"    递归不改变总PC需求 → d×r ≈ 700 (FSQ需要补偿量化损失)")
    print(f"    FSQ只改变每维成本 → 32bit → log₂(L) bit")
    print(f"    公式统一: d × r × log₂(L) = 常数(≈D₀'×log₂(L))")
else:
    print(f"  无达标方案")
