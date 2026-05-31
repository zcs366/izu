"""
Chomsky层级 × d×r常数：跨层级验证

假说：d×r = 常数在Chomsky各层均成立，但常数C随层级升高而减小
  - 正则数据：C 最大（需要最多维度，模式简单但表达力弱）
  - 递归可枚举数据：C 最小（通用压缩最省维度）

生成四层合成数据：
  Type 3: 正则模式 (ab)* — 局部重复
  Type 2: aⁿbⁿ — 嵌套递归  
  Type 1: aⁿbⁿcⁿ — 上下文约束
  Type 0: XOR序列 (aᵢ ⊕ bᵢ ⊕ ...) — 需要计算
"""
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import torch, time

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FULL_DIM = 768
N_SAMPLES = 500
TARGET_COS = 0.95

np.random.seed(42)

# ─── 生成四层合成数据 ──────────────────────────────
def gen_regular(n_samples, dim):
    """Type 3: 正则 (ab)* 模式 — 局部重复"""
    data = np.zeros((n_samples, dim))
    for i in range(n_samples):
        period = np.random.randint(2, 8)
        pattern = np.random.randn(period)
        data[i] = np.tile(pattern, dim // period + 1)[:dim]
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_cf(n_samples, dim):
    """Type 2: aⁿbⁿ 嵌套 — 需要栈"""
    data = np.zeros((n_samples, dim))
    for i in range(n_samples):
        n = np.random.randint(2, dim//4)
        a_part = np.random.randn() * np.ones(n)
        b_part = np.random.randn() * np.ones(n) * (-1)  # 反号
        fill = np.random.randn(dim - 2*n) * 0.01
        data[i, :n] = a_part
        data[i, n:2*n] = b_part
        data[i, 2*n:] = fill
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_cs(n_samples, dim):
    """Type 1: aⁿbⁿcⁿ — 三计数约束"""
    data = np.zeros((n_samples, dim))
    for i in range(n_samples):
        n = np.random.randint(2, dim//6)
        a = np.random.randn() * np.ones(n)
        b = np.random.randn() * np.ones(n) * 2
        c = np.random.randn() * np.ones(n) * (-2)
        fill = np.random.randn(dim - 3*n) * 0.001
        data[i, :n] = a; data[i, n:2*n] = b; data[i, 2*n:3*n] = c
        data[i, 3*n:] = fill
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_re(n_samples, dim):
    """Type 0: XOR序列 — 需要任意计算"""
    data = np.zeros((n_samples, dim))
    for i in range(n_samples):
        seeds = np.random.randn(5)  # 5个种子
        for j in range(dim):
            # XOR-like: 维度j的值取决于j mod 32的位运算
            val = 0
            for b in range(5):
                if (j >> b) & 1:
                    val += seeds[b]
            data[i, j] = val
    return data / np.linalg.norm(data, axis=1, keepdims=True)

# ─── 实验 ──────────────────────────────────────────
print(f"{'═'*60}")
print(f"Chomsky层级 × d×r=常数 跨层验证")
print(f"{'═'*60}")

datasets = {
    'Type3 正则(ab)*': gen_regular(N_SAMPLES, FULL_DIM),
    'Type2 aⁿbⁿ':      gen_cf(N_SAMPLES, FULL_DIM),
    'Type1 aⁿbⁿcⁿ':    gen_cs(N_SAMPLES, FULL_DIM),
    'Type0 XOR':       gen_re(N_SAMPLES, FULL_DIM),
}

results = {}

for name, data in datasets.items():
    print(f"\n{'─'*50}")
    print(f"  {name}")
    
    pca = PCA(n_components=min(FULL_DIM, N_SAMPLES))
    pca.fit(data)
    
    def cos_at_d(d):
        c = pca.transform(data)[:,:d]
        r = c @ pca.components_[:d] + pca.mean_
        n = np.linalg.norm(r, axis=1, keepdims=True); n[n==0]=1
        r /= n
        return np.mean(np.sum(data*r, axis=1))
    
    # 找 D₀
    lo, hi = 8, min(FULL_DIM, N_SAMPLES)
    D0 = hi
    while lo <= hi:
        mid = ((lo+hi)//2//8)*8; mid = max(8, mid)
        if cos_at_d(mid) >= TARGET_COS:
            D0 = mid; hi = mid - 8
        else: lo = mid + 8
    
    # 多维度测试
    d_list = sorted(set(d for d in [D0, D0//2, D0//4, D0//8] if d >= 4), reverse=True)
    
    print(f"    D₀={D0}")
    print(f"    {'d':>5s} {'r':>4s} {'d×r':>5s} {'cos':>7s}")
    print(f"    {'-'*25}")
    
    c_vals = []
    for d in d_list:
        r = int(np.ceil(D0 / d))
        total = r * d
        cos_v = cos_at_d(min(total, min(FULL_DIM, N_SAMPLES)))
        c_vals.append(total)
        marker = "✓" if cos_v >= TARGET_COS else "✗"
        print(f"    {d:5d} {r:4d} {total:5d} {cos_v:7.4f} {marker}")
    
    results[name] = {'D0': D0, 'C_mean': np.mean(c_vals), 'C_std': np.std(c_vals), 
                     'c_vals': c_vals}

# ─── 跨层对比 ──────────────────────────────────────
print(f"\n{'═'*60}")
print(f"跨层对比")
print(f"{'═'*60}")
print(f"{'层级':<20s} {'D₀':>5s} {'C_mean':>7s} {'C_std':>7s} {'值':>20s}")
print(f"{'-'*65}")
for name, r in results.items():
    vals_str = ','.join(str(v) for v in r['c_vals'])
    print(f"{name:<20s} {r['D0']:5d} {r['C_mean']:7.1f} {r['C_std']:7.1f} {vals_str:>20s}")

print(f"\n结论:")
print(f"  若 C_mean 随层级升高递减 → 高层级数据压缩效率更高")
print(f"  若 C_std 在各层均小 → d×r=常数 跨层普适")
