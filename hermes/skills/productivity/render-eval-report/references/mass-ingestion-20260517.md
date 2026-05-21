# 2026-05-17 Mass Ingestion Session — Methodology Reference

## Overview
Single session processed 35+ articles across all levels: 7 极大, 14 大, 13 中/小, plus 2 tools built.
Dominant pattern: user sent links faster than full evaluation per item — rapid-fire mode was essential.

## Flow that emerged

```
User sends link (with or without level prefix)
  → Quick scan via web_extract
  → Level assessment (user prefix or content-based)
    → 极大: wiki/research/YAML + output/极大/plain + HTML + log
    → 大: wiki/research/YAML + output/大/plain + log
    → 中/小: single note file or log-only
  → Return to waiting for next link (do NOT ask questions)
```

## Critical rules for mass ingestion

1. **Never ask questions during rapid fire** — User sends links in volleys. Interrupting breaks flow.
2. **Level marks are binding** — If user says "极大" or "大", obey it. Do not second-guess.
3. **Parallelize 极大** — Use delegate_task for two 极大 lines simultaneously when both are pending.
4. **Batch log updates** — Append log.md entries in bulk after processing batch, not per-item during volley.
5. **Framework synthesis at end** — When batch is done, step back and synthesize the connections between articles into a meta-level evaluation. This turns fragments into system.

## Tool installation pitfalls documented this session

| Tool | Correct package | Gotcha |
|---|---|---|
| wx-cli | `@jackwener/wx-cli` | `wx-cli@1.0.0` is a 2016 unrelated package. Binary is `wx` not `wx-cli`. |
| render_report | `pip install markdown pygments` (pre-installed) | YAML frontmatter required for correct title/eval badge rendering. |

## Consultation overlap during mass ingestion

During this session, five-agent consultation was **fragile** — subagents (deepseek-chat) were frequently interrupted by new user messages. The lesson: during active mass ingestion, defer full consultation to post-batch. Use 军师直断 (direct judge mode) if needed mid-flow. Batch consultation mode (Section 10 of protocol) worked as designed — evaluate first, consult later.
