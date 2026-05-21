# MCP 编排模式 (MCP in the Wild 论文)

## 五种组合模式分类法

| 模式 | 原理 | 使用场景 | 实现 |
|------|------|---------|------|
| P1 Sequential Pipeline | A输出→LLM→B输入 | 链式处理 | `orch.sequential_pipeline([...])` |
| P2 Parallel Fan-Out | 同查询→多服务器并发 | 信息并行采集 | `orch.parallel_fanout(query, [(server,tool)])` |
| P3 Cross-Reference | 多源三角测绘验证 | 可信度增强 | `orch.cross_reference(claim, server_specs)` |
| P4 Iterative Refinement | 跨源迭代→收敛 | 信息质量递进 | `orch.iterative_refine(query, tools, max_iter=5)` |
| P5 Domain Bridging | 跨领域意外发现 | 知识孤岛连接 | 尚未实现 |

## 失败分类法 (F1-F5)
- F1: 上下文衰减 → 检测信息熵变化
- F2: 伪三角测绘 → 追溯源独立性
- F3: 反馈回路振荡 → 硬限制迭代+信息增益门限
- F4: 领域幻觉 → 强制来源引用
- F5: 编排死锁 → 超时+依赖图分析

## 设计原则 (DP1-DP5)
1. 来源多样性优先
2. 组合前验证可用性
3. 模式匹配任务拓扑
4. 编排层管理失败
5. 输出必须降低熵

## Hermes Agent 内置编排工具（已实现）

自 2026-05-20 起，Hermes Agent 的 `tools/mcp_gateway.py` 提供 4 个注册在 `hermes-core` 工具集的编排工具，由 `discover_builtin_tools()` 自动发现，无需额外配置：

| 工具名 | 对应模式 | 能力 |
|--------|---------|------|
| `mcp_orch_sequential` | P1 Sequential Pipeline | 步骤链式执行。支持 `{{capture_as.field}}` 占位符跨步骤传参，fail_fast 控制。通过 `handle_function_call()` 调用已注册工具。 |
| `mcp_orch_parallel` | P2 Parallel Fan-Out | `ThreadPoolExecutor` 并发调用。结果 keyed by tool name，不可用工具隔离报告不影响可用工具。 |
| `mcp_orch_crossref` | P3 Cross-Reference | 多源三角测绘验证。并发查询各 source，分析证据存在性，返回逐源 verdict + 总体置信度 (0.0-0.9)。支持 min_confirmations 阈值。 |
| `mcp_orch_iterate` | P4 Iterative Refinement | 渐进查询 + 信息增益收敛控制。`{{query}}` 占位符动态替换，检测增益低于 min_gain(默认0.15) 或达 max_iterations(默认5) 时收敛。 |

**尚未实现：** P5 Domain Bridging, F1-F5 失败处理。

**实现规约：**
- handler 签名 `fn(args: dict, **kwargs) -> str`，返回 JSON 字符串
- 通过 `handle_function_call()` 调用已注册 MCP 工具，完整经过 pre_tool_call / circuit breaker / error-recovery 钩子链
- 自动过滤不可用工具（check_fn 失败），不阻塞可用工具执行
- `**kwargs` 必须保留（registry.dispatch 可能注入 task_id, user_task 等额外参数）
- ThreadPoolExecutor 并发上限 10 workers，避免过载 MCP 事件循环

**文件路径：** `tools/mcp_gateway.py`（Hermes Agent 源码树中）

**参考实现原型（历史）：** `ita/mcp_pipeline_wrapper.py`（四种模式全通，含 mock 演示）
