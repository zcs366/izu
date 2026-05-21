---
source_url: https://mp.weixin.qq.com/s/50ZARAH6cOeKTSyjJo-I6w
ingested: 2026-05-07
sha256: 6fc16e616c98064235097c58f077a6be05c113304f7e8510cf8443a2c14d6f90
source: 微信公众号
author: Agent 观察者
description: 23 讲系统性拆解 Hermes Agent 的架构、记忆系统、技能系统、安全模型、多平台部署、MCP 集成与实战项目
---

# Hermes Agent 深度拆解专栏（23 讲全系列大纲）

作者：Agent 观察者

定位：面向有一定 AI Agent 开发经验的工程师，系统讲解 Hermes Agent 核心原理、架构设计与实战落地。

## 专栏结构

**总计**：开篇词 + 21 讲 + 结束语 = 23 篇，六大部分。

## 第一部分：基础篇（4 讲）

### 01 | 全景图：三层架构与核心理念
- UI 层（cli.py / gateway/）/ Agent 核心（run_agent.py）/ 执行层（tools/environments/）
- 与 Claude Code、Codex CLI 的定位差异：多入口共享 runtime 与状态策略
- "The self-improving AI agent" 的设计取舍

### 02 | 模型无关的秘密：200+ 模型的统一接入层
- 四条路径：OpenRouter / Nous Portal / 直连厂商 / 本地 Ollama
- resolve_provider_client() 与 HermesOverlay 注册表
- Non-Agentic 模型识别 + Smart Model Routing（按复杂度路由到廉价模型）
- 故障转移（_try_activate_fallback）：主模型限速时无感切换
- 凭证池轮换（credential_pool.py）：同 Provider 多 Key 四种策略

### 03 | 工具系统全解析
- Registry 模式：schema + handler + check_fn 三件套，命令式注册（非装饰器）
- 扁平 tools/ 目录与 TOOLSETS 字典分组机制
- 参数类型强转 coerce_tool_args() 与 JSON 字符串返回值
- 大结果三层防线：工具内上限 / maybe_persist_tool_result / enforce_turn_budget

### 04 | Agent 主循环
- run_agent.py 的 AIAgent 类核心循环拆解
- 工具调用并行执行：_should_parallelize_tool_batch() 路径感知安全
- 空响应恢复：reasoning-only 输出、长度截断续写、压缩重启与重试
- IterationBudget：预算制 + 退还机制 + 压力预警

## 第二部分：核心篇（4 讲）

### 05 | 记忆系统（上）：内置记忆
- MEMORY.md（2,200 字符 / ~800 tokens）与 USER.md（1,375 字符 / ~500 tokens）双文件分工
- 系统提示的冻结快照（frozen snapshot）：为什么不在 session 中实时同步
- memory 工具的 add / replace / remove 语义 + § 分隔符存储格式
- FTS5 会话搜索：SQLite 全文索引 + LLM 摘要
- 核心权衡：信息新鲜度 vs Prompt Cache 效率

### 06 | 记忆系统（下）：可插拔 Memory Provider
- plugins/memory/ 下 8 种 Provider：Byterover / Hindsight / Holographic / Honcho / mem0 / OpenViking / RetainDB / Supermemory
- Honcho 重点：dialectic reasoning、server-side conclusions、per-peer 多 Agent 画像隔离
- 定期 nudge 机制：_memory_nudge_interval = 10、_memory_flush_min_turns = 6
- Agent 自主判断值得记住的内容（非"自动保存一切"、非"等用户说请记住"）

### 07 | 技能系统
- SKILL.md 文件格式与 YAML 前置元数据
- 技能创建触发：_skill_nudge_interval = 10 轮次 nudge + 后台审查
- _spawn_background_review()：fork AIAgent、注入 _SKILL_REVIEW_PROMPT、非阻塞写入
- 技能管理三件套：skills_list / skill_view / skill_manage
- 四级信任等级：builtin > trusted > community > agent-created（INSTALL_POLICY 表）

### 08 | Agent 自我进化
- 进化是工程化的三件事：记忆 nudge、技能 nudge、后台 review
- 轨迹数据收集 + Atropos RL 环境集成：用真实工作轨迹训练 tool-calling 模型

## 第三部分：安全篇（4 讲）

### 09 | 技能安全
- Agent 自动生成的技能文件是最大攻击面
- 120 条威胁正则（THREAT_PATTERNS），12 大类别
- 不可见 Unicode 检测（zero-width / bidi override 等 17 种字符）
- 四级 INSTALL_POLICY × safe/caution/dangerous 裁决

### 10 | 7 层安全防线
用户授权 → 危险命令审批 → 容器隔离 → MCP 凭证过滤 → 上下文文件扫描 → 跨会话隔离 → 输入净化

### 11 | 智能审批与平台化安全
- 智能审批模式：辅助 LLM 评估风险等级（approvals.mode: smart）
- MCP 集成安全：OAuth 2.1 PKCE + OSV 恶意软件扫描
- YOLO 模式三种激活方式与边界

### 12 | 沙箱与执行环境
- 六种后端对比：Local / Docker / SSH / Daytona / Singularity / Modal
- 无服务器后端冷启动、休眠与持久化策略
- 检查点管理器：影子 Git 仓库的文件恢复

## 第四部分：多平台篇（3 讲）

### 13 | Gateway 架构
- gateway/run.py 事件循环 + 平台适配器注册
- session_key 设计：按 platform / chat / thread / user 组合
- home channel 与自动投递
- 跨平台消息格式归一：Markdown / 按钮 / 文件上传 / 语音转写

### 14 | Telegram + Slack 双渠道部署实战

### 15 | ACP 适配器
- ACP（Agent Client Protocol）协议与编辑器集成
- 客户端 MCP 服务器

## 第五部分：进阶篇（3 讲）

### 16 | 扩展机制
- General Plugin、Memory Provider、Context Engine 三条扩展线
- 自定义工具：registry.register() 全流程

### 17 | MCP 集成
- MCP 客户端（tools/mcp_tool.py，2500+ 行）
- discover_mcp_tools() + 动态工具注册（RLock 线程安全）
- OAuth 2.1 PKCE + OSV 扫描

### 18 | 长会话治理
- 上下文压缩（agent/context_compressor.py）
- Token 追踪与跨 Provider 计费
- 大结果三层防线在长会话中的表现

## 第六部分：实战篇（3 讲）

### 19 | 个人知识助手：记忆策略 + skill_nudge + 多渠道访问
### 20 | 团队开发助手：代码审查 + 多用户隔离 + 技能共享
### 21 | 自主 AI 研究员：delegate_task 并行 + 浏览器自动化 + 轨迹数据导出

## 结束语
- 从 Harness Engineering 到 Agent Operating System 的演进方向
- "自我进化"能力的边界
