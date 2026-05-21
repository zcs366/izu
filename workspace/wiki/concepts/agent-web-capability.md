---
title: Agent 互联网能力
created: 2026-05-08
updated: 2026-05-10
type: concept
tags: [agent, web-access, search, browser-control, infrastructure]
sources: [raw/articles/tinyfish-free-search-fetch-api-yuanxiaoer.md]
---

# Agent 互联网能力

AI Agent 获取和处理互联网信息的能力，是 Agent 从"封闭对话"走向"自主操作"的关键基础设施。

## 现状与短板

- Claude Code、Codex、Cursor Agent、OpenClaw、Hermes 等 Agent 框架在 2026 年快速爆发
- **共同短板**：与互联网之间隔着一层纱——无法自主搜索、抓取、读取网页内容
- 传统方案：自建爬虫（高维护成本）或购买第三方 API（高费用）

## 技术方案

### 搜索能力（Search API）
- TinyFish Search API（免费，每分钟 5 次）
- 通过 MCP 协议注入 Agent 上下文
- Agent 可在对话中自主调用搜索获取最新信息

### 网页抓取能力（Fetch API）
- TinyFish Fetch API（免费，每分钟 25 URL）
- **真实浏览器渲染** — 处理 JS、SPA、动态加载内容
- **Stealth 模式** — 过 Cloudflare 等反爬检测
- 返回干净 Markdown，直接供 LLM 使用

### 浏览器控制能力
- **Codex /chrome** — 通过代码层操作 Chrome 浏览器
  - 并行多窗口，不抢鼠标
  - Token 消耗低（非截图+OCR）
  - 与 Computer Use 互补（仅限浏览器）
- Playwright CLI — 脚本化浏览器控制 ^[raw/articles/tinyfish-free-search-fetch-api-yuanxiaoer.md]
- **CDP Bridge MCP** — 通过 Chrome 扩展连接真实浏览器，复用登录态，让 LLM 操控已登录页面 ^[raw/articles/cdp-bridge-mcp.md]

## 应用场景

1. **文档查询** — Agent 自主查 npm 包兼容性，无需人工复制粘贴
2. **资讯推送** — Hermes 定时搜索关键词，抓取摘要，推送飞书/微信
3. **比价/数据采集** — OpenClaw 调用 Fetch API 进行多页面数据比对
4. **自动化测试** — Codex 并行操作多个 Chrome 窗口进行回归测试

## 相关实体

- [[tinyfish]] — 免费 Search/Fetch API 服务商
- [[hermes-agent]] — 通过 TinyFish 补足信息获取短板
- [[openclaw]] — 同样受益于互联网能力

## 核心价值

TinyFish 给 Agent 接上了"眼睛"（搜索+浏览），Codex 的 /chrome 给 Agent 接上了"手"（浏览器操作）。免费的基建 + 开放的接口 + 越来越聪明的模型 —— Agent 自主触达互联网的能力正在从"可能"变成"默认"。
