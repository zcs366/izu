# Midscene MCP Integration Recipe

Midscene.js provides pre-built MCP server packages for visual-driven browser automation. This document covers integration with Hermes Agent via `mcp_servers` config.

## Overview

Midscene is a vision-driven UI automation framework by ByteDance's Web Infra team. Unlike DOM-based tools (Playwright, CDP), Midscene understands screenshots and can interact with shadow DOM / complex UI structures that traditional selectors can't reach.

**Key use case for this user**: publishing videos to 微信视频号 (WeChat Channels), which uses wujie micro-frontend with heavy shadow DOM. Also planned: B站 (Bilibili) and YouTube video publishing + wiki ingestion.

## Available MCP Packages

| Package | Description | Transport |
|---------|-------------|-----------|
| `@midscene/web-mcp` | Browser Bridge mode — connects to existing Chrome via CDP | stdio (npx) |
| `@midscene/computer-mcp` | Desktop control | stdio |
| `@midscene/android-mcp` | Android device control | stdio |
| `@midscene/ios-mcp` | iOS device control | stdio |

## Prerequisites

1. **Node.js** — npx must be available (user has Node v22.22.2)
2. **Chrome with CDP** — Hermes already configured: `browser.cdp_url: http://127.0.0.1:9222`
3. **Vision model API key** — Midscene calls a multimodal model for every operation. See "Vision Model Selection" below.

## Hermes Config

Add to `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  midscene-web:
    command: "npx"
    args: ["-y", "@midscene/web-mcp"]
    env:
      MIDSCENE_MODEL_BASE_URL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      MIDSCENE_MODEL_API_KEY: "[REDACTED]"
      MIDSCENE_MODEL_NAME: "qwen-vl-plus"
      MIDSCENE_MODEL_FAMILY: "qwen3-vl"
      MCP_SERVER_REQUEST_TIMEOUT: "800000"
    timeout: 120
    connect_timeout: 60
```

Restart Hermes after config change. Tools auto-register as `mcp_midscene_web_*`.

## Vision Model Selection

Midscene calls a vision model for every action (screenshot → understand → decide next step). This is a **hard cost** — no way around it.

### What DOESN'T work (verified against this user's providers)

| Provider | Vision Support | Notes |
|----------|---------------|-------|
| DeepSeek | ❌ | Text-only |
| MiniMax (AI Basecamp gpt-5.4) | ❌ | Text-only |
| LM Studio local (mistral-small-3.2) | ❌ | Text-only |
| Groq | ❌ | No vision models |

### Recommended: Qwen VL via Alibaba Cloud Bailian

- **Register**: https://bailian.console.aliyun.com/
- **Endpoint**: `https://dashscope.aliyuncs.com/compatible-mode/v1` (OpenAI-compatible)
- **Free tier**: 1,000,000 tokens/month for vision models
- **Model**: `qwen-vl-plus` (Midscene officially supports)
- **Family**: `qwen3-vl`

### Midscene-Supported Model Families

From Midscene docs, the `MIDSCENE_MODEL_FAMILY` env var accepts these values for Qwen:
- `qwen3-vl` — for Qwen3-VL series (qwen3-vl-plus, etc.)
- `qwen-vl` — for older Qwen-VL series

## How It Works with Hermes Browser

Hermes has `browser.cdp_url: http://127.0.0.1:9222`. Midscene's Browser Bridge mode (`@midscene/web-mcp`) connects to this same CDP endpoint — no additional Chrome configuration needed.

The flow: Hermes → calls `mcp_midscene_web_*` tool → Midscene MCP server → CDP → Chrome.

## Cost Monitoring

Set `DEBUG=midscene:ai:profile:stats` to print usage and latency per operation.

## References

- Midscene MCP docs: https://midscenejs.com/mcp
- Model configuration: https://midscenejs.com/model-config
- Common model recipes: https://midscenejs.com/model-common-config
- GitHub: https://github.com/web-infra-dev/midscene
