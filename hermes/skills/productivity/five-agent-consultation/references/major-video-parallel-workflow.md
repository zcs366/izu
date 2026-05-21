# 极大视频 + 并行转录 + 五人合议工作流

## 模式概述

当用户发送「极大」标记的视频URL时，需要并行启动两条流水线：
1. **转录流水线**：下载音频→faster-whisper→格式化原文
2. **合议流水线**：搜索文字参考→启动五Agent合议（子产→韩信→鲁班→萧何→子贡）

两条流水线互不阻塞。文字参考充足时，评估分析可在STT完成前先行输出。

## 步骤

### 并行启动

```
[收到「极大」视频URL]
  ├─→ 后台: 音频下载(yt-dlp) + faster-whisper转录 (notify_on_complete)
  └─→ 前台: 搜索中文/英文文字参考 + 提取核心技术点
```

### 文字参考搜索策略

1. 优先搜索中文资料（51CTO、CSDN、知乎、新浪财经、微信公众号）
2. 英文补充（TechCrunch、VentureBeat、The Decoder、官方博客/论文）
3. 目标：找到足够写评估分析的结构化内容

### 合议顺序

```
文字参考收集完毕 → 启动合议:
  Step 1: 子产（需求判断）— delegate_task
  Step 2: 韩信（技术远景）— delegate_task（接收子产输出）
  Step 3: 鲁班（工程审计）— delegate_task（接收韩信终局）
  Step 4: 萧何（执行路径）— delegate_task（接收鲁班审计）  ← 可能中断/超时
  Step 5: 子贡（调度包装）— delegate_task（接收萧何路径）  ← 可能中断/超时
  Step 6: 军师终裁
```

### 转录完成后

转录完成后：
1. 校对润色（专有名词修正、合并段落、补标点）
2. 格式化输出（时间戳`## MM:SS` + `>`引用块 + `---`分隔）
3. 存入：`wiki/raw/{slug}-transcript.md`
4. 双路输出：`/mnt/i/hermes/output/极大/{slug}-transcript.md`

### 终裁并入

军师终裁结论写入评估分析的 `C.改进建议` 栏。完整评估分析存入：
- `wiki/research/{slug}-eval.md`
- `/mnt/i/hermes/output/极大/{slug}-eval.md`

### 已知风险

- 萧何和子贡的delegate_task可能中断/超时（deepseek-chat已验证10/10成功率，但长context时仍可能被interrupted）
- 中断时：军师直接执行分析，覆盖缺失角色的视角
- 转录耗时：13-19分钟视频→8-13分钟CPU转录，后台跑不阻塞
