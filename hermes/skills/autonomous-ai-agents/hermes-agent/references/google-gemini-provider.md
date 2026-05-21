# Google Gemini Provider for Hermes Agent — Ground Truth (2026-05)

> ⚠️ **This reference was rewritten 2026-05-10 after extensive debugging.**  
> The Gemini direct provider has significant pitfalls in China/behind-proxy environments.  
> **For most users, the OpenRouter workaround is more reliable.**

---

## Two Ways to Use Gemini

| Method | Reliable? | Proxy needed? | Auth | Notes |
|--------|-----------|--------------|------|-------|
| **Direct `gemini` provider** | ⚠️ Partial | Native adapter bypasses proxy | API key via URL param | Fails in China without paid proxy-aware setup |
| **OpenRouter → Gemini** | ✅ Yes | OpenRouter already proxied | OpenRouter API key | Use `google/gemini-2.0-flash-001` model name |

---

## Method A: Direct Gemini Provider (Built-in)

### How it works

The built-in `gemini` provider (defined in `plugins/model-providers/gemini/__init__.py`) uses a **native Gemini adapter** (`gemini_native_adapter.py`), NOT the standard OpenAI chat-completions transport.

```python
gemini = GeminiProfile(
    name="gemini",
    aliases=("google", "google-gemini", "google-ai-studio"),
    api_mode="chat_completions",
    env_vars=("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta",  # native REST!
    auth_type="api_key",
)
```

The adapter detects which endpoint type to use via two complementary functions:

```python
# From chat_completions.py — determines extra_body format
def _is_gemini_openai_compat_base_url(base_url):
    normalized = str(base_url or "").strip().rstrip("/").lower()
    if not normalized: return False
    if "generativelanguage.googleapis.com" not in normalized: return False
    return normalized.endswith("/openai")     # <-- must end with /openai exactly

# From gemini_native_adapter.py — determines transport selection
def is_native_gemini_base_url(base_url):
    normalized = str(base_url or "").strip().rstrip("/").lower()
    if not normalized: return False
    if "generativelanguage.googleapis.com" not in normalized: return False
    return not normalized.endswith("/openai")  # <-- inverse of above
```

**Key behavior**:
- If base_url ends with `/openai` → OpenAI-compatible transport (Bearer auth, `Authorization: Bearer <key>`)
- If base_url does **NOT** end with `/openai` → Native REST transport (key as query param `?key=<key>`)

### URL Rules

```
                    Ends with /openai  →  /v1beta/openai   ← Correct for compat
                    Ends with /openai/v1 → ❌ Does NOT match! Falls back to native!
```

**Critical pitfall**: The check is `endswith("/openai")`. If your URL is `.../v1beta/openai/v1`, it does NOT end with `/openai` — it ends with `/v1`. The adapter falls back to native mode, sends a REST-format request to the compat endpoint, and gets a 404 or bad-request error.

### The probe_gemini_tier() problem

On startup, Hermes runs `probe_gemini_tier()` which sends a probe request to the Google API to determine if the key is free/paid tier:

```python
def probe_gemini_tier(api_key, base_url, ...):
    # Strips /openai from URL if present
    normalized_base = str(base_url or DEFAULT_GEMINI_BASE_URL).strip().rstrip("/")
    if normalized_base.lower().endswith("/openai"):
        normalized_base = normalized_base[:-len("/openai")]
    url = f"{normalized_base}/models/{model}:generateContent"
    
    with httpx.Client(timeout=timeout) as client:      # <-- NO PROXY!
        resp = client.post(url, params={"key": key}, json=payload, ...)
```

The probe:
- Uses `httpx.Client()` — does NOT read `http_proxy`/`https_proxy` env vars
- Sends the API key as a URL query parameter (native format)
- In China, this call **always times out** without a proxy → returns `"unknown"` tier
- Does NOT block usage — but signals the environment isn't fully set up

### Why direct provider fails in China (the triple wall)

```
1. httpx.Client() doesn't use proxy → probe times out
2. Even if URL ends with /openai/v1 instead of /openai → wrong transport selected
3. Even with correct URL → OpenAI-compat transport needs Bearer auth, 
   but adapter sometimes still sends native-style requests
```

**Result**: You get "API key not valid" 400 errors even though the key is perfectly valid when tested with curl.

### Working config.yaml (if you must use direct)

```yaml
providers:
  google:
    base_url: https://generativelanguage.googleapis.com/v1beta/openai
    key_env: GOOGLE_API_KEY
```

Note: No `/v1` suffix. `key_env` tells the credential pool which env var to read.

---

## Method B: OpenRouter → Gemini (✅ Recommended)

The most reliable way to use Gemini is through OpenRouter, which handles auth, proxy, and routing.

### Model names

Use OpenRouter's `google/gemini-xxx` naming:

| Model | OpenRouter name | Verified |
|-------|----------------|----------|
| Gemini 2.0 Flash | `google/gemini-2.0-flash-001` | ✅ 2026-05-10 |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | Benchmarked |
| Gemini 2.5 Pro | `google/gemini-2.5-pro` | — |
| Gemini 3 Flash Preview | `google/gemini-3-flash-preview` | — |
| Gemini 3.1 Pro Preview | `google/gemini-3.1-pro-preview` | — |

Full list via API:
```bash
curl -s --proxy http://127.0.0.1:7890 \
  "https://openrouter.ai/api/v1/models" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | \
  python3 -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['data'] if 'gemini' in m['id']]"
```

### Usage

```bash
# One-shot
hermes chat -m "google/gemini-2.0-flash-001"

# With explicit provider
hermes chat --provider openrouter -m "google/gemini-2.5-flash"

# Switch default
hermes config set model.default google/gemini-2.0-flash-001
hermes config set model.provider openrouter
```

### How to swap between DeepSeek and Gemini

Keep DeepSeek as default (fast for daily use), switch to Gemini when needed:

```bash
# DeepSeek (default)
hermes chat

# Gemini via OpenRouter
hermes chat -m "google/gemini-2.0-flash-001"
```

Both DeepSeek and OpenRouter use the same API key pattern (Bearer token), so no auth switching is needed.

---

## Diagnosis: The "API key not valid" Error Wall

### Symptom
- `hermes chat --provider google -m gemini-2.0-flash` → `400 API key not valid`
- Same key works with `curl --proxy ... -H "Authorization: Bearer $KEY"`

### Root causes (check in order)

| # | Check | How to verify | Fix |
|---|-------|--------------|-----|
| 1 | Proxy missing | `curl ... --proxy http://127.0.0.1:7890 ...` → works without proxy? Timed out? | Add proxy env or use OpenRouter |
| 2 | URL ends with `/v1` | Check config.yaml: `base_url` should end with `/openai` not `/openai/v1` | Trim the `/v1` |
| 3 | Key not in `.env` | `grep 'GOOGLE_API_KEY' ~/.hermes/.env` | Add key |
| 4 | Free tier exhausted | `curl` test returns 429 | Wait for reset or upgrade |

### The nuclear option

If direct provider keeps failing after all checks pass, **switch to OpenRouter routing** (Method B above). It bypasses the Gemini native adapter entirely and just routes through OpenRouter's proven infrastructure.

---

## Direct API Test (curl, always works)

```bash
# Test key validity + proxy
curl -s --proxy http://127.0.0.1:7890 \
  "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions" \
  -H "Authorization: Bearer $GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"model":"gemini-2.0-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

If this works but Hermes doesn't, the issue is in Hermes' native adapter → use OpenRouter.

---

## Pitfalls (updated ground truth)

- **❗ OpenRouter model names use `google/gemini-xxx` prefix**: Not `gemini-xxx`. The exact name matters — `google/gemini-2.0-flash-001` works, `google/gemini-2.0-flash` may not.
- **❗ Base URL must end with `/openai` exactly**: Not `/openai/v1`. The detection function `_is_gemini_openai_compat_base_url()` checks `endswith("/openai")`. Adding `/v1` silently switches transport modes.
- **❗ Native adapter probe ignores proxy**: `probe_gemini_tier()` uses `httpx.Client()` which doesn't read `http_proxy`. This always times out behind a proxy but doesn't block usage.
- **❗ Free tier quota is per-model, per-day**: All free models share the same daily limit. 429 errors mean quota exhausted for the day.
- **❗ `gemini-flash-latest` resolves at request time**: May point to different models over time. Pin to exact version.
**❗ The built-in `gemini` provider has `google` as an alias**: `--provider google` and `--provider gemini` both resolve to the same built-in provider plugin.
- **❗ `.env` env vars are NOT auto-sourced into shell**: While Hermes reads `.env` internally via `load_env()`, the shell environment doesn't have them. Use `hermes` CLI (which loads `.env`) rather than raw Python/curl that depends on shell env vars.
