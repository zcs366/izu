# 🧠 核战队审阅 · Stage2 技术评审
**日期**: 2026-05-17
**评审团队**: 鲁班（架构审计+装备制造）· 匠石（代码化判断）· Newton（挖根）· Edison（验证判断）
**审阅范围**: AI日报10篇论文（#3、#4按Orwell建议跳过深度分析）

---

## 一、Agent架构与多Agent系统

### 1. Self-Distilled Agentic Reinforcement Learning (SDAR)
- **鲁班**：可以直接用。SDAR的sigmoid-gated OPSD是GRPO训练管线的轻量扩展，不需要新基础设施，只需在现有izu RL训练脚本中插入一个辅助loss头。造一个`izu_trainer_sdar.py`模块（约300行），封装gate逻辑和token级信号映射。无架构冲突——OPSD本来就是GRPO的补充，SDAR只是解决了OPSD的不稳定问题。
- **匠石**：代码为主，模型为辅。gate逻辑是纯代码（sigmoid映射、梯度掩码）；privileged上下文需要通过一个小Teacher模型（同族Qwen2.5-0.5B即可）产出token级信号。代码边界 = 前向传播中的辅助loss计算；模型边界 = Teacher模型的蒸馏信号生成。能用代码实现的都有：gate衰减、负样本软过滤、正样本强化。
- **Newton**：关键隐藏假设——Teacher的privileged context是否真的"富含信息"？论文假设Teacher分支有更多上下文就能产生更高质量的token级信号，但如果Teacher自身被噪声上下文污染（多轮Agent交互中常见），蒸馏信号反而引入偏差。第二个隐患：sigmoid gate的衰减率是固定超参，在长轨迹（>50轮）中累积误差不可忽视。采纳后可能带来：训练稳定性提升但需要更细致的gate温度调节。
- **Edison**：可复现。论文在Qwen2.5/Qwen3上验证，我们有相同模型族的访问权限。核心结果（ALFWorld +9.4%, WebShop +10.2%）是标准的Agent RL评测，环境已成熟。开源代码未明确承诺，但方法描述足够详细（sigmoid gate + detached logits），单块A100-80G即可复现（30B模型需要4×A100）。工程工作量：3-5人/天实现+调参。
- **技术结论**：**可直接用** — 优先级最高的架构采纳。

### 2. MemEye: A Visual-Centric Evaluation Framework for Multimodal Agent Memory
- **鲁班**：评测框架不能直接用，但方法论可直接复用。MemEye设计了4个验证门控（可答性/捷径抵抗/视觉必要性/推理结构）和8个生活场景任务，这些可以作为izu多模态记忆评测的模版。需要造的装备：`izu_memeye_bench` — 一个适配izu Agent接口的评测套件（约500行Python + 场景数据集软链接）。架构上不冲突，但需要izu Agent支持多模态输入输出（尚未完备）。
- **匠石**：代码为主。评测框架本身就是代码逻辑（8场景任务定义、4门控验证流程、13种记忆方法的API封装）。模型边界在于：各场景的"答案提取"需要一个VLM作为oracle judge——但这可以用已有的Gemini/Claude API替代，不需要训练新模型。整套评测管线90%是编排代码，10%是模型API调用。
- **Newton**：核心假设——"像素级视觉证据"对Agent记忆的必要性。论文声称"现有评测纯文本可答"，但绕过的问题是：在当前Agent应用中，纯文本记忆是否真的不够用？如果Agent的决策本质上依赖语义理解而非像素精度，那MemEye的评测压力可能脱离实际应用场景。采纳带来的副作用：过度强调视觉记忆会导致Agent架构向图像存储倾斜，增加存储和检索成本（每帧保存vs语义摘要）。
- **Edison**：条件可复现。论文没有提供完整基准数据集下载链接，但GitHub仓库（https://github.com/xrenaf/MEMLENS）存在。8生活场景数据需要自己采集或请求作者提供。13种记忆方法×4种VLM主干的评测矩阵需要大量API调用（估计$200-500）。有NVIDIA团队背书，数据质量可信。工程工作量：5-7人/天搭建环境+数据准备。
- **技术结论**：**需改造** — 评测方法论可直接用，但完整复现成本较高。

### 3. MinT: Managed Infrastructure for Training and Serving Millions of LLMs
- **Orwell标记为"包装过度"**：Orwell不建议跳过。按指示不做深度技术分析。
- **技术结论**：暂不采纳。

### 4. MCP-Cosmos: World Model-Augmented Agents for Complex Task Execution in MCP Environments
- **Orwell标记为"换说法"**：Orwell不建议跳过。按指示不做深度技术分析。
- **技术结论**：暂不采纳。

---

## 二、MCP协议与工具编排

### 5. MCPShield: Content-Aware Attack Detection for LLM Agent Tool-Call Traffic
- **鲁班**：可以直接用，但需要改造MCP server中间件。MCPShield的核心是"将Agent会话编码为图(SBERT embedding)→GNN分类"，这可以封装为Hermes Agent的一个中间件插件——`hermes_shield_middleware`。架构上，需要在Hermes Agent的MCP调用链路中插入一个拦截点：所有tool call→response走SBERT embedding→GAT/GraphSAGE检测。不冲突，但会增加每次tool call的延迟（~50ms embedding + ~20ms推理）。
- **匠石**：代码为主。SBERT embedding是现成的sentence-transformers库（代码调用），GNN推理可以用训练好的模型权重（模型边界）。论文明确指出：树集成模型在pooled embedding上AUROC达0.975，优于GNN——这意味着可以不跑GNN，直接用XGBoost/随机森林处理embedding，纯代码+少量模型推理。XGBoost推理<1ms，几乎无延迟。
- **Newton**：三个深层问题。第一，论文的训练数据RAS-Eval/ATBench是否覆盖Hermes Agent的MCP调用模式？如果调用模式不同（工具类型、参数结构），检测模型需要重新训练。第二，论文发现"random split膨胀26个百分点的记忆混淆效应"——这意味着部署后的真实性能可能远低于论文报告值（AUROC 0.975→实际可能0.75-0.80）。第三，检测信号主要在SBERT embedding中——攻击者可以通过对抗性参数构造绕过embedding检测。
- **Edison**：有限可复现。论文是单作者（Sultan Zavrak），未公开代码和数据集。AUROC 0.975的结果依赖RAS-Eval和ATBench两个专有基准。没有公开权重意味着我们需要从零训练检测模型，需要收集Hermes Agent的正常和攻击会话数据。工程工作量：数据收集2-3周 + 训练1周（需要人工标注攻击样本）。
- **技术结论**：**需改造** — 方法论正确，但需要重新训练和适配Hermes Agent的MCP调用模式。

### 6. MCP-BiFlow: Uncovering Bidirectional Data-Flow Risks in MCP Ecosystem
- **鲁班**：可以直接用。MCP-BiFlow是一个基于Python的静态分析工具，分析15,452个真实MCP仓库后发现了118条漏洞路径。需要造的装备：`hermes_mcp_auditor` — 封装MCP-BiFlow的MCP Server安全审计脚本，每次接入新的第三方MCP Server时自动运行。架构上不冲突——这是开发期/部署前的审计工具，不影响运行时性能。需要改造之处：MCP-BiFlow目前只分析Python MCP Server，如果Hermes Agent的MCP Server是TypeScript写的，需要扩展支持。
- **匠石**：纯代码。静态分析不需要模型。MCP-BiFlow的核心是MCP感知的entrypoint recovery + 协议特定taint建模 + 过程间传播分析——全部是代码逻辑。可以集成到CI/CD流水线中，作为`mcp_audit`命令。代码边界清晰：输入=MCP Server源码，输出=漏洞路径报告。
- **Newton**：三个隐患。第一，论文的32个确认漏洞基准规模有限（32个case覆盖了多大比例的MCP漏洞类型？）。第二，静态分析有假阳性问题——论文报告的549个候选簇中只有87个服务器确认存在漏洞（~16%确认率），剩下84%需要人工审核，审计工作量不低。第三，MCP-BiFlow只检测Python仓库（15,452个），Hermes Agent可能使用其他语言实现的MCP Server，工具不适用。
- **Edison**：可复现。论文分析了15,452个真实MCP仓库（从GitHub采集），方法论透明。但MCP-BiFlow本身未提供可下载工具包——需要根据论文描述重新实现。工程工作量较大（3-4人/周实现核心分析管线），但方法论可独立验证。
- **技术结论**：**需改造** — 方法论必须采纳，但需要重新实现工具并支持多语言MCP Server分析。

### 7. MCP Workflow Engine: Separating Intelligence from Execution
- **鲁班**：直接复用潜力极高。论文提出的MCP Mediator模式（一个MCP Server同时作为下游MCP Server的Client）与Hermes Agent的编排执行分离设计高度吻合。需要造的装备：`hermes_workflow_engine` — 基于MCP SDK的TypeScript实现，核心是一个Worfklow Executor（解析JSON蓝图→执行MCP调用链）。这是Hermes Agent架构缺失的关键组件——目前Hermes Agent每次执行都走完整推理路径。采纳后可实现"推理一次，执行N次"。
- **匠石**：代码为主。蓝图解析和执行引擎是纯TypeScript代码（约800-1200行）。JSON blueprints的schema定义、参数化模板、循环/并行/数据管道——全部是代码逻辑。模型边界仅在于"首次生成工作流蓝图"——这需要一个Agent推理调用。后续的`run_workflow`调用消耗0 token。典型的"能用代码就别用模型"案例。
- **Newton**：论文的K8s CMDB同步是理想化场景（确定性、结构化、可预编排）。但在非确定性场景（如用户对话、动态网页浏览）中，工作流蓝图的可复用性大幅下降——每次交互可能都是新的。论文声称"token成本降低99%+"，但忽略了一个关键成本：如果蓝图需要频繁重新生成（因为环境变化），Agent的推理成本会转移到蓝图重新生成上。采纳后会带来新的问题：如何判定"环境变化程度"以决定是否需要重新生成蓝图？
- **Edison**：可复现。论文是单作者（Abhinav Singh Parmar），提供了TypeScript实现（基于MCP SDK）。方法论透明，K8s同步场景可自行搭建测试。工程工作量：1-2人/天集成到Hermes Agent中。论文代码未明确开放但方法足够简单，可以独立实现。
- **技术结论**：**可直接用** — 架构设计成熟，实现简单，收益明确。

---

## 三、RAG与知识管理

### 8. Does RAG Know When Retrieval Is Wrong? (CDD)
- **鲁班**：可直接用。CDD（Context-Driven Decomposition）是一个推理时探针——在模型生成答案的同时分解"检索上下文→答案"的因果影响。可以封装为`izu_rag_compliance`模块，在izu和Wiki知识检索后插入CDD探针。架构上不冲突——CDD是一个推理时干预层，不需要修改检索管线或生成模型。需要造的装备：一个轻量CDD探针（~200行Python），调用已有的语言模型接口，无需额外训练。
- **匠石**：模型为主（但极轻量）。CDD是prompt-based探针——通过精心设计的prompt让LLM分解自己的回答中哪些部分归因于检索上下文。不需要训练分类器或新模型。工匠的判断：这是"能用模型但模型开销极小"（每次推理额外消耗30-50 token）的场景，不值得专门写代码规则替代——因为"知识冲突判断"本身需要语义理解。
- **Newton**：论文发现了三个模式中P2最致命——Claude系列的精度提升机制与显式冲突分解不同（CDD的因果敏感度在Claude上仅-3%到+7%）。这意味着CDD探针的有效性高度依赖模型家族，对Gemini有效，对Claude不一定。采纳到izu后，如果izu基于不同基座（如Qwen/Llama），CDD探针的效果需要重新验证。第二个问题：CDD是推理时探针，增加回答延迟（~200ms）。
- **Edison**：可复现。论文发布了Epi-Scale基准，CDD方法是prompt-based，不需要训练。在Gemini-2.5-Flash上验证需要Google API访问（我们有）。工程工作量很小：1人/天实现CDD探针脚本。关键是验证在不同基座模型上的效果。
- **技术结论**：**可直接用** — 低风险、低工程成本，值得立即集成到izu RAG管线。

---

## 四、LLM训练与推理

### 9. SU-01: Gold-Medal-Level Olympiad Reasoning
- **鲁班**：无法直接用在izu Agent训练上，但方法论可提取。SU-01的reverse-perplexity课程SFT + 两阶段RL（可验证RL→证明级RL） + test-time scaling的配方，可以提炼出适用于izu Agent训练的"推理能力扩展配方"。需要造的装备：不需要独立工具，但这些训练技巧可以注入现有的izu训练脚本——特别是reverse-perplexity课程（根据perplexity排序训练数据，从易到难训练）。架构不冲突，反而填补了izu训练中"课程学习"的缺失。
- **匠石**：模型训练为主，代码为辅。核心是训练配方（数据排序策略、两阶段RL切换逻辑）——这些是代码逻辑；但反向困惑度计算、RL奖励信号需要模型推理。代码边界：数据预处理脚本（排序/过滤）、训练调度逻辑；模型边界：RL rollouts、验证器调用。
- **Newton**：论文声称"简单统一的扩展"但隐藏的条件苛刻——340K子8K-token轨迹和200 RL步骤听起来不多，但这些数据是竞赛级高质量数据（IMO/USAMO/IPhO问题+解答），获取成本极高。训练数据本身是最大的壁垒。第二个问题：训练出来的30B-A3B MoE模型在学科竞赛上表现优异，但通用Agent任务（MCP调用、多轮对话）上的泛化能力未评测——可能存在严重的过拟合到竞赛格式。
- **Edison**：不可复现。核心壁垒在训练数据——340K竞赛级轨迹需要专家标注，不是开源数据集。28作者的Teamsize暗示这是大型机构（可能中国高校联合或企业）的项目，训练开销也需要数百块GPU。即使有代码开源（未承诺），无数据也无法复现。硬件要求：30B-A3B MoE模型需要至少8×A100-80G。
- **技术结论**：**暂不可行** — 训练不可复现，但reverse-perplexity课程方法可提取使用。

### 10. Darwin Family: MRI-Trust-Weighted Evolutionary Merging
- **鲁班**：可以直接用。Darwin的进化式模型合并不需要训练，只需要权重重组。可以封装为`izu_darwin_merger`工具——接收多个基础模型权重，输出合并后模型。特别有价值的是跨架构合并（Transformer + Mamba）。需要造的装备：一个模型合并调度脚本（基于evolutionary search + MRI-Trust评估）。架构上不冲突——这是部署前的优化步骤，不改变运行时架构。
- **匠石**：代码为主，模型权重复制为辅。进化搜索算法（14维基因组、交叉/变异/选择）是纯Python代码。MRI-Trust Fusion的可学习信任参数是少量梯度下降（<100步）。模型边界仅在于每次合并后需要用少量评测样本评估质量——但这可以通过轻量评测（如GPQA subset）完成，不需要完整训练循环。
- **Newton**：隐藏问题——进化式合并虽然"无训练"，但进化搜索的计算成本不低。Darwin的旗舰模型Darwin-27B-Opus经历了几代进化搜索？论文未明确说明。如果每代需要评测10-20个子代模型，每个子代模型在GPQA Diamond上的评测成本约$20-50，整个进化搜索可能消耗$1000+。第二个问题：进化合并的稳定性——合并后的模型可能在特定任务上退化（论文只报告了最佳结果，未报告最差/平均/方差）。
- **Edison**：可复现。论文在NeurIPS 2026投稿，方法论透明。关键组件（14D merge genome、MRI-Trust fusion）描述详细。需要8×A100-80G运行合并实验，但小规模验证（4B-8B级模型）单卡A100即可。工程工作量：1-2人/周实现合并管线。论文承诺开源（CC-BY-4.0许可）。
- **技术结论**：**可直接用** — 实用性高，适合izu/Hermes的模型合并需求，建议从4B-8B模型开始验证。

---

## 汇总

| # | 标题 | 技术结论 | 优先级 | 工程成本 |
|---|------|---------|--------|---------|
| 1 | SDAR | ✅ 可直接用 | P0 | 3-5人/天 |
| 2 | MemEye | 🔧 需改造 | P1 | 5-7人/天 |
| 3 | MinT | ❌ 跳过(Orwell) | — | — |
| 4 | MCP-Cosmos | ❌ 跳过(Orwell) | — | — |
| 5 | MCPShield | 🔧 需改造 | P1 | 3-4周 |
| 6 | MCP-BiFlow | 🔧 需改造 | P0 | 3-4人/周 |
| 7 | MCP Workflow Engine | ✅ 可直接用 | P0 | 1-2人/天 |
| 8 | CDD | ✅ 可直接用 | P0 | 1人/天 |
| 9 | SU-01 | ❌ 暂不可行 | P2 | 方法可用 |
| 10 | Darwin | ✅ 可直接用 | P1 | 1-2人/周 |

**优先行动项**：
1. 立刻做：#1 SDAR → izu训练管线注入sigmoid-gated OPSD
2. 立刻做：#7 MCP Workflow Engine → 实现Hermes Agent的Mediator模式
3. 立刻做：#8 CDD → izu RAG管线插入冲突检测探针
4. 本周做：#6 MCP-BiFlow → 建立MCP Server安全审计流程
5. 本周做：#10 Darwin → 从4B模型验证进化合并
6. 规划中：#5 MCPShield → 收集Hermes Agent正常/攻击会话数据
