---
title: TinyFish
created: 2026-05-08
updated: 2026-05-08
type: entity
tags: [service, api, search, mcp, ai-infrastructure]
sources: [raw/articles/tinyfish-free-search-fetch-api-yuanxiaoer.md]
---

# TinyFish

TinyFish（agent.tinyfish.ai）是一个为 AI Agent 提供互联网搜索和网页抓取能力的 API 服务平台。提供 MCP 协议、REST API 和 SDK 三种接入方式。

## 核心功能

### Search API
- 免费使用：每分钟 5 次
- 支持实时搜索，为 Agent 提供互联网信息获取能力
- 可通过 MCP 协议、REST API、Python/TypeScript SDK 调用

### Fetch API
- 免费使用：每分钟 25 个 URL
- **真实浏览器渲染** — 非简单 HTTP GET，能处理 JavaScript、SPA、动态加载内容
- **Stealth 模式** — 可过 Cloudflare 等反爬检测
- 返回干净 Markdown 格式内容，直接放进 LLM 上下文

## 接入方式

1. **MCP 协议（推荐）** — 将 MCP Server 地址丢进 Claude Code、Cursor 等配置，两分钟完成
2. **REST API** — 直接 HTTP 调用
3. **Python/TypeScript SDK** — 框架集成
4. **框架集成** — n8n、Dify、LangChain、CrewAI 官方支持

## 与 [[hermes-agent]] 的结合

TinyFish 可以补足 Hermes Agent 在网页信息获取方面的短板。通过 REST API 将搜索和抓取能力接入 Hermes，可实现：
- 定时搜索关键词最新资讯
- 抓取摘要并推送到飞书/微信
- 替代自建爬虫的复杂逻辑

## 与 [[openclaw]] 的结合

OpenClaw 同样可通过 TinyFish 获得互联网访问能力，突破 Agent 信息获取瓶颈。

## 相关概念

- [[agent-web-capability]] — Agent 互联网能力（待创建）
- MCP 协议生态

## 注册

- 官网：https://agent.tinyfish.ai/sign-up
- 文档：https://docs.tinyfish.ai/
- 无需绑信用卡，新手赠 500 credits
