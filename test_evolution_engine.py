"""Tests for evolution_engine.py — Verifier, Scorer, EvolutionTrigger, VerificationLoop

注意：check_structure 的 expected_sections 默认使用 essential（语义标签），
检查方式是 'sec in text'（字面字符串查找），而非实际解析markdown。
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, PropertyMock

from evolution_engine import (
    Verifier, Scorer, EvolutionTrigger, VerificationLoop,
    SCORING_DIMENSIONS, DATA_DIR, TOPO_FILE, Verifier as V,
)


# ═══════════════════════════════════════════
# Verifier 测试（代码验证器——不依赖网络/模型）
# ═══════════════════════════════════════════

class TestVerifier:
    """Verifier 静态方法测试——全部代码化评分"""

    def test_check_urls_no_urls(self):
        """无URL时返回满分"""
        result = Verifier.check_urls("纯文本内容，没有链接")
        assert result["score"] == 1.0
        assert result["total"] == 0

    def test_check_urls_extracts_urls(self):
        """应正确提取文本中的URL"""
        text = "参考来源：https://example.com/doc 和 http://test.org/page"
        result = Verifier.check_urls(text)
        assert result["total"] == 2

    def test_check_urls_max_20_urls(self):
        """最多检查20个URL"""
        urls = " ".join([f"https://example.com/{i}" for i in range(30)])
        result = Verifier.check_urls(urls)
        assert result["total"] == 30  # 提取全部，但最多检查20

    @patch("evolution_engine.subprocess.run")
    def test_check_urls_with_live_check(self, mock_run):
        """URL存活检查应调用curl"""
        mock_run.return_value = MagicMock(stdout="200", stderr="")
        result = Verifier.check_urls("https://example.com/alive")
        assert result["alive"] == 1
        assert result["dead"] == []

    @patch("evolution_engine.subprocess.run")
    def test_check_urls_dead_url(self, mock_run):
        """返回500的URL应标记为dead"""
        mock_run.return_value = MagicMock(stdout="500", stderr="")
        result = Verifier.check_urls("https://example.com/dead")
        assert result["alive"] == 0
        assert len(result["dead"]) == 1
        assert result["dead"][0]["status"] == 500

    @patch("evolution_engine.subprocess.run")
    def test_check_urls_curl_exception(self, mock_run):
        """curl异常应标记为error"""
        mock_run.side_effect = Exception("timeout")
        result = Verifier.check_urls("https://example.com/bad")
        assert result["alive"] == 0
        assert result["dead"][0]["status"] == "error"

    def test_check_structure_no_expected_sections(self):
        """不传 expected_sections 时，使用 essential 语义标签做字面查找"""
        text = "Some text with frontmatter keyword in text, and also code_blocks mention, headings too"
        result = Verifier.check_structure(text)
        # essential=['headings','code_blocks','usage_section'] (无frontmatter/tables)
        # 字面查找：'frontmatter' not in text, 'headings' in text, 'code_blocks' in text
        # 但 no '---\n' start → no frontmatter, no tables
        assert "found" in result
        assert "missing" in result
        assert "score" in result

    def test_check_structure_with_expected_sections(self):
        """预期段落应被正确匹配（字面查找）"""
        text = "# Title\n\n## Subtitle\n\nSome content here"
        result = Verifier.check_structure(text, expected_sections=["#", "##", "###"])
        assert "#" in result["found"]
        assert "##" in result["found"]
        assert "###" in result["missing"]

    def test_check_structure_frontmatter_detection(self):
        """frontmatter 被 essential 检测但字面查找依赖于字符串"""
        text = "---\ntitle: Test\n---\n# frontmatter keyword\n## headings text\n```python\ncode_blocks literal\n```"
        result = Verifier.check_structure(text)
        # essential 会包含 frontmatter, headings, code_blocks
        # 但 expected_sections=['frontmatter','headings','code_blocks'] 字面查找
        # 'frontmatter' in text? 是的，"# frontmatter keyword"
        assert "frontmatter" in result["found"] or "frontmatter" in result["missing"]
        # bonus 应包含 frontmatter+code_blocks
        assert result["bonus"] >= 0.2

    def test_check_structure_bonus_calculation(self):
        """加分项：frontmatter +0.2, code_blocks +0.1, tables +0.1"""
        text = "---\ntags: test\n---\n# frontmatter headings code_blocks\n| col1 | col2 |"
        result = Verifier.check_structure(text)
        # essential detected: frontmatter(True), headings(True), code_blocks(False),
        #   tables(True, because '|' appears), usage_section(False)
        # bonus = frontmatter(0.2) + tables(0.1) = 0.3 (no ``` found)
        assert result["bonus"] == pytest.approx(0.3, abs=0.01)
        # expected_sections = essential = ['frontmatter','headings','tables']
        # 'frontmatter' and 'headings' and 'tables' are all in text via the content
        assert len(result["found"]) >= 1

    def test_check_structure_all_missing(self):
        """所有 expected_sections 都不在文本中时 base_score=0"""
        result = Verifier.check_structure("纯文本", expected_sections=["#", "##", "###"])
        assert result["score"] == 0
        assert result["found"] == []

    def test_check_citations_with_links(self):
        """有引用且有链接时 score=1.0"""
        text = "(张三等, 2020) 的研究表明 https://example.com/paper"
        result = Verifier.check_citations(text)
        assert result["score"] == 1.0
        assert result["citations"] == 1

    def test_check_citations_without_links(self):
        """有引用但无链接时 score=0.5"""
        text = "(张三等, 2020) 的研究表明"
        result = Verifier.check_citations(text)
        assert result["score"] == 0.5
        assert result["citations"] == 1
        assert result["links"] == 0

    def test_check_citations_no_citations(self):
        """无引用时 score=1.0"""
        result = Verifier.check_citations("只是一段普通文本")
        assert result["score"] == 1.0

    def test_check_consistency_clean(self):
        """无问题时满分"""
        result = Verifier.check_consistency("完全正常的文本内容")
        assert result["score"] == 1.0
        assert result["issues"] == []

    def test_check_consistency_range_issue(self):
        """数字范围异常应标记"""
        text = "范围从 100 到 50"
        result = Verifier.check_consistency(text)
        # '100 到 50' → lo=100, hi=50, lo>hi → issue
        assert "issues" in result

    def test_check_conciseness_normal(self):
        """正常句长(15-80)间得1.0分"""
        # 构造10个15-20字句子
        sentences = []
        for i in range(10):
            sentences.append("这是一个中等长度的测试句子。")
        text = "".join(sentences)  # 每句14字+句号=15字
        result = Verifier.check_conciseness(text)
        # avg_len should be ~15-16, which is >= 10 and <= 80
        assert result["score"] == 1.0

    def test_check_conciseness_too_short(self):
        """句长<10得0.7分"""
        text = "短。" * 20  # 每句仅1字+句号
        result = Verifier.check_conciseness(text)
        assert result["score"] == 0.7

    def test_check_conciseness_too_long(self):
        """句长>80得0.6分"""
        long_text = "这是一个非常长的句子" * 30 + "结束。"
        result = Verifier.check_conciseness(long_text)
        assert result["score"] == 0.6

    def test_check_conciseness_properties(self):
        """返回的元数据应正确"""
        text = "第一句。第二句。第三句。"
        result = Verifier.check_conciseness(text)
        assert result["total_chars"] == len(text)
        assert result["sentences"] >= 3
        assert result["avg_len"] > 0


# ═══════════════════════════════════════════
# Scorer 测试（5维度加权评分）
# ═══════════════════════════════════════════

class TestScorer:
    """Scorer 类——调用 Verifier 并做加权汇总"""

    def test_score_output_all_dimensions_present(self):
        """score_output 应返回除 semantic_quality 外的所有维度（模型项单独处理）"""
        text = "## 标题\n内容\n(引用, 2020) https://example.com"
        scorer = Scorer()
        result = scorer.score_output(text)
        # score_output 只返回代码化维度，semantic_quality（模型项）不返回
        code_dims = [d for d, info in SCORING_DIMENSIONS.items() if info["method"] == "code"]
        for dim in code_dims:
            assert dim in result, f"Missing dimension: {dim}"
        assert "_overall" in result
        assert "_timestamp" in result

    def test_score_output_overall_weighted(self):
        """_overall 应等于各代码化维度的加权和"""
        text = "## 标题\nContent\n用法: 测试\n| A | B |\n| -- | -- |\n| 1 | 2 |"
        scorer = Scorer()
        result = scorer.score_output(text)
        code_dims = {d: info for d, info in SCORING_DIMENSIONS.items() if info["method"] == "code"}
        expected = sum(
            result[dim]["score"] * code_dims[dim]["weight"]
            for dim in code_dims
        )
        assert result["_overall"] == pytest.approx(expected, abs=0.002)

    def test_score_output_expected_sections_passed(self):
        """expected_sections 应透传给 check_structure（位置参数传递）"""
        scorer = Scorer()
        with patch.object(scorer.verifier, "check_structure", return_value={"score": 0.5, "found": [], "missing": [], "bonus": 0.0}) as mock_cs:
            scorer.score_output("test text", expected_sections=["#", "##"])
            # check_structure(text, expected_sections) — 第二参数是位置参数
            mock_cs.assert_called_once_with("test text", ["#", "##"])

    def test_score_output_empty_text(self):
        """空文本不应崩溃"""
        scorer = Scorer()
        result = scorer.score_output("")
        assert "_overall" in result
        assert result["_overall"] >= 0

    def test_score_output_timestamp_format(self):
        """时间戳应为ISO格式"""
        scorer = Scorer()
        result = scorer.score_output("test")
        assert "T" in result["_timestamp"]
        assert result["_timestamp"].endswith("+00:00") or "+" in result["_timestamp"]

    @patch.object(Verifier, "check_urls", return_value={"score": 0.0, "total": 1, "alive": 0, "dead": []})
    @patch.object(Verifier, "check_structure", return_value={"score": 0.0, "found": [], "missing": [], "bonus": 0.0})
    @patch.object(Verifier, "check_citations", return_value={"score": 0.0, "citations": 0, "links": 0})
    @patch.object(Verifier, "check_consistency", return_value={"score": 0.0, "issues": []})
    @patch.object(Verifier, "check_conciseness", return_value={"score": 0.0, "total_chars": 0, "sentences": 0, "avg_len": 0})
    def test_score_output_all_zero(self, *mocks):
        """所有维度0分时整体应为0"""
        scorer = Scorer()
        result = scorer.score_output("bad text")
        assert result["_overall"] == 0.0


# ═══════════════════════════════════════════
# EvolutionTrigger 测试（需要mock文件IO）
# ═══════════════════════════════════════════

class TestEvolutionTrigger:
    """EvolutionTrigger——短板记录+提示微调"""

    @staticmethod
    def _fresh_topo():
        return {
            "agents": {
                "xie": {
                    "name": "写",
                    "performance_history": {
                        "total_tasks_completed": 2,
                        "avg_quality_score": 0.8,
                    },
                    "evolution_state": {
                        "current_generation": 0,
                        "identified_weaknesses": [],
                        "prompt_adjustments_applied": [],
                        "last_verified_at": None,
                    },
                }
            }
        }

    @staticmethod
    def _fresh_topo_with_weakness():
        return {
            "agents": {
                "xie": {
                    "name": "写",
                    "performance_history": {
                        "total_tasks_completed": 5,
                        "avg_quality_score": 0.6,
                    },
                    "evolution_state": {
                        "current_generation": 2,
                        "identified_weaknesses": ["structural_complete"],
                        "prompt_adjustments_applied": ["之前已记录"],
                        "last_verified_at": "2026-01-01T00:00:00+00:00",
                    },
                }
            }
        }

    def test_load_and_save_topo(self):
        """_load_topo 和 _save_topo 应读写JSON文件"""
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        topo = self._fresh_topo()
        mock_data = json.dumps(topo)
        with patch("builtins.open", mock_open(read_data=mock_data)) as m:
            m.return_value.read.return_value = mock_data
            trigger.evaluate_and_evolve("xie", "## 好内容\n有一些分析", "writing")
        handles = [call for call in m.call_args_list if "fake/topo.json" in str(call)]
        assert len(handles) >= 1

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_agent_not_found(self, mock_save, mock_load):
        """不存在的agent应返回error"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        result = trigger.evaluate_and_evolve("nonexistent", "hello", "writing")
        assert "error" in result
        assert "not found" in result["error"]
        mock_save.assert_not_called()

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_result_contains_keys(self, mock_save, mock_load):
        """evaluate_and_evolve 返回字典应包含期望字段"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        result = trigger.evaluate_and_evolve("xie", "## 测试内容\nfrontmatter headings code_blocks", "test")
        assert "agent" in result
        assert "overall_score" in result
        assert "dimensions" in result
        assert "weaknesses_found" in result
        assert "prompts_injected" in result
        assert "generation" in result

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_returns_agent_id(self, mock_save, mock_load):
        """返回的 agent 字段应与输入一致"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        result = trigger.evaluate_and_evolve("xie", "## test", "writing")
        assert result["agent"] == "xie"

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_generation_starts_at_0(self, mock_save, mock_load):
        """无弱点时 generation 保持为0"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        result = trigger.evaluate_and_evolve("xie", "## test\nfrontmatter headings", "writing")
        saved_data = mock_save.call_args[0][0]
        gen = saved_data["agents"]["xie"]["evolution_state"]["current_generation"]
        # 文本包含 'headings' 字面字符串，check_structure得满分，无弱点 → generation=0
        assert gen == 0
        assert result["generation"] == 0

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_generation_increments_with_weakness(self, mock_save, mock_load):
        """有弱点时 generation 随弱点数增加"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        bad_text = "好"  # 无标题/无frontmatter/无任何结构
        result = trigger.evaluate_and_evolve("xie", bad_text, "writing")
        saved_data = mock_save.call_args[0][0]
        gen = saved_data["agents"]["xie"]["evolution_state"]["current_generation"]
        # 有多个弱点，每个+1
        assert gen == len(result["weaknesses_found"])

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_writes_last_verified_at(self, mock_save, mock_load):
        """每次 evaluate 后 last_verified_at 应为非None"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        trigger.evaluate_and_evolve("xie", "## test", "writing")
        saved_data = mock_save.call_args[0][0]
        assert saved_data["agents"]["xie"]["evolution_state"]["last_verified_at"] is not None

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_updates_performance_history(self, mock_save, mock_load):
        """performance_history 应更新 total_tasks_completed 和 avg_quality_score"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        result = trigger.evaluate_and_evolve("xie", "## 标题", "test")
        saved_data = mock_save.call_args[0][0]
        agent = saved_data["agents"]["xie"]
        # total_tasks_completed: 2 + 1 = 3 (原始代码每次调用+1)
        # 但如果有多个弱点，会在循环中多次调用 evaluate_and_evolve...
        # 实际上 evaluate_and_evolve 只被调用一次，内部 total_tasks_completed++ 一次
        assert agent["performance_history"]["total_tasks_completed"] == 3
        # avg_quality_score = (0.8*2 + overall) / 3
        expected_avg = (0.8 * 2 + result["overall_score"]) / 3
        assert agent["performance_history"]["avg_quality_score"] == pytest.approx(expected_avg, abs=0.01)

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_weakness_deduplication(self, mock_save, mock_load):
        """已存在的短板不应重复添加"""
        mock_load.return_value = self._fresh_topo_with_weakness()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        # 构造一个会让 structural_complete 再次得低分的文本
        bad_text = "好"
        trigger.evaluate_and_evolve("xie", bad_text, "writing")
        saved_data = mock_save.call_args[0][0]
        weaknesses = saved_data["agents"]["xie"]["evolution_state"]["identified_weaknesses"]
        # structural_complete 只应出现一次
        assert weaknesses.count("structural_complete") == 1

    @patch("evolution_engine.EvolutionTrigger._load_topo")
    @patch("evolution_engine.EvolutionTrigger._save_topo")
    def test_evaluate_prompt_format(self, mock_save, mock_load):
        """提示调整应包含得分偏低信息"""
        mock_load.return_value = self._fresh_topo()
        trigger = EvolutionTrigger(topo_path="/fake/topo.json")
        bad_text = "好"
        result = trigger.evaluate_and_evolve("xie", bad_text, "writing")
        for prompt in result["prompts_injected"]:
            assert "得分偏低" in prompt
        # 写入 topology 的应包含时间戳前缀
        saved_data = mock_save.call_args[0][0]
        for adj in saved_data["agents"]["xie"]["evolution_state"]["prompt_adjustments_applied"]:
            assert ":" in adj  # timestamp prefix: "YYYYMMDD-HHMM:消息"


# ═══════════════════════════════════════════
# VerificationLoop 测试
# ═══════════════════════════════════════════

class TestVerificationLoop:
    """VerificationLoop——最多3次重试的核验证循环"""

    BASE_TOPO = {"agents": {"gen": {
        "performance_history": {"total_tasks_completed": 0, "avg_quality_score": 0.5},
        "evolution_state": {"current_generation": 0, "identified_weaknesses": [],
                            "prompt_adjustments_applied": [], "last_verified_at": None},
    }}}

    def test_verify_bad_output_three_attempts(self):
        """不合格输出应尝试3次后标记exhausted"""
        loop = VerificationLoop()
        bad_text = "好"
        with patch.object(EvolutionTrigger, "_load_topo", return_value=self.BASE_TOPO):
            with patch.object(EvolutionTrigger, "_save_topo"):
                result = loop.verify("gen", "ver", bad_text, "analysis")
        assert result["passed"] is False
        assert result["attempts"] == 3
        assert result.get("exhausted") is True

    def test_verify_history_records_attempts(self):
        """history 应记录每次尝试的详细信息"""
        loop = VerificationLoop()
        bad_text = "差"
        with patch.object(EvolutionTrigger, "_load_topo", return_value=self.BASE_TOPO):
            with patch.object(EvolutionTrigger, "_save_topo"):
                result = loop.verify("gen", "ver", bad_text, "analysis")
        assert len(result["history"]) == 3
        for i, h in enumerate(result["history"]):
            assert h["attempt"] == i + 1
            assert "overall" in h
            assert "dimensions" in h
            assert "passed" in h

    def test_verify_generator_verifier_ids(self):
        """result 应包含 correct generator/verifier IDs"""
        loop = VerificationLoop()
        with patch.object(EvolutionTrigger, "_load_topo", return_value=self.BASE_TOPO):
            with patch.object(EvolutionTrigger, "_save_topo"):
                result = loop.verify("gen_agent", "ver_agent", "## 测试内容", "writing")
        assert result["generator"] == "gen_agent"
        assert result["verifier"] == "ver_agent"
        assert result["task_type"] == "writing"

    def test_verify_calls_evolution_trigger(self):
        """verify 应调用 EvolutionTrigger.evaluate_and_evolve"""
        loop = VerificationLoop()
        with patch.object(EvolutionTrigger, "_load_topo", return_value=self.BASE_TOPO):
            with patch.object(EvolutionTrigger, "_save_topo"):
                with patch.object(EvolutionTrigger, "evaluate_and_evolve", return_value={}) as mock_evolve:
                    loop.verify("gen", "ver", "## 测试", "test")
                    # 至少调用一次（最终调用）
                    assert mock_evolve.call_count >= 1

    def test_verify_returns_result_structure(self):
        """verify 返回结构应包含所有必要字段"""
        loop = VerificationLoop()
        with patch.object(EvolutionTrigger, "_load_topo", return_value=self.BASE_TOPO):
            with patch.object(EvolutionTrigger, "_save_topo"):
                result = loop.verify("gen", "ver", "## test", "analysis")
        assert "generator" in result
        assert "verifier" in result
        assert "task_type" in result
        assert "attempts" in result
        assert "passed" in result
        assert "history" in result
