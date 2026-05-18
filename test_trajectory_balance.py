"""Tests for trajectory_balance.py — TaskClassifier, BalancedSampler, bootstrap_from_trajectories"""

import pytest
import random as py_random
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

from trajectory_balance import (
    TaskClassifier, BalancedSampler, bootstrap_from_trajectories,
)


# ═══════════════════════════════════════════
# TaskClassifier 测试
# ═══════════════════════════════════════════

class TestTaskClassifier:
    """TaskClassifier.classify 和 classify_from_trajectory 测试"""

    def test_classify_research(self):
        """中文研究类关键词应映射为 research"""
        assert TaskClassifier.classify("这项研究需要深入分析") == "research"
        assert TaskClassifier.classify("我需要调查一下这个问题") == "research"

    def test_classify_search(self):
        """搜索类关键词应映射为 search"""
        assert TaskClassifier.classify("帮我查找资料") == "search"
        assert TaskClassifier.classify("search the web") == "search"

    def test_classify_coding(self):
        """编程类关键词应映射为 coding"""
        assert TaskClassifier.classify("帮我修复这个bug") == "coding"
        assert TaskClassifier.classify("fix this bug in main.py") == "coding"

    def test_classify_writing(self):
        """'写' → writing（排在 coding 规则之前）"""
        assert TaskClassifier.classify("帮我写一个Python脚本") == "writing"

    def test_classify_default_other(self):
        """无匹配关键词应返回 other"""
        assert TaskClassifier.classify("今天天气真好") == "other"
        assert TaskClassifier.classify("1234567890") == "other"

    def test_classify_case_insensitive(self):
        """分类应大小写不敏感"""
        assert TaskClassifier.classify("RESEARCH the problem") == "research"

    def test_classify_from_trajectory_with_step_objects(self):
        """从对象列表推断任务类型——找到第一个 user role 步骤"""
        step1 = MagicMock(role="system", content="system prompt")
        step2 = MagicMock(role="user", content="帮我修复这个排序算法")
        result = TaskClassifier.classify_from_trajectory([step1, step2])
        assert result == "coding"

    def test_classify_from_trajectory_with_dicts(self):
        """从 dict 列表推断任务类型"""
        steps = [
            {"role": "system", "content": "init"},
            {"role": "user", "content": "帮我搜索最新的AI论文"},
        ]
        result = TaskClassifier.classify_from_trajectory(steps)
        assert result == "search"

    def test_classify_from_trajectory_empty(self):
        """空列表返回 other"""
        assert TaskClassifier.classify_from_trajectory([]) == "other"

    def test_classify_from_trajectory_no_user_step(self):
        """无 user role 步骤时返回 other"""
        steps = [
            MagicMock(role="assistant", content="你好"),
            {"role": "tool", "content": "data"},
        ]
        result = TaskClassifier.classify_from_trajectory(steps)
        assert result == "other"

    def test_classify_chat_intent(self):
        """对话/聊天类关键词应映射为 chat"""
        assert TaskClassifier.classify("我想和你聊聊天") == "chat"
        assert TaskClassifier.classify("just a simple ask") == "chat"


# ═══════════════════════════════════════════
# BalancedSampler 核心逻辑测试
# ═══════════════════════════════════════════

@pytest.fixture
def sampler():
    """创建一个使用 mock 状态文件的采样器（避免访问真实文件系统）"""
    with patch("trajectory_balance.Path.exists", return_value=False):
        yield BalancedSampler(state_file="/tmp/.test_sampler_state.json")


class TestBalancedSamplerRecord:
    """BalancedSampler.record 和 record_from_trajectory 测试"""

    def test_record_success(self, sampler):
        """记录一次成功"""
        sampler.record("research", success=True)
        stats = sampler._stats["research"]
        assert stats["total"] == 1
        assert stats["success"] == 1
        assert stats["fail"] == 0
        assert stats["sampled"] == 1

    def test_record_fail(self, sampler):
        """记录一次失败"""
        sampler.record("coding", success=False)
        stats = sampler._stats["coding"]
        assert stats["total"] == 1
        assert stats["success"] == 0
        assert stats["fail"] == 1

    def test_record_multiple_types(self, sampler):
        """多种任务类型的统计互不影响"""
        sampler.record("research", success=True)
        sampler.record("coding", success=False)
        sampler.record("research", success=True)
        assert sampler._stats["research"]["total"] == 2
        assert sampler._stats["research"]["success"] == 2
        assert sampler._stats["coding"]["total"] == 1
        assert sampler._stats["coding"]["success"] == 0

    def test_record_from_trajectory(self, sampler):
        """从轨迹自动分类并记录"""
        steps = [{"role": "user", "content": "帮我搜索最新消息"}]
        sampler.record_from_trajectory(steps, completed=True)
        stats = sampler._stats["search"]
        assert stats["total"] == 1
        assert stats["success"] == 1


class TestBalancedSamplerQuery:
    """BalancedSampler.success_rate / get_weight / should_sample 测试"""

    def test_success_rate_no_data(self, sampler):
        """无数据时应返回 0.5（初始不确定值）"""
        assert sampler.success_rate("unknown") == 0.5

    def test_success_rate_100_percent(self, sampler):
        """全成功→1.0"""
        sampler.record("test", success=True, details="ok")
        assert sampler.success_rate("test") == 1.0

    def test_success_rate_0_percent(self, sampler):
        """全失败→0.0"""
        sampler.record("test", success=False)
        assert sampler.success_rate("test") == 0.0

    def test_success_rate_half(self, sampler):
        """一半成功→0.5"""
        sampler.record("test", success=True)
        sampler.record("test", success=False)
        assert sampler.success_rate("test") == 0.5

    def test_get_weight_no_data_default(self, sampler):
        """无数据应返回 DEFAULT_WEIGHT (1.0)"""
        assert sampler.get_weight("unknown") == 1.0

    def test_get_weight_low_success_high_weight(self, sampler):
        """成功率接近0 → 权重应接近或达到 MAX_WEIGHT 级别"""
        sampler.record("hard", success=False)
        sampler.record("hard", success=False)
        # rate=0 → ratio=0/0.3=0 → weight=max(0.2, 1*(2.0-0))=2.0
        weight = sampler.get_weight("hard")
        assert weight == pytest.approx(2.0)

    def test_get_weight_high_success_low_weight(self, sampler):
        """成功率100% → 权重应很低（简单任务减采样）"""
        for _ in range(5):
            sampler.record("easy", success=True)
        # rate=1.0 → ratio=(1-0.7)/(1-0.7)=1 → weight=max(0.2, 1*(1-1*0.7))=0.3
        weight = sampler.get_weight("easy")
        assert weight == pytest.approx(0.3)

    def test_get_weight_mid_range_default(self, sampler):
        """成功率在窗口内 [0.3,0.7] 应返回默认权重"""
        sampler.record("mid", success=True)
        sampler.record("mid", success=False)
        # rate=0.5 ∈ [0.3, 0.7] → 1.0
        assert sampler.get_weight("mid") == 1.0

    def test_should_sample_weight_ge_1_true(self, sampler):
        """权重≥1.0 时应始终返回 True（不受 random 影响）"""
        sampler.record("low", success=False)  # weight=2.0
        # 即使 random=0.999（接近1），weight≥1 仍 true
        random_orig = py_random.random
        try:
            import trajectory_balance as tb_mod
            # should_sample 内部 import random，patch random.random
            with patch("random.random", return_value=0.999):
                assert sampler.should_sample("low") is True
        finally:
            pass

    def test_should_sample_weight_lt_1_probabilistic(self, sampler):
        """权重<1.0 时依赖 random.random"""
        for _ in range(5):
            sampler.record("high", success=True)  # weight=0.3
        with patch("random.random", return_value=0.1):  # 0.1 < 0.3 → True
            assert sampler.should_sample("high") is True
        with patch("random.random", return_value=0.5):  # 0.5 > 0.3 → False
            assert sampler.should_sample("high") is False


class TestBalancedSamplerPriority:
    """BalancedSampler.get_priority / enqueue / dequeue 测试"""

    def test_get_priority_no_data(self, sampler):
        """无数据时返回 0.5 中等优先级"""
        assert sampler.get_priority("unknown") == 0.5

    def test_get_priority_undersampled_high(self, sampler):
        """低成功率+低采样比例→高优先级"""
        sampler.record("rare", success=False)
        # weight=2.0, under_sampled_penalty=max(0, 1-1/1)=0 → 2.0*(0.5+0.5*0)=1.0
        prio = sampler.get_priority("rare")
        assert prio == pytest.approx(2.0 * 0.5)

    def test_enqueue_dequeue_order(self, sampler):
        """enqueue 后 dequeue 应按优先级降序取出"""
        sampler.record("easy", success=True)   # weight=0.3
        sampler.record("hard", success=False)   # weight=2.0
        sampler.enqueue("easy", base_priority=1.0)
        sampler.enqueue("hard", base_priority=1.0)
        result = sampler.dequeue(2)
        # 先出 hard（优先级高），再出 easy
        assert result == ["hard", "easy"]

    def test_dequeue_limit(self, sampler):
        """dequeue(n) 不应超过队列长度"""
        sampler.enqueue("test", base_priority=1.0)
        result = sampler.dequeue(5)
        assert len(result) == 1

    def test_queue_empty_default(self, sampler):
        """新采样器队列应为空"""
        assert sampler.queue_empty() is True

    def test_enqueue_makes_not_empty(self, sampler):
        """enqueue 后队列不应为空"""
        sampler.enqueue("test", base_priority=1.0)
        assert sampler.queue_empty() is False

    def test_dequeue_empties_queue(self, sampler):
        """dequeue 所有元素后队列应为空"""
        sampler.enqueue("a", base_priority=1.0)
        sampler.dequeue(1)
        assert sampler.queue_empty() is True


class TestBalancedSamplerPersistence:
    """BalancedSampler._load_state / save_state 测试（mock 文件 IO）"""

    @patch("trajectory_balance.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"stats": {"research": {"total": 5, "success": 3, "fail": 2, "sampled": 3, "last_updated": "2026-01-01T00:00:00"}}}')
    def test_load_state_restores_stats(self, mock_file, mock_exists):
        """_load_state 应恢复之前保存的统计"""
        s = BalancedSampler(state_file="/fake/state.json")
        assert s._stats["research"]["total"] == 5
        assert s._stats["research"]["success"] == 3
        assert s._stats["research"]["fail"] == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("trajectory_balance.Path.mkdir")
    def test_save_state_writes_json(self, mock_mkdir, mock_file):
        """save_state 应写入 JSON 到文件"""
        s = BalancedSampler(state_file="/fake/state.json")
        s.record("test", success=True)
        s.save_state()
        # 验证 open 被调用（写入模式）
        written = "".join(
            call[0][0] for call in mock_file().write.call_args_list
        )
        assert "test" in written
        assert "stats" in written

    @patch("trajectory_balance.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="corrupted json{{{")
    def test_load_state_bad_json_does_not_crash(self, mock_file, mock_exists):
        """损坏的状态文件不应抛出异常"""
        s = BalancedSampler(state_file="/fake/state.json")
        # 应成功初始化为空统计
        assert s._stats["anything"]["total"] == 0


class TestBalancedSamplerReport:
    """BalancedSampler.report 测试"""

    def test_report_empty(self, sampler):
        """无数据时报告应包含 '无任务记录'"""
        report = sampler.report()
        assert "无任务记录" in report

    def test_report_with_data(self, sampler):
        """有数据时报告应包含任务类型详情"""
        sampler.record("research", success=True)
        sampler.record("coding", success=False)
        report = sampler.report()
        assert "research" in report
        assert "总任务数: 2" in report
        assert "任务类型数: 2" in report

    def test_report_under_sampled_section(self, sampler):
        """低成功率任务应在 '欠采样' 节中出现"""
        sampler.record("hard", success=False)  # weight=2.0 > 1.5
        report = sampler.report()
        assert "欠采样任务" in report
        assert "hard" in report


# ═══════════════════════════════════════════
# bootstrap_from_trajectories 测试
# ═══════════════════════════════════════════

class TestBootstrapFromTrajectories:
    """bootstrap_from_trajectories 测试"""

    def test_bootstrap_creates_sampler(self):
        """从空轨迹列表应创建默认采样器"""
        with patch("trajectory_balance.Path.exists", return_value=False):
            with patch("trajectory_balance.Path.mkdir"):
                with patch("builtins.open", new_callable=mock_open):
                    s = bootstrap_from_trajectories([])
        assert isinstance(s, BalancedSampler)

    def test_bootstrap_processes_trajectories(self):
        """带轨迹列表时应记录并保存"""
        t1 = MagicMock(steps=[MagicMock(role="user", content="搜索最新消息")], completed=True)
        with patch("trajectory_balance.Path.exists", return_value=False):
            with patch("trajectory_balance.Path.mkdir"):
                with patch("builtins.open", new_callable=mock_open):
                    s = bootstrap_from_trajectories([t1])
        assert len(s._stats) > 0
