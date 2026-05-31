"""
验证: 压缩维度 × 递归轮次 = 常数  (V3 — 大样本+高维噪声)

策略: 1024个多样意图 + σ=0.01噪声 → 768维全量PCA
"""
import torch
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import random

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "answerdotai/ModernBERT-base"
FULL_DIM = 768
TARGET_COS_SIM = 0.95
N_SAMPLES = 1024
NOISE_SIGMA = 0.0  # 不注入噪声，让语义本身决定有效维度

# ─── 生成1024个多样意图 ────────────────────────────
verbs = ["分析","总结","设计","审查","优化","生成","翻译","搜索",
         "解释","对比","评估","预测","规划","调试","重构","部署",
         "监控","记录","归档","提取","转换","合并","分割","计算",
         "模拟","验证","校准","加密","解密","压缩","索引","编排",
         "调度","路由","缓存","序列化","反序列化","归一化","聚类","分类"]
domains = ["代码","数据","论文","报告","文档","日志","配置","数据库",
           "API","前端","后端","网络","安全","性能","内存","存储",
           "模型","算法","图表","测试","部署","运维","用户界面","消息队列",
           "微服务","容器","编排","流水线","监控","告警","认证","授权"]
objects = ["脚本","程序","查询","镜像","配置文件","日志文件","测试用例",
           "API文档","用户手册","技术方案","系统架构","数据管道",
           "机器学习模型","神经网络","特征工程","错误日志","性能报告",
           "安全审计","代码审查","部署清单","数据库模式","缓存策略",
           "负载均衡","容灾方案","备份策略","监控面板","告警规则"]
modifiers = ["高效地","自动地","批量地","增量地","安全地","并发地",
             "异步地","实时地","离线地","分布式地","并行地","串行地",
             "精确地","近似地","保守地","激进地","优雅地","鲁棒地",
             "原子地","幂等地","弹性地","容错地","无损地","有损地"]
adjectives = ["复杂的","简单的","关键的","次要的","紧急的","长期的",
              "短期的","核心的","边缘的","遗留的","新引入的","成熟的",
              "实验性的","生产级的","原型级的","废弃的","推荐的最佳"]

def gen_intent(i):
    t = i % 8
    if t == 0:
        return f"请{random.choice(verbs)}{random.choice(domains)}相关的{random.choice(objects)}"
    elif t == 1:
        return f"帮我{random.choice(verbs)}这个{random.choice(adjectives)}{random.choice(domains)}问题"
    elif t == 2:
        return f"需要{random.choice(verbs)}一份关于{random.choice(domains)}的{random.choice(objects)}"
    elif t == 3:
        return f"用{random.choice(verbs)}的方法处理{random.choice(domains)}中的{random.choice(objects)}"
    elif t == 4:
        return f"{random.choice(modifiers)}{random.choice(verbs)}这个{random.choice(adjectives)}{random.choice(objects)}"
    elif t == 5:
        return f"针对{random.choice(domains)}，{random.choice(verbs)}{random.choice(adjectives)}{random.choice(objects)}"
    elif t == 6:
        return f"{random.choice(verbs)}并{random.choice(verbs)}{random.choice(objects)}的{random.choice(adjectives)}方面"
    else:
        return f"以{random.choice(modifiers)}方式{random.choice(verbs)}{random.choice(domains)}{random.choice(objects)}"

random.seed(42)
intents = [gen_intent(i) for i in range(N_SAMPLES)]

print(f"设备: {DEVICE}")
print(f"样本数: {N_SAMPLES}, 目标 cos_sim ≥ {TARGET_COS_SIM}, 噪声 σ={NOISE_SIGMA}")
print()

# ─── 编码 ─────────────────────────────────────────
print("加载 ModernBERT-base...")
model = SentenceTransformer(MODEL_NAME, device=DEVICE)
print("编码...")
embeddings = model.encode(intents, normalize_embeddings=True)
print(f"Shape: {embeddings.shape}")

# 注入噪声撑开全维度
np.random.seed(42)
noise = np.random.randn(N_SAMPLES, FULL_DIM) * NOISE_SIGMA
embeddings = embeddings + noise
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings = embeddings / norms
print(f"+ 噪声注入完成\n")

# ─── 单轮基线 D₀ ─────────────────────────────────
print("═" * 60)
print("单轮基线：寻找 D₀")
print("═" * 60)

pca_full = PCA(n_components=FULL_DIM, svd_solver='full')
pca_full.fit(embeddings)

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
test_dims = [768, 512, 384, 256, 192, 128, 96, 64, 48, 32, 24, 20, 16, 12, 8]
for d in test_dims:
    if d > FULL_DIM: continue
    _, recon = compress_decompress_single(embeddings, pca_full, d)
    cos_sims = [np.dot(embeddings[i], recon[i]) for i in range(N_SAMPLES)]
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

# ─── 多轮维度 ─────────────────────────────────────
DIMS_TO_TEST = []
d = D0
while d >= 8:
    DIMS_TO_TEST.append(d)
    d = d // 2
if 8 not in DIMS_TO_TEST: DIMS_TO_TEST.append(8)
DIMS_TO_TEST = sorted(set(DIMS_TO_TEST), reverse=True)
print(f"多轮测试维度: {DIMS_TO_TEST}\n")

# ════════════════════════════════════════════════════
# A) 递进式递归
# ════════════════════════════════════════════════════
print("═" * 60)
print("A) 递进式递归")
print("═" * 60)
results_A = []

for d in DIMS_TO_TEST:
    x_recon = np.zeros_like(embeddings)
    rounds = 0
    pc_offset = 0
    
    while True:
        rounds += 1
        end_pc = min(pc_offset + d, FULL_DIM)
        if end_pc <= pc_offset: break
        
        _, recon_full = compress_decompress_single(embeddings, pca_full, end_pc)
        if pc_offset > 0:
            _, recon_old = compress_decompress_single(embeddings, pca_full, pc_offset)
            recon_delta = recon_full - recon_old
        else:
            recon_delta = recon_full
        
        x_recon += recon_delta
        nr = np.linalg.norm(x_recon, axis=1, keepdims=True)
        nr[nr==0] = 1
        x_recon /= nr
        
        cos_sims = [np.dot(embeddings[i], x_recon[i]) for i in range(N_SAMPLES)]
        avg_cos = np.mean(cos_sims)
        if avg_cos >= TARGET_COS_SIM: break
        
        pc_offset = end_pc
        if pc_offset >= FULL_DIM: break
    
    td = rounds * d
    avg_c = np.mean([np.dot(embeddings[i], x_recon[i]) for i in range(N_SAMPLES)])
    results_A.append({'d':d,'rounds':rounds,'dxr':td,'cos':round(avg_c,4),'ok':avg_c>=TARGET_COS_SIM})
    print(f"  d={d:3d} → {rounds:2d}轮 → d×r={td:4d} | cos={avg_c:.4f} {'✓' if avg_c>=TARGET_COS_SIM else '✗'}")

# ════════════════════════════════════════════════════
# B) 残差重编码
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print("B) 残差重编码")
print("═" * 60)
results_B = []

for d in DIMS_TO_TEST:
    residual = embeddings.copy()
    x_recon = np.zeros_like(embeddings)
    rounds = 0
    
    while True:
        rounds += 1
        n_comp = min(d, N_SAMPLES)
        pca_local = PCA(n_components=n_comp, svd_solver='full')
        pca_local.fit(residual)
        
        compressed = pca_local.transform(residual)
        recon_piece = pca_local.inverse_transform(compressed)
        
        x_recon += recon_piece
        nr = np.linalg.norm(x_recon, axis=1, keepdims=True)
        nr[nr==0] = 1
        x_recon /= nr
        
        residual = embeddings - x_recon
        
        avg_cos = np.mean([np.dot(embeddings[i], x_recon[i]) for i in range(N_SAMPLES)])
        if avg_cos >= TARGET_COS_SIM: break
        if rounds >= 50: break
    
    td = rounds * d
    avg_c = np.mean([np.dot(embeddings[i], x_recon[i]) for i in range(N_SAMPLES)])
    results_B.append({'d':d,'rounds':rounds,'dxr':td,'cos':round(avg_c,4),'ok':avg_c>=TARGET_COS_SIM})
    print(f"  d={d:3d} → {rounds:2d}轮 → d×r={td:4d} | cos={avg_c:.4f} {'✓' if avg_c>=TARGET_COS_SIM else '✗'}")

# ════════════════════════════════════════════════════
# 综合对比
# ════════════════════════════════════════════════════
print()
print("═" * 60)
print(f"综合对比 (D₀={D0})")
print("═" * 60)
print(f"{'d':>4s} | {'递进d×r':>8s} {'Δ/D₀':>6s} | {'残差d×r':>8s} {'Δ/D₀':>6s} | 增益")
print("-" * 60)

for i, d in enumerate(DIMS_TO_TEST):
    ra, rb = results_A[i], results_B[i]
    da, db = ra['dxr'] - D0, rb['dxr'] - D0
    gain = ra['dxr'] - rb['dxr']
    gstr = f"残差少{gain}d" if gain > 0 else (f"递进少{abs(gain)}d" if gain < 0 else "相同")
    print(f"{d:4d} | {ra['dxr']:8d} {da:+6d} | {rb['dxr']:8d} {db:+6d} | {gstr}")

# ─── 常数C ───────────────────────────────────────
print()
print("═" * 60)
print("常数C估计")
print("═" * 60)
for label, results in [("递进式", results_A), ("残差重编码", results_B)]:
    ok = [r for r in results if r['ok']]
    if ok:
        c_vals = [r['dxr'] for r in ok]
        print(f"  {label}: C = {np.mean(c_vals):.1f} ± {np.std(c_vals):.1f} (值: {c_vals})")
        print(f"          相对D₀={D0}: {(np.mean(c_vals)-D0):+.1f} ({(np.mean(c_vals)/D0-1)*100:+.1f}%)")

# ─── 关键指标 ─────────────────────────────────────
print()
print("─" * 60)
print("核心判据:")
A_dxr = [r['dxr'] for r in results_A if r['ok']]
B_dxr = [r['dxr'] for r in results_B if r['ok']]
if A_dxr:
    print(f"  1. 递进式 d×r 方差: {np.std(A_dxr):.1f} (越小→常数越稳定)")
if B_dxr:
    print(f"  2. 残差式 d×r 方差: {np.std(B_dxr):.1f}")
    print(f"  3. 残差 vs 递进: 平均差值 {np.mean(A_dxr)-np.mean(B_dxr):.1f} (正→残差更优)")
