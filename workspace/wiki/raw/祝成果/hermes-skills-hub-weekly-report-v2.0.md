# 🏛️ Skills Hub 每周巡查报告
## — 军师祭酒探市记 · 第二期

> **呈：** 张成市
> **日期：** 2026年5月17日（周日）
> **版本：** v2.0
> **范围：** agentskills.io · GitHub 社区 · NousResearch/hermes-agent
> **上次巡查：** v1.0 (2026.5.10) — 7 天前
> **巡查模式：** Cron 自动执行

---

## 一、巡查快照

| 维度 | v1.0 (5/10) | v2.0 (5/17) | 变化 |
|------|------------|------------|------|
| 你管理的技能数 | 85 | **119** | +34 🚀 |
| agentskills.io 规格 | 684 | 持续增长 | — |
| 支持 Agent Skills 客户端 | 约 20 | **33+** | +13 |
| GitHub 顶级 Skill 仓库 | drawio-skill ⭐1.4k | **addyosmani ⭐42k** | 市场爆量 |
| Hermes Agent ⭐ | ~100k | **~149.5k** | 7 天+50k🔥 |
| 官方发布版本 | v0.13.0 | 仍为 v0.13.0 | 活跃开发中 |

### 关键信号

- **Agent Skills 标准全面爆发**：33+ 客户端接入，微软/Stripe/Cloudflare/Netlify 官方出技能
- **你的技能库已经翻过百**（119），但不少是自动生成的 meta skill——真正需要关注的是"用上了多少"
- **v1.0 推荐的三件事全部完成**：Kanban 板已建 ✅ / daily-rituals skill 已创建 ✅ / drawio-skill 已安装 ✅

---

## 二、Hermes Agent 更新（5.10 → 5.16）

### 版本状态

仍为 **v0.13.0**「Tenacity Release」（5 月 7 日发布），但过去一周 **35 个重要 commit** 已推入 main，v0.14.0 在路上。

### 本周关键更新

| 更新 | 重要性 | 对你意味着什么 |
|------|--------|--------------|
| **PyPI / `pip install` 支持** 🆕 | 🔴 最高 | 终于能用 `pip install hermes-agent` 安装了，更新也走 `pip install --upgrade`。后续升级不用追 Git |
| **Notion v2.0 大修** 🆕 | 🔴 最高 | 三种安装路径（HTTP/ntn CLI/WSL回退）、`/markdown` 端点、Notion MCP 接线可选。这与你的 Notion skill/手册体系直接相关 |
| **xAI OAuth 修复** | 🔴 重要 | SSE 预读错误自动重试 + Entitlement 403 友好提示。如果你在用 Grok，这是必须的 |
| **Gateway 弹性升级** | 🟡 中 | 熔断器模式（10 次连续失败后暂停），`/platform list\|pause\|resume` 命令。多平台接入更可靠 |
| **Windows 可靠性修复** | 🟡 中 | 日志去重 / 文件锁竞争修复 / MSYS2 路径规范化。WSL 用户也可能受益 |
| **SSH OAuth 隧道提示** | 🟢 低 | 远程服务器 OAuth 流程会自动打印 SSH 转发命令 |

### 🚨 升级提醒

`hermes-upgrade-safety` skill 已加载。升级 v0.14.0 前必须：
1. 审查 release notes
2. 运行 `hermes update --check`
3. 确认 backup 存在

---

## 三、社区生态大爆发（这周最大的变化）

### 3.1 新增高星项目（v1.0 后新冒出来的）

| 项目 | ⭐ | 定位 | 
|------|---|------|
| **addyosmani/agent-skills** | **42.1k** 🚀 | 生产级工程技能，23 skill，7 个斜杠命令（spec/plan/build/test/review/simplify/ship），极致工程哲学 |
| **vercel-labs/agent-skills** | **26.6k** 🚀 | Vercel 官方：React 最佳实践（40+ 规则）、Web 设计审计（100+ 规则）、React Native、View Transitions |
| **VoltAgent/awesome-agent-skills** | **21.8k** 🚀 | 1000+ 精选技能聚合，48+ 官方团队（微软 133 skill、Anthropic、Stripe、Cloudflare、Sentry、Trail of Bits） |
| **tech-leads-club/agent-skills** | **2.4k** | 安全验证技能注册表，13.4% 开放市场技能有严重问题 → 他们的技能全经过 Snyk 扫描 |
| **supabase/agent-skills** | **2.1k** | Supabase 官方 DB/Auth/Edge Functions 技能，v0.1.2 (5/13) |
| **samber/cc-skills** | ⭐88 | 评测驱动的技能（发评估报告！），v1.10.0 (5/14)，误差率降低 14%-68% |
| **simota/agent-skills** | ⭐36 | 137 个专业 Agent 的大型生态，带 Nexus 编排器 |

### 3.2 趋势判断

**1️⃣ Skill 市场从「散装包」进入「聚合平台」时代**
- awesome-agent-skills（21.8k⭐）类似 npm registry
- officialskills.sh 月活 30 万
- 腾讯云也出了 SkillHub
- **结论**：个人散装 skill 的黄金期已过，聚合平台正在赢家通吃

**2️⃣ 企业官方技能井喷**
- 微软 133 个（.NET/Python/JS/Azure/M365 全系列）
- Stripe/Cloudflare/Netlify/Sentry/Trail of Bits/HashiCorp 全部出官方 skill
- **结论**：你的 wife-base / bing-search / wechat-article-fetch 等"非标工作流"仍然是护城河——大厂不会出国防基地运营 skill

**3️⃣ 安全性成为显学**
- tech-leads-club 的调研：开放市场 13.4% skill 有严重安全问题
- 扫描工具 snyk-agent-scan 出现
- **警惕**：不要盲目安装社区 skill

---

## 四、对你的影响评估

### 4.1 🟢 可补充/升级的领域

| 领域 | 推荐 | 理由 |
|------|------|------|
| **工程工作流** | addyosmani/agent-skills 的 `/spec` `/plan` `/build` `/review` | 你的 plan skill 已不错，但 addyosmani 的版本更成熟（42k⭐验证），斜杠命令模式更直观 |
| **React/前端** | vercel-labs/agent-skills 的 `react-best-practices` | 如果你碰前端，40 条规则值得引入 |
| **Supabase 操作** | supabase/agent-skills | 如果你在用 Supabase 做基地数据库 |
| **技能安全审计** | samber/cc-skills 的 snyk-agent-scan-compliance | 建议跑一轮你的 119 skill 做安全检查 |

### 4.2 🟡 建议吸收/参考的模块

**addyosmani 的 `interview-me` skill** — 通过轮番提问精准获取用户需求。你已经有类似思维模式，但可以借鉴它的 "6 行重述模板 + 自信指数" 的量化方法。

**samber/cc-skills 的评估方法论** — 每个 skill 有发布前评估（with skill vs without 的误差率）。你的 skill 基本没有系统性评估过。

### 4.3 🔴 警惕：社区 skill 质量可能低于自制

不要看到 42k⭐ 就冲动安装。你的 bing-search / wechat-article-fetch / wife-base / classic-to-fairy-tale 在各自领域（零成本中文搜索/微信生态/国防基地/非遗）**无可替代**。社区没有同品类，也不会有。

---

## 五、自上次行动清单回顾

### ✅ 已完成（v1.0 推荐全部执行）

| 任务 | 状态 | 备注 |
|------|------|------|
| 建 Kanban 板 | ✅ | main-board 已创建，3 个初始任务 |
| 创建 daily-rituals skill | ✅ | 读诗20行+手抄+分析/每周短诗/女儿15分钟→一体执行 |
| 安装 drawio-skill | ✅ | 已验证可用，生成了基地规划图 |
| 试用 humanizer | ✅ | 已可用 |
| 试用 baoyu-comic | — | 尚未启动 |

### ❌ 未完成

| 任务 | 原因 |
|------|------|
| 创建 wife-content-pipeline | 精力被其他项目分流，需要在 Kanban 上排期 |
| Kanban 从"试用"变成"日常" | 创建了板但还未形成习惯——这次报告的#1 行动项 |

---

## 六、本周 Top 5 推荐

### 🥇 #1：把 Kanban 变成日常习惯

之前建了板但没用起来。「创建 Kanban 板」只是第一步，「每天看板」才是目的。

**行动**：明天早上去 `/home/zcs/.hermes/kanban/` 看板上的状态。每天至少完成 1 张卡片。做不到的话，连 Kanban 这个工具本身也要重新设计。

### 🥈 #2：运行一次「军师技能审计」

119 个技能中真正频繁使用的不到 15 个。用 `skill_view` 分批审查：

1. 挑出超过 30 天未更新的技能
2. 判断：废弃 / 合并 / 归档
3. 专注 15 个核心技能

**节奏**：每月审一次，下月 15 号执行。

### 🥉 #3：创建 wife-content-pipeline（v1.0 #10）

这是唯一一个从 v1.0 挂到现在没完成的推荐。本周必须落地——建一个整合：
- wife-base（文案输出）
- baoyu-infographic（信息图）
- humanizer（去 AI 味）
- 一键产出公众号 + 抖音 + 小红书内容

**时限**：5 月 24 日前。

### ④ #4：评估 addyosmani/agent-skills 的 interview-me 模块

不安装整个仓库，只考察它在需求澄清上是否有可借鉴的方法。

### ⑤ #5：准备 v0.14.0 升级

v0.14.0 发布后（预计本周内），先跑 `hermes upgrade-safety` checklist，审查 release notes，再升级。**不要跳版本，不要盲目追新。**

---

## 七、军师最后的话

> 这周社区最大的新闻不是 Hermes 的更新，而是 Agent Skills 生态的**企业级爆发**。
>
> 微软、Stripe、Cloudflare、Vercel 都在出官方 skill——说明 Agent Skills 不再是玩具协议，而是基础设施建设。
>
> 你的 119 个技能里，有 15 个核心的已经够用了。问题从来不是 skill 不够，是**用不够**。
>
> 上周的"三件事"你都做了。这周的"一件事"是：**让 Kanban 从"存在"变成"习惯"**。
>
> 装 100 个 skill 不如把一个 skill 用 100 遍。
> 这句话从 v1.0 写到 v2.0，希望不用写到 v3.0。

---

*报告结束 · 每周日更新 · 下一期：2026年5月24日*
