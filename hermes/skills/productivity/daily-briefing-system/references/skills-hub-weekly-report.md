# Skills Hub Weekly Survey — 具体报告类型

> 这是 daily-briefing-system 框架的一个具体实例：每周日10:00的 Hermes Skills Hub 生态系统巡查报告。
> 摘自原 `skills-hub-survey` 技能（已合并到此伞下）。

## 报告触发

- 用户说"去 Skills Hub 逛逛" / "skill 市场有什么新东西" / "做一期技能市场报告"
- 或按 cron 自动执行（每周日 10:00）

## 数据收集（Phase 1）

### Source A: agentskills.io (当前状态)

```bash
curl -sL https://agentskills.io 2>&1 | grep -oP '(?<= )[0-9]+(?= skills across)' | head -1
curl -sL https://agentskills.io 2>&1 | grep -oP '(?<= )[0-9]+(?= Built-in)' | head -1
curl -sL https://agentskills.io 2>&1 | grep -oP '(?<= )[0-9]+(?= Optional)' | head -1
curl -sL https://agentskills.io 2>&1 | grep -oP '(?<= )[0-9]+(?= Community)' | head -1
```

### Source B: Hermes Agent GitHub (官方 releases & commits)

```bash
# Latest release
curl -sL "https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=3" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for r in data:
    print(f\"  [{r['tag_name']}] {r['name']} ({r['published_at'][:10]})\")
"

# Recent commits
curl -sL "https://api.github.com/repos/NousResearch/hermes-agent/commits?per_page=10" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for c in data:
    msg = c['commit']['message'].split(chr(10))[0][:90]
    print(f\"  [{c['sha'][:7]}] {c['commit']['author']['name']}: {msg}\")
"
```

### Source C: GitHub community skills repos

```bash
curl -sL "https://api.github.com/search/repositories?q=agent+skill+SKILL.md&sort=updated&per_page=10" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for r in data.get('items',[]):
    print(f\"  ★{r['stargazers_count']} {r['name']}: {r['description'][:80]}\")
    print(f\"     {r['html_url']}\")
    print(f\"     Updated: {r['updated_at'][:10]} | Lang: {r.get('language','N/A')}\")
"
```

## 报告结构

| Section | Content |
|---------|---------|
| **Header** | Title, date, version, scope (呈：张成市) |
| **一、巡市快照** | Total skills, category changes, notable additions. Table with before/after if vN-1 exists. |
| **二、Tool 进展** | New Hermes release features, tool fixes, security updates. |
| **三、社区新星** | New/trending community skills. Stars, description, why it matters. |
| **四、替代性评估** | Any community skill that could replace local skills. If none, state "自制护城河稳固". |
| **五、推荐 Top 5/10** | Actionable recommendations, prioritized by user's pain points. Emoji tier markers. |
| **六、行动清单** | Today / This week / This month checklists. `- [ ]` format. |
| **Footer** | `*报告结束 · 每周日更新 · 下一期：{next_sunday}*` |

## 输出要求

1. **DUAL OUTPUT**: Always produce both `.md` and `.html` files. Never PDF.
2. **LOCATION**: Save to `I:\hermes\output\doc\` (WSL: `/mnt/i/hermes/output/doc/`)
3. **VERSIONING**: Format: `hermes-skills-hub-weekly-report-v{N}.md` and `.html`. N increment. Never overwrite.
4. **STYLE**: Chinese report. Concise. Tables. Emoji markers (🔴🟡🟢🥇🥈🥉).
5. **HTML conversion**: Use Python `markdown` library. Template in `templates/briefing-html-dark-theme.html`.

## 已知陷阱

1. **GitHub API rate limits** (60 req/hr unauthenticated) — batch queries, minimize calls.
2. **agentskills.io is SPA (Next.js)** — HTML response is large (~250KB), content hydrated by JS. Use grep patterns on pre-rendered state.
3. **Version naming continuity** — Original v1.0 was `hermes-skills-hub-market-report-v1.0`. Cron uses `weekly-report-v2.0+`.
4. **Cron job uses bing-search skill** but actual collection uses curl/GitHub API directly.
