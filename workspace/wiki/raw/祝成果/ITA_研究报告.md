# ITA研究报告：LLM在科学推理与自主研究中的边界与潜力

## 研究问题
What are the current limits and future potential of large language models in scientific reasoning and autonomous research?

## 3个关键洞察
1. LLMs can now automate the full research cycle, but their outputs remain shallow — they optimize within known paradigms rather than discovering new ones.
2. The field is converging on a "co-scientist" model rather than full autonomy, with a three-level taxonomy of LLM roles (Tool → Analyst → Scientist) mapping the trajectory.
3. The missing piece is a "world model" with physical grounding — without real experiment feedback loops, LLM-based scientists will remain trapped in text-space reasoning.

## ITA 6轮合议摘要

### Round 0 — 惠施（概念澄清）
- 元认知≠自我意识≠情境意识：元认知是可测量的功能性能力，自我意识涉及主观体验且AI无证据具备，情境意识是对环境的感知
- 物理自修复（确定性修复）≠认知自修复（概率性修复）
- "修复"的统一定义：偏离检测(诊断)→回归机制(修复)→功能恢复验证
- "具有自我诊断和自我修复能力的自主系统"本质是工程上的系统内部反馈回路

### Round 1 — 墨子（形式化验证）
- 核心假设H1：增强世界模型和实验反馈可提升LLM科学能力（可证伪性：高）
- 核心假设H2：元认知是认知自修复必要条件（可证伪性：中）
- 核心假设H3：统一框架可产生协同效应（可证伪性：低）
- 张力发现：渐进创新(W+E充分) vs 范式突破(需额外机制)，但后续实验未覆盖范式突破

### Round 2 — 商鞅（实验设计）
- 实验1：世界模型对科学推理质量影响（物理模拟器LLM vs 纯文本LLM）
- 实验2：元认知校准对认知自修复影响（有/无元认知模块）
- 实验3：物理自修复电路可靠性验证（微流体+液态金属在模拟空间环境）

### Round 3 — 鲁班（工程可行性初评）
- 实验1 TRL 3-4（可行，评估标准需设计）
- 实验2 TRL 4-5（可行，元认知模块是关键创新）
- 实验3 TRL 5-6（可行，液金稳定性是瓶颈）
- 最大挑战：跨学科整合

### Round 4 — 萧何（资源路径）
- 团队12-14人 | 时间2-3年 | 预算$1.5M-$3M
- 6个关键里程碑（6个月到30个月）
- 核心风险：元认知效果不显著、物理模拟保真度、资金不足、跨学科协作

### Round 5 — 张仪（最强攻击）
- **攻击1**：概念整合的虚假统一（物理vs认知自修复技术栈完全不同）
- **攻击2**：元认知测量困境（测量的是代理指标而非元认知本身）
- **攻击3**：世界模型循环论证
- **攻击4-6**：实验设计缺陷（公平性、代表性）
- **攻击7-10**：工程和资源层面整合不可行
- **韧性评分：4/10**
- **建议：重新定位为三个独立研究方向**
