# Morning Consolidation — 三重门 Cron Job 参考实现

> **文件**：`/mnt/i/hermes/izu/morning_consolidation.py`
> **来源**：Claude Code v2.1.88 泄露源码 `src/services/autoDream/autoDream.ts`
> **cron job**：`morning-consolidation`（每天5:30, job_id: dd2bfeaf81f6）

## 架构

```text
Script Phase (morning_consolidation.py — no_agent=False)
  └─ Gate 1: Time (stat lockfile mtime, ≥24h?)
  └─ Gate 2: Sessions (count sessions since last, ≥5?)
  └─ Gate 3: Lock (file-based advisory lock, 1h expiry)
      └─ Pass? → Agent Prompt Phase (delegate_task)
          └─ Orient → Gather Signal → Consolidate → Prune
```

## 门控参数

| 参数 | 值 | 来源 |
|------|-----|------|
| MIN_HOURS | 24 | Claude Code 标准 |
| MIN_SESSIONS | 5 | Claude Code 标准 |
| LOCK_TIMEOUT | 3600s (1h) | PID 重用防护 |
| MEMORY_CAP | 200行 | Claude Code MEMORY.md 上限 |

## 命令三角

```bash
python3 /mnt/i/hermes/izu/morning_consolidation.py           # 走三重门
python3 /mnt/i/hermes/izu/morning_consolidation.py --force    # 强制（等价 /dream）
python3 /mnt/i/hermes/izu/morning_consolidation.py --check    # 只检查状态
```

## 关联模块

- `circuit_breaker.py` — 子Agent断路保护
- `task_coordinator.py` — 任务类型+结构化结论
- `compression_pipeline.py` — 4层压缩管线
