---
source_url: "https://mp.weixin.qq.com/s/8525DGuxO-W4tQ8v2Hf1Fg"
title: "Anthropic高管断言：别再造AI智能体了！他们用一个文件夹就可以取代智能体"
author: "言非言（AI思想者）— 编译自Anthropic Barry & Mahesh内部演讲"
source: "微信公众号"
ingested: 2026-05-17
sha256: "pending"
project_relevance: "🔴极高 — Anhtropic官方表态「Skills文件夹取代Agent」，直接证明核战队Skills架构方向正确"
---

# 评估分析：Anthropic「造Skill不造Agent」

## 前置说明

**来源**：Anthropic核心团队成员Barry & Mahesh（Claude Code及Agent Skills主导开发者）内部演讲实录，由「AI思想者」编译。

**核心主张**：**停止构建Agent，开始构建Skills。** Agent Loop + Runtime + MCP Servers + Skills = 2026 AI终极架构。

---

## A. 核心论点评估

### 核心主张

**「智商300的AI做不好报税，因为它缺乏领域专业知识。解决方案不是给AI套更多壳、造更多Agent，而是用最简单的'文件夹'把专家经验打包成Skills——代码自文档化、运行时渐进加载、AI可自己写自己改。Skills就是AI时代的'应用软件'。」**

### 与我们已有体系的直接对应

| Anthropic的四个组件 | 我们的对应 | 状态 |
|-------------------|-----------|------|
| Agent Loop（管理上下文） | Hermes Agent / AIAgent / HermesAgentLoop | ✅ 已有 |
| Runtime（文件系统+代码环境） | izu / 终端 / 文件系统 | ✅ 已有 |
| MCP Servers（连接外部工具） | web_extract / browser / 各工具API | ✅ 已有 |
| **Skills（专业知识库）** | **izu的SKILL.md + 核战队Fat Skills** | ✅ **已做且完全一致** |

### 核心洞察逐条验证

**1. 「代码是数字世界的通用接口」**
- Barry & Mahesh发现：让AI写财务报告、做数据分析、生成文档——底层只需要Bash+文件系统
- ✅ 与核战队设计一致——所有Agent最终都通过终端+文件操作

**2. 「Skills解决两个致命痛点」**
- **告别冷启动死锁**：传统工具指令模糊→AI卡死。Skills含代码脚本，代码就是文档，AI可自己修改
- **拯救上下文窗口**：元数据(Metadata)平时加载，技能文件夹(skill.md)按需渐进加载→支持挂载成百上千Skills
- ✅ **核战队五人合议思路一致**——每个Agent只加载自己需要的Skills，不污染全局上下文

**3. 「运行时渐进式加载」**
- 传统做法：把所有工具定义塞进system prompt → 上下文爆了
- Skills做法：只加载目录(Metadata)，要用时再读skill.md
- ✅ **核战队正是此模式**——合议时才召唤对应Agent

**4. 「持续学习 — AI自己写Skills」**
- 未来：AI把写过的程序化知识打包成Skill → 供未来的自己使用
- 「陪你工作30天的Claude，比第1天的Claude强得多」
- ✅ **iza的终极方向**——每次合议技能进化

**5. 「模型=CPU，Runtime=OS，Skills=Apps」**
- 世界只有少数公司能造CPU和操作系统
- 数以千万计的开发者可以写App
- ✅ **Skills层是最大的机会**——izu对标的就是这个「App层」

---

## B. 定论

### 这篇文章的价值：不是新发现，是官方定论

我们已经在做的（SKILL.md、核战队、izu技能体系），Anthropic今天说「这是对的」。

这不是普通的文章，这是Anthropic核心团队从Claude Code的开发实践中得出的架构结论——而我们在独立推理中也走到了完全相同的方向。

| 我们的判断 | 印证力度 | Anthropic的说法 |
|-----------|---------|---------------|
| Thin Harness + Fat Skills | ✅ 终极印证 | 「代码是通用接口，不需要五花八门的Agent」 |
| 技能渐进式加载 | ✅ 终极印证 | 「Metadata目录→按需读skill.md，支持上千技能」 |
| 技能持续进化 | ✅ 方向性印证 | 「AI自己写Skills，第30天比第1天强」 |
| 模型=Cpu，Skills=App | ✅ 定义级印证 | 同样的类比 |

### 对我们意味着什么

**不要再去造什么「通用Agent平台」了。** 按照Anthropic指的路：
- Iz的路径完全正确——Skills作为AI时代的「App」
- 核战队的合议即「Agent Loop」
- MCP（或同等协议）作为外部数据连接器
- 文件和终端就是Runtime

**把这个架构固化下来，就是下一步的工作。**

---

## C. 建议行动

| # | 行动 | 优先级 |
|---|------|--------|
| 1 | 将本文原文+分析存入 `output/极大/` 和 wiki | 现在 |
| 2 | 核战队技能体系对照Anthropic的Skills设计做一次审计——是否有需要调整的设计点 | P1 |
| 3 | 持续学习机制：设计「技能年龄」概念——旧的Skill提醒维护 | P2 |
| 4 | 将此文作为核战队/izu对外叙事的「权威锚点」——「Anthropic官方也这么说」 | P0（用） |

---

## 附：原文精华摘要

> 「代码一旦写好就不再只是给我们看的，它也是给AI看的。AI可以读、可以改、可以自己写。」 — 代码自文档化

> 「传统工具一旦指令写模糊AI就卡死了。而Skills里的代码脚本，本身就是最好的文档。」 — 告别冷启动

> 「以前塞太多工具AI上下文就爆了。现在Skills采用运行时渐进式加载——平时只看目录，要用时才去读技能文件夹。」 — 救上下文窗口

> 「我们的目标是，陪你工作了30天的Claude，绝对比第1天的Claude强得多。它能瞬间获取新能力，按需进化。」 — 持续学习

> 「模型就像CPU，Runtime就像操作系统，Skills就像运行在上面的App。」 — 最终类比
