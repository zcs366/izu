# Citation Schema Design (2026-05-16)

See full document: `wiki/prep/citation-schema-design.md`

## Key Design Decisions

1. **Inline citation format**: `✅[URL]` / `⚠️[来源]` / `❓[说明]` in markdown body. Compatible with standard markdown parsing while supporting programmatic extraction.

2. **Document-level metadata**: YAML frontmatter `references:` field with per-citation verification status (`verified/pending/dead/superseded`).

3. **Centralized citation graph**: Single `wiki/citation-graph.json` file (not distributed per-file) for global queryability. Nodes typed as `document/url/entity/concept/wiki_doc`. Edges typed as `支持/反驳/补充/延伸/引用/适用` with strength (`强/中/弱`) and `verified` boolean.

4. **Verification persistence**: Each pipeline run produces an independent verification report markdown file. The `citation-graph.json` is updated with `verified` state. Failed citations get tagged and can trigger rollback.

5. **Graceful degradation**: If full schema is too heavy, start with inline format only + URL reachability checks + terminal output (no graph file).

## Tools
- `scripts/extract_inline_citations.py` — extract inline citations from markdown
- `scripts/citation_graph.py` — read/write/update citation-graph.json
- `scripts/izu_citation_check.py` — pipeline step for citation verification
