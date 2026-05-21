---
source_url: https://mp.weixin.qq.com/s/i48sF8KVuwX6vXg204TyuA
ingested: 2026-05-10
sha256: 2cfe0c49172e36e1c6b9cf03ba07c7751f84d81b77009d3e047a334ae216ffa8
title: 用 Hermes 直接指挥本地 CodeX 写代码, Profiles 搭建多Agent实践
author: 蝈蝈的AI笔记
description: Hermes Profiles 双 Agent 实战：coder（调度CodeX）+ assistant（日常），含完整搭建步骤
---

哈喽，大家好，我是蝈蝈

很多人用 Hermes 的方式是一个 Agent 包揽所有事，但用久了会发现一个问题：Agent 的记忆越积越杂，行为越来越难预测。写代码时学到的项目习惯，和写日报时积累的表达偏好，全混在同一个 MEMORY.md 里——导致 Agent的记忆会变乱。

而 Hermes里的 Profiles 就是解这个问题的。每个 Profile 是完全隔离的独立环境，有自己的配置、记忆、技能和 Gateway，各自成长，互不干扰。

我自己是用 Profiles 功能在同一台机器上同时跑两个完全独立的 Agent，一个负责每天自动拉数据、整理知识库、推飞书日报, 另一个专门做编程任务。

下面我把整个搭建过程完整记录下来, 直接可以照着做。
一、架构设计：两个 Profile，各司其职
coder Profile 是我们本次新增的, 用来处理代码任务调度员。它自己不写代码，只负责理解需求、拆解任务、调用本地 CodeX 或 Claude Code 执行，审查结果后汇报。这个设计的逻辑是：CodeX 已经积累了大量专业 coding skill，是真正擅长写代码的工具，Hermes 只需要做好"需求翻译"和"结果审查"就够了。

hermes 就是原来的主agent 负责日常的交互, 包括获取新增制作每日简报, 以及知识库整理。

目前这两个 Profile 职责清晰、互不依赖，所以暂时不需要第三个协调 Profile。等真正出现"coder 完成代码后自动触发 assistant 生成文档"这类流水线需求时再加，现阶段不要过度设计。
二、创建 Coder Profile
hermes profile create coder

这一行命令做了两件事：在 ~/.hermes/profiles/coder/ 下创建完整的隔离环境，同时生成 coder 命令别名。从此 coder 等价于 hermes -p coder，所有子命令都可以直接用：

coder setup         # 配置 API 密钥和模型
coder chat          # 开始对话
coder gateway start # 启动 Gateway

模型选择上，coder Profile 的核心工作是任务调度而非代码生成，用轻量模型就够，算力留给 CodeX
三、用 SOUL.md 定义角色
每个 Profile 的 SOUL.md 是系统 prompt 的第一槽位，决定 Agent 的身份和行为倾向，路径是

 ~/.hermes/profiles/coder/SOUL.md。

这里有一个容易混淆的区分：SOUL.md 管"这个 Agent 是谁"，项目根目录的 AGENTS.md 管"在这个项目里做什么"。两个文件职责不同，不要混了。

coder Profile 的 SOUL.md 核心是把"不自己写代码"这个行为倾向写清楚：

# 身份
你是一位代码任务调度专家。你自己不直接编写代码，
而是通过调用 CodeX 或 Claude Code 来完成所有编码工作。

# 工作方式
- 收到需求时，先分析任务类型和复杂度
- 将任务清晰描述后，委派给 CodeX 或 Claude Code 执行
- 审查返回的代码质量，必要时要求修改
- 向用户汇报结果，而不是自己动手写

# 风格
- 简洁直接，像技术项目经理
- 任务拆解精准，指令清晰无歧义

# 避免
- 自己生成大段代码
- 不加审查地直接转发工具返回结果

修改完直接 coder chat 开新会话即生效，无需重启任何服务。
四、连通本地 CodeX
hermes连接本地codex完整调用链如下：

首先要为codex开通设备访问的权限, 在你的chatgpt里配置"安全"里面做开启, 如下图:

然后让你的coder agent 直接尝试连接你本地的codex, coder会给你一个验证码 和 openai的连接用来做配对, 我们点进去连接, 然后输入验证码就好

配置完成后，在飞书里向 coder Profile 发送一个编程任务，可以看到 Hermes 完整地执行了调度链路：先检查 CodeX 登录状态（codex login status），再通过 codex exec resume 把任务派发出去，等待执行，最后读取配置文件验证结果。

执行结果显示：CodeX APP里可以看到新建了执行会话，目标任务完成，smoke 验证通过; 而Hermes 全程没有自己生成代码，只做了调度和验证。到此, Hermes 与本地 CodeX链路打通。
五、多agent日常管理速查
hermes profile list              # 查看所有 Profile 状态
hermes profile show coder        # 查看 coder 的详细配置
hermes profile export coder      # 导出备份为 coder.tar.gz
hermes profile rename coder dev  # 重命名，同步更新别名和服务
hermes update                    # 更新代码并同步所有 Profile 的内置技能
六、下一步
什么时候才真正需要第三个"协调 Profile"？

目前两个 Profile 是并行独立的关系——你找 coder 就是找 coder，找 assistant 就是找 assistant，它们互不知道对方的存在。这在大多数场景下已经够用了。

但有一类需求会打破这个模式：当一个任务需要多个 Profile 按顺序协作完成的时候。 比如这样一条流水线:

这种有依赖关系的多角色流水线，才真正需要一个 orchestrator Profile 来统筹调度。

但现阶段不要急着建它。 过度设计是 Agent 工作流里最常见的坑——架构搭得很漂亮，实际上每天用到的只有两个 Profile 各自独立跑任务。等你真正感觉到"我需要有人来协调它俩"的那一天，再加这一层，不会太晚。
七、写在最后
今天这套配置走下来，核心的感受是：Hermes 的 Profile 系统本质上是在做"专业化分工"。

一个全能 Agent 听起来很美，但时间久了你会发现，它积累的记忆越来越杂，行为越来越难以预测。Profile 强制你在一开始就想清楚——这个 Agent 是干什么的，它的边界在哪里。

coder 只管调度代码，assistant 只管日常，各自积累各自领域的 skill 和 memory。用得越久，每个 Profile 越"专"，而不是越"乱"。 这才是 多agent 的长处所在。

如果这篇对你有帮助，帮忙点赞关注，帮助作者有动力继续更新！

