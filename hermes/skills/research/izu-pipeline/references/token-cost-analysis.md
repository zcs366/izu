# Token消耗分析方法论

> 适用于：审计 izu-pipeline 每次运行的 LLM 调用、token 消耗和成本
> 方法：代码分析（izu-pipeline.py）+ 劳动日志（izu_agent_log.jsonl）+ 模型定价公式

## 数据源

| 数据源 | 路径 | 内容 |
|--------|------|------|
| **劳动日志** | `~/.hermes/izu_agent_log.jsonl` | 每步耗时、输出字符数、回滚次数（v4.1+） |
| **画像文件** | `~/.hermes/izu_profile.json` | 会话持续时长、累计运行次数 |
| **流水线源码** | `/mnt/i/hermes/scripts/izu-pipeline.py` | LLM调用次数、input prompt大小、模型分配 |
| **检查点日志** | `~/.hermes/izu_checkpoint_log.json` | CP2评分、回滚历史 |

## 分析步骤

### 1. 提取每步 LLM 调用次数

从 `izu-pipeline.py` 的每个 `run_*` 函数中计数：

| 步骤 | 函数 | LLM调用 | 说明 |
|------|------|---------|------|
| 探 | `run_scout()` | 3 | `_single_scout()` ×2 = 2 + `aggregate_dual()` ×1 |
| 搜 | `run_search()` | 3 | `_single_search()` ×2 + `aggregate_dual()` ×1 |
| CP2 | `run_checkpoint_cp2()` | 1 | 仅当代码判定模糊时（`needs_llm=True`），否则0 |
| 织 | `run_weave()` | 1 | `call_deepseek(prompt, "织")` |
| 对齐 | `run_align()` | 1 | `call_deepseek(prompt, "对齐")` |
| 写 | `run_write()` | 1 | `call_deepseek(prompt, "写")` |
| 劈 | `run_critique()` | 3 | 三视角各一次 + 聚合（聚合是代码拼接，无LLM） |
| 修 | `run_revise()` | 1 | `call_deepseek(prompt, "修")` |
| 核 | `run_verify()` | 2 | `extract_key_claims()` (断言提取) ×1 + 模糊验证 ×N（通常0-2） |

**典型总数：16次 LLM 调用**（9次 flash + 7次 chat）

### 2. 估算每步输入 token

每个 LLM 调用的输入 = System Prompt + User Prompt。System Prompt 来自 `ROLE_PROMPTS`（约400-600字符）。User Prompt 包含之前的搜索结果/产物片段。

从代码中提取每个 `call_deepseek()` 调用时传入的 prompt 总字符数：

```python
# 探A: prompt = f"...{search_text[:3000]}...{fetched_text[:4000]}...{strategy_text}..."
#          ≈ 8000 chars
# 搜A: prompt = f"...{scout[:3000]}...{extra_text}..."
#          ≈ 5000 chars  
# 织:  prompt = f"...{scout[:2000]}...{search[:5000]}..."
#          ≈ 8000 chars
# 等等
```

**经验值（中文字符 → token，使用 ~1.3 chars/token）：**

| 步骤 | 输入字符数 | 输入 token |
|------|-----------|-----------|
| 探 | ~8000 | ~6150 |
| 搜 | ~5000 | ~3850 |
| CP2 | ~3000 | ~2300 |
| 织 | ~8000 | ~6150 |
| 对齐 | ~4500 | ~3460 |
| 写 | ~6000 | ~4620 |
| 劈 | ~9000 | ~6920 |
| 修 | ~11000 | ~8460 |
| 核 | ~6000 | ~4620 |

### 3. 从劳动日志提取输出 token

```
{"timestamp": "...", "step": "探", "duration_sec": 132, "output_chars": 4270, ...}
```

每步平均输出 = `sum(output_chars) / count`。除以调用次数得到每次调用的输出，再除以 1.3 得到 token 数。

### 4. 模型定价

使用 DeepSeek 公开定价（截至2026年5月）：

| 模型 | 输入 $/1M tokens | 输出 $/1M tokens | 流水线使用步骤 |
|------|----------------|-----------------|--------------|
| deepseek-v4-flash | 0.15 | 0.60 | 探、搜、CP2、核 |
| deepseek-chat | 1.00 | 2.00 | 织、对齐、写、劈、修 |

### 5. 完整流水线成本估算

```python
def estimate_run_cost(logs):
    CHARS_PER_TOKEN = 1.3
    PRICING = {"flash": (0.15, 0.60), "chat": (1.00, 2.00)}
    MODEL_MAP = {"探":"flash","搜":"flash","CP2":"flash","核":"flash",
                 "织":"chat","对齐":"chat","写":"chat","劈":"chat","修":"chat"}
    CALLS = {"探":3,"搜":3,"CP2":1,"织":1,"对齐":1,"写":1,"劈":3,"修":1,"核":2}
    INPUT_CHARS = {"探":8000,"搜":5000,"CP2":3000,"织":8000,"对齐":4500,
                   "写":6000,"劈":9000,"修":11000,"核":6000}
    
    total = 0
    for step, calls in CALLS.items():
        step_logs = [l for l in logs if l["step"] == step]
        avg_out = sum(l["output_chars"] for l in step_logs) / len(step_logs) if step_logs else 0
        in_tok = INPUT_CHARS[step] / CHARS_PER_TOKEN
        out_tok = avg_out / calls / CHARS_PER_TOKEN
        p = PRICING[MODEL_MAP[step]]
        cost = (in_tok * p[0] + out_tok * p[1]) * calls / 1_000_000
        total += cost
    return total
```

## 关键发现（截至2026-05-14）

1. **每次运行成本 ~$0.13**，极低成本验证了 izu 的"低成本"定位
2. **flash 模型占 56% 的调用量**，但只贡献了 ~10% 的成本
3. **劈步骤是最大开销**（约 $0.063，占 49%），因其使用 chat 模型且输出量大
4. **CP2 回滚每次增加 ~$0.0029**（重跑搜步骤）
5. **4 次运行累计成本 ~$0.51**（约 ¥3.73）

## 典型运行性能

| 指标 | 值 |
|------|-----|
| 总 LLM 调用 | 16 次 |
| 输入 token | ~85,000 |
| 输出 token | ~45,000 |
| 总耗时 | 400-900 秒 |
| 基础成本 | ~$0.128 |
| 含约2次CP2回滚 | ~$0.134 |
