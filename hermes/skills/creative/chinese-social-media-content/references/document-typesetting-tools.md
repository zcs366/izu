# Document Typesetting Tools (报刊杂志排版)

CLI-based typesetting tools for newspapers, magazines, newsletters, and print documents. All four tools below work in WSL/Linux and produce PDF output.

## Tool Overview

| Tool | Paradigm | Best For | Install |
|------|----------|----------|---------|
| **Typst** | Markup-based | Fast, modern typesetting from scratch | Binary download |
| **WeasyPrint** | HTML+CSS → PDF | Quick layout using web skills | `pip install` |
| **Vivliostyle CLI** | HTML+CSS → PDF | Complex magazine/book layouts | `npm install -g` |
| **Paged.js CLI** | HTML+CSS → PDF | W3C Paged Media standard compliance | `npm install -g` |

## Installation

### Typst
```bash
curl -fsSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ -C ~/.local/bin --strip-components=1
typst compile document.typ           # → document.pdf
typst watch document.typ             # auto-recompile on save
typst init @preview/dashing-dept-news  # init from newsletter template
```

### WeasyPrint
```bash
pip install weasyprint
weasyprint input.html output.pdf
# Or via Python:
# from weasyprint import HTML
# HTML(filename='input.html').write_pdf('output.pdf')
```

### Vivliostyle CLI
```bash
npm install -g @vivliostyle/cli
vivliostyle build index.html -o magazine.pdf
vivliostyle preview index.html
```

### Paged.js CLI
```bash
npm install -g pagedjs-cli
pagedjs-cli -i index.html -o output.pdf
```

## Workflows

### A: Markdown → Typst → PDF (Fastest)
```bash
# Write in Typst markup with multi-column layout
typst compile newspaper.typ newspaper.pdf
```

### B: HTML + CSS → PDF (Closest to Web Design)
```bash
weasyprint article.html article.pdf
vivliostyle build article.html -o article.pdf
```

### C: Markdown → HTML → PDF (via Pandoc)
```bash
pandoc article.md -o article.html --self-contained
weasyprint article.html article.pdf
```

## Chinese/CJK Fonts

WSL may lack CJK fonts. Install:
```bash
sudo apt install fonts-noto-cjk fonts-noto-cjk-extra
# Or minimal:
sudo apt install fonts-wqy-microhei
```

For WeasyPrint/Vivliostyle, specify in CSS:
```css
body { font-family: "Noto Sans CJK SC", "Source Han Sans SC", sans-serif; }
```

## Troubleshooting

- **WeasyPrint missing deps**: `sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libcairo2`
- **Vivliostyle/Puppeteer**: `npx puppeteer browsers install chrome`
