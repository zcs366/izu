# Morning Consolidation 设计文档

> 基于 Claude Code autoDream 三重门模式移植 | 2026-05-20

## 脚本位置

`/mnt/i/hermes/izu/morning_consolidation.py`

## 命令速查

```bash
python3 morning_consolidation.py           # 正常执行（走三重门）
python3 morning_consolidation.py --force   # 强制（等价 /dream）
python3 morning_consolidation.py --check   # 只检查门控状态
```

## 三重门逻辑

Gate 顺序按计算成本排列——最便宜的检查最先做：

1. **Gate 1: 时间门** — `stat(lockfile).mtime` 距上次 ≥24h（一次系统调用）
2. **Gate 2: 会话门** — 自上次 consolidation 后新增 session ≥5（查 session DB）
3. **Gate 3: 锁文件门** — `~/.hermes/consolidation.lock` 能否获取
   - mtime = 最后 consolidation 时间（双用途）
   - body = 持有者 PID
   - PID 重用防护：进程不存在则允许接替

## Cron Job

- 名称：`morning-consolidation`
- 时间：每天 5:30
- 模式：pure prompt（脚本做门控，prompt 做 consolidation 逻辑）
- 交付：local（有异常才提醒）
- 工具集：search, file, terminal, delegation

## Consolidation 四阶段

1. **Orient** — 读取当前 wiki/ 状态 + fact_store 低信任度条目 + WORKING.md
2. **Gather Signal** — session_search 最近24h新决策/偏好/完成的任务
3. **Consolidate** — 压缩过期 session、删除临时记录、更新时间引用
4. **Prune** — 检查容量上限、标记低价值条目

## 参考

- Claude Code v2.1.88 `src/services/autoDream/autoDream.ts`
- 硅谷温差 Ep2「Agent 记忆系统 = AGI ?」(BV13WRGBoEU3)
