# autoresearch（软件版）

- **类型：** 开源工具（GitHub）
- **作者：** 鸟窝（smallnest）
- **仓库：** https://github.com/smallnest/autoresearch
- **灵感来源：** Karpathy 的 AutoResearch（AI 研究自动化）

## 是什么

将 Karpathy 的 AutoResearch 方法论迁移到软件开发领域：多 AI Agent 交叉审核 + 5 维度量化评分 + 反馈驱动迭代，实现从 Issue 识别到代码合并的全自动闭环。

## 核心循环

1. 识别 GitHub Issue
2. Agent-A（Codex/Claude Code/OpenCode）实现代码
3. Agent-B 按 5 维度评分（正确性/风格/测试/安全/性能，各 0-10）
4. 达标 → 合并；不达标 → 反馈 → Agent-A 重做
5. 以 program.md 为规则核心

## 实际效果

中等复杂度任务约 10 分钟自主完成，代码质量 9.0/10。

## 相关

- [[agent-cross-review-loop]] — 方法论概念
- [[spec-coding-vs-vibe-coding]] — Spec Coding 范式
- [[aihot-code-over-model-principle]] — 匠石原则
