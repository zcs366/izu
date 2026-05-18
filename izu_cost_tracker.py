#!/usr/bin/env python3
"""
izu_cost_tracker.py — Token成本追踪器

从Hermes session文件估算token消耗和费用。
不依赖API返回的usage字段（不修改Hermes代码），
基于消息字符数×模型单价估算。

用法:
  python3 izu_cost_tracker.py scan          # 扫描新session追加成本日志
  python3 izu_cost_tracker.py report        # 输出成本报告
  python3 izu_cost_tracker.py reset         # 清空日志重新扫描
"""
import json, os, sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

SESSION_DIR = Path.home() / '.hermes' / 'sessions'
DATA_DIR = Path('/mnt/i/hermes/data')
OUTPUT_DIR = Path('/mnt/i/hermes/output/doc/cost')
COST_LOG = DATA_DIR / 'cost_log.jsonl'

# ── 模型单价 ($/1M tokens) ──
MODEL_PRICING = {
    'deepseek-v4-flash':       {'input': 0.15, 'output': 0.60},
    'deepseek-chat':           {'input': 0.28, 'output': 1.10},
    'deepseek-reasoner':       {'input': 0.55, 'output': 2.19},
    'claude-sonnet-4':         {'input': 3.00, 'output': 15.00},
    'claude-opus-4':           {'input': 15.00,'output': 75.00},
    'gpt-4o':                  {'input': 2.50, 'output': 10.00},
    'gpt-4o-mini':             {'input': 0.15, 'output': 0.60},
    'gemini-2.0-flash':        {'input': 0.15, 'output': 0.60},
    'minimax':                 {'input': 0.30, 'output': 0.90},
    'qwen-plus':               {'input': 0.10, 'output': 0.40},
    'qwen-max':                {'input': 0.40, 'output': 1.20},
}

# 特殊模型成本（包月已付的不计边际成本）
MONTHLY_MODELS = {'minimax', 'gpt-4o'}  # 包月套餐，边际成本≈0

# 未指定模型时的默认单价
DEFAULT_COST = {'input': 2.00, 'output': 8.00}


def count_tokens(text: str) -> dict:
    """估算token数（混合中英文）"""
    chars = len(text)
    # 估算：中文≈1.7字/token, 英文≈1.3字/token, 代码≈1字/token
    en_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    cn_chars = sum(1 for c in text if ord(c) > 0x4E00)
    code_chars = text.count('```') * 50  # 代码块估算
    other_chars = chars - en_chars - cn_chars
    
    en_tokens = en_chars / 1.3
    cn_tokens = cn_chars / 1.7
    code_tokens = code_chars / 1.0
    other_tokens = other_chars / 1.5
    
    return {
        'chars': chars,
        'estimated_tokens': round(en_tokens + cn_tokens + code_tokens + other_tokens),
        'en_chars': en_chars,
        'cn_chars': cn_chars,
        'code_chars': code_chars,
    }


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> dict:
    """估算成本"""
    model_key = model.lower().strip()
    
    # 包月模型不计边际成本
    if any(m in model_key for m in MONTHLY_MODELS):
        return {'input_cost': 0, 'output_cost': 0, 'total': 0, 'pricing_note': '包月'}
    
    pricing = MODEL_PRICING.get(model_key, DEFAULT_COST)
    input_cost = input_tokens * pricing['input'] / 1_000_000
    output_cost = output_tokens * pricing['output'] / 1_000_000
    
    return {
        'input_cost': round(input_cost, 5),
        'output_cost': round(output_cost, 5),
        'total': round(input_cost + output_cost, 5),
        'pricing_note': model_key,
    }


def scan_session(path: Path) -> dict | None:
    """扫描单个session文件，返回成本记录"""
    try:
        if path.suffix == '.archived' or path.suffix == '.purged':
            return None
        raw = json.loads(path.read_text(encoding='utf-8'))
    except:
        try:
            raw = json.loads(path.read_text())
        except:
            return None
    
    if not isinstance(raw, dict):
        return None
    
    model = raw.get('model', 'unknown')
    msgs = raw.get('messages', [])
    if not msgs:
        return None
    
    # 统计
    input_chars = 0
    output_chars = 0
    user_messages = 0
    assistant_messages = 0
    tool_calls_count = 0
    
    for m in msgs:
        content = m.get('content', '') or ''
        if isinstance(content, list):
            content = ' '.join(p.get('text','') for p in content if isinstance(p,dict))
        content = str(content)
        
        role = m.get('role', '')
        if role == 'user':
            input_chars += len(content)
            user_messages += 1
        elif role == 'assistant':
            output_chars += len(content)
            assistant_messages += 1
            if 'tool_calls' in m and m['tool_calls']:
                tool_calls_count += len(m['tool_calls'])
                # tool call参数也算input
                for tc in m['tool_calls']:
                    args = str(tc.get('function',{}).get('arguments',''))
                    input_chars += len(args)
        elif role == 'tool':
            input_chars += len(content)  # tool返回给模型当input
    
    # 估算token
    input_tokens = count_tokens(' ' * input_chars)['estimated_tokens']
    output_tokens = count_tokens(' ' * output_chars)['estimated_tokens']
    
    # 粗略调整：API开销约20%
    input_tokens = int(input_tokens * 1.2)
    output_tokens = int(output_tokens * 1.2)
    
    cost = estimate_cost(model, input_tokens, output_tokens)
    
    return {
        'session_id': raw.get('session_id', path.stem),
        'model': model,
        'timestamp': raw.get('last_updated', raw.get('session_start', '')),
        'messages': len(msgs),
        'user_msgs': user_messages,
        'assistant_msgs': assistant_messages,
        'tool_calls': tool_calls_count,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'total_tokens': input_tokens + output_tokens,
        **cost,
    }


def scan_all():
    """扫描所有session，追加新记录到成本日志"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 读取已有日志中的session_ids
    existing_ids = set()
    if COST_LOG.exists():
        for line in COST_LOG.read_text().strip().split('\n'):
            if line:
                try:
                    entry = json.loads(line)
                    existing_ids.add(entry.get('session_id', ''))
                except:
                    pass
    
    sessions = sorted(SESSION_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
    
    new_entries = []
    for s in sessions:
        sid = s.stem
        if sid in existing_ids:
            continue
        
        record = scan_session(s)
        if record:
            new_entries.append(record)
    
    if not new_entries:
        print("✅ 无新session需要记录")
        return new_entries
    
    # 追加
    with open(COST_LOG, 'a') as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"📝 新增 {len(new_entries)} 条成本记录")
    for e in new_entries[:5]:
        print(f"  {e['session_id'][:30]:30s} | {e['model']:20s} | {e['total_tokens']:5d}tok | ${e['total']:.5f}")
    if len(new_entries) > 5:
        print(f"  ... 还有 {len(new_entries)-5} 条")
    
    return new_entries


def generate_report():
    """生成成本报告"""
    if not COST_LOG.exists():
        return print("❌ 无成本数据，先运行 scan")
    
    entries = []
    for line in COST_LOG.read_text().strip().split('\n'):
        if line:
            try:
                entries.append(json.loads(line))
            except:
                pass
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = OUTPUT_DIR / f'cost_report_{ts}.md'
    
    if not entries:
        report_path.write_text(f"# 成本报告\n> {ts}\n\n无数据")
        return print(f"📊 报告已写入: {report_path} (空)")
    
    # 各维度汇总
    by_model = defaultdict(lambda: {'count': 0, 'input_tok': 0, 'output_tok': 0, 'cost': 0})
    by_day = defaultdict(lambda: {'count': 0, 'cost': 0})
    
    for e in entries:
        model = e.get('model', 'unknown')
        by_model[model]['count'] += 1
        by_model[model]['input_tok'] += e.get('input_tokens', 0)
        by_model[model]['output_tok'] += e.get('output_tokens', 0)
        by_model[model]['cost'] += e.get('total', 0)
        
        ts_str = e.get('timestamp', '')[:10]
        if ts_str:
            by_day[ts_str]['count'] += 1
            by_day[ts_str]['cost'] += e.get('total', 0)
    
    total_cost = sum(m['cost'] for m in by_model.values())
    total_sessions = len(entries)
    total_tokens = sum(e.get('total_tokens', 0) for e in entries)
    
    lines = [
        f"# 💰 Token成本报告",
        f"> 生成: {ts}",
        f"> 来源: {total_sessions} sessions / {COST_LOG.name}",
        f"",
        f"## 总计",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| Sessions | {total_sessions} |",
        f"| 总Token | {total_tokens:,} |",
        f"| 总成本 | ${total_cost:.4f} |",
        f"| 均次成本 | ${total_cost/max(total_sessions,1):.6f} |",
        f"| 次均Token | {total_tokens//max(total_sessions,1):,} |",
        f"",
    ]
    
    # 按模型
    lines.append("## 按模型")
    lines.append("")
    lines.append(f"| 模型 | 次数 | Input tok | Output tok | 成本 |")
    lines.append(f"|------|------|-----------|------------|------|")
    for model, data in sorted(by_model.items(), key=lambda x: -x[1]['cost']):
        cost = data['cost']
        cost_str = f"${cost:.4f}" if cost > 0.001 else f"${cost:.6f}"
        lines.append(f"| {model} | {data['count']} | {data['input_tok']:,} | {data['output_tok']:,} | {cost_str} |")
    lines.append("")
    
    # 按日期
    lines.append("## 按日期")
    lines.append("")
    lines.append(f"| 日期 | 次数 | 成本 |")
    lines.append(f"|------|------|------|")
    for day, data in sorted(by_day.items()):
        cost = data['cost']
        cost_str = f"${cost:.4f}" if cost > 0.001 else f"${cost:.6f}"
        lines.append(f"| {day} | {data['count']} | {cost_str} |")
    lines.append("")
    
    lines.append(f"---\n报告: {report_path}")
    
    report_path.write_text('\n'.join(lines))
    print(f"📊 报告已写入: {report_path}")
    print(f"\n  💰 总成本: ${total_cost:.4f}")
    print(f"  📝 总Session: {total_sessions}")
    print(f"  🔤 总Token: {total_tokens:,}")
    
    return report_path


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    
    if cmd == 'scan':
        scan_all()
        print()
        generate_report()
    elif cmd == 'report':
        generate_report()
    elif cmd == 'reset':
        if COST_LOG.exists():
            COST_LOG.unlink()
            print("🗑️ 成本日志已清空")
        # 重新扫描
        scan_all()
        generate_report()
    else:
        print(__doc__)
