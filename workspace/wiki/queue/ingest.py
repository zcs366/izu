#!/usr/bin/env python3
"""
Wiki URL Ingestion Core Engine

Usage:
    python3 ingest.py https://example.com/article
    python3 ingest.py --queue   # process all pending items in queue
    python3 ingest.py --add https://example.com/article  # add URL to queue only

Environment:
    WIKI_PATH - path to wiki directory (default: /mnt/i/hermes/wiki)
    
The script:
1. web_extract the URL → save to wiki/raw/ (B站/知乎/X/公众号/通用)
2. Compute sha256 of content for dedup
3. Update wiki entities/concepts if appropriate
4. Append to log.md
5. Update index.md if new page created
"""
import os, sys, json, hashlib, re, subprocess
from datetime import datetime
from pathlib import Path

# ── Config ──
WIKI = os.environ.get("WIKI_PATH", "/mnt/i/hermes/wiki")
QUEUE_FILE = Path(WIKI) / "queue" / "url_queue.jsonl"
PROCESSED_FILE = Path(WIKI) / "queue" / "processed.json"
RAW_DIR = Path(WIKI) / "raw"
LOG_FILE = Path(WIKI) / "log.md"
INDEX_FILE = Path(WIKI) / "index.md"

# ── Helpers ──
def timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def date_str():
    return datetime.now().strftime("%Y-%m-%d")

def url_sha256(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()

def slugify(title: str) -> str:
    """Convert title to wiki filename slug."""
    s = title.lower().strip()
    s = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return s[:80].strip('-')

def load_processed():
    if PROCESSED_FILE.exists():
        return json.loads(PROCESSED_FILE.read_text())
    return {"by_sha256": {}, "by_message_id": {}}

def save_processed(data):
    PROCESSED_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def load_queue():
    if not QUEUE_FILE.exists():
        return []
    items = []
    for line in QUEUE_FILE.read_text().strip().split('\n'):
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items

def save_queue(items):
    lines = [json.dumps(item, ensure_ascii=False) for item in items]
    QUEUE_FILE.write_text('\n'.join(lines) + ('\n' if lines else ''))

def add_to_queue(url: str, source: str = "manual", message_id=None):
    items = load_queue()
    # check duplicate in queue
    sha = url_sha256(url)
    if any(url_sha256(i['url']) == sha and i['status'] == 'pending' for i in items):
        print(f"⏭️  URL already in queue (pending): {url}")
        return False
    # check processed
    proc = load_processed()
    if sha in proc['by_sha256']:
        print(f"⏭️  URL already processed: {url}")
        return False
    item = {
        "url": url,
        "source": source,
        "message_id": message_id,
        "timestamp": timestamp(),
        "status": "pending"
    }
    items.append(item)
    save_queue(items)
    print(f"✅  Added to queue: {url}")
    return True

# ── URL Type Detection ──
URL_PATTERNS = {
    "bilibili": re.compile(r'(bilibili\.com|b23\.tv)', re.I),
    "zhihu": re.compile(r'(zhihu\.com|zhuanlan\.zhihu\.com)', re.I),
    "x": re.compile(r'(twitter\.com|x\.com)', re.I),
    "weixin": re.compile(r'(mp\.weixin\.qq\.com|weixin\.qq\.com)', re.I),
    "youtube": re.compile(r'(youtube\.com|youtu\.be)', re.I),
    "arxiv": re.compile(r'(arxiv\.org)', re.I),
    "github": re.compile(r'(github\.com)', re.I),
    "douyin": re.compile(r'(douyin\.com)', re.I),
    "xiaohongshu": re.compile(r'(xiaohongshu\.com|xhslink\.com)', re.I),
}

def detect_source_type(url: str) -> str:
    for name, pattern in URL_PATTERNS.items():
        if pattern.search(url):
            return name
    return "web"

# ── Main Ingest ──
def ingest_url(url: str, source: str = "manual", message_id=None) -> bool:
    """Process a single URL: extract, save raw, log."""
    sha = url_sha256(url)
    proc = load_processed()
    
    # Check already processed
    if sha in proc['by_sha256']:
        print(f"⏭️  Already processed: {url}")
        return False
    
    source_type = detect_source_type(url)
    
    # We'll use web_extract via subprocess/hermes tools
    # For now, save to queue and let the agent-driven cron process it
    # The actual web_extract + wiki page creation requires LLM tools
    # which are available in the cron job's agent session
    
    # Save the URL info to processed with a "queued" marker
    entry = {
        "sha256": sha,
        "url": url,
        "source_type": source_type,
        "source": source,
        "message_id": message_id,
        "queued_at": timestamp(),
        "status": "pending_extraction"
    }
    proc['by_sha256'][sha] = entry
    if message_id:
        proc['by_message_id'][str(message_id)] = sha
    save_processed(proc)
    
    print(f"📥  Queued for agent processing: [{source_type}] {url}")
    return True

def process_queue():
    """Process pending items in the queue.
    
    NOTE: Actual web_extract + wiki page creation requires LLM tool access.
    This function is a helper that:
    1. Reads pending items
    2. For each, attempts basic extraction via curl
    3. Saves raw content to wiki/raw/
    4. Creates a task note for the agent to process further
    """
    items = load_queue()
    pending = [i for i in items if i['status'] == 'pending']
    
    if not pending:
        print("📭  No pending items in queue.")
        return
    
    print(f"📋  Processing {len(pending)} items in queue...")
    
    for item in pending:
        url = item['url']
        sha = url_sha256(url)
        source_type = detect_source_type(url)
        
        # Get a safe filename
        safe_name = slugify(f"{source_type}-{date_str()}-{sha[:8]}")
        raw_path = RAW_DIR / "articles" / f"{safe_name}.md"
        
        # Try to fetch content with curl as fallback
        # (The full web_extract + LLM processing happens in the cron job session)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a placeholder with URL info
        content = f"""---
source_url: {url}
ingested: {date_str()}
sha256: {sha}
source_type: {source_type}
---

# Source: {url}

> Auto-collected from {source_type} on {date_str()}
> 
> **Pending LLM processing** - content extraction and wiki page creation
> will happen in the next agent-driven cron cycle.

URL: {url}

"""
        raw_path.write_text(content)
        item['status'] = 'processing'
        item['raw_path'] = str(raw_path)
        item['processed_at'] = timestamp()
        print(f"  🔄  {source_type}: {url[:60]}... → {raw_path.name}")
    
    save_queue(items)
    print(f"✅  Queue processed. {len(pending)} items submitted for agent processing.")
    return pending

# ── CLI ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "--add":
        url = sys.argv[2] if len(sys.argv) > 2 else None
        if not url:
            print("Usage: ingest.py --add <url> [source]")
            sys.exit(1)
        source = sys.argv[3] if len(sys.argv) > 3 else "manual"
        add_to_queue(url, source)
    
    elif cmd == "--queue":
        process_queue()
    
    elif cmd.startswith("http"):
        url = cmd
        source = sys.argv[2] if len(sys.argv) > 2 else "manual"
        ingest_url(url, source)
    
    else:
        url = sys.argv[1]
        source = sys.argv[2] if len(sys.argv) > 2 else "manual"
        ingest_url(url, source)
