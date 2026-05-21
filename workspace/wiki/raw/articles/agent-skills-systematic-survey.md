---
title: "首篇Agent Skills系统性综述"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/uVSHYFtwx27t4lEgl-yp6w"
author: "MindChain.AI"
date: 2026-05-19
ingested: 2026-05-19
sha256: 0bf168df6d07b0b2b898502acf37c25e54e377108141f495093eb46dac34f508
type: article
tags: [agent-skills, survey, skill-lifecycle, 127-papers]
eval_level: 极大
---

# 首篇Agent Skills系统性综述

**论文**: A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications
**arXiv**: https://arxiv.org/abs/2605.07358v1
**GitHub**: https://github.com/JayLZhou/Awesome-Agent-Skills

## 核心洞察
"这不是模型不够聪明。而是它缺了一种人类天然具备的能力：把重复经验变成可复用的肌肉记忆。"

首次系统性定义 Agent Skills，围绕"表示→获取→检索→进化"四阶段，梳理 127 篇文献。

## 技能定义
技能 = (M, R, C) 三元组
- M：主指令文档（怎么做）
- R：辅助资源（模板、脚本、参考资料）
- C：触发条件（什么时候该用）

## 三种类型
| 类型 | 特点 |
|------|------|
| 纯文本型 | 参考文档、示例、模板——可读性强，执行确定性弱 |
| 纯代码型 | 可执行脚本、函数——执行可靠，维护成本高 |
| 混合型 | 文本+代码——兼顾可读与可执行，一致性维护最复杂 |

Claude Code的CLAUDE.md + 辅助脚本 = 混合型技能的实践。

## 四条获取路径
1. **人类专家手写**——精度最高，扩展性差（种子层）
2. **从经验中提炼**（最主流）——筛选→抽象压缩→记忆重组→流程打包
3. **即时构建**——新需求时LLM生成候选技能（CREATOR、ToolMakers）
4. **从外部资料挖掘**——文档、代码仓库、Kaggle方案

## 检索四策略
1. 语义向量检索（最常用，但语义近≠适用）
2. 关键词检索（补充过滤）
3. 生成式检索（LLM直接生成技能ID）
4. 结构化检索（层级/依赖关系缩小范围）

**关键发现**：检索召回率 ≠ 执行成功率。

## 技能进化五环节
| 环节 | 内容 |
|------|------|
| 修订 | 失败后修改技能内容 + 单元测试验证 |
| 验证 | 测试通过才能入库 + 成熟度门槛 + 回滚 |
| 策略耦合 | 技能库成为策略训练的一部分 |
| 仓库级进化 | 多用户轨迹汇聚→验证→同步更新 |
| 运行时治理 | "投毒技能"风险——第三方技能隐藏恶意逻辑 |

## 启示
1. Agent竞争力：技能管理能力 > 模型能力
2. 技能生命周期管理 > 技能本身
3. 技能生态系统已成型：SkillNet（30万+）、ClawHub（4万+）、SkillsMP（70万+）
