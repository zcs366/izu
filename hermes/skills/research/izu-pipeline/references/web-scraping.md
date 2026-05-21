# 网页抓取方案

## 当前状态

"搜"角色目前只基于 DuckDuckGo 搜索摘要进行分析，没有真正抓取网页全文。这导致后续"修"角色在需要具体来源时虚构数据。

## 方案一：curl_cffi（推荐）

```python
from curl_cffi import requests

def fetch_page(url):
    """抓取网页全文，绕过反爬"""
    resp = requests.get(url, 
        impersonate="chrome120",
        timeout=30,
        proxy="http://127.0.0.1:7890"
    )
    return resp.text[:10000]  # 截取前10000字符
```

已安装：`pip install curl_cffi`（2026-05-09验证）

## 方案二：agent-browser（备用）

```bash
~/.hermes/hermes-agent/node_modules/.bin/agent-browser navigate "URL"
~/.hermes/hermes-agent/node_modules/.bin/agent-browser snapshot
```

局限：对重度SPA（如n8n Cloud）可能返回空。

## 方案三：终端curl（备用的备用）

```bash
curl -sL --max-time 15 -x http://127.0.0.1:7890 "URL" | head -c 10000
```

局限：部分站点返回403或空响应。WSL环境下DNS可能有问题。

## 集成到流水线

在 `izu-pipeline.py` 的 `run_search()` 中：

```python
# 在"深度钻"步骤抓取前3个URL的全文
for url in top3_urls:
    try:
        full_text = fetch_page(url)
        # 将全文传给"搜"角色
    except:
        # 降级到摘要
        pass
```

## 来源标注规范

所有来源必须三级标注：
- ✅ 真实来源：有URL、curl抓取验证、原文可引用
- ⚠️ 推断数据：基于多个真实来源的合理推断
- ❓ 猜测数据：有趣但缺乏证据——必须显式标注"以下为猜测"
