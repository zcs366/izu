---
source_url: https://mp.weixin.qq.com/s/a1GnGX_FGfr-bEhh0U2kvA
ingested: 2026-05-19
sha256: pending
title: SafeHarness：Agent 运行时安全四层架构
author: 微信公众号（转载 arXiv 论文）
source: 微信公众号
---

# SafeHarness：Agent 运行时安全四层架构

**论文**：*SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment*

## 核心主张

当 LLM 成为 Agent 并调用工具、读写网页/文件/记忆、执行多步骤任务时，安全必须嵌入 Agent 的运行时（Harness），而非仅靠输入输出过滤。

## 传统护栏的三个不足

1. 看不到 Harness 内部状态（风险藏在中间过程）
2. 各安全模块孤立，信号不互通
3. 缺少恢复能力（仅有放行/拦截）

## 六类威胁

- 直接提示注入 / 间接提示注入 / 工具滥用 / 工具篡改 / 记忆污染 / 权限升级

## 四层架构

### 1. Inform（信息净化层）
- 结构化清洗（零宽字符、Unicode 混淆）
- 规则匹配（注入句式）
- 语义过滤（独立 judge 模型区分事实 vs 命令）
- 来源标记（用户输入/工具输出/检索，不同信任等级）

### 2. Verify（动作验证层）
- 规则引擎（快速风险分数）
- 上下文 Judge（独立模型判定安全/不确定/不安全）
- 因果诊断（"没有隐藏指令时还会执行吗"）

### 3. Constrain（权限约束层）
- 能力令牌（有效期、调用次数、签名校验）
- 动态权限上限（破坏性→网络→执行→只读）
- 工具描述完整性校验

### 4. Correct（状态纠偏层）
- 定期检查点（文件系统/执行历史/会话/记忆/权限）
- 回滚至最近安全状态
- 安全降级档位：正常→禁用破坏性→禁用网络→禁用执行→只读

## 实验结果（Agent-SafetyBench）

- ReAct 模式：不安全行为率 ~50% → ~30%
- Multi-Agent：攻击成功率最低，但任务完成率受影响更明显
- Self-Evolving：无保护风险最高（长期记忆/技能演化扩大攻击面）

## 局限性

- 实验环境偏模拟
- 仍依赖 LLM judge（误判/漏判/被诱导）
- 运行时成本不可忽视
- 自适应攻击未解决

## 工程落地启发

1. 从内容审核到运行时安全
2. 工具调用是核心检测点
3. 权限控制不可依赖提示词
4. 记忆模块必须有安全边界
5. Agent 产品需要安全降级模式
