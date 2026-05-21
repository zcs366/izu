---
source_url: https://mp.weixin.qq.com/s/TfR1iLYqJ3QqZK_Aa6ex2w
ingested: 2026-05-10
sha256: 5e0df9b2c80fe8aea6e1472bfca0fc8630dbde0cb1888943f134fc587cb818b8
title: 别到处找Skill！Hermes Agent官方89个内置技能暴力拆解
author: 高管大壮
description: Hermes Agent 89个内置技能18大类暴力拆解，GEPA Loop、skills命令全家桶、slash快捷调用
---

装了一堆skills，不知道怎么用有粉丝跟我要skill，这才是聪明的做法不要到处去找吃灰的skill我不给你重写skill，今天暴力拆解官方内置的89个skillNous Research推出的Hermes Agent，自带89个官方内置技能（Built-in Skills），直接塞进 ~/.hermes/skills/，一键解锁“自进化AI Agent”全家桶这些技能不是普通Tool，不是简单API调用，而是Procedural Memory + Markdown知识文档，支持progressive disclosure（按需加载，省token），还能被Agent自动改进、记忆、组合。我按18大类+杀手级核心玩法，给你一篇公众号爆文级实战指南。读完你就知道：为什么Hermes才是2026年真正的Agent王者，而其他Agent还在“聊天”。（数据来源：Hermes官方Skills Hub & Bundled Skills Catalog，2026最新版）
一、先搞懂Hermes技能系统的“核武器”本质（不看会后悔）Hermes的技能不是“插件”，而是Agent的肌肉记忆：每个skill都是一个带YAML frontmatter的Markdown runbook。Agent用的时候只加载必要部分，上下文干净。支持hermes skills命令一键管理、reset、create。核心闭环：GEPA Loop（Generate → Evaluate → Persist → Adapt），Agent自己造新skill、自我迭代。89个Built-in分18类，覆盖Apple深度集成、视觉爆款内容生产、多代理Kanban协作、MLOps本地炼丹、GitHub全自动流水线……一句话总结：别人Agent是“助手”，Hermes是“会自我进化的AI团队”。
二、89个技能暴力分类拆解（精选杀手级+实战价值）我按官方Categories + 实际杀伤力排序，每类挑最炸的技能，给你功能+用法+爆文/生产力场景+组合玩法。
1. Apple生态类（4个）—— Mac用户直接原生操控现实世界apple-notes：memo CLI全控Apple Notes（建、搜、改）。apple-reminders：remindctl增删改查提醒事项。findmy：实时追踪AirTag/设备。imessage：imsg CLI发收iMessage/SMS。暴力价值：公众号作者在Mac上直接让Agent把脑暴内容扔进Notes、自动发iMessage给编辑、追踪设备提醒发稿截止。零切换成本，Mac生态无缝。
2. Creative创作神器类（15+个，最推荐！）——视觉爆文生产流水线这是Hermes最炸裂的一类，直接把“AI生成内容”干到工业级：comfyui：完整ComfyUI生命周期（装、启、管节点/模型、工作流参数注入），REST+WebSocket直连，生成图/视频/音频。manim-video：3Blue1Brown风格数学/算法动画。baoyu-comic / baoyu-infographic：知识漫画（知识漫画）+21布局×21风格信息图，可视化爆款必备。excalidraw：手绘风架构图、流程图、序列图（JSON）。architecture-diagram：暗黑风SVG云架构图。ascii-art / ascii-video / pixel-art：复古风内容（NES/Game Boy调色板）。p5js：生成艺术、shader、3D交互。claude-design / sketch / popular-web-designs：一键生成HTML落地页、原型、54个真实设计系统（Stripe/Linear/Vercel）。humanizer：去AI味，让文案变“真人”。爆文玩法：你发一条公众号，只需说“用baoyu-infographic+comfyui给我做一张《2026 AI Agent趋势》信息图+漫画版”，Agent直接出图+文案+HTML落地页。内容生产速度提升10倍以上，视觉党狂喜。
3. DevOps & Kanban多代理协作类（3个核心）——真正实现“AI团队”自治kanban-orchestrator：分解任务+专家 roster + “别自己干活”铁律，自动路由给Worker。kanban-worker：坑点、案例、边缘场景全覆盖（lifecycle已自动注入）。webhook-subscriptions：事件驱动Agent运行。暴力价值：开启多Agent模式后，Hermes自己拆任务、分配、并行执行、汇报。公众号爆文写作？直接让orchestrator指挥“研究Agent + 写作Agent + 设计Agent + 发布Agent”一条龙。这是2026年Agent的终极形态。
4. GitHub全流程自动化类（6个）·github-pr-workflow / github-code-review / github-issues / github-repo-management等。·codebase-inspection：pygount代码库分析（LOC、语言占比）。玩法：Agent自动开PR、Review、Merge、发Release。Indie Hacker一人顶一个团队。
5. MLOps / AI工程类（大量）——本地炼丹喝水一样简单（官方内置Axolotl、vLLM、Unsloth、Ollama等相关skills）·Fine-tuning、Serving、Eval、量化全覆盖。·jupyter-live-kernel：实时Python交互。极客价值：本地部署+持续优化模型，Hermes自己炼自己的“专属大脑”。
6. Productivity & Research类（Notion、Linear、Google Workspace、arXiv、Blogwatcher等）·自动管任务、读写Notion、监控RSS、搜学术论文。·email/himalaya：终端全控邮件。
7.其他重磅：Gaming：Minecraft模组服务器、Pokemon无头模拟。Media：GIF搜索、视频处理。MCP：native-mcp连接外部MCP服务器，扩展无限。dogfood：Web App自动化QA。（完整89个可去官方Skills Hub查看，我这里只拆最能打的）
三、高级玩法：让89个技能“自进化”成你的专属武器库
1、核心命令：hermes skills（最常用全家桶）
命令

完整语法示例

功能暴力注释

推荐实战场景 & Pro Tips

list

hermes skills list

列出当前已安装的所有技能（Built-in + Hub + 自定义），只显示名称 + 简短描述（超轻量，Progressive Disclosure）

新手入坑第一条！快速清点武器库。管道过滤：hermes skills list | grep comfyui

search

hermes skills search kubernetes

在Skills Hub + 所有注册表里全文搜索技能

想找某个特定功能时用，秒出匹配ID

browse

hermes skills browse

分页交互式TUI浏览器，浏览所有官方/社区技能注册表

发现新技能神器，像逛App Store

install

hermes skills install official/comfyui hermes skills install https://xxx.com/SKILL.md

安装/激活技能（支持 official/、社区ID、直接URL） 可加 --name 新名字 覆盖frontmatter

解锁Optional技能必备！安装后立即可用

inspect

hermes skills inspect official/baoyu-comic

预览技能完整内容（不安装，直接看SKILL.md + YAML）

想先看代码再决定装不装时用

config

hermes skills config hermes skills config comfyui

交互式配置面板：按平台启用/禁用、设置权限、参数

Mac用户只开Apple生态技能超实用

check

hermes skills check

检查所有Hub安装的技能是否有上游更新

定期执行，保持技能最新

update

hermes skills update

一键更新所有有新版本的Hub技能

保持武器库常新

audit

hermes skills audit

重新扫描+验证已安装技能的完整性与安全

安全审计必备

uninstall

hermes skills uninstall baoyu-infographic

卸载通过Hub安装的技能（不影响Built-in）

清理不需要的技能

reset

hermes skills reset <name> [--restore]

重置被修改过的Bundled内置技能，恢复官方默认版本

玩坏了官方技能？一键回血！

publish

hermes skills publish ./my-skill

将本地技能发布到Skills Hub（支持GitHub等）

想把自己的爆款流程分享给社区时用

tap

hermes skills tap add owner/repo hermes skills tap list

管理自定义技能源（私有GitHub仓库等）

企业/私人技能仓库专用
2、聊天界面内快捷命令（最丝滑用法！）在 hermes chat 或任何消息平台直接输入 / 触发：·/skills →直接唤起技能管理TUI（browse/search/install全功能）·/skill-name →直接调用某个已安装技能（例如 /comfyui、/baoyu-comic）o只输入 /excalidraw 也会让Agent询问你具体需求·所有已安装技能自动注册为slash命令，零学习成本3、Agent内部技能管理工具（GEPA自进化核心）这些是Agent自己调用的内置Tool，不是CLI，但极客必知：·skill_manage：创建/更新/删除/编辑技能（create、patch、edit、delete动作）o这是GEPA Loop（Generate→Evaluate→Persist→Adapt）的核心武器oAgent完成任务后可自动建议“要不要把这个流程保存成新skill？”·skill_view：加载技能完整内容（支持Level 0/1/2 progressive disclosure）手动创建自定义技能终极姿势（3秒搞定）：1)mkdir -p ~/.hermes/skills/my-category/my-skill2)新建 SKILL.md（带YAML frontmatter）3)完成！hermes skills list 立刻可见四、关联后台命令（进阶玩家）·hermes curator：后台技能维护工具（status、run、pause、pin、rollback）o让Agent在后台自动检查、更新、修复技能一句话总结：list / search / browse =查武器install / inspect / config =装武器reset / update / uninstall =管武器publish / tap =造+分享武器skill_manage =让Agent自己造武器（自进化灵魂）现在你手里握着的是真正完整的技能指挥系统，不再是零散的“enable/create”了！
四、零成本上手指南（3分钟入坑）1.安装Hermes AgentHermes Agent 全平台部署及使用全指南——Linux、macOS、WSL2（Win）、Termux2.hermes skills reset --all 同步89个Built-in。3.hermes 启动，输入帮我用baoyu-comic做一篇公众号爆文试试。4.加入Nous Research社区、Skills Hub，贡献/下载521个Community技能。一句话：89个Built-in只是起点，Hermes真正的恐怖在于——它会自己长出第90、第100、第1000个技能。兄弟们，2026年已经不是用AI写文的时代，而是让AI团队替你打工的时代。Hermes Agent + 这89个技能，就是你的私人AI军团。我已经把2026.5.7 于Skills Hub暴力拆解完毕（转发、收藏、点赞三连，就是对我最大的支持！）如果你想与更多的伙伴一起教学成长，来吧
#HermesAgent #AIAgent #Agent编排 #生产力工具 #NousResearch #MCP #ComfyUI #KanbanAI

