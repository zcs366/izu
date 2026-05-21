---
source_url: file:///mnt/i/hermes/wiki_dropbox/cli-manual-v1.0.md
ingested: 2026-05-11
sha256: 979cf5753086b737000bdded0f8c840f6b7363bfdb8d429e34fffbe5e3cd2249
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: CLI 设计哲学手册
---

# CLI 设计哲学手册

> 来源: cli-manual-v1.0.md（用户存入 wiki_dropbox）

# CLI 设计哲学手册

> 从 Unix 到 Agent 时代，命令行界面设计的思考与实践

---

# 第一部分：基础篇

---

## Chapter 1: 概览与核心理念

### 1.1 什么是 CLI 设计哲学？

命令行界面（Command-Line Interface, CLI）是所有开发者每天都要打交道的工具。但一个"能用"的 CLI 和一个"好用"的 CLI 之间的差距，远不止功能完整度那么简单。

**CLI 设计哲学** 是关于如何设计命令行工具的一整套思考框架：它探讨什么是一个好的 CLI、为什么某些设计让人愉悦而另一些让人沮丧、以及如何在技术可行性和用户体验之间做权衡。

> 类比：CLI 设计哲学 ≈ 奶茶店的经营理念
>
> - **菜单设计** = CLI 的 help 系统（能否让新顾客快速知道有什么可以点？）
> - **点单流程** = CLI 的参数解析（`少糖去冰加珍珠` 是 flags，`来杯四季春` 是 positional args）
> - **出品方式** = CLI 的输出（封口严实、标签清晰、温度适宜）
> - **店员培训** = 错误信息设计（"这个没了" vs "芋圆今日售罄，是否需要换成椰果？"）

一个好的 CLI 就像一家好的奶茶店：你不需要在菜单前站五分钟才能搞懂怎么点单。但 CLI 设计比奶茶店更复杂——因为你的"顾客"不是普通人，而是程序员和运维人员，他们对效率、可组合性和一致性的要求更高。

### 1.2 为什么它很重要？

一个设计糟糕的 CLI 会带来真实成本：

| 问题 | 后果 | 典型案例 |
|------|------|----------|
| 不一致的参数风格 | 每次用都要查文档 | `tar -xzf` vs `tar --extract` 的历史遗留 |
| 沉默的失败 | 命令失败但不报错，后续流程全乱 | 管道中某个命令静默退出 |
| 冗长的输出 | 需要 `grep` 才能找到想要的信息 | `npm ls` 打印整棵树 |
| 不合理的默认值 | 用户意识不到陷阱 | `rm` 没有回收站 |
| 晦涩的错误信息 | 用户无从下手 | `Error: EACCES` |

> **坏例子**：一个工具需要你记住 `--enable-feature-x` 来启用 X 功能，但默认是关闭的，而且没有提示。用户不知道有 X 功能，自然也不会去启用它。
>
> **好例子**：`git status` 告诉你 `(use "git add <file>..." to include in what will be committed)` — 它不仅告诉你当前状态，还告诉你下一步可以做什么。

### 1.3 CLI 的三种进化阶段

CLI 设计不是一成不变的。在过去五十年里，它经历了三个阶段：

#### 第一阶段：机器时代（1970s–2000s）— 早期 Unix

Unix 诞生于终端只有电传打字机（teletype）的年代。那时候，屏幕空间极度珍贵，计算资源有限，CLI 的设计目标是**让机器高效**。

- 短选项名：`ls -la` 而不是 `ls --list-all --format=long`
- 沉默原则（Rule of Silence）：没消息就是好消息
- 最小输出：谁有时间看人类可读的提示？
- 错误信息：比精简更精简，只给数字错误码

这个阶段留下了宝贵的遗产（Unix 哲学），但也制造了大量让新人望而生畏的设计。

#### 第二阶段：人本时代（2010s–2023）— clig.dev 为代表

随着开发者工具市场的爆发，CLI 开始从"机器友好"转向"人友好"。clig.dev 的发布是一个标志性事件，它系统性地提出了现代 CLI 的设计原则。

- 长选项名：`--verbose` 比 `-v` 更自文档化
- 丰富的帮助系统：`--help` 不再是几行干巴巴的文本
- 渐进式复杂度：新手只需知道 `git status`，专家可以用 `git rebase --interactive`
- 彩色输出：利用终端颜色传递信息层级
- 美化的错误信息：指出"哪里错了"+"怎么修复"

Heroku CLI、httpie、ripgrep 是这个时代的代表。它们证明了"人性化"和"高性能"可以兼得。

#### 第三阶段：Agent 时代（2023+）— AI 消费 CLI

AI 编码助手的普及正在改变 CLI 的消费方式。现在，CLI 的用户不再只是"坐在键盘前的人类开发者"，还包括"替人类执行任务的 AI Agent"。

这意味着新的设计要求：

- **结构化输出是刚需**：`--json` 不再是可选项，而是必需的。AI 需要解析 stdout，而不是靠眼神 awk。
- **确定性大于花哨性**：彩色输出在 AI 消费时可能变成转义字符灾难。需要 `NO_COLOR` / `--plain` 开关。
- **更丰富的退出码语义**：AI 根据退出码做决策，0/1 不够用了。
- **对话式交互的接口化**：`confirm` 提示在非交互环境中需要 `--yes` / `--no` 参数。
- **自文档化的命令结构**：AI 没有"直觉"，它只能靠 help 和 man page 理解工具。

> 一个 CLI 在 Agent 时代的自我修养：当你被 AI 调用时，你的输出应该像 API 响应一样干净可解析。

### 1.4 核心原则一览

本书围绕五大核心原则展开：

| 原则 | 一句话概括 | 优先级 |
|------|-----------|--------|
| **人性化优先**（Human-First） | CLI 是人用的，然后才是机器用的（但 Agent 时代是并列的） | ★★★★★ |
| **可组合性**（Composability） | 你的输出应该是别人的输入 | ★★★★★ |
| **一致性**（Consistency） | 用户不需要为每个工具重新学习一套规则 | ★★★★☆ |
| **渐进式发现**（Progressive Discovery） | 新手不困惑，专家不烦躁 | ★★★★☆ |
| **对话式交互**（Conversational Interaction） | 帮助、错误信息要像人在说话而不是机器在喷码 | ★★★☆☆ |

### 1.5 生态全景

CLI 不是一个孤立的领域，它有一个完整的生态系统：

```
┌─────────────────────────────────────────────┐
│              CLI 理念层                       │
│  Unix 哲学 · clig.dev · POSIX · GNU 约定     │
├─────────────────────────────────────────────┤
│              CLI 工具层                       │
│  git · docker · gh · ripgrep · jq · httpie  │
├─────────────────────────────────────────────┤
│              CLI 框架层                       │
│  Python: Click/Typer/argparse               │
│  Rust: clap                                 │
│  Go: cobra                                  │
│  Node: commander/yargs                      │
└─────────────────────────────────────────────┘
```

- **框架层**负责将设计哲学具体化为代码约束。比如 Click 的 `@click.option` 装饰器天然鼓励 long option 命名。
- **工具层**是设计哲学的最佳实践集合。观察 git 或 ripgrep 的设计决策，比读一百篇博客更有效。
- **理念层**提供理论指导。Unix 哲学告诉你"做一件事且做好"，clig.dev 告诉你"错误信息要带修复建议"。

本书的主要受众是框架使用者（CLI 开发者）和理念爱好者（CLI 设计师），我们以工具层为案例，以理念层为指引，帮助你在框架层做出更好的设计决策。

---

## Chapter 2: CLI 设计的历史渊源——从 Unix 到现代

### 2.1 Unix 哲学的 CLI 遗产

Unix 的诞生（1969年）不仅是操作系统的革命，更是 CLI 设计的奠基事件。Ken Thompson 和 Dennis Ritchie 在贝尔实验室的 PDP-7 上敲出的那些命令，至今仍在每一台 Linux/Mac 终端里运行着。

Unix 哲学在 CLI 设计领域浓缩为五条原则：

#### 1. 做一件事，并把它做好（Do One Thing Well）

每个工具只解决一个问题。`ls` 只列目录，`grep` 只做文本搜索，`sort` 只排序。

> **为什么？** 因为组合比功能大更重要。如果我需要查看按修改时间排序的文件列表，我可以用 `ls -lt`（ls 自己做了排序），但更好的方式是让它们可组合：`ls | sort -k5`。如果 ls 把排序、格式化、颜色、图标全做了，它就很难和其他工具协作。
>
> **现代启示**：你设计的 CLI 是否在试图做太多事情？如果一个工具的 subcommand 超过 20 个，考虑拆分成多个工具。

#### 2. 文本流即接口（Text Streams as Interface）

Unix 的杀手级特性是管道（pipe）：`|` 符号让一个程序的 stdout 流入另一个程序的 stdin。

```
grep "error" log.txt | sort | uniq -c | sort -nr
```

这行命令把四个工具串联成了一个数据处理流水线。核心前提是：**每个工具的输入和输出都是纯文本流**。

> **现代启示**：
> - 默认输出要是人类可读+机器可解析的（避免表格花样太多导致 `awk` 失效）
> - 提供 `--json` 输出格式以满足 Agent 时代的需求
> - 不要用 ANSI 转义码污染 stdout（有颜色需求的输出请发到 stderr 或提供 `--color` 开关）

#### 3. 沉默原则（Rule of Silence）

经典的 Unix 哲学："当一个程序没什么特别的东西要说时，它应该保持沉默。"

```
$ cp file1 file2
$   # 没有任何输出 = 成功
```

> **为什么？** 因为输出会被用于管道。如果 `cp` 打印了 `"Copied file1 to file2 successfully"`，下游的 `grep` 或 `awk` 就会收到不该收到的文本。
>
> **现代挑战**：沉默原则在交互式使用中很糟糕。用户不知道命令是否执行了。所以现代 CLI 在"交互模式"和"管道模式"之间做区分：
> - 管道中：保持沉默（或由 `--quiet` 控制）
> - 交互终端：给出简洁的成功反馈（`git commit` 会输出一行摘要）

#### 4. 组合而非创建（Composition over Creation）

不要创造新工具，而是组合已有工具。如果三个小程序能完成工作，就不要写一个大程序。

> **现代启示**：你的 CLI 工具应该可以嵌入到别人的工作流中。提供 `--format json`、`--quiet`、`--no-color` 这些让工具"可组合"的参数。

#### 5. 一切皆文件（Everything is a File）

硬件设备、进程、管道、套接字……在 Unix 中都可以用文件描述符操作。这让统一的数据读写模式成为可能。

### 2.2 POSIX Utility Conventions — 13 条语法规则

POSIX（Portable Operating System Interface）标准定义了命令行工具的 13 条语法规则。虽然很多工具不再严格遵守，但理解这些规则是理解 CLI 设计的基础。

| # | 规则 | 解释 | 示例 |
|---|------|------|------|
| 1 | 命令名至少2字符，仅用小写字母 | 避免和内置命令冲突 | `grep` 可以，`G` 不行 |
| 2 | 选项名是单字母，前面加 `-` | 短选项传统 | `-v`, `-l`, `-a` |
| 3 | 选项可以有参数，用空格分隔 | 注意 `-o file` 和 `-ofile` 等价 | `-o output.txt` |
| 4 | 选项参数可选时，必须紧贴选项 | 避免歧义 | `-gfile` 而不是 `-g file` |
| 5 | 多个无参选项可合并 | 节省击键 | `-abc` 等价于 `-a -b -c` |
| 6 | 选项在参数之前 | 解析器顺序处理 | `ls -l /tmp` 而不是 `ls /tmp -l` |
| 7 | `--` 终止选项解析 | 之后的都被视为参数 | `grep -- -v file` 搜索字符串 `-v` |
| 8 | `-` 表示标准输入 | 除非另有约定 | `cat -` 读取 stdin |
| 9 | 选项不可分组（可选参数会歧义） | 规则4的自然推论 | 避免 `-abc` 其中 `-b` 带可选参数 |
| 10 | 选项顺序通常不重要 | 除非有依赖关系 | `-la` 和 `-al` 等价 |
| 11 | 参数顺序由具体工具定义 | POSIX 不做统一要求 | `cp src dst` 但 `mv src dst` |
| 12 | 环境变量可影响工具行为 | 但不应覆盖显式参数 | `POSIXLY_CORRECT=1` |
| 13 | `--help` 和 `--version` 是保留选项 | 应被所有工具支持 | 但不是 POSIX 强制要求（GNU 推广的） |

### 2.3 GNU Coding Standards 与长选项名

POSIX 的短选项（`-v`）在机器时代很好用，但人类记不住 `tar -xzvf` 里四个字母各是什么意思。GNU 项目在 1980 年代引入了**长选项名**（long options），用 `--` 前缀表示：

```
tar --extract --gzip --verbose --file archive.tar.gz
```

当然，没人会这么打字。长选项名的真正价值是 **自文档化（self-documenting）** 和 **脚本可读性**：

- 交互使用：短选项快捷，`tar -xzvf`
- 脚本编写：长选项易读，`tar --extract --gzip --verbose --file archive.tar.gz`
- help 输出：长选项让 `--help` 变得真正有帮助

**Option Table 的概念**：GNU 规范建议每个工具维护一张"选项表"，记录每个选项的短名、长名、参数类型、默认值、描述。这个表既是代码实现，也是文档来源，也是 help 生成的依据。

```
短名  | 长名       | 参数    | 默认值    | 描述
------|------------|---------|-----------|-------------------
-h    | --help     | 无      | -         | 显示帮助信息
-v    | --verbose  | 无      | false     | 输出详细信息
-o    | --output   | 字符串  | stdout    | 输出文件路径
-n    | --count    | 数字    | 10        | 显示条目数
```

> 几乎所有现代 CLI 框架（Click, clap, cobra）都内置了 Option Table 的支持。你只需要声明选项，help 文本、自动补全、参数校验自动生成。

### 2.4 传统沉默 vs 现代反馈：平衡的艺术

这是 CLI 设计中最古老也最重要的张力：

```
Unix 传统：沉默 = 成功
现代哲学：反馈 = 信任
```

| 场景 | 传统 Unix 做法 | 现代做法 | 折中方案 |
|------|---------------|---------|---------|
| 文件复制成功 | 无输出 | `Copied 5 files (2.3MB)` | 交互模式显示，管道模式沉默 |
| 命令执行中 | 无进度指示 | 进度条 | `--progress` 开关控制 |
| 删除文件 | 无确认 | 提示确认或显示回收站信息 | `-f` 跳过确认，`-v` 显示详情 |

**决策原则**：

1. **让输出可预测**：用户和 AI 应该能推断出命令在不同情况下会输出什么
2. **默认行为对新手友好**：`git` 的默认输出很丰富，但切换到管道时会自动精简
3. **用环境变量控制冗长度**：`CI=true pip install` 会降低输出频率
4. **提供 `--json` 和 `--quiet` 作为"安全出口"**

> **为什么沉默原则在 Agent 时代遇到了挑战？**
>
> AI Agent 需要从 stdout 获取数据来做进一步决策。如果工具沉默，Agent 不知道命令是否成功。如果工具输出太多噪音，Agent 不知道该解析什么。所以 Agent 时代需要的不是"沉默"或"热闹"的二选一，而是**可控的输出层级**：
>
> - `--quiet`: 只输出必要的数据结果
> - 默认：人类可读的摘要
> - `--verbose`: 调试级别的详细信息
> - `--json`: 结构化数据供程序/AI 消费

### 2.5 关键转折点：git / docker / Heroku CLI

有三个工具重新定义了"好的 CLI"是什么样的：

#### git（2005）— 从混乱到有序

git 的 CLI 设计其实**并不完美**。`git checkout` 做了三件事（切换分支、恢复文件、创建分支），这是设计上的错误。但 git 做对了几件大事：

- **渐进式复杂度**：`git init` → `git add` → `git commit`，一条简单路径就能完成核心工作流。而高级功能（`git rebase --interactive`）藏在 subcommand 里，不影响新手。
- **help 内嵌工作流提示**：`git status` 不仅告诉你状态，还告诉你下一步命令。
- **一致性 subcommand 结构**：`git <verb> <object>` 的模式成为后来者的模板。

#### docker（2013）— CLI 作为品牌体验

Docker CLI 是"CLI 即品牌"的代表。它的设计哲学是**可发现性（discoverability）**：

- `docker --help` 的输出是精心编排的，按使用场景分组
- subcommand 命名直观：`docker run`, `docker build`, `docker push`, `docker pull`
- 错误信息带着 Docker 的标志性蓝色和具体建议
- 但 docker 也有教训：`docker ps` 令人困惑（为什么不叫 `docker list`？）

> 历史包袱：docker 沿用了 Unix 的 `ps`（process status）来保持一致性，但新用户看到 `docker ps` 的第一反应是"Docker 有 PS 游戏机？"

#### Heroku CLI（2011）— 第一次大规模"人性化"

Heroku CLI 是最早一批面向开发者的 SaaS CLI。它的设计影响深远：

- **对话式错误信息**：不只是报错，还给出修复步骤
- **交互式创建向导**：`heroku create` 进入交互模式
- **美化输出**：表格、颜色、emoji（在当时是革命性的）
- **HTTP API 的 CLI 映射**：`heroku apps:info` 对应 GET /apps/:id

Heroku CLI 证明了一件事：**CLI 可以像 GUI 一样友好，而不损失效率**。

#### 这三个工具的共同启示

| 特征 | git | docker | Heroku CLI |
|------|-----|--------|------------|
| 渐进式复杂度 | ✅ 基本操作很简单 | ✅ run/build/push 清晰 | ✅ create/deploy 直观 |
| 丰富帮助 | ✅ status 带提示 | ✅ help 分组展示 | ✅ 示例丰富 |
| 良好错误信息 | 一般（偏传统） | ✅ 带修复建议 | ✅ 对话式 |
| 一致性 | ⚠️ checkout 有瑕疵 | ✅ 结构统一 | ✅ 模式一致 |
| 结构化输出 | ⚠️ 需要 --porcelain | ✅ --format | ✅ --json |

它们共同定义了现代 CLI 的基准线：如果 2010 年代以后的 CLI 做不到 git 级别的 help 质量和 Heroku 级别的错误信息，那就是不合格的。

---

## Chapter 3: CLI 的基本语言——语法、参数与输出规范

### 3.1 命令语法结构

几乎所有的 CLI 工具遵循同一个基本语法模式：

```
command [options] [arguments]
```

或者更完整的：

```
command [global-options] subcommand [subcommand-options] [arguments]
```

> 类比：这就像中文的"主谓宾"结构。
>
> - **命令** = 动词（做什么？）：`git`, `docker`, `note`
> - **子命令** = 动宾短语（具体做什么？）：`create`, `delete`, `search`
> - **选项** = 副词（怎么做？）：`--verbose`（详细地）, `--force`（强制地）
> - **参数** = 宾语（对谁做？）：`note.txt`, `2024-01-01`

### 3.2 参数类型详解

CLI 参数可以分为三大类：

#### Flags（选项标志，简称"选项"）

Flags 是 CLI 中最灵活的参数类型，又分为两种：

**1. 开关标志（Boolean Flags）**

```
ls -l           # 长格式输出
git --verbose   # 详细输出模式
```

最简形式：要么有（true），要么没有（false）。

> 类比：奶茶的"多糖/少糖/去糖" — 你不需要说"糖度：正常"，只有当你想要改变默认时才需要指定。

**设计要点**：
- 默认值应该是对大多数用户合理的
- 用 `--no-` 前缀提供取消功能：`--color` / `--no-color`
- 避免三重状态（true/false/auto）——如果需要，用枚举值替代

**2. 带值标志（Valued Flags）**

```
gcc -o program source.c     # -o 后面跟输出文件名
curl -o file.html https://...  # -o 后面跟保存路径
```

> 类比：奶茶的"杯子大小" — `--size large` 就像说"大杯"。

**设计要点**：
- 值的分隔方式：`-o file`（空格）或 `-ofile`（紧贴）
- 明确值是必需的还是可选的（可选值容易导致歧义）
- 值最好有合理默认值

#### Positional Arguments（位置参数）

位置参数不靠名字标识，靠位置标识。

```
cp source.txt dest.txt        # source.txt 是源，dest.txt 是目标
mkdir new_project              # new_project 是要创建的目录名
echo hello world               # hello 和 world 都是要打印的内容
```

> 类比：去咖啡店说"来杯拿铁" — "拿铁"就是 positional arg，你不需要说"饮品种类：拿铁"。

**设计要点**：
- 位置参数应该是最常变、最核心的数据
- 不要超过 2-3 个位置参数（否则用户记不住顺序）
- 如果需要多个位置参数，考虑用 subcommand 或 flag 替代

#### Subcommands（子命令）

子命令是"命令中的命令"，适合功能复杂的工具。

```
git commit -m "message"       # commit 是子命令
git push origin main          # push 是子命令
docker container ls           # container 是子命令，ls 是子命令的子命令
```

> 类比：去奶茶店点单 → "我要一杯奶茶"（主命令 create），"咖啡系列"（subcommand），"生椰拿铁"（sub-subcommand）。

**设计要点**：
- 子命令是动词（做的事情），不是名词（操作的对象）
- `note create`（✅）vs `note note-create`（❌）
- 嵌套层级不要太深，最多 2-3 层

### 3.3 长选项 vs 短选项的设计策略

| | 短选项（-v） | 长选项（--verbose） |
|---|------------|-------------------|
| 记忆难度 | 高（必须记住缩写） | 低（看到名字就知道意思） |
| 输入速度 | 快（2字符） | 慢（9字符） |
| 脚本可读性 | 低 | 高 |
| Tab 补全友好 | 一般 | 好 |
| 冲突风险 | 高（26个字母+数字有限） | 低 |

**设计策略**：

1. **高频操作给短选项**：`-v`（verbose）、`-h`（help）、`-o`（output）、`-f`（force/file）
2. **低频/精确操作只给长选项**：`--exclude-pattern` 不需要短别名
3. **短选项遵循传统**：
   - `-h` = help
   - `-v` = verbose / version
   - `-q` = quiet
   - `-f` = force / file
   - `-o` = output
   - `-n` = count / dry-run
4. **不要强行创造短选项**：`--color-when` 不需要 `-c`（容易和 `--config` 的 `-c` 冲突）

> **坏例子**：某个工具用 `-x` 表示"启用实验功能"，但用户看到 `-x` 的第一反应是"删除"（来自 tar/rm 的传统）。用 `--experimental` 而不是 `-x`，或者在 help 中明确说明。

### 3.4 选项组合规则的双刃剑

POSIX 规则允许将多个无参短选项合并：`-abc` 等价于 `-a -b -c`。

```
tar -xzvf archive.tar.gz   # -x (extract) + -z (gzip) + -v (verbose) + -f (file=archive.tar.gz)
ls -la                      # -l (long) + -a (all)
```

**好处**：
- 减少击键次数
- 让高频操作更流畅

**坏处**：
- 如果选项带值（如 `-f file`），组合就复杂了：`-xzvf file.tar.gz` 中，`-f` 后面的值是什么？
- 用户很难分辨 `-xzvf` 是四个独立选项的组合
- 对新手来说，`-xzvf` 看起来像摩斯密码

**设计建议**：
- **只对无参选项支持组合**。如果某个选项带值（即使是可选的），就强制分离
- 提供长选项版本作为"安全通道"：`tar -x -z -v -f file.tar.gz` 应该也能工作
- 在 help 输出中同时展示两种方式：`-la, --list-all --long-format`

### 3.5 `--` 作为选项结束标志

双横线 `--` 是一个被低估的设计。它告诉 CLI 解析器：**此后的所有内容都是位置参数，不是选项**。

```
grep -- "-v" file.txt    # 搜索字符串 "-v"（不含引号）
rm -- -file.txt          # 删除名为 "-file.txt" 的文件
```

> 如果没有 `--`，`grep "-v" file.txt` 会被理解为"用 -v 标志（反向匹配）搜索 file.txt"。

**设计要点**：
- 每个工具都应该支持 `--`
- 如果工具接受位置参数，务必正确处理 `--`
- 在 help 文档中说明 `--` 的用法

> **Agent 时代提醒**：AI Agent 生成的命令中经常包含 `--`，因为 AI 倾向于安全第一，会假设文件名可能以 `-` 开头。确保你的工具正确处理 `--`。

### 3.6 输出三通道原则

每个 CLI 程序有且仅有三个方式与世界通信：

```
┌──────────────────┐
│   stdout (1)      │──→ 正常数据输出
│   stderr (2)      │──→ 日志/错误/诊断信息
│   exit code       │──→ 执行结果状态
└──────────────────┘
```

错误的输出通道分配是 CLI 设计中最常见的错误之一。

#### stdout（标准输出）— 数据通道

stdout 是程序的**主要产出**。它应该只包含"用户调用这个命令想要获取的数据"。

**设计规则**：
- stdout 应该可以被管道的另一端直接消费
- 不要在 stdout 中放调试信息、进度条、问候语
- 即使是人类可读的输出，也应该尽量保持可解析性

```
# ✅ 好的设计：在交互终端带格式化，管道中自动精简
$ note list
  ID │ Title          │ Created
─────┼────────────────┼──────────────────
   1 │ Meeting notes  │ 2024-01-15 10:00
   2 │ TODO           │ 2024-01-16 14:30

$ note list | wc -l
3

# ❌ 坏的设计：在 stdout 里放无关信息
$ note list
Fetching notes from database...
Found 2 notes!
  #1: Meeting notes (2024-01-15)
  #2: TODO (2024-01-16)
Done!

$ note list | grep "Meeting"
Fetching notes from database...   # ❌ 不应该出现在这里
```

#### stderr（标准错误）— 诊断通道

stderr 是程序的**"侧台"**。错误信息、警告、日志、进度条、调试信息都应该走 stderr。

**设计规则**：
- 所有非数据的输出进 stderr
- 错误信息带"错误类型: 具体问题: 修复建议"的三段结构
- 用不同格式区分错误和警告

```
# ✅ 好的设计
if file_not_found:
    print("Error: File './notes/today.md' not found.", file=sys.stderr)
    print("Suggestion: Run 'note create today.md' to create it.", file=sys.stderr)
    sys.exit(1)

# ❌ 坏的设计
if file_not_found:
    print("File not found")  # 去了 stdout，管道下游以为这是数据
    sys.exit(1)
```

#### Exit Code（退出码）— 状态通道

退出码是程序返回给父进程的整数，表示执行结果。

**约定俗成的编码**：

| 退出码 | 含义 | 说明 |
|--------|------|------|
| 0 | 成功 | 命令正常完成 |
| 1 | 通用错误 | 大多数失败情况 |
| 2 | 误用错误 | 如参数格式错误、权限不足 |
| 126 | 命令不可执行 | 权限问题 |
| 127 | 命令未找到 | `command not found` |
| 128+信号 | 被信号终止 | 128+SIGINT = 130（Ctrl+C） |

这在 Agent 时代远远不够。如果 AI Agent 调用了你的工具，退出码 1 可能是"文件不存在"或"网络超时"或"参数错误"——AI 不知道该如何应对。

### 3.7 退出码的 HTTP 风格映射建议

一个更丰富的退出码体系：

```
2xx: 成功类
  - 0: 成功
  - 21: 部分成功（批量操作中某些失败）

4xx: 用户错误类
  - 41: 参数错误（类似 HTTP 400）
  - 42: 认证错误（类似 HTTP 401）
  - 44: 资源不存在（类似 HTTP 404）
  - 45: 冲突（类似 HTTP 409，如重复创建）

5xx: 系统错误类
  - 51: 内部错误
  - 52: 外部服务不可用
  - 53: 资源不足（内存/磁盘）
  - 54: 超时
```

> 这个映射不是 POSIX 标准，但它是**合理的惯例**。选择一个标准并坚持它，同时在文档中明确列出。Agent 时代尤其需要语义丰富的退出码。

### 3.8 输出格式设计

#### 默认格式：人类优先，机器兼容

对于人类读者，表格是最常见的输出格式：

```
NAME        STATUS  PORTS
my-app      Up      8080
my-db       Up      5432
```

**表格设计原则**：
- 列对齐（终端中才对齐，不要用 Tab 分隔）
- 列名有含义
- 不要在列内容里换行（考虑截断+省略号）
- 空值用 `-` 或 `—` 表示，不要留空

#### JSON 格式：机器优先

```json
[
  {"name": "my-app", "status": "Up", "ports": [8080]},
  {"name": "my-db", "status": "Up", "ports": [5432]}
]
```

**JSON 设计原则**：
- 提供 `--json` / `--format json` 选项
- 输出的是 JSON 数组或单对象，不要在外面包一层
- 不要在 JSON 里混合错误信息（错误走 stderr）
- 考虑添加 `--pretty` 或 `--indent` 控制可读性

#### 其他格式

- **CSV/TSV**：适合电子表格导入
- **YAML**：适合配置相关的输出
- **plain**：每行一个值，最简单的管道友好格式
- **quiet**：只输出最必要的信息（通常是 ID 或文件名）

> **设计决策**：默认格式应该是"人类可读 + 机器可解析"的平衡。表格好看，但 awk 处理起来麻烦。如果做不到两者兼顾，优先保证机器可解析性——因为 AI Agent 会越来越多地消费你的输出。

---

## Chapter 4: 实战——从零设计一个 CLI 工具的命令体系

理论讲完了，让我们动手设计一个真实的 CLI 工具。

### 4.1 场景设定

我们要设计一个叫 `note` 的笔记管理 CLI 工具。用户在终端里创建、查看、搜索和管理 Markdown 笔记。

### 4.2 步骤 1：定义用户画像

在没有明确用户画像之前，所有设计决策都是空中楼阁。

**我们的用户**：全栈开发者 / 技术写作者（25-35岁）

| 特征 | 含义 |
|------|------|
| 熟悉终端 | 不怕 basic command，git 日常使用 |
| 追求效率 | 愿意花时间配置工具，但期望"开箱即用"也不差 |
| 主要在本地工作 | 不需要实时云同步（但可能需要与 Git 集成） |
| 笔记量中等 | 每天3-5条笔记，总计几百到几千条 |
| 在 Vim/VS Code 间切换 | 编辑在编辑器中完成，CLI 做管理 |

**非用户**：非技术用户（不会用终端）、Evernote 重度用户（需要富文本和附件）

### 4.3 步骤 2：列出核心操作

从用户角度列出最常做的事情：

```
1. 创建新笔记
2. 查看笔记列表
3. 打开/查看某条笔记
4. 搜索笔记内容
5. 编辑已有笔记
6. 删除笔记
7. 给笔记打标签
8. 按标签筛选笔记
9. 导出笔记
10. 初始化笔记目录
```

修剪到 MVP（最小可行产品）：

```
P0（必须）：创建、查看列表、打开、搜索、删除
P1（重要）：编辑、标签
P2（锦上添花）：导出、初始化、统计
```

### 4.4 步骤 3：选择命令结构

两种主流模式：

#### Git 风格（多命令模式）

```
note create "My Note"          # 创建笔记
note list                      # 列出所有笔记
note open 1                    # 打开编号为1的笔记
note search "keyword"          # 搜索关键词
note delete 1                  # 删除笔记
```

**适用场景**：功能多、操作丰富、子命令数量 > 5

#### 单命令模式（像 `cal` 或 `echo`）

```
note "My Note"                 # 创建笔记（用内容推断意图）
note --view 1                  # 查看笔记
note --search "keyword"        # 搜索
```

**适用场景**：功能单一、操作 < 3 种

#### 我们的选择：Git 风格

`note` 显然需要多个操作，Git 风格更合适。理由：

1. **可扩展性**：未来添加 `tag`、`export`、`archive` 不需要破坏现有用法
2. **自文档化**：`note --help` 列出所有 subcommand，每个 subcommand 各自 `--help`
3. **发现性**：用户通过 `note --help` 可以浏览所有功能

```
note <command> [options] [arguments]
```

### 4.5 步骤 4：设计帮助系统

帮助系统是 CLI 的"门面"。用户第一次使用你的工具时，第一件事就是输 `--help`。

#### 顶层帮助：`note --help`

```
Usage: note <command> [options] [arguments]

一个简洁的终端笔记管理工具。

Commands:
  create    创建新笔记
  list      列出笔记（可按标签筛选）
  open      打开笔记查看或编辑
  search    在笔记内容中搜索关键词
  delete    删除笔记
  tag       管理笔记标签

Options:
  -h, --help         显示帮助信息
  -v, --version      显示版本号

Run 'note <command> --help' for detailed usage of a command.

Examples:
  note create "Meeting notes"
  note list --tag work
  note search "API design" --format json
```

**设计要点**：
- 第一行是用法（Usage），给出最基本的语法模式
- 用场景分组：Commands 一组，Options 一组
- 每个 subcommand 有简短的一句话描述
- 提供 3 个左右的典型示例（新手直接复制就能用）

#### 子命令帮助：`note create --help`

```
Usage: note create <title> [options]

创建一条新笔记。

Arguments:
  title                 笔记标题（必填）

Options:
  -t, --tag <tag>      为笔记添加标签（可多次使用）
  -d, --description    笔记描述/摘要
  -p, --path <path>    指定笔记的保存路径（默认: ./notes/）
  -e, --edit           创建后立即用 $EDITOR 打开编辑
  -h, --help           显示此帮助信息

Examples:
  note create "API Design Notes"
  note create "Weekly Report" --tag work --tag report
  note create "Readme" -e
```

**设计要点**：
- Arguments 和 Options 分开列出
- 显示默认值（"默认: ./notes/"）
- 短选项和长选项并列展示
- 示例覆盖最常见的使用场景

### 4.6 步骤 5：设计输出格式

#### 默认输出（人类可读的表格）

```
$ note list
  ID │ Title               │ Tags      │ Created
─────┼─────────────────────┼───────────┼────────────────────
  1  │ API Design Notes    │ work, dev │ 2024-01-15 10:00
  2  │ Weekly Report       │ work      │ 2024-01-16 14:30
  3  │ Grocery List        │ personal  │ 2024-01-17 09:15
```

#### JSON 输出（机器可消费）

```bash
note list --format json
```

```json
[
  {
    "id": 1,
    "title": "API Design Notes",
    "tags": ["work", "dev"],
    "created_at": "2024-01-15T10:00:00Z"
  },
  {
    "id": 2,
    "title": "Weekly Report",
    "tags": ["work"],
    "created_at": "2024-01-16T14:30:00Z"
  }
]
```

#### Quiet 输出（最小信息）

```bash
$ note list --quiet
1
2
3
```

**设计决策**：默认模式是格式化表格，但 piped 到其他命令时自动切换为 plain（每行一个 ID）模式。提供 `--format` 参数让用户显式控制。

### 4.7 步骤 6：设计错误信息模板

错误信息是 CLI 体验中最容易被忽视的部分。一个好的错误信息能挽回一次糟糕的操作体验。

#### 错误信息的三段结构

```
Error: <错误类型> — <具体问题>

Suggestion: <修复建议>
```

#### 场景 1：文件未找到

```
# ❌ 坏的写法
$ note open 999
Error: file not found

# ✅ 好的写法
$ note open 999
Error: note with ID 999 not found

Suggestion: Run 'note list' to see all available notes.
  Or create it: note create --title "Note 999"
```

#### 场景 2：参数错误

```
# ❌ 坏的写法
$ note create
Error: missing argument

# ✅ 好的写法
$ note create
Error: missing required argument 'title'

Usage: note create <title> [options]
Example: note create "Meeting Notes"
```

#### 场景 3：交互式确认

```
$ note delete 1
Warning: This will permanently delete note "API Design Notes" (ID: 1).
Are you sure? [y/N] y
Deleting... done.
```

#### 场景 4：非交互环境的保护

```
$ note delete 1 --force
# 在 CI 或管道中，自动跳过确认（如果有 --force）
# 如果没有 --force 且不是交互终端，直接报错并提示
```

### 4.8 完整的 `note` 设计展示

```
note — 简洁的终端笔记管理工具

Usage:
  note <command> [options] [arguments]

Commands:
  init                 初始化笔记目录
  create <title>       创建新笔记
  list [--tag] [--json] 列出笔记
  open <id> [--edit]   打开笔记
  search <query>       搜索笔记内容
  delete <id> [--force] 删除笔记
  tag <id> <tag>       为笔记添加标签

Global Options:
  -h, --help       显示帮助
  -v, --version    显示版本号
  --verbose        输出详细信息
  --quiet          最小化输出
  --format <fmt>   输出格式: table (默认), json, plain
  --no-color       禁用彩色输出

Config:
  配置文件: ~/.config/note/config.toml
  环境变量: NOTE_DIR (笔记存储路径), EDITOR (编辑器)

Examples:
  note init                           # 初始化笔记目录
  note create "API Design" --tag dev  # 创建带标签的笔记
  note list --tag work --format json  # 列出工作标签的笔记 (JSON)
  note search "error handling"        # 搜索笔记
  note open 1 --edit                  # 用编辑器打开笔记

Exit Codes:
  0  — 成功
  41 — 参数错误
  44 — 笔记未找到
  51 — 内部错误
```

---

## Chapter 5: 参数详解——Flags, Args 和 Subcommands 的设计决策

### 5.1 每种参数类型的类比和适用场景

参数设计本质上是"把用户意图翻译为程序指令"的过程。不同参数类型对应不同的对话方式。

#### Flags（开关）— 相当于"多糖/少糖/去冰"

**开关 flags** 是最简单的参数：有就是 true，没有就是 false。

```
note list --verbose      # 显示详细信息
note list --no-color     # 不要彩色输出
```

**类比**：去奶茶店点单，店员问"糖度？"
- 你不说 = 默认（正常糖）
- 你说"少糖" = `--less-sugar`
- 你说"无糖" = `--no-sugar`

**设计决策**：
- 默认值应该覆盖 80% 的使用场景
- 如果有"禁用"场景，用 `--no-` 前缀统一风格
- 不需要把每一个内部开关都暴露为 flag（隐藏调试用 flag 用 `--debug` 包裹）

> **好例子**：`git --no-pager log` — 禁用分页器，管道模式自动启用
> **坏例子**：一个工具同时有 `--color`、`--colour`、`--colors` 三个版本

#### Flags（带值）— 相当于"杯子大小"

带值 flags 允许用户提供额外参数：

```
note create "title" --tag work --tag personal   # 多值 flag
note list --format json                          # 单一值 flag
```

**类比**：
- "大杯" = `--size large`
- "加珍珠" = `--add tapioca`（可重复使用）
- "冰量" = `--ice less`（枚举值）

**设计决策**：
- 如果 flag 带的值是枚举，在 help 中列出所有选项：`--format <table|json|plain>`
- 如果 flag 可以重复（多值），在 help 中说明：`--tag <name>`（可多次使用）
- 值的类型要明确：数字、字符串、枚举、文件路径？

> **好例子**：`docker run --label env=prod --label team=backend`
> **坏例子**：`--format` 接受但不校验值，输入错误的格式名产生晦涩的内部错误

#### Positional Args — 相当于"来杯拿铁"

位置参数是 CLI 中最自然的交互方式：用户直接告诉程序"对象是什么"，不需要显式命名。

```
note create "Meeting Notes"         # "Meeting Notes" 是标题
note open 1                         # 1 是笔记 ID
```

**类比**：走进咖啡店直接说"拿铁"，你不需要说"饮品种类：拿铁"。

**什么时候用位置参数？**

| 用 | 不用 |
|---|------|
| 参数是命令的核心数据 | 参数是可选的或极少使用 |
| 大多数调用都会提供 | 参数的含义不直观 |
| 顺序自然（如 `src dst`） | 需要 3 个以上位置参数 |
| 一个命令最多 1-2 个位置参数 | 参数类型含混（是文件名还是URL？） |

> **好例子**：`cp source.txt dest.txt` — 源和目标，顺序自然
> **坏例子**：`tool 1 2 3 --mode x` — 三个数字位置参数，用户要查文档才知道每个是什么意思

#### Subcommands — 相当于"点单 → 咖啡 → 拿铁"

Subcommand 是 CLI 的"动词系统"。工具用 subcommand 来表达不同的操作。

```
note create            # 创建笔记
note list              # 列出笔记
note search "query"    # 搜索笔记
```

**类比**：在奶茶店点单：
1. 选择品类：咖啡/茶/冰沙（= subcommand）
2. 选择具体产品：拿铁/美式/摩卡（= sub-subcommand）
3. 选择定制：大小/糖度/加料（= flags）

**什么时候用 subcommand？**

| 用 | 不用 |
|---|------|
| 工具支持多种互斥操作 | 工具只做一件事 |
| 不同操作有不同的参数 | 所有操作共享参数 |
| 操作数量 > 3 | 操作数量 ≤ 3 |
| 操作间逻辑上并列 | 操作是密切相关的变体 |

> **好例子**：`git commit`, `git push`, `git pull` — 三个不同的操作，独立参数
> **坏例子**：如果一个工具只有"导出"和"导入"两个操作，可以考虑 `tool export` 和 `tool import`，但如果一个操作可以解决，就不需要 subcommand

### 5.2 参数设计检查清单

在设计每个参数时，问自己这五个问题：

#### 1. 需要这个参数的用户场景是什么？

```
❌ 错： "加这个--enable-cache 参数以防万一"
✅ 对： "用户经常会查询同一批数据，加缓存可以减少等待时间"
```

每个参数都应该对应一个真实的用户需求，而不是开发者的"防御性设计"。

#### 2. 参数的默认值是否合理？

```
❌ 错：默认关闭 --verbose（导致用户在排查问题时不知道有这个功能）
✅ 对：默认显示基本信息，--verbose 提供更多细节
```

默认值决定了 80% 用户的使用体验。好的默认值意味着大部分用户不需要碰任何参数。

#### 3. 这个参数应该放在哪个层级？

参数的来源有四个层级，优先级从高到低：

```
命令参数 (highest)
    ↓
环境变量
    ↓
配置文件
    ↓
内置默认值 (lowest)
```

**示例**：

```bash
# 1. 命令行参数（最高优先级）
note list --format json

# 2. 环境变量
export NOTE_FORMAT=json
note list

# 3. 配置文件 (~/.config/note/config.toml)
# [defaults]
# format = "json"

# 4. 内置默认值
# format = "table"
```

**设计原则**：
- **敏感信息**（API key, token）只走环境变量或配置文件，不走命令行（会被进程列表看到）
- **临时覆盖**走命令行（"就这一次换个格式"）
- **全局偏好**走配置文件（"我一直喜欢 JSON 输出"）
- **CI/CD 设置**走环境变量（"在 CI 中禁用交互式确认"）

#### 4. 是否遵循了"flags 优先于 args"的原则？

这是一个经验法则：**当不确定该用 flag 还是 positional arg 时，优先用 flag**。

```
# 谨慎：位置参数
note create "title" "work"

# 更好：flags
note create "title" --tag work

# 最好：分离
note create "title"
note tag 1 work
```

原因：
- flags 是自文档化的（`--tag work` 比单纯 `work` 更清晰）
- flags 没有顺序依赖
- flags 容易设置默认值和校验
- flags 容易扩展（加新选项不破坏现有用法）

**例外**：当参数是命令的核心"操作对象"时，位置参数更自然。`cat file.txt` 比 `cat --file file.txt` 好得多。

#### 5. 参数名是否清晰且一致？

```
❌ 不清晰： --out （输出文件？输出格式？输出路径？输出级别？）
✅ 清晰：   --output-file, --output-format, --output-dir, --verbosity

❌ 不一致： --format, --output-format, --fmt, -f 混用
✅ 一致：   统一用 --format, 短选项 -f
```

### 5.3 配置层次详解

四个配置层级构成了 CLI 的"决策链"：

```
用户敲命令 → 解析命令行参数
                  ↓
            检查环境变量
                  ↓
            读取配置文件
                  ↓
            使用内置默认值 → 最终结果
```

#### 命令行参数（最高优先级）

对一次调用生效，优先级最高。

```bash
note list --format json --verbose
```

#### 环境变量

对当前 shell 会话生效，适合 CI/CD 和敏感信息。

```bash
export NOTE_DIR=~/work/notes
export EDITOR=vim
note create "Meeting Notes" -e
# 会使用 ~/work/notes 作为存储目录，用 vim 打开编辑
```

**通用环境变量惯例**：

| 变量 | 含义 | 支持情况 |
|------|------|---------|
| `EDITOR` | 默认编辑器 | 几乎所有工具 |
| `PAGER` | 默认分页器 | `git`, `man` |
| `NO_COLOR` | 禁用颜色输出 | [no-color.org](https://no-color.org) 倡议 |
| `CLICOLOR` | macOS 颜色控制 | 部分工具 |
| `TERM` | 终端类型 | 影响颜色/宽度 |
| `HOME` | 用户目录 | 几乎所有工具 |
| `XDG_CONFIG_HOME` | 配置文件目录 | 现代 Linux 工具 |

#### 配置文件

持久化存储用户偏好，适合"每次都一样"的设置。

```toml
# ~/.config/note/config.toml
[defaults]
format = "json"
verbose = true

[storage]
dir = "~/work/notes"
```

**配置文件设计原则**：
- 默认自动发现：`$XDG_CONFIG_HOME/tool/` → `~/.config/tool/` → `~/.toolrc`
- 支持 `--config` 参数手动指定
- 格式应和工具语言生态一致（Python 工具用 TOML，Node 工具用 JSON）

#### 内置默认值（最低优先级）

代码里写死的值，确保不给任何配置也能正常使用。

```python
DEFAULTS = {
    "format": "table",
    "verbose": False,
    "storage_dir": "~/notes",
    "editor": "vim"  # 如果 EDITOR 环境变量不存在
}
```

### 5.4 环境变量与命令行参数的互操作模式

#### NO_COLOR 标准

[no-color.org](https://no-color.org) 定义了一个行业标准：如果 `NO_COLOR` 环境变量被设置（无论值是什么），工具**不应**输出 ANSI 颜色转义码。

```bash
export NO_COLOR=1
note list    # 无彩色输出
note list --color always   # 但显式 --color 参数可以覆盖
```

**优先级**：`--color` 命令行参数 > `NO_COLOR` 环境变量 > 内置默认值（auto）

#### 环境变量作为"快捷配置"

```bash
# 让用户临时改变默认行为
NOTE_FORMAT=json note list

# 等价于
note list --format json
```

**设计原则**：
- 环境变量名 = `TOOLNAME_OPTIONNAME`（全大写，下划线分隔）
- 环境变量不应有副作用（设置但不使用不影响其他工具）
- 文档中清晰列出所有支持的环境变量

#### 检测交互式和非交互式环境

工具应该能检测自己是否运行在"交互式终端"还是"管道/CI/Agent"环境中：

```python
import sys

def is_interactive():
    """判断是否在交互式终端中运行"""
    return sys.stdout.isatty() and sys.stdin.isatty()

def should_use_color():
    """判断是否应该输出颜色"""
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True
```

**场景示例**：

| 环境 | 检测方式 | 行为 |
|------|---------|------|
| 人类终端 | `isatty()`=True | 颜色、进度条、交互式确认 |
| 管道 | `isatty()`=False | 无颜色、无交互、更简短的输出 |
| CI 系统 | `CI=true` 环境变量 | 无交互、错误时退出码明确 |
| AI Agent | `NO_COLOR=1` 或 pipe | JSON 输出、确认用 `--yes` |

---

## 附录 C: 现代 CLI 工具速览（10 款标杆工具的设计拆解）

> 每个工具按照统一模板拆解：定位 → 设计哲学 → 最值得借鉴的 3 个设计决策 → 一句话槽点

---

### C.1 ripgrep (rg) — grep 的现代替代

**一句话定位**：递归搜索文本内容，比 grep 快 5-10 倍，默认忽略 .gitignore 中的文件。

**设计哲学**（50 字内）：
> "默认就是对的"——合理的默认设置使得大部分情况下无需任何参数就能获得最佳结果，同时保留高级选项给专家。

**最值得借鉴的 3 个设计决策**：

1. **智能默认值**：默认遵守 `.gitignore`，用户不会在 `node_modules` 里搜东西。这是"默认做正确的事"的教科书级案例。
2. **输出即接口**：默认输出和 grep 完全兼容（`file:line:content`），老脚本可以直接把 `grep` 换成 `rg`。
3. **类型感知搜索**：`rg -t py` 只搜索 Python 文件，`rg -T js` 排除 JS 文件。基于文件扩展名的类型系统设计优雅。

**一句话槽点**：Windows 上初次安装有点绕（虽然这是 Rust 工具的普遍问题，不是 rg 的错）。

---

### C.2 fzf — 通用模糊搜索神器

**一句话定位**：终端通用模糊搜索器，任何列表输入都可以变成交互式搜索界面。

**设计哲学**（50 字内）：
> "万物皆可搜"——将"搜索-选择"模式从编辑器扩展到整个终端，通过管道组合实现无限可能。

**最值得借鉴的 3 个设计决策**：

1. **管道输入即列表**：`ls \| fzf` 就能把文件列表变成可搜索的交互界面。极简接口、极强组合性。
2. **预览窗口**：`--preview 'cat {}'` 实时预览选中文件内容。让用户在做选择时有充分信息。
3. **多输出模式**：按 Enter 输出选中项（给管道），按 Tab 多选（给批量操作），按 Ctrl+C 取消（退出码 1）。输出格式和退出码语义清晰。

**一句话槽点**：配置语法太自由（原生的 `--bind` 表达式像一门小型 DSL，需要学习成本）。

---

### C.3 jq — JSON 查询语言

**一句话定位**：终端 JSON 处理工具，使用领域特定语言（DSL）进行数据查询和转换。

**设计哲学**（50 字内）：
> "管道思维下的 SQL"——把 JSON 当数据库查询，用管道把 `curl ... | jq '.data[]'` 变成数据分析流水线。

**最值得借鉴的 3 个设计决策**：

1. **纯函数式管道**：每个 jq filter（如 `.data`、`.[]`、`select(.age > 18)`）都是纯函数，可组合、可测试。
2. **输出格式质量**：默认输出是带有语法高亮的美化 JSON，而 `-r`（raw）输出纯文本——两种模式覆盖了阅读和消费两个场景。
3. **零依赖运行时**：单二进制文件，在任何 CI 或 Docker 镜像中只需一行 `apt-get install jq`。

**一句话槽点**：filter 语法过于紧凑（`.[] | {name, age: .info.age}` 对新手像天书，但这是 DSL 的宿命）。

---

### C.4 httpie — 人性化 HTTP 客户端

**一句话定位**：用自然语法替代 curl 的 HTTP 客户端，强调可读性和易用性。

**设计哲学**（50 字内）：
> "HTTP 请求应该像写便签一样自然"——用最少的标点符号和最直观的语法表达 HTTP 请求。

**最值得借鉴的 3 个设计决策**：

1. **自然语法分隔**：`http POST api.example.com name=john` — 不需要 `-d`、`-H`、引号。`name=john` 是表单数据，`name:==john` 是 JSON。用等号数量区分类型，极其聪明。
2. **彩色格式化输出**：默认带语法高亮显示请求和响应。JSON 缩进、Header 颜色区分、状态码用颜色标识（2xx 绿/4xx 黄/5xx 红）。
3. **对话式工作流**：支持 `--session` 持久化 cookie 和 header，使 HTTP 调试变成"对话"而非孤立的请求。

**一句话槽点**：简单请求很好用，但复杂场景（自定义 TLS 证书、NTLM 认证等）配置比 curl 还难找——简单场景掩盖了复杂场景的文档缺失。

---

### C.5 bat — cat 的现代替代

**一句话定位**：带语法高亮和 Git 集成的文件查看器，比 `cat` 更适合日常阅读。

**设计哲学**（50 字内）：
> "所见即所得的文件阅读器"——让终端读文件和 IDE 看代码一样赏心悦目，但保持纯文本的简洁性。

**最值得借鉴的 3 个设计决策**：

1. **自动语法检测**：根据文件扩展名自动选择语法高亮规则。这听起来简单，但实现质量（能正确识别数百种语言）区分了好工具和装样子。
2. **Git 集成的行号**：行号区域用颜色标识 Git 变更状态（红色=删除，绿色=新增，灰色=无变更）。阅读即代码审查。
3. **优雅的降级**：当 `bat` 检测到输出是管道（非 TTY）时，自动退化为普通 `cat` 行为，不做高亮和行号——确保管道兼容性。

**一句话槽点**：手动安装（下载 .deb/.rpm）才能获得最新版本，apt 源里的版本通常落后半年。

---

### C.6 fd — find 的简化替代

**一句话定位**：查找文件和目录，语法直观，默认排除 .gitignore 和隐藏文件。

**设计哲学**（50 字内）：
> "搜索文件不该比搜索文本更难"——用拍平的学习曲线和智能默认值，把 `find` 从"劝退级"变成"日常级"。

**最值得借鉴的 3 个设计决策**：

1. **直觉化参数名**：`fd pattern` 而不是 `find . -name '*pattern*'`。参数名（`-e` 扩展名、`-t` 类型）短且一致。
2. **并行执行**：`fd pattern -x command {}` 用 `-x` 替代 find 的 `-exec`，但自动使用 `xargs` 级别的并行度，比 find 快得多。
3. **正则与通配双模式**：默认用正则（精确），`-g` 切到通配符模式（模糊）。用户不需要在两种模式间纠结。

**一句话槽点**：正则默认策略让习惯了通配符的用户一开始会困惑（搜索 `*.rs` 要加 `-g`）。

---

### C.7 eza — ls 的现代替代

**一句话定位**：`ls` 的现代替代品，支持颜色图标、树形视图和 Git 集成。

**设计哲学**（50 字内）：
> "目录列表也可以有品位"——在保持 `ls` 命令兼容性的同时，用颜色、图标和元信息让文件列表变成信息面板。

**最值得借鉴的 3 个设计决策**：

1. **Git 状态一目了然**：`eza --long --git` 在每个文件右侧显示 Git 状态（`M` 修改、`N` 新增、`D` 删除）。在项目目录中比 `ls` 有用 10 倍。
2. **智能颜色系统**：按文件类型（不是扩展名，而是 `file` 命令检测）着色，颜色本身携带信息。
3. **树形视图**：`eza --tree` 替代 `tree` 命令，少了装一个工具的依赖。层级控制、深度限制、过滤规则都和 `eza` 其他功能一致。

**一句话槽点**：图标支持依赖终端字体（Nerd Font），默认体验割裂——有图标好看但需要额外配置，无图标又显得单调。

---

### C.8 tldr — 简化版 man page

**一句话定位**：社区驱动的简化版 man page，用示例代替手册。

**设计哲学**（50 字内）：
> "文档的关键是示例，不是长篇大论"——与其读 5000 行 man page，不如看 5 个最常用的命令示例。

**最值得借鉴的 3 个设计决策**：

1. **示例优先**：每个命令 page 的核心是 5-10 个典型使用示例，每个示例附带一句话说明。用户 90% 的时间只需要这些。
2. **社区驱动**：GitHub 上的 Markdown 仓库作为数据源，任何人都可以贡献。这比官方文档更新更快、更贴近实际使用。
3. **客户端-数据分离架构**：`tldr` 有 10+ 语言的客户端客户端，但共享同一个数据仓库。你用 `tldr`（Go 版）或 `tealdeer`（Rust 版），看到的内容是一样的。

**一句话槽点**：客户端碎片化（Rust/Go/Python/Node 各有一个客户端）导致体验不一致，部分客户端要等很久才更新页面缓存。

---

### C.9 delta — 美观的 diff 查看器

**一句话定位**：`git diff` 的语法高亮渲染器，让代码改动像 IDE 一样可视化。

**设计哲学**（50 字内）：
> "diff 不是文本比较，是变动叙事"——用颜色、线条和布局把代码变更变成一段"谁改了哪里、改了什么"的故事。

**最值得借鉴的 3 个设计决策**：

1. **零配置 Git 集成**：`delta` 作为 `git diff` 的 pager，只需两行 Git 配置就能让整个 Git 体验焕然一新。
2. **侧边栏行号**：在左侧用两列行号展示（左边是旧行号，右边是新行号），配合代码高亮，让"哪一行变了"一目了然。
3. **分割视图 + 代码高亮**：同时支持统一 diff 和分割 diff 两种模式，且每种模式都有语法高亮（不是纯文本 diff）。

**一句话槽点**：大型 diff 文件渲染稍慢（语法高亮所有语言很吃 CPU），对巨型仓库不够友好。

---

### C.10 starship — 最小化快速 prompt 框架

**一句话定位**：跨 Shell 的极速提示符框架，用配置驱动、模块化设计。

**设计哲学**（50 字内）：
> "提示符应该提供信息，而不是装饰"——每个显示在 prompt 中的元素都必须携带对当前开发上下文有用的信息。

**最值得借鉴的 3 个设计决策**：

1. **跨 Shell 统一体验**：同一个配置文件（TOML）在 bash/zsh/fish/powershell 中表现一致。解决了"换 Shell 就要重配 prompt"的世纪难题。
2. **模块化设计**：`nodejs`、`git`、`docker`、`python` 等模块独立开关。想显示 Python 版本？加一行 `python` 到配置即可。不想看 Git 状态？删掉 `git`。
3. **性能优先**：Rust 编写，渲染 10ms 内完成。老旧 prompt（如 oh-my-zsh）需要 200-500ms，starship 快 20-50 倍。对"每敲一个字符都要渲染"的场景来说，这决定了工具是否日常可用。

**一句话槽点**：配置是声明式的但不够自动化，首次配置要手动添加全部想要的模块（虽然默认集合已经很好）。

---

### 附录 C 小结

这 10 款工具代表了现代 CLI 设计的最高水平。它们共同的特征：

| 特征 | 体现 |
|------|------|
| **合理的默认值** | rg 的 .gitignore 遵守、fd 的隐藏文件排除 |
| **管道友好** | jq 的纯函数 filter、bat 的 TTY 检测降级 |
| **渐进式复杂度** | fzf 的 --preview、delta 的 Git 配置 |
| **一致性** | httpie 的语法统一、starship 的跨 shell 体验 |
| **自文档化** | tldr 的示例驱动、所有工具的 --help 质量 |

在 Agent 时代，这些工具的 JSON 输出格式、退出码语义和 NO_COLOR 支持将是新的评判标准。你的 CLI 可能不会和它们竞争，但可以用它们作为镜子——当你设计下一个 CLI 时，问问自己："如果 rg 的设计师看到这个参数命名，他会点头吗？"

---

> 第一部分结束。进入第二部分（Chapter 6-10），我们将深入 CLI 的纵深话题：帮助系统设计、错误处理哲学、彩色输出规范、配置管理、测试策略、以及 Agent 时代的高级模式。
\n\n---\n\n
# CLI设计哲学手册 · 第二部分

> 从"能用"到"好用"，从"人类"到"Agent"
>
> 版本：v1.0 | 章节：Ch6–Ch11 + 附录A/B

---

# Chapter 6: 进阶设计模式——错误处理、进度、颜色与配置

本章从"基础正确"进入"专业质感"的领域。如果说前五章教你如何盖一栋不倒的房子，第六章教你如何装修——让住在里面的人觉得舒适、安全，甚至愉悦。

## 6.1 错误处理的四层模型

错误处理是CLI用户体验中最容易被忽视却又最关键的部分。一个错误的错误信息，可能让用户从"困惑"直接滑向"愤怒"。

我们把错误处理分为四个层次，像奶茶店处理订单异常一样层层递进。

### 第1层：优雅捕获并重写（别把内脏翻给客人看）

**核心原则**：用户看到的应该是问题描述，而不是内部实现细节。

想象你去奶茶店点了一杯"杨枝甘露"，店员回头对厨房喊："**KeyError: 'mango' not found in inventory dict!**"——你作为顾客会完全懵掉。合格的店员会说："不好意思，芒果暂时缺货。"

同样的道理，你的CLI不该把 Python 的 `KeyError`、JavaScript 的 `TypeError: Cannot read property of undefined`、或 Rust 的 `unwrap()` panic 直接抛给用户。

**反例（❌）**：
```
$ myapp read notes/today.md
Traceback (most recent call last):
  File "/usr/lib/python3.10/site-packages/myapp/cli.py", line 42, in read
    content = open(path).read()
FileNotFoundError: [Errno 2] No such file or directory: 'notes/today.md'
```

用户看到这个会想："所以呢？文件到底存不存在？我该怎么办？"

**正例（✅）**：
```
$ myapp read notes/today.md
错误：找不到文件 "./notes/today.md"
请检查路径是否正确，或使用 `myapp list` 查看已有文件。
```

**实现要点**：
- 在顶层入口（`main()` 或 `cli()` 函数）包裹全局异常捕获
- 将技术性异常映射为通俗的错误消息
- 保留调试信息，但仅通过 `--verbose` 或 `--debug` 展示

### 第2层：可操作性错误信息（告诉用户下一步）

仅仅"不展示堆栈"还不够。第二层要求你的错误信息包含可操作的建议。

```
第1层：  "文件不存在。"
第2层：  "文件 ./notes/today.md 不存在，是否创建？[y/N]"
```

**类比**：你去ATM取钱，卡被吞了。ATM说"发生错误" vs "您的卡因超时未取回被吞，请联系客服955XX"。哪个让你更安心？

**可操作性错误信息的公式**：

```
[错误类型]：[具体对象] + [出了什么问题] + [建议操作]
```

| 组件 | 示例 |
|------|------|
| 错误类型 | 错误 / 警告 / 信息 |
| 具体对象 | 文件 `config.yaml`，用户 `admin`，端口 `8080` |
| 什么问题 | 不存在，权限不足，已被占用 |
| 建议操作 | 是否创建？请使用sudo。尝试更换端口。 |

**更多正例**：

```
错误：配置文件 /etc/myapp/config.yaml 格式错误（第12行）
→ 建议：运行 `myapp config validate` 检查配置，或使用 `myapp config init` 重新生成

错误：无法连接数据库 postgres://localhost:5432/mydb
→ 建议：请确认 PostgreSQL 服务正在运行（`systemctl status postgresql`）
```

### 第3层：上下文提示（给出周边信息）

第三层在错误信息中加入上下文，帮助用户快速定位问题。

**场景**：一个 YAML 配置文件解析出错。第1层说"格式错误"，第2层说"第12行格式错误"，第3层说：

```
错误：配置文件 config.yaml 第12行格式错误

 第11行:  database:
 第12行→  host: localhost    ← 此处缩进使用了Tab，请使用空格
 第13行:  port: 5432

提示：YAML 不允许使用 Tab 缩进，请将 Tab 替换为空格。
```

上下文提示让用户**不需要打开编辑器**就能理解问题。这在 CI/CD 管道中尤其有价值——用户可能无法方便地打开服务器上的文件。

**实现建议**：对常见文件类型（JSON/YAML/TOML/INI）预置行上下文提取逻辑，出错时自动展示前后2-3行。

### 第4层："Did you mean?" 建议（自动纠错）

最高层次的错误处理：当用户输入错误时，主动猜测正确意图。

```
$ note opne --title "CLI设计哲学"
错误：未知命令 "opne"
→ 你是不是想打 "note open"？（相似度 80%）
```

```
$ git brig
git: 'brig' is not a git command. See 'git --help'.

The most similar command is:
    branch
```

**技术实现**：基于编辑距离（Levenshtein distance）或字符串相似度算法，在命令/参数/文件名空间中搜索最近匹配项。

**实现要点**：
1. 计算用户输入与所有合法选项的编辑距离
2. 设定阈值（通常距离 ≤ 2 或相似度 ≥ 70%）
3. 返回 Top-3 候选
4. 如果唯一候选的相似度极高（≥ 90%），可以直接询问"是否要运行 X？"

**进阶用法**：结合历史记录。如果用户经常打错同一个命令，可以在帮助信息中加一句：

```
提示：你最近3次将 "open" 打成了 "opne"。要不要创建一个别名？
$ alias opne='note open'
```

---

### 四层模型总结表

| 层次 | 描述 | 用户感受 | 努力程度 |
|------|------|----------|----------|
| 第1层 | 无堆栈、清晰翻译 | "哦，明白了" | 低 |
| 第2层 | 给出可操作建议 | "好的我来修" | 中 |
| 第3层 | 显示上下文信息 | "不用开编辑器了" | 中高 |
| 第4层 | Did you mean? 纠错 | "这工具好聪明" | 高 |

---

## 6.2 进度反馈三种模式

CLI 在处理耗时操作时，最忌讳的是**沉默**。用户不知道程序是在运行还是卡死了。

进度反馈有三种典型模式，像三种不同的烹饪方式。

### Spinner（旋转动画）—— 不确定时长

**适用场景**：你无法预知操作需要多长时间。比如网络请求、搜索、等待锁释放。

**类比**：微波炉加热——你不知道要多久转完，但那个旋转的光盘告诉你"我还活着"。

```
$ myapp deploy
⣾ 正在部署...  (3.2s)

$ myapp search "CLI设计"
⠙ 搜索中...
```

**实现原则**：
- 显示已等待时间（如 `3.2s`），给用户进度预期
- 如果超过 10 秒仍无进展，建议降级为更详细的进度提示
- 不要遮挡错误信息——如果操作失败，Spinner 应立刻停止并展示错误

**Python 示例（rich 库）**：

```python
from rich.console import Console
from time import sleep

console = Console()
with console.status("[bold green]部署中...") as status:
    sleep(5)  # 模拟耗时操作
```

### Progress Bar（进度条）—— 确定进度

**适用场景**：你能预估总工作量，或者至少能给出百分比。比如文件下载、批量处理、数据导入。

**类比**：烤箱烤蛋糕——你知道要烤30分钟，进度条告诉你还有多久。

```
$ myapp import large-dataset.csv
[████████████░░░░░░░░░░] 45/100  45%  ETA 12s  速率: 2.3MB/s
```

**实现原则**：
- 显示：已完成量 / 总量 / 百分比 / 预估剩余时间 / 速率
- 如果无法精确预估总量，但可以分阶段汇报，使用**增量进度条**
- 对超大文件（GB 级别），进度条的更新频率不要超过 10Hz（每100ms一次）

**JavaScript/Node.js 示例（cli-progress）**：

```javascript
const cliProgress = require('cli-progress');
const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
bar.start(total, 0);
// 在循环中更新
bar.update(current);
bar.stop();
```

### Step Indicator（步骤指示器）—— 多阶段流程

**适用场景**：操作包含多个明确的阶段步骤。比如 CI/CD 流水线、安装脚本、初始化流程。

**类比**：宜家家具组装说明书——步骤1/7: 安装桌腿 ✅ → 步骤2/7: 安装桌面 ⏳...

```
$ myapp setup
✓ 步骤 1/4: 检查环境依赖  (0.3s)
✓ 步骤 2/4: 创建配置文件  (0.1s)
⏳ 步骤 3/4: 初始化数据库  (2.1s...)
```

**实现原则**：
- 已完成步骤标 ✅ 或 ✓
- 当前步骤标 ⏳ 或 ➜
- 每步记录耗时，后续步骤给出累积时间
- 错误步骤标 ❌ 并显示失败详情，同时提供恢复命令

---

### 非 TTY 模式下自动禁用动画

**关键守则**：当输出被重定向到文件或管道时，必须禁用所有动画和转义序列。

```
$ myapp deploy > log.txt          # spinner 字符会污染日志
$ myapp deploy | grep "error"     # 转义序列会破坏管道
```

**检测方法**：

```python
import sys
if sys.stdout.isatty():
    # 启用 spinner / progress bar
    pass
else:
    # 改为纯文本日志输出
    pass
```

**降级策略**：

| 模式 | TTY 行为 | 非 TTY 行为 |
|------|----------|-------------|
| Spinner | 旋转动画 + 时间 | 逐行打印 `[3.2s] 部署中...` |
| Progress Bar | 实时渲染进度条 | 每10%打印一行 `45% - 12/100` |
| Step Indicator | 动态更新步骤状态 | 每步完成后打印一行 `[OK] 步骤 1/4` |

---

## 6.3 颜色与样式的使用守则

颜色让CLI从"黑白电报"变成"彩色电视"，但滥用颜色会适得其反。

### 语义化配色方案

建立一套一致的配色语义，让用户形成条件反射：

| 颜色 | 语义 | 使用场景 | 示例 |
|------|------|----------|------|
| 🔴 **红色** | 错误 | 致命错误、失败 | `错误：连接超时` |
| 🟢 **绿色** | 成功 | 操作完成、创建成功 | `✓ 部署成功` |
| 🟡 **黄色** | 警告 | 潜在问题、弃用提示 | `⚠ 此API将在v2.0废弃` |
| 🔵 **蓝色/青色** | 信息 | 提示、路径、链接 | `→ 更多信息：https://docs.example.com` |
| ⚪ **灰色/暗淡** | 次要 | 元数据、时间戳、调试 | `[2024-01-15 14:30:22]` |

**反例（❌）**：用绿色表示错误，用红色表示成功——违反直觉，用户困惑。

**正例（✅）**：红色永远表示需要用户注意的问题，绿色永远表示正面的确认。

### 支持 `NO_COLOR` 和 `--no-color`

`NO_COLOR` 是一个行业标准（[no-color.org](https://no-color.org/)）：如果环境中存在 `NO_COLOR` 变量（无论值是什么），应用不应输出 ANSI 颜色代码。

```bash
# 用户可以通过环境变量全局禁用颜色
$ export NO_COLOR=1
$ myapp deploy
# 所有输出均为纯文本
```

此外，每个 CLI 应提供 `--no-color` / `--color` 参数，优先级高于环境变量：

| 设置 | 效果 |
|------|------|
| 未设 `NO_COLOR`，未传 `--no-color` | 根据 TTY 自动判断 |
| `export NO_COLOR=1` | 禁用颜色（全局） |
| `myapp --no-color` | 禁用颜色（单次） |
| `myapp --color=always` | 强制启用颜色（即使非 TTY） |

### 色盲友好设计

全球约 8% 的男性和 0.5% 的女性有某种形式的色盲。最常见的是红绿色盲（deuteranopia）。

**四原则**：
1. **不要仅靠颜色传达信息**——始终配合符号或文字
   - ❌ 仅用红色文字表示错误
   - ✅ `错误：`（红色文字 + "错误："前缀）
2. **使用符号辅助**：✓ / ✗ / ⚠ / ℹ
3. **避免红绿对比组合**——这是色盲用户最难区分的组合。如果需要突出对比，改用红/蓝或红/黄
4. **测试你的配色**：使用工具如 [Color Oracle](https://colororacle.org/) 或 [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)

**对比**：
```
# 仅靠颜色（❌）
[32m成功[0m   ← 绿色文字，色盲用户可能完全看不出不同

# 颜色 + 符号（✅）
[32m✓ 成功[0m  ← 即使看不出绿色，"✓"符号也传达了正面信息
```

---

## 6.4 配置文件设计

好的CLI不只靠命令行参数，还需要持久化的配置。

### XDG Base Directory 规范

**核心原则**：不要弄乱用户的家目录。

[XDG Base Directory 规范](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) 定义了配置/数据/缓存文件的存放位置：

| 用途 | 环境变量 | 默认路径 | 示例 |
|------|----------|----------|------|
| 配置文件 | `$XDG_CONFIG_HOME` | `~/.config` | `~/.config/myapp/config.toml` |
| 数据文件 | `$XDG_DATA_HOME` | `~/.local/share` | `~/.local/share/myapp/db.sqlite` |
| 缓存文件 | `$XDG_CACHE_HOME` | `~/.cache` | `~/.cache/myapp/thumbnails/` |

**反例（❌）**：在 `~/` 下直接创建 `.myapprc`、`.myapp_history`、`.myapp_cache/`——散落一地，用户想清理都不知道哪些文件属于你的应用。

**正例（✅）**：

```
~/.config/myapp/config.toml    # 配置文件
~/.local/share/myapp/           # 数据文件
~/.cache/myapp/                 # 缓存文件
```

### 配置优先级和合并策略

配置值可以从多个来源获取，优先级从高到低：

```
1. 命令行参数（最高优先级）
2. 环境变量（如 MYAPP_HOST=localhost）
3. 当前目录配置文件（./.myapp.toml）
4. 用户配置文件（~/.config/myapp/config.toml）
5. 系统级配置文件（/etc/myapp/config.toml）
6. 内置默认值（最低优先级）
```

**合并策略**：
- 深层合并（deep merge）：不是简单覆盖整个文件，而是按字段合并
- 如果命令参数设置了 `host`，但没设置 `port`，应从配置文件中读取 `port` 值
- 数组建议使用替换而非合并（否则容易出现重复）

### 支持 `--config` 参数覆盖路径

允许用户指定完全不同的配置文件路径：

```bash
$ myapp --config /path/to/custom-config.toml deploy
```

使用 `--config` 时，跳过所有默认配置路径的查找，直接加载指定文件。

### 配置文件格式推荐

| 格式 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| TOML | 简洁、可读性强、标准规范 | 不支持复杂嵌套 | ✅ **最推荐** |
| YAML | 支持复杂结构、广泛使用 | 缩进敏感、安全风险（`!!python/object`） | 复杂配置 |
| JSON | 程序解析友好 | 不支持注释、可读性差 | 机器生成配置 |
| INI | 熟悉、简单 | 表达能力有限 | 遗留系统 |

---

## 6.5 幂等性与可组合性

这两个概念来自函数式编程和系统设计，但在CLI设计中同样重要。

### 幂等操作：重复执行不改变结果

**定义**：对同一个操作执行一次和执行多次，系统的最终状态是一样的。

**类比**：电灯开关——按一下开灯，再按一下关灯（这是非幂等的）。但 "把灯设为开" ——执行一次是开，执行一百次也是开（幂等）。

**CLI中的幂等设计**：

```bash
# 非幂等（❌）
$ myapp create-user alice    # 第一次成功
$ myapp create-user alice    # 第二次报错 "用户已存在"

# 幂等（✅）
$ myapp ensure-user alice    # 第一次创建用户
$ myapp ensure-user alice    # 第二次检查已存在，不做任何操作，返回成功
```

**为什么重要**：
- 脚本中执行时，网络中断可能导致重试——幂等命令可以安全重试
- CI/CD 流水线中重复执行不会产生副作用
- AI Agent 调用时不确定是否已执行过——幂等命令让Agent安全使用

**幂等性设计模式**：

| 操作类型 | 非幂等方式 | 幂等方式 |
|----------|------------|----------|
| 创建 | `create` | `ensure` / `apply` |
| 配置 | `set` | `ensure` / `apply` |
| 注册 | `register` | `upsert` |
| 安装 | `install` | `ensure-installed` |

### stdin/stdout 管道模式

CLI 的真正威力不在单独使用，而在于**组合**——通过 Unix 管道将多个工具连成一条处理链。

**设计原则**：
1. 默认输出到 stdout（而非直接写到文件）
2. 输出格式应为纯文本、易于解析
3. 如果输出包含结构化数据，提供 `--json` 选项
4. 错误信息输出到 stderr，不污染 stdout 管道

```bash
# 可组合的管道链
$ myapp list --json | jq '.[] | select(.status == "active")' | myapp batch-process
```

**反例（❌）**：

```bash
$ myapp list
[INFO] 正在加载数据...     ← 日志混入 stdout
[INFO] 加载完成
ID: 1, Name: alice         ← 实际数据
ID: 2, Name: bob

$ myapp list | grep "alice"
[INFO] 正在加载数据...     ← grep 也会匹配这一行！
```

**正例（✅）**：

```bash
$ myapp list
1  alice  active
2  bob    inactive

$ myapp list | awk '$3 == "active" {print $2}'
alice
```

### `--json` 输出作为机器接口

提供 `--json` 输出选项，使 CLI 可以同时服务于人类和机器：

```bash
# 人类可读（默认）
$ myapp status
项目状态: 运行中
版本: v2.3.1
内存使用: 256MB / 1024MB

# 机器可读（--json）
$ myapp status --json
{"status":"running","version":"2.3.1","memory_mb":{"used":256,"total":1024}}
```

**设计准则**：
- `--json` 输出应结构稳定（字段名不变，类型固定）
- 包含 `exit_code` 或 `success` 字段，便于脚本判断
- 错误时返回结构化错误信息而非裸字符串
- 遵守 JSON Schema 规范，方便下游程序校验

---

# Chapter 7: 社区资源精选

优质的CLI设计资源分散在网络各处。本章精选10个最有价值的资源，按统一模板整理，方便你按需查阅。

---

## 7.1 clig.dev 中文翻译版

| 属性 | 内容 |
|------|------|
| **链接** | [GitHub - SunBK201/clig.dev-zh](https://github.com/SunBK201/clig.dev-zh) |
| **适合人群** | 所有CLI开发者（入门至中级） |
| **内容概览** | 对原版 clig.dev（Command Line Interface Guidelines）的完整中文翻译，覆盖CLI设计的各个方面：帮助信息、错误处理、输出格式、标志命名等。 |
| **为什么值得看** | clig.dev 是CLI设计领域的"圣经级"指南，由 Google 和 Heroku 的工程师共同撰写。中文版降低了阅读门槛，并保留了大量原文示例。 |
| **一句话评价** | "CLI设计师的第一本必读书，终于有了高质量中文版。" |
| **学到的技能点** | 标志命名规范、帮助系统设计、错误信息写法、退出码约定 |

---

## 7.2 知乎专栏：开发命令行工具的12个最佳实践

| 属性 | 内容 |
|------|------|
| **链接** | [知乎 - 开发命令行工具的12个最佳实践](https://zhuanlan.zhihu.com/p/352302729) |
| **适合人群** | 初中级CLI开发者，Node.js/Go/Python 用户 |
| **内容概览** | 从工具选型到发布运维，覆盖CLI开发全流程。涉及 CLI 框架选择（Commander.js, Cobra, Click）、参数解析、帮助生成、测试策略、自动补全等。 |
| **为什么值得看** | 实操性强，每个最佳实践都配有代码示例，可以直接参考使用。不空谈理论，手把手教。 |
| **一句话评价** | "接地气的实战指南，从零开始带你做出专业CLI。" |
| **学到的技能点** | 框架选型、帮助系统构造、自动补全集成、测试策略 |

---

## 7.3 掘金：从零构建现代CLI工具（Node.js版）

| 属性 | 内容 |
|------|------|
| **链接** | [掘金 - 从零构建现代CLI工具](https://juejin.cn/post/6844904035063119879) |
| **适合人群** | JavaScript/TypeScript 开发者 |
| **内容概览** | 用 Node.js 从零搭建一个完整的CLI工具：项目结构、参数解析（commander/yargs）、交互式输入（inquirer）、配色（chalk）、spinner（ora）、自动更新等。 |
| **为什么值得看** | 保姆级教程，代码可直接复用。npm 生态的工具链选择对 JS 开发者尤为实用。 |
| **一句话评价** | "Node.js CLI开发的百科全书式教程。" |
| **学到的技能点** | Node.js CLI 工具链、交互式输入、配色方案、Spinner 集成、自动更新机制 |

---

## 7.4 掘金：如何把CLI做得专业（七个维度）

| 属性 | 内容 |
|------|------|
| **链接** | [掘金 - 如何把CLI做得专业](https://juejin.cn/post/6844904022566338573) |
| **适合人群** | 有一定CLI开发经验，追求"专业感"的开发者 |
| **内容概览** | 从七个维度分析专业CLI的特征：帮助信息、错误提示、进度展示、配置管理、退出码、管道友好、国际化。每维度配合正反例对比。 |
| **为什么值得看** | 重点在"专业感"——不是如何实现功能，而是如何让用户觉得"这个工具做得很用心"。很多细节是其他教程不会提到的。 |
| **一句话评价** | "从'能用'到'好用'的最佳进阶读物。" |
| **学到的技能点** | 专业化细节处理、退出码设计、国际化支持、管道友好设计 |

---

## 7.5 面向Agent的CLI最佳设计实践（liduos.com）

| 属性 | 内容 |
|------|------|
| **链接** | [liduos.com - 面向Agent的CLI最佳设计实践](https://liduos.com/design-best-practices-of-cli-for-agent.html) |
| **适合人群** | 关注 AI Agent 和 LLM 集成的前沿开发者 |
| **内容概览** | 探讨AI Agent作为CLI新用户的场景和设计要求。涵盖：结构化输出、幂等性、错误码约定、非交互模式、参数完整性约束等。 |
| **为什么值得看** | 这是目前中文社区鲜有的、从 AI Agent 视角讨论CLI设计的文章。如果你在构建 Agent 使用的工具，这是必读材料。 |
| **一句话评价** | "AI时代的CLI设计宣言，领先行业至少一年。" |
| **学到的技能点** | Agent-native CLI设计、结构化输出、幂等API设计、非交互模式 |

---

## 7.6 Atlassian: 10 Design Principles for Delightful CLIs

| 属性 | 内容 |
|------|------|
| **链接** | [Atlassian Blog - 10 Design Principles for Delightful CLIs](https://www.atlassian.com/blog/developer/10-design-principles-for-delightful-clis) |
| **适合人群** | 中高级CLI设计师，产品思维型开发者 |
| **内容概览** | Atlassian 内部总结的10条CLI设计原则：用户优先、渐进式披露、一致胜过完美、失败优雅、可组合性等。每条原则配真实案例（Bitbucket CLI, Jira CLI）。 |
| **为什么值得看** | 来自大型软件公司的工程实践，有真实的用户反馈和数据支撑。不只是理论，更是经过市场验证的经验总结。 |
| **一句话评价** | "大厂CLI设计的第一手经验，含金量极高。" |
| **学到的技能点** | 渐进式信息设计、一致性原则、用户研究驱动的CLI设计 |

---

## 7.7 Thoughtworks: Elevate Developer Experiences with CLI Design

| 属性 | 内容 |
|------|------|
| **链接** | [Thoughtworks - Elevate Developer Experiences with CLI Design](https://www.thoughtworks.com/insights/blog/developer-experience/elevate-developer-experiences-with-cli-design) |
| **适合人群** | 关注开发者体验（DX）的产品经理和工程师 |
| **内容概览** | 从开发者体验角度分析CLI设计：认知负荷、信息架构、交互流畅度、可发现性。提出CLI开发者的"移情设计"理念。 |
| **为什么值得看** | Thoughtworks 以技术咨询著称，文章视角独特——不只是"怎么做"，更是"为什么这样做对用户更好"。 |
| **一句话评价** | "把CLI设计上升到开发者体验的高度，格局打开。" |
| **学到的技能点** | 开发者体验设计、认知负荷管理、移情设计方法、信息架构 |

---

## 7.8 Reddit讨论帖：最佳/最差CLI评选

| 属性 | 内容 |
|------|------|
| **链接** | [Reddit r/programming - Best and worst CLI designs](https://www.reddit.com/r/programming/comments/15w6vcx/best_and_worst_cli_designs/) |
| **适合人群** | 所有CLI使用者/设计者（推荐入门者阅读评论） |
| **内容概览** | Reddit 社区的集体智慧：用户评选的最佳CLI（git, ffmpeg, docker, curl）和最差CLI（tar, npm, svn），以及大量"为什么"的深度评论。 |
| **为什么值得看** | 这是最真实的用户反馈集。CLI设计者的自我感觉和用户实际感受之间往往有差距。这篇讨论帖让你看清真实世界中用户到底喜欢/讨厌什么。 |
| **一句话评价** | "CLI设计的照妖镜——用户的真实吐槽比任何理论都更有说服力。" |
| **学到的技能点** | 用户真实痛点的第一手资料、常见CLI的反面教材、社区共识的设计标准 |

---

## 7.9 Heng Li: Designing a CLI

| 属性 | 内容 |
|------|------|
| **链接** | [Heng Li's Blog - Designing a CLI](https://lh3.github.io/2021/10/10/designing-a-cli) |
| **适合人群** | 生物信息学领域及科学计算CLI开发者 |
| **内容概览** | 著名生物信息学工具（BWA, SAMtools, minimap2）作者李恒的CLI设计心得。强调：简单优于复杂、输入输出明确、版本一致性、最小惊喜原则。 |
| **为什么值得看** | 李恒的工具被全球数万科学家每天使用，他的设计理念经过极端严苛的场景检验。科学计算CLI的用户群体对稳定性和一致性要求极高。 |
| **一句话评价** | "大师级的简约——看李恒如何用最少的API做最多的事。" |
| **学到的技能点** | 最小惊喜原则、版本管理策略、科学计算CLI设计模式、输入输出约定 |

---

## 7.10 Kevin Newton: Exploring CLI Best Practices

| 属性 | 内容 |
|------|------|
| **链接** | [Kevin Newton - Exploring CLI Best Practices](https://kddnewton.com/2024/04/05/exploring-cli-best-practices.html) |
| **适合人群** | 追求高质量代码和用户体验的CLI开发者 |
| **内容概览** | Kevin Newton（Ruby核心贡献者，Syntax Tree等工具作者）深入分析CLI最佳实践：子命令设计、配置处理、退出码约定、处理信号、帮助系统等。 |
| **为什么值得看** | 作者有丰富的语言工具开发经验，文章深入但不晦涩。对信号处理、退出码等细节的讨论尤为出色，这些是其他资料常忽略的。 |
| **一句话评价** | "Ruby社区的CLI设计心得，细节控的最爱。" |
| **学到的技能点** | 信号处理（SIGINT/SIGTERM）、退出码最佳实践、子命令路由设计、配置加载策略 |

---

# Chapter 8: 业内评价与案例分析

理论说再多，不如看看现实世界中那些"封神"或"翻车"的CLI。本章分析四个经典CLI的设计哲学，从中提炼可学习的经验。

## 8.1 Git CLI —— "又爱又恨"的行业标准

### 定位

Git 是版本控制的行业标准，也是许多开发者最早接触的"专业CLI"。它的设计深刻地影响了后来的所有CLI工具。

### 为什么"爱"

1. **一致的子命令模型**：`git <verb> <object>` 模式贯穿始终
   ```
   git add file
   git commit
   git push origin main
   git log --oneline
   ```
   一旦学会这个模式，整个工具的使用方法就一目了然。

2. **强大的管道组合**：Git 的输出默认就是可管道的。
   ```bash
   git log --oneline | head -5
   git branch --merged | grep -v main | xargs git branch -d
   git diff --name-only | grep '\.py$' | xargs pylint
   ```

3. **庞大的社区生态**：`git merge`、`git rebase`、`git stash` 等高级命令，虽然复杂，但成为了行业共同语言。

### 为什么"恨"

1. **不一致的标志命名**：
   - `git log` 用 `--oneline`，但 `git diff` 没有 `--oneline`
   - `git checkout` 的 `-b` 是创建分支，但 `git switch` 用 `-c`
   - `-v` 在有些子命令下是 verbose，在有些子命令下是版本号

2. **命令爆炸**：Git 有超过 150 个子命令，很多命令的功能重叠（`git checkout` 可以切换分支、恢复文件、创建分支——"一个命令做三件事"是违反了单一职责原则的）。

3. **令人困惑的错误信息**：
   ```
   $ git push
   fatal: The current branch master has no upstream branch.
   ```
   对于新手，"upstream branch"是什么意思？正确的命令是什么？Git 的早期版本不会告诉你，直到后来的版本才加了提示。

4. **暂存区（staging area）的认知负担**：`working directory → staging area → repository` 三层模型对新手不友好。

### 学到的经验

| Git 做对了 | Git 做错了 |
|------------|------------|
| 子命令模型一致性 | 命令功能重叠（chekout做三件事） |
| 管道友好输出 | 错误信息晦涩 |
| 渐进式学习曲线 | flag命名不一致 |
| 丰富的配置系统 | 暂存区概念复杂 |
| 强大的别名机制 | 默认行为有时不安全（`git push --force`） |

**教训**：功能强大 ≠ 设计优秀。Git 的成功更多来自其底层数据模型的优雅，而非CLI设计本身。后来的工具（如 `gh`、`docker`）从 Git 的缺点中吸取了很多教训。

---

## 8.2 Docker CLI —— 子命令树模型的成功实践

### 定位

Docker CLI 是目前最成功的容器管理CLI之一，也是"子命令树"模式的标杆。

### 设计亮点

1. **逻辑分组清晰**：
   ```
   docker container run      # 容器管理
   docker image ls           # 镜像管理
   docker network create     # 网络管理
   docker volume inspect     # 卷管理
   docker system prune       # 系统清理
   ```
   每个资源类型（container/image/network/volume）构成一级子命令，操作动词（run/ls/create/inspect/prune）构成二级子命令。这种"名词-动词"结构让命令自然可发现。

2. **别名字系统**：大部分命令提供缩写。
   ```
   docker container run = docker run       # 省略 container
   docker container ls   = docker ps       # 使用传统名称
   docker image ls       = docker images   # 使用传统名称
   ```
   既保留了完整路径的可发现性，又提供了快捷方式。

3. **优秀的人体工学**：
   - `docker run -it` 交互式运行
   - `docker run -d` 后台运行
   - `docker run --rm` 自动删除
   这些 flag 是经过深度设计的，缩写在语义上自然且容易记忆。

4. **错误信息相对友好**：
   ```
   $ docker run non-existent-image
   Unable to find image 'non-existent-image:latest' locally
   docker: Error response from daemon: pull access denied for non-existent-image, repository does not exist or may require 'docker login'.
   ```
   不仅指出错误，还给出了可能的解决方案（`docker login`）。

### 值得学习的点

| 特性 | 为什么好 | 可借鉴到自己的CLI |
|------|----------|-------------------|
| 名词-动词分组 | 命令结构可预测 | 资源型CLI使用 `<resource> <action>` |
| 别名系统 | 新手和专家各取所需 | 提供完整路径和快捷方式 |
| 人性化flag | 常用操作一眼记住 | 设计flag时考虑"这个操作用户每天做吗？" |
| 错误信息+建议 | 用户不会卡住 | 始终在错误信息后附上建议 |

---

## 8.3 Heroku CLI —— SaaS CLI的标杆

### 定位

Heroku CLI 是为 Heroku 云平台设计的CLI，是 SaaS/PaaS 类CLI的早期标杆。许多后来的平台CLI（Vercel, Netlify, Railway）都受其影响。

### 设计亮点

1. **自然语言的命令**：
   ```
   heroku create app-name        # 创建应用（读作"Heroku create app"）
   heroku logs --tail            # 查看日志（读作"Heroku logs tail"）
   heroku config:set KEY=value   # 设置配置
   heroku pg:info                # 查看PostgreSQL信息
   ```
   命令读起来像英文句子，而不是晦涩的缩写。

2. **交互式回退（Interactive fallback）**：
   当必要参数缺失时，Heroku CLI 会根据上下文自动判断，或进入交互模式询问用户。
   ```
   $ heroku create
   # 如果没有指定app名称，自动生成一个随机名称
   Creating app... done, ⬢ thawing-inlet-12345
   ```
   这让快速原型开发时非常顺畅。

3. **addon 系统的子命令扩展**：
   通过 `heroku addons:create` 集成第三方服务，插件化的设计让生态系统蓬勃发展。

4. **连贯的--json输出**：几乎所有命令都支持 `--json`，方便自动化。

### 值得学习的点

| 特性 | 为什么好 | 可借鉴到自己的CLI |
|------|----------|-------------------|
| 自然语言命令 | 降低学习曲线 | 命令命名先读一遍，看是否像自然语言 |
| 交互式回退 | 减少认知负担 | 缺失参数时智能推断或主动询问 |
| 插件化扩展 | 生态系统可生长 | 考虑 CLI 的扩展机制 |
| 全命令--json | 脚本友好 | 从第一天就设计结构化输出 |

---

## 8.4 gh CLI (GitHub CLI) —— 现代CLI的设计取舍

### 定位

GitHub 官方CLI，旨在将 GitHub 工作流带入终端。它代表了2019年之后诞生的新一代CLI的设计风格。

### 设计取舍

1. **"CLI is for humans before machines"**：
   - 默认输出是精美的表格和可读文本，而不是GitHub API的原始JSON
   - 色彩丰富但不刺眼
   - 但所有命令都提供 `--json` 标志

2. **交互式命令的巧妙应用**：
   ```
   $ gh pr create
   # 如果没有传参，gh会交互式地询问：
   # - 哪个分支？
   # - 标题是什么？
   # - 是否创建草稿PR？
   ```
   这是**渐进式披露**的绝佳例子：新手不需要记住所有flag，工具会引导他们完成操作；专家可以使用 `gh pr create --title "..." --body "..." --draft` 跳过交互。

3. **子命令设计一致性**：
   ```
   gh pr create    # PR操作
   gh pr review    # PR操作
   gh pr merge     # PR操作
   gh issue list   # Issue操作
   gh issue view   # Issue操作
   ```
   `gh <资源> <操作>` 的模式清晰且可扩展。

4. **配置的现代处理**：
   - 支持 `~/.config/gh/config.yml`（XDG兼容）
   - 支持 `GH_HOST` 等环境变量
   - 有 `gh config set` 命令，不需要手动编辑配置文件

### 值得学习的点

| 特性 | 为什么好 | 可借鉴到自己的CLI |
|------|----------|-------------------|
| 人类优先+JSON备选 | 兼顾新手和自动化 | 默认人类可读，`--json` 提供机器接口 |
| 交互式回退 | 降低入门门槛 | 缺失参数时进入引导模式 |
| 资源-操作命名 | 一致性高 | 坚持 `<resource> <action>` 模式 |
| 现代配置管理 | 用户无痛配置 | 提供配置子命令，不依赖手动编辑 |

---

## 8.5 现代CLI工具流行度对比表

以下数据为2025年第一季度数据，帮你了解当前CLI生态格局。

| 工具 | 语言 | 发布时间 | GitHub Stars | 设计风格 |
|------|------|----------|-------------|----------|
| **git** | C | 2005 | 53k+ | 子命令模型，功能强大但UX参差 |
| **docker** | Go | 2013 | 29k+ | 名词-动词树，行业标杆 |
| **kubectl** | Go | 2014 | 28k+ | 资源CRUD，复杂但一致 |
| **gh** | Go | 2019 | 13k+ | 现代交互式，人类优先 |
| **pnpm** | JS | 2017 | 30k+ | 简洁渐进，npm替代 |
| **uv** | Rust | 2023 | 36k+ | 极速Python包管理 |
| **ripgrep (rg)** | Rust | 2016 | 49k+ | 简洁专注单一任务 |
| **fd** | Rust | 2017 | 35k+ | 简单替代find |
| **bat** | Rust | 2017 | 51k+ | cat的现代替代 |
| **zoxide** | Rust | 2020 | 25k+ | AI增强cd |
| **eza** | Rust | 2023 | 15k+ | ls现代替代 |

**趋势观察**：
1. **Rust崛起**：新一代CLI工具大量使用Rust开发（ripgrep, fd, bat, uv, zoxide, eza），Rust的性能和内存安全在CLI场景下表现出色
2. **Go稳定**：企业级CLI（docker, kubernetes, gh）偏好Go，编译速度快，跨平台部署简单
3. **专注**：最受欢迎的CLI通常只做好一件事（ripgrep搜索，fd查找文件，bat查看文件）
4. **现代替代**：大量新工具在做"更好的X"——更好的find（fd），更好的cat（bat），更好的cd（zoxide）

---

## 8.6 CLI工程师岗位的市场信号

如果你想把CLI设计作为职业方向，以下是从招聘市场提炼的信号。

### 常见技能要求

**必备技能**：
- 至少精通一门系统级语言（Go / Rust / C / Zig）
- 命令行工具开发经验（flag解析、子命令路由、帮助系统）
- 熟悉终端ANSI转义序列、TTY控制
- CI/CD集成经验（GitLab CI / GitHub Actions）
- Shell脚本能力（bash / zsh）
- 跨平台发布经验（Linux / macOS / Windows）

**加分技能**：
- 终端UI库经验（tui-rs, bubbletea, rich, prompt_toolkit）
- 性能优化经验（处理超大文件的流式输出）
- 包管理工具维护经验（Homebrew / apt / npm）
- 文档生成系统（man pages / --help自动生成）
- AI/LLM集成经验（结构化输出给Agent消费）

### 薪资参考（2025年，美国市场）

| 级别 | 薪资范围（USD） | 典型公司 |
|------|-----------------|----------|
| 初级 CLI 工程师 | $90K - $130K | 中小型SaaS公司 |
| 中级 CLI 工程师 | $130K - $180K | 中型科技公司、DevOps工具公司 |
| 高级 CLI/开发者体验工程师 | $180K - $250K+ | FAANG、顶级DevOps公司 |
| CLI 平台架构师 | $250K - $350K+ | 大型云平台、工具链公司 |

### 如何进入这个领域

1. **贡献开源**：给 ripgrep / fd / bat / gh 等工具提PR，从修复bug开始
2. **创建自己的CLI工具**：解决自己日常工作中的痛点，发布到 crates.io / npm / PyPI
3. **参加CLI jam / hackathon**：短期密集开发的绝佳练习
4. **写CLI设计文章**：建立个人品牌，输出你对CLI设计的思考

---

# Chapter 9: 避坑指南

十五年的CLI开发生涯教会我们一件事：**大多数"用户不友好"不是设计问题，而是疏忽**。CLI的坑往往非常小，小到容易忽略，但累积起来就是"这个工具不好用"的直观感受。

本章列出10个最常见的陷阱，每个都包含：现象 → 原因 → 修复步骤。

---

## 陷阱1：把堆栈跟踪丢给用户

**现象**：
```
$ myapp parse data.csv
Traceback (most recent call last):
  File "myapp/cli.py", line 87, in parse
    result = process(data)
  File "myapp/parser.py", line 34, in process
    value = row['amount'] * 2
TypeError: can't multiply sequence by non-int of type 'str'
```

**原因**：开发者直接抛出了未捕获的异常，或者用了 `--debug` 模式作为默认输出。

**修复步骤**：
1. 在顶层 main() 函数中包裹异常捕获
2. 将技术异常映射为用户可读的错误信息
3. 完整堆栈只有在 `--debug` / `--verbose` 时才展示

```python
def main():
    try:
        # ... 业务逻辑
    except Exception as e:
        if args.debug:
            traceback.print_exc()
        else:
            sys.exit(f"错误：数据解析失败 — {str(e)}")
```

---

## 陷阱2：缺少退出码

**现象**：
```bash
$ myapp deploy
部署失败：连接超时
$ echo $?
0   ← 明明失败了却返回0！
```

**原因**：CLI 没有设置退出码，默认使用 Python/Node 的 0（成功）。

**修复步骤**：
1. 约定退出码语义：
   - `0` = 成功
   - `1` = 一般错误
   - `2` = 参数/用法错误（可复用 sysexits.h 的 `EX_USAGE`）
   - 其他自定义码用于特定场景
2. 在退出路径上显式调用 `sys.exit(code)` 或 `process.exit(code)`

```python
if error:
    sys.exit(1)   # 一般错误
elif args_error:
    sys.exit(2)   # 用法错误
sys.exit(0)       # 成功
```

**为什么重要**：CI/CD 脚本依赖退出码判断是否继续执行。如果退出码始终为 0，错误会被掩盖。

---

## 陷阱3：隐式副作用

**现象**：
```bash
$ myapp config set theme=dark
# 没有任何输出，静默完成
# 用户不确定是否成功
```

**原因**：CLI 执行了操作但没有向用户确认。

**修复步骤**：
1. 所有写入操作（创建/修改/删除）后输出确认信息
2. 提供 `--quiet` / `-q` 让脚本调用时静默
3. 破坏性操作（删除/覆盖）前先提示确认

```bash
# 好：确认信息
$ myapp config set theme=dark
✓ 配置已更新（theme = dark）

# 更好：变更前后对比
$ myapp config set theme=dark
✓ 配置已更新：
  - theme: light → dark

# 破坏性操作前确认
$ myapp delete database
⚠ 警告：这将删除数据库 "myapp-db"！此操作不可撤销。
确认继续？ [y/N]
```

---

## 陷阱4：不一致的flag命名

**现象**：
```bash
$ myapp -v           # verbose
$ myapp --version    # 版本号（长格式）
$ myapp -V           # 版本号（短格式，注意大写V）
```
用户经常混淆 `-v` 和 `-V`，一不留神就打错了。

**原因**：flag命名没有遵循约定，或者同一个缩写被映射到不同含义。

**修复步骤**：
1. 遵守 POSIX/GNU 约定：
   - `-v` = verbose（小写）
   - `-V` = version（大写）
   - `-o` = output（小写）
   - `-f` = force/format（小写）
   - `-q` = quiet（小写）
2. 一个缩写只对应一个含义
3. 如果缩写冲突，优先保留更常用的含义，替另一个含义换缩写

**正例对比**：

| 含义 | 不推荐的写法 | 推荐的写法 |
|------|-------------|------------|
| verbose | `--verbose` / `-v` | `--verbose` / `-v` |
| version | `--version` / `-v` ❌ | `--version` / `-V` ✅ |
| output | `-o` / `-O` 混淆 | `--output` / `-o` |
| force | `--force` / `-f` | `--force` / `-f` |
| format | `--format` / `-f` ❌ | `--format` / `-F` ✅ |

---

## 陷阱5：颜色无法关闭

**现象**：
```bash
$ myapp status | cat
←[32m✓←[0m 运行中   ← ANSI 转义序列污染了输出
```

**原因**：CLI 默认强制输出颜色，且不支持 `NO_COLOR` 环境变量或 `--no-color` 参数。

**修复步骤**：
1. 检查 `NO_COLOR` 环境变量（只要存在就禁用颜色）
2. 提供 `--no-color` / `--color` 参数
3. 非 TTY（管道/重定向）时默认禁用颜色
4. 使用专业的颜色库（支持自动检测的）

```python
import os
import sys

def should_use_color(args):
    if args.no_color:
        return False
    if args.color == 'always':
        return True
    if 'NO_COLOR' in os.environ:
        return False
    return sys.stdout.isatty()
```

---

## 陷阱6：日志信息混入stdout

**现象**：
```bash
$ myapp list | grep "alice"
[INFO] 正在加载数据...     ← 日志信息污染了管道
[INFO] 加载完成
alice  1234
```

**原因**：所有输出都写到了 stdout，包括日志/调试信息。

**修复步骤**：
1. 日志/状态信息写 stderr（`sys.stderr` / `console.error()` / `log.Error()`）
2. 只有实际数据写 stdout
3. 使用合适的日志级别（INFO/DEBUG 只在不干扰时显示）

```python
# Python 示例
import sys

def main():
    print("alice  1234", file=sys.stdout)     # 数据 → stdout
    print("日志：加载完成", file=sys.stderr)   # 日志 → stderr
```

```bash
# 用户使用体验
$ myapp list | grep "alice"      # 管道正常工作
alice  1234

$ myapp list 2>/dev/null         # 用户选择忽略日志
alice  1234
```

---

## 陷阱7：帮助系统不完善

**现象**：
```bash
$ myapp --help
Usage: myapp [OPTIONS] COMMAND
```

就这？没有子命令列表？没有参数说明？没有示例？

**原因**：使用了框架的默认帮助生成器，没有自定义帮助内容。

**修复步骤**：
1. **`-h`**（精简模式）：只显示最常用的命令和参数
2. **`--help`**（完整模式）：所有命令、参数、说明、示例
3. 确保帮助系统的结构：
   ```
   USAGE:
     myapp <command> [options] [arguments]
   
   COMMANDS:
     create    创建新资源
     list      列出所有资源
     delete    删除指定资源
   
   GLOBAL OPTIONS:
     -h, --help         显示帮助信息
     -v, --verbose      详细输出模式
     --version          显示版本号
     --no-color         禁用颜色输出
   
   EXAMPLES:
     myapp create --name my-project
     myapp list --format json
   
   MORE HELP:
     myapp help <command>   查看子命令详情
   ```
4. 为每个子命令提供独立的帮助信息：`myapp create --help`
5. 包含至少2-3个实用示例

---

## 陷阱8：大文件处理没有进度反馈

**现象**：
```bash
$ myapp import 5GB-dataset.csv
# 没有任何输出，命令行卡住3分钟
# 用户以为程序崩溃了
```

**原因**：没有实现进度反馈，用户无法判断程序状态。

**修复步骤**：
1. 预估总工作量（文件大小/行数/步骤数），显示进度条
2. 如果无法预估，使用 spinner 并显示"已处理 X MB"
3. 设置超时检测，如果进度停滞超过 N 秒，显示警告
4. 非 TTY 模式下降级为定期日志输出

```bash
# 好的做法
$ myapp import 5GB-dataset.csv
[████████░░░░░░░░] 42% | 2.1GB/5.0GB | ETA 1m23s | 12.5MB/s
```

---

## 陷阱9：静默失败

**现象**：
```bash
$ myapp backup
# 没有任何输出
# 实际上备份因权限不足而失败，但CLI没有报告
```

**原因**：操作失败时没有输出错误信息，也没有设置非零退出码。代码中用了 `try...except...pass` 或 "fail silently" 模式。

**修复步骤**：
1. 在任何失败路径上输出明确错误信息
2. 始终设置合理的退出码
3. 对于非关键性失败（如可选功能），输出 warning 而非忽略
4. 审计所有异常捕获代码，确保没有空的 `except: pass`

```python
# 坏（静默失败）
try:
    do_backup()
except PermissionError:
    pass   # ← 静默忽略

# 好（明确报告）
try:
    do_backup()
except PermissionError as e:
    print(f"错误：备份失败 — 权限不足（{e}）", file=sys.stderr)
    sys.exit(1)
```

---

## 陷阱10：配置文件不遵循XDG规范

**现象**：
```bash
$ ls ~/
.myapprc  .myapp_history  .myapp_cache/  .myapp_config.json
```

用户在清理家目录时完全不清楚哪些文件属于哪个应用。

**原因**：CLI直接在 `~/` 下创建点文件，没有使用 XDG Base Directory 规范。

**修复步骤**：
1. 使用 `$XDG_CONFIG_HOME/myapp/`（默认 `~/.config/myapp/`）存配置
2. 使用 `$XDG_DATA_HOME/myapp/`（默认 `~/.local/share/myapp/`）存数据
3. 使用 `$XDG_CACHE_HOME/myapp/`（默认 `~/.cache/myapp/`）存缓存
4. 提供自动迁移功能：检测旧路径并提示迁移

```python
import os

def get_config_dir():
    xdg_config = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config:
        return os.path.join(xdg_config, 'myapp')
    return os.path.expanduser('~/.config/myapp')

config_path = os.path.join(get_config_dir(), 'config.toml')
```

---

### 陷阱自查表

| # | 陷阱 | 检查清单 | 优先级 |
|---|------|---------|--------|
| 1 | 堆栈跟踪外露 | 是否捕获了所有顶层异常？是否通过 `--debug` 控制堆栈？ | 🔴 高 |
| 2 | 缺少退出码 | 所有失败路径是否设置了非零退出码？ | 🔴 高 |
| 3 | 隐式副作用 | 变更操作是否输出确认信息？破坏性操作是否有确认提示？ | 🟡 中 |
| 4 | flag命名不一致 | 缩写是否遵循约定？同一缩写是否对应唯一含义？ | 🟡 中 |
| 5 | 颜色无法关闭 | 是否支持 `NO_COLOR`？是否提供 `--no-color`？ | 🟡 中 |
| 6 | stdout混入日志 | 日志信息是否走 stderr？数据是否走 stdout？ | 🔴 高 |
| 7 | 帮助信息不完善 | `-h` 和 `--help` 是否有区分？是否有示例？ | 🟡 中 |
| 8 | 缺少进度反馈 | 耗时操作是否有 spinner/进度条？ | 🟡 中 |
| 9 | 静默失败 | 是否有未报告的失败？是否有空的 `except: pass`？ | 🔴 高 |
| 10 | 不遵循XDG | 配置是否放在 `~/.config/`？数据是否放在 `~/.local/share/`？ | 🟢 低 |

---

# Chapter 10: 进阶技巧与最佳实践

如果前面几章是"必知必会"，本章就是"锦上添花"——让用户觉得"这个工具真贴心"。

## 10.1 帮助系统的层次结构

好的帮助系统不是一层，而是三层递进。

### 第一层：`-h`（精简版）

适用于"我记得这个命令，就是想不起具体参数"的场景。

**特点**：
- 一屏之内（25行内）显示完
- 只包含最常用的命令和参数
- 不显示完整文档

```bash
$ myapp -h
用法: myapp <命令> [参数]

常用命令:
  create    创建新项目
  list      列出项目
  deploy    部署项目

常用选项:
  -h, --help     显示帮助
  -v, --verbose  详细模式
  --version      版本号

使用 "myapp --help" 查看完整帮助
使用 "myapp <命令> --help" 查看命令详情
```

### 第二层：`--help`（完整版）

适用于"第一次使用这个命令"或"需要了解全部功能"的场景。

**特点**：
- 完整展示所有命令、参数、全局选项
- 包含2-3个实用示例
- 列出子命令的 help 入口

```bash
$ myapp --help
# 完整的命令列表、选项、示例...
```

### 第三层：`man`（手册页）

适用于"需要详细的参考文档"的场景。

**特点**：
- 完整的手册页，包含：名称、概要、描述、选项、退出码、示例、文件、BUGS、SEE ALSO
- 使用 `man` 命令查看，支持搜索和分页
- 适合分发为 `.1` `.5` 等格式

```bash
$ man myapp
# 完整的 man page
```

### 子命令帮助

每个子命令应该有自己的帮助：

```bash
$ myapp create --help
用法: myapp create [选项] <项目名>

创建一个新的项目。

参数:
  项目名    项目名称（必填）

选项:
  -t, --template <模板>  使用模板（默认: default）
  -d, --dir <目录>       项目目录（默认: ./<项目名>）
  --private              创建私有项目
  -h, --help             显示帮助

示例:
  myapp create my-project
  myapp create my-project -t react --private
```

---

## 10.2 第一次运行体验（First-run Experience）

第一次运行体验决定了用户对你的CLI的**第一印象**。

### 为什么重要

用户可能会在第一次运行后的30秒内决定：
- "这个工具很棒，我要继续用" → 留下
- "太复杂了，不知道怎么用" → 放弃

### 好的首次体验设计

**第一步：欢迎信息**（简短、不啰嗦）

```bash
$ myapp
👋 欢迎使用 myapp v1.0.0！

  快速开始:  myapp init my-project
  帮助:      myapp --help
  文档:      https://docs.myapp.com
```

**第二步：配置引导**（如果需要）

```bash
$ myapp init my-project
首次运行，先完成配置：

✓ 步骤 1/2: 检测到 Git 已安装
✓ 步骤 2/2: 创建配置文件 ~/.config/myapp/config.toml

完成！接下来你可以：
  myapp deploy      部署项目
  myapp status      查看状态
  myapp --help      查看更多
```

**第三步：检查环境依赖**（避免中途报错）

```bash
$ myapp deploy my-project
⏳ 检查环境依赖...
  ✓ Node.js >= 18.0.0
  ✓ npm >= 9.0.0
  ✓ Docker（可选，用于容器化部署）
环境就绪，开始部署...
```

### 反面教材

```bash
$ myapp
Usage: myapp <command> [options]
# 然后就没了——用户不知道该做什么
```

### 设计原则

1. **不要在首次运行询问太多问题**——最多 2-3 个必要配置
2. **提供明确的"下一步"指引**——用户完成当前操作后，告诉ta可以做什么
3. **可跳过**——提供 `--yes` / `-y` 选项跳过交互式引导
4. **事后可配置**——首次运行设置的偏好，后续可以通过 `myapp config set` 修改

---

## 10.3 Shell补全的自动生成

Shell 补全让你的 CLI 在使用时更流畅。用户按 Tab 键时，自动补全命令、子命令、参数、甚至参数值。

### 支持的 Shell

| Shell | 补全文件位置 | 加载方式 |
|-------|-------------|----------|
| bash | `/etc/bash_completion.d/` 或 `~/.local/share/bash-completion/completions/` | `source <(myapp completion bash)` |
| zsh | `~/.zsh/completion/` | `eval "$(myapp completion zsh)"` |
| fish | `~/.config/fish/completions/` | `myapp completion fish | source` |

### 实现方式

**方式一：手动维护补全脚本**（不推荐）
- 需要手动同步——命令变更时容易忘记更新

**方式二：框架自动生成**（推荐）
- Click（Python）、Cobra（Go）、Commander（JS）等框架内建补全生成
- 在 `myapp completion` 子命令中实现

**方式三：动态补全**（更高级）
- 按需生成，支持参数值补全
- 例如：`myapp deploy <TAB>` 自动补全项目列表
- `gh pr view <TAB>` 自动补全PR列表

```go
// Cobra (Go) 示例
rootCmd.AddCommand(&cobra.Command{
    Use: "completion [bash|zsh|fish]",
    Short: "生成补全脚本",
    Long: "为指定的 shell 生成自动补全脚本。",
    Args: cobra.ExactValidArgs(1),
    ValidArgs: []string{"bash", "zsh", "fish"},
    Run: func(cmd *cobra.Command, args []string) {
        switch args[0] {
        case "bash":
            cmd.Root().GenBashCompletion(os.Stdout)
        case "zsh":
            cmd.Root().GenZshCompletion(os.Stdout)
        case "fish":
            cmd.Root().GenFishCompletion(os.Stdout, true)
        }
    },
})
```

### 动态补全的价值

动态补全可以大幅提升用户体验：

```bash
$ gh pr view <TAB>
# 展示当前仓库的所有 PR 列表
1  修复登录bug    (open)
2  添加导出功能   (open)
3  更新文档       (merged)

$ kubectl logs <TAB>
# 展示所有运行中的 pod 名称
myapp-api-7d8f9b4c6-abc12
myapp-web-6e8a7c3d9-xyz78
```

---

## 10.4 CI/CD 中的 CLI 行为差异

同一个 CLI 在终端（TTY）和 CI/CD 环境中的行为应该不同。

### 需要检查的差异点

| 特性 | TTY 行为 | CI/CD 行为 |
|------|----------|------------|
| 颜色 | 启用（可配置） | 默认禁用 |
| 进度动画 | spinner / progress bar | 定期日志输出 |
| 交互式提示 | 询问用户 | 报错或使用默认值 |
| 确认（Y/n） | 等待输入 | 假设 n 或可配置 |
| 输出长度 | 分页（less） | 完整输出 |

### 检测方式

```python
import sys

def is_ci():
    """检测是否运行在 CI/CD 环境中"""
    ci_env_vars = [
        'CI',           # GitHub Actions, GitLab CI, CircleCI
        'JENKINS_HOME', # Jenkins
        'TEAMCITY_VERSION',
        'TF_BUILD',     # Azure Pipelines
    ]
    return any(var in os.environ for var in ci_env_vars)

def is_tty():
    """检测是否运行在交互式终端中"""
    return sys.stdout.isatty()

# 综合判断
if is_ci():
    # CI 模式：禁用颜色、禁用交互、禁用动画
    pass
elif not is_tty():
    # 管道/重定向模式：禁用颜色和动画，但保持输出
    pass
else:
    # TTY 模式：全功能
    pass
```

### CI/CD 重点设计

1. **永远不要假设有人看输出**——CI/CD 的日志只在失败时被查看
2. **提供 `--ci` 或 `--no-interactive` 模式**——自动使用默认值
3. **明确区分"信息"和"错误"**——CI/CD 工具按退出码判断失败
4. **输出机器可解析的摘要**——比如以 `RESULT: success` 或 `RESULT: failure` 结尾，方便 CI 工具抓取

---

## 10.5 CLI 学习路线图

从零到CLI设计专家的学习路线。

### Day 1：第一次构建

- 选择一个框架（Click/Python, Cobra/Go, Commander/JS）
- 创建一个"Hello World"CLI
- 添加第一个子命令
- 添加第一个参数和 flag

**里程碑**：完成一个能运行的CLI，包含 `--help` 和子命令

### Week 1：基础扎实

- 学习 POSIX/GNU 参数约定
- 实现全局选项解析
- 添加颜色输出（支持 `NO_COLOR`）
- 实现基本的错误处理
- 添加退出码

**里程碑**：CLI 可以在非 TTY 和 TTY 模式下正常运行

### Month 1：专业质感

- 阅读 clig.dev 全篇
- 学习三种进度反馈模式
- 实现配置文件系统（XDG兼容）
- 添加 `--json` 输出
- 实现 shell 补全
- 添加幂等操作

**里程碑**：CLI 达到发布标准，可以公开使用

### Month 3：CLI设计专家

- 深度阅读 5+ 个优秀CLI源码（ripgrep, gh, docker, bat, fd）
- 实现交互式回退（类似 `gh pr create`）
- 设计插件系统
- 实现多语言 i18n 支持
- 编写完整的 man page
- 设计并实现自己的"代表作"CLI

**里程碑**：开源你的 CLI，获得社区反馈

---

## 10.6 测试策略

CLI 测试比普通应用测试更多样化。你需要从多个层级覆盖。

### 单元测试（Unit Tests）

测试单个函数/模块的逻辑。

```python
# 测试参数解析
def test_parse_args():
    args = parse_args(["deploy", "--env", "staging"])
    assert args.command == "deploy"
    assert args.env == "staging"
```

**重点覆盖**：
- 参数解析逻辑
- 配置合并逻辑
- 输出格式化
- 错误处理函数

### 集成测试（Integration Tests）

测试 CLI 作为一个整体运行。

**工具推荐**：
- **[cram](https://bitheap.org/cram/)**：Python 实现的CLI集成测试框架，使用类似 doctest 的格式
- **[bats](https://github.com/bats-core/bats-core)**：Bash 实现的测试框架
- **shelltestrunner**：声明式测试

**cram 示例**：

```
$ myapp create my-project
> 项目 "my-project" 创建成功 (0)

$ myapp list
> my-project (0)

$ myapp list --format json
> ["my-project"] (0)

$ myapp delete non-existent
> 错误：项目 "non-existent" 不存在
> [2]
```

**重点覆盖**：
- 完整的命令执行流程
- 参数组合
- 错误场景
- 退出码验证
- 输出格式检查

### 快照测试（Snapshot Tests）

将 CLI 输出保存为"快照"，后续运行自动对比差异。

**适用场景**：
- `--help` 输出
- `--version` 输出
- `list --format table` 等格式稳定的输出

```javascript
// Jest 快照测试示例
test('help output', () => {
    const output = runMyApp(['--help']);
    expect(output).toMatchSnapshot();
});
```

**优势**：一旦快照建立，后续变更会被自动发现，避免意外破坏。

### 管道测试（Pipeline Tests）

测试 CLI 在管道中的行为。

```bash
# 测试管道兼容性
$ myapp list | myapp batch-process
# 应该有合理的输出和退出码

$ myapp list 2>&1 >/dev/null
# stderr 不应包含数据输出
```

### 非TTY测试

```bash
# 模拟非 TTY 环境
$ echo '' | myapp deploy   # 检查无交互时的行为
$ myapp deploy < /dev/null # 检查非交互式输入
$ myapp list | cat          # 检查管道输出（无色）
```

---

### 测试策略决策树

```
命令是纯计算/转换的吗？
├─ 是 → 单元测试 + 集成测试
└─ 否 → 命令有副作用（写入/删除/网络）？
    ├─ 是 → 集成测试 + 模拟测试（mock external services）
    └─ 否 → 集成测试 + 快照测试

CLI 将被管道使用吗？
├─ 是 → 管道测试 + 非TTY测试
└─ 否 → 不需要

CLI 输出格式会频繁变更吗？
├─ 是 → 使用集成测试而非快照测试（减少维护成本）
└─ 否 → 快照测试 + 集成测试
```

---

# Chapter 11: 未来展望——AI Agent时代的CLI

> **「CLI的下一个十年，用户可能不是人类。」**

本章是手冊中最具推测性的部分——但推测基于已经发生的趋势。截至2025年，Claude Code、GitHub Copilot CLI、Shell Agent 等AI编程助手已经将CLI作为核心交互界面。这不仅仅是"CLI + AI"的简单叠加，而是CLI设计哲学的根本性变革。

让我展开这幅未来图景。

## 11.1 AI Agent正在成为CLI的新用户

传统上，CLI的用户是**人类开发者**。他们坐在终端前，一个命令一个命令地敲，看输出，理解信息，决定下一步做什么。

但2024-2025年间发生了一个静默的转变：**越来越多的CLI命令是由LLM（大语言模型）生成的，由AI Agent代为执行的**。

### 三种交互模式

**模式一：Agent作为"键盘手"（AI-Generated Commands）**

人类和Agent在同一终端"协作"：人类用自然语言描述目标，Agent自动生成并执行CLI命令。

```
人类: "帮我查一下这个项目里哪些文件最近修改过"

Agent: 运行 find . -name "*.py" -mtime -7
       → 输出文件列表

Agent: 运行 git log --oneline -- $(find . -name "*.py" -mtime -7)
       → 显示最近的提交记录

Agent: "以下是你最近修改的Python文件及相关提交..."
```

在这种模式下，**人类最终审批**Agent生成的命令。CLI仍然是给人类看的，但命令是由AI生成的。

**模式二：Agent作为"执行者"（Agent-Executed Commands）**

Agent自主执行CLI命令，不需要人类逐条确认。常见于：
- CI/CD Pipeline自动化
- 定时维护任务
- 批量数据处理

```python
# Agent 自主执行的任务示例
async def deploy_service():
    await run("docker build -t myapp:latest .")
    await run("docker push myapp:latest")
    await run("kubectl apply -f deploy.yaml")
    await run("kubectl rollout status deployment/myapp")
```

在这种模式下，**CLI的消费者是Agent本身**——人类只看最终结果摘要，不看每条命令的详细输出。

**模式三：Agent作为"语言桥梁"（Natural Language Interface）**

人类不再直接敲CLI命令，而是通过Agent用自然语言间接使用CLI。

```
人类: "把 staging 环境的日志压缩后下载到本地"

Agent: 
  1. 运行 ssh staging-server "tar -czf logs.tar.gz /var/log/myapp/"
  2. 运行 scp staging-server:~/logs.tar.gz ./
  3. 运行 tar -xzf logs.tar.gz
  
Agent: "已从staging环境下载日志并解压到当前目录"
```

### 重要洞察

这三种模式的共同点是：**CLI的"用户"正在从单一人类变为人类+Agent的混合体**。

这对CLI设计有什么影响？

## 11.2 Agent-native CLI的设计新要求

当Agent成为用户，CLI设计必须满足一些传统上不重要的要求。

### 要求一：结构化输出（JSON Schema）

人类可以从格式化的表格中提取信息，但Agent需要结构化的、可预测的数据。

```bash
# 人类友好（默认）
$ gh issue list
Showing 3 of 3 issues
#1  Fix login bug    (open)  assigned: alice
#2  Add export       (open)  assigned: bob   
#3  Update docs      (closed)

# Agent友好（--json）
$ gh issue list --json
[
  {"number": 1, "title": "Fix login bug", "state": "open", "assignee": "alice"},
  {"number": 2, "title": "Add export", "state": "open", "assignee": "bob"},
  {"number": 3, "title": "Update docs", "state": "closed", "assignee": null}
]
```

**新要求**：
- JSON输出应该有稳定的Schema（字段名和类型不变）
- Schema应该公开可查（`myapp schema` 或 `myapp --json-schema`）
- 建议提供 JSON Schema 规范文件，Agent 可以据此验证输出

### 要求二：幂等性——避免副作用

Agent不确定某个操作是否已经执行过。如果CLI不是幂等的，Agent可能会：
1. 创建重复资源
2. 注入重复数据
3. 触发不必要的通知

```bash
# 非幂等
$ myapp create-user alice
→ 第一次：用户创建成功
→ 第二次：错误 - 用户已存在

# 幂等
$ myapp ensure-user alice
→ 第一次：用户创建成功
→ 第二次：用户已存在，跳过（退出码 0）
```

**设计原则**：提供 `ensure` / `apply` 风格的操作，代替 `create` / `add`。

### 要求三：明确的错误码和错误类型

Agent很难像人类一样"看懂"一段错误描述文字。它们需要结构化的错误信息。

```bash
# ❌ 不友好（Agent需要解析文本）
错误：数据库连接失败（Error: connect ECONNREFUSED 127.0.0.1:5432）

# ✅ Agent友好
{"error": {"code": "DB_CONNECTION_REFUSED", "message": "无法连接到数据库", "details": {"host": "127.0.0.1", "port": 5432}}}
```

**设计原则**：
- 所有错误应该有明确的错误码（字符串常量）
- 提供 `--json` 下的结构化错误输出
- 错误码应该有文档（`myapp error-codes`）
- Agent可以根据错误码决定重试策略

### 要求四：非交互模式（Non-interactive Mode）

Agent不能"等用户输入"。所有操作要么成功，要么失败——没有中间态。

```bash
# ❌ 交互式确认
$ myapp delete database
⚠ 确认删除数据库？ [y/N]

# ✅ 非交互模式
$ myapp delete database --force
数据库已删除
```

**设计原则**：
- 所有操作都应该能在非交互模式下完成
- 交互式回退是锦上添花，但不能是唯一方式
- 提供 `--yes` / `--force` / `--no-interactive` 标志

### 要求五：输出长度可预测

Agent的上下文窗口有限。CLI的输出应该：

```bash
# ❌ 输出 10000 行
$ myapp list --all
# ... 太长了，Agent的上下文可能被撑爆

# ✅ 提供分页或摘要
$ myapp list --limit 10
# 超出部分用摘要表示
Showing 10 of 1000 items. Use --limit to show more.
```

**设计原则**：
- 默认输出长度有限（10-50行）
- 提供 `--limit` / `--offset` 分页
- 提供 `--summary` 输出摘要信息

## 11.3 CLI vs MCP：竞争与共存

2024年，Anthropic 推出了 **Model Context Protocol（MCP）**——一种让LLM直接调用工具的标准化协议。MCP的出现引发了关于"CLI是否会被取代"的讨论。

### MCP是什么？

MCP定义了一套JSON-RPC协议，让LLM可以直接调用工具函数，获取结构化输入输出——不需要经过CLI层。

```json
// MCP 调用示例
{
  "tool": "list_files",
  "params": {
    "directory": "/home/user/project",
    "pattern": "*.py"
  }
}
// MCP 返回结构化数据，而不是文本输出
```

### CLI vs MCP 的利弊

| 维度 | CLI | MCP |
|------|-----|-----|
| 人类可用 | ✅ 人类直接在终端使用 | ❌ 需要Agent中间层 |
| 脚本化 | ✅ Shell脚本/cron | ❌ 需要HTTP客户端 |
| 生态成熟度 | ✅ 50年基础设施 | ❌ 崭新协议 |
| 结构化输出 | ⚠️ 需要额外支持 | ✅ 原生结构化 |
| 工具发现 | ❌ 需要查文档 | ✅ 工具列表API |
| 参数校验 | ❌ 运行时才能发现错误 | ✅ 静态Schema |
| 组合能力 | ✅ Unix管道极其灵活 | ⚠️ JSON-RPC链式调用 |

### 我的判断：共存而非替代

CLI和MCP将走向**互补共存**而非替代：

1. **MCP不会取代CLI**，因为CLI是给人类用的。开发者不会放弃终端——它是效率最高的编程界面之一。

2. **CLI不会拒绝MCP**，因为MCP能更好地服务Agent。事实上，一些新工具已经开始同时提供CLI和MCP接口。

3. **中间层方案已出现**：像 `mcp-cli` 这样的桥接工具，可以自动将CLI包装成MCP服务器——CLI不需要改造，就能被Agent调用。

```bash
# mcp-cli 桥接：自动包装CLI为MCP工具
$ mcp-cli wrap gh
✓ gh CLI 已包装为 MCP 服务器
  - gh pr create → MCP tool: create_pull_request
  - gh issue list → MCP tool: list_issues
  - gh repo view → MCP tool: view_repository
```

4. **终极趋势**：未来的CLI将同时是"人类界面"和"机器界面"。`--json`输出会更加标准化，JSON Schema、MCP兼容性将成为专业CLI的标准配置。

## 11.4 预测：3年内CLI设计将发生的变化

基于上述分析，我对未来3年CLI设计趋势做出以下预测：

### 2025-2026：过渡期

1. **`--json`从可选项变必选项**——没有 `--json` 输出的CLI会被认为"不专业"
2. **JSON Schema 文档普及**——每个CLI的JSON输出附带公开Schema
3. **首批"Agent-native"CLI出现**——设计文档中明确包含"Agent用户"场景
4. **Shell补全 + LLM补全融合**——CLI帮助系统开始支持自然语言描述

### 2026-2027：融合期

5. **CLI内嵌LLM帮助**——`myapp help --ask "如何批量部署？"` 直接返回自然语言答案
6. **错误信息自带"Agent修复建议"**——错误时自动提示Agent可以调用的修复命令
7. **MCP端点成为CLI标准配置**——`myapp serve-mcp` 将CLI暴露为MCP服务器
8. **"人机协作"CLI模式诞生**——CLI同时输出人类可读文本和机器可读结构化数据

### 2027-2028：成熟期

9. **JSON输出成为CLI默认值**——文本格式是"显示层"，JSON是"数据层"
10. **LLM测试框架出现**——专门测试Agent-CLI交互的测试套件
11. **"Agent体验"（AX, Agent Experience）成为设计维度**——与UX并列
12. **CLI的"API版本化"成为标配**——`--json-version=2` 管理结构化输出的向后兼容性

## 11.5 对人类用户的影响：CLI是写给人类还是AI？

最后一个问题最本质：**当AI Agent开始大量使用CLI，我们的CLI应该优先为谁设计？**

### 三种立场

**立场一：人类优先**
> "CLI永远是给人类用的。Agent只是临时用户。我们应该专注开发者的体验，让Agent适配人类，而不是反过来。"

**立场二：AI优先**
> "未来90%的CLI调用来自Agent。我们应默认输出JSON，人类通过`--pretty`查看可读版本。Agent的需求决定了CLI设计。"

**立场三：双重设计**
> "CLI需要同时服务人类和Agent。就像一个好的API同时提供RESTful和GraphQL接口，CLI也应提供Human Mode和Agent Mode。"

### 我的观点：立场三

我认为**双重设计**是唯一可持续的方案。理由如下：

1. **人类不会退出终端**。终端仍然是最高效的编程界面。Vim/Emacs/Shell 文化在可预见的未来不会消亡。

2. **Agent不是替代，而是增强**。Agent帮人类做"脏活累活"（批量操作、数据提取、环境配置），但这些操作的最终审批者仍然是人类。所以输出必须同时让Agent可解析和人类可理解。

3. **双重设计并不矛盾**。一个命令可以同时输出文本和JSON——这是已经在实践的模式（`gh` 就是最好的例子）。

### 给CLI设计者的建议

**短期（现在就要做）**：
- 确保所有命令支持 `--json`
- 文档中写明JSON输出Schema
- 支持 `NO_COLOR` 和 `--no-interactive`
- 添加幂等操作

**中期（6个月内）**：
- 提供 `--json-schema` 输出
- 为常见操作添加 `ensure-*` 变体
- 支持输出分页/摘要
- 添加 `mcp` 子命令（包装为MCP服务器）

**长期（1-2年）**：
- 将CLI设计为"先机器后人类"——默认输出结构化数据，可读展示是上层渲染
- 建立Agent-CLI交互的测试套件
- 参与AX（Agent Experience）标准制定

### 结语

CLI已经走过了50年。从Unix的纯文本终端，到彩色ANSI界面，再到交互式TUI，再到——现在——同时服务人类和AI Agent。

每一次变革，CLI都没有消亡，而是进化了。这次也不会例外。

**未来的CLI，既是给人类写的，也是给AI写的。但更重要的是——它是人类和AI协作的桥梁。**

当人类说"帮我部署一下"时，Agent理解意图，CLI执行操作，Agent汇报结果，人类点头批准。整个过程流畅、透明、可控。

这才是AI Agent时代CLI设计的美好前景。

---

# 附录A: Claude Code CLI 深度一览

## A.1 定位

**Claude Code** 是 Anthropic 推出的终端AI编程助手。它不是一个传统的CLI工具，而是一个**AI Agent的CLI界面**——人类通过它让Claude直接操作代码库。

官网/仓库：Anthropic 官方产品，2025年发布。

## A.2 核心设计理念

### 1. "Agent-in-Terminal"

Claude Code 不是"在终端里问AI问题"，而是"让AI在终端里工作"。

```
$ claude-code "添加一个用户登录的API端点"
→ Claude 自动：
  1. 阅读现有代码结构
  2. 创建新文件
  3. 运行测试
  4. 提交代码
```

用户不是逐条输入命令，而是用自然语言描述目标，Claude自主完成。

### 2. "渐进式权限"

Claude Code 引入了权限级别概念：

| 权限级别 | 行为 | 适用场景 |
|----------|------|----------|
| **自动** | 自主执行，无需确认 | 读操作、安全的写操作 |
| **确认** | 执行前需要用户批准 | 修改文件、安装依赖 |
| **阻止** | 必须用户手动操作 | 删除文件、连接远程服务器 |

这种设计平衡了效率和安全性——日常操作无需频繁确认，危险操作有防护。

### 3. "透明的思维链"

每次Claude执行操作时，会展示它的"思考过程"：

```
$ claude-code "优化这个函数的性能"
[分析] 检测到函数 process_data() 使用嵌套循环，复杂度 O(n²)
[计划] 1. 使用哈希表优化查找 → O(n)
       2. 添加缓存装饰器
[执行] 正在修改 src/processor.py...
[验证] 运行测试... ✓ 全部通过 (12/12)
[结果] 性能提升：处理时间从 2.3s 降低到 0.15s
```

这种透明性让用户信任Agent的操作。

## A.3 命令结构

```
claude-code [options] [prompt]
```

**主要选项**：
| 选项 | 说明 |
|------|------|
| `-p, --prompt` | 直接传入指令（非交互模式） |
| `--model` | 指定模型版本 |
| `--verbose` | 显示详细思考过程 |
| `--no-confirm` | 自动模式（跳过确认） |
| `--session` | 恢复之前的会话 |

**交互模式**：
- 直接运行 `claude-code` 进入交互式会话
- 在会话中可以输入多条指令
- 支持 `/edit` `/run` `/search` 等Slash命令

## A.4 最值得学习的3个设计特点

### 特点1：安全护栏的设计

Claude Code 的安全模型值得所有"AI增强CLI"学习：
- **非侵入式默认**：初次运行只在当前目录操作，不会扫描全盘
- **操作分类**：读操作自动执行，写操作需要确认，危险操作默认阻止
- **可审计**：所有操作都记录在日志中，方便回滚

### 特点2：渐进式信息披露

Claude Code 不会一开始就显示所有信息：
- 第一层：`[分析]` 一行总结
- 第二层：点击展开详细计划
- 第三层：查看完整代码差异

这符合**认知负荷管理**原则——用户只在需要时看到细节。

### 特点3：非交互模式设计

```
# 非交互模式——CI/CD集成
$ claude-code -p "更新所有依赖到最新版本，确保测试通过" --no-confirm

# 管道模式
$ git diff HEAD~1 | claude-coder -p "用中文描述这些变更"
```

即使是最复杂的Agent操作，也支持完全非交互执行。这是Agent-native CLI的必备特性。

---

# 附录B: GitHub CLI (gh) 深度一览

## B.1 定位

**gh** 是 GitHub 官方命令行工具，旨在将 GitHub 工作流带入终端。它于2019年首次发布，是 GitHub 对"开发者体验"的重要投资。

仓库：[github.com/cli/cli](https://github.com/cli/cli)（13k+ stars）

## B.2 核心设计理念

### "The CLI is for humans before machines"

这句话出自 gh 设计文档，是整个工具的设计基石。

**含义**：
- 默认输出是人类可读的（表格、颜色、图标）
- 所有机器接口（`--json`）是附加功能，不是默认
- CLI应该"感觉像GitHub"，而不是"感觉像GitHub API"

### "减少上下文切换"

gh 的目标是让开发者**不需要离开终端**就能完成GitHub操作。

```bash
# 以前需要：
1. 打开浏览器
2. 导航到 GitHub
3. 找到PR
4. 点击 merge 按钮

# 使用 gh：
$ gh pr merge 42
✓ Pull request #42 已合并
```

### "渐进式披露"

gh 的功能可以按用户熟练程度逐步掌握：

| 阶段 | 会用的命令 | 用户体验 |
|------|-----------|----------|
| 新手 | `gh pr create`（交互式） | 引导式填写，无需记参数 |
| 日常 | `gh pr create --fill` | 使用默认值，少打字 |
| 专家 | `gh pr create --title "..." --body "..." --base main --draft` | 全参数，一步到位 |

## B.3 子命令设计

**核心命令结构**：

```
gh <资源> <操作> [参数]
```

| 资源 | 常用操作 | 示例 |
|------|---------|------|
| `pr` | `create`, `view`, `list`, `checkout`, `merge`, `review`, `close` | `gh pr create` |
| `issue` | `create`, `view`, `list`, `close`, `reopen` | `gh issue list` |
| `repo` | `create`, `clone`, `view`, `fork` | `gh repo create` |
| `release` | `create`, `view`, `list`, `download` | `gh release create` |
| `run` | `view`, `list`, `watch`, `rerun` | `gh run watch` |
| `gist` | `create`, `view`, `list`, `edit` | `gh gist create` |

**设计亮点**：
- 资源名直观（pr, issue, repo）
- 操作名在资源间一致（create, view, list 在所有资源下都有）
- 每个子命令都有独立的 `--help`

## B.4 交互式 Fallback 模式

gh 最值得称道的设计是**当参数缺失时自动进入交互模式**。

```bash
# 完全交互式
$ gh pr create
? 选择分支: main
? 标题: 修复登录bug
? 是否创建草稿PR: Yes
✓ Pull request #42 已创建

# 部分参数
$ gh pr create --title "修复登录bug"
? 选择分支: main  (从git分支列表自动选择)
? 是否创建草稿PR: No

# 全参数（完全非交互）
$ gh pr create --title "修复登录bug" --body "修复了..." --base main --draft
✓ Pull request #42 已创建
```

**实现原理**：
1. 检查是否有必需参数缺失
2. 如果是TTY模式 → 进入交互式提示
3. 如果是非TTY模式 → 报错并提示需要的参数
4. 参数的交互式提示有智能默认值（从git配置、当前分支等推断）

## B.5 最值得学习的3个设计特点

### 特点1：`--json` + `--jq` 的强大组合

gh 提供了 `--json` 输出，并且额外支持 `--jq` 参数（使用 `jq` 语法过滤字段）：

```bash
# 获取PR列表，只选择特定字段
$ gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title) by \(.author.login)"'
42: 修复登录bug by alice
43: 添加导出功能 by bob
```

这是"双重设计"的完美体现：
- 人类默认看表格
- 机器用 `--json` 获取结构化数据
- 高级用户用 `--jq` 精确控制输出

### 特点2：上下文感知的默认值

gh 大量使用当前上下文来推断合理的默认值：

```bash
$ gh pr create
# 自动检测：
# - 当前分支名 → PR标题
# - 最近的commit message → PR标题/body
# - git remote → 目标仓库
# - git config user.name → PR作者
```

这让"零参数"调用成为可能——对于80%的日常操作，用户不需要输入任何参数。

### 特点3：状态和进度反馈

gh 对长时间操作有精心的反馈：

```bash
$ gh pr merge 42
✓ Pull request #42 已合并

$ gh run watch
# 实时显示 GitHub Actions 运行状态
✓ build (ubuntu-latest)   Passed
✓ test (ubuntu-latest)    Passed
✗ lint (ubuntu-latest)    Failed
  ⚠ 查看详细日志: gh run view 12345
```

- 成功操作显示 ✓ 和摘要
- 失败操作显示 ✗ 和排查路径
- 耗时操作显示实时进度

---

## 附录B总结对比：Claude Code vs gh

| 维度 | Claude Code | gh (GitHub CLI) |
|------|-------------|-----------------|
| **定位** | AI编程Agent界面 | GitHub平台CLI |
| **核心理念** | AI-in-Terminal | CLI for humans |
| **用户** | 人类+Agent混合 | 主要为人类 |
| **交互模式** | 自然语言驱动 | 命令驱动+交互式fallback |
| **输出** | 思维链+代码变更 | 表格+颜色+--json |
| **最值得学** | 安全护栏、渐进式信息披露、非交互设计 | --json+--jq、上下文默认值、交互式fallback |

---

> **CLI设计哲学手册 · 第二部分 完**
>
> 第三部分预告（Ch12-Ch18 + 附录C/D）：
> - 框架选型深度对比（Go/Python/Rust/Node）
> - 跨平台发布与包管理
> - 国际化与无障碍设计
> - 性能优化与大规模数据处理
> - CLI安全审计指南
> - 开源CLI项目的社区运营
> - 附录C: ripgrep 源码深度分析
> - 附录D: 从零构建生产级CLI——完整实战

