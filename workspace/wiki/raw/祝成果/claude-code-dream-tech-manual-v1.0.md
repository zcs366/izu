# Claude Code Dream — 深度技术手册

> **版本**：v1.0 | **类型**：模式A · 深度技术手册  
> **内容覆盖**：记忆系统架构 / Dream 四阶段 / 源码分析 / Sleep-time Compute / 社区方案 / 未来展望

---

## 目录

1. [概览与核心理念](#1-概览与核心理念)
2. [记忆系统基础架构](#2-记忆系统基础架构)
3. [Dream 四阶段详解](#3-dream-四阶段详解)
4. [实战：完整记忆整理工作流](#4-实战完整记忆整理工作流)
5. [触发机制与参数详解](#5-触发机制与参数详解)
6. [源码与内部实现](#6-源码与内部实现)
7. [社区资源精选](#7-社区资源精选)
8. [业内评价与案例分析](#8-业内评价与案例分析)
9. [避坑指南](#9-避坑指南)
10. [进阶技巧与最佳实践](#10-进阶技巧与最佳实践)
11. [未来展望](#11-未来展望)
12. [附录：术语表](#附录术语表)

---

## 1. 概览与核心理念

### 1.1 什么是 Dream？

Dream 是 Claude Code 的记忆整理（memory consolidation）系统。它不是叫你起床闹钟，而是 Claude 的**睡眠周期**。

| 现实类比 | Claude Code 对应 |
|---------|-----------------|
| 白天吸收信息 | Auto-memory 记录调试/偏好/决策 |
| REM 睡眠整理记忆 | Dream 合并/修剪/索引记忆文件 |
| 睡醒后神清气爽 | 下一会话启动更快、记忆更准 |

### 1.2 为什么需要它？

没有 Dream 的 Claude Code 面临三个核心问题：

**问题一：矛盾积累**。十次会话后，记忆文件中可能同时存在 "用 Express" 和 "用 Fastify" 两条记录——Claude 不知道哪个是对的。

**问题二：过期信息**。重构删掉了 `src/old/` 目录，但记忆文件里还记着 "调试日志在 src/old/logs/" 这条指令。

**问题三：膨胀失控**。`MEMORY.md` 作为索引文件，官方限制 200 行，但人写的东西只会增不会减——需要定期裁剪。

Dream 就是解决这三个问题的机制。

### 1.3 设计理念

Anthropic 的设计选择体现了几条关键理念：

1. **离线优于在线**。整理记忆不是在每次写入时做（那会打断工作流），而是积累到一定量后一次性处理。这和人类睡眠的逻辑完全一致。
2. **手术刀而非大锤**。Dream 不会重写整个记忆目录，而是逐文件、逐条精准修改。不动的文件就不碰。
3. **可审计**。每次 Dream 运行有完整的 usage 记录（input_tokens / output_tokens），开发者可以跟踪开销。
4. **异步安全**。锁文件机制防止并发修改，背景子代理不会干扰主任务。

---

## 2. 记忆系统基础架构

### 2.1 两层记忆体系

Claude Code 的记忆系统分为两层，Dream 操作的是下层：

```
┌────────────────────────────────────────────────┐
│                  会话上下文                        │
│  ┌────────────────┐  ┌───────────────────┐       │
│  │  CLAUDE.md     │  │  Auto Memory      │       │
│  │  (你写的规则)  │  │  (Claude自己记的)  │       │
│  └────────────────┘  └───────────────────┘       │
│        这两者合并后成为每次会话的初始 context      │
└────────────────────────────────────────────────┘
         ▲                           ▲
         │ 加载                      │ 加载
         │                           │
┌────────┴────────┐    ┌─────────────┴───────────┐
│  CLAUDE.md 文件  │    │  记忆目录 (memory/)      │
│                  │    │  ├── MEMORY.md (索引)    │
│  多级作用域      │    │  ├── debugging.md        │
│  全局/用户/项目  │    │  ├── preferences.md      │
│                  │    │  └── build-commands.md   │
│  └── 你手动维护  │    │       └── Dream 维护 ▬▶│
└─────────────────┘    └─────────────────────────┘
```

### 2.2 CLAUDE.md 文件体系

| 作用域 | 路径 | 共享范围 | 谁维护 |
|--------|------|---------|--------|
| 组织策略 | `/etc/claude-code/CLAUDE.md` | 全组织 | 管理员 |
| 用户全局 | `~/.claude/CLAUDE.md` | 你（所有项目） | 你 |
| 项目共享 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队（Git 共享） | 团队 |
| 项目本地 | `./CLAUDE.local.md`（加入 .gitignore） | 你自己（当前项目） | 你 |

**关键规则**：CLAUDE.md 是你写的，Dream **不会修改**它们。Dream 只操作 Auto-memory 维护的记忆目录。

### 2.3 Auto-memory 架构

Auto-memory 是 Claude Code **自动写笔记**的系统。在每个会话中，Claude 会自动记录：

- 你纠正它的地方（"不要用 npm，用 pnpm"）
- 你明确说"记住这个"的要点
- 它观察到的项目模式（"测试全在 `__tests__/` 下"）
- 重复出现的决策（"每次都用 --workspace 参数"）

**存储位置**（按项目隔离）：

```
~/.claude/projects/<project-hash>/
├── memory/
│   ├── MEMORY.md          # 索引文件（<=200行）
│   ├── debugging.md       # 调试技巧
│   ├── api-conventions.md # API 约定
│   ├── build-commands.md  # 构建命令
│   └── user-preferences.md# 用户偏好
└── <session>.jsonl        # 会话日志
```

**索引文件 MEMORY.md 的结构**：

```markdown
# Memory Index
- 构建: 用 pnpm build（见 build-commands.md）
- 测试: 用 pnpm test -- --run（见 debugging.md）
- API: 所有请求通过 /api/v2（见 api-conventions.md）
- 偏好: 使用 Fastify（非 Express）——2026-03-15 更新
```

**200 行限制**不是硬编码，但它决定了每次会话启动时加载多少记忆——超过后，后面的内容被截断。

### 2.4 Auto-memory vs Dream 的关系

| 维度 | Auto-memory | Dream |
|------|------------|-------|
| 角色 | 记录员（写入） | 图书管理员（整理） |
| 触发时机 | 会话中实时 | 会话间离线（≥24h + ≥5次） |
| 操作 | 新增条目 | 合并/删除/日期化 |
| 读权限 | 会话上下文 | 记忆目录+会话日志 |
| 写权限 | 记忆目录 | 记忆目录 |

> "Auto-memory without Dream is like taking notes but never tidying the notebook." — 社区评价

---

## 3. Dream 四阶段详解

### 3.1 阶段一：定向（Orient）

**目标**：了解当前记忆系统的状态。

**具体操作**：
1. 列出记忆目录所有文件
2. 读取 `MEMORY.md` 索引
3. 浏览已有的 topic 文件，了解每份文件的内容范围
4. 识别最近没有打开过的文件（可能已过期）

**这一步不做任何修改**——只是"睁眼看一圈"，建立当前的知识地图。

**类比**：图书管理员进门先看看书架上的书是怎么摆的。

### 3.2 阶段二：收集信号（Gather Signal）

**目标**：从近期会话中提取需要整理的信息。

**关键设计决策——不做全文读取**：

Dream 的 system prompt 明确指示：

> "grep the JSONL transcripts for narrow terms, don't read whole files"

具体搜索的关键词包括：
- 用户纠正（"不要"、"改为"、"不是"）
- 明确的保存指令（"记住"、"记下来"）
- 跨会话重复出现的主题
- 重要的架构决策

**搜索范围**：用 `grep -rn "<term>" <transcript-dir>/ --include="*.jsonl" | tail -50`

**为什么这么设计**？因为全文读取整个 JSONL 会话日志是巨大的 token 开销。Dream 的设计理念是**低成本整理**，不是"重读一遍日记"。

**类比**：不用重读整本日记，而是快速翻看小标签和标记过的段落。

### 3.3 阶段三：整理（Consolidate）

**目标**：对记忆文件做手术级修改。

**七类操作**：

| 编号 | 操作 | 示例 |
|------|------|------|
| C1 | 日期相对→绝对 | "昨天改了 API" → "2026-03-15 改了 API" |
| C2 | 删除矛盾条目 | 同时有 "用 Express" 和 "用 Fastify"，保留最新/最明确的 |
| C3 | 删除过期信息 | "src/old/ 的调试日志"——该目录已删除 |
| C4 | 合并重复主题 | 五次会话都记了 "用 pnpm"，合并成一条 |
| C5 | 更新引用 | topic 文件改名后，更新索引中的指针 |
| C6 | 精简冗长条目 | 把三行描述压缩成一句 |
| C7 | 去除噪音 | "今天试了三个方案"——没用的决策过程 |

**操作原则**：每条修改都是**唯一可标识的**（文件的指定行范围），不是整体重写。

### 3.4 阶段四：修剪索引（Prune and Index）

**目标**：让 MEMORY.md 保持高质量索引状态。

**具体操作**：
1. 确保 **≤200 行**
2. 移除指向已删除 topic 文件的指针
3. 添加指向新建文件的指针
4. 按相关性/时效性重排序
5. 清除索引中混入的详细内容（索引应该是指针，不是数据本身）

**验证**：整理后重新检查索引与 topic 文件的内容一致性。

---

## 4. 实战：完整记忆整理工作流

### 4.1 场景设定

你在一个 Web 后端项目里用了 Claude Code 三周，累计大约 30 次会话。记忆文件已经膨胀到：

```
~/.claude/projects/<project>/memory/
├── MEMORY.md              # 280 行（超限 80 行）
├── debugging.md           # 混杂了已解决的 bug 和待处理的 bug
├── api-conventions.md     # 引用了 Express（已换成 Fastify）
├── random-notes.md        # 新旧混杂，分不清哪些还适用
├── build-commands.md      # "昨天"用了 6 次，没有绝对日期
└── user-preferences.md    # 80% 内容已重复到 MEMORY.md 中
```

### 4.2 执行整理

在日常会话中，运行：

```
/dream
```

**后台发生了什么？**

```
[Phase 1 - Orient]
  ✓ 读取记忆目录，发现 6 个文件
  ✓ MEMORY.md: 280 行（超限）
  ✓ api-conventions.md: 仍引用 Express

[Phase 2 - Gather Signal]
  ✓ grep "Express" → 3 条记录，最新一条: "改用 Fastify"
  ✓ grep "记住" → 4 条记录，涉及 build 偏好
  ✓ grep debug 相关 → 发现 2 个已解决的 bug 被反复记录

[Phase 3 - Consolidate]
  ✓ api-conventions.md: Express→Fastify 更新
  ✓ debugging.md: 删除已解决 bug 记录，保留待处理的
  ✓ build-commands.md: 6 处 "昨天" → 具体日期
  ✓ random-notes.md: 去重合并，删减 40% 内容
  ✓ user-preferences.md: 与 MEMORY.md 合并后删除（独立文件不再需要）

[Phase 4 - Prune and Index]
  ✓ MEMORY.md: 280→142 行
  ✓ 移除指向已删除 user-preferences.md 的指针
  ✓ 重新排序：按近期使用频率排序
```

### 4.3 整理前后对比

| 指标 | 整理前 | 整理后 | 改善 |
|------|--------|--------|------|
| 记忆文件数 | 6 | 5 | -17% |
| MEMORY.md 行数 | 280 | 142 | -49% |
| 矛盾指令 | 2 处（Express vs Fastify） | 0 | 100% |
| 相对日期 | 6 处 | 0 | 100% |
| 重复条目 | 约 15 条 | 合并为 3 条 | -80% |

### 4.4 验证效果

整理后启动一个新会话，输入 `/memory` 看看记忆摘要是否更清晰。然后测试一下：

```
我们这个项目的 API 风格是什么样的？
```

预期回复应该基于 Fastify（而非 Express）回答。

---

## 5. 触发机制与参数详解

### 5.1 Auto-dream 触发条件

两个条件**必须同时满足**：

```
条件一：距离上次整理 ≥ 24 小时
条件二：距离上次整理 ≥ 5 次会话
```

**设计原理**：

| 条件 | 原因 | 边界情况 |
|------|------|---------|
| 24 小时 | 避免频繁整理（整理本身有 token 成本） | 一次长会话跨 2 天→不触发 |
| 5 次会话 | 积累足够信号才有整理价值 | 10 次快速会话 2 小时内→不触发 |

**类比**：你不会每吃一顿饭就深度整理一次冰箱，但你也不会等到冰箱发臭才整理——24 小时 + 5 次会话就是这个平衡点。

### 5.2 feature flag：tengu_onyx_plover

这是 Anthropic 内部的 feature flag 名字。格式是 `动物_宝石_鸟类` 模式，表示**未发布/实验性功能**。

```json
{
  "feature": "tengu_onyx_plover",
  "enabled": false,          // 服务端控制
  "minHours": 24,
  "minSessions": 5
}
```

注意 `enabled: false`——这是**服务端 feature flag**，你在本地修改无效。Anthropic 在逐步灰度。

### 5.3 手动触发

除了 Auto-dream，还有三种方式可以手动触发：

| 方式 | 命令/操作 | 说明 |
|------|----------|------|
| 显式命令 | `/dream` | 直接执行四阶段整理 |
| 意图识别 | "帮我整理记忆" | Claude 识别意图后自动跑 |
| API 调用 | Managed Agents Dreams API | 对记忆存储做深度整理 |

### 5.4 成本参数

以 913 次会话的深度整理为例：

| 指标 | 数值 |
|------|------|
| 处理会话数 | 913 次 |
| 运行时间 | 约 8-9 分钟 |
| 运行模式 | 后台不可见 |
| Token 成本 | 取决于记忆文件大小（未公开） |
| 对用户影响 | 零（后台运行） |

---

## 6. 源码与内部实现

### 6.1 逆向工程发现

Claude Code 的 Dream 功能最初是社区通过逆向工程发现的（2026 年 3 月）。Marco Kotrotsos 在对 macOS 编译后的 Mach-O 二进制文件运行 `strings` 时发现了以下内部名称：

| 内部名称 | 含义 |
|---------|------|
| `autoDream` | 功能名称入口 |
| `tengu_onyx_plover` | Feature flag 代号 |
| `r49()` | 触发函数 |
| `lQ1()` | 配置加载函数 |
| `tengu` | 遥测事件前缀 |

### 6.2 子代理系统

Dream 的核心实现是一个**后台子代理**（background subagent），特点如下：

- **只读**：对项目代码只有只读权限
- **受限工具集**：只能进行文件读取和写入（不能执行代码、不能联网）
- **无会话能力**：不进行对话，只做整理任务
- **异步执行**：与主会话互不干扰
- **system prompt 覆盖**：覆盖正常的 assistant 行为，代之以整理指令

**安全机制**：

1. **锁文件**：`memory/.dream.lock`，防止多个 Claude Code 实例同时整理
2. **写权限限制**：只能写 `memory/` 目录，不能触碰源码
3. **可取消**：通过 API 可以随时取消正在进行的 Dream
4. **部分失败容错**：失败时输出部分整理的记忆存储，不会丢失已做完的工作

### 6.3 调度基础设施

Claude Code 是 CLI 工具，不是常驻后台服务。Dream 的调度依赖三层架构：

| 层级 | 说明 | 持久性 |
|------|------|--------|
| 会话内 `/loop` | 在当前会话中循环执行 | 不持久（会话结束即止） |
| Desktop 定时任务 | 桌面应用的调度系统 | 持久（机器开着就运行） |
| Cloud 定时任务 | Anthropic 云端调度 | 持久（机器关机也不影响） |

Auto-dream 具体使用哪一层尚未公开，但**三层都已投入生产**。

### 6.4 社区复刻：dream-skill

Grandamenium 开发的 [dream-skill](https://github.com/grandamenium/dream-skill)（66 Stars, MIT 协议）完整复刻了 Dream 的四阶段流程：

| 组件 | 文件 | 作用 |
|------|------|------|
| Skill 提示词 | `SKILL.md` | 四阶段整理 + 入驻提示 |
| 条件检查 | `should-dream.sh` | 24 小时间隔检查 |
| 停止钩子 | `dream-hook.sh` | 在 Claude Code 退出时标记下次整理 |
| 安装器 | `install.sh` | 一键安装（`--auto` 自动配置钩子） |
| 测试工具 | `test-dream.sh` | 创建测试夹具并验证整理效果 |

**与官方 Auto-dream 的关键区别**：

| 维度 | Anghropic 官方 | dream-skill |
|------|---------------|-------------|
| 自动触发 | 内置于二进制 | 通过 Stop hook + flag 文件 |
| 记忆系统检测 | 仅 Native | Native + OpenClaw + 自定义 |
| 可用性 | 服务端 feature flag | **即装即用** |

---

## 7. 社区资源精选

### 7.1 深度分析

| 资源 | 作者 | 适合谁 | 内容概览 | 一句话评价 |
|------|------|--------|---------|-----------|
| [Claude Code Dreams: Anthropic's New Memory Feature](https://claudefa.st/blog/guide/mechanics/auto-dream) | Claudefa.st | 所有用户 | 含完整四阶段 system prompt 原文 | 目前最详细的技术分析 |
| [Does Claude Code Need Sleep?](https://dev.to/akari_iku/does-claude-code-need-sleep-inside-the-unreleased-auto-dream-feature-2n7m) | Akari Iku (DEV) | 技术用户 | 从 feature flag 到 Sleep-time Compute 论文的完整映射 | 技术深度最深 |
| [What Is Claude Code AutoDream?](https://www.mindstudio.ai/blog/what-is-claude-code-autodream-memory-consolidation/) | MindStudio | 产品经理 | 横向对比 AutoDream vs MindStudio 记忆方案 | 适合做产品对比 |

### 7.2 社区实现

| 资源 | 适合谁 | 内容概览 | 学到的技能点 |
|------|--------|---------|-------------|
| [dream-skill](https://github.com/grandamenium/dream-skill) | 想立即用上 Dream 的人 | 官方还未开放时的社区复刻版 | 安装 OpenClaw 风格记忆系统 |
| [CLAUDE_CODE_DISABLE_AUTO_MEMORY](https://code.claude.com/docs/en/env-vars) | 不想用自动记忆的人 | 环境变量控制 Auto-memory | 精细控制记忆系统 |

### 7.3 理论基础

| 资源 | 适合谁 | 为什么值得看 |
|------|--------|-------------|
| [Sleep-time Compute (arXiv 2504.13171)](https://arxiv.org/abs/2504.13171) | 研究者、高级用户 | Dream 的理论根基——Alan Turing 研究所 + Letta + UC Berkeley |
| [Managed Agents Dreams API](https://platform.claude.com/docs/en/managed-agents/dreams) | 开发者 | 官方 API 文档（Research Preview） |

### 7.4 视频资源

| 资源 | 时长 | 一句话 |
|------|------|--------|
| [Claude Code's Hidden /dream Feature](https://www.youtube.com/watch?v=E-1Lmyv6Cjo) | ~15分钟 | 展示/dream 的实际效果 |
| [Claude Code Dream Explained in 6 Minutes](https://www.youtube.com/watch?v=_nzl_R7IoAU) | 6分钟 | 快速入门讲解 |

---

## 8. 业内评价与案例分析

### 8.1 核心评价

> "Claude Code without Auto Dream was essentially sleep-deprived. It kept adding random notes without ever cleaning up." — Claudefa.st 分析

> "Auto-memory without Auto-dream is like taking notes but never organizing them." — 社区开发者

> "The naming is borrowed from REM sleep. Your brain replays the day overnight, consolidates short-term into long-term, throws out noise." — Reddit 用户

### 8.2 真实案例

**案例一：大型项目记忆膨胀**

一个 913 次会话的项目，Auto-dream 在后台运行了约 8-9 分钟完成整理：
- 整理前：索引文件超限 80 行，多份文件矛盾
- 整理后：索引从 280 行减至 142 行
- Token 节省：每次会话启动省去约 140 行的记忆加载

**案例二：社区复刻方案**

dream-skill 的开发者 James Goldbach 面临的问题是：Anthropic 的 Auto-dream 虽然已在 Claude Code 代码中，但被服务端 feature flag `tengu_onyx_plover` 控制，普通用户无法启用。于是他用 Shell 脚本 + Claude 的 skills 系统复刻了一个可用的版本。

**案例三：Sleep-time Compute 论文的影响**

Kevin Lin 等人 2025 年 4 月的论文验证了"离线预计算"的可行性：在测试时（test-time），预计算可以降低 5 倍的计算开销，提升最多 18% 的准确率。论文的 `minSessions: 5` 阈值设计在 Claude Code 中得到了直接继承——暗示 Anthropic 与学术界的紧密联系。

### 8.3 一句话评价

| 角度 | 评价 |
|------|------|
| 产品 | "Auto-memory 的缺失那一半——不是取更多笔记，而是整理已有的笔记" |
| 技术 | "用不到 10 分钟的低成本后台任务，换取了每次会话的记忆质量提升" |
| 理念 | "离线记忆整理的工程设计范本——手术刀式精准修改，不是 bulldozer 式重写" |
| 生态 | "一种新的 AI Agent 设计模式的萌芽：睡眠计算 + 记忆整理 + 异步维护" |

---

## 9. 避坑指南

### 9.1 Dream 相关陷阱

| 现象 | 原因 | 修复 |
|------|------|------|
| `/memory` 看不到 "Auto-dream" 行 | 你的 Claude Code 版本过旧 | 更新至 v2.1.59+ |
| 看到 "Auto-dream: off" 且无法开启 | 服务端 feature flag 控制 | 用 `/dream` 手动，或安装 dream-skill |
| Dream 跑完后记忆反而更混乱 | 可能有极高比例的矛盾数据，整理逻辑混淆 | 手动清理 `~/.claude/projects/<project>/memory/` 并重新运行 |
| 打开 Claude Code 时加载很久 | 记忆文件特别大（>500 行） | 手动 `rm -rf memory/` 并用 `/init` 重建 |
| 两个 Claude Code 实例同时运行 | 锁文件失效或未实现 | 社区版需手动避免 |

### 9.2 记忆系统常见错误

| 现象 | 原因 | 修复 |
|------|------|------|
| Claude 总是忽略你的偏好 | CLAUDE.md 中规则和 Auto-memory 冲突 | 运行 `/dream` 清理矛盾后，重新声明偏好 |
| Claude 提到已删除的目录/文件 | Auto-memory 记录了旧内容 | `/dream` 会自动清理过期引用 |
| 记忆索引超长但有价值信息 | MEMORY.md 混入了详细内容 | Dream 会将其降级到 topic 文件中 |
| Auto-memory 记下了不该记的东西 | 没有选择性记忆的能力 | 关掉 Auto-memory 或定期运行 `/dream` |

### 9.3 性能优化

| 问题 | 建议 |
|------|------|
| 记忆文件太大 | 检查 `~/.claude/projects/<hash>/memory/` 中是否有异常大的文件 |
| Dream 运行频繁 | 无法配置频率——由服务端 `minHours: 24` 和 `minSessions: 5` 控制 |
| 不想用 Dream | 服务端 feature flag 不开即可，手动 `/dream` 随时可用 |

---

## 10. 进阶技巧与最佳实践

### 10.1 手工配合策略

**最佳节奏**：

```
第1周：每次显著变更后手动 /dream
第2周：确认自动触发正常后，每周手动 /dream 一次做双重保障
第3周+：只在认为记忆有问题时才手动触发
```

**大型重构前后**：

在大型重构前运行 `/dream`，确保记忆是最新的准确状态。重构完成后，再运行一次，让 Claude 记录新的项目结构。

### 10.2 记忆文件手动管理

即使有 Dream，你也应该定期检查：

```bash
# 查看记忆目录大小
du -sh ~/.claude/projects/*/memory/

# 查看索引行数
wc -l ~/.claude/projects/*/memory/MEMORY.md

# 查看每个 topic 文件的内容
cat ~/.claude/projects/*/memory/*.md | head -50
```

### 10.3 与 Hermes Agent 的类比

Claude Code Dream 的架构对 Hermes Agent 有直接启发：

| Claude Code Dream | Hermes Agent 对应 |
|-------------------|------------------|
| Four-phase consolidation | memory hygiene skill 中的 session 衰减/压缩 |
| grep narrow terms | session_search 的精搜索模式 |
| 200-line index limit | MEMORY 的紧凑存储约束 |
| Lock file | 并发写入防护 |

（Hermes Agent 的 `agent-memory-hygiene` skill 实际上已经实现了类似 Dream 的机制。）

### 10.4 学习路径

| 阶段 | 时间 | 目标 |
|------|------|------|
| Day 1 | 5 分钟 | 运行 `/memory` 检查 Auto-dream 状态 |
| Day 1 | 5 分钟 | 运行 `/dream` 体验手动整理 |
| Week 1 | 日常 | 观察记忆文件的行数变化趋势 |
| Week 2 | 30 分钟 | 阅读 dream-skill 代码理解四阶段实现 |
| Week 4 | 1 小时 | 阅读 Sleep-time Compute 论文理解理论根基 |

---

## 11. 未来展望

### 11.1 短期（2026 下半年）

**Auto-dream 全面开放**。feature flag `tengu_onyx_plover` 在灰度中，预期年内会正式推送给所有 Claude Code 用户。届时：
- `/memory` 中将默认显示 `Auto-dream: on`
- 不再需要社区复刻版本
- 记忆崩溃（memory collapse）将显著减少

**配置化**。当前 Auto-dream 没有用户可配置的参数（minHours/minSessions 都是硬编码）。预计未来会开放：
- 整理频率（每 12h / 24h / 48h）
- 整理深度（快速/标准/深度）
- 排除列表（不想让 Dream 碰的文件）

### 11.2 中期（2027）

**多层级记忆架构**。当前的 Dream 只操作 memory/ 目录中的文件。未来可能扩展到：
- 跨项目记忆共享（同一个用户在不同项目中的偏好）
- CLAUDE.md 的建议式更新（不直接修改，而是提出建议）
- 知识图谱式记忆（不只条目列表，还有关系的显式表示）

**Sleep-time Compute 的深化**。Dream 目前只做记忆整理，不做预计算。Sleep-time Compute 论文的 5x 计算节约是一个未被充分挖掘的潜力——未来的 Auto-dream 可能会：
- 预计算可能的用户查询
- 预先检索相关记忆
- 生成预加载的 context 布隆过滤器

### 11.3 长期（2028+）

**从记忆整理到认知架构**。Dream 的核心思想——离线异步维护在线知识的质量——可能扩展到 AI Agent 的整个生命周期：

| 领域 | 当前 | 未来 |
|------|------|------|
| 记忆 | 整理 | 自动遗忘 + 联想 |
| 技能 | 手动编写 | 自动发现 + 合并 |
| 工具 | 注册 | 自动适应 + 淘汰 |
| 知识 | 文件 | 知识图谱 + 概念漂移检测 |

**行业影响**。如果 Auto-dream 模式被验证有效，将催生一个 **Agent 睡眠计算** 的新赛道：
- 背景知识库维护即服务
- 记忆质量评分（AI memory hygiene audit）
- 多 Agent 协调中的"睡眠同步"协议

### 11.4 个人预测

> Dream 不会止步于 Claude Code。它代表了一种更广泛的范式转变：**AI Agent 不再只在"响应时"消耗计算资源，而是在"空闲时"默默优化自己**。这个模式在未来两年内将成为 Agent 系统的标配——就像 CI/CD 是现代软件工程的标准一样，**睡眠记忆整理将成为 AI Agent 的标准基础设施**。

---

## 附录：术语表

| 中文 | English | 使用场景 |
|------|---------|---------|
| 自动记忆 | Auto-memory | 会话中自动记录用户偏好和技巧的功能 |
| 梦境整理 | Dream / Auto-dream | 离线整理记忆文件的机制 |
| 记忆整理 | Memory Consolidation | 合并/删除/日期化记忆条目的过程 |
| 索引文件 | MEMORY.md | 记忆目录的顶层索引（≤200行） |
| Topic 文件 | Topic files | 按主题分类的具体记忆内容 |
| Feature flag | Feature flag | 控制功能是否对用户可见的服务端开关 |
| 后台子代理 | Background subagent | 独立于主会话运行的整理代理 |
| 锁文件 | Lock file | 防止并发修改的互斥机制 |
| 会话日志 | Session transcript (JSONL) | 记录每轮对话的日志文件 |
| REM 睡眠类比 | REM sleep analogy | Dream 功能的核心设计隐喻 |
| Sleep-time Compute | Sleep-time Compute | 离线预计算以降低在线计算成本的范式 |
| 测试时计算 | Test-time Compute | 接到查询时才进行计算的传统方式 |
| 记忆漂移 | Memory drift | 随时间和冲突导致记忆质量下降的现象 |
| 零成本假设 | Zero-overhead assumption | 整理工作不影响用户（后台不可见） |
| 信号收集 | Signal gathering | Dream 的第二阶段——从会话日志中提取有用信息 |
| 冲突解决 | Conflict resolution | 处理同一主题的多条矛盾记录 |
| 索引修剪 | Index pruning | 将索引控制在合理大小内的维护操作 |
| 记忆存储 | Memory store | Managed Agents API 中的持久记忆容器 |
| 目标指令 | Instructions (Dream) | 可选的自定义整理重点（最多 4096 字符） |
| 整理成本 | Consolidation cost | 以 token 计量的整理工作消耗 |
| 认知架构 | Cognitive architecture | Agent 记忆/推理/行动的总体设计 |
| 概念漂移 | Concept drift | 用户偏好随时间自然变化导致的记忆失效 |
| 睡眠周期 | Sleep cycle | Dream 触发的时间窗口（24h + 5 sessions） |
| 部分失败容错 | Partial failure tolerance | 整理失败时保留已完成工作的机制 |
| 锁互斥 | Lock mutual exclusion | 确保同时只有一个整理任务运行的防护 |

---

*本文基于 2026 年 5 月公开资料编写。Claude Code Dream 仍在服务端灰度中，具体实现细节可能随版本更新变化。*
