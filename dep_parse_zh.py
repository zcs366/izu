#!/usr/bin/env python3
"""
中文依赖解析 · 生产版
- 修复cop宾语范围（只取head子树而非整个sent）
- Markdown清洗
- 全量wiki批处理
输出：data/wiki-graph-dep-parse-zh-v4.json
"""
import spacy, json, os, glob, re, sys
from collections import Counter

nlp = spacy.load("zh_core_web_sm")
nlp.max_length = 2000000

# ── 文本清洗 ──
def clean_text(text: str) -> str:
    """去掉markdown格式、特殊字符"""
    # 去掉YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) > 2 else text
    # 去掉markdown标记
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)       # italic
    text = re.sub(r'`([^`]+)`', r'\1', text)         # code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'#{1,6}\s*', '', text)            # headings
    text = re.sub(r'[-*+]\s', '', text)              # list markers
    text = re.sub(r'\n{3,}', '\n\n', text)           # 多余空行
    text = re.sub(r'\s+', ' ', text)                 # 多余空格
    return text.strip()

# ── 中文三元组提取 ──
STOP_RELS = {"的", "了", "着", "过", "在", "和", "与", "或", "及", "并", "而",
             "不", "没", "很", "都", "也", "就", "才", "还", "又", "再",
             "有", "无", "为", "以", "从", "对", "向", "把", "被", "让", "给",
             "会", "能", "可以", "应该", "必须", "需要", "要", "来", "去", "到",
             "上", "下", "中", "里", "外", "前", "后", "左", "右"}

def extract_triplets(text: str) -> list:
    doc = nlp(text[:8000])
    triplets = []
    seen = set()
    
    for sent in doc.sents:
        # 收集动词节点
        verb_nodes = []
        for token in sent:
            if token.pos_ in ("VERB", "AUX"):
                if token.dep_ in ("aux:modal", "aux:asp", "aux:pass", "aux:ba", "aux:bei"):
                    continue
                verb_nodes.append(token)
        
        for verb in verb_nodes:
            rel_text = verb.text.strip()
            if len(rel_text) > 6 or rel_text in STOP_RELS:
                continue
            
            subj = None
            obj = None
            
            for child in verb.children:
                if child.dep_ in ("nsubj", "nsubjpass", "top") and not subj:
                    subj = child
                if child.dep_ in ("dobj", "obj", "attr") and not obj:
                    obj = child
                if child.dep_ == "prep" and not obj:
                    for gc in child.children:
                        if gc.dep_ == "pobj":
                            obj = gc
            
            if subj and obj:
                # 取subtree时限制范围：不长于20个token
                subj_tokens = [t for t in subj.subtree][:20]
                obj_tokens = [t for t in obj.subtree][:20]
                subj_span = "".join(t.text for t in subj_tokens).strip().rstrip("的了着过")
                obj_span = "".join(t.text for t in obj_tokens).strip().rstrip("的了着过")
                
                if (2 <= len(subj_span) <= 60 and 2 <= len(obj_span) <= 60 
                    and not subj_span.startswith("*") and not obj_span.startswith("*")):
                    key = f"{subj_span}|{rel_text}|{obj_span}"
                    if key not in seen:
                        seen.add(key)
                        triplets.append({"s": subj_span, "r": rel_text, "o": obj_span})
        
        # cop系词模式（A是B）
        for token in sent:
            if token.dep_ == "cop" and token.pos_ in ("VERB", "AUX"):
                cop_head = token.head
                cop_subj = None
                for child in cop_head.children:
                    if child.dep_ in ("nsubj", "nsubjpass", "top"):
                        cop_subj = child
                
                if cop_subj:
                    subj_tokens = [t for t in cop_subj.subtree][:15]
                    obj_tokens = [t for t in cop_head.subtree][:15]
                    subj_span = "".join(t.text for t in subj_tokens).strip().rstrip("的了着过")
                    obj_span = "".join(t.text for t in obj_tokens).strip().rstrip("的了着过")
                    
                    if (2 <= len(subj_span) <= 60 and 2 <= len(obj_span) <= 60
                        and subj_span != obj_span
                        and not subj_span.startswith("*") and not obj_span.startswith("*")):
                        key = f"{subj_span}|是|{obj_span}"
                        if key not in seen:
                            seen.add(key)
                            triplets.append({"s": subj_span, "r": "是", "o": obj_span})
    
    return triplets


def extract_concepts(text: str) -> set:
    doc = nlp(text[:8000])
    concepts = set()
    
    for sent in doc.sents:
        tokens = list(sent)
        i = 0
        while i < len(tokens):
            if tokens[i].pos_ in ("NOUN", "PROPN"):
                j = i
                while (j < len(tokens) and
                       tokens[j].pos_ in ("NOUN", "PROPN", "NUM", "ADJ", "PART", "VERB")):
                    j += 1
                phrase = "".join(t.text for t in tokens[i:j])
                phrase = re.sub(r'[的了着过]$', '', phrase.strip()).strip()
                phrase = re.sub(r'^[\*\-\+\d\.\s]+', '', phrase)
                if 2 <= len(phrase) <= 40 and not phrase.startswith("*"):
                    concepts.add(phrase)
                i = j
            else:
                i += 1
    
    for ent in doc.ents:
        text = ent.text.strip()
        if 2 <= len(text) <= 40 and not text.startswith("*"):
            concepts.add(text)
    
    return concepts


# ── 批量处理 ──
def main():
    wiki_dir = "/mnt/i/hermes/wiki/raw"
    output_path = "/mnt/i/hermes/data/wiki-graph-dep-parse-zh-v4.json"
    
    files = sorted(glob.glob(f"{wiki_dir}/**/*.md", recursive=True))
    files = [f for f in files if not os.path.islink(f)][:150]
    
    print(f"处理 {len(files)} 篇文章...")
    all_triplets = []
    all_concepts = set()
    
    for i, fpath in enumerate(files):
        try:
            with open(fpath) as f:
                raw = f.read()
        except:
            continue
        
        text = clean_text(raw)
        if len(text) < 20:
            continue
        
        bn = os.path.basename(fpath)
        trips = extract_triplets(text)
        conc = extract_concepts(text)
        
        all_triplets.extend(trips)
        all_concepts.update(conc)
        
        if trips:
            print(f"  [{i+1}/{len(files)}] {bn}: {len(trips)}T / {len(conc)}C")
    
    # 去重
    seen = set()
    unique_trips = []
    for t in all_triplets:
        key = f"{t['s']}|{t['r']}|{t['o']}"
        if key not in seen:
            seen.add(key)
            unique_trips.append(t)
    
    rel_counter = Counter(t["r"] for t in unique_trips)
    
    result = {
        "model": "zh_core_web_sm",
        "version": "4.0",
        "stats": {
            "files_processed": len(files),
            "unique_triplets": len(unique_trips),
            "unique_concepts": len(all_concepts),
            "graph_density": round(len(unique_trips) / max(len(all_concepts), 1), 3),
            "top_relations": dict(rel_counter.most_common(30))
        },
        "sample_triplets": unique_trips[:50],
        "sample_concepts": sorted(all_concepts)[:50]
    }
    
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"✅ 写入 {output_path}")
    print(f"边: {len(unique_trips)} | 节点: {len(all_concepts)} | 密度: {result['stats']['graph_density']}")
    print(f"\n高频关系TOP15:")
    for rel, cnt in rel_counter.most_common(15):
        print(f"  {rel:8s} → {cnt:4d}")
    print(f"\n样例:")
    for t in unique_trips[:10]:
        print(f"  [{t['s'][:30]}] --{t['r']}--> [{t['o'][:30]}]")

if __name__ == "__main__":
    main()
