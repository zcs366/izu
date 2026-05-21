---
source_url: https://mp.weixin.qq.com/s/glKc83ON_B5vTvO9sLnBOw
sha256: e7cc41eda0ac951ff004c1342b5f02ce4008d164c28afac82baa485787d0aa1b
ingested: 2026-05-15
title: "Hermes 强力升级，任务卡死不再成为烦恼"
author: 宋京择
source: 微信公众号 京择说
content_type: article
note: Hermes Agent v0.13.0 韧性版更新解读
---

# Hermes 强力升级，任务卡死不再成为烦恼

**来源**：宋京择（京择说）  
**日期**：2026年5月9日  
**版本**：Hermes Agent v0.13.0 · 韧性版（Tenacity Release）

---

## PART 01 — Kanban · 多智能体看板

Kanban 是这次版本最核心的新功能。一个持久化的多 AI 协作看板，多个 Hermes Worker 可以并行领任务，分工合作。

**核心机制：**

- **心跳检测**：Worker 定期上报状态，死了立刻被感知到，任务自动回收重新分配
- **僵尸检测**：卡死的 Worker 直接被踢出去，任务不因此被卡住
- **幻觉门控**：Worker 声称"完成了"但没有证据，会被拦截要求补充说明
- **独立重试配额**：每个任务可以单独配置最大重试次数，不会无限重试耗光资源

**最期待场景**：一个 orchestrator profile 负责拆解需求、创建任务，多个 Worker profile 并行执行，完成后汇总。这在之前要靠大量手工协调，现在 Kanban 把这个流程标准化了。

---

## PART 02 — /goal · 目标锁定（Ralph Loop）

输入 `/goal 你的目标`，就能给 AI 锁定一个任务目标。无论中间聊了多少岔路，它都会持续追踪目标状态（内部叫 Ralph Loop），不会在多轮对话中悄悄走丢。

相当于给 AI 戴了一个「任务锁链」——开头说好了干什么，它就得做完。让 agent 从"一次性回答问题"变成了"持续跟进一个项目"。

---

## PART 03 — Recovery · Checkpoints v2

以前 gateway 重启，正在进行的对话就断了。这次支持自动恢复：

- gateway 崩溃后重启，对话上下文自动恢复
- `/update` 重启过程中保留 pending 状态的提示和更新进度
- 线程路由在重启前后保持一致
- 缓存的 live session 状态会被正确保留

配合 Checkpoints v2（状态持久化完全重写，支持真正的检查点剪枝 + 磁盘用量上限），AI 的任务记忆更可靠了。

---

## PART 04 — Security · 8 P0 Fixes

- **敏感信息自动脱敏默认开启**：API key、密码、token 在运行时自动过滤
- **Discord 角色白名单修复**：修了一个 CVSS 8.1 的跨服务器越权漏洞
- **WhatsApp 默认拒绝陌生人**：不再对任何人发来的消息都响应
- **定时任务扫描提示词注入**：使用外部数据源触发定时任务时，完整 prompt 都会被扫描

这些功能不是主角，但默认就开启这件事本身就让人安心很多。

---

## 写在最后

核心功能（普通对话、工具调用、定时任务）已经相当成熟，Kanban 和 /goal 是这次最值得关注的亮点——一个解决任务中途卡死，一个解决多轮对话跑偏。安全加固算是额外赠送的"增值服务"。

升级命令：`hermes update`

> **Hermes Agent now finishes what it starts.**
