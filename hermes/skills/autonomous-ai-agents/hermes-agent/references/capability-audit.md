# Capability Audit Reference

Systematic procedure for verifying claimed agent capabilities against actual system state.

## Audit checklist

When asked to "确认你的能力" or "检查你的能力是否真实可用", run these checks:

### 1. CLI tools

```bash
which weasyprint     # PDF via HTML→CSS
which typst          # Professional typesetting
which vivliostyle    # CSS paged media
which pagedjs-cli    # JS-based pagination
which manim          # 3Blue1Brown animation (usually NOT installed)
which edge-tts       # TTS CLI (not needed if Python lib is used instead)
which brv            # ByteRover CLI
which camoufox       # Stealth browser
which docker         # Container runtime
which hindsight      # Memory provider CLI
```

### 2. Python packages

```bash
pip list 2>/dev/null | grep -iE 'pptx|docx|fitz|pymupdf|marker|manim|edge-tts|fastapi|torch'
```

### 3. Skills presence

Skills are in `~/.hermes/skills/` under category subdirectories:
- `creative/` — infographic, comic, diagram, excalidraw, p5js, pixel-art, ascii-art, manim-video
- `media/` — youtube-content
- `productivity/` — ocr-and-documents

Check with:
```bash
find ~/.hermes/skills -name 'SKILL.md' | sort
```

### 4. Hermes tool availability

```bash
hermes tools list     # Shows enabled toolsets
```

Key toolsets: `web`, `browser`, `tts`, `vision`, `image_gen`, `code_execution`

### 5. Verifiable I/O capability matrix template

| Format | Tool/Engine | Status | Notes |
|--------|-------------|--------|-------|
| Markdown `.md` | native | ✅ Always | Default format |
| PDF (WeasyPrint) | `which weasyprint` | ✅/❌ | Fastest PDF |
| PDF (Typst) | `which typst` | ✅/❌ | Professional |
| PDF (Vivliostyle) | `which vivliostyle` | ✅/❌ | CSS magazine |
| PPT `.pptx` | python-pptx | ✅/❌ | |
| Image gen | `image_gen` toolset | ✅/❌ | |
| TTS | `tts` toolset + edge-tts pkg | ✅/❌ | |
| ... | extend per session | | |

### 6. Fix missing capabilities (opportunistic installs)

When the audit finds missing items that are low-cost to install, do it:
- `pip install edge-tts pymupdf --break-system-packages`
- `pip install manim --break-system-packages` (large, may need background process)
- Skills don't need "installation" — they load via `skill_view()` at runtime

## Writing the audit result

Output format: a markdown document with:
1. **Model matrix** (configured providers + their auth status)
2. **Output formats** (table: format → tool → verified status → notes)
3. **Input formats** (table: format → tool → verified status → notes)
4. **Task quick-reference** (user asks X → I do Y → output Z)
5. **Boundaries** (what I can't do)

Save to workspace: `I:\hermes\output\doc\军师祭酒-输入输出能力手册.md`
