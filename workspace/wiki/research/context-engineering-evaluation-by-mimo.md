---
title: "Agent上下文工程三大方案对比评估（MiMo V2.5 Pro产出）"
aliases: ["上下文工程评估", "Claude Code OpenClaw Hermes上下文对比"]
author: "MiMo V2.5 Pro (通过子代理)"
source_article: "raw/articles/context-engineering-three-agents-2026-05-20.md"
created: "2026-05-20"
updated: "2026-05-20"
tags: [上下文工程, Claude Code, OpenClaw, Hermes, context compression, 评估]
sources:
  - raw/articles/context-engineering-three-agents-2026-05-20.md
  - https://arxiv.org/abs/2604.14228
---

# 深度评估：三大Agent上下文工程方案对比

> 由 MiMo V2.5 Pro 评估产出 | 2026-05-20

---

**一句话核心判断**：这是一篇合格的科普级综述，方向选对了，但深度不足、原创贡献有限，且对Hermes的内部机制描述流于表面，核心工程权衡未触及。对已有agent开发经验的团队只能提供概念框架层面的参考价值。

---

## 1. 核心贡献：概念引入大于技术突破

> 最大的价值是让更多人意识到上下文管理是agent系统的第一性问题。

文章正确指出了5个核心痛点：窗口上限、长上下文退化、成本延迟、会话丢失、工具噪音。LangChain四维框架（Write/Select/Compress/Isolate）是不错的思维模型，但并非原创。

**问题**：缺乏token成本实测数据、缺乏不同压缩策略在真实任务上的效果对比。对Hermes用户来说，读源码30分钟收获更大。

---

## 2. Claude Code的5层压缩：可信，但不是官方披露

> 源于VILA Lab对Claude Code公开TypeScript源码的逆向分析（arXiv:2604.14228），有代码级依据。

5层架构：budget reduction → snipping → micro-compaction → context collapse → auto restore。

**关键遗漏**：
- 第5层「压缩后自动恢复工作集」是Claude Code最精妙的设计——把压缩从「毁灭性操作」变成「可逆状态转移」，文章只提了没深挖
- 没有讨论Claude Code compaction API的trade-off：低配置复杂度 vs 零可定制性

> **对izu/Hermes的启示**：Claude Code的auto restore设计值得直接抄——Hermes目前压缩后只有摘要，没有工作集还原机制，这是最大的可改进空间。

---

## 3. Hermes vs Claude Code vs OpenClaw：对比公允，但对Hermes的理解浮于表面

> 三个定位完全不同的产品放在一起对比有科普价值，但本质上是苹果、橙子和香蕉比较甜度。

### 公允之处
- 定位准确：Claude Code封闭不可定制、OpenClaw开放框架、Hermes中间态

### Hermes部分的问题

**阈值设计没讲透**：50%（Agent层）和85%（Gateway层）不是拍脑袋的——当两阈值相同时，每轮都会触发压缩导致Gateway反而变瓶颈。这个是踩坑迭代出来的，文章错失了展示engineering决策的最佳素材。

**漏掉了关键设计**：
- 增量更新怎么工作的——这是Hermes相比Claude Code粗暴全文摘要的最大亮点
- 插件式ContextEngine架构——和OpenClaw「可替换引擎」高度一致
- protect_last_n保护尾巴（默认20条）——实践中比阈值更重要

**结构化交接文档的隐含假设**：这是用Claude-4级别模型的摘要质量保证的，换弱模型可能变废话合集。文章没说。

---

## 4. 对izu/Hermes系统的直接价值

> 能帮你列改进清单，但不能帮你做优先级。

### 直接抄（P0）
1. **压缩后工作集恢复**：Hermes目前缺失的核心能力。压缩后保留活跃文件/工具列表，下次自动预加载
2. **增量摘要的上限感知**：摘要本身设token预算（如500 tokens），超限从零重新总结

### 小心谨慎（P1）
3. **Gateway层字符级token估算误差**：大消息时误差大，需兜底逻辑
4. **85%阈值过于保守**：若Agent层压缩从未触发，Gateway可能来不及兜底

### 自家验证（P2）
5. **结构化交接格式优化**：对debugging/coding/research不同任务类型验证哪种格式信息密度最高

---

## 5. 局限与遗漏

> 文章的最大问题不是说了什么，而是没说什么。

- **压缩精度退化**：没有任何压缩是无损的，完全没讨论每次压缩损失了多少信息
- **压缩本身的token成本**：压缩调用LLM也要消耗token，如果频繁触发可能压缩成本>节省成本
- **模型依赖**：弱模型的摘要能力断崖下跌，Hermes整个压缩设计隐含假设Claude-4级别质量
- **多会话/多Agent场景**：文章只讨论了单Agent单会话

---

## 6. 行动建议

| 优先级 | 任务 | 预期效果 |
|--------|------|----------|
| 🔴 P0 | 实现压缩后工作集恢复 | 消除「压缩后失忆」痛点 |
| 🔴 P0 | 增量摘要设token上限（如500） | 防止摘要膨胀退化 |
| 🔴 P0 | 增加压缩损失的透明度日志 | 方便判断压缩必要性 |
| 🟡 P1 | Gateway层阈值自适应 | 避免过度/不足压缩 |
| 🟡 P1 | 弱模型降级压缩策略 | 保证兼容性 |
| 🟢 P2 | 可插拔压缩策略/持久化记忆对接 | 长期工程 |

---

## 结论

这篇文章是**合格的入门读物**，不是**深入的技术分析**。乏数据、缺乏深度实现细节、缺乏对工程成本的讨论。对于izu团队这样的agent系统实际构建者，只能作为灵感起点，不能作为技术决策依据。

**Hermes的用户应该直接从源码读`context_compressor.py`和`gateway/run.py`，花30分钟比读这篇文章收获更大。**

---

*报告生成时间：2026-05-20 | 由 MiMo V2.5 Pro 评估产出 | 参考 arXiv:2604.14228 (VILA Lab逆向分析)*
