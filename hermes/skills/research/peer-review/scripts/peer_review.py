#!/usr/bin/env python3
"""
同行评议agent v1.0 · 双模型交叉审读
MiniMax审方法/数据/统计 → 千问审文献/创新/术语 → 交叉比对 → 评议报告

用法：
  python3 peer_review.py <论文路径.md>
  python3 peer_review.py --text "论文全文..."  # 直接传入文本
"""
import sys, os, json, time, re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.hermes/.env"))

# === 配置 ===
MINIMAX_KEY = os.environ.get("MINIMAX_CN_API_KEY", "")
MINIMAX_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
MINIMAX_MODEL = "MiniMax-Text-01"

DASHSCOPE_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
DASHSCOPE_MODEL = "qwen-max"

OUTPUT_DIR = "/mnt/i/hermes/output/peer-review"

MINIMAX_PROMPT = """你是一位严苛的学术审稿人。请审读以下论文，从以下三个维度评分（每项0-10分），并给出具体理由：

1. 方法有效性：方法是否清晰？能不能复现？有没有明显漏洞？
2. 数据可信度：数据来源是否标注？样本量是否足够？统计检验是否正确？
3. 逻辑严密性：论证链是否完整？有没有逻辑跳跃？

请用以下格式回复：
【方法有效性】X分 — 理由
【数据可信度】X分 — 理由
【逻辑严密性】X分 — 理由
【综合判定】通过/存疑/不通过 — 一句话总结

论文内容：
"""

QWEN_PROMPT = """你是一位学术期刊的领域编辑。请审读以下论文，从以下三个维度评分（每项0-10分），并给出具体理由：

1. 文献覆盖：是否引用了该领域的关键工作？是否有明显遗漏？
2. 创新性：相比现有工作，这篇论文的贡献是什么？是增量改进还是突破？
3. 术语准确性：专业术语使用是否规范？是否有自创术语未定义？

请用以下格式回复：
【文献覆盖】X分 — 理由
【创新性】X分 — 理由
【术语准确性】X分 — 理由
【综合判定】通过/存疑/不通过 — 一句话总结

论文内容：
"""

TRUNCATION_LIMIT = 8000


def load_paper(path_or_text):
    if os.path.isfile(path_or_text):
        with open(path_or_text, 'r', encoding='utf-8') as f:
            return f.read()
    return path_or_text


def call_minimax(text):
    headers = {"Authorization": f"Bearer {MINIMAX_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MINIMAX_MODEL,
        "messages": [{"role": "user", "content": MINIMAX_PROMPT + text[:TRUNCATION_LIMIT]}],
        "temperature": 0.2, "max_tokens": 2000
    }
    resp = requests.post(MINIMAX_URL, headers=headers, json=payload, timeout=120)
    data = resp.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    return f"[MiniMax错误] {data}"


def call_qwen(text):
    headers = {"Authorization": f"Bearer {DASHSCOPE_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DASHSCOPE_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位严苛的学术审稿人。"},
            {"role": "user", "content": QWEN_PROMPT + text[:TRUNCATION_LIMIT]}
        ],
        "temperature": 0.1, "max_tokens": 2000
    }
    resp = requests.post(DASHSCOPE_URL, headers=headers, json=payload, timeout=120)
    data = resp.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    return f"[千问错误] {data}"


def parse_score(review_text, dimension):
    pattern = rf'【{dimension}】(\d+(?:\.\d+)?)\s*分'
    match = re.search(pattern, review_text)
    return float(match.group(1)) if match else None


def parse_verdict(review_text):
    match = re.search(r'【综合判定】(\S+)', review_text)
    return match.group(1) if match else "未知"


def cross_compare(mm_review, qw_review):
    mm_verdict = parse_verdict(mm_review)
    qw_verdict = parse_verdict(qw_review)
    mm_scores = {
        "方法有效性": parse_score(mm_review, "方法有效性") or 0,
        "数据可信度": parse_score(mm_review, "数据可信度") or 0,
        "逻辑严密性": parse_score(mm_review, "逻辑严密性") or 0,
    }
    qw_scores = {
        "文献覆盖": parse_score(qw_review, "文献覆盖") or 0,
        "创新性": parse_score(qw_review, "创新性") or 0,
        "术语准确性": parse_score(qw_review, "术语准确性") or 0,
    }
    mm_avg = sum(mm_scores.values()) / 3
    qw_avg = sum(qw_scores.values()) / 3
    total = (mm_avg * 0.55) + (qw_avg * 0.45)

    if mm_verdict == "通过" and qw_verdict == "通过":
        verdict = "✅ 入库·高信度"
    elif mm_verdict == "通过" or qw_verdict == "通过":
        verdict = "⚠️ 分歧·升级人工"
    else:
        verdict = "❌ 不入库"

    return {
        "mm_scores": mm_scores, "qw_scores": qw_scores,
        "mm_avg": round(mm_avg, 1), "qw_avg": round(qw_avg, 1),
        "total": round(total, 1),
        "mm_verdict": mm_verdict, "qw_verdict": qw_verdict,
        "final_verdict": verdict
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 peer_review.py <论文路径.md>"); sys.exit(1)
    path = sys.argv[1]
    paper = load_paper(path)
    title = os.path.basename(path) if os.path.isfile(path) else "直接输入"
    print(f"📄 论文: {title}  字数: {len(paper)}  截断: {TRUNCATION_LIMIT}字")
    t0 = time.time()
    with ThreadPoolExecutor() as executor:
        future_mm = executor.submit(call_minimax, paper)
        future_qw = executor.submit(call_qwen, paper)
        mm_review = future_mm.result(timeout=180)
        qw_review = future_qw.result(timeout=180)
    elapsed = time.time() - t0
    compare = cross_compare(mm_review, qw_review)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_title = re.sub(r'[^\w]', '_', title)[:40]
    report_path = os.path.join(OUTPUT_DIR, f"review_{safe_title}_{timestamp}.md")

    report = f"""# 同行评议报告\n\n**论文**: {title}\n**评议时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**模型**: MiniMax-Text-01 + Qwen-Max\n**耗时**: {elapsed:.1f}秒\n\n## MiniMax 评审\n\n{mm_review}\n\n## 千问 评审\n\n{qw_review}\n\n## 交叉比对\n\n| 维度 | MiniMax | 千问 |\n|------|---------|------|\n| 方法有效性 | {compare['mm_scores']['方法有效性']} | — |\n| 数据可信度 | {compare['mm_scores']['数据可信度']} | — |\n| 逻辑严密性 | {compare['mm_scores']['逻辑严密性']} | — |\n| 文献覆盖 | — | {compare['qw_scores']['文献覆盖']} |\n| 创新性 | — | {compare['qw_scores']['创新性']} |\n| 术语准确性 | — | {compare['qw_scores']['术语准确性']} |\n| **均分** | **{compare['mm_avg']}** | **{compare['qw_avg']}** |\n\n| 判定 | MiniMax | 千问 |\n|------|---------|------|\n| 各自判定 | {compare['mm_verdict']} | {compare['qw_verdict']} |\n\n### 最终判定: {compare['final_verdict']}\n### 加权总分: {compare['total']}/10\n\n> 双模型同行评议 v1.0 · 鲁班超级专家团\n"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📋 最终判定: {compare['final_verdict']}  加权总分: {compare['total']}/10  耗时: {elapsed:.1f}秒\n   报告: {report_path}")

if __name__ == "__main__":
    main()
