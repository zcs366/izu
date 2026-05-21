# Wiki Drop — Setup Reference

## Paths

| Item | Path |
|------|------|
| Wiki root | `/mnt/i/hermes/wiki/` (env: `WIKI_PATH`) |
| Queue file | `wiki/queue/url_queue.jsonl` |
| Processed index | `wiki/queue/processed.json` |
| Collector state | `wiki/queue/collector_state.json` |
| Webhook server | `wiki/queue/webhook-server.py` |
| Collector script | `wiki/queue/collector.py` |
| Process script | `wiki/queue/process_queue.py` |
| Drop handler | `wiki/queue/drop_handler.py` |
| Webhook script (crontab) | `wiki/queue/start-webhook.sh` |

## Webhook Server

| Item | Detail |
|------|--------|
| Port | 8765 |
| Host | 0.0.0.0 |
| tmux session | `wiki-webhook` |
| Endpoint | `POST /wiki-drop` |
| Health | `GET /health` |

**Start:**
```bash
tmux new-session -d -s wiki-webhook \
  'cd /mnt/i/hermes/wiki/queue && python3 webhook-server.py 8765'
```

**Verify:**
```bash
curl -s http://localhost:8765/health
# → {"status":"ok","queue_size":0,"total_processed":0}
```

**Send a URL:**
```bash
curl -X POST http://localhost:8765/wiki-drop \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com/article","source":"manual"}'
```

## Cron Jobs

| Name | Schedule | Type | Script |
|------|----------|------|--------|
| `wiki-queue-fetch` | every 15 min | no_agent | `process_queue.py` |

**Crontab auto-recovery** (runs independently of Hermes cron):
```
*/5 * * * * /mnt/i/hermes/wiki/queue/start-webhook.sh >/dev/null 2>&1
```

## Queue File Format (url_queue.jsonl)

```json
{"url":"https://...","source":"telegram","message_id":123,"timestamp":"2026-05-06T14:00:00","status":"pending"}
{"url":"https://...","source":"webhook","message_id":456,"timestamp":"2026-05-06T14:15:00","status":"done","raw_path":"/mnt/i/hermes/wiki/raw/articles/...","title":"Page Title","content_hash":"abc123","processed_at":"2026-05-06T14:15:30"}
```

## Automatically Detected Source Types

- `bilibili` — bilibili.com, b23.tv
- `zhihu` — zhihu.com, zhuanlan.zhihu.com
- `x-twitter` — twitter.com, x.com
- `weixin` — mp.weixin.qq.com, weixin.qq.com
- `youtube` — youtube.com, youtu.be
- `arxiv` — arxiv.org
- `github` — github.com
- `xiaohongshu` — xiaohongshu.com, xhslink.com
- `web` — catch-all for anything else

## Raw File Format (raw/articles/)

HTML files saved with HTML comment frontmatter:
```html
<!--
source_url: https://...
ingested: 2026-05-06
title: Page Title
source_type: web
sha256: <hex>
fetched_by: curl
-->
<!doctype html>...
```

## Optional TG Bot (Path C)

**.env variables:**
```
WIKI_TELEGRAM_BOT_TOKEN=your_bot_token_here
WIKI_TELEGRAM_CHAT_ID=123456789
```

**Run collector:**
```bash
cd /mnt/i/hermes/wiki/queue
python3 collector.py           # one-shot (for cron)
python3 collector.py --watch   # continuous mode
```

## Skills Loaded Together

For full pipeline awareness, load both skills:
- `wiki-drop` — URL detection + pipeline orchestration
- `llm-wiki` — wiki conventions, ingest procedure, page creation rules
