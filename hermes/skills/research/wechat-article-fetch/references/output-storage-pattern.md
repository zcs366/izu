# Output Storage Pattern

After evaluating any article/video, store in two places:

## 1. wiki（必须）

| 内容类型 | wiki路径 |
|---------|---------|
| 转录原文(raw) | `wiki/raw/articles/{slug-raw}.md` 或 `wiki/raw/{slug-transcript}.md` |
| 评估分析 | `wiki/research/{slug-eval}.md` |

## 2. output/I盘（根据深度标注）

| 标注 | output路径 | 内容 |
|------|-----------|------|
| 「大」 | `output/大/{slug-report}.md` + `.html` | 评估报告（含核心摘要/核实/定论/价值） |
| 「极大」 | `output/极大/{slug-report}.md` + `.html` | 深度评估报告 + 可选综述(synthesis-) |
| 「评估可行性」 | 不存output，仅回复 | — |
| 无标注 | 存wiki即可，output可选 | — |

## 铁律

1. `output/大/` 和 `output/极大/` 严格分开，不要混放
2. **HTML双版是标配** — 每份报告必须同时输出 `.md`（可读原文）和 `.html`（渲染友好）双版本，两个文件同名不同后缀。使用 `python3 -c "import markdown"` 将md转html（已装markdown库，无需Pandoc），附加基础CSS样式（`#8B5E3C`棕色调，`#fdf6ee`浅褐背景）。
3. wiki必须同步更新，不能只存output不存wiki
4. 视频类：转录原文 = 带时间戳的完整字幕稿
5. 文章类：转录原文 → 存 `wiki/raw/`；评估 → 存 `wiki/research/`；报告 → 存 `output/{级别}/`

## 对应路径

- wiki base: `/mnt/i/hermes/wiki/`
- output base: `/mnt/i/hermes/output/`
- 大: `/mnt/i/hermes/output/大/`
- 极大: `/mnt/i/hermes/output/极大/`
