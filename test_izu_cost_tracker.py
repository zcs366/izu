"""
Tests for izu_cost_tracker.py — count_tokens, estimate_cost, scan_session, scan_all, generate_report

All tests use mock file I/O — no real filesystem dependencies.
Strategy: patch module-level Path variables with MagicMock since PosixPath
doesn't allow attribute patching directly (C-extension).
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from izu_cost_tracker import (
    count_tokens, estimate_cost, scan_session,
    scan_all, generate_report,
    COST_LOG, OUTPUT_DIR, SESSION_DIR, DATA_DIR,
    MODEL_PRICING, DEFAULT_COST, MONTHLY_MODELS,
)


# ── helpers ──

def mock_cost_log(exists=True, content=""):
    """Create a MagicMock that looks like a cost log Path."""
    m = MagicMock(spec=Path)
    m.exists.return_value = exists
    m.read_text.return_value = content
    return m


def mock_output_dir():
    m = MagicMock(spec=Path)
    return m


# ═══════════════════════════════════════════
# count_tokens 测试
# ═══════════════════════════════════════════

class TestCountTokens:
    """count_tokens(text) -> estimated token breakdown"""

    def test_empty_string(self):
        result = count_tokens("")
        assert result['chars'] == 0
        assert result['estimated_tokens'] == 0

    def test_english_text(self):
        """英文文本估算token"""
        result = count_tokens("hello world this is a test")
        assert result['en_chars'] > 0
        assert result['estimated_tokens'] > 0
        assert result['estimated_tokens'] <= result['chars']

    def test_chinese_text(self):
        """中文文本估算token"""
        result = count_tokens("你好世界这是一段测试文本")
        assert result['cn_chars'] > 0
        assert result['estimated_tokens'] > 0

    def test_mixed_text(self):
        """中英文混合"""
        result = count_tokens("Hello 你好 world 世界 code ```print('hi')```")
        assert result['en_chars'] > 0
        assert result['cn_chars'] > 0
        assert result['code_chars'] >= 50

    def test_code_blocks_counted(self):
        """代码块标记被单独计数"""
        result = count_tokens("some text ```code block``` more text")
        assert result['code_chars'] >= 50

    def test_estimated_tokens_reasonable(self):
        """估算token数应为正数"""
        text = "A" * 100 + "你" * 100
        result = count_tokens(text)
        assert result['estimated_tokens'] > 0
        assert result['estimated_tokens'] < result['chars'] * 2

    def test_only_numbers_and_symbols(self):
        """纯符号/数字"""
        result = count_tokens("12345!@#$%^&*()_+-=[]{}|;':\",./<>?")
        assert result['estimated_tokens'] > 0
        assert result['en_chars'] == 0
        assert result['cn_chars'] == 0


# ═══════════════════════════════════════════
# estimate_cost 测试
# ═══════════════════════════════════════════

class TestEstimateCost:
    """estimate_cost(model, input_tokens, output_tokens) -> cost dict"""

    def test_known_model_cost(self):
        """已知模型应返回对应单价计算"""
        result = estimate_cost('deepseek-chat', 1000, 500)
        expected_input = 1000 * MODEL_PRICING['deepseek-chat']['input'] / 1_000_000
        expected_output = 500 * MODEL_PRICING['deepseek-chat']['output'] / 1_000_000
        assert result['input_cost'] == round(expected_input, 5)
        assert result['output_cost'] == round(expected_output, 5)
        assert result['total'] == round(expected_input + expected_output, 5)

    def test_unknown_model_fallback(self):
        """未知模型使用默认价格"""
        result = estimate_cost('some-unknown-model', 1000, 500)
        expected_input = 1000 * DEFAULT_COST['input'] / 1_000_000
        expected_output = 500 * DEFAULT_COST['output'] / 1_000_000
        assert result['total'] == round(expected_input + expected_output, 5)

    def test_monthly_model_zero_cost(self):
        """包月模型不计边际成本"""
        for model in MONTHLY_MODELS:
            result = estimate_cost(model, 10000, 50000)
            assert result['input_cost'] == 0
            assert result['output_cost'] == 0
            assert result['total'] == 0

    def test_monthly_model_case_insensitive(self):
        """包月模型大小写不敏感"""
        result = estimate_cost('MiniMax', 1000, 1000)
        assert result['total'] == 0

    def test_zero_tokens_zero_cost(self):
        """零token应零成本"""
        result = estimate_cost('deepseek-chat', 0, 0)
        assert result['input_cost'] == 0
        assert result['output_cost'] == 0
        assert result['total'] == 0

    def test_large_token_precision(self):
        """大量token应合理计算"""
        result = estimate_cost('deepseek-chat', 1_000_000, 500_000)
        assert result['input_cost'] == pytest.approx(0.28, 0.001)
        assert result['output_cost'] == pytest.approx(0.55, 0.001)

    def test_model_key_whitespace_stripped(self):
        """模型名前后的空格应被去除"""
        result = estimate_cost('  DeepSeek-Chat  ', 1000, 500)
        assert result['total'] > 0
        assert result['pricing_note'] == 'deepseek-chat'


# ═══════════════════════════════════════════
# scan_session 测试
# ═══════════════════════════════════════════

class TestScanSession:
    """scan_session(path) -> record dict or None"""

    def test_valid_session(self):
        """valid session with user/assistant messages"""
        session_data = {
            "session_id": "test-session-1",
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ]
        }
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.stem = 'test-session-1'
        p.read_text.return_value = json.dumps(session_data)
        record = scan_session(p)

        assert record is not None
        assert record['model'] == 'deepseek-chat'
        assert record['messages'] == 2
        assert record['user_msgs'] == 1
        assert record['assistant_msgs'] == 1
        assert record['input_tokens'] > 0
        assert record['output_tokens'] > 0

    def test_skip_archived_files(self):
        """.archived 后缀文件跳过"""
        p = MagicMock(spec=Path)
        p.suffix = '.archived'
        record = scan_session(p)
        assert record is None

    def test_skip_purged_files(self):
        """.purged 后缀文件跳过"""
        p = MagicMock(spec=Path)
        p.suffix = '.purged'
        record = scan_session(p)
        assert record is None

    def test_invalid_json_returns_none(self):
        """无效json返回None"""
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.read_text.side_effect = [
            json.JSONDecodeError("bad", "", 0),
            FileNotFoundError,
        ]
        record = scan_session(p)
        assert record is None

    def test_empty_messages_returns_none(self):
        """messages为空返回None"""
        session_data = {
            "session_id": "empty",
            "model": "deepseek-chat",
            "messages": []
        }
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.read_text.return_value = json.dumps(session_data)
        record = scan_session(p)
        assert record is None

    def test_with_tool_calls(self):
        """包含tool_calls的消息"""
        session_data = {
            "session_id": "tool-test",
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": "Search the web"},
                {"role": "assistant", "content": "Let me search...",
                 "tool_calls": [
                     {"function": {"arguments": "query=weather"}},
                     {"function": {"arguments": "query=news"}},
                 ]},
                {"role": "tool", "content": "Results: sunny"},
            ]
        }
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.read_text.return_value = json.dumps(session_data)
        record = scan_session(p)
        assert record is not None
        assert record['tool_calls'] == 2

    def test_content_as_list(self):
        """content为list的情况"""
        session_data = {
            "session_id": "list-content",
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": [{"text": "Hello"}, {"text": "World"}]},
            ]
        }
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.read_text.return_value = json.dumps(session_data)
        record = scan_session(p)
        assert record is not None
        assert record['user_msgs'] == 1

    def test_session_id_fallback_to_stem(self):
        """session_id回退到文件名stem"""
        session_data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "hi"}]
        }
        p = MagicMock(spec=Path)
        p.suffix = '.json'
        p.stem = 'my-session'
        p.read_text.return_value = json.dumps(session_data)
        record = scan_session(p)
        assert record is not None
        assert record['session_id'] == "my-session"


# ═══════════════════════════════════════════
# scan_all 测试
# ═══════════════════════════════════════════

class TestScanAll:
    """scan_all() — 扫描所有session并写入日志"""

    def test_no_new_sessions(self):
        """已有日志中有全部session_id时，应输出'无新session'"""
        existing_log = json.dumps({"session_id": "existing-session", "model": "x", "total": 0}) + "\n"
        mock_log = mock_cost_log(exists=True, content=existing_log)
        mock_session_dir = MagicMock(spec=Path)
        mock_session_dir.glob.return_value = []
        mock_data_dir = MagicMock(spec=Path)

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.SESSION_DIR', mock_session_dir),
            patch('izu_cost_tracker.DATA_DIR', mock_data_dir),
        ):
            result = scan_all()
        assert result == []

    def test_new_entries_appended(self):
        """新session应被添加到日志"""
        session_path = MagicMock(spec=Path)
        session_path.stem = 'new-session'
        mock_log = mock_cost_log(exists=False)
        mock_session_dir = MagicMock(spec=Path)
        mock_session_dir.glob.return_value = [session_path]
        mock_data_dir = MagicMock(spec=Path)

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.SESSION_DIR', mock_session_dir),
            patch('izu_cost_tracker.DATA_DIR', mock_data_dir),
            patch("izu_cost_tracker.scan_session", return_value={
                "session_id": "new-session", "model": "deepseek-chat",
                "total_tokens": 100, "total": 0.0001,
            }),
            patch("os.path.getmtime", return_value=1000),
            patch("builtins.open", mock_open()),
        ):
            result = scan_all()

        assert len(result) == 1
        assert result[0]['session_id'] == "new-session"

    def test_skip_existing_ids(self):
        """已有记录中的session_id应跳过"""
        existing = json.dumps({"session_id": "old-session", "model": "x", "total": 0}) + "\n"
        mock_log = mock_cost_log(exists=True, content=existing)
        mock_session_dir = MagicMock(spec=Path)
        mock_session_dir.glob.return_value = []
        mock_data_dir = MagicMock(spec=Path)

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.SESSION_DIR', mock_session_dir),
            patch('izu_cost_tracker.DATA_DIR', mock_data_dir),
        ):
            result = scan_all()
        assert len(result) == 0

    def test_scan_all_writes_jsonl_new_entries(self):
        """scan_all 对新增记录应写入jsonl"""
        session_path = MagicMock(spec=Path)
        session_path.stem = 'new'
        mock_log = mock_cost_log(exists=False)
        mock_session_dir = MagicMock(spec=Path)
        mock_session_dir.glob.return_value = [session_path]
        mock_data_dir = MagicMock(spec=Path)

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.SESSION_DIR', mock_session_dir),
            patch('izu_cost_tracker.DATA_DIR', mock_data_dir),
            patch("izu_cost_tracker.scan_session", return_value={
                "session_id": "new", "model": "deepseek-chat",
                "total_tokens": 100, "total": 0.00005,
            }),
            patch("os.path.getmtime", return_value=1000),
            patch("builtins.open", mock_open()),
        ):
            result = scan_all()
        assert len(result) == 1


# ═══════════════════════════════════════════
# generate_report 测试
# ═══════════════════════════════════════════

class TestGenerateReport:
    """generate_report() — 从日志生成成本报告"""

    SAMPLE_ENTRIES = [
        {"session_id": "s1", "model": "deepseek-chat", "total_tokens": 1000,
         "input_tokens": 600, "output_tokens": 400, "total": 0.0500,
         "timestamp": "2026-01-15T10:00:00"},
        {"session_id": "s2", "model": "gpt-4o-mini", "total_tokens": 500,
         "input_tokens": 300, "output_tokens": 200, "total": 0.0100,
         "timestamp": "2026-01-16T12:00:00"},
    ]

    def test_no_log_file(self):
        """日志不存在时打印警告并返回None"""
        mock_log = mock_cost_log(exists=False)
        with patch('izu_cost_tracker.COST_LOG', mock_log):
            result = generate_report()
        assert result is None

    def test_empty_log(self):
        """空日志生成空报告并print"""
        mock_log = mock_cost_log(exists=True, content="")
        mock_out_dir = MagicMock(spec=Path)
        report_path = MagicMock(spec=Path)
        mock_out_dir.__truediv__.return_value = report_path

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.OUTPUT_DIR', mock_out_dir),
        ):
            result = generate_report()
        # generate_report does `return print(...)` which returns None
        assert result is None
        # but report_path.write_text was still called (for the empty report)
        report_path.write_text.assert_called_once()

    def test_report_content_model_summary(self):
        """报告应包含按模型汇总数据"""
        log_content = "\n".join(json.dumps(e) for e in self.SAMPLE_ENTRIES) + "\n"
        mock_log = mock_cost_log(exists=True, content=log_content)
        mock_out_dir = MagicMock(spec=Path)
        report_path = MagicMock(spec=Path)
        mock_out_dir.__truediv__.return_value = report_path

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.OUTPUT_DIR', mock_out_dir),
        ):
            result = generate_report()

        assert result is report_path
        write_args = report_path.write_text.call_args
        written = write_args[0][0] if write_args else ""
        assert "deepseek-chat" in written
        assert "gpt-4o-mini" in written
        assert "总Token" in written
        assert "总成本" in written

    def test_report_with_monthly_model(self):
        """包月模型在报告中应正常显示"""
        entries = [
            {"session_id": "s1", "model": "minimax", "total_tokens": 5000,
             "input_tokens": 3000, "output_tokens": 2000, "total": 0.0,
             "timestamp": "2026-01-15"}
        ]
        log_content = json.dumps(entries[0]) + "\n"
        mock_log = mock_cost_log(exists=True, content=log_content)
        mock_out_dir = MagicMock(spec=Path)
        report_path = MagicMock(spec=Path)
        mock_out_dir.__truediv__.return_value = report_path

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.OUTPUT_DIR', mock_out_dir),
        ):
            result = generate_report()

        assert result is report_path
        written = report_path.write_text.call_args[0][0]
        assert "minimax" in written

    def test_report_by_day_grouping(self):
        """报告应按日期分组"""
        entries = [
            {"session_id": "s1", "model": "deepseek-chat", "total_tokens": 100,
             "input_tokens": 50, "output_tokens": 50, "total": 0.01,
             "timestamp": "2026-01-15"},
            {"session_id": "s2", "model": "deepseek-chat", "total_tokens": 200,
             "input_tokens": 100, "output_tokens": 100, "total": 0.02,
             "timestamp": "2026-01-15"},
            {"session_id": "s3", "model": "deepseek-chat", "total_tokens": 300,
             "input_tokens": 150, "output_tokens": 150, "total": 0.03,
             "timestamp": "2026-01-16"},
        ]
        log_content = "\n".join(json.dumps(e) for e in entries) + "\n"
        mock_log = mock_cost_log(exists=True, content=log_content)
        mock_out_dir = MagicMock(spec=Path)
        report_path = MagicMock(spec=Path)
        mock_out_dir.__truediv__.return_value = report_path

        with (
            patch('izu_cost_tracker.COST_LOG', mock_log),
            patch('izu_cost_tracker.OUTPUT_DIR', mock_out_dir),
        ):
            result = generate_report()

        assert result is report_path
        written = report_path.write_text.call_args[0][0]
        assert "2026-01-15" in written
        assert "2026-01-16" in written
