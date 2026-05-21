---
source_url: https://mp.weixin.qq.com/s/JMosvoAD7f9MvkaNPFY4PA
ingested: 2026-05-10
sha256: 58c9b83bb937914720645f66046bc854482db02b2aff03af347dc893bbdc164e
title: 从单兵作战到"AI 打工团"：Hermes Agent 0.13.0 全新多智能体看板机制
author: 智能运维前线
source: mp.weixin.qq.com
description: Hermes Agent v0.13.0 "The Tenacity Release" 更新全景：多智能体看板、/goal 持久目标、Checkpoints v2、视频分析、语音克隆、i18n 中文支持、P0 安全修复
---

# 从单兵作战到"AI 打工团"：Hermes Agent 0.13.0 全新多智能体看板机制

由 Nous Research 开发的开源自进化 AI 智能体框架 Hermes Agent 于 2026 年 5 月 7 日正式发布了 v0.13.0 版本。该版本被官方命名为 "The Tenacity Release"（坚韧版），核心标语是"Hermes Agent现在会坚持完成它所开始的任务"。很快就要突破14万 Star了。

## 主要更新亮点

### 1. 多智能体看板（Multi-agent Kanban）
- 多个 Hermes Worker 可以主动提取任务、相互交接并最终关闭任务
- 心跳监控 (Heartbeats)、任务回收 (Reclaim)、僵尸节点检测 (Zombie detection)、单任务重试次数限制 (Retry budgets)
- 防幻觉网关 (Hallucination gate)：专门用于审查 Worker 提交的任务成果

### 2. /goal 指令与 Ralph Loop
- 将 Agent 硬性锁定在一个目标上，确保长期专注
- Ralph Loop 作为一级原语引入

### 3. Checkpoints v2 与无缝会话恢复
- 状态持久化重写，引入真正的数据修剪 (Pruning)
- 断线自动恢复：Gateway 重启、服务中断或源文件重载后自动续接

### 4. 视频分析与语音克隆
- `video_analyze` 工具：支持通过 Gemini 及其他多模态大模型做原生视频内容解析
- xAI Custom Voices TTS 提供商，原生支持语音克隆

### 5. 国际化（i18n）与中文支持
- 网关与 CLI 提示信息支持 7 种语言（简体中文、日语、德语、西班牙语、法语、乌克兰语、土耳其语）
- 官方文档站点新增中文本地化版本 (zh-Hans)

### 6. P0 安全强化（Security Wave）
- 修复并闭环 8 个 P0 安全漏洞
- 默认开启数据脱敏
- Discord 越权修复
- WhatsApp 默认拒绝陌生人
- 修复 TOCTOU 漏洞

### 7. 第 20 个接入平台与 Cron 看门狗
- Google Chat 接入
- 模型提供商平台化为可插拔接口
- Cron no_agent 看门狗模式
