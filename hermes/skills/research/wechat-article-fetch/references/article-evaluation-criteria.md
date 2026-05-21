# Article Evaluation Criteria

This file defines how to evaluate WeChat articles ("福利文/工具文/知识文") for this user — 
deciding whether they're worth acting on, storing, or skipping.

## Article Typing

When the user sends a WeChat article link, first classify it:

| Type | Signal | User's Implicit Question | Evaluation Focus |
|------|--------|------------------------|-----------------|
| **福利文** | Free API key, free credits, free trial, coupon code | "Is this real? Can I use it?" | Verify claim → Test endpoint → Check against existing setup |
| **工具文** | New tool, library, framework, GitHub project | "Should I try this?" | Assess maturity → Relevance to stack → Compare with alternatives |
| **知识文** | Analysis, tutorial, deep dive, architecture breakdown | "Is this worth reading?" | Quality check → User relevance → Wiki storage decision |
| **商业案例** | Startup story, business model analysis | "What can I learn from this?" | Extract actionable insight → Relevance to user's own work |
| **资源合集** | Book lists, course collections, project index | "Is this worth bookmarking?" | Quality check → Likelihood of actual use |

## Evaluation Checklist (per type)

### 福利文
1. **Verify the claim** — Does the article make specific, testable numbers? (e.g., "10万积分" vs official "1万积分")
2. **Test endpoint** — Attempt a quick API call (GET/POST) to verify availability
3. **Check real status** — 200 = live, 402/429 = exhausted, 403 = no access
4. **Check compatibility** — OpenAI-compatible? Needs special adapter? Works with existing config?
5. **Assess effort vs value** — How many steps to claim? How much value? (e.g., Firecrawl 10k credits ≈ $300-400 → worth 10 min of effort)
6. **Document steps** — If actionable, produce numbered step-by-step guide

### 工具文
1. **Check maturity** — GitHub stars, last commit, license
2. **Check relevance** — Does it solve a problem the user currently has?
3. **Compare with alternatives** — What does the user already have that overlaps?
4. **Verdict** — "Use now" / "Wait and track" / "Skip" / "Reference only"
5. **If "use now":** produce setup guide. **If "track":** bookmark GitHub link + note why

### 知识文
1. **Quality check** — Information density, originality, actionable insights
2. **Check for soft ads** — Affiliate links, referral codes, paid-course plugs at end
3. **Decode signal from noise** — Extract the 20% that's valuable, filter out marketing
4. **Wiki storage decision** (see next section)

## Ingestion Depth Decision Tree

After evaluation, decide what to store in wiki:

```
Article evaluated
    │
    ├── Quality/Relevance?
    │   ├── HIGH (original insights, actionable, non-obvious) → [A] Full ingestion
    │   ├── MEDIUM (good reference, complements existing knowledge) → [B] Light ingestion
    │   └── LOW (fluff/expired/news-only) → [C] Skip or raw-only
    │
    ├── Type-specific rules:
    │   ├── 福利文 → raw only (expires fast, low long-term value unless the platform persists)
    │   ├── 工具文 → raw + entity (author) if author is new; concept if new pattern
    │   ├── 知识文 → raw + entity + concept (maximal extraction)
    │   └── 商业案例 → raw only (one-off narrative, not a reusable concept)
    │
    └── Author already in wiki?
        ├── Yes → skip entity creation, just update if needed
        └── No → create entity page
```

### Ingestion Levels

| Level | What to Create | When | Example |
|-------|---------------|------|---------|
| **A: Full** | raw + entity + concept + possible concept update | Article has standalone knowledge value that transcends the specific article | Hermes prompt engineering deep-dive → created concept "hermes-prompt-engineering-five-principles" |
| **B: Light** | raw + entity OR raw + concept update | Article is decent but not foundational | Agent Harness architecture → raw + entity only |
| **C: Minimal** | raw only OR nothing | Thin content, expired deals, fluff | Expired API福利, free-programming-books list (bookmark only) |

## Concept Page Extraction

When an article contains reusable knowledge that transcends the article itself, extract a concept page:

1. **Identify the core idea** — What principle/framework/pattern does the article teach?
2. **Distill to essentials** — Remove article-specific context, keep the generalizable insight
3. **Structure for reference** — Make it navigable (headings, tables, principles)
4. **Cross-link** — Connect to related existing concepts via `[[wikilinks]]`
5. **Tag with source** — YAML frontmatter `source: raw/articles/xxx.md`

Example from this session: The "Hermes 魔鬼在细节里" article contained five prompt engineering principles that were extracted as a standalone concept page (`hermes-prompt-engineering-five-principles.md`). The article itself is raw material; the principles are the durable knowledge.

## Common Pitfalls

- **Soft ads in "knowledge" articles** — The 500-AI-Agents-Projects article had a pptoken.org referral link embedded as a "personal recommendation." Always scan for this.
- **SPA-dependent verification** — n8n Cloud, Firecrawl app, kiro.dev are all JS-heavy SPAs. You can't evaluate them via curl/CLI. Tell the user to check manually or use agent-browser.
- **Bing Chinese search is unreliable** — Searching "商汤 API" returns Chinese history (商 = Shang dynasty). Use English fallback: "SenseNova API" instead.
- **WeChat article numbers are often rounded up** — "10万积分" = 10,000 per official site. Always cross-check.
- **Public API keys in articles are already dead** — By the time the user sees the article, the key is being hammered by thousands of readers. Always test before recommending.
