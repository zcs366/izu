# Discord Platform Configuration Reference

Complete configuration reference for Hermes Agent's Discord gateway platform.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | (required) | Bot token from Discord Developer Portal |
| `DISCORD_ALLOWED_USERS` | (empty=all) | Comma-separated Discord user IDs allowed to chat with the bot |
| `DISCORD_ALLOWED_ROLES` | (empty) | Comma-separated role IDs with access |
| `DISCORD_ALLOWED_CHANNELS` | (empty=all) | Channel IDs where bot responds (whitelist) |
| `DISCORD_IGNORED_CHANNELS` | (empty) | Channel IDs where bot NEVER responds |
| `DISCORD_FREE_RESPONSE_CHANNELS` | (empty) | Channel IDs where bot responds without @mention |
| `DISCORD_REQUIRE_MENTION` | `true` | Require @mention in guild channels (non-DMs) |
| `DISCORD_IGNORE_NO_MENTION` | `true` | Ignore messages in guild channels that don't mention any bot |
| `DISCORD_ALLOW_BOTS` | `none` | `none` / `mentions` / `all` — bot message filtering |
| `DISCORD_AUTO_THREAD` | `true` | Auto-create thread on @mention in text channels |
| `DISCORD_NO_THREAD_CHANNELS` | (empty) | Channel IDs where bot responds directly (no auto-thread) |
| `DISCORD_HOME_CHANNEL` | (auto) | Home channel ID for cron/notification delivery |
| `DISCORD_HOME_CHANNEL_NAME` | (auto) | Human-readable home channel name for logs |
| `DISCORD_PROXY` | (env proxy) | Explicit proxy URL for Discord (overrides http_proxy) |

## Key Behaviors

### @mention Requirement in Guild Channels

By default (`DISCORD_REQUIRE_MENTION=true`), the bot ignores messages in guild channels/threads unless @mentioned. DMs are exempt from this check.

The mention check in `_handle_message()` has a special exception: if the message is in a thread where the bot has **previously participated** (replied or auto-created), the mention requirement is bypassed. This is tracked in an in-memory set (`self._threads`).

**⚠️ Thread memory is lost on gateway restart.** After `systemctl --user restart hermes-gateway`, the bot forgets all previously-participated threads. Messages in existing threads are treated as new guild-channel messages — with `DISCORD_REQUIRE_MENTION=true`, they're silently ignored.

**Fixes:**
1. Set `DISCORD_FREE_RESPONSE_CHANNELS` to the thread/channel ID
2. Set `DISCORD_REQUIRE_MENTION=false` globally
3. Send the first post-restart message with @mention to re-establish thread participation

### Free Response Channels

Set via `DISCORD_FREE_RESPONSE_CHANNELS` or `discord.free_response_channels` in `config.yaml`. Accepts comma-separated channel IDs. Special value `*` means all channels.

When a channel ID (or its parent, for threads) is in this set, the mention requirement is bypassed. Useful for: home channel threads, dedicated support channels, admin channels.

### Allowed/Denied Channel Filtering

Order of operations in `_handle_message()`:
1. **Bot detection** — skip bots unless `DISCORD_ALLOW_BOTS` allows them
2. **User allowlist** (`DISCORD_ALLOWED_USERS` / `DISCORD_ALLOWED_ROLES`) — reject non-allowed users
3. **Multi-agent mention filtering** — if other bots are mentioned but this bot isn't, skip
4. **Allowed channels** (`DISCORD_ALLOWED_CHANNELS`) — if set, only respond in those channels
5. **Ignored channels** (`DISCORD_IGNORED_CHANNELS`) — never respond, even when @mentioned
6. **Free response / @mention check** — skip unless @mentioned or in free-response channel or an active bot thread
7. **Message processing** — handle command, text, attachments

### Slash Commands

On connection, the bot registers slash commands via `/_register_slash_commands()`. These are reconciled with Discord's existing commands:

```python
# Log line on restart:
Safely reconciled N slash command(s): unchanged=0 updated=0 recreated=40 created=0 deleted=0
```

"recreated=40" means all commands were re-registered (expected after restart). The `recreated` count being high is normal — Discord doesn't provide a command identity hash, so Hermes recreates all commands on reconnect.

### Intents Required

In the Discord Developer Portal → Bot → Privileged Gateway Intents, enable:
- ✅ **MESSAGE CONTENT INTENT** — Required for bot to read message text. Without it, `message.content` is empty → bot silently ignores all messages
- ✅ **SERVER MEMBERS INTENT** — Required for role-based allowlists
- ❌ **PRESENCE INTENT** — Optional, Hermes doesn't use it

### Pitfalls

- **Silent bot after restart:** If the bot appears online but doesn't respond to messages, check (1) Message Content Intent is enabled in Developer Portal, (2) `DISCORD_REQUIRE_MENTION` is not causing silent ignore, (3) the user ID is in `DISCORD_ALLOWED_USERS`
- **Thread messages ignored after restart:** In-memory thread participation list is reset. Use `DISCORD_FREE_RESPONSE_CHANNELS` or @mention the bot in first message
- **Slash commands take time to propagate:** After reconnection, slash commands are re-registered. Discord can take 1-2 minutes to propagate them to all guilds
- **No `Using proxy for Discord` log line:** If this line is missing from gateway startup, the proxy env vars aren't reaching the process. Check `systemctl --user show hermes-gateway.service --property=Environment` to verify
- **DISCORD_HOME_CHANNEL is a thread:** Verified via `curl -H "Authorization: Bot $TOKEN" https://discord.com/api/v10/channels/$ID`. Type 11 = PUBLIC_THREAD, type 12 = PRIVATE_THREAD. Threads in guilds still respect `DISCORD_REQUIRE_MENTION` unless in free response channels.

## Verification Commands

```bash
# Check bot status and channel type
TOKEN=$(grep DISCORD_BOT_TOKEN ~/.hermes/.env | cut -d= -f2-)
curl -s -H "Authorization: Bot $TOKEN" https://discord.com/api/v10/users/@me | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{d[\"username\"]}#{d.get(\"discriminator\",\"\")}')"

# Check a channel/thread type
curl -s -H "Authorization: Bot $TOKEN" https://discord.com/api/v10/channels/<ID> | python3 -c "import json,sys; d=json.load(sys.stdin); type_map={0:'GUILD_TEXT',1:'DM',11:'PUBLIC_THREAD',12:'PRIVATE_THREAD'}; print(f'{d.get(\"id\")} = {type_map.get(d.get(\"type\"),\"?\")} name={d.get(\"name\",\"\")}')"

# Test message sending (via gateway internal API)
# From a Hermes session:
send_message(target="discord:#常规", message="test")
```
