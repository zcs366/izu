---
name: llm-wiki
description: "Karpathy's LLM Wiki: build/query interlinked markdown KB."
version: 2.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
    category: research
    related_skills: [obsidian, arxiv]
---

# Karpathy's LLM Wiki

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike traditional RAG (which rediscovers knowledge from scratch per query), the wiki
compiles knowledge once and keeps it current. Cross-references are already there.
Contradictions have already been flagged. Synthesis reflects everything ingested.

**Division of labor:** The human curates sources and directs analysis. The agent
summarizes, cross-references, files, and maintains consistency.

## When This Skill Activates

Use this skill when the user:
- Asks to create, build, or start a wiki or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present at the configured path
- Asks to lint, audit, or health-check their wiki
- References their wiki, knowledge base, or "notes" in a research context

## Wiki Location

**Location:** Set via `WIKI_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/wiki`.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or
any editor. No database, no special tooling required.

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only, rotated yearly)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── entities/           # Layer 2: Entity pages (people, orgs, products, models)
├── concepts/           # Layer 2: Concept/topic pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**Layer 1 — Raw Sources:** Immutable. The agent reads but never modifies these.
**Layer 2 — The Wiki:** Agent-owned markdown files. Created, updated, and
cross-referenced by the agent.
**Layer 3 — The Schema:** `SCHEMA.md` defines structure, conventions, and tag taxonomy.

## Resuming an Existing Wiki (CRITICAL — do this every session)

When the user has an existing wiki, **always orient yourself before doing anything**:

① **Read `SCHEMA.md`** — understand the domain, conventions, and tag taxonomy.
② **Read `index.md`** — learn what pages exist and their summaries.
③ **Scan recent `log.md`** — read the last 20-30 entries to understand recent activity.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
# Orientation reads at session start
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

Only after orientation should you ingest, query, or lint. This prevents:
- Creating duplicate pages for entities that already exist
- Missing cross-references to existing content
- Contradicting the schema's conventions
- Repeating work already logged

For large wikis (100+ pages), also run a quick `search_files` for the topic
at hand before creating anything new.

## Initializing a New Wiki

When the user asks to create or start a wiki:

1. Determine the wiki path (from `$WIKI_PATH` env var, or ask the user; default `~/wiki`)
2. Create the directory structure above
3. Ask the user what domain the wiki covers — be specific
4. Write `SCHEMA.md` customized to the domain (see template below)
5. Write initial `index.md` with sectioned header
6. Write initial `log.md` with creation entry
7. Confirm the wiki is ready and suggest first sources to ingest

### SCHEMA.md Template

Adapt to the user's domain. The schema constrains agent behavior and ensures consistency:

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source. This lets a reader trace each
  claim back without re-reading the whole raw file. Optional on single-source pages where the
  `sources:` frontmatter is enough.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary | archive
  tags: [from taxonomy below]
  aliases: [alt-name-1, alt-name-2]  # optional, for growth archives
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review so weak claims
don't silently harden into accepted wiki fact.

### raw/ Frontmatter

Raw sources ALSO get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

The `sha256:` lets a future re-ingest of the same URL skip processing when content is unchanged,
and flag drift when it has changed. Compute over the body only (everything after the closing
`---`), not the frontmatter itself.

## Tag Taxonomy
[Define 10-20 top-level tags for the domain. Add new tags here BEFORE using them.]

Example for AI/ML:
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages

### Standard (Reference) Entities
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

### Growth Archive Entities
A specialized entity page for tracking a person's/thing's development over time. Unlike reference entities (which are factual snapshots), growth archives accumulate entries chronologically and track strategy changes.

**Structure:**
- **Frontmatter**: Same as standard entity, plus `aliases: [nickname1, nickname2]` for known alternative names
- **Archive Summary table**: quick-glance info (age, grade, current status, current strategic priority)
- **Core Profile**: fixed facts (learning type, diagnosis, traits) that don't change often
- **📓 Growth Record**: chronological entries with `### YYYY-MM-DD | Title` headers. Each entry:
  - Date + source (which platform/conversation generated this entry)
  - Facts/observations (markdown tables where appropriate)
  - Quotes from user conversations if the user's own words carry weight
  - Outcome/assessment (what happened, what was learned)
  - **No opinions or editorializing from the agent** — the archive is the user's record, not the agent's analysis
- **💡 学习策略库 / Strategy Tracker**: tabular record of strategies tried, with status and effect columns
- **🏷️ Tags Index**: labels like `#对话记录 #策略迭代 #情绪观察 #里程碑 #反思 #战情`
- **🔗 关联文件 / Linked Files**: paths to related documents (conventions, reports, research)

**Use case examples:** Child development tracking, skill acquisition journey, project evolution, pet care log, personal health history.

**Don't create growth archives for:** things that change rarely or don't benefit from chronological accumulation (documentation topics, static reference concepts).

**Concrete example:** See `references/growth-archive-example-duanmu.md` for a worked example of a child development archive with cron-based auto-update.

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
```

### index.md Template

The index is sectioned by type. Each entry is one line: wikilink + summary.

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

**Scaling rule:** When any section exceeds 50 entries, split it into sub-sections
by first letter or sub-domain. When the index exceeds 200 entries total, create
a `_meta/topic-map.md` that groups pages by theme for faster navigation.

### log.md Template

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## Model Selection & Configuration

Wiki operations (ingest → summarize → cross-reference → entity extraction → synthesis) are LLM-intensive. The main agent's default model may not be ideal for this workload — use a dedicated wiki model.

### Recommended Model Setup

**Platform: OpenRouter** (free tier, zero cost)
**Primary model: `google/gemma-4-31b-it:free`** (via OpenRouter)
- 31B dense, strong reasoning + Chinese support
- Fast inference — critical for batch ingest (many calls per source)
- Free, no rate-limit worries for personal use

**Long-document fallback: `nvidia/nemotron-3-super-120b-a12b:free`**
- 1M token context — for full-book/long-paper ingestion
- Slower (MoE cold-start) but 1M context means no chunking

### Hermes Config

Add to `~/.hermes/config.yaml`:

```yaml
providers:
  openrouter:
    base_url: https://openrouter.ai/api/v1

delegation:
  model: google/gemma-4-31b-it:free
  provider: openrouter
  base_url: https://openrouter.ai/api/v1

fallback_providers:
  - openrouter
```

This ensures delegated wiki tasks use the free model automatically. Main conversation model stays unchanged.

### Switching Models Mid-Session

```bash
# Switch main session to wiki model for manual wiki work
/model openrouter/google/gemma-4-31b-it:free

# Switch back
/model deepseek-v4-flash

# Long-document mode
/model openrouter/nvidia/nemotron-3-super-120b-a12b:free
```

### Discovering Free Models

To update the free model list (models change over time):

```bash
curl https://openrouter.ai/api/v1/models | python3 -c "
import json,sys
data = json.load(sys.stdin)
models = data.get('data', data if isinstance(data, list) else [])
for m in models:
    pricing = m.get('pricing', {})
    if pricing.get('prompt') == '0':
        print(f\"{m['id']} — {m.get('name', '')}\")
"
```

See `references/openrouter-free-models.md` for the verified free model list.

### Pitfall: Free Models Are Ephemeral

- Free models get deprecated without notice as providers change pricing
- Run the discovery command above to verify current availability
- Always test with a quick curl before committing to a model for batch operations
- **Nemotron** (`nvidia/nemotron-3-super-120b-a12b:free`) has a cold-start latency of 30-60s on first call; plan accordingly for batch jobs

### Pitfall: Model Quality vs Cost Trade-off

- Free models are free because they're the provider's loss-leader — expect occasional throttling during peak hours
- If wiki ingest quality degrades (summaries become shallow, cross-references miss), switch to a paid model temporarily:
  - `openai/gpt-4.1-mini` (~$0.40/M tokens) — fast, excellent summarization
  - `anthropic/claude-sonnet-4` — best for complex entity resolution
  - All switchable by changing one model name in config.yaml

## Conversation Auto-Archiving (Cron + session_search)

A pattern for keeping a wiki page current by scanning conversations daily.

**When to use:** The user has a recurring topic (a child's development, a project's progress, a skill being learned) that comes up in conversation regularly. Rather than manually updating the wiki each time, set up a cron job that scans for new conversations and appends new findings automatically.

### Setup Steps

1. **Create the target wiki page** first (typically a Growth Archive entity — see above). The cron agent needs to know the exact path.

2. **Create a cron job** with `cronjob(action='create', ...)` that runs daily:
   - `schedule`: `"0 22 * * *"` (10 PM daily — after the day's conversations are done)
   - `enabled_toolsets`: `["search", "file"]` (needs session_search + file read/write)
   - `deliver`: `"origin"` (reports back to the user's home channel)
   - `prompt`: Must include:

3. **Cron prompt structure:**
   ```
   每日任务：扫描当天关于[TOPIC]的讨论，存入wiki[PAGE_PATH]。

   1. session_search（无参数查看近期会话预览）找到与[TOPIC]相关的会话
   2. 读取现有档案 [PAGE_PATH]，查看最新的记录日期，避免重复
   3. 如果有新内容（上次记录之后的新消息），以 ### [日期] | 标题 格式追加到 📓 成长记录 章节
   4. 更新页面头部的 updated 字段日期
   5. 如果内容涉及策略尝试/效果，同步更新 策略库 章节
   6. 更新 index.md 中该条目的一行摘要（日期）
   7. 追加简短 log 到 log.md
   8. 有新内容就输出总结，没有就回复 "[SILENT]" 静默跳过
   ```

4. **Silent delivery:** The `[SILENT]` convention is critical — the cron job runs daily but most days will have nothing new. Without silent delivery, the user gets empty notifications every night. Only report when there's actual new content.

### Pitfalls

- **session_search needs context** — it returns summaries, not full transcripts. When scanning, include multiple keyword variants (topic name, aliases, related terms) to maximize recall.
- **Deduplication is manual** — the cron job must read the archive's last entry date and only process sessions after that date. Include `avoid duplicate` instructions in the prompt.
- **Don't create the cron job without user consent** — ask first. Auto-archiving a sensitive topic (health, child development) without explicit buy-in violates trust.
- **The cron agent has no memory** — each run starts fresh. The prompt must be completely self-contained with the wiki page path and search keywords.
- **Rate limiting** — if the topic generates multiple conversations per day, the cron agent's session_search may hit tool limits. Set `result processing: take the most relevant 2-3 sessions` as a guard.

## URL Ingestion Pipeline

When `wiki-drop` skill is also loaded, URLs can be auto-ingested via three paths:
- **Conversation:** User says "存入wiki" + URL → immediate LLM ingestion
- **Webhook:** HTTP POST to port 8765 → queued → cron fetches raw HTML every 15 min
- **TG Bot:** Dedicated collector bot → queued → same cron pipeline

The queue lives at `wiki/queue/url_queue.jsonl`. The background cron job
(`wiki-queue-fetch`, every 15 min) fetches raw content via curl and saves
to `raw/articles/` — but does NOT do LLM analysis. That happens on-demand
when the agent processes the content in conversation.

**When orienting to the wiki, check for pending queue items** if the user
asks about recent ingestions or sources they forwarded.

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste), integrate it into the wiki:

① **Capture the raw source:**
   - **URL → try `web_extract` first.**
     - If it returns content (non-empty): save to `raw/articles/` as markdown.
     - If it fails (Payment Required, empty content, timeout): **fall back to
       `curl` + Python HTML extraction**. Chinese platforms (WeChat, Zhihu, Bilibili)
       commonly trigger this failure. See `wiki-drop` skill's
       `references/chinese-platform-extraction.md` for platform-specific recipes.
     - If curl also fails → queue the URL (`wiki/queue/url_queue.jsonl`) and
       tell the user it'll be processed in the batch cycle.
   - **PDF → use `web_extract`** (handles PDFs), save to `raw/papers/`
   - **Pasted text → save** to appropriate `raw/` subdirectory
   - **Name the file descriptively**: `raw/articles/slug.md` (lowercase, hyphens).
     For WeChat articles, use a topic-based slug (e.g., `yunyu-tiandi-jiaotai-yuanliu.md`)
     rather than the opaque article ID.
   - **Add raw frontmatter** (`source_url`, `ingested`, `sha256` of the body).
     **Workflow for sha256:** Save the file first (with empty sha256), then compute
     the hash over the body, then patch it in. The hash must be over content below
     the closing `---` only, not the frontmatter itself.
     ```bash
     sha256sum wiki/raw/articles/slug.md | cut -d' ' -f1
     # Then: update sha256: field in frontmatter with this value
     ```
     On re-ingest of the same URL: recompute the sha256, compare to the stored value —
     skip if identical, flag drift and update if different. This catches silent
     source changes without re-processing unchanged content.

② **Discuss takeaways** with the user — what's interesting, what matters for
   the domain. (Skip this in automated/cron contexts — proceed directly.)

③ **Check what already exists** — search index.md and use `search_files` to find
   existing pages for mentioned entities/concepts. This is the difference between
   a growing wiki and a pile of duplicates.

④ **Write or update wiki pages:**
   - **New entities/concepts:** Create pages only if they meet the Page Thresholds
     in SCHEMA.md (2+ source mentions, or central to one source)
   - **Existing pages:** Add new information, update facts, bump `updated` date.
     When new info contradicts existing content, follow the Update Policy.
   - **Cross-reference:** Every new or updated page must link to at least 2 other
     pages via `[[wikilinks]]`. Check that existing pages link back.
   - **Tags:** Only use tags from the taxonomy in SCHEMA.md
   - **Provenance:** On pages synthesizing 3+ sources, append `^[raw/articles/source.md]`
     markers to paragraphs whose claims trace to a specific source.
   - **Confidence:** For opinion-heavy, fast-moving, or single-source claims, set
     `confidence: medium` or `low` in frontmatter. Don't mark `high` unless the
     claim is well-supported across multiple sources.

⑤ **Update navigation:**
   - Add new pages to `index.md` under the correct section, alphabetically
   - Update the "Total pages" count and "Last updated" date in index header
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
   - List every file created or updated in the log entry

⑥ **Report what changed** — list every file created or updated to the user.

A single source can trigger updates across 5-15 wiki pages. This is normal
and desired — it's the compounding effect.

### 2. Query

When the user asks a question about the wiki's domain:

① **Read `index.md`** to identify relevant pages.
② **For wikis with 100+ pages**, also `search_files` across all `.md` files
   for key terms — the index alone may miss relevant content.
③ **Read the relevant pages** using `read_file`.
④ **Synthesize an answer** from the compiled knowledge. Cite the wiki pages
   you drew from: "Based on [[page-a]] and [[page-b]]..."
⑤ **File valuable answers back** — if the answer is a substantial comparison,
   deep dive, or novel synthesis, create a page in `queries/` or `comparisons/`.
   Don't file trivial lookups — only answers that would be painful to re-derive.
⑥ **Update log.md** with the query and whether it was filed.

### 3. Lint

When the user asks to lint, health-check, or audit the wiki:

① **Orphan pages:** Find pages with no inbound `[[wikilinks]]` from other pages.
```python
# Use execute_code for this — programmatic scan across all wiki pages
import os, re
from collections import defaultdict
wiki = "<WIKI_PATH>"
# Scan all .md files in entities/, concepts/, comparisons/, queries/
# Extract all [[wikilinks]] — build inbound link map
# Pages with zero inbound links are orphans
```

② **Broken wikilinks:** Find `[[links]]` that point to pages that don't exist.

③ **Index completeness:** Every wiki page should appear in `index.md`. Compare
   the filesystem against index entries.

④ **Frontmatter validation:** Every wiki page must have all required fields
   (title, created, updated, type, tags, sources). Tags must be in the taxonomy.

⑤ **Stale content:** Pages whose `updated` date is >90 days older than the most
   recent source that mentions the same entities.

⑥ **Contradictions:** Pages on the same topic with conflicting claims. Look for
   pages that share tags/entities but state different facts. Surface all pages
   with `contested: true` or `contradictions:` frontmatter for user review.

⑦ **Quality signals:** List pages with `confidence: low` and any page that cites
   only a single source but has no confidence field set — these are candidates
   for either finding corroboration or demoting to `confidence: medium`.

⑧ **Source drift:** For each file in `raw/` with a `sha256:` frontmatter, recompute
   the hash and flag mismatches. Mismatches indicate the raw file was edited
   (shouldn't happen — raw/ is immutable) or ingested from a URL that has since
   changed. Not a hard error, but worth reporting.

⑨ **Page size:** Flag pages over 200 lines — candidates for splitting.

⑩ **Tag audit:** List all tags in use, flag any not in the SCHEMA.md taxonomy.

⑪ **Log rotation:** If log.md exceeds 500 entries, rotate it.

⑫ **Report findings** with specific file paths and suggested actions, grouped by
   severity (broken links > orphans > source drift > contested pages > stale content > style issues).

⑬ **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

## Working with the Wiki

### Searching

```bash
# Find pages by content
search_files "transformer" path="$WIKI" file_glob="*.md"

# Find pages by filename
search_files "*.md" target="files" path="$WIKI"

# Find pages by tag
search_files "tags:.*alignment" path="$WIKI" file_glob="*.md"

# Recent activity
read_file "$WIKI/log.md" offset=<last 20 lines>
```

### Bulk Ingest

When ingesting multiple sources at once, batch the updates:
1. Read all sources first
2. Identify all entities and concepts across all sources
3. Check existing pages for all of them (one search pass, not N)
4. Create/update pages in one pass (avoids redundant updates)
5. Update index.md once at the end
6. Write a single log entry covering the batch

### Archiving

When content is fully superseded or the domain scope changes:
1. Create `_archive/` directory if it doesn't exist
2. Move the page to `_archive/` with its original path (e.g., `_archive/entities/old-page.md`)
3. Remove from `index.md`
4. Update any pages that linked to it — replace wikilink with plain text + "(archived)"
5. Log the archive action

### Obsidian Integration

The wiki directory works as an Obsidian vault out of the box:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries
- The `raw/assets/` folder holds images referenced via `![[image.png]]`

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings (usually on by default)
- Install Dataview plugin for queries like `TABLE tags FROM "entities" WHERE contains(tags, "company")`

If using the Obsidian skill alongside this one, set `OBSIDIAN_VAULT_PATH` to the
same directory as the wiki path.

### Obsidian Headless (servers and headless machines)

On machines without a display, use `obsidian-headless` instead of the desktop app.
It syncs vaults via Obsidian Sync without a GUI — perfect for agents running on
servers that write to the wiki while Obsidian desktop reads it on another device.

**Setup:**
```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault for the wiki
ob sync-create-remote --name "LLM Wiki"

# Connect the wiki directory to the vault
cd ~/wiki
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

**Continuous background sync via systemd:**
```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/home/user/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
# Enable linger so sync survives logout:
sudo loginctl enable-linger $USER
```

This lets the agent write to `~/wiki` on a server while you browse the same
vault in Obsidian on your laptop/phone — changes appear within seconds.

## Pitfalls

- **`web_extract` is NOT universal** — JS-heavy Chinese platforms (WeChat, Zhihu, Bilibili)
  reliably fail with Payment Required or empty responses. Always have a curl + Python
  extraction fallback ready. The `wiki-drop` skill's `references/chinese-platform-extraction.md`
  has platform-specific recipes.
- **Never modify files in `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — read SCHEMA + index + recent log before any operation in a new session.
  Skipping this causes duplicates and missed cross-references.
- **Always update index.md and log.md** — skipping this makes the wiki degrade. These are the
  navigational backbone.
- **Don't create pages for passing mentions** — follow the Page Thresholds in SCHEMA.md. A name
  appearing once in a footnote doesn't warrant an entity page.
- **Don't create pages without cross-references** — isolated pages are invisible. Every page must
  link to at least 2 other pages.
- **Frontmatter is required** — it enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy** — freeform tags decay into noise. Add new tags to SCHEMA.md
  first, then use them.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds. Split pages over
  200 lines. Move detailed analysis to dedicated deep-dive pages.
- **Ask before mass-updating** — if an ingest would touch 10+ existing pages, confirm
  the scope with the user first.
- **Rotate the log** — when log.md exceeds 500 entries, rename it `log-YYYY.md` and start fresh.
  The agent should check log size during lint.
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates,
  mark in frontmatter, flag for user review.

## Related Tools

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that
compiles sources into a concept wiki with the same Karpathy inspiration. It's Obsidian-compatible,
so users who want a scheduled/CLI-driven compile pipeline can point it at the same vault this
skill maintains. Trade-offs: it owns page generation (replaces the agent's judgment on page
creation) and is tuned for small corpora. Use this skill when you want agent-in-the-loop curation;
use llmwiki when you want batch compile of a source directory.
