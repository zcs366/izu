# Ecosystem Survey — Skills Hub & GitHub 生态巡查

> **Used in:** 2026-05-10 Skills Hub market report session
> **Purpose:** Weekly recurring survey of the AI agent skills ecosystem
> **Class-level technique** — reusable for any agent ecosystem (Hermes Skills Hub, MCP servers, Claude Code skills, etc.)

## Survey Target Types

| Type | What to check | Method |
|------|--------------|--------|
| **Skills Hub** (agentskills.io) | Total skills, new categories, trending | `curl -sL https://agentskills.io` → parse sidebar categories |
| **Hermes Agent GitHub** | Recent releases, new tools, commits | GitHub API: `releases`, `commits`, `contents/skills` |
| **Community repos** | New SKILL.md repos, popular ones | GitHub search: `q=agent+skill+SKILL.md&sort=updated` |
| **Built-in skills** | Current onboarded skills | `skills_list` tool or check `~/.hermes/skills/` |

## Data Collection Commands

### Skills Hub total count + category distribution
```bash
curl -sL https://agentskills.io | grep -oP '[0-9]+ Skills' | head -5
```

### Hermes Agent recent commits
```bash
curl -sL "https://api.github.com/repos/NousResearch/hermes-agent/commits?per_page=10"
```
Extract: commit message, author, date. Look for: `feat`, `fix`, security-related, new tool additions.

### Hermes Agent latest release
```bash
curl -sL "https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=1"
```
Extract: tag_name, name, body (changelog). Key sections: Highlights, new tools, security fixes.

### Hermes Agent skills directory
```bash
curl -sL "https://api.github.com/repos/NousResearch/hermes-agent/contents/skills"
```
Lists all built-in skill directories. Compare against what's already onboarded.

### Trending community skills
```bash
curl -sL "https://api.github.com/search/repositories?q=SKILL.md+agent&sort=updated&per_page=15"
```
Extract: name, stars, description, updated_at. Flag repos with rapid growth or from known developers.

### Hermes Agent docs skills page
```bash
curl -sL "https://hermes-agent.nousresearch.com/docs/skills"
```
Shows the full registry: built-in (87) + optional (76) + community (521) with categories.

## Analysis Template

For each survey, produce:

1. **Snapshot**:
   - Total skills (current vs last week delta)
   - New categories / removed categories
   - New Hermes Agent version (if any)

2. **New tools worth noting**:
   - Tool name, what it does, why it matters to this user

3. **Community picks**:
   - Top 3 new community repos with descriptions
   - Any repos from known developers/builders

4. **Replacement detection**:
   - For each of the user's onboarded skills, check if a community skill provides the same or better function
   - Flag if a built-in Hermes skill now supersedes a custom one

5. **Recommendations** (top 5):
   - Most actionable items for the user this week

## Output Convention

- Versioned: `hermes-skills-hub-weekly-report-v{N}.{md|html}`
- Dual format: MD + HTML always
- Path: `I:\hermes\output\doc\`
- Cron: weekly on Sunday 10:00
- Top recommendations must come first — the user reads the first 3 lines, decides whether to keep reading
