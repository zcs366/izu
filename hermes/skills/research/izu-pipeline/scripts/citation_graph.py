#!/usr/bin/env python3
"""izu 引用图谱模块 — 创建/读取/更新 wiki/citation-graph.json"""
import json, sys, re
from pathlib import Path
from datetime import datetime

DEFAULT_PATH = "/mnt/i/hermes/wiki/citation-graph.json"

class CitationGraph:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = Path(path)
        self.data = self._load_or_init()
    def _load_or_init(self) -> dict:
        if self.path.exists(): return json.loads(self.path.read_text(encoding="utf-8"))
        return {"version": 1, "updated_at": datetime.now().isoformat(), "nodes": [], "edges": []}
    def save(self):
        self.data["updated_at"] = datetime.now().isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
    def add_node(self, node_id: str, node_type: str = "url", path: str = "", title: str = "") -> bool:
        if any(n["id"] == node_id for n in self.data["nodes"]): return False
        n = {"id": node_id, "type": node_type}
        if path: n["path"] = path
        if title: n["title"] = title
        self.data["nodes"].append(n); return True
    def add_edge(self, source: str, target: str, relation: str = "支持", strength: str = "中", verified: bool = False, note: str = "") -> bool:
        for e in self.data["edges"]:
            if e["source"] == source and e["target"] == target:
                e.update({"relation": relation, "strength": strength})
                if verified: e["verified"] = True
                if note: e["note"] = note; return False
        e = {"source": source, "target": target, "relation": relation, "strength": strength, "verified": verified}
        if note: e["note"] = note
        self.data["edges"].append(e); return True
    def import_from_citations(self, citations: list[dict], doc_id: str):
        self.add_node(doc_id, "document")
        for c in citations:
            url, text, conf = c.get("url"), c.get("text", ""), c.get("confidence", "unknown")
            if url:
                target_id = f"url:{url}"
                self.add_node(target_id, "url", title=text[:80])
            else:
                m = re.search(r'(wiki/[^\s\)\]\}]+)', text)
                if m:
                    target_id = f"doc:{m.group(1)}"; self.add_node(target_id, "wiki_doc", path=m.group(1))
                else:
                    target_id = f"concept:{text[:40]}"; self.add_node(target_id, "concept", title=text[:80])
            rel = {"verified": "支持", "inferred": "补充", "guess": "引用"}.get(conf, "引用")
            strg = {"verified": "强", "inferred": "中", "guess": "弱"}.get(conf, "中")
            self.add_edge(source=doc_id, target=target_id, relation=rel, strength=strg, verified=(conf=="verified"), note=text[:100] if not url else "")
    def get_stats(self) -> dict:
        nbt, ebr, vc = {}, {}, 0
        for n in self.data["nodes"]:
            t = n.get("type","unknown"); nbt[t]=nbt.get(t,0)+1
        for e in self.data["edges"]:
            r = e.get("relation","unknown"); ebr[r]=ebr.get(r,0)+1
            if e.get("verified"): vc+=1
        return {"nodes": len(self.data["nodes"]), "edges": len(self.data["edges"]), "types": nbt, "relations": ebr, "verified": vc}

if __name__ == "__main__":
    if len(sys.argv) < 2: print("用法: init|info|verify <file.md>"); sys.exit(1)
    g = CitationGraph()
    cmd = sys.argv[1]
    if cmd == "init": g.save(); print(f"图谱已创建: {DEFAULT_PATH}")
    elif cmd == "info":
        s = g.get_stats(); print(f"节点: {s['nodes']}  边: {s['edges']}  已验证: {s['verified']}")
    elif cmd == "verify" and len(sys.argv) >= 3:
        from extract_inline_citations import extract_inline_citations
        text = Path(sys.argv[2]).read_text(encoding="utf-8")
        cits = extract_inline_citations(text)
        g.import_from_citations(cits, f"doc:{Path(sys.argv[2]).stem}")
        g.save(); print(f"{len(cits)} 条引文已写入图谱")
