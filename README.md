# izu / 爱祝 — 陪你走得道快乐的知识研究系统

> **izu** (爱祝 / ai祝) is a knowledge research system that walks with you from "I don't know" to "I see it clearly" to "the joy of understanding."

## 项目介绍 · Introduction

**中文**

izu（爱祝）不是一个更好的 Deep Research。它是一个陪你走完「不知道→知道→得道快乐」全过程的知识研究系统。基于 **Async Generator Agent Loop** 架构，集成轨迹信用评分、进化引擎、微信文章采集（透心）、Agent 拓扑 API 与中文依存分析等模块。

项目根植于「明学七则」——长编是索引不是池子、定本由学习者自己写、参数必须开放、展望超过总结、写作标准厚重、以乐为终。产品哲学不是产出准确答案，而是让学习者想继续。

代码仓库：https://github.com/zcs366/izu

**English**

Izu is not a better Deep Research. It is a companion on the path to joyful understanding — a research system that accompanies you from confusion to clarity to delight. Built upon an **Async Generator Agent Loop**, it integrates trajectory credit scoring, an evolution engine, WeChat article harvesting (Touxin), an Agent topology API, and Chinese dependency parsing.

The system is rooted in the Seven Principles of Ming: long-form is an index, not a pool; the definitive text is written by the learner; parameters must be open; outlook outweighs summary; writing standard: weight; joy is the end. The product philosophy is not producing correct answers, but making the learner want to continue.

Repository: https://github.com/zcs366/izu

---

## 架构图 · Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     izu System                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Agent Loop (agent_loop.py)              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │   │
│  │  │ Query    │  │ Turn     │  │ Streaming     │  │   │
│  │  │ Params   │──▶│ State    │──▶│ Tool Executor │  │   │
│  │  └──────────┘  └──────────┘  └───────┬───────┘  │   │
│  │                                       │          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌───────▼───────┐  │   │
│  │  │ Cost     │  │ Event    │  │ Izu Adapter   │  │   │
│  │  │ Ladder   │  │ Stream   │  │ (subagent桥)   │  │   │
│  │  └──────────┘  └──────────┘  └───────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────┐  ┌───────────────┐  ┌──────────────┐  │
│  │ 透心         │  │ 轨迹信用评分    │  │ 进化引擎      │  │
│  │ Touxin      │  │ Trajectory    │  │ Evolution    │  │
│  │ (多版本采集)  │  │ Credit Score  │  │ Engine       │  │
│  ├─────────────┤  ├───────────────┤  ├──────────────┤  │
│  │ touxin.py  │  │ trajectory_   │  │ evolution_   │  │
│  │ touxin_v1_ │  │ credit.py     │  │ engine.py    │  │
│  │ simple.py  │  │ trajectory_   │  │ izu_         │  │
│  │ touxin_    │  │ balance.py    │  │ evolution_   │  │
│  │ shield.py  │  │               │  │ pipeline.py  │  │
│  │ touxin_    │  │               │  │              │  │
│  │ adaptive.py│  │               │  │              │  │
│  └─────────────┘  └───────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ 拓扑 API     │  │ 中文依存分析   │  │ 记忆系统      │  │
│  │ Topology     │  │ Dep Parse    │  │ Memory       │  │
│  ├──────────────┤  ├──────────────┤  ├───────────────┤  │
│  │ topology_    │  │ dep_parse_   │  │ izu_session_  │  │
│  │ api.py       │  │ zh.py        │  │ memory.py     │  │
│  │              │  │              │  │ izu_working_  │  │
│  │              │  │              │  │ memory.py     │  │
│  │              │  │              │  │ izu_self_     │  │
│  │              │  │              │  │ model.py      │  │
│  │              │  │              │  │ izu_memory_   │  │
│  │              │  │              │  │ maintenance.py│  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ 成本追踪      │  │ Skill评分    │  │ 升级防护       │  │
│  │ Cost Tracker │  │ Skill Scorer│  │ Upgrade Guard │  │
│  ├──────────────┤  ├──────────────┤  ├───────────────┤  │
│  │ izu_cost_    │  │ izu_skill_   │  │ izu_hermes_   │  │
│  │ tracker.py   │  │ scorer.py    │  │ upgrade_      │  │
│  │              │  │ izu_skill_   │  │ guard.py      │  │
│  │              │  │ ecosystem_   │  │               │  │
│  │              │  │ health.py    │  │               │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│                                          ┌───────────┐  │
│  ┌──────────────┐                        │ 数据      │  │
│  │ 数据脚本      │                        │ data/     │  │
│  │ scripts/     │                        │ (git-     │  │
│  │ mcp_traffic_ │                        │ ignored)  │  │
│  │ logger.py    │                        └───────────┘  │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 核心模块 · Core Modules

### 1. Agent Loop (`agent_loop.py`)

izu 的核心异步生成器 Agent 循环，受 Claude Code v2.1.88 源码架构启发。

- **Async Generator**: 统一事件流 (`THINKING → TOOL_CALL → TOOL_RESULT → MESSAGE → DONE`)
- **Cost Ladder**: 四级上下文压缩阶梯（截断→清除→小模型摘要→全量摘要），`70% → 85% → 95%` 阈值触发
- **Streaming Tool Executor**: 只读工具在 LLM 生成时并行执行，有副作用工具串行
- **9 种终止原因**: COMPLETED / BLOCKING_LIMIT / ABORTED_STREAMING / ABORTED_TOOLS / PROMPT_TOO_LONG / MODEL_ERROR / MAX_TURNS / COST_LIMIT / USER_STOPPED
- **收益递减检测**: 连续低产出轮次自动终止
- **IzuAdapter**: 桥接现有 subagent 系统的适配器（搜→写→劈流水线）

```python
async for event in AgentLoop(call_model, tool_handler).run(params):
    match event.type:
        case EventType.THINKING:  ...
        case EventType.DONE:      print(event.metadata["reason"])
```

### 2. 轨迹信用评分 (`trajectory_credit.py`)

从 Orchard 论文「信用分配」思想迁移的轻量级评分系统，零外部 API 调用。

- 6 维度评分：推理深度 (30%) / 信息密度 (25%) / 决策信号 (20%) / 工具使用 (15%) / 长度修正 (10%)
- Rise Segment 检测：信用分数连续上升的阶段自动标记
- Hermes Session JSONL 解析：从 `.jsonl` 文件加载轨迹
- 高信用轨迹导出：用于 skill 提取优先级排序

```bash
python -m izu.trajectory_credit --input sessions.jsonl --output credit.jsonl
```

### 3. 轨迹平衡采样 (`trajectory_balance.py`)

基于 Orchard 论文「Balanced Adaptive Rollout」思想的采样平衡器。

- 监控各任务类型成功率，动态调整采样权重
- 目标比例 `[0.3, 0.7]`：正难负易
- 任务分类器基于关键词匹配，无模型依赖
- 支持 `research` / `search` / `write` / `code` 等任务类型

```python
sampler = BalancedSampler()
sampler.record("research", success=True)
weight = sampler.get_weight("research")
```

### 4. 进化引擎 (`evolution_engine.py`)

ReVeal 推理时扩展，践行「匠石铁律」——90% 评分代码化，仅语义质量需模型。

- 6 维度验证：URL 存活率 / 结构完整性 / 引用准确性 / 内部一致性 / 简洁度 / 语义质量（10% 模型）
- 代码验证器：`Verifier` 含 URL 检查、结构检查、一致性检查
- 自动修复：`RepairContext` 自动解决低分问题

```bash
python -m izu.evolution_engine.py batch
```

### 5. 进化管道 (`izu_evolution_pipeline.py`)

统一 `trajectory_credit` + `trajectory_balance` + `evolution_engine` 三组件的集成管道。

```bash
python3 izu_evolution_pipeline.py run   # 运行完整进化管道
python3 izu_evolution_pipeline.py report
```

### 6. 透心 — 微信/知乎文章采集 (`touxin*.py`)

多版本抗反爬采集系统，专门用于采集中文平台文章内容：

| 版本 | 文件 | 说明 |
|------|------|------|
| v1 简单版 | `touxin_v1_simple.py` | Playwright + Cookie 注入 |
| v2 隐身版 | `touxin.py` | playwright-stealth 反检测 + 人类行为模拟 |
| v3 破盾版 | `touxin_shield.py` | 策略路由: A(Cookie+Stealth) → B(缓存镜像) → C(标题搜索转载) |
| v4 自适应版 | `touxin_adaptive.py` | 对策矩阵驱动，失败→匹配模式→自动尝试对策，成功率追踪 |

### 7. Agent 拓扑 API (`topology_api.py`)

Agent 关系拓扑的 CRUD 接口，支持任务分配与进化数据接入。

- Agent 注册/查询/列表
- 关系管理（协作/避免/竞争/依赖）
- 任务分配策略（默认最多 7 Agent，探索率 0.15）
- 涌现指标追踪（负载分布、瓶颈检测）

```python
topo = AgentTopology()
topo.register_agent("agent_001", "研究员", "research", ["AI", "NLP"])
```

### 8. 中文依存分析 (`dep_parse_zh.py`)

基于 spaCy `zh_core_web_sm` 的中文依存解析流水线。

- Markdown 清洗（去 frontmatter / bold / italic / code / links）
- 主语-动词-宾语三元组提取
- 过滤停用关系词
- 输出到 `data/wiki-graph-dep-parse-zh-v4.json`

### 9. 记忆系统 (`izu_session_memory.py` / `izu_working_memory.py` / `izu_self_model.py` / `izu_memory_maintenance.py`)

| 模块 | 功能 |
|------|------|
| `izu_session_memory.py` | Session 压缩、时间衰减曲线、遗忘门控 |
| `izu_working_memory.py` | Top-K 工作记忆队列（注意力密度原理） |
| `izu_self_model.py` | Self Model 快照、身份锚点提取与漂移检测 |
| `izu_memory_maintenance.py` | 自动维护流水线（每 6 小时） |

```bash
python3 izu_session_memory.py audit     # 扫描 session 状态
python3 izu_working_memory.py queue session.jsonl
python3 izu_self_model.py snapshot      # 拍快照
```

### 10. 成本追踪 (`izu_cost_tracker.py`)

从 Hermes session 文件估算 token 消耗和费用的离线追踪器。

- 多模型定价数据库（deepseek / claude / gpt / gemini / qwen 等）
- 包月模型特殊处理
- `scan` / `report` / `reset` CLI 命令

### 11. Skill 评分与生态健康 (`izu_skill_scorer.py` / `izu_skill_ecosystem_health.py`)

- 批量扫描用户 SKILL.md，对接 evolution_engine 的 5 维度评分
- 自动修正低分 SKILL
- 看板输出与健康报告

```bash
python3 izu_skill_scorer.py scan --min    # 只输出低分
python3 izu_skill_scorer.py check <name>
python3 izu_skill_ecosystem_health.py full  # 全流程
```

### 12. Hermes 升级防护 (`izu_hermes_upgrade_guard.py`)

升级前快照 → 升级 → 升级后 diff → 自动修复兼容问题。

```bash
python3 izu_hermes_upgrade_guard.py protect  # 一键防护
```

### 13. 其他工具

| 文件 | 说明 |
|------|------|
| `izu_memory_health.sh` | 记忆系统健康检查 Shell 脚本 |
| `scripts/mcp_traffic_logger.py` | MCP 流量日志记录 |

---

## 目录结构 · Directory Structure

```
izu/
├── __init__.py                    # 包入口，导出 AgentLoop 等核心类
├── agent_loop.py                  # [核心] Async Generator Agent Loop
├── trajectory_credit.py           # [核心] 轨迹信用评分
├── trajectory_balance.py          # 轨迹平衡采样
├── evolution_engine.py            # [核心] 进化引擎
├── izu_evolution_pipeline.py      # 进化管道集成
├── touxin.py                      # 透心 v2 — 隐身版采集
├── touxin_v1_simple.py            # 透心 v1 — 简单版采集
├── touxin_shield.py               # 透心 v3 — 破盾版采集
├── touxin_adaptive.py             # 透心 v4 — 自适应版采集
├── topology_api.py                # [核心] Agent 拓扑 API
├── dep_parse_zh.py                # [核心] 中文依存分析
├── izu_session_memory.py          # Session 记忆管理
├── izu_working_memory.py          # 工作记忆队列
├── izu_self_model.py              # Self Model 快照
├── izu_memory_maintenance.py      # 记忆自动维护
├── izu_cost_tracker.py            # Token 成本追踪
├── izu_skill_scorer.py            # SKILL.md 批量评分
├── izu_skill_ecosystem_health.py  # Skill 生态健康管理
├── izu_hermes_upgrade_guard.py    # Hermes 升级防护
├── izu_memory_health.sh           # 记忆健康 Shell 脚本
├── test_agent_loop.py             # 单元测试（11 测）
├── README.md                      # 本文件
├── docs/
│   └── audit-report-izu-2026-05-19.md   # 代码审计报告
├── scripts/
│   └── mcp_traffic_logger.py      # MCP 流量日志
├── data/                          # 数据目录（git-ignored）
│   ├── credit_trajectories.jsonl
│   ├── test_session.jsonl
│   ├── sampler_state.json
│   └── touxin-*.json
└── .gitignore
```

---

## 快速开始 · Quick Start

### 依赖

```bash
# Python 3.11+
pip install pytest       # 测试
pip install playwright   # 透心采集
pip install spacy        # 中文依存分析
python -m spacy download zh_core_web_sm
pip install playwright-stealth  # 透心反检测
```

⚠️ 暂无 `requirements.txt` — 按需安装各模块对应的库。

### 运行 Agent Loop 演示

```bash
cd /mnt/i/hermes/izu
python -m izu.agent_loop
```

### 运行测试

```bash
cd /mnt/i/hermes/izu
python -m pytest test_agent_loop.py -v
```

### 使用轨迹评分

```bash
cd /mnt/i/hermes/izu
python -m izu.trajectory_credit --input data/test_session.jsonl --report
```

### 采集文章（透心）

```bash
cd /mnt/i/hermes/izu
python touxin_v1_simple.py    # 简单版
python touxin.py              # 隐身版
```

### 中文依存分析

```bash
cd /mnt/i/hermes/izu
python dep_parse_zh.py
```

---

## 开发状态 · Development Status

该项目处于 **早期原型阶段**。审计报告 (`docs/audit-report-izu-2026-05-19.md`) 记录了以下状态：

| 维度 | 指标 |
|------|------|
| 代码总量 | 21 Python 文件 + 1 Shell 脚本 ≈ 5,746 行 |
| 版本控制率 | 43%（9/21 文件被 git 追踪） |
| 测试覆盖率 | 1 个测试文件（11 测，覆盖 agent_loop） |
| 包管理 | ❌ 无 requirements.txt / pyproject.toml |
| CLI 入口 | ❌ 无统一 main.py / cli.py |

**注意**：代码仓库 (`/mnt/i/hermes/izu/`) 与项目官网仓库 (`/home/zcs/izu/`) 为两个独立 git 仓库。

---

## 许可证 · License

MIT

---

## 关于 · About

**军师祭酒 (Strategist)** — 原为三国曹魏首席谋官职。在这里，是一种角色：陪你思考的人。

项目创造者 **张成市 (Zhang Chengshi)** — 诗人、编辑、两个女儿的爸爸。

---

*读得快的地方是你已经知道的；读得慢的地方是你正在想的。下次来，我们从那里开始。*

*The parts you read quickly — you already know. The parts you slow down on — that's where you're thinking. Next time, we'll start from there.*
