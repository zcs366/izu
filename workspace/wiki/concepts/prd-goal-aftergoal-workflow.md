# PRD-Goal-AfterGoal 三段式研发流水线

> **核心概念：** 利用 AI Agent（Claude Code）的斜杠命令机制，将软件开发固化为「人类定方向 → AI 执行实现 → AI 自动收尾」的三阶段闭环流程。由百度内研团队（鸟窝/smallnest）在百度 iCafe/iCode/Gerrit 体系上验证并开源。
>
> **首次收录：** 2026-05-20 | 来源：百度Geek说

## 三阶段结构

```
/prd（需求→PRD→拆卡）→ /goal（卡→代码→测试）→ /after-goal（提交→合入→关闭）
```

| 阶段 | 命令 | 人类角色 | AI 角色 | 价值 |
|------|------|---------|---------|------|
| 1 | `/prd` | 主导方向 | 辅助结构化输出 | 强制先想清楚：用户故事/验收标准/Non-Goal/依赖 |
| 2 | `/goal` | 验收结果 | 主导实现 | 卡片足够小+验收标准明确=AI一次到位 |
| 3 | `/after-goal` | 无需介入 | 全自动执行 | 提交→打分→合入→更新描述→关闭卡片，一键收尾 |

## 核心设计原则

### Non-Goal 机制
- 每个 PRD 必须明确「不做的事」——减少"做完了你说不是这个意思"的返工
- Non-Goal 比 Goal 更难写，但回报更大

### 卡片粒度铁律
- 足够小：AI 一次能实现 → 快速反馈，避免死循环
- 验收标准明确 → AI 自动写单元测试
- 依赖关系标注 → 按顺序实现，避免冲突
- 卡片 ID 绑定 → commit message、CR 全链路追踪

### CLI > 浏览器
- 凡是能用 CLI 完成的操作，不要用浏览器
- iCafe/iCode/Gerrit 的 CLI 工具远优于 playwright-cli 模拟网页操作

## 与「军师-开干」工作流的关系

| 维度 | 百度 PRD→Goal→After-Goal | 军师·开干工作流 |
|------|--------------------------|----------------|
| 定方向 | PRD（含Non-Goal+卡） | 你说方向→军师出PRD+卡→你说"开干" |
| 执行 | `/goal 卡ID` | 军师逐卡执行 |
| 收尾 | `/after-goal`（自动化） | **缺：** 自动更新wiki+打log |
| 价值观 | CLI > 浏览器 | CLI > UI（一致） |
| 卡片系统 | iCafe（百度自研） | P0/P1/P2（可改进：加ID+验收标准） |

## 开源项目

- **GitHub：** https://github.com/smallnest/goal-workflow
- **官网：** https://goal.rpcx.io/

## 来源

- [[../raw/articles/prd-goal-after-goal-ai-dev-workflow|原始文章]]（百度Geek说）
- [[niaowo|作者：鸟窝]]
- [[../output/极大/prd-goal-after-goal-ai-workflow.md|军师合议报告]]
