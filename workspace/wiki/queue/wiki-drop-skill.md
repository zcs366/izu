---
name: wiki-drop
description: "Auto-detect URLs in conversation → queue for wiki ingestion. Works with llm-wiki skill."
version: 1.0.0
metadata:
  hermes:
    tags: [wiki, ingestion, url, auto-detect]
    category: research
    related_skills: [llm-wiki]
---

# Wiki Drop — Auto URL Ingestion

When this skill is loaded alongside `llm-wiki`, the agent automatically
detects URLs in user messages and processes them as wiki ingestion requests.

## Activation Rule

**Trigger:** User sends a message containing one or more URLs.

**Behavior:**
1. Detect all URLs in the message
2. For each URL:
   a. Use `web_extract` to fetch the content
   b. Save to `wiki/raw/` with proper frontmatter (source_url, ingested, sha256)
   c. Analyze the content for entities, concepts, and relationships
   d. Create or update wiki pages (entities/, concepts/)
   e. Update index.md and log.md
3. Report back to the user with a summary of what was ingested

## URL Sources

The system handles these source types:
- **B站** (bilibili.com, b23.tv) — video/article
- **知乎** (zhihu.com) — article/answer
- **微信公众号** (mp.weixin.qq.com) — article
- **X/Twitter** (twitter.com, x.com) — tweet/thread
- **YouTube** (youtube.com, youtu.be) — video
- **arXiv** (arxiv.org) — paper
- **GitHub** (github.com) — repo/issue
- **小红书** (xiaohongshu.com) — post
- **通用网页** — any other URL

## Queue Fallback

If the agent is busy or the content is too large to process immediately,
add the URL to the queue file instead:

```
wiki/queue/url_queue.jsonl
```

The cron job will pick it up and process it asynchronously.

## Conversation Flow

- **URL only** (no text): Auto-ingest, respond with summary
- **URL + text**: Ingest the URL, respond to the text
- **Multiple URLs**: Process batch, respond with combined summary
- **"#wiki" prefix**: Force wiki ingestion even for short/local URLs

## Response Style

After ingestion, respond with:
```
📥 已摄入 [{source_type}]
标题: {title}
实体: [[entity1]], [[entity2]]
概念: [[concept1]]
保存: raw/articles/{filename}.md
```

If queued:
```
📋 已加入处理队列
{url}
将在下次批处理时完成（约15分钟内）
```
