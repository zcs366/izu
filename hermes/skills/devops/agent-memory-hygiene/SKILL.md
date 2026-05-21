---
name: agent-memory-hygiene
description: "Agent生态健康维护系统——覆盖记忆/Skill/工具三大核心资产的日常维护：Session衰减/压缩/遗忘/Self Model快照 + Skill健康扫描/自动修正/看板 + 升级自动防护。核心原则：Agent系统不是越存越多，而是越维护越健康。"
version: 2.2.0
author: 军师祭酒
tags:
  - ecosystem-health
  - memory-system
  - skill-health
  - session-compaction
  - forgetting-mechanism
  - working-memory
  - self-model
  - health-monitoring
  - upgrade-guard
  - auto-fix
trigger: "agent health OR 生态维护 OR 系统维护 OR 记忆卫生 OR skill健康 OR 升级防护 OR 全面体检"
metadata:
  hermes:
    category: devops
---

# Agent 生态健康维护系统

> **核心问题**：Agent系统运行数周后，记忆膨胀不衰减、skill质量参差不齐、工具配置散乱、一场Hermes升级打乱全部定制。
> **核心路线**：三大支柱（记忆·Skill·工具）各自有独立的维护生命周期，但由统一的cron管线协调调度。
> **关键机制**：每日6:00自动扫描→修正→报告→归档，有异常才提醒，无变化则静默。

---

## 一、三大支柱

```
┌─────────────────────────────────────────────────────┐
│          Agent 生态健康维护系统                        │
├───────────────┬────────────────┬────────────────────┤
│   记忆健康    │   Skill健康     │   升级防护盾        │
│   izu_session │ izu_skill_     │ izu_hermes_        │
│   _memory.py  │ ecosystem_     │ upgrade_guard.py   │
│   izu_self_   │ health.py      │                    │
│   model.py    │ izu_skill_     │                    │
│               │ scorer.py      │                    │
├───────────────┼────────────────┼────────────────────┤
│ 压缩/遗忘/    │ 扫描/评分/      │ 升级前快照/升级后   │
│ Self Model   │ 自动修正/看板   │ diff/兼容检查       │
│ 快照/漂移检测 │ is_user_skill    │                    │
│               │ 保护            │                    │
├───────────────┼────────────────┼────────────────────┤
│ cron: 每6h    │ cron: 每日6:00 │ 按需触发            │
│ 安静维护      │ 有异常才提醒    │ /pre-upgrade        │
└───────────────┴────────────────┴────────────────────┘
```

---

## 二、记忆健康（已有，v1.0核心内容保留）

> 详见下文「三~九」节——Session衰减/自动压缩/遗忘清理/工作记忆/Self Model/自动化管线/陷阱/首次部署/监控指标。

---

## 三、Skill健康（v2.0新增）

### 3.1 健康扫描

使用 `izu_skill_scorer.py` 对所有SKILL.md进行6维评分：

| 维度 | 权重 | 评分方法 |
|------|------|----------|
| URL存活率 | 20% | curl检查前20个URL |
| 结构完整性 | 20% | frontmatter/标题/代码块/表格/用法段检测+加分 |
| 引用准确性 | 15% | 有引用无链接则扣分 |
| 内部一致性 | 20% | 排除日期/版本/时间后的数字范围异常检测 |
| 简洁度 | 15% | 平均句长偏离10-40字扣分 |
| (元数据) | — | 检查frontmatter/date/version/tags/description |

### 3.2 评分器特殊处理

```python
# check_structure — SKILL专用版
# 自动检测：frontmatter(+0.2分) / 代码块(+0.1) / 表格(+0.1)
# 替代了旧版只搜 ## 标题字符串的简陋逻辑

# check_consistency — 排除已知误报模式
cleaned = re.sub(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', '', text)  # 日期: 2026-05-16
cleaned = re.sub(r'v?\d+\.\d+(\.\d+)?', '', cleaned)         # 版本: v1.0.0
cleaned = re.sub(r'\d{1,2}:\d{2}[-~到]\d{1,2}:\d{2}', '', cleaned)  # 时间: 6:30-7:00
```

### 3.3 自动修正（仅用户skill）

```python
def is_user_skill(content) -> bool:
    """跳过Hermes官方/外部skill的判断逻辑"""
    # 外部特征: homepage: / metadata:hermes / author: Hermes Agent / plugin:
    # 命中任一 → 跳过自动修正（避免被上游升级覆盖）
```

自动修正动作：
- **缺失date** → 从frontmatter `date: 2026-05-18` 补齐
- **缺失version** → 从frontmatter `version: 1.0.0` 补齐

### 3.4 看板输出

```
## 🧬 Skill生态健康看板
> 2026-05-18 08:32 | 136个skills
| 🟡 0.70-0.85 | 135 | ███████████████████ |
| 🟠 0.50-0.70 |   1 | █                  |
| 🔴 <0.50     |   0 | ░                  |
| **平均**     | **0.774** |               |
```

### 3.5 核心工具一览

| 工具 | 位置 | 功能 |
|------|------|------|
| `izu_skill_scorer.py` | `/mnt/i/hermes/izu/` | 6维评分引擎 |
| `izu_skill_ecosystem_health.py` | `/mnt/i/hermes/izu/` | 扫描+自动修正+看板+报告 |
| `izu_hermes_upgrade_guard.py` | `/mnt/i/hermes/izu/` | 升级前快照+升级后diff |

---

## 四、Session衰减审计（原有核心）

### 衰减曲线参数

```
半衰期: 24小时（可调）
遗忘阈值: 0.15（低于此值自动清理）
压缩阈值: 50轮（超过此值需压缩为摘要）

衰减公式: score = 0.5^(age_hours / half_life) × access_boost × importance
访问增强: 1.0 + min(accesses, 10) × 0.05
永久条目: persistent=True 的条目不衰减
```

### 状态判定

| 分数 | 状态 | 处理 |
|------|------|------|
| ≥0.7 | 🟢活跃 | 保持 |
| 0.15~0.69 | 🟡渐弱 | 超过50轮则压缩 |
| <0.15 | 🔴待遗忘 | 自动清理 |

---

## 五、规则提取压缩（零LLM成本）

### 提取维度

从session消息中自动提取（基于正则，不调用模型）：

| 维度 | 提取方式 | 用途 |
|------|----------|------|
| **用户意图** | 关键词匹配（开干/启动/创建/写/部署/？） | 快速了解用户关注点 |
| **决策/结论** | 决策信号词（因此/所以/结论/决定/军师终裁） | 保留关键判断 |
| **工具调用** | 从tool_calls提取函数名 + 去重统计 | 了解工具使用模式 |
| **关键事实** | 路径/文件名 + success/complete信号 | 保留可操作性结果 |
| **代码片段** | 正则提取 ``` 代码块 | 保留技术产出 |
| **引用链接** | URL正则提取 | 保留来源 |

### 压缩输出格式

```markdown
# Session 压缩摘要
> 原始: {session_name} | {N}轮 | {age}h前
> 分数: {score} | 状态: {state}

## 用户意图/问题
- {intent_1}

## 决策/结论
- {decision_1}

## 工具调用 (去重)
- {tool_name} ×{count}

## 关键事实
- {fact}

## 代码 (片段)
- {snippet}

## 引用链接
- {url}
---
压缩于: {timestamp}
原始: {N}轮 → 摘要: {M}行
```

---

## 六、工作记忆 → 系统提示集成

### 机制

1. `izu_working_memory.py` 从最近3个活跃session提取top-K(K=5)高价值条目
2. 写入 `WORKING.md`
3. SOUL.md 尾部引用 WORKING.md 路径
4. 每次新会话启动，系统提示自动载入 → 工作记忆上下文就绪

### 评分规则（启发式，零模型成本）

```python
if 决策信号词(记住/重要/必须/决定/结论): +30
if 引用性("上次"/"之前"/"刚才"/"前面"): +15
if 动作(写入/创建/修改/部署): +10
if 疑问句: +8
if 用户消息: +5
if 助手长回复(>200字): +3
if 极短回复("好的"/"明白"/"嗯"/"ok"): -5
```

---

## 七、Self Model 身份漂移检测

### 锚点提取

从SOUL.md中提取不可变的身份定义：
- name / role / description / personality / color / mission

### 版本管理

- 每次快照生成版本指纹 hash(name|role|description|...)
- 指纹变化 → 告警身份漂移
- 对比最新两个版本差异 → 精确到锚点级别的变更

---

## 八、自动化维护管线

### 8.1 Cron Job 报告决策树

cron job 的交付报告遵守以下规则，避免「报告疲劳」：

**判断逻辑（按顺序）：**

1. 先跑 `izu_skill_ecosystem_health.py full` 或对应维护脚本
2. 读取生成的 dashboard 和 report，比较昨日数据
3. 识别三类异常：
   - **新增低分**：昨天均分>0.70，今天<0.70 → 详细报告
   - **阈值突破**：任何 skill 总分 < 0.65 → 详细报告（即使昨日已在低分区）
   - **系统性退化**：平均分下降 > 0.02 或 🟠/🔴 数量增加 → 中等详细报告
4. 以上皆无 → 一句话看板：`🌅 Skill生态健康 · N/N 正常 · 平均分X.XXX`

**报告格式模板：**

```markdown
# 异常模式（触发③阈值突破或①新增低分）
🌅 Skill生态健康 · N/N 正常 · 平均分X.XXX
⚠️ **{skill_name}** 总分 **{score}**（低于0.65阈值）
问题诊断：{维度得分表}
建议：{修复方向}

# 正常模式（无异常）
🌅 Skill生态健康 · N/N 正常 · 平均分X.XXX
```

**关键区别**：
- 「<0.65」= 当前状态异常，需要报告提醒用户关注
- 「新增低分」= 趋势恶化，需要报告对比昨日数据
- 「持续低分无恶化」= 已知问题，正常模式一句话即可，无需重复强调

### 推荐cron配置

```yaml
# 记忆维护 — 每6小时
schedule: "0 */6 * * *"
script: izu_memory_maintenance.py   # compact → purge → report → snapshot(凌晨)

# Skill生态健康 — 每日6:00
schedule: "0 6 * * *"
name: skill-ecosystem-health
prompt: "每天清晨的Skill生态系统健康维护"  # 安静维护，有异常才报告

# Morning Consolidation — 每日5:30（三重门门控）
schedule: "30 5 * * *"
name: morning-consolidation
prompt: "记忆整合任务，走三重门（时间→会话→锁文件）"
enabled_toolsets: [search, file, terminal, delegation]
deliver: local  # 有异常才提醒，平时静默
```

### 8.2 Cron Job 报告决策树

```bash
# ── 记忆健康 ──
python3 /mnt/i/hermes/izu/izu_session_memory.py audit     # 审计session状态
python3 /mnt/i/hermes/izu/izu_session_memory.py compact   # 压缩
python3 /mnt/i/hermes/izu/izu_session_memory.py purge     # 清理
python3 /mnt/i/hermes/izu/izu_session_memory.py report    # 报告
python3 /mnt/i/hermes/izu/izu_self_model.py snapshot      # Self Model快照

# ── Skill健康 ──
python3 /mnt/i/hermes/izu/izu_skill_scorer.py scan        # 全扫描
python3 /mnt/i/hermes/izu/izu_skill_scorer.py scan --min  # 只看低分
python3 /mnt/i/hermes/izu/izu_skill_scorer.py check <名>  # 单个检查
python3 /mnt/i/hermes/izu/izu_skill_ecosystem_health.py fix     # 扫描+自动修正
python3 /mnt/i/hermes/izu/izu_skill_ecosystem_health.py dashboard # 看板
python3 /mnt/i/hermes/izu/izu_skill_ecosystem_health.py full     # 全流程

# ── 升级防护 ──
python3 /mnt/i/hermes/izu/izu_hermes_upgrade_guard.py snapshot   # 升级前
python3 /mnt/i/hermes/izu/izu_hermes_upgrade_guard.py check      # 升级后
python3 /mnt/i/hermes/izu/izu_hermes_upgrade_guard.py protect    # 一键引导
```

---

## 九、陷阱与注意事项

### 通用陷阱

| 陷阱 | 说明 | 对策 |
|------|------|------|
| **遗忘过度** | 阈值太高(>0.3)，新session也被清理 | 保持0.10~0.15 |
| **压缩过度** | 关键决策漏提取 | 提取得分规则要迭代：漏了什么→加关键词 |
| **永久条目膨胀** | 太多persistent标记，失去遗忘效果 | 限制persistent≤10条 |
| **工作记忆污染** | WORKING.md写入太多低价值条目 | K≤5，评分严格 |
| **自动修正覆盖外** | 自动修正Hermes官方skill | `is_user_skill()` 保护已启用，外部skill不碰 |
| **报告疲劳** | 每6h长篇报告无人看 | 只输出diff，无变化静默 |

### 关键原则

```
1. 遗忘不是失败，是维持系统健康的必要机制
2. 规则提取优于模型提取（零成本、可审计、稳定）
3. 记忆大小不应该和交互轮数成正比
4. 工作记忆应该被主动管理，而不是被动截断
5. 永久条目越少越好
6. 自动修正只修用户skill，不动Hermes官方
```

---

## 十、首次部署步骤

```bash
# 1. 记忆系统初始化
python3 session_memory.py audit
python3 session_memory.py compact
python3 session_memory.py purge
python3 session_memory.py report
python3 working_memory.py snapshot
python3 self_model.py snapshot

# 2. Skill系统初始化
python3 izu_skill_scorer.py scan
python3 izu_skill_ecosystem_health.py fix
python3 izu_skill_ecosystem_health.py dashboard

# 3. 升级防护首次快照
python3 izu_hermes_upgrade_guard.py snapshot

# 4. 设置cron
# 记忆：cronjob(action='create', schedule='0 */6 * * *', script='memory_maintenance.py', no_agent=True)
# Skill：cronjob(action='create', schedule='0 6 * * *', name='skill-ecosystem-health', ...)
```

---

## 十一、监控指标

| 指标 | 健康值 | 警告值 | 危险值 |
|------|--------|--------|--------|
| 活跃session占比 | >20% | 10~20% | <10% |
| 待遗忘session占比 | <10% | 10~30% | >30% |
| Skill平均分 | ≥0.75 | 0.65~0.75 | <0.65 |
| 低分skill占比（<0.70） | <5% | 5~15% | >15% |
| 跨越阈值skill（<0.65） | 0个 | 1个（持续则关注非报告） | ≥2个 |
| 新发低分skill（昨日≥0.70→今日<0.70） | 0个 | 1个（需详细报告） | ≥2个 |
| Self Model指纹漂移 | 0次/周 | 1次/周 | >2次/周 |

**告警程度分级**：
- **🔴 红色告警**（详细报告）：新发低分 skill ≥ 1 个，或 <0.65 skill ≥ 2 个，或平均分下降 > 0.03
- **🟡 黄色关注**（简短报告）：持续低分 skill 1 个（0.50~0.65），或平均分下降 0.01~0.03
- **🟢 正常**（一句话）：以上皆无

---

## 支持文件

| 文件 | 内容 |
|------|------|
| `references/claude-code-autodream-benchmark.md` | 与 izu 遗忘引擎的逐项对照 |
| `references/claude-code-patterns-izu-modules.md` | 三个移植模块（Circuit Breaker / Coordinator / Compression） |
| `references/session-compaction-implementation.md` | 规则压缩的代码实现参考 |
| `references/skill-ecosystem-health-tools.md` | Skill&升级防护工具详细说明 |
| `references/claude-code-autodream-benchmark.md` | Claude Code autoDream 三重门+锁文件设计对照 |
| `references/morning-consolidation-script.md` | morning_consolidation.py 设计文档和用法 |
| `references/low-score-debugging-workflow.md` | 低分skill分析工作流 + 维度解读 + 历史案例 |

---

## 十二、Claude Code autoDream 对照基准（2026-05-20 新增）

> **来源**：Claude Code v2.1.88 泄露源码 `src/services/autoDream/autoDream.ts`
> **价值**：业界唯一已知的工程化 Dreaming 实现，可作本系统 consolidation 管线的黄金对照基准

### 12.1 autoDream 设计要点

| 维度 | Claude Code 实现 | 我们的对应 | 差距 |
|------|-----------------|-----------|------|
| **触发条件** | 三重门：≥24h + ≥5新session + 文件锁 | 手动触发 / 定时cron | ❌ 缺状态感知触发 |
| **执行体** | fork独立subagent，不中断主会话 | 依赖主agent进程 | ❌ 缺独立后台进程 |
| **锁保护** | 文件锁：mtime=lastConsolidatedAt, body=PID, PID重用防护 | 无 | ❌ 缺防重入 |
| **输出约束** | 硬性200行 MEMORY.md 上限 | 无硬性cap | ❌ 缺膨胀防线 |
| **手动指令** | `/dream` 命令 | 无统一命令 | ❌ 缺快捷入口 |
| **合并策略** | 删过期、解矛盾、时间精确化 | Ebbinghaus衰减 + 冲突检测 | ✅ 更智能 |
| **回滚** | 无回收站 | `izu_recycle_bin.py` | ✅ 有回收站 |
| **决策算法** | 规则型（删过期条目） | 遗忘曲线+冲突检测→三选一 | ✅ 更先进 |

### 12.2 三重门触发模式（推荐借鉴）

Gate 顺序按计算成本排列——最便宜的检查最先做：

```python
# 伪代码：autoDream 触发逻辑
def should_consolidate():
    # Gate 1: 时间门（最便宜，一次stat）
    hours_since = (now - last_consolidated_at).hours
    if hours_since < MIN_HOURS:   # MIN_HOURS = 24
        return False

    # Gate 2: 会话门（中等成本，查session数）
    new_sessions = count_sessions_since(last_consolidated_at)
    if new_sessions < MIN_SESSIONS:  # MIN_SESSIONS = 5
        return False

    # Gate 3: 锁文件门（最贵，IO操作）
    if not acquire_consolidation_lock():
        return False   # 另一个进程已在跑

    return True
```

### 12.3 锁文件设计（推荐借鉴）

```python
# 锁文件：~/.hermes/consolidation.lock
# mtime = 最后consolidation时间（双用途！）
# 内容 = 持有者的PID
#
# PID重用防护：如果文件存在但PID已死，认为锁已过期
# 锁过期时限：比MIN_HOURS更长

def acquire_consolidation_lock() -> bool:
    lock_path = Path("~/.hermes/consolidation.lock")
    if lock_path.exists():
        pid = int(lock_path.read_text().strip())
        if is_pid_alive(pid):
            return False      # 真正的锁
        # PID已死 → 锁过期，允许接替
    lock_path.write_text(str(os.getpid()))
    os.utime(lock_path, None)  # 更新mtime
    return True
```

### 12.4 操作建议

基于此对照，本系统的 consolidation 管线应优先补齐的缺口（按收益排序）：

1. **锁文件 + 三重门**（2h工作量）—— 立即提升稳定性 ✅ 已实现 `morning_consolidation.py`
2. **统一命令**（0.5h）—— `izu memory consolidate` 等价于 `/dream`
3. **硬性容量上限**（1h）—— 为记忆文件设定行数/大小上限
4. **后台 subagent 执行**（4h）—— 长远目标，需改cron架构

### 12.5 Morning Consolidation Cron Job

已实现脚本：`/mnt/i/hermes/izu/morning_consolidation.py`

```bash
python3 morning_consolidation.py           # 走三重门
python3 morning_consolidation.py --force   # 强制（等价 /dream）
python3 morning_consolidation.py --check   # 只检查
```

已创建的 cron job：
- 名称：morning-consolidation (job_id: dd2bfeaf81f6)
- 时间：每天 5:30
- 模式：纯 prompt（需要 delegate_task 跑 Agent 任务）
- 交付：local（有异常才提醒）

### 12.6 扩展阅读

Claude Code 泄露源码中与本系统直接相关的其他范式：

| 范式 | 文件 | 相关性 |
|------|------|--------|
| 4层压缩管线（Snip→Microcompact→Collapse→Auto） | `wiki/comparisons/claude-code-patterns-deep.md` | session 压缩/Compact 策略 |
| Circuit Breaker（收益递减检测） | 同上 | 防止 consolidation subagent 空转 |
| Coordinator 最小权限（仅3个工具） | 同上 | delegate_task 任务类型设计 |
| ToolSearch 按需加载 | 同上 | 工具池分级策略 |

---

## 十三、运维脚本自愈工程（自检脚本加固模式）

记忆系统需要一组可靠的 cron 脚本来驱动维护。这些脚本面临的核心风险是：**静默失败**（脚本退出非零但无告警、连锁失败、无超时保护）。

### 12.1 安全运行模式（safe_run）

任何 shell 包装脚本都应遵循这个模式——各步骤隔离、超时保护、局部失败不阻断全局：

```bash
# ☠️ 错误写法：一条命令失败，整个脚本中断
python3 cmd1.py      # 失败 → exit 1，cmd2 不执行
python3 cmd2.py

# ✅ 正确写法：各步骤独立，有超时，失败不影响后续
safe_run() {
    local label="$1"
    local cmd="$2"
    local logfile="$3"
    if timeout 60 bash -c "$cmd" >> "$REPORT" 2>"$logfile.tmp"; then
        echo "✅ $label 成功"
    else
        local rc=$?
        echo "⚠️ $label 失败 (exit=$rc)" >> "$REPORT"
        echo "❌ $label 失败 (exit=$rc)" >&2
        cat "$logfile.tmp" > "$logfile"
    fi
}

safe_run "阶段A" "python3 cmd1.py" "$ERROR_LOG"
safe_run "阶段B" "python3 cmd2.py" "$ERROR_LOG"
```

**关键规则**：
1. 每个子命令用 `timeout 60` 保护，防止 Python 脚本卡死
2. 每个子命令的 stderr 独立写入错误日志文件
3. 失败的步骤只追加警告到报告，不阻断后续步骤
4. 最终汇总：有错则输出警告路径，无错则静默

### 12.2 配置变更保护（写后验证）

对 YAML/JSON/TOML 配置文件做任何写入操作时必须加验证：

```python
# ☠️ 错误写法：正则替换 + 无验证
re.sub(r'脆弱正则', new_val, content)  # 缩进一变就失效
write(path, content)                     # 写进去了但可能是错的

# ✅ 正确写法：结构化解析 + 读回验证
from ruamel.yaml import YAML
yaml = YAML()
with open(path) as f: cfg = yaml.load(f)
cfg["delegation"]["model"] = new_val
with open(path, "w") as f: yaml.dump(cfg, f)

# 读回验证
with open(path) as f: verify = f.read()
actual = get_current_model_from_file(verify)
if actual != new_val: raise ConfigError("验证失败")
```

**适用场景**：所有通过 cron 定时修改配置文件的脚本——模型切换、环境切换、API key 轮换等。

### 12.3 静默失败终结者

cron 脚本最大的敌人不是出错，而是**出错无人知**。每个运维脚本应：

1. **写日志**到统一目录（如 `~/.hermes/logs/`），含时间戳和操作结果
2. **stdout 输出清晰**——cron 的 `no_agent=True` 模式会捕获 stdout 作为交付内容，失败时要输出 `❌` 信号
3. **退出码正确**——`exit 0` 成功，`exit 1` 失败，这样 cron 的 `last_status` 才能准确反映
4. **关键失败通知**——模型切换、配置变更等关键操作失败时，通过通知脚本发告警

```python
# 通知模式（静默失败不阻塞主流程）
def send_notification(title, body):
    if os.path.exists(NOTIFICATION_SCRIPT):
        subprocess.run(["bash", NOTIFICATION_SCRIPT, title, body],
                       timeout=10, capture_output=True)
    # 主流程继续，通知失败不阻断切换
```

### 12.4 cron 健康评估方法论

当用户问"定时任务运行状态如何"，按以下三步系统评估：

**第一步：全量扫描**
- 用 `cronjob(action='list')` 获取所有任务
- 按 `last_status` 分组（ok / error / null / paused）
- 识别模式：单次故障 vs 系统性故障

**第二步：逐项排查**
- error 任务 → 检查 `script` 路径是否存在
- 手动运行脚本（注意 `no_agent=True` 的脚本运行方式）
- 查看日志文件确认错误详情

**第三步：评级标准**

| 指标 | 甲上（铁军） | 甲下（小恙） | 乙（有伤） | 丙（需整顿） |
|------|:----------:|:----------:|:--------:|:----------:|
| 成功率 | ≥95% | 85-94% | 70-84% | <70% |
| 静默失败数 | 0 | 1-2 | 3-5 | >5 |
| 修复时间 | 当日 | 2日内 | 1周内 | 搁置 |

综合评级优先级：数据面 > 通信面 > 性能面。

---

## 十三、设计哲学

> 记忆系统不是一个存储层，它是一个**生态**。
>
> - 每条记忆应该有自己的生命周期：出生→活跃→衰减→遗忘
> - 每个Skill应该有自己的健康基线：创建→使用→评估→修炼或退役
> - 每次升级应该有防护盾：快照→diff→验证→修复
> - 好的维护系统能自动回答：「什么值得记住」「什么可以忘掉」「什么健康」「什么需要修」
> - 维护应该**零人工介入**，但**人工可审计**
> - 消耗应该**零额外API调用**——规则工程比模型调用更可靠、更便宜、更可预测

---

## 版本记录

**v2.0.0**（2026-05-18）
- 从「记忆卫生」升级为「Agent生态健康维护系统」
- 新增三大支柱架构：记忆/Skill/升级防护
- 新增Skill健康扫描+自动修正+看板
- 新增`is_user_skill()`保护机制
- 新增升级防护盾（快照+diff+检查）
- 新增命令速查表

**v1.0.0**（初始创建）
- 四大组件：Session衰减/自动压缩/遗忘清理/工作记忆/Self Model
- 衰减曲线参数模板
- 规则提取压缩方法
- 自动化维护管线设计
- 监控指标体系
