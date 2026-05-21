# 📋 待研究主题Plan清单 · 2026-05-16

**输入来源**：论文日报（6篇）+ 快速扫描 + 视频扩展

---

## 🔴 必研（今日执行）

### 1. 主题：AI Agent Harness 设计决策与框架对比
- **来源依据**：论文#4（Architectural Design Decisions in AI Agent Harnesses，⭐⭐⭐⭐⭐）、视频扩展发现的Firecrawl Harness解读、多Agent框架对比博文
- **研究方式**：→ **izu-pipeline**（领域级深度研究）
- **预期产出**：Agent Harness设计决策矩阵 + 当前izu架构对照分析 + 改进建议
- **理由**：直接关联izu/Hermes的Agent架构，论文系统性梳理了Harness的决策维度，框架对比提供了实操数据

### 2. 主题：Knowledge Graph RAG 技术路线与部署经验
- **来源依据**：论文#1（⭐⭐⭐⭐）+ 吴恩达B站教程 + GraphRAG部署博文
- **研究方式**：→ **paper-translate** 单篇深翻
- **预期产出**：论文全文翻译 + 技术路线评估 + 与当前RAG方案的对比
- **理由**：直接关联izu的检索模块，知识图谱增强是当前确定性的效率突破口

### 3. 主题：Self-Improving Code Generation —— 语义熵与行为共识
- **来源依据**：论文#6（Self-Improving Code via Semantic Entropy，⭐⭐⭐）+ HN讨论
- **研究方式**：→ **paper-translate** 单篇深翻
- **预期产出**：论文解读 + 实践可行性评估
- **理由**：匠石原则（代码优先、确定性验证）的直接技术支撑

---

## 🟡 可研（本周内）

1. **Enterprise Multi-Agent Architecture 企业级能力对齐设计**（论文#2）
   - 快速扫读架构图 + 能力对齐方法论 → 与izu当前设计对照
   
2. **Multi-Agent Frameworks 2026 横向对比**（博客资源）
   - LangGraph / CrewAI / AutoGen / Google ADK → 提取每个框架的Harness设计特点

3. **Agentifying Agentic AI**（论文#3）
   - 阅读摘要+结论即可，判断其提出的Agent社会维度是否对izu有启发

---

## 🟢 观望（趋势跟踪）

1. **Multiagent Systems 最新论文列表**（论文#5）——作为持续资源池
2. **Agentic Scaling Laws**（Reddit讨论中提及）——如果形成系统化理论，值得跟进

---

## 🛤️ 路由决策

| 必研项 | 路由 | 执行方式 | 状态 |
|--------|------|---------|------|
| #1 Agent Harness | → izu-pipeline | 八步深度研究 | 🚀 待启动 |
| #2 KG-RAG | → paper-translate | 全文翻译+izu解读 | 📄 待启动 |
| #3 Self-Improving Code | → paper-translate | 全文翻译+izu解读 | 📄 待启动 |

---

## ⚡ 今日执行顺序

1. **优先**：启动 Agent Harness 的 izu-pipeline（深度研究，产出决策矩阵）
2. **并行**：启动 KG-RAG 的 paper-translate（快速评估方法对现有RAG的提升幅度）
3. **跟进**：Self-Improving Code 的 paper-translate（评估实践可行性）
