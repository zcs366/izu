# MetaGPT

- **类型：** 开源框架（GitHub）
- **作者：** geekan 等
- **仓库：** https://github.com/geekan/MetaGPT
- **状态：** 活跃 | 67,700+ GitHub Stars（2026-05）
- **许可证：** MIT

## 是什么

多 Agent 软件开发框架。"Code = SOP(Team)"——将软件开发建模为标准操作流程，由产品经理、架构师、项目经理、工程师四个角色智能体协作完成。

## 核心机制

输入一句话需求 → PM 出用户故事+竞品分析 → 架构师出系统设计 → PM 排期 → 工程师出代码 → QA 跑测试。多 Agent 之间的产出形成天然约束和校验，避免单 Agent "一条路走到黑"。

## 与 agent-skills / autoresearch 的对比

| 维度 | MetaGPT | agent-skills | autoresearch |
|------|---------|-------------|--------------|
| 范式 | 角色分工协作 | Spec→检查点 | 交叉审核循环 |
| Agent数 | 4-5 固定角色 | 1 个按 Skill 执行 | 2-3 个交叉审核 |
| 适合 | 从零搭项目 | 规范已有开发 | Bug修复/功能迭代 |

## 相关

- [[agent-cross-review-loop]] — 多Agent交叉审核方法论
- [[spec-coding-vs-vibe-coding]] — Spec Coding 范式
- [[autoresearch]] — smallnest 的交叉审核实现
