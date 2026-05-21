# 从 Hermes 凭证池读取 API Key 的模式

> 2026-05-18 · 适用于所有需要 LLM API 的独立脚本（izu-pipeline.py, daily-research-orchestra.py 等）

## 问题

独立脚本（不跑在 Hermes Agent 内部）通过环境变量读 API key：
```python
API_KEY = os.environ.get("IZU_API_KEY") or ""
```

但 Hermes 本体用凭证池（`~/.hermes/auth.json`）管理密钥。两个问题：
1. 环境变量可能持有过期/占位符 key（`sk-82c...31ac` 仅 13 字符）
2. 凭证池中有真实 key 但脚本看不到

## 解决方案：`_load_pool_keys()`

```python
import os, json

_HERMES_AUTH_PATH = os.path.expanduser("~/.hermes/auth.json")

def _load_pool_keys():
    """从 Hermes auth.json 凭证池读取可用 API key。"""
    try:
        if not os.path.exists(_HERMES_AUTH_PATH):
            return {}
        with open(_HERMES_AUTH_PATH) as f:
            store = json.load(f)
        pool = store.get("credential_pool", {})
        result = {}
        for prov, entries in pool.items():
            for e in entries:
                tok = e.get("access_token", "")
                if tok and tok != "***" and len(tok) > 10:
                    if prov not in result:
                        result[prov] = {
                            "key": tok,
                            "base_url": e.get("base_url", ""),
                            "label": e.get("label", prov),
                        }
        return result
    except Exception:
        return {}

_POOL_KEYS = _load_pool_keys()
```

## 覆盖逻辑

环境变量 key 和凭证池 key 之间按此优先级决策：

```python
# 如果环境变量 key 明显是占位符（< 20 字符），用凭证池覆盖
if env_key in ("", "***") or len(env_key) < 20:
    pool_entry = _POOL_KEYS.get("deepseek", {}).get("key")
    if pool_entry:
        env_key = pool_entry
```

20 字符的经验阈值：
- Hermes 真实 API key 最短 ~35 字符（DeepSeek `sk-xxx`）
- 占位符/过期 key 通常 ≤13 字符（如 `sk-82c...31ac`）
- MiniMax CN key 长达 126 字符

## 多层 Fallback 链

```python
providers = [
    ("MiniMax", API_URL, API_KEY, model),           # 主 provider
    ("DeepSeek", FALLBACK_URL, FALLBACK_KEY, model), # 备用
]

# 第三层：从凭证池读 OpenRouter
or_pool = _POOL_KEYS.get("openrouter", {})
if or_pool.get("key"):
    base = or_pool["base_url"].rstrip("/")
    or_url = base + ("/chat/completions" if not base.endswith("/chat/completions") else "")
    providers.append(("OpenRouter", or_url, or_pool["key"], model))
```

## 诊断命令

```bash
# 检查冲突：环境变量 vs 凭证池
python3 -c "
import os, json
e = os.environ.get('IZU_FALLBACK_KEY', '')
print(f'ENV: len={len(e)}, prefix={e[:12]}')
d = json.load(open(os.path.expanduser('~/.hermes/auth.json')))
for entry in d.get('credential_pool', {}).get('deepseek', []):
    t = entry['access_token']
    print(f'POOL: len={len(t)}, prefix={t[:12]}, src={entry[\"source\"]}, lbl={entry[\"label\"]}')
"

# 测试 key 是否工作（Python requests，不走代理）
python3 -c "
import requests
resp = requests.post('https://api.deepseek.com/v1/chat/completions',
    headers={'Authorization': 'Bearer <KEY>', 'Content-Type': 'application/json'},
    json={'model': 'deepseek-chat', 'messages': [{'role':'user','content':'OK'}], 'max_tokens': 5},
    timeout=15)
print(resp.json()['choices'][0]['message']['content'] if 'choices' in resp.json() else resp.json())
"
```

## ⚠️ 代理陷阱

`.env` 中可能设了 `http_proxy=http://127.0.0.1:7890`。

- `curl` **会走代理** → 若代理干扰 HTTPS 请求，返回误导性 401
- Python `requests` **默认不走代理**（除非显式设置 `proxies=...`）

**不要用 curl 测试 API key 有效性。** 用 Python requests 代替。

```python
# 正确的测试方式
resp = requests.post(url, headers=headers, json=body, timeout=15)
```

## 已知提供凭证池中有效的 provider

| provider | key 来源 | 典型长度 | 状态 |
|----------|----------|----------|------|
| deepseek | `env:DEEPSEEK_API_KEY` + manual 备用 | 35 字符 | ✅ 已验证 |
| openrouter | `env:OPENROUTER_API_KEY` | 73 字符 | ✅ 已验证 |
| minimax-cn | `env:MINIMAX_CN_API_KEY` | 126 字符 | ❌ 可能过期 |
| nvidia | `env:NVIDIA_API_KEY` | 70 字符 | ✅ 存在 |
