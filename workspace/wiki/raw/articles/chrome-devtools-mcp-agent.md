---
source_url: https://mp.weixin.qq.com/s/c6ZOScVGArLv0ozcfMrnCw
ingested: 2026-05-14
sha256: b6472386f0baa62e
title: Agent 终于能实时控制 Chrome 了！还能集成到 UI自动化中
author: 技术小宇宙
source: 微信公众号
---

Chrome 在3月的正式版中支持了 MCP 直连能力，方便 Agent 直接访问页面。也能接入到 puppeteer 中，提高 UI 自动化调试效率。

OpenClaw 在3月中旬更新了直连 Chrome 功能。之前 Agent 操控浏览器需要新启动一个 Chrome 实例，现在可以直接连接并操作你正在用的 Chrome，保留登录态、cookie 等所有用户信息。

核心能力来自 chrome-devtools-mcp，Chrome 官方的 MCP 工具，支持获取网页内容、操作页面、截图、监控网络、访问控制台等。

## 配置步骤

前置条件：Chrome 升级到 146+，启用远程调试（chrome://inspect/#remote-debugging）

安装：
```
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect
```

或手动配置 MCP JSON：
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--autoConnect"]
    }
  }
}
```

--autoConnect 表示直连已启动的 Chrome，不复用则需要 --browserUrl 指定 ws 地址。

## 如何在 Puppeteer 中集成

核心原理仍是 Puppeteer Connect：通过 Chrome 远程调试端口获取 WebSocket 地址，用 puppeteer.connect() 直连。

步骤：启动 Chrome 带调试端口 → 获取 WS 地址 → puppeteer.connect → 操控现有页面或新建页面

同时运行 chrome-devtools-mcp + puppeteer 时注意：不要指定 --isolated（会创建独立上下文），否则无法看到 Puppeteer 注入的脚本。

## 总结

Agent 直连 Chrome 没有黑科技，底层仍是 Puppeteer Connect。但 Chrome 放开了标准用户的 debug 权限，使得 Agent 可以复用真实浏览器的登录态，省去每次登录，在真实环境而非隔离环境中测试。

延伸：Claude Agent SDK 搭建测试用例生成 agent、NanoClaw 对接飞书、Agent Skills vs MCP 等。
