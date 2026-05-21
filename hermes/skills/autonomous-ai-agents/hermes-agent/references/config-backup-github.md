# Hermes Config Backup to GitHub

Securely backup your Hermes Agent configuration (.hermes directory) to a GitHub repository, including skills, scripts, and sanitized config — without exposing API keys or secrets.

## When to Use

- User wants to version control their Hermes setup
- User needs a "project" to show for API credit applications (MiMo 100T, etc.)
- User wants to replicate their setup on another machine
- User asks to "back up my Hermes config to GitHub"

## Workflow

### 1. Assess What to Include

| Include | Exclude |
|---------|---------|
| `config.yaml` (sanitized) | `.env` — contains ALL API keys |
| `SOUL.md` | `auth.json` — OAuth tokens |
| `skills/` (all SKILL.md + refs) | `sessions/` — chat transcripts |
| `scripts/` (custom scripts) | `logs/` — runtime logs |
| `bin/` (custom binaries) | `*.db`, `*.db-shm`, `*.db-wal` — SQLite databases |
| Cron config (`cron/jobs.json`) | `cache/`, `audio_cache/`, `image_cache/` |
| Gateway state (non-sensitive) | `checkpoints/`, `spawn-trees/`, `state-snapshots/` |
| | `cron/output/` — past job outputs |
| | `skill_backups/`, `sandboxes/`, `pastes/` |
| | `plugins/`, `node/`, `__pycache__/` |

### 2. Sanitize config.yaml

The `config.yaml` file contains API keys in these sections:
- `providers.*.api_key` — provider credentials
- `delegation.api_key` — subagent model key
- `auxiliary.*.api_key` — vision, compression, etc.
- `mcp_servers.*.headers.Authorization` — MCP Bearer tokens
- `platforms.*.extra.*` — app secrets and channel IDs

**Sanitization checklist** — replace each with a placeholder:

```yaml
# Before:
api_key: sk-or-PLACEHOLDERv1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# After:
api_key: YOUR_OPENROUTER_API_KEY_HERE
```

Also sanitize:
- Bearer tokens: `Bearer [REDACTED]-xxx` → `Bearer YOUR_TINYFISH_TOKEN`
- App IDs/secrets: `app_id: xxx` → `app_id: YOUR_APP_ID`
- Channel IDs: `direct:xxx` → `direct:your_channel_id_here`
- Any private IPs (optional): `http://192.168.1.7:11234` → `http://your-local-server:port`

### 3. Create GitHub Repository

**Via GitHub API (when `gh` CLI not available):**

```python
import requests, base64

token = "ghp_xxxxxxxxxxxx"  # Personal Access Token
headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

# Create private repo
r = requests.post("https://api.github.com/user/repos", headers=headers, json={
    "name": "hermes-agent-config",
    "description": "Hermes Agent configuration backup",
    "private": True,  # Private by default for security
    "auto_init": False
})

# Upload files via Contents API
def upload(path, content, message="Add file"):
    data = {"message": message, "content": base64.b64encode(content.encode()).decode()}
    requests.put(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
                 headers=headers, json=data)
```

**Via `gh` CLI (recommended for interactive use):**
```bash
gh repo create hermes-agent-config --private --description "Hermes Agent config backup"
git init
git add .
git commit -m "Initial backup"
git branch -M main
git remote add origin https://github.com/<user>/hermes-agent-config.git
git push -u origin main
```

### 4. .gitignore Template

```gitignore
# Secrets and credentials
.env
.env.*
*.pem
*.key
auth.json
channel_directory.json

# Session data and logs
sessions/
logs/
*.log

# Database files
*.db
*.db-shm
*.db-wal
*.sqlite

# Cache and temp
cache/
audio_cache/
image_cache/
images/
tool_cache/
checkpoints/
spawn-trees/
state-snapshots
cron/output/
skill_backups/
sandboxes/
pastes/
pairing/
hooks/
plugins/
node/

# Compiled
__pycache__/
*.pyc
```

### 5. Upload Strategic Skills

For a backup repo, upload all active skills. But if the goal is a **showcase project** (e.g., for API credit applications), select the most impressive custom skills:

| Skill | Why it's impressive |
|-------|-------------------|
| `wife-base` | Real business support system — proves practical AI application |
| `research/wiki-*` | Knowledge management pipeline — shows technical depth |
| `parenting/*` | Non-trivial domain application |
| `creative/*` | Content generation capabilities |
| Custom scripts | Shows system-level integration |

Skip: bundled/default/third-party skills that ship with Hermes. Focus on what the user built or configured themselves.

### 6. README Template

Include a README that describes:
- What this setup does
- Key highlights (number of skills, unique integrations)
- How to use/deploy
- Security note about API keys

**Example for API credit applications** (MiMo 100T, etc.): Mention specific integrations, custom skills, real-world use cases, and multi-platform setup.

## Security Rules (CRITICAL)

1. **NEVER upload `.env`** — it contains all API keys
2. **NEVER upload `auth.json`** — OAuth tokens
3. **Sanitize `config.yaml`** — replace every key/token with a placeholder
4. **Check for embedded credentials in scripts** — some scripts may contain hardcoded tokens
5. **Use private repos by default** — only make public if explicitly requested
6. **Verify after upload** — `grep -r "sk-"` on the repo to catch missed keys

## Verification

After upload, verify:
```bash
grep -rn "sk-" config.yaml scripts/ skills/  # Should show NO real keys
grep -rn "api_key:" config.yaml              # Should show only placeholders
grep -rn "Bearer" config.yaml                # Should show only placeholders
```

## Related

- `hermes config edit` — view/edit config
- `hermes config env-path` — locate .env
- `hermes config check` — verify config integrity
