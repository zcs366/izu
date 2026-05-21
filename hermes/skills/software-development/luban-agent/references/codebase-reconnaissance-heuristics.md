# 代码库侦察实用技巧

从本会话（2026-05-15 审计韩信Loop合约方案）中提炼的Heuristics。

## 一、先查数据再说理

审计方案之前，先看实际数据长什么样——**数据胜过推理**。

### 技巧1：直接读持久化文件

```python
# 替代"推断数据结构"→直接读
cd ~/.hermes && python3 -c "
import json
with open('cron/jobs.json') as f:
    data = json.load(f)
jobs = data['jobs']
print(f'Total: {len(jobs)}')
print(f'Active: {len([j for j in jobs if j.get(\"enabled\", True)])}')
"
```

**为什么：** 方案可能说"35个活跃cron"，但你能看到的是34个active/1个paused、每个job的实际schedule类型、script/context_from/skills分布。这些决定了"安全网"的真实影响范围。

### 技巧2：用search_files搜关键模式

```python
# 高效搜索——不要读整个文件
search_files(pattern="max_attempts", path="cron/")
# → 0 matches，确认"系统中不存在"
search_files(pattern="pause_on_fail", path="cron/")
# → 0 matches，确认"自动暂停逻辑不存在"
```

**注意：** `search_files`的参数要限制path到相关目录（cron/、tools/），否则全仓搜索太慢。可以同时搜多个级别——先确定文件在哪里，再确定模式是否存在。

### 技巧3：验证关键断言（"现有X支持Y"）

方案说"现有cron系统支持context_from链式注入"→验证：

```python
search_files(pattern="context_from", path="cron/scheduler.py")
# → 找到注入代码，确认支持
# → 读那几行，看实现方式（注入格式、截断长度、失败处理）
```

方案说"现有系统已有max_attempts"→验证：

```python
search_files(pattern="max_attempts|max_retry|failure_count", path="cron/")
# → 0 match → 这是结论，不是观点
```

### 技巧4：了解系统边界（不只看功能，看怎么用的）

查数据分布不仅查"有什么job"，还要查：

- **no_agent vs LLM比例**（no_agent的不要安全网，纯脚本job不需要fail上限）
- **context_from链**（链式依赖的job需要等待上游逻辑）
- **schedule密度**（每分钟跑的vs每天跑的，安全网阈值不同）

### 技巧5：读源码的"关键三处"

1. **入口函数**（cronjob()的action分发）—— 理解API能力
2. **存储读写**（mark_job_run/load_jobs）—— 理解持久化字段
3. **执行循环**（run_job/tick）—— 理解失败处理路径

这三处读完，基本覆盖了"方案中提到的功能是否存在"的验证需求。

## 二、真实数据 = 审计基础

本会话发现的真实分布（从jobs.json直接读取）：

| 指标 | 值 |
|------|-----|
| 总job数 | 35 |
| 活跃job数 | 34 |
| no_agent job | 1（wiki-dropbox） |
| LLM agent job | 33（所有带prompt/skills的） |
| 使用context_from | 0 |
| 使用script | 2（wiki-dropbox、祝成果入库） |
| 使用skills | ~15个（paper-top-digest、bing-search等） |

这个分布直接决定了安全网的设计——34个活跃LLM job每个都可能失败，max_attempts默认值要覆盖最坏的场景（33个LLM job中任何一个可能在半夜API down时连续失败）。

## 三、关于"确认不存在"的方法论

当你需要确认"某个功能是否存在"时：

1. 第一步：`search_files(pattern=<功能名>)` → 0 match = 不存在
2. 但是要小心——功能可能**不在搜索关键词下**。比如"自动暂停"可能不叫`pause_on_fail`而叫`auto_disable`或`max_attempts`。
3. **多重关键词搜索：** 同语义的多个词都搜一遍（`max_attempts` | `failure_count` | `auto_pause` | `auto_disable`）
4. **看周围的逻辑：** 搜`mark_job_run`——它处理的是单次运行的状态更新，没有聚合失败计数的逻辑。如果有累计机制，一定在这里附近。
5. **最终确认：** 读那部分的全部源码。`mark_job_run`的完整实现（~50行）读一遍就确定没有累计逻辑。

**结论：** 搜不到 + 读了相关逻辑的实现 = "系统中不存在"是事实，不是推理错误。
