# ITA · 核战队记忆系统改造计划 — P0/P1 标注清单

> **生成:** 2026-05-18
> **来源:** 军师终裁（五人合议记录 + 代码摸底）
> **原则:** 地基不稳不盖二楼

---

## 总览

| 层级 | 项目 | 状态 | 工时预估 |
|------|------|------|----------|
| **P0** | 记忆系统三部曲 | ✅ 工具就位 / ❌ 自动化缺失 | 3-5h |
| **P1** | Evolver工程 | ⚠️ 骨架完成 / ❌ 系统未联 | 8-12h |
| **P2** | 技能趋势跟踪 | 🔄 融入现有cron | — |

---

## 🚨 P0 — 记忆系统（已开工，缺收尾）

### P0-1 Session Memory 衰减与遗忘（izu_session_memory.py）

**状态:** ✅ 工具已写，功能完整

**当前实现:**
- `izu_session_memory.py` (122行) — 衰减曲线(sigmoid)、遗忘门控(<0.15)、session audit、MEMORY.md衰减分析、报告生成
- 已产出记忆健康报告 `output/doc/memory_health/memory_health_20260517_2349.md`

**剩余差距（❌→收尾）：**

| # | 差距 | 具体动作 | 工时 |
|---|------|----------|------|
| 1 | ❌ 自动压缩未实现 | `cmd_compact` 当前只print占位文案。需实现：读取超50轮session → LLM摘要压缩 → 替换原文件 | 1.5h |
| 2 | ❌ 遗忘清理未自动化 | 待遗忘session(score<0.15)无人回收。需加 `cmd_purge`：标记→确认→归档或删除 | 1h |
| 3 | ❌ 无定时cron | 记忆健康报告需手动跑。应设cron `每6h` 自动生成+写入output/doc/memory_health/ | 0.5h |
| 4 | ⚠️ 健康报告格式待标准化 | 报告头YAML frontmatter缺失，不方便wiki入库 | 0.5h |

**P0-1 剩余: ~3.5h**

---

### P0-2 工作记忆 Top-K 队列（izu_working_memory.py）

**状态:** ✅ 工具已写，功能完整

**当前实现:**
- `izu_working_memory.py` (175行) — 消息评分(关键词+角色+长度)、top-K提取(K=5)、WORKING.md写入、session集成到MEMORY.md
- 支持.json和.jsonl两种session格式

**剩余差距（❌→收尾）：**

| # | 差距 | 具体动作 | 工时 |
|---|------|----------|------|
| 1 | ❌ 未接入Hermes启动流程 | WORKING.md写好了但Hermes启动时不读取。需改config.yaml或加hook让系统启动时自动加载WORKING.md | 1h |
| 2 | ⚠️ scoring规则需验证 | 当前基于关键词的启发式打分(30-10-8-5-3)，未与真实用户行为对标。需跑一次标注对比 | 0.5h |

**P0-2 剩余: ~1.5h**

---

### P0-3 Self Model 快照（izu_self_model.py）

**状态:** ✅ 工具已写，功能完整

**当前实现:**
- `izu_self_model.py` (132行) — 从SOUL.md提取身份锚点(name/role/personality/color/mission)、版本化快照、指纹对比、diff输出
- 已产出 `self_model_20260517_234941.json` (5锚点)

**剩余差距（❌→收尾）：**

| # | 差距 | 具体动作 | 工时 |
|---|------|----------|------|
| 1 | ❌ 无自动化触发 | 当前是手动命令调用。应：①设cron每日凌晨生成快照 ②SOUL.md变更时自动触发 | 0.5h |
| 2 | ⚠️ diff不是"真正diff" | 当前只比内容字符串不同。应加：①语义级漂移检测（锚点是否偏离核心定位）②漂移告警 | 可选 |

**P0-3 剩余: ~0.5h**

---

## 📋 P1 — Evolver 工程（骨架就位，缺系统联动）

### P1-1 技能量化评分（evolution_engine.py）

**状态:** ✅ 核心评分引擎已写 / ⚠️ 未接入SKILL.md

**当前实现:**
- `evolution_engine.py` (326行) — 5维度Scorer(URL存活/结构/引用/一致性/简洁度) + VerificationLoop(最多3次重试) + EvolutionTrigger(短板→提示调整)
- 信任验证循环：生成Agent→核验证Agent独立校验

**剩余差距（❌→联调）：**

| # | 差距 | 具体动作 | 工时 |
|---|------|----------|------|
| 1 | ❌ 未接入SKILL.md | Scorer当前评分任意文本，不读SKILL.md文件。需：遍历~/.hermes/skills/*/SKILL.md → 逐篇评分 → 输出技能健康报告 | 2h |
| 2 | ❌ 未接入izu拓扑数据 | `evolution_engine.py` 引用了 `izu-agent-topology-data.json` 但实际评分不依赖它。需统一拓扑+评分的数据流 | 1h |
| 3 | ❌ 短板自动修复未实现 | 当前只记录弱点，不自动改SKILL.md。需：①短板识别→②生成修改建议→③军师审批→④自动patch | 3h |
| 4 | ⚠️ Trajectory Credit + Balance 已写好但未连入进化循环 | `trajectory_credit.py`(632行评分+rise段标记) + `trajectory_balance.py`(391行平衡采样) 是两个独立模块。需整合到EvolutionTrigger | 1h |

**P1-1 剩余: ~7h**

---

### P1-2 成本作为优化目标

**状态:** ❌ 未开始

**当前:**
- 无token成本追踪模块
- 无"越用越便宜"的指标

**具体动作:**

| # | 动作 | 工时 |
|---|------|------|
| 1 | 建Token成本追踪器：每次Hermes调用后记录{tokens, model, cost}到data/cost_log.jsonl | 1h |
| 2 | 成本看板：每日/周/月成本趋势、按Agent/模型分类 | 1h |
| 3 | 接入Evolver：成本作为评分维度之一(weight ≤0.10) | 0.5h |

**P1-2 剩余: ~2.5h**

---

### P1-3 对话→SKILL自动转化

**状态:** ❌ 未开始

**具体动作:**

| # | 动作 | 工时 |
|---|------|------|
| 1 | 用izu_trajectory_credit识别高价值轨迹(credit>0.7) | 0.5h(现有工具) |
| 2 | 对话→SKILL.md模板生成器（从high credit轨迹提取步骤→结构化SKILL） | 2h |
| 3 | 军师审批流程（自动生成的SKILL需军师确认才写入） | 0.5h |

**P1-3 剩余: ~3h**

---

## 🎯 火线行动清单

### 这周开干（P0收尾）

| 优先级 | 事 | 谁来做 | 预计 |
|--------|----|--------|------|
| 🔴P0-1a | `izu_session_memory.py` — 实现自动压缩(`cmd_compact`) | 我来写代码 | ~1.5h |
| 🔴P0-1b | `izu_session_memory.py` — 遗忘清理(`cmd_purge`) | 我来 | ~1h |
| 🔴P0-1c | 加cron：每6h自动生成记忆健康报告 | 我来 | ~0.5h |
| 🔴P0-2a | 工作记忆接入Hermes启动流 | 我来 | ~1h |
| 🔴P0-3a | Self Model快照cron(每日凌晨) | 我来 | ~0.5h |

### 下周启动（P1开干）

| 优先级 | 事 | 谁做 | 预计 |
|--------|----|------|------|
| 🟡P1-1a | evolution_engine接入SKILL.md评分 | 我 | ~2h |
| 🟡P1-1b | trajectory_credit + balance整合进进化循环 | 我 | ~1h |
| 🟡P1-2a | Token成本追踪器 | 我 | ~1h |
| 🟡P1-3a | 对话→SKILL自动转化Pipeline | 我 | ~2.5h |

---

## 📌 已做总结（已标注完成的）

已完成的P0-P3项在代码里都标了 `P0-1/P0-2/P0-3` 注释头，并且5月17日已产出一份完整的记忆健康报告。Evolver引擎的核心评分逻辑(5维×权重)和核验证循环(最多3次重试)也都写好了。**缺的是收尾的10%**——自动压缩、遗忘清理、cron定时、系统联调。

**一句话：地基已经打了80%，现在把最后20%的钢筋水泥灌进去，就可以盖二楼。**
