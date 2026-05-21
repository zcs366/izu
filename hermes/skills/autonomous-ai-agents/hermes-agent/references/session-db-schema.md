# Hermes SessionDB Schema

The Hermes Agent stores session state in a SQLite database at `~/.hermes/state.db` (or `$HERMES_HOME/state.db`). This is used by the built-in session management, the `session_replay.py` diagnostic tool, the `ctx_dashboard.py` context monitor, and the gateway's session resume feature (v0.13.0+).

## Schema

### `sessions` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | TEXT PK | Session ID (format: `YYYYMMDD_HHMMSS_random`, e.g. `20260508_135204_0974a7c5`) |
| `source` | TEXT NOT NULL | Origin platform (`cli`, `telegram`, `weixin`, `tui`, `cron`, `acp`, `api`, etc.) |
| `user_id` | TEXT | User identifier on the platform |
| `model` | TEXT | Model name used (e.g. `deepseek-v4-flash`) |
| `model_config` | TEXT | JSON blob of model config overrides |
| `system_prompt` | TEXT | System prompt used for this session |
| `parent_session_id` | TEXT FK | Reference to parent session (for branching) |
| `started_at` | REAL NOT NULL | Unix timestamp (seconds, with decimals) |
| `ended_at` | REAL | Unix timestamp when session ended |
| `end_reason` | TEXT | Why session ended (e.g. `completed`, `interrupted`, `error`) |
| `message_count` | INTEGER DEFAULT 0 | Number of messages |
| `tool_call_count` | INTEGER DEFAULT 0 | Number of tool calls |
| `input_tokens` | INTEGER DEFAULT 0 | Total input (prompt) tokens |
| `output_tokens` | INTEGER DEFAULT 0 | Total output (completion) tokens |
| `cache_read_tokens` | INTEGER DEFAULT 0 | Tokens read from cache |
| `cache_write_tokens` | INTEGER DEFAULT 0 | Tokens written to cache |
| `reasoning_tokens` | INTEGER DEFAULT 0 | Reasoning/thinking tokens |
| `billing_provider` | TEXT | Provider for billing |
| `billing_base_url` | TEXT | Base URL for billing |
| `billing_mode` | TEXT | Billing mode |
| `estimated_cost_usd` | REAL | Estimated cost |
| `actual_cost_usd` | REAL | Actual cost (if available) |
| `cost_status` | TEXT | Cost tracking status |
| `cost_source` | TEXT | Cost data source |
| `pricing_version` | TEXT | Pricing schema version |
| `title` | TEXT | Session title (user-defined or auto-generated) |
| `api_call_count` | INTEGER DEFAULT 0 | Number of API calls made |
| `FOREIGN KEY` | `(parent_session_id) REFERENCES sessions(id)` | |

### `messages` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK AUTO | Auto-incrementing message ID |
| `session_id` | TEXT NOT NULL FK | References `sessions(id)` |
| `role` | TEXT NOT NULL | `user`, `assistant`, `tool`, `system` |
| `content` | TEXT | Message content text |
| `tool_call_id` | TEXT | ID of the tool call this result belongs to |
| `tool_calls` | TEXT | JSON array of tool call objects |
| `tool_name` | TEXT | Tool name (for tool role messages) |
| `timestamp` | REAL NOT NULL | Unix timestamp |
| `token_count` | INTEGER | Token count for this message |
| `finish_reason` | TEXT | Stop reason (`stop`, `tool_calls`, `length`, etc.) |
| `reasoning` | TEXT | Reasoning content |
| `reasoning_content` | TEXT | Visible reasoning content |
| `reasoning_details` | TEXT | Detailed reasoning info |
| `codex_reasoning_items` | TEXT | Codex-specific reasoning |
| `codex_message_items` | TEXT | Codex-specific message items |

## Query Patterns

### List recent sessions
```sql
SELECT id, source, model, title, message_count,
       input_tokens, output_tokens, started_at
FROM sessions
ORDER BY started_at DESC
LIMIT 20;
```

### Get session summary with cost
```sql
SELECT id, title, source, model,
       message_count, api_call_count,
       input_tokens + output_tokens + cache_read_tokens AS total_tokens,
       estimated_cost_usd,
       started_at, ended_at
FROM sessions
WHERE id = '<session_id>';
```

### Get full message timeline for a session
```sql
SELECT id, role, content, tool_calls, tool_name,
       token_count, timestamp
FROM messages
WHERE session_id = '<session_id>'
ORDER BY timestamp ASC;
```

### Token usage breakdown
```sql
SELECT session_id,
       SUM(CASE WHEN role = 'user' THEN token_count ELSE 0 END) AS user_tokens,
       SUM(CASE WHEN role = 'assistant' THEN token_count ELSE 0 END) AS assistant_tokens,
       SUM(CASE WHEN role = 'tool' THEN token_count ELSE 0 END) AS tool_tokens
FROM messages
WHERE session_id = '<session_id>'
GROUP BY session_id;
```

### Tool call frequency
```sql
SELECT m.tool_name, COUNT(*) AS call_count,
       SUM(m.token_count) AS total_tokens
FROM messages m
WHERE m.role = 'tool' AND m.tool_name IS NOT NULL
GROUP BY m.tool_name
ORDER BY call_count DESC;
```

## Notes

- Timestamps are Unix epoch in **seconds** (float with millisecond precision), not milliseconds.
- Session IDs are generated as `{YYYYMMDD}_{HHMMSS}_{random8chars}`.
- The `tool_calls` column stores JSON. It can be either a JSON array `[{...}, {...}]` or a single JSON object `{...}` depending on the provider. Always normalize with `json.loads()`.
- Cache hit rates can exceed 100% (cache reads / input tokens) because cache includes system prompt overlap across sessions.
- The `sessions` table uses `id` as the key; older schemas (pre-v0.12) may use `session_id` instead.
