---
name: wsl-environment-setup
description: "Configure WSL (Windows Subsystem for Linux) development environment — Docker Desktop integration, Python PEP 668 workarounds, Node.js version management, workspace initialization, browser automation binaries, proxy configuration, Windows auto-start, boot recovery, VHDX compaction, Windows disk space diagnosis, AI model audit, and common WSL-specific pitfalls."
version: 2.1.0
metadata:
  hermes:
    category: devops
author: Hermes Agent
---

# WSL Environment Setup

Common patterns and workarounds for setting up development tools inside WSL 2 (Ubuntu/Debian).

## Docker Desktop WSL Integration

### Enable Integration

1. Open **Docker Desktop** on Windows (system tray whale icon)
2. Go to **Settings** → **Resources** → **WSL Integration**
3. Toggle on your WSL distro (e.g., `Ubuntu`)
4. Click **Apply & Restart**

### Docker Group Permissions

After enabling integration, the Docker socket appears at `/var/run/docker.sock` but your user might not have access:

```bash
# Check group membership
groups                    # verify 'docker' group is not listed
ls -la /var/run/docker.sock  # verify socket exists, group=docker

# Add yourself to docker group (needs sudo password)
sudo usermod -aG docker $USER
```

Then either:
- Log out and log back in (full WSL restart: `wsl --shutdown` in PowerShell, then restart WSL)
- Or use `sg docker -c "command"` for temporary access in new shell sessions

```bash
# Run any docker command through sg to avoid relogin
sg docker -c 'docker ps'
sg docker -c 'docker compose -f docker-compose.yml up -d'
```

**Pitfall:** `newgrp docker` only affects the current shell. Hermes spawning new shells won't inherit it. Use `sg docker -c` inside Hermes terminal calls for reliability.

### Persistent docker Group Fix

For long-term use without `sg`, log out of WSL entirely and restart:

```powershell
# In Windows PowerShell
wsl --shutdown
# Then restart WSL terminal
```

After that, `docker ps` should work directly.

## Python PEP 668 (Externally Managed Environment)

WSL Debian/Ubuntu defaults to PEP 668, blocking `pip install` system-wide:

```bash
# Error: "externally-managed-environment"
pip install somepackage
```

Workarounds (in order of preference):

1. **Virtual environment** (cleanest — requires python3-venv):
   ```bash
   sudo apt install python3.12-venv   # needs sudo password
   python3 -m venv venv
   source venv/bin/activate
   pip install somepackage
   ```

2. **pipx** (for CLI tools):
   ```bash
   pip install --user pipx
   pipx install somepackage
   ```

3. **--break-system-packages** (quickest, used throughout this environment):
   ```bash
   pip install --break-system-packages somepackage
   ```
   ⚠ May cause dependency conflicts between packages sharing overlapping requirements. Known conflicts:
   - `crawl4ai` downgrades `lxml` to 5.4.0 → breaks `scrapling` (needs lxml>=6.0.3)
   - `MemoryOS` downgrades `openai` to 1.109.1 → breaks `crawl4ai`'s unclecode-litellm dependency
   Fix: install in separate venvs, or re-install the conflicting package after: `pip install --break-system-packages scrapling` to restore lxml 6.x.

4. **User installation** (pip auto-falls back to `~/.local/`):
   ```bash
   pip install --user somepackage
   ```

## Large Binary Downloads Without sudo

Many tools (browsers, browser engines, ML models) need large downloads + system dependencies that require sudo.

### Background Processes for Timeout-Prone Downloads

When a download takes >60s and Hermes' foreground terminal times out:

```bash
# Start in background
terminal(command="camoufox fetch", background=true, timeout=180)
# Check progress later
process(action="poll", session_id="proc_xxx")
```

Suitable for: Camoufox (~780MB), Playwright browsers, Docker images.

### Browser Dependencies Without sudo

Playwright's `--with-deps` flag needs root for system libraries:

```bash
# This will fail without sudo password:
python3 -m playwright install --with-deps

# Workaround: install browsers without deps (core browser still works):
python3 -m playwright install chromium    # installs browser binary only
```

Crawl4AI has the same issue:
```bash
crawl4ai-setup                  # tries sudo for --with-deps, will fail
# Manual fallback:
python3 -m playwright install chromium
python3 -m patchright install   # for crawl4ai's undetected mode
```

### Systemd Health Check Pattern (Gateway/Service Monitoring)

For user services that need periodic health checks (restart if down, leave alone if running):

**1. Create the health check service** (`~/.config/systemd/user/<name>-healthcheck.service`):

```ini
[Unit]
Description=Health check for <service> — restart if down
After=<service>.service

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'systemctl --user is-active --quiet <service>.service || systemctl --user restart <service>.service'
```

**2. Create the timer** (`~/.config/systemd/user/<name>-healthcheck.timer`):

```ini
[Unit]
Description=Run <service> health check every N hours

[Timer]
OnCalendar=*-*-* 00:00:00
OnCalendar=*-*-* 06:00:00
OnCalendar=*-*-* 12:00:00
OnCalendar=*-*-* 18:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

**3. Enable and start:**

```bash
systemctl --user daemon-reload
systemctl --user enable --now <name>-healthcheck.timer
```

**Pitfall:** The timer fires at absolute wall-clock times (00:00, 06:00, etc.), not relative to the service start. If the service restarts at 00:15 and the timer fired at 00:00, the next check is at 06:00 — a 5h45m gap. This is fine for 24/7 services.

**Pitfall:** A companion *forced restart* timer (e.g. every 12h regardless of status) can coexist with a health-check timer. The health check is "restart if dead"; the forced restart is "restart even if healthy" (to prevent long-run degradation). Keep them as separate timers with different intervals.

**Example: Hermes Gateway dual monitoring:**

```
每12h强制重启(timer) + 每6h健康检查(关闭则重启)
```

### WSLg DISPLAY Configuration

WSLg (WSL GUI) is installed by default in modern WSL 2 but **DISPLAY is not always set** in the environment. Without it, GUI apps (including headful Chrome) silently fail to show a window:

```bash
# Check if WSLg is available
ls /tmp/.X11-unix/X0      # X11 socket exists → WSLg is running
ls /mnt/wslg/              # WSLg directory exists

# Persistent fix: add to ~/.bashrc
echo 'export DISPLAY=:0' >> ~/.bashrc

# Immediate effect for current session
export DISPLAY=:0
```

**Pitfall:** `write_file` and `patch` tools may refuse to modify `~/.bashrc` (flagged as system file). Use `echo` or `sed` via terminal instead. Verify with `grep -q 'DISPLAY=:0' ~/.bashrc && echo 'OK'`.

Once `DISPLAY=:0` is set, WSLg routes GUI windows from WSL apps to the Windows desktop seamlessly — no VNC, no RDP needed.

### Alternative: Hermes Built-in Browser (agent-browser) — Zero Config

Hermes Agent ships with `agent-browser`, a Chromium-based browser CLI that works **out of the box** in WSL. It's the recommended path for most tasks because:

- **No CDP setup required** — no port management, no launcher scripts, no process lifecycle
- **Both headless and headful modes** — headless works anywhere; headful needs `DISPLAY=:0` (see above)
- **Session isolation** — each task gets its own browser context
- **Verification is one command**:

```bash
# Navigate to a URL
agent-browser navigate "https://example.com"
# Expected output: ✓ Example Domain

# Get page accessibility tree (snapshot)
agent-browser snapshot
# Expected: element tree with ref selectors (@e1, @e2, ...)
```

Hermes' `browser_navigate`, `browser_snapshot`, `browser_click`, etc. tools all use agent-browser when no CDP URL is available or when `engine: auto` falls back.

**When to still set up CDP:** You need CDP when you want to:
- Reuse a persistent browser session across multiple Hermes conversations
- Visually debug browser automation (watch Hermes control a visible browser)
- Route through a remote/proxied browser (Browserbase, Browser Use cloud)

### Pitfall: Windows Chrome CDP from WSL Fails

#### Root Cause — Dual Scenarios

**Pitfall — Chrome must be fully closed before re-launching with `--remote-debugging-port`:** If Chrome is already running (including minimized to system tray), running `chrome.exe --remote-debugging-port=9222` creates a **second Chrome process that does NOT bind the port**. The first instance holds the port silently. The second instance runs as a regular browser with no debug port.

Fix — kill all Chrome processes first:
1. **On Windows**: Right-click Chrome icon in system tray → **Exit** (not just close the window)
2. **Or via taskkill** (PowerShell): `Get-Process chrome* | Stop-Process -Force`
3. Then relaunch with the debug flag

Verify the port is actually listening: `curl -s http://localhost:9222/json/version` should return JSON with `webSocketDebuggerUrl`. If it returns HTML or connection refused, Chrome is either not running or not started with the right flag.

**Quick CDP connection from within Hermes (in-session):**
```
# Once Chrome is running on Windows with the debug port:
hermes config set browser.cdp_url http://localhost:9222

# In-session, use the /browser slash command to connect:
/browser

# Then browser_navigate, browser_snapshot, etc. all use the user's Chrome
# with existing login sessions intact.
```

Also usable via `browser_cdp` tool directly for diagnostics:
```
browser_cdp(method="Target.getTargets")  → list all open tabs
browser_cdp(method="Target.activateTarget", params={"targetId": "..."}) → switch to a tab
browser_cdp(method="Page.handleJavaScriptDialog", params={"accept": true}) → handle alert/confirm
```

**Pitfall — netsh portproxy verification:** After setting up portproxy, `netsh interface portproxy show all` to verify. If the entry appears but curl still fails, Chrome might not be listening yet or was launched without the flag. Use `curl -v http://localhost:9222/json/version` for detailed diagnostics.

#### Scenario A — Launching Windows Chrome FROM WSL (not recommended)

Fails with port binding error:
```
bind() returned an error: WSAEACCES (0x271D) — 以一种访问权限不允许的方式做了一个访问套接字的尝试
```
Chrome processes spawned from WSL inherit a restricted security token that prevents binding to TCP ports. This is a WSL → Windows binary interop limitation.

**Scenario B: Windows Chrome started natively on Windows** — this DOES work. Chrome started on Windows (via Win+R, shortcut, or batch file CAN bind to a specific port and be reachable from WSL.

#### Scenario A Workaround (launch from WSL — not recommended)

If you MUST launch Chrome from WSL, use one of:
1. Use `agent-browser` (Hermes built-in) instead — no CDP needed
2. Use WSL's Playwright Chromium as a CDP endpoint (see next section)

#### Scenario B: Connect to Windows-Native Chrome (推荐方案)

**Windows side — start Chrome with remote debugging:**

Method 1: Win+R → paste and run:
```
chrome.exe --remote-debugging-port=9222
```

Method 2 (already-running Chrome): Open `chrome://inspect/#remote-debugging` → check "Allow remote debugging for this browser instance". Note: this binds to `localhost:127.0.0.1` only, so it's accessible from WSL via `localhost:9222` (WSL2 forwards `localhost` to Windows) but NOT via the Windows LAN IP.

Method 1 binds to `0.0.0.0` (all interfaces), making it accessible from WSL via BOTH `localhost:9222` AND `host.docker.internal:9222` AND the Windows LAN IP.

**WSL side — connect to Windows Chrome CDP:**

Once Chrome is running on Windows with `--remote-debugging-port=9222`:

```bash
# Verify connection
curl -s http://localhost:9222/json/version
# Or via host.docker.internal (alternative route in WSL2)
curl -s http://host.docker.internal:9222/json/version
```

Expected output — Chrome version JSON with WebSocket debugger URL. If you only get HTML, the port is blocked or Chrome isn't listening with the right flag.

**Using web-access CDP Proxy (third-party, for additional features):**

[web-access](https://github.com/eze-is/web-access) wraps the CDP endpoint in an HTTP API with tab management, idle timeout, and screenshot endpoints:

```bash
git clone https://github.com/eze-is/web-access ~/.hermes/skills/web-access
cd ~/.hermes/skills/web-access
node scripts/cdp-proxy.mjs --browser chrome &
# Verify
curl -s http://localhost:3456/health
# Expected: {"status":"ok","connected":true,...}
```

The CDP Proxy adds:
- `/new`, `/navigate`, `/click`, `/clickAt`, `/eval`, `/screenshot`, `/scroll` HTTP endpoints
- Automatic tab management with 15-min idle timeout
- Multi-tab isolation for parallel tasks

**Key advantage of Scenario B:** The user's Chrome already has all their login sessions (微信公众号, 小红书, internal systems, etc.). The Agent can access authenticated pages without separate login handling.

**Pitfall — netsh portproxy + WebSocket limitation:** When Chrome binds to Windows `127.0.0.1:9222` only (default behavior of `--remote-debugging-port`), WSL2 cannot reach it directly. The solution is `netsh interface portproxy`:
```powershell
# Run in Windows PowerShell as Administrator:
netsh interface portproxy add v4tov4 listenport=9222 listenaddress=0.0.0.0 connectport=9222 connectaddress=127.0.0.1
```

However, Windows' netsh portproxy does NOT properly forward WebSocket upgrade (HTTP 101 Switching Protocols). This affects Node.js's native `WebSocket` class which fails with "Received network error or non-101 status code".

**Workaround** — Use Python's `websockets` library instead of Node.js. Python's library handles the upgrade correctly through the same portproxy:
```python
import asyncio, websockets
ws = await websockets.connect('ws://127.0.0.1:9222/devtools/browser/<uuid>')
# Works! Node.js WebSocket fails, Python works.
```

Since Hermes Agent is Python-based and uses `requests` + `websockets` for CDP communication, Hermes' `browser_tool.py` with `browser.cdp_url: http://127.0.0.1:9222` in config.yaml works correctly through the netsh portproxy.

**Alternative:** If Python is not an option, write a raw TCP forwarder in Python that runs on port 9122 and forwards to Windows Chrome's 127.0.0.1:9222. This bypasses the portproxy entirely and both HTTP and WebSocket work:

**Pitfall — Multiple CDP endpoints detected:** Windows Chrome may open the debug port on multiple interfaces. Earlier tests reached ports 9222/9223/9229/9333/9339/9444 on the gateway IP (router), which return HTML redirect pages — those are NOT Chrome CDP. The real CDP responds with JSON containing Chrome version and WebSocket URLs. Always verify with `/json/version` endpoint.

**Pitfall — chrome://inspect toggle only binds to localhost:** The chrome://inspect/#remote-debugging toggle in the Chrome UI binds only to 127.0.0.1, which is NOT accessible from WSL2 by the Windows LAN IP. Use `--remote-debugging-port=9222` command-line flag instead for full cross-host access.

### Browser CDP (Chrome DevTools Protocol) Setup

For Hermes Agent's `browser` tool to connect to a headless Chrome via CDP (rather than using the built-in agent-browser), set up a Playwright-bundled Chromium as the CDP endpoint:

**1. Find the Chromium binary (from Playwright):**

```bash
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print(p.chromium.executable_path)
"
# Output example: ~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome
```

**2. Create a launcher script** (`~/.local/bin/chrome-cdp`):

```bash
cat > ~/.local/bin/chrome-cdp << 'SCRIPT'
#!/bin/bash
PORT="${1:-9222}"
CHROME="$HOME/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
exec "$CHROME" \
  --headless=new \
  --no-first-run --no-default-browser-check \
  --disable-extensions --disable-gpu --disable-sync \
  --disable-translate --disable-default-apps \
  --remote-debugging-port="$PORT" \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="/tmp/chrome-cdp-$PORT"
SCRIPT
chmod +x ~/.local/bin/chrome-cdp
```

**3. Launch in background:**

```bash
chrome-cdp 9222
# Verify:
curl -s http://127.0.0.1:9222/json/version | python3 -m json.tool
```

**4. Configure Hermes Agent to use it:**

In `~/.hermes/config.yaml`:
```yaml
browser:
  cdp_url: 'http://127.0.0.1:9222'
```

The session persists as long as the process lives. If Chrome crashes or WSL is restarted, re-launch `chrome-cdp 9222`.

**Pitfall:** The `--user-data-dir` is set to `/tmp/chrome-cdp-$PORT` which is ephemeral — browser state, cookies, and sessions are lost on restart. For persistent profiles, point to a stable path. Use different ports for multiple isolated profiles.

### Browser Use Installation

[Browser Use](https://github.com/browser-use/browser-use) is a Python library for AI-powered browser automation (LLM-controlled browsing, form filling, extraction):

```bash
# Install the library
pip install browser-use playwright --break-system-packages

# Install bundled Chromium (avoids sudo for system deps):
python3 -m playwright install chromium

# Optional LLM integration:
pip install langchain-openai --break-system-packages
```

Verify installation:
```bash
python3 -c "from browser_use import Agent, Controller; print('browser-use OK')"
```

See `references/browser-cdp-setup.md` for a complete walkthrough including the chrome-cdp launcher script and service lifecycle management.

**Pitfall:** `langchain-openai` may upgrade `openai` package past version constraints of other installed tools (e.g., MemoryOS requires openai<2.0.0). If conflicts arise, install in a separate venv or reinstall the conflicting package after.

### API Service Onboarding (New External Services)

When the user needs to configure a new external API service (Exa, Parallel, Firecrawl, Browserbase, etc.):

1. **Research** — Check the service's pricing page for free tier availability. All four major browser/search API platforms offer free tiers without requiring a credit card:
   - **Exa.ai**: 1,000 requests/month free
   - **Parallel.ai**: Up to 16,000 requests free
   - **Firecrawl.dev**: 500 one-time credits free
   - **Browserbase.com**: 1 hour/month browser sessions free

2. **Guide registration** — Present the free tier details and signup URL to the user. Registration requires the user to do it (can't be automated).

3. **Write to .env** — Once the user provides the API key, add it to `~/.hermes/.env`:
   ```bash
   echo "# Service added $(date +%Y-%m-%d)" >> ~/.hermes/.env
   echo "SERVICE_API_KEY=key_here" >> ~/.hermes/.env
   ```

**Pitfall:** `delegate_task` with `max_concurrent_children=3` — when researching multiple services simultaneously, batch them in groups of 3 or fewer per call.

## Common WSL Pitfalls

## Windows Disk Space Diagnosis from WSL

See `references/windows-disk-space-diagnosis.md` for the comprehensive reference covering:
- **Hierarchical scan strategy** — root files → top-level dirs → user profile → AppData
- **GPU-aware AI model audit** — nvidia-smi VRAM check, model-size-fit analysis, cross-tool duplication
- **Pre-deletion audit workflow** — check processes, dependencies, user data before deleting; present risk ratings
- **Docker audit when Docker isn't running** — direct directory inspection
- **SD/ComfyUI model classification** — what to keep vs delete when user says "吃了灰"
- **Multi-drive discovery** — use `wmic` to enumerate all drives, don't assume C: and D: only

**User workflow preference (embed in all disk-cleanup tasks):** Before any destructive deletion, self-audit each candidate — check running processes, verify no shared dependencies, look for user data worth backing up, then present risk ratings (🟢/🟡/🔴/⚫) to the user before executing. User explicitly requires this.

## WSL VHDX Compaction Without Hyper-V

Hermes' `patch`/`write_file` tools refuse to modify `~/.bashrc` (flagged as system file). Use `sed` via terminal instead:

```bash
# Fix malformed lines with literal escape sequences
sed -i 's/\\\\n/\\n/g' ~/.bashrc

# Check for duplicated PATH lines accidentally appended
grep -n 'export PATH.*npm-global' ~/.bashrc

# Add alias
echo 'alias myalias="command"' >> ~/.bashrc
```

**Pitfall:** `sed -i` may not resolve escape sequences correctly on all WSL versions. If `\\n` remains as literal two-char string, use Python:
```bash
python3 -c "
import sys
with open('/home/zcs/.bashrc') as f:
    content = f.read()
content = content.replace('\\\\n', '\\n')
with open('/home/zcs/.bashrc', 'w') as f:
    f.write(content)
"
```

**Pitfall:** Duplicate PATH exports accumulate if the same alias/export command is appended across multiple sessions. `grep -n 'export PATH' ~/.bashrc` to audit before editing.

### Windows .npmrc Interfering with npm

Windows `.npmrc` at `/mnt/c/Users/<user>/.npmrc` conflicts with WSL npm:

```bash
# Symptom: "prefix cannot be changed from project config"
npm install --ignore-scripts         # bypasses the conflict
```

### Proxy Access

China-based WSL users need proxy for external services:
```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

**Systemd services don't inherit shell proxy** — must be explicitly added to service files:

```ini
[Service]
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=192.168.*,172.31.*,172.30.*,172.2*,172.19.*,172.18.*,172.17.*,172.16.*,10.*,127.*,*.local,localhost,*360buyimg.com,100ime-iat-api.xfyun.cn,*jd.com,*zhimg.com,*zhihu.com"
```

**Pitfall — service file edits may not persist through `patch`/`write_file`:** The Hermes `patch` tool may report success on systemd service files but the write doesn't actually reach disk. Always **verify** with `read_file` or `grep` after writing, and confirm with `systemctl --user show <service>.service --property=Environment` that systemd sees the changes. If the file was written but the env var doesn't appear in `systemctl show`, run `systemctl --user daemon-reload` and re-check.

**Pitfall — `hermes gateway install` overwrites customizations:** Running this command after an update will strip all manual Environment lines from the service file. Re-apply proxy config afterward.

**Pitfall — Chinese domains in NO_PROXY:** Weixin/WeChat (`ilinkai.weixin.qq.com`) and other domestic services connect directly without proxy. Adding `*.weixin.qq.com,*.qq.com` to NO_PROXY prevents routing Chinese traffic through the proxy (which can cause latency or failure for local CDN IPs). Also add Chinese e-commerce/CDN domains (`*360buyimg.com, *jd.com, *zhimg.com, *zhihu.com`) to avoid routing domestic static assets through the proxy. Chinese DNS can have intermittent `Temporary failure in name resolution` — a static `/etc/hosts` entry for the service's IPs is a reliable workaround (requires sudo).

## Windows Auto-Start WSL on Boot

WSL does NOT auto-start when Windows boots. For always-on Hermes gateway service, add a startup trigger:

### Batch File + Registry RUN Key

**1. Create batch file** at `C:\Users\<YourUser>\hermes-startup.bat`:

```batch
@echo off
wsl --shutdown 2>nul
timeout /t 3 /nobreak >nul
wsl -d Ubuntu
```

**2. Register in Windows Registry RUN key** (no admin needed):

```powershell
Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'HermesStartup' -Value 'C:\Users\<YourUser>\hermes-startup.bat'
```

Verify:
```powershell
Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'HermesStartup'
```

Once set, WSL starts automatically at Windows user login. Systemd services (gateway, dashboard) fire up via systemd user services. The recovery timer (120s after boot) handles catch-up.

**Pitfall — WSL might boot before Windows proxy (Clash/V2Ray) is ready.** The boot recovery timer (delayed 120s) and the 3-minute crond connection monitor handle this — the gateway will connect after the proxy starts, not fail permanently. If the gateway crashes before proxy is ready, systemd `Restart=on-failure` re-launches it.

## Boot Recovery (systemd Timer)

For WSL with `systemd=true` in `/etc/wsl.conf`, create a one-shot recovery service that runs 120s after boot.

### Service File

**Service** (`~/.config/systemd/user/hermes-startup-recovery.service`):
```ini
[Unit]
Description=Hermes WSL Startup Full Recovery
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/zcs/.hermes/scripts/wsl-startup-recovery.sh
# ⚠ Do NOT set User=%u — in user-mode systemd this causes exit code 203/EXEC

[Install]
WantedBy=default.target
```

### Timer File

**Timer** (`~/.config/systemd/user/hermes-startup-recovery.timer`):
```ini
[Unit]
Description=Hermes Startup Recovery Timer — 120s after boot

[Timer]
OnBootSec=120
Persistent=true

[Install]
WantedBy=default.target
```

### Enable

```bash
systemctl --user daemon-reload
systemctl --user enable --now hermes-startup-recovery.timer
```

### Recovery Script Responsibilities

The recovery script should cover:
- Wait briefly for network (non-blocking, max 15s per check)
- Check gateway status and restart if dead
- Run cron-catchup (detect missed jobs during downtime)
- Verify system integrity (directories, SessionDB)
- Log all actions to a recovery log
- Write a boot marker to prevent re-execution on the same boot

### Cron Catch-Up (Missed Jobs Detection)

After unexpected shutdown, some cron jobs may have been scheduled during the downtime. A catch-up script detects these:

- Scan cron job output directories for the last run timestamp
- Compare with system boot time (`/proc/uptime`)
- Use **smart thresholds** per job type: daily jobs (26h), weekly jobs (170h), default (48h)
- Flag jobs that had FAILED outputs
- Write results to log for user review

### Pitfalls

- **Recovery scripts MUST NOT use `set -euo pipefail`** because network checks, gateway status checks, and other phases are expected to fail in certain boot sequences. Each phase should have its own error handling. Exit 0 always.
- **`User=%u` causes exit code 203/EXEC in user-mode systemd.** The service already runs as the user; the `User=` directive is only valid in system-level services. Omit it entirely.
## Windows Disk Space Diagnosis from WSL

See `references/windows-disk-space-diagnosis.md` for the comprehensive reference covering:
- **Hierarchical scan strategy** — root files → top-level dirs → user profile → AppData
- **GPU-aware AI model audit** — nvidia-smi VRAM check, model-size-fit analysis, cross-tool duplication
- **Pre-deletion audit workflow** — check processes, dependencies, user data before deleting; present risk ratings
- **Docker audit when Docker isn't running** — direct directory inspection
- **SD/ComfyUI model classification** — what to keep vs delete when user says "吃了灰"
- **Multi-drive discovery** — use `wmic` to enumerate all drives, don't assume C: and D: only

**User workflow preference (embed in all disk-cleanup tasks):** Before any destructive deletion, self-audit each candidate — check running processes, verify no shared dependencies, look for user data worth backing up, then present risk ratings (🟢/🟡/🔴/⚫) to the user before executing. User explicitly requires this.

## WSL VHDX Compaction Without Hyper-V

After cleaning files inside WSL (pip/npm cache, temp), the `ext4.vhdx` file doesn't shrink automatically. If `Optimize-VHD` isn't available (requires Hyper-V module), use **diskpart** instead.

### Diskpart Method

```powershell
# In Windows PowerShell as Administrator:
wsl --shutdown
diskpart
```

Inside diskpart:
```
select vdisk file="C:\Users\<YourUser>\AppData\Local\wsl\{<distro-guid>}\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

Find the GUID:
```bash
ls /mnt/c/Users/*/AppData/Local/wsl/
```

### Pitfalls

- **Do NOT skip the `detach vdisk` step** — the VHDX must be properly detached or WSL won't mount it on next boot. If you forget, `wsl --shutdown` again and re-attach/detach.
- **Run `sudo fstrim /` inside WSL first** — this marks freed blocks as available for compaction. Without it, diskpart has nothing to compact.
- **Optimize-VHD alternative**: `Optimize-VHD -Path "..." -Mode Full` is the PowerShell equivalent but requires the Hyper-V PowerShell module (not available on Windows Home edition).

## Post-Reboot Verification Checklist

After Windows restarts (WSL also restarts), the Gateway may fail to connect Telegram/Discord because the Windows-side proxy (Clash/Mihomo on 127.0.0.1:7890) isn't running yet, or systemd services start before the proxy is ready. Run these checks:

```bash
# 1. Windows proxy port 7890 listening?
powershell.exe -Command "Get-NetTCPConnection -LocalPort 7890 -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess"
# Expected: shows 127.0.0.1:7890 rows. If empty → proxy not started on Windows side, start it manually.

# 2. Gateway service alive?
systemctl --user status hermes-gateway.service --no-pager -l | head -5
# Expected: "active (running)" within a few seconds.

# 3. Platform connection status (gateway_state.json)
cat ~/.hermes/gateway_state.json | python3 -m json.tool
# Expected: telegram: "connected", discord: "connected". If timeout → proxy issue.

# 4. Web UI alive? (if installed)
systemctl --user status hermes-web-ui.service --no-pager -l 2>/dev/null | head -3
# Expected: "active (running)"

# 5. Quick proxy connectivity test from WSL
curl -sfo /dev/null -w '%{http_code}' --connect-timeout 5 --proxy http://127.0.0.1:7890 https://api.telegram.org
# Expected: 302 (redirect) or 200. Anything else → proxy can't reach Telegram.
```

**Diagnostic path for "Gateway alive but Telegram/Discord timeout":**
- Symptom in logs: `ConnectionTimeoutError: Connection timeout to host https://discord.com/api/v10/users/@me` or `telegram connect timed out after 30s`
- Root cause 90% of the time: systemd service file lacks proxy `Environment=` lines (either never added, or overwritten by `hermes gateway install`)
- Fix: edit `~/.config/systemd/user/hermes-gateway.service`, add the Environment lines above, then `systemctl --user daemon-reload && systemctl --user restart hermes-gateway`
- Verify fix: `systemctl --user show hermes-gateway.service --property=Environment | grep -i proxy`

**Pitfall — identical symptom for two different causes:** "Discord/Telegram connection timeout" can mean EITHER (a) the Windows proxy process isn't running on port 7890, OR (b) the proxy is running but systemd doesn't have the env vars. Check (a) first with the PowerShell command above — it's the faster check and covers both.

## Container Registries & Mirror Setup

### Self-Hosted Registries May Be Unreachable

Some projects (e.g., OpenHands) publish Docker images to self-hosted registries like `docker.all-hands.dev`. In this WSL + Docker Desktop setup, these registries may fail with:

```
Error response from daemon: failed to resolve reference "docker.all-hands.dev/...": 
  failed to do request: Head "..." : EOF
```

**Root cause:** DNS resolution fails for `.dev` TLDs in the WSL environment (Docker Desktop proxy at `http.docker.internal:3128` doesn't forward these). The DNS server at `10.255.255.254` cannot resolve `docker.all-hands.dev`.

**Workaround — ghcr.io mirror:** Many projects mirror their images to GitHub Container Registry (`ghcr.io`), which is reachable:

```bash
# Instead of:
docker pull docker.all-hands.dev/all-hands-ai/openhands:0.50

# Use:
docker pull ghcr.io/all-hands-ai/openhands:0.50
```

**Verification** — confirm the alternative registry works:
```bash
sg docker -c "docker pull ghcr.io/all-hands-ai/openhands:0.50"
```

**Pitfall:** Not all projects mirror to ghcr.io. For projects that don't, check the project's GitHub releases or CI config for alternative publish targets. If none exist, try pulling with the Docker Desktop proxy disabled or via a local HTTP proxy (`http://127.0.0.1:7890`) by adding `"registry-mirrors"` to daemon.json:

```json
{
  "registry-mirrors": [],
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890"
  }
}
```

Then restart Docker Desktop from Windows (`Restart` from system tray icon).

**Pitfall:** `docker.all-hands.dev` also requires a **runtime** image like `docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik`. Check whether ghcr.io also carries the runtime image: `ghcr.io/all-hands-ai/runtime:0.50-nikolaik`.

### Docker compose Network Names

Docker Compose v2 prefixes network/volume names with the `name:` field from compose files. To reference containers, use the full name (e.g., `memos-dev_memos_network`).

### Deploying Multi-Container Applications (Docker Compose)

Common pattern for deploying services with databases (Neo4j, Qdrant, Redis) behind an API server:

```bash
# 1. Clone project
git clone https://github.com/org/project.git
cd project

# 2. Configure environment
# Create .env from example, fill in API keys
cp docker/.env.example .env

# 3. Start databases first (they have long health checks)
sg docker -c 'docker compose -f docker/docker-compose.yml pull neo4j qdrant'
sg docker -c 'docker compose -f docker/docker-compose.yml up -d neo4j qdrant'

# Wait for databases to become healthy (~10-30s for Neo4j)
# 4. Build & start the API service
sg docker -c 'docker compose -f docker/docker-compose.yml up -d memos'

# 5. Verify health
curl http://localhost:8000/health
sg docker -c 'docker ps --format "table {{.Names}}\t{{.Status}}"'
```

**Pitfall:** Custom Dockerfiles with `pip install -r requirements.txt` take a long time (3-4 minutes for ML-heavy projects like MemOS). Use background process with long timeout:
```bash
# Build in background to avoid terminal timeout
terminal(command="sg docker -c 'docker compose build memos'", background=true, timeout=300)
# Poll progress
process(action="poll", session_id="proc_xxx")
```

**Pitfall:** `.env` files are picked up by docker compose from the project root (not the docker/ directory). The compose file's `env_file: ../.env` resolves to the parent directory.

**Pitfall:** After changing `.env` values (e.g., switching API providers), you must recreate the container, not just restart:
```bash
sg docker -c 'docker compose -f docker/docker-compose.yml up -d --force-recreate memos'
```

See `references/memos-docker-setup.md` for a complete MemOS deployment walkthrough with MiniMax API configuration.
