# 🔭 前沿扫描日报

**日期**：2026-05-17（周日）· **猎手状态**：🟢 活跃
**信源**：arXiv / HuggingFace Daily Papers (05-15) / HN / Reddit / 技术博客
**研究方向**：Agent自我迭代 · 多Agent协作 · AI×人文社科

---

## 📊 今日全景扫描结果

### 支柱一：Agent 自我迭代（Self-Evolution）

| # | 论文/资源 | 来源 | 一句话核心方法 | 热度 |
|---|-----------|------|---------------|------|
| 1 | **Self-Distilled Agentic RL (SDAR)** `2605.15155` | HF #3 (77↑) | RL主目标 + OPSD辅助蒸馏，sigmoid门控选择性地强化正信号、弱化教师拒绝信号 | ⭐⭐⭐⭐⭐ |
| 2 | **EvolveMem: Self-Evolving Memory** `2605.13941` | HF (21↑) | 双层次共进化：存储知识 + 检索机制，LLM诊断模块做AutoResearch | ⭐⭐⭐⭐⭐ |
| 3 | **Do Self-Evolving Agents Forget?** `2605.09315` | arXiv 05-10 | 证明自我进化非单调——四通道（workflow/skill/model/memory）均出现能力退化；提出CPE | ⭐⭐⭐⭐ |
| 4 | **Self-Evolving Software Agents** `2604.27264` | arXiv 04-29 | BDI推理 + LLM，从经验中自动挖掘新需求→生成代码更新 | ⭐⭐⭐⭐ |
| 5 | **PREPING: Building Memory w/o Tasks** `2605.13880` | HF (24↑) | 任务前内存构建，proposer引导的合成演练解决冷启动 | ⭐⭐⭐ |
| 6 | **Awesome-Self-Evolving-Agents** | GitHub | 自进化Agent论文大全，三大方向分类 | ⭐⭐⭐ |

### 支柱二：多Agent协作架构

| # | 论文/资源 | 来源 | 一句话核心方法 | 热度 |
|---|-----------|------|---------------|------|
| 1 | **Beyond Individual Intelligence (LIFE)** `2605.14892` | HF (42↑) | LIFE框架：奠定基础→集成协作→归因失败→自我进化，四个阶段因果关联 | ⭐⭐⭐⭐⭐ |
| 2 | **WildClawBench** `2605.10912` | HF (39↑, 371★) | 原生运行时评测（非沙箱），19个前沿模型最高仅62.2%，harness影响±18pp | ⭐⭐⭐⭐ |
| 3 | **AgentMaster: A2A+MCP** `2507.21105` | EMNLP 2025 | 首个组合A2A和MCP的MAS框架，BERTScore 96.3%，支持多模态 | ⭐⭐⭐⭐ |
| 4 | **Agent Identity Protocol** `2603.24775` | arXiv 03-26 | MCP+A2A上的可验证委托身份协议 | ⭐⭐⭐ |
| 5 | **MCP vs A2A: 2026 Guide** | OneReach博客 | MCP做上下文/数据连接，A2A做协调层 | ⭐⭐⭐ |

### 支柱三：AI × 人文社科

| # | 论文/资源 | 来源 | 一句话核心方法 | 热度 |
|---|-----------|------|---------------|------|
| 1 | **When AI Meets Science** `2605.06033` | arXiv v3 05-12 | 分析2.27亿篇学术论文，AI支持的研究集中在少数CS相关主题，引用溢价但撤销率更高 | ⭐⭐⭐⭐ |
| 2 | **SHARE: Social-Humanities AI** `2604.11152` | HF / arXiv | 首个面向社科人文的预训练模型家族，匹配通用模型性能 | ⭐⭐⭐ |
| 3 | **Provocations from Humanities** `2502.19190` | arXiv | 人文学者对GenAI研究的挑衅性批判，强调抵抗CS对人文的提取 | ⭐⭐⭐ |
| 4 | **arXiv将封禁AI生成幻觉提交者** | Ars Technica 05-26 | 预印本服务器开始对AI生成垃圾论文的提交者实施一年禁令 | ⭐⭐⭐ |

---

## 🔥 今日热点信号

| 信号 | 详情 |
|------|------|
| 🚀 **SDAR 爆发** | HF #3论文（77↑），自我蒸馏+RL在Agent训练上的新范式，GitHub已开源（64★） |
| 🔴 **自进化Agent会遗忘** | 多团队独立发现同一问题：非单调进化导致能力退化——这是当前最大瓶颈 |
| 🏗️ **WildClawBench 揭示伪进步** | 19个前沿模型在真实原生运行时中最高仅62.2%，harness切换可波动18个百分点 |
| 📰 **arXiv打击AI垃圾论文** | 5月实施禁令，AI生成的幻觉论文提交者将被封禁一年 |
| 💬 **HN热议：AI Agent真的赚钱吗？** | "Do AI Agents Make Money in 2026?" 讨论AI代理的商业模式困境 |

---

## 🎯 值得深挖 TOP3

| 排名 | 论文 | 为什么值得 | 关联项目 |
|------|------|-----------|---------|
| 🥇 | **SDAR** `2605.15155` | 最实用的Agent训练方法创新——RL+蒸馏的sigmoid门控策略，可在Hermes Agent的训练管线中直接试验 | Hermes Agent |
| 🥈 | **EvolveMem** `2605.13941` | 自进化记忆架构——双层次共进化，AutoResearch替代手动调参，与我们izu的记忆系统设计直接吻合 | 爱祝/izu |
| 🥉 | **LIFE Survey** `2605.14892` | 统一三大支柱的框架性文献——LIFE四阶段提供了研究定位的理论脚手架 | 爱祝/Hermes |

---

> 💡 **军师的话**：本周最值得关注的是"自进化Agent的遗忘问题"——三篇独立论文（SDAR的稳定性问题、遗忘论文的CPE、EvolveMem的revert-on-regression）都指向同一件事：自我进化如果不加约束，会自我抵消。这不是bug，是self-evolution的内在矛盾。谁先解决这个，谁就能做出真正的"长寿命Agent"。
>
> 📌 **明日关注**：SHARE模型的开源进展（首个社科人文专用LLM），以及WildClawBench的后续模型评测更新。
