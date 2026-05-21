# DuckDuckGo Search Fallback for wiki-project-study

When the `web_search` and `web_extract` tools return "Payment Required" errors (Firecrawl credits exhausted), use DuckDuckGo search via the `ddgs` Python package instead.

## Detection

Firecrawl exhaustion looks like:
```
Error searching web: Payment Required: Failed to search. Insufficient credits...
```

## Fallback Procedure

### 1. Give the research agent `terminal` tool access

The research agent needs `toolsets=["web","search","terminal"]` so it can fall back to DDGS.

### 2. Add fallback instruction to agent prompt

Add to the research agent's prompt:
```
If web_search fails with "Payment Required" errors, use terminal to run ddgs instead:
python3 << 'PYEOF'
from ddgs import DDGS
with DDGS(proxy="http://127.0.0.1:7890") as ddgs:
    for r in ddgs.text("YOUR QUERY", max_results=5):
        print(f"TITLE: {r['title']}")
        print(f"URL: {r['href']}")
        print(f"BODY: {r['body'][:300]}")
        print("---")
PYEOF
```

### 3. Key differences for the agent

- ddgs v9.x returns `body` field, NOT `snippet`
- Results are less rich than Firecrawl (no markdown extraction, just search snippets)
- Proxy is mandatory: `proxy='http://127.0.0.1:7890'`
- Some queries may time out — retry with shorter queries or fewer results
- For page-level content extraction, still try `web_extract` as it may work independently of Firecrawl

## Full API Reference (ddgs v9.x)

### Installation

```bash
pip install ddgs --break-system-packages
```

### Shell one-liner (for terminal tool)

```bash
python3 << 'PYEOF'
from ddgs import DDGS
with DDGS(proxy="http://127.0.0.1:7890") as ddgs:
    for r in ddgs.text("query", max_results=5):
        print(f"TITLE: {r['title']}")
        print(f"URL: {r['href']}")
        print(f"BODY: {r['body'][:300]}")
        print("---")
PYEOF
```

### Result fields

| Field   | Type | Description                     |
|---------|------|---------------------------------|
| `title` | str  | Result title                    |
| `href`  | str  | Target URL                      |
| `body`  | str  | Descriptive text (replaces old `snippet`) |

**⚠ CRITICAL**: ddgs v9.x returns `body`, NOT `snippet`. Using `r['snippet']` will crash with `KeyError`. Older tutorials mentioning `snippet` are for the deprecated `duckduckgo_search` package.

### Additional Pitfalls

1. **Use `ddgs`, NOT `duckduckgo_search`** — the old package was renamed and the old one has compat issues.
2. **Proxy is mandatory** — without `proxy='http://127.0.0.1:7890'`, connections fail with `ConnectError`. Must be HTTP proxy (not SOCKS5).
3. **Rate limits apply** — DuckDuckGo may block excessive automated queries. Add `time.sleep(1)` between queries for batch research.
4. **HTML-scraped** — not an official API; format may change upstream without notice.
5. **Heredoc scripts are more reliable** than inline `python3 -c "..."` for multi-line DDGS calls — the shell escaping in `-c` can break.
6. **Cannot integrate with Hermes' built-in `web_search` tool** — only usable via `terminal` or `execute_code`.

## State

- ✅ ddgs v9.14.2 installed at `~/.local/lib/python3.12/site-packages/ddgs/`
- ✅ Proxy configured for China environment
- ✅ Tested and working during OpenClaw and NotebookLM research sessions
