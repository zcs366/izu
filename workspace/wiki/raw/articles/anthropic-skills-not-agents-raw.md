---
source_url: "https://mp.weixin.qq.com/s/8525DGuxO-W4tQ8v2Hf1Fg"
title: "Anthropic高管断言：别再造AI智能体了！他们用一个文件夹就可以取代智能体"
author: "言非言（AI思想者）— 编译自Anthropic Barry & Mahesh内部演讲"
source: "微信公众号"
ingested: 2026-05-17
sha256: "pending"
---

# Anthropic高管断言：“别再造AI智能体了！”他们用一个文件夹，就可以取代智能体

> 本文基于Anthropic团队核心成员Barry与Mahesh的最新内部演讲实录编译。他们主导了Claude Code及Agent Skills的开发。

## 核心论点

当所有人都在给AI套壳、造各种垂直领域的"智能体(Agent)"时，Anthropic团队踩了刹车。他们发现：**代码才是连接数字世界的通用接口，不需要那么多五花八门的Agent。**

## 痛点：智商300的AI报不好税

AI有智商有能力，但缺乏「专业经验」。智商300的天才数学家和经验丰富的税务老手——你会选后者。现在的AI就像前者，不给极其详尽的背景信息就干不好活。

## 解法：别造Agent了，造Skill

Skill本质上就是一个「文件夹」，里面打包了文件、指令和程序化知识。放在Git里做版本控制，扔进Google Drive，打包给同事。

相比传统「工具(Tools)」，Skills解决两个致命痛点：

1. **告别冷启动死锁**：传统工具指令模糊AI就卡死。Skills含代码脚本，代码自文档化，AI可自己修改。
2. **拯救上下文窗口**：Skills采用「运行时渐进式加载」— 平时只看目录(Metadata)，要用时才读skill.md。支持挂载成百上千个技能。

## MCP + Skills = 2026 AI终极架构

- MCP连接外部世界的数据
- Skills提供处理这些数据的「专家经验」

**通用架构**：Agent Loop + Runtime（文件系统+代码环境）+ MCP Servers + Skills

基于此架构，Claude无需重新训练，配上对应MCP和Skills就变身行业专家。

## 终极目标：让AI自己写技能

「陪你工作了30天的Claude，绝对比第1天的Claude强得多。它能瞬间获取新能力，按需进化，丢弃过时技能。」

## 终极类比

模型 = CPU，Runtime = 操作系统，Skills = 应用软件。

世界上只有少数公司能造CPU和操作系统，但有数以千万计的开发者可以写软件。Skills就是把AI的「应用层」向所有人敞开。
