---
name: recursive-thinking
description: TRT（Test-time Recursive Thinking）——零训练、纯上下文驱动的递归自我改进。4轮迭代：生成rollouts→自排序→知识蒸馏→策略更新。答案提取经6次迭代收敛到鲁棒三层体系。配套代码辅助LSE实现跨批次prompt进化。izu前沿实验室·太阳神计划核心引擎。
version: 1.1.0
author: 军师祭酒 / izu前沿实验室
tags:
  - TRT
  - 递归思考
  - 自我改进
  - 零训练
  - Agent自我迭代
  - 数学推理
  - 太阳神计划
  - LSE
  - TRT-H
  - 元合议
trigger: "递归思考|TRT|自我改进推理|难题攻关|代码辅助进化|LSE|元合议|TRT-H"
metadata:
  hermes:
    category: research
------

# TRT · Test-time Recursive Thinking

> "让模型自己和自己下棋反思——零训练、纯上下文驱动的递归自我改进。"
> —— izu前沿实验室，基于微软TRT论文 (arXiv 2602.03094) 独立实现

## 一、核心算法

```
for round in 1..4:
  1. 生成rollouts (模型: 基于问题+知识+策略，生成3个候选解答，用"---"分隔)
  2. 自排序     (模型: 评估自己的候选，选最佳)
  3. 知识蒸馏   (模型: 对比最佳vs其他，提取教训)
  4. 策略更新   (模型: 基于新知识，生成新探索策略)
  [代码层: 答案提取(三层fallback)、教训去重(difflib,阈值0.7)、知识窗口(8条)、策略去重]
```

**匠石原则**：代码做循环控制、去重、答案提取、上下文管理。模型只做生成、排序、蒸馏、策略四项语义任务。

## 二、适用场景

- 数学推理题（GSM8K / AIME / MATH）
- 逻辑推理题（需要多步推理）
- 代码debug（自检+改进）
- 任何有确定答案、需要多次反思的推理任务

**不适用**：开放式创意任务（诗歌、故事），因为自排序缺乏客观标准。

## 三、使用方法

### 命令行

```bash
# 稳定版（推荐）
python3 /mnt/i/hermes/work/trt_v0.6.py

# 代码辅助LSE
python3 /mnt/i/hermes/work/lse_code_assisted_v1.py
```

编辑脚本中的 `PROBLEMS` 字典添加新题目。

### Python API

```python
from trt_v0_6 import trt_solve
answer, knowledge, clean_rate = trt_solve("你的问题", max_rounds=4, verbose=True)
```

## 四、已验证效果

### 演示题（4级难度）
| 难度 | 题目 | 答案 | 耗时 | 状态 |
|------|------|------|------|------|
| EASY | 速度×时间求和 | 200公里 | 32s | ✅ |
| MEDIUM | 折扣反算 | 300元 | 34s | ✅ |
| HARD | 连续整数平方和 | 7,8,9 | 41s | ✅ |
| AIME | 中国剩余定理 | 157,472 | 58s | ✅ |

### AIME标准benchmark（2024 AIME I 5题）
| 题目 | 得分 | 状态 |
|------|------|------|
| AIME1 (walk speed) | 0/1 | ❌ 发现退化问题 |
| AIME2 (log) | 1/1 | ✅ |
| AIME3 (game theory) | 1/1 | ✅ 提取失败 |
| AIME5 (circle) | 1/1 | ✅ |
| AIME8 (inradius) | 0/1 | ❌ |
| **总计** | **3/5 (60%)** | |

模型：deepseek-chat | 详见 `references/aime-benchmark-20260516.md`

## 五、已知限制

1. **答案提取噪音**：模型偶尔输出说明文字而非纯答案。代码层正在加fallback提取逻辑。
2. **上下文膨胀**：5轮后教训可能重复。已用difflib去重+8条滑动窗口缓解。
3. **自排序偏差**：模型可能偏好"看起来更完整"的答案而非"更正确"。
4. **仅限可验证领域**：数学/逻辑/代码。开放性任务需改造自排序标准。
5. **🆕 TRT退化**：当自排序不可靠时，递归可能放大错误（见AIME1案例）。这是TRT的边界条件——需要自排序准确率≥任务准确率的模型才能保证正向改进。
优先级2: 最后几行的等号后数字（跳过说明行）
优先级3: 最后非说明行中的数字序列
   └─ 失败→fallback到次佳rollout的答案
```

**关键修复**：不过滤单数字（AIME答案需要）、LaTeX清理、次佳fallback。

### 5.2 FINAL_ANSWER 格式陷阱 ⚠️

**不要用 `FINAL_ANSWER:` 格式。** 在TRT的一次调用生成3个rollout场景下，模型用"---"分隔3个方案，`FINAL_ANSWER` 行可能只出现在整个响应的末尾而非每个rollout内部。简单正则提取会导致全部FAIL。

详见 `references/answer-extraction-evolution.md`

## 六、配套：代码辅助LSE（跨批次进化）

TRT是"同题内递归反思"。LSE是"跨批次prompt进化"。

**代码辅助LSE** 突破了单模型元认知瓶颈：
- 代码层：错误分类（FORMAT/COMPUTE/OTHER）→ 模板匹配 → 选择进化方向
- 模型层：只做文本生成（根据模板生成修复后的Skill）
- 结果：50%→75% (+25pp)

详见 `references/code-assisted-lse.md`

## 七、已知限制

1. **仅限可验证领域**：数学/逻辑/代码。自排序在开放任务中缺乏客观标准。
2. **上下文膨胀**：4轮后教训可能重复——已用difflib去重+8条滑动窗口缓解。
3. **自排序偏差**：模型可能偏好"看起来更完整"的答案而非"更正确"。AIME级需人工复核。
4. **FINAL_ANSWER 在TRT中失败**：单次调用多rollout场景不可用。

## 八、配套：TRT-H元合议（群体层反思）

TRT-H在五人合议中植入元认知观察者，让多Agent系统反思自己的讨论流程。

**元角色**诊断低效模式（跟风/群体盲思/遗漏/主题漂移），发出硬约束干预指令。

**跨层发现——诊断-干预不对称性**：
- 个体层（TRT）：诊断✅ 干预⚠️（有效但不稳定）
- 工具层（LSE）：诊断✅ 干预⚠️（+25pp但未达上限）
- 群体层（TRT-H）：诊断✅ 干预❌（软指令共识比未降）

干预难度与系统复杂度成正比。详见 `references/methodology-document.md`

## 九、进化路线

```
v0.2-v0.5: 答案提取迭代（标注格式→FINAL_ANSWER陷阱→三层fallback）
v0.6 (当前): 鲁棒三层提取 + 次佳fallback，100%干净率
v0.7:       五人合议TRT杂交（五Agent各自递归→共享知识→再递归）
v1.0:       Hermes Skill集成 + 代码辅助LSE联动
```

## 九、使用方法

### 命令行

```bash
python3 /mnt/i/hermes/work/trt_v0.6.py
```

编辑脚本中的 `PROBLEMS` 字典添加新题目。

### 代码辅助LSE

```bash
python3 /mnt/i/hermes/work/lse_code_assisted_v1.py
```
