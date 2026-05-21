# SDAR 门控 OPSD 插入方案 · 实施记录

> **文档版本**: v1.0 · 2026-05-21
> **作者**: 子产+匠石（核战队）— 军师 实施
> **状态**: ✅ 已实施（Phase 0-3）
> **源代码**: `scripts/izu_sdar.py`（~350行）
> **完整计划**: `wiki/raw/祝成果/sdar-integration-plan.md`

## 概述

SDAR (Self-Distillation with Adaptive Reward) 门控 OPSD 将 izu 管线内置的质检信号（出口评分卡、CP2、对齐检查、沙箱验证、引文验证、核断言分）融合为门控信号，用于 On-Policy Self-Distillation 损失计算。

## 架构

┌──────────────────────────────────────┐
│          OPSDManager                  │
│  (单例，管理OPSD状态机 + 梯度缓冲区)   │
├──────────────────────────────────────┤
│  ┌─────────┐ ┌────────┐ ┌──────────┐ │
│  │Teacher  │ │Student │ │Gate Sig  │ │
│  │Snapshot │ │Buffer  │ │Fuser     │ │
│  └────┬────┘ └───┬────┘ └─────┬────┘ │
│       │          │             │      │
│  ┌────▼──────────▼─────────────▼────┐ │
│  │     OPSD Loss Computer           │ │
│  │  (对比teacher/student logits)    │ │
│  └──────────────────────────────────┘ │
└──────────────────────────────────────┘

## 关键决策

**MiniMax M2.7 不支持 logprobs** → SDAR 使用 DeepSeek 收集 logprobs，主流程保持 MiniMax。
`parse_logprobs_from_response()` 对不支持的 provider 返回 None，零侵入。

## 文件清单

| 文件 | 说明 |
|------|------|
| `scripts/izu_sdar.py` | OPSDManager + parse_logprobs + 双日志 |
| `scripts/izu-pipeline.py` | call_api() 扩展 + 主循环门控注入 + 负样本采集 |
| `scripts/izu-env.sh` | SDAR_ENABLED / SDAR_MODE 环境变量 |

## 输出文件

| 文件 | 格式 | 用途 |
|------|------|------|
| `~/.hermes/sdar_gate_log.jsonl` | JSONL | 门控信号日志，每步一条 |
| `~/.hermes/sdar_negative_samples.jsonl` | JSONL | 负样本库，每次回溯一条 |

## 使用方法

```bash
# 启用收集模式（采集教师快照）
SDAR_ENABLED=1 SDAR_MODE=collect python3 -u izu-pipeline.py "<主题>"

# 启用训练模式（师生对比，需要同主题已跑过collect）
SDAR_ENABLED=1 SDAR_MODE=train python3 -u izu-pipeline.py "<同主题>" --from 探

# 零开销模式（不产生任何SDAR调用，默认）
SDAR_ENABLED=0 python3 -u izu-pipeline.py "<主题>"
```

## 三种运行时模式

| 模式 | 值 | 行为 | 开销 |
|------|-----|------|------|
| 收集 | `collect` | 教师快照采集 + 门控信号日志 | ~50ms/步 |
| 训练 | `train` | 师生对比 + OPSD权重计算 + 梯度记录 | ~100ms/步 |
| 冻结 | (SDAR_ENABLED=0) | 零开销 | 0 |

## 信号融合公式

```
gate_score = α * exit_score_norm + β * quality_ratio + γ * cite_score_norm
gate_scaled = 2 * clip(gate_score, 0, 1) - 1  # 映射到 [-1, 1]
```

默认权重: α=0.4 (exit_score), β=0.4 (quality_checks), γ=0.2 (cite_score)

## 待做

- 用 `SDAR_MODE=collect` 跑 3~5 个不同 topic 的完整流水线，采集 gate_score 分布，校准正负阈值
