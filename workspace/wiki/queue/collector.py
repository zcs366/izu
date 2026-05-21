#!/usr/bin/env python3
"""
Telegram Wiki Collector - Polls a dedicated Telegram chat for new URLs.

REQUIRES A SEPARATE BOT (not the Hermes gateway bot)
to avoid getUpdates conflict.

Setup:
1. Talk to @BotFather on Telegram → /newbot → create "WikiDropBot"
2. Copy the token, add to ~/.hermes/.env as WIKI_TELEGRAM_BOT_TOKEN
3. Create a group or channel, add both yourself and the new bot
4. Get the chat ID (send a message, then visit:
   https://api.telegram.org/bot<TOKEN>/getUpdates)
5. Set the chat ID below or via env WIKI_TELEGRAM_CHAT_ID

Usage:
    python3 collector.py              # run once (for cron)
    python3 collector.py --watch      # run continuously

Environment:
    WIKI_TELEGRAM_BOT_TOKEN - separate bot token
    WIKI_TELEGRAM_CHAT_ID   - chat/group/channel ID to monitor
    WIKI_PATH               - wiki path (default: /mnt/i/hermes/wiki)
"""
import os, sys, json, time, re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ingest import add_to_queue, load_processed, save_processed

# ── Config ──
TOKEN = os.environ.get("WIKI_TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("WIKI_TELEGRAM_CHAT_ID", "")
WIKI = os.environ.get("WIKI_PATH", "/mnt/i/hermes/wiki")
STATE_FILE = Path(WIKI) / "queue" / "collector_state.json"

API_BASE = f"https://api.telegram.org/bot{TOKEN}"
POLL_TIMEOUT = 10  # seconds for long polling

# URL regex
URL_REGEX = re.compile(
    r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[\w\-\.~:/?#\[\]@!$&\'()*+,;=]*)?',
    re.I
)

# ── State ──
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_update_id": 0, "processed_ids": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

# ── Telegram API ──
def api_call(method, params=None):
    """Call Telegram Bot API."""
    if params is None:
        params = {}
    url = f"{API_BASE}/{method}"
    data = json.dumps(params).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  ⚠ HTTP {e.code}: {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"  ⚠ API error: {e}")
        return None

def get_updates(offset=0, timeout=10):
    """Get updates from Telegram."""
    params = {
        "offset": offset,
        "timeout": timeout,
        "allowed_updates": ["message"]
    }
    result = api_call("getUpdates", params)
    if result and result.get("ok"):
        return result.get("result", [])
    return []

# ── URL Extraction ──
def extract_urls(text):
    """Extract all URLs from text."""
    return URL_REGEX.findall(text)

def extract_urls_from_message(msg):
    """Extract URLs from a Telegram message, including entities."""
    urls = set()
    
    # From entities (more reliable)
    entities = msg.get("entities", []) or msg.get("caption_entities", [])
    text = msg.get("text", "") or msg.get("caption", "")
    
    for entity in entities:
        if entity.get("type") == "url":
            start, length = entity["offset"], entity["length"]
            url = text[start:start+length]
            urls.add(url)
        elif entity.get("type") == "text_link":
            urls.add(entity.get("url", ""))
    
    # From regex fallback
    if text:
        for url in extract_urls(text):
            urls.add(url)
    
    return list(urls)

# ── Main Collection ──
def collect_once():
    """Single collection pass."""
    if not TOKEN:
        print("❌ WIKI_TELEGRAM_BOT_TOKEN not set")
        return 0
    
    state = load_state()
    offset = state.get("last_update_id", 0)
    
    updates = get_updates(offset=offset + 1, timeout=POLL_TIMEOUT)
    if not updates:
        return 0
    
    new_urls = 0
    max_update_id = offset
    
    for update in updates:
        update_id = update.get("update_id", 0)
        max_update_id = max(max_update_id, update_id)
        
        msg = update.get("message", {})
        chat = msg.get("chat", {})
        chat_id = str(chat.get("id", ""))
        
        # Filter by chat ID if configured
        if CHAT_ID and chat_id != CHAT_ID:
            continue
        
        # Skip own messages
        if msg.get("from", {}).get("is_bot"):
            continue
        
        message_id = msg.get("message_id")
        if message_id and message_id in state.get("processed_ids", []):
            continue
        
        urls = extract_urls_from_message(msg)
        if not urls:
            continue
        
        for url in urls:
            ok = add_to_queue(url, source="telegram", message_id=message_id)
            if ok:
                new_urls += 1
        
        if message_id:
            if "processed_ids" not in state:
                state["processed_ids"] = []
            state["processed_ids"].append(message_id)
            # Keep last 500 to avoid unbounded growth
            if len(state["processed_ids"]) > 500:
                state["processed_ids"] = state["processed_ids"][-500:]
    
    if max_update_id > offset:
        state["last_update_id"] = max_update_id
        save_state(state)
    
    return new_urls

def collect_watch():
    """Continuous collection loop."""
    print(f"━━━ Telegram Wiki Collector (watching) ━━━")
    print(f"  Chat: {CHAT_ID or 'ALL (filter by env)'}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    while True:
        try:
            count = collect_once()
            if count:
                print(f"  [{datetime.now().strftime('%H:%M:%S')}] +{count} URLs collected")
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"  ⚠ Error: {e}")
            time.sleep(30)

# ── CLI ──
if __name__ == "__main__":
    if "--watch" in sys.argv:
        collect_watch()
    else:
        count = collect_once()
        print(f"Collected {count} new URLs.")
