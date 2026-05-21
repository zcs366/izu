# Spec Coding vs Vibe Coding

> 概念 | AI辅助开发的两种范式

## 定义

**Vibe Coding**（氛围编程）：给 AI 模糊意图，让它自由发挥，跑通就算完事。短期快，长期累积技术债务——无测试、无文档、无安全检查、接口设计混乱。

**Spec Coding**（规范编程）：先定义技术规范和代码风格，让 AI 始终在同一套规则下干活。核心不是"更好的 Prompt"，而是把工程流程拆成可执行的检查点。

## 为什么重要

模型越强，走捷径越明显。GPT-5 级别的模型拿到任务就往前冲，不会主动补测试、边界、安全和可维护性。Spec Coding 用规则约束模型的"聪明但懒"的本能。

## 与匠石原则的关系

本 wiki 已有 [[aihot-code-over-model-principle|匠石原则]]（能用代码就别用模型）。Spec Coding 是这条原则在编码领域的具体化：不是不让 AI 写代码，而是让 AI 写代码之前先过规范检查。

## 关键实现

- **agent-skills**（Addy Osmani，33k+ GitHub Stars）：22 个可复用技能包覆盖完整开发生命周期（Meta → Define → Plan → Build → Verify → Deploy），每个 Skill 含检查点、规范约束、交付标准
- GitHub：https://github.com/addyosmani/agent-skills
- 与 Hermes Skills 的区别：agent-skills 面向 AI 编码规范，Hermes Skills 面向 Agent 通用能力

## 张成市适用性

⚠️ **有条件适用。** 你在用 Hermes 做大量 Agent 开发，Spec Coding 思路与你的"先哲学后行动"底层一致——先定规范再动手。但 agent-skills 本身面向 Claude Code/Codex 等编码工具，不是 Hermes 原生。核心价值是设计思路（工程流程拆成检查点），不是直接用这个工具。
