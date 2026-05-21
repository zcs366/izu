---
title: Hermes Gateway 架构
created: 2026-05-07
updated: 2026-05-07
type: concept
tags: [agent, architecture, multi-platform]
sources: [raw/articles/hermes-agent-deep-dive-series-agent-observer.md]
confidence: high
---

# Hermes Gateway 架构

[[Hermes Agent]] 的多平台接入层，负责将同一套 Agent Runtime 复用到 15+ 消息平台。

## 架构原理

- **gateway/run.py**：事件循环 + 平台适配器注册
- **gateway/platforms/ 下二十余个适配器**：统一接口设计（base.py），每个平台一个子目录
- **session_key**：按 platform / chat / thread / user 组合创建会话，**不跨平台共享上下文**
- **home channel**：cron 结果、主动消息、跨平台通知自动投递到用户默认的"家渠道"

## 跨平台消息归一化

- Markdown 自动适配各平台语法差异
- 按钮 / 文件上传 / 语音备忘录转写
- 图片理解（自动调用视觉模型）

## 平台生命周期回调

平台适配器定义了连接/断开/错误等生命周期的接口回调。

## 相关条目

- [[Hermes Agent]]
- [[ACD 适配器]]
