# Nate Silver 基线统计方案设计

> **作者**: Nate Silver（数据统计与预测专家）
> **日期**: 2026-05-16
> **对象**: izu-pipeline (7步骤 Agent 管线：探→搜→织→对齐→写→劈→修→核)
> **预算约束**: DeepSeek ~¥2/百万 token；用户日均 1h 有效时间

---

## 1. 工具失败率控制图 (p-Chart for Tool Failure Rate)

### 1.1 "工具失败"操作定义

在 izu-pipeline 中，每次工具调用（DeepSeek API + 搜索 API）视为一个"试验"（trial）。以下情形记为一次 **工具失败**（binary: 1 = 失败, 0 = 成功）：

| 失败类型 | 判定规则 | 示例 |
|----------|----------|------|
| **API 超时** | 调用耗时 > 30s 或 HTTP 504/503 | DeepSeek chat completion 超时 |
| **返回为空** | 工具返回 content 为空字符串或 `null` | 搜索无结果返回 `[]` |
| **格式错误** | 返回 JSON 无法解析，或缺失必填字段 | 工具返回 `{"error": ...}` |
| **状态码异常** | HTTP 4xx/5xx 非超时 | 429 限流、401 鉴权 |
| **逻辑拒绝** | 模型返回"我无法完成此操作"等拒绝 | 拒绝检索特定主题 |

**排除项**: 用户主动中断、预算余量耗尽导致的自然终止不计入工具失败。

### 1.2 采样方案

- **采样单元**: 每次 izu-pipeline **单条**完整运行（一次 query → 7步管线完成）
- **采集周期**: 连续 **14 天**（满足中心极限定理对 p-chart 的要求）
- **目标样本量**: **n = 50 次运行/天** → 总计 **700 次运行**
- **样本量依据**:
  - 单次运行约 15–25 次工具调用（7步 × 平均 2-3 次调用/步）
  - 预期失败率 p₀ ≤ 5%（保守估计）
  - 控制图要求每个子组 n ≥ 1/(1-p₀) ≈ 20，n=50 提供充足统计效力
  - 日均 1h 用户时间可手动触发 ~10 次运行；剩余 40 次通过 cron 自动触发随机 query（从预置 query 池中抽取）

### 1.3 控制图类型与计算方法

使用 **p-Chart（不合格品率控制图）**，公式如下：

**中心线 (CL)**:
$$CL = \bar{p} = \frac{\sum_{i=1}^{k} x_i}{\sum_{i=1}^{k} n_i}$$

其中 $x_i$ 是第 i 天的失败次数，$n_i$ 是第 i 天的运行次数（固定 50）。

**控制上限/下限 (UCL/LCL)**:
$$UCL = \bar{p} + 3 \sqrt{\frac{\bar{p}(1-\bar{p})}{n_i}}$$
$$LCL = \max\left(0, \bar{p} - 3 \sqrt{\frac{\bar{p}(1-\bar{p})}{n_i}}\right)$$

**判异准则**（Western Electric Rules）:
1. **1点 > 3σ** → 失控（超出 UCL/LCL）
2. **连续 9 点位于中心线同侧** → 系统偏移
3. **连续 6 点递增/递减** → 趋势异常
4. **连续 14 点交替上下** → 分层异常

**当 p₀ 未知时**：使用前 14 天数据估计 $\bar{p}$，第 15 天起绘制正式控制图。若 $\bar{p} \times n < 5$ 或 $(1-\bar{p}) \times n < 5$，则需增大 n 或改用 Laney p'-chart（修正过离散）。

### 1.4 数据采集方案

```python
# 采集量估算: ~250 行 Python 代码

# 核心数据结构
class ToolCallRecord:
    run_id: str          # UUID, 一次 pipeline 运行
    step: str            # "探"|"搜"|"织"|"对齐"|"写"|"劈"|"修"|"核"
    tool_name: str       # "deepseek_chat"|"web_search"|...
    start_time: float    # unix timestamp
    end_time: float
    status: str          # "success"|"timeout"|"empty_response"|"format_error"|"http_error"|"refusal"
    error_msg: str | None
    tokens_used: int
    cost_yuan: float
```

**存储**: SQLite 表 `tool_call_log`，每行一次工具调用。

**额外 API 开销**: **每天 0 次额外 API 调用**（仅记录已有调用的结果，不增加新请求）。日志记录本身的 I/O 消耗可忽略不计（<1ms/条）。

### 1.5 输出物

| 产出 | 格式 | 时间节点 |
|------|------|----------|
| 工具调用日志表 | SQLite | 持续采集（D+1 起可用） |
| p-Chart (14天基线) | Matplotlib PNG + 数据表 CSV | 基线期满日 **D+14** |
| 控制界限报告 | Markdown | 基线期满日 **D+14** |

---

## 2. 安全事件泊松分布模型 (Poisson CUSUM for Safety Events)

### 2.1 "安全事件"操作定义

安全事件指管线产出中具有**可验证危害**的特定事件类型。每条流水线运行独立计数。

| 事件类型 | 定义 | 检测方法 |
|----------|------|----------|
| **假引文 (Hallucinated Citation)** | 引用不存在的文献/URL/数据，或张冠李戴 | 后续 GraphRAG 检测 + 人工复核 |
| **越权工具调用** | Agent 调用未授权的工具或访问未授权的数据源 | 工具调用日志审计 |
| **指令泄露** | 系统提示词/工具描述被注入到最终输出 | 输出正则扫描（关键词: "system prompt", "你是一个..."等） |
| **有害内容** | 输出包含政治敏感、歧视性、暴力等不安全内容 | 关键词过滤 + 人工复核 |
| **信息泄露** | 输出中包含 API key、路径、用户名等敏感信息 | 正则匹配（`sk-*`, `api_key` 等） |

**基线重点关注**: **假引文**（与 GraphRAG 课题直接相关）+ **越权工具调用**（安全底线）。

### 2.2 观测窗口与采样

- **观测窗口**: 按**天**为单位（T = 1 天），保证泊松分布假设的独立性
- **基线期**: **连续 30 天**（泊松分布参数 λ 的 95% 置信区间宽度满足 ±30% 精度要求）
- **每日运行数**: 50 次/天（同工具失败率采集）
- **总样本**: 50 × 30 = **1,500 次 pipeline 运行**
- **阳性事件基线期望**: 假设假引文率 ~2–5% → 每日期望事件数 λ₀ ≈ 1–2.5/天
- **λ 精度验证**: 对于 λ₀ = 2/天，n=30 天得到的 95% CI 为 [1.24, 2.97]（使用 χ² 分布的精确置信区间），相对宽度 ±43%，可接受

### 2.3 λ 估计方法

使用 **极大似然估计 (MLE)**：

$$\hat{\lambda} = \frac{1}{T} \sum_{t=1}^{T} X_t$$

其中 $X_t$ 是第 t 天的安全事件发生次数，T = 30。

**95% 置信区间**（精确法，基于 χ² 分布）：

$$\left[ \frac{1}{2T} \chi^2_{0.025, 2S}, \quad \frac{1}{2T} \chi^2_{0.975, 2(S+1)} \right]$$

其中 $S = \sum_{t=1}^{T} X_t$ 是总事件数。

**若 S = 0**（基线期未观察到任何事件）：
使用 "Rule of Three"：95% CI 上界为 $3/T$ = 3/30 = **0.1 次/天**。即事件率 ≤ 0.1/天（95% 置信）。

### 2.4 异常检测阈值

使用 **Poisson CUSUM（累积和）控制图** 进行在线监控：

**CUSUM 统计量**：
$$C_t^+ = \max(0, C_{t-1}^+ + X_t - k)$$
$$C_t^- = \min(0, C_{t-1}^- + X_t - k)$$

其中：
- $k = \frac{\lambda_1 - \lambda_0}{\ln(\lambda_1) - \ln(\lambda_0)}$（参考值），$\lambda_0$ = 基线均值，$\lambda_1$ = 待检测的偏移目标
- **检测目标**: 偏移至 2×λ₀（即翻倍）
- **阈值 h**: 选择 h = **3**（对应 ARL₀ ≈ 400 天，即平均每 400 天一次误报）
- **判断准则**: 当 $C_t^+ > h$ 或 $|C_t^-| > h$ 时触发告警

**简化版替代方案（适用于运维能力有限的团队）**：
使用 **Shewhart c-chart**（单位缺陷数控制图）：

$$CL = \bar{c} = \hat{\lambda}$$
$$UCL = \bar{c} + 3\sqrt{\bar{c}}$$
$$LCL = \max(0, \bar{c} - 3\sqrt{\bar{c}})$$

当 $\bar{c} = 2$ 时，UCL = 2 + 3×√2 = **6.24**，即单日事件 > 6 次触发告警。

### 2.5 数据采集方案

```python
# 采集量估算: ~180 行 Python 代码

# 在 pipeline 每步输出后插入检测钩子
class SafetyEvent:
    run_id: str
    event_type: str          # "hallucinated_citation"|"unauthorized_tool"|"prompt_leak"|"harmful_content"|"info_leak"
    severity: int            # 1-5, 1=可疑, 5=确定
    source_step: str         # 哪个步骤产生的
    evidence: str            # 证据文本摘要
    detected_by: str         # "graphrag_detector"|"regex_scan"|"manual_review"
    timestamp: float
```

**存储**: SQLite 表 `safety_events`。

**额外 API 开销**:
- 假引文检测: 不额外增加（复用后续 GraphRAG 检测功能）
- 正则扫描: 0 额外开销
- 越权工具调用审计: 0 额外开销（依赖工具调用日志）
- **合计**: 每天 **0 次额外 API 调用**

### 2.6 输出物

| 产出 | 格式 | 时间节点 |
|------|------|----------|
| 安全事件日志表 | SQLite | 持续采集 |
| λ 估计报告（含 95% CI） | Markdown | **D+30** |
| Poisson CUSUM 或 c-chart | Matplotlib PNG | **D+30** |
| 异常检测阈值设定文档 | Markdown | **D+30 后固化** |

---

## 3. 假引文分层抽样方案 (Stratified Sampling for Hallucination Audit)

### 3.1 分层维度

izu wiki 知识库的假引文检测需要进行**人工复核**的黄金标准（ground truth）标注。由于全量复核成本过高，采用分层抽样降低样本量。

**三层交叉分层策略**:

#### 层 1: 领域 (Domain)
根据 izu wiki 的目录结构划分。假设约 8–12 个主要领域：

| 领域 | 预期文件数 | 假引文风险估计 |
|------|-----------|--------------|
| 技术文档 / API | 高 | 低（结构化，易验证） |
| 产品说明 | 中 | 中 |
| 内部流程/SOP | 中 | 高（缺乏外部对照） |
| 会议纪要 | 低 | 高 |
| 组织架构/人员 | 低 | 低 |
| 历史记录 | 低 | 中 |
| 外部引用文献 | 中 | 高（假引文重灾区） |

#### 层 2: 信源等级 (Source Authority)
按文档中引用的外部信源可靠性分级：

| 信源等级 | 定义 | 预期占比 |
|----------|------|---------|
| A 级 | 官方文档、权威学术期刊、政府网站 | 30% |
| B 级 | 知名媒体、行业报告、维基百科 | 40% |
| C 级 | 个人博客、论坛、非官方渠道 | 20% |
| D 级 | 无外部引用（内部文档） | 10% |

#### 层 3: 实体类型 (Entity Type)
按被引用的实体类型分层：

| 实体类型 | 示例 | 假引文风险 |
|----------|------|-----------|
| 文献/论文 | "据 Smith et al. (2023)..." | **高** |
| 统计数据 | "数据显示 87% 的用户..." | **高** |
| 历史事件 | "2022年3月该公司..." | 中 |
| 技术术语/概念 | "Transformer 架构..." | 低 |
| 代码/API | "调用 get_user() 返回..." | 低 |
| 人名/职位 | "CEO 王某某表示..." | 中 |

### 3.2 样本量计算

使用 **Neyman 分配** 的最小样本量公式：

$$n_0 = \frac{\left(\sum_{h=1}^{H} W_h \sigma_h\right)^2}{\left(\frac{E}{z_{\alpha/2}}\right)^2 + \frac{1}{N} \sum_{h=1}^{H} W_h \sigma_h^2}$$

其中：
- $H$ = 层数（此处 = 3 个维度交叉，若每维 4 × 4 × 6 = 96 层，但实际很多为空；有效层约 20–30）
- $W_h = N_h / N$ = 第 h 层权重
- $\sigma_h = \sqrt{p_h(1-p_h)}$ = 第 h 层假引文率的标准差
- $p_h$ = 第 h 层假引文率（基线未知时使用 **pilot 估计**）
- $E$ = 边际误差（Margin of Error）
- $z_{\alpha/2}$ = 标准正态分布临界值
- $N$ = 总体大小（izu wiki 总文档数，假设 ~500 篇）

**参数设定**:
- **置信水平**: **95%** → $z_{0.025} = 1.96$
- **边际误差**: **E = 8%**（±8 个百分点，对假引文率调查已足够精确）
- **预期总体假引文率**: $p \approx 5\%$（保守估计）
- **设计效应 (Design Effect, DEFF)**: 分层抽样相对于简单随机抽样的效率。由于层间假引文率差异大，DEFF ≈ 0.6–1.2。取 DEFF = **1.0**（保守）

**计算过程 (不考虑分层简化版)**:
$$n_0 = \frac{1.96^2 \times 0.05 \times 0.95}{0.08^2} = \frac{3.8416 \times 0.0475}{0.0064} \approx 28.5$$

**考虑分层调整后**:
- 使用 Neyman 分配的样本量通常为 SRS 的 80–90%
- $n \approx 28.5 \times 1.0 \times 1.1$（有限总体校正系数，N=500）
- 有限总体校正: $n = \frac{n_0}{1 + \frac{n_0 - 1}{N}} = \frac{28.5}{1 + 27.5/500} \approx 27.0$

**最终建议**: **n = 50 篇文档**（向上取整，预留 10% 因质量问题废弃）。

### 3.3 层内分配方案

使用 **Neyman 最优分配**：

$$n_h = n \times \frac{W_h \sigma_h}{\sum_{h} W_h \sigma_h}$$

**实际操作简化**（无需每层精确估计 σₕ）：
使用 **比例分配 + 高风险层超采样**：
- 标准层（技术文档、产品说明等，σ ≈ 0.1）：按比例分配
- 高风险层（外部引用文献、会议纪要，σ ≈ 0.3）：**2× 超采样**
- 极低风险层（代码/API，σ ≈ 0.02）：**0.5× 欠采样**

**层分配例表**（假设 500 篇文档，n=50）：

| 层组合 | Nₕ | Wₕ | σₕ | 分配权重 | nₕ |
|--------|-----|-----|-----|---------|-----|
| 技术-高信源-低实体 | 150 | 0.30 | 0.10 | 0.30×0.10 = 0.03 | 15 |
| 外部引用-A/B级-文献/数据 | 80 | 0.16 | 0.30 | 0.16×0.30 = 0.048 | 24 |
| 内部SOP-低信源-概念 | 60 | 0.12 | 0.15 | 0.12×0.15 = 0.018 | 9 |
| 其他层 | 210 | 0.42 | 0.10 | 0.042 | 24(按比例分摊) |

**人工复核工作量**: n=50 篇，每篇平均审核 ~15 分钟 = **12.5 小时**。在日均 1h 条件下，约 **2 周**完成。

### 3.4 置信区间计算

对于分层抽样，总体假引文率的 **点估计**：

$$\hat{p}_{strat} = \sum_{h=1}^{H} W_h \hat{p}_h$$

其中 $\hat{p}_h = x_h / n_h$ 是第 h 层的样本假引文率。

**95% 置信区间**：

$$\hat{p}_{strat} \pm z_{0.025} \times SE(\hat{p}_{strat})$$

$$SE(\hat{p}_{strat}) = \sqrt{\sum_{h=1}^{H} W_h^2 \frac{\hat{p}_h(1-\hat{p}_h)}{n_h - 1} \times (1 - f_h)}$$

其中 $f_h = n_h / N_h$ 是第 h 层的**抽样比**，$(1 - f_h)$ 为**有限总体校正因子**。

**当某些层 $\hat{p}_h = 0$ 时**：使用 **Wilson 分数区间** 代替 Wald 区间，避免零方差问题：

$$\hat{p}_h = \frac{x_h + \frac{z^2}{2}}{n_h + z^2}, \quad SE = \frac{\sqrt{\hat{p}_h(1 - \hat{p}_h) + \frac{z^2}{4n_h}}}{\sqrt{n_h}}$$

（Agresti-Coull 修正）

### 3.5 试点 (Pilot) 阶段

在正式分层抽样前进行 **Pilot 研究**：

| 项目 | 参数 |
|------|------|
| Pilot 样本量 | n_pilot = **10 篇**（每篇人工复核） |
| 目的 | 估计各层 σₕ，验证分层方案合理性 |
| 产出 | 各层的 $\hat{p}_h$ 和 $\hat{\sigma}_h$ |
| 时长 | 约 2–3 天（日均 1h） |
| 采样方法 | 简单随机抽样（不分层） |

Pilot 完成后，根据实际 $\hat{\sigma}_h$ 调整 Neyman 分配比例，再进行正式 n=50 的抽样。

### 3.6 数据采集方案

```python
# 采集量估算: ~200 行 Python 代码

# 知识库元数据提取
class WikiDocument:
    path: str                # 文件路径
    domain: str              # 领域标签（从目录推断）
    source_level: str        # A/B/C/D 信源等级
    entity_types: list[str]  # 包含的实体类型
    file_size: int           # 用于加权
    citation_count: int      # 引用数（proxy for risk）
    last_modified: datetime

# 分层抽样引擎
class StratifiedSampler:
    def compute_allocation(self, strata: dict, n: int) -> dict[str, int]:
        # 实现 Neyman 分配
        pass
    
    def draw_sample(self, allocation: dict) -> list[WikiDocument]:
        # 在各层内使用 random seed 固定抽样
        pass

# 复核结果记录
class AuditRecord:
    doc_id: str
    reviewer: str
    has_false_citation: bool
    false_citation_count: int
    severity: int           # 1-5
    notes: str
    review_duration_minutes: float
```

**存储**: SQLite 表 `audit_records`。

**额外 API 开销**: **0 次**（人工审核，不产生 API 调用）。

### 3.7 输出物

| 产出 | 格式 | 时间节点 |
|------|------|----------|
| Wiki 文档元数据清单 | CSV | **D+1**（一次性脚本） |
| Pilot 抽样结果报告 | Markdown | **D+3** |
| 正式分层抽样方案（含分配表） | Markdown | **D+4**（pilot 后调整） |
| 50 篇复核全部完成 | 审核记录表 | **D+18**（pilot 3d + 正式 15d） |
| 假引文率点估计 ± 95% CI | Markdown + PDF | **D+18** |
| 分层效率分析（DEFF 报告） | Markdown | **D+19** |

---

## 4. 三基线联合实施方案

### 4.1 时间线

```
D+0   ─── 开始基线数据采集
  │
D+1   ─── Wiki 元数据提取脚本完成 → 工具调用日志开始记录
  │
D+3   ─── Pilot 人工复核完成（10篇）→ 调整分层方案
  │
D+4   ─── 正式分层抽样方案锁定
  │
D+14  ─── 工具失败率 p-Chart 基线期满 → 控制图初稿
  │
D+18  ─── 全部 50 篇假引文复核完成 → 假引文率 ±95% CI 报告
  │
D+30  ─── 安全事件泊松模型基线期满 → λ 估计 + CUSUM 阈值
  │
D+31  ─── 三基线综合报告发布（Nate Silver Final Report）
```

### 4.2 代码总量估算

| 模块 | 代码量 (Python) | 用途 |
|------|-----------------|------|
| 工具调用日志中间件 | ~120 行 | pipeline 钩子，记录每次工具调用 |
| 控制图生成 | ~80 行 | p-Chart 计算 + Matplotlib 绘图 |
| 安全事件检测钩子 | ~100 行 | 5 类安全事件的正则/规则检测 |
| Poisson 模型 | ~60 行 | λ MLE + CI + CUSUM 统计量 |
| Wiki 元数据提取 | ~80 行 | 目录解析 + 信源等级标注 |
| 分层抽样引擎 | ~100 行 | Neyman 分配 + 随机抽样 |
| 辅助工具 (CLI) | ~50 行 | 报告生成、数据导出 |
| **合计** | **~590 行** | |

### 4.3 额外 API 开销汇总

| 模块 | 每日额外 API 调用 | 每日额外 token 消耗 | 每日额外成本 |
|------|-------------------|--------------------|-------------|
| 工具调用日志 | 0 | 0 | ¥0 |
| 安全事件检测 | 0 | 0 | ¥0 |
| 假引文抽样 (人工) | 0 | 0 | ¥0 |
| **合计** | **0** | **0** | **¥0** |

**零额外 API 成本**——所有数据均来自已有流水线的日志记录和人工审核。

### 4.4 统计软件依赖

| 工具 | 用途 | 已在环境中？ |
|------|------|-------------|
| Python `scipy.stats` | χ² 分位数、正态分布、泊松分布 | 通常已安装 |
| Python `statsmodels` | CUSUM 实现（`statsmodels.tsa.stattools`） | 可能需安装 |
| Python `matplotlib` | 控制图可视化 | 通常已安装 |
| Python `numpy` | 数值计算 | 通常已安装 |
| Python `sqlite3` | 数据持久化（内置） | ✅ 内置 |

---

## 5. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| p₀ 远高于 5%（如 >20%） | 低 | 控制界限过宽 → 失去检测能力 | 延长基线期至 28 天，或增大 n 至 100 |
| 基线期 S=0（零安全事件） | 中 | 无法估计 λ | 使用 Rule of Three 设定上限，延长期至 60 天 |
| 人工复核质量不一致 | 中 | 假引文标签噪声 | 每篇 double review，Cohen's κ ≥ 0.7 |
| Wiki 文档数远少于 500 | 低 | 分层过细 → 层内样本不足 | 合并稀疏层，或改用 post-stratification |
| 预算约束限制 cron 运行 | 中 | 无法达到 50 次/天 | 降低至 20 次/天，延长基线期至 35 天 |

---

## 6. 参考文献与方法论依据

1. Montgomery, D. C. (2019). *Introduction to Statistical Quality Control* (8th ed.). Wiley. — p-Chart 与 CUSUM 标准参考
2. Lucas, J. M. (1985). "Counted Data CUSUM's." *Technometrics*, 27(2), 129–144. — Poisson CUSUM 理论
3. Cochran, W. G. (1977). *Sampling Techniques* (3rd ed.). Wiley. — Neyman 分配与分层抽样
4. Agresti, A., & Coull, B. A. (1998). "Approximate Is Better than 'Exact' for Interval Estimation of Binomial Proportions." *The American Statistician*, 52(2), 119–126. — Wilson/Agresti-Coull 区间
5. Hanley, J. A., & Lippman-Hand, A. (1983). "If Nothing Goes Wrong, Is Everything All Right?" *JAMA*, 249(13), 1743–1745. — Rule of Three

---

> **签名**: Nate Silver  
> *"The numbers have no way of speaking for themselves. We speak for them."*
