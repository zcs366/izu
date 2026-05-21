#!/usr/bin/env python3
"""
izu 行内引文提取器 v1.0 — 从 pipeline 写步骤 markdown 输出中提取 ✅⚠️❓ 行内引文。
使用：python3 extract_inline_citations.py <markdown文件>
输出：提取报告（stdout）+ JSON 文件（同名.citations.json）
"""
import re, json
from pathlib import Path
from datetime import datetime

def extract_inline_citations(text: str) -> list[dict]:
    citations = []
    inline_pattern = r'([✅❓]|⚠️?)\[([^\]]+)\]'
    for match in re.finditer(inline_pattern, text):
        confidence_char = match.group(1).strip()
        if not confidence_char:
            continue
        content = match.group(2).strip()
        confidence_map = {"✅": "verified", "⚠️": "inferred", "❓": "guess"}
        url = None
        url_match = re.search(r'https?://[^\s\)\]\}]+', content)
        if url_match:
            url = url_match.group(0)
            clean_content = re.sub(r'https?://[^\s\)\]\}]+', '', content).strip()
            clean_content = re.sub(r'^[\s,，；;:：]+|[\s,，；;:：]+$', '', clean_content)
            content = clean_content if clean_content else content
        citations.append({
            "confidence": confidence_map.get(confidence_char, "unknown"),
            "text": content[:200], "url": url,
            "position": match.start(), "type": "inline",
        })
    ref_pattern = r'^\s*([✅❓]|⚠️?)\s*(.*?)[：:]\s*(https?://[^\s\)\]\}]+)'
    for match in re.finditer(ref_pattern, text, re.MULTILINE):
        confidence_char = match.group(1)
        description = match.group(2).strip()
        url = match.group(3)
        confidence_map = {"✅": "verified", "⚠️": "inferred", "❓": "guess"}
        citations.append({
            "confidence": confidence_map.get(confidence_char, "unknown"),
            "text": description[:200], "url": url,
            "position": match.start(), "type": "reference_section",
        })
    seen = set()
    deduped = []
    for c in citations:
        key = f"{c['url'] or ''}:{c['text'][:50]}"
        if key not in seen:
            seen.add(key)
            deduped.append(c)
    return deduped

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2: print("用法: python3 extract_inline_citations.py <文件.md>"); sys.exit(1)
    filepath = sys.argv[1]
    citations = extract_inline_citations(Path(filepath).read_text(encoding="utf-8"))
    print(f"引文: {len(citations)} 条")
    for c in citations:
        print(f"  [{c['confidence']:>8}] {c['text'][:50]} -> {c.get('url','-')}")
    out = str(Path(filepath).with_suffix(".citations.json"))
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"source": Path(filepath).name, "total": len(citations), "citations": citations}, f, ensure_ascii=False, indent=2)
    print(f"JSON: {out}")
