"""Tests for izu_skill_scorer.py — find_all_skills, score_skill, scan_all, generate_report"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from izu_skill_scorer import (
    find_all_skills, score_skill, scan_all,
    print_results, generate_report,
    SKILLS_USER_DIR,
)


# ═══════════════════════════════════════════
# find_all_skills 测试
# ═══════════════════════════════════════════

class TestFindAllSkills:
    def test_no_skills_dir(self):
        """不存在的目录应返回空列表"""
        skills = find_all_skills(Path("/nonexistent/skills"))
        assert skills == []

    def test_skip_archive(self, tmp_path):
        """.archive 目录下的 SKILL.md 应被排除"""
        root = tmp_path / "skills"
        (root / "test-skill").mkdir(parents=True)
        (root / "test-skill" / "SKILL.md").write_text("# Test Skill\nContent")

        archive = root / ".archive" / "old-skill"
        archive.mkdir(parents=True)
        (archive / "SKILL.md").write_text("# Old Skill\nOld content")

        skills = find_all_skills(root, exclude_archive=True)
        names = [s["name"] for s in skills]
        assert "test-skill" in names
        assert "old-skill" not in names

    def test_include_archive(self, tmp_path):
        """exclude_archive=False 时应包含 .archive 下的文件"""
        root = tmp_path / "skills"
        (root / "active").mkdir(parents=True)
        (root / "active" / "SKILL.md").write_text("# Active")

        archive = root / ".archive" / "retired"
        archive.mkdir(parents=True)
        (archive / "SKILL.md").write_text("# Retired")

        skills = find_all_skills(root, exclude_archive=False)
        assert len(skills) == 2

    def test_nested_directory_category(self, tmp_path):
        """嵌套目录中的 SKILL.md 应使用上级目录名作为 category"""
        root = tmp_path / "skills"
        (root / "research" / "paper-reader").mkdir(parents=True)
        (root / "research" / "paper-reader" / "SKILL.md").write_text("# Paper Reader")

        skills = find_all_skills(root)
        assert len(skills) == 1
        assert skills[0]["name"] == "paper-reader"
        # research 不是 'root' 也不是 'skills'
        assert skills[0]["category"] == "research"

    def test_multiple_skills_in_subdirs(self, tmp_path):
        """多个子目录中的 SKILL.md 都应被发现"""
        root = tmp_path / "skills"
        for name in ["skill-a", "skill-b", "skill-c"]:
            (root / name).mkdir(parents=True)
            (root / name / "SKILL.md").write_text(f"# {name}")

        skills = find_all_skills(root)
        assert len(skills) == 3
        names = [s["name"] for s in skills]
        assert "skill-a" in names and "skill-b" in names and "skill-c" in names

    def test_skill_metadata(self, tmp_path):
        """每条 skill 应有正确的 metadata"""
        root = tmp_path / "skills"
        (root / "my-skill").mkdir(parents=True)
        content = "# My Skill\n\nDescription\n\nUsage\n"
        (root / "my-skill" / "SKILL.md").write_text(content)

        skills = find_all_skills(root)
        s = skills[0]
        assert s["name"] == "my-skill"
        assert s["content"] == content
        assert s["lines"] == len(content.split("\n"))
        assert s["path"].endswith("SKILL.md")
        assert "category" in s

    def test_read_encoding_fallback(self, tmp_path):
        """read_text 失败时应有 fallback"""
        root = tmp_path / "skills"
        (root / "buggy").mkdir(parents=True)
        (root / "buggy" / "SKILL.md").write_text("# Buggy")

        with patch.object(Path, "read_text", side_effect=[UnicodeDecodeError("utf-8", b"", 0, 1, "bad"), "# Buggy"]):
            skills = find_all_skills(root)
            assert len(skills) == 1


# ═══════════════════════════════════════════
# score_skill 测试（mock Verifier）
# ═══════════════════════════════════════════

class TestScoreSkill:
    @patch("izu_skill_scorer.Verifier")
    def test_basic_scoring(self, mock_verifier_cls):
        """skip_url_check=True 时使用手动评分"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier

        # 模拟 Verifier 方法返回固定值
        mock_verifier.check_structure.return_value = {"score": 0.9, "found": ["##", "###"], "missing": [], "bonus": 0.2}
        mock_verifier.check_citations.return_value = {"score": 0.8, "citations": 1, "links": 1}
        mock_verifier.check_consistency.return_value = {"score": 1.0, "issues": []}
        mock_verifier.check_conciseness.return_value = {"score": 0.7, "total_chars": 200, "sentences": 5, "avg_len": 40.0}

        skill = {
            "name": "test-skill",
            "category": "root",
            "path": "/fake/skills/test-skill/SKILL.md",
            "content": "# Test\n\nDescription\n\nUsage\n\n```python\nx=1\n```",
            "lines": 10,
        }

        result = score_skill(skill, skip_url_check=True)
        assert result["name"] == "test-skill"
        assert result["category"] == "root"
        # overall = 0.8*0.20 + 0.9*0.20 + 0.8*0.15 + 1.0*0.20 + 0.7*0.15
        #         = 0.16 + 0.18 + 0.12 + 0.20 + 0.105 = 0.765
        assert result["overall"] == pytest.approx(0.765, abs=0.002)
        assert result["dimensions"]["structural_complete"] == 0.9

    @patch("izu_skill_scorer.Verifier")
    def test_has_frontmatter_true(self, mock_verifier_cls):
        """有 YAML frontmatter 时应检测到"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier
        for m in ["check_structure", "check_citations", "check_consistency", "check_conciseness"]:
            getattr(mock_verifier, m).return_value = {"score": 0.8}

        content = "---\ntags: [test, skill]\ndate: 2026-01-15\nversion: 1.0.0\n---\n# Test\nCore mission: test\n"
        skill = {"name": "fm", "category": "root", "path": "/fake/SKILL.md", "content": content, "lines": 8}
        result = score_skill(skill, skip_url_check=True)
        assert result["extras"]["has_frontmatter"] is True
        assert result["extras"]["has_tags"] is True
        assert result["extras"]["has_date"] is True
        assert result["extras"]["has_version"] is True
        assert result["extras"]["has_description"] is True

    @patch("izu_skill_scorer.Verifier")
    def test_no_frontmatter(self, mock_verifier_cls):
        """无 frontmatter 时相关 extras 应为 False"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier
        for m in ["check_structure", "check_citations", "check_consistency", "check_conciseness"]:
            getattr(mock_verifier, m).return_value = {"score": 0.8}

        skill = {"name": "nofm", "category": "root", "path": "/fake/SKILL.md", "content": "# Just a title", "lines": 3}
        result = score_skill(skill, skip_url_check=True)
        assert result["extras"]["has_frontmatter"] is False
        assert result["extras"]["has_tags"] is False

    @patch("izu_skill_scorer.Verifier")
    def test_has_code_example(self, mock_verifier_cls):
        """含代码块时应检测到"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier
        for m in ["check_structure", "check_citations", "check_consistency", "check_conciseness"]:
            getattr(mock_verifier, m).return_value = {"score": 0.8}

        skill = {"name": "code", "category": "root", "path": "/fake/SKILL.md",
                 "content": "# Test\n```python\nprint('hi')\n```", "lines": 5}
        result = score_skill(skill, skip_url_check=True)
        assert result["extras"]["has_code_example"] is True

    @patch("izu_skill_scorer.Verifier")
    def test_expected_sections_for_long_skill(self, mock_verifier_cls):
        """长技能(>50行)应添加额外预期段落"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier
        mock_verifier.check_structure.return_value = {"score": 0.8, "found": ["##"], "missing": [], "bonus": 0.0}

        long_content = "\n".join([f"Line {i}" for i in range(60)])
        skill = {"name": "long", "category": "root", "path": "/fake/SKILL.md",
                 "content": long_content, "lines": 60}
        score_skill(skill, skip_url_check=True)

        # 应传入包含 SKILL_EXPECTED_IF_LONG 的 expected_sections
        call_kwargs = mock_verifier.check_structure.call_args
        assert call_kwargs is not None
        expected = call_kwargs[1].get("expected_sections", [])
        assert "用法" in expected or "Usage" in expected

    @patch("izu_skill_scorer.Verifier")
    @patch("izu_skill_scorer.Scorer")
    def test_no_skip_url_check(self, mock_scorer_cls, mock_verifier_cls):
        """skip_url_check=False 时应使用 Scorer.score_output"""
        mock_scorer = MagicMock()
        mock_scorer_cls.return_value = mock_scorer
        mock_scorer.score_output.return_value = {
            "url_validity": {"score": 0.9},
            "structural_complete": {"score": 0.8},
            "citation_accuracy": {"score": 0.7},
            "consistency": {"score": 0.85},
            "conciseness": {"score": 0.75},
            "_overall": 0.805,
        }

        skill = {"name": "test", "category": "root", "path": "/fake/SKILL.md",
                 "content": "# Test", "lines": 3}
        result = score_skill(skill, skip_url_check=False)
        assert result["overall"] == pytest.approx(0.805, abs=0.002)
        mock_scorer.score_output.assert_called_once()

    @patch("izu_skill_scorer.Verifier")
    def test_extras_description_check(self, mock_verifier_cls):
        """描述检查应匹配中英文关键词"""
        mock_verifier = MagicMock()
        mock_verifier_cls.return_value = mock_verifier
        for m in ["check_structure", "check_citations", "check_consistency", "check_conciseness"]:
            getattr(mock_verifier, m).return_value = {"score": 0.8}

        # 中文关键词
        skill_cn = {"name": "cn", "category": "root", "path": "/fake/SKILL.md",
                    "content": "# 测试\n功能：这是一个测试skill", "lines": 3}
        result_cn = score_skill(skill_cn, skip_url_check=True)
        assert result_cn["extras"]["has_description"] is True

        # 英文关键词
        skill_en = {"name": "en", "category": "root", "path": "/fake/SKILL.md",
                    "content": "# Test\nDescription: This is a test skill", "lines": 3}
        result_en = score_skill(skill_en, skip_url_check=True)
        assert result_en["extras"]["has_description"] is True

        # 无描述
        skill_no = {"name": "no", "category": "root", "path": "/fake/SKILL.md",
                    "content": "# Just a title", "lines": 3}
        result_no = score_skill(skill_no, skip_url_check=True)
        assert result_no["extras"]["has_description"] is False


# ═══════════════════════════════════════════
# scan_all 测试
# ═══════════════════════════════════════════

class TestScanAll:
    @patch("izu_skill_scorer.find_all_skills")
    @patch("izu_skill_scorer.score_skill")
    def test_scan_all_basic(self, mock_score, mock_find):
        """scan_all 应对所有 skill 评分并排序"""
        mock_find.return_value = [
            {"name": "skill-a", "category": "root", "path": "/a/SKILL.md", "content": "# A", "lines": 3},
            {"name": "skill-b", "category": "root", "path": "/b/SKILL.md", "content": "# B", "lines": 5},
        ]
        mock_score.side_effect = [
            {"name": "skill-a", "overall": 0.5, "dimensions": {}, "extras": {}, "details": {}},
            {"name": "skill-b", "overall": 0.9, "dimensions": {}, "extras": {}, "details": {}},
        ]
        results = scan_all()
        assert len(results) == 2
        # 默认按总分升序排列（低分在前）
        assert results[0]["overall"] == 0.5
        assert results[1]["overall"] == 0.9

    @patch("izu_skill_scorer.find_all_skills")
    @patch("izu_skill_scorer.score_skill")
    def test_scan_all_min_score_filter(self, mock_score, mock_find):
        """min_score>0 时应只返回低于阈值的 skill"""
        mock_find.return_value = [
            {"name": "low", "overall": 0.3, "content": "# Low", "lines": 2},
            {"name": "high", "overall": 0.8, "content": "# High", "lines": 2},
        ]
        mock_score.side_effect = [
            {"name": "low", "overall": 0.3, "dimensions": {}, "extras": {}, "details": {}},
            {"name": "high", "overall": 0.8, "dimensions": {}, "extras": {}, "details": {}},
        ]
        results = scan_all(min_score=0.7)
        assert len(results) == 1
        assert results[0]["name"] == "low"

    @patch("izu_skill_scorer.find_all_skills")
    @patch("izu_skill_scorer.score_skill")
    def test_scan_all_max_results(self, mock_score, mock_find):
        """max_results 应限制返回数量"""
        mock_find.return_value = [
            {"name": f"skill-{i}", "content": f"# {i}", "lines": 2} for i in range(5)
        ]
        mock_score.side_effect = [
            {"name": f"skill-{i}", "overall": 0.1 * (i + 1), "dimensions": {}, "extras": {}, "details": {}}
            for i in range(5)
        ]
        results = scan_all(max_results=2)
        assert len(results) == 2

    @patch("izu_skill_scorer.find_all_skills")
    @patch("izu_skill_scorer.score_skill")
    def test_scan_all_handles_exception(self, mock_score, mock_find):
        """评分失败时应跳过而非崩溃"""
        mock_find.return_value = [
            {"name": "good", "content": "# Good", "lines": 2},
            {"name": "bad", "content": "# Bad", "lines": 2},
        ]
        mock_score.side_effect = [
            {"name": "good", "overall": 0.9, "dimensions": {}, "extras": {}, "details": {}},
            Exception("评分失败"),
        ]
        results = scan_all()
        assert len(results) == 1
        assert results[0]["name"] == "good"


# ═══════════════════════════════════════════
# print_results 测试
# ═══════════════════════════════════════════

class TestPrintResults:
    def test_print_results_empty(self, capsys):
        """空结果应打印 '无结果'"""
        print_results([])
        captured = capsys.readouterr()
        assert "无结果" in captured.out

    def test_print_results_nonempty(self, capsys):
        """非空结果应打印表格"""
        results = [
            {
                "name": "test-skill", "category": "root", "overall": 0.85,
                "dimensions": {"url_validity": 0.9, "structural_complete": 0.8,
                               "citation_accuracy": 0.7, "consistency": 0.9, "conciseness": 0.8},
                "extras": {"has_frontmatter": True, "has_description": True,
                           "has_tags": True, "has_date": True, "has_version": True,
                           "has_code_example": True},
                "lines": 20,
            }
        ]
        print_results(results)
        captured = capsys.readouterr()
        assert "test-skill" in captured.out
        assert "🟢" in captured.out  # 0.85 >= 0.85

    def test_print_results_with_warnings(self, capsys):
        """缺少 extras 时应显示警告标记"""
        results = [
            {
                "name": "bad-skill", "category": "root", "overall": 0.6,
                "dimensions": {"url_validity": 0.5, "structural_complete": 0.5,
                               "citation_accuracy": 0.5, "consistency": 0.5, "conciseness": 0.5},
                "extras": {"has_frontmatter": False, "has_description": False,
                           "has_tags": False, "has_date": False, "has_version": False,
                           "has_code_example": False},
                "lines": 5,
            }
        ]
        print_results(results)
        captured = capsys.readouterr()
        assert "⚠️" in captured.out


# ═══════════════════════════════════════════
# generate_report 测试
# ═══════════════════════════════════════════

class TestGenerateReport:
    def test_generate_report(self, tmp_path):
        """generate_report 应写入有效的 markdown 文件"""
        results = [
            {"name": "top-skill", "category": "research", "overall": 0.92,
             "dimensions": {"url_validity": 0.9, "structural_complete": 0.95,
                            "citation_accuracy": 0.85, "consistency": 0.9, "conciseness": 0.8},
             "extras": {}, "lines": 30},
            {"name": "mid-skill", "category": "dev", "overall": 0.65,
             "dimensions": {"url_validity": 0.6, "structural_complete": 0.7,
                            "citation_accuracy": 0.5, "consistency": 0.6, "conciseness": 0.7},
             "extras": {}, "lines": 20},
        ]

        with patch("izu_skill_scorer.OUTPUT_DIR", tmp_path):
            report_path = generate_report(results)

        assert report_path.exists()
        content = report_path.read_text()
        assert "SKILL健康扫描报告" in content
        assert "top-skill" in content
        assert "mid-skill" in content
        assert "0.92" in content
        assert "0.65" in content

    def test_generate_report_no_results(self, tmp_path):
        """空结果应生成包含 basic 信息的报告"""
        with patch("izu_skill_scorer.OUTPUT_DIR", tmp_path):
            report_path = generate_report([])
        assert report_path.exists()
        content = report_path.read_text()
        assert "0 个skills" in content or "0个" in content
