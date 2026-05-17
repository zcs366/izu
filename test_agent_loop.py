"""
agent_loop.py 单元测试
验证 Async Generator、CostLadder、StreamingToolExecutor 的核心行为
"""
import asyncio
import pytest
from izu.agent_loop import (
    AgentLoop, QueryParams, CostLadder, StreamingToolExecutor,
    Event, EventType, TerminalReason, ToolCall, ToolSafety,
)


class TestCostLadder:
    def test_normal(self):
        cl = CostLadder(10000)
        assert cl.assess(1000) == "normal"

    def test_warning(self):
        cl = CostLadder(10000)
        assert cl.assess(7500) == "warning"

    def test_compact(self):
        cl = CostLadder(10000)
        assert cl.assess(8800) == "compact"

    def test_blocking(self):
        cl = CostLadder(10000)
        assert cl.assess(9600) == "blocking"

    def test_l0_truncate(self):
        cl = CostLadder(10000)
        msgs = [{"role": "user", "content": f"msg{i}"} for i in range(100)]
        result = cl.compact_l0(msgs, keep=10)
        assert len(result) == 10
        assert "L0_truncate" in cl.applied_levels

    def test_l1_clear_stale(self):
        cl = CostLadder(10000)
        msgs = [
            {"role": "user", "content": "hello"},
            {"role": "tool", "content": "[Cleared] old result"},
            {"role": "user", "content": "world"},
        ]
        result = cl.compact_l1(msgs)
        assert len(result) == 2
        assert "[Cleared]" not in str(result)

    def test_l2_summarize(self):
        cl = CostLadder(10000)
        msgs = [{"role": "user", "content": f"msg{i}"} for i in range(50)]
        result, summary = cl.compact_l2(msgs)
        assert len(result) == 5
        assert "摘要" in summary


class TestAgentLoop:
    @pytest.mark.asyncio
    async def test_completes_normally(self):
        async def mock_model(msgs, sys, tools):
            yield "分析结果：这是一个设计模式。"
            await asyncio.sleep(0.01)

        def mock_handler(name, args):
            return f"[{name}] done"

        loop = AgentLoop(mock_model, mock_handler)
        params = QueryParams(prompt="测试", max_turns=3)

        events = []
        async for event in loop.run(params):
            events.append(event)

        assert any(e.type == EventType.DONE for e in events)
        done_event = [e for e in events if e.type == EventType.DONE][0]
        assert done_event.metadata["reason"] in (
            TerminalReason.COMPLETED, TerminalReason.MAX_TURNS
        )

    @pytest.mark.asyncio
    async def test_respects_max_turns(self):
        async def mock_model(msgs, sys, tools):
            yield "需要更多工具调用 ```tool:read```"
            await asyncio.sleep(0.01)

        def mock_handler(name, args):
            return "[read] file content"

        loop = AgentLoop(mock_model, mock_handler)
        params = QueryParams(prompt="测试", max_turns=2)

        events = []
        async for event in loop.run(params):
            events.append(event)

        progress_events = [e for e in events if e.type == EventType.PROGRESS]
        assert len(progress_events) <= 2  # 不超过 max_turns

    @pytest.mark.asyncio
    async def test_abort_signal(self):
        async def mock_model(msgs, sys, tools):
            yield "开始..."
            await asyncio.sleep(0.5)
            yield "继续..."

        def mock_handler(name, args):
            return "ok"

        abort = asyncio.Event()

        async def abort_soon():
            await asyncio.sleep(0.1)
            abort.set()

        loop = AgentLoop(mock_model, mock_handler)
        params = QueryParams(prompt="测试", max_turns=5, abort_signal=abort)

        events = []
        async def collect():
            async for event in loop.run(params):
                events.append(event)

        await asyncio.gather(collect(), abort_soon())

        done = [e for e in events if e.type == EventType.DONE]
        assert len(done) > 0
        # abort 在 streaming 期间触发 → ABORTED_STREAMING 是正确的
        assert done[0].metadata["reason"] in (
            TerminalReason.USER_STOPPED, TerminalReason.ABORTED_STREAMING
        )

    @pytest.mark.asyncio
    async def test_cost_limit(self):
        async def mock_model(msgs, sys, tools):
            yield "x" * 10000  # 大量 token
            await asyncio.sleep(0.01)

        def mock_handler(name, args):
            return "ok"

        # 高成本追踪
        def expensive_cost(ti, to):
            return 100.0  # 每次调用 $100

        loop = AgentLoop(mock_model, mock_handler, cost_tracker=expensive_cost)
        params = QueryParams(prompt="测试", max_turns=5, max_cost_usd=0.01)

        events = []
        async for event in loop.run(params):
            events.append(event)

        done = [e for e in events if e.type == EventType.DONE]
        assert done[0].metadata["reason"] == TerminalReason.COST_LIMIT


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
