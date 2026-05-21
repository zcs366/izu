# δ-mem: 大语言模型的高效在线记忆机制 — 全文翻译

> 原文：arXiv 2605.12357v1 [cs.AI] (2026-05-12)
> 作者：Jingdi Lei†, Di Zhang†, Junxian Li, Weida Wang, Kaixuan Fan, Xiang Liu, Qihan Liu, Xiaoteng Ma, Baian Chen, Soujanya Poria
> 机构：NTU, 复旦大学, Mind Lab, SJTU, CUHK, HKUST(GZ)
> 翻译时间：2026-05-13
> 术语注格式：**首次出现的专业术语**以**粗体**标注，括号内附原文+一句话定义。

---

## Abstract / 摘要

**原文：**
Large language models increasingly need to accumulate and reuse historical information in long-term assistants and agent systems. Simply expanding the context window is costly and often fails to ensure effective context utilization. We propose δ-mem, a lightweight memory mechanism that augments a frozen full-attention backbone with a compact online state of associative memory. δ-mem compresses past information into a fixed-size state matrix updated by delta-rule learning, and uses its readout to generate low-rank corrections to the backbone's attention computation during generation. With only an 8×8 online memory state, δ-mem improves the average score to 1.10× that of the frozen backbone and 1.15× that of the strongest non-δ-mem memory baseline. It achieves larger gains on memory-heavy benchmarks, reaching 1.31× on MemoryAgentBench and 1.20× on LoCoMo, while largely preserving general capabilities. These results show that effective memory can be realized through a compact online state directly coupled with attention computation, without full fine-tuning, backbone replacement, or explicit context extension.

**译文：**
大语言模型在长期助手和智能体系统中越来越需要积累和复用历史信息。简单地扩展上下文窗口代价高昂，且往往不能保证上下文的有效利用。我们提出 δ-mem，一种轻量级记忆机制，它在冻结的全注意力骨干（**full-attention backbone**，即使用标准自注意力机制的预训练Transformer模型，参数在训练δ-mem时保持冻结不动）之上，增加了一个紧凑的**在线联想记忆状态**（**online state of associative memory / OSAM**，一个在推理过程中随输入持续更新的固定大小矩阵，用于压缩存储历史信息）。δ-mem 将过去信息压缩为一个通过**delta规则学习**（**delta-rule learning**，一种在线学习规则，每次仅根据预测误差的残差来更新记忆状态，而非重新存储全部信息）更新的固定尺寸状态矩阵，并在生成过程中利用其读出信号生成对骨干注意力计算的**低秩修正**（**low-rank corrections**，通过低维矩阵乘积对注意力查询和输出施加微调，参数远少于完整微调）。仅凭一个 8×8 的在线记忆状态，δ-mem 的平均得分提升至冻结骨干的 1.10 倍，最强非δ-mem记忆基线的 1.15 倍。在记忆密集型基准上增益更大：MemoryAgentBench 达到 1.31 倍，LoCoMo 达到 1.20 倍，同时大体保持了通用能力。这些结果表明，有效的记忆可以通过紧凑的在线状态直接耦合注意力计算来实现，无需全量微调、替换骨干架构或显式扩展上下文。

---

## 1. Introduction / 引言

**原文：**
As large language models (LLMs) are increasingly deployed in memory-heavy scenarios requiring continuous interaction, such as long-term personalized assistants and long-horizon agent systems, their life-cycle must go beyond responding to isolated prompts and instead accumulate, update, and reuse historical information over extended memory-heavy tasks. In these settings, model performance depends not only on understanding the current input, but also on effectively leveraging relevant past context during test-time.

**译文：**
随着大语言模型越来越多地被部署在需要持续交互的记忆密集型场景中——如长期个性化助手和长周期智能体系统——其生命周期必须超越对孤立提示的响应，转而需要在漫长的记忆密集型任务中积累、更新和复用历史信息。在这些设定下，模型性能不仅取决于对当前输入的理解，还取决于在推理时有效利用相关历史上下文的能力。

**原文：**
An intuitive way is to simply expand the input context and retain more interaction history. However, this strategy only reduces the memory problem to a long-context processing problem, which is both computationally expensive and increasingly difficult to harness. On the one hand, standard attention incurs quadratic cost with respect to context length. On the other hand, simply increasing the context window does not guarantee effective use of the additional information, as models often suffer from context degradation or context rot when the context becomes very long, which suggests that even million-token context windows do not fundamentally solve the memory problem.

**译文：**
一种直觉的做法是简单地扩展输入上下文、保留更多交互历史。然而，这种策略只是把记忆问题化约为长上下文处理问题，不仅计算代价高昂，而且越来越难以有效驾驭。一方面，标准注意力的代价随上下文长度呈二次增长。另一方面，仅增加上下文窗口并不能保证有效利用额外信息——当上下文变得非常长时，模型往往遭受**上下文退化**（**context degradation / context rot**，指随着上下文越来越长，模型对其中信息的提取和利用效率反而下降的现象），这意味着即使百万token的上下文窗口也不能从根本上解决记忆问题。

**原文：**
From a unified perspective, existing memory mechanisms can be characterized along two dimensions under a given context window: memory state, which defines how historical information is stored, and memory steering, which determines how stored information influences backbone reasoning. Under this framework, prior methods fall into three paradigms...

**译文：**
从一个统一的视角来看，现有记忆机制可以在给定上下文窗口下沿两个维度来刻画：**记忆状态**（**memory state**，定义历史信息如何被存储）和**记忆引导**（**memory steering**，决定存储的信息如何影响骨干的推理）。在此框架下，先前的方法可分为三种范式：

- **文本记忆机制**（**Textual Memory Mechanisms / TMMs**）：将记忆以文本形式存储，通过输入上下文注入。灵活但受限于上下文窗口、检索噪声和压缩损失。
- **外部通道记忆机制**（**Outside-channel Memory Mechanisms / OMMs**）：记忆保持在外部模块中，通过检索或编码在外部通道上与骨干交互。模块化好但引入开销和整合复杂性。
- **参数化记忆机制**（**Parametric Memory Mechanisms / PMMs**）：将记忆编码到前缀或适配器的参数中。高效且兼容冻结骨干，但静态特性限制了其对动态演化信息的适应。

**原文：**
Following this motivation, we propose δ-mem, a memory mechanism that keeps a compact and dynamically updated memory alongside a frozen full-attention backbone. Instead of storing all historical tokens in the input context, δ-mem compresses past information into an online state of associative memory (OSAM). This state is continuously updated via delta-rule learning as new tokens arrive... During generation, δ-mem does not simply retrieve text from memory. Instead, the current input queries the online state to extract context-relevant associative memory signals, which are then transformed into a low-rank correction to the backbone's attention components.

**译文：**
基于这一动机，我们提出 δ-mem——一种在冻结全注意力骨干旁维持紧凑且动态更新记忆的机制。δ-mem 不将所有历史token存储在输入上下文中，而是将过去信息压缩为一个在线联想记忆状态。随着新token到来，该状态通过delta规则学习持续更新……在生成过程中，δ-mem并非简单地从记忆中检索文本。相反，当前输入查询在线状态以提取上下文相关的联想记忆信号，这些信号随后被转换为对骨干注意力组件的低秩修正。

**原文：**
Our contributions can be summarized as follows:
• We propose δ-mem, a memory mechanism that augments a frozen full-attention backbone with a compact online state of associative memory...
• We show that an extremely small memory state, implemented as an 8×8 matrix, can retain useful historical signals through OSAM...
• We evaluate δ-mem on multiple memory-heavy and general capability benchmarks with significant gains...

**译文：**
我们的贡献可总结如下：
• 提出δ-mem——一种用紧凑的在线联想记忆状态增强冻结全注意力骨干的记忆机制，使历史信息能被动态维持并直接耦合到骨干的注意力计算中。
• 证明一个极小的记忆状态（8×8矩阵）就能通过OSAM保留有用的历史信号，并在显式历史被移除后仍能帮助模型恢复上下文相关信息。
• 在多个记忆密集型和通用能力基准上评估δ-mem，在MemoryAgentBench和LoCoMo等任务上取得了显著增益。

---

## 2. Preliminaries / 预备知识

**原文：**
In terms of a Transformer for sequence modeling, let x∈R^{N×d} denote the input hidden sequence of a selected Transformer layer, where N is the sequence length and d is the hidden dimension... We use Q, K, V to denote the query, key, and value in attention, and use S_t to denote the online state after processing position t.

**译文：**
在用于序列建模的Transformer中，令 x∈R^{N×d} 表示选定Transformer层的输入隐藏序列，其中 N 为序列长度，d 为隐藏维度……我们用 Q、K、V 表示注意力中的查询、键和值，用 S_t 表示处理位置 t 之后的在线状态。

**原文：**
Concretely, δ-mem maintains a matrix S as the online state of associative memory. As tokens are processed, this state is updated sequentially to compactly encode key–value associations from the historical context. Given a memory key k_t ∈ R^r and value v_t ∈ R^r at position t, the state is expected to store the association k_t ↦ v_t.

**译文：**
具体而言，δ-mem维护一个矩阵 S 作为在线联想记忆状态。随着token被处理，该状态被依次更新，以紧凑地编码历史上下文中的键-值关联。给定位置 t 的记忆键 k_t ∈ R^r 和值 v_t ∈ R^r，状态被期望存储关联 k_t ↦ v_t。

**原文：**
This memory update can then be regarded as optimizing an online regression loss using SGD... This formulation writes only the residual information along the key direction. Consequently, well-learned associations induce negligible updates, whereas predictive discrepancies dynamically correct the memory state. Inspired by gated retention design in Qwen-Next, we further introduce a forget gate to control long-range state evolution:

S_t = λ_t S_{t-1} + β_t (v_t − S_{t-1} k_t) k_t^⊤

Here λ_t controls how much previous memory is retained, while β_t controls the strength of the residual write. This gated delta update forms the basis of the stable online memory dynamics in δ-mem.

**译文：**
这一记忆更新可被视为使用SGD优化一个在线回归损失……该公式仅在键方向上写入残差信息。因此，已被良好学习的关联引起极小的更新，而预测偏差则动态地修正记忆状态。受Qwen-Next中门控保留设计的启发，我们进一步引入**遗忘门**（**forget gate**，控制旧记忆保留比例的可学习门控参数 λ_t）来控制长程状态演化：

S_t = λ_t S_{t-1} + β_t (v_t − S_{t-1} k_t) k_t^⊤

其中 λ_t 控制先前的记忆被保留多少，β_t 控制残差写入的强度。这种**门控delta更新**（**gated delta update**，结合了delta规则学习和门控遗忘机制的在线状态更新方式）构成了δ-mem中稳定在线记忆动态的基础。

---

## 3. δ-mem / 核心方法

**原文：**
At each position, δ-mem follows the same computation order: read associative memory signals from the old state, use the signals to steer attention, and then write the current information into the state. In this way, the model can compress history into a state that evolves with the sequence and use it in later reasoning, without updating the backbone parameters.

**译文：**
在每个位置，δ-mem遵循相同的计算顺序：从旧状态读取联想记忆信号，用信号引导注意力，然后将当前信息写入状态。通过这种方式，模型可以将历史压缩到一个随序列演化的状态中，并在后续推理中使用它，而无需更新骨干参数。

### 3.1 Memory Projections / 记忆投影

**原文：**
To form the online state of associative memory, given a hidden state x_t ∈ R^d at the current position, δ-mem projects it into a low-dimensional associative memory space... Normalizing the query and key can reduce state instability caused by scale drift during long-sequence recurrence.

**译文：**
为形成在线联想记忆状态，给定当前位置的隐藏状态 x_t ∈ R^d，δ-mem将其投影到低维联想记忆空间（r ≪ d）……对查询和键进行归一化可以减少长序列循环过程中由尺度漂移引起的状态不稳定性。

**原文：**
The write gate and retention gate are also determined by the current hidden state: β_t = σ(W_β x_t + b), λ_t = 1 − β_t. This allows the state update to be adjusted dimension by dimension: some dimensions retain old memory, while others write the current information more actively.

**译文：**
写入门和保留门也由当前隐藏状态决定：β_t = σ(W_β x_t + b), λ_t = 1 − β_t。这使得状态更新可以逐维度调整：某些维度保留旧记忆，而其他维度则更积极地写入当前信息。

### 3.2 Reading from Online State of Associative Memory / 从在线联想记忆状态读取

**原文：**
Before writing the current information, δ-mem first reads from the old state: r_t = S_{t-1} q^m_t. The read vector r_t ∈ R^r is the result of querying the online memory state with the current input. Since the size of S_{t-1} is fixed, the cost of this step is independent of the history length.

**译文：**
在写入当前信息之前，δ-mem首先从旧状态读取：r_t = S_{t-1} q^m_t。读取向量 r_t ∈ R^r 是用当前输入查询在线记忆状态的结果。由于 S_{t-1} 的大小是固定的（r×r），这一步的代价与历史长度无关。

**原文：**
This reading form is complementary to standard attention. Attention compares the query with all keys within the explicit context, while δ-mem directly obtains continuous associative memory signals from the compressed state. It does not return text segments or add context tokens. Instead, it provides history-dependent steering signals before the attention computation.

**译文：**
这种读取形式与标准注意力互补。注意力将查询与显式上下文中的所有键进行比较，而δ-mem从压缩状态中直接获取连续的联想记忆信号。它不返回文本片段，也不添加上下文token。相反，它在注意力计算之前提供了依赖于历史的引导信号。

### 3.3 Steering Attention through Low-Rank Corrections / 通过低秩修正引导注意力

**原文：**
The associative memory signals steer the attention computation through two lightweight linear mappings. First, the read signal r_t is projected into a query-side correction and an output-side correction... The query-side correction is then added to the original query of the frozen backbone. The attention output a_t is then computed using the corrected query and the frozen backbone keys and values, while the output-side correction is added after attention.

**译文：**
联想记忆信号通过两个轻量级线性映射引导注意力计算。首先，读取信号 r_t 被投影为查询端修正和输出端修正……查询端修正随后被加到冻结骨干的原始查询上。注意力输出 a_t 随后使用修正后的查询和冻结骨干的键与值来计算，而输出端修正在注意力之后被加上。

**原文：**
The low-rank correction here is different from a static adapter. Although W^Δ_q and W^Δ_o are fixed after training, their input r_t comes from the dynamic state S_{t-1}. Therefore, the same set of parameters can produce different steering effects under different histories.

**译文：**
这里的低秩修正不同于静态适配器。虽然 W^Δ_q 和 W^Δ_o 在训练后是固定的，但它们的输入 r_t 来自动态状态 S_{t-1}。因此，同一组参数可以在不同的历史条件下产生不同的引导效果。

### 3.4 Writing into Online State of Associative Memory / 写入在线联想记忆状态

**原文：**
After the current attention computation is completed, δ-mem writes the information at the current position into the online state... The difference between the target value and this prediction defines the residual information to be written... The three terms have clear roles: the first term retains the previous state, the second term removes the old prediction component along the current key direction, and the third term writes the new value into the same direction. Thus, the memory state is updated by error correction with controlled forgetting, rather than by unselectively accumulating new outer products.

**译文：**
当前注意力计算完成后，δ-mem将当前位置的信息写入在线状态……目标值与当前预测之间的差异定义了要写入的残差信息……三项有明确的作用：第一项保留先前状态，第二项沿当前键方向移除旧的预测成分，第三项将新值写入同一方向。因此，记忆状态是通过带受控遗忘的误差修正来更新的，而非不加选择地累积新的外积。

### 3.5 Writing Granularity of Online State / 在线状态的写入粒度

**原文：**
A token is the finest granularity, but it is not always the most suitable one. In conversations and agent trajectories, messages, semantic segments, or stage-level events are often more stable. We therefore examine three writing strategies.

**译文：**
token是最细的粒度，但并非总是最合适的。在对话和智能体轨迹中，消息、语义片段或阶段级事件往往更稳定。因此，我们考察了三种写入策略：

**原文（TSW）：**
Token-State Write updates the online state at each token position. It preserves the finest-grained information and is suitable for scenarios that need to capture local changes. However, since every token triggers a write operation, the state is also more easily affected by format symbols, repeated expressions, and short-term noise.

**译文（TSW）：**
**Token状态写入**（**Token-State Write / TSW**，在每个token位置更新在线状态）保留最细粒度信息，适合需要捕捉局部变化的场景。但由于每个token都触发写入操作，状态也更容易受到格式符号、重复表达和短期噪声的影响。

**原文（SSW）：**
Sequence-State Write raises the writing granularity from unit tokens to a message segment... We first obtain the segment representation by averaging the hidden states of all tokens within this message. SSW reduces redundant writes and smooths the state evolution. The cost is that some fine-grained token-level details are absorbed by the averaged segment representation.

**译文（SSW）：**
**序列状态写入**（**Sequence-State Write / SSW**，以消息片段为单位更新在线状态）将写入粒度从单元token提升到消息片段……我们通过对消息内所有token的隐藏状态取平均来获得片段表示。SSW减少了冗余写入并平滑了状态演化。代价是某些细粒度token级细节被平均化的片段表示所吸收。

**原文（MSW）：**
Multi-State Write adjusts the state organization. A single state needs to contain facts, preferences, task progress, and local events at the same time, which may easily lead to overwriting and interference. MSW decomposes memory into multiple parallel sub-states... This organization allows different sub-states to accumulate different types of information, thereby reducing mutual interference within a single state.

**译文（MSW）：**
**多状态写入**（**Multi-State Write / MSW**，将记忆分解为多个并行的子状态，每个子状态独立更新和读取）调整了状态组织。单一状态需要同时容纳事实、偏好、任务进度和局部事件，很容易导致覆盖和干扰。MSW将记忆分解为多个并行子状态……这种组织方式允许不同子状态积累不同类型的信息，从而减少单一状态内的相互干扰。

### 3.6 Training Objective / 训练目标

**原文：**
δ-mem is trained with the standard SFT loss. For each example, the context tokens are first written into the online state, producing S_C, while they are not replayed as explicit backbone input during prediction. The frozen backbone only receives the query Q and response Y, and the stored state steers attention through δ-mem.

**译文：**
δ-mem使用标准的**监督微调**（**SFT / Supervised Fine-Tuning**，在有标注数据上进行的自回归语言建模训练）损失进行训练。对于每个样本，上下文token首先被写入在线状态以产生 S_C，而在预测过程中它们不作为显式的骨干输入被重放。冻结的骨干仅接收查询 Q 和响应 Y，存储的状态通过δ-mem引导注意力。

---

## 4. Experiments / 实验

### 4.1 Experimental Setup / 实验设置

**原文：**
We evaluate our method on general tasks and memory-heavy benchmarks... For the memory-heavy side, we utilize LoCoMo, alongside MemoryAgentBench to evaluate the retention, retrieval, and utilization of memory information across extended interaction histories.

**译文：**
我们在通用任务和记忆密集型基准上评估方法……对于记忆密集型方面，我们使用 **LoCoMo**（一个评估LLM长期对话记忆能力的基准）和 **MemoryAgentBench**（评估跨扩展交互历史的记忆信息保留、检索和利用的基准）。

**原文：**
We compare δ-mem against representative memory mechanisms. All methods are built on the same Qwen3-4B-Instruct backbone... We additionally report trainable parameter counts for rank-8 configurations to compare memory effectiveness under similar or smaller adaptation budgets.

**译文：**
我们将δ-mem与代表性记忆机制进行比较。所有方法都建立在相同的 Qwen3-4B-Instruct 骨干上……我们还报告了rank-8配置下的可训练参数量，以在相似或更小的适配预算下比较记忆效果。

### 4.2 Main Results / 主要结果

**原文（核心结果）：**
δ-mem achieves the strongest performance across all methods. The TSW variant reaches the best average score of 51.66%, improving over the Qwen3-4B-Instruct backbone (46.79%) by +4.87 points and over Context2LoRA (44.90%) by +6.76 points... On MemoryAgentBench, δ-mem improves the average score from 29.54% to 38.85%, with MSW performing best. On LoCoMo, MSW achieves the highest average of 49.12%.

**译文（核心结果）：**
δ-mem在所有方法中取得了最强的性能。TSW变体达到最佳平均分51.66%，较Qwen3-4B-Instruct骨干（46.79%）提升+4.87分，较Context2LoRA（44.90%）提升+6.76分……在MemoryAgentBench上，δ-mem将平均分从29.54%提升至38.85%，MSW表现最佳。在LoCoMo上，MSW达到最高平均分49.12%。

**原文（基线对比）：**
Across baselines, different memory mechanisms exhibit distinct limitations. Textual memory methods show inconsistent gains, likely due to retrieval noise and information loss. Parametric memory methods such as Context2LoRA tend to generalize less robustly across tasks, as their memory is statically encoded in parameters. The MLP Memory baseline performs relatively limited...

**译文（基线对比）：**
不同基线展现了各自的局限性。文本记忆方法增益不一致，可能由于检索噪声和信息损失。参数化记忆方法（如Context2LoRA）跨任务的泛化不够稳健，因为其记忆被静态编码在参数中。MLP Memory基线的表现相对有限……

### 4.3 Cross-Backbone Results / 跨骨架结果

**原文：**
δ-mem improves the average score on all backbones. Specifically, it boosts Qwen3-4B-Instruct from 46.79% to 51.66%, Qwen3-8B from 47.20% to 50.86%, and SmolLM3-3B from 26.08% to 36.96%. Notably, the effectiveness of the writing strategies varies by model capacity. On the more capable Qwen3-8B... segment-level writing (SSW) smooths state updates... In contrast, the smaller SmolLM3-3B exhibits a substantial performance leap driven by MSW, indicating that smaller backbones benefit significantly from separating memory into multiple states to minimize interference.

**译文：**
δ-mem在所有骨架上均提升了平均分：Qwen3-4B-Instruct从46.79%到51.66%，Qwen3-8B从47.20%到50.86%，SmolLM3-3B从26.08%到36.96%。值得注意的是，写入策略的效果随模型容量而变化。在能力更强的Qwen3-8B上，SSW通过平滑状态更新效果最好……而在较小的SmolLM3-3B上，MSW带来了大幅跃升，表明小骨架从将记忆分离为多状态以减少干扰中获益显著。

---

## 5. Ablative Study / 消融研究

### 5.1 Context Recovery / 上下文恢复

**原文：**
To examine whether the online state of associative memory can preserve useful historical information without explicit context replay, we evaluate δ-mem under a no-context setting, where the original historical context is removed and only the compressed memory state is injected... On HotpotQA, the overall EM increases from 0.08% to 6.48%, and the overall F1 improves from 8.27% to 15.20%. The gains are especially large on the Bridge subset... On LoCoMo, δ-mem also improves the overall average from 3.49% to 8.05%.

**译文：**
为检验在线联想记忆状态能否在无显式上下文回放的条件下保留有用的历史信息，我们在无上下文设置下评估δ-mem——原始历史上下文被移除，仅注入压缩的记忆状态。在HotpotQA上，整体EM从0.08%提升至6.48%，整体F1从8.27%提升至15.20%。Bridge子集增益尤其显著……在LoCoMo上，δ-mem也将整体平均分从3.49%提升至8.05%。

### 5.2 Heads Ablation / 注意力头消融

**原文：**
We first study where the memory-induced correction should be injected within the attention block... Among single-branch variants, the output branch performs best... The full qkvo configuration achieves the best average score of 48.05%. While qkvo yields the highest average score, its marginal gain over qo does not justify the extra parameter overhead. Thus, we default to qo for an optimal performance-efficiency trade-off.

**译文：**
我们首先研究记忆引导的修正应注入注意力块的哪个位置……在单分支变体中，输出分支表现最佳……完整qkvo配置达到最佳平均分48.05%。虽然qkvo取得了最高平均分，但其相对于qo的边际增益不足以证明额外参数开销的合理性。因此我们默认选择qo以实现性能-效率的最优平衡。

### 5.3 Insertion Depth Ablation / 插入深度消融

**原文：**
Applying memory correction to all layers achieves the best overall performance... Among partial-layer variants, the middle-layer configuration performs best... This indicates that intermediate layers provide a particularly effective interface for memory injection, balancing semantic abstraction and task-specific computation.

**译文：**
在所有层施加记忆修正取得了最佳整体性能……在部分层变体中，中间层配置表现最佳……这表明中间层为记忆注入提供了特别有效的接口，平衡了语义抽象和任务特定计算。

---

## 6. Related Work / 相关工作

（三条线：文本记忆→外部通道记忆→参数化记忆。核心区分点已在前文引言中翻译，此处不再重复。）

δ-mem与LoRA的关键差异：LoRA的低秩更新是静态的——训练完成后ΔW固定不变；δ-mem的低秩注意力修正来自运行时动态演化的在线状态 S_{t-1}，同一组参数在不同历史下产生不同的引导效果。δ-mem是**状态条件化**（state-conditioned）的记忆，而非行为上的持久修改。

---

## 7. Conclusion / 结论

**原文：**
In this work, we introduced δ-mem, a lightweight memory mechanism that equips a frozen full-attention backbone with a compact and dynamically updated online state of associative memory... Empirically, δ-mem improves performance on memory-heavy benchmarks while largely preserving the general capabilities of the frozen backbone. Notably, even with an extremely small 8×8 online state, the model can recover useful historical information after explicit context is removed, showing that effective memory does not require extending explicit context or heavy external retrieval modules.

**译文：**
在本文中，我们引入了δ-mem——一种轻量级记忆机制，为冻结的全注意力骨干配备了一个紧凑且动态更新的在线联想记忆状态……实验表明，δ-mem在记忆密集型基准上提升了性能，同时大体保留了冻结骨干的通用能力。尤其值得注意的是，即使仅使用一个极小的8×8在线状态，模型也能在显式上下文被移除后恢复有用的历史信息，表明有效记忆并不需要扩展显式上下文或依赖重型外部检索模块。

---

## 附录要点

- **训练设置**：在QASPER数据集的2,219个最短样本上训练1个epoch，骨干序列长度512，记忆写入预算8,192 tokens。r=8, α=16。8×A800 GPU，bf16精度，DeepSpeed ZeRO-2。学习率2×10⁻⁴，cosine衰减。
- **推理效率**：δ-mem GPU内存使用接近Vanilla和Context2LoRA，远优于MLP Memory和MemGen。解码吞吐量略低于Vanilla（因每步需读写状态），但显著快于MemGen。
- **参数开销**：TSW/SSW仅4.87M（0.12%骨干），MSW仅19.47M（0.48%骨干）。对比MemGen 46.20M、MLP Memory 3078M。
