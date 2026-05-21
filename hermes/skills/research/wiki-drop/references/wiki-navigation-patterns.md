# Wiki Navigation Patterns

> When a wiki outgrows flat indexing — what to do, and what NOT to do.

## The Trap: MOC for AI-Assisted Wikis

MOC (Map of Content), popularized in the Obsidian/PKM community, is a manually-curated note that links to all related notes on a topic. It works for **solo humans navigating thousands of notes without AI**.

For an AI-assisted wiki (where an Agent can semantic-search, reason across entities, and surface cross-domain connections), MOC is an anti-pattern:
- **Redundant** — the AI can already do `fact_store.reason(["AGI", "教育"])` to find connections MOC would take hours to manually encode
- **Maintenance burden** — someone must update links, and that someone is rarely the AI
- **Flat links, no judgment** — MOCs list pages; they don't state what the user currently thinks about the topic

## The Alternative: Topic Entry Points

Instead of MOC, build 3-5 **hand-written entry pages** (`wiki/entry-points/`) for the user's core concerns. Each page (~200 words) follows this structure:

```markdown
# Topic Name

> 入口·核心判断 | YYYY-MM-DD

## 这个主题对我意味着什么
[One paragraph — why this matters to THIS user specifically]

## 我现在知道什么
[Knowledge inventory — what's solid, what's framework-level]

## 我还不确定什么
[Honest knowledge gaps — this is the most valuable section]

## 关键入口
- [[link to key pages]] — not exhaustive, just the 3-5 most important

## 下一步
[One line — where to dig next. This line gets updated after major research outputs]
```

### Key differences from MOC

| MOC | Entry Point |
|-----|-------------|
| Lists ALL related pages | Links only the 3-5 most important |
| Requires manual link maintenance | AI can auto-update the "下一步" line |
| Structure-first (categories) | Judgment-first (opinions) |
| Static | Living (updated when knowledge advances) |
| For navigation only | For navigation + self-assessment |

### When to create entry points

- Wiki exceeds 50+ pages with clear topic clusters
- User asks about knowledge management methodology
- The flat index.md starts feeling unwieldy despite being well-maintained

### Integration with index.md

Entry points sit **above** the flat catalog in `index.md`:

```markdown
## 入口（主题导航）
- [[entry-points/agi]] — AGI全景
- [[entry-points/izu]] — izu / Agent系统
...
```

The index.md continues to serve as the complete catalog. Entry points are the curated front door.

### Anti-patterns to avoid

- **Too many entry points** — if you have 15, they're just a second index. Cap at 5-7.
- **Entry points as task lists** — they state what's known/unknown, not what to do today
- **Entry points as link farms** — if the "关键入口" section has 20 links, it's a MOC in disguise
