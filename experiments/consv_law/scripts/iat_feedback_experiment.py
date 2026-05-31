"""
验证：递归反馈能否使总维度 < D_noisy？（ARQ风格）

ARQ (Automatic Repeat reQuest):
  发送方 → d dims → 接收方解码
  接收方检测误差 → 若cos<target → 请求重传下一批PCs
  接收方累积所有批次 → 达标停止

关键对比：
  A) 无噪声单轮 D₀
  B) 有噪声单轮 D_noisy（一次传够，对抗噪声）
  C) 有噪声ARQ反馈  d×r（分批传，每批中小维度，达标准止）
  
判据：C < B？（反馈是否比单次抗噪编码更省维度）
"""
import numpy as np
from sklearn.decomposition import PCA
import time

FULL_DIM = 768
N_SAMPLES = 2000
TARGET_COS = 0.95
NOISE_STD = 0.01  # SNR = 1/(D₀×σ²) ≈ 0.18 → cos_max ≈ 0.90, 刚好能到0.95

np.random.seed(42)
data = np.random.randn(N_SAMPLES, FULL_DIM)
data /= np.linalg.norm(data, axis=1, keepdims=True)

t0 = time.time()
pca = PCA(n_components=FULL_DIM)
pca.fit(data)
EFF = FULL_DIM

def encode(x, d): return pca.transform(x)[:, :d]
def decode(c, d):
    r = c @ pca.components_[:d] + pca.mean_
    n = np.linalg.norm(r, axis=1, keepdims=True); n[n==0]=1
    return r/n
def cos_sim(x,y): return np.mean(np.sum(x*y, axis=1))

# ─── A) 无噪声 D₀ ─────────────────────────────────
def find_min(cond_fn, label):
    lo, hi = 8, EFF; best = EFF
    while lo <= hi:
        mid = ((lo+hi)//2//8)*8; mid = max(8,min(mid,EFF))
        if cond_fn(mid): best=mid; hi=mid-8
        else: lo=mid+8
    print(f"  {label}: {best}")
    return best

D0 = find_min(lambda d: cos_sim(data, decode(encode(data,d), d)) >= TARGET_COS, "D₀ (无噪声)")

# ─── B) 有噪声单轮 D_noisy ─────────────────────────
def noisy_single_ok(d):
    c = encode(data,d) + np.random.randn(N_SAMPLES,d)*NOISE_STD
    return cos_sim(data, decode(c,d)) >= TARGET_COS
D_noisy = find_min(noisy_single_ok, f"D_noisy (σ={NOISE_STD}, 单轮)")
print(f"  噪声开销: +{D_noisy-D0} ({(D_noisy/D0-1)*100:.0f}%)")

# ─── C) ARQ反馈 ──────────────────────────────────
def arq_transmit(x, d_per, max_r=50):
    """每轮传d_per维PCs，噪声信道，累积解码，达标即停"""
    recon = np.zeros_like(x)
    pc_start = 0
    
    for rnd in range(max_r):
        pc_end = min(pc_start + d_per, EFF)
        actual_d = pc_end - pc_start
        if actual_d <= 0: break
        
        # 编码当前批次PCs
        full_c = encode(x, pc_end)  # (N, pc_end)
        if pc_start > 0:
            c_slice = full_c[:, pc_start:pc_end]  # 增量: (N, actual_d)
        else:
            c_slice = full_c  # (N, actual_d)
        c_noisy = c_slice + np.random.randn(N_SAMPLES, actual_d)*NOISE_STD
        
        # 解码增量
        piece = c_noisy @ pca.components_[pc_start:pc_end]
        recon += piece
        
        # ARQ: 不归一化中间结果（保持增量叠加的线性性）
        # 只在最后归一化
        
        # 检查是否达标（用归一化版本）
        recon_n = recon.copy()
        n = np.linalg.norm(recon_n, axis=1, keepdims=True); n[n==0]=1
        recon_n /= n
        
        if cos_sim(x, recon_n) >= TARGET_COS:
            return recon_n, rnd+1, True
        
        pc_start = pc_end
    
    n = np.linalg.norm(recon, axis=1, keepdims=True); n[n==0]=1
    return recon/n, max_r, False

# 测试多种d
dim_list = sorted(set(d for d in [D0//2, D0//4, D0//8, D0//16, D0//32, D0//64] if d>=4), reverse=True)
print(f"\n  测试 d × r (vs D_noisy={D_noisy})")
print(f"  {'d':>5s} {'r':>4s} {'d×r':>5s} {'cos':>7s} {'达标':>4s} {'vs D₀':>7s} {'vs Dn':>7s}")
print(f"  {'-'*45}")

best_arq = {'total': 9999, '达标': False}
for d in dim_list:
    _, rnd, ok = arq_transmit(data, d)
    total = rnd * d
    cs = cos_sim(data, arq_transmit(data, d)[0])
    print(f"  {d:5d} {rnd:4d} {total:5d} {cs:7.4f} {'✓' if ok else '✗':>4s} {total-D0:+7d} {total-D_noisy:+7d}")
    if ok and total < best_arq['total']:
        best_arq = {'d': d, 'r': rnd, 'total': total, '达标': True}

# 如果粗搜未达，细搜
if not best_arq['达标']:
    print(f"\n  细搜最佳d...")
    for d in range(max(8, D0//64), D0, 4):
        _, rnd, ok = arq_transmit(data, d)
        if ok and rnd*d < best_arq['total']:
            best_arq = {'d': d, 'r': rnd, 'total': rnd*d, '达标': True}

# ─── 结论 ─────────────────────────────────────────
print(f"\n{'═'*55}")
print(f"D₀={D0} (无噪声单轮)")
print(f"D_noisy={D_noisy} (噪声σ={NOISE_STD}单轮, 开销+{D_noisy-D0})")
if best_arq['达标']:
    print(f"ARQ反馈: d={best_arq['d']}, r={best_arq['r']}, d×r={best_arq['total']}")
    saving_pct = (1 - best_arq['total']/D_noisy)*100
    print(f"  vs D_noisy: 节省 {D_noisy - best_arq['total']} dims ({saving_pct:.0f}%)")
    vs_d0 = best_arq['total'] - D0
    vs_d0_str = '≤D₀ ✓ 突破!' if vs_d0 <= 0 else f'+{vs_d0} (未突破信息守恒)'
    print(f"  vs D₀:     {vs_d0_str}")
else:
    print(f"ARQ反馈: 无达标方案")
print(f"耗时: {time.time()-t0:.1f}s")
