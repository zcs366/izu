"""Tests for izu_session_memory.py — decay_score, session_info, compact_session, CLI commands"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call
from datetime import datetime

from izu_session_memory import (
    decay_score, state_str, count_turns, session_info,
    parse_session, compact_session,
    HERMES, MEMORY_FILE, SESSIONS, DECAY_HALF_LIFE,
    FORGET_THRESHOLD, COMPACT_THRESHOLD,
)

# 对于 CLI 命令，用 import 整个模块以便 patch module-level globals
import izu_session_memory as ism


# ═══════════════════════════════════════════
# decay_score 测试
# ═══════════════════════════════════════════

class TestDecayScore:
    """decay_score 函数测试"""

    def test_persistent_always_one(self):
        """persistent=True 始终返回 1.0"""
        assert decay_score(1000, persistent=True) == 1.0
        assert decay_score(0, persistent=True) == 1.0
        assert decay_score(999999, importance=0.1, persistent=True) == 1.0

    def test_zero_age(self):
        """age=0 且非 persistent 时，只受 importance 和 accesses 影响"""
        # td=0.5**0=1.0, ab=1.0, imp=1.0 → min(1, max(0, 1.0*1.0*1.0))=1.0
        assert decay_score(0, importance=1.0, accesses=0) == 1.0

    def test_one_half_life(self):
        """age=DECAY_HALF_LIFE(24h) → td=0.5，importance=1.0 → 0.5"""
        score = decay_score(DECAY_HALF_LIFE)
        assert score == pytest.approx(0.5, abs=0.01)

    def test_two_half_lives(self):
        """age=48h → td=0.25"""
        score = decay_score(DECAY_HALF_LIFE * 2)
        assert score == pytest.approx(0.25, abs=0.01)

    def test_high_accesses_boost(self):
        """多次访问应有小幅增强效果"""
        no_access = decay_score(12, accesses=0)
        many_access = decay_score(12, accesses=10)
        assert many_access > no_access

    def test_accesses_capped_at_10(self):
        """accesses 应被 cap 在 10"""
        capped = decay_score(12, accesses=100)
        ten = decay_score(12, accesses=10)
        assert capped == pytest.approx(ten)

    def test_importance_boosts_score(self):
        """importance>1 应放大分数"""
        high_imp = decay_score(24, importance=1.5)
        normal = decay_score(24, importance=1.0)
        assert high_imp > normal

    def test_score_clamped_zero(self):
        """极老条目应被 clamp 到 0.0"""
        score = decay_score(1_000_000, importance=0.1)
        assert score == 0.0

    def test_score_clamped_one(self):
        """新条目不应超过 1.0"""
        score = decay_score(0, importance=2.0, accesses=100)
        assert score == 1.0

    def test_very_old_with_persistent(self):
        """非常老的 persistent 条目仍为 1.0"""
        assert decay_score(100000, persistent=True) == 1.0


class TestStateStr:
    """state_str 辅助函数测试"""

    def test_active(self):
        """score≥0.7 返回活跃"""
        assert "活跃" in state_str(0.7)
        assert "活跃" in state_str(1.0)

    def test_fading(self):
        """score 在 [FORGET_THRESHOLD, 0.7) 返回渐弱"""
        assert "渐弱" in state_str(0.5)
        assert "渐弱" in state_str(FORGET_THRESHOLD)

    def test_forget(self):
        """score < FORGET_THRESHOLD 返回待遗忘"""
        assert "待遗忘" in state_str(0.0)
        assert "待遗忘" in state_str(FORGET_THRESHOLD - 0.01)


# ═══════════════════════════════════════════
# count_turns / session_info 测试（mock 文件 IO）
# ═══════════════════════════════════════════

class TestCountTurns:
    def test_count_turns_basic(self):
        """正确统计轮数（每2个 role 标记为1轮）"""
        data = '\n'.join([
            '{"role": "user", "content": "hello"}',
            '{"role": "assistant", "content": "world"}',
            '{"role": "user", "content": "again"}',
            '{"role": "assistant", "content": "ok"}',
        ])
        with patch("builtins.open", mock_open(read_data=data)):
            assert count_turns(Path("/f/s.json")) == 2

    def test_count_turns_empty(self):
        """空文件返回 0"""
        with patch("builtins.open", mock_open(read_data="")):
            assert count_turns(Path("/f/empty.json")) == 0

    def test_count_turns_no_role_lines(self):
        """无 role 字段返回 0"""
        with patch("builtins.open", mock_open(read_data='{"key": "val"}')):
            assert count_turns(Path("/f/bad.json")) == 0

    def test_count_turns_read_error(self):
        """文件读取异常返回 0"""
        with patch("builtins.open", side_effect=OSError):
            assert count_turns(Path("/nonexistent.json")) == 0


class TestSessionInfo:
    @patch("izu_session_memory.count_turns", return_value=10)
    @patch("izu_session_memory.os.path.getmtime", return_value=1_000_000)
    def test_session_info_basic(self, mock_mtime, mock_turns):
        """session_info 应返回结构化信息"""
        info = session_info(Path("/sessions/test.json"))
        assert info["session"] == "test"
        assert info["turns"] == 10
        assert info["age_hours"] > 0
        assert "state" in info
        assert "score" in info
        assert "needs_compact" in info
        assert "candidate" in info

    @patch("izu_session_memory.count_turns", return_value=100)
    @patch("izu_session_memory.os.path.getmtime", return_value=datetime.now().timestamp())
    def test_session_info_needs_compact(self, mock_mtime, mock_turns):
        """turns ≥ COMPACT_THRESHOLD 时 needs_compact=True"""
        info = session_info(Path("/sessions/big.json"))
        assert info["needs_compact"] is True

    @patch("izu_session_memory.count_turns", return_value=5)
    @patch("izu_session_memory.os.path.getmtime", return_value=datetime.now().timestamp())
    def test_session_info_not_needs_compact(self, mock_mtime, mock_turns):
        """turns < COMPACT_THRESHOLD 时 needs_compact=False"""
        info = session_info(Path("/sessions/small.json"))
        assert info["needs_compact"] is False

    @patch("izu_session_memory.count_turns", return_value=0)
    @patch("izu_session_memory.os.path.getmtime", return_value=1_000_000)
    def test_session_info_zero_turns(self, mock_mtime, mock_turns):
        """0轮会话仍是有效会话"""
        info = session_info(Path("/sessions/empty.json"))
        assert info["turns"] == 0
        assert info["score"] <= 1.0


# ═══════════════════════════════════════════
# parse_session 测试（mock Path.read_text）
# ═══════════════════════════════════════════

class TestParseSession:
    def test_parse_json_dict_with_messages(self):
        """解析 dict 格式的 JSON（含 messages 键）"""
        data = json.dumps({
            "messages": [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "world"},
            ]
        })
        with patch.object(Path, "read_text", return_value=data):
            msgs = parse_session(Path("/f/s.json"))
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"

    def test_parse_json_dict_with_conversation(self):
        """解析含 conversation 键的 JSON"""
        data = json.dumps({
            "conversation": [
                {"role": "user", "content": "hi"},
            ]
        })
        with patch.object(Path, "read_text", return_value=data):
            msgs = parse_session(Path("/f/s.json"))
        assert len(msgs) == 1

    def test_parse_json_lines(self):
        """逐行 JSON 格式"""
        data = '\n'.join([
            '{"role": "user", "content": "a"}',
            '{"role": "assistant", "content": "b"}',
        ])
        with patch.object(Path, "read_text", return_value=data):
            msgs = parse_session(Path("/f/s.json"))
        assert len(msgs) == 2

    def test_parse_invalid_json(self):
        """无效 JSON 应返回空列表"""
        with patch.object(Path, "read_text", return_value="not json at all"):
            msgs = parse_session(Path("/f/bad.json"))
        assert msgs == []

    def test_parse_empty_file(self):
        """空文件返回空列表"""
        with patch.object(Path, "read_text", return_value=""):
            msgs = parse_session(Path("/f/empty.json"))
        assert msgs == []


# ═══════════════════════════════════════════
# extract_key_content 测试（纯函数，无需 mock）
# ═══════════════════════════════════════════

class TestExtractKeyContent:
    def test_extract_user_intents(self):
        """user 消息含意图关键词应提取"""
        msgs = [
            {"role": "user", "content": "开干这个项目吧"},
            {"role": "user", "content": "帮我写一个测试脚本"},
        ]
        result = ism.extract_key_content(msgs)
        assert len(result["intents"]) >= 2

    def test_extract_assistant_decisions(self):
        """assistant 含决策词应提取"""
        msgs = [
            {"role": "assistant", "content": "因此: 我们应该采用方案A"},
        ]
        result = ism.extract_key_content(msgs)
        assert len(result["decisions"]) >= 1
        assert "因此" in result["decisions"][0]

    def test_extract_code_blocks(self):
        """assistant 中代码块应提取"""
        msgs = [
            {"role": "assistant", "content": "代码如下:\n```python\nx=1\n```\n"},
        ]
        result = ism.extract_key_content(msgs)
        assert len(result["code_blocks"]) >= 1

    def test_extract_urls(self):
        """assistant 中 URL 应提取"""
        msgs = [
            {"role": "assistant", "content": "请参考 https://example.com/doc"},
        ]
        result = ism.extract_key_content(msgs)
        assert "https://example.com/doc" in result["urls"]

    def test_extract_tool_calls(self):
        """tool_calls 应提取函数名"""
        msgs = [
            {"role": "assistant", "content": "searching...",
             "tool_calls": [{"function": {"name": "web_search"}}]},
        ]
        result = ism.extract_key_content(msgs)
        assert "web_search" in result["tool_actions"]

    def test_extract_tool_role_key_facts(self):
        """tool role 中长内容含文件/路径信息应提取"""
        msgs = [
            {"role": "tool", "content": "成功将数据写入 /mnt/c/data/result.txt，completed successfully in 3.2s，已保存文件到本地"},
        ]
        result = ism.extract_key_content(msgs)
        assert len(result["key_facts"]) >= 1

    def test_extract_content_list(self):
        """content 为 list 时提取 text"""
        msgs = [
            {"role": "user", "content": [{"type": "text", "text": "hello"}]},
        ]
        result = ism.extract_key_content(msgs)
        assert isinstance(result, dict)

    def test_extract_empty_msgs(self):
        """空消息列表返回空结构"""
        result = ism.extract_key_content([])
        assert result["intents"] == []
        assert result["decisions"] == []
        assert result["code_blocks"] == []


# ═══════════════════════════════════════════
# compact_session 测试
# ═══════════════════════════════════════════

@pytest.fixture
def mock_hermes(tmp_path):
    """临时 HERMES 目录避免污染真实文件系统"""
    hermes_dir = tmp_path / ".hermes"
    (hermes_dir / "memories" / "compacted").mkdir(parents=True)
    with patch("izu_session_memory.HERMES", hermes_dir):
        yield hermes_dir


class TestCompactSession:
    def test_compact_session_success(self, mock_hermes):
        """基本压缩流程应创建压缩文件"""
        data = json.dumps({
            "messages": [
                {"role": "user", "content": "帮我写一个脚本"},
                {"role": "assistant", "content": "因此: 方案如下\n```python\nx=1\n```"},
            ]
        })
        session_path = mock_hermes / "sessions" / "test_session.json"
        session_path.parent.mkdir(parents=True, exist_ok=True)
        session_path.write_text(data)

        result = compact_session(session_path)
        assert result.exists()
        assert "_compact.md" in result.name
        # 原始文件应被重命名为 .archived
        assert not session_path.exists()
        assert session_path.with_suffix(".archived").exists()

    def test_compact_session_unparseable(self, mock_hermes):
        """不可解析的 session 应抛出 ValueError"""
        session_path = mock_hermes / "sessions" / "bad.json"
        session_path.parent.mkdir(parents=True, exist_ok=True)
        session_path.write_text("bad data")
        with pytest.raises(ValueError, match="无法解析session"):
            compact_session(session_path)


# ═══════════════════════════════════════════
# CLI 命令测试（mock 模块级别的 SESSIONS 等）
# ═══════════════════════════════════════════

class TestCmdDecay:
    def test_cmd_decay_no_file(self):
        """MEMORY.md 不存在时应打印错误"""
        with patch.object(Path, "exists", return_value=False):
            with patch("izu_session_memory.print") as mock_print:
                ism.cmd_decay()
        mock_print.assert_called_with(f"❌ {MEMORY_FILE} not found")


class TestCmdCompact:
    def test_cmd_compact_by_name_not_found(self):
        """按名称压缩找不到时打印错误"""
        with patch.object(ism.SESSIONS.__class__, "glob", return_value=[]):
            with patch("izu_session_memory.print") as mock_print:
                ism.cmd_compact(name="nonexistent")
        mock_print.assert_any_call("❌ 未找到包含 'nonexistent' 的session")


# ═══════════════════════════════════════════
# 集成风格测试：用 tmp_path 构建真实目录+文件
# ═══════════════════════════════════════════

class TestIntegration:
    """使用真实临时目录的集成测试"""

    def test_decay_and_state_str_chain(self):
        """decay_score → state_str 链条：各状态边界"""
        assert "活跃" in state_str(decay_score(0))
        assert "待遗忘" in state_str(decay_score(1_000_000, importance=0.1))

    def test_compact_roundtrip(self, tmp_path):
        """完整压缩流程：解析→提取→写入→检查内容"""
        hermes_dir = tmp_path / "hermes"
        (hermes_dir / "memories" / "compacted").mkdir(parents=True)
        session_dir = hermes_dir / "sessions"
        session_dir.mkdir(parents=True)

        session_data = json.dumps({
            "messages": [
                {"role": "user", "content": "搜索最新的AI论文"},
                {"role": "assistant", "content": "因此: 推荐阅读attention is all you need\nhttps://arxiv.org/abs/1706.03762"},
            ]
        }, indent=2)
        session_path = session_dir / "ai_search.json"
        session_path.write_text(session_data)

        with patch("izu_session_memory.HERMES", hermes_dir):
            compact_path = compact_session(session_path)

        assert compact_path.exists()
        content = compact_path.read_text(encoding="utf-8")
        assert "ai_search" in content
        assert "attention" in content  # 决策/结论
        assert "arxiv" in content      # 引用链接

    def test_compact_5turns_roundtrip(self, tmp_path):
        """5轮会话压缩：多轮交流应有完整摘要"""
        hermes_dir = tmp_path / "hermes2"
        (hermes_dir / "memories" / "compacted").mkdir(parents=True)
        session_dir = hermes_dir / "sessions"
        session_dir.mkdir(parents=True)

        msgs = [
            {"role": "user", "content": "帮我写一个脚本"},
            {"role": "assistant", "content": "好的 开始写"},
            {"role": "user", "content": "需要处理文件"},
            {"role": "assistant", "content": "因此 我们这样处理"},
            {"role": "user", "content": "再添加一个功能"},
            {"role": "assistant", "content": "综上所述 最终方案确定"},
        ]
        session_path = session_dir / "coding_session.json"
        session_path.write_text(json.dumps({"messages": msgs}))

        with patch("izu_session_memory.HERMES", hermes_dir):
            compact_path = compact_session(session_path)

        assert compact_path.exists()
        content = compact_path.read_text(encoding="utf-8")
        assert "coding_session" in content

    def test_decay_boundary_values(self):
        """decay_score 边界：0 和 1 的 clamp 行为"""
        # 超大年龄 + 0 importance → clamp 到 0
        assert decay_score(1e9, importance=0.0) == 0.0
        # 超大年龄 + 很大 importance + persistent → 1.0
        assert decay_score(1e9, importance=10.0, persistent=True) == 1.0

    def test_session_info_from_real_file(self, tmp_path):
        """从真实 session 文件获取 session_info"""
        session_path = tmp_path / "sessions" / "real.json"
        session_path.parent.mkdir(parents=True)
        session_path.parent.parent.mkdir(parents=True, exist_ok=True)

        data = '\n'.join([
            '{"role": "user", "content": "hello"}',
            '{"role": "assistant", "content": "world"}',
        ])
        session_path.write_text(data)

        info = session_info(session_path)
        assert info["session"] == "real"
        assert info["turns"] == 1

    def test_extract_content_no_tool_calls_none(self):
        """tool_calls 字段缺失时不应报错"""
        msgs = [
            {"role": "assistant", "content": "hello"},
        ]
        result = ism.extract_key_content(msgs)
        assert result["tool_actions"] == []

    def test_extract_question_as_intent(self):
        """含问号的内容应被识别为意图"""
        msgs = [{"role": "user", "content": "什么是transformer架构?"}]
        result = ism.extract_key_content(msgs)
        assert len(result["intents"]) >= 1
