---
source_url: PLACEHOLDER
ingested: 2026-05-14
sha256: 187b628a51dd94d0
note: macOS only，用户Windows/WSL不可用，但机制值得了解
title: Hermes也支持computer use了，还能后台操作软件
author: 程序员生存之道
source: 微信公众号
---

Computer use：AI 看屏幕、点鼠标、敲键盘，替你干活。

但传统方案有个致命问题——电脑被控制时你什么都干不了。Claude Computer Use 这样，ChatGPT Operator 也这样。要么等它干完，要么给它单独开台虚拟机。

Hermes 走了另一条路：你干你的，它干它的。

## 技术原理

底层驱动 cua-driver 用 macOS SkyLight 私有 SPI——SLEventPostToPid、SLPSPostEventRecordTo——把输入事件直接投递到目标进程。不经过鼠标、键盘、任何输入设备。不是模拟点击，而是直接投递事件告诉应用哪里被点击了。

所以光标不动、焦点不抢、Space 不切。Agent 在后台操作 Safari，你同时在 VS Code 里写代码。

## 模型无关

Claude Computer Use 绑死 Anthropic 原生 schema。Hermes 不绑——任何能调工具的模型都行：Claude、GPT-4、Gemini、OpenRouter 视觉模型、甚至本地 vLLM 跑的开源模型。

## 上手

```bash
hermes tools   # 选 Computer Use (macOS)
# 装驱动，给辅助功能权限
```

## 限制

- macOS only，Windows/Linux 暂不支持后台模式
- 需要辅助功能权限（系统设置 → 隐私与安全 → 辅助功能）
- macOS 14.0+（Sonoma）为佳

## 使用原则

有 API 走 API。有 CLI 走 CLI。有 browser 工具走 browser。Computer Use 留给没 API 的原生应用——Mail、Finder、Figma、Sketch。

- Hermes Agent：github.com/NousResearch/hermes-agent
- cua-driver：github.com/trycua/cua
