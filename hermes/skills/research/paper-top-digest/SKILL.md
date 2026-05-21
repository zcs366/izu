---
name: paper-top-digest
description: 每日从论文下载TOP10、技术博客TOP5、论坛TOP5、视频平台等全源搜索筛选前沿AI/科技内容，输出结构化日报（2-3篇精选），发 Telegram 和元宝。支持重复推荐和项目关联匹配。
version: 2.0.0
metadata:
  hermes:
    tags: [paper, digest, daily, ai, frontier, search, cron]
    category: research
    related_skills: [paper-translate-research, wiki-drop, bing-search, youtube-content]
author: Hermes Agent
------

# 论文前沿日报 — Paper Top Digest v2.0

> **🔑 触发词**：`paper日报`
>
> 定时任务每日 08:00 自动执行，也可手动触发。

## 核心理念

不追求"新"而追求"值"——每天只推 2-3 篇真正值得读的内容。可以重复推荐（好论文不怕看两遍），可以循环推荐（同一主题持续跟进）。选文标准：**下载/阅读/点赞量高**，或**与我们正在做的项目直接相关**。

## 我们正在做的项目（用于关联匹配）

| 项目 | 关键词 | 匹配方向 |
|------|--------|---------|
| **爱祝（izu）** | AI研究、知识管理、智能体协作 | Agent架构、RAG、知识图谱、多Agent系统 |
| **Hermes Agent** | AI Agent框架、工具调用、Gateway | Agent框架设计、工具编排、MCP协议、网关架构 |
| **Wiki 知识系统** | 知识库、Markdown/HTML、信息摄入 | 文档格式、知识管理、信息检索、GraphRAG |
| **论文skill / 转录skill** | 学术翻译、音视频转录 | 翻译模型、Whisper/STT、多模态理解 |
| **日常管理** | 运输安全、国防教育、家庭教育 | 相关行业技术应用 |

## 信息来源（全源覆盖）

### 一、论文下载源

| # | 来源 | 搜索方式 | 看什么 |
|---|------|---------|--------|
| 1 | **HuggingFace Daily Papers** | web_extract huggingface.co/papers | 社区投票数、下载量 |
| 2 | **arXiv** | API（cs.AI / cs.CL / cs.LG / cs.CV） | 新提交 + 高引用 |
| 3 | **Papers With Code** | web_extract paperswithcode.com | SOTA 基准 + GitHub stars |
| 4 | **Semantic Scholar** | web_search + API | 引用量、影响力分数 |
| 5 | **Google Scholar** | web_search | 高引新论文 |
| 6 | **OpenReview** | web_extract openreview.net | 顶会审稿讨论热度 |
| 7 | **ACL Anthology** | web_extract aclanthology.org | NLP 领域最佳论文 |
| 8 | **PMLR** | web_extract proceedings.mlr.press | ICML/NeurIPS 最新论文集 |
| 9 | **ResearchGate** | web_search | 阅读量、下载量 |
| 10 | **Connected Papers** | web_extract | 重要论文的关联图谱 |

### 二、技术博客源

| # | 来源 | 搜索方式 |
|---|------|---------|
| 11 | **Medium**（Towards Data Science） | web_search site:medium.com |
| 12 | **Substack**（AI 作者） | web_search site:substack.com |
| 13 | **Hacker Noon** | web_extract hackernoon.com |
| 14 | **Dev.to** | web_search site:dev.to |
| 15 | **机器之心 / 量子位** | web_extract（中文源） |

### 三、论坛源

| # | 来源 | 搜索方式 |
|---|------|---------|
| 16 | **Hacker News** | HN API `/topstories` → 过滤 AI/LLM/ML |
| 17 | **Reddit** r/MachineLearning / r/LocalLLaMA | Reddit JSON API → 按 hot |
| 18 | **LessWrong** | web_search site:lesswrong.com |
| 19 | **知乎**（AI/LLM 话题） | web_search site:zhihu.com |
| 20 | **Lobsters** | web_extract lobste.rs |

### 四、视频源（论文解读视频）

| # | 来源 | 搜索方式 |
|---|------|---------|
| 21 | **YouTube**（AI 论文解读频道） | web_search + youtube-content skill |
| 22 | **B站**（AI 论文解读 UP 主） | web_search + bilibili API |

## 筛选标准

### 量化指标（客观）

| 指标 | 来源 | 阈值 |
|------|------|------|
| HuggingFace 投票/下载 | HF Papers | >20 votes |
| arXiv 引用量 | Semantic Scholar | >5（新论文放宽） |
| GitHub Stars | Papers With Code | >100 |
| HN 评论数 | Hacker News | >30 |
| Reddit 点赞数 | Reddit | >50 |
| 阅读量/播放量 | 博客/视频 | >5000 |

### 项目关联度（主观判断）

每当一篇内容与上述项目关键词匹配，加一档推荐星级。

### 星级标准

| ⭐ | 含义 |
|-----|------|
| ⭐⭐⭐⭐⭐ | 必读——直接相关 + 高热度 |
| ⭐⭐⭐⭐ | 推荐——高热度或强相关 |
| ⭐⭐⭐ | 可选——一般热度，可扩展视野 |

## 输出格式

每天 **2-3 篇**，按以下格式：

```markdown
# 📄 AI 前沿日报

**日期**：2026-05-14 · **呈：张成市**
**今日精选**：2 篇 ｜ 来源：arXiv / HN / HuggingFace
**关联项目**：爱祝 / Hermes

---

## 1. 论文标题（English Title）

- **技术分类**：Agent 架构
- **来源**：[arXiv 2501.xxxxx](url) ｜ HN 讨论 [42 comments](url)
- **热度**：❤️ 156 · 💬 42 · ⭐ GitHub 320
- **主要观点**：（≤50字）
- **摘要**：（3-5句中文）
- **与我们相关**：直接关联 Hermes Agent 的工具编排设计，特别是第3节的多Agent调度策略
- **推荐**：⭐⭐⭐⭐⭐
- **扩展阅读**：
  - 关联论文：[Title](url)
  - 解读博客：[Title](url)
  - 视频解读：[B站/YouTube](url)

---

## 2. 论文标题（English Title）

...（同上格式）

---

> 💡 **军师的话**：（1-2句趋势观察或盲点提醒）
>
> 📌 **昨日值得重读**：昨日推荐的 XX 论文，今天社区有新讨论 → [链接]
```

## 重复推荐规则

同一篇论文可以在以下情况再次推荐：
1. 社区出现新的重要讨论/解读
2. 有团队发布了开源复现
3. 与我们新启动的项目产生了关联
4. 距上次推荐已过 7 天，且仍有讨论热度

## 循环推荐规则

同一主题的论文可连续多日推荐不同篇，形成主题追踪线。

## 手动触发与定时任务

- **手动**：说 `paper日报`
- **定时**：每日 08:00 → Telegram（龙马）+ 元宝（刺史频道）
- **定时任务 ID**：`65eba5595103`

## 依赖

- `web_search` / `web_extract` / `bing-search` skill
- arXiv API、HN API、Reddit JSON API（均免费无需 key）
- Semantic Scholar API（免费）
