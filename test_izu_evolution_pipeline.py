"""Tests for izu_evolution_pipeline.py — run_pipeline, get_latest_sessions, cmd_report"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, PropertyMock, call

from izu_evolution_pipeline import (
    get_latest_sessions, run_pipeline, cmd_report,
    IZU_DIR, SESSION_DIR, DATA_DIR, OUTPUT_DIR,
)


# ═══════════════════════════════════════════
# get_latest_sessions 测试
# ═══════════════════════════════════════════

class TestGetLatestSessions:
    """get_latest_sessions——按修改时间获取最近session文件"""

    @patch("izu_evolution_pipeline.Path.glob")
    @patch("izu_evolution_pipeline.os.path.getmtime")
    def test_returns_sorted_by_mtime(self, mock_mtime, mock_glob):
        """应按修改时间降序排列"""
        mock_glob.side_effect = [
            [Path("/sessions/a.json"), Path("/sessions/b.json")],   # *.json
            [],                                                       # *.jsonl
        ]
        mock_mtime.side_effect = [100, 200]  # b 更新
        sessions = get_latest_sessions(limit=10)
        assert len(sessions) == 2
        assert sessions[0].name == "b.json"
        assert sessions[1].name == "a.json"

    @patch("izu_evolution_pipeline.Path.glob")
    @patch("izu_evolution_pipeline.os.path.getmtime")
    def test_limit_respected(self, mock_mtime, mock_glob):
        """limit 参数应限制返回数量"""
        mock_glob.side_effect = [
            [Path(f"/sessions/s{i}.json") for i in range(5)],
            [],
        ]
        mock_mtime.side_effect = list(reversed(range(5)))
        sessions = get_latest_sessions(limit=3)
        assert len(sessions) == 3

    @patch("izu_evolution_pipeline.Path.glob")
    def test_includes_both_json_and_jsonl(self, mock_glob):
        """应同时包含 .json 和 .jsonl 文件"""
        json_files = [Path(f"/sessions/{i}.json") for i in range(2)]
        jsonl_files = [Path(f"/sessions/{i}.jsonl") for i in range(2)]
        mock_glob.side_effect = [json_files, jsonl_files]
        with patch("izu_evolution_pipeline.os.path.getmtime", return_value=100):
            sessions = get_latest_sessions(limit=10)
        assert len(sessions) == 4

    @patch("izu_evolution_pipeline.Path.glob")
    def test_empty_dir(self, mock_glob):
        """空目录返回空列表"""
        mock_glob.side_effect = [[], []]
        sessions = get_latest_sessions(limit=10)
        assert sessions == []


# ═══════════════════════════════════════════
# run_pipeline 测试
# ═══════════════════════════════════════════

class TestRunPipeline:
    """run_pipeline——完整进化管线的集成测试（全部mock）"""

    SESSION_DATA = {
        "session_id": "s1",
        "model": "test-model",
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "world", "finish_reason": "stop"},
        ],
    }

    def _make_mock_file(self, name="s1.json", data='{}'):
        f = MagicMock()
        f.name = name
        f.stem = name.replace(".json", "").replace(".jsonl", "")
        f.read_text.return_value = data
        return f

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_empty_sessions(self, mock_open_file, mock_json_load, mock_json_dump,
                            mock_json_loads, mock_get_sessions, mock_outdir):
        """无session时返回空结果"""
        mock_get_sessions.return_value = []
        result = run_pipeline()
        assert result["sessions_processed"] == 0
        assert result["total_steps"] == 0
        mock_json_dump.assert_not_called()

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_parses_session_files(self, mock_open_file, mock_json_load,
                                  mock_json_dump, mock_json_loads,
                                  mock_get_sessions, mock_outdir):
        """应解析session文件并计数"""
        mock_get_sessions.return_value = [self._make_mock_file("test_session.json")]
        mock_json_loads.return_value = self.SESSION_DATA
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[], high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()
                result = run_pipeline()

        assert result["sessions_processed"] == 1

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_handles_parse_exception(self, mock_open_file, mock_json_load,
                                     mock_json_dump, mock_json_loads,
                                     mock_get_sessions, mock_outdir):
        """解析异常应跳过该文件"""
        mock_file = self._make_mock_file("bad.json")
        mock_file.read_text.side_effect = json.JSONDecodeError("bad json", "", 0)
        mock_get_sessions.return_value = [mock_file]
        mock_json_loads.side_effect = json.JSONDecodeError("bad", "", 0)

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            MockCreditScorer.return_value = MagicMock()
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()
                result = run_pipeline()
        assert result["sessions_processed"] == 0

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_credit_scoring_invoked(self, mock_open_file, mock_json_load,
                                    mock_json_dump, mock_json_loads,
                                    mock_get_sessions, mock_outdir):
        """应调用 CreditScorer.score_trajectory"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = self.SESSION_DATA
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        mock_step = MagicMock(role="assistant", content="hello",
                              credit_score=0.8, tool_name=None)
        mock_scored = MagicMock(steps=[mock_step], high_credit_steps=[mock_step],
                                rise_segments=[])

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = mock_scored
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()
                result = run_pipeline()

        assert result["sessions_processed"] == 1
        mock_scorer.score_trajectory.assert_called()

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_balanced_sampler_invoked(self, mock_open_file, mock_json_load,
                                      mock_json_dump, mock_json_loads,
                                      mock_get_sessions, mock_outdir):
        """应调用 BalancedSampler.record 和 save_state"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = {
            "session_id": "s1",
            "messages": [
                {"role": "user", "content": "帮我写一个程序"},
                {"role": "assistant", "content": "好的", "finish_reason": "stop"},
            ],
        }
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[
                    MagicMock(role="user", content="帮我写一个程序",
                              credit_score=0.5, tool_name=None),
                    MagicMock(role="assistant", content="好的",
                              credit_score=0.6, tool_name=None),
                ],
                high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                mock_sampler = MagicMock()
                MockSampler.return_value = mock_sampler
                run_pipeline()

        mock_sampler.record.assert_called()
        mock_sampler.save_state.assert_called_once()

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_topology_file_read_and_write(self, mock_open_file, mock_json_load,
                                          mock_json_dump, mock_json_loads,
                                          mock_get_sessions, mock_outdir):
        """应读取/创建topology数据并写入"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = self.SESSION_DATA

        mock_topo_data = {"agents": {}, "last_evolution": None, "total_evolutions": 0}
        mock_json_load.return_value = mock_topo_data

        step_user = MagicMock(role="user", content="hi", credit_score=0.5, tool_name=None)
        step_asst = MagicMock(role="assistant", content="hello", credit_score=0.7, tool_name=None)

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[step_user, step_asst], high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()

                with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    run_pipeline()

        mock_json_dump.assert_called()
        assert mock_json_dump.call_count >= 1

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_report_written(self, mock_open_file, mock_json_load,
                            mock_json_dump, mock_json_loads,
                            mock_get_sessions, mock_outdir):
        """应生成进化报告文件"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = self.SESSION_DATA
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[MagicMock(role="user", content="hi", credit_score=0.5, tool_name=None)],
                high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()

                with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    mock_report_path = MagicMock()
                    mock_outdir.__truediv__.return_value = mock_report_path
                    run_pipeline()

        mock_report_path.write_text.assert_called_once()
        written_content = mock_report_path.write_text.call_args[0][0]
        assert "进化循环报告" in written_content

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_weakness_summary_in_result(self, mock_open_file, mock_json_load,
                                        mock_json_dump, mock_json_loads,
                                        mock_get_sessions, mock_outdir):
        """result 应包含 weaknesses_recorded"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = self.SESSION_DATA
        mock_json_load.return_value = {
            "agents": {
                "test_agent": {
                    "performance_history": {"total_tasks_completed": 0, "avg_quality_score": 0.5},
                    "evolution_state": {
                        "current_generation": 0,
                        "identified_weaknesses": ["structural_complete", "conciseness"],
                        "prompt_adjustments_applied": [],
                        "last_verified_at": None,
                    },
                }
            },
            "last_evolution": None,
            "total_evolutions": 0,
        }

        step = MagicMock(role="user", content="hi", credit_score=0.5, tool_name=None)
        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[step], high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()
                with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    result = run_pipeline()

        assert "weaknesses_recorded" in result
        assert "structural_complete" in result["weaknesses_recorded"]
        assert "conciseness" in result["weaknesses_recorded"]

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_task_type_classification(self, mock_open_file, mock_json_load,
                                      mock_json_dump, mock_json_loads,
                                      mock_get_sessions, mock_outdir):
        """不同user消息应被正确分类"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = {
            "session_id": "s1",
            "messages": [
                {"role": "user", "content": "帮我研究一下AI的发展趋势"},
                {"role": "assistant", "content": "好的", "finish_reason": "stop"},
            ],
        }
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        step_user = MagicMock(role="user", content="帮我研究一下AI的发展趋势",
                              credit_score=0.5, tool_name=None)
        step_asst = MagicMock(role="assistant", content="好的",
                              credit_score=0.6, tool_name=None)

        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[step_user, step_asst], high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                mock_sampler = MagicMock()
                MockSampler.return_value = mock_sampler
                with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    run_pipeline()

        recorded = mock_sampler.record.call_args_list
        task_types = [c[0][0] for c in recorded]
        assert "research" in task_types

    @patch("izu_evolution_pipeline.OUTPUT_DIR")
    @patch("izu_evolution_pipeline.get_latest_sessions")
    @patch("izu_evolution_pipeline.json.loads")
    @patch("izu_evolution_pipeline.json.dump")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_topo_file_not_exists_creates_new(self, mock_open_file, mock_json_load,
                                              mock_json_dump, mock_json_loads,
                                              mock_get_sessions, mock_outdir):
        """topo文件不存在时应创建新topology"""
        mock_get_sessions.return_value = [self._make_mock_file("s1.json")]
        mock_json_loads.return_value = self.SESSION_DATA
        mock_json_load.return_value = {"agents": {}, "last_evolution": None, "total_evolutions": 0}

        step = MagicMock(role="user", content="hi", credit_score=0.5, tool_name=None)
        with patch("izu_evolution_pipeline.CreditScorer") as MockCreditScorer:
            mock_scorer = MagicMock()
            MockCreditScorer.return_value = mock_scorer
            mock_scorer.score_trajectory.return_value = MagicMock(
                steps=[step], high_credit_steps=[], rise_segments=[],
            )
            with patch("izu_evolution_pipeline.BalancedSampler") as MockSampler:
                MockSampler.return_value = MagicMock()
                with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
                    mock_exists.return_value = False
                    run_pipeline()

        mock_json_dump.assert_called()


# ═══════════════════════════════════════════
# cmd_report 测试
# ═══════════════════════════════════════════

class TestCmdReport:
    """cmd_report——输出当前拓扑状态"""

    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_report_no_file(self, mock_open_file, mock_json_load, capsys):
        """topo文件不存在时应打印 '无拓扑数据'"""
        # DATA_DIR is a real Path; mock topo file existence
        with patch.object(Path, "exists", return_value=False):
            cmd_report()
        captured = capsys.readouterr()
        assert "无拓扑数据" in captured.out

    @patch("izu_evolution_pipeline.DATA_DIR")
    @patch("izu_evolution_pipeline.json.load")
    @patch("builtins.open")
    def test_report_with_data(self, mock_open_file, mock_json_load, mock_datadir, capsys):
        """有topo数据时应打印状态摘要"""
        topo_data = {
            "last_evolution": "2026-05-14T00:00:00",
            "total_evolutions": 5,
            "agents": {
                "a1": {
                    "performance_history": {"avg_quality_score": 0.85},
                    "credit_profile": {"avg_credit": 0.6},
                    "evolution_state": {"identified_weaknesses": ["conciseness", "consistency"]},
                },
                "a2": {
                    "performance_history": {"avg_quality_score": 0.75},
                    "credit_profile": {"avg_credit": 0.5},
                    "evolution_state": {"identified_weaknesses": ["url_validity"]},
                },
            },
        }
        mock_json_load.return_value = topo_data

        with patch("izu_evolution_pipeline.Path.exists") as mock_exists:
            mock_exists.return_value = True
            cmd_report()

        captured = capsys.readouterr()
        assert "进化引擎拓扑状态" in captured.out
        assert "总进化次数: 5" in captured.out
        assert "Agent数: 2" in captured.out
        assert "平均质量分" in captured.out
        assert "短板排行" in captured.out
        assert "conciseness" in captured.out
