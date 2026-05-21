#!/usr/bin/env python3
"""
Extract article text and metadata from WeChat (mp.weixin.qq.com) HTML.

Usage:
    python3 scripts/extract-wechat-article.py < article.html
    curl -sL <url> | python3 scripts/extract-wechat-article.py

Output: Full article text to stdout, metadata to stderr.
Returns exit code 1 if extraction failed.
"""

import sys
import re
import json


def extract(html):
    """Returns (title, author, description, nickname, text) or raises ValueError."""
    # Title
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_m.group(1).strip() if title_m else ''

    # Author
    author_m = re.search(
        r'<meta[^>]*name=["\']author["\'][^>]*content=["\'](.*?)["\']',
        html, re.DOTALL)
    author = author_m.group(1).strip() if author_m else ''

    # Description
    desc_m = re.search(
        r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        html, re.DOTALL)
    description = desc_m.group(1).strip() if desc_m else ''

    # Nickname
    nickname_m = re.search(r'var\s+nickname\s*=\s*["\'](.*?)["\']', html)
    if not nickname_m:
        nickname_m = re.search(r'"nickname"\s*:\s*"(.*?)"', html)
    nickname = nickname_m.group(1).strip() if nickname_m else ''

    # Article content
    content_m = re.search(
        r'id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
    if not content_m:
        content_m = re.search(
            r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*<script',
            html, re.DOTALL)

    if not content_m:
        raise ValueError("Could not find article content in HTML")

    content = content_m.group(1)
    text = re.sub(r'<br\s*/?>', '\n', content)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = text.strip()

    if len(text) < 100:
        raise ValueError(
            f"Extracted text too short ({len(text)} chars) — extraction failed")

    return title, author, description, nickname, text


if __name__ == '__main__':
    html = sys.stdin.read()
    try:
        title, author, description, nickname, text = extract(html)
        meta = {
            'title': title,
            'author': author,
            'nickname': nickname,
            'description': description,
            'length': len(text)
        }
        print(json.dumps(meta, ensure_ascii=False), file=sys.stderr)
        print(text)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
