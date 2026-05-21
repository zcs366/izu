# 评估输出路由规则

用户通过标记表达处理深度。以下表为准：

| 用户标记 | 处理深度 | wiki输出 | I盘输出 | 成对要求 |
|---------|---------|---------|---------|---------|
| `极大 <URL>` | 军师级+合议 | `research/{slug}-eval.md` + `raw/{slug}-transcript.md` | `/mnt/i/hermes/output/极大/{slug}-transcript.md` + `{slug}-eval.md` | ✅ 成对 |
| `大 <URL>` | 标准评估 | 同上 | `/mnt/i/hermes/output/大/{slug}-transcript.md` + `{slug}-eval.md` | ✅ 成对 |
| 无标记/评估分析存入wiki | 标准评估 | 同上 | 不入 | — |
| 评估可行性 | 评估不入wiki | 不入 | 不入 | — |
| 存入wiki | 仅入库 | `raw/articles/{slug}-raw.md` | 不入 | — |

## 绝对路径

I盘在WSL中的挂载点：`/mnt/i/hermes/output/`
即Windows路径：`I:\hermes\output\`

## 铁律

- 转录原文（带时间戳全文）和评估分析必须成对出现，缺一不可
- 用户习惯看原文，需要原文「慢慢消化」
- 大和极大文件夹严格分开，不混放
- wiki仍然必须入库
