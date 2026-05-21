# izu-pipeline Session Checkpoint + `--resume` 实现记录

**日期**：2026-05-16 | **版本**：v4.5

## 背景

五人合议（子产/韩信/鲁班/萧何/子贡/军师）确定 P1 任务为 izu Session Checkpoint。当前 `izu-pipeline.py` 已有 `--from <步骤名>` 参数支持从指定步开始，但缺少：
1. 自动检测最后完成步的 `--resume` 能力
2. 每步完成后的 checkpoint 快照持久化

## 实现

### 新增代码

**位置**：`izu-pipeline.py`（1385行，+55行）

**新增组件：**
1. `MANIFEST_DIR` 配置 — `.checkpoints/` 目录，与流水线输出同层级
2. `save_manifest(topic, step, results_map)` — 每步完成后写入包含当前所有已生成步产物路径的 JSON 快照
3. `load_manifest(topic)` — 读取最新 manifest，返回 last_completed_step → 计算 next_idx
4. `run_pipeline()` 中 `start_from == "resume"` 分支 — 调用 `load_manifest()` 获取起始索引，预填充 `results` 字典
5. `--resume` CLI 参数 — 用法：`python3 izu-pipeline.py <主题> --resume`

### 关键设计决策

- **复用已有基础设施**：未引入新文件或依赖。`save_step()`/`find_latest_step()` 已存在，manifest 只记录它们产生的文件路径。
- **零日常成本**：`save_manifest()` 仅在流水线运行时被调用（写入 ~1KB JSON），不影响常规 API 调用次数或延迟。
- **slug 一致性**：manifest 文件名基于话题名生成，与 `save_step()` 使用相同的 slug 算法（前30字符，去除非字母数字符号，空格→下划线）。
- **轻量级**：不存储原始数据（各步产物已存为 `.md` 文件），manifest 只存储路径索引和最后完成步名称。

### 行数统计

| 组件 | 行数 |
|------|------|
| 配置 + `save_manifest()` | ~25行 |
| `load_manifest()` | ~15行 |
| pipeline resume 分支 | ~10行 |
| CLI 参数 + help 文本 | ~5行 |
| **总计** | **~55行** |

### 假引文检测器

**位置**：`scripts/izu_fake_cite_check.py`（30行）

纯启发式，零 LLM 调用。检查项：
1. URL 域名合理性（长度≥4字符）
2. arXiv ID 格式检查（10+字符含点号）
3. URL 存活检查（HEAD 请求，5秒超时）
4. HTTP 状态码（≥400 标记可疑）

## 用法

```bash
# 正常启动
python3 izu-pipeline.py "Agent自我演进新范式"

# 中断后恢复（自动检测最后完成的步）
python3 izu-pipeline.py "Agent自我演进新范式" --resume

# 假引文检测
python3 izu_fake_cite_check.py /path/to/izu/output.md
```

## 与现有系统关系

| 组件 | 关系 |
|------|------|
| `izu_checkpoint.py` (228行) | 独立存在，负责 CP2 信源充分度评分。与 session checkpoint 正交 |
| `izu_session_serde.py` | 底层序列化支持。`save_manifest()` 直接写 JSON 不依赖它 |
| `save_step()`/`find_latest_step()` | 基础 IO 函数，manifest 依赖它们完成文件路径记录 |
| `--from <步骤名>` | 保留，`--resume` 的降级方案。当无 manifest 时回退到 `--from` |
