# SDAR 门控 OPSD 插入方案

> **项目**: P0-2 · 核战队（子产+匠石）  
> **目标**: 在 izu 训练管线中插入 SDAR 门控 OPSD（On-Policy Self-Distillation）辅助目标  
> **基准效果**: ALFWorld +9.4%, Search-QA +7.0%, WebShop +10.2% (Qwen2.5/Qwen3)  
> **约束**: 匠石原则（能用代码不用模型）+ 刘伯温原则（可验证/可测量/可失败/可回滚）

---

## 1. izu 管线现状深入调研

### 1.1 整体架构

izu 是一个八步骤深度研究流水线，v4.2 版（1693行 Python）。

```
探×2 → 搜×2 → [CP2] → 织 → 对齐 → 写 → 劈×3 → 修 → 引文验证 → 核
```

| 步骤 | 角色 | 调用方式 | 产出 | LLM调用 |
|------|------|----------|------|---------|
| 探(scout) | 双探并行勘探 | 2×LLM + 2×DDG搜索 | 知识地图草稿 | 2次 |
| 搜(search) | 双搜并行深度钻 | 2×LLM + DDG补充搜索 | 结构化搜索报告 | 2次 |
| CP2 | 硬检查点 | 代码评分+LLM降级 | 信源充分度评分 | 条件1次 |
| 织(weave) | 编织关联网络 | 1×LLM（无搜索） | 关联地图 | 1次 |
| 对齐(align) | 代码对齐检查 | 纯代码（代码合规检查器） | 对齐报告 | 0次(已替换) |
| 写(write) | 厚重写作 | 1×LLM | 初稿 | 1次 |
| 劈(critique) | 三视角批评 | 3×LLM | 批评报告 | 3次 |
| 修(revise) | 修改定稿 | 1×LLM | 定本 | 1次 |
| 引文验证 | 代码URL可达性 | 纯代码 | 引文报告 | 0次 |
| 核(verify) | 断言核验 | 代码提取+搜索+LLM模糊兜底 | 核验报告 | 条件1次 |

**核心特征**:
- 每步都是独立 LLM 调用，通过 `call_api()` 函数向 MiniMax M2.7（主）或 DeepSeek（备）发送请求
- token 消耗巨大：完整 8 步流水线 = 9~13 次 LLM 调用 × 每调用 ~7000-8000 max_tokens
- 当前**无梯度训练组件**——全都是推理调用，纯 prompt engineering 驱动
- 存在「画像闭环」：读/写用户画像 → 注入上下文 → 更新画像

### 1.2 关键代码定位

**核心文件**: `/mnt/i/hermes/scripts/izu-pipeline.py` (1693行)

**API 调用入口** (第653-691行):
```python
def call_api(prompt, role, temperature=0.7, model=None):
    """调用LLM API，主用MiniMax，失败时降级到DeepSeek"""
    # 双provider + 3次重试
    # 返回: data["choices"][0]["message"]["content"]
```

**步骤函数签名**:
```python
run_scout(topic) → (fpath, merged)
run_search(topic, scout_path, profile_context) → (fpath, merged)
run_weave(topic, scout_path, search_path) → (fpath, result)
run_align(topic, weave_path) → (fpath, report)  # 已代码化
run_write(topic, weave_path, align_path, output_format, profile_context, write_prefs) → (fpath, result)
run_critique(topic, write_path) → (fpath, combined)
run_revise(topic, write_path, critique_path) → (fpath, result)
run_verify(topic, revise_path, scout_path) → (fpath, verify_report)
```

**助手模块**:
- `izu_checkpoint.py` (228行): CP2检查点引擎，纯代码评分
- `izu_align_checker.py` (293行): 对齐检查器，纯代码替代LLM
- `izu_sandbox.py` (354行): 代码沙箱验证
- `izu_citation_check.py` (422行): 引文验证
- `izu_shared/temporal_decay.py` (744行): 时序衰减断言存储（SQLite + 半衰期衰减）
- `izu_shared/decision_graph.py` (442行): 决策图引擎
- `izu_shared/tier.py` (~80行): 信源分级表

**流水线主循环** (第1539-1624行):
```python
for i in range(start_idx, len(all_steps)):
    step = all_steps[i]
    results[step] = step_funcs[step]()
    # 出口评分卡 / CP2 / 沙箱检查 等后处理
```

### 1.3 当前管线的「训练特性」评估

| 特性 | 现状 | SDAR插入可行性 |
|------|------|---------------|
| 可微性 | ❌ 纯LLM推理，没有梯度 | 需插入 `log_probs` 收集点 |
| 奖励信号 | ❌ 无显式奖励 | 出口评分卡(90分阈值)可作为粗糙奖励 |
| 数据流 | ✅ 线性DAG，步骤间文件传递 | 门控信号可在每步出口注入 |
| 可重放 | ✅ manifest checkpoint支持恢复 | OPSD需要正负样本对 |
| 模型访问 | ✅ call_api() 统一入口 | 需扩展以返回 logprobs |
| 批处理 | ❌ 单topic串行 | 不支持，SDAR可单样本工作 |

---

## 2. SDAR 门控 OPSD 核心机制

### 2.1 SDAR-OPSD 原理简述

SDAR (Self-Distillation with Adaptive Reward) 的核心思想：

1. **教师模型**生成 token 序列 T = {t₁, t₂, ..., tₙ}
2. **学生模型**（自己）在同一 prompt 下生成 token 序列 S = {s₁, s₂, ..., sₙ}
3. **门控对比**：对每个 token position i，比较 tᵢ 与 sᵢ 的 logits 分布
4. **正门控**：若教师置信度高（entropy 低）且学生与教师一致 → 强化该 token 梯度
5. **负衰减**：若学生产生「好教师不会生成的序列」（如幻觉、低质量尾巴）→ 软衰减负梯度
6. **OPSD 损失函数**：

```
L_OPSD = -Σᵢ [ wᵢ * log P_θ(sᵢ | context) ]
其中 wᵢ = gate_function(teacher_logprobs, student_logprobs, reward)
```

### 2.2 izu 场景中的门控信号源

izu 管线天然产生多种可充当门控的信号：

| 信号源 | 位置 | 类型 | 质量 | 获取成本 |
|--------|------|------|------|---------|
| 出口评分卡 | 每步完成 | 数值 (0-100) | 中（LLM自评有噪声） | 已有，1次额外LLM调用 |
| CP2检查点 | 搜→织之间 | 数值 (0-10) | 中高（代码+LLM混合） | 已有 |
| 对齐检查 | 织→写之间 | pass/warn/fail | 高（纯代码） | 已有，0成本 |
| 沙箱验证 | 写→修之间 | pass/fail/timed_out | 高（真实执行） | 已有 |
| 引文验证 | 修→核之间 | 死链数+断言验证分 | 高（代码+搜索） | 已有 |
| 核步骤断言分 | 最终步 | 数值 (0-100) | 高（代码+LLM混合） | 已有 |

**核心洞察**: izu 管线已经内置了丰富的门控信号，SDAR 不需要额外引入奖励模型——可以直接复用这些现成的质检信号。

---

## 3. SDAR 门控 OPSD 插入方案

### 3.1 整体架构

```
┌──────────────────────────────────────────────────┐
│                  SDAR Manager                     │
│  (单例，管理OPSD状态机 + 梯度缓冲区)               │
├──────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌──────────────────┐  │
│  │Teacher  │  │Student  │  │Gate Signal Fuser │  │
│  │Snapshot │  │Buffer   │  │(融合多源信号)    │  │
│  └────┬────┘  └────┬────┘  └────────┬─────────┘  │
│       │            │                │             │
│  ┌────▼────────────▼────────────────▼──────────┐ │
│  │          OPSD Loss Computer                  │ │
│  │  (对比teacher/student logits, 计算w_i)       │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│            izu-pipeline 修改点                      │
│                                                    │
│  1. call_api() → 扩展返回 logprobs                 │
│  2. 每步完成后 → 收集 (teacher_logprobs, reward)   │
│  3. 出口处 → 融合门控信号 → 更新OPSD权重          │
│  4. 回滚时 → 记录负样本对（低分+低logprobs）       │
└──────────────────────────────────────────────────┘
```

### 3.2 四个插入点

#### 插入点 A: `call_api()` 扩展（代码修改）

**位置**: `/mnt/i/hermes/scripts/izu-pipeline.py` 第653-691行

**修改内容**:
1. 在 API 请求中添加 `logprobs=True, top_logprobs=5` 参数
2. 解析响应中的 `logprobs` 字段
3. 返回扩展格式 `(content, logprobs_dict)`

**代码修改**:

```python
def call_api(prompt, role, temperature=0.7, model=None, return_logprobs=False):
    """调用LLM API，返回(content, logprobs_dict)"""
    system = ROLE_PROMPTS.get(role, ROLE_PROMPTS["搜"])
    if model is None:
        model = API_MODEL_FAST if role in ("探", "搜", "核") else API_MODEL
    
    providers = [...]  # 不变
    
    for provider_name, url, key, mdl in providers:
        for attempt in range(3):
            try:
                payload = {
                    "model": mdl, 
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ], 
                    "temperature": temperature, 
                    "max_tokens": MAX_TOKENS,
                }
                if return_logprobs:
                    payload["logprobs"] = True
                    payload["top_logprobs"] = 5
                
                resp = requests.post(url, ...)
                data = resp.json()
                if "choices" in data:
                    choice = data["choices"][0]
                    content = choice["message"]["content"]
                    logprobs = choice.get("logprobs", {}) if return_logprobs else None
                    return (content, logprobs)
                ...
    return ("ERROR: ...", None)
```

**兼容性**: 所有现有调用保持 `return_logprobs=False` 默认值，零侵入。

**推理验证**: 需检查所选 provider（MiniMax M2.7, DeepSeek）是否支持 `logprobs` 参数。若不支持 → 降级方案：使用 token-level 困惑度估算替代（见3.5节）。

#### 插入点 B: OPSD 状态管理器（新文件）

**位置**: 新建 `/mnt/i/hermes/scripts/izu_sdar.py`

```python
"""SDAR 门控 OPSD 管理器 v0.1

核心数据结构：
- teacher_snapshot: Dict[str, Dict] — 教师token logprobs缓存
  键 = f"{step}_{topic_hash}"，值 = {tokens, logprobs, avg_logprob}
- student_buffer: 同结构（当前运行产生）
- gate_signals: List[Dict] — 多源门控信号融合队列
- opsd_weights: Dict[int, float] — token级OPSD权重 w_i

信号融合公式：
  gate_score = α * exit_score + β * quality_passes + γ * cite_score
  其中 α=0.4, β=0.4, γ=0.2 (可配置)
"""

class OPSDManager:
    def __init__(self, half_life_days=30):
        self.teacher_snapshots = {}    # 教师快照缓存(序列化到temporal_decay)
        self.student_buffer = {}       # 当前运行学生logprobs
        self.gate_signals = []         # 门控信号历史
        self.weights_cache = {}        # OPSD权重缓存
        self.mode = "collect"          # collect | compute | freeze
        
    def record_teacher(self, step, prompt_hash, logprobs_data):
        """记录教师logprobs"""
        key = f"{prompt_hash}"
        avg_lp = np.mean([t.get("logprob", 0) for t in logprobs_data.get("tokens", [])])
        self.teacher_snapshots[key] = {
            "step": step,
            "tokens": logprobs_data.get("tokens", []),
            "avg_logprob": avg_lp,
            "timestamp": datetime.now().isoformat(),
        }
        # 持久化到 temporal_decay（可回滚）
        from izu_shared.temporal_decay import store_assertion
        store_assertion("sdar", f"teacher:{key}", self.teacher_snapshots[key], weight=1.0)
    
    def record_student(self, step, prompt_hash, logprobs_data):
        """记录学生logprobs"""
        key = f"{prompt_hash}"
        self.student_buffer[key] = {
            "step": step,
            "tokens": logprobs_data.get("tokens", []),
            "timestamp": datetime.now().isoformat(),
        }
    
    def fuse_signals(self, exit_score, quality_checks, cite_score):
        """融合多源门控信号 → gate_score [-1, 1]"""
        signal = {
            "exit_score": exit_score / 100.0,   # 归一化
            "quality_passed": quality_checks.get("passed", 0) / max(quality_checks.get("total", 1), 1),
            "cite_score": cite_score / 100.0,
        }
        gate = (0.4 * signal["exit_score"] + 
                0.4 * signal["quality_passed"] + 
                0.2 * signal["cite_score"])
        # 映射到[-1, 1]：≥0.7为正门控，<0.3为负衰减
        return 2.0 * gate - 1.0, signal
    
    def compute_opsd_weights(self, prompt_hash):
        """计算OPSD权重 w_i"""
        teacher = self.teacher_snapshots.get(prompt_hash)
        student = self.student_buffer.get(prompt_hash)
        if not teacher or not student:
            return None
        
        weights = []
        for t_token, s_token in zip(teacher["tokens"], student["tokens"]):
            t_lp = t_token.get("logprob", -10)
            s_lp = s_token.get("logprob", -10)
            
            # 教师置信度高 → 门控强
            teacher_confidence = np.exp(t_lp)  # [0,1]
            
            # 师生一致度
            agreement = np.exp(s_lp)  # 学生在该token上的置信度
            
            # 门控权重: 教师置信度高 + 学生与教师一致 → 强正权重
            w = teacher_confidence * (2 * agreement - 1)
            weights.append(w)
        
        return weights
    
    def get_gradient_scale(self):
        """返回当前OPSD梯度缩放系数"""
        # 基于最近N步的平均gate_score动态调整
        recent = self.gate_signals[-10:] if len(self.gate_signals) >= 10 else self.gate_signals
        if not recent:
            return 1.0
        avg_gate = np.mean([s["gate"] for s in recent])
        return max(0.1, min(2.0, 1.0 + avg_gate))
    
    def rollback_snapshot(self, prompt_hash):
        """回滚：从temporal_decay恢复最近快照"""
        from izu_shared.temporal_decay import get_assertion
        return get_assertion("sdar", f"teacher:{prompt_hash}")
    
    def clear_buffer(self):
        """清理学生缓冲区（每次完整pipeline结束后）"""
        self.student_buffer.clear()
        # 保留 gate_signals 前100条用于趋势分析
        if len(self.gate_signals) > 100:
            self.gate_signals = self.gate_signals[-100:]
```

#### 插入点 C: 每步出口 SDAR 门控注入

**位置**: `/mnt/i/hermes/scripts/izu-pipeline.py` 第1539-1624行（主循环）

**修改内容**: 在每个步骤出口评分卡逻辑之后，增加 SDAR 信号收集：

```python
# ── SDAR 门控注入 ────────────────────────────────
if SDAR_ENABLED and content_exit and len(content_exit) > 50:
    # 1. 从 call_api 获取 logprobs（需在 step_func 中传递）
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    
    # 2. 收集多源门控信号
    exit_signal = exit_score.get("score", 50)
    quality_checks = {"passed": 0, "total": 0}  # 来自对齐/沙箱
    cite_signal = 50.0  # 来自引文验证
    
    if step == "搜":
        cp_result = run_checkpoint_cp2(topic, search_path)
        quality_checks = {
            "passed": cp_result[1].get("t1_count", 0) + cp_result[1].get("t2_count", 0),
            "total": max(cp_result[1].get("count", 1), 1),
        }
    elif step == "写":
        sb_result = run_sandbox_check(topic, write_path, "写")
        if sb_result[0]:
            quality_checks = {"passed": 1, "total": 1}
    elif step == "引文验证":
        cite_result = run_citation_check_pipeline(topic, revise_path)
        cite_signal = compute_cite_score(cite_result[1])
    
    # 3. 融合门控信号
    gate, signal_detail = sdar_manager.fuse_signals(exit_signal, quality_checks, cite_signal)
    sdar_manager.gate_signals.append({"step": step, "gate": gate, "detail": signal_detail})
    
    # 4. 计算OPSD权重（如果有师生对）
    # 首轮运行时mode=collect只收集教师数据
    # 后续相同topic恢复运行时mode=compute，师生对比
    weights = sdar_manager.compute_opsd_weights(prompt_hash)
    if weights:
        grad_scale = sdar_manager.get_gradient_scale()
        print(f"  🎯 SDAR: gate={gate:.2f}, grad_scale={grad_scale:.2f}, weights_len={len(weights)}")
# ── ─────────────────────────────────────────────
```

#### 插入点 D: 回滚时的 OPSD 负样本采集

**位置**: `/mnt/i/hermes/scripts/izu-pipeline.py` 回滚逻辑处（第1572-1623行）

**修改内容**: 当出口评分卡触发回溯或CP2触发重搜时，记录负样本对：

```python
# 在重搜/回溯逻辑中插入负样本采集
if SDAR_ENABLED:
    sdar_manager.record_negative_sample({
        "step": step,
        "topic": topic,
        "exit_score": exit_score.get("score", 0),
        "logprobs_avg": student_logprobs_avg,
        "reason": exit_score.get("action", "回溯"),
        "retry_count": retry_count,
    })
```

---

### 3.3 运行时模式

SDAR 有三种运行时模式，通过环境变量 `SDAR_MODE` 控制：

| 模式 | 值 | 行为 | 推理开销 |
|------|-----|------|---------|
| 收集 | `collect` | 教师快照采集 + 门控信号日志 | 额外 ~50ms/步（logprobs解析） |
| 训练 | `train` | 师生对比 + OPSD权重计算 + 梯度记录 | 额外 ~100ms/步 |
| 冻结 | `freeze` | 零开销（SDAR Manager no-op） | 0 |

**过渡策略**：
1. 首轮：`SDAR_MODE=collect` — 只收集教师快照，建立基线
2. 次轮（同topic）：`SDAR_MODE=train` — 师生对比，更新权重
3. 生产部署：`SDAR_MODE=freeze` — 不产生任何开销

### 3.4 持久化与回滚

| 组件 | 存储方式 | 回滚方式 |
|------|---------|---------|
| 教师快照 | temporal_decay (SQLite WAL) | `sdar_manager.rollback_snapshot(key)` |
| 门控信号日志 | JSONL (`~/.hermes/sdar_gate_log.jsonl`) | 按时间戳截断 |
| OPSD权重缓存 | 内存 Dict + 定期序列化 | 从last_checkpoint重建 |
| 负样本库 | JSONL (`~/.hermes/sdar_negative_samples.jsonl`) | 同回滚点截断 |

### 3.5 关键风险与降级方案

| 风险 | 概率 | 影响 | 降级方案 |
|------|------|------|---------|
| MiniMax API 不支持 logprobs | 高 | 无法获取token级分布 | ① 使用token级困惑度近似估算（通过output token长度/重复度）② 回退到sequence-level平均logprob（需LLM返回conf_score） |
| DeepSeek API 不支持 logprobs | 中 | 降级后同样缺失 | 同上，但影响更小（DeepSeek是备用provider） |
| logprobs 增加API延迟 | 中 | 每步+200~500ms | ① 仅在首轮收集模式下开启 ② 异步记录logprobs，不阻塞主流程 |
| 门控信号噪声大 | 低-中 | 权重计算不稳定 | ① 信号平滑（EMA）② 自适应阈值（动态调整正负门控边界） |
| temporal_decay 写入失败 | 低 | 快照丢失 | ① 同步写内存+定期batch写盘 ② 退化为纯内存模式 |

---

## 4. 具体代码修改建议

### 4.1 文件修改清单

| 文件 | 修改类型 | 预估行数 | 风险 |
|------|---------|---------|------|
| `izu-pipeline.py:call_api()` | 扩展返回格式 + logprobs参数 | ~20行 | 中（需验证API兼容性） |
| `izu-pipeline.py:run_pipeline()` | 主循环注入SDAR门控 | ~60行 | 低（条件开关，默认关闭） |
| `izu-pipeline.py:回滚逻辑` | 负样本采集 | ~15行 | 低 |
| **新文件** `izu_sdar.py` | OPSD管理器完整实现 | ~250行 | 低（独立模块，不侵入主干） |
| `izu_shared/temporal_decay.py` | （可选）扩展存储接口 | ~10行 | 低 |
| **新文件** `tests/test_sdar.py` | 单元测试 | ~100行 | - |

**总计**: 估算 ~455 行新增/修改代码

### 4.2 关键代码片段（已就绪）

见上文 3.2 节各插入点的具体代码实现。所有代码遵循匠石原则：
- 纯 Python，零外部依赖（除 numpy 外）
- 通过环境变量控制开关，零侵入主干管线
- 所有持久化走 temporal_decay，天然支持回滚

### 4.3 测试策略

| 测试层级 | 测试内容 | 验证指标 |
|---------|---------|---------|
| 单元测试 | OPSDManager 数据流 | 教师/学生logprobs正确匹配 |
| 单元测试 | gate_signals 融合公式 | 输入 → 预期输出 |
| 单元测试 | temporal_decay 读写 | 持久化+恢复一致性 |
| 集成测试 | call_api(logprobs=True) | API 返回格式解析 |
| 集成测试 | 完整管线+SDAR_MODE=collect | 每步logprobs成功记录 |
| 回滚测试 | checkpoint恢复后重建OPSD状态 | 状态一致 |
| 压力测试 | 连续20轮管线运行 | 内存不泄漏，temporal_decay不膨胀 |

### 4.4 可用性验证协议（刘伯温约束）

```
[可验证]  每次运行产生 sdar_gate_log.jsonl，可用数据分析脚本审计
[可测量]  每一步收集 gate_score, avg_logprob, exit_score 三维数据
[可失败]  SDAR_ENABLED=0 | SDAR_MODE=freeze 立刻回到原始行为
[可回滚]  temporal_decay 存储所有快照，通过 checkpoint key 回滚
```

---

## 5. 估算工时

| 阶段 | 任务 | 预估工时 | 依赖 |
|------|------|---------|------|
| **Phase 0**: 调研 | 验证API logprobs兼容性 | 2h | MiniMax/DeepSeek API |
| **Phase 0**: 调研 | 现有管线+信号源映射梳理 | 1h | - |
| **Phase 1**: 实现 | 新建 izu_sdar.py (OPSDManager) | 4h | Phase 0 |
| **Phase 1**: 实现 | 修改 call_api() 扩展 | 1h | Phase 0 |
| **Phase 1**: 实现 | 修改 run_pipeline() 门控注入 | 2h | izu_sdar.py |
| **Phase 1**: 实现 | 回滚负样本采集 | 1h | - |
| **Phase 2**: 测试 | 单元测试 + 集成测试 | 4h | Phase 1 |
| **Phase 2**: 测试 | 端到端验证（1轮collect+1轮train） | 2h | Phase 2 |
| **Phase 3**: 部署 | 环境变量配置 + 文档更新 | 1h | Phase 2 |

**总工时**: ~18 小时（约2.5人天）

**保守估算（含Buffer + 文档 + 意外）**: 24 小时（3人天）

---

## 6. 当前管线结构速查表（供参考）

### 6.1 步骤执行图

```
topic + env
    │
    ▼
  run_scout(topic)
    │  ├─ _single_scout("前沿研究 最新进展", "A")  →  call_api + ddg_search
    │  └─ _single_scout("争议 批评 反思 局限", "B") →  call_api + ddg_search
    │  └─ aggregate_dual(result_a, result_b)      →  call_api
    ▼
  run_search(topic, scout_path, profile_context)
    │  ├─ _single_search("深度分析 研究 案例", "A") →  call_api
    │  └─ _single_search("对比 评估 基准 实验", "B") →  call_api
    │  └─ aggregate_dual(result_a, result_b)      →  call_api
    ▼
  [CP2]  run_checkpoint_cp2(topic, search_path)
    │  ├─ code_score() → 数量/等级/覆盖
    │  └─ LLM降级（条件调用）
    ▼
  run_weave(topic, scout_path, search_path)     →  call_api
    ▼
  run_align(topic, weave_path)                  →  pure_code
    ▼
  run_write(topic, weave_path, align_path, ...) →  call_api
    ▼
  [沙箱] run_sandbox_check(topic, write_path)
    ▼
  run_critique(topic, write_path)
    │  ├─ 劈-逻辑与技术  →  call_api
    │  ├─ 劈-事实与来源  →  call_api
    │  └─ 劈-表达与风格  →  call_api
    ▼
  run_revise(topic, write_path, critique_path)  →  call_api
    ▼
  run_citation_check_pipeline(topic, revise_path) →  pure_code
    ▼
  run_verify(topic, revise_path, scout_path)
    │  ├─ code_extract_claims()          →  pure_code
    │  ├─ code_verify_claim() × N        →  pure_code
    │  └─ LLM模糊兜底（条件调用）          →  call_api
    ▼
  ✅ 导出 + 更新画像
```

### 6.2 门控信号强度矩阵

| 步骤 | 信号类型 | 数据形式 | 频率 | 可靠性 | SDAR可用性 |
|------|---------|---------|------|--------|-----------|
| 探 | 搜索覆盖率 | T1/T2计数 + 重叠率 | 每次 | 高（纯代码） | ✅ 可直接用作奖励 |
| 搜 | CP2充分度 | 0-10分 | 每次 | 高 | ✅ 高信噪比 |
| 织 | 无（LLM唯一） | - | 每次 | - | ❌ 需依赖出口评分卡 |
| 对齐 | 关键词覆盖 | pass/warn/fail | 每次 | 高（纯代码） | ✅ 可用作质量过滤 |
| 写 | 沙箱验证 | pass/fail/timed_out | 有代码块时 | 极高 | ✅ 硬真理信号 |
| 劈 | 3视角无_aggr | - | 每次 | - | ❌ 仅出口评分卡 |
| 修 | 沙箱验证 | pass/fail/timed_out | 有代码块时 | 极高 | ✅ 硬真理信号 |
| 引文验证 | URL死链率 | 0-100% | 每次 | 高（纯代码） | ✅ 强引用质量信号 |
| 核 | 断言验证分 | 0-100分 | 每次 | 高（代码+搜索） | ✅ 最强最终信号 |

---

## 7. 附录：SDAR 全局配置建议

```python
# 在 izu-pipeline.py 顶部添加
# ── SDAR 门控 OPSD 配置 ─────────────────────────
SDAR_ENABLED = os.environ.get("SDAR_ENABLED", "0") == "1"
SDAR_MODE = os.environ.get("SDAR_MODE", "collect")  # collect | train | freeze
SDAR_GATE_ALPHA = float(os.environ.get("SDAR_GATE_ALPHA", "0.4"))  # exit_score权重
SDAR_GATE_BETA = float(os.environ.get("SDAR_GATE_BETA", "0.4"))    # quality_checks权重
SDAR_GATE_GAMMA = float(os.environ.get("SDAR_GATE_GAMMA", "0.2"))  # cite_score权重
SDAR_HALF_LIFE_DAYS = int(os.environ.get("SDAR_HALF_LIFE_DAYS", "30"))
```

对应 `izu-env.sh` 扩展行:
```bash
# SDAR 门控 OPSD
export SDAR_ENABLED="${SDAR_ENABLED:-0}"
export SDAR_MODE="${SDAR_MODE:-collect}"
```

---

## 8. 下一步行动（Phase 0 前置确认）

1. **API兼容性验证**（最关键）:
   ```bash
   # 测试 MiniMax 是否支持 logprobs
   curl -X POST https://api.minimax.chat/v1/chat/completions \
     -H "Authorization: Bearer $IZU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"say hi"}],
          "max_tokens":10,"logprobs":true,"top_logprobs":5}'
   ```

2. **信号基线收集**: 启用 `SDAR_MODE=collect` 运行 3~5 个不同topic的完整流水线，统计各步的 gate_score 分布

3. **阈值校准**: 根据基线数据调整 gate 正负阈值（默认 正≥0.3, 负<0.0）

4. **所有结果可审计**: `~/.hermes/sdar_gate_log.jsonl` 和 `~/.hermes/sdar_negative_samples.jsonl` 的格式设计

---

> **文档版本**: v1.0 · 2026-05-21  
> **作者**: 子产+匠石（核战队） — 军师 实施
> **状态**: ✅ 已实施

---

## 9. 实施记录（2026-05-21）

### Phase 0 验证结果

| 检查项 | 结果 | 详情 |
|--------|------|------|
| MiniMax M2.7 logprobs | ❌ 不支持 | API响应中无`logprobs`字段 |
| DeepSeek logprobs | ✅ 完美支持 | token-level logprob + top_logprobs |
| 降级决策 | ✅ | SDAR用DeepSeek收集logprobs，主流程保持MiniMax |

### Phase 1 实现清单

| 文件 | 修改 | 行数 |
|------|------|------|
| `scripts/izu_sdar.py` | **新建** — OPSDManager + parse_logprobs + 日志 | ~350行 |
| `scripts/izu-pipeline.py:call_api()` | 扩展`return_logprobs`参数 | ~25行 |
| `scripts/izu-pipeline.py:run_pipeline()` | SDAR配置初始化 | ~8行 |
| `scripts/izu-pipeline.py:run_pipeline()` | 门控信号注入（出口评分后） | ~20行 |
| `scripts/izu-pipeline.py:run_pipeline()` | 负样本采集（回溯当前步） | ~10行 |
| `scripts/izu-pipeline.py:run_pipeline()` | 负样本采集（回溯上游） | ~10行 |
| `scripts/izu-env.sh` | SDAR环境变量配置 | 3行 |

### 产出文件

| 文件 | 用途 | 格式 |
|------|------|------|
| `~/.hermes/sdar_gate_log.jsonl` | 门控信号日志 | JSONL, 每步一条 |
| `~/.hermes/sdar_negative_samples.jsonl` | 负样本库 | JSONL, 每次回溯一条 |

### 验证结果

- ✅ SDAR gate信号在管线中正确输出（`🎯 SDAR gate=0.xxxx`）
- ✅ 门控信号写入 JSONL 日志
- ✅ 回溯时负样本写入 JSONL 日志
- ✅ `SDAR_ENABLED=0` 时零侵入（`SDAR_ENABLED` 默认关闭）
- ✅ 向后兼容：现有`call_api()`调用无需修改

## 待做：基线收集

按计划第585-589条，需用`SDAR_MODE=collect`跑3~5个不同topic的完整流水线，采集gate_score分布，校准正负阈值。**尚未执行**。
