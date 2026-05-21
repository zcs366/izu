# HTML双通道渲染 · 背景与实战

> 2026-05 社区趋势：AI输出从Markdown向HTML进化
> 引爆点：Karpathy（124万浏览）→ Thariq Shihipar（440万/16h）→ 社区共识

## 核心理念

```
Markdown = 源文件层（编辑、协作、版本控制）
HTML     = 浏览/交付层（阅读、展示、决策、交互）
```

类似「源码」与「编译产物」的关系。.md 是 source of truth，.html 是面向人的消费形态。

## 演进路线（Karpathy勾勒）

```
raw text → Markdown（当前默认） → HTML（正在形成新默认） → interactive neural videos/simulations（终点）
```

## 为什么是现在？

1. **模型更强**：能稳定产出结构完整的HTML
2. **上下文更大**：额外标签的token成本不再敏感
3. **工具链成熟**：Claude Artifacts/Canvas已铺垫浏览器渲染习惯

## HTML比Markdown好在哪

| 维度 | Markdown | HTML |
|------|----------|------|
| 阅读体验 | 线性，从头读到尾 | 可跳转、折叠、tab切换、并排对比 |
| 信息密度 | 纯文本+简单格式 | SVG图表、交互控件、空间布局 |
| 交付形态 | 像草稿 | 像正式产出物 |
| 版本控制 | ✅ diff干净 | ❌ diff噪音大 |
| 编辑协作 | ✅ 天然适合 | ❌ 改一行需懂HTML |

## 实际应用场景（Thariq 20例覆盖）

- 探索与规划：多方案并排对比
- 代码review：diff、模块关系、热点路径空间化
- 设计系统：design token、组件变体
- 研究与学习：折叠区块、tab切换、术语表、图示
- 报告：时间线、图表、状态概览
- 定制编辑器：拖拽、切换、调参—人机协作界面

## 我们的输出体系

### 当前

```
wiki/         → .md（正确——源文件层）
output/大/    → .md（可以升级——交付层也应该是.html）
output/极大/  → .md（可以升级）
```

### 目标

```
wiki/         → .md（保持源文件层）
output/大/    → .md（源文件） + .html（交付层）
output/极大/  → .md（源文件） + .html（交付层）
output/doc/   → .md（技术报告源文件）
```

### 渲染脚本

`tools/render_report.py`（待建）

```
python tools/render_report.py <md_path>
```

输入：Markdown文件 → 输出：同目录同名.html

HTML模板应包含：
- 目录/锚点导航
- 折叠区块（深度分析默认折叠）
- 并排对比表格
- SVG内嵌图表（关键数据可视化选项）

## 关键警示

- ❌ **这不是Anthropic产品公告**：Karpathy是个人工作流推荐，非产品路线图
- ❌ **wiki不改HTML**：天然Markdown的优势（版本控制、搜索、diff）不可替代
- ❌ **不双向同步**：.md→.html单向，绝不反向（否则破坏源文件结构）
- ✅ **社区共识正在凝聚**：早一个月晚一个月差距巨大

## 原始来源

- Karpathy X: https://x.com/karpathy/status/2053872850101285137
- 军师评估入库: wiki/research/html-output-revolution-eval.md
