---
source_url: https://mp.weixin.qq.com/s/AixAcVKUm7OwdkxDE1ITMw
ingested: 2026-05-14
sha256: eba2e1cc4d39d2d9f3c597874ce04f8765b5c04bb03668910ceb40cfd063a855
title: "Browser Harness：592 行 Python，让 AI 彻底接管你的浏览器，而且它还会自己&quot;进化&quot;"
author: AGI商业新声
source: 微信公众号（AGI商业新声）
content_type: article
---

"你再也不需要亲自用浏览器了。"

这句话写在项目 README 里，听着狂妄，但看完它的实现方式，你会觉得这帮人可能是认真的。

先说一个让人吃惊的细节

大多数 AI 浏览器自动化项目的逻辑是这样的：预先定义好一堆操作函数（点击、输入、滚动、截图……），然后让 LLM 在这些函数里挑选调用。函数不够用？开发者手动加。

Browser Harness 的做法完全不同。

当 Agent 在执行任务时发现 helpers.py 里缺一个函数，比如它需要上传文件，但没有 upload_file() 这个方法，它不会报错，不会停下来请求人工介入。它会自己打开 helpers.py，写一个 upload_file() 函数，然后继续执行任务。

● agent: wants to upload a file
  │
  ● helpers.py → upload_file() missing
  │
  ● agent edits the harness and writes it    helpers.py   192 → 199 lines
  │                                                       + upload_file()
  ✓ file uploaded

工具不够用，就自己造工具。这不是自动化，这是自我进化的自动化。

这个项目叫 Browser Harness，来自 browser-use 团队，目前 4.7k star，400 fork，总共 592 行 Python 代码。

这个项目在做什么

一句话：给 LLM 一根 WebSocket 线直连 Chrome，中间什么都不加。

不用 Selenium，不用 Playwright，不用任何浏览器自动化框架。Browser Harness 直接走 CDP（Chrome DevTools Protocol），通过一个 WebSocket 连接到你正在用的真实浏览器，让 AI Agent 像人一样操作网页：浏览、点击、填表、上传文件、切 tab，什么都能干。

项目的自我定位非常明确："The simplest, thinnest, self-healing harness."

Simplest：总共 592 行代码。
Thinnest：没有框架层、没有预设流程、没有行为限制。
Self-healing：缺什么能力就自己补，运行时动态扩展。

核心架构：四个文件讲完一切

整个项目的运行时代码就四个文件，这在当下动辄成千上万行的 AI Agent 项目里几乎是异类：

run.py（约 36 行） 是入口。它做的事情极简——启动 Python 环境，预加载 helpers，然后把控制权交给 Agent。

helpers.py（约 195 行） 是核心工具库。它提供了 Agent 操作浏览器的基础函数。但关键在于，这个文件不是"写死"的——Agent 在执行过程中可以（并且被鼓励）往里面添加新函数。

admin.py + daemon.py（合计约 361 行） 负责底层通信。daemon 管理 CDP WebSocket 连接和 socket 桥接，admin 处理浏览器引导和初始化。

SKILL.md 是日常使用指南，install.md 是首次安装指南。

就这些。没有配置文件地狱，没有插件系统，没有抽象层套抽象层。

"自愈"机制：为什么这很重要

传统的浏览器自动化最大的痛点是什么？脆弱。

网站改了一个 class name，你的选择器失效了，整条流程挂掉。你需要人工排查、修复、重新部署。Selenium 时代是这样，Playwright 时代本质上还是这样。

Browser Harness 的思路是：与其试图预判所有可能的情况，不如让 Agent 在运行时自己解决遇到的问题。

这背后的原理并不复杂，现代 LLM（特别是 Claude、GPT-4 这个级别的）已经具备了：阅读网页 DOM 结构的能力、理解 CDP 协议的能力、编写 Python 函数的能力。Browser Harness 做的事情就是把这三者连起来，给 Agent 一个"可以修改自己工具箱"的权限。

当 Agent 遇到一个它没有现成函数处理的场景时，它的行为链是：
识别问题（"我需要上传文件，但没有这个函数"）；理解上下文（读 helpers.py 的现有代码，理解代码风格和 CDP 调用模式）；编写解决方案（在 helpers.py 里新增函数）；继续执行；
这就是为什么它自称 "self-healing"——不是自动修 bug 的那种 self-healing，而是自动补全能力缺口的 self-healing。

Domain Skills：Agent 自己写的"攻略"

Browser Harness 有一个 domain-skills/ 目录，里面按网站分文件夹，存放针对特定网站的操作技能：GitHub、LinkedIn、Amazon 等。

但这里有一个反直觉的设计决策：这些 skill 文件不允许人类手写。

README 里明确说了：

"Skills are written by the harness, not by you. Just run your task with the agent — when it figures something non-obvious out, it files the skill itself. Please don't hand-author skill files; agent-generated ones reflect what actually works in the browser."
每个 skill 文件记录的是 Agent 在实际操作某个网站时摸索出来的选择器、交互流程和边界情况。因为是 Agent 自己在真实浏览器里试出来的，所以它记录的是"实际有效"的操作路径，而不是人类根据文档猜测的"理论上应该有效"的路径。

贡献方式也很有趣。你让 Agent 帮你完成某个网站上的任务，Agent 在过程中会自动生成 skill 文件，你直接把这个文件夹作为 PR 提交就行。

这本质上是一种众包 + AI 协作的知识沉淀方式：无数用户在不同网站上使用 Browser Harness，Agent 在每次任务中学到的"攻略"被提取出来，沉淀成 domain skill，供所有用户复用。

Setup 体验：一句话搞定

安装流程被设计得极其简洁。你在 Claude Code 或 Codex 里粘贴下面的指令：

Set up https://github.com/browser-use/browser-harness for me.Read `install.md` first to install and connect this repo to my real browser. Then read `SKILL.md` for normal usage. Always read `helpers.py` because that is where the functions are. When you open a setup or verification tab, activate it so I can see the active browser tab. After it is installed, open this repository in my browser and, if I am logged in to GitHub, ask me whether you should star it for me as a quick demo that the interaction works — only click the star if I say yes. If I am not logged in, just go to browser-use.com.
Agent 会自己读 install.md，安装依赖，连接到你的真实浏览器。

连接成功后，它还会做一个小 demo：打开这个 GitHub 仓库页面，如果你已经登录了 GitHub，问你要不要帮你点个 star。这个 demo 设计得很聪明：它同时验证了"Agent 能控制浏览器"、"Agent 能读取页面状态"、"Agent 会在操作前征求你同意"三件事。

项目还提供了免费的远程浏览器服务（通过 cloud.browser-use.com），免费档位给 3 个并发浏览器，还带代理和验证码解决。这对需要隐身操作或者部署 Agent 的场景很实用。更有意思的是，它甚至允许 Agent 自己去注册这个远程浏览器服务的 API key，通过读取 docs.browser-use.com/llms.txt 完成注册流程。

它跟 browser-use 主项目是什么关系

browser-use 组织下有两个主要项目。主项目 browser-use/browser-use 是一个更完整的 AI 浏览器 Agent 框架，抽象层更厚，功能更全。

Browser Harness 走的是完全相反的方向：极简、直连、不设限。它更像是一个给"高级玩家"的底层工具，适合那些不想要框架约束、希望 Agent 有最大自由度的场景。

如果做个类比：browser-use 像是 Django，全功能框架，开箱即用；browser-harness 像是 Flask 的极端精简版——只给你最基础的管道，其他全靠你（或者说你的 Agent）自己搭建。

这个设计哲学的深层含义

项目 README 末尾有两个链接，一个叫 "Bitter Lesson"，一个叫 "Skills"。

"Bitter Lesson" 几乎可以确定是在引用 Richard Sutton 2019 年那篇著名的文章《The Bitter Lesson》。Sutton 的核心观点是：AI 研究历史反复证明，依靠人类知识做手工工程的方法最终都会输给利用大规模算力进行通用学习的方法。

Browser Harness 的设计显然受到了这个理念的影响。它不试图预先定义所有可能的浏览器操作（那是"手工工程"），而是给 Agent 最大的自由度，让它在任务中自己学习和扩展能力（那是"通用学习"）。592 行代码不是偷懒，是刻意的设计选择：代码越少，Agent 的自由度越大。

这也解释了为什么它要求 domain skill 必须由 Agent 生成而非人工编写，人类写的"攻略"是基于理解和猜测的，Agent 写的"攻略"是基于实际交互验证的。

实际使用场景

从 domain-skills/ 目录和项目描述来看，Browser Harness 的目标场景包括但不限于：

日常自动化：LinkedIn 社交拓展、Amazon 下单、报销填表这类重复性网页操作。与传统 RPA 不同的是，它不需要提前录制流程，Agent 自己探索完成。

子 Agent 任务分发：在更大的 Agent 系统中，Browser Harness 可以作为一个"浏览器子 Agent"被调用，专门处理需要真实浏览器交互的环节。

隐身与规避场景：通过远程浏览器服务的代理和验证码解决能力，可以处理一些对自动化检测比较严格的网站。

风险与局限

安全边界。让 AI 直连你的真实浏览器，操作你登录过的所有网站——这件事的安全含义不需要我展开说。项目确实有一个"勾选复选框确认授权"的步骤，但一旦授权，Agent 的操作边界基本上是无限的。你的银行网站、邮箱、社交账号，全都在 Agent 的触及范围内。

可控性。没有框架、没有 guardrail 意味着 Agent 理论上可以做任何事。592 行代码的极简设计是一把双刃剑：给了 Agent 最大自由度的同时，也意味着出错时几乎没有安全网。

稳定性。项目目前 0 个正式 release，38 个 open PR，状态明显还在快速迭代中。对于生产环境使用需要谨慎评估。

CDP 依赖。直接走 Chrome DevTools Protocol 意味着它只能控制 Chromium 内核的浏览器。Firefox、Safari 用户不在服务范围内。

社区与项目状态

截至目前：4.6k star，400 fork，144 commits，14 watchers，12 open issues，38 open PRs，0 个正式 release。

38 个 open PR 是一个值得注意的数字——对于一个 400 fork 的项目来说，说明社区贡献热情不低，但项目维护者的合并速度还跟不上。这在快速增长的开源项目中很常见，但如果长期不解决会影响社区活跃度。

项目语言 100% Python，MIT 协议，配套了 .env.example 和 pyproject.toml，打包规范比较标准。

与同类项目的对比

对比 Playwright + AI wrapper 方案（如 LaVague、Agent-E 等）：这些方案本质上还是在自动化框架之上包一层 AI 决策。Browser Harness 砍掉了自动化框架这一层，直连 CDP。更薄，但也更"野"。

对比 browser-use 主项目：主项目更适合想要开箱即用的用户，Browser Harness 更适合想要极致控制和最大灵活度的用户。两者是互补关系。

对比 Computer Use / Screen-based Agent（如 Anthropic 的 Computer Use、Open Interpreter 等）：这些方案通过屏幕截图 + 视觉理解来操作电脑。Browser Harness 走的是结构化的 CDP 路线，精度更高、速度更快，但仅限浏览器场景。

结语

Browser Harness 做了一个大胆的赌注：与其给 AI 一套精心设计的工具，不如给它一根直连浏览器的线，让它自己造工具。

592 行代码，没有框架，没有抽象层，没有预设流程。Agent 缺什么能力就自己写，遇到新网站就自己摸索出攻略。这在今天的 AI Agent 生态里是一种相当极端的设计选择。

它可能不适合所有人。如果你需要可预测、可审计、有明确安全边界的浏览器自动化，传统框架或者 browser-use 主项目更合适。但如果你想体验"让 AI 真正自由地使用浏览器"是什么感觉，Browser Harness 可能是目前最纯粹的一个实现。

用项目自己的话说："You will never use the browser again."

至于这到底是一句宣传语还是一个预言，取决于你对 AI 能力边界的判断。

项目地址：https://github.com/browser-use/browser-harness
