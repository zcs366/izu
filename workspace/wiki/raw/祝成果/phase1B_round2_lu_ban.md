# Phase 1B — izu 5轮合议

## Round 2: 鲁班（工程可行）

### 最小可行产品（MVP）工程计划

**MVP定义**：Agent可靠性评估工具包（Layer 1）
- 输入：Agent在测试任务上的执行日志（JSONL格式）
- 输出：4维12指标报告 + 失败模式分类

**技术栈选型**：

| 组件 | 选型 | 理由 |
|------|------|------|
| 核心语言 | Python 3.12 | ML生态最佳集成 |
| 评估引擎 | 纯Python实现 | 无额外依赖，可在任何CI环境中运行 |
| 任务框架 | pytest衍生 | 工程师最熟悉，降低采纳门槛 |
| 报告生成 | HTML+JS（Plotly） | 交互式可视化，无需后端 |
| 测试集格式化 | JSON Schema | 灵活的输入格式，易集成 |
| 分发 | PyPI + Docker | 即装即用 |

### 架构设计

```
agent-eval/
├── core/                   # 核心评估引擎
│   ├── consistency.py      # 一致性评估
│   ├── robustness.py       # 鲁棒性评估  
│   ├── predictability.py   # 可预测性评估
│   └── safety.py           # 安全性评估
├── metrics/                # 12个指标的实现
│   ├── variability.py      # 变异系数
│   ├── stability.py        # 稳定性指数
│   ├── calibration.py      # 校准度
│   └── ... (共12个)
├── collectors/             # 数据收集适配器
│   ├── langchain.py        # LangChain集成
│   ├── openai.py           # OpenAI API适配
│   └── generic.py          # 通用JSONL输入
├── reporters/              # 报告生成
│   ├── html_reporter.py    # HTML可视化报告
│   ├── json_reporter.py    # 机器可读输出
│   └── slack_reporter.py   # Slack集成
└── cli.py                  # 命令行入口
```

### 开发工作量估算

**Phase 1 — 核心引擎（3周，1人）**
- Week 1: 评估框架 + 一致性指标（~800行代码）
- Week 2: 鲁棒性+可预测性指标（~600行）
- Week 3: 安全性指标 + 基础报告（~500行）

**Phase 2 — 集成层（2周，1人）**
- LangChain/LlamaIndex集成（~300行）
- OpenAI API/Claude API适配器（~200行）
- 通用JSONL解析器（~150行）

**Phase 3 — 工具完善（2周，1人）**
- HTML交互式报告（~500行JS+CSS）
- Docker镜像 + CI集成示例
- 文档（README + 5个教程）

**总计**：7周，单人可完成

### 关键技术挑战

**挑战1：指标的定义一致性**
- 同个指标在不同Agent类型上含义不同（例：编码Agent的"一致性"是输出代码完全相同还是语义相同？）
- **解决方案**：插件化的对比器（comparator），允许用户自定义"相等性"的定义

**挑战2：鲁棒性评估的扰动自然性**
- 输入扰动需要保持自然语义（例如"将查询改写而不改变意图"）
- **解决方案**：内置LLM辅助的扰动生成器（可选调用，非必需）

**挑战3：安全性评估的覆盖面**
- 越狱手段日新月异，静态列表不够
- **解决方案**：集成安全基准测试集（如SafetyBench）+ 可扩展的测试注入接口

### 部署架构

```
[开发环境]                 [CI/CD]                   [生产环境]
  pytest集成 ←────────── GitHub Actions ──────────→ 定期评估报告
     │                      │                            │
     └── agent-eval ────────┘                        Slack/Datadog
     (本地运行)                                      告警通知
```

零基础设施依赖：所有计算在CI runner上完成，报告作为CI artifact存储

### 成本估算

**开发成本**（7周单人全职）：$14,000-21,000（按$2k-3k/周）
**运行成本**（评估时的LLM API调用）：
- 每次评估~$5-20（依Agent任务复杂度而定）
- 假设每周每Agent评估2次，10个Agent → $100-400/周
- 年度运行成本：$5,000-20,000

**对比**：一个Agent生产事故的平均损失 ~$50,000-500,000 → ROI极其明确
