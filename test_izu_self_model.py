"""Tests for izu_self_model.py — extract_anchors, compute_fingerprint, snapshot, cmd_list, cmd_diff"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
from datetime import datetime

from izu_self_model import (
    extract_anchors, compute_fingerprint, snapshot, cmd_list, cmd_diff,
    HERMES, SOUL_FILE, SNAPSHOTS_DIR
)


# ═══════════════════════════════════════════
# extract_anchors 测试
# ═══════════════════════════════════════════

class TestExtractAnchors:
    """extract_anchors 函数测试"""

    def test_extract_all_anchor_types(self):
        """应能分别提取每种锚点（因re.DOTALL下(.+)会跨行匹配，每次只测一个完整字段）"""
        # role: 非贪婪匹配，在换行处停止
        assert extract_anchors("**角色**：AI助手\nxxx")["role"] == "AI助手"
        # mission: re.DOTALL下跨行匹配到末尾
        assert extract_anchors("核心使命：帮助用户解决问题")["mission"] == "帮助用户解决问题"
        # name: re.DOTALL下(.+)匹配到末尾
        assert extract_anchors("name: hermes-agent")["name"] == "hermes-agent"
        # description: re.DOTALL下(.+)匹配到末尾
        assert extract_anchors("description: 智能AI助手")["description"] == "智能AI助手"
        # personality: 非贪婪匹配，在换行处停止
        assert extract_anchors("**性格**：友好、专业\nxxx")["personality"] == "友好、专业"
        # color: 双引号包围，匹配到"
        assert extract_anchors('color: "#8B5CF6"')["color"] == "#8B5CF6"

    def test_extract_partial_anchors(self):
        """文本中只有部分锚点时，应只返回匹配到的"""
        text = "**角色**：测试员\nname: tester\n"
        anchors = extract_anchors(text)
        assert anchors == {"role": "测试员", "name": "tester"}

    def test_extract_no_anchors(self):
        """无匹配锚点时应返回空字典"""
        text = "这是一段普通文本，没有锚点标记"
        anchors = extract_anchors(text)
        assert anchors == {}

    def test_extract_empty_text(self):
        """空文本应返回空字典"""
        assert extract_anchors("") == {}

    def test_extract_with_chinese_colon(self):
        """应同时支持中文冒号:和英文冒号:"""
        text_en = "name: my_agent"
        text_cn = "name：my_agent"
        assert extract_anchors(text_en)["name"] == "my_agent"
        assert extract_anchors(text_cn)["name"] == "my_agent"

    def test_extract_multiline_mission(self):
        """mission锚点应能跨行匹配（re.DOTALL）"""
        text = "核心使命：帮助用户解决\n技术问题并\n提供支持"
        anchors = extract_anchors(text)
        assert "mission" in anchors
        assert "帮助" in anchors["mission"]

    def test_extract_role_stops_at_newline(self):
        """role锚点使用非贪婪匹配，应在换行处停止"""
        text = "**角色**：AI\n助手"
        anchors = extract_anchors(text)
        assert anchors["role"] == "AI"


# ═══════════════════════════════════════════
# compute_fingerprint 测试
# ═══════════════════════════════════════════

class TestComputeFingerprint:
    """compute_fingerprint 函数测试"""

    def test_same_anchors_same_fingerprint(self):
        """同样的锚点内容应生成相同的指纹"""
        a1 = {"role": "AI", "name": "test"}
        a2 = {"role": "AI", "name": "test"}
        assert compute_fingerprint(a1) == compute_fingerprint(a2)

    def test_different_anchors_different_fingerprint(self):
        """不同锚点内容应生成不同的指纹"""
        a1 = {"role": "AI", "name": "test"}
        a2 = {"role": "AI", "name": "other"}
        assert compute_fingerprint(a1) != compute_fingerprint(a2)

    def test_fingerprint_is_string_of_digits(self):
        """指纹应为纯数字字符串"""
        fp = compute_fingerprint({"role": "AI"})
        assert isinstance(fp, str)
        assert fp.isdigit()

    def test_fingerprint_order_independent(self):
        """指纹应不受键顺序影响"""
        a1 = compute_fingerprint({"a": "1", "b": "2"})
        a2 = compute_fingerprint({"b": "2", "a": "1"})
        assert a1 == a2

    def test_fingerprint_empty_dict(self):
        """空字典应能生成指纹"""
        fp = compute_fingerprint({})
        assert isinstance(fp, str)
        assert fp.isdigit()


# ═══════════════════════════════════════════
# snapshot 测试
# ═══════════════════════════════════════════

class TestSnapshot:
    """snapshot 函数测试"""

    @patch("izu_self_model.SOUL_FILE")
    @patch("izu_self_model.datetime")
    @patch("builtins.print")
    def test_snapshot_creates_file(self, mock_print, mock_dt, mock_soul):
        """snapshot 应生成正确的JSON快照文件"""
        mock_soul.exists.return_value = True
        mock_soul.read_text.return_value = "**角色**：AI\nname: test"

        # Mock datetime.now() to return a real datetime, then mock strftime/isoformat on it
        fixed_dt = datetime(2025, 1, 15, 10, 30, 0)
        mock_dt.now.return_value = fixed_dt

        # Mock SNAPSHOTS_DIR operations
        with patch("izu_self_model.SNAPSHOTS_DIR") as mock_snap_dir:
            mock_snap_dir.mkdir.return_value = None
            out_path = MagicMock(spec=Path)
            mock_snap_dir.__truediv__.return_value = out_path

            snapshot()

            mock_snap_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
            out_path.write_text.assert_called_once()
            written = json.loads(out_path.write_text.call_args[0][0])
            assert written["version"] == "20250115_103000"
            assert written["anchors"]["role"] == "AI"
            assert written["anchors"]["name"] == "test"
            assert written["fingerprint"] == compute_fingerprint({"role": "AI", "name": "test"})

    @patch("izu_self_model.SOUL_FILE")
    @patch("builtins.print")
    def test_snapshot_no_soul_file(self, mock_print, mock_soul):
        """SOUL.md不存在时应打印错误信息"""
        mock_soul.exists.return_value = False
        snapshot()
        mock_print.assert_called_with(f"❌ 未找到SOUL.md: {mock_soul}")

    @patch("izu_self_model.SOUL_FILE")
    @patch("izu_self_model.datetime")
    @patch("builtins.print")
    def test_snapshot_includes_raw_length(self, mock_print, mock_dt, mock_soul):
        """快照应包含原始内容长度"""
        mock_soul.exists.return_value = True
        soul_content = "**角色**：AI助手\n核心使命：测试\n"
        mock_soul.read_text.return_value = soul_content

        fixed_dt = datetime(2025, 1, 15, 10, 30, 0)
        mock_dt.now.return_value = fixed_dt

        with patch("izu_self_model.SNAPSHOTS_DIR") as mock_snap_dir:
            mock_snap_dir.mkdir.return_value = None
            out_path = MagicMock(spec=Path)
            mock_snap_dir.__truediv__.return_value = out_path

            snapshot()

            written = json.loads(out_path.write_text.call_args[0][0])
            assert written["raw_length"] == len(soul_content)


# ═══════════════════════════════════════════
# cmd_list 测试
# ═══════════════════════════════════════════

class TestCmdList:
    """cmd_list 函数测试"""

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_list_no_snapshots(self, mock_print, mock_snap_dir):
        """无快照时应打印提示"""
        mock_snap_dir.glob.return_value = []
        cmd_list()
        mock_print.assert_called_with("❌ 无Self Model快照")

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_list_with_snapshots(self, mock_print, mock_snap_dir):
        """有快照时应列出所有版本"""
        snap1 = MagicMock(spec=Path)
        snap1.name = "self_model_20250115_103000.json"
        snap1.read_text.return_value = json.dumps({
            "fingerprint": "123456789012",
            "anchors": {"role": "AI", "name": "test"}
        })
        snap1.__lt__ = lambda self, other: self.name < other.name

        snap2 = MagicMock(spec=Path)
        snap2.name = "self_model_20250116_103001.json"
        snap2.read_text.return_value = json.dumps({
            "fingerprint": "987654321098",
            "anchors": {"role": "AI", "name": "new_test"}
        })
        snap2.__lt__ = lambda self, other: self.name < other.name

        mock_snap_dir.glob.return_value = [snap1, snap2]

        cmd_list()

        assert mock_print.call_count >= 2
        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "self_model_20250115" in call_args
        assert "self_model_20250116" in call_args


# ═══════════════════════════════════════════
# cmd_diff 测试
# ═══════════════════════════════════════════

def _make_sortable_path_mock(name, read_text_data):
    """Helper to create a MagicMock Path that supports sorted() by name"""
    m = MagicMock(spec=Path)
    m.name = name
    m.read_text.return_value = json.dumps(read_text_data)
    # Support sorting by name via __lt__
    def lt(self, other):
        return self.name < other.name
    m.__lt__ = lt
    return m


class TestCmdDiff:
    """cmd_diff 函数测试"""

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_diff_less_than_two(self, mock_print, mock_snap_dir):
        """快照不足2个时应提示"""
        mock_snap_dir.glob.return_value = [MagicMock(spec=Path)]
        cmd_diff()
        mock_print.assert_called_with("❌ 需要至少2个版本才能对比")

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_diff_no_changes(self, mock_print, mock_snap_dir):
        """两个版本一致时应提示无变更"""
        old_data = {
            "timestamp": "2025-01-15T10:30:00",
            "fingerprint": "123456789012",
            "anchors": {"role": "AI", "name": "test"}
        }
        new_data = {
            "timestamp": "2025-01-16T10:30:00",
            "fingerprint": "123456789012",
            "anchors": {"role": "AI", "name": "test"}
        }
        snap_old = _make_sortable_path_mock("self_model_20250115.json", old_data)
        snap_new = _make_sortable_path_mock("self_model_20250116.json", new_data)
        mock_snap_dir.glob.return_value = [snap_old, snap_new]

        cmd_diff()

        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "无变更" in call_args or "一致" in call_args

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_diff_detects_changes(self, mock_print, mock_snap_dir):
        """锚点有变化时应检测并输出变更详情"""
        old_data = {
            "timestamp": "2025-01-15T10:30:00",
            "fingerprint": "111111111111",
            "anchors": {"role": "AI助手", "name": "hermes"}
        }
        new_data = {
            "timestamp": "2025-01-16T10:30:00",
            "fingerprint": "222222222222",
            "anchors": {"role": "AI助手-v2", "name": "hermes"}
        }
        snap_old = _make_sortable_path_mock("self_model_20250115.json", old_data)
        snap_new = _make_sortable_path_mock("self_model_20250116.json", new_data)
        mock_snap_dir.glob.return_value = [snap_old, snap_new]

        cmd_diff()

        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "AI助手" in call_args
        assert "AI助手-v2" in call_args
        assert "role" in call_args
        assert "已变更" in call_args

    @patch("izu_self_model.SNAPSHOTS_DIR")
    @patch("builtins.print")
    def test_diff_detects_new_and_removed_anchors(self, mock_print, mock_snap_dir):
        """应能检测锚点新增和移除"""
        old_data = {
            "timestamp": "2025-01-15T10:30:00",
            "fingerprint": "111111111111",
            "anchors": {"role": "AI", "mission": "help"}
        }
        new_data = {
            "timestamp": "2025-01-16T10:30:00",
            "fingerprint": "222222222222",
            "anchors": {"role": "AI", "name": "new"}
        }
        snap_old = _make_sortable_path_mock("self_model_20250115.json", old_data)
        snap_new = _make_sortable_path_mock("self_model_20250116.json", new_data)
        mock_snap_dir.glob.return_value = [snap_old, snap_new]

        cmd_diff()

        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "mission" in call_args
        assert "缺失" in call_args
