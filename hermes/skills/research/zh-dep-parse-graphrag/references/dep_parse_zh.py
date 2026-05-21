#!/usr/bin/env python3
"""
中文依赖解析 · 知识图谱构建 — 生产版
详见父技能 SKILL.md 第三节的中文特殊处理说明。
部署位置: izu/dep_parse_zh.py
"""
# 完整脚本已在 izu/dep_parse_zh.py，此处为占位引用。
# 核心要点:
#   1. lemma_为空 → 用 token.text
#   2. cop模式 → A是B → (A, 是, B)
#   3. noun_chunks不可用 → 手动提取连续NOUN/PROPN
#   4. 文本预处理 → 去markdown标记
#   5. 停用词过滤 → STOP_RELS 集合
# 详见 SKILL.md 第三节。
