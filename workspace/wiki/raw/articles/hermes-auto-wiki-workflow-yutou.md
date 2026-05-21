---
source_url: https://mp.weixin.qq.com/s/3G6Dw7Up_fFgu1gGzqrV2A
ingested: 2026-05-07
sha256: 50dc7098c9036161e535a39177b03ac31e5d35f42e331ec5ece391e9aade838b
source: 微信公众号
author: 芋头小宝
description: Hermes+Obsidian+AutoCLI+WeChat，构建自动抓取→编译入库→微信日报的AI知识系统
---

# 用 Hermes 搭了一套「自动抓信息→入库知识库→微信汇报」的系统

作者：芋头小宝

## 痛点

使用 Karpathy LLM Wiki 一段时间后发现"有点重"：每天手动筛选文章、拷贝输入输出、离不开电脑——"感觉自己像是在给 AI 打工，充当 AI 的手脚"。

**升级方案**：结合 Hermes Agent，搭建自动抓取信息入库、自动筛选整理、分类沉淀、自动微信汇报的知识系统。

## 流程概览

```
定时抓取信息 → 编译进 LLM Wiki → 微信汇报入库结果
```

## 三步拆解

### 1. AutoCLI + Hermes：信息抓取自动化

**AutoCLI（OpenCLI）**：浏览器信息抓取开源项目，无需 API Key，复用 Chrome 已有登录态，支持 90+ 站点。

在 Obsidian 中建立 `AI NEWS HUB` 文件夹，让 Hermes 在指定路径下执行抓取任务。Hermes 自动创建多层级目录，按日期归档。

然后创建定时任务（cron），每天下午 5 点自动执行抓取。

### 2. Hermes + llm-wiki skill：定时梳理入库

在 `AI NEWS HUB` 路径下，让 Hermes 调用内置的 `llm-wiki` skill 将抓取内容转化为 wiki。

> "让 Hermes 充当知识编译器，把信息流压成认知地图。"

步骤 1 和步骤 2 可以串联成定时流水线——抓取完成后自动入库，不需人工盯着。

### 3. Hermes + 微信：日报推送

Hermes 接入个人微信渠道后，入库完成后自动生成日报，把新增的关键信息发到微信。

日报结构：一句话同步结果 → 今日重点 → 100 字摘要 → 报告位置。

> "它主动汇报，才能督促我每天都会看知识库，用知识库。"

## 核心价值：从"堆"到"运转"

```
以前：把内容往知识库里堆
现在：知识库自己运转——自动接新信息→自动归档整理→自动按主题沉淀→自动把结果汇报给我
```

## 相关文章推荐（同作者）

- 卡兹克写作风格 Skill + Karpathy LLM Wiki：构建能自我进化的文章写作知识库
- 0成本玩转龙虾智能体（OpenClaw 系列多篇）
