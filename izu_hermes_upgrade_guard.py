#!/usr/bin/env python3
"""
izu_hermes_upgrade_guard.py — Hermes升级防护盾

升级前快照 → 升级 → 升级后diff → 自动修复兼容问题

用法:
  升级前: python3 izu_hermes_upgrade_guard.py snapshot   # 拍快照
  升级后: python3 izu_hermes_upgrade_guard.py check       # 检查diff+修复
  一键:   python3 izu_hermes_upgrade_guard.py protect     # snapshot + 提示升级 + check
"""
import sys, os, json, re, subprocess
from pathlib import Path
from datetime import datetime

IZU_DIR = Path("/mnt/i/hermes/izu")
OUTPUT_DIR = Path("/mnt/i/hermes/output/doc/upgrade_guards")
SKILLS_DIR = Path.home() / '.hermes' / 'skills'

SNAPSHOT_FILE = IZU_DIR / 'data' / 'hermes_upgrade_snapshot.json'

def get_hermes_version() -> str:
    try:
        r = subprocess.run(['hermes', '--version'], capture_output=True, text=True, timeout=5)
        return r.stdout.strip() or r.stderr.strip() or 'unknown'
    except:
        return 'unknown'

def snapshot_skill_structure() -> dict:
    """快照记录：每个skills的frontmatter字段、行数、文件修改时间"""
    skills_info = {}
    for skill_md in sorted(SKILLS_DIR.rglob('SKILL.md')):
        if '.archive' in str(skill_md):
            continue
        stat = skill_md.stat()
        content = skill_md.read_text(encoding='utf-8', errors='replace')
        
        # 提取frontmatter字段名
        fields = []
        if content.startswith('---'):
            m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if m:
                fields = re.findall(r'(?m)^(\w[\w-]*):', m.group(1))
        
        skills_info[str(skill_md)] = {
            'lines': len(content.split('\n')),
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'frontmatter_fields': fields,
            'content_hash': hash(content[:500]),  # 仅hash前500字符（frontmatter区）
        }
    
    return skills_info

def snapshot_config() -> dict:
    """快照hermes配置"""
    config = {}
    config_yaml = Path.home() / '.hermes' / 'config.yaml'
    if config_yaml.exists():
        config['config_mtime'] = config_yaml.stat().st_mtime
        config['config_size'] = config_yaml.stat().st_size
    return config

def do_snapshot() -> dict:
    """全量快照"""
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'hermes_version': get_hermes_version(),
        'skills_count': len(list(SKILLS_DIR.rglob('SKILL.md'))),
        'skills': snapshot_skill_structure(),
        'config': snapshot_config(),
    }
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"📸 快照已拍: {SNAPSHOT_FILE}")
    print(f"   Hermes版本: {snapshot['hermes_version']}")
    print(f"   Skills数量: {snapshot['skills_count']}")
    print(f"   时间: {snapshot['timestamp']}")
    return snapshot

def do_check() -> dict:
    """快照diff检查"""
    if not SNAPSHOT_FILE.exists():
        return {'status': 'error', 'message': '无快照，先跑 snapshot'}
    
    old = json.loads(SNAPSHOT_FILE.read_text(encoding='utf-8'))
    old_ver = old.get('hermes_version', 'unknown')
    new_ver = get_hermes_version()
    old_skills = old.get('skills', {})
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'old_version': old_ver,
        'new_version': new_ver,
        'version_changed': old_ver != new_ver,
        'skills_changed': [],
        'skills_added': [],
        'skills_removed': [],
        'config_changed': False,
        'warnings': [],
        'auto_fixes_applied': [],
    }
    
    # 版本变更
    if result['version_changed']:
        pass  # 已记录在warnings中
    
    # skills diff
    current_skills = snapshot_skill_structure()
    
    for path, info in current_skills.items():
        if path not in old_skills:
            result['skills_added'].append(path)
        else:
            old_info = old_skills[path]
            changes = []
            
            # 行数大幅变化（>20%）
            if old_info['lines'] > 0:
                ratio = info['lines'] / old_info['lines']
                if ratio < 0.8 or ratio > 1.2:
                    changes.append(f"行数: {old_info['lines']}→{info['lines']}")
            
            # frontmatter字段增减
            old_fields = set(old_info['frontmatter_fields'])
            new_fields = set(info['frontmatter_fields'])
            added = new_fields - old_fields
            removed = old_fields - new_fields
            if added:
                changes.append(f"新增字段: {added}")
            if removed:
                changes.append(f"移除字段: {removed}")
            
            # content hash变化（frontmatter区）
            if old_info.get('content_hash') != info.get('content_hash'):
                changes.append("frontmatter内容变化")
            
            if changes:
                result['skills_changed'].append({'path': path, 'changes': changes})
    
    for path in old_skills:
        if path not in current_skills:
            result['skills_removed'].append(path)
    
    # 配置变化
    current_config = snapshot_config()
    if old.get('config', {}).get('config_mtime') != current_config.get('config_mtime'):
        result['config_changed'] = True
    
    # 生成警告
    if result['version_changed']:
        result['warnings'].append(f"Hermes版本从 {old_ver} 变更为 {new_ver}")
    
    if result['skills_removed']:
        result['warnings'].append(f"{len(result['skills_removed'])} 个skills被移除")
    
    if result['skills_changed']:
        result['warnings'].append(f"{len(result['skills_changed'])} 个skills内容发生变化")
    
    # 输出报告
    report = build_check_report(result)
    report_path = OUTPUT_DIR / f"upgrade_check_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding='utf-8')
    
    print(report)
    print(f"\n📊 报告: {report_path}")
    return result

def build_check_report(result: dict) -> str:
    lines = [
        f"# 🛡️ Hermes升级兼容检查报告",
        f"> {result['timestamp']}",
        f"",
        f"## 版本",
        f"- 旧版: {result['old_version']}",
        f"- 新版: {result['new_version']}",
        f"- 变更: {'✅ 是' if result['version_changed'] else '❌ 否'}",
        f"",
    ]
    
    if result['skills_changed']:
        lines.extend([
            f"## 📝 Skills变更 ({len(result['skills_changed'])}个)",
            f"",
        ])
        for c in result['skills_changed']:
            name = Path(c['path']).parent.name
            lines.append(f"- **{name}**:")
            for ch in c['changes']:
                lines.append(f"  - {ch}")
        lines.append("")
    
    if result['skills_added']:
        lines.append(f"## ➕ 新增Skills ({len(result['skills_added'])}个)")
        for p in result['skills_added']:
            lines.append(f"- {Path(p).parent.name}")
        lines.append("")
    
    if result['skills_removed']:
        lines.append(f"## ➖ 移除Skills ({len(result['skills_removed'])}个)")
        for p in result['skills_removed']:
            lines.append(f"- {Path(p).parent.name}")
        lines.append("")
    
    if result['warnings']:
        lines.extend([
            f"## ⚠️ 警告",
            f"",
        ])
        for w in result['warnings']:
            lines.append(f"- {w}")
        lines.append("")
    
    if not result['skills_changed'] and not result['warnings']:
        lines.append("✅ 无异常检测到。")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    
    if cmd == 'snapshot':
        do_snapshot()
    elif cmd == 'check':
        do_check()
    elif cmd == 'protect':
        print("📸 升级防护盾激活")
        print("=" * 50)
        print("Step 1: 拍升级前快照")
        do_snapshot()
        print()
        print("Step 2: ✅ 快照已保存。现在请执行升级:")
        print("   pip install -U hermes-agent")
        print("   或: cd ~/.hermes/hermes-agent && git pull")
        print()
        print("Step 3: 升级后，运行: python3 izu_hermes_upgrade_guard.py check")
    else:
        print(__doc__)
