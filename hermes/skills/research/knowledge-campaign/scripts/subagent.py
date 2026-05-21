#!/usr/bin/env python3
"""
三智能体管道·子任务脚本 v0.4.1
直接调用 DeepSeek API，绕过 delegate_task 缓存问题。
「搜」角色现在内置 DuckDuckGo 搜索，不再仅靠 LLM 训练数据。

改动 (v0.4.1):
  - 已废弃"搜"角色改为手动搜索+LLM总结的工作模式
  - 新增 ddgs_search()：内置 DuckDuckGo 搜索，最多 8 条结果
  - 新增 fetch_url_text()：curl 抓取网页正文
  - roll_collect(): 搜索=>抽取=>总结，将真实搜索结果注入 LLM prompt
  - 模型从 deepseek-v4-flash 改为 deepseek-chat（更稳定，支持更长的上下文）
  - 错误处理：API 超时/错误时回退到 LLM 备用知识
"""
import sys, json, requests, subprocess, re, html, os

DEEPSEEK_KEY = "[REDACTED]"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"  # v0.4.1: 从 v4-flash 升级

SYSTEM_PROMPTS = {
    "搜": (
        "你是一个深度研究智能体，拥有联网搜索能力。"
        "你的任务是基于搜索结果和自身知识，收集详细、准确的资料。"
        "输出要结构化，关键数据注明来源，对每个引用的数据给出具体的背景（如发布日期、发布机构）。"
        "如果你找到的是自相矛盾的信息，同时展示双方。"
    ),
    "写": (
        "你是一个写作智能体。根据搜集到的资料，输出一篇结构清晰、通俗易懂的文章。"
        "面向非专业读者，避免术语堆砌。开头一锤定音，每段有画面，结尾推开一扇窗。"
        "用户可能对某个具体的人/业务不熟悉——必须读取用户提供的上下文注入。"
        "如果用户业务信息（如'托管书法''国防基地'）显式注入了prompt，以注入信息为准，"
        "不要用训练数据中同名人物替代实际人物。"
    ),
    "劈": (
        "你是一个审读开劈智能体。你的任务是不留情面地批评给定的内容。"
        "找漏洞、找数据缺失、找逻辑断裂、找模棱两可的说法。不需要说好话。"
        "你需要像用户张成市那样劈：不留情、专找漏洞、质问来源、追究逻辑断裂。"
        "特别注意：文章是否准确理解了用户/业务的实际情况，还是用训练数据中的刻板印象替代了真实情况。"
    ),
}


# ---- 联网搜索工具 (v0.4.1 新增) ----

def ddgs_search(query: str, max_results: int = 8) -> list[dict]:
    """使用 DuckDuckGo 搜索，返回结果列表 [{title, url, snippet}, ...]"""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]
    except ImportError:
        # fallback: 用 curl 直接请求 ddg lite
        return _ddgs_curl_fallback(query, max_results)
    except Exception as e:
        return [{"title": f"[搜索失败: {e}]", "url": "", "snippet": ""}]


def _ddgs_curl_fallback(query: str, max_results: int = 8) -> list[dict]:
    """当 duckduckgo_search 包不可用时的 curl 降级方案"""
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://lite.duckduckgo.com/lite?q={encoded}"
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "10", url],
            capture_output=True, text=True, timeout=15
        )
        html_content = result.stdout
        # 从 HTML 表格中提取结果（DDG Lite 用表格布局）
        results = []
        snippets = re.findall(r'<tr>.*?class="[^"]*result-snippet[^"]*"[^>]*>(.*?)</tr>', html_content, re.DOTALL)
        for snip in snippets[:max_results]:
            clean = re.sub(r'<[^>]+>', '', snip).strip()
            clean = html.unescape(clean)
            if clean:
                results.append({"title": clean[:60], "url": "", "snippet": clean[:200]})
        if not results:
            # 备用：直接从纯文本提取
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = html.unescape(text)
            lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 30]
            for line in lines[:max_results]:
                results.append({"title": line[:60], "url": "", "snippet": line[:200]})
        return results
    except Exception as e:
        return [{"title": f"[搜索降级失败: {e}]", "url": "", "snippet": ""}]


def fetch_url_text(url: str, max_chars: int = 2000) -> str:
    """curl 抓取网页正文"""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "8", url],
            capture_output=True, text=True, timeout=10
        )
        text = re.sub(r'<[^>]+>', ' ', result.stdout)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except:
        return ""


def roll_collect(prompt: str, max_results: int = 8) -> str:
    """
    搜索 => 抓取 => LLM 总结：
    1. 用 prompt 中的关键词搜索
    2. 提取结果摘要
    3. 尝试抓取排名靠前的页面正文
    4. 将所有内容打包喂给 LLM 做结构化总结
    """
    # 提取搜索关键词：取 prompt 的前 120 字作为搜索词
    search_query = prompt[:120].strip()
    
    # 1. 搜索
    results = ddgs_search(search_query, max_results)
    
    if not results or (len(results) == 1 and results[0].get("title", "").startswith("[搜索")):
        # 搜索彻底失败，回退到纯 LLM
        return f"[INFO: 搜索不可用，将基于自身知识回答]\n\n用户问题: {prompt}"
    
    # 2. 构建搜索摘要
    parts = ["## 搜索结果\n"]
    for i, r in enumerate(results[:max_results], 1):
        parts.append(f"### [{i}] {r.get('title', '无标题')}")
        if r.get("url"):
            parts.append(f"来源: {r['url']}")
        if r.get("snippet"):
            parts.append(f"摘要: {r['snippet']}")
        parts.append("")
    
    # 3. 尝试抓取前 3 个页面的正文
    parts.append("## 抓取正文\n")
    for i, r in enumerate(results[:3], 1):
        if r.get("url") and r["url"].startswith("http"):
            text = fetch_url_text(r["url"], 2000)
            if text:
                parts.append(f"### [{i}] 正文 ({r['url']}):\n{text}\n")
    
    # 4. 加入用户原始 prompt
    parts.append(f"## 用户要求\n{prompt}")
    parts.append("\n请基于以上搜索结果和自身知识，给出结构化、带来源标注的回答。")
    
    return "\n".join(parts)


# ---- DeepSeek API 调用 ----

def call_deepseek(prompt, role="搜", temperature=0.7):
    system = SYSTEM_PROMPTS.get(role, SYSTEM_PROMPTS["搜"])
    
    # v0.4.1: "搜"角色先做真实搜索，再喂给 LLM
    if role == "搜":
        enriched = roll_collect(prompt)
        prompt = enriched
    
    resp = requests.post(
        DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": 4096,
        },
        timeout=300,
    )
    data = resp.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"ERROR: {json.dumps(data, ensure_ascii=False)}"


# ---- CLI 入口 ----

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: subagent.py <角色:搜|写|劈> <prompt>")
        sys.exit(1)

    role = args[0]
    prompt = " ".join(args[1:]) if len(args) > 1 else sys.stdin.read()

    result = call_deepseek(prompt, role)
    print(result)
