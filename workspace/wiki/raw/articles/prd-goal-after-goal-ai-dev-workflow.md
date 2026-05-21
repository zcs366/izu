---
source_url: https://mp.weixin.qq.com/s/0dSfok0fLN-OTIIYIYZ5rg
ingested: 2026-05-21
sha256: 17ffbb83eeeeee4e05c8df318149c1133dbe1aedd9cdace9c17a89439effea0e
title: PRD → Goal → After-Goal：AI 主导全流程研发实践
author: 鸟窝
source: 百度Geek说
source_type: 微信公众号
---

# PRD → Goal → After-Goal：AI 主导全流程研发实践

**来源**：百度Geek说（作者：鸟窝）
**链接**：https://mp.weixin.qq.com/s/0dSfok0fLN-OTIIYIYZ5rg

## 核心摘要

本文通过真实案例展示了如何利用 Claude Code 的 `/prd`、`/goal`、`/after-goal` 三个斜杠命令，实现从需求拆解到代码合入的全自动化开发流程。该流程将原本分散、手动的多环节研发过程固化为高效、自动化的三阶段协作，显著提升开发效率与规范性。

**开源项目**：https://github.com/smallnest/goal-workflow
**官网**：https://goal.rpcx.io/

## 背景：传统研发流程痛点

在百度内部，功能从需求到上线通常经历：**写 PRD → 拆卡片 → 写代码 → 提 CR → 合入 → 关卡片**。环节多、工具分散（iCafe、iCode、Gerrit），每一步需手动操作，容易遗漏。

借助 Claude Code Skill 机制，将流程固化为三个阶段：

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   /prd      │     │   /goal      │     │  /after-goal  │
│  需求 → PRD │──▶  │  卡片 → 代码  │──▶  │  代码 → 合入   │
│  PRD → 卡片 │     │  代码 → 测试  │     │  合入 → 关卡   │
└─────────────┘     └──────────────┘     └───────────────┘
      ↑                    ↑                    ↑
 人类定方向           AI 执行实现          AI 执行收尾
 AI 辅助拆解        人类验收结果          流程自动闭环
```

## 第一阶段：/prd — 需求拆解

使用 `/prd` 将产品需求生成结构化 PRD 文档，并拆分为多个 iCafe 卡片。

**为什么要先写 PRD：**
- 用户故事与验收标准
- **Non-Goal**（明确不做的事）
- 卡片依赖关系与实现顺序

PRD 写完后再拆卡片，每个卡片足够小、验收标准足够明确，才能配合 `/goal` 高效实现。

## 第二阶段：/goal — 逐卡实现

通过 `/goal 实现卡片 XXX`，Claude Code 自动完成：
1. 查询卡片获取描述和验收标准
2. 理解项目上下文（CLAUDE.md、现有代码）
3. 实现代码
4. 编写测试
5. 验证（go vet、go build、go test）

## 第三阶段：/after-goal — 提交合入关闭卡片

固化为 Skill 后，Claude Code 自动执行：
1. 提交代码（commit message 以卡片 ID 开头）
2. 推送 Gerrit
3. 打分 + 合入
4. 更新卡片描述（保留原有内容追加实现总结）
5. 关闭卡片（先查可用状态）

## 经验总结

### 1. PRD 先行，避免返工
### 2. 卡片粒度要适中
### 3. 依赖关系决定实现顺序
### 4. CLI 工具优于浏览器操作
### 5. Skill 是流程知识的载体
### 6. 踩坑即修正，不留到后面

## 三阶段协作模式

| 阶段 | 人类角色 | AI 角色 |
|------|---------|---------|
| **/prd** | 主导方向 | 辅助结构化输出 |
| **/after-goal** | 无需介入 | 全自动执行，流程自动闭环 |
