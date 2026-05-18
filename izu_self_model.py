#!/usr/bin/env python3
"""
izu_self_model.py — Self Model Snapshot & Identity Anchoring

P0-3 of 核战队记忆系统改造计划.

从SOUL.md和system prompt中提取"身份锚点"——不变的自我定义。
生成版本化快照，支持不同版本间diff对比，防止人格漂移。

用法:
  python3 izu_self_model.py snapshot     # 生成当前Self Model快照
  python3 izu_self_model.py diff          # 对比最新两个版本差异
  python3 izu_self_model.py list          # 列出所有版本快照
"""

import json, sys, os, re
from datetime import datetime
from pathlib import Path

HERMES = Path(os.getenv('HERMES_HOME', Path.home() / '.hermes'))
SOUL_FILE = HERMES / 'SOUL.md'
SNAPSHOTS_DIR = HERMES / 'memories' / 'self_model'

# 身份锚点提取规则
ANCHOR_PATTERNS = [
    ('role', r'\*\*角色\*\*\s*[：:]\s*(.+?)(?:\n|$)'),
    ('mission', r'核心使命[：:]\s*(.+?)(?:\n|$)'),
    ('name', r'name\s*[:：]\s*(.+)'),
    ('description', r'description\s*[:：]\s*(.+)'),
    ('personality', r'\*\*性格\*\*\s*[：:]\s*(.+?)(?:\n|$)'),
    ('color', r'color\s*[:：]\s*"(.+)"'),
]


def extract_anchors(text: str) -> dict:
    """从SOUL.md文本中提取身份锚点"""
    anchors = {}
    for key, pattern in ANCHOR_PATTERNS:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            anchors[key] = m.group(1).strip()
    return anchors


def compute_fingerprint(anchors: dict) -> str:
    """基于锚点内容生成版本指纹"""
    raw = '|'.join(f'{k}={v}' for k, v in sorted(anchors.items()))
    return str(hash(raw) % (10 ** 12))


def snapshot():
    """生成当前Self Model快照"""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    if not SOUL_FILE.exists():
        return print(f"❌ 未找到SOUL.md: {SOUL_FILE}")

    content = SOUL_FILE.read_text()
    anchors = extract_anchors(content)
    fingerprint = compute_fingerprint(anchors)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    snapshot_data = {
        'version': ts,
        'fingerprint': fingerprint,
        'timestamp': datetime.now().isoformat(),
        'source': str(SOUL_FILE),
        'anchors': anchors,
        'raw_length': len(content),
    }

    out_path = SNAPSHOTS_DIR / f'self_model_{ts}.json'
    out_path.write_text(json.dumps(snapshot_data, indent=2, ensure_ascii=False))

    print(f"\n🧬 Self Model 快照已生成")
    print(f"   版本: {ts}")
    print(f"   指纹: {fingerprint}")
    print(f"   锚点数: {len(anchors)}")
    for k, v in anchors.items():
        print(f"     {k}: {v[:60]}")
    print(f"   已写入: {out_path}")


def cmd_list():
    """列出所有版本快照"""
    snapshots = sorted(SNAPSHOTS_DIR.glob('self_model_*.json'))
    if not snapshots:
        return print("❌ 无Self Model快照")

    print(f"\n📋 Self Model 快照列表 ({len(snapshots)}个版本)")
    for s in snapshots:
        data = json.loads(s.read_text())
        print(f"  {s.name}  |  指纹:{data['fingerprint']}  |  锚点:{list(data['anchors'].keys())}")


def cmd_diff():
    """对比最新两个版本的差异"""
    snapshots = sorted(SNAPSHOTS_DIR.glob('self_model_*.json'), reverse=True)
    if len(snapshots) < 2:
        return print("❌ 需要至少2个版本才能对比")

    old, new = json.loads(snapshots[1].read_text()), json.loads(snapshots[0].read_text())

    print(f"\n🔍 Self Model Diff")
    print(f"   旧版: {snapshots[1].name} ({old['timestamp'][:16]})")
    print(f"   新版: {snapshots[0].name} ({new['timestamp'][:16]})")

    changes = []
    all_keys = set(old['anchors'].keys()) | set(new['anchors'].keys())
    for k in sorted(all_keys):
        ov = old['anchors'].get(k, '❌缺失')
        nv = new['anchors'].get(k, '❌缺失')
        if ov != nv:
            changes.append((k, ov, nv))
            print(f"\n  ⚠️ {k} 已变更:")
            print(f"     旧: {ov}")
            print(f"     新: {nv}")

    if not changes:
        print("\n  ✅ 无变更 — 身份锚点稳定")

    # 指纹变化
    if old['fingerprint'] != new['fingerprint']:
        print(f"\n  🔐 指纹变化: {old['fingerprint']} → {new['fingerprint']}")
    else:
        print(f"\n  🔐 指纹: {old['fingerprint']} (一致)")


if __name__ == '__main__':
    cmds = {'snapshot': snapshot, 'list': cmd_list, 'diff': cmd_diff}
    c = sys.argv[1] if len(sys.argv) > 1 else 'snapshot'
    cmds.get(c, lambda: print(__doc__))()
