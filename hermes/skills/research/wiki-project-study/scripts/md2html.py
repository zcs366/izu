#!/usr/bin/env python3
"""
md2html.py — Convert Markdown to styled HTML (no external libs).

Usage:
    python md2html.py input.md output.html "Project Title"

If output.html is omitted, prints to stdout.
If title is omitted, uses filename base.
"""

import re
import sys
import os


def md_to_html(md_text, project_name="Manual", css_extra=""):
    """Convert markdown to full HTML document with styling."""
    lines = md_text.split('\n')
    html_parts = []
    in_code = False
    in_list = {'ul': False, 'ol': False}
    in_table = None

    def _close_list():
        for k in list(in_list.keys()):
            if in_list[k]:
                html_parts.append(f'</{k}>\n')
                in_list[k] = False

    def _close_table():
        nonlocal in_table
        if in_table:
            html_parts.append('</tbody></table>\n')
            in_table = None

    def _inline(t):
        t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        return t

    for raw in lines:
        stripped = raw.strip()

        # Code blocks
        if stripped.startswith('```'):
            _close_list()
            _close_table()
            if in_code:
                html_parts.append('</code></pre>\n')
                in_code = False
            else:
                html_parts.append('<pre><code>')
                in_code = True
            continue
        if in_code:
            html_parts.append(raw + '\n')
            continue

        # Empty line
        if not stripped:
            _close_list()
            _close_table()
            html_parts.append('\n')
            continue

        # Headings
        if stripped.startswith('#### '):
            _close_list()
            _close_table()
            html_parts.append(f'<h4>{_inline(stripped[5:])}</h4>\n')
        elif stripped.startswith('### '):
            _close_list()
            _close_table()
            html_parts.append(f'<h3>{_inline(stripped[4:])}</h3>\n')
        elif stripped.startswith('## '):
            _close_list()
            _close_table()
            anchor = re.sub(r'[^a-z0-9\u4e00-\u9fff-]', '',
                            stripped[3:].strip().lower().replace(' ', '-'))[:40]
            html_parts.append(f'<h2 id="{anchor}">{_inline(stripped[3:])}</h2>\n')
        elif stripped.startswith('# '):
            _close_list()
            _close_table()
            html_parts.append(f'<h1>{_inline(stripped[2:])}</h1>\n')

        # Lists
        elif stripped.startswith('- '):
            _close_table()
            if not in_list['ul']:
                html_parts.append('<ul>\n')
                in_list['ul'] = True
            html_parts.append(f'<li>{_inline(stripped[2:])}</li>\n')
        elif (stripped and stripped[0].isdigit() and stripped[1:3] == '. ') or stripped.startswith('1. '):
            _close_table()
            if not in_list['ol']:
                html_parts.append('<ol>\n')
                in_list['ol'] = True
            content = stripped[stripped.index(' ') + 1:]
            html_parts.append(f'<li>{_inline(content)}</li>\n')

        # Tables
        elif stripped.startswith('|') and stripped.endswith('|') and len(stripped) > 3:
            _close_list()
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if '---' in stripped:
                continue
            if in_table is None:
                html_parts.append('<table><thead><tr>')
                for c in cells:
                    html_parts.append(f'<th>{_inline(c)}</th>')
                html_parts.append('</tr></thead><tbody>\n')
                in_table = True
            else:
                html_parts.append('<tr>')
                for c in cells:
                    html_parts.append(f'<td>{_inline(c)}</td>')
                html_parts.append('</tr>\n')

        # Blockquote
        elif stripped.startswith('> '):
            _close_list()
            _close_table()
            html_parts.append(f'<blockquote>{_inline(stripped[2:])}</blockquote>\n')
        elif stripped == '>':
            _close_list()
            _close_table()
            html_parts.append('<blockquote></blockquote>\n')

        # Horizontal rule
        elif stripped.startswith('---'):
            _close_list()
            _close_table()
            html_parts.append('<hr>\n')

        # Paragraph (catch-all)
        else:
            _close_list()
            _close_table()
            html_parts.append(f'<p>{_inline(stripped)}</p>\n')

    _close_list()
    _close_table()
    body = ''.join(html_parts)
    return _wrap_html(project_name, body, css_extra)


def _wrap_html(title, body, css_extra=""):
    css = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"WenQuanYi Zen Hei","Noto Sans CJK SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.8;color:#1a1a2e;max-width:840px;margin:0 auto;padding:2em 1.5em;background:#f8f9fa}
h1{font-size:26px;color:#0f3460;border-bottom:3px solid #0f3460;padding-bottom:8px;margin:1.5em 0 0.8em}
h2{font-size:20px;color:#1a3a6e;border-bottom:1px solid #dde;padding-bottom:4px;margin:1.2em 0 0.6em}
h3{font-size:17px;color:#2a5a9e;margin:1em 0 0.4em}
p{margin:0.6em 0;text-align:justify}
ul,ol{margin:0.5em 0 0.5em 1.8em}
li{margin:0.3em 0}
table{width:100%;border-collapse:collapse;margin:1em 0;font-size:14px}
th{background:#0f3460;color:white;padding:8px 12px;text-align:left}
td{padding:6px 12px;border:1px solid #ddd}
tr:nth-child(even) td{background:#f5f7fa}
code{font-family:"JetBrains Mono","Fira Code",monospace;font-size:13px;background:#eef;padding:2px 5px;border-radius:3px}
pre{background:#1a1a2e;color:#e8e8e8;padding:14px 18px;border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.5;margin:0.8em 0}
pre code{background:transparent;color:inherit;padding:0}
blockquote{border-left:4px solid #0f3460;padding:8px 16px;margin:0.8em 0;background:#eef2f8;color:#444;border-radius:0 4px 4px 0}
hr{border:none;border-top:1px solid #ddd;margin:2em 0}""" + css_extra

    cover = f"""<div class="cover">
<h1>{title}</h1>
<p class="meta">自动生成 · 军师祭酒</p>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>{css}
.cover{{text-align:center;padding:3em 1em;margin-bottom:2em;background:linear-gradient(135deg,#1a1a2e,#0f3460);color:#e8e8e8;border-radius:12px}}
.cover h1{{font-size:32px;border:none;margin:0;color:#fff}}
.cover .meta{{font-size:13px;color:#8899bb;margin-top:0.5em}}
</style></head>
<body>
{cover}
{body}
</body></html>"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    title = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(in_path))[0]

    with open(in_path, encoding='utf-8') as f:
        md_text = f.read()

    html = md_to_html(md_text, project_name=title)

    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ {out_path}")
    else:
        print(html)


if __name__ == '__main__':
    main()
