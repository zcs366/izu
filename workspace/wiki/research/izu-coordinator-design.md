# izu Agent 协作冲突管理 — izu_coordinator

> **一句话概括**：当 7+ 智能体并行工作时，总有人会抢文件、产生矛盾、陷入死锁。这个系统管这些。
> **版本**：v1.0.0 | 脚本：`scripts/izu_coordinator.py`

---

## 1. 四层协作保障机制

| 层次 | 组件 | 解决的问题 |
|------|------|-----------|
| ① 文件锁 | `FileLock` | 两个 Agent 同时写同一文件 → 串行化 |
| ② 依赖图 | `DependencyGraph` | Agent A 等 B，但 B 等 A → 死锁检测 |
| ③ 冲突仲裁 | `Arbitrator` | 两个 Agent 给出相反结论 → 自动裁决 |
| ④ 总协调器 | `Coordinator` | 统一管理以上三层 |

## 2. 集成到 izu pipeline

在 `izu-pipeline.py` 中：

```python
from izu_coordinator import Coordinator

coord = Coordinator()

# 注册所有智能体（声明依赖）
coord.register_agent("探_A", depends_on=[], tools=["search"])
coord.register_agent("探_B", depends_on=[], tools=["search"])
coord.register_agent("搜_A", depends_on=["探_A", "探_B"], tools=["search"])
# ... 等13个

# 文件锁保护
with coord.lock_context("step_output.md", "搜_A") as locked:
    if locked:
        write_output()

# 状态更新
coord.set_status("探_A", "completed", output_path)

# 冲突仲裁
conflicts = coord.detect_conflicts()
coord.auto_resolve()

# 全景报告
print(coord.summary())
```

## 3. 仲裁规则

| # | 规则 | 说明 |
|---|------|------|
| 1 | 注册优先 | 死锁时先注册的 Agent 先执行 |
| 2 | 文件独占 | 同一文件同一时间只能一个 Agent 写 |
| 3 | 锁超时 | 60秒后自动释放过期锁 |
| 4 | 依赖就绪 | 只有所有依赖完成，Agent 才能启动 |
| 5 | 关键路径 | 最长依赖链决定总执行时间 |

## 4. 依赖图示例（izu 13 智能体）

```
探_A ──┐
       ├── 搜_A ──┐
探_B ──┘          │
                  ├── 织 → 对齐 → 写 → 沙箱 ──┬── 劈_A ──┐
探_A ──┐          │                            ├── 劈_B ──┤
       ├── 搜_B ──┘                            └── 劈_C ──┤
探_B ──┘                                                   ├── 修 → 核
```

## 5. 已知限制

1. 这是**单机版**协调器，不处理分布式场景
2. 文件锁基于文件系统（`O_EXCL`），在 NFS 上不可靠
3. 仲裁规则是硬编码的，暂不支持自定义策略
4. 死锁检测是静态的（基于依赖声明），不检测运行时死锁
