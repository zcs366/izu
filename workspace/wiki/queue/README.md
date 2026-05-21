# Wiki URL Ingestion Queue

## 架构

```
用户转发URL ──┬──→ 路径A: 对话中直接处理 (实时)
              ├──→ 路径B: HTTP Webhook → 队列 → 批处理
              └──→ 路径C: 专用TG Bot → 队列 → 批处理
```

所有路径最终汇入同一个队列，由 cron job 统一处理。

## 文件结构

```
queue/
├── README.md           ← 本文件
├── url_queue.jsonl     ← URL队列，每行一个JSON
├── processed.json      ← 已处理URL的索引 (sha256去重)
├── collector.py        ← Telegram Bot 收集器 (路径C)
├── webhook-server.py   ← HTTP Webhook 接收端 (路径B)
└── ingest.py           ← 核心摄入脚本 (供cron job调用)
```

## 队列格式 (url_queue.jsonl)

每行一个JSON对象：
```json
{"url":"https://...","source":"telegram|webhook|chat","message_id":123,"timestamp":"2026-05-06T14:00:00","status":"pending"}
```

status: pending → processing → done | failed
