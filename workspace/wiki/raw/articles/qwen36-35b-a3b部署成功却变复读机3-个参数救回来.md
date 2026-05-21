---
source_url: file:///mnt/i/hermes/wiki_dropbox/Qwen3.6-35B-A3B部署成功却变复读机？3 个参数救回来.md
ingested: 2026-05-10
sha256: bd48b9c8722a738dcd6456d07f96f51dbf2a78f14e48f466827de506156c01f1
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: Qwen3.6-35B-A3B部署成功却变"复读机"？3 个参数救回来
---

# Qwen3.6-35B-A3B部署成功却变"复读机"？3 个参数救回来

> 来源: Qwen3.6-35B-A3B部署成功却变复读机？3 个参数救回来.md（用户存入 wiki_dropbox）

# Qwen3.6-35B-A3B部署成功却变"复读机"？3 个参数救回来

[![mikesay](https://pic1.zhimg.com/v2-abed1a8c04700ba7d72b45195223e0ff_l.jpg?source=32738c0c&needBackground=1)](https://www.zhihu.com/people/mikesay)

[mikesay](https://www.zhihu.com/people/mikesay)

关注

13 人赞同了该文章





《RTX 2080 Ti 22GB 成功部署 Qwen3.6-35B-A3B》发出去很受欢迎，很多读者照着部署成功了，有人说"老显卡终于没白压着"。

部署跑通后，我接着用 TurboQuant 把上下文从 48K 扩展到 128K，解决了长文章读不完的问题。

但折腾还没完——又有朋友反馈：**模型跑是跑起来了，一问长回答就变成复读机，循环复读永不停！**

经过研究，问题解决了。今天从头到尾讲清楚，让大家少踩坑。

------

## 一、什么叫"复读机"？

先说现象。模型部署好了，启动正常，速度也还行。但一问稍微长一点的问题，输出就变成这样：

> 机器学习是人工智能的一个分支，让计算机通过数据学习规律……机器学习是人工智能的一个分支，让计算机通过数据学习规律……机器学习是……

**一句话循环往复，永远停不下来。** 不是卡死，速度照样跑，但内容全是废话。

更诡异的是，短回答没问题，一问长回答就出问题。你以为模型坏了，其实只是参数没调对。

------

## 二、为什么偏偏是 Qwen3.6 会这样？

要解决问题，先搞清楚原因。

Qwen3.6-35B-A3B 是个 MoE（混合专家）模型，总参数 35B，但每次推理只激活约 3B 参数。这和传统稠密模型有本质区别：

**[MoE 模型](https://zhida.zhihu.com/search?content_id=274459991&content_type=Article&match_order=1&q=MoE+模型&zhida_source=entity)每次只激活一小部分"专家"，采样分布和稠密模型完全不同。** 它对 [min_p](https://zhida.zhihu.com/search?content_id=274459991&content_type=Article&match_order=1&q=min_p&zhida_source=entity) 等采样参数特别敏感，默认参数在 MoE 模型上就会出问题。

具体来说，三个参数是罪魁祸首：



| 参数                                                         | 默认值 | 问题                                                         |
| ------------------------------------------------------------ | ------ | ------------------------------------------------------------ |
| min_p                                                        | 0.1    | 阈值太高，过滤掉太多合理候选词，模型只能在少数几个词里选，最后只能复读 |
| [repeat_penalty](https://zhida.zhihu.com/search?content_id=274459991&content_type=Article&match_order=1&q=repeat_penalty&zhida_source=entity) | 1.1    | 和 MoE 采样器冲突，反而让模型更爱重复                        |
| [temp](https://zhida.zhihu.com/search?content_id=274459991&content_type=Article&match_order=1&q=temp&zhida_source=entity) | 1.0    | 对指令任务偏高，输出不够稳定                                 |



**简单说：默认参数是为稠密模型设计的，MoE 模型拿来用，就像让穿跑鞋的人去跳芭蕾——不是不能跳，是得换双合适的鞋。**

------

## 三、修复方案：改几个参数就够了

不用重装、不用编译，只要在启动命令里加几个参数就行。

## 核心修复参数

```text
--min-p 0.0
--repeat-penalty 1.0
--temp 0.6
--top-k 40
--top-p 0.95
```

## 参数解释



| 参数             | 设置值 | 为什么这么设                                                 |
| ---------------- | ------ | ------------------------------------------------------------ |
| --min-p          | 0.0    | 禁用最小概率过滤，保留所有候选词，模型可以自由选词不再复读   |
| --repeat-penalty | 1.0    | 禁用重复惩罚，排除与采样器的冲突                             |
| --temp           | 0.6    | [Qwen 官方推荐](https://zhida.zhihu.com/search?content_id=274459991&content_type=Article&match_order=1&q=Qwen+官方推荐&zhida_source=entity)温度，平衡创造性与确定性 |
| --top-k          | 40     | Qwen 官方推荐，限制采样范围                                  |
| --top-p          | 0.95   | Qwen 官方推荐，核采样保证多样性                              |



**最关键的一个参数就是 --min-p 0.0，其他参数配合使用效果最佳。**

------

## 四、完整启动命令（Windows 批处理脚本）

把下面的内容保存为 .bat 文件，双击即可启动：

> **注意：** 以下路径 D:\llama-turboquant\ 是示例路径，请替换成你实际安装的路径。

```text
@echo off
chcp 65001 >nul
cls
echo ========================================
echo   TurboQuant - 128K Context Mode
echo   with Anti-Repetition Fix
echo ========================================
echo.
set PATH=D:\llama-turboquant\dlls;%PATH%
cd /d D:\llama-turboquant\bin

llama-server.exe ^
  -m D:\llama-turboquant\models\qwen3.6-35b-a3b-instruct-Q4_K_M.gguf ^
  --jinja ^
  -ngl 99 ^
  -c 131072 ^
  -fa on ^
  -t 8 ^
  -b 4096 ^
  --cache-type-k q4_1 ^
  --cache-type-v q4_1 ^
  --host 0.0.0.0 ^
  --port 8081 ^
  --no-mmap ^
  -np 1 ^
  --min-p 0.0 ^
  --repeat-penalty 1.0 ^
  --temp 0.6 ^
  --top-k 40 ^
  --top-p 0.95

pause
```

**说明：**

- -c 131072 是 128K 上下文（TurboQuant 模式），如果不用 TurboQuant 可以改成 -c 49152
- 其他参数和上篇文章一致，全 GPU 加速、8 线程、Flash Attention 开启

------

## 五、修复效果对比

我用两个测试任务验证了修复效果。

## 测试 1：写一段Python代码

**提示词：** 请用 Python 写一个快速排序算法，每步解释一下。

**修复前：** 循环复读，无法结束。

**修复后：**

> 快速排序是一种高效的排序算法，核心思想是选择一个基准值，将数组分为小于和大于基准的两部分，然后递归排序。
> 以下是 Python 实现：
> def quick_sort(arr): if len(arr) <= 1: return arr pivot = arr[len(arr) // 2] left = [x for x in arr if x < pivot] middle = [x for x in arr if x == pivot] right = [x for x in arr if x > pivot] return quick_sort(left) + middle + quick_sort(right)
> 每步解释：
> 选择中间元素作为基准值（pivot） 将数组分为三部分：小于、等于、大于基准 对左右两部分递归调用快速排序 将结果拼接返回
> 时间复杂度平均为 O(n log n)，是最常用的排序算法之一。

**流畅自然，代码正确，没有一句废话。**

## 测试 2：连续 5 个任务稳定性

连续跑了 5 个不同长度的任务，结果全部成功，无任何复读现象：



| 任务 | 输入 tokens | 输出 tokens | 生成速度 | 状态 |
| ---- | ----------- | ----------- | -------- | ---- |
| 1    | 34          | 805         | 47.0 t/s | ✅    |
| 2    | 144         | 1339        | 50.1 t/s | ✅    |
| 3    | 46          | 2100        | 46.2 t/s | ✅    |
| 4    | 89          | 95          | 48.0 t/s | ✅    |
| 5    | 238         | 104         | 45.7 t/s | ✅    |



**修复前后对比：**



| 指标       | 修复前     | 修复后     |
| ---------- | ---------- | ---------- |
| 复读现象   | 偶尔出现   | 完全消失   |
| 生成速度   | 45-48 t/s  | 47-50 t/s  |
| 回答质量   | 循环、无效 | 流畅、自然 |
| 任务完成率 | 约 70%     | 100%       |



**修复不仅解决了复读问题，速度还略有提升。**

------

## 六、踩坑经验总结

## 经验 1：min_p 不是越小越好，但 MoE 模型确实需要关掉

--min-p 0.0 对 Qwen MoE 模型是必须的。如果你用其他 MoE 模型（比如 Mixtral），可以从 --min-p 0.02 开始测试，逐步调整。

## 经验 2：repeat_penalty 必须和 min_p 配对

单独改 min_p 效果有限，必须同时把 repeat_penalty 设为 1.0（禁用），否则两个参数互相冲突，问题依旧。

## 经验 3：采样器顺序不用管

实测默认顺序就能正常工作，不需要手动指定采样器链。

## 经验 4：生成速度不受影响

很多人担心改参数会降低速度。实测下来，修复后速度反而略有提升（47-50 t/s），因为模型不再重复无用输出，有效吞吐量提高了。

------

## 七、适用模型范围

这个方案在我的配置上验证有效：

- ✅ **Qwen3.6-35B-A3B (Q4_K_M)** + TurboQuant 128K 上下文
- ✅ **Qwen3.6-35B-A3B (Q4_K_M)** + llama.cpp 标准模式 48K 上下文
- ⚠️ **其他 Qwen MoE 系列**：可能需要微调 min_p 值
- ⚠️ **其他 MoE 架构**：建议从 --min-p 0.02 开始测试
- ℹ️ **非 MoE 模型（纯稠密模型）**：默认参数通常没问题，不需要改

------

## 写在最后

折腾老显卡就像修一辆老车——**每一个问题都是和它对话的机会，每一次踩坑都是更懂它的过程。**

RTX 2080 Ti 是几年前的旗舰卡，现在价格只有新卡的零头。但很多人下载了模型、尝试了部署，但遇到一个问题就放弃了。其实只要搞懂了底层原理，老显卡照样能跑出好效果。你们看，本文就是本地模型Qwen3.6-35B-A3B帮我修改的，效果还不错吧。

如果你也遇到本地模型出现复读机问题，照着上面的参数改一下，立竿见影！

------

**RTX 2080 Ti 22GB 部署 Qwen3.6-35B-A3B 系列文章导航：**

1. 第一篇：[RTX 2080 Ti 22GB 成功部署 Qwen3.6-35B-A3B](https://zhuanlan.zhihu.com/p/2036104742041019044)
2. 第二步：[TurboQuant 解锁 128K 上下文](https://zhuanlan.zhihu.com/p/2036106454172705932)
3. **第三步：解决复读机问题** — 本文
