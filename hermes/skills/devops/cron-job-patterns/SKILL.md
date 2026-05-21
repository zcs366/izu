---
name: cron-job-patterns
description: 设计 Hermes Agent 自动化定时任务——纯 prompt 驱动 vs 脚本驱动、工具集配置、多 Agent 流水线编排、常见反模式与陷阱
version: 1.0.0
author: 军师祭酒
tags:
  - cron
  - automation
  - scheduling
  - pipeline
  - regular-tasks
  - hermes
  - cronjob
trigger: "定时任务|cron job|研究编排|pipeline|每小时|每2h|定期|设置定时|cron配置|cron设置|自动调度|编排流水线"
---

# Cron Job 设计模式

> Hermes Agent 的 cron job 系统支持两种运行模式。选择错误会导致脚本永远跑不起来。本技能覆盖何时用哪种模式、如何配置、以及常见陷阱。

## 一、两种运行模式

### 模式 A：Pure Prompt（推荐用于 Agent 工作流）

当 cron job 需要 **Agent 工具**（`delegate_task`、`web_search`、`write_file`、`send_message` 等）时，必须使用此模式。

```
cronjob(action='create',
  name='我的定时任务',
  prompt='详细的流水线指令，使用delegate_task、web_search等工具...',
  schedule='5 * * * *',
  enabled_toolsets=['web', 'file', 'terminal', 'delegation'],
  deliver='origin')
```

**工作原理**：
- 调度器在每个 tick 启动一个 Agent session
- Agent 收到 prompt 作为任务指令
- 可以使用所有配置的 toolsets 中的工具
- 最终 response 自动交付到 `deliver` 指定的目标

**适用场景**：
- 需要调用 `delegate_task` 派生子 Agent
- 需要 `web_search`/`web_extract` 获取外部信息
- 需要 `write_file` 写入结果
- 多步骤推理流水线
- 多 Agent 会商/合议

### 模式 B：Script-only（用于纯数据收集 / 看门狗）

当 cron job 只运行一个脚本，不需要 Agent 推理时使用。

```
cronjob(action='create',
  name='磁盘监控',
  script='disk_watchdog.sh',
  no_agent=True,
  schedule='0 * * * *',
  deliver='origin')
```

**工作原理**：
- `no_agent=True`：完全跳过 LLM，直接运行脚本
- 脚本的 stdout 被直接交付（非空时才发送）
- **脚本不能访问任何 Agent 工具**（`hermes_tools` 是 execute_code 沙箱的，不是系统模块）

**适用场景**：
- 磁盘/内存/GPU 监控阈值报警
- 纯 shell 命令的文件操作
- 不需要推理的路由式任务

### 混合模式 B'：Script → Agent（数据收集 + Agent 处理）

```
cronjob(action='create',
  name='研究编排',
  script='collect_data.py',   # 收集上下文数据
  prompt='处理上述数据的指令...',  # Agent 使用脚本输出作为上下文
  schedule='5 * * * *',
  enabled_toolsets=['web', 'delegation'])
```

**工作原理**：
- 先运行 `script`，其 stdout 被注入 Agent 的上下文中
- 然后 Agent 接收 `prompt` 处理这些上下文
- **脚本仍然不能使用 Agent 工具**——它只是数据采集步骤

---

## 二、🔴 核心陷阱：Standalone 脚本无法使用 Agent 工具

### 致命反模式

```python
# ❌ 下面这行在 standalone Python 脚本中永远跑不起来
from hermes_tools import delegate_task, web_search, write_file
```

`hermes_tools` 模块**只存在于 `execute_code` 沙箱中**，不是操作系统级别的 Python 模块。在 cron job 的 `script` 中、在 `terminal()` 中、在任何 standalone Python 进程中，这个 import 都会报 `ModuleNotFoundError`。

### 正确做法

**Agent 工具调用必须发生在 prompt 中**。脚本的职责只是：
- 收集静态数据
- 生成上下文文本
- 检查文件/状态

然后 prompt 中的 Agent 使用这些上下文 + 自己的工具能力完成任务。

### 案例：双轨道会商流水线修复

**错误设计**：
- `research_orchestrator.py`（524 行 Python 脚本）
- 第 53 行：`from hermes_tools import web_search, write_file, delegate_task, send_message`
- 结果是：cron job 每次触发都报 `ModuleNotFoundError`
- Agent 虽然能绕过错误手动执行 prompt，但每次开头都有一大段红色错误

**正确设计**：
- cron job 去掉 `script` 参数
- 保留 `prompt`（描述完整的 Phase 0→Phase 4 流水线）
- 设置 `enabled_toolsets=['web', 'file', 'terminal', 'delegation']`
- Agent 自然使用 prompt 中的指令 + toolsets 中的工具完成任务
- 无错误、无噪音、正常定时执行

---

## 三、工具集配置（enabled_toolsets）

设置 cron job 时，`enabled_toolsets` 决定 Agent 可用的工具范围。合理限制可减少 token 开销：

| 工具集 | 包含的工具 | 适用场景 |
|--------|-----------|---------|
| `web` | web_search, web_extract, browser_* | 需要联网搜索 |
| `file` | read_file, write_file, search_files, patch | 文件操作 |
| `terminal` | terminal | Shell 命令 |
| `delegation` | delegate_task | 派生子 Agent |
| `search` | session_search | 检索历史会话 |
| `skills` | skill_view, skill_manage, skills_list | 操作技能 |

**常见组合**：
- 三路搜索流水线：`['web', 'file', 'terminal', 'delegation']`
- 每日报告生成：`['web', 'file', 'search', 'terminal']`
- 纯数据处理：`['file', 'terminal']`

---

## 四、配置示例

### 每日研究扫描（纯 prompt + delegation）

```python
cronjob(action='create',
  name='izu前沿实验室·每日猎手扫描',
  skills=['paper-top-digest'],
  prompt='加载paper-top-digest skill → 执行每日论文扫描...',
  schedule='0 9 * * *',
  enabled_toolsets=['web', 'file', 'terminal'],
  deliver='origin')
```

### 每小时会商流水线（多 Agent 编排）

```python
cronjob(action='create',
  name='核战队·三部门定时研究编排·每小时',
  prompt='''
Phase 0: 三路并行搜索（delegate_task 3个子Agent）
Phase 1A: ITA 6轮合议（顺序执行）
Phase 1B: izu 5轮合议（顺序执行）
Phase 2: 核战队终审
Phase 3: 一口吞摘要 + 可证伪预测
Phase 4: 入库 wiki/raw/祝成果/
  ''',
  schedule='5 * * * *',
  enabled_toolsets=['web', 'file', 'terminal', 'delegation'],
  deliver='origin')
```

### 定时升级检查（script + no_agent）

```python
cronjob(action='create',
  name='Hermes升级-预设日期',
  skills=['hermes-upgrade-safety'],
  schedule='once at 2026-05-17 03:00',
  enabled_toolsets=['terminal', 'file'])
```

## 五、锁文件 + 三重门模式（Claude Code autoDream 模式）

> **来源**：Claude Code v2.1.88 泄露源码 `src/services/autoDream/autoDream.ts`
> **文件**：`/mnt/i/hermes/izu/morning_consolidation.py`（移植实现）

### 5.1 设计要点

对于需要"有状态"的定时任务（如记忆 consolidation），不能用简单的定时触发——需要三重门控：

```python
# Gate 顺序按计算成本排列——最便宜的检查最先做
def should_consolidate():
    # Gate 1: 时间门（最便宜，一次 stat 系统调用）
    if hours_since_last_check < MIN_HOURS:
        return False

    # Gate 2: 会话门（中等成本，查 session 数）
    if new_sessions_since_last_check < MIN_SESSIONS:
        return False

    # Gate 3: 锁文件门（最贵，IO+进程检查）
    if not acquire_lock():
        return False  # 另一进程已在运行

    return True
```

### 5.2 锁文件设计（双用途）

```python
# 锁文件路径: ~/.hermes/consolidation.lock
# mtime = 最后执行时间（双用途！既是锁，也是状态存储）
# body  = 持有者 PID（PID 重用防护）
# 过期时间 = 1 小时（超过此时间即使 PID 还存在也视为过期）

def acquire_consolidation_lock() -> bool:
    lock_path = CONFIG["LOCK_FILE"]
    if lock_path.exists():
        pid = int(lock_path.read_text().strip())
        if is_pid_alive(pid):
            return False      # 真正的锁
        # PID 已死 → 锁过期，允许接替
    lock_path.write_text(str(os.getpid()))
    os.utime(lock_path, None)  # 更新 mtime
    return True
```

**为什么用锁文件而不是内存锁**：cron job 在不同 ticks 中运行，不是同一个进程。文件锁是跨进程同步的唯一可靠方式。

### 5.3 命令三角

为每个带门控的 cron job 设计三个命令入口：

| 命令 | 用途 | 场景 |
|------|------|------|
| `script.py` | 走三重门（cron 默认） | 正常调度 |
| `script.py --force` | 跳过门控（等价 `/dream`） | 手动触发 |
| `script.py --check` | 只检查门控状态 | 调试/可视化 |

### 5.4 适用场景

- 记忆 consolidation（24h + 5 sessions 门控）
- 磁盘/Token 使用量阈值触发（低于阈值不执行）
- 网络可达性检查（不在线不触发外发任务）
- 批量数据处理（上次跑完了一轮？还不到时候）

**核心原则**：最便宜的检查最先做。脚本做 stat/read/check，Agent 做搜索/写文件/delegate_task。

---

## 六、验证方法

创建 cron job 后，用以下步骤验证：

```python
# 1. 检查 job 是否配置正确
cronjob(action='list')  # 确认 job_id、schedule、enabled、script/prompt

# 2. 立即触发一次手动运行
cronjob(action='run', job_id='xxx')

# 3. 等待交付（deliver='origin' 将结果送回当前会话）
# 检查输出：是否有 Script Error 报头？
# 如果 no_agent=True 的脚本：exit_code 是否为 0？
```
