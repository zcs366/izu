#!/usr/bin/env python3
"""
成市守恒律 (Chengshi Conservation Law) 全实验复现脚本
按论文章节顺序运行，保存结构化数据到 data/ 和 results/
"""
import numpy as np
import torch
import json
import time
import os
os.environ["HF_HUB_OFFLINE"] = "1"
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel

# ─── 路径配置 ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FULL_DIM = 768
TARGET_COS = 0.95
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
run_log = {"experiment": "成市守恒律全实验复现", "timestamp": TIMESTAMP, "seed": SEED, "device": DEVICE, "results": {}}

def save_json(name, data):
    path = os.path.join(RESULTS_DIR, f"{TIMESTAMP}_{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=float)
    print(f"  ✅ 保存: {path}")
    return path

def save_npy(name, arr):
    path = os.path.join(DATA_DIR, f"{TIMESTAMP}_{name}.npy")
    np.save(path, arr)
    print(f"  ✅ 保存: {path}")
    return path

def cos_sim(x, y):
    return float(np.mean(np.sum(x * y, axis=1)))

def find_min_d(data, encode_fn, decode_fn, label, noise_std=0, max_dim=FULL_DIM):
    """二分搜最小达标维度"""
    lo, hi = 8, max_dim
    best = max_dim
    while lo <= hi:
        mid = ((lo + hi) // 2 // 8) * 8
        mid = max(8, min(mid, max_dim))
        c = encode_fn(data, mid)
        if noise_std > 0:
            c = c + np.random.randn(*c.shape) * noise_std
        r = decode_fn(c, mid)
        if cos_sim(data, r) >= TARGET_COS:
            best = mid
            hi = mid - 8
        else:
            lo = mid + 8
    print(f"  {label}: D={best}")
    return best

# ════════════════════════════════════════════════════
# §3.1 T-C2 同模型意图编码实验
# ════════════════════════════════════════════════════
print("═" * 65)
print("§3.1 T-C2 同模型意图编码实验")
print("═" * 65)

INTENTS = [
    "让MiMo写一首关于春天的现代诗，不要押韵，要有意象",
    "检查ITA编码器的FSQ量化精度是否达标",
    "把最近三天的论文日报合并成一份周报",
    "搜索Kolmogorov复杂度在程序分析中的应用",
    "评估Anthropic Managed Agents对IDC架构的影响",
    "用户想了解Sapir-Whorf假说和压缩理论的关联",
    "清理output目录下所有未分类文件",
    "联系arxiv背书候选人Barry O'Sullivan",
    "用gzip计算两个函数的归一化压缩距离",
    "分析叶学伟系列文章中关于语义压缩的核心论点",
    "创建IAT三条路线的PAL文件",
    "对比DeepSeek V4和MiMo V2.5在代码生成上的差异",
    "把Δ胶囊的256维占位向量替换为真实语义嵌入",
    "总结今天投喂的72篇叶学伟文章的核心脉络",
    "设计一个实验验证压缩态传输的保真度",
    "找到StarCoder2模型中适合提取函数指纹的隐藏层",
    "用Chomsky层级解释为什么正则文法不能描述编程语言",
    "把Pro的意图压缩成64维向量传给MiMo解码",
    "评估辛顿和乔姆斯基在语言本质上的分歧",
    "为一个完全不懂AI的人解释什么是嵌入向量",
]

print("加载 ModernBERT-base...")
tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base", trust_remote_code=True)
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base", trust_remote_code=True).to(DEVICE)
model.eval()

def encode_intents(texts):
    vectors = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(DEVICE)
        with torch.no_grad():
            outputs = model(**inputs)
            vec = outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()
        vectors.append(vec)
    return np.array(vectors)

vectors = encode_intents(INTENTS)
save_npy("tc2_intents_768d", vectors)

DIMS_TO_TEST = [768, 512, 384, 256, 128, 64, 48, 32, 24, 16, 12, 8]
tc2_results = []
for dim in DIMS_TO_TEST:
    truncated = np.zeros_like(vectors)
    truncated[:, :dim] = vectors[:, :dim]
    orig_norm = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10)
    trunc_norm = truncated / (np.linalg.norm(truncated, axis=1, keepdims=True) + 1e-10)
    cos_mean = float(np.mean(np.sum(orig_norm * trunc_norm, axis=1)))
    cos_std = float(np.std(np.sum(orig_norm * trunc_norm, axis=1)))
    
    orig_sim = cosine_similarity(vectors)
    trunc_sim = cosine_similarity(truncated)
    nn_match = sum(1 for i in range(len(vectors)) 
                   if np.argsort(orig_sim[i])[-2] == np.argsort(trunc_sim[i])[-2])
    nn_acc = nn_match / len(vectors)
    
    tc2_results.append({"dim": dim, "cosine_mean": round(cos_mean, 4), "cosine_std": round(cos_std, 4), 
                         "nn_accuracy": round(nn_acc, 4), "bits": dim * 32, "compression_ratio": round(768/dim, 2)})
    print(f"  dim={dim:4d}  cos={cos_mean:.4f}±{cos_std:.4f}  NN_acc={nn_acc:.3f}  {dim*32}bits  {768/dim:.1f}x")

run_log["results"]["tc2"] = tc2_results

# ════════════════════════════════════════════════════
# §3.2 d×r=常数 平凡验证（随机高斯 PCA）
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("§3.2 d×r=常数 平凡验证 (随机高斯 PCA)")
print("═" * 65)

data_random = np.random.randn(2000, FULL_DIM)
data_random /= np.linalg.norm(data_random, axis=1, keepdims=True)
save_npy("section32_random_data", data_random)

pca_random = PCA(n_components=FULL_DIM)
pca_random.fit(data_random)

def encode_pca(x, d):
    return pca_random.transform(x)[:, :d]

def decode_pca(c, d):
    r = c @ pca_random.components_[:d] + pca_random.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True)
    nr[nr == 0] = 1
    return r / nr

D0 = find_min_d(data_random, encode_pca, decode_pca, "D₀(无噪声)")
D_noisy = find_min_d(data_random, encode_pca, decode_pca, f"D_noisy(σ=0.01)", noise_std=0.01)

# d×r 多组验证
dr_results = []
for d in [384, 256, 192, 128, 96, 64, 48, 32, 24, 16, 12, 8]:
    recon = np.zeros_like(data_random)
    pc_offset = 0
    rounds = 0
    for rnd in range(50):
        rounds = rnd + 1
        end_pc = min(pc_offset + d, FULL_DIM)
        actual_d = end_pc - pc_offset
        if actual_d <= 0:
            break
        c_batch = encode_pca(data_random, end_pc)[:, pc_offset:end_pc]
        piece = c_batch @ pca_random.components_[pc_offset:end_pc]
        recon += piece
        nr = np.linalg.norm(recon, axis=1, keepdims=True)
        nr[nr == 0] = 1
        recon_n = recon / nr
        if cos_sim(data_random, recon_n) >= TARGET_COS:
            break
        pc_offset = end_pc
    cs = cos_sim(data_random, recon_n if rounds > 0 else np.zeros_like(data_random))
    dr_results.append({"d": d, "rounds": rounds, "d_times_r": d * rounds, "cos_sim": round(cs, 4),
                        "converged": cs >= TARGET_COS})
    status = "✓" if cs >= TARGET_COS else "✗"
    print(f"  d={d:4d}  r={rounds:2d}  d×r={d*rounds:5d}  cos={cs:.4f}  {status}")

converged = [r for r in dr_results if r["converged"]]
c_vals = [r["d_times_r"] for r in converged]
C_mean = float(np.mean(c_vals)) if c_vals else 0
C_std = float(np.std(c_vals)) if c_vals else 0
print(f"  C = {C_mean:.1f} ± {C_std:.1f}")

run_log["results"]["section32"] = {"D0": D0, "D_noisy": D_noisy, "C_mean": C_mean, "C_std": C_std, "dr_results": dr_results}

# ════════════════════════════════════════════════════
# §3.3 Chomsky 层级合成数据实验
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("§3.3 Chomsky 层级合成数据实验")
print("═" * 65)

def gen_regular(n, dim):
    data = np.zeros((n, dim))
    for i in range(n):
        period = np.random.randint(2, 8)
        pattern = np.random.randn(period)
        data[i] = np.tile(pattern, dim // period + 1)[:dim]
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_cf(n, dim):
    data = np.zeros((n, dim))
    for i in range(n):
        k = np.random.randint(2, dim // 4)
        a_part = np.random.randn() * np.ones(k)
        b_part = np.random.randn() * np.ones(k) * (-1)
        fill = np.random.randn(dim - 2 * k) * 0.01
        data[i, :k] = a_part
        data[i, k:2*k] = b_part
        data[i, 2*k:] = fill
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_cs(n, dim):
    data = np.zeros((n, dim))
    for i in range(n):
        k = np.random.randint(2, dim // 6)
        a = np.random.randn() * np.ones(k)
        b = np.random.randn() * np.ones(k) * 2
        c = np.random.randn() * np.ones(k) * (-2)
        fill = np.random.randn(dim - 3 * k) * 0.001
        data[i, :k] = a; data[i, k:2*k] = b; data[i, 2*k:3*k] = c
        data[i, 3*k:] = fill
    return data / np.linalg.norm(data, axis=1, keepdims=True)

def gen_re(n, dim):
    data = np.zeros((n, dim))
    for i in range(n):
        seeds = np.random.randn(5)
        for j in range(dim):
            val = sum(seeds[b] for b in range(5) if (j >> b) & 1)
            data[i, j] = val
    return data / np.linalg.norm(data, axis=1, keepdims=True)

chomsky_data = {
    "Type3_regular": gen_regular(500, FULL_DIM),
    "Type2_anbn": gen_cf(500, FULL_DIM),
    "Type1_anbncn": gen_cs(500, FULL_DIM),
    "Type0_XOR": gen_re(500, FULL_DIM),
}

chomsky_results = {}
for name, data_ch in chomsky_data.items():
    pca_ch = PCA(n_components=min(FULL_DIM, 500))
    pca_ch.fit(data_ch)
    lo, hi = 8, min(FULL_DIM, 500)
    D0_ch = hi
    while lo <= hi:
        mid = ((lo + hi) // 2 // 8) * 8
        mid = max(8, mid)
        c_ch = pca_ch.transform(data_ch)[:, :mid]
        r_ch = c_ch @ pca_ch.components_[:mid] + pca_ch.mean_
        nr = np.linalg.norm(r_ch, axis=1, keepdims=True); nr[nr == 0] = 1
        r_ch /= nr
        if cos_sim(data_ch, r_ch) >= TARGET_COS:
            D0_ch = mid; hi = mid - 8
        else:
            lo = mid + 8
    print(f"  {name}: D₀={D0_ch}")
    chomsky_results[name] = {"D0": D0_ch}
    save_npy(f"chomsky_{name}", data_ch)

run_log["results"]["chomsky"] = chomsky_results

# ════════════════════════════════════════════════════
# §3.4 语义反馈实验（结构化不对齐）
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("§3.4 语义反馈实验（结构化不对齐）")
print("═" * 65)

SHARED_PCS = 20
ROTATED_PCS = 50
ROT_START = SHARED_PCS

signal_basis = np.linalg.qr(np.random.randn(FULL_DIM, SHARED_PCS + ROTATED_PCS))[0].T
coeffs = np.random.randn(2000, SHARED_PCS + ROTATED_PCS) * 5.0
noise_fb = np.random.randn(2000, FULL_DIM) * 0.2
data_fb = coeffs @ signal_basis + noise_fb
data_fb /= np.linalg.norm(data_fb, axis=1, keepdims=True)
save_npy("section34_feedback_data", data_fb)

pca_s = PCA(n_components=FULL_DIM)
pca_s.fit(data_fb)

R_fb = np.linalg.qr(np.random.randn(ROTATED_PCS, ROTATED_PCS))[0]
pca_r_comps = pca_s.components_.copy()
pca_r_comps[ROT_START:ROT_START + ROTATED_PCS] = R_fb @ pca_r_comps[ROT_START:ROT_START + ROTATED_PCS]

def encode_s(x, d):
    return pca_s.transform(x)[:, :d]

def decode_s(c, d):
    r = c[:, :d] @ pca_s.components_[:d] + pca_s.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr == 0] = 1; return r / nr

def decode_r_fb(c, d):
    r = c[:, :d] @ pca_r_comps[:d] + pca_s.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr == 0] = 1; return r / nr

c_full_fb = encode_s(data_fb, FULL_DIM)

D0_s = find_min_d(data_fb, encode_s, decode_s, "D₀(发送自闭环)")
D_mis = find_min_d(data_fb, encode_s, decode_r_fb, "D_misalign")

# 反馈实验
best_fb = None
for d1 in [SHARED_PCS, SHARED_PCS + ROTATED_PCS // 2, SHARED_PCS + ROTATED_PCS]:
    d1 = max(8, min(d1, FULL_DIM))
    r1 = decode_r_fb(c_full_fb, d1)
    resid = data_fb - r1
    rpca = PCA(n_components=min(FULL_DIM, 2000))
    rpca.fit(resid)
    cumvar = np.cumsum(rpca.explained_variance_ratio_)
    for cov_target in [0.5, 0.7, 0.85, 0.9, 0.95]:
        d2 = int(np.searchsorted(cumvar, cov_target) + 1)
        d2 = max(2, min(d2, FULL_DIM // 4))
        rc = rpca.transform(resid)
        piece = rc[:, :d2] @ rpca.components_[:d2] + rpca.mean_
        recon_fb = r1 + piece
        nr = np.linalg.norm(recon_fb, axis=1, keepdims=True); nr[nr == 0] = 1; recon_fb /= nr
        cs_fb = cos_sim(data_fb, recon_fb)
        total_fb = d1 + d2
        if cs_fb >= TARGET_COS:
            saving = (1 - total_fb / D_mis) * 100 if D_mis > 0 else 0
            print(f"  d₁={d1:4d} d₂={d2:3d} total={total_fb:5d} cos={cs_fb:.4f} vsD₀={total_fb-D0_s:+5d} vsDm={total_fb-D_mis:+5d} 节省{saving:.0f}%")
            if best_fb is None or total_fb < best_fb["total"]:
                best_fb = {"d1": d1, "d2": d2, "total": total_fb, "cos": round(cs_fb, 4), "vs_D0": total_fb - D0_s, "vs_Dmis": total_fb - D_mis, "saving_pct": round(saving, 1)}

if best_fb:
    d1_opt = best_fb["d1"]
    r1 = decode_r_fb(c_full_fb, d1_opt)
    resid = data_fb - r1
    rpca = PCA(n_components=min(FULL_DIM, 2000))
    rpca.fit(resid)
    for d2 in range(2, min(100, D0_s), 2):
        rc = rpca.transform(resid)
        piece = rc[:, :d2] @ rpca.components_[:d2] + rpca.mean_
        recon_fb = r1 + piece
        nr = np.linalg.norm(recon_fb, axis=1, keepdims=True); nr[nr == 0] = 1; recon_fb /= nr
        cs_fb = cos_sim(data_fb, recon_fb)
        total_fb = d1_opt + d2
        if cs_fb >= TARGET_COS and total_fb < best_fb["total"]:
            saving = (1 - total_fb / D_mis) * 100
            best_fb = {"d1": d1_opt, "d2": d2, "total": total_fb, "cos": round(cs_fb, 4), "vs_D0": total_fb - D0_s, "vs_Dmis": total_fb - D_mis, "saving_pct": round(saving, 1)}
    print(f"  细搜最优: d₁={best_fb['d1']} d₂={best_fb['d2']} total={best_fb['total']} 节省{best_fb['saving_pct']:.0f}%")

run_log["results"]["section34_feedback"] = {"D0_sender": D0_s, "D_misalign": D_mis, "best_feedback": best_fb}

# ════════════════════════════════════════════════════
# §3.5 FSQ 量化压缩实验
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("§3.5 FSQ 量化压缩实验")
print("═" * 65)

def fsq_quantize(z, L):
    bound = (L - 1) / 2
    z_norm = np.tanh(z) * bound
    z_quant = np.round(z_norm)
    z_quant = np.clip(z_quant, -bound, bound)
    return z_quant / bound

data_fsq = np.random.randn(2000, FULL_DIM)
data_fsq /= np.linalg.norm(data_fsq, axis=1, keepdims=True)
save_npy("section35_fsq_data", data_fsq)

pca_fsq = PCA(n_components=384)
compressed_fsq = pca_fsq.fit_transform(data_fsq)

def pca_reconstruct(c, pca_obj):
    r = c @ pca_obj.components_ + pca_obj.mean_
    nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr == 0] = 1; return r / nr

fp32_recon = pca_reconstruct(compressed_fsq, pca_fsq)
fp32_cos = cos_sim(data_fsq, fp32_recon)
print(f"  FP32 384D 基线: cos={fp32_cos:.4f}, 1536 bytes")

fsq_results = []
best_fsq = None
z_mean = compressed_fsq.mean(axis=0)
z_std = compressed_fsq.std(axis=0) + 1e-8
z_for_fsq = (compressed_fsq - z_mean) / z_std

for L in [3, 5, 7, 9, 11, 15, 31, 63]:
    z_q = fsq_quantize(z_for_fsq, L)
    z_r = z_q * z_std + z_mean
    recon = pca_reconstruct(z_r, pca_fsq)
    cs = cos_sim(data_fsq, recon)
    bpd = np.log2(L)
    tbytes = 384 * bpd / 8
    ratio = 1536 / tbytes if tbytes > 0 else 0
    ok = cs >= TARGET_COS
    fsq_results.append({"L": L, "bits_per_dim": round(bpd, 1), "bytes": round(tbytes, 1), 
                         "cos_sim": round(cs, 4), "compression_ratio": round(ratio, 1), "达标": ok})
    print(f"  FSQ-{L:2d}  {bpd:.1f}bit/dim  {tbytes:.0f}B  cos={cs:.4f}  {ratio:.1f}x  {'✓' if ok else ''}")
    if ok and (best_fsq is None or tbytes < best_fsq["bytes"]):
        best_fsq = {"L": L, "bytes": round(tbytes, 1), "cos_sim": round(cs, 4), "ratio": round(ratio, 1)}

# 语义意图 FSQ 验证
model_st = SentenceTransformer("answerdotai/ModernBERT-base", device=DEVICE, local_files_only=True)
intents_fsq = [
    "我需要你帮我分析这篇论文的方法论缺陷", "请用三句话总结今天的所有讨论",
    "帮我在wiki里搜索关于语言压缩的所有文章", "将这段代码从Python翻译成Rust",
    "生成一份关于上周工作的总结报告", "对比分析GPT-4和Claude在代码生成上的差异",
    "用通俗的语言解释反向传播算法", "设计一个实验来验证压缩维度乘以递归轮次等于常数",
    "帮我找出项目中所有未完成的TODO项", "写一封邮件给合作者讨论论文修改意见",
]
emb_fsq = model_st.encode(intents_fsq, normalize_embeddings=True)
pca_i = PCA(n_components=len(intents_fsq))
c_i = pca_i.fit_transform(emb_fsq)
z_i = (c_i - c_i.mean(axis=0)) / (c_i.std(axis=0) + 1e-8)
intent_fsq_results = []
for L in [3, 5, 7, 9, 15, 31]:
    z_q = fsq_quantize(z_i, L)
    z_r = z_q * c_i.std(axis=0) + c_i.mean(axis=0)
    recon = pca_reconstruct(z_r, pca_i)
    cs = cos_sim(emb_fsq, recon)
    b = len(intents_fsq) * np.log2(L) / 8
    intent_fsq_results.append({"L": L, "bytes": round(b, 1), "cos_sim": round(cs, 4), "达标": cs >= TARGET_COS})
    print(f"  意图 FSQ-{L}: {b:.1f}B cos={cs:.4f} {'✓' if cs >= TARGET_COS else ''}")

run_log["results"]["section35_fsq"] = {"fp32_baseline": {"cos": round(fp32_cos, 4), "bytes": 1536}, "best_fsq": best_fsq, "fsq_results": fsq_results, "intent_fsq": intent_fsq_results}

# ════════════════════════════════════════════════════
# §3.6 递归验证：递进式 + 残差重编码
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("§3.6 递归验证 (递进式 + 残差重编码)")
print("═" * 65)

emb_rec = model_st.encode(intents_fsq, normalize_embeddings=True)
pca_rec = PCA(n_components=min(FULL_DIM, len(intents_fsq)))
pca_rec.fit(emb_rec)

DIMS_REC = [384, 256, 192, 128, 96, 64, 48, 32, 24, 16]
rec_results = {"progressive": [], "residual": []}

# A) 递进式
print("  A) 递进式递归:")
for d in DIMS_REC:
    x_recon = np.zeros_like(emb_rec)
    x_cur = emb_rec.copy()
    rounds = 0
    pc_off = 0
    for _ in range(50):
        rounds += 1
        end = min(pc_off + d, pca_rec.n_components_)
        actual = end - pc_off
        if actual <= 0:
            break
        c_batch = pca_rec.transform(x_cur)[:, :end]
        if pc_off > 0:
            c_old = pca_rec.transform(x_cur)[:, :pc_off]
            r_full = c_batch @ pca_rec.components_[:end] + pca_rec.mean_
            r_old = c_old @ pca_rec.components_[:pc_off] + pca_rec.mean_
            piece = r_full - r_old
        else:
            piece = c_batch @ pca_rec.components_[:end] + pca_rec.mean_
        x_recon += piece
        nr = np.linalg.norm(x_recon, axis=1, keepdims=True); nr[nr == 0] = 1; x_recon /= nr
        x_cur = emb_rec - x_recon
        cs = cos_sim(emb_rec, x_recon)
        nn_acc = sum(1 for i in range(len(emb_rec)) if np.argmax(np.dot(x_recon[i:i+1], emb_rec.T)[0]) == i) / len(emb_rec)
        if cs >= TARGET_COS and nn_acc >= 0.90:
            break
        pc_off = end
        if pc_off >= pca_rec.n_components_:
            break
    cs_final = cos_sim(emb_rec, x_recon)
    rec_results["progressive"].append({"d": d, "rounds": rounds, "d_times_r": d * rounds, "cos_sim": round(cs_final, 4)})
    print(f"    d={d:4d} r={rounds:2d} d×r={d*rounds:4d} cos={cs_final:.4f}")

# B) 残差重编码
print("  B) 残差重编码:")
for d in DIMS_REC:
    x_recon = np.zeros_like(emb_rec)
    residual = emb_rec.copy()
    rounds = 0
    for _ in range(20):
        rounds += 1
        n_comp = min(d, len(emb_rec), residual.shape[1])
        pca_l = PCA(n_components=n_comp)
        pca_l.fit(residual)
        c_l = pca_l.transform(residual)
        piece = pca_l.inverse_transform(c_l)
        x_recon += piece
        nr = np.linalg.norm(x_recon, axis=1, keepdims=True); nr[nr == 0] = 1; x_recon /= nr
        residual = emb_rec - x_recon
        cs = cos_sim(emb_rec, x_recon)
        if cs >= TARGET_COS:
            break
    cs_final = cos_sim(emb_rec, x_recon)
    rec_results["residual"].append({"d": d, "rounds": rounds, "d_times_r": d * rounds, "cos_sim": round(cs_final, 4)})
    print(f"    d={d:4d} r={rounds:2d} d×r={d*rounds:4d} cos={cs_final:.4f}")

run_log["results"]["section36_recursive"] = rec_results

# ════════════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("全实验汇总")
print("═" * 65)
print(f"  §3.1 T-C2: 384维断崖, {tc2_results[2]['nn_accuracy']:.2%} NN准确率")
print(f"  §3.2 d×r: D₀={D0}, D_noisy={D_noisy}, C={C_mean:.1f}±{C_std:.1f}")
ch_display = " ".join(f"{k}=D₀{v['D0']}" for k, v in chomsky_results.items())
print(f"  §3.3 Chomsky: {ch_display}")
if best_fb:
    print(f"  §3.4 反馈: d₁+d₂={best_fb['total']} (vs D₀={D0_s}), 节省{best_fb['saving_pct']:.0f}%")
if best_fsq:
    print(f"  §3.5 FSQ: FSQ-{best_fsq['L']} {best_fsq['bytes']}B ({best_fsq['ratio']}x), cos={best_fsq['cos_sim']:.4f}")

save_json("run_log", run_log)
print(f"\n📦 全部数据已保存到 {RESULTS_DIR}/ 和 {DATA_DIR}/")
print(f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
