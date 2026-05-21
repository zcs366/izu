# Browser CDP Setup on WSL (Chrome DevTools Protocol)

## Overview

Hermes Agent's `browser` tool supports connecting to an external Chrome instance via CDP (Chrome DevTools Protocol). This is useful for:

- Persistent browser sessions across agent turns
- Debugging browser behavior via DevTools
- Using a Chrome profile with saved cookies/login states
- Running browser automation with the full Chrome engine (vs. the default headless mode)

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Chromium binary | `~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome` | Bundled by Playwright, no sudo needed |
| Launcher script | `~/.local/bin/chrome-cdp` | Convenience wrapper to launch Chrome with CDP flags |
| CDP endpoint | `ws://127.0.0.1:9222` | WebSocket URL for the DevTools Protocol |
| Hermes config | `~/.hermes/config.yaml → browser.cdp_url` | Tells the agent where to find Chrome |

## Script: chrome-cdp

```bash
#!/bin/bash
# Launch Chrome with CDP (Chrome DevTools Protocol) for browser automation
# Usage: chrome-cdp [port]     # default port 9222

PORT="${1:-9222}"
CHROME="$HOME/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

exec "$CHROME" \
  --headless=new \
  --no-first-run --no-default-browser-check \
  --disable-extensions --disable-gpu --disable-sync \
  --disable-translate --disable-default-apps \
  --remote-debugging-port="$PORT" \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="/tmp/chrome-cdp-$PORT" \
  "$@"
```

## Lifecycle

### Start

```bash
# Background (for agent use)
chrome-cdp 9222 &

# Foreground (for debugging)
chrome-cdp 9222

# Via Hermes terminal (background with process management)
# Use terminal() with background=true
```

### Verify

```bash
curl -s http://127.0.0.1:9222/json/version
# Should return JSON with Browser, Protocol-Version, webSocketDebuggerUrl
```

### Stop

```bash
# Kill by port
kill $(lsof -ti:9222)

# Or find the process
ps aux | grep chrome.*remote-debugging.*9222
```

## Common Issues

### Port Already in Use

```bash
lsof -ti:9222 | xargs kill -9
chrome-cdp 9222
```

### Chromium Path Changed

Playwright version updates change the cache directory. If you update Playwright, find the new path:

```bash
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print(p.chromium.executable_path)
"
```

Then update the `CHROME` variable in `~/.local/bin/chrome-cdp`.

### Session State Lost

The `--user-data-dir=/tmp/chrome-cdp-$PORT` is ephemeral. For persistent sessions (cookies, local storage):

1. Create a permanent directory: `mkdir -p ~/.chrome-profiles/cdp-9222`
2. Update the script to use: `--user-data-dir="$HOME/.chrome-profiles/cdp-$PORT"`

### Multiple Isolated Profiles

Use different ports for different contexts:

```bash
chrome-cdp 9222  # Main session
chrome-cdp 9223  # Secondary session
```

Each gets its own `--user-data-dir` (based on port) and its own CDP endpoint.
