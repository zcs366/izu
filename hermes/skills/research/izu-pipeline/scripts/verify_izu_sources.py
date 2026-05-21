#!/usr/bin/env python3
"""
izu 管线信号源验证脚本

验证所有依赖的信号源是否就绪：
1. LLM API（MiniMax + DeepSeek）
2. 搜索（DuckDuckGo）
3. 网页抓取（curl_cffi）
4. Hermes 凭证池
5. 输出目录可写

用法: python3 verify_izu_sources.py

需先 source izu-env.sh 或设置环境变量:
  export IZU_API_KEY="sk-cp-..."
  export IZU_API_URL="https://api.minimax.chat/v1/chat/completions"
"""
import json, os, sys, requests

print("=" * 50)
print("izu 信号源验证")
print("=" * 50)

all_ok = True

# 1. LLM API
print("\n## 1. LLM API")
api_key = os.environ.get("IZU_API_KEY", "")
api_url = os.environ.get("IZU_API_URL", "")
model = os.environ.get("IZU_API_MODEL", "MiniMax-M2.7")
print(f"  Key: {'✅ 已设置' if api_key and len(api_key) > 20 else '❌ 未设置或太短'}")
print(f"  URL: {api_url or '❌ 未设置'}")
print(f"  Model: {model}")

try:
    r = requests.post(
        api_url, timeout=15,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 10}
    )
    ok = r.status_code == 200
    print(f"  API调用: HTTP {r.status_code} {'✅' if ok else '❌'}")
    all_ok &= ok
except Exception as e:
    print(f"  API调用失败: {e} ❌")
    all_ok = False

# 2. DuckDuckGo 搜索
print("\n## 2. DuckDuckGo 搜索")
try:
    from ddgs import DDGS
    with DDGS() as ddgs:
        results = list(ddgs.text("test query", max_results=3))
        print(f"  DDGS: {len(results)} 条结果 ✅")
except Exception as e:
    print(f"  DDGS: {e} ❌")
    all_ok = False

# 3. curl_cffi
print("\n## 3. 网页抓取 (curl_cffi)")
try:
    from curl_cffi import requests as curl_req
    r = curl_req.get("https://httpbin.org/status/200", impersonate="chrome110", timeout=10)
    print(f"  HTTP {r.status_code} {'✅' if r.status_code == 200 else '❌'}")
except Exception as e:
    print(f"  curl_cffi: {e} ❌")
    all_ok = False

# 4. 凭证池
print("\n## 4. Hermes 凭证池")
try:
    with open(os.path.expanduser("~/.hermes/auth.json")) as f:
        store = json.load(f)
    pool = store.get("credential_pool", {})
    valid_keys = 0
    for prov, entries in pool.items():
        for e in entries:
            tok = e.get("access_token", "")
            if len(tok) > 20:
                valid_keys += 1
    print(f"  有效key: {valid_keys} {'✅' if valid_keys > 0 else '❌'}")
    all_ok &= valid_keys > 0
except Exception as e:
    print(f"  {e} ❌")
    all_ok = False

# 5. 输出目录
print("\n## 5. 输出目录")
out_dir = "/mnt/i/hermes/output/izu-pipeline"
os.makedirs(out_dir, exist_ok=True)
ok = os.access(out_dir, os.W_OK)
print(f"  {out_dir}: {'✅ 可写' if ok else '❌ 不可写'}")
all_ok &= ok

print(f"\n{'=' * 50}")
print(f"总体结果: {'✅ 全部通过' if all_ok else '❌ 有失败项'}")
print(f"{'=' * 50}")
sys.exit(0 if all_ok else 1)
