# 🔭 IZU前沿实验室 · 每日论文扫描日报

**日期**：2026-05-16（周六）
**猎手**：Scout
**扫描范围**：arXiv / GitHub / HN / Reddit / ICLR 2026 RSI Workshop
**研究方向**：Agent自我迭代 · 多Agent协作 · AI×人文社科

---

## 一、Agent自我迭代（Self-Evolution / Self-Improvement / RSI）

### 今日捕获 TOP 论文

| # | 论文 | 来源 | 一句话核心方法 | 热度指标 | 值得深挖 |
|---|------|------|--------------|---------|---------|
| 1 | **Autogenesis: A Self-Evolving Agent Protocol** (2604.15034) | arXiv cs.AI + GitHub | 提出AGP协议，RSPL层将所有组件注册为版本化资源，SEPL层实现propose→assess→commit闭环演化；AGS系统动态实例化/检索/精炼协议资源 | ⭐ HF Paper · v3更新于5/7 · GitHub: DVampire/Autogenesis | ✅ **TOP1** |
| 2 | **SkillOS: Learning Skill Curation for Self-Evolving Agents** (2605.06614) | arXiv cs.AI (May 7) | 用RL训练skill curator管理外部SkillRepo，frozen executor + trainable curator分离，composite reward + grouped task streams | ⭐ HF Paper · Twitter热议 · 7天前仅 | ✅ **TOP2** |
| 3 | **CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification** (2604.01687) | arXiv cs.AI | Skill Generator + Surrogate Verifier协同演化，无ground-truth下提供可行动反馈，SkillsBench最高pass rate | ⭐ HF Paper · GitHub: Zhang-Henry/CoEvoSkills | ✅ **TOP3** |
| 4 | **Continual Harness: Online Adaptation for Self-Improving Foundation Agents** (2605.09998) | arXiv cs.LG/AI (May 11) | 无重置自改进harness，agent在单次运行中在线精炼prompt/sub-agent/skill/memory，Pokemon Red验证 | ⭐ HF Paper · 28页 | — |
| 5 | **Self-Evolving Software Agents** (2604.27264) | arXiv cs.SE/AI | BDI(信念-欲望-意图)+LLM架构，自动演化模块从经验中挖掘新需求并合成代码更新 | 多Agent环境验证 | — |

### ICLR 2026 RSI Workshop 亮点

- **Oral #1 - Agent0**: 从零数据通过工具集成推理释放自演化agent（OpenReview）
- **Oral #3 - Learning to Continually Learn via Meta-learning Agentic Memory Designs**
- **Oral #4 - PostTrainBench**: LLM agent能否自动化LLM后训练？
- **Spotlight #7 - Towards Execution-Grounded Automated AI Research**
- **Spotlight #15 - ACE**: 自演化LLM编码框架 + 对抗性单元测试生成 + 偏好优化
- **共110篇接收论文** — RSI已成为ICLR 2026最热workshop

---

## 二、多Agent协作架构（Multi-Agent Orchestration / A2A / MCP）

| # | 论文 | 来源 | 一句话核心方法 | 热度指标 | 值得深挖 |
|---|------|------|--------------|---------|---------|
| 6 | **Qualixar OS: A Universal Operating System for AI Agent Orchestration** (2604.06392) | arXiv cs.AI/MA/SE | 应用层Agent OS：支持10 LLM提供商、8+框架、7传输协议、12种多Agent拓扑，含Forge团队设计引擎 + Claw Bridge(MCP+A2A) | ⭐ HF Paper · 2821测试用例 · GitHub: qualixar/qualixar-os | ✅ **值得深挖** |
| 7 | **MAGE: Multi-Agent Self-Evolution with Co-Evolutionary Knowledge Graphs** (2605.10064) | arXiv (May 2026) | 四子图协同演化的知识图谱外化自知识，9个benchmark验证 | Twitter热议 | — |
| 8 | **ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration** (2605.03042) | arXiv cs.AI (May 2026) | 跨模型对抗性协作的自主研究harness，open-source | HF Paper | — |

---

## 三、AI×人文社科（AI for Social Science / Humanities / Politics）

| # | 论文/资源 | 来源 | 一句话核心 | 热度 |
|---|----------|------|-----------|------|
| 9 | **SHARE: Social-Humanities AI for Research and Education** (2604.11152) | arXiv cs.CL | 首个专为社科人文领域从零预训练的因果语言模型，100倍更少token即达Phi-4级别性能；配套MIRROR界面不生成文本仅辅助审阅 | ⭐ HF Paper |
| 10 | **International AI Safety Report 2026** | 国际AI安全报告 | 系统性分析AI对民主/社会系统风险，含RAND正式模型分析AI如何侵蚀人类集体能动性 | 多机构联合发布 |

---

## 四、今日热点信号（GitHub / HN / Reddit / Twitter）

| 信号 | 来源 | 说明 | 热度 |
|------|------|------|------|
| 🐍 **OUROBOROS** — 自创建AI Agent爆火 | GitHub (razzant/ouroboros) | 能读写自己源码、通过git提交演化、自写宪法。俄PhD研究员构建。Reddit r/agi热议 | 🔥🔥🔥🔥🔥 |
| 📢 **"Less Human AI Agents, Please"** | Hacker News #47845429 | HN热帖讨论AI agent应该更像工具而非人类，开发者反思agent UX设计 | 🔥🔥🔥🔥 |
| 🎓 **ICLR 2026 RSI Workshop 110篇论文** | ICLR Rio de Janeiro | RSI从思想实验走向工程实践，Agent0/PostTrainBench/SkillRL等oral论文引发关注 | 🔥🔥🔥🔥 |
| 🔬 **Self-Evolving Agents = 2026年最热AI趋势** | 多平台共识 | IEEE Spectrum / LinkedIn / Medium多篇分析文章确认self-evolving agents为2026年度趋势 | 🔥🔥🔥 |
| 🏛 **WEF发布Agentic AI for Government报告** | WEF + Stanford HAI AI Index 2026 | 政府级Agentic AI实施框架，AI治理成为政策焦点 | 🔥🔥🔥 |

---

## 五、今日趋势判断

> **"Self-Evolving Agents正在从单点突破走向协议标准化。"**
>
> Autogenesis (AGP) 和 Qualixar OS 的同步出现标志着一个关键节点：前者定义了"如何演化"的协议层，后者定义了"如何编排"的OS层。两者互补，恰好对应Hermes Agent当前在Gateway和self-improvement两条线上的需求。OUROBOROS的火爆则说明社区对"真正能改自己代码"的agent有极高的情绪需求——但安全性和治理仍是盲区。
>
> AI×人文社科方向仍处于"基建期"——SHARE是第一个专为SSH领域预训练的模型，但应用层工具还很匮乏。

---

## 六、明日关注

- [ ] Autogenesis的GitHub代码仓库结构（看RSPL/SEPL实现质量）
- [ ] SkillOS的composite reward设计细节（可能复用）
- [ ] OUROBOROS的安全讨论（自修改agent的审计与回滚）
- [ ] ICLR RSI Workshop Agent0论文全文

---

*📋 扫描完成于 2026-05-16 09:01 CST · 共扫描20+来源，捕获10篇有效论文，3篇值得深挖*
