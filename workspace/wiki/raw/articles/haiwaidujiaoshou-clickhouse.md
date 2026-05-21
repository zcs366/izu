---
source_url: https://www.36kr.com/p/3808336062177029
sha256: ceaf15621d264cb83cb9c8d49522b3ea9cd2cfcb56a34c0ee8a10c04456cbf27
ingested: 2026-05-21
title: "AI Labs 都在用，ClickHouse 能成为AI 日志的实时分析引擎吗？"
author: 海外独角兽
source: 微信公众号
---

# ClickHouse 深度拆解

## 核心数据

- **ARR**：2024年中 ~$15M → 2025年末 ~$160M（18个月10x增长）
- **融资**：2026年1月 D轮 $400M，估值 $15B（94x ARR）
- **付费云客户**：~1000 → 3000+（3x）

## 三大产品线

1. **ClickHouse Cloud**：核心OLAP引擎，比Snowflake便宜~88%，毫秒级返回
2. **ClickStack**：统一可观测性平台（OTel + ClickHouse + HyperDX），成本约Datadog 30-50%
3. **Langfuse**：AI可观测性/LLM工程平台（2026.1收购，MIT开源），2000+付费客户

## AI受益逻辑

- LLM推理日志是append-only事件流+高基数列扫描，完美匹配ClickHouse workload
- 顶级客户：Anthropic（PB/天日志）、OpenAI（部分迁离Datadog）
- Agentic Data Stack：内部工具DWAINE已服务250+用户，日均200+查询

## 反方观点

- 无AI/ML能力，只存储查询
- Anthropic为air-gapped私有化部署，OpenAI自行运维不付费
- 护城河正被SingleStore、StarTree复制

## 关键判断

> 性能+成本优势在AI时代突出，平台化故事最完整（仅次于Databricks）。BYOC全面GA和ClickStack GTM执行是估值天花板关键。

**对张成市的价值**：ClickHouse是AI Infra核心受益标的，其从OLAP→可观测性→AI可观测性的TAM扩张路径值得借鉴。94x ARR估值反映了市场对AI数据基础设施的极高预期。
