---
entity_type: tool
first_seen: 2026-05-14
source: https://github.com/Hmbown/DeepSeek-TUI
note: 终端原生 DeepSeek V4 编程 Agent，Rust/MIT，27.8k Stars。非DeepSeek官方产品。
---

# DeepSeek-TUI

终端原生 AI 编程 Agent，由独立开发者 Hunter Bown 基于 DeepSeek V4 构建。Rust 编写，MIT 开源。

## 基本数据

- **GitHub：** Hmbown/DeepSeek-TUI，27.8k Stars，2.3k Forks（2026-05-14）
- **语言：** Rust 95.4%
- **许可：** MIT
- **当前版本：** v0.8.35
- **安装：** npm / Cargo / Homebrew / 二进制下载 / Docker

## 核心能力

| 能力 | 说明 |
|------|------|
| 三种模式 | Plan（只读分析）/ Agent（交互确认）/ YOLO（全自动） |
| 1M-token 上下文 | 可吞入中型代码库，prefix-cache 约 90% 成本折扣 |
| 子Agent并发 | 默认10个并行，可配至20个 |
| Auto Mode | flash 模型判断复杂度，自动选 pro 或 flash |
| Skills 系统 | 按需加载 SKILL.md，按描述匹配 |
| MCP 支持 | 连接 Model Context Protocol 服务器 |
| 沙箱 | Seatbelt (macOS) / Landlock (Linux) / Job Objects (Windows) |
| 会话保存/恢复 | Checkpoint + 回滚 |

## 成本

| 模型 | 输入成本 (per 1M tokens) |
|------|------------------------|
| DeepSeek V4 Flash | $0.14 |
| Claude Opus 4.7 (Claude Code用) | ~$15.00 |

约 Claude Code 的 1/100 成本。实测：bug修复+应用开发总共 9.47 元。

## 局限

- **模型锁定：** 只能用 DeepSeek V4 系列，不能切其他模型
- **插件生态：** Skills 社区内容稀疏
- **文档：** 教程/cookbook 滞后，靠社区补
- **Windows：** 支持但次要，shell 执行路径有边缘问题
- **Agent 工程成熟度：** 与 Codex 有差距（界面、审计通过率）

## 竞争定位

介于 Claude Code（10x成本，成熟生态）和 Cursor/Windsurf（IDE集成，GUI友好）之间。核心卖点是极致性价比 + DeepSeek V4 专属优化。
