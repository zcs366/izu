#!/bin/bash
# Wiki Webhook Server - startup/recovery script
# Restores the wiki-drop webhook server if not running.

WIKI_PATH="${WIKI_PATH:-/mnt/i/hermes/wiki}"
PORT=8765

# Check if already running
if curl -sf http://localhost:$PORT/health > /dev/null 2>&1; then
    exit 0
fi

# Start via tmux
cd "$WIKI_PATH/queue"
tmux new-session -d -s wiki-webhook "python3 webhook-server.py $PORT"
echo "wiki-webhook started on port $PORT"
