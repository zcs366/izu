# 🎬 视频扩展洞察

**日期**：2026-05-16 · 基于今日论文主题

## 今日论文主题关键词
Multi-Agent Architecture / Agent Harness / Knowledge Graph RAG / Self-Improving Code Generation

---

## 值得看的视频（Top 3）

### 1. How to Create and Use AI Agents in 2026
- **来源**：YouTube
- **链接**：https://www.youtube.com/watch?v=4TvH-OZhwxI
- **核心观点**：从"人为在环"到"Agent在环"的设计范式转变，整个系统架构需要跟着变
- **与今日论文关联**：直接对应论文#4（Agent Harness架构决策）和论文#2（企业Agent设计）
- **⚡值得看理由**：2026年视角，讨论Agent-in-the-loop架构转型，对izu/Hermes的Agent框架设计有实操指导

### 2. 【吴恩达】2025年公认最好的【Agent知识图谱】教程
- **来源**：B站
- **链接**：https://www.bilibili.com/video/BV1YnpMznEFb/
- **核心观点**：Google ADK + 多智能体系统架构 + 知识图谱的集成方法
- **与今日论文关联**：直接对应论文#1（知识图谱RAG）和论文#3（Agentifying Agentic AI）
- **⚡值得看理由**：吴恩达出品，覆盖从知识图谱构建到多智能体系统的完整链路

### 3. Best Multi-Agent Frameworks in 2026: LangGraph, CrewAI, OpenAI...
- **来源**：GuruSup 博客
- **链接**：https://gurusup.com/blog/best-multi-agent-frameworks-2026
- **核心观点**：6大主流多Agent框架的横向对比（OpenAI Agents SDK、LangGraph、CrewAI、AutoGen/AG2、Google ADK）
- **与今日论文关联**：论文#4（Agent Harness）的实操配套——看各框架在Harness设计决策上的取舍
- **⚡值得看理由**：2026年最新框架对比，直接可转化为izu框架设计的参考

---

## 📡 新视野扩展

### 从视频话题中发现的论文遗漏视角

1. **Agent-in-the-loop 设计范式**：多数论文停留在"能力堆叠"层面讨论Agent，视频中提出的人→Agent→系统的"三角架构"在今日论文中没有覆盖。这是Harness设计的核心思想转变。

2. **框架对比中的"生产环境陷阱"**：LangGraph vs CrewAI vs AutoGen的讨论揭示，论文通常只讨论理论架构，但实际生产中每个框架都有自己的坑——状态管理、错误恢复、成本控制。论文#4（Harness决策）如果没包括这些实操维度，将是不完整的。

3. **GraphRAG的实际部署经验**：知识图谱RAG论文是理论方法，但B站视频和社区文章已经积累了实际部署GraphRAG的回退策略、索引成本、查询延迟数据。

### 🔄 与论文的互补关系

| 论文话题 | 视频/社区提供的额外视角 |
|---------|----------------------|
| Knowledge Graph RAG（#1） | 实际部署成本、索引策略、回退机制 |
| Enterprise Agent Design（#2） | 企业落地的组织阻力、ROI衡量 |
| Agentifying Agentic AI（#3） | Agent互动的"社交协议"实操经验 |
| Agent Harness设计决策（#4） | 各框架在Harness维度上的实际取舍 |
| Self-Improving Code（#6） | HN社区对新方法的批判性评价 |
