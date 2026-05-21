# Claude Code 移植模块：izu 工具库（2026-05-20）

> 基于 Claude Code v2.1.88 泄露源码的三个设计模式移植。
> 全部位于 `/mnt/i/hermes/izu/`。

## 模块一览

| 模块 | 文件 | Claude Code 来源 | 用途 |
|------|------|-----------------|------|
| Circuit Breaker | `circuit_breaker.py` | 断路器集（Auto-Compact/YOLO/Max-Output） | 子Agent稳定性保护 |
| Task Coordinator | `task_coordinator.py` | Coordinator模式 + Agent Swarm 6种类型 | 任务类型分流 + 结构化结论 |
| Compression Pipeline | `compression_pipeline.py` | 4层压缩（Snip→Micro→Collapse→Summary） | 会话压缩 + 9段式摘要 |

## 与 memory consolidation 的关系

三模块在 morning_consolidation cron job（每天5:30）中按以下顺序配合：

```text
Circuit Breaker 初始化（防无限重试）
  → Task Coordinator 委派 consolidate 子任务
    → Compression Pipeline 执行消息压缩
      → Circuit Breaker 报告状态
```

## 关键设计决策

1. **零LLM成本**：所有模块基于规则/字符串处理，不调模型
2. **中文+英文双关键词**：task_coordinator 的判断函数同时支持中英
3. **从便宜到贵**：compression_pipeline 的 Snip($0)→Microcompact($0)→Collapse(~$0)→Summary(规则) 遵循Claude Code的成本感知原则
