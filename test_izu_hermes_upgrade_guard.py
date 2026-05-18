"""Tests for izu_hermes_upgrade_guard.py — get_hermes_version, snapshot_skill_structure,
snapshot_config, do_snapshot, do_check, build_check_report"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
from datetime import datetime

from izu_hermes_upgrade_guard import (
    get_hermes_version, snapshot_skill_structure, snapshot_config,
    do_snapshot, do_check, build_check_report, SNAPSHOT_FILE,
    SKILLS_DIR, IZU_DIR, OUTPUT_DIR
)


# ═══════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════

FIXED_DT = datetime(2025, 1, 15, 10, 30, 0)


def _make_sortable_skill_mock(name, path_str, extra_fields=None):
    """Create a MagicMock Path that supports sorted() by name"""
    m = MagicMock(spec=Path)
    m.name = name
    m.read_text.return_value = extra_fields.get("content", "content") if extra_fields else "content"
    # stat
    stat = MagicMock()
    stat.st_size = extra_fields.get("size", 100) if extra_fields else 100
    stat.st_mtime = extra_fields.get("mtime", 100.0) if extra_fields else 100.0
    m.stat.return_value = stat
    # str()
    m.configure_mock(**{'__str__.return_value': path_str})
    # Support sorted() via __lt__
    def lt(self, other):
        return self.name < other.name
    m.__lt__ = lt
    return m


# ═══════════════════════════════════════════
# get_hermes_version 测试
# ═══════════════════════════════════════════

class TestGetHermesVersion:
    """get_hermes_version 函数测试"""

    @patch("izu_hermes_upgrade_guard.subprocess.run")
    def test_version_success(self, mock_run):
        """hermes --version 成功时应返回版本号"""
        mock_run.return_value.stdout = "v2.0.0\n"
        mock_run.return_value.stderr = ""
        assert get_hermes_version() == "v2.0.0"

    @patch("izu_hermes_upgrade_guard.subprocess.run")
    def test_version_from_stderr(self, mock_run):
        """版本信息在 stderr 时也应正确返回"""
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "v1.5.0"
        assert get_hermes_version() == "v1.5.0"

    @patch("izu_hermes_upgrade_guard.subprocess.run")
    def test_version_command_timeout(self, mock_run):
        """超时异常时应返回 'unknown'"""
        mock_run.side_effect = Exception("timeout")
        assert get_hermes_version() == "unknown"

    @patch("izu_hermes_upgrade_guard.subprocess.run")
    def test_version_empty_output(self, mock_run):
        """输出全空时应返回 'unknown'"""
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        assert get_hermes_version() == "unknown"


# ═══════════════════════════════════════════
# snapshot_skill_structure 测试
# ═══════════════════════════════════════════

class TestSnapshotSkillStructure:
    """snapshot_skill_structure 函数测试"""

    @patch("izu_hermes_upgrade_guard.SKILLS_DIR")
    def test_no_skills(self, mock_skills_dir):
        """无SKILL.md文件时应返回空字典"""
        mock_skills_dir.rglob.return_value = []
        assert snapshot_skill_structure() == {}

    @patch("izu_hermes_upgrade_guard.SKILLS_DIR")
    def test_skill_with_frontmatter(self, mock_skills_dir):
        """含frontmatter的SKILL.md应正确提取字段"""
        skill_md = _make_sortable_skill_mock(
            "SKILL.md",
            "/home/user/.hermes/skills/test-skill/SKILL.md",
            {"size": 500, "mtime": 1000.0, "content": "---\nname: test-skill\nversion: 1.0\n---\n\nContent here"}
        )
        mock_skills_dir.rglob.return_value = [skill_md]

        result = snapshot_skill_structure()
        assert len(result) == 1
        path_key = "/home/user/.hermes/skills/test-skill/SKILL.md"
        info = result[path_key]
        assert info["size"] == 500
        assert info["frontmatter_fields"] == ["name", "version"]
        # "---\nname: test-skill\nversion: 1.0\n---\n\nContent here" → 6 lines
        assert info["lines"] == 6

    @patch("izu_hermes_upgrade_guard.SKILLS_DIR")
    def test_skill_without_frontmatter(self, mock_skills_dir):
        """不含frontmatter的SKILL.md应有空字段列表"""
        skill_md = _make_sortable_skill_mock(
            "SKILL.md",
            "/home/user/.hermes/skills/simple/SKILL.md",
            {"size": 200, "mtime": 2000.0, "content": "Just content without frontmatter"}
        )
        mock_skills_dir.rglob.return_value = [skill_md]

        result = snapshot_skill_structure()
        info = result["/home/user/.hermes/skills/simple/SKILL.md"]
        assert info["frontmatter_fields"] == []

    @patch("izu_hermes_upgrade_guard.SKILLS_DIR")
    def test_skill_with_archive_skipped(self, mock_skills_dir):
        """.archive 目录下的SKILL.md应被跳过"""
        skill_md = _make_sortable_skill_mock(
            "SKILL.md",
            "/home/user/.hermes/skills/.archive/old/SKILL.md"
        )
        mock_skills_dir.rglob.return_value = [skill_md]

        result = snapshot_skill_structure()
        assert result == {}

    @patch("izu_hermes_upgrade_guard.SKILLS_DIR")
    def test_multiple_skills(self, mock_skills_dir):
        """多个SKILL.md应全部被记录（按名称排序）"""
        skill1 = _make_sortable_skill_mock(
            "SKILL.md", "/home/user/.hermes/skills/a/SKILL.md"
        )
        skill2 = _make_sortable_skill_mock(
            "SKILL.md", "/home/user/.hermes/skills/b/SKILL.md"
        )
        mock_skills_dir.rglob.return_value = [skill1, skill2]

        result = snapshot_skill_structure()
        assert len(result) == 2


# ═══════════════════════════════════════════
# snapshot_config 测试
# ═══════════════════════════════════════════

class TestSnapshotConfig:
    """snapshot_config 函数测试"""

    @patch("izu_hermes_upgrade_guard.Path.home")
    def test_config_exists(self, mock_home):
        """config.yaml 存在时应返回 mtime 和 size"""
        config_yaml = MagicMock(spec=Path)
        config_yaml.exists.return_value = True
        config_yaml.stat.return_value.st_mtime = 1234.0
        config_yaml.stat.return_value.st_size = 5678

        home_path = MagicMock(spec=Path)
        home_path.__truediv__.return_value.__truediv__.return_value = config_yaml
        mock_home.return_value = home_path

        result = snapshot_config()
        assert result["config_mtime"] == 1234.0
        assert result["config_size"] == 5678

    @patch("izu_hermes_upgrade_guard.Path.home")
    def test_config_not_exists(self, mock_home):
        """config.yaml 不存在时应返回空字典"""
        config_yaml = MagicMock(spec=Path)
        config_yaml.exists.return_value = False

        home_path = MagicMock(spec=Path)
        home_path.__truediv__.return_value.__truediv__.return_value = config_yaml
        mock_home.return_value = home_path

        result = snapshot_config()
        assert result == {}


# ═══════════════════════════════════════════
# do_snapshot 测试
# ═══════════════════════════════════════════

class TestDoSnapshot:
    """do_snapshot 函数测试"""

    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("builtins.print")
    def test_do_snapshot_basic(self, mock_print, mock_dt, mock_snap_file,
                               mock_config, mock_skills, mock_version):
        """do_snapshot 应正确生成快照结构并写入文件"""
        mock_dt.now.return_value = FIXED_DT
        mock_version.return_value = "v2.0.0"
        mock_skills.return_value = {"skill1": {"lines": 10}}
        mock_config.return_value = {"config_mtime": 1000.0}

        mock_parent = MagicMock()
        mock_snap_file.parent = mock_parent
        mock_snap_file.__str__.return_value = "/fake/snapshot.json"

        result = do_snapshot()

        mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_snap_file.write_text.assert_called_once()
        written = json.loads(mock_snap_file.write_text.call_args[0][0])
        assert written["hermes_version"] == "v2.0.0"
        assert written["skills"] == {"skill1": {"lines": 10}}
        assert written["timestamp"] == "2025-01-15T10:30:00"
        assert result["hermes_version"] == "v2.0.0"

    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("builtins.print")
    def test_do_snapshot_unknown_version(self, mock_print, mock_dt, mock_snap_file,
                                         mock_config, mock_skills, mock_version):
        """版本获取失败时应记录为 unknown"""
        mock_dt.now.return_value = FIXED_DT
        mock_version.return_value = "unknown"
        mock_skills.return_value = {}
        mock_config.return_value = {}

        mock_parent = MagicMock()
        mock_snap_file.parent = mock_parent

        result = do_snapshot()
        assert result["hermes_version"] == "unknown"


# ═══════════════════════════════════════════
# build_check_report 测试
# ═══════════════════════════════════════════

class TestBuildCheckReport:
    """build_check_report 函数测试"""

    def test_report_with_all_fields(self):
        """完整的结果数据应生成全面报告"""
        result = {
            "timestamp": "2025-01-15T10:30:00",
            "old_version": "v1.0.0",
            "new_version": "v2.0.0",
            "version_changed": True,
            "skills_changed": [
                {"path": "/skills/a/SKILL.md", "changes": ["行数: 10→15"]}
            ],
            "skills_added": ["/skills/b/SKILL.md"],
            "skills_removed": ["/skills/c/SKILL.md"],
            "config_changed": True,
            "warnings": ["Hermes版本从 v1.0.0 变更为 v2.0.0"],
            "auto_fixes_applied": [],
        }
        report = build_check_report(result)
        assert "Hermes升级兼容检查报告" in report
        assert "v1.0.0" in report
        assert "v2.0.0" in report
        assert "Skills变更" in report
        assert "新增Skills" in report
        assert "移除Skills" in report
        assert "警告" in report

    def test_report_no_changes(self):
        """无变更时应显示 ✅ 无异常"""
        result = {
            "timestamp": "2025-01-15T10:30:00",
            "old_version": "v1.0.0",
            "new_version": "v1.0.0",
            "version_changed": False,
            "skills_changed": [],
            "skills_added": [],
            "skills_removed": [],
            "config_changed": False,
            "warnings": [],
            "auto_fixes_applied": [],
        }
        report = build_check_report(result)
        assert "无异常" in report
        assert "✅" in report


# ═══════════════════════════════════════════
# do_check 测试
# ═══════════════════════════════════════════

class TestDoCheck:
    """do_check 函数测试"""

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("builtins.print")
    def test_check_no_snapshot(self, mock_print, mock_snap_file):
        """无快照文件时应返回错误"""
        mock_snap_file.exists.return_value = False
        result = do_check()
        assert result["status"] == "error"
        assert "无快照" in result["message"]

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("izu_hermes_upgrade_guard.OUTPUT_DIR")
    @patch("builtins.print")
    def test_check_version_change_detected(self, mock_print, mock_outdir, mock_dt,
                                           mock_config, mock_skills, mock_version, mock_snap_file):
        """版本变化应被正确检测"""
        old_snapshot = {
            "hermes_version": "v1.0.0",
            "skills": {},
            "config": {"config_mtime": 1000.0},
        }
        mock_snap_file.exists.return_value = True
        mock_snap_file.read_text.return_value = json.dumps(old_snapshot)

        mock_version.return_value = "v2.0.0"
        mock_skills.return_value = {}
        mock_config.return_value = {"config_mtime": 1000.0}
        mock_dt.now.return_value = FIXED_DT

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        result = do_check()
        assert result["old_version"] == "v1.0.0"
        assert result["new_version"] == "v2.0.0"
        assert result["version_changed"] is True
        assert "Hermes版本从" in result["warnings"][0]

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("izu_hermes_upgrade_guard.OUTPUT_DIR")
    @patch("builtins.print")
    def test_check_skill_change_detected(self, mock_print, mock_outdir, mock_dt,
                                         mock_config, mock_skills, mock_version, mock_snap_file):
        """skills文件变化应被正确检测（行数变化>20%）"""
        old_snapshot = {
            "hermes_version": "v1.0.0",
            "skills": {
                "/skills/test/SKILL.md": {
                    "lines": 100,
                    "frontmatter_fields": ["name", "version"],
                    "content_hash": 12345,
                }
            },
            "config": {},
        }
        mock_snap_file.exists.return_value = True
        mock_snap_file.read_text.return_value = json.dumps(old_snapshot)

        mock_version.return_value = "v1.0.0"
        # 150 lines → ratio=1.5 > 1.2, should be detected
        mock_skills.return_value = {
            "/skills/test/SKILL.md": {
                "lines": 150,
                "frontmatter_fields": ["name", "version"],
                "content_hash": 12345,
            }
        }
        mock_config.return_value = {}
        mock_dt.now.return_value = FIXED_DT

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        result = do_check()
        assert len(result["skills_changed"]) == 1
        assert "行数" in result["skills_changed"][0]["changes"][0]

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("izu_hermes_upgrade_guard.OUTPUT_DIR")
    @patch("builtins.print")
    def test_check_skill_added_removed(self, mock_print, mock_outdir, mock_dt,
                                       mock_config, mock_skills, mock_version, mock_snap_file):
        """新增和移除的skills应被检测"""
        old_snapshot = {
            "hermes_version": "v1.0.0",
            "skills": {
                "/skills/old/SKILL.md": {"lines": 10, "frontmatter_fields": [], "content_hash": 1},
            },
            "config": {},
        }
        mock_snap_file.exists.return_value = True
        mock_snap_file.read_text.return_value = json.dumps(old_snapshot)

        mock_version.return_value = "v1.0.0"
        mock_skills.return_value = {
            "/skills/new/SKILL.md": {"lines": 20, "frontmatter_fields": [], "content_hash": 2},
        }
        mock_config.return_value = {}
        mock_dt.now.return_value = FIXED_DT

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        result = do_check()
        assert len(result["skills_added"]) == 1
        assert len(result["skills_removed"]) == 1
        assert "/skills/new/SKILL.md" in result["skills_added"]
        assert "/skills/old/SKILL.md" in result["skills_removed"]

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("izu_hermes_upgrade_guard.OUTPUT_DIR")
    @patch("builtins.print")
    def test_check_generates_report_file(self, mock_print, mock_outdir, mock_dt,
                                         mock_config, mock_skills, mock_version, mock_snap_file):
        """do_check 应生成报告文件"""
        old_snapshot = {
            "hermes_version": "v1.0.0",
            "skills": {},
            "config": {},
        }
        mock_snap_file.exists.return_value = True
        mock_snap_file.read_text.return_value = json.dumps(old_snapshot)

        mock_version.return_value = "v1.0.0"
        mock_skills.return_value = {}
        mock_config.return_value = {}
        mock_dt.now.return_value = FIXED_DT

        mock_outdir.mkdir.return_value = None
        report_path = MagicMock(spec=Path)
        mock_outdir.__truediv__.return_value = report_path

        do_check()
        report_path.write_text.assert_called_once()
        report_content = report_path.write_text.call_args[0][0]
        assert "Hermes升级兼容检查报告" in report_content

    @patch("izu_hermes_upgrade_guard.SNAPSHOT_FILE")
    @patch("izu_hermes_upgrade_guard.get_hermes_version")
    @patch("izu_hermes_upgrade_guard.snapshot_skill_structure")
    @patch("izu_hermes_upgrade_guard.snapshot_config")
    @patch("izu_hermes_upgrade_guard.datetime")
    @patch("izu_hermes_upgrade_guard.OUTPUT_DIR")
    @patch("builtins.print")
    def test_check_config_change(self, mock_print, mock_outdir, mock_dt,
                                 mock_config, mock_skills, mock_version, mock_snap_file):
        """config 变化应被检测"""
        old_snapshot = {
            "hermes_version": "v1.0.0",
            "skills": {},
            "config": {"config_mtime": 1000.0},
        }
        mock_snap_file.exists.return_value = True
        mock_snap_file.read_text.return_value = json.dumps(old_snapshot)

        mock_version.return_value = "v1.0.0"
        mock_skills.return_value = {}
        mock_config.return_value = {"config_mtime": 2000.0}
        mock_dt.now.return_value = FIXED_DT

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        result = do_check()
        assert result["config_changed"] is True
