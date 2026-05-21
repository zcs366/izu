# WeChat iLink DNS Failure Diagnosis

## Symptom

- WeChat bot shows "无法连接" on the user's phone
- Gateway log shows: `iLink sendmessage rate limited` followed by disconnect
- Or: `Cannot connect to host ilinkai.weixin.qq.com:443 ssl:default [Temporary failure in name resolution]`

## Root Causes

### 1. DNS resolution failure (WSL-specific)

WSL auto-generates `/etc/resolv.conf` with `nameserver 10.255.255.254`, which forwards to Windows DNS. Windows DNS can intermittently fail to resolve `ilinkai.weixin.qq.com` (a Chinese CDN domain).

**Evidence in logs:**
```
[Temporary failure in name resolution]
```

### 2. iLink rate limiting

Sending too many messages in a short period triggers iLink's rate limiter (`ret=-2 errmsg=rate limited`), which causes the connection to drop. This was observed on May 4, 2026, when multiple messages were sent in succession.

**Evidence in logs:**
```
iLink sendmessage rate limited: ret=-2 errcode=None errmsg=rate limited
```

## Resolution Steps

### Step 1: Verify current state

```bash
# Check gateway status
systemctl --user status hermes-gateway

# Check WeChat connection in logs
grep weixin ~/.hermes/logs/gateway.log | tail -5

# Check DNS resolution
getent hosts ilinkai.weixin.qq.com
```

### Step 2: Restart gateway

```bash
systemctl --user restart hermes-gateway
```

Wait ~30 seconds for WeChat to reconnect (must wait for Telegram+Discord timeout sequence first).

### Step 3: Add static hosts entries (if DNS failure is recurrent)

Requires root/sudo:

```bash
sudo tee -a /etc/hosts > /dev/null << 'EOF'

# WeChat iLink API - static entries to prevent DNS resolution failures
117.89.176.78 ilinkai.weixin.qq.com
61.151.230.245 ilinkai.weixin.qq.com
101.227.131.211 ilinkai.weixin.qq.com
180.101.242.203 ilinkai.weixin.qq.com
EOF
```

Note: IPs may change over time (CDN). Re-resolve with `getent hosts ilinkai.weixin.qq.com` and update if needed.

### Step 4: Ensure proxy is configured for gateway (China users)

The gateway service file must have `http_proxy`/`https_proxy` environment variables. Without them, Telegram and Discord will also timeout.

See `references/platform-setup-recipes.md` → "Proxy for China Users".

### Step 5: If rate-limited, reduce message frequency

iLink has a rate limit. If your bot sends many automated messages:
- Add artificial delays between sends
- Batch messages rather than sending individually

## Prevention

- **6-hour health check timer**: `hermes-gateway-healthcheck.timer` automatically restarts the gateway if it crashes
- **12-hour forced restart timer**: `hermes-gateway-restart.timer` prevents long-run degradation
- **Shell wrapper in .bashrc**: Typing `hermes` in the terminal checks/starts the web UI as a safety net

## Verification

After resolving:

```bash
# Check gateway is active
systemctl --user is-active hermes-gateway

# Check WeChat is connected
grep "✓ weixin connected" ~/.hermes/logs/gateway.log | tail -1

# Verify DNS works
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 https://ilinkai.weixin.qq.com
# Should return 404 (expected - means endpoint is reachable)
```
