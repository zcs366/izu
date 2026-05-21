---
name: daily-briefing-system
description: "Set up recurring daily topic-based briefing reports delivered via cron jobs to multiple messaging platforms (Telegram + WeChat), with fixed-point structure, flexible news items, information source attribution, and auto-reminder system."
version: 1.0.0
author: Hermes Agent
tags:
  - cron
  - briefing
  - daily-report
  - content-curation
  - multi-platform
  - reminder
metadata:
  hermes:
    category: productivity
------

# Daily Briefing System

A reusable pattern for setting up **automated daily content briefings** — delivering curated, topic-specific reports to the user every morning via multiple messaging platforms, with a follow-up reminder system.

## When to Use This Skill

Trigger: The user asks to set up "每日简报", "每周周报", "定时推送", "daily briefing", "content digest", or any recurring information delivery schedule covering multiple topics across different days of the week.

## Core Architecture

The system has three layers:

```
Layer 1: Report Cron Jobs (daily, e.g. 09:00)
  └─ Each day → one self-contained agent session
  └─ Deliver to one primary platform (e.g. Telegram)
  └─ Save to archive file

Layer 2: Reminder Cron Jobs (evening, e.g. 18:00)
  └─ Each day → one reminder message
  └─ "今天的XX周报看了吗？回复我"
  └─ Same primary platform

Layer 3: Archive Directory
  └─ /output/weekly_reports/DDD-topic-YYYY-MM-DD.md
```

## Delivery Architectures

There are two valid delivery architectures — choose based on user preference:

### A. Dual-Push (both platforms get auto-delivered)
- One cron job pushes report to Platform A (via `deliver` parameter)
- The cron job prompt instructs agent to `send_message` to Platform B
- Same pattern for reminders
- Best for: users who consume content on both platforms equally

### B. Dual-Track (one auto, one on-demand)
- Cron jobs push to Platform A only (no `send_message` to Platform B in prompt)
- On Platform B, the user requests reports on-demand by saying "发周报" (or e.g. "周一的")
- When requested, the agent generates the report in the **current conversation session**, using web search for current data and the report structure template
- Best for: users who want different engagement patterns per platform (e.g. auto-push on Telegram for notification, on-demand on WeChat for deeper discussion)
- **Pitfall:** On-demand generation means the agent must be able to search the web for current information and compose the full report in one session. No pre-canned reports.

## Report Structure Template

Each daily briefing follows this structure:

### 📊 五个固定关注点（必须填满，每条60-150字）

5 topic-specific fixed points that remain consistent week over week (for trend tracking).

### 🔄 灵活快讯（5-10条）

Flexible items based on current events. One sentence each.

### 💡 点睛（可选）

A closing insight, quote, or call-to-action relevant to the day's topic.

### 📎 信息源

Every piece of sourced information must include the name and URL link at the bottom of the report. **This is a hard requirement — the user insisted on information source attribution.**

## Cron Job Prompt Structure

Each cron job prompt must be **fully self-contained** — it runs in a fresh agent session with zero context from prior conversations.

### Essential Elements in Every Prompt

1. **Role definition** — who the agent is (e.g. "你是军师祭酒")
2. **User context** — who the report is for and their specific interests
3. **Report structure** — the exact format to follow (5 fixed + 5-10 flexible + source attribution)
4. **Delivery instructions** — the final response is auto-delivered. For Dual-Push architecture, ALSO use send_message to the second platform. For Dual-Track, no second-platform delivery in prompt.
5. **Save instructions** — write to an archive file
6. **Execution flow** — web_search → web_extract → compose → output

### Dual-Delivery Pattern (Architecture A: Dual-Push)

The cron job's `deliver` parameter sends to ONE platform. For dual-push, the prompt must instruct the agent to use `send_message` for the second platform:

```python
# In the cron job prompt:
# "1. Your final response IS the report (auto-delivered to Telegram)
#  2. ALSO use send_message to deliver to WeChat: target='weixin:USER_ID@im.wechat'
#  3. Save to file: /path/to/archive/DDD-topic-$(date +%Y-%m-%d).md"
```

### On-Demand Pattern (Architecture B: Dual-Track)

When the second platform is on-demand, cron jobs only push to primary. On the second platform, when user says "发周报" or "周三的" etc:

1. Determine current day → topic
2. Web search latest news per fixed points
3. Compose 5-fixed + 5-10-flexible structure
4. Deliver in current conversation
5. Save to archive file

### Reminder Cron Job Pattern

Create a separate cron job at 18:00 (or desired time) on the same day as the report:

- Prompt: simple reminder message with a nudge
- Dual-Push: deliver to one + send_message to the other
- Dual-Track: deliver only to primary platform (no second-platform reminder)
- Name convention: `提醒-周X·主题`

## Scheduling Reference

Configure exact times per user preference. Common patterns:

| Cron Expression | Meaning | Example Use |
|----------------|---------|-------------|
| `0 8 * * 1` | Monday at 08:00 | Report (early morning) |
| `0 9 * * 1` | Monday at 09:00 | Report (after commute) |
| `0 18 * * 1-7` | Daily at 18:00 | Reminder (evening check) |

## Multi-Topic Layout (Seven-Pulse Framework)

When the user has multiple interest areas, organize them across the week in descending seriousness order:

| Day | Topic | Tone | Fixed Points (Example) |
|-----|-------|------|----------------------|
| Mon | Serious interest #1 (e.g. poetry) | Formal, deep | 行业动态+经典推荐+新作品评+理论+出版 |
| Tue | Serious interest #2 (e.g. parenting) | Warm, practical | 新研究+方法+资源+技巧+共读 |
| Wed | Macro/current affairs | Analytical | 军事/国防+中国经济+世界经济+政策+热点 |
| Thu | Technology | Fast, info-dense | 美一梯队+美二梯队+中国企业+生态+亮点 |
| Fri | Academic/publishing | Scholarly | 考古+论文+新书+出版+编辑 |
| Sat | Self-improvement | Actionable | 新思路+新任务+新机会+新方法+践行 |
| Sun | Lifestyle/wellness | Relaxed, warm | 健身+冥想+园艺+饮食+放松 |

## Delegation for Research

When researching multiple topics to populate the initial 信息源清单, use `delegate_task` for parallel research:

```python
# Split into batches of 3 (max_concurrent_children default)
delegate_task(tasks=[
    {"context": "...", "goal": "...", "toolsets": ["web"]},
    {"context": "...", "goal": "...", "toolsets": ["web"]},
    {"context": "...", "goal": "...", "toolsets": ["web"]},
])
```

**Critical pitfall:** `delegate_task` has a hard limit of `max_concurrent_children=3` (configurable in config.yaml). If you pass more than 3 tasks, the call fails with an error. Split into multiple batches.

## 具体报告类型实例

本框架已产出的具体报告类型：

### Skills Hub 生态系统周刊（每周日 10:00）

触发：用户说"去 Skills Hub 逛逛"或 cron 自动执行。
产出：`hermes-skills-hub-weekly-report-v{N}.md` + `.html`

报告结构：巡市快照 → Tool进展 → 社区新星 → 替代性评估 → 推荐Top N → 行动清单。
数据源：agentskills.io HTML抓取 + GitHub API (Hermes releases/commits/community repos) + 本地技能对比。
HTML渲染模板：`templates/briefing-html-dark-theme.html`（暗色主题，960px容器，打印优化，零外部依赖）。
完整方法论：`references/skills-hub-weekly-report.md`

如需新增其他主题的周报（如"AI论文周刊""竞品动态日报"），在此基础上复制模板即可。

## Common Pitfalls

### Pitfall: Large number of cron jobs fails on single create call
Each cron job requires one `cronjob(action='create')` call. You CANNOT batch-create cron jobs. Create them sequentially or in parallel batches using independent calls.

### Pitfall: Prompts must be fully self-contained
Cron job sessions start fresh — they have NO access to:
- The current conversation history
- Skills loaded in the parent session
- Variables or context from the initiating session
- Memory (if not explicitly configured)

Every prompt must include: role definition, user info, structure, delivery, and save instructions.

### Pitfall: Report requires information sources
The user may require that every piece of sourced information has a URL attribution at the bottom of the report. This is a non-negotiable requirement — enforce it in the prompt structure as a dedicated section.

### Pitfall: send_message requires correct target format
For WeChat: `target="weixin:USER_ID@im.wechat"`
For Telegram (if not the auto-delivery target): check the user's Telegram ID

### Pitfall: 18:00 reminders are independent cron jobs
The reminder system uses SEPARATE cron jobs, not conditional logic within the report job. Create them as independent `cronjob(action='create')` calls with their own schedule and prompt.

### Pitfall: web_search / web_extract API may be unavailable in cron sessions
When generating reports in cron sessions, web_search and web_extract may fail with "Payment Required" if firecrawl API credits are exhausted. The fallback chain for report generation:

1. Try `web_search` first (fastest if credits available)
2. If failed → use `bing-search` skill (`~/.hermes/scripts/bing_search.sh`)
3. If `web_extract` also fails → use `curl -s -L <url>` to extract page content directly
4. If curl returns gzipped binary → try `curl -s -L --compressed <url>`

**Bing query strategy pitfall:** Avoid broad keywords like "古籍 2025" or "考古 新闻" — they return Baidu Baike/Zhihu pages, not news. Use precise event names (e.g. "2025年度全国十大考古新发现揭晓"). See the bing-search skill's keyword strategy table for details.

### Pitfall: Some topics have report-specific section formats
The generic `💡 点睛` section may be replaced by a topic-specific variant. For example, the Friday 古代学术·出版业 report uses `💡 本周书话` (a book recommendation with title, author, publisher, and rationale). Check the topic reference file for format variations before composing.

## References

The file `references/seven-pulse-张成市-weekly-briefing.md` in this skill directory contains the concrete implementation for a seven-topic weekly briefing system (Chinese-language poetry/parenting/defense/AI/academia/self-management/lifestyle), including all 14 cron job prompts, user preferences, and delivery configuration.

## Verifying the System

After creating all cron jobs, verify with:
```bash
hermes cron list
# Should show all report + reminder jobs as "scheduled"
```
