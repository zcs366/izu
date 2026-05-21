# ReVeal进化引擎：izu定制化设计

> 基于 ReVeal (arxiv 2506.11442, ICLR 2026) 的验证驱动进化框架
> 匠石原则约束：能用代码就别用模型——验证环节代码化，模型只做语义生成

---

## 一、ReVeal核心机制提炼

### 1.1 训练循环（简化为izu可实现的推理时扩展）

```
原始ReVeal训练（需要RL训练基础设施，暂不实现）：
  for episode in training:
    Agent生成代码 → Agent生成测试用例 → 工具执行测试 → 
    奖励信号（通过/失败 + 覆盖率） → TAPO信用分配 → 策略更新

izu版本（推理时扩展，零训练成本）：
  for task in tasks:
    Agent生成输出 → 验证Agent生成评估用例 → 
    代码执行验证（匠石原则：代码做） → 评分写入performance_history →
    触发规则：如果连续N次低分 → 微调提示策略
```

### 1.2 TAPO算法理解

Turn-level Advantage with Preference Optimization：
- 把长程推理分解为逐轮次的"生成→验证"对
- 每轮分配信用：这轮做得更好还是更差？
- 偏好优化：好的轮次 → 正信号，差的 → 负信号

**izu简化版**（不训练模型，改提示策略）：
- 任务分解为步骤级"生成→验证"对
- 每个步骤结束后评分（代码验证）
- 连续低分步骤 → 该Agent在该步骤类型上存在短板 → 记录到weaknesses
- 下次同类任务 → 在提示中注入"上次在这步出过问题，注意XX"

### 1.3 关键洞察

ReVeal的核心不是"训练更强的模型"，而是：
1. **验证信号要可靠** → 代码执行（出错就是出错，不依赖模型判断）
2. **信用分配到轮次** → 知道哪步出问题比知道整体出问题更有用
3. **协同进化** → 生成和验证同步提升，验证越好生成越可靠

---

## 二、izu进化引擎架构

```
┌─────────────────────────────────────────────────────────┐
│                    izu进化引擎 v0.1                      │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌──────────────────┐ │
│  │ 生成Agent  │───▶│ 验证Agent  │───▶│ 代码执行器       │ │
│  │ (模型)     │    │ (生成用例) │    │ (实际运行验证)    │ │
│  └───────────┘    └───────────┘    └───────┬──────────┘ │
│       ▲                                    │            │
│       │           ┌───────────┐            │            │
│       └───────────│ 提示微调器 │◀───────────┘            │
│                   │ (记录短板) │   评分反馈              │
│                   └───────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### 组件说明

| 组件 | 用什么做 | 匠石原则依据 |
|------|---------|------------|
| 生成Agent | LLM | 语义生成，代码做不了 |
| 验证Agent | LLM生成评估用例 | 设计测试用例需要语义理解 |
| 代码执行器 | Python/Shell | 确定性的，验证"引用是否有效"、"URL是否可达"、"输出是否合格式" |
| 评分器 | 代码公式 | 加权计算各维度分数，不依赖模型判断 |
| 提示微调器 | 代码+模板 | 根据评分结果，从模板库选择改进提示注入 |
| 短板记录 | 代码（JSON写入） | 持久化Agent能力演变 |

---

## 三、评分维度（代码化）

```python
SCORING_DIMENSIONS = {
    "factual_accuracy": {
        "weight": 0.35,
        "method": "code",  # URL存活检查、引用匹配
        "description": "事实准确率"
    },
    "structural_completeness": {
        "weight": 0.25,
        "method": "code",  # 检查输出是否包含所有要求的章节
        "description": "结构完整性"
    },
    "consistency": {
        "weight": 0.20,
        "method": "code",  # 自洽性检查（是否有自相矛盾）
        "description": "内部一致性"
    },
    "conciseness": {
        "weight": 0.10,
        "method": "code",  # token数/信息密度比
        "description": "简洁度"
    },
    "semantic_quality": {
        "weight": 0.10,
        "method": "model",  # 仅此项需要模型判断
        "description": "语义质量"
    }
}
```

**模型只做10%的评分工作。**

---

## 四、进化触发与策略

### 4.1 触发条件（代码判断）

```python
def should_evolve(agent_id, interaction_record):
    # 条件1：连续3次任务quality_score低于阈值
    recent = get_recent_scores(agent_id, n=3)
    if all(s < EVOLVE_THRESHOLD for s in recent):
        return True, "consecutive_low"
    
    # 条件2：某个维度连续低于0.5
    dim_scores = get_dimension_scores(agent_id, n=5)
    for dim, scores in dim_scores.items():
        if np.mean(scores) < 0.5:
            return True, f"dim_weak:{dim}"
    
    # 条件3：探索触发（每10次任务随机探索一次）
    if random.random() < EXPLORATION_RATE:
        return True, "exploration"
    
    return False, None
```

### 4.2 进化策略（提示微调，不训练模型）

| 触发原因 | 策略 | 实现 |
|---------|------|------|
| 连续低分 | 注入自检提示："请特别注意XX，上次同类任务在这里出错" | 模板注入 |
| 某维度弱 | 针对性提示："本次任务请优先保证引用准确，引用前验证URL" | 维度模板 |
| 探索 | 尝试新的提示排列（如调整Agent角色描述、增加约束） | A/B测试 |

---

## 五、与Agent关系拓扑的联动

进化引擎和关系拓扑是两个子系统，但需要共享数据：

| 数据 | 进化引擎写入 | 关系拓扑读取 | 作用 |
|------|-----------|-----------|------|
| performance_history | ✅ | ✅ | 影响Agent任务分配权重 |
| identified_weaknesses | ✅ | ✅ | 避免将短板Agent分配到不合适的任务 |
| prompt_adjustments | ✅ | ❌ | 仅进化引擎内部使用 |
| interaction_log | ✅ | ✅ | 关系拓扑计算Agent间协作效率 |

**数据流**：进化引擎是数据生产者，关系拓扑是数据消费者。

---

## 六、MVP实现范围

### 第一版（1周内）

- [ ] 代码验证器：URL存活检查、输出结构检查、引用完整性
- [ ] 评分器：5维度加权评分（90%代码化）
- [ ] 短板记录：每次任务结束后自动更新Agent的weaknesses字段
- [ ] 简单提示微调：连续3次低分 → 注入"注意XX"模板

### 不做的事

- ❌ 不做RL训练（需要GPU+大规模数据）
- ❌ 不做模型参数修改（只改提示策略）
- ❌ 不做自动A/B测试框架（手动观察）

---

## 七、下一步行动

1. 阅读ReVeal论文全文（特别是TAPO算法细节，第4-5节）
2. 实现代码验证器（URL检查+结构检查）
3. 在izu下一次实际任务中试运行评分模块
4. 收集3-5次任务数据后评估进化效果
