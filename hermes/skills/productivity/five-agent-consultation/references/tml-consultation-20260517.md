# TML交互模型五人合议记录 · 2026-05-17

**事件**：Thinking Machines Lab 交互模型（TML-Interaction-Small）
**触发**：用户说"极大，<视频URL>"
**类型**：完整五人合议（标准模式）
**关联技能**：media-transcribe-research（视频评估分析→极大分流→合议触发）
**子代理模型**：deepseek-chat（5/5完成）
**总耗时**：约8分钟（5个子代理 + 军师终裁）

---

## 核心输入

视频内容：TML-Interaction-Small（276B MoE/12B激活）
- 200ms time-aligned micro-turns
- Encoder-free early fusion
- 双模型架构（前台200ms实时 + 后台异步推理）
- FD-bench 77.8 vs GPT-2-RT 46.8，延迟0.40s

来源公司：Mira Murati创立，翁荔加盟，$2B种子轮

## 各Agent产出摘要

| Agent | 核心结论 |
|-------|---------|
| **子产** | 该关注/研究（窄做），不着急接入API。取方法论投入ITA和核战队设计 |
| **韩信** | 6个月后双模型协同架构原型。0-2月TML消化→2-4月方法论吸收→4-6月原型集成 |
| **鲁班** | 砍42%任务：紧凑上下文包永久砍掉、前台Agent合并到双通道。P0只做3件事 |
| **萧何** | P0窗口不足（鲁班估20h实际22.5h），发现隐性工时。三档时间线+风险矩阵 |
| **子贡** | 方案A(22.5h·混合轮换·等POC结果)+ABC三预案+三级包装方案+周报模板 |

## 关键冲突与裁决

| 冲突 | 裁决 |
|------|------|
| P0窗口20h vs 22.5h | 采信萧何—鲁班低估了文档撰写+测试排错 |
| 双通道执行时间：P0 vs P2 | 采信鲁班—核战队反馈闭环未跑通前不宜启动 |
| 紧凑上下文包 | 永久砍掉—与Hermes session/checkpoint/context engine 三重重叠 |

## 军师终裁

**方案A**：TML拆解入库(4h) + ITA M1推进(持续) + 双通道POC脚本(7.5h)
**排班**：混合轮换（每日三事各20min）
**POC失败**：等结果再决策（POC 7.5h=7.5天工期，现在花3-5h规划备用方案等于提前浪费40%工时）

## 配套产出

- 评估分析：`wiki/research/thinking-machines-lab-interaction-model-eval.md`
- 转录稿：`wiki/raw/thinking-machines-interaction-model-transcript.md`
- 原始JSON：`wiki/raw/thinking-machines-interaction-model-raw.json`

## 关键洞察（用于后续合议）

1. **萧何必须验证鲁班的工时假设** — 鲁班的工程估算常暗含"每天2-3小时"的隐性假设，与张成市日均1h不符
2. **合议→评估分析整合** — 极大视频触发的合议，军师终裁结论须写入视频评估分析的C.改进建议栏
3. **信息同源偏差** — 连续处理同一频道"最佳拍档"的三期视频，报道风格趋同，评估分析需主动找反方视角
