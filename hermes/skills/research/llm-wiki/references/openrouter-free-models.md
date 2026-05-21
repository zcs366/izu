# OpenRouter Free Models

> Verified 2026-05-08 via `curl https://openrouter.ai/api/v1/models`
> 28 models currently free (pricing.prompt = "0")

## Recommended for Wiki Operations

| Model ID | Params | Context | Best For | Speed |
|----------|--------|---------|----------|-------|
| `google/gemma-4-31b-it:free` | 31B Dense | 32K | **Primary choice** — balanced reasoning, speed, Chinese | Fast |
| `nvidia/nemotron-3-super-120b-a12b:free` | 120B MoE | **1M** | Ultra-long docs, full books | Slow (cold start) |
| `meta-llama/llama-3.3-70b-instruct:free` | 70B Dense | 128K | Knowledge-rich synthesis | Medium |
| `qwen/qwen3-coder:free` | ? | 128K | Code-related wiki content | Fast |
| `qwen/qwen3-next-80b-a3b-instruct:free` | 80B MoE | ? | Chinese-heavy content | Medium |
| `google/gemma-4-26b-a4b-it:free` | 26B MoE | ? | Lightweight reasoning | Fast |
| `google/lyria-3-pro-preview` | ? | ? | Preview model | Medium |
| `google/lyria-3-clip-preview` | ? | ? | Preview model | Medium |
| `openrouter/free` | Auto-routed | varies | Testing only — unpredictable model | Varies |
| `openrouter/owl-alpha` | ? | ? | Experimental | Varies |

## Other Free Models (Less Suitable for Wiki)

| Model ID | Notes |
|----------|-------|
| `baidu/cobuddy:free` | Baidu chatbot — not general-purpose |
| `baidu/qianfan-ocr-fast:free` | OCR only |
| `tencent/hy3-preview:free` | Tencent preview |
| `minimax/minimax-m2.5:free` | General chat |
| `liquid/lfm-2.5-1.2b-thinking:free` | 1.2B — too small for wiki work |
| `liquid/lfm-2.5-1.2b-instruct:free` | 1.2B — too small |
| `nvidia/nemotron-3-nano-30b-a3b:free` | Smaller Nemotron variant |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Reasoning variant |
| `nvidia/nemotron-nano-12b-v2-vl:free` | Vision-language |
| `nvidia/nemotron-nano-9b-v2:free` | 9B — lightweight |
| `openai/gpt-oss-120b:free` | OpenAI OSS 120B |
| `openai/gpt-oss-20b:free` | OpenAI OSS 20B |
| `z-ai/glm-4.5-air:free` | GLM lite |
| `poolside/laguna-xs.2:free` | Code-focused |
| `poolside/laguna-m.1:free` | Code-focused |
| `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` | Uncensored variant |
| `meta-llama/llama-3.2-3b-instruct:free` | 3B — too small |
| `nousresearch/hermes-3-llama-3.1-405b:free` | 405B — huge but slow |

## Model Selection Decision Tree

```
Need to ingest a source?
├── Short article / normal web page → google/gemma-4-31b-it:free
├── Long document (32K-1M tokens) → nvidia/nemotron-3-super-120b-a12b:free
├── Chinese-heavy / coding content → qwen/qwen3-coder:free
├── Quality degradation on free model → swap to gpt-4.1-mini (paid)
└── Batch ingest (5+ sources) → gemma-4 (fastest throughput)
```

## Verification Commands

```bash
# Test model availability
source ~/.hermes/.env && \
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "google/gemma-4-31b-it:free",
    "messages": [{"role":"user","content":"hi"}],
    "max_tokens": 10
  }'

# List current free models
curl -s https://openrouter.ai/api/v1/models | python3 -c "
import json,sys
data = json.load(sys.stdin)
models = data.get('data', data if isinstance(data, list) else [])
print(f'Total: {len(models)} | Free:', sum(1 for m in models if m.get(\"pricing\",{}).get(\"prompt\") == \"0\"))
for m in models:
    if m.get('pricing',{}).get('prompt') == '0':
        print(f'  {m[\"id\"]}')
"
```

## Pitfalls

- Free models can be deprecated without notice — re-check monthly
- Nemotron has 30-60s cold start latency (first request after idle period)
- `openrouter/free` routes to unpredictable models — never use for wiki ingest (inconsistent quality)
- Some free models have hidden rate limits (~10 req/min) — rotate across multiple models for batch jobs
