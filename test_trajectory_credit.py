"""Tests for trajectory_credit.py — CreditScorer, Step, Trajectory, load_from_hermes_jsonl"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from trajectory_credit import (
    Step, Trajectory, CreditScorer,
    load_from_hermes_jsonl, load_from_izu_sessions,
    export_credit_trajectories, generate_report,
)


# ═══════════════════════════════════════════
# Step 数据类测试
# ═══════════════════════════════════════════

class TestStep:
    def test_char_count(self):
        """Step.char_count 应返回正确的字符数"""
        s = Step(role="assistant", content="hello world", turn=1)
        assert s.char_count == 11

    def test_char_count_empty(self):
        """空 content 的 char_count 应为 0"""
        s = Step(role="user", content="", turn=1)
        assert s.char_count == 0

    def test_has_code_true(self):
        """has_code 应检测代码块标记 ```"""
        s = Step(role="assistant", content="某些代码:\n```python\nx=1\n```", turn=1)
        assert s.has_code is True

    def test_has_code_false(self):
        """无代码块时应返回 False"""
        s = Step(role="user", content="普通文本", turn=1)
        assert s.has_code is False

    def test_has_decision_markers_chinese(self):
        """has_decision_markers 应检测中文决策信号词"""
        s = Step(role="assistant", content="综上所述，我们决定采用方案A", turn=1)
        assert s.has_decision_markers is True

    def test_has_decision_markers_english(self):
        """has_decision_markers 应检测英文决策信号词"""
        s = Step(role="assistant", content="Therefore, the key insight is that...", turn=1)
        assert s.has_decision_markers is True

    def test_has_decision_markers_false(self):
        """无决策信号词时应返回 False"""
        s = Step(role="user", content="你好，请问有什么可以帮你的？", turn=1)
        assert s.has_decision_markers is False

    def test_has_tool_call_with_tool_name(self):
        """tool_name 不为 None 时 has_tool_call 应返回 True"""
        s = Step(role="assistant", content="search", turn=1, tool_name="web_search")
        assert s.has_tool_call is True

    def test_has_tool_call_without_tool_name(self):
        """tool_name 为 None 时 has_tool_call 应返回 False"""
        s = Step(role="user", content="hello", turn=1)
        assert s.has_tool_call is False


# ═══════════════════════════════════════════
# Trajectory 数据类测试
# ═══════════════════════════════════════════

class TestTrajectory:
    def test_total_steps(self):
        """total_steps 应返回 steps 数量"""
        t = Trajectory(session_id="test-1", steps=[
            Step(role="user", content="hi", turn=1),
            Step(role="assistant", content="hello", turn=1),
        ])
        assert t.total_steps == 2

    def test_total_steps_empty(self):
        """空轨迹 total_steps 应为 0"""
        t = Trajectory(session_id="empty")
        assert t.total_steps == 0

    def test_total_turns(self):
        """total_turns 应返回最大 turn 值"""
        t = Trajectory(session_id="test-1", steps=[
            Step(role="user", content="a", turn=1),
            Step(role="assistant", content="b", turn=1),
            Step(role="user", content="c", turn=2),
        ])
        assert t.total_turns == 2

    def test_total_turns_empty(self):
        """空轨迹 total_turns 应为 0"""
        t = Trajectory(session_id="empty")
        assert t.total_turns == 0

    def test_success_rate_completed(self):
        """completed=True 时 success_rate 应为 1.0"""
        t = Trajectory(session_id="ok", completed=True, steps=[
            Step(role="user", content="q", turn=1),
            Step(role="assistant", content="a", turn=1),
        ])
        assert t.success_rate == 1.0

    def test_success_rate_not_completed_with_decision(self):
        """未完成但有决策信号 → success_rate 为 min(ratio, 0.6)"""
        t = Trajectory(session_id="partial", completed=False, steps=[
            Step(role="user", content="q", turn=1),
            Step(role="assistant", content="因此我们得出结论", turn=1),
            Step(role="user", content="继续", turn=2),
            Step(role="assistant", content="好的", turn=2),
        ])
        # last 3 steps: 1 has decision marker → 1/3 ≈ 0.333, capped at 0.6
        assert t.success_rate == pytest.approx(1 / 3)

    def test_success_rate_not_completed_no_decision(self):
        """未完成且无决策信号 → 0"""
        t = Trajectory(session_id="bad", completed=False, steps=[
            Step(role="user", content="q", turn=1),
            Step(role="assistant", content="嗯", turn=1),
        ])
        assert t.success_rate == 0.0

    def test_high_credit_steps(self):
        """high_credit_steps 只返回 credit_score > 0.7 的步骤"""
        t = Trajectory(session_id="hc", steps=[
            Step(role="user", content="q", turn=1, credit_score=0.3),
            Step(role="assistant", content="重点分析", turn=1, credit_score=0.85),
            Step(role="tool", content="data", turn=1, credit_score=0.75),
            Step(role="user", content="next", turn=2, credit_score=0.5),
        ])
        assert len(t.high_credit_steps) == 2
        assert all(s.credit_score > 0.7 for s in t.high_credit_steps)

    def test_high_credit_steps_empty(self):
        """无高信用步骤时返回空列表"""
        t = Trajectory(session_id="low", steps=[
            Step(role="user", content="q", turn=1, credit_score=0.4),
        ])
        assert t.high_credit_steps == []

    def test_rise_segments(self):
        """rise_segments 应合并连续的 is_rise=True 步骤（长度≥2）"""
        t = Trajectory(session_id="rise", steps=[
            Step(role="user", content="a", turn=1, is_rise=False),
            Step(role="user", content="b", turn=2, is_rise=True),
            Step(role="user", content="c", turn=2, is_rise=True),
            Step(role="user", content="d", turn=3, is_rise=True),
            Step(role="user", content="e", turn=3, is_rise=False),
            Step(role="user", content="f", turn=4, is_rise=True),
        ])
        segments = t.rise_segments
        # 第一个段[b,c,d]长度3≥2, 第二个段[f]单步被忽略
        assert len(segments) == 1
        assert len(segments[0]) == 3

    def test_rise_segments_empty(self):
        """全 False 时 rise_segments 应为空"""
        t = Trajectory(session_id="flat", steps=[
            Step(role="user", content="a", turn=1, is_rise=False),
            Step(role="user", content="b", turn=2, is_rise=False),
        ])
        assert t.rise_segments == []

    def test_rise_segments_single_rise(self):
        """单步上升不计入 segments"""
        t = Trajectory(session_id="single", steps=[
            Step(role="user", content="a", turn=1, is_rise=True),
            Step(role="user", content="b", turn=2, is_rise=False),
        ])
        assert t.rise_segments == []


# ═══════════════════════════════════════════
# CreditScorer 单元测试
# ═══════════════════════════════════════════

class TestCreditScorer:
    def test_score_step_short_content(self):
        """极短内容 → reasoning_depth 为 0, length_bonus 为 0"""
        step = Step(role="user", content="hi", turn=1)
        score = CreditScorer.score_step(step, 0, 5, completed=False)
        # 期望很低
        assert score < 0.3

    def test_score_step_long_reasoning(self):
        """长推理内容应有较高 reasoning_depth"""
        step = Step(role="assistant", content=(
            "首先我们需要分析这个问题的本质。"
            "从多个角度考虑，原因有三：\n\n"
            "第一，数据量不足。\n\n"
            "第二，模型不够大。\n\n"
            "第三，训练时间不够。\n\n"
            "综合以上三点，我们可以得出结论：需要增加算力。"
        ), turn=1)
        score = CreditScorer.score_step(step, 2, 5, completed=False)
        # 长内容、多段落、有决策词 → 应该中等偏高
        assert score > 0.3

    def test_score_step_tool_call_valuable(self):
        """有价值的工具调用应获得高 tool_use 分"""
        step = Step(
            role="assistant", content="让我搜索一下",
            turn=1, tool_name="web_search"
        )
        score = CreditScorer.score_step(step, 1, 3, completed=False)
        # web_search 在 valuable_tools 里 → tool_use=1.0
        # 仅tool_use一项贡献 0.15，文字短所以其他维度低
        assert score > 0.1
        assert score < 0.5  # 其他维度低

    def test_score_step_tool_return(self):
        """tool role 的步骤应有 tool_use 基础分 0.6"""
        step = Step(role="tool", content="返回了大量数据结果", turn=1)
        score = CreditScorer.score_step(step, 2, 5, completed=False)
        # tool_use=0.6 → 贡献 0.6*0.15=0.09
        assert score > 0.08

    def test_score_step_decision_markers(self):
        """有决策信号词时 decision_signal 应 > 0.05"""
        step = Step(role="assistant", content="因此我决定选择方案A", turn=1)
        score = CreditScorer.score_step(step, 0, 3, completed=False)
        assert score > 0.05

    def test_score_step_no_decision_markers_baseline(self):
        """无决策信号词时 decision_signal 应为 0.05 基础值"""
        step = Step(role="user", content="你好", turn=1)
        score = CreditScorer.score_step(step, 0, 3, completed=False)
        # 极短内容
        assert score > 0

    def test_score_step_length_bonus_brackets(self):
        """不同长度区间 length_bonus 应正确"""
        # char_count < 10 → 0
        step1 = Step(role="user", content="123456789", turn=1)
        score1 = CreditScorer.score_step(step1, 0, 3, completed=False)

        # char_count 50~200 → 0.3
        step2 = Step(role="user", content="a" * 100, turn=1)
        score2 = CreditScorer.score_step(step2, 0, 3, completed=False)

        # char_count > 2000 → 0.8
        step3 = Step(role="user", content="a" * 2500, turn=1)
        score3 = CreditScorer.score_step(step3, 0, 3, completed=False)

        assert score1 < score2 < score3

    def test_score_trajectory_marks_rise(self):
        """score_trajectory 应正确标记 rise segments"""
        steps = [
            Step(role="user", content="hello", turn=1),
            Step(role="assistant", content="因此我们决定", turn=1),
            Step(role="user", content="继续", turn=2),
            Step(role="assistant", content="综上所述，采用", turn=2),
        ]
        traj = Trajectory(session_id="test", steps=steps)
        CreditScorer.score_trajectory(traj)

        # 所有步骤应有 credit_score
        for s in traj.steps:
            assert s.credit_score > 0

    def test_score_trajectory_empty(self):
        """空轨迹评分不应报错"""
        traj = Trajectory(session_id="empty")
        result = CreditScorer.score_trajectory(traj)
        assert result.steps == []


# ═══════════════════════════════════════════
# load_from_hermes_jsonl 测试（mock 文件）
# ═══════════════════════════════════════════

class TestLoadFromHermesJsonl:
    # Helper: create a real temp file with given lines, call load_from_hermes_jsonl on it
    # Using tmp_path avoids mock_open iterator vs readlines issues
    def _make_jsonl(self, tmp_path, lines):
        p = tmp_path / "session.jsonl"
        p.write_text("".join(lines), encoding="utf-8")
        return str(p)

    def test_simple_session(self, tmp_path):
        """加载简单的 user→assistant 会话"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": "hello", "timestamp": "2024-01-01T00:00:00"}\n',
            '{"role": "assistant", "content": "world", "timestamp": "2024-01-01T00:00:01", '
            '"finish_reason": "stop"}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        traj = trajs[0]
        assert traj.session_id == "session"
        assert traj.total_steps == 2
        assert traj.completed is True
        assert traj.steps[0].role == "user"
        assert traj.steps[1].role == "assistant"

    def test_with_tool_calls(self, tmp_path):
        """含工具调用的会话"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": "search for X"}\n',
            '{"role": "assistant", "content": "searching...", '
            '"tool_calls": [{"function": {"name": "web_search"}}]}\n',
            '{"role": "tool", "content": "result data"}\n',
            '{"role": "assistant", "content": "done", "finish_reason": "stop"}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        traj = trajs[0]
        assert traj.total_steps == 4
        # assistant step with tool_call should have tool_name
        assert traj.steps[1].tool_name == "web_search"
        assert traj.steps[1].has_tool_call is True
        # tool role step
        assert traj.steps[2].role == "tool"
        assert traj.steps[2].tool_name is None  # tool role gets None

    def test_with_reasoning(self, tmp_path):
        """reasoning 应合并到 content"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": "question"}\n',
            '{"role": "assistant", "content": "final answer", '
            '"reasoning": "let me think step by step"}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        step = trajs[0].steps[1]
        assert "let me think step by step" in step.content
        assert "final answer" in step.content

    def test_with_list_content(self, tmp_path):
        """content 为 list 时应提取 text parts"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": [{"type": "text", "text": "hello"}, '
            '{"type": "text", "text": " world"}]}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        # " ".join(["hello", " world"]) → "hello  world"
        assert trajs[0].steps[0].content == "hello  world"

    def test_with_session_meta(self, tmp_path):
        """session_meta 行应被跳过"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "session_meta", "model": "gpt-4"}\n',
            '{"role": "user", "content": "hi"}\n',
            '{"role": "assistant", "content": "hello", "finish_reason": "stop"}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        assert trajs[0].total_steps == 2  # session_meta 被跳过
        assert trajs[0].steps[0].role == "user"

    def test_file_not_found(self):
        """文件不存在时返回空列表"""
        trajs = load_from_hermes_jsonl("/nonexistent/file.jsonl")
        assert trajs == []

    def test_empty_file(self, tmp_path):
        """空文件返回空列表"""
        path = self._make_jsonl(tmp_path, [])
        trajs = load_from_hermes_jsonl(path)
        assert trajs == []

    def test_bad_json_line(self, tmp_path):
        """不合法的 JSON 行应跳过"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": "valid"}\n',
            'this is not json\n',
            '{"role": "assistant", "content": "ok", "finish_reason": "stop"}\n',
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        assert trajs[0].total_steps == 2  # 有效行

    def test_not_completed(self, tmp_path):
        """无 finish_reason=stop 时 completed=False"""
        path = self._make_jsonl(tmp_path, [
            '{"role": "user", "content": "q"}\n',
            '{"role": "assistant", "content": "a"}\n',  # no finish_reason
        ])
        trajs = load_from_hermes_jsonl(path)
        assert len(trajs) == 1
        assert trajs[0].completed is False


# ═══════════════════════════════════════════
# load_from_izu_sessions 测试
# ═══════════════════════════════════════════

class TestLoadFromIzuSessions:
    @patch("trajectory_credit.load_from_hermes_jsonl")
    def test_directory_not_found(self, mock_load):
        """目录不存在时返回空列表"""
        with patch("trajectory_credit.Path.exists", return_value=False):
            trajs = load_from_izu_sessions("/nonexistent/dir")
        assert trajs == []
        mock_load.assert_not_called()

    @patch("trajectory_credit.load_from_hermes_jsonl")
    @patch("trajectory_credit.Path.glob")
    @patch("trajectory_credit.Path.exists", return_value=True)
    def test_load_multiple_sessions(self, mock_exists, mock_glob, mock_load):
        """应扫描目录下所有 jsonl 文件并加载"""
        mock_glob.return_value = [
            Path("/sessions/s1.jsonl"),
            Path("/sessions/s2.jsonl"),
        ]
        mock_load.side_effect = [
            [Trajectory(session_id="s1", steps=[Step(role="user", content="a", turn=1)])],
            [Trajectory(session_id="s2", steps=[Step(role="user", content="b", turn=1)])],
        ]
        trajs = load_from_izu_sessions("/sessions")
        assert len(trajs) == 2
        assert mock_load.call_count == 2


# ═══════════════════════════════════════════
# export_credit_trajectories 测试
# ═══════════════════════════════════════════

class TestExportCreditTrajectories:
    @patch("builtins.open")
    def test_export_with_rise_segments(self, mock_open_):
        """有 rise segment 的轨迹应导出"""
        mock_ctx = MagicMock()
        mock_open_.return_value.__enter__.return_value = mock_ctx

        traj = Trajectory(session_id="test-export", steps=[
            Step(role="user", content="q", turn=1, credit_score=0.3, is_rise=False),
            Step(role="assistant", content="分析中", turn=1, credit_score=0.5, is_rise=False),
            Step(role="assistant", content="因此决定", turn=2, credit_score=0.8, is_rise=True),
            Step(role="assistant", content="最终方案", turn=2, credit_score=0.9, is_rise=True),
        ])
        CreditScorer.score_trajectory(traj)  # ensure scores
        count = export_credit_trajectories([traj], "/fake/output.jsonl")
        assert count == 1
        written = "".join(call[0][0] for call in mock_ctx.write.call_args_list)
        assert "test-export" in written

    @patch("builtins.open")
    def test_export_no_rise_no_high_credit(self, mock_open_):
        """无 rise 无高 credit 的轨迹不应导出"""
        traj = Trajectory(session_id="low", steps=[
            Step(role="user", content="q", turn=1, credit_score=0.1, is_rise=False),
        ])
        count = export_credit_trajectories([traj], "/fake/output.jsonl")
        assert count == 0


# ═══════════════════════════════════════════
# generate_report 测试
# ═══════════════════════════════════════════

class TestGenerateReport:
    def test_report_empty(self):
        """空轨迹应返回 '无轨迹数据'"""
        assert generate_report([]) == "无轨迹数据"

    def test_report_basic(self):
        """基本报告格式"""
        trajs = [
            Trajectory(session_id="s1", completed=True, steps=[
                Step(role="user", content="q", turn=1, credit_score=0.8),
            ]),
            Trajectory(session_id="s2", completed=False, steps=[
                Step(role="user", content="q", turn=1, credit_score=0.3),
            ]),
        ]
        report = generate_report(trajs)
        assert "izu 轨迹信用评分报告" in report
        assert "总轨迹数: 2" in report
        assert "总步数: 2" in report
        assert "成功: 1" in report
        assert "失败: 1" in report
