---
name: cdp-bridge-mcp
title: CDP Bridge MCP — 真实浏览器访问的 MCP 桥接服务
description: 通过 Chromium 扩展连接真实浏览器会话，让 LLM 复用登录态操作浏览器页面
tags: [mcp, browser, cdp, agent-web-capability, chromium]
created: 2026-05-10
---

# CDP Bridge MCP

## 一句话概括

CDP Bridge MCP 是一个 MCP 桥接服务，通过 Chrome 扩展接入你**正在使用**的浏览器，让 AI Agent 可以读取、操作、截图你的真实浏览器页面——**复用所有登录态和 Cookie**。

## 与同类方案的对比

| 方案 | 浏览器实例 | 登录态 | 部署复杂度 | 适合场景 |
|------|-----------|--------|-----------|---------|
| Playwright MCP | 新开沙箱 | ❌ 需重登 | 低 | 自动化测试/脚本化流程 |
| Chrome DevTools MCP | 可连调试端口 | ✅ 需配置 | 中 | DevTools 协议精细操作 |
| **CDP Bridge MCP** | **真实浏览器** | **✅ 全复用** | **低** | **LLM 实时协作/交互式任务** |

## 架构

```
LLM Agent (MCP Client)
    ↓ MCP 协议
CDP Bridge MCP Server (Python, uvx 启动)
    ↓ WebSocket
Chrome Extension → 你的真实浏览器标签页
```

## 提供的工具

- `browser_get_tabs` — 获取标签页列表
- `browser_scan` — 扫描页面（简化 HTML，减少 token）
- `browser_execute_js` — 执行 JavaScript
- `browser_switch_tab` — 切换标签页
- `browser_navigate` — 导航到 URL
- `browser_screenshot` — 截图
- `browser_cookies` — 读取 Cookie

## 安装方式

一行命令：`uvx cdp-bridge@latest`

MCP 客户端配置为标准 `uvx` 命令格式即可。

## 风险提示

- ⚠️ 给予 LLM 真实浏览器访问权限，存在安全风险——需配合严格的授权边界
- ⚠️ 项目较新（三黄工作室），稳定性和维护持续性待观察
- ⚠️ WSL 环境下运行需要 Windows Chrome + 扩展加载 + 网络互通

## 关联概念

- [[agent-web-capability]] — AI Agent 的网页能力总览
- [[autocli-opencli]] — 另一款复用 Chrome 登录态的抓取工具（CLI 方式）
- [[hermes-agent]] — 集成了浏览器工具的自主 AI 代理
- [[genericagent]] — CDP Bridge MCP 的代码参考来源


## 相关

- [[browser-harness]] — 同走CDP路线的极简方案，592行直连Chrome
