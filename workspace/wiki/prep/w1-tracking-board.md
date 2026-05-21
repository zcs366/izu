# W1 跟踪看板（5/18→5/23）

## 总览
- 总工时预算：6h
- 关键路径：GraphRAG schema（W2依赖）
- 风险等级：中等

## 每日跟踪表
| 日期 | 任务 | 状态 | 工时 | 交付物 | 问题 |
|------|------|------|------|--------|------|
| 5/18（周一） | GraphRAG schema 定案 + 假引文分类模型 | 待开始 |  |  |  |
| 5/19（周二） | 假引文检测器原型（规则版） | 待开始 |  |  |  |
| 5/20（周三） | CAST 工具校准审计 | 待开始 |  |  |  |
| 5/21（周四） | CAST 校准修复代码 | 待开始 |  |  |  |
| 5/22（周五） | Misevolve 安全边界调研 | 待开始 |  |  |  |
| 5/23（周六） | Nate Silver 基线初稿审阅 + W1 复盘 | 待开始 |  |  |  |

## 预研产出索引
- GraphRAG假引文预研：wiki/prep/graphrag-false-citation-pre-study.md
- CAST工具校准审计：wiki/prep/cast-tool-audit-report.md
- 对齐代码化：scripts/izu_align_checker.py（已上线）

## 环境基线（实际数值）
- 脚本总行数：izu-pipeline.py 1301行，izu_align_checker.py 287行
- 脚本哈希（MD5）：izu-pipeline.py = `e0f6618414d869b46c49491a89b7b471`，izu_align_checker.py = `97b78162dd1d99fc36093d001b1c153c`
- 依赖项数：scripts/*.py 共 16 个文件
- 每日管线建议运行次数：10次

## Git 状态
- 当前仓库未启用 git（无 .git 目录）
