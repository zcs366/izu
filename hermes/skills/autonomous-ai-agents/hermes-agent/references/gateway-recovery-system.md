# Gateway Recovery System — Three-Layer Auto-Healing

A battle-tested pattern for keeping Hermes Gateway + Web UI + Dashboard online across boots, network blips, and proxy failures. Designed for China-based WSL2 deployments where proxy availability lags behind system boot.

Three services are orchestrated in sequence via a single systemd timer:

```
① gateway-boot-recovery.sh    →  ensures Telegram/Discord/WeChat connected
② web-ui-boot-recovery.sh     →  ensures hermes-web-ui (port 8648) online
③ dashboard-boot-recovery.sh  →  ensures hermes dashboard (port 9119) online
```

## Architecture

```
Layer 1: BOOT RECOVERY          Layer 2: CRON MONITOR       Layer 3: GATEWAY SELF-HEAL
┌──────────────────────────┐   ┌────────────────────────┐   ┌──────────────────────────┐
│ systemd timer            │   │ crontab */3 * * * *    │   │ Gateway built-in reconn. │
│ (120s after boot)        │   │   + */5 * * * *        │   │ (up to 20 retries)       │
│                          │   │   webui + dash monitor │   │                          │
│                          │   │                        │   │                          │
│ → wait for network       │   │ → check "✓ connected"  │   │ → exponential backoff    │
│ → wait for proxy (7890)  │   │ → detect "timed out"   │   │ → auto-reconnect loop    │
│ → 3x gateway restart     │   │ → auto-restart gateway │   │ → 30s→60s→120s delay     │
│ → verify all platforms   │   │ → no-op if healthy     │   │                          │
│ → emergency mode (10x)   │   │                        │   │                          │
└──────────────────────────┘   └────────────────────────┘   └──────────────────────────┘
                                                  systemd Restart=always (60s)
```

## Layer 1: Boot Recovery

### Script: `~/.hermes/scripts/gateway-boot-recovery.sh`

What it does:
1. Records `BOOT_ID` from `/proc/sys/kernel/random/boot_id` — idempotent per boot
2. Waits up to 30s for network (`ping 114.114.114.114`)
3. Waits up to 15s for proxy (`curl -x http://127.0.0.1:7890 http://www.gstatic.com`)
4. Three rounds of: restart gateway → wait 30s → check logs for `✓ connected`
5. If any platform still down → emergency mode: restart every 60s, up to 10 rounds
6. Writes state file to prevent re-execution on the same boot

Key detection logic:
```bash
WEIXIN_OK=$(grep "✓ weixin connected" ~/.hermes/logs/gateway.log | tail -1)
TELEGRAM_OK=$(grep "✓ telegram connected" ~/.hermes/logs/gateway.log | tail -1)
```

### systemd Service: `~/.config/systemd/user/hermes-gateway-recovery.service`

Unified service that orchestrates gateway, web-ui, and dashboard recovery sequentially:

```ini
[Unit]
Description=Hermes Gateway & Web UI & Dashboard Boot Recovery
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/zcs/.hermes/scripts/wsl-startup-recovery.sh
# Do NOT add User=%u — in user-mode systemd this causes exit code 203/EXEC
# (The service already runs as the current user; User= is for system-level services.)
Environment="PATH=/home/zcs/.hermes/hermes-agent/venv/bin:/home/zcs/.hermes/node/bin:/home/zcs/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="HOME=/home/zcs"

[Install]
WantedBy=default.target
```

Execution order: gateway → web-ui → dashboard.

### systemd Timer: `~/.config/systemd/user/hermes-gateway-recovery.timer`

```ini
[Unit]
Description=Hermes Gateway Boot Recovery Timer
After=network-online.target

[Timer]
OnBootSec=120          # 2 minutes after boot — gives proxy time to start
Persistent=true        # catch up after shutdown
OnFailure=hermes-gateway-recovery.service
```

Enable:
```bash
systemctl --user daemon-reload
systemctl --user enable --now hermes-gateway-recovery.timer
```

## Layer 2: Continuous Monitor

### Script: `~/.hermes/scripts/gateway-connection-monitor.sh`

Runs every 3 minutes via crontab. Checks:

**Direct log check** — looks for `✓ connected` status lines in recent journalctl:
```bash
journalctl --user -u hermes-gateway --since "5 min ago" | grep -E "✓.*connected"
```

**Failure detection** — catches explicit errors:
```bash
journalctl ... | grep -E "✗.*error|Disconnected|timed out"
```

**Stuck-in-timeout detection** — catches the case where gateway is running but can't connect (safe restart trigger):
```bash
TIMEOUT_COUNT=$(tail -100 $GW_LOG | grep -c "timed out")
RECONNECTING=$(tail -100 $GW_LOG | grep -c "Reconnect.*error")
CONNECTED_COUNT=$(tail -100 $GW_LOG | grep -c "✓.*connected")
if [ "$TIMEOUT_COUNT" -gt 5 ] && [ "$RECONNECTING" -gt 3 ] && [ "$CONNECTED_COUNT" -eq 0 ]; then
    NEED_RESTART=true
fi
```

**Lock file** prevents concurrent execution:
```bash
LOCKFILE="/tmp/hermes-monitor.lock"
if ! mkdir "$LOCKFILE" 2>/dev/null; then
    # Check if lock is stale (>10 min)
    ...
fi
```

**Exit codes** for systemd integration: `exit 0` = healthy, `exit 1` = failure after retries.

### Crontab Entry

```
*/3 * * * * /home/zcs/.hermes/scripts/gateway-connection-monitor.sh >/dev/null 2>&1
```

## Layer 3: Gateway Built-in Self-Healing

Hermes Gateway already has:
- Built-in reconnect loop (up to 20 attempts, logged as "Reconnecting platform (attempt N/20)")
- `Restart=always` in systemd service (60s restart delay, max 300s with 5-step escalation)
- `RestartMaxDelaySec=300` prevents restart-storm

## Cron Catch-Up After Power Loss

When unexpected shutdown occurs (power loss, child hitting the power button), cron jobs scheduled during the downtime never fired. A catch-up script on boot detects and reports missed jobs.

### Detection Logic

The script (`cron-catchup.sh`) operates at the filesystem level — no Gateway/CLI dependency:

1. Calculate boot time from `/proc/uptime`
2. Scan `~/.hermes/cron/output/<job-id>/` for the most recent output file
3. Parse the filename timestamp (format: `YYYY-MM-DD_HH-MM-SS.md`)
4. Compare with boot time — if last run was before boot AND the expected interval has elapsed, flag as missed

### Smart Thresholds by Job Type

Not all jobs run at the same frequency. Use job-ID-based thresholds:

| Job Type | Threshold | Examples |
|----------|-----------|---------|
| Daily (论文日报, 每日扫描, 研究管道) | 26 hours | `65eba5595103`, `c5c558c8f9a4`, `6cf70b7b2ddb` |
| Weekly (周报, 提醒, 群报) | 170 hours (7 days) | `bf7309fa7a51` through all `* * * * N` jobs |
| Default (other) | 48 hours | Jobs without known cadence |

### Filesystem Implementation (No Gateway Dependency)

```bash
for JOB_DIR in ~/.hermes/cron/output/*/; do
    JOB_ID=$(basename "$JOB_DIR")
    LAST_FILE=$(ls -t "$JOB_DIR" 2>/dev/null | head -1)
    # Parse timestamp from filename: 2026-05-15_08-34-28.md
    # Compare epoch with boot_epoch
    # Flag if overdue beyond threshold
done
```

### Job with FAILED Output

If the output file contains `FAILED`, flag immediately regardless of threshold — the last attempt failed and may need retry.

## Pitfalls

### User=%u Causes Exit Code 203/EXEC in User-Mode systemd

**Symptom:** `systemctl --user status` shows `code=exited, status=203/EXEC` with no other error.

**Root cause:** The `User=%u` directive is only valid in **system-level** services (`systemctl start`, not `systemctl --user start`). In user-mode systemd, the service already runs as the logged-in user. Adding `User=` causes systemd to look for a full user session context (PAM, logind) that user-mode oneshots don't have.

**Fix:** Simply remove the `User=` line from the `[Service]` section. The service inherits the caller's user identity automatically.

### Recovery Scripts Must Not Use `set -euo pipefail`

**Symptom:** The recovery script exits early without completing all phases, because a network check, gateway status check, or directory scan returned a non-zero exit code.

**Root cause:** `set -e` causes the script to abort on ANY command failure. In boot recovery scenarios, many checks are expected to fail temporarily (network not ready, proxy not started, gateway still starting). These should be handled per-phase, not globally.

**Fix:** Remove `set -euo pipefail` from the shebang/header. Use per-command error handling:
```bash
# ❌ Bad: exits early if ping fails
set -euo pipefail
ping -c 1 114.114.114.114 || echo "Network not ready, continuing..."

# ✅ Good: each phase handles its own errors
for i in $(seq 1 15); do
    ping -c 1 -W 1 114.114.114.114 >/dev/null 2>&1 && NET_OK=1 && break
    sleep 1
done
[ "$NET_OK" = "1" ] || echo "网络未就绪（继续执行）"
```

### Boot Marker Prevents Re-Execution

The same recovery script must not run twice on the same boot (e.g., if the timer fires again). Use a boot-ID marker:

```bash
BOOT_ID=$(cat /proc/sys/kernel/random/boot_id)
MARKER_FILE="$HOME/.hermes/.startup_recovery_done"
if [ -f "$MARKER_FILE" ]; then
    PREV_BOOT=$(cat "$MARKER_FILE")
    [ "$PREV_BOOT" = "$BOOT_ID" ] && echo "Already ran this boot" && exit 0
fi
# ...run recovery...
echo "$BOOT_ID" > "$MARKER_FILE"
```

### Windows Auto-Start Integration

The recovery system assumes WSL is already running. On Windows boot, WSL does NOT auto-start. You must add a startup trigger:

1. Create `C:\Users\<User>\hermes-startup.bat` with `wsl --shutdown && timeout /t 3 && wsl -d Ubuntu`
2. Add to Registry: `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run` as `HermesStartup`

The recovery timer (120s after WSL boot) handles the rest — the gateway connects, platforms come online, cron catch-up detects missed jobs.

## Proxy Dependency Checklist

All three layers depend on the service file having correct proxy env vars. After `hermes gateway install` (which overwrites the service file), re-apply:

```
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,::1,*.weixin.qq.com,*.qq.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
Environment="TELEGRAM_PROXY=http://127.0.0.1:7890"
```

Verify with:
```bash
systemctl --user show hermes-gateway.service --property=Environment | grep -c "TELEGRAM_PROXY"
```

## Verification

```bash
# All platforms connected?
tail -5 ~/.hermes/logs/gateway.log | grep "✓.*connected"

# All web UIs responsive?
curl -s -o /dev/null -w "web-ui(8648): %{http_code}\n" http://127.0.0.1:8648
curl -s -o /dev/null -w "dashboard(9119): %{http_code}\n" http://127.0.0.1:9119

# Boot timer active?
systemctl --user is-active hermes-gateway-recovery.timer

# All recovery scripts exist?
ls -la ~/.hermes/scripts/*recovery*.sh

# All monitoring cron entries?
crontab -l | grep monitor

# Proxy in gateway service?
systemctl --user show hermes-gateway.service --property=Environment | grep -oP '(http_proxy|TELEGRAM_PROXY)'
```
