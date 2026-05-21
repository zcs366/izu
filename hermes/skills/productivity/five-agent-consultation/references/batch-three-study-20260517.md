# 2026-05-17 Batch Three-Study Consultation

## Context
Three 极大 level studies accumulated during mass ingestion session:
1. **Evolver Engineering** (周昌) — Theoretical framework: Harness→Evolver transition
2. **Agent Memory Survey** (20+ institutions, arxiv:2602.052) — 3D classification framework
3. **Skills Replace Agent Frameworks** (Johnson7788) — Paradigm confirmation

## Flow
- Each study was independently evaluated first (wiki+output+HTML+log)
- Consultation was triggered after all three studies were evaluated (user said "启动三极大")
- Subagents ran sequentially: 子产→韩信→鲁班(interrupted)→军师直断

## Key findings

### 子产 priority
| P0 | Memory system (3 narrow: decay + working memory + self model) | 2 weeks |
|---|---|---|
| P1 | Evolver engineering (3 narrow: skill scoring + cost + eval dataset) | 3 weeks |
| P2 | Skills trend monitoring | ongoing cron |

### 韩信 vision
3-month end state: memory has structure, skills have evaluation, forgetting has algorithm.

### 军师终裁
P0 memory first. "地基不稳不盖二楼" — memory system POC must pass before Evolver starts.

## Pitfall documented
**Subagent fragility during rapid-fire sessions** — deepseek-chat subagents frequently interrupted by incoming user messages mid-consultation. Solutions:
1. Defer full consultation to post-batch (batch mode)
2. Use 军师直断 (direct judge) for mid-flow decisions
3. Do NOT start consultation while user is still actively sending links

## Outcome
Three P0 Python tools built post-consultation:
- `izu_session_memory.py` — decay curve + session audit (745 sessions scanned)
- `izu_working_memory.py` — top-k queue + WORKING.md
- `izu_self_model.py` — identity anchor extraction + versioning + diff
