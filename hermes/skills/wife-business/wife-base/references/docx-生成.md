# Markdown → Word 文档生成（Python-docx）

## 用途

将 wife-base 产出的 markdown 文件转换为可直接递交/打印的 .docx 格式。洁琼是计算机新手，优先交付 Word 文档，md 文件作为编辑源留存。

## 前置条件

```bash
pip install python-docx
```

## 核心代码模板

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# === 全局字体 ===
style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)

# === 标题 ===
title = doc.add_heading('文档标题', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# === 联系人信息 ===
for line in ['呈报单位：XXX', '联系人：张洁琼 / 19961507078']:
    p = doc.add_paragraph(line)
    p.runs[0].font.size = Pt(10.5)

# === 章节标题 ===
doc.add_heading('一、章节名', level=2)

# === 正文 ===
doc.add_paragraph('正文内容...')

# === 表格 ===
table = doc.add_table(rows=4, cols=3, style='Table Grid')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
# 标题行
for i, h in enumerate(['列1', '列2', '列3']):
    table.rows[0].cells[i].text = h
# 数据行
for row_idx, row_data in enumerate(data_2d):
    for col_idx, cell_text in enumerate(row_data):
        table.rows[row_idx + 1].cells[col_idx].text = cell_text

# === 保存 ===
doc.save('/path/to/output.docx')
```

## 格式化要点

| 元素 | 方法 | 说明 |
|------|------|------|
| 全局字体 | `doc.styles['Normal'].font.name = '微软雅黑'` | 中文文档首选 |
| 标题居中 | `title.alignment = WD_ALIGN_PARAGRAPH.CENTER` | 文档标题用 level=0 |
| 章节标题 | `doc.add_heading('标题', level=2)` | level=2 对应二级标题 |
| 表格样式 | `style='Table Grid'` | 带边框格线 |
| 表格居中 | `table.alignment = WD_TABLE_ALIGNMENT.CENTER` | 表格整体居中 |
| 加粗文字 | `run.bold = True` | 段落内部分文字加粗 |
| 项目符号 | `doc.add_paragraph('文本', style='List Bullet')` | 无序列表 |
| 编号列表 | `doc.add_paragraph('文本', style='List Number')` | 有序列表 |

## 输出路径规范

所有 .docx 文件存入 `wife_business/01_国防基地/活动方案/` 目录，与对应 .md 文件同名。

## 已知限制

- python-docx 不直接支持 Markdown 自动解析，需手动逐元素构建
- 复杂嵌套结构（表格内列表）需特殊处理
- 中文字体仅在 Windows/Mac 已安装对应字体时生效
