---
source_url: file:///mnt/i/hermes/wiki_dropbox/hermes-skills-hub-market-report-v1.0.md
ingested: 2026-05-11
sha256: 5c1a2dbfc565c0cd090542b3ce00643a6acf23b906262920fd3a42865d5825c9
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: 🏛️ Skills Hub 市场趋势报告
---

# 🏛️ Skills Hub 市场趋势报告

> 来源: hermes-skills-hub-market-report-v1.0.md（用户存入 wiki_dropbox）

# 🏛️ Skills Hub 市场趋势报告
## — 军师祭酒探市记

> **呈：** 张成市
> **日期：** 2026年5月10日
> **版本：** v1.0
> **范围：** Hermes Skills Hub (agentskills.io) · GitHub 社区 · NousResearch/hermes-agent v0.13.0

---

## 一、探市路线

- 出发：agentskills.io（684 skill 总览）
- 深入：NousResearch/hermes-agent GitHub（v0.13.0 更新）
- 广撒网：GitHub 社区 Skill 仓库（15+ 活跃仓库抽样）
- 对标：你已有的 85 skill 对比市场主流

---

## 二、当前 Skill 市场主流格局

### 2.1 市场全景

| 维度 | 数据 |
|---|---|
| **总技能数** | **684** |
| 来源构成 | 87 Built-in（Hermes 原生） + 76 Optional + 521 Community |
| 分类体系 | 18 大类 |
| 注册中心 | 4 个（Hermes 官方 / Anthropic / LobeHub / Community） |
| 开放标准 | Agent Skills 格式（Anthropic 发起，Hermes/Claude Code/Codex 通用） |

### 2.2 热门品类 TOP 5

| 排名 | 品类 | 技能数 | 核心技能 |
|---|---|---|---|
| 🥇 | **Creative / 创意** | 19 内置 | p5.js · Manim · Excalidraw · ComfyUI · Ascii-art · Pixel-art · Songwriting |
| 🥈 | **MLOps** | 11 内置 | llama.cpp · vLLM · DSPy · Axolotl · Unsloth · lm-eval-harness |
| 🥉 | **AI Agents** | 4 内置 | Claude Code · Codex · OpenCode · Hermes Agent self-config |
| ④ | **Productivity** | 7 内置 | Airtable · Notion · Linear · Google Workspace · OCR · Nano-PDF · Maps |
| ⑤ | **GitHub** | 6 内置 | Code Review · Issues · PR Workflow · Repo Mgmt · Auth · Codebase Inspection |

### 2.3 冷门但高增长品类（值得关注）

- **Security（6个）** — v0.13.0 升格为独立品类，8个 P0 安全漏洞已修复
- **Finance（社区）** — 社区在推，但 Hermes 官方尚未覆盖
- **Translation（LobeHub 大量贡献）** — 你已有 classic-to-fairy-tale，可考虑扩展

---

## 三、社区生态动向（GitHub 巡视）

### 3.1 高星项目

| 项目 | ⭐ | 亮点 |
|---|---|---|
| **drawio-skill** (Agents365-ai) | ⭐1358 | 文本驱动专业图表，社区爆款 |
| **awesome-agent-skills** (jrmapa) | ⭐6 | 技能聚合目录，标准化趋势 |
| **agent-skills-directory** (XD-BASHARAT) | ⭐3 | TS 编写的技能搜索目录 |
| **AbsolutelySkilled** (Samuelca6399) | ⭐3 | 产线级领域技能合集，Astro 构建 |

### 3.2 新锐项目

| 项目 | 方向 |
|---|---|
| confid9ntial-fhevm-skill | Zama FHEVM 全同态加密 |
| reddit-skills | 浏览器自动化 Reddit 操作 |
| ios-skills-collection | 200+ iOS/Swift/Xcode SKILL.md |
| senpi-waifu | senpi 技能自主运行 CLI（TradeWife） |
| autoimprove-cc | 自动化 Claude Code SKILL.md 改进循环 |

### 3.3 趋势判断

> 社区正从「单技能仓库」向 **技能目录/聚合平台** 演化，
> 类比 npm 早期：散装包 → 目录索引 → 一键安装。
>
> Hermes Agent 已内置 `skills_list` 和 `skill_manage` 工具，
> 但**社区安装链尚未完全自动化**，这是你的先发窗口。

---

## 四、Tool 进展深度跟踪

### 4.1 v0.13.0「Tenacity 发布」（2026.5.7 — 三天前）

```
864 commits · 588 PRs · 282 issues 关闭 · 128,366 行变更
295 位社区贡献者
```

### 4.2 与你 workflow 相关的关键更新

| 功能 | 优先级 | 价值点 |
|---|---|---|
| **Kanban 多 Agent 板** | 🔴 最高 | 持久化任务板 + 心跳检测 + 僵尸回收 + 重试预算 + 幻觉门控 + 卡住自动通知 |
| **`/goal` 指令** | 🔴 最高 | 跨会话锁定目标，不再忘记要做什么 |
| **video_analyze 工具** | 🟡 中 | 基地训练视频分析、学员动作识别 |
| **xAI Custom Voices TTS** | 🟢 潜力 | 声音克隆，给孩子讲故事、基地宣传 |
| **Cron no_agent 模式** | 🟡 中 | 看门狗式定时脚本，零 token 开销 |
| **敏感信息默认打码** | 🟢 安全 | 输出自动过滤凭证 |
| **Google Chat 第 20 平台** | 🟢 弹性 | 按需接入 |

### 4.3 近期工具 bug 修复

- `vision_analyze` 修复：像素直传视觉模型，不再走辅助文本
- tool-result-storage 修复：通过 stdin 绕过 128KB 参数上限
- kanban 通知闭环：unblock 后重新通知

---

## 五、已有 Skill 替代性评估

### 5.1 自制 Skill 护城河

| 自制 Skill | 评估 | 行动 |
|---|---|---|
| **bing-search** | 零成本 + 高度个性化 | ✅ 维持，社区无可替代 |
| **wechat-article-fetch** | 微信生态壁垒 | ✅ 维持核心工作流 |
| **classic-to-fairy-tale** | 非遗独有品类 | ✅ 持续维护，可考虑扩展年表 |
| **wiki-project-study** | 深度研究+中文手册 | ✅ 已验证差异化优势 |
| **wife-base** | 基地全栈运营 | ✅ 核心资产，持续迭代 |
| **yuanbao** | 微信生态壁垒 | ✅ 维持 |

**结论：自制比社区同类质量更高，暂无需大换血。**

### 5.2 可用但未充分利用的内置 Skill

| Skill | 当前状态 | 建议激活场景 |
|---|---|---|
| `humanizer` | 已装少用 | 每次周报/公众号输出后跑一轮 |
| `sketch` | 已装少用 | 出方案/原型快速出 HTML |
| `popular-web-designs` | 已装未用 | 妻子基地宣传物料参考 |
| `baoyu-infographic` | 已装可用 | 托管招生海报、基地科普 |
| `baoyu-comic` | 已装可用 | 女儿反哺式教学、青少年国防教育 |

---

## 六、推荐 Top 10 — 按「军师诊断」优先排序

> 核心原则：先解决「精力太散」和「执行力」，再谈功能扩展。

### 🥇 第一梯队：立即行动，直接影响执行力

**① Kanban（已有）—— 今天就要建第一块板**
- 诊断中对症：一直在开始很少完成 → Kanban 让你开干的事有闭环
- 建议：今晚建一块板，放明天要完成的 3 件事。养成习惯前先跑起来

**② 自建 `daily-rituals` Skill 🆕**
- 诊断中的每日功课打包：读诗 20 行 + 手抄 + 50 字分析 / 每周一首短诗 / 每天 15 分钟教女儿
- 作用：一个指令执行每日闭环，不再"记得就做，忘了就算"

### 🥈 第二梯队：增强输出质量

**③ `drawio-skill`（社区爆款 ⭐1358）🆕**
- 基地规划图 / 学校流程 / 知识体系图 / 项目时间线
- 一句话：一张图胜过千言

**④ `humanizer`（已有）.set_active()**
- 周报/公众号/方案输出 → 去 AI 味 → 质感提升一个档次
- 你作为文字工作者，这是必用工具

**⑤ `sketch`（已有）.set_active()**
- 快速出 HTML 原型比写长篇文档效率高 10 倍

### 🥉 第三梯队：妻子事业助攻

**⑥ `popular-web-designs`（已有）.set_active()**
- 基地/托管宣传物设计参考源

**⑦ `baoyu-infographic`（已有）.set_active()**
- 基地科普 / 托管招生 → 信息图比文字触达率高 3 倍

**⑧ `baoyu-comic`（已有）.set_active()**
- 女儿教学 + 青少年国防教育 → 最佳载体

### 🟢 第四梯队：长期潜力

**⑨ `maps`（已有）.set_active()**
- 基地场地规划 / 接送路线 / 山林 CS 路线设计

**⑩ 自建 `wife-content-pipeline` 🆕**
- 整合 wife-base + baoyu-comic + baoyu-infographic + humanizer + youtube-content
- 一个指令 = 3 平台内容 + 1 信息图 + 1 漫画
- **这是效率的量变到质变**

---

## 七、行动清单（军师军令）

### 今天（5月10日）

- [ ] **建第一块 Kanban 板**，放明天 3 件事
- [ ] 装 `drawio-skill`
- [ ] 试用一次 `humanizer` 处理一段文字

### 本周内

- [ ] 创建 `daily-rituals` skill，设置每日功课提醒
- [ ] 试用 `baoyu-comic` 给女儿做一个知识漫画
- [ ] 试用 `sketch` 出一个基地概念原型

### 本月内

- [ ] 创建 `wife-content-pipeline` 一站式产出管线
- [ ] Kanban 从"试用"变成"日常"

---

> **军师最后的话：**
>
> Skills Hub 684 个技能，你有的 85 个已经覆盖 80% 的功能面。
> 你最大的短板不是技能不够，是真把它们用起来。
>
> 装 100 个技能不如把一个技能用 100 遍。
> 今天就从 Kanban 那块板开始。

---

*报告结束 · 每周日更新 · 下一期：2026年5月17日*

