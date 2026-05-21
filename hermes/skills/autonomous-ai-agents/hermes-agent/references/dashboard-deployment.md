# Hermes Dashboard Deployment & Auto-Recovery

Covers `hermes dashboard` — the built-in web UI for Hermes Agent (port 9119). Manages config, API keys, sessions, and optionally exposes the embedded TUI Chat tab.

## Architecture

```
Browser → http://localhost:9119 → hermes dashboard (Python/FastAPI) → Hermes Gateway API
```

## CLI Reference

```bash
hermes dashboard --help

# Start
hermes dashboard --port 9119 --no-open        # default port 9119
hermes dashboard --port 9119 --tui             # enable embedded chat tab
hermes dashboard --port 9119 --no-open --tui

# Stop all running instances
hermes dashboard --stop

# List running instances
hermes dashboard --status
```

Options:
| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 9119 | HTTP port |
| `--host` | 127.0.0.1 | Bind address |
| `--no-open` | — | Don't open browser automatically |
| `--insecure` | — | Allow non-localhost binding (⚠ exposes API keys) |
| `--tui` | — | Expose embedded TUI via PTY/WebSocket (or set `HERMES_DASHBOARD_TUI=1`) |
| `--stop` | — | Stop all dashboard processes and exit |
| `--status` | — | List running dashboard processes and exit |

## Systemd Service

### Service File

```ini
[Unit]
Description=Hermes Agent Dashboard — Built-in Web UI (port 9119)
After=network-online.target hermes-gateway.service
Wants=network-online.target hermes-gateway.service
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/home/$USER/.hermes/hermes-agent/venv/bin/python /home/$USER/.local/bin/hermes dashboard --port 9119 --no-open
WorkingDirectory=/home/$USER/.hermes/hermes-agent
Environment="PATH=/home/$USER/.hermes/hermes-agent/venv/bin:/home/$USER/.hermes/node/bin:/home/$USER/.local/bin:..."
Environment="VIRTUAL_ENV=/home/$USER/.hermes/hermes-agent/venv"
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

**Key points:**
- `After=hermes-gateway.service` — dashboard depends on gateway being available
- Uses `--no-open` flag — prevents browser auto-open (which fails headless)
- The Python binary is from the hermes-agent venv

### Enable & Verify

```bash
systemctl --user daemon-reload
systemctl --user enable --now hermes-dashboard

# Verify
systemctl --user status hermes-dashboard
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9119
# Should return 200
```

## Boot Recovery

The dashboard recovery is wired into the same unified timer as gateway and web-ui:

### Service: `~/.config/systemd/user/hermes-gateway-recovery.service`

```ini
[Unit]
Description=Hermes Gateway & Web UI & Dashboard Boot Recovery
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/zcs/.hermes/scripts/gateway-boot-recovery.sh
ExecStart=/home/zcs/.hermes/scripts/web-ui-boot-recovery.sh
ExecStart=/home/zcs/.hermes/scripts/dashboard-boot-recovery.sh
```

Execution order: gateway → web-ui → dashboard (sequential).

### Script: `~/.hermes/scripts/dashboard-boot-recovery.sh`

What it does:
1. Waits for network (up to 15s)
2. Checks systemd service status
3. Tests HTTP 200 response from port 9119
4. Three attempts: restart → wait 15s → retry
5. Before each restart: `hermes dashboard --stop` to clean stale PID files
6. Emergency mode: restart every 30s, up to 10 rounds
7. Writes state file by `BOOT_ID` for idempotency

### Timer: `~/.config/systemd/user/hermes-gateway-recovery.timer`

Shared timer — runs 120 seconds after boot:
```ini
[Timer]
OnBootSec=120
Persistent=true
OnFailure=hermes-gateway-recovery.service
```

## Continuous Monitoring

### Script: `~/.hermes/scripts/dashboard-connection-monitor.sh`

Runs every 5 minutes via crontab:
```
*/5 * * * * /home/zcs/.hermes/scripts/dashboard-connection-monitor.sh >/dev/null 2>&1
```

Detection logic:
- Systemd service not active → `hermes dashboard --stop` then `systemctl --user start`
- HTTP not 200 → `hermes dashboard --stop` then `systemctl --user restart`
- Lock file prevents concurrent runs (10 min stale timeout)

## ⚠️ Known Issues

### Duplicate Processes

`hermes dashboard` manages its own PID tracking via `hermes dashboard --stop` and `hermes dashboard --status`. If started manually AND via systemd, you can get two processes. Always use `hermes dashboard --stop` before systemd restart to clean stale state.

### Auth Token

The dashboard logs an auth token on startup:
```
Auth enabled — token: 30850f53082ff5170e67d6f30eb...
```
This token is required for API access. Find it in:
```bash
journalctl --user -u hermes-dashboard | grep "Auth enabled"
```

## Verification Checklist

```bash
# Service running?
systemctl --user is-active hermes-dashboard

# HTTP response?
curl -s http://127.0.0.1:9119 | head -3

# Boot timer active?
systemctl --user is-active hermes-gateway-recovery.timer

# Monitoring cron?
crontab -l | grep dashboard

# Only one process?
hermes dashboard --status
```
