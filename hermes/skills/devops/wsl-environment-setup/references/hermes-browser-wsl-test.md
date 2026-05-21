# Hermes Browser in WSL — Verification & Troubleshooting

Captured 2026-05-12 during Chrome CDP setup session.

## Environment Baseline

- WSL 2 (Ubuntu) with Docker Desktop integration, Hermes Agent self-deployed
- Windows 10.0.26200
- WSLg 1.0.73 installed, `/tmp/.X11-unix/X0` present, `/mnt/wslg/` present
- Playwright 1.59.0 (Chromium 1217) installed in Hermes venv
- agent-browser installed at `~/.hermes/hermes-agent/node_modules/.bin/agent-browser`
- Windows Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe`

## Quick Health Check

```bash
# 1. agent-browser works (no CDP needed)
~/.hermes/hermes-agent/node_modules/.bin/agent-browser navigate "https://example.com"

# 2. headful mode (needs DISPLAY=:0)
export DISPLAY=:0
~/.hermes/hermes-agent/node_modules/.bin/agent-browser navigate "https://example.com"

# 3. Playwright Chromium standalone
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    p = b.new_page()
    p.goto('https://httpbin.org/get')
    print(f'OK: {p.title()}')
    b.close()
"

# 4. agent-browser snapshot (accessibility tree)
~/.hermes/hermes-agent/node_modules/.bin/agent-browser snapshot
# Returns element tree with ref selectors for clicking
```

## Windows Chrome CDP Failure (From WSL)

### Symptom
After launching Windows Chrome from WSL with CDP flags:
- `netstat -ano | findstr 9222` shows nothing
- `curl http://127.0.0.1:9222/json/version` times out
- Chrome logs show: `bind() returned an error: WSAEACCES (0x271D)`

### Diagnosis
The error `WSAEACCES` (Windows Sockets Error 10013) means the Chrome process's security token — inherited from the WSL → Windows binary launch interop — doesn't have permission to bind TCP ports. This is not a Docker/firewall/port-conflict issue.

### Attempted Fixes (all failed)
- PowerShell `Start-Process` with various flags
- cmd.exe batch file (also fails due to UNC path limitation in WSL)
- VBScript `WScript.Shell.Run`
- `subprocess.Popen` from Python with `DETACHED_PROCESS`
- Different ports (not just 9222)
- Fresh user data dirs
- Killing all Chrome instances first

### Working Alternative
Use WSL's native Playwright Chromium as CDP endpoint (see SKILL.md's Browser CDP section) or just use agent-browser directly.

## WSLg DISPLAY Notes

- WSLg can serve GUI but DISPLAY is NOT set automatically in non-login shells or when Hermes spawns subprocesses
- Must explicitly set `export DISPLAY=:0` in the shell/session
- WSLg renders GUI windows as native Windows windows (visible in taskbar, resizable)
- No VNC/Tailscale needed for GUI — it's a local desktop integration feature

## Hermes Config for Browser

Current working config (`~/.hermes/config.yaml`):
```yaml
browser:
  inactivity_timeout: 120
  command_timeout: 30
  engine: auto          # falls back to agent-browser when no CDP
  cdp_url: 'http://127.0.0.1:9222'   # unused unless Chrome CDP is running
  dialog_policy: must_respond
```

`engine: auto` + dangling `cdp_url` is fine — if nothing listens on 9222, Hermes uses its built-in agent-browser automatically.
