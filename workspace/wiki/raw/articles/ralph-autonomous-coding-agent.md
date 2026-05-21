---
title: "Ralph：自主AI编码代理（19.1k Stars）"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/-fQNIn6V0FRk4L6Ar37_-A"
author: "牛码架构"
date: 2026-05-19
ingested: 2026-05-19
sha256: fd4a6b06e223725d206429adb7affdff2007018694717c93297c0f73c39e38fc
type: article
tags: [ralph, autonomous-coding, agent-loop, AI-coding-tool]
eval_level: 极大
---

# Ralph：自主AI编码代理

**GitHub**: https://github.com/snarktank/ralph (19.1k Stars)

## 核心能力
- **自主执行**：需求→编码→测试→提交，全程无人干预
- **持续学习**：通过git历史、progress.txt、prd.json跨迭代积累知识
- **质量保障**：内置类型检查、测试和CI集成

## 工作流程
1. 创建PRD → 2. 转换为JSON格式（prd.json）→ 3. 运行ralph.sh
- 创建特性分支 → 选最高优先级未通过故事 → 实现 → 质量检查 → 提交 → 更新状态 → 重复

## 关键概念
- **小任务原则**：每个PRD项目必须足够小，在一个上下文窗口中完成
- **AGENTS.md更新**：每次迭代后回写学习到的模式、注意事项和约定
- **反馈循环**：类型检查→测试→CI保持绿色
- **浏览器验证**：前端故事须在浏览器中验证

## 适用场景
✅ 快速实现大量小功能
✅ 需要自动化编码+测试的项目
✅ 希望AI从历史迭代中学习

❌ 超大任务需要人工干预
❌ 依赖AI编码工具质量
❌ 仅支持Amp和Claude Code
