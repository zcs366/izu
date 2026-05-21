---
title: Hermes Agent 安全模型
created: 2026-05-07
updated: 2026-05-10
type: concept
tags: [agent, security]
sources: [raw/articles/hermes-agent-deep-dive-series-agent-observer.md, raw/articles/ai-anquan-gongfang-kb-v1.2.md, raw/articles/supply-chain-attack-mistralai-hermes-20260513.md]
confidence: high
---

# Hermes Agent 安全模型

[[Hermes Agent]] 采用**7 层纵深防御**策略，覆盖从用户交互到沙箱执行的全链路安全。

## 7 层安全防线

Hermes 的 7 层纵深防御与 [[ai-security-five-layer-framework]]（AI 安全五层结构）的第三层（Agent 和协议层）及第五层（组织和治理层）高度对应。更多 AI 安全总体框架参见 [[ai-security-workshop]]。

| 层 | 防御措施 |
|---|---|
| ① 用户授权 | 允许名单 / DM 配对 |
| ② 危险命令审批 | tools/approval.py：手动 / 智能 / off 三种模式 + 正则模式库 |
| ③ 容器隔离 | Docker / Singularity / Modal 硬化 |
| ④ MCP 凭证过滤 | 子进程环境变量隔离 |
| ⑤ 上下文文件扫描 | 项目文件中的 prompt injection 检测 |
| ⑥ 跨会话隔离 | session 互不可见、cron 路径防穿越 |
| ⑦ 输入净化 | 工作目录参数白名单 |

## 技能安全扫描

- **120 条威胁正则**（THREAT_PATTERNS 数组），12 大类别：exfiltration / injection / destructive / persistence / network / obfuscation / execution / traversal / mining / supply_chain / privilege_escalation / credential_exposure
- **不可见 Unicode 检测**：zero-width / bidi override 等 17 种字符
- **四级 INSTALL_POLICY × safe/caution/dangerous 裁决**
- 无 LLM 语义审计（确定性、零额外成本、可审计）

## 智能审批模式

辅助 LLM 评估操作风险等级（`approvals.mode: smart`）。多平台审批体验：
- CLI 确认
- Telegram 按钮
- Slack 交互

## 沙箱与执行后端

六种后端的安全隔离对比：Local / Docker / SSH / Daytona / Singularity / Modal。无服务器后端（Daytona、Modal）的冷启动、休眠与持久化。

检查点管理器：影子 Git 仓库的文件恢复机制。

## 供应链攻击暴露的缺失

2026年5月 MistralAI PyPI 投毒事件暴露了7层防线的一个盲区：**供应链层缺失**。当前7层防线全部假设"从合法渠道获取的包是安全的"，而 Mini Shai-Hulud 攻击证明攻击者可以打穿发布链路本身——恶意版本通过 PyPI 官方包名分发，无对应 GitHub tag/commit，利用用户对"官方来源"的信任。

**应补充的防御：**
- Pip hash-checking / 锁定依赖版本
- 环境变量隔离——Agent 不应默认拥所有 Key
- 短期有效 token 替代永久 API Key

详见 [[supply-chain-attack-mistralai-hermes]]。

## YOLO 模式

三种激活方式：`--yolo` 参数 / `/yolo` 命令 / `HERMES_YOLO_MODE=1` 环境变量。绕过审批直接执行。
