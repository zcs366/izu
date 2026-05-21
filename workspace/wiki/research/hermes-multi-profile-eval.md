---
title: 评估：Hermes Agent 多Profile实战——搭AI同事军团
source: wiki/raw/articles/hermes-multi-profile-ai-colleagues.md
date: 2026-05-19
eval_level: 极大
tags: [评估, Hermes Agent, 多Profile, 实战, Gateway]
---

## 核心判断

**这是"最落地"的一篇。** 从架构设计到配置细节，从省钱技巧到角色分工，直接可复用的实战方案。

## 关键提炼

### 一、为什么选Hermes
Claude Code / Codex / Cursor 都是"一人到底"——Hermes的Profile隔离是独有能力。

### 二、架构设计
同一台服务器运行3个独立Gateway，共享技能目录，隔离会话/记忆/配置。
- 小爱马 🐴 全能助手 (default)
- 虾仔 🦐 全栈开发 (coder)
- 爱老师 🧬 研究分析 (research)

### 三、核心配置
每个Profile有独立：
- .env (API Key等)
- config.yaml (模型、内存等配置)
- SOUL.md (角色定义/人设)

### 四、省钱技巧
主模型：DeepSeek V4 Flash / MiniMax M2.7
辅助模型：智谱GLM免费系列（glm-4v-flash, glm-4.5-flash, glm-4-flash）

## 对张成市的价值

**高。** 这篇跟你的场景几乎完全匹配：

- 你目前就是"一个人干多工种"（军师、工程师、内容创作、数据分析）
- 多Profile正是替你分清角色的好方案
- 省钱技巧跟你"薅羊毛"偏好完美契合
- 但：F2-4飞书的Profile隔离在平台上尚未完美实现，实际落地需要调试

## 连接点
→ Cat Wu专访：Profile角色的"各司其职" + "一个人交付单元" = 每个Profile本身就是最小交付单元
→ Self-Improving源码解析：Skill共享 + Memory隔离的设计
→ Agent Skill生态：SOUL.md + Skill库 = 你的"AI同事军团"
