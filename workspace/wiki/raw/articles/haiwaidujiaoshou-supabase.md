---
source_url: https://www.woshipm.com/ai/6397694.html
sha256: 5f47b87a4adb566bdc070906e1868139215014890459b91085991aceab85404a
ingested: 2026-05-21
title: "Supabase：百亿美元估值，vibe coding 的默认后端？"
author: 海外独角兽
source: 微信公众号
---

# Supabase 深度拆解

## 核心数据

- **估值**：接近完成GIC领投的5亿美元F轮融资，估值100亿美元
- **用户**：截至2026年Q1累计突破700万（16个月7x增长）
- **定位**：PostgreSQL为核心的一站式后端服务（Auth/Storage/Edge Functions/Vector）

## 两条AI时代大势的交叉

1. **Postgres作为AI的心智语言**：其文档、Stack Overflow数据、GitHub代码成为模型预训练数据
2. **Coding Agent作为AI需求的最大爆发点**：Anthropic ARR从$90亿跳至$300亿级别

> "coding agent 实现了，AGI 的 90% 就实现了。"

## Agent-First 产品布局

- **agent-skills仓库 & MCP server**：18+ coding agent原生集成
- **PGlite**：3MB WASM Postgres，浏览器/Node内亚秒级冷启动，本地零云成本
- **BKND / Supabase Lite**：面向agent的"最小可发布项目"

## 技术收购

- **OrioleDB**（2024.04）：替代存储引擎，只读>4x、读写>4.5x、TPC-C >5.5x提升
- **Multigres**（2025.06）：水平扩展，解锁enterprise-scale workload
- **Hydra/pg_duckdb**（2025.12）：DuckDB在Postgres内部运行，打通OLAP

## 增长驱动

- 65%的YC公司是Supabase客户
- Vibe Coding平台（Lovable/v0/Bolt）将Supabase作为默认backend内置
- Agent自动推荐（Claude Code/Codex/Cursor）零获客成本

## 风险

- AI快速发展可能削弱distribution moat
- Enterprise就绪度~75%，缺SCIM/Managed BYOC/PCI DSS
- Neon（被Databricks收购）是直接竞争者

**核心观点**：Supabase站在Postgres心智语言×Coding Agent爆发的交叉点上，"给agent更好的Postgres capability"取代"给人类更好的开发体验"成为新路线图。

**对张成市的价值**：Supabase是vibe coding时代基础设施的核心标的。理解BaaS如何从服务人类开发者转向服务Agent，对判断AI应用层基础设施投资方向极有价值。
