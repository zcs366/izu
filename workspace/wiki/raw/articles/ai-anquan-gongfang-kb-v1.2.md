---
source_url: https://mp.weixin.qq.com/s/M7jFCJ77pvX0Xe7cRJMP6w
ingested: 2026-05-10
sha256: 28f5f8db38195fa5d69daef6eb8c11a4556717db616a7fbaf18425c18969ba8c
source: AI安全工坊
author: taielab
original_pub: 微信公众号
description: 不是越狱，是系统：AI 安全工坊知识库 v1.2，一份开放的中文 AI 安全知识库介绍
---

# 不是越狱，是系统：AI 安全工坊知识库 v1.2

我整理了一份开放的中文 AI 安全知识库，给所有正在构建、评估和治理 AI 系统的人，如果你看了对你有帮助可以友情赞助支持作者并分享给更多有需要的人。文末获取知识库地址。

使用说明：本文和知识库内容欢迎学习、引用、纠错与非商业传播。禁止二次盗版、打包售卖、改头换面做商业资料包或课程牟利。

## AI 安全从模型输出走向系统行为

过去一年，很多人谈 AI 安全，第一反应还是两个词：Prompt 注入，模型越狱。现在的 AI 系统，早就不只是一个聊天窗口。它会读文件、查数据库、调用 API、操作浏览器、连接 SaaS、写代码、跑命令、触发工作流。它接入 MCP、A2A、RAG、向量库、Agent 框架、权限系统、日志平台、模型注册表、数据管道。

AI 的风险已经从"模型输出"扩展到了"系统行为"。真正的问题不再只是"这个模型会不会回答危险问题？"，而是：
- 它能访问哪些数据？
- 它能调用哪些工具？
- 它的 token 能不能被错误复用？
- 它读到的网页、邮件、文档能不能污染上下文？
- 它的输出会不会进入 SQL、HTML、代码、审批流？
- 它的训练集、评估集、模型文件、依赖包能不能被投毒？
- 发生事故后，我们能不能复盘 prompt、RAG 片段、工具调用和权限链路？

## AI 安全五层结构

### 第一层：模型层
越狱、幻觉、对齐、欺骗、能力隐藏、推理链可监控性、模型记忆、训练数据泄露。

### 第二层：应用层
Prompt Injection、RAG 污染、Insecure Output Handling、Function Calling 滥用、LLM-mediated SSRF / SQLi / XSS、用户确认边界。

### 第三层：Agent 和协议层
MCP、A2A、Tool Poisoning、跨 server 工具影子、STDIO 本地子进程风险、OAuth Resource Indicator、token audience、marketplace 供应链。

### 第四层：工程和供应链层
数据摄取、评估集污染、模型注册表、AIBOM / ML-BOM、模型签名、依赖包投毒、HuggingFace 模型审计。

### 第五层：组织和治理层
红队评估、蓝队监控、事件响应、隐私合规、EU AI Act、中国备案、NIST AI RMF、ISO/IEC 42001、行业垂直风险。

这些层不是互相独立的。一次真实 AI 安全事故往往会跨越好几层。

## 知识库状态（v1.2）

截至 2026-04-30：
- 23 个活跃一级章节
- 176 个二级专题
- 202 个三级知识点
- 12+ 张配套 Bitable
- 约 3000 条结构化记录
- 70+ 份附件与报告
- 1600+ 条真实 URL

结构化数据：482 条工具清单、190 篇论文、82 起真实案例、384 条 MITRE ATLAS 中文化数据、337 条全库引用反查。

## v1.2 重点补强

1. **LLM 应用层安全**：LLM API 攻击面、Insecure Output Handling、Function/API Chaining、LLM-mediated SSRF/SQLi/XSS
2. **AI Red Team Assessment 模板**：Scope、Rules of Engagement、Threat Model、Payload Set、测试 Harness、Scorer、风险评级、证据包、Retest 流程
3. **Agent / MCP 事件响应**：读了什么上下文、哪个工具被调用、tool schema、用户确认、token 签发、session 复用、RAG 检索片段、跨 server 污染
4. **MLSecOps 和供应链**：数据来源门禁、训练/评估集污染检测、Registry 晋级门禁、AIBOM/ML-BOM、模型签名与溯源、HuggingFace 模型审计
5. **前沿安全方向**：Sleeper Agents、Sandbagging、Emergent Misalignment、自我复制评估、CoT 注入、Verifier 绕过、长推理 DoS、RLVR 安全影响、XR 隐私、VLA 对抗、边端 AI 攻击面等

## 原则

开放、中性、利他、全球、可追溯。入口开放，基础知识不做付费墙，不作厂商背书，不把旧结论包装成权威。

作者：taielab · 公众号：AI 安全工坊
