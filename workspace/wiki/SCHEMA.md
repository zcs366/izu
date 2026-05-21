# Wiki Schema

## Domain

文学、诗歌、中国古代学术、人工智能、计算机技术、个人知识管理

## Conventions

- File names: lowercase, hyphens, no spaces (e.g., `tang-poetry-overview.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
---
```

## Tag Taxonomy

- Literature: poetry, prose, criticism, translation, writing
- Ancient Chinese: classics, history, philosophy, philology
- AI/ML: model, architecture, training, inference, alignment
- Programming: python, javascript, web, devops, tool
- Personal: project, goal, habit, reflection
- Hermes: agent, skill, config, plugin
- Publishing: typst, latex, pdf, typesetting

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when fully superseded

## Update Policy

When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter
