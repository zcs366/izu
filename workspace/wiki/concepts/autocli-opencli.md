---
title: AutoCLI（OpenCLI）
created: 2026-05-07
updated: 2026-05-07
type: concept
tags: [tool, automation]
sources:
  - raw/articles/hermes-auto-wiki-workflow-yutou.md
  - raw/articles/opencli-bing-search-skill-60man.md
confidence: medium
---

# AutoCLI（OpenCLI）

浏览器信息抓取开源项目。无需 API Key，直接复用 Chrome 浏览器中已有的登录态，能实现 90+ 站点的信息抓取。

## 核心特性

- **免 API Key**：复用 Chrome 登录态
- **多站点支持**：90+ 站点
- **与 Hermes 集成**：可作为 skill 接入 [[Hermes Agent]]，由 Hermes 接管抓取任务

## 典型用途

与 Hermes Agent + llm-wiki skill 配合，构建自动化知识库工作流（见 [[hermes-auto-wiki-workflow]]）。

## BASH 自动化搜索实战（养马系列）

可配合 Hermes 构建纯终端的 Bing 自动化搜索技能（[[60分男人（养马系列）]]）：

1. 使用 `opencli browser open/type/click/eval/extract` 系列命令模拟人工搜索
2. Bash 脚本实现：搜索 → 翻页 → 提取链接 → 下载网页 → 按日期归档（自动去重）
3. 封装为 Hermes SKILL.md，一句话触发搜索+总结
4. **零 API 费用**：先下载到本地过滤，再喂大模型，Token 消耗砍 90%

详见 `raw/articles/opencli-bing-search-skill-60man.md`。
