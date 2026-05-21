# GraphRAG 引文 Schema 设计初稿

> W2 关键路径核心交付物。与 izu-pipeline 写步骤 + 引文验证步骤对接。
> 日期：2026-05-16 | 状态：初稿

---

## 一、问题回顾

izu wiki 的 markdown 文件产出中，引文（URL、实体引用、数据来源）缺乏统一格式。写步骤自然语言表述来源，引文验证步骤没有标准格式可提取。结果：无法程序化验证引文真实性，假引文问题无法自动化检测。

---

## 二、Schema 设计方案

### 2.1 行内引文格式

采用 markdown 兼容的 `[置信标记](来源)` 格式。不影响阅读，同时支持程序提取。

**格式规则：**
- ✅[URL] — 可从来源确认的事实
- ⚠️[URL] — 基于多源的合理推断
- ❓[说明] — 猜测，无法验证
- 来源可以是 URL、wiki 文件路径、或概念名

**场景示例1：直接引用URL**
```
GPT-4 训练成本估计超过1亿美元 ✅[https://openai.com/blog/gpt-4]
```
✅ 前是断言，✅后是证实来源

**场景示例2：推断性结论**
```
Scaling Law 的边际收益在递减 ⚠️[arXiv:2301.12345]
```
推断性结论，来源只部分支持

**场景示例3：推测**
```
一些人（如Gary Marcus）认为光靠增大模型永远到不了AGI ❓[个人观点，非实证]
```
猜测，标注了依据性质而非URL

**场景示例4：多来源印证**
```
RLHF显著提升模型对齐能力 ✅[https://arxiv.org/abs/2203.02155] ✅[Anthropic博客]
```
多来源印证同一事实

**场景示例5：引用 wiki 内部文档**
```
端木的听觉通道堵塞在学习拼音时表现明显 ✅[wiki/entities/端木-wo-aiduanmu.md]
```
引用 wiki 内部实体档案，可用文件存在性检查验证

**场景示例6：引用概念定义**
```
"明"是izu七则之首 ✅[wiki/concepts/izu-七则.md]
```
引用知识库概念，可检查概念存在性和关系一致性

---

### 2.2 文档级引用元数据

在 YAML frontmatter 中增加 `references` 和 `validated` 字段。

```yaml
---
title: AGI长编 · 面3：技术面
version: v2.0
tags: [AGI, 技术路线, 大语言模型]
references:
  - id: ref-gpt4-blog
    url: https://openai.com/blog/gpt-4
    title: GPT-4 Technical Report
    status: verified          # verified / pending / dead / superseded
    verified_at: 2026-05-10
  - id: ref-arxiv-scaling
    url: https://arxiv.org/abs/2301.12345
    title: Scaling Law Discussion
    status: dead              # 死链，需要更新
  - id: ref-wiki-duanmu
    path: wiki/entities/端木-wo-aiduanmu.md
    title: 端木成长档案
    status: verified
    verified_at: 2026-05-16
  - id: ref-izu-七则
    path: wiki/concepts/izu-七则.md
    title: 明学七则
    status: pending
related:
  - file: wiki/concepts/izu-七则.md
    relation: 延伸
  - file: wiki/entities/端木-wo-aiduanmu.md
    relation: 引用
  - url: https://arxiv.org/abs/2601.05866
    relation: 补充
validated_at: 2026-05-16
next_review: 2026-06-16
---
```

字段说明：
- references.id — 唯一标识，供行内引文引用
- references.status — 验证状态，供程序化检查
- related — 本文与其它文档的关系
- validated_at — 最后验证时间
- next_review — 下次审查时间

---

### 2.3 引用图谱结构

设计一个轻量的关系图谱文件，存储文档/实体间的引用关系。

**方案：单一图谱文件 wiki/citation-graph.json**

不采用分布式存储（每个文件存自己相关的），理由是：
1. 集中式图谱方便全局查询（"哪些文档引用了A？"）
2. 验证时只需读一个文件，无需扫描所有 markdown
3. JSON 格式易于程序读写

```json
{
  "version": 1,
  "updated_at": "2026-05-16",
  "nodes": [
    {"id": "doc:AGI技术面", "type": "document", "path": "output/doc/AGI长编_面3_技术面.md"},
    {"id": "entity:端木", "type": "entity", "path": "wiki/entities/端木-wo-aiduanmu.md"},
    {"id": "concept:izu-七则", "type": "concept", "path": "wiki/concepts/izu-七则.md"},
    {"id": "url:https://openai.com/blog/gpt-4", "type": "url"},
    {"id": "url:https://arxiv.org/abs/2601.05866", "type": "url"}
  ],
  "edges": [
    {"source": "doc:AGI技术面", "target": "url:https://openai.com/blog/gpt-4", 
     "relation": "支持", "strength": "强", "verified": true},
    {"source": "doc:AGI技术面", "target": "entity:端木",
     "relation": "引用", "strength": "弱", "verified": false,
     "note": "仅作为类比引用，非核心论据"},
    {"source": "concept:izu-七则", "target": "entity:端木",
     "relation": "适用", "strength": "中", "verified": false}
  ]
}
```

**关系类型枚举：**
| 关系 | 含义 | 检查方式 |
|------|------|---------|
| 支持 | 来源数据支持断言 | 语义验证 |
| 反驳 | 来源与断言矛盾 | 语义验证 |
| 补充 | 来源补充说明但非直接证据 | 仅URL检查 |
| 延伸 | 相关但不直接引用 | 无检查 |
| 引用 | 文中引用了实体/概念 | 文件存在性检查 |
| 适用 | 概念适用于实体 | 无检查 |

**强度定义：**
- 强：断言的核心支撑，引文错误则断言不成立
- 中：断言的重要补充，引文错误则断言弱化
- 弱：参考性引用，引文错误不影响断言有效性

---

### 2.4 验证结果持久化

引文验证步骤产出的验证结果，存储为独立的验证报告文件和图谱更新。

**验证报告格式（/mnt/i/hermes/output/doc/{slug}_引文验证_{timestamp}.md）：**

```
## 引文验证报告
文件: AGI长编_面3_技术面.md
验证时间: 2026-05-16 09:32:47

### 总览
| 指标 | 数值 |
| 引文总数 | 15 |
| 已验证 ✅ | 10 |
| 死链 ❌ | 2 |
| 无法确认 ⚠️ | 3 |

### 死链详情
- ❌ https://old-blog.example.com → HTTP 404
- ❌ https://dead-link.org/article → ConnectionError

### 语义验证结果
| 断言 | 引文 | 判定 |
| GPT-4训练成本>1亿美元 | ✅[openai.com/blog/gpt-4] | SUPPORTED |
| Scaling Law边际收益递减 | ⚠️[arXiv:2301.12345] | PARTIAL |

### 图谱更新
- 新增边: 3条
- 更新状态: 2条（verified→dead）
```

**验证历史追踪方式：**
- 验证报告本身是一个 markdown 文件
- 每次验证更新 citation-graph.json 中的 verified 字段
- 验证历史可通过文件名中的时间戳回溯

**失败引文的标记流程：**
1. 引文验证步骤发现死链 → 标记 status=dead
2. 图谱中对应 edge 的 verified 设为 false
3. 下次写步骤时可识别并提示作者更新
4. 连续3次验证失败 → 自动从引用列表中降级为 ⚠️

---

## 三、与 izu-pipeline 的集成方案

### 3.1 写步骤

写步骤的 prompt 已更新（含引文标注指令）。输出示例：

```
# 实际输出示例

GPT-4 的训练成本超过1亿美元 ✅[https://openai.com/blog/gpt-4]。

Scaling Law 在2024年后边际收益递减 ⚠️[arXiv:2301.12345]。

一些人认为光靠增大模型永远到不了AGI ❓[Gary Marcus个人博客]。

RLHF技术显著提升了模型对齐能力 
✅[https://arxiv.org/abs/2203.02155] ✅[Anthropic博客, 2024]。
```

**写步骤同时输出的元数据文件：**
写步骤做完后，自动生成一个 `{slug}_引用_{timestamp}.yaml` 的旁注文件，包含 YAML references 字段的草案。

### 3.2 引文验证步骤

**验证步骤的输入：**
- 写步骤产出的 markdown 文件（含行内引文）
- 当前 citation-graph.json（现有图谱）
- wiki/ 目录下所有实体/概念文件（存在性检查）

**验证步骤的输出：**
- 验证报告 markdown 文件
- 更新后的 citation-graph.json
- 失败引文列表（供修步骤参考）

**验证步骤的检查顺序：**
1. 提取所有行内引文（代码层）
2. URL 可达性检查（HEAD 请求）
3. 文件路径存在性检查（wiki 内部引用）
4. 语义验证（可选LLM：断言是否被引文支持）

### 3.3 回滚策略

当引文验证发现严重问题时：

**轻度问题（死链 < 20%、语义不匹配 < 30%）：**
- 记录验证报告
- 标记 specific 引文为 ⚠️
- 继续流水线

**中度问题（死链 20-50% 或 语义不匹配 30-60%）：**
- 标记为 ⚠️
- 回退到修步骤，要求补充/替换来源
- 修步骤完成后重新验证

**重度问题（死链 > 50% 或 任何假引文：断言凭空编造）：**
- 标记为 ❌
- 回退到织或写步骤
- 要求重新组织关联地图后再写作
- 审计当前 pipeline 是否数据污染

---

## 四、实施路线

### W2 周一
- 在写步骤中实现行内引文格式输出（prompt 已加，需验证实际输出是否符合格式）
- 写一个 `extract_inline_citations.py` 从 markdown 中提取所有行内引文
- 集成到引文验证步骤

### W2 周二
- 创建 citation-graph.json 的读写模块
- 实现验证步骤：URL 可达性 + 文件存在性检查
- 实现验证报告输出

### W2 周三-周四
- 图谱更新逻辑（验证后自动更新 graph 的 verified 状态）
- 回滚策略代码化
- 与写步骤联调

### 依赖项
- W2 开工前：引文验证步骤必须在 pipeline 中可用（✅ 今天已集成）
- W2 开工前：写步骤必须有引文标注指令（✅ 今天已加）
- W2 开工前：citation-graph.json 初始版本（这个文档就是初稿）

---

## 五、风险与备选

### 关键风险
1. 写步骤的 LLM 不按引文格式输出——即使加了 prompt 指令，LLM 可能忽略或格式走样
   缓解：验证步骤可做格式容错，支持多种变体
   如果不行：在修步骤中增加"修正引文格式"的指令

2. citation-graph.json 单文件并发冲突——如果多个流水线同时运行，写操作冲突
   缓解：使用文件锁（Python fcntl 或 filelock 库）
   备选：降级为每个文档独立存储引用元数据，不做全局图谱

3. 验证步骤增加 pipeline 运行时间——每个 URL 的 HEAD 请求耗时不等
   缓解：设置超时 5 秒，并行检查（concurrent.futures）
   限流：最多验证 50 个 URL/次运行

### 降级方案
如果完整方案推不动，执行降级：
1. 先用行内引文格式（不需要图谱文件）
2. 只做 URL 可达性检查（不需要语义验证）
3. 验证报告直接输出到 terminal（不需要持久化）
