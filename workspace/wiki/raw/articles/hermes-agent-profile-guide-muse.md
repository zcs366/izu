---
source_url: https://mp.weixin.qq.com/s/HSg9PNGINzVtj7gmuqYahg
ingested: 2026-05-07
sha256: 73cc417854a3c64074ccf0303d447a5c23a822eaa9f0c1cb6f499e4e6efbb182
source: 微信公众号
author: 缪斯每天都开心
description: 用西游记人物讲解 Hermes Agent 多 Profile 机制，覆盖 SOUL.md/MEMORY.md/USER.md 三文件分工与真实工作场景迁移
---

# Hermes Agent 多 Profile 实战：用西游记理解多 Agent 配置

作者：缪斯每天都开心

## 核心思路

不要让一个 Agent 什么都做。用 **profile** 把不同 Agent 的模型、记忆、技能和任务边界拆开，让每个 Agent 都在自己擅长的范围内工作。

## Profile 是什么？

一个 profile 就是一个独立的 Hermes 运行实例（独立的 Hermes home 目录）。

### 每个 Profile 拥有
- **config.yaml**：模型、provider、工具、终端后端配置
- **.env**：API Key、Bot Token 等环境变量
- **SOUL.md**：Agent 的身份、人设和核心行为准则
- **memories/MEMORY.md**：Agent 的长期笔记（你告诉它的事实）
- **memories/USER.md**：用户画像（Agent 自动推断维护）
- **skills/**：该 profile 可用的技能
- **sessions/**：会话记录
- **cron jobs**：定时任务
- **state database**：状态数据库

### 创建与使用
```bash
hermes profile create sunwukong  # 创建
sunwukong setup                   # 配置（自动生成包装脚本 ~/.local/bin/<name>）
sunwukong chat                    # 直接使用
hermes -p sunwukong chat          # 或显式指定
hermes profile list               # 列表查看，* 标记默认
hermes profile use sunwukong      # 设默认
```

## 三文件分工（核心）

| 文件 | 职责 | 谁来写 | 何时生效 |
|---|---|---|---|
| **SOUL.md** | Agent 是谁（身份/人格/语气/工作风格） | 你 | 新会话生效 |
| **MEMORY.md** | 你告诉 Agent 的事实（环境/约定/经验） | 你 + Agent | 实时 |
| **USER.md** | Agent 对你的推断画像 | Agent 自动维护 | 实时 |

**不要混着写**。SOUL.md 不适合写临时任务或项目规则（项目规则放 AGENTS.md 或 .hermes.md）。MEMORY.md 不适合放大段日志或通用知识。

## 实战示例：西游记

- **唐僧（用户）**：取经队伍核心保护对象
- **孙悟空（先锋 Agent）**：侦查/识破伪装/战斗/高风险判断 — 机敏果断，用火眼金睛
- **猪八戒（后勤 Agent）**：后勤/搬运/扎营/打听消息 — 有点懒但关键时刻不掉链子

## 迁移到真实工作场景

| Profile | 角色 | 适合任务 |
|---|---|---|
| coder | 编程 Agent | 写代码、改 Bug、重构 |
| researcher | 研究 Agent | 搜资料、竞品分析、整理报告 |
| tester | 测试 Agent | 写测试、跑测试、分析失败日志 |
| docs | 文档 Agent | 写 README、API 文档、教程 |
| ops | 运维 Agent | 查服务器、跑脚本、定时任务 |

## 注意事项

- **Profile 不是文件系统沙箱**：不同 profile 的 Agent 仍有同一系统用户的文件访问权限。真正隔离需用 Docker/SSH/Modal/Daytona
- **Profile 不等于工作目录**：需单独配置 `terminal.cwd`
- **修改 SOUL.md 后需新开会话**：它影响 system prompt，缓存不实时刷新
- **Skill 支持自动创建和自我改进**：>5 次工具调用后自动整理为 Skill，使用中发现过时自动修补
