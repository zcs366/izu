# 🧬 核战队审阅 · Stage1 信号评审
**日期**: 2026-05-17
**评审团队**: 子产（需求判断）· Nate Silver（信号分析）· George Orwell（破壁者）
**审阅范围**: AI日报10篇论文

---

## 1. SDAR — Self-Distilled Agentic Reinforcement Learning

- **子产**：**必关注**。自蒸馏作为RL辅助门控目标，解决Agent长程奖励稀疏问题。直接关联izu Agent后训练管线（Qwen2.5/Qwen3上ALFWorld+9.4%, WebShop+10.2% 超过GRPO）。技术点：sigmoid门控自蒸馏+轨迹级RL联合优化。
- **Nate Silver信号**：**P=0.85**。在3个标准Agent基准+2个模型族上系统验证，跨模型家族一致涨点。HF 77 upvotes，有开源代码，可复现性好。
- **Orwell破壁者**：**真信号**。OPSD本身不是全新概念，但作为"门控辅助目标"与RL联合优化是多轮Agent场景下的实质创新。实验跨模型家族、跨任务对比，无cherry-pick证据。
- **汇总**：🌟🌟🌟🌟🌟 **必读**

---

## 2. MemEye — Visual-Centric Evaluation for Multimodal Agent Memory

- **子产**：**必关注**。多模态Agent记忆评测框架，从视觉证据粒度和检索使用复杂度两维度构建基准。直接关联izu Agent记忆评测管线。
- **Nate Silver信号**：**P=0.80**。NVIDIA背景，46页长文含15图。13记忆方法×4 VLM主干的系统消融。HF 50 upvotes。基准泛化性需时间验证。
- **Orwell破壁者**：**真信号**。现有评测多可纯文本作答，MemEye首次强制像素级视觉证据参与，填补明确空白。4个验证门控设置严谨。
- **汇总**：🌟🌟🌟🌟🌟 **必读**

---

## 3. MinT — LLM Training and Serving Infrastructure

- **子产**：**可关注**。基于K8s的LoRA训练推理管理系统。与现有项目无直接管线关联。
- **Nate Silver信号**：**P=0.55**。HF 205 upvotes（W20周榜第1），但缺乏严格性能对比benchmark。60+作者暗示工业界白皮书性质。
- **Orwell破壁者**：**包装过度**。核心思想（LoRA serving on K8s）已有成熟方案（vLLM+K8s, TGI等）。60+作者但创新有限。
- **汇总**：🌟🌟🌟 **可选**

---

## 4. MCP-Cosmos — World Model-Augmented Agents for MCP

- **子产**：**可关注**。世界模型增强的MCP Agent。与工具编排相关但对核心管线不直接有用。
- **Nate Silver信号**：**P=0.50**。仅2位作者，20+ MCP-Bench任务，实验规模有限。缺与其他方案的系统对比。
- **Orwell破壁者**：**换说法**。"世界模型增强Agent"并非新概念—Dyna（1990）、MuZero等早已成熟。BYOWM概念有趣但实现浅。
- **汇总**：🌟🌟🌟 **可选**

---

## 5. MCPShield — Attack Detection for MCP Tool-Call Traffic

- **子产**：**可关注**。用GNN检测MCP工具调用会话攻击。与MCP安全相关，非核心需求。
- **Nate Silver信号**：**P=0.65**。实验管道完整，关键发现（metadata-only AUROC仅0.64，内容嵌入推至0.89+）有说服力。作者诚实报告了random-split高估问题。
- **Orwell破壁者**：**真信号**。关键发现—graph结构不比pooled embeddings有效（XGBoost在pooled上AUROC 0.975超过GNN的0.917）。诚实报告加分。
- **汇总**：🌟🌟🌟 **可选**

---

## 6. MCP-BiFlow — Bidirectional Data-Flow Risks in MCP

- **子产**：**推荐关注**。MCP-BiFlow静态分析框架。直接实用价值：15,452个仓库普查，118条漏洞路径。与MCP Server安全直接相关。
- **Nate Silver信号**：**P=0.75**。数据基础扎实：大规模仓库分析、32个漏洞上93.8%召回率、与四家竞品对比。可复现。
- **Orwell破壁者**：**真信号**。系统性安全审计，技术贡献（MCP-aware entrypoint recovery, protocol-specific taint semantics）是实质性新工作。
- **汇总**：🌟🌟🌟🌟 **推荐**

---

## 7. MCP Workflow Engine — Separating Intelligence from Execution

- **子产**：**推荐关注**。Agent推理一次生成蓝图，后续零token执行。token成本降低99%+。与Agent推理效率直接相关。
- **Nate Silver信号**：**P=0.70**。单一案例数据详细。token成本降低99%+有说服力。3月投稿缺后续反响。工程细节丰富，可复现。
- **Orwell破壁者**：**真信号**。"智能与执行分离"概念并非全新，但"MCP-native"是实现层面的新东西。关键创新在工作流蓝图在MCP协议层面的一等公民实现。但单一案例不足以证明通用性。
- **汇总**：🌟🌟🌟🌟 **推荐**

---

## 8. CDD — Context Compliance under Knowledge Conflict

- **子产**：**推荐关注**。CDD探针诊断RAG上下文合规问题。与RAG可靠性直接相关，Wiki/RAG管线可借鉴。
- **Nate Silver信号**：**P=0.75**。跨模型评估（Gemini-2.5-Flash+Claude家族），N=500的TruthfulQA测试。CDD在Gemini上64.1%因果敏感度，Claude仅±7%—诚实报告差异。Epi-Scale基准公开。
- **Orwell破壁者**：**真信号**。已有大量RAG冲突检测工作，CDD创新在信念分解、区分"上下文合规"与"检索质量"、发现模型家族差异。有真实发现。
- **汇总**：🌟🌟🌟🌟 **推荐**

---

## 9. SU-01 — Gold-Medal-Level Olympiad Reasoning

- **子产**：**必关注**。反向困惑度课程SFT+两阶段RL+测试时扩展，IMO 2025/USAMO 2026和IPhO 2024/2025金牌。与推理能力提升工程可复制性极高。
- **Nate Silver信号**：**P=0.85**。HF 137 upvotes，77页报告。30B-A3B参数效率令人印象深刻。但奥赛题存在数据泄露风险（2025/2026题可能已在训练数据中）。
- **Orwell破壁者**：**真信号**。虽有o1/o3/R1验证在先，但反困惑度课程的SFT设计和明确的效率标杆是实质工程进步。并非"换说法"。需注意奥赛数据泄露风险。
- **汇总**：🌟🌟🌟🌟🌟 **必读**

---

## 10. Darwin Family — Evolutionary Model Merging

- **子产**：**推荐关注**。无梯度权重进化合并，旗舰模型GPQA #6。与模型合并策略相关。
- **Nate Silver信号**：**P=0.70**。NeurIPS 2026投稿中。86.9% GPQA Diamond有说服力。但进化搜索的可复现性天然较低。
- **Orwell破壁者**：**真信号**。模型合并领域已有大量工作，但14维基因组、MRI-Trust引导、跨架构合并是实质性创新。GPU开销未报告是缺憾。
- **汇总**：🌟🌟🌟🌟 **推荐**

---

## 🧬 免疫系统优先汇总

| 论文 | Orwell标记 | 是否跳过 |
|------|-----------|---------|
| 1. SDAR | **真信号** | ❌ 不跳过 |
| 2. MemEye | **真信号** | ❌ 不跳过 |
| 3. MinT | **包装过度** | ⚠️ 建议跳过深度分析 |
| 4. MCP-Cosmos | **换说法** | ⚠️ 建议跳过深度分析 |
| 5. MCPShield | **真信号** | ❌ 不跳过 |
| 6. MCP-BiFlow | **真信号** | ❌ 不跳过 |
| 7. MCP Workflow Engine | **真信号** | ❌ 不跳过 |
| 8. CDD | **真信号** | ❌ 不跳过 |
| 9. SU-01 | **真信号** | ❌ 不跳过 |
| 10. Darwin Family | **真信号** | ❌ 不跳过 |

**Orwell最终判断**：10篇中2篇建议免疫跳过（20%噪音率），其余8篇为真实信号。整体日报质量较高。建议优先深度阅读SDAR、MemEye、SU-01三篇必读论文。
