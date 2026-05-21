---
source_url: https://mp.weixin.qq.com/s/qzevOsuhez1Q0T9Ae2B_Kw
ingested: 2026-05-14
sha256: ed2b368930149335
title: 强烈推荐！这个 Skill 画架构图质量超高，一句话出图
author: 五月君
source: 微信公众号
note: 用户已内置此 Skill（architecture-diagram，Cocoon AI 出品），无需额外安装
---

做技术这行，总有些事是真心懒得做的，画架构图算一个。

不是不重要，是太麻烦。要么打开 draw.io 从头拖组件，要么用 Mermaid 写一堆语法还要反复调位置，最后搞出来的效果差强人意，发给别人一看，"就这？"。更多时候干脆跳过这一步，直接在文档里写"架构如下图所示"，然后图是空白的。

最近发现一个 Skill 把这件事解决了，效果出乎意料地好，顺手写篇文章给大家也安利一下。

先看效果——这是我用它帮 Skills Hub 项目生成的架构图：

整体是深色主题，组件按前端、后端、数据库、外部服务分颜色标注，层级关系清晰，连接箭头干净，底部还有三栏信息卡片做补充说明。最重要的是，它输出的是一个独立的 HTML 文件，浏览器直接打开，不依赖任何第三方工具。

用的字体是 JetBrains Mono，整体风格偏工程审美，比那种糖果色的 UI 图要耐看。

顺手又让它画了一张微服务架构图，用的提示词是"微服务应用的典型架构是什么？"，不到 1 分钟出图：

图里涵盖了接入层、安全层、治理层、业务层、数据层、消息层、下游服务、基础设施完整的八个层次，Kafka/RabbitMQ 消息总线、Service Mesh（Istio/Envoy）、每个微服务独享数据库，该有的细节全在。这张图一字没改，就是给了一句话，直接生成的。

这个 Skill 叫 architecture-diagram，由 Cocoon AI 开发（MIT 开源）。核心亮点：
- 一句话描述架构，自动出深色主题 SVG 架构图
- 输出独立 HTML 文件，浏览器直接打开，不依赖任何工具
- 颜色语义化：前端=青色、后端=绿色、数据库=紫色、云服务=琥珀色、安全=玫红
- 字体 JetBrains Mono，暗色网格背景（slate-950）

使用方式：直接描述系统架构，AI 自动生成 HTML。几轮对话就能调整到位。

其他场景：也可以直接描述一个架构，比如 "Create an architecture diagram for: React frontend + Node.js/Express API + PostgreSQL database + Redis cache + JWT authentication"，或者让它画一个"典型的 SaaS 架构"当模板，再按需修改。

Skill 地址：https://github.com/Cocoon-AI/architecture-diagram-generator
