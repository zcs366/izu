---
source_url: https://mp.weixin.qq.com/s/qTJyHyay1KeHLu4H66r50Q
ingested: 2026-05-10
sha256: 7e8d01853ad61552fa8440c60fece51916194056d1732952a2a53bbef2e6fada
source: 微信公众号
author: 弈qi
original_pub: 微信公众号
description: Hermes Agent 是怎样"自进化"的——在线经验沉淀与离线训练双路径详解
---

# Hermes Agent 是怎样"自进化"的

Hermes Agent 的"进化"发生在两个地方：上下文层和训练数据层。在线链路：任务完成后写 memory、存 skill、存 session。离线链路：rollout 导成 trajectory，经 verifier 和 reward 验收后送 Atropos 训练。

## 一、在线经验沉淀

### 1. System Prompt 分层构建

稳定层（缓存前缀）由 _build_system_prompt() 负责，按序装：身份 → memory 指导 → skill 指导 → 冻结 memory 快照 → 冻结 user profile → skills 索引 → 项目文件。临时层只在当前调用前注入，不会回写消息历史。

### 2. Memory 精选记忆

MEMORY.md（约800 Token）：环境事实、项目约定、工具怪癖。USER.md（约500 Token）：用户偏好、工作方式、沟通习惯。两者冻结成快照，不随当前 session 修改而变——缓存前缀保持稳定。

### 3. Skill 自动生成

Hermes 的 Skill 自动生成由独立 Agent 在后台完成。Skill 可以被模型在对话中调用（skill_view/skill_manage/manage_skills 等工具），实现"用完即复用"。

### 4. Cron 周期性推动

cron 系统让 Hermes 可以主动发消息：每日摘要、定期搜索、监控变化。比被动响应更进一步——Agent 有"日程意识"。

## 二、离线训练回路

rollout 数据导出为 trajectory → verifier + reward 函数验收 → 带 token 级信号的数据送 Atropos 训练框架。实现"经验→模型权重"的深层进化。

## 关键代码片段

- _build_system_prompt() 稳定层构建
- format_for_system_prompt() 冻结快照
- 临时层注入机制
- MemoryStore 文件读写与去重
- 外部 memory provider（Honcho）集成
