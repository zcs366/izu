---
name: peer-review
description: 双模型同行评议——MiniMax审方法/数据/逻辑，千问审文献/创新/术语。并行审读→交叉比对→评议报告。鲁班超级专家团旗下同行评议Agent的实际执行体。
version: 1.0.0
tags:
  - 同行评议
  - 论文审读
  - 双模型
  - MiniMax
  - 千问
  - 交叉验证
trigger: "论文入库前评议 | peer_review | 同行评议 | 审一下这篇"
metadata:
  hermes:
    category: research
author: Hermes Agent
------

# 同行评议 · 双模型交叉审读系统

> "在吕克昂学园，亚里士多德让弟子收集158个城邦的政体，然后逐一评议。2500年后，同一个逻辑结构在跑——只是评议者从一个人变成了两个模型。"

## 触发条件

- **自动**：新论文markdown下载到 `wiki/raw/` 后，军师调用 peer_review.py 进行入库前评议
- **手动**：用户说"审一下这篇""同行评议""这篇论文怎么样"

## 架构

### 双模型分工

| 模型 | 来源 | 审读维度 | 成本 | 特质 |
|------|------|---------|------|------|
| **MiniMax-Text-01** | MiniMax官方API（包月/按量） | 方法有效性·数据可信度·逻辑严密性 | ¥0.0055/篇 | 严苛，用实证标准审问 |
| **Qwen-Max** | 阿里云百炼（按量） | 文献覆盖·创新性·术语准确性 | ¥0/月（100万token免费） | 温和，但领域编辑视角 |

### 评分维度

| 维度 | 权重 | 审读模型 | 得分范围 |
|------|------|---------|---------|
| 方法有效性 | 25% | MiniMax | 0-10 |
| 数据可信度 | 20% | MiniMax | 0-10 |
| 逻辑严密性 | 15% | MiniMax | 0-10 |
| 文献覆盖 | 15% | 千问 | 0-10 |
| 创新性 | 15% | 千问 | 0-10 |
| 术语准确性 | 10% | 千问 | 0-10 |

### 判定逻辑

```
双过 → ✅ 入库·高信度
一过一否 → ⚠️ 分歧·升级人工
双否 → ❌ 不入库（附双份驳回理由）
```

加权总分 = MiniMax均分 × 0.55 + 千问均分 × 0.45

## 使用

```bash
cd /mnt/i/hermes/scripts
python3 peer_review.py <论文路径.md>          # 从文件读取
python3 peer_review.py --text "论文全文..."    # 直接传入
```

输出：`output/peer-review/review_XXX_YYYYMMDD_HHMMSS.md`

首次验证（2026-05-15，白皮书《从游戏中长出的学习》）：
- MiniMax 7.7/10（方法/数据/逻辑）
- 千问 8.0/10（文献/创新/术语）
- 加权 7.8/10
- 判定：⚠️ 分歧·升级人工
- 耗时：41.8秒
- 人工仲裁：通过（教育理论·框架构建类别，非实证研究）

## 已知陷阱

### 陷阱一：截断

论文超过8000字会被截断（目前硬限制）。对于超过8000字的白皮书/长编，截断首端。如果核心方法在尾部，可能漏评。

**缓解**：长白皮书先拆成章节再审，或分"方法节""结果节""讨论节"逐段审。

### 陷阱二：环境变量

两个API key均从 `.hermes/.env` 读取（`MINIMAX_CN_API_KEY` 和 `DASHSCOPE_API_KEY`）。脚本已含 `dotenv.load_dotenv()`，只需要这两个变量在 `.env` 中存在。

如果API报"login fail"或"you didn't provide an API key"，检查 `.env` 中这两个key。

### 陷阱三：千问按量计费

阿里百炼按量付费。Qwen-Max 约2元/百万token。单篇论文约5000 token输入+500 token输出 ≈ ¥0.011。每月100万token免费额度覆盖约200篇论文，超出后按量计费。

MiniMax包月到2026-06-14，期内随便用。

### 陷阱四：MiniMax判定偏严

经验：MiniMax倾向于"存疑"（对方法复现性和量化指标要求高），千问倾向于"通过"（更看重理论框架完整性）。这不是bug——是双模型设计的核心价值。不一致标记正是需要人工介入的信号。

## 进化闭环

每次评议产出的分歧 → 记入 `output/peer-review/` + log.md → 用于校准双模型评分 → 下次评议更精确。

## 配置参考

- MiniMax API: https://api.minimaxi.com/v1/text/chatcompletion_v2
- 千问 API: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
- 脚本: `scripts/peer_review.py`
