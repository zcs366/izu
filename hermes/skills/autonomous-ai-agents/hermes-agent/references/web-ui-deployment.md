# Web UI Deployment & Auto-Recovery

Covers `hermes-web-ui` (v0.5.11+) — companion web dashboard for Hermes Agent. Provides a browser-based chat UI at port 8648.

## Architecture

```
Browser → http://localhost:8648 → hermes-web-ui (Node) → Hermes Gateway API (127.0.0.1:8642)
```

## Systemd Service

### Correct Service File

Uses the direct server entry point, NOT the `start` subcommand:

```ini
[Unit]
Description=Hermes Agent Web UI Dashboard
After=network-online.target hermes-gateway.service
Wants=network-online.target hermes-gateway.service
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/path/to/node /path/to/hermes-web-ui/dist/server/index.js
Environment="NODE_ENV=production"
Environment="PORT=8648"
Environment="PATH=/home/$USER/.hermes/node/bin:/home/$USER/.local/bin:..."
Environment="HERMES_HOME=/home/$USER/.hermes"
# If behind proxy (China users):
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,::1,*.weixin.qq.com,*.qq.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
Restart=always
RestartSec=10
RestartMaxDelaySec=60
RestartSteps=3
KillMode=process
TimeoutStopSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**Key differences from the `start` subcommand approach:**
- Direct `ExecStart` to `dist/server/index.js` — systemd can track the child process
- `KillMode=process` — cleanly kills the Node process
- `After=hermes-gateway.service` — web UI depends on gateway being up

### Finding the Correct Paths

```bash
which node
# typically: /home/$USER/.local/bin/node or /home/$USER/.nvm/versions/...
find / -path "*/hermes-web-ui/dist/server/index.js" 2>/dev/null
```

### Enable & Verify

```bash
systemctl --user daemon-reload
systemctl --user enable --now hermes-web-ui

# Verify
systemctl --user status hermes-web-ui
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8648
# Should return 200
```

## ⚠️ Critical: Shell Wrapper Pitfall

The `.bashrc` shell wrapper that auto-starts the web UI must use `systemctl`, NOT `hermes-web-ui start`:

```bash
# ❌ WRONG — creates duplicate processes that conflict with systemd:
hermes() {
    hermes-web-ui status &>/dev/null || {
        hermes-web-ui start &>/dev/null &
        echo " ⚡ hermes-web-ui started (port 8648)" >&2
    }
    command hermes "$@"
}

# ✅ CORRECT — uses systemd to manage lifecycle:
hermes() {
    if ! systemctl --user is-active --quiet hermes-web-ui 2>/dev/null; then
        systemctl --user start hermes-web-ui 2>/dev/null
        echo " ⚡ hermes-web-ui started via systemd (port 8648)" >&2
    fi
    command hermes "$@"
}
```

**Why this matters:** `hermes-web-ui start` uses `spawn()` with `detached: true` — it forks to background and writes its own PID file (`~/.hermes-web-ui/server.pid`). If systemd is **also** running the web UI, you get two Node processes competing for port 8648, causing HTTP 502 or process thrashing.

## Boot Recovery

The web UI recovery is wired into the same systemd timer as the gateway recovery, ensuring sequential execution (gateway → web UI):

### Service: `~/.config/systemd/user/hermes-gateway-recovery.service`

```ini
[Unit]
Description=Hermes Gateway & Web UI Boot Recovery
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/zcs/.hermes/scripts/gateway-boot-recovery.sh
ExecStart=/home/zcs/.hermes/scripts/web-ui-boot-recovery.sh
```

### Timer: `~/.config/systemd/user/hermes-gateway-recovery.timer`

Runs 120 seconds after boot, giving the proxy server and gateway time to start.

### Script: `~/.hermes/scripts/web-ui-boot-recovery.sh`

What it does:
1. Waits for network (up to 15s)
2. Checks systemd service status
3. Tests HTTP 200 response from port 8648
4. Three attempts: restart → wait 15s → retry
5. Emergency mode: restart every 30s, up to 10 rounds
6. Writes state file by `BOOT_ID` for idempotency

Key detection:
```bash
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://127.0.0.1:8648)
if [ "$HTTP_CODE" != "000" ]; then
    echo "✅ Web UI responsive (HTTP $HTTP_CODE)"
fi
```

Failed response codes that trigger restart: `000` (no response), `502`, `503`.

## Continuous Monitoring

### Script: `~/.hermes/scripts/web-ui-connection-monitor.sh`

Runs every 5 minutes via crontab:

```
*/5 * * * * /home/zcs/.hermes/scripts/web-ui-connection-monitor.sh >/dev/null 2>&1
```

Detection logic:
- Systemd service not active → `systemctl --user start`
- HTTP 000/502/503 → `systemctl --user restart`
- Lock file prevents concurrent runs (10 min stale timeout)

## Verification Checklist

```bash
# Service running?
systemctl --user is-active hermes-web-ui

# HTTP response?
curl -s http://127.0.0.1:8648 | head -3

# Boot timer active?
systemctl --user is-active hermes-gateway-recovery.timer

# Monitoring cron?
crontab -l | grep web-ui

# Only one process?
ps aux | grep "hermes-web" | grep -v grep
# Should show exactly 1 process

# No stale duplicates?
ls -la ~/.hermes-web-ui/server.pid 2>/dev/null
# Should exist (written by systemd-managed process)
```
