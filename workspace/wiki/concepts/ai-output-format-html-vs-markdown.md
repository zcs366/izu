---
title: AI时代输出格式之争：HTML vs Markdown
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [AI, 输出格式, Markdown, HTML, LLM, Agent, Claude Code]
sources:
  - raw/articles/ai-output-format-markdown-replaced-by-html.md
confidence: high
---

# AI时代输出格式之争：HTML vs Markdown

## 概述

在AI Agent时代，Markdown作为LLM输出标准格式的地位正受到HTML的挑战。核心论点来自Claude Code团队成员Thariq的文章《Using Claude Code: The Unreasonable Effectiveness of HTML》：Markdown的优势（简洁、易手写、低token）在Agent工作流中正在消失，而HTML的丰富表达能力（表格、SVG、交互、颜色编码、响应式布局）正在成为新优势。

## 核心对比

| 维度 | Markdown | HTML |
|------|----------|------|
| 诞生年份 | 2004 | 1991（早13年） |
| 设计哲学 | 做减法，保留最基础结构 | 做加法，表达越丰富越好 |
| 人类手写 | ⭐ 极优，符号直观 | ❌ 烦琐，标签多 |
| AI生成 | ✅ token成本低 | ⚠️ 需更多token |
| 表格 | ❌ 简陋，不能合并/设色 | ✅ 完整HTML表格 |
| SVG/流程图 | ❌ ASCII字符拼凑 | ✅ 原生矢量+交互 |
| 颜色编码 | ❌ 不支持 | ✅ 完整CSS支持 |
| 交互组件 | ❌ 不支持 | ✅ 滑块/按钮/拖拽 |
| 折叠/标签页 | ❌ 不支持 | ✅ details/summary |
| 响应式布局 | ❌ 不支持 | ✅ 完整CSS布局 |
| 渲染依赖 | 需要专用渲染器 | 任何浏览器原生渲染 |
| 分享便捷度 | 需转HTML/PDF或上传平台 | 上传S3即得链接 |
| 版本控制 | ✅ 纯文本，diff清晰 | ⚠️ 行变化多 |

## 关键论点

### Thariq的论点链条

1. **长文档不可读**：超过100行的Markdown文件，人类大脑会自动放弃处理。没有视觉层次、颜色编码、可折叠区块，纯文本无法阅读。
2. **Agent不手写**：Markdown易手写的核心优势在Agent工作流中消失，因为用户不再亲自编辑文件，而是让AI去改。
3. **表达力不足**：Claude在Markdown里不得不用ASCII画图、用Unicode字符估算颜色——"用铅笔画油画"。
4. **HTML交互能力**：HTML可生成带滑块/按钮的一次性编辑器，调参后一键导出——Markdown做不到。

### 作者苗正的判断

- HTML不会完全取代Markdown
- **Markdown不可替代的场景**：日常聊天、快速记录、短答复、版本控制、训练语料、结构化Prompt
- **HTML正在取代的场景**：长文档/研究报告、代码审查、设计工具、需要视觉结构和交互的内容
- 核心转变：从"好不好写"到"好不好读、好不好交互"
- 类比：以前用GPU玩游戏，现在用GPU跑大模型——外部变了，工具跟着变

## 对Agent实践的意义

- Claude Design已全面基于HTML运行
- Claude Code的PR附HTML代码解释器比GitHub原生diff更直观
- Hermes Agent的输出格式策略可参考：短内容用Markdown，长文档/设计交付用HTML
- 已关联skill: `claude-design`（全面基于HTML运行）

## 延伸阅读

- 原始文章: `raw/articles/ai-output-format-markdown-replaced-by-html.md`
- Thariq原文: 《Using Claude Code: The Unreasonable Effectiveness of HTML》
- Claude Design: 基于HTML的AI设计工具
