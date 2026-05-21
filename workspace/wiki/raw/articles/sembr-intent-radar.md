---
source_url: https://mp.weixin.qq.com/s/lwmfvV21VIc1Sb50fmeLMg
ingested: 2026-05-19
sha256: pending
title: Sembr v1.0 开源：一句话中文，自动盯紧全球信息流
author: Peakstone Labs
source: 微信公众号
---

# Sembr v1.0 开源：一句话中文，自动盯紧全球信息流

**原文标题**：你的 Agent 还在用关键词搜新闻？——Sembr v1.0 开源

## 核心概念

自部署的意图雷达（Intent Radar）。用户用自然语言描述关注点，持续扫描 53 个中英文新闻源，用 BGE-M3 语义向量匹配，LLM 写分析摘要，推送到邮箱。

### Reverse RAG

经典 RAG：用户输入查询 → 检索匹配文档 → LLM 回答
Reverse RAG（Sembr）：用户定义意图 → 嵌入一次 → 每篇新文章匹配所有意图 → 命中后摘要推送

## 部署

```bash
git clone https://github.com/Peakstone-Labs/sembr.git
cd sembr
cp .env.example .env   # 填一行 API key
docker compose up --build
```

## 核心数据

- 预置源：53个（22 RSS + 1 Twitter + 30 NewsAPI.ai）
- 嵌入：BGE-M3（SiliconFlow 免费档）
- 向量库：Qdrant（int8 量化，10M 向量约 600MB RAM）
- LLM：DeepSeek-V4-Flash（默认）
- 成本：一个意图一天不到一毛人民币
- 推送：邮件（Telegram/Discord/Slack 路线图）
- 三个旋钮：匹配阈值(0-1) / 分析视角(Prompt) / 扫描节奏(5min~每天)

## Agent 作为一等公民

- 自部署：`sembr/agent/INSTALL.md` 面向 Agent 自主执行
- 自管理：`sembr/agent/sembr/` 含 5 份文件（SKILL.md + references），Hermes 等可直接用
- 流水线节点：`POST /api/external/intents/{id}/fire` 同步端点，一次 HTTP 调用返回匹配文章+LLM 摘要

## 竞品对比（五项全拿）

Feedly Pro+ AI / Inoreader Pro / Bloomberg Terminal / Perplexity Pro 均无法五项全拿：
1. 语义匹配 ✅
2. 双语中英 ✅
3. 自定义源 ✅
4. 自部署 ✅
5. 每意图独立分析 ✅

## GitHub 状态

- Stars: 2k
- Forks: 296
- Contributors: 22
- License: MIT
- 最新 commit: 2026-05-19
