#!/usr/bin/env python3
"""
Custom MCP Server Scaffold
===========================
基于本会话产出的两个 MCP 服务器（action-bridge、project-context）抽象出的模板。
遵循 async stdin/stdout MCP 协议，注册后自动发现工具。

使用方式：
  1. 复制此文件到 /mnt/i/hermes/scripts/your-server-name.py
  2. 修改 SERVER_NAME 和工具定义
  3. 在 config.yaml 的 mcp_servers 中添加：
     your-server-name:
       command: /home/zcs/.hermes/hermes-agent/venv/bin/python3
       args: ["/mnt/i/hermes/scripts/your-server-name.py"]
       timeout: 30
  4. 重启 Hermes Agent
"""

import json, sys, asyncio

SERVER_NAME = "your-server-name"
SERVER_VERSION = "1.0.0"


# ============================================================
# 工具函数 — 在这里定义你的业务逻辑
# ============================================================

async def tool_hello(params: dict) -> dict:
    """示例工具：返回问候信息"""
    name = params.get("name", "world")
    return {
        "content": [{"type": "text", "text": json.dumps({
            "message": f"Hello, {name}!",
            "server": SERVER_NAME,
            "version": SERVER_VERSION
        }, ensure_ascii=False)}]
    }


# 工具注册表：名称 -> (描述, 输入Schema, 处理函数)
TOOLS = {
    "hello": {
        "description": "示例工具 — 返回问候信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "你的名字"}
            }
        },
        "handler": tool_hello
    }
    # 在这里添加更多工具...
}


# ============================================================
# MCP 协议处理（一般不需要修改）
# ============================================================

async def handle_message(message: dict) -> dict:
    msg_id = message.get("id")
    method = message.get("method")
    params = message.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "tools": [
                    {"name": name, **info}
                    for name, info in TOOLS.items()
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0", "id": msg_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
            }
        handler = TOOLS[tool_name]["handler"]
        return await handler(params.get("arguments", {}))

    elif method == "notifications/initialized":
        return None

    return {
        "jsonrpc": "2.0", "id": msg_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }


async def main():
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    writer_transport, _ = await asyncio.get_event_loop().connect_write_pipe(
        lambda: asyncio.Protocol(), sys.stdout
    )
    while True:
        try:
            line = await asyncio.wait_for(reader.readline(), timeout=300)
            if not line:
                break
            msg = json.loads(line.decode())
            resp = await handle_message(msg)
            if resp:
                data = json.dumps(resp) + "\n"
                writer_transport.write(data.encode())
                await writer_transport.drain()
        except (asyncio.TimeoutError, json.JSONDecodeError, EOFError):
            continue


if __name__ == "__main__":
    asyncio.run(main())
