"""
Chomsky文法生成 → ModernBERT编码 → PCA压缩维度测量

每层500句，用文法生成器产生真正需要该层压缩能力的文本
  Type3: 正则 — 随机 (ab)* (cd)* 重复模式
  Type2: CF — 随机 aⁿbⁿ 嵌套
  Type1: CS — 随机 aⁿbⁿcⁿ 三约束
  Type0: RE — 伪随机生成（程序级复杂性）
"""
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import torch, random, time

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
N_PER_LEVEL = 500
TARGET_COS = 0.95

random.seed(42)
np.random.seed(42)

# ─── 文法生成器 ────────────────────────────────────
WORDS = ["猫","狗","鸟","鱼","马","牛","羊","鸡","鸭","鹅",
         "花","草","树","叶","山","水","云","雨","雪","风",
         "跑","飞","游","走","跳","叫","吃","喝","睡","醒",
         "红","蓝","绿","白","黑","大","小","高","低","长",
         "的","了","和","或","但","如果","那么","因为","所以","虽然"]

def gen_type3(n_sentences):
    """正则：随机词的有限重复模式 (AB)* """
    sentences = []
    for _ in range(n_sentences):
        a = random.choice(WORDS[:20])
        b = random.choice(WORDS[20:40])
        reps = random.randint(2, 8)
        s = (a + b) * reps
        sentences.append(s)
    return sentences

def gen_type2(n_sentences):
    """CF：aⁿbⁿ 嵌套 — 一对词的前后对称"""
    sentences = []
    for _ in range(n_sentences):
        a = random.choice(WORDS[:10])
        b = random.choice(WORDS[10:20])
        c = random.choice(WORDS[20:30])
        n_a = random.randint(2, 5)
        n_b = n_a  # 关键：aⁿbⁿ
        mid = random.choice(["的","和","但","所以"])
        s = a*n_a + mid + b*n_b + random.choice(WORDS[30:40])
        sentences.append(s)
    return sentences

def gen_type3_chinese(n_sentences):
    """正则中文：简单SVO + 重复修饰"""
    sentences = []
    subjects = ["猫","狗","鸟","鱼","马","孩子","老师","医生","工人","农民"]
    verbs = ["跑","飞","游","走","跳","吃","喝","看","听","说"]
    objects = ["花","草","树","山","水","饭","茶","书","画","歌"]
    adjs = ["红的","蓝的","大的","小的","高的","长的","快的","慢的","好的","新的"]
    for _ in range(n_sentences):
        s = random.choice(subjects)
        v = random.choice(verbs)
        o = random.choice(objects)
        # 简单重复修饰
        mod = random.choice(adjs)
        sentences.append(f"{mod}{s}{v}{mod}{o}")
    return sentences

def gen_type2_chinese(n_sentences):
    """CF中文：嵌套结构 「X的Y的Z」"""
    sentences = []
    for _ in range(n_sentences):
        depth = random.randint(2, 4)
        parts = []
        for _ in range(depth):
            parts.append(random.choice(WORDS[:20]))
        # 嵌套: X的Y的Z的W
        s = "的".join(parts)
        v = random.choice(WORDS[20:30])
        o = random.choice(WORDS[30:40])
        sentences.append(s + v + o)
    return sentences

def gen_type1_chinese(n_sentences):
    """CS中文：远距离一致 「X把Y的Z给V了」"""
    sentences = []
    for _ in range(n_sentences):
        who = random.choice(["我","你","他","她","他们","我们"])
        what = random.choice(["书","画","饭","茶","花","信","包","门","窗","灯"])
        whose = random.choice(["他的","她的","我的","你的","老师的","朋友的"])
        verb = random.choice(["拿","送","寄","放","关","开","买","卖","借","还"])
        # 把字句：远距离约束
        sentences.append(f"{who}把{whose}{what}给{verb}了")
    return sentences

def gen_type0_chinese(n_sentences):
    """RE中文：条件推理链 「如果A那么B因为C所以D除非E」"""
    sentences = []
    conds = ["如果下雨","如果堵车","如果迟到","如果失败","如果生病",
             "虽然困难","尽管危险","即使反对","无论结果","就算输了"]
    thens = ["就不去","就取消","就推迟","就放弃","就休息",
             "也要坚持","也要完成","也要出发","也要试试","也要开心"]
    becauses = ["因为太远","因为没钱","因为累了","因为不值得","因为没时间",
                "所以坚持","所以等待","所以努力","所以接受","所以改变"]
    consequences = ["所以算了","所以继续","所以停止","所以加速","所以减速",
                    "但是值得","但是无奈","但是无悔","但是遗憾","但是必要"]
    for _ in range(n_sentences):
        s = f"{random.choice(conds)}，{random.choice(thens)}，{random.choice(becauses)}，{random.choice(consequences)}"
        sentences.append(s)
    return sentences

# ─── 生成 ─────────────────────────────────────────
print("生成各层文本...")
levels = {
    'L1_正则': gen_type3_chinese(N_PER_LEVEL),
    'L2_CF':   gen_type2_chinese(N_PER_LEVEL),
    'L3_CS':   gen_type1_chinese(N_PER_LEVEL),
    'L4_RE':   gen_type0_chinese(N_PER_LEVEL),
}

all_texts = []
all_labels = []
for label, texts in levels.items():
    all_texts.extend(texts)
    all_labels.extend([label] * len(texts))

print(f"总计 {len(all_texts)} 句")

# ─── 编码 ─────────────────────────────────────────
print("编码...")
model = SentenceTransformer("answerdotai/ModernBERT-base", device=DEVICE)
emb = model.encode(all_texts, normalize_embeddings=True)
FULL_DIM = emb.shape[1]

# ─── 逐层PCA ─────────────────────────────────────
print(f"\n{'═'*60}")
print(f"Chomsky层级 × 压缩维度")
print(f"{'═'*60}")

for label in ['L1_正则', 'L2_CF', 'L3_CS', 'L4_RE']:
    mask = [l == label for l in all_labels]
    data = emb[mask]
    n = len(data)
    
    pca = PCA(n_components=min(FULL_DIM, n))
    pca.fit(data)
    
    def cos_at_d(d):
        d = min(d, pca.n_components_)
        c = pca.transform(data)[:,:d]
        r = c @ pca.components_[:d] + pca.mean_
        nr = np.linalg.norm(r, axis=1, keepdims=True); nr[nr==0]=1
        r /= nr
        return np.mean(np.sum(data*r, axis=1))
    
    # 扫描D₀（从小到大，找第一个达标的）
    D0 = min(FULL_DIM, n)
    for d in range(8, min(FULL_DIM, n)+1, 8):
        if cos_at_d(d) >= TARGET_COS:
            D0 = d
            break
    
    # 测多维度
    d_list = sorted(set(d for d in [D0, D0//2, D0//4, D0//8, D0//16] if d>=4), reverse=True)
    c_vals = []
    print(f"\n  {label} (n={n})")
    print(f"  D₀={D0}")
    print(f"  {'d':>5s} {'r':>3s} {'d×r':>5s} {'cos':>7s}")
    for d in d_list:
        r = int(np.ceil(D0 / d))
        total = r * d
        cos_v = cos_at_d(min(total, min(FULL_DIM, n)))
        c_vals.append(total)
        print(f"  {d:5d} {r:3d} {total:5d} {cos_v:7.4f}")
    print(f"  C = {np.mean(c_vals):.1f} ± {np.std(c_vals):.1f}")

# ─── 对比 ─────────────────────────────────────────
print(f"\n{'═'*60}")
print(f"结论：语义复杂度 ↔ 压缩维度的关系")
print(f"{'═'*60}")
print(f"  若 D₀ 随层级递增 → 验证「语义越复杂→需要越多压缩维度」")
print(f"  若 D₀ 不变 → ModernBERT 等距编码（所有层级坍缩到同一流形）")
print(f"  若 D₀ 随层级递减 → 意外发现（复杂结构的嵌入更紧凑）")
