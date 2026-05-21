#!/usr/bin/env python3
"""
izu_checkpoint.py — Cross-Review Loop 检查点引擎 v0.1
首节点：CP2（搜→织）信源充分度评分

哲学：代码做计数/分级/日期，LLM做相关性判断。
不达标 → 输出缺什么（等级/相关度/时效）→ 上游重搜。
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PASS_THRESHOLD = 7.0
MAX_RETRIES = 3
LOG_PATH = Path.home() / ".hermes" / "izu_checkpoint_log.json"
TIER1_DOMAINS = {
    "arxiv.org", "github.com", "openai.com", "anthropic.com",
    "deepseek.com", "nousresearch.com", "nature.com", "science.org",
    "acm.org", "ieee.org", "papers.nips.cc", "jmlr.org",
    "dl.acm.org", "proceedings.mlr.press", "neurips.cc"
}
TIER2_DOMAINS = {
    "medium.com", "towardsdatascience.com", "dev.to", "hashnode.com",
    "blog.google", "ai.googleblog.com", "research.google",
    "meta.com", "about.fb.com", "engineering.fb.com",
    "huggingface.co", "pytorch.org", "tensorflow.org",
    "mp.weixin.qq.com", "zhuanlan.zhihu.com",
    "theverge.com", "techcrunch.com", "wired.com", "arstechnica.com"
}

def load_search_results(filepath):
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"搜结果文件不存在: {filepath}")
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
        if isinstance(data, list): return data
        elif isinstance(data, dict) and "results" in data: return data["results"]
    except json.JSONDecodeError:
        pass
    results = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = line.split("|", 2)
        if len(parts) >= 1:
            results.append({"url": parts[0].strip(), "title": parts[1].strip() if len(parts) > 1 else "", "snippet": parts[2].strip() if len(parts) > 2 else ""})
    return results

def extract_domain(url):
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1).replace("www.", "") if match else ""

def get_tier(domain):
    if domain in TIER1_DOMAINS or any(d in domain for d in ["arxiv", "github", ".edu", ".gov"]): return 1
    if domain in TIER2_DOMAINS or any(d in domain for d in ["blog.", "research.", "engineering."]): return 2
    return 3

def extract_date_from_snippet(snippet):
    patterns = [r'(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})', r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(20\d{2})', r'(20\d{2})']
    for pat in patterns:
        m = re.search(pat, snippet, re.IGNORECASE)
        if m: return m.group(0)
    return None

def code_score(results):
    urls = [r.get("url", "") for r in results]
    snippets = [r.get("snippet", "") for r in results]
    domains = [extract_domain(u) for u in urls if u]
    tiers = [get_tier(d) for d in domains]
    count = len(urls)
    count_score = min(10, count * 2)
    t1_count = sum(1 for t in tiers if t == 1)
    t2_count = sum(1 for t in tiers if t == 2)
    tier_score = min(10, t1_count * 4 + t2_count * 2)
    dates_found = []
    for s in snippets:
        d = extract_date_from_snippet(s)
        if d: dates_found.append(d)
    recent = sum(1 for d in dates_found if "2026" in d or "2025" in d)
    freshness_score = min(10, recent * 3 + len(dates_found))
    return {"count": count, "count_score": round(count_score, 1), "t1_count": t1_count, "t2_count": t2_count, "tier_score": round(tier_score, 1), "dates_found": len(dates_found), "recent_dates": recent, "freshness_score": round(freshness_score, 1), "domains": domains, "tiers": tiers, "urls": urls}

def llm_relevance_prompt(results, research_topic):
    items = []
    for r in results[:10]:
        items.append(f"- [{r.get('title', '无标题')}]({r.get('url', '')})：{r.get('snippet', '')[:200]}")
    return f"""你是 izu 流水线的"织"角色，负责审核搜索结果的质量。

研究主题：{research_topic}

搜索结果（{len(results)}条）：
{chr(10).join(items)}

请做三件事：
1. 逐条判断相关性（直接相关/间接相关/不相关）
2. 判断信源等级是否足以支撑深度研究（是否缺T1级信源？是否过度依赖微信/知乎？）
3. 给"与问题的相关度"打分（0-10）

输出格式（严格 JSON）：
{{"relevance_score": 7.5, "direct_count": 5, "indirect_count": 3, "irrelevant_count": 2, "tier_feedback": "缺T1级学术信源，微信占60%", "missing_angles": ["缺少学术论文角度", "缺少产业报告角度"]}}

只输出 JSON，不输出其他内容。"""

def compute_final_score(code, llm):
    relevance_score = float(llm.get("relevance_score", 5))
    final = (code["count_score"] * 0.20 + code["tier_score"] * 0.30 + relevance_score * 0.30 + code["freshness_score"] * 0.20)
    return {"final_score": round(final, 1), "passed": final >= PASS_THRESHOLD, "breakdown": {"count": (code["count_score"], 0.20), "tier": (code["tier_score"], 0.30), "relevance": (relevance_score, 0.30), "freshness": (code["freshness_score"], 0.20)}, "t1_count": code["t1_count"], "t2_count": code["t2_count"], "direct_count": llm.get("direct_count", 0), "indirect_count": llm.get("indirect_count", 0), "tier_feedback": llm.get("tier_feedback", ""), "missing_angles": llm.get("missing_angles", [])}

def log_checkpoint(node, score_data, retry_count):
    entry = {"timestamp": datetime.now().isoformat(), "node": node, "score": score_data["final_score"], "passed": score_data["passed"], "retry": retry_count, "breakdown": score_data["breakdown"], "tier_feedback": score_data.get("tier_feedback", ""), "missing_angles": score_data.get("missing_angles", [])}
    log = []
    if LOG_PATH.exists():
        try: log = json.loads(LOG_PATH.read_text())
        except json.JSONDecodeError: log = []
    log.append(entry)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2))

def check_cp2(results_file, research_topic, retry_count=0):
    results = load_search_results(results_file)
    code = code_score(results)
    needs_llm = code["t1_count"] == 0 or code["count"] < 4
    return {"code_scores": code, "needs_llm": needs_llm, "research_topic": research_topic, "results_count": len(results), "llm_prompt": llm_relevance_prompt(results, research_topic) if needs_llm else None}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 izu_checkpoint.py cp2 <搜结果文件> <研究主题>")
        print("     python3 izu_checkpoint.py log  # 查看检查点日志")
        sys.exit(1)
    command = sys.argv[1]
    if command == "log":
        if LOG_PATH.exists():
            print(json.dumps(json.loads(LOG_PATH.read_text()), ensure_ascii=False, indent=2))
        else:
            print("暂无检查点日志")
        sys.exit(0)
    if command == "cp2":
        if len(sys.argv) < 4:
            print("用法: python3 izu_checkpoint.py cp2 <搜结果文件> <研究主题>")
            sys.exit(1)
        result = check_cp2(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))
