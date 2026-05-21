# P0-1 MCP 安全审计 CI/CD 方案

> 版本：v1.0 | 状态：草案 | 审计人：鲁班（核战队·工程审计）
> 创建：2026-05-17 | 参考论文：MCP-BiFlow (arXiv:2605.07836)

---

## 1. 背景与目标

### 1.1 MCP-BiFlow 核心发现

MCP-BiFlow 论文分析了 **15,452 个真实 MCP 仓库**，发现 **118 条漏洞路径**（87 个服务器存在漏洞），证明不安全传播是 MCP 生态的**系统性故障模式**。核心攻击面：

| 风险方向 | 描述 |
|---------|------|
| **请求方→敏感操作**（Inbound） | 攻击者控制的参数传播到敏感操作（命令执行、文件写入、网络请求） |
| **响应方→主机/模型**（Outbound） | 不可信外部数据或敏感内部数据通过 MCP 输出暴露，影响主机或模型行为 |

### 1.2 本项目目标

在 Hermes Agent **接入第三方 MCP Server 之前**，自动扫描并阻断不安全的数据传播路径。将 MCP-BiFlow 的双向污点分析思路**工程化**为可重复执行的 CI/CD 检查流水线。

### 1.3 约束

- **刘伯温约束**：可验证、可测量、可失败、可回滚
- **匠石约束**：能用代码就不用模型

---

## 2. Hermes 当前 MCP Server 接入现状（调研结论）

### 2.1 接入方式

Hermes 通过 `config.yaml` 的 `mcp_servers` 段配置 MCP Server，支持两种传输方式：

```
mcp_servers:
  action-bridge:
    command: /home/zcs/.hermes/hermes-agent/venv/bin/python3
    args: ["/mnt/i/hermes/scripts/mcp-action-bridge.py"]
    timeout: 120
  project-context:
    command: /home/zcs/.hermes/hermes-agent/venv/bin/python3
    args: ["/mnt/i/hermes/scripts/project-context.py"]
    timeout: 30
```

**两种传输方式**：
- **stdio**（本地进程）：`command` + `args` — 通过 stdin/stdout 通信
- **HTTP**（远程服务）：`--url URL` — 通过 HTTP/S 端点

### 2.2 当前已注册的 MCP Server

| 服务器名称 | 类型 | 传输方式 | 暴露工具 | 安全风险评级 |
|-----------|------|---------|---------|------------|
| `action-bridge` | 自定义桥接服务 | stdio | trigger_webhook, run_script, list_hooks, custom_webhook | **高危** |
| `project-context` | 项目上下文读取 | stdio | get_context, init_context, list_projects | **低危** |
| MemOS `mcp_serve` | MOS 记忆系统 | (未激活) | chat, create_user, search_memories, add_memory, delete_memory 等 | **中危** |

### 2.3 风险分析

| 服务器 | 具体风险 |
|--------|---------|
| **action-bridge** | `custom_webhook` 允许向任意 URL 发起请求，`run_script` 执行任意路径脚本，`trigger_webhook` 暴露硬编码的 webhook URL。没有任何输入校验、URL 白名单、命令白名单。典型 **Inbound 不安全传播**。 |
| **project-context** | 读取文件系统上的 context 文件，若被符号链接攻击可读取任意文件。`init_context` 写入文件到任意路径。 |
| **MemOS mcp_serve** | 暴露 `delete_all_memories`、`create_user` 等危险操作，无认证检查。若远程暴露即为高危。 |

### 2.4 关键发现

1. **当前无安全审计流程**：接入 MCP Server 完全靠人工配置，无自动扫描
2. **无 TIRITH 策略覆盖**：Hermes 内置 TIRITH 安全策略引擎（`security.tirith_enabled: true`），但 MCP 的输入校验未接入 TIRITH
3. **无污点传播分析**：不追踪参数从请求到敏感操作的传播路径
4. **无依赖扫描**：不检查 MCP Server 依赖的第三方库漏洞
5. **无 STDIO/HTTP 端点验证**：不验证远程 MCP 端点的 TLS/身份

---

## 3. 审计方案

### 3.1 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP 安全审计 CI/CD 流水线                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① 静态扫描层 (Static Analyzer)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MCP-Audit CLI                  (Python/go)         │   │
│  │ ├─ config_audit:   验证 mcp_servers 配置合法性      │   │
│  │ ├─ taint_scan:     污点传播分析（MCP-BiFlow 简化版） │   │
│  │ ├─ dep_scan:       依赖安全扫描                     │   │
│  │ ├─ transport_audit:传输层安全审计                   │   │
│  │ └─ report:         输出审计报告 (JSON/Markdown)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ② 动态验证层 (Runtime Validator)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MCP-Sandbox                    (Docker sandbox)     │   │
│  │ ├─ 启动 MCP Server 到隔离容器                       │   │
│  │ ├─ 注入恶意 payload 验证                                    │   │
│  │ └─ 检测命令执行/文件写入/网络请求等敏感操作                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ③ CI/CD 集成层                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GitHub Actions / Makefile / Pre-commit Hook          │   │
│  │ ├─ pre-commit: 提交前扫描 mcp_servers 配置           │   │
│  │ ├─ CI: PR 时全量审计                                 │   │
│  │ └─ CD: 部署前签名验证                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 静态扫描：`mcp-audit` CLI 工具

#### 3.2.1 `config_audit` — 配置合法性检查

```bash
# 检查 config.yaml 中的 mcp_servers 配置
mcp-audit config --config ~/.hermes/config.yaml
```

**检查项**：
- `command` 路径是否在白名单中（`/home/zcs/.hermes/hermes-agent/venv/bin/python3`, `/usr/bin/python3` 等）
- `args` 中的脚本路径是否在白名单中
- `timeout` 是否设置了合理的上限（≤300s）
- `--url` 的域名是否在允许列表中
- 是否配置了 `env` 环境变量注入（禁止覆盖 `PATH`, `HOME`, `LD_PRELOAD` 等）
- 敏感标志检测（`--yolo`, `--dangerous`, `allow-elevated` 等）

**通过/失败阈值**：
- 所有检查项必须通过 → PASS
- 任何一项不通过 → FAIL + 输出具体修复建议

#### 3.2.2 `taint_scan` — 污点传播分析

这是 MCP-BiFlow 的核心思想工程化。针对 Python 实现的 MCP Server 进行简化的污点分析。

**污点源（Taint Sources）**：
- `arguments.get(...)` / `params.get(...)` / `inputSchema` 定义的参数
- `request.args` / `request.json` / `request.form`（HTTP 方式）
- 环境变量和外部文件内容

**污点汇聚点（Taint Sinks）**：
- `subprocess.run/Popen/call` — 命令执行
- `os.system` / `os.popen` — 命令执行
- `exec` / `eval` — 代码执行
- `open()` / `Path().write_text()` — 文件写入
- `urllib.request.urlopen` / `requests.post` — 网络请求（任意 URL）
- `os.remove` / `shutil.rmtree` — 文件删除
- `json.dumps(result)` 返回给调用方 — 信息泄露（Outbound）

**规则示例**：

```python
# 规则: 不可信参数→命令执行
RULES = [
    {
        "id": "MCP-001",
        "name": "taint-to-subprocess",
        "severity": "critical",
        "sources": ["arguments.get", "params.get", "inputSchema"],
        "sinks": ["subprocess.run", "subprocess.Popen", "os.system"],
        "desc": "用户可控参数直接传入命令执行函数，可能导致 RCE"
    },
    {
        "id": "MCP-002",
        "name": "taint-to-file-write",
        "severity": "high",
        "sources": ["arguments.get", "params.get"],
        "sinks": ["open().write", "Path().write_text", "os.write"],
        "desc": "用户可控参数写入文件，可能导致任意文件写入"
    },
    {
        "id": "MCP-003",
        "name": "taint-to-arbitrary-url",
        "severity": "high",
        "sources": ["arguments.get", "params.get"],
        "sinks": ["urllib.request.urlopen", "requests.post", "requests.get"],
        "desc": "用户可控参数构造网络请求，可能导致 SSRF"
    },
    {
        "id": "MCP-004",
        "name": "outbound-sensitive-data",
        "severity": "medium",
        "sources": ["os.environ", "open().read", "subprocess.check_output"],
        "sinks": ["json.dumps(result)", "result.content"],
        "desc": "敏感数据通过 MCP 输出返回给调用方，可能导致信息泄露"
    },
    {
        "id": "MCP-005",
        "name": "no-input-validation",
        "severity": "medium",
        "sources": ["arguments.get"],
        "sinks": ["(no validation before sink)"],
        "desc": "参数未经任何校验直接传入敏感函数"
    },
]
```

**实现方式**：AST 级别的正则 + 简单数据流追踪（不依赖完整 DataFlow 框架，匠石原则）

```bash
mcp-audit taint --server mcp-action-bridge.py --rules rules.yaml
```

#### 3.2.3 `dep_scan` — 依赖安全扫描

```bash
mcp-audit deps --server-dir /mnt/i/hermes/scripts/
```

- 检查 `requirements.txt` / `pyproject.toml` 中的依赖版本
- 比对各依赖的已知 CVE（使用 OSV API：https://api.osv.dev）
- 标记过时/不受支持的库

#### 3.2.4 `transport_audit` — 传输层安全审计

```bash
mcp-audit transport --url http://localhost:8000/mcp
```

- HTTP 端点：检查是否使用了 HTTPS（非 localhost 必须 HTTPS）
- 检查是否启用了 mTLS 或 API Key 认证
- stdio 端点：检查父进程身份，防止未授权调用
- 检查 `protocolVersion` 是否符合最新规范（2024-11-05 或更新）

### 3.3 动态验证：`mcp-sandbox` 沙箱测试

#### 3.3.1 架构

```
┌──────────────────────────────────────┐
│  Docker Sandbox Container            │
│  ┌──────────────┐   ┌────────────┐  │
│  │ MCP Server   │   │ Probe      │  │
│  │ (被测)       │◄──┤ (注入器)   │  │
│  │ stdin/stdout │   │            │  │
│  └──────┬───────┘   └────────────┘  │
│         │                           │
│  ┌──────▼───────┐                   │
│  │ Monitor      │                   │
│  │ (检测敏感操作)│                   │
│  └──────────────┘                   │
└──────────────────────────────────────┘
```

#### 3.3.2 测试用例

| 测试 ID | 描述 | payload 示例 | 预期检测 |
|---------|------|-------------|---------|
| `SANDBOX-001` | 命令注入 | `{"name": "run_script", "arguments": {"script_name": "notify-wechat; rm -rf /"}}` | 阻断并告警 |
| `SANDBOX-002` | 路径穿越 | `{"name": "get_context", "arguments": {"cwd": "../../../etc/passwd"}}` | 阻断 |
| `SANDBOX-003` | SSRF 测试 | `{"name": "custom_webhook", "arguments": {"url": "http://169.254.169.254/latest/meta-data/"}}` | 阻断 |
| `SANDBOX-004` | 过大 payload | 发送 10MB 的 JSON payload | 限流并告警 |
| `SANDBOX-005` | 资源耗尽 | 并发 100 个请求 | 限流 |
| `SANDBOX-006` | 编码混淆 | URL-编码/Base64 编码的命令注入 | 解码后检测 |

#### 3.3.3 运行方式

```bash
# 在沙箱中启动并测试
mcp-audit sandbox --server action-bridge --test test-suite.yaml

# 输出: sandbox-report.json
# 包含: test_id, passed/failed, evidence, duration
```

### 3.4 CI/CD 集成

#### 3.4.1 Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: mcp-config-audit
        name: MCP Config Security Audit
        entry: mcp-audit config --config .hermes/config.yaml
        language: system
        files: 'config\.yaml$'
        pass_filenames: false
```

#### 3.4.2 GitHub Actions CI

```yaml
# .github/workflows/mcp-security-audit.yml
name: MCP Security Audit
on:
  pull_request:
    paths:
      - '.hermes/config.yaml'
      - 'scripts/*-mcp*.py'
      - 'scripts/mcp-action-bridge.py'
      - 'scripts/project-context.py'

jobs:
  mcp-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install mcp-audit
        run: pip install mcp-audit  # 待发布到 PyPI
      
      - name: Static Audit
        run: |
          mcp-audit config --config .hermes/config.yaml
          mcp-audit taint --server scripts/mcp-action-bridge.py
          mcp-audit deps --server-dir scripts/
      
      - name: Sandbox Test
        run: |
          mcp-audit sandbox --server action-bridge
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: mcp-audit-report
          path: mcp-audit-report.json
```

#### 3.4.3 本地 Makefile 集成

```makefile
.PHONY: mcp-audit mcp-sandbox

# 快速审计
mcp-audit:
	mcp-audit config --config ~/.hermes/config.yaml
	mcp-audit taint --server /mnt/i/hermes/scripts/mcp-action-bridge.py
	mcp-audit taint --server /mnt/i/hermes/scripts/project-context.py

# 完整管线
mcp-audit-full: mcp-audit
	mcp-audit deps --server-dir /mnt/i/hermes/scripts/
	mcp-audit transport --server action-bridge
	mcp-audit report --format markdown --output /mnt/i/hermes/output/doc/mcp-audit-report.md

# 沙箱测试（需要 Docker）
mcp-sandbox:
	mcp-audit sandbox --server action-bridge --test test-suite.yaml
```

### 3.5 审计报告格式

```json
{
  "version": "1.0",
  "timestamp": "2026-05-17T06:00:00Z",
  "servers": [
    {
      "name": "action-bridge",
      "transport": "stdio",
      "path": "/mnt/i/hermes/scripts/mcp-action-bridge.py",
      "checks": {
        "config_audit": {"status": "FAIL", "issues": [
          {"id": "CFG-001", "severity": "high", "desc": "custom_webhook 无 URL 白名单"},
          {"id": "CFG-002", "severity": "high", "desc": "run_script 无命令白名单"}
        ]},
        "taint_scan": {"status": "FAIL", "issues": [
          {"id": "MCP-001", "path": "L224-L239", "desc": "custom_webhook 参数 url 直接传入 urlopen，无校验"},
          {"id": "MCP-003", "path": "L164-L178", "desc": "trigger_webhook payload 直接发送到外部"},
          {"id": "MCP-005", "path": "L190-L198", "desc": "script_name 无任何输入校验"}
        ]},
        "dep_scan": {"status": "PASS"},
        "sandbox": {"status": "FAIL", "tests": [
          {"id": "SANDBOX-001", "passed": false, "reason": "命令注入 payload 被执行"},
          {"id": "SANDBOX-003", "passed": false, "reason": "SSRF 到元数据端点未阻断"}
        ]}
      },
      "overall": "FAIL",
      "fix_instructions": "见 4.1 节"
    },
    {
      "name": "project-context",
      "transport": "stdio",
      "path": "/mnt/i/hermes/scripts/project-context.py",
      "checks": {
        "config_audit": {"status": "PASS"},
        "taint_scan": {"status": "WARN", "issues": [
          {"id": "MCP-002", "path": "L104-L111", "severity": "medium", "desc": "init_context 的 content 参数直接写入文件"}
        ]},
        "dep_scan": {"status": "PASS"},
        "sandbox": {"status": "PASS"}
      },
      "overall": "WARN",
      "fix_instructions": "init_context 应对写入路径和内容大小做限制"
    }
  ],
  "summary": {
    "total_servers": 2,
    "passed": 0,
    "warn": 1,
    "failed": 1,
    "total_issues": 6,
    "critical": 2,
    "high": 3,
    "medium": 1
  }
}
```

### 3.6 Pass/Fail 判定规则

| 层级 | 条件 | 结果 |
|------|------|------|
| **PASS** | 所有检查项通过，无 CRITICAL 和 HIGH 级别问题 | ✅ 允许接入 |
| **WARN** | 无 CRITICAL，≤1 个 HIGH 问题 | ⚠️ 需要审核后接入 |
| **FAIL** | 任意 CRITICAL 或 ≥2 个 HIGH 问题 | ❌ 禁止接入，修复后重审 |

---

## 4. 针对当前 MCP Server 的修复建议

### 4.1 action-bridge 修复方案

```python
# 行动项 1: URL 白名单
ALLOWED_WEBHOOK_URLS = [
    "https://hook.make.com/*",
    "https://webhook.n8n.local/*",
]
# 禁止访问内网 IP 和元数据服务

# 行动项 2: 命令白名单
ALLOWED_SCRIPTS = [
    "/mnt/i/hermes/scripts/notify-wechat.py",
    "/mnt/i/hermes/scripts/daily-digest.sh",
]

# 行动项 3: 输入校验
def validate_script_name(name: str) -> bool:
    if name not in ALLOWED_SCRIPTS:
        return False
    if ".." in name or "/" in name:
        return False  # 防止路径穿越
    return True

# 行动项 4: 移除 custom_webhook 工具（或限制为 GET-only 且 URL 白名单）
```

### 4.2 project-context 修复方案

```python
# 行动项: init_context 限制
ALLOWED_CONTEXT_DIRS = ["/mnt/i/hermes", "/home/zcs"]
MAX_CONTENT_SIZE = 10000  # 10KB

def validate_context_path(path: str) -> bool:
    resolved = os.path.realpath(path)
    for allowed in ALLOWED_CONTEXT_DIRS:
        if resolved.startswith(allowed):
            return True
    return False
```

---

## 5. 实现路线图与工时估算

### 5.1 阶段划分

| 阶段 | 任务 | 产出 | 工时 | 优先级 |
|------|------|------|------|--------|
| **P0** | `mcp-audit config`：配置检查模块 | mcp-audit CLI（config 子命令） | 4h | 🔴 立即 |
| **P0** | `mcp-audit taint`：AST 污点扫描 | taint 子命令 + rules.yaml | 8h | 🔴 立即 |
| **P0** | action-bridge 紧急修复 | 添加 URL/命令白名单、输入校验 | 2h | 🔴 立即 |
| **P1** | `mcp-audit sandbox`：Docker 沙箱测试 | sandbox 子命令 + test-suite | 8h | 🟡 本周 |
| **P1** | project-context 修复 | 路径校验，大小限制 | 1h | 🟡 本周 |
| **P1** | Pre-commit Hook 集成 | `.pre-commit-config.yaml` | 1h | 🟡 本周 |
| **P2** | GitHub Actions Workflow | `.github/workflows/` | 2h | 🟢 两周内 |
| **P2** | `mcp-audit deps`：依赖扫描 | deps 子命令 + OSV API 集成 | 4h | 🟢 两周内 |
| **P2** | `mcp-audit transport`：传输层审计 | transport 子命令 | 3h | 🟢 两周内 |
| **P2** | 报告格式与 Web UI 展示 | 报告模板 + HTML 渲染 | 3h | 🟢 可选 |
| **合计** | | | **36h** | |

### 5.2 总工时

| 类别 | 工时 |
|------|------|
| **核心工具开发**（P0-P1） | 24h |
| **CI/CD 集成**（P1-P2） | 6h |
| **现有 Server 修复**（P0） | 3h |
| **文档与测试** | 3h |
| **合计** | **36h（约 4.5 人日）** |

### 5.3 依赖项

- Python ≥ 3.10
- Docker（动态沙箱测试用）
- 网络访问：GitHub API / OSV API
- Hermes Agent `config.yaml` 读写权限

---

## 6. 可验证性设计

### 6.1 可验证

每个审计步骤有明确输入/输出规范：

```bash
# 验证方式 1: 运行审计
mcp-audit config --config test/fixtures/bad-config.yaml \
  --expected-fail "CFG-001" \
  --verbose

# 验证方式 2: 测试一致性
mcp-audit taint --server test/fixtures/taint-example.py \
  | jq '.checks.taint_scan.issues | length' \
  | grep -q 3  # 预期发现 3 个问题
```

### 6.2 可测量

所有审计输出含 `severity`、`count`、`pass_rate` 指标：

```json
{
  "metrics": {
    "config_pass_rate": 0.85,
    "taint_critical_count": 2,
    "sandbox_test_pass_rate": 0.67,
    "overall_score": 0.47
  }
}
```

### 6.3 可失败

每个阶段独立判定：
- 配置检查失败 → 中止流水线
- 污点扫描发现 CRITICAL → 中止
- 沙箱测试失败 → 告警但不中止（需人工审核）

### 6.4 可回滚

- 每次审计报告写入版本化目录：`/mnt/i/hermes/output/doc/mcp-audit-reports/YYYY-MM-DD_HHMMSS.json`
- MCP Server 配置通过 Git 管理，审计通过的 commit 记录在案
- 紧急回滚命令：`mcp-audit rollback --report mcp-audit-report-2026-05-17.json`

---

## 7. 附录

### 7.1 参考论文

- MCP-BiFlow: "Unsafe by Flow: Uncovering Bidirectional Data-Flow Risks in MCP Ecosystem" (arXiv:2605.07836, May 2026)
- 核心方法：MCP-aware 入口点恢复 + 协议特定污点建模 + 过程间传播分析

### 7.2 相关文件

| 路径 | 说明 |
|------|------|
| `/mnt/i/hermes/scripts/mcp-action-bridge.py` | 当前高危 MCP Server（需紧急修复） |
| `/mnt/i/hermes/scripts/project-context.py` | 中等风险 MCP Server |
| `/home/zcs/MemOS/src/memos/api/mcp_serve.py` | MemOS 记忆系统 MCP Server |
| `/mnt/i/hermes/.hermes/config.yaml.bak.*` | 当前配置备份 |
| `/mnt/i/hermes/Hermes_Agent_操作指令集.md` | Hermes MCP 命令参考（14 章） |

### 7.3 术语表

| 术语 | 说明 |
|------|------|
| MCP | Model Context Protocol，模型上下文协议 |
| MCP-BiFlow | 双向 MCP 污点分析框架（论文） |
| Taint Source | 污点源，不可信数据入口 |
| Taint Sink | 污点汇聚点，敏感操作/暴露点 |
| Inbound Risk | 请求方到服务方的风险 |
| Outbound Risk | 服务方到主机/模型的风险 |
| SSRF | 服务端请求伪造 |
| RCE | 远程代码执行 |
| TIRITH | Hermes Agent 内置安全策略引擎 |
