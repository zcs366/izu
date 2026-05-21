---
title: AI Agent Token经济学
created: 2026-05-20
updated: 2026-05-20
type: concept
tags: [agent, token-economy, cost-analysis, swe-bench, openhands, economics]
sources:
  - arXiv:2604.22750
  - output/极大/ai-agent-token-economy-report.md
confidence: high
---

# AI Agent Token经济学

> **核心命题**: AI Agent的隐形账单——Token消耗结构、成本预测与效率优化。
> **原始论文**: [How Do AI Agents Spend Your Money?](https://arxiv.org/abs/2604.22750) (arXiv:2604.22750, 2026-04)
> **研究团队**: 密歇根大学、斯坦福、MIT、Google DeepMind、微软AI、All Hands AI

---

## 核心数据

| 关键指标 | 数值 | 含义 |
|---------|------|------|
| Agent vs 纯推理 | **1000×** | Agent编码消耗是纯推理的1000倍 |
| 输入:输出Token比 | **154:1** | 每输出1Token，先输入154 |
| 同任务波动 | **最高30×** | 同一问题不同次运行差30倍 |
| 跨模型最大差 | **>150万** | 最省(GPT-5) vs 最费(Kimi-K2) |
| 自预测相关系数 | **r≤0.39** | 模型自己都不知道 |
| 人类预测 | **τ=0.32** | 人更看不准 |

---

## 七大发现

### 1. Agent成本结构极端畸形
Agent编码任务平均成本 $1.857，输入Token主导。原因：多轮交互、长上下文、工具执行结果累积。^[arXiv:2604.22750]

### 2. Token消耗随机性极强
同任务4次运行，最贵是最便宜的2倍，部分高达30倍。事前预测几乎不可能。^[arXiv:2604.22750]

### 3. 多花钱 ≠ 好效果（逆测试时间缩放）
Token消耗越多，解决率反而越低。高消耗本质是"无效绕圈"而非"深度思考"。^[arXiv:2604.22750]

### 4. 模型Token效率差异极大
GPT-5/5.2性价比最高；Kimi-K2最费最差（比GPT-5多花150万+token/任务）。^[arXiv:2604.22750]

### 5. 人类无法预测Agent成本
专家评估难度与实际成本的肯德尔相关系数仅0.32。复杂度的"人维度"与"算力维度"不匹配。^[arXiv:2604.22750]

### 6. 模型自我预测能力差
最好模型的自预测相关系数仅0.39。Claude Sonnet 3.7/4的预测成本甚至超实际成本2倍。^[arXiv:2604.22750]

### 7. 系统性低估
所有模型都低估实际Token消耗，尤其输入Token。即便消耗达百万Token，预估仍极低。^[arXiv:2604.22750]

---

## 消耗阶段解构

| 阶段 | 占比 | 关键活动 | 优化杠杆 |
|------|------|---------|---------|
| 准备 | 9.98% | 任务规划、环境搭建 | 模板化 |
| 探索 | **30.37%** | 代码搜索、根因分析 | **最大空间** |
| 修复 | **33.53%** | 代码编辑、调试迭代 | 减少无效修改 |
| 验证 | 16.59% | 测试、回归 | 缓存 |
| 收尾 | 9.53% | 最终检查 | 有限 |

探索+修复占2/3成本。^[arXiv:2604.22750]

---

## 与ITA的关联

详见极大级评估报告 [output/极大/ai-agent-token-economy-report.md](../output/极大/ai-agent-token-economy-report.md)

核心启示：
- ITA必须内置**成本透明机制**（实时Token统计、预算上限、用户授权）
- **上下文压缩**是第一优先级（154:1的比例倒逼）
- **提前止损逻辑**（无进展探测、替代路径推荐）
- **成本感知的模型选型**（探索用GPT-5省token，修复用Claude 4/4.5深入）
|
|---
|
## 实践对照 —— Anthropic CFO战略（2026）

| Token层面（本篇） | 公司层面（[[anthropic-cfos-strategy]]） |
|------------------|---------------------------------------|
| Agent每输出1Token需吃154个输入 | 算力是核心战略资产，不是可变成本 |
| 多花钱≠好效果，成本达峰后准确率下降 | 降价（杰文斯悖论）反而营收爆发 |
| GPT-5性价比最高，Kimi-K2最费最差 | 三平台（Trainium+TPU+GPU）动态编排 |
| 上下文压缩是第一优先级 | 自研编排层实现跨平台算力互换 |
| 探索+修复占2/3成本 | 财务自动化：周报几小时→30分钟 |

**合成结论**: Token效率问题（微观）与公司战略（宏观）指向同一个方向——**成本透明、动态编排、效率优先**，才是Agent规模化落地的唯一路径。^[output/极大/anthropic-cfo-cone-of-uncertainty-report.md]
|
|---
|
## 相关概念

- [[agent-three-evolution-stages]] — Agent三阶段演进论
- [[swe-bench]] — Agent编码评估基准
- [[openhands-agent-framework]] — Agent编码平台

---

## 引用

```bibtex
@article{bai2026how,
  author    = {Longju Bai and Zhemin Huang and Xingyao Wang and Jiao Sun
               and Rada Mihalcea and Erik Brynjolfsson and Alex Pentland
               and Jiaxin Pei},
  title     = {How Do AI Agents Spend Your Money? Analyzing and Predicting
               Token Consumption in Agentic Coding Tasks},
  journal   = {arXiv:2604.22750},
  year      = {2026}
}
```
