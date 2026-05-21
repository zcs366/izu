---
source_url: https://mp.weixin.qq.com/s/Yl75baRMkEF7mNAyRc-WAQ
ingested: 2026-05-07
sha256: 8ba6fb35787faabe613d2cba4652af1a4021991f5c0fa959c41352256b3ee502
source: 微信公众号
author: 60分男人（养马系列）
description: 用 OpenCLI 打造纯终端 Bing 自动化搜索技能，本地存档、自动去重、封装为 Hermes Skill，实现零 API 成本的自主可控搜索
---

# 养马系列：纯终端 Bing 自动化搜索 + 本地内容存档

作者：60分男人

## 背景

Hermes 自带搜索的痛点：付费 API 成本高、不稳定、结果不完整。用 OpenCLI 的 browser 功能模拟人类浏览器行为，实现**零 API 成本**的全网搜索。

## 核心脚本：bing_search_skill.sh

一个 Bash 脚本，自动完成 Bing 搜索 → 翻页 → 提取链接 → 下载网页内容 → 按日期归档。

### 关键特性
- **模拟人工操作**，规避反爬检测
- **自动修复**带前缀的非法链接
- **按日期归档**结果（`bing_search_result/YYYY-MM-DD/`）
- **自动去重**：当天多次搜索自动追加索引，不重复下载
- **纯终端运行**，无需桌面环境

### 目录结构
```
bing_search_result/
└─ 2026-05-03/
   ├─ 00_搜索索引.txt        # 所有结果的标题+链接索引
   └─ pages/                 # 所有网页的 Markdown 内容
      ├─ 1_标题1.md
      └─ 2_标题2.md
```

### 使用方式
```bash
./bing_search_skill.sh "关键词" 页数
```

## 封装为 Hermes Skill

在 `~/.hermes/skills/research/bing-search/` 创建 SKILL.md：

```yaml
name: bing-search
description: 使用 OpenCLI 进行 Bing 自动化搜索，保存网页内容到本地
tags: [research, search, opencli, bing]
```

调用方式：`使用 bing-search 技能搜索"关键词"，翻10页，然后总结核心内容`

## 核心价值：省钱 + 自主可控

- **零 API 费用**：浏览器能看到什么，AI 就能拿到什么
- **Token 消耗砍 90%**：先下载到本地过滤，再喂给大模型，不传广告/导航
- **数据自主可控**：所有内容在本地硬盘，不怕 API 涨价/关停/泄露
- **可扩展**：定时监控关键词、自动跟踪新闻、批量竞品分析

## 系列归属

本文为 **养马系列技术专栏** 的一篇，专注于个人 AI 助手的自主可控与生产力提升。
