---
source_url: https://mp.weixin.qq.com/s/Ml-qJnxMEJ5oDPFQwVJfhA
ingested: 2026-05-11
sha256: 7cb059624a4b0c3597f20a006c793eae1ff0a7957c5401361c3b673d5d0a936e
title: Hermes Agent 实战应用
author: 求索深思
source: 微信公众号
---

高效使用原则、安全实践、实战案例、费用对比
一、高效使用的核心原则原则一：前置上下文，减少来回
❌ 错误示范：

"帮我修 bug"

✅ 正确示范：

"修复 api/handlers.py 第 47 行的 TypeError——process_request() 从 parse_body() 收到了 None"

一条信息包含足够上下文，胜过三轮追问。
原则二：让 Agent 用自己的工具
❌ 错误示范：

"打开 tests/test_foo.py，看第 42 行，然后……"

✅ 正确示范：

"找到并修复失败的测试"

Agent 有文件搜索、终端、代码执行等工具，让它自己探索和迭代。
原则三：善用上下文文件
如果你发现自己在反复告诉 Agent 同样的事情：

"用 tabs 不用 spaces"

"我们用 pytest"

"API 在 /api/v2"

就把这些写进 AGENTS.md。一劳永逸。
原则四：主动触发技能创建
完成复杂任务后：

"把你刚才做的保存为一个叫 deploy-staging 的技能"

下次直接 /deploy-staging 就能复用。
原则五：管理记忆容量
定期说：

"清理一下你的记忆""把旧的 Python 3.9 笔记更新——我们现在用 3.12 了"

保持记忆精炼、最新。
原则六：用委派处理并行任务
需要同时调研三个方向？

 delegate_task(
   tasks=[
     {goal: "调研方案A", context: "..."},
     {goal: "调研方案B", context: "..."},
     {goal: "调研方案C", context: "..."}
   ]
 )
每个子 Agent 独立运行，只返回最终摘要，大幅节省主对话的 token。
原则七：选对模型做对事
用 /model 随时切换：

复杂推理和架构决策：Claude Sonnet/Opus、GPT-4o

简单的格式化、重命名、模板生成：快速模型（Gemini Flash、GPT-4o-mini）
二、Memory 工具使用方法两种目标目标说明示例user用户档案用户偏好、沟通风格memoryAgent 笔记环境配置、技能、经验三种动作

 # 1. 添加新条目
memory add target="memory"content="MySQL密码：5612"

# 2. 更新现有条目
memory replace target="memory"old_text="旧内容"content="新内容"

# 3. 删除条目
 memory remove target="memory"old_text="要删除的内容"实际示例

 # 保存今天学到的备份技巧
memory add target="memory"content="Hermes备份：sync-to-backup.sh脚本会自动备份自定义skill"

# 保存用户偏好
memory add target="user"content="沟通风格：简洁直接，中文优先"

# 更新已有信息
memory replace target="memory"old_text="备份脚本"content="备份脚本已优化，支持自动检测自定义skill"

# 查看当前记忆
 memory三、安全最佳实践1. 不信任的代码用隔离环境

 # 处理不信任的代码时
 hermes config set terminal.backend docker2. 命令审批要谨慎
不要轻易选 "Always"

先用 "Session"（仅本次会话）

确认安全后再考虑 "Always"
3. 消息平台设置白名单

 # 永远不要开启这个（除非测试）
 GATEWAY_ALLOW_ALL_USERS=false
 
 # 设置允许的用户
 FEISHU_ALLOWED_USERS=ou_xxxx
 TELEGRAM_ALLOWED_USERS=1234564. 技能安装注意安全
安装时查看安全扫描结果

dangerous 级别的技能会被自动阻止

从可信来源安装技能
四、实战案例案例 1：自动日报
需求：每天早上 8 点汇总昨天的工作

配置：

 # 创建定时任务
 hermes cron create "0 8 * * *""生成昨天的工作日报，包括代码提交、文档更新、会议记录"
 
 # 设置输出渠道
 hermes cron set-channel telegram
效果：

每天早上 8 点自动执行

汇总代码提交、文档更新、会议记录

发送到你的 Telegram
案例 2：GitHub 监控
需求：监控关注的仓库，有新 Issue 及时通知

配置：

 # 使用 GitHub 技能
 hermes skills install github-issues
 
 # 创建监控任务
 hermes cron create "*/30 * * * *""检查 nousresearch/hermes 仓库的新 Issue，分类后通知"
效果：

每 30 分钟检查一次

自动分类（Bug、Feature、Question）

发送通知
案例 3：内容创作助手
需求：把 X 推文改写成公众号文章

配置：

 # 创建 Skill
cat > ~/.hermes/skills/rewrite-wechat/SKILL.md << 'EOF'
---
name: rewrite-wechat
description: 将推文改写成公众号文章
---

## 执行步骤
1. 保留核心观点
2. 补充背景说明
3. 添加结构化标题
4. 生成封面图建议
5. 调整为公众号格式
 EOF
使用：

"用 rewrite-wechat 技能把这篇推文改写成公众号文章"
案例 4：代码审查
需求：提交代码前自动审查

配置：

# 安装代码审查技能
hermes skills install github-code-review

# 使用
hermes -q "审查当前分支的代码变更，重点关注安全问题和性能问题"五、费用对比Hermes vs 其他方案项目HermesOpenClawChatGPT Plus月费5 | 10-15$20
模型自带（灵活选择）绑定特定服务固定 GPT-4记忆成本按需召回（稳定）全量加载（递增）无持久记忆部署自有 VPS / WSL云服务云端数据位置本地 ~/.hermes/云端云端实测数据
跑在 5 美元/月的 VPS 上完全没问题

比 OpenClaw 便宜 30%-60%

记忆调用成本稳定，不会越用越贵
省钱技巧
用便宜模型处理简单任务

/model google/gemini-2.5-flash  # 简单任务
/model anthropic/claude-sonnet-4  # 复杂任务
定期压缩上下文

/compress  # 手动压缩
善用委派

并行任务用 delegate_task

子 Agent 只返回摘要，节省 token
六、技能管理技能来源来源数量说明builtin~86 个内置技能（已预装）official45 个Nous Research 官方可选skills.sh142 个社区技能索引github大量GitHub 技能仓库clawhub45 个ClawHub 技能市场浏览和安装

# 浏览官方技能
hermes skills browse --source official

# 浏览社区技能
hermes skills browse --source skills-sh

# 搜索特定技能
hermes skills search "spring boot"
hermes skills search "video"

# 预览技能详情
hermes skills inspect <skill-name>

# 安装技能
hermes skills install <skill-name>推荐技能
开发相关：

spring-boot - Spring Boot 开发

docker-management - Docker 容器管理

github-code-review - 代码审查

实用工具：

obsidian - Obsidian 笔记管理

feishu-sender - 飞书消息发送

bilibili-video - B站视频处理
七、常见问题Q: 记忆丢失怎么办？
# 检查记忆文件
cat ~/.hermes/memory/MEMORY.md
cat ~/.hermes/memory/USER.md

# 从备份恢复
ls ~/.hermes-backup/memories/

# 搜索历史对话
session_search "关键词"Q: 技能不生效？
# 检查技能是否安装
hermes skills list

# 检查技能是否启用
hermes skills config

# 手动加载技能
/skill <skill-name>Q: Gateway 连接失败？
# 检查配置
cat ~/.hermes/.env | grep FEISHU

# 检查日志
tail -f ~/.hermes/logs/gateway.log

# 重启 Gateway
hermes gateway restart下一步
🚀 回到 入门指南 开始安装

📖 阅读 核心概念 深入理解

🏗️ 了解 架构与评析 技术细节
