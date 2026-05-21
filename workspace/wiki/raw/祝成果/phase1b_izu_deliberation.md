# Phase 1B: izu 5轮合议

**Date:** 2026-05-21 (Cron Run)
**Track:** izu - Production LLM Agent Architecture: Runtime Patterns, Structural Backpressure, and Multi-Agent Orchestration

---

## Round 0: 子产 · 需求判断与研究方向

### 问题判断
- **真实问题**：Multi-agent系统在企业级部署中的协调成本指数增长已成为行业共识
- **紧迫性**：8/10 — 行业处于agent大规模部署临界点
- **三个子方向均有实质性未解问题**
  - Runtime Patterns：缺乏生产级状态管理/错误恢复实践
  - Structural Backpressure：几乎无系统性文献
  - Multi-Agent Orchestration：缺乏成熟编排模式分类

### 研究边界
- 不包括：prompt工程、模型训练、框架API使用教程
- 重点关注：架构模式谱系、背压机制、失败模式目录、可观测性框架

### 建议优先级
backpressure > orchestration patterns > runtime patterns

---

## Round 1: 韩信 · 技术远景

### 3年技术发展时间轴
| 时期 | 里程碑 |
|------|--------|
| 2026 H2 | 混乱期：8种架构模式初步收敛，背压停留在"错误处理"心智模型 |
| 2027 | 结构化背压元年：Token预算管理成为标配；Agent Scheduler开源 |
| 2028 | 可观测性与自治编排：OpenTelemetry agent-native扩展；自治拓扑切换 |
| 2029 | 架构成熟期：Agent OS概念落地；编排失败模式目录形成行业标准 |

### 三条路线对比
| 路线 | 核心理念 | 推荐优先级 |
|------|---------|-----------|
| A: 中间件/网关 | 透明代理层（AIMD+熔断）| ★★★★★ 短期最高性价比 |
| B: 框架内建 | LangGraph等内置资源管理 | ★★★★ 中期主流方向 |
| C: Agent OS | 独立运行时平台 | ★★ 长期探索，投入风险高 |

### 关键技术成熟度 (TRL)
| 方向 | 当前 | 2028预期 |
|------|------|---------|
| 架构模式图谱分类 | TRL 5 | TRL 7 |
| 结构化背压 | TRL 2-3 | TRL 5-6 |
| 编排失败模式目录 | TRL 1-2 | TRL 4 |
| Agent可观测性 | TRL 3-4 | TRL 6-7 |
| 自治编排 | TRL 1 | TRL 3 |

---

## Round 2: 鲁班 · 工程可行性评估

### 系统架构
四层架构：请求入口 → 调度代理层（速率限制/优先级队列/并发准入/背压+断路器）→ Agent执行引擎（状态机/工具调用器/Token预算管理器）→ LLM API Provider网关 → 可观测性层

### 模块可行性
| 模块 | 判定 | 理由 |
|------|------|------|
| HTTP代理层背压 | ✅ 可行 | HiveMind验证：<3ms开销 |
| AIMD+断路器 | ✅ 可行 | 标准分布式系统模式 |
| Per-run Token预算 | ✅ 可行 | 代码级实现简单 |
| 优先级队列 | ✅ 可行 | 标准数据结构 |
| Agent状态机(LangGraph) | ✅ 可行 | 生产级状态机 |
| MCP协议工具调用 | ✅ 可行 | 已成事实标准 |
| 多Provider速率限制追踪 | ⚠️ 部分可行 | Header格式不统一 |
| 自动成本优化 | ⚠️ 部分可行 | meta-cognition不可靠 |
| Agent OS | ❌ 暂不可行 | 需求未收敛 |
| 形式化验证agent行为 | ❌ 暂不可行 | 概率性输出不可形式化验证 |
| 跨provider热备failover | ❌ 暂不可行 | prompt差异无法自动适配 |

### MVP方案（4周）
- Proxy层 300行代码骨架：TokenBucket + CircuitBreaker + Semaphore + PriorityQueue
- 协议：HTTP proxy代理（零侵入，agent只需改base URL）
- 交付：3个provider profile + /metrics endpoint + YAML配置文件

---

## Round 3: 萧何 · 执行路径

### 团队配置
2人核心(Infra+Agent工程师) + 0.5 DevOps + 0.5 架构师 = 3 FTE等效

### 预算
$60,000–82,000（12周），其中LLM API成本占60-80%

### 12周三阶段
- **Phase 1（Week 1-4）MVP**: 20并发agent、Proxy背压、单一provider
- **Phase 2（Week 5-8）增强**: 100并发、完整可观测性、多provider
- **Phase 3（Week 9-12）生产化**: 生产就绪、安全审计、文档交付

### 关键技术锁定
- LangGraph + MCP + Proxy背压架构
- 不做：Agent OS、全自动路由、跨provider热备

---

## Round 4: 张仪 · 最强攻击

### 致命缺陷
1. **LangGraph+MCP生态成熟度不足**：快速迭代期，API稳定性存疑
2. **2人核心团队无法支撑生产级系统**：严重低估了工程复杂度
3. **成本控制幻觉**："减少无效调用"无法解决结构性成本问题
4. **安全合规空白**：提示注入防护、数据隔离、审计日志几乎未提及
5. **监控可观测性缺失**：LLM Agent的非确定性行为需要完善的可观测性

### 最可能失败原因
1. 时间表崩溃：4周MVP扣除环境搭建后实际编码不足2周
2. 技术栈兼容性问题：LangGraph与MCP集成遇文档不全/边缘情况
3. 团队过载：2人同时处理架构、编码、测试、文档，认知负荷过高
4. 成本超支：开发阶段LLM API调用远超预期

### 最终裁决
**No-Go.** 风险收益比严重失衡。建议改为：A)内部工具级而非生产级；B)延长至6个月+预算$150-200K+5-6人团队；C)选更成熟技术栈。
