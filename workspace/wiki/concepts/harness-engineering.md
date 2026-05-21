---
title: "Harness Engineering"
aliases: [Agent Harness, Harness设计]
tags: [AI工程, Agent, 范式, 工程化]
---

# Harness Engineering

2026年AI圈最新范式，核心公式：**Agent = Model + Harness**。Anthropic定义为"模型之外的一切"——所有代码、配置、执行逻辑、约束规则、反馈回路。

## 起源
- **Mitchell Hashimoto**: 2026.2.5 《My AI Adoption Journey》
- **OpenAI Codex团队**: 2026.2.11 《Harness engineering: leveraging Codex in an agent-first world》
- **Anthropic**: 2026.3.24 《Harness design for long-running application development》

## 核心组件
- 确定性约束门控（架构Linter、重试上限、前置提交钩子）
- 反馈循环与自我验证（写-测-修循环、预完工检查清单）
- 上下文治理与Gardening（上下文防火墙、熵值管理）

## 相比Prompt/Context Engineering
| 阶段 | 时间 | 关注点 |
|------|------|--------|
| Prompt Engineering | 2023-2024 | 怎么跟AI说话 |
| Context Engineering | 2025 | 给AI看什么信息 |
| Harness Engineering | 2026 | 构建什么环境让AI工作 |

## 关联概念
Context Engineering, Agent Infra, AI工程范式
