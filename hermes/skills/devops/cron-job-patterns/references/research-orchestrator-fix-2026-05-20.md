# Research Orchestrator 修复实录 (2026-05-20)

## 问题

cron job `556042150b72`（核战队·三部门定时研究编排·每小时）使用 `research_orchestrator.py` 作为 `script`。脚本第 53 行：

```python
from hermes_tools import web_search, write_file, delegate_task, send_message
```

每次触发都报 `ModuleNotFoundError: No module named 'hermes_tools'`。

## 根因

`hermes_tools` 模块**只存在于 Hermes `execute_code` 沙箱内**，不是系统级 Python 包。任何 standalone Python 进程（包括 cron job 的 `script`）都无法 import 它。

## 修复

1. 从 cron job 中去掉 `script` 参数
2. 保留 `prompt`（原 prompt 已经描述了完整的流水线）
3. cron job 成为纯 prompt 驱动
4. 死掉的 `research_orchestrator.py`（524 行）被删除
5. 架构文档转为 `research-orchestrator-arch.md` 保留

## 教训

- 不要在 standalone 脚本中写 `from hermes_tools import ...`——它永远跑不起来
- 需要 Agent 工具的 cron job 必须用 prompt 驱动
- `script` 参数只适合纯数据收集（无 Agent 工具调用）
- 如果 prompt 本身就覆盖了完整流程，脚本就是多余的死代码
