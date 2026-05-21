---
source_url: https://mp.weixin.qq.com/s/dNLJagjAoHtiUJj_bc8k0g
sha256: dbbb816340ad45a3f6ba529f92bb1bc85edd5867edd617f38f5dfb2dbd8c84eb
ingested: 2026-05-21
title: AI-First 产研团队的交付路径
author: 昀启AI+
source: 微信公众号
content_type: article
description: 提出六段式交付闭环、L0/L1/L2三层上下文加载模型、Skill-as-Code等原创概念框架，系统阐述AI-First团队的工作模式。
tags: [上下文工程, Skill-as-Code, AI-First, 六段式交付, 上下文加载模型]
---

# AI-First 产研团队的交付路径

**核心观点**：AI编程的差异不在模型能力，而在上下文质量。通过六段式交付闭环（需求→PRD→方案→拆解→编码→上下文更新）实现上下文逐级收敛，配合L0/L1/L2三层加载模型和Skill-as-Code，把AI编程从"玄学"拉回可管控、可度量、可复制的"工程学"。

**关键概念**：
- **初稿准确率**：AI协作的前置核心指标，比代码行数和生成速度更可靠
- **六段式交付闭环**：上下文逐级收敛、阶段持续校验、结果最终回写
- **隐性上下文**：每个阶段的显性产出给人审查，隐性上下文是下一阶段AI的真正"燃料"
- **L0/L1/L2三层加载模型**：项目级/文件级/任务级，在对的层级把对的信息以对的颗粒度交给对的执行环节
- **Skill-as-Code**：把团队规范和工作方法硬编码为可版本管理的工程资产
- **update-context Skill**：代码变更后上下文同步刷新，既"建新城"也"还旧账"

**六阶段职责分配**：

1. **业务需求**：人定义目标/边界/优先级，AI起草需求内容 → 产出需求文档
2. **PRD设计**（write-prd Skill）：人澄清歧义/确认范围，AI生成结构化PRD → 产出AI可执行的PRD
3. **技术方案设计**（write-tech-design Skill）：人评审架构可行性，AI产出方案初稿 → 产出技术方案+API契约
4. **任务拆解**（breakdown-tasks Skill）：人确认优先级与依赖，AI拆解为可执行单元 → 产出WBS任务列表
5. **Daily Coding Agent**（编码/单测/CR Skill）：人审核关键逻辑，AI编码→单测→CR→修复循环 → 产出可交付代码
6. **上下文更新**（update-context Skill）：人审检沉淀结果，AI回写知识与上下文 → 产出更新后的知识资产

**Skill工程价值**：
- 标准化：消除对个人Prompt水平的依赖
- 可复制：从个人经验转化为组织资产
- 可度量：可针对具体环节追踪初稿准确率
- 治理：将团队规范硬编码到AI执行过程中

**Agent执行**：Harness = 编排循环 + 工具 + 记忆 + 上下文管理 + 护栏 + 验证，全部模块协同工作。

---

## 对Hermes Agent实践的价值

**价值评估**：★★★★★（极高）

这篇文章的框架与张成市的Hermes Agent实践高度吻合：
1. **Skill-as-Code** 直接对应Hermes的Skill系统（.hermes/skills/），可将团队规范写成SKILL.md
2. **L0/L1/L2三层上下文模型** 可直接映射到Hermes的context loading策略
3. **六段式交付闭环** 为Hermes的workflow编排提供了完整的产研视角
4. **update-context Skill** 与Hermes的知识库自动更新能力完美对接
5. **初稿准确率** 作为AI协作的核心指标，可用于评估Hermes Agent的实际效果
