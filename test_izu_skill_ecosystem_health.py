"""
Tests for izu_skill_ecosystem_health.py — metadata, is_user_skill, auto_fix_skill,
run_scan_and_fix, generate_dashboard, save_report, check_hermes_version

All tests use mock file I/O — no real filesystem dependencies.
No dependency on spacy or playwright.
Strategy: patch module-level Path variables with MagicMock since PosixPath
doesn't allow attribute patching directly (C-extension).
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open

from izu_skill_ecosystem_health import (
    get_skill_metadata_from_content,
    is_user_skill,
    auto_fix_skill,
    run_scan_and_fix,
    generate_dashboard,
    save_report,
    check_hermes_version,
    IZU_DIR, OUTPUT_DIR,
    AUTO_FIX_RULES,
)


# ═══════════════════════════════════════════
# get_skill_metadata_from_content 测试
# ═══════════════════════════════════════════

class TestGetSkillMetadata:
    """get_skill_metadata_from_content(content) -> metadata dict"""

    def test_with_full_frontmatter(self):
        """完整frontmatter应有所有字段"""
        content = """---
name: test-skill
date: 2026-01-15
version: 1.0.0
tags: [python, tools]
---
# Test Skill
## 功能
Some description
"""
        meta = get_skill_metadata_from_content(content)
        assert meta['has_date'] is True
        assert meta['has_version'] is True
        assert meta['has_tags'] is True
        assert meta['has_frontmatter'] is True
        assert meta['has_description'] is True

    def test_no_frontmatter(self):
        """无frontmatter时"""
        content = "# Just a title\n\nSome content"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_frontmatter'] is False
        assert meta['has_date'] is False
        assert meta['has_version'] is False

    def test_empty_frontmatter(self):
        """frontmatter为空"""
        content = "---\n---\nbody"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_frontmatter'] is True
        assert meta['has_date'] is False
        assert meta['has_version'] is False

    def test_partial_frontmatter_date_only(self):
        """只有date字段"""
        content = "---\ndate: 2026-03-20\n---\nbody"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_date'] is True
        assert meta['has_version'] is False
        assert meta['has_tags'] is False

    def test_description_in_body(self):
        """description在body前500字符内"""
        content = "---\ndate: 2026-01-01\n---\n## 功能\nThis skill does X"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_description'] is True

    def test_no_description(self):
        """无描述时has_description为False"""
        content = "---\ndate: 2026-01-01\n---\n## Usage\njust a command"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_description'] is False

    def test_version_with_quotes(self):
        """version字段可带引号"""
        content = '---\nversion: "2.0"\n---\nbody'
        meta = get_skill_metadata_from_content(content)
        assert meta['has_version'] is True

    def test_invalid_date_format(self):
        """非202x开头的日期不算有效date"""
        content = "---\ndate: 2019-01-01\n---\nbody"
        meta = get_skill_metadata_from_content(content)
        assert meta['has_date'] is False


# ═══════════════════════════════════════════
# is_user_skill 测试
# ═══════════════════════════════════════════

class TestIsUserSkill:
    """is_user_skill(content) -> bool"""

    def test_no_frontmatter_not_user_skill(self):
        """无frontmatter的skill不算用户自定义（源码头部return False）"""
        content = "# Bare skill\nsome content"
        assert is_user_skill(content) is False

    def test_homepage_external(self):
        """有homepage字段的不是用户skill"""
        content = """---
name: web-search
homepage: https://example.com
---
"""
        assert is_user_skill(content) is False

    def test_hermes_metadata_external(self):
        """metadata含hermes的不是用户skill"""
        content = """---
name: my-skill
metadata: hermes/tool
---
"""
        assert is_user_skill(content) is False

    def test_openclaw_metadata_external(self):
        """metadata含openclaw的不是用户skill"""
        content = """---
name: my-skill
metadata: openclaw/1.0
---
"""
        assert is_user_skill(content) is False

    def test_author_hermes_external(self):
        """author为Hermes的不是用户skill"""
        content = """---
name: my-skill
author: Hermes Agent
---
"""
        assert is_user_skill(content) is False

    def test_plugin_external(self):
        """有plugin字段的不是用户skill"""
        content = """---
name: my-skill
plugin: some-plugin
---
"""
        assert is_user_skill(content) is False

    def test_compatibility_external(self):
        """有compatibility字段的不是用户skill"""
        content = """---
name: my-skill
compatibility: hermes-1.0
---
"""
        assert is_user_skill(content) is False

    def test_user_skill_with_plain_frontmatter(self):
        """纯用户skill不应被误判为外部"""
        content = """---
name: my-tool
date: 2026-01-15
version: 1.0.0
---
Some user-defined tool content
"""
        assert is_user_skill(content) is True


# ═══════════════════════════════════════════
# auto_fix_skill 测试
# ═══════════════════════════════════════════

class TestAutoFixSkill:
    """auto_fix_skill(path, content, issues) -> (success, message)"""

    def test_no_frontmatter_skip(self):
        """无frontmatter的skill跳过修复"""
        succ, msg = auto_fix_skill("/fake/path", "# No frontmatter", [])
        assert succ is False
        assert "跳过" in msg

    def test_external_skill_skip(self):
        """外部skill跳过修复"""
        content = """---
name: ext
homepage: https://x.com
---
body
"""
        succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is False
        assert "外部" in msg

    def test_missing_date_added(self):
        """缺失date字段应补充"""
        content = """---
name: my-skill
version: 1.0.0
---
body
"""
        with patch("pathlib.Path.rename"), patch("pathlib.Path.write_text") as wt:
            succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is True
        assert "date" in msg

    def test_missing_version_added(self):
        """缺失version字段应补充"""
        content = """---
name: my-skill
date: 2026-01-15
---
body
"""
        with patch("pathlib.Path.rename"), patch("pathlib.Path.write_text") as wt:
            succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is True
        assert "version" in msg

    def test_both_missing_added(self):
        """同时缺失date和version"""
        content = """---
name: my-skill
description: A tool
---
body
"""
        with patch("pathlib.Path.rename"), patch("pathlib.Path.write_text") as wt:
            succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is True
        assert "date" in msg
        assert "version" in msg

    def test_nothing_missing_no_change(self):
        """date和version都存在时无需修改"""
        content = """---
name: my-skill
date: 2026-01-15
version: 1.0.0
---
body
"""
        with patch("pathlib.Path.rename"), patch("pathlib.Path.write_text"):
            succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is False
        assert "无需修改" in msg

    def test_backup_created_before_write(self):
        """修复前创建.bak备份"""
        content = """---
name: my-skill
---
body
"""
        mock_rename = MagicMock()
        with (
            patch("pathlib.Path.rename", mock_rename),
            patch("pathlib.Path.write_text"),
        ):
            succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is True
        mock_rename.assert_called_once()

    def test_malformed_frontmatter(self):
        """frontmatter格式异常"""
        content = """---
name: bad
-  only one dash
"""
        succ, msg = auto_fix_skill("/fake/path", content, [])
        assert succ is False
        assert "格式异常" in msg or "跳过" in msg


# ═══════════════════════════════════════════
# run_scan_and_fix 测试
# ═══════════════════════════════════════════

class TestRunScanAndFix:
    """run_scan_and_fix(auto_fix) -> report dict"""

    @patch("izu_skill_ecosystem_health.scan_all")
    def test_scan_summary_counts(self, mock_scan_all):
        """报告应包含各等级计数"""
        mock_scan_all.return_value = [
            {"name": "s1", "path": "/f1", "overall": 0.90},
            {"name": "s2", "path": "/f2", "overall": 0.75},
            {"name": "s3", "path": "/f3", "overall": 0.60},
            {"name": "s4", "path": "/f4", "overall": 0.40},
        ]
        report = run_scan_and_fix(auto_fix=False)
        assert report['total'] == 4
        assert report['excellent'] == 1  # >=0.85
        assert report['good'] == 1       # 0.70-0.85
        assert report['fair'] == 1       # 0.50-0.70
        assert report['poor'] == 1       # <0.50
        assert report['avg'] == pytest.approx(0.662, 0.01)

    @patch("izu_skill_ecosystem_health.scan_all")
    def test_top_and_bottom_skills(self, mock_scan_all):
        """报告应列出最优和最差skills"""
        mock_scan_all.return_value = [
            {"name": f"skill-{i}", "path": f"/f{i}", "overall": i / 10}
            for i in range(0, 10)  # 0.0, 0.1, ..., 0.9
        ]
        report = run_scan_and_fix(auto_fix=False)
        assert len(report['top_skills']) == 5
        assert report['top_skills'][0] == "skill-9"
        assert len(report['bottom_skills']) == 5
        assert report['bottom_skills'][0] == "skill-0"

    @patch("izu_skill_ecosystem_health.scan_all")
    def test_auto_fix_runs_on_low_skills(self, mock_scan_all):
        """auto_fix=True时应自动修正低分skills"""
        mock_scan_all.return_value = [
            {"name": "low", "path": "/f1", "overall": 0.50},
            {"name": "high", "path": "/f2", "overall": 0.90},
        ]

        with patch("pathlib.Path.read_text", return_value="---\nname: low\n---\nbody"), \
             patch("izu_skill_ecosystem_health.auto_fix_skill", return_value=(True, "已补 date")):
            report = run_scan_and_fix(auto_fix=True)

        assert len(report['auto_fixed']) == 1
        assert "low" in report['auto_fixed'][0]
        assert len(report['auto_fix_failed']) == 0

    @patch("izu_skill_ecosystem_health.scan_all")
    def test_auto_fix_skips_high_scores(self, mock_scan_all):
        """auto_fix=True时高分skills跳过"""
        mock_scan_all.return_value = [
            {"name": "good", "path": "/f1", "overall": 0.95},
        ]
        report = run_scan_and_fix(auto_fix=True)
        assert len(report['auto_fixed']) == 0

    @patch("izu_skill_ecosystem_health.scan_all")
    def test_single_skill_edge_case(self, mock_scan_all):
        """只有一个skill的情况"""
        mock_scan_all.return_value = [
            {"name": "only", "path": "/f1", "overall": 0.80},
        ]
        report = run_scan_and_fix(auto_fix=False)
        assert report['total'] == 1
        assert report['avg'] == 0.80


# ═══════════════════════════════════════════
# generate_dashboard 测试
# ═══════════════════════════════════════════

class TestGenerateDashboard:
    """generate_dashboard(report) -> dashboard string"""

    SAMPLE_REPORT = {
        'timestamp': '2026-01-15T10:00:00',
        'total': 10,
        'excellent': 5,
        'good': 3,
        'fair': 1,
        'poor': 1,
        'avg': 0.78,
        'bottom_skills': ['poor-skill'],
        'top_skills': ['best-skill', 'good-skill'],
        'auto_fixed': ['fixed-skill: done'],
        'auto_fix_failed': [],
    }

    def test_dashboard_contains_header(self):
        """看板应包含标题和skills总数"""
        dashboard = generate_dashboard(self.SAMPLE_REPORT)
        assert "Skill生态健康看板" in dashboard
        assert "10个skills" in dashboard

    def test_dashboard_has_levels(self):
        """看板包含等级分布"""
        dashboard = generate_dashboard(self.SAMPLE_REPORT)
        assert "≥0.85" in dashboard
        assert "0.70-0.85" in dashboard
        assert "0.50-0.70" in dashboard
        assert "<0.50" in dashboard

    def test_dashboard_with_poor_skills_shows_warning(self):
        """有低分skills时显示待关注"""
        report = {
            'timestamp': '', 'total': 2, 'excellent': 0, 'good': 0,
            'fair': 1, 'poor': 1, 'avg': 0.4,
            'bottom_skills': ['bad-skill'],
            'top_skills': [],
            'auto_fixed': [],
            'auto_fix_failed': [],
        }
        dashboard = generate_dashboard(report)
        assert "需要关注" in dashboard
        assert "bad-skill" in dashboard

    def test_dashboard_all_healthy(self):
        """全高分时显示全部健康"""
        report = {
            'timestamp': '', 'total': 3, 'excellent': 3, 'good': 0,
            'fair': 0, 'poor': 0, 'avg': 0.95,
            'bottom_skills': [],
            'top_skills': ['top1', 'top2'],
            'auto_fixed': [],
            'auto_fix_failed': [],
        }
        dashboard = generate_dashboard(report)
        assert "全部skills在健康区" in dashboard

    def test_dashboard_shows_top_skills(self):
        """看板显示最佳实践skills"""
        dashboard = generate_dashboard(self.SAMPLE_REPORT)
        assert "最佳实践" in dashboard
        assert "best-skill" in dashboard
        assert "good-skill" in dashboard

    def test_dashboard_shows_auto_fixes(self):
        """有自动修正时显示修正记录"""
        dashboard = generate_dashboard(self.SAMPLE_REPORT)
        assert "自动修正" in dashboard
        assert "fixed-skill" in dashboard

    def test_dashboard_bar_chart_width(self):
        """柱状图字符数与比例一致"""
        report = dict(self.SAMPLE_REPORT)
        report['total'] = 10
        report['excellent'] = 10
        report['good'] = 0
        report['fair'] = 0
        report['poor'] = 0
        dashboard = generate_dashboard(report)
        lines = dashboard.split('\n')
        excellent_line = [l for l in lines if '≥0.85' in l][0]
        assert '█' in excellent_line


# ═══════════════════════════════════════════
# save_report 测试
# ═══════════════════════════════════════════

class TestSaveReport:
    """save_report(report, dashboard) -> (report_path, dashboard_path)"""

    SAMPLE_REPORT = {
        'timestamp': '2026-01-15T10:00:00',
        'total': 5, 'excellent': 2, 'good': 2, 'fair': 1, 'poor': 0,
        'avg': 0.82,
        'bottom_skills': ['low'],
        'top_skills': ['high'],
        'auto_fixed': ['fixed-1: done'],
        'auto_fix_failed': [],
    }

    def test_save_report_creates_output_dir(self):
        """保存报告时创建输出目录"""
        mock_out_dir = MagicMock(spec=Path)
        with (
            patch('izu_skill_ecosystem_health.OUTPUT_DIR', mock_out_dir),
            patch('pathlib.Path.write_text'),
        ):
            save_report(self.SAMPLE_REPORT, "dashboard content")
        mock_out_dir.mkdir.assert_called_once()

    def test_save_report_writes_markdown(self):
        """生成md报告文件"""
        mock_report_path = MagicMock()
        mock_dash_path = MagicMock()
        mock_out_dir = MagicMock(spec=Path)
        mock_out_dir.__truediv__.side_effect = [mock_report_path, mock_dash_path]

        with (
            patch('izu_skill_ecosystem_health.OUTPUT_DIR', mock_out_dir),
        ):
            save_report(self.SAMPLE_REPORT, "dashboard content")

        # Verify write_text was called on both paths
        mock_report_path.write_text.assert_called_once()
        call_args = mock_report_path.write_text.call_args[0][0]
        assert "Skill Ecosystem Health Report" in call_args
        assert "fixed-1" in call_args

    def test_save_report_writes_dashboard_txt(self):
        """生成dashboard文本文件"""
        mock_report_path = MagicMock()
        mock_dash_path = MagicMock()
        mock_out_dir = MagicMock(spec=Path)
        mock_out_dir.__truediv__.side_effect = [mock_report_path, mock_dash_path]

        with (
            patch('izu_skill_ecosystem_health.OUTPUT_DIR', mock_out_dir),
        ):
            save_report(self.SAMPLE_REPORT, "dashboard text content")

        mock_dash_path.write_text.assert_called_once_with("dashboard text content", encoding='utf-8')

    def test_save_report_returns_paths(self):
        """返回(report_path, dashboard_path)元组"""
        mock_report_path = MagicMock()
        mock_dash_path = MagicMock()
        mock_out_dir = MagicMock(spec=Path)
        mock_out_dir.__truediv__.side_effect = [mock_report_path, mock_dash_path]

        with (
            patch('izu_skill_ecosystem_health.OUTPUT_DIR', mock_out_dir),
        ):
            rp, dp = save_report(self.SAMPLE_REPORT, "dash")

        assert rp is mock_report_path
        assert dp is mock_dash_path

    def test_save_report_empty_auto_fixed(self):
        """auto_fixed为空时不应报错"""
        report = dict(self.SAMPLE_REPORT)
        report['auto_fixed'] = []

        mock_report_path = MagicMock()
        mock_dash_path = MagicMock()
        mock_out_dir = MagicMock(spec=Path)
        mock_out_dir.__truediv__.side_effect = [mock_report_path, mock_dash_path]

        with (
            patch('izu_skill_ecosystem_health.OUTPUT_DIR', mock_out_dir),
        ):
            rp, dp = save_report(report, "dash")
        assert rp is mock_report_path


# ═══════════════════════════════════════════
# check_hermes_version 测试
# ═══════════════════════════════════════════

class TestCheckHermesVersion:
    """check_hermes_version() -> version dict"""

    def test_version_success(self):
        """执行成功时返回版本信息"""
        mock_result = MagicMock()
        mock_result.stdout = "Hermes Agent v2.0.0\n"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            result = check_hermes_version()
        assert result['version'] == "Hermes Agent v2.0.0"
        assert 'checked_at' in result

    def test_version_fallback_on_error(self):
        """执行失败时返回unknown"""
        with patch("subprocess.run", side_effect=FileNotFoundError("no hermes")):
            result = check_hermes_version()
        assert result['version'] == "unknown"

    def test_version_fallback_on_timeout(self):
        """超时时返回unknown"""
        with patch("subprocess.run", side_effect=TimeoutError("timeout")):
            result = check_hermes_version()
        assert result['version'] == "unknown"

    def test_version_uses_stderr_fallback(self):
        """stdout为空时使用stderr"""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Hermes v1.0"

        with patch("subprocess.run", return_value=mock_result):
            result = check_hermes_version()
        assert result['version'] == "Hermes v1.0"
