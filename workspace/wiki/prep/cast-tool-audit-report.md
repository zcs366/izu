# CAST 工具校准审计报告

**审计人**：Hermes Agent  
**日期**：2026-05-16  
**审计对象**：`/mnt/i/hermes/scripts/izu-pipeline.py`（v4.2）  
**类型**：工具绑定 → 代码实现一致性扫描（"工具校准"）

---

## 1. 审计范围说明

### 1.1 审计目标

验证 `izu-pipeline.py` 中每个 Agent 步骤（探/搜/织/对齐/写/劈/修/核）的实际代码行为是否严格匹配 `STEP_TOOLSETS`（第77-86行）及 `TOOLSET_DESCRIPTIONS`（第89-98行）的权限声明。

### 1.2 审计方法

- 逐函数追踪各 `run_*` 函数（`run_scout` → `run_verify`）的**实际调用链**
- 识别所有对以下函数的调用：`ddg_search`、`curl_fetch`、`call_deepseek`、`read_step`、`save_step`、`find_latest_step`、`code_*`、`validate_code_blocks`
- 对照 `STEP_TOOLSETS` 判断是否有**越权调用**（不该用的工具用了）、**描述-行为不一致**、或**逻辑缺陷**
- 检查 `_AGENT_DEFS`（第1168-1177行）是否与 `STEP_TOOLSETS` 一致

### 1.3 工具许可矩阵（参考基准）

| 步骤 | `STEP_TOOLSETS` | 应有权访问 |
|------|-----------------|-----------|
| 探   | search, web     | 搜索 + curl 抓取 |
| 搜   | search          | 仅搜索 |
| 织   | file            | 仅读写文件 |
| 对齐 | file            | 仅读文件 |
| 写   | file            | 仅写文件 |
| 劈   | file            | 仅读文件 |
| 修   | file, search    | 读写文件 + 搜索 |
| 核   | search, file    | 搜索 + 读文件 |

---

## 2. 当前工具绑定总览

### 2.1 步骤 vs 实际调用表

| 步骤 | 函数 | 允许的工具集 | 实际调用的函数 | 符合？ |
|------|------|------------|----------------|--------|
| 探 | `run_scout` | search, web | `ddg_search()` ✓, `curl_fetch()` ✓, `dedup_and_tier_results()` ✓, `code_dedup_aggregate()` ✓, `aggregate_dual()` → `call_deepseek()` ✓, `save_step()` → 写文件 ❌ | **越权：写文件** |
| 搜 | `run_search` | search | `read_step()` ✓, `ddg_search()` ✓, `dedup_and_tier_results()` ✓, `code_dedup_aggregate()` ✓, `aggregate_dual()` → `call_deepseek()` ✓, `save_step()` → 写文件 ❌ | **越权：写文件** |
| 织 | `run_weave` | file | `read_step()` ✓, `call_deepseek()` ✓ (提示词注入约束), `save_step()` ✓ | ✅ |
| 对齐 | `run_align` | file | `run_align_code()` → `check_alignment()` → 纯代码文件操作 ✓, `save_step()` → 写文件 ❌ | **越权：写文件** |
| 写 | `run_write` | file | `read_step()` ✓, `call_deepseek()` ✓, `save_step()` ✓ | ✅ |
| 劈 | `run_critique` | file | `read_step()` ✓, `code_fact_check_urls()` → `requests.head()` ❌, `call_deepseek()` ✓, `save_step()` ✓ | **越权：HTTP 请求** |
| 修 | `run_revise` | file, search | `read_step()` ✓, `call_deepseek()` ✓, `save_step()` ✓ | ✅ |
| 核 | `run_verify` | search, file | `read_step()` ✓, `ddg_search()` ✓, `code_extract_claims()` ✓, `code_verify_claim()` ✓, `code_fact_check_urls()` → `requests.head()` ✓, `call_deepseek()` ✓, `save_step()` → 写文件 ❌ | **越权：写文件** |

### 2.2 `_AGENT_DEFS` vs `STEP_TOOLSETS` 对齐检查

| 步骤 | `STEP_TOOLSETS` (L77-86) | `_AGENT_DEFS` (L1168-1177) | 一致？ |
|------|--------------------------|---------------------------|--------|
| 探 | `["search", "web"]` | `["search", "web"]` | ✅ |
| 搜 | `["search"]` | `["search"]` | ✅ |
| 织 | `["file"]` | `["file"]` | ✅ |
| 对齐 | `["file"]` | `["file"]` | ✅ |
| 写 | `["file"]` | `["file"]` | ✅ |
| 劈 | `["file"]` | `["file"]` | ✅ |
| 修 | `["file", "search"]` | `["file", "search"]` | ✅ |
| 核 | `["search", "file"]` | `["search", "file"]` | ✅ |

> **注意**：`_AGENT_DEFS` 与 `STEP_TOOLSETS` 完全一致（这是好的），但仅作为元数据存在，未被任何运行时检查机制引用——即没有任何代码在执行前验证某步骤的调用是否超出其 `_AGENT_DEFS` 权限。`_AGENT_DEFS` 是**声明式注释**，不是**运行时护栏**。

---

## 3. 缺陷清单

### 缺陷 #1（严重：高）「探」步骤越权写文件

- **位置**：`run_scout()` → `save_step()`，第770行
- **描述**：`STEP_TOOLSETS["scout"] = ["search", "web"]` 明确禁止探步骤操作文件。但 `run_scout()` 调用 `save_step()`（第770行），向 `/mnt/i/hermes/output/izu-pipeline/` 写入 `.md` 文件。这是**工具集声明与实践行为的根本矛盾**。
- **影响**：探的角色提示词（第397行）说"不能读写项目目录中的文件"，但代码实际写道。在 LLM 自主 agent 范式中，这可能导致 LLM 推断其权限不一致。
- **修复建议**：
  - 方案 A（推荐）：将 `save_step` 操作挪出 `run_scout`，交由调度器统一在步骤完成后持久化输出
  - 方案 B（轻量）：将 `STEP_TOOLSETS["scout"]` 改为 `["search", "web", "file"]` 使声明与行为一致
  - 方案 C（更差）：保留现状但不修复——声明与行为差距将继续累积技术债

### 缺陷 #2（严重：高）「核」步骤越权写文件

- **位置**：`run_verify()` → `save_step()`，第1104行
- **描述**：`STEP_TOOLSETS["verify"] = ["search", "file"]`，且描述（第97行）明确说"不能写入或修改项目文件"。但 `run_verify()` 在最后调用 `save_step()` 写入核报告文件。
- **影响**：与缺陷 #1 相同——声明与行为不一致。核步骤的 LLM 提示词（第528行）约束"不能写入"也是被代码自身违反的。
- **修复建议**：同缺陷 #1。建议将 `save_step` 职责统一到流水线调度逻辑中（`run_pipeline` 方法），而非各 `run_*` 函数自行写入。

### 缺陷 #3（严重：中）「劈」步骤越权发起 HTTP 请求

- **位置**：`run_critique()` → `code_fact_check_urls()` → `requests.head()`，第930行、第355行
- **描述**：`STEP_TOOLSETS["critique"] = ["file"]`，且提示词（第498行）说"只能读取写的产出文件。不能搜索网络"。但 `run_critique()` 在启动 LLM 批评前，先调用 `code_fact_check_urls()` 发出 HTTP `HEAD` 请求检查死链——这是**网络操作**，不在 `["file"]` 权限范围内。
- **影响**：虽然 `code_fact_check_urls` 是纯代码函数（不是 LLM 调用），但技术上属于"web"工具类操作，违反了"最小权限"原则。
- **修复建议**：
  - 将 `code_fact_check_urls` 调用上移：在`写`步骤结束后由流水线统一做死链检查，或在`修`步骤中做（其工具集包含 `search`）
  - 或将 `STEP_TOOLSETS["critique"]` 改为 `["file", "web"]` 如果认为死链预检是合法的
  - 推荐：**改为流水线级检查**，在 `run_pipeline` 中 `写→沙箱→死链` 三个步骤统一做

### 缺陷 #4（严重：中）「搜」步骤越权写文件 + 读文件

- **位置**：`run_search()` → `read_step()` 第780行 + `save_step()` 第813行
- **描述**：`STEP_TOOLSETS["search"] = ["search"]` 是最严格的——只有搜索。但 `run_search()` 既调用 `read_step()` 读取探的产出文件（第780行），又调用 `save_step()` 写文件（第813行）。即**越权读写文件**。
- **影响**：搜的提示词（第422行）说"不能发起新的抓取"是合理的，但说"只能进行网络搜索"与代码实际行为（读文件构造 prompt + 写文件持久化）矛盾。
- **修复建议**：同样建议将 `save_step` 统一到流水线层。`read_step` 是读取上游产物，属于合法的"传递依赖"，建议在 `STEP_TOOLSETS["search"]` 中增加 `file` 权限以匹配实际行为。

### 缺陷 #5（严重：中）「对齐」步骤越权写文件

- **位置**：`run_align()` → `run_align_code()` → `open(fpath, "w")`，第255行（izu_align_checker.py）
- **描述**：`STEP_TOOLSETS["align"] = ["file"]`，描述（第93行）说"只能读取项目目录中的文件，不能修改文件或搜索网络"。但 `run_align_code()` 确实在写入文件（第255行），即**越权写文件**。
- **影响**：与缺陷 #1/2/4 同根同源——`save_step` 语义被内嵌在各 `run_*` 函数中，导致几乎所有"不允许写文件"的步骤实际上都在写。
- **修复建议**：同缺陷 #1。

### 缺陷 #6（严重：低）「探」步骤的 `ddg_search` 调用两次——第706行 + 第728行

- **位置**：`run_scout()` → `_single_scout()`，第706行（主搜索）和第728行（"趋势参考"搜索）
- **描述**：在每个探子过程中，`ddg_search` 被调用两次——一次用于主搜索，一次用于"trends 2026"趋势参考。但趋势搜索的结果仅用于构造 LLM prompt 中的 `strategy_text`（第742行），且只取前3条。这导致**每个探子产生 2 次搜索 API 调用**，双探共 4 次搜索。这不是"越权"，而是**低效使用**，且未在工具声明中体现"探可能调多次搜索"的行为特征。
- **影响**：搜索配额翻倍。文档描述"探×2"暗示 2 次搜索，实际是 4 次。搜索工具的频次边界不透明。
- **修复建议**：合并搜索查询（`f"{variant_topic} {topic} 前沿 2026"`），将两次搜索合为一次，减轻 API 调用负担。

### 缺陷 #7（严重：低）「探」步骤 curl 抓取结果未在搜索报告中充分回传

- **位置**：`run_scout()` → `_single_scout()`，第718-723行
- **描述**：探步骤使用 `curl_fetch()` 抓取前3个搜索结果的全文字段（第722行），然后将完整文本传递给 LLM（第739行）。但**搜步骤的提示词**（第794行）说"所有✅来源必须来自探步骤中curl抓取的原文"——然而搜步骤的输入只有探的 LLM 输出（即 `scout` 文本），而非原始 curl 抓取结果。这意味着搜步骤的 LLM **只能从探的摘要中推断**抓取内容，而非直接访问原始抓取。
- **影响**：这导致搜步骤"必须引用原始抓取"的约束在实际中无法强制执行——搜只能引用探步骤的 LLM 输出中声称的内容。这是一个**信息链衰减**问题。
- **修复建议**：
  - 将原始抓取结果作为结构化数据追加到搜索 prompt 中（类似第725-726行的 `search_text` 做法），确保搜步骤也能直接访问 curl 原文
  - 或者：移除搜步骤"必须引用curl原文"的约束，承认"搜的输入是探的摘要"

### 缺陷 #8（严重：低）`_AGENT_DEFS` 未在运行时被引用为权限控制机制

- **位置**：第1168-1177行定义，整文件范围
- **描述**：`_AGENT_DEFS` 在 `run_pipeline` 中被定义，仅用于初始化 `AGENT_STATUS` 字典（第1178-1179行）的状态键。从未有任何代码检查 `AGENT_STATUS[step_name]` 的工具集是否与实际调用一致。即：**工具集声明是纯文档，不是运行时护栏**。
- **影响**：如果一个新 `run_*` 函数被添加或现有函数被修改但忘记更新 `STEP_TOOLSETS`，没有任何预警机制。
- **修复建议**：
  - 添加可选的单元测试：对每个 `run_*` 函数，静态分析其调用的函数名，与 `STEP_TOOLSETS` 预期权限对比
  - 或在 `run_pipeline` 中增加 `assert` 检查：步骤启动前检查其依赖文件是否存在等前置条件

---

## 4. 根因分析

上述8项缺陷中，**缺陷#1/2/4/5**（共4项高/中严重度）有同一个根因：

> **`save_step()` 被嵌入各 `run_*` 函数内部**，而非作为流水线调度器的统一职责。

`save_step` 是一个**写文件操作**。如果某个步骤的工具集不允许写文件（探/搜/对齐/核），则 `save_step` 的调用即构成越权。但如果不让 `run_*` 函数调用 `save_step`，就需要调度器（`run_pipeline` 的步骤循环）在每步完成后自动持久化函数返回值——这是设计模式的缺陷，而非个别疏漏。

### 修复建议（根因层级）

将流水线架构从：

```python
def run_scout(topic):
    # ... do work ...
    fpath = save_step(topic, "探", merged)  # 步骤内写文件
    return fpath, merged
```

改为：

```python
def run_scout(topic):
    # ... do work ...
    return merged  # 只返回内容，不写文件

# 调度器统一处理
for step in steps:
    content = step_funcs[step]()
    fpath = save_step(topic, step, content)  # 调度器写文件
```

这样所有步骤的 `STEP_TOOLSETS` 中的 `["file"]` 就只表示"步骤可以操作具体项目的文件"，而持久化步骤产出的**元操作**由调度器执行，不属于任何特定步骤的权限范围。

---

## 5. 修复优先级排序

| 优先级 | 缺陷 | 严重程度 | 预估工时 | 策略 |
|--------|------|---------|----------|------|
| P0 | #1 探越权写文件 | 高 | 2h | 架构重构：将 `save_step` 移至调度器 |
| P0 | #2 核越权写文件 | 高 | 2h | 同上（与 #1 同根因，一起修复） |
| P1 | #4 搜越权读写文件 | 中 | 1h | 同上，或调整 `STEP_TOOLSETS` |
| P1 | #5 对齐越权写文件 | 中 | 0.5h | 同上（简单，`run_align_code` 返回值已包含 report 字符串） |
| P2 | #3 劈越权 HTTP 请求 | 中 | 1h | 将 `code_fact_check_urls` 移至流水线调度器级别 |
| P3 | #6 探双重搜索低效 | 低 | 0.5h | 合并搜索查询字符串 |
| P3 | #7 探→搜信息链衰减 | 低 | 1h | 将 curl 原始抓取结果传递给搜的输入 |
| P3 | #8 无运行时护栏 | 低 | 1.5h | 添加权限检查单元测试或 `assert` |

### 预估总工时：**6.5 ~ 9.5 小时**

---

## 6. 综合结论

**主要问题**：`save_step` 的调用位置导致至少 4 个步骤（探、搜、对齐、核）存在声明与行为不一致。这不是逐个修补的问题，而是需要**架构层调整**——将文件持久化从步骤内部移动到调度器层。

**次要问题**：劈步骤的 HTTP 死链预检越权、探步骤低效的双重搜索、探→搜间的信息链衰减，以及 `_AGENT_DEFS` 的声明不被运行时引用。

**建议优先处理**：P0（架构重构）+ P2（死链预检迁移）+ P1（权限声明调整），这三项完成后工具校准缺陷即可从 8 项减少到 3 项低严重度项。

---

*报告生成于 2026-05-16 | 审计范围：izu-pipeline.py v4.2 (1301 行) + izu_align_checker.py v1.0 (287 行) + izu_sandbox.py v1.0 (354 行)*
