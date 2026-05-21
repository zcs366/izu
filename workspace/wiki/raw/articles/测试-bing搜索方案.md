---
source_url: file:///mnt/i/hermes/wiki_dropbox/测试-bing搜索方案.md
ingested: 2026-05-08
sha256: dbb3de5b93364fb1c90ed05d200aded0bdc8446e1c4aba8e02462bb0c8c5fa1a
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: 测试：Bing搜索自动化方案
---

# 测试：Bing搜索自动化方案

> 来源: 测试-bing搜索方案.md（用户存入 wiki_dropbox）

# 测试：Bing搜索自动化方案

这是用来测试 wiki_dropbox 自动处理流程的测试文件。

## 核心思路

使用curl模拟浏览器搜索Bing，配合Python正则提取搜索结果。
零API成本，数据自主可控。

## 实现要点

1. User-Agent必须设置为现代浏览器
2. 翻页参数使用 `&first=N`
3. 结果在 `<li class="b_algo">` 中
4. 标题在 `<h2><a>` 中
5. 摘要在 `<div class="b_caption">` 中

## 应用场景

- 日常信息搜集
- 竞品分析
- 技术调研
- 国防教育基地内容素材

