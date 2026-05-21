---
source_url: https://mp.weixin.qq.com/s/4bSn0UiTauf_FoMGMS6JBQ
ingested: 2026-05-19
sha256: 0736b74654f783c04d3d2194adc55ba421e2c96b9ff8ff8c5ef2baf690048a9d
title: 伯克利神作背刺OpenAI：持续学习才是真神！
author: 新智元
source: 微信公众号
note: web_extract抓取，内容截断~5000字。核心信息完整。
---

# 伯克利神作背刺OpenAI：持续学习才是真神！

**来源**：新智元，2026年5月18日

## 核心内容

伯克利等发布FST框架：通过快慢分层解决大模型持续学习死局。

AI工程师Dan McAteer预言，2026年持续学习（continual learning）即将爆发。

通过记忆/上下文快速适应+权重缓慢调整的分层机制，模型保留可塑性避免灾难性遗忘。

这是伯克利等机构的AI实验：让同一个大语言模型连续学三个任务——先学需要多跳检索的事实核验HoVer；再学代码推理CodeIO；最后学物理题Physics。每个任务训200步就切换。

用主流RL范式训练，模型在第一关HoVer上学会。到了第二关CodeIO完全卡住。学不动。

换上FST框架，同一个模型，三关都能学会。

## 关键论文

- 标题：Learning, Fast and Slow: Towards LLMs That Adapt Continually
- 预印本：https://arxiv.org/abs/2605.12484
- 项目主页：https://gepa-ai.github.io/gepa/blog/2026/05/11/learning-fast-and-slow/

## 作者阵容

Matei Zaharia (Databricks联合创始人，Apache Spark作者)
Joseph Gonzalez (伯克利，vLLM作者之一)
Inderjit Dhillon (UT Austin与Google，ML领域元老级人物)
以及一群伯克利的博士。

## FST核心思想

不要一组参数同时承担两个矛盾职能。传统RL训练里模型只有一组参数——既要「快速适应当前任务」又要「保留通用推理能力」。两者天然冲突。

FST做法：分成两套权重。
- 慢权重：模型参数，定期用RL调
- 快权重：prompt优化器GEPA自动演化

两者交替更新。类比大脑的互补学习系统（CLS）：海马体是快权重，新皮层是慢权重。

## 关键结果

- 数据效率：CodeIO上达到RL同等性能仅用1/3训练步数——3倍效率
- 遗忘减少：匹配准确率下KL散度比RL低70%
- 可塑性保留：训完Math后再训HoVer-hard，RL模型几乎完全学不动（可塑性塌缩到0），FST几乎恢复到基础模型水平
- 持续学习：三任务连续切换（HoVer→CodeIO→Physics），FST三关全过，RL在第二关卡住

## 行业格局

- Ilya Sutskever认为持续学习还要5-20年
- 业界过去两年集体押注推理（reasoning）
- FST首次让持续学习从空想变成可工程化的方向

## 核心洞察

「快慢分工」作为一种范式语言，比FST这个具体方法更重要。
推理能力不是AI的终点——持续学习才是。
