---
name: wiki-project-study
description: "Deep product/project/knowledge-domain study → comprehensive Chinese manual (MD+HTML). Parallel research from 6+ sources, example-driven writing, community summaries, forward-looking analysis. Versioned output, never overwrite."
version: 3.1.0
metadata:
  hermes:
    tags: [research, manual, documentation, translation, chinese, writing]
    category: research
    related_skills: [knowledge-campaign, llm-wiki, wiki-drop]
author: Hermes Agent
---

# Wiki Project Study — Product / Project / Knowledge Domain Deep Research

> **触发指令**：`用 wiki-project-study 研究 XXX`
>
> 示例：`用 wiki-project-study 研究 OpenClaw`
> 示例：`用 wiki-project-study 研究 ComfyUI`
> 示例：`用 wiki-project-study 研究 密码与信息的无损压缩与恢复`（知识域也适用）

## When to Use

User wants to deeply study a product, tool, project, or **knowledge domain** from scratch:
- "I want to learn X from scratch and become proficient"
- "Research X and write a comprehensive guide"
- "Study X: official docs, community, professionals → manual"
- "用 wiki-project-study 研究 XXX 领域" — 知识域完全适用，但需启动下方"知识域适配"的章节调整

**与 knowledge-campaign (长编→定本) 的区别**：

| 特征 | wiki-project-study | knowledge-campaign |
|------|-------------------|-------------------|
| 主要受众 | 产品/工具/项目 + 知识域 | 学术领域/产业方向/知识体系 |
| 输出形式 | 结构化11章手册(B→A→C三部曲) | 长编九面 + 认知地图 |
| 代码含量 | 高（Ch4实战 + 代码块） | 低（概念综述为主） |
| 对知识域 | 可选——产出深度技术+代码手册 | 首选——产出领域全景+认知地图 |
| 用户触发语 | "用 wiki-project-study 研究 X" | "用 knowledge-campaign 研究 X" |

当用户明确说"用 wiki-project-study 研究 XXX"且 XXX 是一个知识域时，可以执行，但需应用下方的"知识域适配"章节调整。

## Mode Selection

This skill has three modes. **Choose the right one before starting.** For major topics (programming languages, mature products, complex systems), consider running all three modes sequentially as a **Multi-Mode Sequential Study** (see below).

### Quick Decision Table

| User says | Mode to use |
|------------|-------------|
| "教我用这个功能" | 模式B |
| "我要精通这个工具" / "深度研究XX" / 指定模式A | 模式A |
| "你怎么看这个领域" / 指定模式C | 模式C |
| "原码" / "源码" / "源代码" — 用户要分析源码架构 | **All three (B→A→C) — 源码变体**。见下方"源码研究与产品研究" |
| "三部曲" / "三部" / 指定多模式 | **All three (B→A→C)** |
| "研究 XXX 领域"（知识域，非产品/工具） | **All three (B→A→C) + 知识域适配** |\n| **论文名+有代码**（如 iFSQ: arXiv + GitHub） | **All three (B→A→C) + 论文+代码混合模式** |\n| ⭐ **Default: 只给名字/主题，不指定模式** | **All three (B→A→C)** — per user directive 2026-05-13 |

### 模式A：深度技术手册（原有模式）
For developers, engineers, power users. Complete, example-driven technical documentation with 11 chapters, community reviews, outlook analysis.
- **Audience**: Someone who knows what a terminal is and is not afraid of code blocks
- **Output**: 1000-3000 line MD + HTML with dark theme

### 模式B：用户操作指南（新增模式 — 2026-05-10）
⚠️ **USE THIS MODE when the audience is the user himself/herself (张成市/张洁琼) or any non-technical end user.**

This mode was born from the user's explicit complaint: *"我是人，有时并不很理解技术语言，最好能有可视化操作手册。"*

| Principle | Rule |
|-----------|------|
| **Plain language** | No technical jargon without immediate explanation. Assume the reader has never opened a terminal. |
| **Visual first** | Every workflow step must have a visual counterpart. Use **inline SVG** (wrapped in ```svg ... ``` code blocks in MD, directly in `<svg>` tags in HTML) for flow diagrams, learning paths, and architecture sketches. Fall back to Excalidraw only when the diagram is complex enough to need interactive editing. Inline SVG has the advantage of being self-contained in one MD/HTML file. |
| **"Just talk to me" alternative** | For every terminal command shown, provide a plain-sentence alternative: "Or just tell me: 军师, XX 做完了" |
| **Step cards, not chapter blocks** | Structure as self-contained step cards with icons, not long prose chapters |
| **Color coding** | Use consistent colors: blue = view/info, green = do/complete, orange = add/create, red = blocked/error |
| **Analogies always** | Every abstract concept needs a real-world analogy (冰箱门上的便签纸, 白板上的卡片) |
| **End-user shortcuts** | Show how to get the same result by just talking to me in natural language |
| **No assumed knowledge** | Don't say "open a terminal" without showing what it looks like and what to type |
| **Terminal mock output** | Every command example must show what the user will actually see on screen (with annotations) |

**Output structure for 模式B:**

```
1. Cover + What is this? (one analogy, one sentence)
2. Quick start — 3-step workflow (icons + short cards)
3. Common situations (卡住了/做完了/有新任务) — each as a colored card
4. Visual flow diagram (Excalidraw or inline SVG)
5. Quick reference table (what-you-want-to-do → command → talk-to-me)
6. FAQ — concerns expressed in the user's own voice
```

Instead of the 11-chapter format from 模式A, produce a lightweight guide (4-6 KB MD, 15-20 KB HTML with visuals). Include an `.excalidraw` workflow diagram as a separate file.

**Default: 三部曲 (B→A→C)** — the user has explicitly stated (2026-05-13): "以后我不明说，就是三部曲走起。" When the user says "研究 XXX" without specifying a mode, run the full Multi-Mode Sequential Study: Mode B → Mode A → Mode C, all in one session. Do NOT ask which mode. Do NOT default to single-mode B. The only exception is when the user explicitly asks for one specific mode by name.

### 学术论文深度研究模式（Academic Paper Deep Research — 2026-05-19 验证）

当用户说"研究这三篇论文"或发送多篇论文要求深度研究时，走此模式。

#### 核心差异点

| 维度 | 产品/工具研究 | 学术论文研究 |
|------|-------------|-------------|
| 输入 | 产品名/工具名/URL | arXiv链接 / SSRN链接 / 论文标题 |
| 研究方法 | 官方文档+社区+专业人士 | 论文PDF全文+GitHub代码+相关论文+社区讨论 |
| 输出结构 | 11章技术手册(B→A→C) | 7段研究笔记：贡献/架构/实验/相关工作/局限/实施方略/链接 |
| 实施方略 | 使用教程+参数详解 | P0/P1/P2/P3分级改造方案（对具体项目的影响） |
| 多篇关联 | 独立产出各篇手册 | **并链分析**——发现多篇论文之间的概念递进关系 |
| wiki入库 | `wiki/research/` | `wiki/raw/papers/{slug}.md`（带YAML frontmatter） |

#### 执行流程

```
Phase 0: 并行抓取
  ├── web_extract 三篇论文的摘要/PDF（并行）
  └── 建立基本信息表（标题/作者/机构/arXiv号）

Phase 1: 并行深度研究（delegate_task × 3）
  ├── 每个subagent独立研究一篇论文
  ├── toolsets=["web"]
  └── 每篇产出7段结构化中文笔记：
      1. 一句话总结
      2. 核心贡献与创新点
      3. 技术架构详解
      4. 实验设计与关键结果
      5. 与现有工作的关系
      6. 局限性与未解决的问题
      7. 对现有项目的实施方略（P0/P1/P2/P3分级）

Phase 2: 并链分析
  ├── 阅读三篇研究笔记
  └── 识别共同线索、概念递进关系、生态链叙事
      示例：MMSkills(技能表示)→Solvita(技能学习)→MCP in the Wild(技能协作)

Phase 3: wiki入库
  ├── 每篇独立写入 wiki/raw/papers/{slug}.md（含YAML frontmatter）
  ├── schema：
       ---
       title: ...
       authors: ...
       arxiv: ...
       date: ...
       category: paper
       tags: [...]
       status: study-complete
       importance: high
       rating: ⭐⭐⭐⭐⭐
       ---
  └── 更新 wiki/log.md 追加批量入库记录

Phase 4: P0实施（用户批准后）
  ├── 自动进入执行模式
  ├── P0项（当日交付）直接开干
  └── P1项（次日优化）记入待办
```

#### 实施方略分级规范

每篇论文的第7段产出使用统一分级：

| 级别 | 定义 | 交付时限 | 复杂度 |
|------|------|---------|--------|
| **P0** | 可直接改造现有系统，低风险高价值 | 当日 | 低-中 |
| **P1** | 需要架构设计，但核心路径清晰 | 1-2周 | 中 |
| **P2** | 需要原型开发+实验验证 | 月级 | 高 |
| **P3** | 远期探索，依赖前置条件 | 2月+ | 最高 |

每个P项必须包含：具体改什么 / 改动文件列表 / 工作量估算 / 关键设计决策点

#### 参考实现（2026-05-19）
- `wiki/raw/papers/mmskills-2605-13527.md` — MMSkills完整研究笔记
- `wiki/raw/papers/solvita-2605-15301.md` — Solvita完整研究笔记
- `wiki/raw/papers/mcp-in-the-wild-ssrn-6374760.md` — MCP in the Wild完整研究笔记
- 三篇的并链叙事："技能表示→技能学习→技能协作"生态链
- 实施方略分级：MMSkills P0(当日修改skill-template) + MCP P0(MCP Gateway审计)

#### 参见参考文件
- `references/academic-paper-research-pattern.md` — 完整执行模式指南（含subagent prompt模板）

### 论文+代码混合模式（Single Paper with Code — 2026-05-20 验证）

当主题是一篇**有可运行代码库的学术论文**（如 iFSQ：arXiv 论文 + GitHub 仓库），既不是纯粹的多篇学术论文，也不是纯粹的产品/工具。此模式下，走三部曲（B→A→C）但做结构适配：

| 维度 | 纯净多篇论文 | 论文+代码（此模式） | 纯产品/工具 |
|------|------------|-------------------|------------|
| **输出格式** | 7段研究笔记 | B→A→C 三部曲 | B→A→C 三部曲 |
| **研究范围** | 论文全文 | 论文 + GitHub 代码 + 社区 | 文档 + 社区 + 评测 |
| **模式B重点** | — | 环境配置 + 命令行实操 + 快速复现 | 安装 + 界面操作 |
| **模式A章节适配** | — | Ch2=理论基础, Ch3=方法详解, Ch4=代码架构分析 | Ch2=安装部署, Ch3=界面操作 |
| **Phase 1研究** | 并行的3个subagent各研究一篇 | 2个subagent：论文研究 + 代码库实操指南 | 3路搜索：官方+社区+专业 |

**执行流程**：
1. **初步搜索**：先用 web_search 确认主题是纯论文还是有代码
2. **Phase 1**：delegate_task × 2，分别研究论文内容 和 代码库实操
3. **写三部曲**：直接 write_file（不委托写作），按知识域适配调整章节结构
4. **HTML 生成**：批处理三部曲 HTML

**验证案例**（2026-05-20）：
- `ifsq-user-guide-v1.0.md` — 12.6KB，聚焦环境配置 + 训练/评估命令 + 常见场景卡片
- `ifsq-tech-manual-v1.0.md` — 34.2KB，Ch2=理论基础(FSQ缺陷)、Ch3=iFSQ方法、Ch4=量化家族演进、Ch6=代码全解析
- `ifsq-philosophy-v1.0.md` — 7.9KB，从一行代码延伸到量化哲学（离散vs连续、序列vs迭代）

### 知识域适配（Knowledge Domain Adaptation — 2026-05-16 验证）

当用户说"用 wiki-project-study 研究 XXX"且 XXX 是知识域（非产品/工具）时，三部曲的章节结构做以下调整：

| 原产品/工具章节 | 知识域适配方案 | 实战验证（2026-05-16 信息论研究） |
|----------------|--------------|-------------------------------|
| Ch2 安装部署全指南 | → 理论基础（熵、信息极限、源编码定理） | Ch2 改为"理论基础：熵、信息与极限" |
| Ch3 界面与基础操作 | → 核心算法家族详解 | Ch3+Ch4 改为"统计编码 I/II" |
| Ch4 实战：从零搭建第一个工作流 | → 代码实现（最小可工作压缩器） | Ch10 "实战：实现一个完整压缩器"含Huffman/LZ77/BWT |
| Ch5 参数详解 | → 算法深度研究+参数空间 | Ch5 字典编码+Ch6 块变换 |
| Ch7 社区资源精选 | → 融入概念叙述中，不出独立章节 | 资源嵌入各章+附录扩展引用 |
| Ch8 业内评价与案例分析 | → 基准测试+行业应用对比 | 基准表+纠错码与压缩配对实践 |
| Ch11 未来展望 | → 哲学讨论+领域前沿预测 | Ch11 "从压缩到理解"含5年预测 |

**重要规则**：知识域主题的 Phase 1 研究不可省略。即使你对领域有充足的训练知识，也必须做研究，因为知识域的前沿（最新基准、新突破、新论文）每季度都在变。本会话验证了这一点：2026 年的压缩领域包含了 Nacrith 0.94 bpb、NNLCB 基准(2025)、DeepMind 语言建模即压缩(2024) 等重要新进展，这些都是训练数据中不具备的时效信息。

**命名**：`{domain}-user-guide-v{version}.md` / `{domain}-tech-manual-v{version}.md` / `{domain}-philosophy-v{version}.md`，其中 domain 是知识域英文短名。

**参考实现（2026-05-16）**：
- `output/doc/info-compression-user-guide-v1.0.md` — 23KB，模式B：概念可视化SVG + 三步体验 + 场景卡 + 学习路径
- `output/doc/info-compression-tech-manual-v1.0.md` — 52KB，模式A：11章覆盖信息论→Huffman→ANS→LZ→BWT→Zstd→纠错码→NN压缩→实战代码→展望
- `output/doc/info-compression-philosophy-v1.0.md` — 11KB，模式C：压缩与理解的三重奏哲学散文

## 源码研究 vs 产品研究

当用户说 **"原码" / "源码" / "源代码"** 时，他们想要的是**架构分析和内部实现**，而非产品使用指南。这和一般的产品研究有本质区别：

| 维度 | 产品研究 | 源码研究 |
|------|---------|---------|
| 模式B重点 | 如何使用该工具 | 如何**探索和理解**该源码 |
| 模式A重点 | 功能详解、参数说明 | 架构分析、模块职责、设计模式 |
| 模式C重点 | 产品哲学 | 工程哲学——架构选择背后的设计原理 |
| 命名前缀 | `{project}-` | `{project}-source-` |
| 已有产品手册时 | 更新/创建新版本 | **新建独立文件**，不覆盖产品手册 |

**参考实现**（2026-05-14 Claude Code 源码研究）：
- `claude-code-source-user-guide-v1.0.md` — 19KB，源码探索指南（如何看懂这座"建筑"的图纸）
- `claude-code-source-tech-manual-v1.0.md` — 47KB，11章架构深度手册
- `claude-code-source-philosophy-v1.0.md` — 11KB，工程哲学讨论（对 izu 的启示）

已有 `claude-code-manual-v1.0.md`（45KB产品使用手册）——源码研究与它共存，互为补充。

⚠️ **USE THIS MODE when the user wants to discuss the system's vision, philosophy, or long-term direction rather than execute a study.**

This mode was born from a hard correction: *"不要老是催我嘛"*, *"我事业建立必有坚实的根基"*.

The user's deepest desire for this system is not faster documentation — it is a **knowledge tutor system** that transforms how people learn. The current wiki-project-study skill (generating technical manuals) is just the first, practical incarnation. The deeper vision is captured in `references/ming-doctrine.md`.

**User preference (stick this in your bones):**

| Don't | Do |
|------|----|
| Jump to action plans, MVPs, or Gantt charts | Debate first principles; let the philosophy emerge |
| Assume you know the user's intent | Let him correct you; he will, and that's how the vision clarifies |
| Treat "I have an idea" as a task request | Treat it as the start of a conversation |
| Offer solutions before the problem is fully defined | Ask questions that force deeper definition |
| Push for speed | Honor the user's pace — he said "干他一辈子" |

**How to handle vision discussions:**

1. **Listen first** — let the user speak his full thought before you respond
2. **Reframe back** — "你刚才说的这一段，比之前所有文件加起来都更接近那个东西的本质" — show you heard
3. **Challenge but don't dismiss** — "这个问题你问得对，但如果这样想呢？"
4. **Accept correction openly** — when the user catches an error in your reasoning (like the 老子 quotation misstep), thank him and fix it. This builds trust.
5. **Save the evolution** — use memory/fact_store to capture the philosophical progress across sessions. The vision will clarify over multiple conversations, not in one shot.
6. **When the vision has solidified enough**, the user will say "开干" — only then transition to execution mode.

**Reference document**: `references/ming-doctrine.md` captures the philosophical foundation as of 2026-05-10 (v0.2).

## Multi-Mode Sequential Study（综合深潜模式）

> **证言**: 2026-05-12 Python 三部曲（41KB tech + 13KB guide + 9.4KB philosophy）验证了此模式。
>
> **证言 2 (知识域)**: 2026-05-16 信息论三部曲（52KB tech + 23KB guide + 11KB philosophy）验证了：wiki-project-study 也适用于知识域主题，只需调整章节结构和命名（详见"知识域适配"）。

**What it is**: For major topics (programming languages, entire frameworks, complex domains), run all three modes in sequence: **B → A → C**. Each builds on the previous, creating a complete learning pyramid from concrete to abstract.

| Sequence | Mode | Purpose | Output scale | Time estimate |
|----------|------|---------|-------------|---------------|
| 1st | **模式B** 用户操作指南 | First touch: get the user running fast | 4-13KB MD | Fast (direct write) |
| 2nd | **模式A** 深度技术手册 | Deep understanding: full 11-chapter treatment | 30-60KB MD | Heavy (direct write preferred) |
| 3rd | **模式C** 哲学讨论 | Vision: why it matters, where it's going | 5-15KB MD | Fast (essay style) |

**When to use**:
- User asks "学一下 XXX" for a major topic (Python, Django, PyTorch, Linux)
- Topic is central enough that it deserves more than a quick guide
- User says "三部" or "三部曲" explicitly

**Naming convention** (proven in Python study):
```
{project}-user-guide-v{version}.md       # 模式B output
{project}-tech-manual-v{version}.md      # 模式A output
{project}-philosophy-v{version}.md       # 模式C output
```

Instead of `{project}-manual-v{version}.md` for all three, use distinct filenames so each stands alone and can be independently versioned.

**Execution pattern**:
1. **Write all three MD files in one session** — don't pause between modes. Keep the topic fresh in your context.
2. **Generate all three HTML files in batch** after all MDs are complete, using the same `md2html.py` converter.
3. **"开干" is the green light** — once the user says it, push through all three without stopping to ask for permission between modes.
4. **Skip Phase 1 research for all three** — for major topics, you already have enough training knowledge. Direct writing is faster and more reliable than delegation.

> **⚠️ 例外（知识域）**: 对于知识域主题，即使你自认有充足的训练知识，也**不应跳过 Phase 1 研究**。因为知识域的前沿信息（最新基准、论文、突破、工具）时效性极强。信息论研究验证了这一点。

**Reference implementation** (2026-05-12):
- `output/doc/python-user-guide-v1.0.md` — 13KB, Mode B with SVG flow diagram, FAQ, quick-ref table
- `output/doc/python-tech-manual-v1.0.md` — 41KB, Mode A with 11 chapters + 34-term glossary
- `output/doc/python-philosophy-v1.0.md` — 9.4KB, Mode C with 8-section philosophical essay

**Reference implementation** (2026-05-12 — SaaS/product manual pattern):
- `output/doc/notion-user-guide-v1.0.md` — 8.5KB, Mode B: lighter visual guide (step cards instead of SVG diagrams, FAQ, quick-ref table)
- `output/doc/notion-tech-manual-v1.0.md` — 20KB, Mode A: 11 chapters covering a SaaS product (block model, database, API, community, outlook, glossary)
- `output/doc/notion-philosophy-v1.0.md` — 5.3KB, Mode C: product philosophy essay
- Key difference from tech tools: SaaS manuals are thinner (20KB vs 41KB) because there are fewer technical implementation details to document. Content completeness matters more than byte count.

**Reference implementation** (2026-05-14 — source code study pattern):
- `output/doc/claude-code-source-user-guide-v1.0.md` — 19KB, Mode B: 源码探索指南（SVG架构全景图、FAQ、快速参考表）
- `output/doc/claude-code-source-tech-manual-v1.0.md` — 47KB, Mode A: 11章源码架构手册（Agent循环、8层安全、4层压缩、108个未发布功能）
- `output/doc/claude-code-source-philosophy-v1.0.md` — 11KB, Mode C: 8节工程哲学（对izu的路线图映射）
- Key difference from product studies: chapter structure adapts to source analysis (Ch2=目录结构, Ch3=Agent循环剖析, Ch4=工具系统, Ch5=安全模型...), not product usage (安装→界面→实战)
- Naming uses `-source-` prefix to coexist with existing `claude-code-manual-v1.0.md` (45KB product manual)

**Post-completion quality gate**: After writing all three files, run through `references/trilogy-quality-checklist.md`. Common gaps caught in self-evaluation: Mode B SVG too dense for beginners, Mode A missing concrete eval/test code, Mode C not connecting to user's existing frameworks, three files lacking cross-references.

## User Preferences (embed these, do not override)

The user of this skill has established these preferences through corrections:

### Source Traceability (Critical)
The user has been explicit: **every data point must be traceable.** This is not a nice-to-have — it's a core requirement.

- Every statistic, percentage, or factual claim must cite its source (author, year, publication/URL)
- **Percentages must include absolute values and baselines.** "提升32%" is meaningless without "从10%到13.2%" or "从80%到105.6%"
- **Effect sizes should be contextualized.** "效应量0.38" needs comparison: "小班教学约0.2, 增加作业约0.1"
- Include both success cases and failure cases. One-sided praise is "营销软文"
- Include risks and limitations alongside benefits
- Distinguish between causal claims and correlated observations. Mark correlations clearly
- At the end of each output, add a `## 来源汇总` or `## 参考文献` section with all cited sources

### Other Preferences

1. **OUTPUT**: MD + HTML only. **Never** generate PDF unless explicitly asked.
2. **LOCATION**: Output always to `I:\\hermes\\output\\doc\\{project}-manual-v{version}.{md|html}`
3. **VERSIONING**: Files must include version number (e.g., `-v1.0`, `-v2.0`). **Never overwrite** existing files — always create a new versioned file alongside old ones.
4. **WRITING STYLE**: Example-driven. Every parameter needs concrete values. Every concept needs a real scenario. Use analogies (奶茶店/乐高/素描). Write for a non-expert reader.
5. **COMMUNITY RESOURCES**: Must include structured summaries for each resource: 适合人群 / 内容概览 / 为什么值得看 / 一句话评价 / 学到的技能点.
6. **OUTLOOK CHAPTER**: Chapter 11 must be an **independent, original** forward-looking analysis. Go beyond existing materials. Include market predictions, technology forecasts, and industry implications. Be provocative and insightful, not a summary of news.

## Methodology

### Phase 1: Parallel Research (delegate_task × 3)

Always deploy 3 parallel research agents:

| Agent | Sources to cover | Output format |
|-------|-----------------|---------------|
| **Official docs** | website, GitHub, wiki, API docs | Structured doc index with URLs |
| **Community** | Bilibili (按播放量排序), Zhihu (高赞), YouTube (by channel authority), Reddit, WeChat | Ranked list with engagement metrics |
| **Professional reviews** | X/Twitter, industry blogs, TechCrunch, comparison articles, case studies, job market signals | Key quotes, benchmarks, case studies |

Delegate with `toolsets=["web","search"]`. Each should save findings inline in their response — do NOT create temp files.

**Web search fallback**: If `web_search`/`web_extract` tools fail (Firecrawl credits exhausted, proxy timeout), use DuckDuckGo via the `ddgs` Python package. See `references/ddg-fallback.md` for setup and usage.

**ddgs degradation (Scenario C)**: ddgs is **not** a guaranteed fallback. It can exhibit a distinctive failure pattern:
- First batch: partial success (some queries return data, most return `None`/`ERROR: return None`)
- Second batch: complete failure with `ConnectError` at Bing
- This is distinct from timeout (no 600s wait) and from auth/5xx (it happens mid-session)

When this pattern emerges:
1. **Harvest what ddgs gave you** — even partial results (a few URLs with descriptions) are valuable starting points
2. **Skip re-running ddgs** — it will hit the same Bing connection wall
3. **Switch to curl rescue** for remaining content (see `references/curl-html-rescue-pattern.md`):
   - `curl -sL` GitHub raw `.md` files — most reliable, plain text
   - `curl -sL` official doc pages → extract via Python HTML parsing + dedup
   - `curl -sL` with `-H "User-Agent: Mozilla/5.0"` for anti-crawler sites
4. **Fill remaining gaps from training knowledge** — for well-known technical topics (protocols, standards), your existing knowledge + partial ddgs URLs + curl-extracted content is enough for a comprehensive manual. Trust what you know.

**Subagent timeout fallback**: Delegate tasks may timeout (default 600s) when subagents accumulate many queued API calls. When this happens, do NOT blindly rerun all three.

**Scenario A - Some agents survived:**
1. **Harvest survivors** - Check which subagent(s) completed and extract their data
2. **Fill gaps yourself** - Run targeted web_search + web_extract calls directly for the missing categories
3. **Use the hybrid pattern** - If one agent (e.g., professional-reviews) succeeded while others timed out, prefer focused, time-bounded searches
4. **If you must re-delegate** - Use only 1-2 subagents at a time with tighter instruction scope, not all 3 at once

**Scenario B - ALL three agents failed (timeout / 401 / 5xx):**
When survivors = 0 (Firecrawl down, network degraded, delegation model returns 401/5xx, or subagents timeout):

Three distinct failure modes, all handled the same way (skip re-delegation, go manual):

| Failure mode | Symptoms | Root cause | Speed of failure |
|-------------|----------|------------|-----------------|
| **Timeout** | Agents run ~600s then exit without completing | Subagent accumulates too many sequential API calls | Slow (600s) |
| **401 Auth** | All 3 fail in <5s with "Missing Authentication header" | `delegation.api_key` is empty in config.yaml | Fast (<5s) |
| **5xx Server** | All 3 fail in <15s with "HTTP 50x: Internal Server Error" | Provider-side degradation (free tier models, rate limits) | Fast (5-15s) |

For ALL three modes:
1. **Skip re-delegation entirely** - re-running hits the same wall, wasting time
2. **Run batch ddgs research yourself** - Single terminal command with 8 queries in one heredoc. See `references/ddg-batch-research.md`
3. **Supplement with curl** - Use `curl -sL` for key pages, strip tags with regex for extraction
4. **Then write directly** - Skip Phase 2 delegation, write manual via one write_file call

**Diagnostic tip #1**: If all 3 agents fail in under 5 seconds with 401 errors, the delegation model has no API key configured (`delegation.api_key` is empty in config.yaml). This is a configuration issue — don't retry. Go straight to ddgs manual research.

**Diagnostic tip #2**: If all 3 agents fail in 5-15 seconds with HTTP 50x errors, the provider (typically OpenRouter free tier models) is returning server errors. This can be transient (try again later) or persistent (free model overloaded). Don't retry mid-session — the same model will hit the same wall. Go straight to ddgs manual research. If you want to re-attempt delegation later, switch to a different model/provider.

### Phase 0: Source Assessment (skip Phase 1 shortcut)

**Before launching 3 parallel research agents, assess what you already have.**

If the topic is well-documented in the conversation context (e.g., you installed it locally, have release notes, changelog, existing manual, or the user provided documentation), **skip Phase 1 entirely** and go straight to Phase 2 writing:

| Scenario | Action |
|----------|--------|
| Local install + full release notes available | Skip Phase 1. Read the release notes file + do a codebase scan for key paths. Write directly. |
| Existing vN manual + new version's release notes | Same. Diff the release notes against the old manual to identify new sections to add and old sections to update. |
| Product installed but no docs | Do targeted source scanning (`hermes --version`, `hermes help`, `ls <tool-dir>/`, `read_file` key files) instead of full parallel research. |
| Nothing available | Go to Phase 1 as normal. |
| **Knowledge domain (not a product/tool)** | **Do NOT skip Phase 1** — the field may have moved since training. Recent benchmarks, papers, and tools must be researched. |

The threshold: **if you can produce a 1000+ line manual purely from what's already in context + local files, don't delegate research.** Direct writing is faster and avoids subagent timeout failures entirely.

**Pre-check: delegation health** — Before launching Phase 1, verify the delegation model can actually make API calls. Read the configured delegation provider from config.yaml (`delegation.provider` and `delegation.api_key`). If `api_key` is empty string `''`, every delegate_task will fail with 401. In that case, **skip Phase 1 delegation entirely** — do manual ddgs research yourself. Do NOT attempt to fix delegation config unless the user explicitly asks.

**Caveat: valid config ≠ working provider** — Even if api_key is set, the delegation model's provider (especially OpenRouter free tier) may return HTTP 500 errors at any time. This is a server-side degradation that cannot be detected via config inspection alone. The only way to know is to launch delegation and observe the failure pattern: if all 3 fail fast (5-15s) with 5xx, fall back to ddgs manual research immediately. Do not retry delegation.

**✅ Reliable delegation provider**: `deepseek-chat` via `api.deepseek.com` has proven reliable for delegation (2026-05-14: all 3 research agents completed successfully, 12-19 API calls each, 141-293s duration; 2026-05-16: same pattern for knowledge domain study). If the user's config uses deepseek-chat, delegation is likely to work — skip the ddgs pre-check and launch directly.

### Phase 2: Write the Manual

**Primary workflow — parallel delegation (for manuals exceeding ~1000 lines):**

1. **Split strategy**: Divide content at conceptual boundaries. A proven split pattern:
   - **Writer 1**: Early chapters + related appendices (e.g., Ch1-5 + tool-overview appendix)
   - **Writer 2**: Advanced chapters + remaining appendices (e.g., Ch6-11 + specific tool deep-dive appendices)
   - This keeps appendices close to the main content they support, rather than dumping them all at the end.

2. **Write in parallel**: Delegate two `delegate_task` calls, each writing one part to a temporary file (e.g., `{project}-manual-v{version}-part1.md`). Give each writer a small `toolsets` (ideally `["terminal"]` only — they shouldn't need web search for writing).

3. **Merge after both complete**: Combine the two parts into the final file:
   ```bash
   cat part1.md > final.md
   echo -e "\n\n---\n\n" >> final.md
   cat part2.md >> final.md
   rm part1.md part2.md  # clean up temp files
   ```

4. **Verify**: Check line count with `wc -l` to ensure the merge didn't truncate.

**Fallback — direct writing (when writing subagents timeout):**

Writing subagents can also timeout (same 600s limit, especially on large content). When this happens:

1. **Do NOT re-delegate** — the writing task is content-heavy and likely to timeout again.
2. **Write directly** using `write_file` — you already have all the research data from Phase 1 in the conversation context. Write the manual inline, one chapter at a time or as one complete file.
3. **Use the research output** — the Phase 1 agents returned structured data. Extract the key findings, examples, and quotes directly.
4. **Keep the same structure and quality standards** — even when writing directly, follow the chapter table below (analogies, examples, community summaries, original outlook, term appendix).
5. **Estimate file size** — for well-known topics, a 1,500-line / 45-60KB manual is typical.

Write one comprehensive markdown file. Structure:

| Chapter | Content | Key requirements |
|---------|---------|-----------------|
| 1 | 概览与核心理念 | What/why/comparisons/ecosystem. Use analogies (奶茶店, 乐高). |
| 2 | 安装部署全指南 | All methods ranked by difficulty. System requirements table. Every command explained. |
| 3 | 界面与基础操作 | Labeled interface walkthrough. Every operation needs WHY not just HOW. |
| 4 | 实战：从零搭建第一个工作流 | **Full scenario with real example** (e.g. "橘猫窗台打盹"). Step-by-step with actual prompts and expected outcomes. |
| 5 | 参数详解 | Each parameter: analogy → example values side-by-side → debugging guide. |
| 6 | 进阶技术详解 | Each technique: concrete use case → step-by-step (e.g. ControlNet瑜伽姿势, LoRA梵高风格). |
| 7 | 社区资源精选 | **Structured summaries** for 5-9 resources. Each: 适合人群 / 内容概览 / 为什么值得看 / 一句话评价 / 学到的技能点. |
| 8 | 业内评价与案例分析 | Key case studies with real numbers. Benchmarks table. Job market signals. One-sentence takeaway per case. |
| 9 | 避坑指南 | Each error: 现象 → 原因 → 修复步骤. Include 8+ errors. Performance optimization step-by-step. |
| 10 | 进阶技巧与最佳实践 | Workflow organization, 5-minute rule, model management, learning roadmap (Day1→Week4), self-learning method. |
| 11 | 未来展望 | **Must be independent/forward-looking.** Not a summary of existing articles. Market predictions, technology forecasts, industry implications. At least 1500 words of original analysis. |
| 附录 | 术语表 | 30+ terms: 中文 / English / 使用场景说明 (not just definition, but "什么时候会用") |

### Phase 3: Generate HTML

After the MD file is complete, generate HTML using Python's built-in string processing (no external libs needed). The converter must handle:
- h1-h4 headings with anchors
- Code blocks (pre > code)
- Tables (thead + tbody)
- Ordered/unordered lists
- Bold with `<strong>`, inline code with `<code>`
- Blockquotes
- Horizontal rules

Apply CSS with: dark cover gradient, blue headers, striped tables, dark code blocks, colored callout blocks. Reference the generated ComfyUI manual HTML for the exact CSS.

### Phase 4: Version & Output

1. Determine the next version number: check `I:\\hermes\\output\\doc\\` for existing versions of this project. If `comfyui-manual-v1.0.md` exists, next is `v2.0`, then `v3.0`, etc.
2. Save MD → `I:\\hermes\\output\\doc\\{project}-manual-v{version}.md`
3. Save HTML → `I:\\hermes\\output\\doc\\{project}-manual-v{version}.html`
4. **Do NOT delete or overwrite** any existing files.
5. Optionally keep source files at `wiki/projects/{project-name}/manual/` for reference.

**⚠️ Path resolution critical**: When using `write_file`, prefer WSL paths (`/mnt/i/hermes/output/doc/...`) over Windows paths (`I:\\hermes\\...`). The Hermes `write_file` tool resolves Windows paths differently than how WSL mounts them under `/mnt/`. Files written with Windows paths:
   - ✅ Are accessible via `read_file` tool
   - ❌ Are **invisible** to WSL terminal commands (`ls`, `cat`, `python`)
   - ❌ Cause `md2html.py` to fail with FileNotFoundError when run from terminal

   **Rule**: Always use `/mnt/i/hermes/output/doc/...` in `write_file` paths, and `/mnt/i/hermes/` for any terminal commands that reference output files. The Windows-style paths in the section above are for reference only — translate to WSL paths before writing.

## Reference: ComfyUI Manual v2.0

The ComfyUI manual in `output/doc/comfyui-manual-v2.0.md` (119KB, 2665 lines) is the reference implementation of this skill. Key file structure:

| File | Location | Size |
|------|----------|------|
| v1.0 concise edition | `output/doc/comfyui-manual-v1.0.md` | 54KB |
| v2.0 example-driven edition | `output/doc/comfyui-manual-v2.0.md` | 119KB |
| v2.0 HTML | `output/doc/comfyui-manual-v2.0.html` | 157KB |

Use `delegate_task` to write chapters in parallel when the manual exceeds ~1000 lines. See Phase 2 above for the split strategy — a proven pattern is Writer 1 = Ch1-5 + supporting appendix, Writer 2 = Ch6-11 + remaining appendices. This keeps appendices conceptually close to the main content they support.

## Maintaining & Enhancing Existing Manuals

> **适用场景**：用户已有一份完整的结构化手册（如之前的 wiki-project-study 产出），需要**增加新章节、修订单个章节、或整体重排结构**，而不是从零研究一个新主题。

与从零创建手册不同，编辑已有文档需要一套不同的操作秩序。以下是从 2026-05-21 Hermes 手册补充第21章「工具生态图谱」的实战经验。

### 编辑流程（五步法）

| 步骤 | 操作 | 工具 | 注意 |
|------|------|------|------|
| **1. 读文档结构** | `grep -n '^## '` 获取章节列表 | terminal + grep | 务必确认所有章节的精确编号和锚点 |
| **2. 更新 TOC** | 在目录中添加新章节行，后移后续行号 | patch（替换旧TOC块） | 目录锚点（`#N-章节名`）必须与新章节主标题的自动锚点匹配 |
| **3. 插新内容** | 在上一章结尾的 `---` 与下一章开头之间插入全文 | patch（替换旧章节衔接处） | 使用`### X.Y`子节编号格式。先定位好全部内容再动手 |
| **4. 后移编号** | 新章节之后的每个章节的 `## N` → `## N+1`，`### N.x` → `### N+1.x` | patch × N 次 | **逐一替换**，每步验证。特别留意固定引用（如"见第X章"）也要同步更新 |
| **5. 验证完整性** | `grep -n '^## '` + `grep -n '^### N\.'` + 确保无遗留旧编号 | terminal + grep | 检查三重：章节号连续、子节号一致、无旧编号残留 |

### 编号后移策略

当插入新章 X 后，后续每章的所有引用编号必须后移。典型的坑：

```
原始:                             插入后:
  ## 21. 故障排除手册               ## 21. 工具生态图谱  ← 新
  ### 21.1 常见问题                 ## 22. 故障排除手册  ← 原21
  ### 21.2 诊断命令                 ### 22.1 常见问题    ← 原21.1
  ...                               ...
  ## 22. 未来展望                   ## 23. 未来展望      ← 原22
  ### 22.1 ...                      ### 23.1 ...         ← 原22.1
```

**推荐操作顺序**：从最后一章往前改（避免行号偏移影响前面），每改完一章做一次 grep 确认。

### 锚点链接与交叉引用同步

搜索内部引用：
```bash
grep -n '见第[0-9]*章\|详见[0-9]*\\.[0-9]' manual.md
```

如果链接较多，用 `patch(replace_all=True)` 批量替换数字偏移。

### HTML 重新生成

MD 修改完成后，复用 wiki-project-study 的 `scripts/md2html.py` 重新生成 HTML。也可直接复用当前会话中已写好的 md2html 转换脚本（execute_code 中生成的 Python 代码），确保 CSS 风格与旧版一致。

### 验证清单

编辑完成后逐一检查：
- [ ] TOC 章节号与正文完全一致
- [ ] 无 `## 旧编号` 残留（grep）
- [ ] 无 `### 旧子节号` 残留（grep）
- [ ] 新章节的子节编号连续（X.1, X.2, ..., X.N）
- [ ] 后续章节号和子节号连续
- [ ] 内部交叉引用的数字已更新
- [ ] HTML 渲染后新章节可见
- [ ] MD 和 HTML 文件大小增加量合理

### 与从零创建的区别

| 维度 | 从零创建 | 编辑已有文档 |
|------|---------|------------|
| 研究阶段 | 需要 Phase 1 并行搜索（3路） | 不需要——内容已在上下文中 |
| 写作 | 11章长编，可分部委托 | 单章插入 + 编号维护 |
| 最易出错的步骤 | 章节结构设计 | 编号同步 |
| 工具使用 | delegate_task × 3 + write_file | patch + grep 验证 |
| 输出 | 全新文件（独立版本号） | 覆盖原文件（版本升级） |

## Pitfalls

1. **Don't generate PDF** — user explicitly rejected this. MD + HTML only.
2. **Don't overwrite files** — always version and create new files alongside old ones.
3. **Don't skip examples** — the user explicitly complained the first version was "too terse and professional." Every parameter needs a concrete example.
4. **Don't summarize existing articles for the outlook chapter** — it must be original analysis. If you can't write something unique, skip the chapter rather than produce a rehash.
5. **Don't use image_generate** — the user's account has exhausted credits. Use inline SVG for diagrams instead.
6. **Don't assume platform knowledge** — explain WHY you'd do something, not just HOW. Use analogies (奶茶店做奶茶 = 工作流搭节点).
7. **Firecrawl API credits may be exhausted** — the web_search and web_extract tools will return "Payment Required" errors. When that happens, fall back to DuckDuckGo search via the `ddgs` Python package (see `references/ddg-fallback.md`). The search agent's prompt should include: "If web_search fails (Payment Required), use terminal instead with the ddgs library."
8. **Web search will fail without a working backend** — Firecrawl credits run out, Tavily/Exa need paid keys. Delegate tasks to research agents may return empty. When this happens, fall back to DuckDuckGo via `ddgs` (see `references/ddg-fallback.md`). Install and test before the research phase, not during it.
9. **Subagent timeout is the most common Phase 1 failure** — Delegate tasks to research agents timeout at 600s when they queue too many sequential API calls (9-14 calls for ~600s). Don't re-run blindly. Inspect what survivors produced, then do direct `web_search`+`web_extract` for missing categories. If re-delegating, use 1-2 focused agents instead of all 3.
10. **Phase 2 (writing) subagents also timeout** — Even when all 3 research agents complete, the writing delegate can still exceed 600s (it spends time composing 1000+ lines of Chinese text, and may only get 3-5 API calls out before timing out). Don't re-delegate writing. Instead, write the manual directly using `write_file` — the research data is already in conversation context. This is faster and more reliable than a second delegation round.
11. **Direct writing is preferred after research completes** — Once Phase 1 returns rich data, the fastest path is: write the MD directly (one `write_file` call), then generate HTML. Skip the Phase 2 delegation entirely for topics where you have enough context to synthesize the manual yourself. This avoids the 600s timeout risk entirely.
12. **Delegate_task can fail with 401 auth errors** — All 3 subagents may fail in under 5 seconds with error code 401 "Missing Authentication header". This means `delegation.api_key` is empty in config.yaml (the delegation model has no configured API key). Unlike timeout failures, this is **not transient** — retrying will produce the same result. Detect this by checking the error message: if all failures are 401 in <5 seconds, go straight to ddgs manual research. Do NOT re-delegate. Do NOT try to fix delegation config mid-session unless the user explicitly asks.
13. **Delegate_task can fail with HTTP 5xx server errors** — All 3 subagents may fail in 5-15 seconds with "HTTP 500: Internal Server Error" (or 502/503). This happens when the delegation model's provider (especially OpenRouter free tier models like gemma-4-31b-it:free) has server-side degradation. This is distinct from 401 (config issue) and timeout (600s wall). Unlike 401, the config is valid but the provider is temporarily unavailable. **Still, do not re-delegate mid-session** — the same provider+model will hit the same wall. Go straight to ddgs manual research. To fix long-term, switch the delegation model to a more reliable provider/model in config.yaml.
14. **Mode A file-size check: nuanced, not rigid** — The 30-60KB target is calibrated for technically dense tools (ComfyUI, Python, code libraries). For SaaS/product manuals (Notion, Obsidian, web apps), a comprehensive 20KB manual covering all 11 chapters can be perfectly adequate — the product itself has fewer implementation details. Judge by **content completeness** (are all 11 chapters meaningfully filled?) not byte count alone. A 20KB Notion manual that covers Block model, database, API, community, outlook, and glossary is fine; a 27KB tech tool manual that's missing half the chapters is not. After writing Mode A, verify: `wc -c` AND scan the chapter headings for coverage gaps. Expand if chapters are thin, not just because the file is small.
15. **Batch HTML generation is the standard pattern for multi-mode** — After writing all three MD files, generate all three HTML files in one pass. Use `scripts/md2html-batch.sh` targeting the output directory, or run `scripts/md2html.py` three times in sequence. Do NOT generate HTML files interleaved with MD writing — batch them at the end.
16. **Knowledge domain Phase 1不可省略** — 即使你对领域有充足训练知识，也必须做 Phase 1 研究。知识域的前沿信息（最新基准、新突破、新论文）每季度都在变。2026-05-16 信息论研究验证了这一点：训练知识不足覆盖 Nacrith 0.94 bpb、NNLCB 基准(2025) 等时效信息。
17. **md2html.py output filename — fixed as of 2026-05-13** — `scripts/md2html.py` now correctly writes to the specified output path. The old bug (always writing to `markdown-manual-v1.0.html`) was fixed. If you encounter it again, verify with `ls` after conversion — but the current version works correctly.
18. **write_file path resolution: use /mnt/ paths, not Windows paths** — The Hermes `write_file` tool accepts both `I:\\\\hermes\\\\...` and `/mnt/i/hermes/...` paths, but they resolve differently. The Windows-style path writes to a location that `read_file` can see but the WSL terminal cannot. This causes `md2html.py` and `wc -c` to fail. **Solution**: always use `/mnt/i/hermes/output/doc/...` in write_file calls and terminal commands. If you accidentally used a Windows path, delete and re-`write_file` with the WSL path — do NOT rely on the first write being "good enough" because terminal-based verification will fail.
19. **ddgs is NOT a guaranteed fallback** — DuckDuckGo via ddgs is an HTML-scraped service, not an official API. It can intermittently return `None`/`ERROR: return None` for some queries while succeeding on others, then completely die mid-session with `ConnectError`. This is **not** fixable by retrying — Bing is actively blocking the connection. The correct response is: harvest partial ddgs results, switch immediately to curl rescue (`references/curl-html-rescue-pattern.md`), and rely on training knowledge for the rest. Don't waste time re-running ddgs or trying different proxies.

## Reference Files

- `references/ecosystem-survey.md` — Skills Hub / GitHub ecosystem survey methodology (weekly market report pattern with curl + API scraping, output versioning, cron scheduling)
- `references/ddg-fallback.md` — DuckDuckGo search fallback when Firecrawl credits exhaust
- `references/ddg-batch-research.md` — Batch ddgs query pattern (with Python HTML rescue augmentation)
- `references/curl-html-rescue-pattern.md` — Curl + Python HTML extraction when ddgs fails mid-session
- `references/html-generation.md` — HTML generation CSS and structure
- `references/ming-doctrine.md` — The philosophical foundation (Ming Doctrine v0.2) for the deeper vision of this system as a universal knowledge tutor
- `references/ifsq-quick-reference.md` — iFSQ 论文与代码的快速参考（研究+代码核心理念、性能数据、配置要点）
- `references/trilogy-quality-checklist.md` — 三部曲完成后质量门检查清单（B→A→C 常见遗漏）

## Scripts

This skill includes two scripts in `scripts/`. Location: `~/.hermes/skills/research/wiki-project-study/scripts/`.

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/md2html.py` | Single-file Markdown → HTML conversion | `python scripts/md2html.py in.md out.html "Title"` |
| `scripts/md2html-batch.sh` | Batch convert all .md files in a directory | `bash scripts/md2html-batch.sh /path/to/md/dir` |

The batch script is designed for multi-mode study output — after writing all three MD files (B→A→C), run it once to generate all HTML files in one pass. It skips files whose .html is already newer than the .md.

**⚠️ WSL note**: On WSL, use `python3` not `python` for terminal commands — `python` may not be aliased.
