---
title: Google I/O 2026 — Agent全景发布
created: 2026-05-21
updated: 2026-05-21
type: concept
tags: [google-io, gemini, agent, antigravity, tpu, omni, spark, search, ai-landscape, ai-trends]
sources:
  - youtube: AmR8mr5VreI (Best Partners TV, 2026-05-20)
  - youtube: wYSncx9zLIU (Google I/O 2026 Keynote)
confidence: high
---

# Google I/O 2026 — Agent全景发布

> **核心信号**: AI的下一阶段——从生成内容走向替你行动。Google全栈五层架构+六款Agent级产品同步出击。
> **大会时间**: 2026-05-19
> **来源解读**: Best Partners TV深度解读（27min）

---

## 一、五层全栈架构

Sundar Pichai登台展示的Google AI十年五层图：

| 层级 | 内容 |
|------|------|
| 产品与平台层 | Google搜索、Gemini App、Workspace、Chrome、Android |
| 模型与工具层 | Gemini系列（Omni/3.5 Flash/Spark/Pro）、Antigravity |
| 顶级研究层 | DeepMind前沿研究、世界模型、多模态 |
| 安全层 | SynthID水印、安全容器化、Agent权限控制 |
| AI基础设施层 | TPU 8t/8i（双芯片架构）、JAX+Pathways跨站点训练 |

**打法的关键词**：全栈。能在每一层快速迭代，公司的每一个角落都被AI点亮。

---

## 二、基础设施：第八代TPU

- **TPU 8t**（训练）：原始算力比上一代高~3倍
- **TPU 8i**（推理）：接近每秒1500 token
- **跨站点训练**：基于JAX+Pathways，训练可跨多个数据中心、全球超100万颗TPU——原本几个月的训练压缩到几周
- **Token增长曲线**：Google系产品+API月处理token量——两年前9.7万亿 → 去年I/O 480万亿 → 今天3.2千万亿（一年7倍增长）

---

## 三、模型层：三款新模型

### Gemini Omni
- **定位**：从任何输入生成任何输出——将Gemini智能与Veo、Nano Banana、Genie等生成模型融合
- **关键能力**：对直觉物理的更深掌握（前几代在动能、重力上易翻车，Omni是阶跃式进步）
- **Demo亮点**：用自然语言对话编辑视频——"把这个圆变成黑洞"→画面元素实时变形；"在傍晚散步"→整体氛围/光线/节奏同步改变
- **首发**：Gemini Omni Flash即日可用，Omni Pro即将推出

### Gemini 3.5 Flash
- **强项**：Agent编程（是Gemini 3系列被采用最多一代之后的新迭代）
- **跑分**：全面超越Gemini 3.1 Pro，包括Terminal-Bench 2.1、GDPval-AA、MCP Atlas
- **多模态**：CharXiv Reasoning 84.2%
- **速度**：每秒输出token数量是其他前沿模型的4倍
- **成本**：前沿级能力，定价不到对标前沿模型的一半——日均万亿token的公司，80%负载从其他模型迁到此，**每年省超10亿美元**
- **内部采用**：Google内部开发者每天处理token从3月的5000亿飙升至3万亿，每几周翻一番

### Gemini Spark（消费级Agent）
- **定位**：你的个人AI Agent，24/7在线（跑在Google Cloud专用虚拟机上，笔记本合上依然工作）
- **动力**：Gemini 3.5 + Antigravity Harness
- **当前集成**：Google自家工具（文档、邮箱、日历、聊天）
- **未来**：几周内通过MCP协议接入第三方工具
- **核心demo**：起草邮件（跨文档/邮箱/聊天搜集信息+按个人语气写）→ 组织社区街区派对（自动生成RSVP跟踪表+起草提醒邮件+做PPT+查小区业委会规定）
- **入口扩张**：今夏进Chrome成为Agentic浏览器→今年晚些时候获得手机端专属入口
- **支持Skill上传**：用户可从网上找到喜欢的skill并上传使用

---

## 四、Agent平台：Antigravity 2.0

- **定位**：Agent-First的开发者平台
- **升级内容**：完整CLI体验 + Antigravity SDK + 原生语音支持 + 与Android/Firebase/AI Studio整合
- **桌面应用**：全新独立桌面应用，围绕agent对话/产出/多agent编排组织界面
- **Agent Harness强化**：新增子Agent、hooks、异步任务管理等核心原语
- **里程碑Demo**：93个子Agent并行工作，12小时异步运行，15000+次模型请求，处理26亿token，从零写一个**可运行的操作系统**——最后现场跑通了Doom游戏
  - 全程API额度消耗不到1000美元
  - "Gemini 3.1 Pro上做不到的事"

---

## 五、产品层：Agent进入日常入口

### AI搜索框（Search AI Mode）
- **生成式UI**：用户搜"黑洞怎么影响时空"→ 搜索直接生成可交互的动画模拟器，可拖拽滑块调整参数
  - 后台用Antigravity驱动的Agentic Coding框架（安全容器化环境读写文件执行代码）
  - 今年夏天免费开放
- **长期任务应用**：搜"这周末能做什么"→ 搜索主动问是否生成周末计划 → 自动生成包含天气/路途/孩子兴趣/日历冲突的个性化计划 → 可分享给家人同步日历
- 模型在思考时**实时显示**"正在生成什么代码、判断哪些信息用什么UI组件呈现"

### Universal Cart（通用购物车）
- 跨商家的标准化购物车——基于Google钱包，自动识别信用卡权益，挖隐藏优惠
- 用户可同时在多个商家加购，Universal Cart自动检查兼容性
- 今夏先在美国搜索+Gemini App上线，YouTube和Gmail随后

### Android Halo
- 让手机上看清Agent状态的新交互层

### Google Pics
- Workspace中的全新AI图像创作编辑工具（Nano Banana + 精细控制）
- 理解画面元素关系，可悬停移除/调整尺寸/加文本/翻译
- 所有输出自动打SynthID水印

### Google Flow更新
- Omni进入Flow → 视频换天换地、增加特效、加入新角色
- Agent能**并行做多步操作**

### Stitch
- 语音驱动的UI设计工具，过去一年全球生成超1亿张UI设计

---

## 六、战略信号：AI进入"替你行动"时代

1. **编码是最容易被定价的场景，但编码之外还有大片未被定价的领域**——图片、视频、音频、PPT、邮件、搜索、购物、日程、文档协作
2. **Google有模型+入口+工作流+用户每天在用的产品**，把Gemini推进成一整套执行系统
3. **消费级Agent时刻真的要来了**——Spark是面向所有人的Agent，而不仅是开发者和企业
4. **AGI近在眼前**（Demis开场第一句话："AGI离我们只剩几年了"）
5. **Token Maxing**（Token拉满）是衡量进展的客观指标——3.2千万亿月token背后是产品被广泛使用的信号

---

## 七、对你的价值

- **Harness工程得到Google背书**：Antigravity的Agent Harness框架（子Agent/hooks/异步任务）与Hermes的Harness工程理念高度吻合
- **MCP被Google采纳**：Spark将通过MCP接入第三方工具，MCP协议成为事实标准再获确认
- **成本优势是Agent普及的关键**：3.5 Flash的定价策略证明了前沿模型+低成本才能支撑大规模Agent场景
- **跨入口Agent是方向**：搜索/浏览器/手机主屏，Agent不应只活在单个App里
