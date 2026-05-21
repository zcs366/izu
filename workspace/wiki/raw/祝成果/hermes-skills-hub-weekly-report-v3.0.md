# 🏛️ Skills Hub 每周巡查报告
## — 军师祭酒探市记 · 第三期

> **呈：** 张成市
> **日期：** 2026年5月17日（周日）
> **版本：** v3.0
> **范围：** agentskills.io · GitHub 社区 · NousResearch/hermes-agent
> **上次巡查：** v2.0 (2026.5.16) — 1 天前
> **巡查模式：** Cron 自动执行

---

## 一、巡查快照

| 维度 | v2.0 (5/16) | v3.0 (5/17) | 变化 |
|------|------------|------------|------|
| 你管理的技能数 | 119 | **119** | 持平 |
| Hermes Agent ⭐ | ~149.5k | **153k** | +3.5k 🔥 |
| 支持 Agent Skills 客户端 | 33+ | **~43** | +10 🚀 |
| 顶级 Skill 仓库 #1 | addyosmani ⭐42.1k | **mattpocock ⭐86.9k** 🆕 | 新王登基 |
| 顶级 Skill 仓库 #2 | addyosmani ⭐42.1k | **addyosmani ⭐42.5k** | +400 |
| 顶级 Skill 仓库 #3 | VoltAgent ⭐21.8k | **VoltAgent ⭐22k** | +200 |
| 官方发布版本 | v0.13.0 (5/7) | **v0.14.0 (5/16)** 🆕 | 9 天后大版本 |
| GitHub gh skill CLI | — | **正式发布** 🆕 | 技能管理标准化 |
| Scientific Agent Skills | 未记录 | **K-Dense-AI ⭐5.7k** 🆕 | 科研新品类 |

### 关键信号

- **v0.14.0 昨天发布了！** — 这是 Hermes 史上最大的基础设施版本。PyPI 安装、Windows 原生、xAI Grok、X 搜索、Teams、`/handoff`…… 一堆大东西
- **Matt Pocock 的 skill 仓库爆了** — 86.9k⭐，一周前 #1 GitHub Trending。哲学和 addyosmani 完全不同（轻量、可组合、聚焦沟通对齐而非流程纪律），值得深入考察
- **gh skill CLI** — GitHub 正式推出官方 skill 管理工具，技能分发的"最后一公里"问题被解决
- **你的技能数持平（119）** — 这是好事。v2.0 强调"用够 100 遍"，v2.0 到 v3.0 间隔才 1 天，没有新增是合理的

---

## 二、Hermes Agent v0.14.0「Foundation Release」— 深度解读

**发布时间：** 2026年5月16日（昨天）
**版本号：** v0.14.0
**代号：** "The Foundation Release"
**规模：** 808 commits · 633 PRs · 1393 文件变更 · 165k 行新增 · 545 issues 关闭

### 核心更新（按对你影响排序）

| 更新 | 重要性 | 对你意味着什么 |
|------|--------|--------------|
| **PyPI 安装** 🆕 | 🔴 最高 | `pip install hermes-agent` 即可。更新走 `pip install --upgrade`，不再追 Git。升级流程彻底简化 |
| **OpenAI 兼容本地代理** 🆕 | 🔴 最高 | `hermes proxy` 把 Claude Pro/ChatGPT Pro/SuperGrok 的 OAuth 转成 OpenAI 端点，给 Codex/Aider/Cline 用。如果你交叉使用多种 agent，这是桥梁 |
| **x_search（X/Twitter 搜索）** 🆕 | 🔴 重要 | OAuth 或 API key 接入，实时搜 X。对舆情监测/行业动态追踪极有价值——结合 paper-top-digest 可以做一个"热点脉冲"信号 |
| **Microsoft Teams 支持** 🆕 | 🔴 重要 | 全链路（Graph 认证 + webhook + pipeline + 推送）。如果基地/学校/托管用 Teams 协作，可直接接入 |
| **hermes send CLI 命令** 🆕 | 🔴 重要 | `hermes send --to telegram "消息"` / 管道输入 / `--file` 支持。Cron/脚本直通 gateway，无需跑完整网关。这对 cron job 输出落地极有价值 |
| **/handoff 实时会话转移** 🆕 | 🟡 高 | 在不同模型/角色间实时转交会话。可将复杂任务转给更强模型处理 |
| **xAI Grok OAuth** 🆕 | 🟡 高 | grok-4.3，1M 上下文窗口。推理/长文档分析备用 |
| **跨会话 1h Claude 提示缓存** | 🟡 中 | Anthropic/OpenRouter 通道的提示缓存有效期延长到 1 小时。长会话性能提升 |
| **Windows 原生 Beta** | 🟡 中 | PowerShell 安装器。如果你有 Windows 用户，这降低门槛 |
| **LINE + SimpleX Chat** | 🟢 低 | 两个新平台，共 22 个 messaging 平台 |
| **冷启动提速 ~19s** | 🟢 低 | `hermes` 启动更快了 |
| **browser_console 提速 180x** | 🟢 低 | 持久 CDP WS 连接 → 浏览器操作响应极快 |

### 🚨 升级提醒

v2.0 已经提醒过了，现在正式发布，可以行动了：

1. `pip install --upgrade hermes-agent`
2. 运行 `hermes doctor` 诊断兼容性
3. 试用 `hermes send --to telegram "test"`（见下方 #4 推荐）
4. 配置 `x_search` 工具（如需要）

---

## 三、社区生态：本周最大的新闻是 Matt Pocock

### 3.1 技能仓库排位变了

本周最震撼的变化：**mattpocock/skills 以 86.9k⭐ 超越 addyosmani（42.5k⭐）成为 GitHub Skill 仓库第一。**

| 排名 | 仓库 | ⭐ | 哲学 | 定位 |
|------|------|---|------|------|
| 🥇 | **mattpocock/skills** 🆕 | **86.9k** | 轻量/可组合/聚焦沟通对齐 | 工程沟通技能包（/grill-me /diagnose /tdd） |
| 🥈 | addyosmani/agent-skills | **42.5k** | 严谨/流程驱动/spec→plan→build | 生产级工程技能框架（/spec /plan /build） |
| 🥉 | VoltAgent/awesome-agent-skills | **22k** | 聚合/目录 | 1000+ 官方+社区技能目录 |
| ④ | K-Dense-AI/scientific-agent-skills 🆕 | **5.7k** | 科学/研究专用 | 135 个科研专用技能 + 100+ 数据库接口 |
| ⑤ | vercel-labs/agent-skills | **~26k** | React/前端 | Vercel 官方 40+ 规则 |

### 3.2 mattpocock/skills 深度分析

**为什么火？**
Matt Pocock（TypeScript 权威，前 Vercel）从自己 `.claude` 目录直接开源。不是"设计出来的框架"，是**每天在用的实际工具**。

**核心技能矩阵：**
```
/grill-me          → 详细提问对齐需求（非代码场景）
/grill-with-docs   → 对齐 + 创建共享语言 CONTEXT.md + ADR
/tdd              → 红-绿-重构循环
/diagnose         → 结构化调试循环
/triage           → issue 分类状态机
/zoom-out         → 系统上下文理解代码
/to-prd           → 模块化→PRD
/improve-codebase-architecture → 泥球代码库救援
/setup-matt-pocock-skills → 一键安装向导
```

**和 addyosmani 的核心差异：**

| 维度 | mattpocock | addyosmani |
|------|-----------|-----------|
| **风格** | "别试图读心，先对齐然后写代码" | "先写 spec 再写代码" |
| **技能数** | ~20（精炼） | 23（系统化） |
| **安装方式** | `npx skills@latest add` | `/plugin market add` |
| **核心价值** | 沟通对齐 + 术语统一 + TDD | 全生命周期：spec→plan→build→test→review→ship |
| **star 增长速度** | 爆炸性（77k→86.9k 一周内） | 稳定增长 |

**对你的影响：**
- `/grill-me` 和 `/grill-with-docs` 与你的 `five-agent-consultation` 有互补性
- `/diagnose` 的调试循环比大多数通用调试流程更精炼
- `/triage` 的 issue 状态机可借鉴到你的 Kanban 工作流中

### 3.3 其他值得关注的新项目

| 项目 | ⭐ | 值得关注的点 |
|------|---|-----------|
| **K-Dense-AI/scientific-agent-skills** 🆕 | 5.7k | 135 个科研技能（化学/生物/医学/金融）。如果你的 izu-pipeline 涉及科学领域研究，这是强力补充 |
| **microsoft/azure-skills** 🆕 | — | 微软 Azure 技能插件：19+ skills + 200+ MCP 工具 + Foundry 集成。如果你碰 Azure 生态，值得看 |
| **gh skill CLI** 🆕 | — | 4月16日发布，5月成为热话题。`gh skill install` / `gh skill publish` / `gh skill list`。正式标准化了技能的分发流程 |

### 3.4 趋势判断

**这周最大的趋势：Skill 仓库从"工程框架"走向"个人风格化工具"。**

- addyosmani = 系统化/流程驱动/大型工程 → 适合复杂团队
- mattpocock = 轻量/沟通驱动/个人风格 → 适合独立开发者和小团队
- **两个都不冲突，互补使用**

---

## 四、对你的影响评估

### 4.1 🟢 直接可用的新能力

| 能力 | 来源 | 价值 | 建议 |
|------|------|------|------|
| **hermes send CLI** | v0.14.0 | Cron 脚本直出 Telegram/其他平台 | ✅ 立即试用。你的 cron job 输出可以走 `hermes send --to telegram` 直达手机 |
| **x_search** | v0.14.0 | 实时搜 X（Twitter） | 🟡 评估。对基地/托管行业舆情监测有用 |
| **hermes proxy** | v0.14.0 | OAuth 转 OpenAI 代理 | 🟡 如果你同时用 Codex/其他 agent，这是一个桥 |
| **/grill-me + /grill-with-docs** | mattpocock | 轻量版五人合议 | 🟡 参考其"提问→对齐"的交互模式 |

### 4.2 🟡 可吸收参考的模块

- **mattpocock 的 `/triage` 状态机** — 你 Kanban 工作流的 issue 流程可以借鉴它的角色定义
- **mattpocock 的 `/diagnose` 调试循环** — 精简版（reproduce → minimise → hypothesise → instrument → fix → regression-test）。比你的通用调试更结构化
- **mattpocock 的共享语言思想**（CONTEXT.md + 术语统一）— 你的技能库中缺少"共享术语"这一层

### 4.3 🔴 护城河依旧坚固

你独有的技能（bing-search / wechat-article-fetch / wife-base / classic-to-fairy-tale / izu-pipeline / daily-rituals）仍然没有社区替代品。社区里的都是通用工程技能，非标工作流只有你有。

---

## 五、自上次行动清单回顾

### ✅ 已完成

| 任务 | 状态 | 备注 |
|------|------|------|
| 建 Kanban 板 | ✅ (v2.0) | 已建但未形成日常习惯 |
| 创建 daily-rituals skill | ✅ (v2.0) | 已在用 |
| 安装 drawio-skill | ✅ (v2.0) | 已验证 |
| 试用 humanizer | ✅ (v2.0) | 已体验 |

### ❌ 未完成

| 任务 | 原因 |
|------|------|
| 试用 baoyu-comic | 精力被其他项目分流 |
| 创建 wife-content-pipeline | 仍未落地，v1.0 到 v3.0 三周未动 |
| Kanban 从"试用"变成"日常" | 板建了但没养成习惯 |

### v2.0 推荐项回顾

| # | 推荐 | 状态 |
|---|------|------|
| 🥇 Kanban 变成日常习惯 | ❌ 未完成 |
| 🥈 军师技能审计 | ❌ 未启动 |
| 🥉 创建 wife-content-pipeline | ❌ 仍未落地 |
| ④ 评估 addyosmani interview-me | ❌ |
| ⑤ 准备 v0.14.0 升级 | ✅ **v0.14.0 已发布，现在可以行动** |

---

## 六、本周 Top 5 推荐

### 🥇 #1：升级到 v0.14.0

昨天发布的 Foundation Release 是 Hermes 史上最大的基础设施版本。PyPI 安装、`hermes send`、x_search、proxy 全是实用的。

**行动：**
```bash
pip install --upgrade hermes-agent
hermes doctor
```

### 🥈 #2：试用 `hermes send` 打通 cron 输出链路

这是 v0.14.0 里你最该立即用的功能：

```bash
hermes send --to telegram "Skills Hub 巡查完成"
cat report.md | hermes send --to telegram:-1001234567890
```

一下子让你的所有 cron job（本报告、论文日报、管弦乐队）都能直出 Telegram。**不需要跑完整 gateway。**

### 🥉 #3：阅读 mattpocock/skills 的/grill-me 和/diagnose

不安装整个仓库，只考察两个技能的思路：
- `/grill-me` — 它的"对齐提问"模式和你五人合议的开头（子产断该不该）有异曲同工
- `/diagnose` — 它的调试循环可以给你的软件工程工作流提供补充

查看：
```
https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me
https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnose
```

### ④ #4：装 `hermes send` 后的第一件事——用管道输出这篇报告

```bash
cat hermes-skills-hub-weekly-report-v3.0.md | hermes send --to telegram "Skills Hub 巡查 v3.0"
```

这不仅是试工具，而是构建"看完报告→落到手里"的最后一公里。

### ⑤ #5：正式把 wife-content-pipeline 排上日程

从 v1.0 起三周没落地的唯一推荐。v3.0 不能再拖了。

**最小可行方案**：创建一个整合脚本，把 wife-base + humanizer 串起来，一个命令生成三平台内容。不需要一次做完，先跑通单平台链路。

可借鉴的已用工具：`hermes send`（v0.14.0）→ 输出能直达妻子微信/Telegram。

---

## 七、军师最后的话

> 这周是两个"新王"的故事。
>
> 第一，**v0.14.0 发布了**。Hermes 从"git clone 才能用"变成了"pip install 就能用"。这个变化比你想象的大——它意味着 Hermes 正式从早期用户阶段进入主流可用阶段。你要接住这个信号。
>
> 第二，**Matt Pocock 86.9k⭐** 在不到一周内超越 addyosmani 四个月的积累。这说明 community 不只需要流程纪律（addyosmani），更需要"对齐先于执行"的沟通工具。你已经在用五人合议做这件事——但可以做得更轻量、更日常。
>
> **这次 Top 5 推荐和前两次不一样：**
> - v1.0 说"装东西"
> - v2.0 说"用起来"
> - **v3.0 说"打通最后一公里"**
>
> 升级 v0.14.0 → 装 hermes send → 把巡检报告推到你手机上。这周就这一件事：**让你的 cron job 输出真的到达你的手机。**

---

*报告结束 · 每周日更新 · 下一期：2026年5月24日*
