"""Tests for dep_parse_zh.py — clean_text, extract_triplets, extract_concepts

依赖 mock: spacy.load (通过 patch dep_parse_zh.nlp)
"""

import pytest
from unittest.mock import patch, MagicMock


# ═══════════════════════════════════════════
# clean_text 测试（纯文本，无需 mock）
# ═══════════════════════════════════════════

class TestCleanText:
    """clean_text 函数测试"""

    def test_remove_yaml_frontmatter(self):
        from dep_parse_zh import clean_text
        text = "---\ntitle: test\n---\n实际内容"
        assert clean_text(text) == "实际内容"

    def test_remove_bold_markdown(self):
        from dep_parse_zh import clean_text
        assert clean_text("**粗体**内容") == "粗体内容"

    def test_remove_italic_markdown(self):
        from dep_parse_zh import clean_text
        assert clean_text("*斜体*内容") == "斜体内容"

    def test_remove_code_inline(self):
        from dep_parse_zh import clean_text
        assert clean_text("`code`块") == "code块"

    def test_remove_links(self):
        from dep_parse_zh import clean_text
        assert clean_text("[文本](http://url.com)") == "文本"

    def test_remove_headings(self):
        from dep_parse_zh import clean_text
        assert clean_text("## 二级标题") == "二级标题"

    def test_remove_list_markers(self):
        from dep_parse_zh import clean_text
        assert clean_text("- 列表项") == "列表项"

    def test_normalize_multiple_spaces(self):
        from dep_parse_zh import clean_text
        assert "  " not in clean_text("多   个   空格")

    def test_combined_formatting(self):
        from dep_parse_zh import clean_text
        text = "## **标题** *斜体* `代码` [链接](url)"
        assert clean_text(text) == "标题 斜体 代码 链接"

    def test_strip_result(self):
        from dep_parse_zh import clean_text
        assert clean_text("  两边有空格  ") == "两边有空格"

    def test_no_frontmatter_plain_text(self):
        from dep_parse_zh import clean_text
        assert clean_text("普通文本") == "普通文本"

    def test_empty_text(self):
        from dep_parse_zh import clean_text
        assert clean_text("") == ""

    def test_excessive_newlines(self):
        from dep_parse_zh import clean_text
        text = "第一段\n\n\n\n\n第二段"
        assert "\n\n\n" not in clean_text(text)


# ═══════════════════════════════════════════
# 通用 mock 工具
# ═══════════════════════════════════════════

def make_token(text, dep, pos, i, head=None, children=None, subtree=None):
    tok = MagicMock(spec=object)
    tok.text = text
    tok.dep_ = dep
    tok.pos_ = pos
    tok.i = i
    tok.head = head if head else tok
    tok.children = children if children else []
    tok.subtree = subtree if subtree else [tok]
    # 让 subtree 可迭代（已经是 list）
    return tok


def make_sent(tokens):
    sent = MagicMock()
    sent.__iter__ = lambda s: iter(tokens)
    return sent


# ═══════════════════════════════════════════
# extract_triplets 测试
# ═══════════════════════════════════════════

class TestExtractTriplets:
    """extract_triplets 测试 — patch dep_parse_zh.nlp"""

    # ───────── helpers ─────────
    def _basic_doc(self, subj_text, verb_text, obj_text):
        obj = make_token(obj_text, "dobj", "NOUN", 2)
        subj = make_token(subj_text, "nsubj", "NOUN", 0)
        verb = make_token(verb_text, "ROOT", "VERB", 1,
                          children=[subj, obj])
        subj.head = verb
        obj.head = verb
        sent = make_sent([subj, verb, obj])
        doc = MagicMock()
        doc.sents = [sent]
        return doc

    # ───────── tests ─────────
    @patch("dep_parse_zh.nlp")
    def test_basic_triplet(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        mock_nlp.return_value = self._basic_doc("人工智能", "推动", "发展")
        trips = extract_triplets("人工智能推动发展")
        assert len(trips) == 1
        assert trips[0]["s"] == "人工智能"
        assert trips[0]["r"] == "推动"
        assert trips[0]["o"] == "发展"

    @patch("dep_parse_zh.nlp")
    def test_no_verb(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        tok = make_token("太阳", "ROOT", "NOUN", 0)
        doc = MagicMock()
        doc.sents = [make_sent([tok])]
        mock_nlp.return_value = doc
        assert extract_triplets("太阳") == []

    @patch("dep_parse_zh.nlp")
    def test_empty_text(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        doc = MagicMock()
        doc.sents = []
        mock_nlp.return_value = doc
        assert extract_triplets("") == []

    @patch("dep_parse_zh.nlp")
    def test_duplicate_suppression(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        doc = self._basic_doc("猫", "吃", "鱼")
        # 两次相同句子 → 应去重
        doc.sents = [doc.sents[0], doc.sents[0]]
        mock_nlp.return_value = doc
        assert len(extract_triplets("猫吃鱼猫吃鱼")) == 1

    @patch("dep_parse_zh.nlp")
    def test_stop_rels_filtered(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        verb = make_token("的", "ROOT", "VERB", 1)
        doc = MagicMock()
        doc.sents = [make_sent([verb])]
        mock_nlp.return_value = doc
        assert extract_triplets("的") == []

    @patch("dep_parse_zh.nlp")
    def test_aux_filtered(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        aux = make_token("会", "aux:modal", "AUX", 1)
        doc = MagicMock()
        doc.sents = [make_sent([aux])]
        mock_nlp.return_value = doc
        assert extract_triplets("会") == []

    @patch("dep_parse_zh.nlp")
    def test_cop_pattern(self, mock_nlp):
        from dep_parse_zh import extract_triplets
        subj = make_token("Python", "nsubj", "NOUN", 0)
        cop = make_token("是", "cop", "VERB", 1)
        head = make_token("语言", "ROOT", "NOUN", 2,
                          children=[subj, cop],
                          subtree=[make_token("语言", "ROOT", "NOUN", 2)])
        subj.head = head
        cop.head = head
        sent = make_sent([subj, cop, head])
        doc = MagicMock()
        doc.sents = [sent]
        mock_nlp.return_value = doc
        trips = extract_triplets("Python是语言")
        assert any(t["r"] == "是" for t in trips)

    @patch("dep_parse_zh.nlp")
    def test_long_verb_filtered(self, mock_nlp):
        """长度超过6的动词不应产生三元组"""
        from dep_parse_zh import extract_triplets
        obj = make_token("目标", "dobj", "NOUN", 2)
        subj = make_token("系统", "nsubj", "NOUN", 0)
        verb = make_token("1234567", "ROOT", "VERB", 1, children=[subj, obj])
        subj.head = verb
        obj.head = verb
        doc = MagicMock()
        doc.sents = [make_sent([subj, verb, obj])]
        mock_nlp.return_value = doc
        assert extract_triplets("系统1234567目标") == []


# ═══════════════════════════════════════════
# extract_concepts 测试
# ═══════════════════════════════════════════

class TestExtractConcepts:
    """extract_concepts 测试 — patch dep_parse_zh.nlp"""

    @patch("dep_parse_zh.nlp")
    def test_basic_noun(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        tok = make_token("人工智能", "NOUN", 0)
        doc = MagicMock()
        doc.sents = [make_sent([tok])]
        doc.ents = []
        mock_nlp.return_value = doc
        assert "人工智能" in extract_concepts("人工智能")

    @patch("dep_parse_zh.nlp")
    def test_propn(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        tok = make_token("OpenAI", "PROPN", 0)
        doc = MagicMock()
        doc.sents = [make_sent([tok])]
        doc.ents = []
        mock_nlp.return_value = doc
        assert "OpenAI" in extract_concepts("OpenAI")

    @patch("dep_parse_zh.nlp")
    def test_entities(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        doc = MagicMock()
        doc.sents = [make_sent([])]
        ent = MagicMock()
        ent.text = "中华人民共和国"
        doc.ents = [ent]
        mock_nlp.return_value = doc
        assert "中华人民共和国" in extract_concepts("")

    @patch("dep_parse_zh.nlp")
    def test_short_phrase_filtered(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        tok = make_token("的", "PART", 0)
        doc = MagicMock()
        doc.sents = [make_sent([tok])]
        doc.ents = []
        mock_nlp.return_value = doc
        assert len(extract_concepts("的")) == 0

    @patch("dep_parse_zh.nlp")
    def test_no_concepts(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        doc = MagicMock()
        doc.sents = [make_sent([])]
        doc.ents = []
        mock_nlp.return_value = doc
        assert extract_concepts("...") == set()

    @patch("dep_parse_zh.nlp")
    def test_compound_phrase(self, mock_nlp):
        """NOUN + VERB 应拼接"""
        from dep_parse_zh import extract_concepts
        t1 = make_token("机器", "NOUN", 0)
        t2 = make_token("学习", "VERB", 1)
        doc = MagicMock()
        doc.sents = [make_sent([t1, t2])]
        doc.ents = []
        mock_nlp.return_value = doc
        concepts = extract_concepts("机器学习")
        assert any("学习" in c for c in concepts)

    @patch("dep_parse_zh.nlp")
    def test_trailing_particles_removed(self, mock_nlp):
        from dep_parse_zh import extract_concepts
        tok = make_token("测试了", "NOUN", 0)
        doc = MagicMock()
        doc.sents = [make_sent([tok])]
        doc.ents = []
        mock_nlp.return_value = doc
        concepts = extract_concepts("测试了")
        assert any("测试" in c for c in concepts)

    @patch("dep_parse_zh.nlp")
    def test_multi_token_noun_phrase(self, mock_nlp):
        """多个连续 NOUN/PROPN 应合并为一个短语"""
        from dep_parse_zh import extract_concepts
        t1 = make_token("自然", "NOUN", 0)
        t2 = make_token("语言", "NOUN", 1)
        t3 = make_token("处理", "VERB", 2)
        doc = MagicMock()
        doc.sents = [make_sent([t1, t2, t3])]
        doc.ents = []
        mock_nlp.return_value = doc
        concepts = extract_concepts("自然语言处理")
        # NOUN+NOUN+VERB 都在允许范围内
        assert any("语言处理" in c for c in concepts)
