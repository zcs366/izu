#!/usr/bin/env python3
"""
izu_session_memory.py — Session Memory Compaction & Decay Curve

P0-1 of 核战队记忆系统改造计划.

功能:
  1. Timeline Compaction — 将超过N轮的会话压缩为结构化摘要
  2. 重要性衰减曲线 — 对每条记忆应用时间衰减权重
  3. 遗忘门控 — 衰减到阈值以下的记忆自动压缩或标记

用法:
  python3 izu_session_memory.py audit         # 扫描所有session评估状态
  python3 izu_session_memory.py compact <id>  # 压缩指定会话生成摘要
  python3 izu_session_memory.py compact       # 自动压缩所有需压缩的会话
  python3 izu_session_memory.py decay         # 对MEMORY.md应用衰减分析
  python3 izu_session_memory.py purge         # 清理待遗忘的session
  python3 izu_session_memory.py report        # 输出完整记忆健康报告
"""

import json, sys, os, math, shutil, re
from pathlib import Path
from datetime import datetime
from collections import Counter

# ── 配置 ──
HERMES = Path(os.getenv('HERMES_HOME', Path.home() / '.hermes'))
MEMORY_FILE = HERMES / 'memories' / 'MEMORY.md'
USER_FILE = HERMES / 'memories' / 'USER.md'
SESSIONS = HERMES / 'sessions'

# 衰减参数
DECAY_HALF_LIFE = 24       # 半衰期(小时)
FORGET_THRESHOLD = 0.15    # 遗忘阈值
COMPACT_THRESHOLD = 50     # 压缩阈值(轮次)

# ══════════════════════════════════════════════
# 衰减曲线
# ══════════════════════════════════════════════

def decay_score(age_hours: float, importance: float = 1.0, accesses: int = 0, persistent: bool = False) -> float:
    """计算记忆活跃度分数 (0~1)。persistent=True的条目不衰减。"""
    if persistent:
        return 1.0  # 永久条目始终活跃
    td = 0.5 ** (age_hours / DECAY_HALF_LIFE)          # 时间衰减
    ab = 1.0 + min(accesses, 10) * 0.05                  # 访问增强
    return min(1.0, max(0.0, td * ab * importance))

def state_str(score: float) -> str:
    return "🟢活跃" if score >= 0.7 else ("🟡渐弱" if score >= FORGET_THRESHOLD else "🔴待遗忘")

# ══════════════════════════════════════════════
# Session Compaction
# ══════════════════════════════════════════════

def count_turns(path: Path) -> int:
    try:
        with open(path) as f:
            return sum(1 for l in f if '"role":' in l) // 2
    except: return 0

def session_info(path: Path) -> dict:
    turns, mtime = count_turns(path), os.path.getmtime(path)
    age = (datetime.now() - datetime.fromtimestamp(mtime)).total_seconds() / 3600
    imp = min(1.0, turns / 100) * decay_score(age)
    return dict(session=path.stem, turns=turns, age_hours=round(age,1),
                score=round(imp,3), state=state_str(imp),
                needs_compact=turns >= COMPACT_THRESHOLD,
                candidate=imp < FORGET_THRESHOLD)

def parse_session(path: Path) -> list:
    """解析session文件为消息列表"""
    try:
        raw = path.read_text(encoding='utf-8')
    except:
        raw = path.read_text()
    
    msgs = []
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            for key in ['messages', 'conversation', 'history', 'turns']:
                if key in data and isinstance(data[key], list):
                    msgs = data[key]; break
    except json.JSONDecodeError:
        for line in raw.split('\n'):
            line = line.strip()
            if line:
                try: msgs.append(json.loads(line))
                except: pass
    return msgs

def extract_key_content(msgs: list) -> dict:
    """从消息中规则提取关键内容（零LLM成本）"""
    result = {
        'decisions': [], 'intents': [], 'code_blocks': [],
        'urls': set(), 'key_facts': [], 'tool_actions': [],
    }
    
    for i, m in enumerate(msgs):
        role = m.get('role', '')
        content = m.get('content', '') or ''
        if isinstance(content, list):
            content = ' '.join(p.get('text','') for p in content if isinstance(p,dict))
        content = str(content)
        
        if role == 'user':
            c_lower = content.lower()
            if any(w in c_lower for w in ['开干','启动','开始','创建','写','部署','安装','设置']):
                result['intents'].append(content[:100])
            if '?' in content:
                result['intents'].append(content[:100])
            continue
        
        if role == 'assistant':
            # 决策/结论
            if any(mk in content for mk in ['因此', '所以', '结论', '决定', '最终', '综上所述',
                                              '军师终裁', '方案', '核战队决议']):
                for para in content.split('\n'):
                    para = para.strip()
                    if any(mk in para for mk in ['因此:', '所以:', '结论:', '决定:', '军师终裁:',
                                                  '**结论**', '**决定**', '**方案**']):
                        result['decisions'].append(para[:150])
                        break
                else:
                    result['decisions'].append(content[:150])
            
            # 代码
            code_parts = re.findall(r'```[\w]*\n.*?```', content, re.DOTALL)
            for cp in code_parts:
                result['code_blocks'].append(cp[:80])
            
            # 链接
            found = re.findall(r'https?://[^\s\)\]>]+', content)
            result['urls'].update(found)
            
            # 工具调用
            for tc in m.get('tool_calls', []):
                fn = tc.get('function',{}).get('name', tc.get('name',''))
                result['tool_actions'].append(fn)
            continue
        
        if role == 'tool' and len(content) > 50:
            if any(k in content for k in ['/mnt/', '.md', '.py', 'success', 'completed', '写入']):
                result['key_facts'].append(content[:100])
    
    return result

def compact_session(path: Path) -> Path:
    """压缩单个session，返回压缩文件路径"""
    info = session_info(path)
    msgs = parse_session(path)
    if not msgs:
        raise ValueError("无法解析session")
    
    extracted = extract_key_content(msgs)
    
    COMPACTED_DIR = HERMES / 'memories' / 'compacted'
    COMPACTED_DIR.mkdir(parents=True, exist_ok=True)
    
    lines = [
        f"# Session 压缩摘要",
        f"> 原始: {path.stem} | {info['turns']}轮 | {info['age_hours']:.1f}h前",
        f"> 分数: {info['score']:.3f} | 状态: {info['state']}",
        "",
    ]
    
    if extracted['intents']:
        lines.append("## 用户意图/问题")
        for it in extracted['intents'][:5]:
            lines.append(f"- {it}")
        lines.append("")
    
    if extracted['decisions']:
        lines.append("## 决策/结论")
        for d in extracted['decisions'][:8]:
            lines.append(f"- {d}")
        lines.append("")
    
    if extracted['tool_actions']:
        # 去重统计
        tc = Counter(extracted['tool_actions'])
        lines.append("## 工具调用 (去重)")
        for tool, count in tc.most_common(10):
            lines.append(f"- {tool} ×{count}")
        lines.append("")
    
    if extracted['key_facts']:
        lines.append("## 关键事实")
        for f in extracted['key_facts'][:6]:
            lines.append(f"- {f}")
        lines.append("")
    
    if extracted['code_blocks']:
        lines.append("## 代码 (片段)")
        for c in extracted['code_blocks'][:4]:
            lines.append(f"- {c}")
        lines.append("")
    
    if extracted['urls']:
        lines.append("## 引用链接")
        for u in sorted(extracted['urls'])[:6]:
            lines.append(f"- {u}")
        lines.append("")
    
    lines.append("---")
    lines.append(f"压缩于: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"原始: {info['turns']}轮 → 摘要: {len(lines)}行")
    
    compact_path = COMPACTED_DIR / f"{path.stem}_compact.md"
    compact_path.write_text('\n'.join(lines), encoding='utf-8')
    
    # 重命名原始session为.archived（不删除，但不再参与下次扫描）
    archived_path = path.with_suffix('.archived')
    path.rename(archived_path)
    
    return compact_path

# ══════════════════════════════════════════════
# CLI 命令
# ══════════════════════════════════════════════

def cmd_audit():
    sessions = sorted(SESSIONS.glob('*.json'), key=os.path.getmtime, reverse=True)
    sessions += sorted(SESSIONS.glob('*.jsonl'), key=os.path.getmtime, reverse=True)
    
    print(f"\n📊 Session Memory Audit — {HERMES}")
    print(f"   {len(sessions)} sessions, half-life={DECAY_HALF_LIFE}h, forget<{FORGET_THRESHOLD}\n")
    
    counts = {"🟢":0,"🟡":0,"🔴":0}
    for s in sessions[:60]:
        info = session_info(s)
        prefix = "🟢" if "活跃" in info['state'] else ("🟡" if "渐弱" in info['state'] else "🔴")
        counts[prefix] = counts.get(prefix,0)+1
        compact_mark = " ⚡需压缩" if info['needs_compact'] else ""
        print(f"  {info['state']} {s.name[:45]:45s} | {info['turns']:3d}轮 | {info['age_hours']:5.1f}h | {info['score']:.2f}{compact_mark}")
    
    print(f"\n  汇总: 🟢{counts.get('🟢',0)}活跃 / 🟡{counts.get('🟡',0)}渐弱 / 🔴{counts.get('🔴',0)}待遗忘")
    need_c = sum(1 for s in sessions if session_info(s)['needs_compact'])
    print(f"  需压缩: {need_c} 个会话")

def cmd_decay():
    if not MEMORY_FILE.exists(): return print(f"❌ {MEMORY_FILE} not found")
    entries = [e.strip() for e in MEMORY_FILE.read_text().split('§') if e.strip()]
    print(f"\n📉 Decay Analysis — {MEMORY_FILE.name} ({len(entries)} entries)\n")
    dying = 0; persistent = 0
    for i, e in enumerate(entries):
        is_persistent = '[persistent]' in e.lower() or '[永久]' in e or '⚠️' in e
        age = (len(entries)-i)*12
        sc = decay_score(age, persistent=is_persistent)
        st = "🟢永久" if is_persistent else state_str(sc)
        if is_persistent: persistent += 1
        elif sc < FORGET_THRESHOLD: dying += 1
        mark = " 🔒永久" if is_persistent else ""
        print(f"  {st} [{sc:.2f}]{mark} {e[:65]}")
    print(f"\n  汇总: {persistent}永久 / {dying}待遗忘 / {len(entries)-persistent-dying}正常")

def cmd_report():
    cmd_audit()
    print("\n" + "="*60)
    cmd_decay()
    # 简版工作记忆建议
    sessions = sorted(SESSIONS.glob('*'), key=os.path.getmtime, reverse=True)
    active = [s for s in sessions[:20] if session_info(s)['score'] >= 0.3]
    print(f"\n🧠 工作记忆建议(top-k): 取活跃度最高的{min(5,len(active))}个会话")
    for s in active[:5]:
        info = session_info(s)
        print(f"  {s.name[:40]} ({info['score']:.2f})")

def cmd_compact(name=''):
    """压缩session（可指定名称，或自动压缩所有需压缩的）"""
    sessions = sorted(SESSIONS.glob('*.json'), key=os.path.getmtime, reverse=True)
    sessions += sorted(SESSIONS.glob('*.jsonl'), key=os.path.getmtime, reverse=True)
    
    targets = []
    if name:
        for s in sessions:
            if name in s.stem:
                targets.append(s); break
        if not targets:
            return print(f"❌ 未找到包含 '{name}' 的session")
    else:
        for s in sessions:
            info = session_info(s)
            if info['needs_compact'] and info['score'] >= 0.3:
                targets.append(s)
        if not targets:
            return print("✅ 无可压缩session")
    
    print(f"\n📦 Session 压缩 — {len(targets)} 个\n")
    compressed, errors = 0, 0
    for s in targets:
        info = session_info(s)
        try:
            result = compact_session(s)
            compressed += 1
            print(f"  ✅ {s.stem[:40]:40s} | {info['turns']:3d}轮 → {result.name}")
        except Exception as e:
            errors += 1
            print(f"  ❌ {s.stem[:40]:40s} | 失败: {e}")
    
    print(f"\n  完成: {compressed}个压缩, {errors}个失败")

def cmd_purge():
    """清理待遗忘session（score<FORGET_THRESHOLD的）"""
    sessions = sorted(SESSIONS.glob('*.json'), key=os.path.getmtime, reverse=True)
    sessions += sorted(SESSIONS.glob('*.jsonl'), key=os.path.getmtime, reverse=True)
    
    candidates = [s for s in sessions if session_info(s)['candidate']]
    if not candidates:
        return print("✅ 无待清理session")
    
    print(f"\n🗑️  遗忘清理 — {len(candidates)} 个待处理\n")
    
    for s in candidates:
        info = session_info(s)
        # 5轮以上的存档到compacted，5轮以下的直接标记
        if info['turns'] >= 5:
            try:
                result = compact_session(s)
                print(f"  📦 {s.stem[:40]:40s} | {info['turns']}轮 {info['score']:.3f} → 压缩归档")
            except Exception as e:
                print(f"  ⚠️ {s.stem[:40]:40s} | 压缩失败, 直接清理: {e}")
                PURGED_DIR = HERMES / 'memories' / 'purged'
                PURGED_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(s), str(PURGED_DIR / s.name))
                print(f"  🗑️  {s.stem[:40]:40s} | 已移至purged")
        else:
            # 短会话直接标记为.purged
            purged_path = s.with_name(s.stem + '.purged')
            s.rename(purged_path)
            print(f"  🗑️  {s.stem[:40]:40s} | {info['turns']}轮 {info['score']:.3f} → 已清理")
    
    print(f"\n  完成: {len(candidates)} 个已处理")

if __name__ == '__main__':
    cmds = {
        'audit': cmd_audit,
        'decay': cmd_decay,
        'report': cmd_report,
        'compact': lambda: cmd_compact(sys.argv[2]) if len(sys.argv) > 2 else cmd_compact(),
        'purge': cmd_purge,
    }
    c = sys.argv[1] if len(sys.argv) > 1 else 'report'
    cmds.get(c, lambda: print(__doc__))()
