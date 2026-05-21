---
source_url: https://mp.weixin.qq.com/s/J1EZzYVx0VcologP-hEwVg
ingested: 2026-05-10
sha256: 41896e180b37ffddd724954b5453e0213798f7b549088d26a90020be3668436a
title: Playwright拉爆了！请给你的Agent安装上真正的浏览器访问能力——CDP Bridge MCP
author: 三黄工作室
source: mp.weixin.qq.com
---

# CDP Bridge MCP

> PS：这是三黄工作室第二个开源项目～苦于Playwright MCP、Chrome Devtools MCP无法真正流畅的操控浏览器，每次总是会打开沙箱并且失去登录态，受GA项目的影响，我们制作了可以完全直连访问浏览器的MCP。

CDP Bridge MCP 是一个连接 MCP 客户端与真实浏览器会话的桥接服务。它通过配套的 Chromium 扩展接入浏览器页面，让大模型客户端可以读取标签页、扫描页面、执行 JavaScript、截图、导航和读取 Cookie。

## 项目介绍

CDP Bridge MCP 适合需要让大模型操作真实浏览器的场景。和无状态 HTTP 抓取不同，它连接的是你已经登录、已经打开的浏览器页面，因此可以复用真实浏览器里的登录态、Cookie、页面状态和前端渲染结果。

代码仓库：https://github.com/Unagi-cq/cdp-bridge-mcp

## 为什么用 CDP Bridge MCP？

Playwright MCP 和 Chrome DevTools MCP 的局限：
- Playwright MCP：偏向自动化测试，新开浏览器实例，无登录态
- Chrome DevTools MCP：偏向调试协议，需要配置调试参数

CDP Bridge MCP 的优势：
- **复用真实登录态**：连接已登录的浏览器标签页，直接使用现有 Cookie、登录状态
- **适合 LLM 交互式任务**：读取、分析、点击前判断、执行脚本、截图
- **页面内容优化**：browser_scan 对 HTML 做简化，过滤脚本、样式和不可见元素，减少 token 浪费
- **启动链路轻量**：uvx cdp-bridge 启动，浏览器端加载扩展即可连接

## 可用工具

| 工具名 | 说明 |
|--------|------|
| browser_get_tabs | 获取已连接标签页列表 |
| browser_scan | 扫描当前页面内容，简化 HTML 或纯文本 |
| browser_execute_js | 在当前标签页执行 JavaScript |
| browser_switch_tab | 切换活动标签页 |
| browser_navigate | 跳转到指定 URL |
| browser_screenshot | 获取页面截图 |
| browser_cookies | 读取 Cookie |

## 安装

使用 uvx 一行启动：
```
uvx cdp-bridge@latest
```

MCP 客户端配置示例（JSON）：
```json
{
  "mcpServers": {
    "cdp-bridge": {
      "command": "uvx",
      "args": ["cdp-bridge@latest"]
    }
  }
}
```

浏览器端加载扩展（Chromium）：
1. 打开 chrome://extensions/
2. 开启开发者模式
3. 加载 src/cdp_bridge/tmwd_cdp_bridge 文件夹

默认连接 127.0.0.1:18765。

## 项目来源

三黄工作室首个开源项目，浏览器插件和部分代码参考并来源于 GenericAgent。
