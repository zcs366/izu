#!/usr/bin/env python3
"""
izu_working_memory.py — Working Memory Top-K Queue

P0-2 of 核战队记忆系统改造计划.
基于注意力密度原理：当前会话中只保留最重要的K条信息在工作台上.
支持.json（嵌套JSON）和.jsonl（行分隔JSON）格式.

用法:
  python3 izu_working_memory.py queue <session_file>
  python3 izu_working_memory.py snapshot
  python3 izu_working_memory.py integrate <session_file>
"""

import json, sys, os
from datetime import datetime
from pathlib import Path

HERMES = Path(os.getenv('HERMES_HOME', Path.home() / '.hermes'))
MEMORY_FILE = HERMES / 'memories' / 'MEMORY.md'
SESSIONS = HERMES / 'sessions'
WORKING = HERMES / 'memories' / 'WORKING.md'
K = 5


def score_message(content: str, role: str = '') -> int:
    """为消息内容打分 (0~100)"""
    if not content or not isinstance(content, str):
        return 0
    s = 0
    c = content.lower()
    if any(w in c for w in ['记住', '重要', '注意', '必须', '决定', '结论', '因此']):
        s += 30
    if any(w in c for w in ['上次', '之前', '刚才', '前面']):
        s += 15
    if any(w in c for w in ['写入', '创建', '修改', '删除', '部署', '创建']):
        s += 10
    if '?' in content or '?' in content:
        s += 8
    if role == 'user':
        s += 5
    if role == 'assistant' and len(content) > 200:
        s += 3
    if content.strip() in ['好的', '明白', '嗯', 'ok', '收到']:
        s -= 5
    return max(0, s)


def extract(path: Path) -> list:
    """从session提取top-k工作记忆条目"""
    items = []
    try:
        raw = path.read_text()
        msgs = []
        # 尝试JSON对象格式
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                for key in ['messages', 'conversation', 'history', 'turns']:
                    if key in data and isinstance(data[key], list):
                        msgs = data[key]
                        break
        except json.JSONDecodeError:
            # JSONL格式
            for line in raw.split('\n'):
                line = line.strip()
                if line:
                    try:
                        msgs.append(json.loads(line))
                    except:
                        pass

        for msg in msgs:
            content = msg.get('content', '') or ''
            if isinstance(content, dict):
                content = str(content)
            role = msg.get('role', '')
            s = score_message(content, role)
            if s > 0:
                items.append({
                    'score': s, 'role': role,
                    'preview': content[:120],
                    'tool': msg.get('name', '') if role == 'tool' else '',
                })
    except:
        pass

    items.sort(key=lambda x: x['score'], reverse=True)
    return items[:K]


def write_snapshot(items: list, source: str = ''):
    """写入WORKING.md"""
    lines = [
        f"# 工作记忆快照",
        f"> 生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 来源: {source or '当前会话'}",
        f"> K={K}\n",
    ]
    for i, item in enumerate(items, 1):
        lines.append(f"## [{i}/{K}] 优先级 {item['score']}")
        lines.append(f"- 角色: {item.get('role', '?')}")
        if item.get('tool'):
            lines.append(f"- 工具: {item['tool']}")
        lines.append(f"- 内容: {item['preview']}\n")

    WORKING.parent.mkdir(parents=True, exist_ok=True)
    WORKING.write_text('\n'.join(lines))
    return str(WORKING)


def cmd_queue(name: str):
    path = SESSIONS / name
    if not path.exists():
        matches = list(SESSIONS.glob(f'*{name}*'))
        path = matches[0] if matches else None
    if not path:
        return print(f"❌ 未找到: {name}")

    items = extract(path)
    out = write_snapshot(items, path.name)
    print(f"\n🧠 工作记忆 top-{K} — {path.name}")
    for i, item in enumerate(items, 1):
        print(f"  [{i}] 分数:{item['score']:3d} | {item['role']:10s}")
        print(f"       {item['preview']}")
    print(f"\n  已写入: {out}")


def cmd_snapshot():
    latest = sorted(SESSIONS.glob('session_*.json'), key=os.path.getmtime, reverse=True)
    if not latest:
        return print("❌ 无可用session")
    all_items, seen = [], set()
    for s in latest[:3]:
        for item in extract(s):
            p = item['preview'][:60]
            if p not in seen:
                seen.add(p)
                all_items.append(item)
    all_items.sort(key=lambda x: x['score'], reverse=True)
    out = write_snapshot(all_items[:K], 'last 3 sessions')
    print(f"🧠 工作记忆快照已写入: {out}")


def cmd_integrate(name: str):
    path = SESSIONS / name if (SESSIONS / name).exists() else None
    if not path:
        matches = list(SESSIONS.glob(f'*{name}*'))
        path = matches[0] if matches else None
    if not path:
        return print(f"❌ 未找到: {name}")

    items = [i for i in extract(path) if i['score'] >= 25]
    if not items:
        return print("  ⚠️ 无高价值决策需要集成")

    print(f"\n📝 集成 {len(items)} 条决策到永久记忆:")
    for d in items:
        print(f"  📌 {d['preview']}")

    with open(MEMORY_FILE, 'a') as f:
        f.write(f"\n§\n# 从 {path.name} 集成 ({datetime.now().strftime('%m-%d %H:%M')})\n")
        for d in items:
            f.write(f"- {d['preview']}\n")
    print(f"  已追加到: {MEMORY_FILE}")


if __name__ == '__main__':
    cmds = {
        'queue': lambda: cmd_queue(sys.argv[2]) if len(sys.argv) > 2 else print("需session名"),
        'snapshot': cmd_snapshot,
        'integrate': lambda: cmd_integrate(sys.argv[2]) if len(sys.argv) > 2 else print("需session名"),
    }
    c = sys.argv[1] if len(sys.argv) > 1 else 'snapshot'
    cmds.get(c, lambda: print(__doc__))()
