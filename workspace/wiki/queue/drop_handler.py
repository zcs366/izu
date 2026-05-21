#!/usr/bin/env python3
"""
Wiki Drop - Conversation-based URL ingestion handler.

When this skill is loaded, the agent will:
1. Auto-detect URLs in user messages
2. Offer to ingest them into the wiki
3. Process them using the llm-wiki pipeline

Usage: Load this skill in gateway sessions where you want
automatic URL detection for wiki ingestion.
"""
import os, sys, json, hashlib, re
from datetime import datetime
from pathlib import Path

WIKI = os.environ.get("WIKI_PATH", "/mnt/i/hermes/wiki")
QUEUE_FILE = Path(WIKI) / "queue" / "url_queue.jsonl"

def url_sha256(url):
    return hashlib.sha256(url.encode()).hexdigest()

def add_url_to_queue(url, source="chat"):
    """Add a URL to the wiki ingestion queue."""
    # Check if already in queue
    if QUEUE_FILE.exists():
        for line in QUEUE_FILE.read_text().strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if url_sha256(item['url']) == url_sha256(url) and item['status'] == 'pending':
                    return False, "already_in_queue"
            except:
                continue
    
    item = {
        "url": url,
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "pending"
    }
    
    with open(QUEUE_FILE, 'a') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return True, "queued"

def extract_urls(text):
    """Extract URLs from text."""
    pattern = re.compile(
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?'
        r'(?:/[\w\-\.~:/?#\[\]@!$&\'()*+,;=]*)?',
        re.I
    )
    return pattern.findall(text)
