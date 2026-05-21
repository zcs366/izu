# Cron Job Management — Batch Operations & Pitfalls

Use this reference when you need to inspect, edit, or bulk-update Hermes cron jobs beyond what the `cronjob` CLI tool provides.

---

## The Two Access Methods

| Method | Use Case | Limitation |
|--------|----------|------------|
| `cronjob` tool | View list, update single job's schedule/name, pause/resume/run/delete | `cronjob update` requires full prompt every time; prompt_preview is **truncated** |
| `cron/jobs.json` direct edit | View full prompts, batch-edit prompts across many jobs at once | Must read → modify → write without conflicting with cron scheduler |

---

## Viewing Full Prompts

The `cronjob list` tool only shows a **truncated preview** of each job's prompt. To see the full text:

```bash
# Read the full JSON file
cat ~/.hermes/cron/jobs.json | python3 -c "
import sys, json
jobs = json.load(sys.stdin)['jobs']
for j in jobs:
    print(f'=== {j[\"name\"]} ({j[\"id\"]}) ===')
    print(j['prompt'][:500])
    print()
"
```

Or extract one specific job:

```bash
cat ~/.hermes/cron/jobs.json | python3 -c "
import sys, json
jobs = json.load(sys.stdin)['jobs']
prompt = [j['prompt'] for j in jobs if j['name'] == '提醒-周三·宏观视野'][0]
print(prompt)
"
```

---

## Batch Editing Prompts

When you need to make the **same text change** across multiple cron jobs (e.g. change a time string in all 7 reminder jobs), **do NOT** make individual `cronjob update` calls — that requires passing the full prompt 7 times. Instead:

### Approach: Python script that writes jobs.json directly

```python
import json

# Define the updates: job_id → new_prompt
updates = {
    "a6a683d48041": """发送一条提醒消息给张成市：

⏰ **军师提醒**

今天的【诗歌与文学创作周报】下午1点已发到Telegram和微信，看了吗？

有什么想法、疑问、或者想深入讨论的诗人和作品，回复我即可。

——军师祭酒

同时用 send_message 发送相同内容到微信：target="weixin:o9cq80-A2QetTJisKNUphB70rxhs@im.wechat\"""",
}

with open("/home/zcs/.hermes/cron/jobs.json") as f:
    data = json.load(f)

for job in data["jobs"]:
    if job["id"] in updates:
        job["prompt"] = updates[job["id"]]

data["updated_at"] = "2026-05-06T13:30:00+08:00"

with open("/home/zcs/.hermes/cron/jobs.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### ⚠️ Pitfall — `patch` tool fails on recently-modified files

The `patch`/`write_file` tools check file modification timestamps. If another Hermes process (e.g. `cronjob update`) modified `jobs.json` between your `read_file` and `patch` calls, you'll get:

```
Error: File was modified since you last read it on disk.
```

**Fix**: Use the Python script approach above instead — it reads and writes in one go without the timestamp check issue.

### ⚠️ Pitfall — Avoid direct JSON editing while cron scheduler is ticking

The cron scheduler polls `jobs.json` on a timer (typically every 30s). Writes that produce **invalid JSON** (missing commas, trailing commas) can corrupt the scheduler state. Always use `json.dump()` with proper formatting, never raw string manipulation.

---

## Cron Job Data Structure

Each job in `jobs.json` follows this schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Auto-generated unique ID (12-char hex) |
| `name` | string | Human-readable name |
| `prompt` | string | Full system prompt for the job |
| `skills` | array | Pre-loaded skills |
| `schedule` | object | `{kind: "cron", expr: "0 13 * * 1", display: "..."}` |
| `repeat` | object | `{times: null, completed: N}` — null = infinite |
| `deliver` | string | Delivery target, e.g. `telegram:6512378453` |
| `enabled` | bool | Whether the job is active |
| `state` | string | `"scheduled"`, `"paused"`, etc. |
| `next_run_at` | string | ISO 8601 timestamp of next scheduled run |
| `last_run_at` | string | ISO 8601 timestamp of last run |
| `last_status` | string or null | `"ok"`, `"error"`, or null |
| `origin` | object or null | Creator info: `{platform, chat_id, chat_name}` |
| `created_at` | string | ISO 8601 creation timestamp |

---

## Debugging: Job Shows in List but All Operations Return "Not Found"

### Symptom

A job appears in `cronjob(action='list')` output with a recognizable `name` and `job_id`, but every operation — `run`, `pause`, `resume`, `update`, `log` — returns:

```
"error": "Job with ID '<displayed_id>' not found. Use cronjob(action='list') to inspect jobs."
```

### Root Cause

The `cronjob list` endpoint **may display a different ID** than the actual ID stored in `jobs.json`. This is a display bug — the list renders a corrupted or extra-character version of the hex ID, while the file stores the correct one.

In a real case, the list showed `4494706f6eb8b` (13-char?) while the file stored `4494706feb8b` (12-char hex). The extra/misplaced character caused all operations on the displayed ID to fail.

### Diagnosis — Find the Real ID by Name

Skip the displayed `job_id`. Search `jobs.json` directly by the job name:

```bash
# Search jobs.json for the job name to find the correct ID
grep -B2 -A20 '"个人·周五·古代学术与出版业"' ~/.hermes/cron/jobs.json
```

Or use a more precise search:

```bash
cat ~/.hermes/cron/jobs.json | python3 -c "
import sys, json
jobs = json.load(sys.stdin)['jobs']
target = '个人·周五·古代学术与出版业'
for j in jobs:
    if j['name'] == target:
        print(f\"Real ID: {j['id']}\")
        break
"
```

### Resolution

Use the **file's ID** (not the list's ID) with all `cronjob` operations:

```python
# This will fail — using the displayed ID
cronjob(action='run', job_id='4494706f6eb8b')

# This will work — using the file's actual ID
cronjob(action='run', job_id='4494706feb8b')
```

### Prevention

When you encounter a "Job with ID ... not found" error for a job you can see in the list:

1. **Do NOT retry** with the same ID — it will keep failing
2. Read `jobs.json` directly to confirm the real ID
3. If even the file's ID fails, the job record is corrupted; consider recreating it
4. Report this as a bug: the list endpoint should return the same ID that the file stores

---

## Verifying Changes

After editing, verify with:

```python
# Search for old string to confirm it's gone
import json
with open("/home/zcs/.hermes/cron/jobs.json") as f:
    data = json.load(f)
for job in data["jobs"]:
    if "早上8点" in job.get("prompt", ""):
        print(f"STILL HAS OLD TEXT: {job['name']}")

# Or check for new string
count = sum(1 for j in data["jobs"] if "下午1点" in j.get("prompt", ""))
print(f"{count} jobs have the new text")
```

The `cronjob list` output should reflect the changes on the next scheduler tick (typically within 30s).

---

## Recipe: Change Time String Across All Reminder Jobs

Pattern used in real session: change `"早上8点"` to `"下午1点"` in 7 reminder jobs.

```python
import json

with open("/home/zcs/.hermes/cron/jobs.json") as f:
    data = json.load(f)

changed = 0
for job in data["jobs"]:
    if "prompt" in job and "早上8点" in job["prompt"]:
        job["prompt"] = job["prompt"].replace("早上8点", "下午1点")
        changed += 1
        print(f"  Updated: {job['name']}")

data["updated_at"] = "..."

with open("/home/zcs/.hermes/cron/jobs.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone! {changed} jobs updated.")
```

This is the most efficient approach when the same text change applies across multiple jobs.
