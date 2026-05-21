---
title: Hermes 自动知识库工作流
created: 2026-05-07
updated: 2026-05-07
type: concept
tags: [workflow, automation, wiki]
sources: [raw/articles/hermes-auto-wiki-workflow-yutou.md]
confidence: medium
---

# Hermes 自动知识库工作流

由 [[芋头小宝]] 实践并分享的自动化知识系统方案，使用 [[Hermes Agent]] 将 Obsidian/Karpathy LLM Wiki 从"手动维护的被动仓库"升级为"自动运转的知识系统"。

## 流水线

```
[定时触发]
    │
    ▼
1. AutoCLI 抓取信息  ─── Hermes 调度，按日期归档到 Obsidian
    │
    ▼
2. llm-wiki 编译入库  ─── Hermes 调用内置 skill，压成认知地图
    │
    ▼
3. 微信日报推送      ─── 入库完成自动生成日报发送到微信
```

## 三步骤详解

### 步骤 1：AutoCLI + Hermes 自动抓取
- [[AutoCLI（OpenCLI）]] 浏览器抓取工具，复用 Chrome 登录态，无需 API Key
- 抓取 X/Twitter 点赞 top10 等内容，按日期归档
- 创建定时任务（cron），每天固定时间自动执行

### 步骤 2：Hermes + llm-wiki 编译入库
- Hermes 调用内置 `llm-wiki` skill，将抓取内容转化为结构化 wiki 页面
- "让 Hermes 充当知识编译器，把信息流压成认知地图"
- 与步骤 1 串联成定时流水线，无需人工介入

### 步骤 3：微信日报推送
- Hermes 接入个人微信渠道
- 入库完成后自动生成日报：今日总览 → 重点摘要 → 报告位置
- 主动汇报，驱动用户每天查看和使用知识库

## 核心价值

- **以前**：把内容往知识库里堆（被动仓库）
- **现在**：知识库自己运转——自动接新信息 → 自动归档整理 → 自动按主题沉淀 → 自动汇报结果

"让'沉淀'第一次变成了'反馈'，让'存档'真正变成了'经营'。"

## 相关条目

- [[Hermes Agent]]
- [[芋头小宝]]
- [[AutoCLI（OpenCLI）]]
- [[llm-wiki]]（Karpathy LLM Wiki 系统）
