# Hermes Agent MCP 模拟验证层方案

## 1. 问题背景 & 目标

### 1.1 现状

Hermes Agent 通过 MCP (Model Context Protocol) 连接外部工具服务器。当 LLM 决定调用一个 MCP 工具时，调用流程为：

```
LLM → tool_calls → AIAgent._execute_tool_calls()
  → _execute_tool_calls_sequential() or concurrent()
  → AIAgent._invoke_tool() or handle_function_call()
  → registry.dispatch()
  → _make_tool_handler() → _call_once() → server.session.call_tool()
```

**问题**：此流程将 MCP 调用直接发给外部服务器，没有提前验证的环节。如果 LLM 生成的参数不合理（路径穿越、参数越界、非预期操作等），会直接作用于外部系统。

### 1.2 目标

在 Hermes Agent 发出 MCP 调用**之前**，插入一个「模拟验证层」：

1. **模拟执行**：不真正调用 MCP 服务器，而是根据工具的 input schema 和参数语义做轻量级验证
2. **异常阻断**：如果模拟结果异常（参数无效、安全风险、资源不存在等），阻止实际调用并返回友好的错误信息
3. **透明降级**：验证通过则正常执行，对 LLM 无感知

### 1.3 约束条件

- 不训练世界模型（MCP-Cosmos 论文的完整方案过于重）
- 能用代码就不用模型（匠石约束）
- 可验证/可测量/可失败/可回滚（刘伯温约束）

---

## 2. MCP 调用完整链路分析

### 2.1 核心代码文件

| 文件 | 角色 | 关键函数 |
|------|------|----------|
| `tools/mcp_tool.py` | MCP 客户端核心 | `_make_tool_handler()`, `_call_once()`, `register_mcp_servers()`, `_register_server_tools()` |
| `tools/registry.py` | 统一工具注册中心 | `register()`, `dispatch()`, `get_toolset_for_tool()` |
| `model_tools.py` | 工具调用调度器 | `handle_function_call()` (L699-L838) |
| `run_agent.py` | Agent 主循环 | `_execute_tool_calls()` (L10206), `_invoke_tool()` (L10248), `_execute_tool_calls_sequential()` (L10761), `_execute_tool_calls_concurrent()` (L10360) |
| `agent/tool_guardrails.py` | 已有 guardrail 机制 | `ToolCallGuardrail.before_call()`, `ToolGuardrailDecision` |

### 2.2 调用链详解

#### 路径 A: 顺序执行 (_execute_tool_calls_sequential)

```
run_agent.py L10761 _execute_tool_calls_sequential()
  ├── L10792-10800: get_pre_tool_call_block_message()  ← 插件钩子：可阻断
  ├── L10803-10806: _tool_guardrails.before_call()      ← 已有 guardrail
  ├── L10810: _execution_blocked 检查
  └── L10830-10841: 实际执行（内联调用 handle_function_call）
```

#### 路径 B: 并发执行 (_execute_tool_calls_concurrent)

```
run_agent.py L10360 _execute_tool_calls_concurrent()
  └── L10406+: ThreadPoolExecutor → _invoke_tool()
       ├── L10257-10268: get_pre_tool_call_block_message()  
       └── L10326: handle_function_call()
```

#### 路径 C: handle_function_call (最终统一入口)

```
model_tools.py L699 handle_function_call()
  ├── L726: coerce_tool_args()          ← 参数类型强制转换
  ├── L742-757: pre_tool_call 钩子      ← 插件可阻断
  ├── L780-790: registry.dispatch()    ← 真正分派
  └── L835-838: 异常处理
```

#### MCP 工具 handler (_make_tool_handler)

```
tools/mcp_tool.py L2158 _make_tool_handler()
  ├── L2176-2190: 断路器检查           ← 已有一个"半模拟"机制（失败计数器）
  ├── L2192-2198: 服务器连接检查
  ├── L2200-2248: _call() 异步调用     ← 真正发往 MCP 服务器
  ├── L2250-2297: _call_once() + 错误处理
  └── 认证恢复、会话过期重试等
```

### 2.3 关键拦截点

| 拦截点 | 位置 | 当前能力 | 可插拔性 |
|--------|------|----------|----------|
| **pre_tool_call 钩子** | `model_tools.py:742` + `run_agent.py:10792` | 插件系统可阻断 | ✅ 已有 hook 机制 |
| **tool_guardrails** | `run_agent.py:10803` | 回路检测 (重复调用、零进展) | ✅ 已有类 |
| **断路器** | `mcp_tool.py:2176` | 连续失败后临时阻断 | ✅ 已有机制 |
| **registry.dispatch** | `registry.py:373` | 通用分派 | 可通过注册 wrapper |
| **_invoke_tool** | `run_agent.py:10248` | 特殊工具 + handle_function_call | 可直接修改 |

---

## 3. 模拟验证层设计方案

### 3.1 总体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         Agent Loop                              │
│  run_agent.py:_execute_tool_calls_sequential()                  │
│                                                                  │
│  ┌─────────────┐   ┌──────────────────┐   ┌──────────────────┐ │
│  │ pre_tool_call│ → │ 模拟验证层 (NEW) │ → │ handle_function │ │
│  │ hook (插件)  │   │                  │   │ _call()          │ │
│  └─────────────┘   └──────────────────┘   └──────────────────┘ │
│                           │                                      │
│                           ▼                                      │
│                    ┌──────────────────┐                         │
│                    │ registry.dispatch│                         │
│                    │ → MCP server     │                         │
│                    └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 核心策略：三层验证

我们设计三层验证，每层可独立启用/关闭：

```
Layer 1: Schema 合规验证（轻量，无外部调用）
  - 参数类型、格式、required 字段匹配
  - 通过 jsonschema 库验证

Layer 2: 语义合理性验证（轻量，无外部调用）
  - 路径穿越检测（路径参数中检测 ../ 等）
  - 参数值域检查（整型范围、字符串长度）
  - 已知危险操作检测（命令行注入、危险文件写入）
  - 针对特定 MCP 工具类型的专有规则

Layer 3: 模拟执行验证（可选，需配置）
  - 对幂等/只读调用，调用 MCP server 的 list_resources/read_resource 做预确认
  - 对比结果与预期 schema
  - 仅对 MCP 工具生效，不影响内置工具
```

### 3.3 验证规则引擎

验证规则以 **静态配置 + 代码策略** 结合：

#### 静态配置 (config.yaml)

```yaml
mcp_simulation_layer:
  enabled: true
  log_level: info            # debug | info | warn
  
  # 各层的开关
  layers:
    schema_validation: true
    semantic_validation: true
    simulation_execution: false   # 默认关闭，开销较大
  
  # 阻断策略
  block_on:
    schema_error: true
    semantic_error: true
    simulation_error: false
  
  # 工具级别覆盖
  tool_overrides:
    mcp_filesystem_write_file:
      block_on_schema: true
      block_on_semantic: true
    mcp_github_create_issue:
      block_on_schema: false   # 允许宽松
      block_on_semantic: false
  
  # 安全规则配置
  path_injection_patterns:
    - "../"
    - "..\\"
    - "/etc/"
    - "/proc/"
    
  max_string_length: 10000
  max_array_length: 1000
```

#### 代码策略 (Python)

```python
# tools/mcp_simulation.py (NEW)

class MCPSimulationValidator:
    """MCP 模拟验证器"""
    
    RULES: dict[str, list[ValidationRule]] = {
        # 按工具名前缀分组
        "mcp_filesystem": [
            PathTraversalRule(),
            FileSizeRule(max_bytes=10*1024*1024),
        ],
        "mcp_github": [
            GitHubIssueFormatRule(),
        ],
        # 默认规则（适用所有 MCP 工具）
        "*": [
            SchemaValidationRule(),
            ParameterTypeRule(),
        ],
    }
    
    def validate(self, tool_name: str, args: dict) -> ValidationResult:
        """执行验证，返回结果"""
        ...
```

### 3.4 集成方案 A：插件方式（推荐，0 侵入）

#### 原理

利用 Hermes Agent 已有的 **pre_tool_call hook 机制**。插件系统在 `model_tools.py:742` 和 `run_agent.py:10792` 两处注册了 `get_pre_tool_call_block_message()`。实现一个插件，在该钩子中执行模拟验证，返回 blocking message。

#### 新增文件

```
~/.hermes/hermes-agent/plugins/mcp_simulation/
├── manifest.yaml
├── __init__.py
└── simulation.py
```

#### manifest.yaml

```yaml
name: mcp-simulation
version: "1.0.0"
description: "MCP 工具调用模拟验证层"
author: "Hermes Core"
hooks:
  pre_tool_call: simulation.pre_tool_call_handler
```

#### simulation.py 核心逻辑

```python
# plugins/mcp_simulation/simulation.py

import json
import logging
import os
import re
from typing import Optional, Dict, Any

from hermes_cli.plugins import Plugin

logger = logging.getLogger(__name__)

# ── 第三层 ── ── ── ── ── ── ── ── ──
# 注册为 pre_tool_call hook handler

def pre_tool_call_handler(
    tool_name: str,
    tool_input: Dict[str, Any],
    **kwargs,
) -> Optional[Dict]:
    """pre_tool_call 钩子处理函数。
    
    返回 None = 放行
    返回 {"action": "block", "message": "..."} = 阻断
    """
    # 只处理 MCP 工具
    toolset = _get_toolset(tool_name)
    if not toolset or not toolset.startswith("mcp-"):
        return None  # 非 MCP 工具，放行
    
    validator = _get_validator()
    result = validator.validate(tool_name, tool_input)
    
    if not result.passed:
        msg = _format_block_message(tool_name, result)
        logger.warning("MCP 模拟验证阻断: %s - %s", tool_name, msg)
        return {"action": "block", "message": msg}
    
    return None  # 放行
```

### 3.5 集成方案 B：直接修改 handle_function_call（更可靠）

#### 原理

在 `model_tools.py:handle_function_call()` 中，定位后 `coerce_tool_args()` 之后、`pre_tool_call` 钩子之前，插入 MCP 工具检测 + 验证逻辑。

#### 修改位置

**`model_tools.py` L726 之后，L742 之前** 插入：

```python
# ── MCP 模拟验证层 ──
if not skip_pre_tool_call_hook:
    try:
        from tools.mcp_simulation import validate_mcp_call
        block_msg = validate_mcp_call(function_name, function_args)
        if block_msg is not None:
            return json.dumps({"error": block_msg}, ensure_ascii=False)
    except Exception as _sim_err:
        logger.debug("MCP simulation validation error: %s", _sim_err)
# ── ── ── ── ── ── ── ── ── ── ── ──
```

#### 新增文件

```
~/.hermes/hermes-agent/tools/mcp_simulation.py  (NEW)
```

### 3.6 方案对比

| 维度 | 方案 A（插件） | 方案 B（直接修改） |
|------|---------------|-------------------|
| 侵入性 | 零侵入 | 中等（改 3 行） |
| 部署难度 | 放目录即可 | 改核心代码 |
| 可插拔 | ✅ 可随时启用/禁用 | ❌ 硬编码 |
| 可靠性 | 依赖 hook 接口稳定 | ✅ 更直接可靠 |
| 性能开销 | 略有 hook 传递 | ✅ 直接调用 |
| 测试覆盖 | 插件级测试 | 需要修改单元测试 |
| **推荐指数** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**推荐采用方案 B + 方案 A 混合**：核心逻辑放在 `tools/mcp_simulation.py`（方案 B 的新文件），然后在 `model_tools.py` 中引用。同时，如果用户希望更灵活的启用/禁用，可以通过方案 A 插件方式注册 hook。

---

## 4. 详细实现计划

### 4.1 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `tools/mcp_simulation.py` | **新建** | 模拟验证核心引擎：验证规则、Schema 校验、语义分析 |
| `model_tools.py` | **修改** | L726 后插入 ~10 行调用代码 |
| `hermes_cli/plugins/mcp_simulation/manifest.yaml` | **新建** | 可选插件的 manifest |
| `hermes_cli/plugins/mcp_simulation/__init__.py` | **新建** | 可选插件的入口 |
| `tests/tools/test_mcp_simulation.py` | **新建** | 验证层单元测试 |

### 4.2 `tools/mcp_simulation.py` 详细设计

```python
"""
MCP 模拟验证层 — 在 MCP 工具调用前执行轻量级模拟验证。

架构：
  validate_mcp_call()  — 统一入口，供 handle_function_call 调用
  MCPSimulationEngine  — 验证引擎，按层执行规则
  ValidationRule       — 规则基类
  SchemaRule           — Schema 合规规则
  SemanticRule         — 语义合理性规则
  PathTraversalRule    — 路径穿越检测
  ConfigLoader         — 从 config.yaml 加载配置
  
使用：
  from tools.mcp_simulation import validate_mcp_call
  block_msg = validate_mcp_call("mcp_fs_read", {"path": "/tmp/test.txt"})
  if block_msg: return {"error": block_msg}
"""

# 核心接口
def validate_mcp_call(tool_name: str, args: dict) -> Optional[str]:
    """
    对 MCP 工具调用执行模拟验证。
    
    Args:
        tool_name: 注册的工具名称（带 mcp_ 前缀）
        args: 参数字典
        
    Returns:
        None → 验证通过，放行
        str → 阻断消息，应作为 error 返回给 LLM
    """
    ...

# 验证结果  
@dataclass
class ValidationResult:
    passed: bool
    message: str = ""
    layer: str = ""
    rule: str = ""

# 规则基类
class ValidationRule(ABC):
    @abstractmethod
    def validate(self, tool_name: str, args: dict) -> ValidationResult:
        ...

# Schema 合规规则
class SchemaValidationRule(ValidationRule):
    """使用 jsonschema 库验证参数是否符合工具 input schema"""
    def validate(self, tool_name: str, args: dict) -> ValidationResult:
        schema = registry.get_schema(tool_name)
        if not schema:
            return ValidationResult(passed=True)
        # 提取 input schema 中的 parameters 部分
        params_schema = schema.get("parameters", {})
        try:
            jsonschema.validate(instance=args, schema=params_schema)
            return ValidationResult(passed=True)
        except jsonschema.ValidationError as e:
            return ValidationResult(
                passed=False,
                message=f"参数 Schema 校验失败: {e.message}",
                layer="schema",
                rule="SchemaValidation"
            )

# 路径穿越检测
class PathTraversalRule(ValidationRule):
    """检测路径参数中的目录穿越攻击"""
    PATTERNS = [
        re.compile(r"(\.\./|\.\.\\)"),
        re.compile(r"^/etc/"),
        re.compile(r"^/proc/"),
        re.compile(r"^/sys/"),
        re.compile(r"^/dev/"),
    ]
    
    def validate(self, tool_name: str, args: dict) -> ValidationResult:
        for key, value in _flatten_args(args):
            if isinstance(value, str) and ("path" in key.lower() or "file" in key.lower() or "dir" in key.lower()):
                for pattern in self.PATTERNS:
                    if pattern.search(value):
                        return ValidationResult(
                            passed=False,
                            message=f"检测到路径穿越: 参数 '{key}' 包含非法路径 '{value}'",
                            layer="semantic",
                            rule="PathTraversal"
                        )
        return ValidationResult(passed=True)

# 参数值域检查
class ParameterBoundsRule(ValidationRule):
    """检查数值参数是否在合理范围内"""
    BOUNDS = {
        "limit": (1, 1000),
        "timeout": (1, 3600),
        "max_results": (1, 500),
        "count": (1, 1000),
    }
    
    def validate(self, tool_name: str, args: dict) -> ValidationResult:
        for key, (min_v, max_v) in self.BOUNDS.items():
            if key in args and isinstance(args[key], (int, float)):
                if args[key] < min_v or args[key] > max_v:
                    return ValidationResult(
                        passed=False,
                        message=f"参数 '{key}' 值 {args[key]} 超出允许范围 [{min_v}, {max_v}]",
                        layer="semantic",
                        rule="ParameterBounds"
                    )
        return ValidationResult(passed=True)
```

### 4.3 `model_tools.py` 修改点

在 `handle_function_call()` 函数的 L726 (`function_args = coerce_tool_args(...)`) 之后，L742 (`if not skip_pre_tool_call_hook:`) 之前插入：

```python
    # ── MCP 模拟验证层 ──
    # 在执行 MCP 工具前执行轻量级模拟验证，阻止异常调用
    if function_name.startswith("mcp_"):
        try:
            from tools.mcp_simulation import validate_mcp_call
            block_msg = validate_mcp_call(function_name, function_args)
            if block_msg is not None:
                logger.info(
                    "MCP simulation blocked %s(%s): %s",
                    function_name, function_args, block_msg,
                )
                return json.dumps({"error": block_msg}, ensure_ascii=False)
        except Exception:
            logger.debug("MCP simulation error (fail-open)", exc_info=True)
            # fail-open: 验证异常时不阻断，放行
    # ── ── ── ── ── ── ── ── ── ── ──
```

**修改量**：约 15 行新增代码，0 行删除。

### 4.4 规则激活矩阵

| 规则 | 默认状态 | 适用 MCP 工具 | 响应 |
|------|----------|---------------|------|
| Schema Validation | ON | 所有 | 阻断 + 错误提示 |
| Required Field Check | ON | 所有 | 阻断 + 提示缺失字段 |
| Type Coercion Fix | ON | 所有 | 自动修正 + 不阻断 |
| Path Traversal | ON | filesystem/* | 阻断 + 安全警告 |
| Parameter Bounds | ON | 所有 | 阻断 + 范围提示 |
| String Length Check | ON | 所有 | 阻断 + 长度提示 |
| Array Size Check | ON | 所有 | 阻断 + 大小提示 |
| Dangerous Command | ON | shell/*, exec/* | 阻断 + 安全警告 |
| Auth Token Exposure | ON | 所有 | 阻断 + 安全警告 |
| Simulation Execute | OFF | 幂等工具 | 警告 + 不阻断 |

### 4.5 可验证性设计

每条阻断记录均输出结构化日志：

```python
{
    "event": "mcp_simulation_blocked",
    "tool_name": "mcp_filesystem_write_file",
    "function_args": {"path": "/etc/passwd", "content": "..."},
    "layer": "semantic",
    "rule": "PathTraversal",
    "message": "检测到路径穿越: 参数 'path' 包含非法路径 '/etc/passwd'",
    "timestamp": "2026-05-17T06:30:00Z",
    "session_id": "sess_xxx"
}
```

### 4.6 可回滚设计

- **fail-open**：验证层抛异常时不阻断（`except Exception: pass`），保证不影响原有流程
- **配置开关**：`mcp_simulation_layer.enabled: false` 完全禁用
- **渐进式部署**：先 warn 不 block，确认无误后再开启 block 模式
- **工具级别覆盖**：可以对特定 MCP 工具单独配置策略

---

## 5. 估算工时

| 模块 | 工时 (人时) | 说明 |
|------|------------|------|
| `mcp_simulation.py` Schema 校验引擎 | 4h | jsonschema 集成 + 规则框架 |
| `mcp_simulation.py` 语义规则实现 | 6h | 路径穿越、值域、字符串等 8+ 规则 |
| `mcp_simulation.py` 配置加载 | 2h | config.yaml 读取 + 规则开关 |
| `model_tools.py` 修改 + 集成 | 1h | 插入 15 行代码 + import |
| 单元测试 | 4h | 覆盖各规则 + 边界情况 |
| 集成测试 | 2h | 与真实 MCP server 联调 |
| 文档 | 1h | README + 代码注释 |
| **合计** | **20h** | ~2.5 人天（含测试和文档） |

---

## 6. 风险评估

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| 验证层误阻断正常调用 | 🔴 高 | fail-open 机制 + 渐进式部署 (warn → block) |
| 性能开销影响 LLM 响应速度 | 🟡 中 | 验证在 1ms 内完成；支持按工具关闭 |
| Schema 不完全导致漏检 | 🟡 中 | 语义规则作为补充；支持自定义规则扩展 |
| 与现有 pre_tool_call 插件冲突 | 🟢 低 | 验证层先执行，插件后执行；互不干扰 |
| MCP 工具名不匹配 mcp_ 前缀 | 🟢 低 | `registry.get_toolset_for_tool()` 更可靠 |

---

## 7. 后续扩展

1. **MCP-Cosmos 轻量版**：对非幂等 MCP 工具做"dry-run"——先调用 MCP 服务器的 capabilities 接口获取工具是否支持 dry-run
2. **统计仪表板**：将阻断事件上报至 metrics 系统，分析哪些 MCP 工具调用被频繁阻断
3. **自适应规则**：根据历史阻断数据自动调整规则启停

---

## 附录 A: 代码位置速查

```
tools/mcp_tool.py               # MCP 客户端，3408 行
  L2158: _make_tool_handler()   # 每个 MCP 工具的 handler 工厂
  L2905: _register_server_tools() # 注册 MCP 工具到 registry
  L3042: register_mcp_servers()  # 批量注册入口

model_tools.py                  # 工具调度核心，867 行
  L699: handle_function_call()  # 主调度函数 ← 插入点

run_agent.py                    # Agent 主循环，15411 行
  L10206: _execute_tool_calls()  # 工具调用分派
  L10248: _invoke_tool()         # 单工具调用（并发路径）
  L10761: _execute_tool_calls_sequential() # 顺序执行路径

tools/registry.py               # 工具注册中心，563 行
  L373: dispatch()              # 最终分派

agent/tool_guardrails.py        # 已有回路检测
  L144: ToolGuardrailDecision   # 决策数据结构
  L238: before_call()           # 调用前检查
```

## 附录 B: MCP 调用 + 模拟验证层完整流程图

```
AIAgent.run_conversation()
  │
  ▼
API call → 得到 tool_calls
  │
  ▼
_execute_tool_calls()
  ├── _should_parallelize_tool_batch() → 判断是否并发
  │
  ├── _execute_tool_calls_sequential()
  │   ├── pre_tool_call hook (插件)
  │   ├── tool_guardrails.before_call()
  │   ├── [MCP 模拟验证层] ← NEW
  │   │   ├── Schema Validation
  │   │   ├── Semantic Validation  
  │   │   └── (可选) Simulation Execution
  │   ├── handle_function_call()
  │   │   ├── coerce_tool_args()
  │   │   ├── [MCP 模拟验证层] ← 双重保障
  │   │   ├── pre_tool_call hook
  │   │   └── registry.dispatch()
  │   └── → MCP server.call_tool()
  │
  └── _execute_tool_calls_concurrent()
      └── (同上，通过 _invoke_tool())
```

---

*文档版本: v1.0 | 2026-05-17*
