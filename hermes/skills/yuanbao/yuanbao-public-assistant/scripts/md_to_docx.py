#!/usr/bin/env python3
"""
MD/HTML → Word 转换器
将 I:/hermes/output/ 下的 .md/.html 文件转为 .docx，输出到同目录。
匠石原则：纯代码，零LLM。
"""
import os, re, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT_DIR = "/mnt/i/hermes/output"

def md_to_docx(md_path: str, docx_path: str = None) -> str:
    """将 Markdown 文件转为 Word 文档。返回 docx 路径。"""
    if docx_path is None:
        docx_path = md_path.rsplit(".", 1)[0] + ".docx"
    
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    doc = Document()
    # 设置默认字体
    style = doc.styles['Normal']
    font = style.font
    font.name = '宋体'
    font.size = Pt(11)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    
    lines = text.split('\n')
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []
    
    for i, line in enumerate(lines):
        # 代码块
        if line.strip().startswith('```'):
            if in_code_block:
                # 结束代码块
                code_text = '\n'.join(code_lines)
                p = doc.add_paragraph()
                run = p.add_run(code_text)
                run.font.name = 'Consolas'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                p.paragraph_format.left_indent = Inches(0.3)
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # 表格检测（简单管道表格）
        if '|' in line and line.strip().startswith('|'):
            in_table = True
            table_rows.append(line)
            continue
        elif in_table and line.strip():
            if '|' in line:
                table_rows.append(line)
                continue
            else:
                # 表格结束，渲染
                _render_table(doc, table_rows)
                table_rows = []
                in_table = False
        
        stripped = line.strip()
        if not stripped:
            continue
        
        # 标题
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            level = len(header_match.group(1))
            heading = doc.add_heading(header_match.group(2), level=level)
            continue
        
        # 无序列表
        list_match = re.match(r'^[-*+]\s+(.+)$', stripped)
        if list_match:
            p = doc.add_paragraph(list_match.group(1), style='List Bullet')
            _apply_inline_format(p, list_match.group(1))
            continue
        
        # 有序列表
        num_match = re.match(r'^\d+[.)]\s+(.+)$', stripped)
        if num_match:
            p = doc.add_paragraph(num_match.group(1), style='List Number')
            _apply_inline_format(p, num_match.group(1))
            continue
        
        # 水平线
        if stripped in ('---', '***', '___'):
            doc.add_paragraph('─' * 60)
            continue
        
        # 引用
        if stripped.startswith('>'):
            quote_text = re.sub(r'^>\s?', '', stripped)
            p = doc.add_paragraph()
            run = p.add_run(quote_text)
            run.font.italic = True
            run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
            p.paragraph_format.left_indent = Inches(0.5)
            continue
        
        # 普通段落
        p = doc.add_paragraph()
        _apply_inline_format(p, stripped)
    
    # 残留表格
    if table_rows:
        _render_table(doc, table_rows)
    
    doc.save(docx_path)
    return docx_path


def html_to_docx(html_path: str, docx_path: str = None) -> str:
    """HTML → Word。先用简单方式提取文本再转。"""
    if docx_path is None:
        docx_path = html_path.rsplit(".", 1)[0] + ".docx"
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 简单HTML→文本提取
    # 移除script/style标签
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # 标题
    for i in range(1, 7):
        html = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'\n## \1\n', html, flags=re.IGNORECASE)
    
    # 段落
    html = re.sub(r'<p[^>]*>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</p>', '\n', html, flags=re.IGNORECASE)
    
    # 换行
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    
    # 列表
    html = re.sub(r'<li[^>]*>', '- ', html, flags=re.IGNORECASE)
    html = re.sub(r'</li>', '\n', html, flags=re.IGNORECASE)
    
    # 粗体/斜体
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.IGNORECASE)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.IGNORECASE)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.IGNORECASE)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.IGNORECASE)
    
    # 移除其余标签
    html = re.sub(r'<[^>]+>', '', html)
    
    # 写入临时md
    tmp_md = html_path.rsplit(".", 1)[0] + "_tmp.md"
    with open(tmp_md, "w", encoding="utf-8") as f:
        f.write(html)
    
    result = md_to_docx(tmp_md, docx_path)
    os.remove(tmp_md)
    return result


def _apply_inline_format(paragraph, text):
    """处理行内格式：粗体、斜体、行内代码"""
    # 拆分粗体 **text**
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith('*') and part.endswith('*') and not part.startswith('**'):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        elif part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(9)
        else:
            paragraph.add_run(part)


def _render_table(doc, rows):
    """将管道表格行渲染为Word表格"""
    # 解析行
    parsed = []
    for row in rows:
        if re.match(r'^[\s|:\-]+$', row):  # 分隔行
            continue
        cells = [c.strip() for c in row.strip('|').split('|')]
        parsed.append(cells)
    
    if not parsed or len(parsed) < 1:
        return
    
    ncols = max(len(r) for r in parsed)
    table = doc.add_table(rows=len(parsed), cols=ncols, style='Light Grid Accent 1')
    
    for i, row in enumerate(parsed):
        for j, cell_text in enumerate(row):
            if j < ncols:
                table.cell(i, j).text = cell_text


def find_files(keyword: str = None, limit: int = 10):
    """在 OUTPUT_DIR 中查找 md/html 文件。按修改时间倒序。"""
    files = []
    for root, dirs, filenames in os.walk(OUTPUT_DIR):
        for f in filenames:
            if f.endswith(('.md', '.html')):
                full = os.path.join(root, f)
                stat = os.stat(full)
                files.append((full, stat.st_mtime, f))
    
    files.sort(key=lambda x: x[1], reverse=True)
    
    if keyword:
        files = [f for f in files if keyword.lower() in f[2].lower()]
    
    return files[:limit]


# === CLI ===
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # 列出最近文件
        print("📂 I:/hermes/output/ 最近的文件：")
        for path, mtime, name in find_files(limit=15):
            import datetime
            dt = datetime.datetime.fromtimestamp(mtime)
            size = os.path.getsize(path)
            print(f"  {dt.strftime('%m-%d %H:%M')}  {size:>8,}B  {name}")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "find":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        results = find_files(keyword, limit=10)
        for path, mtime, name in results:
            print(f"FOUND:{path}")
    
    elif cmd == "convert":
        # 转换指定文件
        filepath = sys.argv[2] if len(sys.argv) > 2 else None
        if not filepath or not os.path.exists(filepath):
            # 查找最新文件
            results = find_files(limit=1)
            if not results:
                print("ERROR: No files found")
                sys.exit(1)
            filepath = results[0][0]
        
        if filepath.endswith('.md'):
            result = md_to_docx(filepath)
        elif filepath.endswith('.html'):
            result = html_to_docx(filepath)
        else:
            print(f"ERROR: Unsupported format: {filepath}")
            sys.exit(1)
        
        print(f"CONVERTED:{result}|{filepath}")
    
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: converter.py [find [keyword]] [convert [filepath]]")
