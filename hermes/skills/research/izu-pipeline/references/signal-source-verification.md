# izu-pipeline 信号源验证清单

> 2026-05-21 · 用于 Phase 0 环境就绪检查 · 确保 pipeline 的所有外部依赖可用

## 验证层级

izu-pipeline 依赖三类信号源，按关键度降序：

```
LLM API (主) → LLM API (备用) → 搜索 (DDGS) → 网页抓取 (curl_cffi) → Hermes凭证池 (兜底)
```

## 快速验证脚本

```bash
cd /mnt/i/hermes && source scripts/izu-env.sh && python3 -c "
import os, json, requests

# 1. 环境变量
print('=== 1. 环境变量 ===')
for k in ['IZU_API_KEY', 'IZU_API_URL', 'IZU_API_MODEL', 'IZU_FALLBACK_KEY', 'IZU_FALLBACK_URL']:
    v = os.environ.get(k, 'NOT SET')
    print(f'  {k}: {\"OK (\"+str(len(v))+\" chars)\" if len(v)>10 else v[:20]}')

# 2. MiniMax API
print('=== 2. MiniMax API ===')
try:
    r = requests.post(os.environ.get('IZU_API_URL','https://api.minimax.chat/v1/chat/completions'),
        headers={'Authorization': f\"Bearer {os.environ.get('IZU_API_KEY','')}\", 'Content-Type': 'application/json'},
        json={'model': os.environ.get('IZU_API_MODEL','MiniMax-M2.7'), 'messages':[{'role':'user','content':'ping'}], 'max_tokens':10},
        timeout=15)
    print(f'  HTTP {r.status_code} {\"✅\" if r.status_code==200 else \"❌\"}')
except Exception as e:
    print(f'  ❌ {e}')

# 3. DuckDuckGo 搜索
print('=== 3. 搜索 (DDGS) ===')
try:
    from ddgs import DDGS
    with DDGS() as ddgs:
        results = list(ddgs.text('api test', max_results=3))
        print(f'  {len(results)} results ✅')
except Exception as e:
    print(f'  ❌ {e}')

# 4. curl_cffi 抓取
print('=== 4. curl_cffi ===')
try:
    from curl_cffi import requests as curl_req
    r = curl_req.get('https://httpbin.org/status/200', impersonate='chrome110', timeout=10)
    print(f'  HTTP {r.status_code} ✅')
except Exception as e:
    print(f'  ❌ {e}')

# 5. Hermes 凭证池
print('=== 5. 凭证池 ===')
try:
    with open(os.path.expanduser('~/.hermes/auth.json')) as f:
        store = json.load(f)
    pool = store.get('credential_pool', {})
    for prov, entries in pool.items():
        for e in entries:
            tok = e.get('access_token','')
            print(f'  {e.get(\"label\",prov)}: {len(tok)} chars {\"✅\" if len(tok)>20 else \"❌\"}')
except Exception as e:
    print(f'  ❌ {e}')

# 6. 输出目录
print('=== 6. 输出目录 ===')
d = '/mnt/i/hermes/output/izu-pipeline'
os.makedirs(d, exist_ok=True)
print(f'  {\"✅\" if os.access(d, os.W_OK) else \"❌\"} {d}')
"
```

## 验证结果判定

| 信号源 | 关键度 | 必须通过? | 备注 |
|--------|--------|-----------|------|
| MiniMax API | 🔴 主provider | 必须 | 所有LLM调用依赖此路 |
| DeepSeek备用 | 🟡 备用 | 建议 | 主API挂时自动降级 |
| DDGS搜索 | 🔴 必需 | 必须 | 探/搜/核三步都需要搜索 |
| curl_cffi | 🔴 必需 | 必须 | 探步骤需要抓取网页全文 |
| 凭证池 | 🟡 兜底 | 建议 | 环境变量key过期时的救命方案 |
| 输出目录 | 🟢 基础设施 | 必须 | 所有产出文件写入位置 |

## 常见失败模式

### 模式A：API 200但内容异常
- 症状：HTTP 200 但 `choices` 为空或 `finish_reason` 非 `stop`
- 排查：检查 `model` 名是否正确，MiniMax M2.7 用 `MiniMax-M2.7`

### 模式B：DDGS 返回 None
- 症状：搜索返回空列表，但 `ddgs` 包已安装
- 排查：代理问题。DDGS 默认走 `http_proxy`，如果代理宕机会超时
- 修复：`DDGS(proxy=None)` 跳过代理

### 模式C：API URL 被覆盖
- 症状：`source izu-env.sh` 后 `$IZU_API_URL` 和运行时读取的不同
- 排查：Hermes `.env` 或 `config.yaml` 的环境变量段覆盖了值
- 详见 izu-pipeline 陷阱六

### 模式D：curl_cffi 导入失败
- 症状：`ModuleNotFoundError: No module named 'curl_cffi'`
- 修复：`pip install curl_cffi`
- 注意：curl_cffi 需要 Rust 编译器（`apt install cargo`），安装较慢
