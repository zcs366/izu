"""Tests for izu_working_memory.py — score_message, extract, write_snapshot, CLI commands"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
from datetime import datetime

from izu_working_memory import (
    score_message, extract, write_snapshot,
    cmd_queue, cmd_snapshot, cmd_integrate,
    HERMES, MEMORY_FILE, SESSIONS, WORKING, K
)


# ═══════════════════════════════════════════
# score_message 测试
# ═══════════════════════════════════════════

class TestScoreMessage:
    """score_message 函数测试"""

    def test_empty_content_returns_zero(self):
        """空内容或非字符串应返回 0"""
        assert score_message("") == 0
        assert score_message("   ") == 0

    def test_important_keywords_add_30(self):
        """包含 '记住' '重要' '决定' 等词汇应 +30 (any匹配，只加一次)"""
        s = score_message("记住这个重要结论")
        assert s == 30  # 记住/重要/结论 → any匹配加30一次

    def test_previous_reference_adds_15(self):
        """包含 '上次' '之前' 等词汇应 +15"""
        s = score_message("上次我们讨论过这个问题")
        assert s >= 15

    def test_action_keywords_add_10(self):
        """包含 '写入' '创建' '修改' '删除' 等词汇应 +10"""
        s = score_message("我已写入配置文件并创建了新目录")
        assert s >= 10

    def test_question_mark_adds_8(self):
        """包含半角 '?' 应 +8（代码只检查半角）"""
        s = score_message("这个配置对吗?")
        assert s >= 8

    def test_user_role_bonus_5(self):
        """role='user' 应 +5"""
        s = score_message("hello", role="user")
        assert s >= 5

    def test_long_assistant_bonus_3(self):
        """assistant 且内容 >200 字符应 +3"""
        long_text = "word " * 50  # ~250 chars
        s = score_message(long_text, role="assistant")
        assert s >= 3

    def test_trivial_reply_penalty(self):
        """简短回复如 '好的' '明白' 减5分，最低0"""
        assert score_message("好的", role="user") == 0  # 5-5=0
        assert score_message("嗯") == 0

    def test_score_never_below_zero(self):
        """最低分为 0"""
        assert score_message("嗯", role="") >= 0
        assert score_message("ok") >= 0


# ═══════════════════════════════════════════
# extract 测试
# ═══════════════════════════════════════════

class TestExtract:
    """extract 函数测试"""

    @patch("izu_working_memory.Path.read_text")
    def test_extract_from_json_object(self, mock_read):
        """从JSON对象格式的session提取top-K条目"""
        mock_read.return_value = json.dumps({
            "messages": [
                {"role": "user", "content": "记住这个重要配置"},
                {"role": "assistant", "content": "好的"},
                {"role": "user", "content": "必须修改部署脚本"},
                {"role": "assistant", "content": "已更新。"},
            ]
        })
        items = extract(Path("/fake/session.json"))
        assert len(items) <= K
        # "记住这个重要配置" → 含 '记住'/'重要' → any匹配加30；user +5 → 35
        assert items[0]["score"] >= 30
        assert items[0]["role"] == "user"

    @patch("izu_working_memory.Path.read_text")
    def test_extract_from_jsonl(self, mock_read):
        """从JSONL格式的session提取top-K条目"""
        mock_read.return_value = (
            '{"role": "user", "content": "hello"}\n'
            '{"role": "assistant", "content": "重要决定：明天上线"}\n'
            '{"role": "user", "content": "注意版本兼容性问题"}\n'
        )
        items = extract(Path("/fake/session.jsonl"))
        assert len(items) <= K
        # 排序结果：
        #   "注意版本兼容性问题": 注意(+30) + user(+5) = 35
        #   "重要决定：明天上线": 重要/决定(any+30) = 30
        #   "hello": user(+5) = 5
        assert items[0]["score"] == 35
        assert items[0]["role"] == "user"
        assert items[1]["score"] == 30
        assert items[1]["role"] == "assistant"

    @patch("izu_working_memory.Path.read_text")
    def test_extract_handles_malformed_json(self, mock_read):
        """损坏的JSON应静默处理"""
        mock_read.return_value = "{this is not json"
        items = extract(Path("/fake/bad.json"))
        assert items == []

    @patch("izu_working_memory.Path.read_text")
    def test_extract_sorts_by_score_desc(self, mock_read):
        """返回结果应按分数降序排列"""
        mock_read.return_value = json.dumps({
            "messages": [
                {"role": "user", "content": "你好"},
                {"role": "user", "content": "重要：部署计划"},
                {"role": "user", "content": "必须修改pipeline配置文件"},
                {"role": "user", "content": "这次决定采用绿色方案"},
            ]
        })
        items = extract(Path("/fake/session.json"))
        scores = [i["score"] for i in items]
        assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))

    @patch("izu_working_memory.Path.read_text")
    def test_extract_limits_to_k(self, mock_read):
        """返回结果不超过K条"""
        many_msgs = [
            {"role": "user", "content": f"重要任务{i}"}
            for i in range(50)
        ]
        mock_read.return_value = json.dumps({"messages": many_msgs})
        items = extract(Path("/fake/session.json"))
        assert len(items) <= K

    @patch("izu_working_memory.Path.read_text")
    def test_extract_handles_dict_content(self, mock_read):
        """content 为 dict 类型时不应崩溃"""
        mock_read.return_value = json.dumps({
            "messages": [
                {"role": "user", "content": {"decision": "confirmed", "key": "val"}},
            ]
        })
        items = extract(Path("/fake/session.json"))
        assert isinstance(items, list)


# ═══════════════════════════════════════════
# write_snapshot 测试
# ═══════════════════════════════════════════

class TestWriteSnapshot:
    """write_snapshot 函数测试"""

    @patch("izu_working_memory.WORKING")
    def test_write_snapshot_creates_file(self, mock_working):
        """write_snapshot 应正确生成 MARKDOWN 内容"""
        mock_parent = MagicMock()
        mock_working.parent = mock_parent
        mock_working.__str__.return_value = "/fake/.hermes/memories/WORKING.md"

        items = [
            {"score": 85, "role": "user", "preview": "记住要配置数据库连接", "tool": ""},
            {"score": 42, "role": "assistant", "preview": "已修改deploy脚本", "tool": ""},
        ]
        result = write_snapshot(items, source="test_sesh.json")

        mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_working.write_text.assert_called_once()
        written = mock_working.write_text.call_args[0][0]
        assert "工作记忆快照" in written
        assert "test_sesh.json" in written
        assert "[1/5]" in written
        assert "85" in written
        assert "记住要配置数据库连接" in written

    @patch("izu_working_memory.WORKING")
    def test_write_snapshot_includes_tool_field(self, mock_working):
        """含 tool 字段时应输出工具行"""
        mock_working.parent = MagicMock()
        mock_working.__str__.return_value = "/fake/.hermes/memories/WORKING.md"

        items = [
            {"score": 70, "role": "tool", "preview": "搜索返回结果", "tool": "web_search"},
        ]
        write_snapshot(items)
        written = mock_working.write_text.call_args[0][0]
        assert "web_search" in written
        assert "工具:" in written


# ═══════════════════════════════════════════
# cmd_queue 测试
# ═══════════════════════════════════════════

class TestCmdQueue:
    """cmd_queue CLI 命令测试"""

    @patch("izu_working_memory.SESSIONS")
    @patch("izu_working_memory.extract")
    @patch("izu_working_memory.write_snapshot")
    @patch("builtins.print")
    def test_cmd_queue_found_by_exact_name(self, mock_print, mock_write, mock_extract, mock_sessions):
        """cmd_queue 应精确匹配session文件"""
        exact_path = MagicMock(spec=Path)
        exact_path.exists.return_value = True
        exact_path.name = "session_test.json"
        mock_sessions.__truediv__.return_value = exact_path
        mock_extract.return_value = [{"score": 50, "role": "user", "preview": "重要内容"}]

        cmd_queue("session_test.json")
        mock_extract.assert_called_once_with(exact_path)
        mock_write.assert_called_once()

    @patch("izu_working_memory.SESSIONS")
    @patch("izu_working_memory.extract")
    @patch("izu_working_memory.write_snapshot")
    @patch("builtins.print")
    def test_cmd_queue_found_by_fuzzy_match(self, mock_print, mock_write, mock_extract, mock_sessions):
        """精确名不存在时应尝试模糊匹配"""
        exact_path = MagicMock(spec=Path)
        exact_path.exists.return_value = False
        mock_sessions.__truediv__.return_value = exact_path
        fuzzy_match = MagicMock(spec=Path)
        fuzzy_match.name = "session_test.json"
        mock_sessions.glob.return_value = [fuzzy_match]
        mock_extract.return_value = [{"score": 40, "role": "user", "preview": "test"}]

        cmd_queue("test")
        mock_sessions.glob.assert_called_once()
        mock_extract.assert_called_once_with(fuzzy_match)

    @patch("izu_working_memory.SESSIONS")
    @patch("builtins.print")
    def test_cmd_queue_not_found(self, mock_print, mock_sessions):
        """找不到session时应提示错误"""
        exact_path = MagicMock(spec=Path)
        exact_path.exists.return_value = False
        mock_sessions.__truediv__.return_value = exact_path
        mock_sessions.glob.return_value = []
        cmd_queue("nonexistent")
        mock_print.assert_called_with("❌ 未找到: nonexistent")


# ═══════════════════════════════════════════
# cmd_snapshot 测试
# ═══════════════════════════════════════════

class TestCmdSnapshot:
    """cmd_snapshot CLI 命令测试"""

    @patch("izu_working_memory.SESSIONS")
    @patch("izu_working_memory.os.path.getmtime")
    @patch("izu_working_memory.extract")
    @patch("izu_working_memory.write_snapshot")
    @patch("builtins.print")
    def test_cmd_snapshot_merges_from_latest_three(self, mock_print, mock_write,
                                                   mock_extract, mock_getmtime, mock_sessions):
        """cmd_snapshot 应从最近3个session中提取去重合并"""
        s1 = MagicMock(spec=Path)
        s1.name = "session_1.json"
        s2 = MagicMock(spec=Path)
        s2.name = "session_2.json"
        s3 = MagicMock(spec=Path)
        s3.name = "session_3.json"
        mock_sessions.glob.return_value = [s1, s2, s3]
        mock_getmtime.side_effect = [100, 200, 300]

        mock_extract.side_effect = [
            [{"score": 90, "role": "user", "preview": "A" * 61}],
            [{"score": 80, "role": "user", "preview": "B" * 61}],
            [{"score": 70, "role": "user", "preview": "C" * 61}],
        ]

        cmd_snapshot()
        assert mock_extract.call_count == 3
        mock_write.assert_called_once()
        args = mock_write.call_args[0]
        assert len(args[0]) <= K

    @patch("izu_working_memory.SESSIONS")
    @patch("builtins.print")
    def test_cmd_snapshot_no_sessions(self, mock_print, mock_sessions):
        """无可用session时应提示"""
        mock_sessions.glob.return_value = []
        cmd_snapshot()
        mock_print.assert_called_with("❌ 无可用session")


# ═══════════════════════════════════════════
# cmd_integrate 测试
# ═══════════════════════════════════════════

class TestCmdIntegrate:
    """cmd_integrate CLI 命令测试"""

    @patch("izu_working_memory.SESSIONS")
    @patch("izu_working_memory.extract")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_cmd_integrate_appends_high_value_decisions(self, mock_print, mock_open_file,
                                                        mock_extract, mock_sessions):
        """integrate 应将高分条目写入 MEMORY_FILE"""
        exact_path = MagicMock(spec=Path)
        exact_path.exists.return_value = True
        exact_path.name = "session_work.json"
        mock_sessions.__truediv__.return_value = exact_path

        mock_extract.return_value = [
            {"score": 85, "role": "user", "preview": "决定采用微服务架构"},
            {"score": 30, "role": "user", "preview": "普通消息"},
        ]

        cmd_integrate("session_work.json")
        # 只有 >= 25 的条目被集成
        handle = mock_open_file()
        written_lines = [c[0][0] for c in handle.write.call_args_list]
        assert any("决定采用微服务架构" in line for line in written_lines)
        assert any("从 session_work.json 集成" in line for line in written_lines)

    @patch("izu_working_memory.SESSIONS")
    @patch("izu_working_memory.extract")
    @patch("builtins.print")
    def test_cmd_integrate_none_high_value(self, mock_print, mock_extract, mock_sessions):
        """无高分条目时应提示"""
        exact_path = MagicMock(spec=Path)
        exact_path.exists.return_value = True
        mock_sessions.__truediv__.return_value = exact_path

        mock_extract.return_value = [
            {"score": 10, "role": "user", "preview": "你好"},
        ]
        cmd_integrate("session_work.json")
        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "无高价值" in call_args or "⚠️" in call_args
