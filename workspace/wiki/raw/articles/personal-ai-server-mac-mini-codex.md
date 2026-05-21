---
source_url: https://mp.weixin.qq.com/s/1QtNFn-ySGhRi-aaq-ZVLw
ingested: 2026-05-21
sha256: 08b734dff3a5f5851c311484db88467d99eff542326ff54d2b0068efbf2cd3ae
title: 个人专属超级AI系统搭建教程：MacBook + Mac mini + Codex + 龙虾 + Tailscale = 个人专属超级 AI 系统
author: 勤劳的树懒同学
source: 微信公众号
content_type: text
---

# 个人专属超级AI系统搭建教程：MacBook + Mac mini + Codex + 龙虾 + Tailscale = 个人专属超级 AI 系统

MacBook + Mac mini + Codex + 龙虾 + Tailscale 个人专属超级AI系统搭建教程一、这套系统到底要解决什么问题
这套系统只解决一个问题：搭建一套属于自己的超级 AI 系统。

这个系统不是单纯装几个软件，而是把各个软硬件分工清楚，并组成一个有机的整体。

这个有机的系统，好用、易用，能工作，能休闲，真正的成为个人专属的超级AI系统。

工作用 MacBook：日常操作入口。
你在公司、外面、家里，都用 MacBook 来做项目、看文件、写代码、远程登录 Mac mini、控制任务。

家里 Mac mini：长期在线的 AI 工作主机。
它负责跑 Codex App、Codex CLI、OpenClaw/龙虾 gateway、各种长期任务、skill、脚本、自动化。

Codex：真正的 agent 执行层。
以后主要让 Codex 来读项目、改文件、跑命令、生成 skill、维护代码、打包项目。

龙虾 / OpenClaw：gateway 和记忆承载层。
它负责飞书、微信、定时任务、消息接入、会话记忆、旧 agent 流程。未来它不一定当主力 agent，而是更像一个“消息网关 + 调度器”。（龙虾不适合作为 agent 的核心，他太不靠谱，太不可控）

Tailscale：安全远程网络。
它让 MacBook、iPhone、Mac mini 像在同一个私有局域网里一样互相访问，不需要把 SSH、VNC、网关端口暴露到公网。
二、整体架构图

┌────────────────────────────┐│        工作 MacBook         ││  - 写代码 / 看文件           ││  - SSH 到 Mac mini           ││  - VS Code / Cursor Remote   ││  - 远程桌面控制              │└─────────────┬──────────────┘              │              │ Tailscale 私有网络              │ ssh / vnc / http 内网访问              ▼┌────────────────────────────┐│       家里 Mac mini          ││  - 常驻在线                  ││  - Codex App                 ││  - Codex CLI                 ││  - OpenClaw / 龙虾 Gateway   ││  - tmux 长任务               ││  - skills / workspace / git  │└─────────────┬──────────────┘              │              │ gateway / webhook / CLI 调用              ▼┌────────────────────────────┐│       飞书 / 微信 / GitHub    ││  - 消息入口                  ││  - 任务触发                  ││  - 代码仓库                  ││  - 文件同步                  │└────────────────────────────┘
一句话总结：
MacBook 是遥控器；Mac mini 是机房；Codex 是工人；龙虾是前台和网关；Tailscale 是专线。
整体系统搭建好之后如下图：
三、为什么不让 MacBook 直接干所有事
MacBook 可以干，但不适合作为长期 agent 主机。

原因有几个：

第一，MacBook 作为我的工作电脑，经常带走、关盖、切网络、换环境。agent 跑长任务容易中断。

第二，MacBook 作为工作电脑，任务太多会乱。今天写文章，明天调代码，后天跑图片，环境容易污染。

第三，Mac mini 可以长期放在家里，不动、不关、不休眠。它更像一个自己的“小型 AI 服务器”。

所以最终原则是：
MacBook 负责发号施令；Mac mini 负责持续执行。

四、Mac mini 的定位
Mac mini 以后就是我们的 Codex 专用主机。

它上面主要放这些东西：

~/dev/github/           # GitHub 项目目录~/dev/lab/              # 临时实验目录~/.codex/               # Codex 配置、skills、AGENTS.md~/.openclaw/            # 龙虾配置、workspace、agent、memory~/.openclaw/workspace/  # 龙虾工作区
建议长期保持这个思路：
重要项目进 GitHub；临时项目放 lab；Codex 规则放 ~/.codex；龙虾旧工作流放 ~/.openclaw；大文件不要随便进 git。五、第一步：Mac mini 基础环境安装1. 安装 Xcode Command Line Toolsxcode-select --install
这个是 macOS 上跑 git、编译工具、很多开发依赖的基础。
2. 安装 Homebrew
执行 Homebrew 官网给的安装命令。装好后确认：
brew --versionbrew doctor
然后建议安装基础工具（直接执行下面这个命令）：
brew install git node python uv jq wget tree ripgrep fd tmux
这些工具大概分工是：
git       管代码版本node      跑前端、npm、Codex CLIpython    跑脚本uv        更快的 Python 包管理jq        处理 JSONwget      下载文件tree      看目录结构ripgrep   快速搜索文本fd        快速找文件tmux      长任务会话保持

六、第二步：安装 Codex
Codex 有三种常用形态：
Codex App        图形界面，适合完整项目开发、浏览器、Computer UseCodex CLI        终端 agent，适合 SSH、脚本、自动化、改文件Codex IDE 插件   适合 Cursor / VS Code 里直接用
安装 Codex CLI：
npm i -g @openai/codex
安装后运行：
codex
第一次会提示登录，可以用 ChatGPT 账号或 API key。

也可以升级：
npm i -g @openai/codex@latest
Codex 的用户级配置文件在：
~/.codex/config.toml
codex app去官网下载即可。
七、第三步：安装龙虾 / OpenClaw
在 Mac mini 上安装：
npm install -g openclaw@latest
初始化：
openclaw onboard
常用检查命令：
openclaw statusopenclaw status --deepopenclaw doctoropenclaw models listopenclaw models status
启动 gateway：
openclaw gateway start
查看 gateway 状态：
openclaw gateway status --deep
看日志：
openclaw logs --follow --local-time
你的龙虾主要承担：
1. 飞书 / 微信消息接入2. 定时任务3. 老的 agent 记忆4. gateway 转发5. 未来调用 codex exec 做真正执行
龙虾不一定需要装在 mac mini 上，也可以装在原来的 Windows 电脑上。安装可以参考：原版龙虾安装指南：用龙虾驱动GPT5.4帮你干活

龙虾的相关配置也可以参考上面的文章。

也就是说，未来不一定要让龙虾自己思考、自己写代码。更好的模式是：
飞书 / 微信消息    ↓龙虾 gateway 接收    ↓解析任务    ↓调用 Codex CLI / skill / 脚本    ↓把结果回传给飞书 / 微信

系统运行的工作流如下图：八、第四步：安装 Tailscale
Mac mini 和 MacBook 都安装 Tailscale。

安装后，两台设备登录同一个 Tailscale 账号。

然后在 Mac mini 上查看自己的 Tailscale IP，一般是：
100.x.x.x
以后 MacBook 连接 Mac mini，就不要用公网 IP，也不要开路由器端口，直接用：
ssh john@100.x.x.x
或者：
vnc://100.x.x.x
当前方案可以先保持简单：
Tailscale 负责打通私有网络；macOS 自带 SSH 负责登录；macOS 屏幕共享负责远程桌面。九、第五步：开启 Mac mini 远程登录
在 Mac mini 上开启 SSH：
sudo systemsetup -setremotelogin on
测试：
ssh 你的用户名@100.x.x.x
例如：
ssh john@100.88.xx.xx
第一次连接会提示确认指纹，输入：
yes
以后就可以远程进入 Mac mini 的终端。
十、第六步：开启 Mac mini 屏幕共享
在 Mac mini 上：
系统设置  → 通用  → 共享  → 打开“屏幕共享”
建议只允许你自己的用户访问，不要开所有用户。

然后在 MacBook 上打开 Finder：
前往  → 连接服务器
输入：
vnc://100.x.x.x
这样就可以远程看到 Mac mini 桌面。

这条通道适合：
1. 用 Codex App2. 需要浏览器操作3. 需要 Computer Use4. 需要图形界面配置软件5. 远程救急
SSH 通道适合：
1. 跑 Codex CLI2. 改文件3. 执行命令4. 看日志5. 跑 tmux 长任务
在 tailscale 组建的网络里面工作示意图如下：
十一、第七步：防止 Mac mini 睡眠
Mac mini 必须常驻，否则 agent 跑一半会断。

查看当前电源设置：
pmset -g
建议设置：
sudo pmset -a sleep 0 displaysleep 10 disksleep 0 womp 1 tcpkeepalive 1
如果想临时强制不睡，可以跑：
caffeinate -dimsu
更强一点的方式是：
sudo pmset -a disablesleep 1
但这个属于比较强硬的设置，建议确认稳定后再用。

也可以去设置里面用图形界面设置，是一样的。
十二、第八步：用 tmux 保持长期任务
SSH 最大的问题是：你一断线，普通终端任务可能就没了。

所以 Mac mini 上必须用 tmux。

安装：
brew install tmux
创建一个 Codex 会话：
tmux new -s codex
进入后运行：
codex
退出但不关闭任务：
Ctrl + b然后按 d
重新回来：
tmux attach -t codex
常用命令：
tmux lstmux new -s codextmux new -As codextmux attach -t codextmux kill-session -t codex
推荐你的 Mac mini 长期有几个 tmux 窗口：
codex       跑 Codex CLIgateway     跑龙虾 gateway / 看状态logs        看 openclaw logsdev         跑 npm / python / skillmonitor     看 htop / 系统状态
以 mac min 为核心的整个系统示意图如下：
十三、日常工作流场景一：人在公司，用 MacBook 控制家里 Mac minissh john@100.x.x.xtmux new -As codexcd ~/dev/github/你的项目codex
然后你直接对 Codex 说：
检查这个项目结构，找出 README、AGENTS.md 和 package.json，告诉我怎么启动。
或者：
根据当前项目，我的需求是xxxx，直接给我结果场景二：用 MacBook 远程桌面操作 Codex AppFinder → 前往 → 连接服务器 → vnc://100.x.x.x
然后直接打开 Mac mini 上的 Codex App。

适合：
1. 看图形界面2. 用浏览器3. 处理需要 Computer Use 的任务4. 远程调试网页5. 操作复杂 UI场景三：飞书里发任务，让龙虾接，再转给 Codex
最终理想形态是：
你在飞书发一句：“把公众号 skill 打包并同步到 GitHub。” 飞书 bot 收到    ↓龙虾 gateway 判断任务    ↓进入对应 workspace    ↓调用 codex exec 或 skill CLI    ↓Codex 修改文件 / 打包 / git commit    ↓龙虾把结果回飞书
这就是后面的重点升级方向。

龙虾不再是主 agent，而是：
消息入口 + 权限控制 + 会话记忆 + 调度层
Codex 才是：
真正干活的 agent runtime十四、推荐目录结构
Mac mini 上建议这样整理：

mkdir -p ~/dev/githubmkdir -p ~/dev/labmkdir -p ~/dev/archivemkdir -p ~/.codex/skillsmkdir -p ~/.openclaw/workspace
结构：
~/dev/github/  wechat-article-pipeline-skill/  codex-gateway/  feishu-bridge/  godot-game-demo/ ~/dev/lab/  test-skill/  test-image-jobs/  temp-codex-output/ ~/.codex/  config.toml  AGENTS.md  skills/ ~/.openclaw/  openclaw.json  workspace/  agents/  memory/

十五、AGENTS.md 的作用
以后每个重要项目都应该有自己的：
AGENTS.md

它相当于给 Codex 的项目说明书。

比如公众号 skill 项目里可以写：
# AGENTS.md ## 项目目标 这是一个微信公众号文章生成 skill。 ## 工作原则 - 优先输出 Markdown + HTML 混合格式- 图片生成不要所有图片一个风格- 标题图、中间图、结尾图要有不同角色- 代码修改后必须跑测试- 打包前检查目录结构 ## 禁止事项 - 不要把临时文件提交到 git- 不要把 API key 写进仓库- 不要删除用户原始文章
这样 Codex 进入项目后，就知道这个项目的规矩。
十六、GitHub 工作流
每个重要项目都应该进 GitHub。

基本流程：
cd ~/dev/github/你的项目 git statusgit add .git commit -m "update"git push
如果是第一次建仓库：
git initgit add .git commit -m "initial commit"git branch -M maingit remote add origin git@github.com:你的用户名/仓库名.gitgit push -u origin main
建议 .gitignore 写清楚：
.DS_Storenode_modules/.env.env.localdist/build/tmp/.cache/
龙虾 workspace 这种可能很大的目录，不要乱传 GitHub。
十七、这套系统的安全原则1. 不开公网端口
不要把这些东西暴露到公网：
SSH 22VNC 5900OpenClaw gateway本地 Web 服务调试端口
统一走 Tailscale。
2. SSH 只在 Tailscale 内用
连接方式：
ssh john@100.x.x.x
不要搞：
ssh john@公网IP3. API Key 不进 Git
.env 必须进 .gitignore。
.env.env.*4. Codex 改代码前先 git status
每次大改之前：
git statusgit add .git commit -m "checkpoint before codex changes"
这样 Codex 改坏了也能回滚。
十八、常用命令速查表Mac mini 远程ssh john@100.x.x.xtmux

tmux lstmux new -s codextmux new -As codextmux attach -t codextmux kill-session -t codexCodexcodexcodex --versionnpm i -g @openai/codex@latest龙虾 / OpenClawopenclaw statusopenclaw status --deepopenclaw doctoropenclaw gateway startopenclaw gateway status --deepopenclaw logs --follow --local-timeopenclaw models listopenclaw models status电源pmset -gsudo pmset -a sleep 0 displaysleep 10 disksleep 0 womp 1 tcpkeepalive 1caffeinate -dimsuGitgit statusgit add .git commit -m "update"git pushgit pull

十九、故障排查1. SSH 连不上
检查：
ping 100.x.x.x
如果 ping 不通：
1. Mac mini 是否开机2. Mac mini 是否登录 Tailscale3. MacBook 是否登录同一个 Tailscale4. Tailscale 后台是否在线
如果 ping 通但 ssh 不通：
sudo systemsetup -getremotelogin
开启：
sudo systemsetup -setremotelogin on2. 远程桌面连不上
检查 Mac mini：
系统设置 → 通用 → 共享 → 屏幕共享
确认打开。

连接地址：
vnc://100.x.x.x
不要用公网 IP。
3. Codex 命令找不到
检查：
which codexcodex --version
重新安装：
npm i -g @openai/codex@latest4. tmux 里滚动不方便
进入 copy mode：
Ctrl + b然后按 [
退出：
q
不建议一开始就强行开鼠标模式，容易影响复制。等用熟了再配置。tmux 启动无法用鼠标或者上下键滚屏，必须用上面的命令才才能滚屏。
5. 龙虾 gateway 挂了
检查：
openclaw gateway status --deepopenclaw doctoropenclaw logs --follow --local-time
如果需要重启：
openclaw gateway restart6. Mac mini 像断电一样重新登录
优先检查睡眠和系统重启记录：
pmset -g log | grep -i "Entering Sleep"last reboot
然后确认：
pmset -g
如果发现 sleep 不是 0，就重新设置防睡眠。
二十、最终演进路线
这套系统可以分三阶段走。
第一阶段：远程专用主机
目标：
Mac mini 常驻Tailscale 打通SSH 可用屏幕共享可用Codex CLI 可用tmux 可用
做到这里，你已经有一台自己的 AI 工作站了。
第二阶段：Codex 主力化
目标：
项目都放 ~/dev/github每个项目有 AGENTS.mdCodex CLI 负责改文件Codex App 负责复杂图形任务GitHub 做版本管理
这时如果已经深度使用龙虾的，可以先保留龙虾，但不再让它承担复杂 agent 任务，慢慢把处理任务都迁移到 codex。
第三阶段：龙虾降级为 gateway
目标：
飞书 / 微信 / 定时任务    ↓龙虾 gateway    ↓codex exec / skill CLI    ↓结果回传
也就是：
龙虾负责接活；Codex 负责干活；GitHub 负责留痕；Mac mini 负责常驻。二十一、这套方案的最终形态
最终你要的不是“装了一堆 AI 软件”。

你要的是一个自己的 AI 工作系统：
人在 MacBook 上发任务；任务进入 Mac mini；Codex 理解项目并执行；龙虾负责外部消息入口；Tailscale 保证远程安全；GitHub 保存所有成果；tmux 保证任务不断；AGENTS.md 保证每个项目有自己的规矩。
这套系统搭好以后，你后面做这些事都会顺：
1. 写公众号，做自媒体2. 做自己工作相关的任务3. 维护 GitHub 项目4. 跑飞书自动处理任务的机器人5. 做自动化日报6. 做图片生成流水线7. 做自己的协同成长的人工智能助理8. 把 Mac mini 变成真正的个人 AI 服务器
一句话：
MacBook 是你的驾驶舱；Mac mini 是你的机房；Codex 是你的工程师；龙虾是你的消息前台；Tailscale 是你的专线网络。
这就是这套系统的核心逻辑。

最终的目标就是搭建一个属于你个人的超级 AI 系统。

都看到这里了，点赞收藏，加马上行动起来吧。

