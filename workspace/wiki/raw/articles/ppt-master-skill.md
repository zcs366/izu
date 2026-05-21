---
title: PPT Master Skill：一个真正可编辑的AI PPT生成Skill
source_url: https://mp.weixin.qq.com/s/-SN8HExLSA3sbRHvLo9ByA
author: colagold
ingested: 2026-05-21
sha256: fd80495520f09375ab479e1f6d93cb05b9718dfd1e165b3b73a6fd5744656755
content_type: wechat-article
category: AI工具/Skill
---

PPT Master短时间内拿下大量 GitHub Star，并持续登上 AI 开源趋势榜。截至发稿时间已经有14.7k star

PPT Master的核心理念非常直接：

AI 生成的 PPT，必须是真正可编辑的 PowerPoint。

不是网页截图。
不是导出的图片。
不是只能在线看的 HTML Deck。

而是：
能在 PowerPoint 中直接打开每个元素都可以点击编辑支持真实文本框、图表、动画支持母版与模板复用支持旁白、视频导出完整 .pptx
这个方向，其实和目前很多 AI PPT 产品完全不同。

项目信息

PPT Master GitHub 仓库: https://github.com/hugohe3/ppt-master?utm_source=chatgpt.com

PPT Master Demo:https://hugohe3.github.io/ppt-master/
PPT Master一、为什么 PPT Master 会火？
目前 AI PPT 工具大概有四类：
类型输出形式可编辑性模板填充型基于固定模板生成有限编辑图片型每页是一张图基本不可编辑HTML 演示型Web Slide不是真 PPT原生 PPT 型真正的 DrawingML完全可编辑
PPT Master 属于最后一种。这也是它最核心的价值。很多 AI PPT 产品看起来很“精美”，但本质上：
修改标题会错位不能改单个元素图表不是图表动画是假动画导出后无法继续协作
而 PPT Master 的目标，是让 AI 生成结果真正进入企业 PPT 工作流。
二、PPT Master 到底是什么？
它并不是一个 SaaS 网站。 而是一个：

基于 AI Agent 的 PPT 工作流系统skill

官方描述非常准确：
你在 Claude Code / Cursor / VSCode Copilot 中与 AI 对话AI 自动读取文档分析结构规划页面最终输出真实 PPTX
整个过程都运行在本地。

这意味着：
不依赖云端 PPT 平台数据不上传第三方服务器不绑定某家 AI 厂商可以接入 Claude / GPT / Gemini 等模型
这一点其实非常重要。 因为企业里最敏感的，往往就是：
财报商业计划书投融资材料内部战略文档
很多公司不可能允许上传到在线 PPT SaaS。 而 PPT Master 的 Local-first 设计，天然适合企业场景。
三、它最强的能力：真正生成原生 PPT 元素
这是整个项目最“硬核”的地方。 官方明确强调：

Every shape, text box, and chart is clickable and editable in PowerPoint. (GitHub[1])

也就是说：

AI 不是在“截图”。 而是在真正构建：
ShapeTextBoxChartLayoutTransitionAnimation
底层其实是直接操作 OOXML / DrawingML。

这一点非常像：

“PowerPoint 编译器”

而不是传统的：

“PPT 图片生成器”

效果展示
Magazine— warm earthy tones, photo-rich layoutAcademic — structured research format, data-drivenNature Documentary — immersive photography, minimal UI四、模板复刻能力，非常惊艳
这是我认为整个项目最有价值的能力之一。

PPT Master 支持：

直接读取任意 .pptx，提取模板结构。

包括：
字体配色母版Layout图形关系Sprite Crop页面结构
然后： AI 后续生成的新 PPT，可以直接套用这个模板。 这意味着：

你可以：
复刻公司品牌模板复刻客户模板复刻咨询公司风格复刻高质量商业 Deck
这比“固定模板生成”高级太多。
五、支持真正的 PPT 动画
很多 AI PPT 产品的动画，本质是：

GIF

视频

Web 动效

但 PPT Master 直接输出：

Page Transition

Entrance Animation

而且是原生 PowerPoint 动画。

这意味着：

PowerPoint 可以直接播放

Keynote 也兼容

不需要第三方播放器

这一点在演讲场景里非常重要。
六、支持 AI 配音与视频导出
这是它另一个很有意思的能力。

流程大概是：

AI 生成 PPT

从 Speaker Notes 读取讲稿

TTS 生成配音

将音频嵌入 PPT

PowerPoint 直接导出 MP4

甚至支持：

ElevenLabs

MiniMax

CosyVoice

Qwen TTS

还能做 Voice Cloning。

这意味着：

未来 AI 不只是生成 PPT。

而是：

直接生成完整“演讲视频”。
八、PPT Master 的技术架构，其实很像 Agent Workflow
这个项目最值得学习的地方，不只是 PPT。

而是它体现了一种：
unsetunsetAI Agent Workflow 的新想法unsetunset
整个流程本质是：

文档输入
   ↓
内容分析
   ↓
页面规划
   ↓
设计系统生成
   ↓
SVG布局
   ↓
OOXML转换
   ↓
PPTX导出

这已经不是单纯的：

Prompt → Output

而是：

多阶段 AI Pipeline

非常像：

DeepResearch

Manus

Devin

Claude Code Skill

这种 Agent Runtime。
九、为什么这个方向很重要？
因为 AI PPT 过去一直有个根本问题：

“生成”和“编辑”是断裂的。

传统 AI PPT：

生成很快

但无法进入真实工作流

而真正的商业 PPT：

一定需要多人协作

一定需要反复修改

一定需要母版与规范

一定需要最终人工调整

所以：

真正的 AI PPT，不是“自动生成最终结果”。

而是：

AI 生成一个可以继续工作的 PPT。

这才是企业真正需要的。
十、安装与使用
项目本身非常简单。

只需要：

git clone https://github.com/hugohe3/ppt-master.git

cd ppt-master

pip install -r requirements.txt

然后：

在 Claude Code / Cursor 中：

请根据 report.pdf 生成一份融资路演 PPT

AI 就会开始完整生成流程。
