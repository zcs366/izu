---
type: entity
category: project
created: 2026-05-14
updated: 2026-05-14
confidence: medium
sources:
  - raw/articles/browser-harness-self-healing-cdp.md
tags: [browser-automation, cdp, self-healing, agent, oss]
---

# Browser Harness

Browser Harness 是 [[browser-use]] 团队的极简浏览器自动化项目——592行Python，直连Chrome DevTools Protocol（CDP），不走Playwright/Selenium。核心理念：**给LLM一根WebSocket线直连Chrome，让它自己造工具。**

## 核心特征

- **592行代码**：四个文件（run.py / helpers.py / admin.py / daemon.py），无框架层
- **Self-healing**：Agent运行时发现 helpers.py 缺函数，会自己打开文件写一个新函数然后继续执行
- **直连CDP**：WebSocket直连Chrome，不经过任何自动化框架
- **Domain Skills**：Agent在实际操作中自动生成的网站"攻略"，不允许人手写——记录的是"实际有效"的操作路径
- **MIT协议**，4.7k stars，GitHub: [browser-use/browser-harness](https://github.com/browser-use/browser-harness)

## 与 browser-use 主项目关系

browser-use 主项目是全功能Agent框架（类比Django），Browser Harness 是极简底层工具（类比Flask/raw socket）。互补关系。

## 安全风险

直连真实浏览器意味着Agent可触及用户已登录的所有网站（银行、邮箱、社交账号）。项目有勾选框确认授权步骤，但一旦授权边界基本无限。

## 相关概念

- [[cdp-bridge-mcp]] — CDP桥接，另一种让LLM操控浏览器的方式
- [[browser-use]] — 同团队的全功能浏览器Agent框架
