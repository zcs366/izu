# GraphRAG 假引文问题深度预研

> 为 izu-wiki GraphRAG W1/W2 关键路径提供方案选型依据。W2 schema 设计依赖此输出。
> 日期：2026-05-16 | 状态：初稿 | 作者：Hermes Agent

---

## 问题定义

GraphRAG 生成的回答中，引文（citation）指向的知识图谱三元组或源文档与回答内容不匹配——要么引用的实体/关系不存在于检索子图中，要么引用存在但推理路径不成立。本质是**检索召回偏差 + LLM 结构化理解失效 + 生成环节的归因错位**三者叠加。

---

## 已知原因

| # | 原因 | 说明 |
|---|------|------|
| 1 | **图结构噪声** | LLM 自动构建的 KG 含冗余实体、不可靠关系——DEG-RAG 发现可压缩 ~40% 规模（ICLR 2026） |
| 2 | **浅层检索（Shallow Retrieval）** | 单轮检索只走一跳，多跳关系（→Springfield→State Capital→Illinois）被截断 |
| 3 | **线性化信息损失** | 三元组序列化破坏图拓扑，Transformer 缺乏对关系结构的归纳偏置（arXiv:2512.09148） |
| 4 | **注意力路径过拟合** | LLM 过度依赖短路径三元组（Path Reliance Degree 过高），忽略长程证据 |
| 5 | **向量检索召回偏差** | 语义相似度命中非相关内容，top-k 截断丢失关键证据（RAG-KG-IL, 2025） |
| 6 | **LLM 参数知识干扰** | 模型用预训练记忆覆盖检索结果——FACTUM 证明：参数记忆贡献过强是引文幻觉的关键机制 |
| 7 | **KG 三元组与文本矛盾** | 检索到的三元组与源文本 chunk 冲突时，检测方案 MCC 下降 44-84%（FinBench 2026） |
| 8 | **生成即编造** | 当无相关数据时，向量检索仍返回近似结果，LLM 据此编造引文（MetaRAG 2025） |

---

## 方案对比表

### 方案 A：交叉编码器重排（Cross-Encoder Reranking）

| 维度 | 说明 |
|------|------|
| **原理** | 检索后插入 cross-encoder（如 BGE-reranker-v2-m3）对候选子图/text chunk 做细粒度相关性评分，过滤低分噪声 |
| **适用性** | izu-wiki 中等规模（~1000 页面），cross-encoder 单次推理约 50-100ms |
| **实现难度** | ⭐⭐ 中低——集成到 izu-pipeline 搜寻步骤之间，需新增 rerank 子步骤 |
| **预期效果** | 召回精度 +15~20%，假引文率降低 ~30%（BGE-reranker 在 MultiRAG 基准上 precision 提升 0.069） |
| **成本** | 一次推理 ~2K token，¥0.004/次，可运行本地 SBERT 版本降至零成本 |
| **优点** | 成熟方案、社区工具链完善（HuggingFace + FAISS）、不依赖 LLM 调用 |
| **缺点** | 增加延迟 50-200ms；对图结构噪声（如实体消歧失败）无效；不能解决 LLM 归因错位 |

### 方案 B：LLM 自我校验 + 反问验证（Self-Check & Reverse Verification）

| 维度 | 说明 |
|------|------|
| **原理** | 回答生成后，LLM 对每个引文三元组做反向验证——要求模型从引文反推源证据，或对断言做"你能从哪些 chunk 证明这一点"的自问自答 |
| **适用性** | 任何 GraphRAG 系统，与 LLM 无关（DeepSeek 可用） |
| **实现难度** | ⭐⭐⭐ 中——需实现断言提取、独立 verify 步骤、回滚逻辑 |
| **预期效果** | 假引文率降低 40-60%（FACTUM 检测 AUC 提升 37.5%；GGA 检出率优于语义基线） |
| **成本** | 每次验证 ~500-800 token，¥0.001-0.0016/次，按 10 条断言/回答计 ~¥0.016/回答 |
| **优点** | 直接解决归因错位；可复用 izu-pipeline 现有"核"步骤模式；无需额外模型 |
| **缺点** | 增加 LLM 调用次数 ~3-5x；自校验存在"确认偏误"（LLM 倾向同意自己）；DeepSeek 成本累积 |

### 方案 C：KG 噪声清洗（Entity Resolution + Triple Reflection）

| 维度 | 说明 |
|------|------|
| **原理** | 构建 KG 后，先做实体消歧（合并同义实体，如"izu" vs "izu-system"），再用 LLM-as-Judge 反射过滤不可靠关系（DEG-RAG: Less is More, ICLR 2026） |
| **适用性** | izu-wiki 的 markdown 实体关系图——实体命名不一致常见，关系信噪比低 |
| **实现难度** | ⭐⭐⭐⭐ 高——需实现 blocking 策略、相似度度量、LLM 关系质量评分 |
| **预期效果** | KG 规模压缩 30-40%，QA 准确率 +8-15%，减少因噪声实体引发的假引文 |
| **成本** | 一次性离线构建；实体消歧 ~¥1-3/千实体；关系反射 ~¥0.1-0.3/千关系 |
| **优点** | 从源头减少噪声；一次投入持续收益；与方案 A/B 正交可叠加 |
| **缺点** | 实现周期长（1-2周）；过度清洗可能丢失有用信息；需定义"可信关系"标准 |

### 方案 D：多信号融合检索（Hybrid Retrieval + Weighted RRF）

| 维度 | 说明 |
|------|------|
| **原理** | 同时跑 BM25（关键词）、稠密向量（语义）、图遍历（Personalized PageRank / 社区发现）三通道检索，加权 Reciprocal Rank Fusion 合并结果（Kaggle Swiss Legal 方案） |
| **适用性** | izu-wiki 已有实体 + 关系图，天然支持图遍历检索 |
| **实现难度** | ⭐⭐⭐⭐ 高——需维护三套索引、实现 RRF 融合、调试权重 |
| **预期效果** | 召回率 +20-30%，假引文率降低 25-35%（法律检索 benchmark Macro F1 从 0.327→0.691） |
| **成本** | 离线索引构建 ~¥2-5（嵌入），在线检索延迟 ~200-500ms |
| **优点** | 图遍历直接解决多跳问题；BM25 兜底避免空召回 |
| **缺点** | 工程复杂度高；权重调优依赖 eval；与现有 izu-pipeline 架构差异大 |

### 方案 E：引文无生成验证（Verification-Only Architecture）

| 维度 | 说明 |
|------|------|
| **原理** | LLM 仅评分/验证候选引文，**从不生成**引文字符串。所有引文直接从检索结果中选取（Swiss Legal GraphRAG, 2026） |
| **适用性** | 任何 RAG 系统，本质是架构限制而非事后检测 |
| **实现难度** | ⭐⭐ 中低——改变 prompt 策略 + 后处理约束 |
| **预期效果** | **消除**引文编造（citation fabrication 归零），但不解决引文与回答不一致问题 |
| **成本** | 几乎零增量成本 |
| **优点** | 从架构层面杜绝编造引文；极低实现成本 |
| **缺点** | 不能解决"引用对但推理错"；需要回答中引文格式严格约束 |

### 方案 F：多 Agent 交叉验证（Multi-Agent Validation）

| 维度 | 说明 |
|------|------|
| **原理** | 两个独立 Agent 分别生成回答和验证回答，不一致时触发回滚或修正（izu 现有"劈×3"模式可复用） |
| **适用性** | izu-pipeline 原生支持多 Agent 交叉审核——"修→核"步骤已实现类似逻辑 |
| **实现难度** | ⭐⭐⭐ 中——复用 izu-pipeline 现有 infrastructure |
| **预期效果** | 假引文率降低 30-50%（Multi-Agent RAG benchmark 减少 ~49 个幻觉语句） |
| **成本** | LLM 调用翻倍（验证 Agent ¥0.02/次） |
| **优点** | 与 izu 现有架构天然契合；可逐步增强 |
| **缺点** | 延迟翻倍；验证 Agent 也有幻觉风险；需要定义明确的"矛盾"判定标准 |

---

## 推荐方案

### 第一推荐：方案 B（LLM 自我校验 + 反问验证）✕ 方案 F（多 Agent 交叉验证）组合

**选择理由：**

1. **直接命中问题本质**——假引文的核心是 LLM 的归因错位（FACTUM 证明），自我校验 + 交叉验证直接对此下手
2. **与 izu-pipeline 现有架构零摩擦**——"核"步骤已实现搜索验证关键断言，"修"步骤类似 cross-review loop，只需扩展验证粒度到引文级别
3. **低成本启动**——不需要引入新模型（cross-encoder）、不需要重写检索层（multi-signal fusion）、不需要离线清洗（KG denoising），全部在现有 DeepSeek API 上完成
4. **可渐进增强**——W1 先实现引文级别的自校验，W2 再加独立验证 Agent，3-5 天可上线

**为什么不选其他方案？**
- **不选 A（Cross-Encoder）**：izu 没有现成的 cross-encoder 模型，部署 SBERT 或 BGE-reranker 需要 GPU 或 ONNX 推理，W1 时间不够。且 cross-encoder 不解决 LLM 归因错位——引文可以"相关但错误"
- **不选 C（KG 噪声清洗）**：收益高但周期长（1-2周），适合 W3/W4 做，不适合 W1 关键路径。且 izu wiki 当前规模（~1000 页面）噪声问题不严重
- **不选 D（多信号融合）**：架构改动太大，izu-pipeline 的"探→搜→织"线性流程不支持多通道并行检索。这是 W3+ 的中期重构目标
- **不选 E（引文无生成）**：它不解决"引文对但推理错"的问题——izu 的假引文问题更多是推理路径断裂而非编造引文本身
- **方案 B+F 组合**覆盖了从"生成侧自检"到"独立验证"的完整链路，且分步可实现

### 备选方案：方案 C（KG 噪声清洗）

如果 W1 验证发现 izu wiki 的图结构噪声严重（实体复用率 > 20%），备选方案 C 可提至 W2 并行执行。建议 W1 收集实体分布统计后决策。

---

## W1 实施路线

### 周一（5/18）

| 时段 | 任务 | 产出 |
|------|------|------|
| 上午 | **引文幻觉检测基线——数据侧** | ① 对 izu pipeline 最近的 100 条输出做人工标注：标注每条引文是否成立（成立/不成立/模糊） |
| | | ② 统计假引文率、类型分布（编造/错位/过泛化） |
| | | ③ 产出 `wiki/prep/citation-baseline-stats.md` |
| 下午 | **引文幻觉检测基线——代码侧** | ① 实现 `izu_citation_check.py`——基础版：提取回答中所有引文标记 + 对应三元组 |
| | | ② 对每条引文做"引文 → 检索子图"的精确匹配检查 |
| | | ③ 统计匹配失败率作为自动化基线 |

### 周二（5/19）

| 时段 | 任务 | 产出 |
|------|------|------|
| 上午 | **方案 B 核心：引文级自校验** | ① 在 `izu-pipeline.py` 的"修→核"之间插入引文验证子步骤 |
| | | ② 实现 prompt：对每条引文要求 LLM 输出"该断言是否严格由检索三元组支持" + 理由 |
| | | ③ 输出格式：`{citation_idx, claim, source_triple, verdict: SUPPORTED/PARTIAL/CONTRADICT, confidence}` |
| 下午 | **回滚逻辑 + 日志** | ① 对 PARTIAL/CONTRADICT 的引文触发局部回滚——返回"织"步骤补充检索 |
| | | ② 记录引文验证通过率到 `izu_agent_log.jsonl` |
| | | ③ 与周一基线对比，产出效果评估 |

### 周三-周五扩展（如果 W1 时间充裕）

| 日 | 任务 |
|----|------|
| 周三 | 实现**反问验证**（Reverse Verification）——从引文三元组反推源 chunk，检查语义一致性 |
| 周四 | 实现方案 F 的**交叉验证 Agent**——独立 Agent 仅做引文验证，与生成 Agent 结果对比 |
| 周五 | 集成测试 + W2 schema 设计文档初稿 |

### 关键输出

```
wiki/prep/
├── graphrag-false-citation-pre-study.md   ← 本文
├── citation-baseline-stats.md              ← 周一产出：基线数据
├── citation-verify-prototype-results.md    ← 周二产出：自校验评估
└── graphrag-schema-w2-design.md            ← 周五产出：W2 schema 设计
```

---

## 参考

1. GGA: Detecting Hallucinations in GraphRAG via Attention Patterns (arXiv:2512.09148, 2025)
2. FACTUM: Mechanistic Detection of Citation Hallucination (arXiv:2601.05866, 2026)
3. DEG-RAG: Denoising KGs for RAG (ICLR 2026)
4. FinBench-QA-Hallucination: GraphRAG Hallucination Benchmark (arXiv:2603.20252, 2026)
5. Hybrid GraphRAG for Cross-Lingual Legal Citation Retrieval (IJECS, 2026)
6. RAG-KG-IL: RAG vs KG Integration (arXiv:2503.13514, 2025)
7. MetaRAG: Hallucination Detection Framework (arXiv:2509.09360, 2025)
8. GraphSEARCH: Multi-Step Graph Retrieval (arXiv:2509.22009, 2025)
