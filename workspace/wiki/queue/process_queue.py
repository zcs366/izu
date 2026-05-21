#!/usr/bin/env python3
"""
Wiki Queue Processor - lightweight fetch + save to raw/.

Reads the queue, fetches each URL via curl/requests,
saves content to wiki/raw/articles/, marks as done.

The heavy LLM analysis (entity extraction, page creation)
happens on-demand when the user queries the wiki.
"""
import os, sys, json, hashlib, re, subprocess, tempfile
from datetime import datetime
from pathlib import Path

WIKI = os.environ.get("WIKI_PATH", "/mnt/i/hermes/wiki")
QUEUE_FILE = Path(WIKI) / "queue" / "url_queue.jsonl"
RAW_DIR = Path(WIKI) / "raw" / "articles"
LOG_FILE = Path(WIKI) / "log.md"

# URL patterns for source detection
URL_PATTERNS = {
    "bilibili": re.compile(r'(bilibili\.com|b23\.tv)', re.I),
    "zhihu": re.compile(r'(zhihu\.com|zhuanlan\.zhihu\.com)', re.I),
    "x-twitter": re.compile(r'(twitter\.com|x\.com)', re.I),
    "weixin": re.compile(r'(mp\.weixin\.qq\.com|weixin\.qq\.com)', re.I),
    "youtube": re.compile(r'(youtube\.com|youtu\.be)', re.I),
    "arxiv": re.compile(r'(arxiv\.org)', re.I),
    "github": re.compile(r'(github\.com)', re.I),
    "xiaohongshu": re.compile(r'(xiaohongshu\.com|xhslink\.com)', re.I),
}

def timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def date_str():
    return datetime.now().strftime("%Y-%m-%d")

def url_sha256(url):
    return hashlib.sha256(url.encode()).hexdigest()

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return s[:60].strip('-')

def detect_source_type(url):
    for name, pattern in URL_PATTERNS.items():
        if pattern.search(url):
            return name
    return "web"

def fetch_url(url, timeout=30):
    """Try to fetch a URL using curl or requests."""
    # Try curl first (better for Chinese sites with proxy)
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), 
             "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=timeout+5
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            return result.stdout, "curl"
    except Exception:
        pass
    
    # Try Python requests as fallback
    try:
        import requests
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code == 200 and len(resp.text) > 100:
            return resp.text, "requests"
    except Exception:
        pass
    
    return None, None

def extract_title(html, url):
    """Try to extract a page title from HTML."""
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I | re.S)
    if m:
        return m.group(1).strip()[:120]
    
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.I | re.S)
    if m:
        return m.group(1).strip()[:120]
    
    # Fallback: derive from URL
    path = url.split('//', 1)[-1].split('?')[0].rstrip('/')
    return path.replace('/', ' - ')[:80]

def load_queue():
    if not QUEUE_FILE.exists():
        return []
    items = []
    for line in QUEUE_FILE.read_text().strip().split('\n'):
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except:
                continue
    return items

def save_queue(items):
    lines = [json.dumps(item, ensure_ascii=False) for item in items]
    QUEUE_FILE.write_text('\n'.join(lines) + ('\n' if lines else ''))

def process_item(item):
    """Fetch a URL and save raw content."""
    url = item['url']
    sha = url_sha256(url)
    source_type = detect_source_type(url)
    
    print(f"  Fetching: {url[:80]}...")
    
    content, method = fetch_url(url)
    if not content:
        print(f"  ✗ Failed to fetch: {url[:60]}")
        item['status'] = 'failed'
        item['error'] = 'fetch_failed'
        item['processed_at'] = timestamp()
        return item
    
    # Extract title
    title = extract_title(content, url)
    
    # Save raw content
    safe_name = slugify(f"{source_type}-{title[:40]}-{sha[:8]}")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / f"{safe_name}.html"
    
    # Compute content hash
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Write raw file with frontmatter comment
    raw_content = f"""<!--
source_url: {url}
ingested: {date_str()}
title: {title}
source_type: {source_type}
sha256: {content_hash}
fetched_by: {method}
-->
{content}
"""
    raw_path.write_text(raw_content, encoding='utf-8')
    
    print(f"  ✓ Saved: {raw_path.name} ({len(content)} bytes)")
    
    # Update item
    item['status'] = 'done'
    item['raw_path'] = str(raw_path)
    item['title'] = title
    item['content_hash'] = content_hash
    item['processed_at'] = timestamp()
    
    return item

def process_queue(max_items=3):
    """Process pending items in the queue."""
    items = load_queue()
    pending = [i for i in items if i['status'] == 'pending']
    
    if not pending:
        print("📭 No pending items.")
        return 0
    
    print(f"📋 Processing up to {max_items} of {len(pending)} pending items...")
    
    processed = 0
    for i, item in enumerate(pending):
        if i >= max_items:
            break
        updated = process_item(item)
        
        # Update the original item in the list
        for j, orig in enumerate(items):
            if orig.get('timestamp') == item.get('timestamp') and orig.get('url') == item.get('url'):
                items[j] = updated
                break
        
        processed += 1
    
    save_queue(items)
    print(f"✅ Processed {processed} items.")
    return processed

if __name__ == "__main__":
    count = process_queue()
    print(f"\nDone. {count} URLs processed.")
