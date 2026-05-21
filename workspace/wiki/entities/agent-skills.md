# agent-skills

- **类型：** 开源工具（GitHub）
- **作者：** Addy Osmani（Google 工程师）
- **状态：** 活跃 | 33,600+ GitHub Stars（2026-05）
- **仓库：** https://github.com/addyosmani/agent-skills
- **许可证：** MIT

## 是什么

22 个可复用的 AI 编码技能包，将资深工程师的开发工作流封装为可执行流程。不是 Prompt 集合，而是把 **需求 → 计划 → 构建 → 验证 → 部署** 拆成含检查点的工程流水线。

## 核心机制

每个 Skill（技能包）覆盖一个开发阶段，包含：规范约束、检查点、交付标准。AI 在执行任务前先过规范检查，而非直接写代码。

22 个 Skills 分类：
- **Meta** — 发现该用哪个 Skill
- **Define** — 澄清需求（PRD、用户故事）
- **Plan** — 分解任务（技术方案、架构决策）
- **Build** — 写代码（按规范、含测试）
- **Verify** — 证明正确（测试、安全检查、性能基准）
- **Deploy** — 上线（发布检查清单、回滚预案）

## 与 Hermes Skills 的对比

| 维度 | agent-skills | Hermes Skills |
|------|-------------|---------------|
| 面向 | AI 编码规范 | Agent 通用能力 |
| 粒度 | 开发阶段检查点 | 任务工作流 |
| 触发 | 开发流程中自动匹配 | 按需加载 |
| 生态 | GitHub 独立项目 | Hermes Skills Hub |

## 相关

- [[spec-coding-vs-vibe-coding]] — Spec Coding 概念
- [[aihot-code-over-model-principle]] — 匠石原则
