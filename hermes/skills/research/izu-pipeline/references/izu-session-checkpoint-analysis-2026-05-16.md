# izu Session Checkpoint 执行路径分析（2026-05-16 萧何审计）

> 背景：萧何角色对"izu Session Checkpoint"功能的可行性进行系统分解。
> 审计源：实际代码 `/mnt/i/hermes/scripts/`（4文件，共2368行）

## 1. 资源盘点

| 文件 | 行数 | 可复用率 | 说明 |
|------|------|---------|------|
| izu-pipeline.py | 1309 | 60% | save_step/find_latest_step提供基线存储模式 |
| izu_coordinator.py | 477 | 70% | DAG依赖图+FileLock可复用于Session状态管理 |
| izu_sandbox.py | 354 | 10% | 沙箱模块，与session checkpoint无关 |
| izu_checkpoint.py | 228 | 40% | 检查点评分逻辑可复用，缺序列化/恢复引擎 |
| 已有数据 | — | — | izu_checkpoint_log.jsonl(10.9K) + izu_profile.json(2K) |

**需新开发：~730行**
- izu_session_serde.py (~280行)：Session元数据序列化/反序列化、断点标记、快照哈希
- izu_branch.py (~250行)：分支管理——时间旅行(v4.7)基础、分支链表、合并策略
- checkpoint扩展(至izu_checkpoint.py) (~200行)：CP1/CP3/CP4/CP5完整实现

## 2. 阶段拆解

| 阶段 | 输入 | 输出 | 工时(h) | 实际日历(0.25系数) |
|------|------|------|---------|-------------------|
| P1: 序列化引擎 | save_step/find_latest_step模式 | session_serde | 5h | 20天(4周) |
| P2: 分支管理 | Coordinator.DependencyGraph | branch | 4h | 16天(3.2周) |
| P3: CP1/3/4/5补齐 | izu_checkpoint.py CP2 | 5检查点完整 | 6h | 24天(4.8周) |
| P4: 流水线集成 | P1+P2+P3 | --checkpoint恢复 | 3h | 12天(2.4周) |
| P5: 时间旅行(v4.7) | P2分支+快照 | 任意节点恢复/回溯 | 4h | 16天(3.2周) |
| **总计** | | | **22h** | **约16周** |

## 3. 关键路径

**P1→P2→P5**（48天 = 20+16+12），P1序列化引擎是阻塞点。

CP补齐(24天)可与P2并行，不构成阻塞。

## 4. 风险矩阵

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| save_step文件名命名不稳定→序列化丢失 | 60% | 高 | 引入UUID主键+一致性校验和 |
| 流水线中途中断→未定义状态 | 50% | 高 | P4增加SIGINT处理+自动保存 |
| 分支膨胀→磁盘爆炸 | 30% | 中 | P2实现LRU GC+最大分支数限制 |
| CP5评分标准模糊 | 80% | 中 | 借鉴CP2代码评分+LLM判断模式 |
| 日均1h→排期过长 | 100% | 低 | 分拆双周里程碑，完成P1即MVP |

## 5. 边际成本

| 维度 | 当前 | 新增后 | 增幅 |
|------|------|--------|------|
| 运行时间 | 15-25min | +5-10min（序列化+哈希） | +30% |
| 存储 | ~50K步/次 | +20K JSON+5K索引 | +40% |
| API调用 | ~20次/pipeline | +4次（新CP各需1次LLM） | +20% |
| 冷启动恢复 | 不支持 | 任意中断点恢复+10s | 新增但可控 |
