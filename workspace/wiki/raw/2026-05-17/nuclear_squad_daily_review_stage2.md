**此文件由鲁班+匠石+Newton+Edison在2026-05-17 08:36生成**

---

# 核战队日报审阅 Stage 2：技术评审

## 评审框架

| 角色 | 职能 | 权重 |
|------|------|------|
| **鲁班（主）** | 技术落地判断：哪些能用？怎么改？ | 最终决策 |
| **匠石** | 代码vs模型判断：哪些直接编码落地？哪些需要训练/推理模型？ | 工程可行性 |
| **Newton** | 挖根检查：有没有被忽略的深层问题？方法学缺陷？ | 风险揭示 |
| **Edison** | 可复现性验证：哪些结果可信？哪些可能造假？ | 实验可信度 |

---

## Orwell预筛结果（简要判断）

- ❌ **MinT (#3)** — 重复劳动，已有Ray Serve/vLLM/K8s成熟方案。跳过深度评审。
- ❌ **MCP Workflow Engine (#7)** — 伪深度，99%+ token节省数学不可能（除非baseline是逐token全量LLM调用）。跳过深度评审。
- ⚠️ **SDAR (#1)** — 重复劳动嫌疑，self-play+RL已有大量工作。给出简短判断，跳过完整深度评审。

---

## 1. SDAR (Self-Distilled Agentic RL) — ⚠️ 预筛标记，简短判断

**鲁班判断**：自蒸馏（behavior cloning自己轨迹）+ RL的组合，缺乏真实环境交互下RL部分无意义。Hermes Agent已有多轮推理能力，SDAR的方案不提供增量价值。**不落地**。

**匠石判断**：纯代码落地，无需专门模型训练。但如果要复现，需要搭建环境循环+轨迹采集+蒸馏训练的pipeline，工程成本高而收益低。

**Newton挖根**：被忽略的深层问题——SDAR假设智能体的自采样轨迹包含正确的、可学习的改进信号。但在没有外部奖励或环境反馈的情况下，自蒸馏只是强化已有偏差（self-reinforcing bias loop）。RL部分若无ground-truth reward signal，Q值估计会飘移到荒谬值。

**Edison验证**：HF 77票，无公开代码复现。自蒸馏结果高度依赖初始化质量和采样多样性，难以在论文中诚实报告——论文中呈现的改进可能是随机种子选择的结果。

**综合**：❌ 不投入。框架层面的重复构建是token浪费。

---

## 2. MemEye — 多模态Agent记忆视觉中心评估框架

**鲁班判断**：直接可用。Hermes Agent和izu的memory system需要视觉记忆保真度评估。建议做两件事：
1. **代码落地**（匠石方向）：将MemEye的评估pipeline直接集成到izu的memory evaluation bench中。
2. **模型适配**：如果测评发现视觉记忆中关键项丢失，可能需要微调VL encoder或增加caption正则化。

具体做法：
- 提取MemEye的评估指标：visual fidelity score, recall precision, confabulation rate
- 在izu的memory eval中新增visual modality测试套件
- 不需要完整复现MemEye框架，取方法论即可

**匠石判断**：
- **可代码落地（80%）**：评估pipeline的逻辑是templated + metric计算，直接写Python类即可。需要：
  - 定义测试视觉场景（合成图 + 真实截图）
  - 自动化注入Agent memory → 查询 → 比较输入输出
  - metric计算（BLEU/ROUGE变体 + 语义相似度 + 视觉元素匹配率）
- **需要模型调用（20%）**：评估本身需要VL模型提取ground truth，但这是一次性的预标注工作

**Newton挖根**：
- 深层问题 #1：视觉记忆保真度评估的ground truth定义本身是哲学问题——"看到"的视觉信息量远超文本可表达。MemEye的评估必然损失信息，评估的是"文本化后的视觉记忆"而非真正的视觉记忆。
- 深层问题 #2：NVIDIA可能用自家视觉模型做evaluator，对开源VL模型（Qwen2-VL, LLaVA）有bias。若我们使用不同VL模型，评估结果可能系统性偏离。
- 深层问题 #3：评估集规模未知。小样本（<500 cases）得到的confabulation rate统计不可靠。

**Edison验证**：
- NVIDIA出品 → 代码和数据通常会公开，复现可能性中高
- 关键验证点：论文中的evaluator是否独立于被测试的memory system？如果两者是同一个模型系列，有self-serving bias
- 需要复现的指标：visual fidelity score在不同query类型（事实型vs开放型）上的分布

**综合**：✅ 可行，P0优先。建议：
1. 先实现评估pipeline代码（匠石落地）
2. 在自己的模型上run一遍baseline
3. 根据结果决定是否调整memory system设计
4. 注意：不要过度依赖MemEye的绝对分数，关注相对改进

---

## 3. MinT (#3) — ❌ 预筛标记，简短判断

**鲁班判断**：已有的Kubernetes + Ray + vLLM生态完全覆盖MinT声称的功能。当前izu/Hermes Agent规模远未到"百万级"需求。**不落地、不跟踪**。

**Newton挖根**：HF 205票周榜#1暗示的可能是"运维痛点"，但MinT的方案若仅仅是编排层包装，则LLM集群运维中最难的网络拓扑优化/通信调度/故障恢复等问题都没解决。

**综合**：❌ 跳过。

---

## 4. MCP-Cosmos — 世界模型增强的MCP环境Agent

**鲁班判断**：直接相关，但需要谨慎评估工程可行性。核心建议：
- **代码落地（60%）**：MCP tool call planning中加入可选的world model predictive layer。具体：
  1. 在Hermes Agent的MCP tool executor中插入一个pre-invocation分析点
  2. 在此分析点中，轻量world model预测tool call的可能effect/outcome
  3. 如果预测到危险/不一致的结果，阻止或修改调用
- **需要模型（40%）**：world model本身需要训练或依赖已有模型。有两种路线：
  - 路线A（轻量）：用prompt engineering让通用LLM做"mental simulation" → 代码即可，不需额外模型
  - 路线B（重）：训练专用world model → 需要izi项目投入训练资源

**匠石判断**：
- **立即可以做（代码落地）**：MCP tool call的pre-invocation分析hook，用一个结构化prompt让现有模型（Hermes Agent本身或izu model）做mental simulation。这是工程钩子+prompt engineering，不依赖新模型。
- **需要模型（长期）**：真正的world model（可对tool调用的输出做概率预测）需要训练。建议短期内用路线A，观测效果后再决定是否走路线B。
- 工程成本：路线A约3-5个工作日实现集成。

**Newton挖根**：
- 深层问题 #1：世界模型的多步预测误差累积。MCP tool call链可能很长，单步预测准确率即使90%，10步后accuracy ≈ 35%。论文可能只报告了单步或短链结果。
- 深层问题 #2：世界模型泛化性——对于未见过的MCP tool（新API），world model必须做zero-shot预测，这可能退化到纯prompt-based reasoning，失去"模型"的优势。
- 深层问题 #3：MCP-Cosmos是否解决了OOD（out-of-distribution）的tool call序列？真实agent行为中，tool调用序列的分布与训练数据不同，world model的校准会偏移。

**Edison验证**：
- 论文未公开benchmark → 效应量未知。这是最大红牌。
- 可复现的关键指标：world model的next-state prediction accuracy vs. 无模型baseline
- 怀疑：如果做了fair comparison（same LLM without world model vs. with world model），改进幅度可能很小（<5%）
- 建议：我们自己做ablation study，在Izou内部先用路线A，测量tool call成功率变化

**综合**：✅ 跟踪但不要依赖。P1优先级合理。建议行动：
1. 本周：实现MCP tool pre-invocation analysis hook（代码落地）
2. 用路线A（prompt-based mental simulation）跑一轮实验
3. 如果发现显著改进（>10% tool call success rate），再考虑路线B

---

## 5. MCPShield — MCP工具调用流量攻击检测，GNN，AUROC 0.975

**鲁班判断**：安全框架，当前不紧急但未来必须。MCPShield的GNN架构本身不复杂，核心是特征工程和数据集质量。
- **代码落地（90%）**：安全检测框架本质上是分类器 -> log data collection -> feature extraction -> GNN inference。工程上可copy architecture。
- **需要模型（10%）**：GNN模型训练。但训练一次后部署推理，不需要在线训练。

具体做法：
1. 提取MCPShield的特征设计（节点特征：tool call参数类型/长度/熵；边特征：调用顺序/间隔）
2. 在我们的MCP调用日志上复现特征提取逻辑
3. 用简单替代模型（XGBoost/Logistic Regression）先评估baseline

**匠石判断**：
- **核心代码落地**：MCP traffic logging + feature extraction pipeline可以在2-3天内写出
- 安全问题特殊——不需要完美检测，需要低误报率。AUROC 0.975如果是真实数据训练的，误报率可能仍然无法接受（安全领域FP率要求 < 0.1%）
- 建议：先做logging layer（这本身就有价值），模型训练等积累足够数据后再做

**Newton挖根**：
- 深层问题 #1：AUROC 0.975是实验环境下的数字。真实MCP tool调用分布是极度不平衡的（>99.9%正常调用），在这个分布下AUROC会大幅下降。
- 深层问题 #2：攻击类型定义的完备性。MCPShield覆盖了已知的攻击模式（injection, path traversal, SSRF等），但零日攻击（novel attack patterns）必然miss。GNN在OOD检测上表现通常不佳。
- 深层问题 #3：图构造方式。如果图构造粒度是"per-session"，GNN需要处理不同长度的序列——长序列的图太大，短序列的图信息不足。

**Edison验证**：
- AUROC 0.975需要查看完整confusion matrix（TPR, FPR, precision-recall curve）。安全论文常只报AUROC不报FPR@TPR=0.95这种工程指标。
- 需要检查测试集的attack ratio——如果test set是50% normal / 50% attack（常见做法），AUROC会虚高。
- 我们的validation计划：用MCP-BiFlow发现的87个真实漏洞构造测试集，看MCPShield的方案能否检出。

**综合**：✅ P2合理。建议：
1. P0/P1任务完成后，花2天做logging layer
2. 先不用GNN，XGBoost baseline足够
3. 等自身MCP流量积累到一定量级后再评估是否需要复杂模型

---

## 6. MCP-BiFlow — MCP生态双向数据流风险分析

**鲁班判断**：**本周最高优先级论文（和鲁班的工程直觉完全吻合）**。这不是"论文"而是安全审计报告——直接产出产品安全checklist。
- **纯代码落地（100%）**：不需要任何模型。只需要：
  1. 解析87个漏洞的CWE分类和攻击模式
  2. 映射到Hermes Agent的MCP tool使用场景
  3. 产出安全rules + automated scanning script
- 这是本周必须产出的交付物：一份直接可执行的MCP安全checklist + 对应测试case

具体行动方案：
1. 通读MCP-BiFlow全文（已标记必须读）
2. 提取87个漏洞的类型分布（命令注入、路径遍历、SSRF、prompt泄露等）
3. 对每种类型，写出Hermes Agent的对应防护策略
4. 自动化测试：对izu的MCP tool sandbox跑一遍这87个模式的测试case

**匠石判断**：
- **工程产出类型**：安全规则库（YAML/JSON）+ 自动化测试脚本（Python/pytest）+ CI gate
- 完全不需要模型推理，纯逻辑规则和正则匹配即可
- 漏洞复现需要搭建demo环境，但这是工程测试的常规操作
- 产出交付形式：
  - `mcp_security_rules.yaml` — 87个漏洞的检测规则
  - `test_mcp_vulnerabilities.py` — 自动化测试套件
  - `MCP_SECURITY_CHECKLIST.md` — 开发人员手册
- 工程成本估算：2-3天完成核心工作

**Newton挖根**：
- 深层问题 #1（重要）：15,452仓库扫描的完整性和假阳性率。论文声称发现87个漏洞，但未报告FP率。如果FP率很高（>20%），实际新的漏洞可能远少于87。
- 深层问题 #2：扫描工具的局限性。MCP-BiFlow的审计工具可能只覆盖了某些协议层（如HTTP transport），对stdin/stdio transport的覆盖不足。缺失的漏洞可能比发现的更多。
- 深层问题 #3（关键）：时间敏感性。MCP生态在快速变化，87个漏洞中的一部分可能已经被修复（论文到我们阅读的时间差）。需要检查是否存在already-patched的情况。
- 深层问题 #4：扫描方法的报告缺乏——没有详细说明使用的静态分析规则、动态测试用例、扫描工具的版本。这使得独立复现困难。

**Edison验证**：
- 15,452仓库的扫描是可复现的（如果工具公开），但审计结果的验证需要人工检查每个漏洞。
- 如果论文只展示了漏洞摘要而非完整case-by-case报告，可复现性评审会说"results partially reproducible"
- 我们的最佳策略：不试图完全复现扫描，而是提取方法论和漏洞类型学，在自己的代码库上运行类似扫描

**综合**：✅ **P0行动**。这是核战队本周最有工程价值的论文。交付物：
1. 安全规则库（~2天）
2. 自动化测试套件（~1天）
3. 直接提升izu MCP tool sandbox的安全性

---

## 7. MCP Workflow Engine (#7) — ❌ 预筛标记，简短判断

**鲁班判断**：智能与执行分离是软件工程常识（IoC/MVC），包装成"引擎"是换皮。99%+ token节省的声明意味着：要么baseline选了最简单的case，要么计算方法是"不调用LLM时节省100%"。**不落地**。

**Newton挖根**：99%+ token节省需要仔细看分母——如果分母是"每次LLM调用的所有token"，而分子是"跳过推理节省的token"，那么即使用较长的prompt只推理一个token，节省也不会超过50%。数学上不可能达到99%+。

**综合**：❌ 跳过。概念（workflow template）有借鉴价值，但不需要读这篇论文——复用已有设计模式即可。

---

## 8. Does RAG Know — RAG知识冲突下上下文合规诊断，CDD探针

**鲁班判断**：**直接用于Wiki知识系统（P1项目）**。CDD探针解决的是RAG系统的根本问题：当检索结果与模型固有知识冲突时，模型选择信任谁。
- **纯代码落地（95%）**：CDD探针的构造是一套systematic prompt template + evaluation metrics。仅有5%需要LLM调用（执行探针查询）。
- 不需要训练新模型，也不需要微调。

具体行动方案：
1. 构造CDD探针测试集（在Wiki知识系统领域——从知识库中选取常见topic + 人工制造冲突）
   - 冲突类型A：检索文档A有信息x，检索文档B有信息y（x≠y）→ 模型应综合或标注矛盾
   - 冲突类型B：检索文档有信息x，模型世界知识有 ¬x → 模型应遵循context
   - 冲突类型C：检索文档中的信息与query无关 → 模型应识别并忽略
2. 在Hermes Agent + Wiki知识系统上跑CDD探针
3. 如果发现Agent频繁忽略上下文而依赖世界知识，则需要调整system prompt或retrieval reranking策略

**匠石判断**：
- 工作量估算（精细化）：
  - 开发CDD探针框架（Python类 + prompt templates）: ~1天
  - 构造领域测试集: ~1天（半自动生成 + 人工校对）
  - 运行评估、分析结果: ~0.5天
  - 修复Agent行为（如prompt tuning）: ~0.5天
- 总计：~3天，一个人完成
- 完全不需要模型训练，也不需要GPU

**Newton挖根**：
- 深层问题 #1：CDD探针假设"上下文应该优于世界知识"——但这是有争议的。如果RAG检索到一篇质量低劣或过时的文档，模型坚持按照它的世界知识（训练时学习的）可能是正确行为。CDD无法区分"正确的上下文无视"和"合理的上下文无视"。
- 深层问题 #2：CDD探针的构造依赖人工标注的"正确答案"。对于知识冲突场景，ground truth本身可能不存在（两个来源都有权威性）。这导致evaluation metric的客观性下降。
- 深层问题 #3：LLM-as-judge用于CDD评估时，存在judge bias——如果judge和被测模型是同一个模型系列，评估结果倾向于"支持"模型的无视行为。

**Edison验证**：
- Does RAG Know论文可能公开了探针测试集 → 可以直接在我们的系统上跑
- 关键验证：我们自己构造的测试集上，模型行为是否与论文报告的分布一致？如果差异大，说明论文的测试集有偏（可能选了模型表现最差/最好的case）
- 验证计划：先用论文原测试集跑一遍（如果公开），再用自己的领域测试集跑一遍，对比两组结果

**综合**：✅ **P1立即行动**。核心价值是诊断工具，不是修复方案。先用CDD发现问题，再根据问题类型制定修复策略。注意不要过度信任CDD的"ground truth"。

---

## 9. SU-01 — 金牌级奥赛推理，30B-A3B，反向困惑度课程+两阶段RL

**鲁班判断**：技术创新有启发性，但直接落地的门槛高。
- **需要模型训练**（匠石判断：90%模型 + 10%代码）：反向困惑度课程（逆序课程学习）+ 两阶段RL需要完整的训练pipeline
- 但是可以提取可落地的**工程启发**：
  1. **阶段一：反向困惑度课程** → 训练时先用高难度样本，再用低难度样本微调。这个策略可以直接在izu的RL训练pipeline中实验——先做reward tuning，再改curriculum scheduling逻辑。
  2. **阶段二：两阶段RL** → 第一阶段探索多样化策略，第二阶段聚焦最优策略。可以借鉴phase scheduler的设计。

**匠石判断**：
- **直接落地不可行**：SU-01的30B-A3B MoE架构训练需要大量算力（估计> 1000 GPU-hours），超出当前项目预算
- **可借鉴但不复制**：
  - 反向困惑度课程的实现：在izu的RL trainer中新增data sampler，支持从高loss样本到低loss样本的调度
  - 两阶段RL的切换逻辑：基于探索率 / reward plateau检测的phase transition
- 工程成本：实现curriculum sampler + phase scheduler ~ 2-3天
- 验证成本：跑一轮RL实验 ~ 数十到上百 GPU-hours

**Newton挖根**：
- 深层问题 #1（严重）："反向困惑度课程"的本质是什么？困惑度低表示模型自信（简单样本），困惑度高表示模型不确定（困难样本）。从困难到简单的课程相当于先做hard negative mining再做fine-tuning——这在RL中可能导致早期的不稳定崩溃（divergence）。论文如何防止早期崩溃？
- 深层问题 #2：金牌级奥赛推理 → narrow domain specialization。SU-01可能在IMO/Gaokao等benchmark上表现优异，但general reasoning能力可能受损。需要看论文是否报告了通用benchmark（MMLU, GSM8K, HumanEval等）的退化。
- 深层问题 #3：30B-A3B的MoE架构中，expert分配策略是什么？如果expert specialize在不同的推理类型上，反向课程可能破坏已经形成的expert specialization。

**Edison验证**：
- 关键复现问题：SU-01的训练细节是否充分公开？
  - MoE架构的expert数量、top-k值、router mechanism？
  - RL训练的reward model设计？是learnt RM还是rule-based RM？
  - 课程学习的pacing schedule（多快从easy切换到hard）？
- 如果这些细节缺少，论文的复现可信度为低
- 建议关注的方向：如果论文在ArXiv上且有代码仓库，可以等代码release后再深入评估

**综合**：✅ P2合理。建议：
1. 不要尝试复制SU-01训练（算力不够且风险高）
2. 提取curriculum scheduling idea，在izu较小的setting下实验
3. MoE架构的记录留存——如果未来izu需要扩展到MoE，SU-01的design choices有参考价值

---

## 10. Darwin Family — 进化式模型合并，无训练扩展推理，GPQA #6

**鲁班判断**：模型合并是低成本提升模型能力的好方法，但非战略方向。
- **代码落地（70%）** + **需要模型（30%）**：进化式合并的框架代码（genetic algorithm over model merge configurations）可以写。但需要多个base模型才能合并。
- 当前Hermes Agent只维护一个主模型版本 → 没有多模型可供合并。
- 但是可以作为**serving optimization**的备用方案：当需要快速迭代模型版本时，用进化合并替代完整的finetune，节省训练成本。

**匠石判断**：
- 工程落地路径：
  1. 实现进化合并框架（基于现有model soup库）：~2天
  2. 收集多个finetune checkpoint（不同RL阶段、不同seed、不同数据配比）
  3. 运行进化搜索找到最优合并权重
  4. 评估合并模型 vs. 原始模型
- 不需要训练，只需要推理和评估 → 成本低
- 适用场景：
  - 快速组装prototype模型
  - 在不训练的情况下修复某个benchmark的缺陷
  - 探索不同训练策略的组合效果

**Newton挖根**：
- 深层问题 #1：进化合并的搜索空间爆炸。如果有N个模型，M种合并算法（linear, TIES, DARE, etc.），搜索空间是巨大的。Darwin用什么策略控制搜索？如果只是random search + 有限轮次，结果不可靠。
- 深层问题 #2：GPQA #6的位置——前5名是哪些模型？如果前5名都是单个大幅finetune的模型（如Claude, GPT-4变体），那#6的位置含金量高。如果前5名也是合并模型，那这只是"合并竞赛"的佐证，而非突破。
- 深层问题 #3：合并后的模型的可解释性和可控性下降。如果合并后的模型在某个测试case上表现异常（如突然有偏见输出），很难归因到哪个父模型的问题。

**Edison验证**：
- 进化合并的结果具有高度随机性：不同seed的进化搜索产生不同合并结果
- 论文需要报告多组结果（mean ± std）而非单一best result
- 如果只报告一次实验的最好结果，可复现性极低
- 我们的验证策略：用公开的model merge library（mergekit）复现Darwin的进化搜索，看是否能得到接近的GPQA分数

**综合**：✅ P2合理。建议：
1. 先实现mergekit-based进化合并框架（代码复用度高）
2. 等izu有2-3个有意义的checkpoint后再跑合并实验
3. 作为辅助工具，不做主力投入

---

## 各论文技术评审汇总

| # | 论文 | 鲁班判断 | 匠石判断（代码/模型比） | Newton挖根（深层问题数） | Edison验证 | 综合 |
|---|------|----------|------------------------|--------------------------|------------|------|
| 1 | SDAR | ❌ 不投入 | 代码即可，不值做 | 1个严重(self-reinforcing bias) | 不可复现(无公开代码) | ❌ |
| 2 | MemEye | ✅ P0：集成评估pipeline | 80%代码+20%模型 | 3个(ground truth定义/evaluator bias/样本量) | 中高可复现 | ✅ |
| 3 | MinT | ❌ 跳过 | — | 跳过(Orwell预筛) | — | ❌ |
| 4 | MCP-Cosmos | ✅ P1跟踪：先路线A | 60%代码+40%模型 → 路线A 95%代码 | 3个(误差累积/泛化/OOD) | 低(无公开benchmark) | ⚠️ 跟踪 |
| 5 | MCPShield | ✅ P2准备 | 90%代码+10%模型 | 3个(AUROC虚高/零日检测/图构造) | 中(需全confusion matrix) | ✅ P2 |
| 6 | MCP-BiFlow | ✅ **P0本周**：安全checklist | 100%纯代码 | 4个(FP率/扫描覆盖/时效性/方法细节) | 部分可复现 | ✅ **P0** |
| 7 | MCP Workflow Engine | ❌ 跳过 | — | 跳过(Orwell预筛) | — | ❌ |
| 8 | Does RAG Know | ✅ **P1立即**：CDD诊断 | 95%代码+5%LLM调用 | 3个(ground truth争议/judge bias/领域适配) | 高(测试集可能公开) | ✅ **P1** |
| 9 | SU-01 | ✅ P2启发 | 10%代码+90%模型 | 3个(训练不稳定/narrow specialization/expert分配) | 低(细节不充分) | ✅ P2启发 |
| 10 | Darwin Family | ✅ P2备用 | 70%代码+30%模型 | 3个(搜索爆炸/排名含金量/可解释性) | 低(随机性高) | ✅ P2 |

---

## 行动级联（按本周可执行性排序）

### 🚀 立即开始（P0 — 本周第1-2天）

**任务1: MCP-BiFlow安全审计落地**（鲁班主推）
- 产出：`mcp_security_rules.yaml` + `test_mcp_vulnerabilities.py` + `MCP_SECURITY_CHECKLIST.md`
- 责任人：鲁班 + 匠石（纯代码落地）
- 工时：2-3天
- 依赖：无

**任务2: MemEye视觉记忆评估pipeline**（鲁班主推）
- 产出：izu memory evaluation bench新增visual modality测试套件
- 责任人：匠石（80%代码）+ 鲁班（20%评估指标选择）
- 工时：2-3天
- 依赖：izu memory system已有框架

**任务3: CDD探针诊断Wiki知识系统**（鲁班主推）
- 产出：CDD探针框架代码 + 领域测试集 + 诊断报告
- 责任人：匠石（探针代码）+ 鲁班（结果分析）
- 工时：2-3天
- 依赖：Wiki知识系统P1项目已部署

### 📅 本周跟进（P1 — 本周第3-5天）

**任务4: MCP-Cosmos路线A实验**
- 产出：MCP tool pre-invocation hook + prompt-based mental simulation
- 责任人：匠石（工程钩子）+ 鲁班（实验设计）
- 工时：2天

**任务5: MCPShield logging layer**
- 产出：MCP调用日志收集组件 + 特征提取pipeline
- 责任人：匠石
- 工时：1-2天

### 📋 本月跟进（P2）

**任务6: SU-01反向课程学习实验**（izu RL trainer改造）
**任务7: Darwin Family合并框架**（mergekit集成）
**任务8: MCPShield GNN模型训练**（依赖足够的MCP日志积累）

---

## 关键技术风险总览

| 风险 | 来源 | 严重程度 | 缓解措施 |
|------|------|----------|----------|
| CDD ground truth争议 | #8 Newton | 中 | 不做绝对判断，只报告"遵从上下文的比例"而非"正确率" |
| MCP-Cosmos误差累积 | #4 Newton | 高 | 先用路线A，只做单步prediction，不做多步 |
| SU-01训练不稳定 | #9 Newton | 高 | 不在缺失细节时尝试复现，只取课程学习思想 |
| Darwin搜索爆炸 | #10 Newton | 中 | 有限搜索（N<5模型，M<3算法，<100轮） |
| MCP-BiFlow漏洞时效性 | #6 Newton | 中 | 扫描当前版本代码库确认漏洞状态 |
| MemEye evaluator bias | #2 Newton | 低 | 使用独立evaluator（不同模型系列） |

---

## 技术评审结论

**可以直接用的技术（本周可落地）**：
1. ✅ **MCP-BiFlow (#6)** — 安全规则库+测试套件，纯代码产出
2. ✅ **MemEye (#2)** — 视觉记忆评估pipeline，代码+少量模型调用
3. ✅ **Does RAG Know (#8)** — CDD诊断探针，纯代码+LLM推理

**需要造装备/训练模型的技术（本月可准备）**：
4. ⚠️ **MCP-Cosmos (#4)** — 路线A（prompt预测）可快速实现，路线B（world model训练）需延期
5. ⚠️ **MCPShield (#5)** — 先做logging+特征提取，等数据量够再训练GNN
6. ⚠️ **SU-01 (#9)** — 提取反向课程思想，不要尝试复制训练
7. ⚠️ **Darwin Family (#10)** — 实现合并框架，等有多个checkpoint再跑

**不投入的技术**：
8. ❌ SDAR (#1) — self-reinforcing bias风险
9. ❌ MinT (#3) — 已有成熟方案
10. ❌ MCP Workflow Engine (#7) — 数学不可能声明

---

## 一周技术产出日历建议

| 天 | 上午 | 下午 |
|----|------|------|
| **Day 1** | MCP-BiFlow漏洞解析+规则分类 | CDD探针框架代码 |
| **Day 2** | MCP-BiFlow测试套件实现 | MemEye评估pipeline代码 |
| **Day 3** | CDD探针+Wiki知识系统测试 | MemEye评估运行+结果分析 |
| **Day 4** | MCP-Cosmos路线A: pre-invocation hook | MCPShield: logging layer |
| **Day 5** | 整合所有产出+文档 | 回顾+调整下周计划 |

---

*评审完成时间：2026-05-17 08:36*
*四位一体签名：鲁班 + 匠石 + Newton + Edison*
