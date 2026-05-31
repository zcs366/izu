"""
Part 2 补完: 语义数据验证 (500样本, τ=0.99)
"""
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import random, torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FULL_DIM = 768
N = 500
TARGET = 0.99

verbs = ["分析","总结","设计","审查","优化","生成","翻译","搜索",
         "解释","对比","评估","预测","规划","调试","重构","部署",
         "监控","记录","归档","提取","转换","合并","分割","计算",
         "模拟","验证","校准","加密","解密","压缩","索引","编排",
         "调度","路由","缓存","序列化","归一化","聚类","分类","回归",
         "降维","升维","嵌入","投影","插值","外推","平滑","锐化"]
domains = ["代码","数据","论文","报告","文档","日志","配置","数据库",
           "API","前端","后端","网络","安全","性能","内存","存储",
           "模型","算法","图表","测试","部署","运维","UI","消息队列",
           "微服务","容器","编排","流水线","监控","告警","认证","授权",
           "加密","解密","签名","验证","序列化","反序列化","编解码","压缩"]
objects = ["脚本","程序","查询","镜像","配置","日志","测试用例",
           "API文档","用户手册","技术方案","系统架构","数据管道",
           "模型","神经网络","特征工程","错误日志","性能报告",
           "安全审计","代码审查","部署清单","数据库模式","缓存策略",
           "负载均衡","容灾方案","备份策略","监控面板","告警规则",
           "权限模型","加密方案","签名算法","哈希函数","编码器","解码器"]
modifiers = ["高效地","自动地","批量地","增量地","安全地","并发地",
             "异步地","实时地","离线地","分布式地","并行地","串行地",
             "精确地","近似地","保守地","激进地","优雅地","鲁棒地",
             "原子地","幂等地","弹性地","容错地","无损地","有损地"]
adj = ["复杂的","简单的","关键的","次要的","紧急的","长期的",
       "短期的","核心的","边缘的","遗留的","新引入的","成熟的",
       "实验性的","生产级的","原型级的","废弃的","推荐的"]

random.seed(99)
intents = []
for i in range(N):
    t = i % 12
    if t == 0: s = f"请{random.choice(verbs)}{random.choice(domains)}相关的{random.choice(objects)}"
    elif t == 1: s = f"帮我{random.choice(verbs)}这个{random.choice(adj)}{random.choice(domains)}问题"
    elif t == 2: s = f"需要{random.choice(verbs)}一份关于{random.choice(domains)}的{random.choice(objects)}"
    elif t == 3: s = f"用{random.choice(verbs)}方法处理{random.choice(domains)}{random.choice(objects)}"
    elif t == 4: s = f"{random.choice(modifiers)}{random.choice(verbs)}{random.choice(adj)}{random.choice(objects)}"
    elif t == 5: s = f"针对{random.choice(domains)}{random.choice(verbs)}{random.choice(adj)}{random.choice(objects)}"
    elif t == 6: s = f"{random.choice(verbs)}并{random.choice(verbs)}{random.choice(objects)}的{random.choice(adj)}方面"
    elif t == 7: s = f"以{random.choice(modifiers)}方式{random.choice(verbs)}{random.choice(domains)}{random.choice(objects)}"
    elif t == 8: s = f"为什么{random.choice(objects)}需要{random.choice(verbs)}？从{random.choice(domains)}角度"
    elif t == 9: s = f"对比{random.choice(modifiers)}和{random.choice(modifiers)}{random.choice(verbs)}的优劣"
    elif t == 10: s = f"如何{random.choice(modifiers)}{random.choice(verbs)}{random.choice(domains)}的{random.choice(objects)}"
    else: s = f"{random.choice(adj)}的{random.choice(objects)}在{random.choice(domains)}中如何{random.choice(verbs)}"
    intents.append(s)

print(f"编码 {N} 个意图...")
model = SentenceTransformer("answerdotai/ModernBERT-base", device=DEVICE)
emb = model.encode(intents, normalize_embeddings=True)

pca = PCA(n_components=min(FULL_DIM, N))
pca.fit(emb)
EFF_DIM = pca.n_components_

def cos_at_d(pca, emb, d):
    c = pca.transform(emb)[:,:d]
    recon = np.zeros_like(emb)
    for i in range(len(emb)):
        for j in range(d):
            recon[i] += c[i,j] * pca.components_[j]
    recon += pca.mean_
    nr = np.linalg.norm(recon, axis=1, keepdims=True)
    nr[nr==0] = 1
    recon /= nr
    return np.mean([np.dot(emb[i], recon[i]) for i in range(len(emb))])

# 找D₀
D0 = None
for d in range(EFF_DIM, 0, -2):
    avg = cos_at_d(pca, emb, d)
    if avg < TARGET:
        D0 = d + 2
        break
if D0 is None: D0 = 2

print(f"语义 D₀ (τ={TARGET}) = {D0}")
print()

dim_list = sorted([D0, D0//2, D0//4, D0//8, D0//16], reverse=True)
dim_list = [d for d in dim_list if d >= 2]
print(f"{'d':>4s} {'轮次':>4s} {'d×r':>5s} {'cos_sim':>8s} {'Δ/D₀':>6s}")
print("-" * 40)
for d in dim_list:
    r = int(np.ceil(D0 / d))
    total = r * d
    cos = cos_at_d(pca, emb, min(total, FULL_DIM))
    print(f"{d:4d} {r:4d} {total:5d} {cos:8.4f} {total-D0:+6d}")

vals = [int(np.ceil(D0/d))*d for d in dim_list]
print(f"\nC ≈ {np.mean(vals):.1f} ± {np.std(vals):.1f}")
