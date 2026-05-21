---
source_url: https://www.zhihu.com/answer/2037856197462766743
syndicated_url: https://m.thepaper.cn/newsDetail_forward_33110439
ingested: 2026-05-14
sha256: c7a9d1e3f5b2a8c4
title: DeepSeek-TUI 霸榜GitHub，小白不到10元开发应用，将带来哪些影响？
author: 朱卫军（知乎 pydatalysis）
source: 知乎回答（澎湃新闻转载）
content_type: product-review
note: DeepSeek-TUI 实测+影响分析。非DeepSeek官方产品，个人开发者基于V4的终端编程Agent，MIT开源。
---

DeepSeek-TUI 是个人开发者 Hunter Bown 基于 DeepSeek V4 开发的终端原生编程智能体。不是 DeepSeek 官方产品。被称为「DeepSeek 版 Claude Code」「国产 Codex CLI」。

一天内 Star 从 8.7k 飙升至 16.3k（截至撰文时），目前已达 27.8k。

**为什么需要 TUI？**

大模型竞争正从模型能力转向 Agent 工作流。OpenAI 有 Codex，Anthropic 有 Claude Code，DeepSeek 一直缺官方 Agent 框架。关键事件：OpenAI 最近一次升级把推理接口全面切换到 Responses API，导致 V4 在 Codex 上完全失效。DeepSeek V4 需要一个自己的 Codex。

**三种工作模式**

- Plan：观察模式，分析项目、生成计划，不执行修改
- Agent：调用工具（读文件、改代码、执行shell），关键步骤要求用户确认
- YOLO：激进模式，AI 自动推进整个任务链

**实测1：开发 macOS 剪贴板应用 ClipMemo**

要求钉选、iCloud 同步、菜单栏支持。结果：基本功能完备，甚至额外增加了定时清理、去重。不足：iCloud 同步开关存在但实际不生效。

**实测2：开源项目 GKD Bug 修复**

Android 自动化项目（Kotlin + Android Framework）。全过程 13 分钟，AI 自动完成：克隆仓库→分析结构→查函数调用→生成 patch→验证。形成 debugging loop。找出并「修复」三处 bug。Codex (GPT-5.5 高) 审计后指出六个问题，包括一个漏掉的明确逻辑 bug。

**核心特色**

- 原生 MCP 与 skills 支持
- Auto Mode：先用 flash 模型判断复杂度，简单用便宜模型，复杂用 pro
- 极致性价比：bug 修复 + 应用开发总共 9.47 元
- 界面展开所有细节，信息压力较大

**影响分析**

1. 成本降到 10 元以内。过去 AI 辅助编程需要买 Claude Pro 订阅（$20/月），现在一整个开发流程不到 10 块钱
2. 小白也能开发应用。不需要学编程语言，用自然语言描述需求即可
3. 大模型竞争转向 Agent 工作流。垂直整合（模型团队+Agent 工程团队）的优势越来越重要
4. DeepSeek 生态终于有了真正的 Agent 外壳，官方已收录到 awesome-deepseek-agent
