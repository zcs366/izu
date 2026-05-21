# Hermes Doctor 彻底诊断报告 2026-05-16

## 概要

| 等级 | 已修复 | 待处理 | 总计 |
|------|--------|--------|------|
| 🔴 致命 | 1 | 1 | 2 |
| 🟠 严重 | 0 | 2 | 2 |
| 🟡 一般 | 0 | 3 | 3 |
| ⚪ 轻微 | 0 | 4 | 4 |
| **合计** | **1** | **10** | **11** |

---

## 🔴 致命级（立即处理）

### ✅ FIXED: Gateway 崩溃轮询

**症状**: `hermes-gateway.service` 启动即崩溃 → systemd 自动重启 → 再崩溃 → 无限循环
**根因**: `config.yaml` 第521行 feishu.home_channel 格式错误：

```
# 旧的（错误）
home_channel: oc_78369cca70e5beb4f88b34e933593b1f

# 新的（正确）
home_channel:
  platform: feishu
  chat_id: oc_78369cca70e5beb4f88b34e933593b1f
```

**处理**: 已修复，gateway 已恢复运行（PID 2827, running 50s+），cron 调度已恢复。

---

### ❌ PENDING: C: 盘爆满警告（96%）

**症状**: `df -h /mnt/c/` → **519G 总容量，已用 493G，仅剩 26G（4%）**
**风险**: Windows 系统盘写满会导致系统不稳定、WSL 故障、数据库损坏
**溯源方向**:
```
# 查大目录
du -sh /mnt/c/Users/Administrator/* | sort -rh | head -10

# 常见大户：node_modules / AppData / 微信 / 回收站
```
**建议**: 
1. 清理 `C:\Users\Administrator\AppData\Local\Temp`
2. 清理 `C:\Windows\Temp`
3. 微信文件存储迁移到 D 盘
4. 运行 `cleanmgr` 清理系统文件
5. 考虑扩展 C 盘或迁移大文件

---

## 🟠 严重级（需要关注）

### ❌ PENDING: Gemini API Key 无效

**症状**: `hermes doctor` → `✗ gemini (invalid API key)`
**影响**: 影响 `auxiliary.vision` 的 fallback 路由，当前 vision 走 `lm-studio`（本地）可以绕开
**处理**: 检查 `.env` 中 `GOOGLE_API_KEY` 和 `GEMINI_API_KEY` 是否过期，重新申请
- 当前 base_url: `https://generativelanguage.googleapis.com/v1beta/openai/v1`
- 免费额度: Gemini 2.0 Flash 免费，2.5 Pro 付费

### ❌ PENDING: Hermes 落后上游 447 个 commit

**症状**: `hermes --version` → `v0.13.0`，`Update available: 447 commits behind`
**风险**: 漏洞修复、新功能、API 变更的缺失逐渐累积
**处理**: `hermes update`（但需先评估 breaking changes）
- v0.13.0 → 后续版本可能改了 home_channel 格式等配置结构
- 升级前建议 `cp -r ~/.hermes ~/.hermes.backup`
- 升级后可能需要 `hermes config migrate`

---

## 🟡 一般级（计划内修复）

### ❌ PENDING: 2 个 cron job 因余额不足失败（402）

**症状**:
- `4494706feb8b`（个人·周五·古代学术与出版业）: **HTTP 402: Insufficient Balance**
- `cb51d123758f`（群·周五·文化艺术乡村民俗）: **HTTP 402: Insufficient Balance**
**根因**: 向 yuanbao 发送消息时，源宝 API 账户余额不足
**影响**: 昨日（5/15）这两条内容未投递到 yuanbao 群
**处理**: 检查 yuanbao 账户余额/充值。可通过 `hermes cron run <id>` 重试

### ❌ PENDING: Discord Unknown Channel（404）

**症状**: 日志显示 `discord.errors.NotFound: 404 Not Found (error code: 10003): Unknown Channel`
**影响**: Gateway 尝试向已删除/不可见的 Discord 频道发送消息（重启通知等）
**处理**: 确认 Discord 中是否有已删除的频道尚在配置中，清理 `free_response_channels` 或删除老的频道引用

### ❌ PENDING: MCP 服务器初始连接失败

**症状**:
| MCP Server | 状态 | 
|---|---|
| `project-context` | ✗ 连接关闭 |
| `action-bridge` | ✗ 连接关闭 |
| `tinyfish` | ✗ 连接关闭 |
| `midscene-web` | ✗ 超时 |

**分析**: 这些都是 gateway 启动时的初始连接尝试（3次重试后放弃），不影响会话中的按需加载。typical stderr/stdin 协议问题。
**处理**: 
- `project-context`、`action-bridge`: Python stdio MCP 脚本在 gateway 环境需要额外调试，非紧急
- `tinyfish`: 远程 MCP，网络/代理问题
- `midscene-web`: npm exec `@midscene/web-mcp` 超时，可能 npm registry 慢或依赖缺失

---

## ⚪ 轻微级（可忽略）

### ℹ️ PENDING: Alibaba Cloud Coding Plan 404
- 非必需，未配 key，仅在联通性测试中报 404

### ℹ️ PENDING: OAuth 登录未配置
- Nous Portal / OpenAI Codex / Google Gemini OAuth / MiniMax OAuth — 全都没登录，但不是必需的（API key 已够用）

### ℹ️ PENDING: 可选工具依赖未满足
- `computer_use` / `homeassistant` / `rl` / `messaging` / `hermes-yuanbao` / `spotify` — 均为可选工具，按需启用

### ℹ️ PENDING: 大量可选 API key 未配置
- 60+ 可选 key 留空，**正常现象**。核心功能（DeepSeek、OpenRouter、DashScope、MiniMax CN）均已就绪

---

## ✅ 系统健康项目

| 项目 | 状态 |
|------|------|
| Hermes 版本 | v0.13.0 (2026.5.7) |
| Python 环境 | 3.11.15 (venv active) |
| 配置文件 | config.yaml v23 ✓ |
| .env 存在 | ✓ |
| 核心 API 连通 | OpenRouter ✓ DeepSeek ✓ DashScope ✓ MiniMax CN ✓ |
| Skills | 119 enabled (70 builtin + 49 local) |
| 记忆系统 | holographic provider active ✓ |
| SessionDB | 363 sessions, 正常 |
| 系统目录 | cron/sessions/logs/skills/memories 完整 |
| SOUL.md | ✓ (persona 已配置) |
| 系统服务 | systemd linger enabled ✓ |
| 基础工具链 | git ✓ rg ✓ docker ✓ Node.js ✓ Python ✓ |
| 代理配置 | HTTP_PROXY=127.0.0.1:7890 ✓ |
| WSL | systemd=true ✓ default=zcs ✓ |
| tmux | wiki-webhook session active ✓ |

---

## 处理清单（按优先级）

1. **今日**：清理 C 盘，释放至少 30-50G 空间
2. **本周**：检查 Gemini API key，考虑重新申请
3. **本周**：检查 yuanbao 余额，重试失败的两个 cron job
4. **规划**：评估 `hermes update`（447 commits behind），备份后执行
5. **空闲**：调试 MCP 服务器连接问题
6. **可选**：清理 Discord 频道引用
