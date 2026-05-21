# 🔬 论文快速扫描
**日期**：2026-05-14 · **呈：张成市**
**扫描**：7篇去重论文（10篇中2组重复）

---

### 1. Retrieval-Conditioned Topology Selection for Multi-Agent Code Generation
- **核心技术方向**：多Agent拓扑动态选择
- **预判核心贡献**：⚠️ 不硬编码Agent通信拓扑，而是用检索动态选择——这是Agent协同从"静态图"到"动态图"的关键一步
- **与izu/Hermes的关系**：7/10。izu八步流水线目前是固定的串行/并行拓扑。这篇可以启发"根据研究主题动态选择哪些Agent并行、哪些串行"
- **深挖建议**：🟡 可挖
- **建议研究方式**：paper-translate单篇深翻

### 2. ReVeal: Self-Evolving Code Agents via Iterative Generation-Verification
- **核心技术方向**：自演进Agent · 生成-验证闭环
- **预判核心贡献**：⚠️ 多轮RL让Agent通过"生成代码→自动验证→根据结果改进"循环自我提升。不是靠人类反馈，是靠自动验证。这正是匠石第1条（"能用代码就别用模型"）的AI版本：AI自己写代码验证自己
- **与izu/Hermes的关系**：10/10。直接命中匠石宪法核心。izu的核（验证）阶段目前只检查事实——这篇把验证扩展到"让模型自己生成验证标准然后自我改进"
- **深挖建议**：🔴 必挖
- **建议研究方式**：izu八步长编（全流程深度研究）

### 3. TagRAG: Tag-guided Hierarchical Knowledge Graph for RAG
- **核心技术方向**：标签引导 · 分层图RAG
- **预判核心贡献**：⚠️ 用标签体系引导知识图谱的分层构建，解决GraphRAG"全局一锅粥"的问题。把知识摘要按语义层级组织
- **与izu/Hermes的关系**：7/10。wiki的知识图谱方向。Neo4j里存的实体+概念+对比可以用类似的分层标签引导
- **深挖建议**：🟡 可挖
- **建议研究方式**：paper-translate单篇深翻

### 5. Self-Evolving Framework for Terminal Agents via Observational Context Compression
- **核心技术方向**：终端Agent · 上下文压缩
- **预判核心贡献**：⚠️ 终端场景（CLI/Shell）中Agent通过压缩历史观测降低推理成本。实用性强
- **与izu/Hermes的关系**：6/10。Hermes Agent的终端工具调用可能受益。但优先度低于ReVeal
- **深挖建议**：🟡 可挖
- **建议研究方式**：paper-translate单篇深翻 · 或纳入izu长编作为对比案例

### 6. Architectural Design Decisions in AI Agent Harnesses
- **核心技术方向**：Agent Harness架构设计空间
- **预判核心贡献**：⚠️ 系统化梳理Agent框架的架构决策维度。偏综述
- **与izu/Hermes的关系**：8/10。通用但重要——可以作为izu系统设计的对照清单
- **深挖建议**：🟡 可挖
- **建议研究方式**：wiki-project-study（作为设计参考手册）

### 7. Agentifying Agentic AI
- **核心技术方向**：Agent性 · 关系维度
- **预判核心贡献**：⚠️ 这篇可能是一篇概念性/哲学论文。核心论点："Agentic"不只是自主完成任务的AI，必须包含"关系维度"——即Agent存在于与他者的关系中才成为真正的Agent
- **与izu/Hermes的关系**：9/10。直接支撑izu白皮书的核心论题——"陪伴不是功能，是关系"。这篇给了学术语言来论证izu为什么不是"更好的工具"而是"真正的Agent"
- **深挖建议**：🔴 必挖
- **建议研究方式**：izu八步长编（哲学基础论证，支撑白皮书v0.3）

### 8. GRASP: Gradient Realignment via Active Shared Perception for Multi-Agent Collaborative Optimization
- **核心技术方向**：多Agent · 梯度对齐 · 共享感知
- **预判核心贡献**：⚠️ 通过共享感知空间对齐多个Agent的优化目标，避免协同中的"各自为政"
- **与izu/Hermes的关系**：6/10。技术层面偏底层（基于梯度），对izu的prompt级协同借鉴有限
- **深挖建议**：🟢 可跳
- **建议研究方式**：skip

### 9. Self-Improving Coding Agent (2504.15228)
- **核心技术方向**：Agent自我编辑代码
- **预判核心贡献**：⚠️ Agent利用基础工具（文件读写/终端）自主编辑自身代码来提升基准性能。与ReVeal互补——ReVeal靠验证改进行为，这篇靠修改代码改进能力
- **与izu/Hermes的关系**：9/10。匠石原则第5条"做减法不做加法"——如果Agent能自己审计pipeline、自己删掉不再需要的拐杖函数，这就是自动化版的功能大扫除
- **深挖建议**：🔴 必挖（与ReVeal合并为一个研究主题）
- **建议研究方式**：纳入ReVeal的izu长编作为对比——自演进Agent的双路径（行为改进 vs 代码改进）

---

## 📋 综合建议

### 🔴 今日必挖（2个主题）

| 主题 | 论文 | 路由 | 理由 |
|------|------|------|------|
| 自演进Agent双路径 | ReVeal(#2) + Self-Improving(#9) | izu八步长编 | 直接决定izu下一个升级方向——验证驱动的自我改进+代码级自我优化 |
| Agent的关系本质 | Agentifying(#7) | izu八步长编 | 哲学基础论证，支撑白皮书v0.3——用学术语言建立izu的不可替代性 |

### 🟡 可择日深挖

| 论文 | 建议方式 | 优先级 |
|------|---------|--------|
| Agent Harness架构(#6) | wiki-project-study | 中 |
| TagRAG(#3) | paper-translate | 中 |
| Agent拓扑选择(#1) | paper-translate | 低 |
| 终端Agent压缩(#5) | paper-translate | 低 |

### 🟢 可跳过
- GRASP(#8)：基于梯度的底层优化，对prompt级协同借鉴有限
- 重复论文(#4, #10)：与#2/#9内容重复

### ⚡ 今日执行顺序建议
1. 先跑izu-pipeline：**"自演进AI Agent范式——从ReVeal到Self-Improving Coding Agent"**（合并#2+#9）
2. 后跑izu-pipeline：**"Agent的关系本质与AI知识同路人的哲学基础"**（#7）
