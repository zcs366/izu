# Hermes 企业架构蓝图
## 基于老白四层架构的 Hermes 映射方案

> **来源灵感：** 老白《IM+Agent+Skills+Knowledge Base：新一代企业软件架构》
> **原文：** `raw/articles/im-agent-skills-knowledgebase-architecture.md`
> **评估：** `research/im-agent-skills-kb-architecture-evaluation.md`
> **本文定位：** 将老白的企业通用架构范式映射到 Hermes Agent 生态，形成可落地的企业部署蓝图

---

## 一、架构总览：老白四层 → Hermes 四层

老白描述的企业通用架构，每一层在 Hermes Agent 体系中都有精确的对应模块：

```
老白架构层                  Hermes 对应模块                  状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Layer 0: IM 交互层    →   Gateway（多平台接入层）            ✅ 已就绪
Layer 1: Agent 调度层 →   Agent Runtime（任务编排/路由）      ✅ 已就绪
Layer 2: Skills 层    →   Skill System + Skill Market        ✅ 已就绪
Layer 3: 系统原子能力 →   MCP Tools + Tool System             ✅ 已就绪
Layer 4: 知识库层     →   Wiki + Memory System + SOUL.md     ✅ 已就绪
```

**核心论断：** Hermes 已经拥有了老白描述的整套企业级架构的所有组件。这不是「需要做什么」，而是「如何把已有的东西组装成企业解决方案」。

---

## 二、逐层映射与配置方案

### Layer 0: IM 交互层 → Gateway

**老白观点**：IM 不是聊天工具，是企业 AI 的「操作系统界面」。Agent 不应该是 IM 里的一个机器人账号，而应该是底层协议级别的整合。

**Hermes 现状**：
- Gateway 已支持 15+ 渠道（Telegram / Discord / WeChat / DingTalk / Feishu / Yuanbao / SMS / Email 等）
- 每条消息经过统一的消息管道处理，不限于 IM 协议级别
- Gateway 已在生产环境中稳定运行

**企业部署建议**：
```
接入矩阵（按企业常用度排序）：
  P0 - 飞书（国内企业首选，上下文最完整）
  P0 - 钉钉（国内覆盖最广）
  P0 - 企业微信（微信生态联动）
  P1 - Slack（海外团队）
  P1 - Teams（M365生态）
```

**配置改动量**：每个渠道配置一次 API Token + Webhook，约为 0 行代码，5 分钟/渠道。

---

### Layer 1: Agent 调度层 → Agent Runtime

**老白观点**：
- 意图理解 → 任务规划 → 动态编排 → 人工确认 → 多Agent协调
- 自主度应与业务影响范围匹配

**Hermes 现状**：
- Agent Runtime 是 Hermes 的核心，天然支持多轮推理 + 工具调用 + 动态规划
- 已支持 Kanban 多Agent任务编排（依赖链/熔断器/Fleet模式）
- 人工审批机制已在安全模型中（技能安全扫描/智能审批/沙箱隔离）

**企业部署建议**：
```
自主度分级策略：
  查询类（读数据库、搜知识库）→ 全自动，无需审批
  写入类（创建工单、发邮件）→ 需用户一键确认
  高风险类（删除、签合同、付款）→ 需多人审批闭环
```

**配置改动量**：通过 SOUL.md 的审核规则定义，零代码，配置即可。

---

### Layer 2: Skills 层 → Skill System + Skill Market

**老白观点**：Skills 是「业务能力的原子单元」，是关键创新。Skills 使业务规则与代码解耦，由 Agent 动态编排而不是硬编码。

**Hermes 现状**：
- Skill 系统是 Hermes 的核心特征之一
- Skill Market 已有 647+ 个社区贡献的 Skills（2026-05现状）
- Skills 的输入/输出 schema 定义完整
- 支持自定义 Skills（写 python 文件即可）

**企业部署建议**：
```
Skill 分类清单（企业版）：
  
  通用 Skills（开箱即用）：
  ┣━ web_search / web_extract — 信息检索
  ┣━ read_file / write_file — 文档处理
  ┣━ terminal（受控）— 系统操作
  ┣━ image_generate — 内容生成
  ┗━ cronjob — 定时任务
  
  企业定制 Skills（需开发）：
  ┣━ ERP 查询 Skill（封装 SAP/Oracle API）
  ┣━ CRM 查询/写入 Skill（封装 Salesforce 等）
  ┣━ OA 审批 Skill（封装飞书/钉钉审批流）
  ┣━ 数据报表 Skill（封装 BI 工具）
  ┣━ 合同查询 Skill（封装合同管理系统）
  ┗━ 客户360 Skill（跨系统统一视图）
```

**关键洞察**：每个企业 Skill 本质上就是一个 MCP Tool 的实现。Hermes 已完整支持 MCP 协议层。

---

### Layer 3: 系统原子能力层 → MCP Tools + Tool System

**老白观点**：通过统一协议把现有系统能力暴露出来，供 Skills 调用。核心挑战是语义统一。

**Hermes 现状**：
- 完整的 Tool System 架构：注册 → 过滤 → 暴露 → 执行
- 原生支持 MCP 协议（业界标准）
- 支持 20+ 内置工具集（terminal/file/search/web/browser 等）
- MCP Gateway 概念页已入库

**企业部署建议**：
```
典型企业的 MCP 连接清单：
  财务系统（SAP/Oracle/金蝶/用友）→ 封装为查询/写入 MCP Tools
  CRM 系统（Salesforce/纷享销客）→ 封装为客户数据 MCP Tools
  OA 系统（飞书/钉钉/企业微信）→ 封装为审批/考勤 MCP Tools
  文档系统（Confluence/SharePoint/飞书文档）→ 封装为检索 MCP Tools
```

**实施路径**：每个系统连入 = 1 个 MCP Server 的部署配置，无需修改 Hermes 核心。

---

### Layer 4: 企业知识库 → Wiki + Memory + SOUL

**老白观点**：这是最难也最有价值的一层。知识库不是静态存储，而是持续运营的飞轮系统——越用越丰富，越用越准确。

**Hermes 现状**：
- **Wiki 知识库**：305+ 页知识体，80 概念页，71 实体，55 研究报告，全部跨文档可检索
- **Memory 系统**：Session Memory（FTS5跨会话召回）+ Working Memory（Top-K队列）+ Self Model（身份锚点快照）
- **SOUL.md**：核心身份文件，定义任务执行风格和协作协议
- **知识飞轮已在运转**：日报→论文审阅→核战队评估→知识入库，已形成每日知识循环

**企业部署建议**：
```
企业知识库分层：
  
  Layer 4a: 公开知识（已有 wiki + 46源公众号）— 行业知识、技术前沿
  Layer 4b: 企业私域知识（需企业自行灌入）— 内部文档、流程规范
  Layer 4c: 运营记忆（Memory系统）— 会话记录、决策历史
  Layer 4d: 身份锚点（SOUL.md）— 企业价值观、执行风格
  
  飞轮闭环：
  Agent 执行任务 → 日志下沉 → 自动摘要 → 知识库扩增 → Agent 能力提升 → 更多任务交给 Agent
```

**配置改动量**：企业私域知识灌入只需一次数据导入（文档批量处理），后续飞轮自动运转。

---

## 三、企业部署路径（三阶段）

### Phase 1: 基础接入（1-2周）
```
Day 1-3: Gateway 渠道接入（企微/飞书/钉钉任选一个）
Day 4-7: Wiki 知识库灌入（企业文档先导）
Day 8-14: 通用 Skills 开箱调试（搜索/文档/终端等）
成果: 企业内部的「超级知识助手」上线
```

### Phase 2: 系统打通（3-6周）
```
Week 3-4: MCP Server 连接第一个核心业务系统（如OA审批）
Week 5-6: 2-3个核心业务 MCP Tools 上线
Week 6: 原子化 Skills 封装 + 权限分级落地
成果: 企业核心业务可通过 Agent 查询和操作
```

### Phase 3: 飞轮运转（7-12周）
```
Week 7-8: 知识飞轮闭环搭建（自动摘要+回写知识库）
Week 9-10: Kanban 多Agent编排上线（复杂业务流程自动化）
Week 11-12: 安全审计 + 合规检查 + 业务人员培训
成果: 企业级 AI Agent 平台正式投产
```

---

## 四、对ITA的启示

老白架构中有一句深刻的话：**「Skills 是业务能力的原子单元」**。

这恰恰是 ITA 的镜像：
- Hermes Skill = 业务层面的「最小可验证能力单元」
- ITA 追求的 = 代码层面的「最小可验证语义单元」

它们的本质问题是相同的——**如何定义一个不可再分的能力/语义边界，让系统可以可靠地识别、调用和组合它？**

老白从架构层面给了答案（输入/输出Schema + 自然语言描述 + 权限边界），ITA 从代码语义层面给出答案（操作等价类聚类 + 隐空间编码 + Steering操控）。两条路径在同一个深层次问题上交汇。

---

## 五、行动清单

| # | 行动 | 优先级 | 工时 |
|:-:|------|:------:|:----:|
| 1 | 将本文写入 wiki/concepts/ 作为 Hermes 企业架构入口页 | P0 | 0.5h |
| 2 | 将老白原文与46源中的老范FDE企业AI/InfoQ MCP Gateway做交叉引用 | P1 | 1h |
| 3 | 补充企业级 Skills 的示例文档（在 Skill System 概念页中） | P1 | 1h |
| 4 | 将四层架构映射图更新到 Hermes Gateway 概念页 | P2 | 0.5h |

---

> **一句话总结：** Hermes 已经拥有了老白描述的完整企业架构的全部组件。不需要再造轮子，需要的是「把方向盘和座椅调对位置」——配置 → 接入 → 飞轮运转。

> 撰写：军师祭酒 · 2026-05-21
