#!/usr/bin/env python3
"""
izu_skill_ecosystem_health.py — Skill生态系统健康管理系统

三合一：扫描 → 自动修正 → 报告发布
对接已有的：
- izu_skill_scorer.py（评分）
- izu_memory_maintenance.py（记忆维护）
- evolution_engine.py（进化引擎）

用法:
  python3 izu_skill_ecosystem_health.py scan        # 全扫描+报告
  python3 izu_skill_ecosystem_health.py fix          # 自动修正低分skills
  python3 izu_skill_ecosystem_health.py dashboard    # 看板输出（给用户看）
  python3 izu_skill_ecosystem_health.py full         # 全部：扫描+修正+报告+看板
"""
import sys, os, re, json, subprocess
from pathlib import Path
from datetime import datetime

IZU_DIR = Path("/mnt/i/hermes/izu")
OUTPUT_DIR = Path("/mnt/i/hermes/output/doc/skill_health")
HERMES_SKILLS_DIR = Path.home() / '.hermes' / 'skills'
HERMES_HOME = Path.home() / '.hermes'

sys.path.insert(0, str(IZU_DIR))
from izu_skill_scorer import scan_all, find_all_skills, score_skill, generate_report

# ── 自动修正规则 ──
AUTO_FIX_RULES = {
    "missing_date": {
        "trigger": lambda s: s['overall'] < 0.75 and not s['extras']['has_date'],
        "action": "add_date_to_frontmatter",
        "desc": "给 frontmatter 补上 date: 字段"
    },
    "missing_version": {
        "trigger": lambda s: s['overall'] < 0.75 and not s['extras']['has_version'] and s['lines'] > 50,
        "action": "add_version_to_frontmatter",
        "desc": "给 frontmatter 补上 version: 1.0.0"
    },
}

def get_skill_metadata_from_content(content: str) -> dict:
    """提取SKILL.md的YAML frontmatter元数据"""
    fm = ""
    if content.startswith('---'):
        m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if m:
            fm = m.group(1)
    
    result = {
        'has_date': bool(re.search(r'(?m)^date:\s*20[2-9]\d', fm)),
        'has_version': bool(re.search(r'(?im)^version:\s*["\']?(\d+\.\d+)', fm)),
        'has_tags': bool(re.search(r'(?m)^tags:', fm)),
        'has_description': bool(re.search(r'(?i)(功能|description)', content[:500])),
        'has_frontmatter': content.startswith('---'),
    }
    return result

def is_user_skill(content: str) -> bool:
    """判断是否为用户自定义skill（非Hermes官方/外部）"""
    if not content.startswith('---'):
        return False
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return True  # 无frontmatter算用户skill
    fm = m.group(1).lower()
    # 外部skill特征：有homepage / metadata含hermes / author=Hermes Agent / plugin提供
    if 'homepage:' in fm:
        return False
    if 'metadata:' in fm and ('hermes' in fm or 'openclaw' in fm):
        return False
    if 'author: hermes' in fm:
        return False
    if 'plugin:' in fm:
        return False
    if 'compatibility:' in fm:
        return False
    return True


def auto_fix_skill(path: str, content: str, issues: list) -> tuple[bool, str]:
    """自动修正SKILL的元数据缺失"""
    if not content.startswith('---'):
        return False, "无frontmatter，跳过自动修复"
    
    # 跳过Hermes官方/外部skill
    if not is_user_skill(content):
        return False, "外部skill，跳过自动修复"
    
    # 拆frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "frontmatter格式异常"
    
    fm = parts[1]
    body = parts[2]
    today = datetime.now().strftime('%Y-%m-%d')
    changed = False
    
    # 检查并补 date
    if not re.search(r'(?m)^date:', fm):
        # 在 version: 或 author: 或 tags: 后面追加
        insert_after = None
        for field in ['version:', 'author:', 'tags:', 'name:', 'description:']:
            m = re.search(rf'(?m)^({re.escape(field)}.*?)$', fm)
            if m:
                insert_after = m.start(1) + len(m.group(1))
        if insert_after:
            fm = fm[:insert_after] + f"\ndate: {today}" + fm[insert_after:]
            changed = True
    
    # 检查并补 version
    if not re.search(r'(?im)^version:', fm):
        # 在 name: 或 description: 后面追加
        insert_after = None
        for field in ['description:', 'name:']:
            m = re.search(rf'(?m)^({re.escape(field)}.*?)$', fm)
            if m:
                insert_after = m.start(1) + len(m.group(1))
                break
        if insert_after:
            fm = fm[:insert_after] + f"\nversion: 1.0.0" + fm[insert_after:]
            changed = True
    
    if not changed:
        return False, "无需修改"
    
    new_content = f"---{fm}---{body}"
    
    # 安全写入
    backup = Path(path + '.bak')
    if not backup.exists():
        Path(path).rename(backup)
    
    Path(path).write_text(new_content, encoding='utf-8')
    return True, f"已补 date={today}/version=1.0.0"


def run_scan_and_fix(auto_fix: bool = False) -> dict:
    """全扫描+可选自动修正"""
    all_results = scan_all()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': len(all_results),
        'excellent': sum(1 for r in all_results if r['overall'] >= 0.85),
        'good': sum(1 for r in all_results if 0.70 <= r['overall'] < 0.85),
        'fair': sum(1 for r in all_results if 0.50 <= r['overall'] < 0.70),
        'poor': sum(1 for r in all_results if r['overall'] < 0.50),
        'avg': round(sum(r['overall'] for r in all_results) / len(all_results), 3),
        'bottom_skills': [r['name'] for r in all_results[:5]],
        'top_skills': [r['name'] for r in sorted(all_results, key=lambda x: -x['overall'])[:5]],
        'auto_fixed': [],
        'auto_fix_failed': [],
    }
    
    if auto_fix:
        for r in all_results:
            if r['overall'] >= 0.75:
                continue
            path = r['path']
            content = Path(path).read_text(encoding='utf-8')
            succ, msg = auto_fix_skill(path, content, [])
            if succ:
                report['auto_fixed'].append(f"{r['name']}: {msg}")
            elif '无需修改' not in msg:
                report['auto_fix_failed'].append(f"{r['name']}: {msg}")
    
    return report


def generate_dashboard(report: dict) -> str:
    """生成看板文本（给飞书/Telegram交付用）"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 分布柱状图
    total = report['total']
    def bar(count, char='█', width=20):
        return char * max(1, int(count / max(total, 1) * width)) if count > 0 else '░'
    
    lines = [
        f"## 🧬 Skill生态健康看板",
        f"> {now} | {total}个skills",
        f"",
        f"| 等级 | 数量 | 分布 |",
        f"|------|------|------|",
        f"| 🟢 ≥0.85 | {report['excellent']:>3d} | {bar(report['excellent'])} |",
        f"| 🟡 0.70-0.85 | {report['good']:>3d} | {bar(report['good'])} |",
        f"| 🟠 0.50-0.70 | {report['fair']:>3d} | {bar(report['fair'])} |",
        f"| 🔴 <0.50 | {report['poor']:>3d} | {bar(report['poor'])} |",
        f"| **平均** | **{report['avg']:.3f}** | |",
        f"",
        f"### 📉 待关注",
    ]
    
    if report['fair'] > 0 or report['poor'] > 0:
        lines.append(f"> 🟠{' 🔴' if report['poor'] > 0 else ''} 以下skills需要关注：")
        for name in report['bottom_skills'][:5]:
            lines.append(f"- `{name}`")
    else:
        lines.append("> ✅ 全部skills在健康区。")
    
    lines.extend([
        f"",
        f"### 📈 最佳实践",
        f"> 🟢 以下skills是质量标杆：",
    ])
    for name in report['top_skills'][:3]:
        lines.append(f"- `{name}`")
    
    if report['auto_fixed']:
        lines.extend([
            f"",
            f"### 🔧 自动修正",
        ])
        for fix in report['auto_fixed']:
            lines.append(f"- ✅ {fix}")
    
    if report['auto_fix_failed']:
        for fail in report['auto_fix_failed']:
            lines.append(f"- ❌ {fail}")
    
    lines.append(f"\n---\n*🤖 自动健康扫描 · 每日6:00*")
    return '\n'.join(lines)


def save_report(report: dict, dashboard: str):
    """保存报告到output目录"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    
    # Markdown报告
    report_path = OUTPUT_DIR / f'ecosystem_health_{ts}.md'
    md_content = [
        f"# Skill Ecosystem Health Report",
        f"> {report['timestamp']}",
        f"",
        f"## Summary",
        f"- Total: {report['total']}",
        f"- Average: {report['avg']}",
        f"- Excellent (≥0.85): {report['excellent']}",
        f"- Good (0.70-0.85): {report['good']}",
        f"- Fair (0.50-0.70): {report['fair']}",
        f"- Poor (<0.50): {report['poor']}",
        f"",
        f"## Auto-fixed",
    ]
    for fix in report['auto_fixed']:
        md_content.append(f"- {fix}")
    report_path.write_text('\n'.join(md_content), encoding='utf-8')
    
    # 看板文本
    dashboard_path = OUTPUT_DIR / f'dashboard_{ts}.txt'
    dashboard_path.write_text(dashboard, encoding='utf-8')
    
    print(f"📊 报告: {report_path}")
    print(f"📋 看板: {dashboard_path}")
    return report_path, dashboard_path


def check_hermes_version() -> dict:
    """检查当前Hermes版本"""
    try:
        r = subprocess.run(['hermes', '--version'], capture_output=True, text=True, timeout=5)
        ver = r.stdout.strip() or r.stderr.strip()
    except:
        ver = "unknown"
    return {'version': ver, 'checked_at': datetime.now().isoformat()}


# ── 主入口 ──
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    
    if cmd == 'scan':
        print("🔍 全扫描中...")
        report = run_scan_and_fix(auto_fix=False)
        dashboard = generate_dashboard(report)
        save_report(report, dashboard)
        print(dashboard)
    
    elif cmd == 'fix':
        print("🔍 扫描+自动修正中...")
        report = run_scan_and_fix(auto_fix=True)
        # 修正后重新扫描
        report2 = run_scan_and_fix(auto_fix=False)
        dashboard = generate_dashboard(report2)
        save_report(report2, dashboard)
        print(f"✅ 修正了 {len(report['auto_fixed'])} 个skills")
        for f in report['auto_fixed']:
            print(f"  {f}")
        print()
        print(dashboard)
    
    elif cmd == 'dashboard':
        report = run_scan_and_fix(auto_fix=False)
        dashboard = generate_dashboard(report)
        print(dashboard)
    
    elif cmd == 'full':
        print("🔄 全流程：扫描 → 修正 → 报告 → 看板")
        report = run_scan_and_fix(auto_fix=True)
        report2 = run_scan_and_fix(auto_fix=False)
        dashboard = generate_dashboard(report2)
        save_report(report2, dashboard)
        
        # 同时触发记忆维护
        print("\n🧹 触发记忆维护...")
        subprocess.run([sys.executable, str(IZU_DIR / "izu_memory_maintenance.py")], 
                      timeout=300, cwd=str(IZU_DIR))
        
        print("\n" + dashboard)
        print(f"\n✅ 全流程完成")
    
    else:
        print(__doc__)
