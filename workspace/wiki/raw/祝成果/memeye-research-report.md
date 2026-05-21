# MemEye 评测框架调研报告

> **调研目标**: P1-1 — 调研 MemEye 评测框架 (arXiv:2605.15128)，确定 iZu 可复用的评测子集  
> **调研日期**: 2026-05-17  
> **版本**: v1.0

---

## 1. MemEye 框架摘要（300字）

MemEye（arXiv:2605.15128，2026-05-14）是由 Rutgers、Notre Dame、Princeton 等高校联合提出的**视觉中心的 Agent 长期记忆评测框架**。其核心创新是**双轴分类法**：

- **X 轴（视觉证据粒度）**：决定性问题所需的视觉证据精度，从 scene-level → region-level → instance-level → pixel-level 四级递进
- **Y 轴（检索使用复杂度）**：从单一证据检索（Y1）→ 多证据整合（Y2）→ 演化综合/状态变化追踪（Y3），逐级提升推理难度

基于该框架，MemEye 构建了 **8 个生活场景任务**，包含 **371 道平行 MCQ + 开放问答**，每道题标注了 (X,Y) 坐标和 clue 轮次。框架还设计了 **4 个消融验证门控**（Answerability、Shortcut Resistance、Visual Necessity、Reasoning Structure），确保问题必须依赖视觉记忆而非捷径。

评估了 **13 种记忆方法**在 **4 种 VLM 主干**上的表现，主要发现：
1. 基于 caption 的方法在 scene/region 级别有竞争力，但在 instance/pixel 级存在残留差距
2. 语义检索在 76%+ 的 Y3 案例中混淆了相关性与时效权威性，倾向返回过时证据
3. 视觉记忆本身不解决演化综合问题——证据保留与时态状态选择是分离的

**代码 & 数据**: github.com/MinghoKwok/MemEye | huggingface.co/datasets/MemEyeBench/MemEye

---

## 2. 8 个任务概览及其与 iZu 记忆需求的相关性

| # | 任务名称 | 场景描述 | 对话轮次 | 图片数 | 问题数 (MCQ) | 核心记忆能力 | 与 iZu 相关性 |
|---|---------|---------|---------|-------|-------------|-------------|-------------|
| 1 | **Brand_Memory_Test** (品牌记忆) | 用户查看多家汉堡/饮料品牌的菜品与价格，询问哪些是特定标识中的品牌标志 | 多轮多会话 | ~25 (5品牌×5图) | ~15 | 实例级视觉细节记忆、品牌标志识别 | **高** — iZu 需要跨会话记住用户喜好、商品偏好 |
| 2 | **Card_Playlog_Test** (卡牌对战记录) | 用户在卡牌游戏中历经多局比赛，询问历史出牌记录、胜负判定 | 多轮多会话 | ~20 | ~15 | 时序推理、状态变化追踪 | **高** — iZu 需要记录用户操作历史、做状态推断 |
| 3 | **Cartoon_Entertainment_Companion** (卡通娱乐伙伴) | 用户分享多张卡通/动漫图片，讨论剧情，后续询问角色细节 | 长对话多会话 | ~30 | ~25 | 细粒度像素级视觉记忆、角色属性回忆 | **中** — 偏娱乐场景，但像素级记忆需求可借鉴 |
| 4 | **Home_Renovation_Interior_Design** (家装室内设计) | 用户浏览多套室内设计方案（多张图片），讨论材质/颜色方案，后续询问修改 | 多轮多会话 | ~20 | ~20 | 跨图片参照、视觉属性变更追踪 | **中高** — iZu 需要记录用户偏好变更、对比选项 |
| 5 | **Multi-Scene_Visual_Case_Archive_Assistant** (多场景视觉案例归档) | 用户分享来自不同地点/时间的事故/案例照片，Agent 归档后需回忆关键视觉细节 | 多会话 | ~25 | ~20 | 跨场景检索、精细视觉特征记忆 | **高** — 类似 iZu 的 cross-session 信息归档与检索 |
| 6 | **Outdoor_Navigation_Route_Memory_Assistant** (户外导航路线记忆) | 用户分享路标/地标照片，Agent 需要记忆路线信息和导航决策 | 多轮多会话 | ~20 | ~15 | 空间记忆、时序路线追踪 | **中高** — 空间位置记忆需求可类比 |
| 7 | **Personal_Health_Dashboard_Assistant** (个人健康仪表盘) | 用户分享健康数据图表/饮食照片，Agent 需要跟踪健康指标变化 | 多轮多会话 | ~20 | ~15 | 图表理解、数值变化追踪、趋势分析 | **高** — iZu 需要跟踪用户数据变化、做数据驱动的记忆 |
| 8 | **Social_Chat_Memory_Test** (社交聊天记忆) | 用户分享社交活动照片，Agent 需记住人物关系、对话上下文 | 多会话 | ~20 | ~15 | 人物身份识别、社交上下文记忆 | **中** — 与 iZu 的用户画像记忆相关 |

**总计**: 8 个任务，371 道 MCQ + 371 道 Open-Ended 平行题。每道题标注了 (X,Y) 坐标、关联 session_id 和 clue 轮次。

### 与 iZu 高度相关的子集 (Top 4)

| 优先级 | 任务 | 理由 |
|--------|------|------|
| ★★★★★ | **Brand_Memory_Test** | 核心考验实例级视觉记忆 + 跨会话品牌/偏好检索，直接对应 iZu 的用户偏好记忆 |
| ★★★★★ | **Multi-Scene_Visual_Case_Archive_Assistant** | 多场景跨会话的视觉信息归档与检索，直接对应 iZu 的核心记忆场景 |
| ★★★★☆ | **Personal_Health_Dashboard_Assistant** | 数据变化追踪 + 跨会话趋势理解，对应 iZu 的用户行为数据记忆 |
| ★★★★☆ | **Card_Playlog_Test** | 状态变更 + 时序推理，对应 iZu 的操作历史与状态推断 |

---

## 3. 直接复用可行性评估

### 3.1 数据格式分析

MemEye 的 JSON 数据结构如下（来自 HF 数据集 schema）：

```json
{
  "character_profile": { "...": "..." },
  "multi_session_dialogues": [
    {
      "session_id": "D1",
      "date": "2026-03-01",
      "dialogues": [
        {
          "round": "D1:1",
          "user": "...",
          "assistant": "...",
          "input_image": ["../image/.../...png"]
        }
      ]
    }
  ],
  "human-annotated QAs": [
    {
      "question": "...",
      "answer": "...",
      "point": [["X2"], ["Y1"]],
      "session_id": ["D1"],
      "clue": ["D1:1"]
    }
  ]
}
```

**iZu 对数据格式的适配需求**：
- iZu 的记忆接口需要适配 MemEye 的 `multi_session_dialogues` 格式 —— **需要格式转换层**
- iZu 的评测脚本需要支持 MemEye 的 `point` (X,Y 坐标) 标记 —— **需要扩展评测逻辑**
- MemEye 使用 LLM-as-a-Judge 和 Exact Match 两种评分方式 —— **可直接复用评测脚本**

### 3.2 代码仓库结构评估

MemEye 的仓库结构：

```
MemEye/
├── benchmark/           # 13种记忆方法的评测实现
│   ├── a-mem/          # A-MEM 方法
│   ├── evermemos/      # EverMemos 方法
│   ├── gen_agents/     # Generative Agents 方法
│   ├── m2a/            # M2A 方法
│   ├── memgpt/         # MemGPT 方法
│   └── memoryos/       # MemoryOS 方法
├── config/
│   ├── tasks/          # 任务配置文件 (YAML)
│   ├── methods/        # 方法配置文件
│   └── models/         # 模型配置文件
├── router/             # 评测路由脚本
├── tools/              # 工具函数
└── docs/               # 文档
```

**iZu 复用时需要修改的部分**：

| 组件 | 直接复用? | 改动量 | 说明 |
|------|----------|--------|------|
| **评测数据 (HuggingFace)** | ✅ 可直接下载 | 0 | HF 数据集 `MemEyeBench/MemEye` 公开可下载 |
| **问题标注 (Q&A)** | ✅ 可直接使用 | 0 | 371 道 MCQ + 371 道 Open-Ended |
| **双轴分类 (X,Y 坐标)** | ⚠️ 部分复用 | 小 | X/Y 坐标标注体系可直接保留，但 iZu 可附加自己的记忆能力维度 |
| **4 个验证门控** | ✅ 可直接复用 | 0 | Answerability / Shortcut Resistance / Visual Necessity / Reasoning Structure |
| **评测代码 (router/)** | ⚠️ 部分复用 | 中 | 需要适配 iZu 的记忆接口协议 |
| **记忆方法实现 (benchmark/)** | ❌ 不可直接复用 | 大 | iZu 有自己的记忆系统架构，需独立实现适配器 |
| **LLM-as-a-Judge prompt** | ✅ 可直接复用 | 小 | Judge prompt 可直接沿用或微调 |
| **Exact Match 评测** | ✅ 可直接复用 | 小 | MCQ 的 Exact Match 逻辑通用 |

### 3.3 直接复用改动量总结

| 级别 | 改动量 | 说明 |
|------|--------|------|
| **数据层** | **低**（~1 人日） | 下载 HF 数据集，编写 iZu 数据加载器适配 `multi_session_dialogues` |
| **评测层** | **中**（~2 人日） | 复用 router 逻辑 + 适配 iZu 的记忆系统调用接口 |
| **评分层** | **低**（~0.5 人日） | LLM-as-a-Judge prompt 直接复用，Exact Match 逻辑通用 |
| **方法层** | **不适用** | iZu 不直接复用 13 种记忆方法，而是用 iZu 自己的记忆系统替代 |

**总估计**: ~3–4 人日（如果只复用一个高度相关的子集，约 2 人日）

---

## 4. 建议：立即复用 / 部分复用 / 只借鉴思路

### 最终建议：**部分复用（Partial Reuse）**

#### 具体方案

| 复用级别 | 内容 | 优先级 |
|---------|------|--------|
| **立即复用** | （1）Top-4 任务的 65 道 MCQ + Open-Ended 平行题作为 iZu 评测子集 | P0 |
|  | （2）4 个验证门控评估机制 | P0 |
|  | （3）LLM-as-a-Judge scoring prompt | P0 |
| **部分复用** | （4）双轴分类法 (X,Y 坐标)→ 映射到 iZu 的记忆能力维度体系 | P1 |
|  | （5）数据格式（`multi_session_dialogues` schema）→ 转为 iZu 内部格式 | P1 |
|  | （6）router 评测流水线架构 → 复用设计模式 | P2 |
| **只借鉴思路** | （7）整个 8 个任务数据（371 题）作为扩展评测集 | P2 |
|  | （8）13 种记忆方法的对比基线 → 参考设计 iZu 的消融实验 | P3 |

#### 推荐的评测子集（iZu 优先复用）

| 子集名称 | 包含任务 | 题数 | 对应 iZu 能力 |
|----------|---------|------|-------------|
| **izu-memeye-core** | Brand_Memory_Test + Multi-Scene_Visual_Case_Archive + Personal_Health_Dashboard + Card_Playlog | 65 MCQ + 65 OE = **130 题** | 用户偏好记忆、跨会话检索、数据变化追踪、状态推理 |
| **izu-memeye-all** | 全部 8 个任务 | 371 MCQ + 371 OE = **742 题** | 完整记忆能力评估 |

#### 推荐路线

```
第 1 步（立即开始）：从 HuggingFace 下载 Top-4 子集数据 + 编写 iZu 数据适配器
第 2 步（1-2 天）：集成 LLM-as-a-Judge + Exact Match 评测脚本
第 3 步（3-4 天）：适配 router 评测流水线，对接 iZu 记忆系统接口
第 4 步（5-6 天）：运行完整评测 + 结果分析
```

---

## 附录 A：与其他评测框架的对比

| 维度 | MemEye | MemLens (xrenaf/MEMLENS) | LoCoMo | Mem-Gallery |
|------|--------|--------------------------|--------|-------------|
| 视觉中心性 | ✅ 强（双轴分类） | ✅ 强 | ❌ 弱 | ❌ 弱 |
| 问题数 | 371 MCQ + 371 OE | 789 (子集 195) | 300+ | 187 |
| 状态变化追踪 | ✅ Y3 级别 | ✅ Knowledge Update | ❌ | ❌ |
| 验证门控 | ✅ 4 个门控 | ❌ | ❌ | ❌ |
| 粒度标签 | ✅ X1~X4, Y1~Y3 | ❌ | ❌ | ❌ |
| 发布状态 | 2026-05-14（刚刚发布） | 2026-05-06 | 已发表 (EMNLP) | 已发表 |

> **注意**: 用户上下文中提到的 `github.com/xrenaf/MEMLENS` 是一个**不同的评测框架**（MemLens），有 789 道题、5 种任务类型、4 种上下文长度（32K/64K/128K/256K）。虽然名称相似，但 MemEye（本报告主体）来自 `github.com/MinghoKwok/MemEye`，两团队不同。建议 iZu 关注 MemEye（更关注视觉证据粒度）而非 MemLens。

---

## 附录 B：关键资源链接

| 资源 | 链接 |
|------|------|
| 论文 (arXiv) | https://arxiv.org/abs/2605.15128 |
| 项目主页 | https://minghokwok.github.io/MemEye/ |
| GitHub 仓库 | https://github.com/MinghoKwok/MemEye |
| HuggingFace 数据集 | https://huggingface.co/datasets/MemEyeBench/MemEye |
| 数据集图片 | https://huggingface.co/datasets/MemEyeBench/MemEye/tree/main/data/image |

---

*本报告由调研员生成，基于 arXiv:2605.15128 v1 及对应 GitHub/HuggingFace 资源。*
