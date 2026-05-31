#!/usr/bin/env python3
"""IAT T-C2: 同模型意图编码实验 — 找到压缩态的最小可传输维度"""
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from datetime import datetime

# ── 配置 ──
MODEL_NAME = "answerdotai/ModernBERT-base"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DIMS_TO_TEST = [768, 512, 384, 256, 128, 64, 48, 32, 24, 16, 12, 8]

# ── 测试意图（模拟Agent通信中的实际意图） ──
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

def encode_intents(model, tokenizer, intents):
    """用ModernBERT编码意图，返回768维向量"""
    vectors = []
    for text in intents:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, 
                          max_length=128, padding=True).to(DEVICE)
        with torch.no_grad():
            outputs = model(**inputs)
            # 取[CLS] token的hidden state
            vec = outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()
        vectors.append(vec)
    return np.array(vectors)

def truncate_vectors(vectors, dim):
    """截断向量到指定维度并用零填充剩余"""
    truncated = np.zeros_like(vectors)
    truncated[:, :dim] = vectors[:, :dim]
    return truncated

def compute_fidelity(original, truncated):
    """计算截断后的保真度"""
    # Cosine similarity between original and truncated
    orig_norm = original / (np.linalg.norm(original, axis=1, keepdims=True) + 1e-10)
    trunc_norm = truncated / (np.linalg.norm(truncated, axis=1, keepdims=True) + 1e-10)
    cosine_sims = np.sum(orig_norm * trunc_norm, axis=1)
    
    # Nearest-neighbor retrieval accuracy: does truncated vector's nearest neighbor
    # match the original vector's nearest neighbor?
    from sklearn.metrics.pairwise import cosine_similarity
    orig_sim = cosine_similarity(original)
    trunc_sim = cosine_similarity(truncated)
    
    # For each query, check if top-1 match (excluding self) is the same
    nn_match = 0
    for i in range(len(original)):
        orig_nn = np.argsort(orig_sim[i])[-2]  # top-1 excluding self
        trunc_nn = np.argsort(trunc_sim[i])[-2]
        if orig_nn == trunc_nn:
            nn_match += 1
    
    return {
        "cosine_mean": float(np.mean(cosine_sims)),
        "cosine_std": float(np.std(cosine_sims)),
        "nn_accuracy": nn_match / len(original),
    }

# ── 主实验 ──
print(f"🚀 IAT T-C2 同模型意图编码实验")
print(f"   模型: {MODEL_NAME}")
print(f"   设备: {DEVICE}")
print(f"   意图数: {len(INTENTS)}")
print(f"   测试维度: {DIMS_TO_TEST}")
print()

print("📥 加载模型...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True).to(DEVICE)
model.eval()
print(f"   ✅ 加载完成，hidden_dim={model.config.hidden_size}")

print("\n🔤 编码意图...")
vectors = encode_intents(model, tokenizer, INTENTS)
print(f"   ✅ 编码完成，shape={vectors.shape}")

print("\n📊 压缩-保真度实验:")
print(f"{'维度':>5} | {'cos_sim均值':>10} | {'cos_sim标准差':>10} | {'NN准确率':>8} | {'bits/意图':>10} | {'压缩比':>8}")
print("-" * 70)

results = []
for dim in DIMS_TO_TEST:
    truncated = truncate_vectors(vectors, dim)
    fid = compute_fidelity(vectors, truncated)
    
    bits = dim * 32  # FP32
    compression = 768 / dim
    
    print(f"{dim:>5} | {fid['cosine_mean']:>10.4f} | {fid['cosine_std']:>10.4f} | {fid['nn_accuracy']:>8.3f} | {bits:>10} | {compression:>8.1f}x")
    results.append({"dim": dim, **fid, "bits": bits, "compression": compression})

# ── 找到摩斯码下限 ──
cliff_dim = None
for r in results:
    if r["nn_accuracy"] < 0.75:  # NN准确率跌破75%
        cliff_dim = r["dim"]
        break

print(f"\n🔑 关键发现:")
print(f"   NN准确率断崖维度: {cliff_dim}维" if cliff_dim else "   所有维度NN准确率均>75%")
print(f"   ModernBERT原始维度: 768 → 实验已覆盖")

# 找到仍保持>90%保真度的最小维度
min_high_dim = None
for r in results:
    if r["cosine_mean"] > 0.90 and r["nn_accuracy"] > 0.85:
        min_high_dim = r
if min_high_dim:
    print(f"   高保真最小维度: {min_high_dim['dim']}维")
    print(f"     cos_sim={min_high_dim['cosine_mean']:.4f}, NN_acc={min_high_dim['nn_accuracy']:.3f}")
    print(f"     压缩比: {768/min_high_dim['dim']:.0f}x, 传输成本: {min_high_dim['bits']} bits")

print(f"\n⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
