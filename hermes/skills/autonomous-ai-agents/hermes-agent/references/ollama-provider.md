# Ollama Provider Setup for Hermes Agent

Ollama runs locally and exposes an OpenAI-compatible API. This guide covers connecting Hermes Agent (running in WSL) to Ollama (running on the Windows host).

## Architecture

```
Windows (host)                    WSL (Hermes Agent)
┌─────────────────┐              ┌──────────────────────┐
│ Ollama          │  localhost   │ hermes (hermes)        │
│ port 11434      │─────────────▶│ config.yaml:          │
│ (OpenAI compat) │  WSL2 auto- │  ollama provider      │
└─────────────────┘  maps to    │  base_url:            │
                   │  Windows    │  http://localhost:    │
                   │   host      │  11434/v1             │
                   └─────────────┴──────────────────────┘
```

## Setup

### 1. Install Ollama on Windows

Download from [ollama.com](https://ollama.com/download/windows). Default install path:
```
C:\Users\<User>\AppData\Local\Programs\Ollama
```

Ollama runs as a Windows service (auto-start). Verify in system tray or via `ollama --version` in PowerShell.

### 2. Add Provider to Hermes config.yaml

Add to `~/.hermes/config.yaml`:

```yaml
providers:
  ollama:
    base_url: http://localhost:11434/v1
```

No API key needed (Ollama defaults to no auth).

### 3. Add to Fallback (optional)

```yaml
fallback_providers:
- openrouter
- ollama
```

### 4. Test Connection

From WSL:

```bash
# List available models
curl -s http://localhost:11434/v1/models

# Quick inference test
curl -s http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma2:latest","messages":[{"role":"user","content":"Say hello in 3 words"}],"max_tokens":20}'
```

### 5. Use in Hermes

```bash
# CLI
hermes -m ollama/qwen3:32b-q4_K_M

# Within session
/model ollama/qwen3:32b-q4_K_M

# Gateway (Telegram/Discord)
/model ollama/qwen3:32b-q4_K_M
```

## VRAM Budget (RTX 2080 Ti — 22 GB)

| Model Size | Quantization | Approx VRAM | Feasible? |
|------------|-------------|-------------|-----------|
| 9B (gemma2) | Q4_0 | ~6 GB | ✅ Smooth |
| 24B (mistral-small3.1) | Q4_K_M | ~15 GB | ✅ Comfortable |
| 27B (gemma3:27b) | Q4_K_M | ~17 GB | ✅ OK |
| 32B (qwen3/deepseek-r1) | Q4_K_M | ~20 GB | ⚠️ Nearly full |
| >40B | — | >25 GB | ❌ Won't fit |

- With 32B models loaded, VRAM is near capacity — avoid running other GPU workloads simultaneously.
- Use `ollama stop <model>` to unload a model before loading a different one.
- Qwen3 32B Q4_K_M is ~20 GB, leaving ~2 GB for system overhead — tight but functional.

## Model Selection Tips

- **中文对话**: `qwen3:32b-q4_K_M` (Qwen 3 has strong Chinese capabilities)
- **代码/英文**: `mistral-small3.1:24b` (Mistral Small 3.1, best balance of quality vs VRAM)
- **深度推理**: `deepseek-r1:32b` (DeepSeek R1, chain-of-thought reasoning)
- **无审查**: `huihui_ai/qwq-abliterated:latest` (abliterated QwQ, no content refusals)
- **轻量快速**: `gemma2:latest` (9B, fast responses)

## Pitfalls

- **WSL2 auto-maps `localhost` to Windows** — no need for host IP or `host.docker.internal`. If it doesn't work, check Windows Firewall for port 11434.
- **Ollama must be running on Windows first** — it doesn't auto-start from WSL. Ensure the Ollama system tray icon is present.
- **VRAM exhaustion with 32B models** — if inference hangs or errors, free VRAM: `ollama stop qwen3:32b-q4_K_M && ollama stop deepseek-r1:32b`
- **No auth by default** — if you've configured Ollama authentication (`OLLAMA_AUTH` env var), set `api_key` in the config.
