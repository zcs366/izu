#!/usr/bin/env python3
"""
mcp_traffic_logger.py — MCP调用日志收集基线
==============================================
用途：从agent.log提取MCP工具调用记录，追加到data/mcp_traffic_log.ndjson

部署：作为cron job每30分钟运行一次
设计：零API调用，只解析已有日志文件
"""

import json
import re
import gzip
from datetime import datetime, timezone
from pathlib import Path

# 配置
AGENT_LOG = Path("/home/zcs/.hermes/profiles/sandbox/logs/agent.log")
OUTPUT = Path("/mnt/i/hermes/izu/data/mcp_traffic_log.ndjson")
STATE = Path("/mnt/i/hermes/izu/data/mcp_logger_state.json")

# MCP相关日志模式
MCP_PATTERNS = [
    # 服务器注册/连接
    (r"MCP:\s+registered\s+(\d+)\s+tool\(s\)\s+from\s+(\d+)\s+server\(s\)", "registration"),
    (r"MCP server '(\w+)' initial connection failed", "connection_fail"),
    (r"MCP server '(\w+)' connected", "connection_ok"),
    (r"MCP:\s+(\d+)\s+tool\(s\)\s+from\s+(\d+)\s+server\(s\)\s+\((\d+)\s+failed\)", "server_status"),
    # 工具调用（run_agent层）
    (r"Unrepairable tool_call arguments for (\w+)", "unrepairable_args"),
    (r"tool_call_id: ([a-zA-Z0-9_]+)", "tool_call"),
]


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_position": 0, "last_run": None}


def save_state(pos: int):
    state = {"last_position": pos, "last_run": datetime.now(timezone.utc).isoformat()}
    STATE.write_text(json.dumps(state, ensure_ascii=False))
    return state


def extract_mcp_events(log_path: Path, from_pos: int) -> list:
    """从agent.log的指定位置起，提取MCP相关事件"""
    if not log_path.exists():
        return [], 0

    size = log_path.stat().st_size
    if size <= from_pos:
        return [], size

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        f.seek(from_pos)
        lines = f.readlines()

    events = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for pattern, event_type in MCP_PATTERNS:
            m = re.search(pattern, line)
            if m:
                events.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "type": event_type,
                    "raw": line[:300],
                    "matched_groups": list(m.groups()),
                })
                break  # 第一个匹配跳出

    return events, size


def append_events(events: list, output_path: Path):
    if not events:
        return 0
    count = 0
    with open(output_path, "a", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            count += 1
    return count


def main():
    # 加载断点
    state = load_state()
    from_pos = state.get("last_position", 0)

    # 提取新事件
    events, latest_size = extract_mcp_events(AGENT_LOG, from_pos)

    if events:
        count = append_events(events, OUTPUT)
        print(f"MCP_LOG | 追加 {count} 条事件 (from pos {from_pos} → {latest_size})")
    else:
        print(f"MCP_LOG | 无新事件 (pos {latest_size}, 文件大小 {AGENT_LOG.stat().st_size})")

    # 保持断点（每次记录最新位置）
    if latest_size > 0:
        save_state(latest_size)


if __name__ == "__main__":
    main()
