"""Tests for izu_memory_maintenance.py — run, main (steps 1-4, midnight/regular scheduling)"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
from datetime import datetime

from izu_memory_maintenance import (
    run, main, IZU_DIR, HERMES_HOME, OUTPUT_DIR
)


# ═══════════════════════════════════════════
# run 函数测试
# ═══════════════════════════════════════════

class TestRun:
    """run 辅助函数测试"""

    @patch("izu_memory_maintenance.subprocess.run")
    def test_run_calls_subprocess(self, mock_subproc):
        """run 应调用 izu_session_memory.py 并传入指定参数"""
        mock_subproc.return_value.stdout = "compact done"
        mock_subproc.return_value.stderr = ""
        result = run("compact")
        mock_subproc.assert_called_once()
        args = mock_subproc.call_args[0][0]
        assert str(IZU_DIR / "izu_session_memory.py") in args
        assert "compact" in args
        assert "compact done" in result

    @patch("izu_memory_maintenance.subprocess.run")
    def test_run_returns_stdout_and_stderr(self, mock_subproc):
        """run 应合并 stdout 和 stderr 返回"""
        mock_subproc.return_value.stdout = "output\n"
        mock_subproc.return_value.stderr = "warnings\n"
        result = run("purge")
        assert "output" in result
        assert "warnings" in result

    @patch("izu_memory_maintenance.subprocess.run")
    def test_run_uses_correct_cwd(self, mock_subproc):
        """run 应在 IZU_DIR 目录下执行"""
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""
        run("report")
        assert mock_subproc.call_args[1]["cwd"] == str(IZU_DIR)

    @patch("izu_memory_maintenance.subprocess.run")
    def test_run_uses_sys_executable(self, mock_subproc):
        """run 应使用 sys.executable"""
        import sys
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""
        run("compact")
        args = mock_subproc.call_args[0][0]
        assert args[0] == sys.executable


# ═══════════════════════════════════════════
# main 函数测试 — 常规时间
# ═══════════════════════════════════════════

FIXED_DT = datetime(2025, 1, 15, 14, 30)  # 14:30, not midnight
FIXED_DT_MIDNIGHT = datetime(2025, 1, 15, 0, 0)
FIXED_DT_6AM = datetime(2025, 1, 15, 6, 0)


class TestMainRegular:
    """main 在非凌晨时间运行"""

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_runs_compact_and_purge(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """main 应依次执行 compact 和 purge"""
        mock_dt.now.return_value = FIXED_DT
        mock_subproc.return_value.stdout = "ok"
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        main()

        call_args_list = [c[0][0] for c in mock_subproc.call_args_list]
        compact_calls = [a for a in call_args_list if "compact" in str(a)]
        purge_calls = [a for a in call_args_list if "purge" in str(a)]
        assert len(compact_calls) == 1
        assert len(purge_calls) == 1

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_generates_report(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """main 应生成健康报告"""
        mock_dt.now.return_value = FIXED_DT
        mock_subproc.return_value.stdout = "report content\n"
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        report_path = MagicMock(spec=Path)
        mock_outdir.__truediv__.return_value = report_path

        main()

        report_path.write_text.assert_called_once()
        written = report_path.write_text.call_args[0][0]
        assert "记忆系统健康报告" in written
        assert "report content" in written

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_appends_working_memory(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """报告应附加工作内存快照"""
        mock_dt.now.return_value = FIXED_DT
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        report_path = MagicMock(spec=Path)
        mock_outdir.__truediv__.return_value = report_path

        main()

        call_args_list = [c[0][0] for c in mock_subproc.call_args_list]
        wm_calls = [a for a in call_args_list if "izu_working_memory.py" in str(a)]
        assert len(wm_calls) == 1

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_regular_skip_self_model(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """非凌晨时间不应执行 Self Model 快照"""
        mock_dt.now.return_value = FIXED_DT
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        main()

        call_args_list = [c[0][0] for c in mock_subproc.call_args_list]
        sm_calls = [a for a in call_args_list if "izu_self_model.py" in str(a)]
        assert len(sm_calls) == 0

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_outputs_start_and_end_messages(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """main 应打印维护开始和完成信息"""
        mock_dt.now.return_value = FIXED_DT
        # strftime is called in the main() function on datetime.now() result
        # Since mock_dt.now() returns FIXED_DT (a real datetime), strftime works natively
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        main()

        call_args = " ".join(str(c) for c in mock_print.call_args_list)
        assert "记忆维护流水线" in call_args
        assert "记忆维护完成" in call_args


# ═══════════════════════════════════════════
# main 函数测试 — 凌晨时间
# ═══════════════════════════════════════════

class TestMainMidnight:
    """main 在凌晨/6点运行"""

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_at_midnight_triggers_self_model(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """0点时应触发 Self Model 快照"""
        mock_dt.now.return_value = FIXED_DT_MIDNIGHT
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        main()

        call_args_list = [c[0][0] for c in mock_subproc.call_args_list]
        sm_calls = [a for a in call_args_list if "izu_self_model.py" in str(a)]
        assert len(sm_calls) == 1

    @patch("izu_memory_maintenance.subprocess.run")
    @patch("izu_memory_maintenance.datetime")
    @patch("izu_memory_maintenance.OUTPUT_DIR")
    @patch("builtins.print")
    def test_main_at_6am_triggers_self_model(self, mock_print, mock_outdir, mock_dt, mock_subproc):
        """6点时应触发 Self Model 快照"""
        mock_dt.now.return_value = FIXED_DT_6AM
        mock_subproc.return_value.stdout = ""
        mock_subproc.return_value.stderr = ""

        mock_outdir.mkdir.return_value = None
        mock_outdir.__truediv__.return_value = MagicMock(spec=Path)

        main()

        call_args_list = [c[0][0] for c in mock_subproc.call_args_list]
        sm_calls = [a for a in call_args_list if "izu_self_model.py" in str(a)]
        assert len(sm_calls) == 1
