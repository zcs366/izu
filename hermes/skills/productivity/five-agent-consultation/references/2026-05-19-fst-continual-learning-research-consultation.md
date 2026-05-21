# FST持续学习论文研究合议 · 2026-05-19

## 背景

用户发送「极大」标记的微信文章链接，内容为伯克利+Databricks的FST（Fast-Slow Training）框架，通过快慢分层解决LLM持续学习问题。

## 合议序列（6轮完整，零超时）

| Round | 角色 | 模型 | 耗时 | 核心发现 |
|-------|------|------|------|---------|
| 0 | 惠施 | deepseek-chat | 43s | 7概念操作性定义+5模糊地带 |
| 1 | 墨子 | deepseek-chat | 160s | **O(1)vsO(N)漏洞**：快权重~30Kb固定容量，N>5饱和 |
| 2 | 商鞅 | deepseek-chat | 81s | 12任务三梯度实验，最小烟雾测试1.5h |
| 3 | 鲁班 | deepseek-chat | 119s | izu已在FST范式路上(Skill=快权重)，仅需400行 |
| 4 | 萧何 | deepseek-chat | 104s | 方案A: 2-3天/13-18h，日均API<3¢ |
| 5 | 张仪 | deepseek-chat | 38s | **表征冲突**：多Skill共享KV-Cache的信号混叠 |
| — | 军师 | 直断 | — | 裁决+签核，P0烟雾测试前置 |

## 关键发现

### 墨子：信息论漏洞
快权重容量固定~30Kb（M×L×H），任务知识~2-8Kb/task线性增长。N>5时快权重饱和→慢权重被迫漂移→FST退化回RL。论文仅测N=3-5，恰好落在边界内。

### 张仪：表征冲突（5Agent集体盲区）
不是容量问题——是多个快权重在共享Transformer注意力头中的信号混叠。8-15个Skill并行激活时互相覆盖信号。降级方案：显式Skill路由（50行，每次只激活1-2个Skill）。

### 陷阱二十：容量错觉
鲁班「无容量限制」vs 墨子「N>5饱和」的冲突被裁决为**非冲突**——鲁班指磁盘存储容量，墨子指信息编码容量，张仪指表征空间容量。同一词三层含义。

## 输出
- raw: `wiki/raw/articles/fst-continual-learning-wechat.md`
- output: `output/极大/fst-continual-learning-eval-20260519.md`
