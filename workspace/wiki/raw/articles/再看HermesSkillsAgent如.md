---
source_url: https://mp.weixin.qq.com/s/a9-UIXS8nHVxhDue4RFN8Q
ingested: 2026-05-21
sha256: e0e8c8499c51ed53
title: 再看Hermes Skills：Agent 如何自我进化？
author: 若飞
source: 微信公众号
level: standard
---

架构师（JiaGouX）我们都是架构师！
架构未来，你来不来？

这段时间，Hermes Agent 被讨论得很多。

热闹的部分不重复了。让我停下来的，还是之前一直在想的那个问题：Agent 做完一件复杂事情以后，系统到底留下了什么？

只留下聊天记录，下次还是要翻历史。只留下几条 Memory，大概能记住"你是谁""项目在哪里"。但如果它能留下一个可复用、可验证、可修订的做事方法，后面用起来会很不一样。

我现在越来越觉得：Agent 的下一轮差距，不会只落在更长上下文和更强模型上，还会落在它有没有一层可维护的过程资产。

Hermes 在这件事上做得比大多数开源 Agent 彻底。这篇不打算做源码导读，更想借着它聊一个更大的问题——团队经验怎样被写进系统。
太长不看版• Memory、Session Search、Skill 得分开看。 事实记忆回答"环境和偏好是什么"，会话检索回答"过去聊过什么"，Skill 回答的是"这类事以后怎么做"。• Hermes 吸引我的不只是"会自动写 Skill"。 更关键的是它把过程资产放进了运行时主路径：创建、加载、使用、修补、安全扫描，一整套都系统化了。• 这条线和前面写过的 Claude Skills、Codex AGENTS.md、OpenClaw 是同一类问题。 都在把隐性经验外部化，让人和 Agent 都能复用。• 自动沉淀经验很诱人，也很危险。 没有评估、版本、权限和回滚，自动生成的 Skill 很容易把一次误判固化成长期默认动作。• 更稳的方式是先从高频流程、验证流程、排障流程开始。 先让经验变小、变准、可检查，再谈自我进化。Agent 长期资产分层先把"记忆"拆开
很多 Agent 讨论会卡在一个词上：Memory。

用户偏好叫 Memory，项目路径叫 Memory，上次失败的日志也叫 Memory。再往外扩，部署步骤、排障经验、PR review 清单，好像都能叫 Memory。

词一宽，系统边界就糊了。

之前写 Hermes 三层学习机制那篇就提过这件事，再拎出来讲一遍，因为实在太容易混。
层次保存什么更适合的形态事实记忆用户偏好、项目约定、环境事实小型 memory 文件或用户画像会话检索历史对话、任务记录、上下文线索SQLite / FTS / 向量检索过程资产流程、坑点、验证、工具组合Skill、Runbook、Checklist
拿"发一个 Next.js 服务"举例。

Memory 记的是"仓库在哪、默认分支是什么、团队用 pnpm、线上在 Vercel"。Session Search 找的是"上次这个项目发布时踩过什么坑"。Skill 留下的是"以后这类发布该怎么做：先检查环境变量，再跑构建，再 smoke test，最后看日志回执"。

这三层都像记忆，但其实不是一回事。

Hermes 的内置 memory 由 MEMORY.md 和 USER.md 两个文件组成，容量是刻意收紧的：MEMORY.md 约 2,200 字符，USER.md 约 1,375 字符。会话开始时作为 frozen snapshot 注入系统提示，中途更新会落盘，但不会改当前会话的 system prompt。

之前聊过这个设计，现在再看还是觉得克制。它不是不能更新记忆，而是刻意不在会话中途重建 system prompt。背后不是偷懒，是很现实的成本判断——高变化的信息不该放进一个需要长期命中缓存的骨架里。之前聊 prompt caching 时算过这笔账：Claude Code 92% 缓存命中率靠的就是"稳定前缀不乱动"。Hermes 在 memory 这层做了一样的取舍。

历史会话交给 state.db 和 FTS5 检索。需要找"上次怎么处理的"，用 session_search 召回就行，不用每次都把历史塞进模型。之前我把它比作档案室，这个比方现在还管用：档案室很重要，但你不会把每个柜子都背在身上。

Skill 再往前一步。

它不只回答"上次发生了什么"，还会把成功路径整理成"这类事情以后怎么做"。这就是我说的过程资产。
Hermes 把过程资产放到了运行时
Hermes GitHub README 对自己定位很直接：self-improving AI agent。

之前把它和 OpenClaw 摆在一起看过。简单说，OpenClaw 更偏入口和调度——消息怎么进来、会话怎么路由；Hermes 更偏执行和学习引擎——工具怎么用、经验怎么沉淀。

这次不重复那个对比，更想看的是 Hermes 在 Skills 这层到底做到了什么程度。

官方 Skills 文档把 Skill 定义成按需加载的知识文档，走 progressive disclosure。大意是：
• Level 0：先看 skills_list()，只拿名称、描述、分类；• Level 1：相关时用 skill_view(name) 加载完整内容；• Level 2：需要细节时再加载某个支撑文件。
这个设计和 Anthropic Skills 的方向是一致的——Skill 不适合写成一段巨大的提示词，更适合做成一组可按需进入上下文的工作单元。

Hermes 更进一步的地方是 Agent 可以自己创建、修补、编辑、删除 Skill。复杂任务成功完成、走过错误和死胡同、用户纠正了做法、发现非平凡工作流，都可能触发 Agent 创建 Skill。

这就把 Skill 从"人写给 Agent 的资料"，推成了"Agent 参与维护的过程资产"。

这里说准确一点。

"5 次工具调用后自动写 Skill"这种说法方便传播，但容易压扁细节。之前翻过源码，run_agent.py 里的实现更像一套 best-effort review：主任务先完成，后台再判断有没有东西值得保存。不是硬编码"满了就一定写"。

不是每个复杂任务都值得写 Runbook，也不是每次修 bug 都要形成流程。难点在于分辨：这次经验以后还会不会复用，保存下来会不会反过来误导下一次。
让我觉得它在认真做这件事的几个细节
说"过程资产"谁都会说。真让我觉得 Hermes 不是在喊口号的，是几个很像线上系统的工程细节。

第一，Skill 创建有落盘纪律。

它不是把内容拼出来就 write() 完事。实际是先写临时文件，再用 os.replace() 原子替换。进程中途崩了，磁盘上留下的要么是旧版本，要么是新版本，不会是半截文件。扫描顺序也有讲究：先落盘、再扫描最终文件系统状态，失败就整目录回滚。这是在躲 TOCTOU（检查和使用之间的竞态），做过后端系统的应该很熟悉。

到这里 Skill 才更像一个可维护资产，而不是模型吐出来的一段 Markdown。

第二，Skill 内容走 User Message 注入，不碰 System Prompt。

这个取舍值得多说两句。Hermes 加载 Skill 后，不是把内容追加到 System Prompt 里，而是作为一条带 [SYSTEM: ...] 前缀的 User Message 塞进对话。

为什么？因为一碰 System Prompt，Prompt Cache 就碎了。

之前聊 prompt caching 时算过这笔账：一个 30 轮工具调用的复杂任务，不碰 System Prompt 能省下 95% 以上的重复 token 成本。User Message 的指令跟随权重确实比 System Prompt 低一些，但这是一个算过账的取舍——牺牲一点指令遵循的可靠性，换来数十倍的成本降幅。

换句话说，Hermes 做的不是"把 Skill 塞进去"，而是把高变化的过程知识从需要稳定缓存的系统骨架里拆出去。

第三，patch 靠 fuzzy match，承认 LLM 记不准空格。

Hermes patch Skill 的做法我还挺喜欢的。它没假设模型能一字不差地引用旧内容，而是复用了 fuzzy match 去做替换——空格、缩进、换行、转义这些小差异尽量容忍。

这类设计不酷，但很工程。因为如果 patch 只接受精确命中，Agent 的自我修补大概率会死在工具调用失败上。说直白点：很多系统的问题不是不会改，而是改不进去。

第四，patch 之后不强改当前会话。

Skill 被 patch 成功后，Hermes 会清理索引缓存和磁盘快照，但效果要到下一个会话才体现——当前会话的 System Prompt 不会被回写。

这是一种最终一致性：当前任务发现问题并修补，下一个任务开始时系统干净地加载新版本。不炫，但很像真实系统的边界感。
这条线上不只有 Hermes
如果只盯 Hermes，容易把它看成一个单点创新。

但过去几个月我们写过的几条线放在一起看，它们回答的其实是同一个问题：经验到底该放在哪里。

之前写 Anthropic 的 Agent Skills 那篇，聊的是团队经验怎么被 Agent 稳定复用。Skill 有用的地方不止 SKILL.md，还有 references、scripts、assets、examples、hooks 这些外围结构。它让模型进入一个整理好的小工作区，不是只读一段提示词。

写 Codex 仓库那篇，方向不太一样。OpenAI 把 AGENTS.md、justfile、CI、schema fixtures、release workflow 放在一起，形成仓库级的默认流程。不是给人看的文档，而是在把团队默认共识写进仓库，让人和 Agent 都沿同一套路径工作。

然后是我们一直在跟的 OpenClaw。之前的结论是：如果 OpenClaw 也把自动 skill 沉淀、触发、复用、修补、安全扫描做成系统主路径，它在 learning loop 这一层会非常接近 Hermes。后面的差异就不是"有没有"，而是"放在运行时的什么位置"。

Hermes 站在第三个位置。它关心的是运行时：Agent 做事过程中遇到的路径、坑点和修正，能不能沉淀成下次可加载、可修补的 Skill。
几条经验外部化路线
所以我更愿意这样看：
• Claude Skills 把团队经验做成工作单元；• Codex 把工程经验写进仓库和流程；• Hermes 把运行时经验沉淀成过程资产。
三者不是互相替代，从不同层面把隐性经验外部化。

所以我不太想把 Hermes 简单归类成"比 OpenClaw 多了自动 Skill"。这个说法能解释一部分，但会漏掉它在运行时经验层上的位置。更底层的变化是：Agent 系统开始有意识地区分事实、历史和做事方法，并把"做事方法"当一等资产管。
自动沉淀不是免费午餐
过程资产一旦能自动生成，就有一个新风险：错误经验也会自动沉淀。

这比"模型当场答错"麻烦得多。

当场答错，影响一次任务。坏 Skill 进入系统，影响的是后面一串同类任务——它会让 Agent 更快、更稳定地走向错误路径。

Hermes 在安全上做了一件对的事：不把防线全交给模型自觉。

它的 guard 里有 90 多类威胁模式，扫的不只是"危险命令"这种大词，还有很具体的东西：通过 curl 拼接环境变量外传凭据、直接引用 ~/.hermes/.env、DAN 之类的越狱短语、零宽字符和 RTL override 这些不可见 Unicode——之前讲 memory 安全扫描时提过类似机制，Skill 这边覆盖面更大。

更关键的是它不是一刀切。built-in、trusted、community、agent-created 用不同安装策略：内置 Skill 完全信任，社区 Skill 只允许最安全级别的操作，Agent 自创建的 Skill 允许中等风险但危险操作会问用户。同样是 Skill，来路不同，不能共用一套信任假设。

NousResearch 的 hermes-agent-self-evolution 仓库走得更远。它用 DSPy + GEPA 去优化 Skill、工具描述、系统提示和代码。流程大概是：读当前 Skill / prompt / tool，生成评估数据，用 GEPA 结合执行轨迹生成候选变体，评估后过约束门禁，最后以 PR 形式进入 hermes-agent。

我更在意的不是"自动优化"四个字。

是后面的约束：测试必须过，Skill 大小受限，不能破坏缓存兼容，语义不能偏离原目标，所有变化走 PR review，不直接提交。

这至少让我放心了一点：他们不是只想让 Skill 长出来，也在认真管它怎么长歪。

自我改进如果没有评估集、版本和审查，很容易把一次"看起来更好"的改动写进系统，然后一路放大。
Skill 进入生产系统，要多几道门
如果今天让我把 Hermes 这套思路借到自己的 Agent 系统里，不会一上来就追求"全自动自我进化"。

我会先把门禁做出来。
Skill 进入生产系统的闭环
第一道门，结构。

每个 Skill 至少要说清楚：什么时候触发、解决什么问题、需要什么工具、步骤是什么、怎么验收、哪些情况不适用。Hermes 要求 frontmatter、大小限制、目录结构，其实就是在给"可被系统消费的经验"定最小契约。没有验证方法的 Skill，不会让它进入自动加载。

第二道门，来源。

内置 Skill、团队 Skill、社区 Skill、Agent 自生成 Skill，不该共用一套信任级别。我会直接把来源做成分级策略，不是写在文档里提醒大家小心。Hermes 对不同来源的安装策略就是这个方向——信任应该在框架层表达，靠人记不靠谱。团队内部也一样：生产发布、数据导出、权限变更的 Skill，不能和"写周报"用一套准入策略。

第三道门，评估。

评估不一定一开始就很重，但至少要有最小样例：这个 Skill 解决哪几个典型任务，成功输出大概长什么样，哪些错误不能再出现，变更前后有没有回放过历史轨迹。Hermes 的 self-evolution 仓库给了个好提醒：不是"能改就行"，而是先有评估样例，再让候选变体进 PR。

第四道门，版本和回滚。

这个我会写得重一点。因为这恰好是 Hermes 现阶段让我最想补的一块：patch 后旧版本容易消失，出了误修正恢复成本很高。更稳的方式是每次变更有 diff、有 changelog、有最近 N 个版本可恢复。高风险 Skill 走 PR，低风险 Skill 可以自动合并，但也要能追溯。

第五道门，权限。

一个 Skill 能调用哪些工具、能读写哪些目录、能不能访问网络、能不能碰凭据，都要有边界。否则 Skill 很容易从"过程资产"变成"权限包装"。

这些不太性感，但真到生产里大多躲不过去。
我们能从 Hermes 学什么
往学术线上追，这条思路不新。2023 年 NVIDIA 的 Voyager 就证明过：Agent 可以把成功行为沉淀成一个持续增长的 skill library。

但论文世界和工程世界差得远。Voyager 解决的是"技能能不能累积"，Hermes 回答的是另一层问题：技能累积以后，怎么在真实系统里安全地存、便宜地用、出了问题还能改。

所以我更倾向于把 Hermes 当一个提醒：Agent 系统的重心正在往经验层移动。

过去大家先拼模型，再拼工具，再拼上下文。现在这些当然还重要，但差距会越来越多出现在另一层：

团队有没有把反复发生的事情，整理成 Agent 能稳定复用的资产。

个人场景里这叫"越用越顺手"。团队场景里就叫工程化。

对团队来说，先沉淀成 Skill 的通常可以从三类小东西开始：
• 高频流程：发布、建 PR、生成周报、同步 issue；• 验证流程：改完功能怎么验、怎么跑测试、怎么看日志；• 排障流程：告警来了先查哪里、哪些命令不能跳过、什么时候升级给人。
这些东西小，但复用频率高，也最容易被验证。

等这些小 Skill 跑稳了，再谈 self-evolution 才有意义。

之前写 Agent Harness 综述时说过：Harness 的差距不在"有没有工具"，而在工具、上下文、权限、记忆、流程和验证能不能组成一个稳定工作台。Hermes Skills 这次给我的启发，是把其中"流程"这一层再往前推了一步——流程不只是人提前写好的，也可以从任务轨迹里慢慢长出来。

但它要长在工程系统里，不能只长在模型的自我感觉里。
写在最后
这次看 Hermes，最想留下来的不是某个具体实现，也不只是"自动创建 Skill"这个卖点。

是一个更朴素的问题：

Agent 做完一件事以后，系统要留下些什么。

留下事实记忆，它下次更懂你。

留下会话检索，它下次能找回历史。

留下过程资产，它下次才可能少走弯路。

这三件事都重要，但不能混成一团。混在一起会变成一个越来越厚、越来越难维护的上下文垃圾桶。分开管理，才有机会长成可演进的 Agent Runtime。

工程团队早就靠这套办法工作了。

我们写 Runbook，写 Checklist，写 Postmortem，写 CI，写发布手册。现在 Agent 也开始学这套老办法。

老办法不新，但能复利。
这篇和前面几篇的关系
整理一下这条线上我们聊过的几个点，方便大家前后对照：
• Anthropic Skills — 团队经验怎么变成 Agent 可复用的工作单元•Codex 仓库 — 工程经验怎么写进仓库，人和 Agent 走同一套路径• Hermes 架构拆解 — 和 OpenClaw 摆在一起看，一个是网关一个是引擎• Hermes 三层学习机制 — Memory / Session / Skills 的分层，和 OpenClaw 的差异到底在哪• Agent Harness 综述 — 同一个模型，做出来的 Agent 为什么差这么远• Agent 最小闭环 — 30 分钟手搓一个最小 Agent，看清骨架• Prompt Caching — 缓存命中率对 Agent 成本的影响，稳定前缀为什么不能乱动
这次这篇算是把"流程"这条线往前推了一步：从"经验放在哪里"到"经验以什么形态进入生产系统"。
参考资料
官方与 GitHub：
• Hermes Agent GitHub：https://github.com/NousResearch/hermes-agent• Hermes Agent Skills System：https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/• Hermes Agent Persistent Memory：https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/• Hermes Agent Skills Hub：https://hermes-agent.nousresearch.com/docs/skills/• Hermes Agent Self-Evolution：https://github.com/NousResearch/hermes-agent-self-evolution• Evolutionary Self-Improvement Issue：https://github.com/NousResearch/hermes-agent/issues/337• Anthropic Agent Skills：https://claude.com/blog/skills• Voyager 论文：https://arxiv.org/abs/2305.16291• Reflexion 论文：https://arxiv.org/abs/2303.11366
如喜欢本文，请点击右上角，把文章分享到朋友圈

如有想了解学习的技术点，请留言给若飞安排分享

因公众号更改推送规则，请点“在看”并加“星标”第一时间获取精彩技术分享

·END·

相关阅读：

刚刚，Claude Code“代码泄露”背后：如何重新看 Agent Harness

大家都在讲 Harness，但它到底该怎么理解

模型越来越强，为什么大家却开始重写 Harness

如何让单个 Agent 做长任务不失真：Anthropic 给出了一套更工程化的答案

Claude Code高手的 8 个 Claude Code 实战习惯

别从 README 开始：一个架构师会怎样翻 Codex 仓库

Spec 不是代码的替代品，它是 AI Coding 的上下文管理层

如何让 Agents 自己设计、升级 Agents

OpenAI怎么把开源项目维护做成工作流：Skills、AGENTS.md 和 CI 的一套组合拳

Claude Skills 入门：把“会用 AI”变成“可复制的工程能力”

一套可复制的 Claude Code 配置方案：CLAUDE.md、Rules、Commands、Hooks
Claude Code 最佳实践：把上下文变成生产力（团队可落地版）把 AI 当成新同事：Agent Coding 的上下文与验证体系一周写百万行的背后：Cursor长时间运行 Agent 的工程方法论2026年生活重启指南我真不敢相信，AI 先加速的是工程师。扒一扒 Claude Cowork 系统提示词：Anthropic 如何打造数字同事Cowork 安全架构深度解析：从 Claude Code 到 Cowork，Anthropic 如何把“可控”做成产品Anthropic官方万字长文：AI Agent评估的系统化方法论银弹还是枷锁？Claude Agent SDK 的架构真相Claude Code创始人亲授13条使用技巧Claude Code 内部工具开源 code-simplifier：终结 AI 屎山代码的终极方案
版权申明：内容来源网络，仅供学习研究，版权归原创者所有。如有侵权烦请告知，我们会立即删除并表示歉意。谢谢!
架构师
我们都是架构师！

