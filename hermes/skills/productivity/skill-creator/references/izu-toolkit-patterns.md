# IZU Toolkit Creation Pattern

Created from session 2026-05-18 where 5 Python tools were built for the IZU evolution engine.

## Standard Module Structure

Each `izu_*.py` tool follows this pattern:

```python
#!/usr/bin/env python3
"""
izu_something.py — Module description

用法:
  python3 izu_something.py subcommand [args]
"""
import sys, json, os
from pathlib import Path
from datetime import datetime

# Paths
IZU_DIR = Path(__file__).parent
DATA_DIR = Path('/mnt/i/hermes/data')
OUTPUT_DIR = Path('/mnt/i/hermes/output/doc/<category>')

# If importing sibling modules
sys.path.insert(0, str(IZU_DIR))
```

## CLI Subcommand Pattern

Use a dict-based dispatch at the bottom:

```python
if __name__ == '__main__':
    cmds = {
        'sub1': cmd_func1,
        'sub2': cmd_func2,
    }
    c = sys.argv[1] if len(sys.argv) > 1 else 'default'
    cmds.get(c, lambda: print(__doc__))()
```

## Cross-Module Import (Critical)

Tools import from each other. Always prepend `IZU_DIR` to `sys.path`:

```python
sys.path.insert(0, str(IZU_DIR))
from evolution_engine import Scorer, Verifier
```

This works because all tools live under `/mnt/i/hermes/izu/`.

## Error: Path for skill_scanner's `score_skill`

When scanning many files (137 SKILL.md files), the **URL validity check** in `Verifier.check_urls()` does `curl` on every URL found. This:
- Times out on large batches (>30 files)
- Blocks the entire scan

**Fix:** Add a `skip_url_check` parameter:

```python
def score_skill(skill, skip_url_check=False):
    if skip_url_check:
        # Default URL score to 0.8, skip curl
        url_validity = {"score": 0.8}
    else:
        # Full check
        url_validity = verifier.check_urls(content)
```

## Error: Session file Format Mismatch

Hermes stores sessions as **single JSON objects** (not JSONL):

```json
{
  "session_id": "...",
  "model": "...",
  "messages": [{"role": "user", "content": "..."}, ...]
}
```

But `trajectory_credit.load_from_hermes_jsonl()` expects **one JSON per line**. Both formats exist in the sessions directory. Handle both:

```python
raw = json.loads(path.read_text())
if isinstance(raw, dict) and 'messages' in raw:
    # Hybrid format: single JSON with messages array
    for msg in raw['messages']:
        ...
else:
    # JSONL format: one object per line
    for line in raw.strip().split('\n'):
        msg = json.loads(line)
```

## Output Structure

All reports go to `output/doc/<category>/<report_name>_<timestamp>.md`.

| Category | Path |
|----------|------|
| Memory health | `output/doc/memory_health/` |
| Skill health | `output/doc/skill_health/` |
| Evolution | `output/doc/evolution/` |
| Cost | `output/doc/cost/` |

## Rule-Based Processing Priority

**匠石铁律: 能用代码就别用模型.**

When building scoring/extraction tools, achieve ~90% of work with code rules:
- Keyword-based scoring (not LLM) for decision extraction
- Regex for URL extraction and citation counting
- Character count for token estimation
- Section markers for structure analysis

Reserve LLM for the final 10% — semantic quality judgment.

## Cron Deployment Pattern

For cron scripts that need absolute paths (cron requires scripts under `~/.hermes/scripts/`):

```bash
cp /mnt/i/hermes/izu/izu_script.py ~/.hermes/scripts/izu_script.py
```

Then reference by filename only in cronjob creation.
