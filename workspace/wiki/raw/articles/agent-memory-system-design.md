---
source_url: https://mp.weixin.qq.com/s/fGlOQqpeNVeXvDlgHJPaKw
sha256: 9db68da851a1ced92b1afd1a4b00d5201f94ad713ee106dcac6e4a762eda6879
ingested: 2026-05-19
title: Agent 记忆系统设计：四种类型、三大策略、完整代码实现
author: 未知（公众号转载）
source: 微信公众号
eval_level: 极大
tags: [Agent Memory, 记忆系统, ChromaDB, Episodic Memory, ITA]
---

# Agent 记忆系统设计

## 四种记忆类型
1. 上下文记忆（In-context Memory）：工作台，system prompt+对话历史+检索结果
2. 外部记忆（External Memory）：结构化（SQLite/PostgreSQL）+向量（Chroma/Pinecone）
3. 情景记忆（Episodic Memory）：事件日志，任务结果+反思
4. 语义/参数记忆（Semantic/Parametric Memory）：模型权重中的通识

## 核心设计原则
- 记忆操作包裹LLM调用：先检索→再调用→后写入
- 检索是瓶颈：检索不到正确的记忆，Agent就当那些记忆不存在
- 三种遗忘策略：摘要、选择性保留、卸载到外部记忆

## 关键代码
- MemoryStore类（ChromaDB + OpenAI Embeddings）：remember/recall/forget
- EpisodicLogger类：结构化事件日志，含task/approach/outcome/duration/token_cost/quality_score
- Memory-Augmented Agent：retrieve→build prompt→call LLM→write memory

