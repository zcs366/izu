---
source_url: https://mp.weixin.qq.com/s/Su6tSY12iOJ3Ejh0WkTR-w
ingested: 2026-05-07
sha256: d9826141cc37dffee96bbe478341c2e897c2e2cd77cd0d1e3ed9218423ad4c33
source: 微信公众号
author: 小张
description: 用 Rust 重写 Hermes Agent，13 crate 模块化架构设计，核心四大 Trait，配置兼容 Python 版本
---

# 用 Rust 重写 Hermes Agent：13 个 crate 的模块化工坊

作者：小张

## 动机

Python 版 hermes-agent 的痛点：启动慢（冷启动 3-5 秒）、内存占用高（空载 200MB+）、async/sync 桥接地狱、部署依赖复杂、类型安全缺失。

## 架构设计：13 个 crate，严格 DAG

``` 
hermes-rs/crates/
  hermes-core/        # 共享类型：Message、ToolCall、Platform、Error
  hermes-config/      # YAML 配置 + .env + SOUL.md 人格加载
  hermes-security/    # 注入扫描、环境变量过滤、路径防护
  hermes-state/       # SQLite + FTS5 全文搜索
  hermes-llm/         # LLM 客户端：OpenAI 兼容 + SSE 流式
  hermes-terminal/    # 终端执行后端：Local + Docker
  hermes-skills/      # 技能系统：SKILL.md 解析、CRUD
  hermes-tools/       # 工具注册表 + 9 个内置工具
  hermes-mcp/         # MCP 协议客户端（stdio + JSON-RPC）
  hermes-agent/       # 核心 Agent 循环：对话编排、上下文压缩
  hermes-gateway/     # 网关 + 5 个平台适配器
  hermes-cron/        # 定时任务调度器
  hermes-cli/         # 交互式终端 UI
```

## 四大核心 Trait

1. **LlmClient**：LLM 调用抽象（complete + stream），每种 API 一个独立 struct
2. **ToolHandler**：工具执行抽象（execute），注册到 RwLock<HashMap>
3. **TerminalBackend**：执行环境抽象（Local + Docker 同一接口）
4. **PlatformAdapter**：消息平台抽象，每个平台一个文件，实现四个方法

## 性能对比

| 指标 | Python 版 | Rust 版 |
|---|---|---|
| 代码行数 | ~50,000 | ~5,000 |
| 模块数 | 100+ 文件 | 13 crate / 66 文件 |
| 编译产物 | 需要 Python runtime | 单个 25MB 二进制 |
| 类型安全 | 运行时（mypy 可选） | 编译时保证 |
| async 模型 | asyncio + threading 混合 | 纯 tokio async |

## 配置兼容

读取 Python 版本完全相同的配置文件（config.yaml + .env），零迁移成本。支持项目本地配置：项目目录下放 `.hermes/config.yaml` 自动覆盖全局。

## 项目地址

https://github.com/coder-brzhang/hermes-rs
