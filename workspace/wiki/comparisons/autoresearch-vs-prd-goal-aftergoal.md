# Autoresearch vs PRD→Goal→After-Goal 对比

> **对比目的：** 同为鸟窝（smallnest）开源的两个项目/方法论，分别走向「多智能体交叉审核」和「三段式固定流程」两条路径。理解其差异有助于选择合适场景。

| 对比维度 | Autoresearch | PRD → Goal → After-Goal |
|---------|-------------|------------------------|
| 开发者 | 鸟窝（smallnest） | 鸟窝（smallnest） |
| 核心理念 | 多智能体 review + 开发 | 三段式固定流程（PRD→卡片→自动收尾） |
| 开发方式 | 多Agent交叉审核循环 | 单智能体按卡片实现 |
| 代码审核 | 5个维度自动打分 | 无（依赖人类验收） |
| 灵活度 | 更灵活可配置 | 固定流程 |
| **开发速度** | 慢 | **快** |
| **Token费用** | 高 | **低** |
| 适用场景 | 大规模复杂项目、质量敏感 | 中小型模块、日常迭代 |
| 缺点 | 慢、贵、易死循环 | 单一视角、缺少交叉验证 |

## 军师判断

**PRD→Goal→After-Goal更适合我们当前的日常工作。** 原因：

1. 你一天6小时，不是全职——多Agent交叉审核的Token/时间成本太高
2. 我们的任务体量——大多是模块级功能，不是百万元项目
3. 军师本身就是一个"单智能体"——再加交叉审核链路的边际收益有限

但 Autoresearch 的思路可以作为 **post-merge 审计**：一个功能开发完后，让另一个Agent做五分钟快速CR。不是多轮交叉，是一轮质量门。

## 参考

- [[prd-goal-aftergoal-workflow|PRD→Goal→After-Goal 三段式研发流水线]]
- [[../raw/articles/autoresearch-software-dev|Autoresearch 原始文章]]
- [[niaowo|作者：鸟窝]]
