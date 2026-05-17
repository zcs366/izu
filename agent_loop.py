"""
izu Agent Loop v1.0 — Async Generator 主循环
=============================================
基于 Claude Code v2.1.88 源码架构启示，为 izu 设计的异步生成器 Agent 循环。

核心设计：
    Async Generator — 统一事件流、终止信号、错误处理
    Continue Site — 每轮状态原子更新，显式转换原因
    成本阶梯 — 从便宜到贵的上下文管理
    流式工具执行 — 安全工具在 LLM 生成时并行执行

用法：
    async for event in agent_loop.run(params):
        match event.type:
            case EventType.THINKING:  ...
            case EventType.DONE:      print(event.metadata["reason"])
            ...

版本: v1.0.0 | 2026-05-14 | 军师祭酒
"""

from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncGenerator, Optional, Callable

# ═══════════════════════════════════════════
# 事件类型
# ═══════════════════════════════════════════

class EventType(Enum):
    THINKING = "thinking"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    MESSAGE = "message"
    PROGRESS = "progress"
    DONE = "done"
    ERROR = "error"


class TerminalReason(Enum):
    COMPLETED = "completed"
    BLOCKING_LIMIT = "blocking_limit"
    ABORTED_STREAMING = "aborted_streaming"
    ABORTED_TOOLS = "aborted_tools"
    PROMPT_TOO_LONG = "prompt_too_long"
    MODEL_ERROR = "model_error"
    MAX_TURNS = "max_turns"
    COST_LIMIT = "cost_limit"
    USER_STOPPED = "user_stopped"


class ToolSafety(Enum):
    READ_ONLY = "read_only"
    SIDE_EFFECT = "side_effect"
    DANGEROUS = "dangerous"


# ═══════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════

@dataclass
class Event:
    type: EventType
    content: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class QueryParams:
    prompt: str
    system_prompt: str = ""
    max_turns: int = 10
    max_cost_usd: float = 0.50
    temperature: float = 0.7
    tools: list[dict] = field(default_factory=list)
    abort_signal: Optional[asyncio.Event] = None


@dataclass
class TurnState:
    turn: int = 0
    messages: list[dict] = field(default_factory=list)
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    tool_results: dict[str, str] = field(default_factory=dict)
    errors_this_turn: int = 0
    consecutive_failures: int = 0
    transition: Optional[str] = None
    compression_applied: list[str] = field(default_factory=list)


@dataclass
class ToolCall:
    name: str
    arguments: dict
    safety: ToolSafety = ToolSafety.READ_ONLY
    call_id: str = ""


# ═══════════════════════════════════════════
# 成本阶梯
# ═══════════════════════════════════════════

class CostLadder:
    """
    从便宜到贵的上下文压缩。
    L0: 截断($0) → L1: 清除过期($0) → L2: 小模型摘要(~$0.001) → L3: 全量摘要(~$0.01)
    """
    WARNING_THRESHOLD = 0.70
    ERROR_THRESHOLD = 0.85
    BLOCK_THRESHOLD = 0.95

    def __init__(self, max_tokens: int = 64000):
        self.max_tokens = max_tokens
        self.applied_levels: list[str] = []

    def assess(self, current_tokens: int) -> str:
        ratio = current_tokens / self.max_tokens
        if ratio >= self.BLOCK_THRESHOLD:
            return "blocking"
        elif ratio >= self.ERROR_THRESHOLD:
            return "compact"
        elif ratio >= self.WARNING_THRESHOLD:
            return "warning"
        return "normal"

    def compact_l0(self, messages: list[dict], keep: int = 20) -> list[dict]:
        self.applied_levels.append("L0_truncate")
        return messages[-keep:]

    def compact_l1(self, messages: list[dict]) -> list[dict]:
        self.applied_levels.append("L1_clear_stale")
        return [m for m in messages if "[Cleared]" not in str(m.get("content", ""))]

    def compact_l2(self, messages: list[dict]) -> tuple[list[dict], str]:
        self.applied_levels.append("L2_summarize")
        summary = f"[对话摘要: 前{len(messages) - 5}条已压缩]"
        return messages[-5:], summary


# ═══════════════════════════════════════════
# 流式工具执行器
# ═══════════════════════════════════════════

class StreamingToolExecutor:
    """在LLM生成时并行执行只读工具。有副作用工具必须串行。"""

    def __init__(self, handler: Callable):
        self._handler = handler
        self._running: dict[str, asyncio.Task] = {}

    def can_execute(self, safety: ToolSafety) -> bool:
        if not self._running:
            return True
        active = [t for t in self._running.values() if not t.done()]
        if safety == ToolSafety.READ_ONLY:
            return all(getattr(t, '_safety', None) == ToolSafety.READ_ONLY for t in active)
        if safety == ToolSafety.SIDE_EFFECT:
            return len(active) == 0
        return False

    async def execute(self, call: ToolCall) -> str:
        if not self.can_execute(call.safety):
            await asyncio.gather(*self._running.values(), return_exceptions=True)
        task = asyncio.create_task(self._execute_one(call))
        task._safety = call.safety
        self._running[call.call_id] = task
        return await task

    async def _execute_one(self, call: ToolCall) -> str:
        try:
            result = await asyncio.to_thread(self._handler, call.name, call.arguments)
            return str(result)
        except Exception as e:
            return f"[ERROR] {call.name}: {e}"


# ═══════════════════════════════════════════
# 终止辅助
# ═══════════════════════════════════════════

def _done(reason: TerminalReason) -> Event:
    """构造终止事件"""
    return Event(EventType.DONE, reason.value, {"reason": reason})


# ═══════════════════════════════════════════
# Agent 主循环
# ═══════════════════════════════════════════

class AgentLoop:
    """
    izu Agent 主循环 — Async Generator。
    6阶段流水线: 压缩→调用→恢复→递减检测→工具收集→转场。
    9种终止原因。
    """

    MAX_CONSECUTIVE_FAILURES = 3
    DIMINISHING_THRESHOLD = 3
    MIN_TOKENS_PER_TURN = 500

    def __init__(self, call_model, tool_handler, cost_tracker=None):
        self._call_model = call_model
        self._executor = StreamingToolExecutor(tool_handler)
        self._cost = cost_tracker or (lambda i, o: 0.0)
        self._ladder = CostLadder()

    async def run(self, params: QueryParams) -> AsyncGenerator[Event, None]:
        state = TurnState(messages=[{"role": "user", "content": params.prompt}])
        abort = params.abort_signal or asyncio.Event()

        while state.turn < params.max_turns:
            state.turn += 1
            if abort.is_set():
                yield _done(TerminalReason.USER_STOPPED)
                return

            if state.total_cost_usd >= params.max_cost_usd:
                yield Event(EventType.ERROR, f"超过成本预算 ${params.max_cost_usd}")
                yield _done(TerminalReason.COST_LIMIT)
                return

            yield Event(EventType.PROGRESS,
                       f"第 {state.turn}/{params.max_turns} 轮",
                       {"turn": state.turn})

            # Stage 1: 压缩检查
            status = self._ladder.assess(state.total_tokens)
            if status == "blocking":
                yield Event(EventType.ERROR, "Token 超安全线")
                yield _done(TerminalReason.BLOCKING_LIMIT)
                return
            elif status == "compact":
                yield Event(EventType.THINKING, "上下文压缩中...")
                applied = self._ladder.applied_levels
                if "L0_truncate" not in applied:
                    state.messages = self._ladder.compact_l0(state.messages)
                    yield Event(EventType.PROGRESS, "L0 截断完成")
                elif "L1_clear_stale" not in applied:
                    state.messages = self._ladder.compact_l1(state.messages)
                    yield Event(EventType.PROGRESS, "L1 清除完成")
                else:
                    state.messages, summary = self._ladder.compact_l2(state.messages)
                    yield Event(EventType.PROGRESS, f"L2 摘要: {summary[:80]}...")
                state.compression_applied = applied.copy()
            elif status == "warning":
                yield Event(EventType.PROGRESS, "上下文用量较高",
                           {"ratio": state.total_tokens / self._ladder.max_tokens})

            # Stage 2: 模型调用
            yield Event(EventType.THINKING, "思考中...")
            try:
                turn_tokens = 0
                assistant_content = ""
                tool_calls: list[ToolCall] = []

                async for chunk in self._call_model(
                    state.messages, params.system_prompt, params.tools
                ):
                    if abort.is_set():
                        yield _done(TerminalReason.ABORTED_STREAMING)
                        return

                    content = chunk if isinstance(chunk, str) else chunk.get("content", "")
                    assistant_content += content
                    turn_tokens += len(content) // 4

                    # 检测工具调用
                    if "```tool:" in content:
                        tc = self._parse_tool(content)
                        if tc:
                            tool_calls.append(tc)
                            yield Event(EventType.TOOL_CALL, tc.name, {"call_id": tc.call_id})
                            if self._executor.can_execute(tc.safety):
                                result = await self._executor.execute(tc)
                                yield Event(EventType.TOOL_RESULT, result[:500], {"tool": tc.name})

                # Stage 3: 错误恢复
                if not assistant_content and state.consecutive_failures > 0:
                    state.consecutive_failures += 1
                    if state.consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
                        yield Event(EventType.ERROR, f"连续{self.MAX_CONSECUTIVE_FAILURES}次失败")
                        yield _done(TerminalReason.MODEL_ERROR)
                        return
                    state.transition = "error_recovery"
                    continue

                state.consecutive_failures = 0
                state.messages.append({"role": "assistant", "content": assistant_content})
                state.total_tokens += turn_tokens
                state.total_cost_usd += self._cost(turn_tokens, turn_tokens)

                # 每轮后成本检查（Stage 3.5）
                if state.total_cost_usd >= params.max_cost_usd:
                    yield Event(EventType.ERROR, f"超过成本预算 ${params.max_cost_usd}")
                    yield _done(TerminalReason.COST_LIMIT)
                    return

                # Stage 4: 收益递减检测
                if self._is_diminishing(state, turn_tokens):
                    yield Event(EventType.THINKING, f"产出偏低({turn_tokens}t)，已达边界")
                    yield Event(EventType.MESSAGE, assistant_content)
                    yield _done(TerminalReason.COMPLETED)
                    return

                # Stage 5+6: 消息输出 + 转场
                yield Event(EventType.MESSAGE, assistant_content)

                if tool_calls:
                    state.transition = "next_turn_tools_pending"
                elif state.turn >= params.max_turns:
                    yield _done(TerminalReason.MAX_TURNS)
                    return
                else:
                    yield _done(TerminalReason.COMPLETED)
                    return

            except asyncio.CancelledError:
                yield _done(TerminalReason.ABORTED_STREAMING)
                return
            except Exception as e:
                state.consecutive_failures += 1
                yield Event(EventType.ERROR, f"异常: {str(e)[:200]}")
                if state.consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
                    yield _done(TerminalReason.MODEL_ERROR)
                    return
                state.transition = "error_recovery"
                continue

        yield _done(TerminalReason.MAX_TURNS)

    def _parse_tool(self, content: str) -> Optional[ToolCall]:
        if "```tool:read" in content:
            return ToolCall("read", {}, ToolSafety.READ_ONLY)
        elif "```tool:write" in content:
            return ToolCall("write", {}, ToolSafety.SIDE_EFFECT)
        return None

    def _is_diminishing(self, state: TurnState, turn_tokens: int) -> bool:
        return (
            state.turn >= self.DIMINISHING_THRESHOLD
            and turn_tokens < self.MIN_TOKENS_PER_TURN
        )


# ═══════════════════════════════════════════
# 适配器：桥接现有 subagent 系统
# ═══════════════════════════════════════════

class IzuAdapter:
    """将 Async Generator 循环适配到现有 subagent 系统"""

    def __init__(self, script: str = "/mnt/i/hermes/scripts/subagent.py"):
        self._script = script

    async def _agent(self, role: str, prompt: str, timeout: int = 600) -> str:
        proc = await asyncio.create_subprocess_exec(
            "python3", self._script, role, prompt,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
            if proc.returncode != 0:
                return f"[ERROR] {role}: {stderr.decode()[:200]}"
            return stdout.decode().strip()
        except asyncio.TimeoutError:
            proc.kill()
            return f"[TIMEOUT] {role}"

    async def search_parallel(self, queries: list[str]) -> AsyncGenerator[Event, None]:
        tasks = [self._agent("搜", q) for q in queries]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            yield Event(EventType.TOOL_RESULT, result[:300])

    async def write_critique(self, topic: str, search: str) -> AsyncGenerator[Event, None]:
        yield Event(EventType.PROGRESS, "写作中...")
        article = await self._agent("写", f"写关于'{topic}'的文章。\n资料：{search[:2000]}")
        yield Event(EventType.PROGRESS, "审阅中...")
        critique = await self._agent("劈", f"审阅：\n{article[:3000]}")
        yield Event(EventType.MESSAGE, article[:500])
        yield Event(EventType.TOOL_RESULT, f"审阅: {critique[:300]}")


# ═══════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════

async def demo():
    async def mock_model(messages, sys, tools):
        for r in ["让我思考一下...", "这是一个有趣的问题。", "我的分析如下：问题的核心在于设计的平衡。"]:
            yield r
            await asyncio.sleep(0.3)

    def mock_handler(name, args):
        return f"[{name}] 完成"

    loop = AgentLoop(mock_model, mock_handler)
    params = QueryParams(
        prompt="分析 Claude Code 的 Async Generator 设计模式",
        system_prompt="你是 izu，学术研究助手。",
        max_turns=3,
    )

    print("═" * 50)
    print("  izu Agent Loop v1.0 — Async Generator 演示")
    print("═" * 50)

    async for event in loop.run(params):
        icon = {
            EventType.THINKING: "🧠", EventType.TOOL_CALL: "🔧",
            EventType.TOOL_RESULT: "📋", EventType.MESSAGE: "💬",
            EventType.PROGRESS: "📊", EventType.ERROR: "❌",
            EventType.DONE: "✅",
        }.get(event.type, "•")

        if event.type == EventType.DONE:
            reason = event.metadata.get("reason", "unknown")
            print(f"  ✅ 完成 — 终止原因: {reason}")
        else:
            print(f"  {icon} [{event.type.value}] {event.content[:120]}")

    print("\n  演示结束。")


if __name__ == "__main__":
    asyncio.run(demo())
