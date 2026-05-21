---
source_url: file:///mnt/i/hermes/wiki_dropbox/markdown-manual-v1.0.md
ingested: 2026-05-11
sha256: 628e030b72ecadb4857bb02ead07577a0056e74941a42759dcf5f5966c7eab56
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: Markdown 完全中文手册 v1.0
---

# Markdown 完全中文手册 v1.0

> 来源: markdown-manual-v1.0.md（用户存入 wiki_dropbox）

# Markdown 完全中文手册 v1.0

## 示例驱动 · 从入门到精通

---

> **Markdown 是什么？**
>
> 如果你曾经在 GitHub 上读过 README，在 Obsidian 里记过笔记，或者在 Notion 里写过文档——你已经在用 Markdown 的"方言"了。
>
> 它不是什么高科技，而是一种"写起来像邮件，读起来像书"的轻量级标记语言。2004 年由 John Gruber 和 Aaron Swartz 创造，如今已经成为技术写作、知识管理、文档协作的通用语言——6,779 家公司、1 亿 + GitHub 仓库在使用它。
>
> 这本手册，从零开始带你精通 Markdown。

---

# 第1章 概览与核心理念

## 1.1 Markdown 是什么？一个乐高故事

想象一下你面前有两套积木：

- **Word 文档** = 一套精美但封闭的乐高城堡。你只能在微软的城堡里玩，换个地方就散架。要修改颜色？得点七八下菜单。
- **Markdown 文件** = 一箱朴素的乐高基础砖。每块砖长什么样你一眼就看得清清楚楚。要搭个城堡？写几行符号就够了。要搬家？整个文件往哪搬都行。

Markdown 的核心哲学就一句话：**从你写下第一个字符起，这篇文章就是可读的**。

```
# 我的标题

这是一段**加粗**的文字。
```

上面这段，即使在没有渲染的记事本里打开，你也能一眼看出"# "表示标题，"**加粗**"表示强调。这就是 Markdown 的设计灵魂——**标记符号本身就是表达**。

## 1.2 为什么要学 Markdown？五个理由

### 📦 可移植性
你的笔记不依赖任何特定软件。VS Code 能打开，Typora 能打开，手机备忘录也能打开。十年后你换了个操作系统，这些 .md 文件依然完好无损。

### 🎯 专注写作本身
不用像 Word 那样边写边调字体大小、行距、颜色。Markdown 让你**先写好内容，再决定样式**。内容与样式分离，这是每一个写作者的解放。

### 🧩 生态极其丰富
Markdown 不是孤岛：

| 用途 | 工具 |
|------|------|
| 写博客 | GitHub Pages + Jekyll, Hugo, Next.js + MDX |
| 写书 | Leanpub, GitBook, mdBook |
| 做笔记 | Obsidian, Logseq, Roam |
| 写文档 | Docusaurus, MkDocs, Read the Docs |
| 技术交流 | GitHub Issues, PRs, Discussions |

### 🔗 天然适合版本控制
.md 是纯文本，Git diff 一目了然。团队协作、文章修改记录、学术论文版本管理——天然适合。

### 🤖 AI 时代的通用语
2024-2026 年间，Markdown 更成为 AI 交互的标准格式：
- `llms.txt` 标准让网站为 AI 爬虫提供精炼的 Markdown 内容
- Claude Code 用 `CLAUDE.md` / `AGENTS.md` 定义项目规范
- Cursor 用 `.cursor/rules` 控制 AI 行为
- 几乎所有 LLM 原生输出 Markdown

## 1.3 与其他格式的比较

| 维度 | Markdown | HTML | Word (.docx) | LaTeX | AsciiDoc |
|------|----------|------|-------------|-------|----------|
| 学习曲线 | ★☆☆☆☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| 可读性（纯文本） | ★★★★★ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ | ★★★★☆ |
| 排版能力 | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ |
| 版本控制友好 | ★★★★★ | ★★★★☆ | ★☆☆☆☆ | ★★★★★ | ★★★★★ |
| 跨平台 | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★★ |
| 适合场景 | 文档/笔记/博客 | 网页 | 办公文档 | 学术论文 | 技术文档 |

**一句话总结**：Markdown 是"写"的格式，不是"排"的格式。当你需要快速产出可读内容，又不想被排版工具绑架——选 Markdown。

## 1.4 生态全景图

```
Markdown 生态（简化版）

├── 规范标准
│   ├── CommonMark  ← 基准标准，明确无歧义
│   └── GFM          ← GitHub 扩展，最广泛应用
│
├── 编辑器
│   ├── Typora       ← WYSIWYG，所见即所得
│   ├── VS Code      ← 全能编辑器，插件丰富
│   ├── Obsidian     ← 知识管理，双向链接
│   ├── iA Writer    ← 专注写作
│   └── HackMD       ← 协作文档
│
├── 转换工具
│   ├── Pandoc       ← 万能转换器，30+ 格式
│   └── mdBook       ← 生成电子书/文档站
│
├── 发布平台
│   ├── GitHub       ← README, Wiki, Issues
│   ├── GitBook      ← 技术文档
│   ├── Leanpub      ← 自助出版
│   └── 知乎/掘金     ← 中文技术社区
│
└── AI 时代
    ├── llms.txt     ← 为 AI 爬虫提供的内容摘要
    ├── CLAUDE.md    ← 定义 AI 行为规范
    └── .cursor/rules← AI 编程助手规则
```

## 1.5 版本与规范：别被"方言"吓到

Markdown 最让人困惑的地方是**它有多种"方言"**。就像同样说中文，北京话和广东话有些词不一样。

但好消息是：**所有方言的 80% 是相同的**。你只要学会 CommonMark（核心标准）和 GFM（GitHub 扩展），就能覆盖 95% 的使用场景。

| 方言 | 特点 | 什么时候用 |
|------|------|-----------|
| **CommonMark** | 纯净标准，无歧义 | 写跨平台内容 |
| **GFM** | CommonMark + 表格/任务列表/代码高亮 | GitHub 相关 |
| **Pandoc** | 80+ 扩展，格式间转换 | 学术写作/格式转换 |
| **Obsidian** | Wiki 链接/Callouts/Mermaid | 个人知识管理 |
| **MDX** | Markdown + React 组件 | 交互式文档/博客 |

---

# 第2章 语法基础（上）：CommonMark 核心

> 这一章教你 Markdown 的"普通话"——学会它，去哪个平台都通用。

## 2.1 标题：文章的骨架

**原理**：用 `#` 的数量表示标题层级，就像文章大纲里的 1、1.1、1.1.1。

**用法**：

```markdown
# 一级标题（相当于 H1）
## 二级标题（H2）
### 三级标题（H3）
#### 四级标题（H4）
##### 五级标题（H5）
###### 六级标题（H6）
```

**最佳实践**：
- 一篇文章只用一个 H1（`#`），通常是标题本身
- H2（`##`）以下的层级可以自由使用
- 不要跳过层级（比如 H2 直接到 H4）

**另一种写法**（Setext 风格，少用但要知道）：

```markdown
一级标题
=======

二级标题
-------
```

> 💡 **为什么要有这种写法？** 因为 Markdown 的灵感来自纯文本邮件，而 ASCII 艺术风格的写标题在邮件正文中很常见。

## 2.2 段落与换行

**段落**：用空行分隔。连续的两段文字之间，空一行。

```markdown
这是第一段文字。它和下面的段落之间有一个空行。

这是第二段文字。
```

**换行**：在行尾加**两个空格**再回车。这是 Markdown 最容易被忽略的细节。

```markdown
这是第一行（行尾有两个空格）··
这是第二行，和上一行在同一段落内。
```

> ⚠️ **常见误区**：很多人以为直接回车就是换行，实际上回车只是"软换行"，渲染后两个回车之间的内容会在同一个段落里。如果要开始新段落，必须用空行。

## 2.3 强调：给文字加点"表情"

**斜体**：用 `*` 或 `_` 包裹

```markdown
这是*斜体*，这也是_斜体_。
```

**粗体**：用 `**` 或 `__` 包裹

```markdown
这是**粗体**，这也是__粗体__。
```

**粗斜体**：用 `***` 或 `___` 包裹

```markdown
这是***粗斜体***。
```

> 💡 **为什么有两种写法？** `*` 更常见，因为 `_` 在单词内部会被当成下划线（比如 `_file_name_` 会被渲染成斜体）。建议统一用 `*`。

## 2.4 列表：组织信息的骨架

### 无序列表

用 `-`、`*` 或 `+` 开头：

```markdown
- 苹果
- 香蕉
- 樱桃
```

渲染效果：
- 苹果
- 香蕉
- 樱桃

### 有序列表

用数字加点号：

```markdown
1. 第一步：打开冰箱
2. 第二步：把大象放进去
3. 第三步：关上冰箱门
```

渲染效果：
1. 第一步：打开冰箱
2. 第二步：把大象放进去
3. 第三步：关上冰箱门

**数字不需要递增**——下面这样也能得到同样的效果：

```markdown
1. 第一步
1. 第二步
1. 第三步
```

> 实用技巧：写文档时所有有序列表项都用 `1.`，这样增加条目时不用重新编号。

### 嵌套列表

缩进 2 空格或 4 空格：

```markdown
- 水果
  - 热带水果
    - 芒果
    - 菠萝
  - 温带水果
    - 苹果
    - 梨
- 蔬菜
  1. 叶菜类
  2. 根茎类
```

### 列表中的段落和代码

列表项内放多个段落：在段落前缩进 4 空格或 1 个制表符。

```markdown
- 这是一个列表项。

  这是同一个列表项内的第二段（前面缩进 4 空格）。

- 这是另一个列表项。
```

## 2.5 链接：连接世界的锚点

Markdown 支持三种链接，各有各的用处。

### 行内式链接（最常用）

```markdown
[百度](https://www.baidu.com)
[点击这里](https://example.com "鼠标悬停时显示的标题")
```

### 参考式链接（提高可读性）

适合同一链接在文中多次出现：

```markdown
我推荐 [Google][google] 作为搜索引擎，但 [Bing][bing] 也不错。

[google]: https://www.google.com "谷歌"
[bing]: https://www.bing.com "必应"
```

> **什么时候用参考式？** 写长文时，把链接统一放在文末，正文保持干净。比如技术文档中引用多个来源时特别有用。

### 自动链接（最简单的 URL）

```markdown
<https://www.example.com>
<email@example.com>
```

## 2.6 图片

```markdown
![替代文本](图片URL)
![替代文本](图片URL "图片标题")
```

> ⚠️ **注意**：图片没有"调整大小"的语法。要调整图片尺寸，得用 HTML：`<img src="url" width="400">`。

## 2.7 代码：写程序员的语言

### 行内代码

用反引号 `` ` `` 包裹：

```markdown
在终端输入 `ls -la` 查看文件列表。
```

### 代码块

**缩进风格**（Markdown 原生，现在少用）：

```markdown
    // 缩进 4 空格或 1 个制表符
    def hello():
        print("Hello")
```

**围栏代码块**（CommonMark 引入，推荐）：

```markdown
```
// 两个换行符中间的代码
def hello():
    print("Hello")
```
```

> 💡 **对比**：缩进风格在嵌套列表中容易混淆。围栏代码块更清晰，且可以标记语言实现语法高亮。

## 2.8 引用：引经据典

用 `>` 符号：

```markdown
> 这是引用文字。
>
> 这是同一引用中的第二段。
>
> > 这是嵌套引用。
```

**实际应用场景**：引用古诗、引用他人的观点、高亮重要提示。

## 2.9 分隔线

三个或以上的 `-`、`*` 或 `_`：

```markdown
---
***
___
```

用于分隔不同章节、不同话题。常见于博客文章中分隔"阅读更多"之前的摘要和正文。

## 2.10 转义字符

用反斜杠 `\` 让 Markdown 符号按字面显示：

```markdown
\*这不是斜体\*
\# 这不是标题
```

常用转义场景：

| 原文 | 转义后显示 | 说明 |
|------|-----------|------|
| `\*literal\*` | \*literal\* | 显示星号本身 |
| `\\` | \ | 显示反斜杠本身 |
| `\` | ` | 显示反引号 |
| `\[` | \[ | 显示方括号 |

---

# 第3章 语法基础（下）：GFM 扩展

> GFM（GitHub Flavored Markdown）是 CommonMark 的超集，增加了日常写作用到最多的几个扩展。学会这章，你在 GitHub、GitLab、Gitee 上写 README、Issues、Wiki 都没问题了。

## 3.1 表格

GFM 的表格语法简洁但强大：

```markdown
| 姓名 | 年龄 | 职业 |
|------|:----:|:---:|
| 张三 | 28 | 工程师 |
| 李四 | 35 | 设计师 |
| 王五 | 42 | 教师 |
```

**对齐方式**：

| 写法 | 对齐效果 |
|------|---------|
| `:---` | 左对齐（默认） |
| `:---:` | 居中 |
| `---:` | 右对齐 |

> **实际场景**：做项目对比、列出工具清单、展示数据。相比 markdown 表格的简单语法，Pandoc 还有更高级的网格表格（grid table），但 GFM 的管道表格（pipe table）最常用。

## 3.2 任务列表

```markdown
- [x] 已完成的任务
- [ ] 未完成的任务
- [ ] 另一个待办事项
```

**实际场景**：GitHub Issue 中的进度追踪、个人待办清单、项目 Roadmap。

> ⚠️ **注意**：方括号内的空格必须是 `[ ]`（中间一个空格），不是 `[]`。勾选 `[x]` 时用小写 x。

## 3.3 删除线

```markdown
~~这行文字被删除了~~
```

**实际场景**：更新日志中标记废弃的功能、表达"我说错了"的修正、幽默效果。

## 3.4 自动链接

GFM 会自动将 URL 转换成链接：

```markdown
访问 https://github.com 会自动变成链接
```

不用加 `<` `>` 包围符，这是 GFM 和 CommonMark 的区别。

## 3.5 围栏代码块 + 语法高亮

GFM 突破性地让围栏代码块支持**语言标记**：

```markdown
```python
def greet(name):
    return f"Hello, {name}!"
\```
```

> **支持的编程语言超过 100 种**，包括 JavaScript、Python、Java、Go、Rust、SQL、YAML、JSON 等。GitHub 甚至会为代码块添加文件名提示和复制按钮。

## 3.6 Emoji 快捷写法（GitHub 特有）

```markdown
:smile: :rocket: :heart: :tada:
```

实际应用：在 Issue 评论中快速表达情绪，为 README 增加生动感。

---

# 第4章 编辑器选择与配置

> "工欲善其事，必先利其器。"Markdown 的编辑器选择非常多，从极致简单的纯编辑到功能完备的笔记系统应有尽有。本章帮你找到最适合自己的那一个。

## 4.1 编辑器速览对比

| 编辑器 | 核心体验 | 价格 | 适合人群 | 平台 |
|--------|---------|------|---------|------|
| **Typora** | WYSIWYG，所见即所得 | ¥89（买断） | 写作者、学生 | Win/Mac/Linux |
| **VS Code** | 代码 + 文档一体化 | 免费 | 开发者、技术写作者 | Win/Mac/Linux |
| **Obsidian** | 知识管理 + 双向链接 | 免费（同步收费） | 笔记达人、PKM 爱好者 | Win/Mac/Linux/移动端 |
| **Notion** | All-in-one 协作空间 | 免费/付费 | 团队协作、项目管理 | Web/移动端 |
| **iA Writer** | 极致无干扰写作 | ¥198（买断） | 专业作家 | Win/Mac/iOS/Android |
| **HackMD** | 实时协作 Markdown | 免费/付费 | 团队文档协作 | Web |
| **Mark Text** | 开源 Typora 替代 | 免费 | 任何人 | Win/Mac/Linux |

## 4.2 各编辑器详解

### 🥇 Typora —— 所见即所得的标杆

**一句话**：你在屏幕上看到的样子，就是最终输出的样子。

**安装**（Windows）：
1. 访问 typora.io 下载安装包
2. 安装后选择一个主题（GitHub、Newsprint、Night 等）
3. 设置 → 通用 → 选择"显示源码模式"快捷键（Ctrl+/）

**适合**：写博客、做笔记、不喜欢看"纯代码"符号的写作者。

**实用配置**：
- 开启"行号显示"——写长文时方便定位
- 图片设置 → 复制图片到 ./assets 文件夹——这样移动 .md 文件时图片不会丢失

### 🥇 VS Code —— 开发者的万能编辑器

**一句话**：如果 Typora 是傻瓜相机，VS Code 就是单反——功能强大但需要一些配置。

**安装**（Windows）：
1. 下载 VS Code（code.visualstudio.com）
2. 安装推荐扩展：
   - **Markdown Preview Enhanced** — 实时预览 + 导出 PDF/HTML/PPT
   - **Markdown All in One** — 快捷键、自动格式化、目录生成
   - **markdownlint** — 语法检查，避免格式错误
3. 快捷键：`Ctrl+Shift+V` 打开侧边预览，`Ctrl+K V` 打开独立预览窗口

**适合**：程序员、需要同时写代码和文档的人、需要高级格式化的人。

### 🥇 Obsidian —— 知识管理的终极武器

**一句话**：不仅是编辑器，更是你的"第二大脑"。

**安装**：obsidian.md 下载，打开后选择"创建新库"——直接选择已有的 .md 文件夹。

**核心特性**：
- `[[双向链接]]` — 像维基百科一样链接笔记
- `![[嵌入]]` — 在一个笔记中嵌入另一个笔记的内容
- 图谱视图（Graph View）— 可视化你的知识连接

**适合**：长期记笔记的人、构建个人知识库的人、钻研某个领域的研究者。

## 4.3 我的第一套配置建议

如果你是**零基础新手**，推荐这个最小配置：

1. **安装 Typora**（免费试用期足够你学会基础用法）
2. **新建文件夹** `D:\notes` 存放所有 .md 文件
3. **每天写一点**——从今天开始，用 Markdown 写日记、读书笔记、工作记录

一个月后，如果你觉得 Typora 不够用，再升级到 VS Code 或 Obsidian。

---

# 第5章 实战：从零写出第一个 Markdown 文档

> 理论学完了，现在动手。本章用一个完整的场景带你走一遍 Markdown 的创作全流程。

## 场景：写一篇技术博客《给女儿讲什么是风》

你是一个技术爸爸，想用 Markdown 写一篇博客，既讲科学原理又带文学趣味。

### 第一步：选择编辑器

打开 **VS Code**（或你喜欢的编辑器），新建文件 `what-is-wind.md`。

### 第二步：写标题和前言

```markdown
# 给女儿讲什么是风

> "爸爸，风是从哪里来的？"
>
> 五岁的女儿站在窗前，看着摇曳的树叶，问出了这个让无数父母头疼的问题。

今天，我用科学和诗意一起回答她。
```

### 第三步：分节展开

```markdown
## 科学小课堂：风是"逃跑"的空气

风不是"来的"，而是**空气在"逃跑"**。

| 谁在热 | 谁在冷 | 结果 |
|:------:|:------:|:----:|
| 地面 | 高空 | 热空气上升 |
| 海边 | 海面 | 白天海风吹上岸 |
| 沙漠 | 绿洲 | 热空气跑向冷空气 |

### 用一句话记住

> **风，就是因为太阳把一处空气加热了，它"待不住"，就跑去找凉快的地方。**

## 诗意小课堂：古人怎么说风？

> "解落三秋叶，能开二月花。过江千尺浪，入竹万竿斜。"
>
> —— 李峤《风》

这首诗的妙处是：**全诗没有一个"风"字，但句句都在写风。**

## 在家做个小实验：造风！

你需要：

- [x] 一个气球
- [ ] 一个电风扇（可选）
- [ ] 一片羽毛或纸屑

### 实验步骤

1. **吹气球**，但不系口
2. **松手！**——气球里的空气"逃跑"了，喷出去的气就是**人造风**
3. 把手放在气球口前 —— ~你感受到了什么？~ 你感受到了气流！

```python
# 模拟风的简单代码（给长大的你）
def wind_speed(pressure_diff):
    """气压差越大，风速越快"""
    if pressure_diff > 100:
        return "台风！关好窗户！"
    elif pressure_diff > 30:
        return "微风，适合放风筝"
    else:
        return "没风，但可以出去走走"
```

## 结语

下次当你站在窗前，女儿问"风从哪里来"时——

```markdown
**科学回答**：太阳能加热空气，冷热空气对流。

**诗意的回答**：风是太阳写给大地的情书，每阵风都是云朵的私语。
```

### 拓展阅读

- [走近科学：风的形成](https://example.com)
- [给孩子的气象学](https://example.com)
```

### 第四步：预览

VS Code 中按 `Ctrl+Shift+V` 查看预览。你会看到：
- 标题层级清晰
- 表格工整
- 代码块有语法高亮
- 引用块突出显示
- 任务列表可勾选

### 第五步：导出

- **导出 HTML**：VS Code 预览区右键 → 复制 HTML
- **导出 PDF**：用 Typora 打开 → 文件 → 导出 → PDF
- **发布到 GitHub**：新建仓库，上传 .md 文件，GitHub 自动渲染

### 实际效果（渲染后预览）

> 这篇博客如果放在 GitHub 上，孩子也能读，程序猿同事也能看，既有技术含量又有人文温度。这就是 Markdown 的魅力——**它让技术写作不那么"技术"。**

---

# 第6章 进阶技术详解

> 基础语法学完了，格现在进入高阶领域。本章覆盖四个方向：多格式转换、学术写作、知识管理、交互式文档。

## 6.1 Pandoc：文档格式的万能转换器

Pandoc 由 John MacFarlane 开发（2006 年），是文档格式转换领域的"瑞士军刀"。**支持 30+ 输入格式、40+ 输出格式**。

### 安装

```bash
# Windows (Chocolatey)
choco install pandoc

# macOS
brew install pandoc

# Linux
sudo apt install pandoc
```

### 核心用法

```bash
# Markdown → HTML
pandoc input.md -o output.html

# Markdown → PDF（需要 LaTeX 引擎）
pandoc input.md -o output.pdf --pdf-engine=xelatex

# Markdown → Word
pandoc input.md -o output.docx

# 多个文件合并
pandoc ch1.md ch2.md ch3.md -o book.html

# 带模板的幻灯片
pandoc slides.md -t revealjs -o slides.html
```

### Pandoc 的 Markdown 扩展

Pandoc 不是"又一个 Markdown 方言"，它让你**自由启停 80+ 扩展**。

**YAML 元数据块**（写在文件最开头）：

```markdown
---
title: "我的论文"
author: "张三"
date: "2026-05-07"
abstract: "这是一篇关于..."
bibliography: references.bib
---
```

**脚注**：

```markdown
这是一句话[^1]。

[^1]: 这是脚注的内容，通常放在页面底部。
```

**数学公式**（使用 LaTeX 语法）：

```markdown
爱因斯坦的质能方程：$E = mc^2$

当 $\alpha > \beta$ 时，我们得到...

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

**定义列表**：

```markdown
Markdown
:   一种轻量级标记语言，由 John Gruber 创造。

Pandoc
:   一个文档格式转换工具，支持 30+ 格式。
```

**Cross-reference**（交叉引用）：

```markdown
参见 [@fig:wind-chart] 中的数据。

![风速随时间变化](chart.png){#fig:wind-chart}
```

### 实际场景

> **学术写作**：先用 Markdown 写论文初稿，再用 Pandoc 导出 Word 或 LaTeX 格式投稿。参考文献用 BibTeX 管理，一键生成引用列表。

> **电子书出版**：写一章一个 .md 文件，用 Pandoc 合并后导出 ePub 或 PDF。Leanpub 平台直接接受 Markdown 格式的书稿。

## 6.2 MDX：Markdown + React 组件

MDX 让 Markdown 有了"生命"。你可以在文章里插入交互式 React 组件：

```mdx
import Chart from './components/Chart'

# 销售数据分析

这是一个交互式图表，鼠标悬停查看详情：

<Chart data={data} type="line" />

```javascript
// 普通代码块（不会渲染成组件）
const data = [1, 2, 3, 4]
\```
```

**适用场景**：
- 技术文档中嵌入交互式示例（代码沙箱、图表）
- 博客文章插入交互式地图或可视化
- 组件库的文档（Storybook、Docusaurus）

**常用框架**：Next.js、Gatsby、Storybook、Docusaurus 都支持 MDX。

## 6.3 Obsidian 高级玩法：个人知识库

Obsidian 把 Markdown 变成了知识管理的终极武器。

### 双向链接

```markdown
在[[读书笔记]]中，我提到了[[认知心理学]]的相关研究。
```

链接后自动生成关系图谱（Graph View），你可以直观看到知识点之间的连接。

### Callouts（高亮块）

```markdown
> [!NOTE] 提示
> 这是普通提示。

> [!WARNING] 警告
> 这是一个注意事项！

> [!TIP] 技巧
> 试试这个高级用法。

> [!IMPORTANT] 重要
> 这是必须记住的内容。
```

### Mermaid 图表（代码块内）

```markdown
\```mermaid
graph TD
    A[开始] --> B{是否下雨？}
    B -->|是| C[带伞]
    B -->|否| D[出门散步]
\```
```

渲染后会生成流程图、时序图、甘特图等。

## 6.4 表格进阶：Pandoc 的四种表格

GMF 的管道表格适合简单数据，但如果表格内容复杂（单元格换行、多行文本），需要更强大的表格语法。

### 网格表格（Grid Tables）

```markdown
+----------+----------+----------+
| 姓名     | 描述     | 备注     |
+==========+==========+==========+
| 张三     | 这是     | 工程师   |
|          | 一段     |          |
|          | 描述     |          |
+----------+----------+----------+
| 李四     | 设计师   | 自由职业 |
+----------+----------+----------+
```

网格表格支持单元格内多行文本、跨行合并（用 `=` 加粗分隔线表示）。

---

# 第7章 社区资源精选

> "学 Markdown 最好的方法，是看别人怎么用。"本章精选国内外最优质的学习资源。

## 📺 B站：新版 Markdown 从入门到精通

| 项目 | 内容 |
|------|------|
| **链接** | https://www.bilibili.com/video/BV1UrLxz5ECw/ |
| **适合人群** | 编程初学者、技术写作者、零基础学生 |
| **内容概览** | 系统完整的 Markdown 教学视频，覆盖历史背景、底层原理、所有基础语法、实际应用场景 |
| **为什么值得看** | B 站最完整的 Markdown 系列教程之一，视频形式直观易懂 |
| **一句话评价** | "B 站最全面的 Markdown 视频教程，编程人员必看" |
| **学到的技能点** | 核心语法、编辑器使用、技术文档规范 |

## 📝 知乎：Markdown 入门教程——从基础到高级的完全指南

| 项目 | 内容 |
|------|------|
| **链接** | https://zhuanlan.zhihu.com/p/1955591233448677534 |
| **适合人群** | 程序员、作家、知识工作者 |
| **内容概览** | 从简介到高级技巧的完整文字指南，涵盖平台差异、写作系统构建 |
| **为什么值得看** | 知乎上结构最完整的 Markdown 教程，文字版便于快速查阅 |
| **一句话评价** | "知乎 Markdown 入门第一选择" |
| **学到的技能点** | 高级技巧、平台特性对比、写作系统 |

## 📚 菜鸟教程：Markdown 教程

| 项目 | 内容 |
|------|------|
| **链接** | https://www.runoob.com/markdown/md-tutorial.html |
| **适合人群** | 零基础中文学习者 |
| **内容概览** | 国内最经典的 Markdown 入门教程，中英文对照，含所有基础语法 |
| **为什么值得看** | 菜鸟教程是国内最权威的技术入门网站之一，配有在线练习环境 |
| **一句话评价** | "中文 Markdown 入门标杆，上手最快的教程" |
| **学到的技能点** | 全部基础语法、HTML 混编、实际写作应用 |

## 📖 Markdown 指南中文站

| 项目 | 内容 |
|------|------|
| **链接** | https://markdown.com.cn/ |
| **适合人群** | 所有 Markdown 用户 |
| **内容概览** | 官方风格的中文参考指南，基本语法、GFM 扩展、速查表、最佳实践 |
| **为什么值得看** | 这是 Markdown Guide 的中文镜像翻译版，质量极高，遵循 CommonMark 规范 |
| **一句话评价** | "最佳 Markdown 中文参考手册，查语法就翻它" |
| **学到的技能点** | CommonMark 规范语法、GFM 扩展、跨平台兼容性 |

## 🔗 ToMarkdown：Markdown 完全指南

| 项目 | 内容 |
|------|------|
| **链接** | https://www.tomarkdown.org/zh/guides/markdown-complete-guide |
| **适合人群** | 所有阶段的学习者 |
| **内容概览** | 综合所有 Markdown 知识点，从基础到高级，含 "30 分钟快速上手" 入门路径 |
| **为什么值得看** | 系统极其完整，含 Typora、VS Code、Obsidian 等主流工具的配置 |
| **一句话评价** | "中文 Markdown 百科级别资源" |
| **学到的技能点** | 全栈 Markdown 技能、多平台适配、工具配置 |

## 💬 Reddit：r/Markdown

| 项目 | 内容 |
|------|------|
| **链接** | https://www.reddit.com/r/Markdown/ |
| **适合人群** | 深入了解 Markdown 社区的进阶用户 |
| **内容概览** | Markdown 社区讨论：编辑器推荐、语法技巧、疑难解答 |
| **为什么值得看** | 社区实时讨论，能学到实用技巧和最新工具 |
| **一句话评价** | "英文社区中探讨 Markdown 的第一聚集地" |
| **学到的技能点** | 社区推荐的编辑器/工具、疑难杂症解决 |

---

# 第8章 业内评价与案例分析

## 8.1 市场数据

- **6,779+ 家公司**在正式使用 Markdown（2024 年数据）
- **1 亿 + GitHub 仓库**使用 Markdown 编写 README
- **Markdown 工具市场规模**：$1.02B（2024 年），预计持续增长
- **Obsidian 用户**：约 300 万+
- **Pandoc 下载量**：在 Haskell 生态中排名前 5 的工具

## 8.2 顶级科技公司的 Markdown 使用

### GitHub：一手推动了 GFM

GitHub 不仅是 Markdown 的最大用户，也是 GFM 规范的制定者。GitHub 上的每个仓库都有 README.md，每个 Issue 和 PR 都支持 Markdown 注释。

**数据**：GitHub 每分钟有数千条 Issue/PR 评论使用 Markdown 格式。

### Microsoft：Visual Studio Code 与 Markdown

VS Code 对 Markdown 的支持是这个编辑器成功的关键因素之一：
- 内置 Markdown 预览
- 丰富的 Markdown 扩展生态
- Docs.microsoft.com 完全用 Markdown 构建

### Anthropic/OpenAI：AI 与 Markdown 的融合

Claude Code 引入 `CLAUDE.md` 和 `AGENTS.md` 文件，让 Markdown 成为定义 AI 行为规范的标准格式。

## 8.3 典型应用案例

### 案例 1：Leanpub 自助出版

**场景**：技术作者想写一本编程书籍。

**流程**：
1. 用 Markdown 写各章（`ch1.md`, `ch2.md`, ...）
2. Push 到 GitHub
3. Leanpub 自动拉取并生成 ePub/PDF 版本

**数据**：Leanpub 上最畅销的技术书籍中，超过 80% 是用 Markdown 写作的。

### 案例 2：GitBook 技术文档

**场景**：公司需要一份 API 文档。

**流程**：
1. 技术写手用 Markdown 写 API 文档
2. GitBook 自动渲染成美观的文档站
3. 与 GitHub 仓库同步，每次提交自动部署

**数据**：超过 50 万组织使用 GitBook 发布文档（2024 年数据）。

### 案例 3：Obsidian 个人知识库

**场景**：研究员构建个人知识体系。

**流程**：
1. 每天用 Obsidian 记录阅读笔记
2. 用 `[[双向链接]]` 连接相关概念
3. 图景可视化知识网络

**数据**：Obsidian 用户平均每周创建 50+ 笔记，使用 200+ 双向链接。

## 8.4 与竞品的对比

| 维度 | Markdown | AsciiDoc | reStructuredText |
|------|----------|----------|-----------------|
| 学习曲线 | ★☆☆ | ★★★ | ★★★ |
| 生态广度 | ★★★★★ | ★★★ | ★★ |
| Python 生态 | 一般 | 一般 | ★★★★★（Python 官方文档） |
| 复杂文档 | ★★ | ★★★★ | ★★★★ |
| 静态网站生成器 | Jekyll/Hugo/Next.js | Antora | Sphinx |
| 书籍出版 | Leanpub/Leanpub | Asciidoctor | Read the Docs |

**一句话总结**：通用场景选 Markdown，Python 文档选 reST，企业级复杂文档选 AsciiDoc。

## 8.5 就业市场信号

- 技术写手岗位中，Markdown 已取代 DITA 成为首要要求
- 软件工程师岗位中，"熟练使用 Markdown" 已成标配要求
- DevRel、PM、DevOps 岗位普遍要求 Markdown 文档能力
- 知识管理相关岗位中，Obsidian/Logseq 经验成为加分项

---

# 第9章 避坑指南

> Markdown 看似简单，但坑不少。本章覆盖最常见的 12 个陷阱，以及如何优雅地绕过它们。

## 坑 1：换行不生效 🚫

**现象**：在 Markdown 里按了回车，预览时两行文字却连在一起。

**原因**：Markdown 的"软换行"要求在行尾加两个空格。

**修复**：

```markdown
// ❌ 错误
第一行
第二行

// ✅ 正确
第一行··（行尾两个空格）
第二行
```

**更简单的方案**：在两个"段落"之间加空行，开始新段落。

## 坑 2：下划线变成了斜体 🚫

**现象**：`some_file_name` 中的下划线被渲染成了斜体。

**原因**：`_` 是斜体的标记符号。

**修复**：用反斜杠转义：

```markdown
// ❌ 错误：some_file_name
some_file_name

// ✅ 正确
some\_file\_name
```

**更好的方案**：用反引号包裹（代码体）：

```markdown
`some_file_name`
```

## 坑 3：列表后的代码块不显示 🚫

**现象**：列表项后跟一个代码块，代码块的缩进不对。

**原因**：列表后的代码块需要额外缩进才能被识别为"属于列表项"。

**修复**：

```markdown
// ✅ 正确
- 这是一个列表项

  ```python
  print("这段代码属于上面的列表项")
  ```

// 注意代码块前面缩进 2 空格（和列表项文字对齐）
```

## 坑 4：数字列表永远从 1 开始 🚫

**现象**：写了 `3. 第一步`，预览始终显示从 1 开始。

**原因**：Markdown 不关心你写的数字是多少。

**修复**：

```markdown
1. 第一步：先完成这件事
1. 第二步：再做那个
1. 第三步：最后收尾
```

> ⚠️ 所有项都用 `1.`，Markdown 会自动递增编号。这是**特性**不是 bug——方便你插入新项时不用整个重编。

## 坑 5：表格中的竖线冲突 🚫

**现象**：表格单元格中要写"国家 A | 国家 B"。

**原因**：`|` 是表格的分隔符。

**修复**：用 HTML 的 `|` 转义：

```markdown
| 国家 | 关系 |
|------|------|
| 中国 &124; 美国 | 贸易伙伴 |
```

或者改用 Pandoc 的网格表格。

## 坑 6：标题内的链接不解析 🚫

**现象**：`## [Google](https://google.com)` 没有变成可点击的链接。

**原因**：CommonMark 规范中标题内的链接是正常解析的，但某些平台不支持。

**修复**：在标题后直接放链接，或者用 HTML：

```markdown
## 参考资源 {#resources}
```

## 坑 7：不同平台渲染不同 🚫

**现象**：在 Typora 里写的美美的表格，贴到 GitHub 上变形了。

**原因**：不同平台的 Markdown 解析器实现有差异。

**修复**：
1. 只用 CommonMark + GFM 语法——这是所有平台的"最大公约数"
2. 避免使用平台专属扩展（如 Obsidian 的 Callouts）
3. 跨平台发布前预览测试

## 坑 8：图片路径问题 🚫

**现象**：在本地能看到图片，上传到 GitHub 就裂了。

**原因**：图片路径使用的是本地绝对路径。

**修复**：

```markdown
// ❌ 错误（本地路径）
![图片](D:\images\photo.png)

// ❌ 错误（相对路径，但图片没提交）
![图片](./images/photo.png)

// ✅ 正确（相对路径，图片在仓库中）
![图片](./images/photo.png)

// ✅ 正确（CDN 图片链接）
![图片](https://cdn.example.com/photo.png)
```

## 坑 9：引用内的代码块 🚫

**现象**：在 `>` 引用内想放代码块，写 `>` 后直接 ```` ``` ```` 不生效。

**原因**：引用内的代码块需要在 `>` 后加一个空格再写代码块符号。

**修复**：

```markdown
> 这是一段引用文字。
>
> ```python
> print("这段代码在引用内")
> ```
```

## 坑 10：HTML 混编的兼容性问题 🚫

**现象**：在 Markdown 中写 `<div>` 标签，渲染效果不如预期。

**原因**：CommonMark 允许内联 HTML，但块级 HTML 需要特殊处理。

**修复**：

```markdown
// 块级 HTML 前后需要有空行
<div class="custom">

内容

</div>
```

**最佳实践**：除非必要，避免在 Markdown 中混编 HTML。如果需要大量 HTML，说明 Markdown 可能不是合适的工具。

## 性能优化：大文件 Markdown 的编辑技巧

当 .md 文件超过几千行时，建议：

1. **分文件管理**：一章一个 .md 文件，用目录索引
2. **使用 VS Code 的大纲视图**：`Ctrl+Shift+O` 按标题导航
3. **图片链接外部化**：小图片用 Base64 embed，大图片用 CDN
4. **关闭实时预览**：大型文件的实时预览会消耗性能
5. **使用 Pandoc 合并**：写作时分开，发布时合并

---

# 第10章 进阶技巧与最佳实践

## 10.1 标题命名的艺术

**好标题** = 清晰的层级 + 简洁的表达 + 利于搜索

```markdown
## 第2章 语法基础（上）：CommonMark 核心语法
```

对比：

```markdown
## 2.1 标题
```

> **原则**：后续你（或别人）搜索时，标题要能独立传达内容含义。

## 10.2 用 Markdown 管理写作项目

**建议的项目结构**：

```
my-book/
├── book.md         # 总体规划 + 目录
├── ch1/            # 第一章的素材
│   ├── ch1.md
│   ├── images/
│   └── notes.md
├── ch2/
│   ├── ch2.md
│   └── images/
├── style.css       # 自定义样式
├── metadata.yaml   # Pandoc 元数据
└── Makefile        # 自动化构建
```

**设置 Makefile (Linux/Mac) 或 batch 脚本 (Windows)**：

```makefile
# 一键编译整本书
all:
	pandoc ch1/ch1.md ch2/ch2.md -o output/book.html --css=style.css

pdf:
	pandoc ch1/ch1.md ch2/ch2.md -o output/book.pdf --pdf-engine=xelatex
```

## 10.3 5 分钟学会：提高效率的快捷键

### VS Code Markdown 快捷键

| 操作 | Windows/Linux | Mac |
|------|--------------|-----|
| 打开预览 | `Ctrl+Shift+V` | `Cmd+Shift+V` |
| 切换粗体 | `Ctrl+B` | `Cmd+B` |
| 切换斜体 | `Ctrl+I` | `Cmd+I` |
| 切换代码块 | Alt+`（反引号） | Option+` |
| 插入表格 | `Alt+Shift+F` | `Option+Shift+F` |

### Typora 快捷键

| 操作 | 快捷键 |
|------|--------|
| 切换标题等级 | `Ctrl+1` ~ `Ctrl+6` |
| 插入表格 | `Ctrl+T` |
| 代码块 | `Ctrl+Shift+K` |
| 引用 | `Ctrl+Shift+Q` |
| 切换源码模式 | `Ctrl+/` |

## 10.4 Day1 → Week4 学习路线

| 时间 | 目标 | 方法 |
|------|------|------|
| Day 1 | 理解 Markdown 是什么 | 读完第1章，装一个编辑器 |
| Day 2-3 | 掌握基础语法 | 按照第2-3章，每节练习10分钟 |
| Day 4 | 写出第一个文档 | 按第5章教程写一篇博客 |
| Week 2 | 系统掌握 | 读完全部语法，记笔记 |
| Week 3 | 工具进阶 | 配置 Pandoc，尝试格式转换 |
| Week 4 | 建立工作流 | 用 Obsidian 建立笔记系统，或配置 SSG |

## 10.5 写代码时 Markdown 的最佳搭档

**代码注释中的 Markdown**（别笑，这很有用）：

```python
"""
# 模块文档

这个模块处理**用户认证**功能。

## 主要类

### UserAuthenticator

用于处理用户登录和登出。

## 使用示例

authenticator = UserAuthenticator()
authenticator.login("张三", "密码")
"""
```

**Git commit message 中的 Markdown**：

```bash
git commit -m "feat: 添加用户登录功能

- [x] 实现登录验证
- [x] 添加 JWT token 支持
- [ ] 添加刷新 token 功能（待完成）
- [ ] 添加登录日志

Closes #1234"
```

## 10.6 维护 Markdown 文档的 5 条原则

1. **一致性**：统一用 `-` 做列表符号，不要 `- * +` 混用
2. **简洁性**：一个 .md 文件不超过 1000 行（太长就拆分）
3. **可寻址性**：每个章节的标题要有明确含义，方便搜索
4. **版本管理**：用 Git 管理 .md 文件，每次修改都提交
5. **预览检查**：提交前务必预览，语法错误最影响阅读体验

---

# 第11章 未来展望

> 本章为独立撰写的原创分析，基于当前趋势推测 Markdown 的未来走向。

## 11.1 AI 原生文档格式：Markdown 2.0？

2024-2026 年，一个显著趋势是 Markdown 正在成为 AI 的"原生输入格式"：

- **llms.txt 标准**（2024 年提出）：网站提供一个 `llms.txt` 文件，用结构化 Markdown 告诉 AI 爬虫"哪些内容最重要"。这是网站与 AI 之间的"握手协议"。
- **CLAUDE.md / AGENTS.md**（2025-2026）：在项目根目录放一个 Markdown 文件，定义 AI 的行为边界。看似简单，实则是"人类通过文档教 AI 做事"的范式雏形。
- **Cursor Rules / .cursorrules**：用 Markdown 格式定义 AI 编程助手的行为准则。

**预测**：到 2028 年，Markdown 可能成为"AI 上下文标准格式"——每个 AI 项目（不限于编程）都会有一个 `context.md` 或类似的文件，用标准化的 Markdown 结构告诉 AI："我是谁、我在做什么、你应该怎么做"。

## 11.2 从"标记语言"到"结构化数据格式"

Markdown 正在突破"写文档"的边界，走向结构化数据：

- **Front Matter (YAML + Markdown)**：已经广泛用于静态站点、笔记系统
- **Obsidian Properties**：2024 年引入的元数据系统，让 Markdown 笔记拥有数据库字段
- **Markdown + JSON**：AI 工具开始用 Markdown 格式输出结构化数据（JSON in md）

**预测**：未来 3-5 年，会出现"结构化 Markdown"规范——在标准 Markdown 基础上增加明确的字段定义、类型系统、数据验证层。这将使 Markdown 既保持人类可读，又能被机器程序化处理。

## 11.3 协作实时编辑的进化

当前的 Markdown 协作（HackMD、GitBook）主要依赖云平台。但有两个趋势值得关注：

1. **本地优先 + 同步**：Obsidian Sync 证明了本地 Markdown + 端到端加密同步模式可行
2. **CRDT 冲突解决**：自动合并多人的编辑，类似 Google Docs 的实时协作

**预测**：3 年内会出现支持 CRDT + 本地优先的 Markdown 编辑器，多人实时编辑 Markdown 文档就像编辑 Google Docs 一样自然，同时保留纯文本的控制权。

## 11.4 多媒体与交互性扩展

Markdown 的传统弱项是多媒体和交互性。但前沿探索正在改变这一点：

- **MDX** 已经支持 React 组件嵌入
- **Mermaid** 让图表成为代码块的一部分
- **Structuring**：用 Markdown 编写交互式教程、测验、工作坊

**预测**：未来的 Markdown 标准可能会引入"行为块"（Behavior Blocks）——类似于代码块，但标记不同的交互模式（` ```quiz`、` ```poll`、` ```form`）。

## 11.5 合规与审计

Markdown + Git 已经被一些企业用于合规场景：
- SOC 2 审计要求文档版本可追溯
- ISO 27001 要求变更记录
- 法律文档需要明确的修订历史

**预测**：将出现"可审计 Markdown"标准——在 Markdown 中嵌入数字签名、时间戳、权限控制字段，文档的每一行修改都有审计记录。

## 11.6 中文 Markdown 社区的未来

中文 Markdown 社区有几个值得关注的信号：

1. **知乎、掘金、CSDN 等平台**纷纷支持 Markdown 发布（虽然各有方言差异）
2. **中文技术书籍**越来越多使用 Markdown 写作（从 Leanpub 到出版社内部流转）
3. **Obsidian 中文社区**非常活跃，国产插件和主题不断涌现

**预测**：3-5 年内会出现"中文 Markdown 排版规范"——针对中文排版习惯（段落缩进、引号转换、全角标点）的 Markdown 扩展标准。

## 11.7 市场与商业前景

| 领域 | 当前规模 | 5 年预测 |
|------|---------|---------|
| Markdown 工具市场 | $1.02B | $2.5-3.0B |
| Obsidian 用户 | ~3M | 10-15M |
| AI + Markdown 服务 | 萌芽期 | $500M+ |
| 企业文档即代码 | 早期采用 | 主流 |

> **结论**：Markdown 不会消失，也不会被取代。它的核心价值——**纯文本、可版本控制、人类可读**——在未来 20 年依然是数字内容创作的基石。如同 HTML 是 Web 的基础，Markdown 正在成为"人类与 AI 共同写作"的基础。

---

# 附录：术语表

| 术语 | English | 什么时候用到 |
|------|---------|------------|
| CommonMark | CommonMark | Markdown 的标准化规范，几乎所有现代 Markdown 解析器都遵循 |
| GFM | GitHub Flavored Markdown | 在 GitHub 上写 Issue、PR、README 时使用 |
| YAML Front Matter | YAML Front Matter | 每篇文章开头的元数据（标题、日期、标签），Jekyll/Hugo 必用 |
| 围栏代码块 | Fenced Code Block | Markdown 中写多行代码时用 \`\`\` 包裹 |
| 行内代码 | Inline Code | 在一行文字中标记一小段代码（\`代码\`） |
| 引用式链接 | Reference-style Link | 长篇写作中将链接统一放在文末，正文用 `[文字][引用名]` |
| WYSIWYG | What You See Is What You Get | Typora 的所见即所得编辑模式 |
| Pandoc | Pandoc | 需要在 Markdown、Word、LaTeX、ePub 之间转换格式时 |
| MDX | MDX | 用 React/Next.js 写需要交互组件的技术文档或博客时 |
| Obsidian | Obsidian | 做个人知识管理、记笔记、构建"第二大脑"时 |
| 双向链接 | Bidirectional Link | Obsidian/Logseq 中连接不同笔记，形成知识网络 |
| Callouts | Callouts | Obsidian 或某些主题中做提示/警告/信息区块 |
| Mermaid | Mermaid | 在 Markdown 中画流程图、时序图、甘特图时 |
| 表格对齐 | Table Alignment | GFM 表格中用 `:---` `:---:` `---:` 控制列对齐 |
| 任务列表 | Task List | 待办事项、进度追踪 `- [ ]` `- [x]` |
| 删除线 | Strikethrough | ~~标记废弃或删除的文字~~ |
| 转义 | Escape | 想让 Markdown 符号按字面显示时加 `\` |
| 斜体 | Italic / Emphasis | `*文字*` 或 `_文字_` 表示强调 |
| 粗体 | Bold / Strong | `**文字**` 或 `__文字__` 表示特别强调 |
| 引用 | Blockquote | 引用别人的话、诗文、或做提示区块 |
| 分隔线 | Horizontal Rule | `---` 或 `***` 表示段落之间的分割 |
| 语法高亮 | Syntax Highlighting | 代码块中标记语言让关键字着色显示 |
| 超链接 | Hyperlink / Link | `[文字](URL)` 或 `[文字][引用]` 做链接 |
| 图片嵌入 | Image Embedding | `![alt](URL)` 在文档中插入图片 |
| 脚注 | Footnote | 学术写作、文章末尾加注释 `[^1]` |
| 数学公式 | Math / LaTeX | $E=mc^2$ 用 Pandoc 或 Obsidian 的数学支持 |
| 静态站点生成器 | Static Site Generator (SSG) | Jekyll/Hugo 把 Markdown 渲染成静态网站 |
| 元数据 | Metadata | 文章的标题、日期、作者等结构化信息（YAML 头部） |
| 纯文本 | Plain Text | .md 文件本质是纯文本，任何编辑器都能打开 |
| CRDT | Conflict-free Replicated Data Type | 多人实时协作编辑 Markdown 时用的算法 |
| llms.txt | llms.txt | 网站为 AI 爬虫准备的结构化 Markdown 内容摘要 |
| CLAUDE.md | CLAUDE.md | 项目根目录中定义 AI 行为规范的 Markdown 文件 |
| 文档即代码 | Docs as Code | 像管理代码一样管理文档（Git 版本控制、CI/CD 部署） |
| 内容与样式分离 | Content-Style Separation | 先写好内容结构，样式由渲染器处理——Markdown 的核心哲学 |
| 纯文本邮件 | Plain Text Email | Markdown 的设计灵感来源，干净的无格式文本 |
| AST | Abstract Syntax Tree | Pandoc 先把文档解析成 AST 再输出，所以能任意格式互转 |

---

*本手册自动生成，示例驱动。版本 v1.0 | 2026-05-07*

