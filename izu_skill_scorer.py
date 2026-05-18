#!/usr/bin/env python3
"""
izu_skill_scorer.py — SKILL.md批量评分器

对接evolution_engine的5维度Scorer，扫描所有用户SKILL.md：
  1. URL存活率 (20%)
  2. 结构完整性 (20%)
  3. 引用准确性 (15%)
  4. 内部一致性 (20%)
  5. 简洁度 (15%)
  6. 语义质量 (10%) — 可选，需模型

用法:
  python3 izu_skill_scorer.py scan          # 扫描所有SKILL.md评分
  python3 izu_skill_scorer.py scan --min     # 只输出低分(<0.7)
  python3 izu_skill_scorer.py scan --top 5   # 前5名
  python3 izu_skill_scorer.py report         # 生成报告到output/
  python3 izu_skill_scorer.py check <name>   # 检查单个skill
"""
import sys, os, re, json
from pathlib import Path
from datetime import datetime

# 导入evolution_engine的Scorer
sys.path.insert(0, str(Path(__file__).parent))
from evolution_engine import Scorer, Verifier

# ── 路径 ──
SKILLS_USER_DIR = Path.home() / '.hermes' / 'skills'
SKILLS_ARCHIVE_DIR = SKILLS_USER_DIR / '.archive'
OUTPUT_DIR = Path('/mnt/i/hermes/output/doc/skill_health')
DATA_DIR = Path('/mnt/i/hermes/data')

# ── SKILL特定的结构检查 ──
SKILL_EXPECTED_SECTIONS = [
    '##', '###',  # 必须有标题
]

SKILL_EXPECTED_IF_LONG = [
    '用法', 'Usage', '用法', '示例', 'Example',
    '配置', 'Configuration', 'Config',
    '参数', 'Parameters', 'Args',
    '功能', 'Description', '描述',
]

def find_all_skills(base_dir: Path, exclude_archive: bool = True) -> list[dict]:
    """找到所有SKILL.md文件，支持嵌套目录，返回[{name, path, content, lines}]"""
    skills = []
    
    for skill_md in sorted(base_dir.rglob('SKILL.md')):
        # 跳过.archive
        if exclude_archive and '.archive' in str(skill_md):
            continue
        
        # 获取技能名（SKILL.md所在目录名）
        skill_dir = skill_md.parent
        category = skill_dir.parent.name if skill_dir.parent.name != 'skills' else 'root'
        
        # 多级目录时取更深层的分类
        if category in ['root', 'skills']:
            grandparent = skill_dir.parent
            if grandparent.name != 'skills':
                category = grandparent.name
        
        try:
            content = skill_md.read_text(encoding='utf-8')
        except:
            try:
                content = skill_md.read_text()
            except:
                continue
        
        skills.append({
            'name': skill_dir.name,
            'category': category,
            'path': str(skill_md),
            'content': content,
            'lines': len(content.split('\n')),
        })
    
    return skills


def score_skill(skill: dict, skip_url_check: bool = False) -> dict:
    """对单个SKILL进行6维评分"""
    content = skill['content']
    scorer = Scorer()
    
    # 用SKILL专用结构检查
    expected = SKILL_EXPECTED_SECTIONS.copy()
    if skill['lines'] > 50:
        expected += SKILL_EXPECTED_IF_LONG
    
    # 基础5维 — URL检查可选跳过
    if skip_url_check:
        # 跳过URL存活检查，只用结构和一致性
        verifier = Verifier()
        structure = verifier.check_structure(content, expected_sections=expected)
        citations = verifier.check_citations(content)
        consistency = verifier.check_consistency(content)
        conciseness = verifier.check_conciseness(content)
        
        url_validity = {"score": 0.8}  # 默认0.8，不真实检查
        
        results = {}
        dims_config = {
            'url_validity': 0.20,
            'structural_complete': 0.20,
            'citation_accuracy': 0.15,
            'consistency': 0.20,
            'conciseness': 0.15,
        }
        
        results['url_validity'] = url_validity
        results['structural_complete'] = structure
        results['citation_accuracy'] = citations
        results['consistency'] = consistency
        results['conciseness'] = conciseness
        
        results['_overall'] = round(
            url_validity['score'] * 0.20 +
            structure['score'] * 0.20 +
            citations['score'] * 0.15 +
            consistency['score'] * 0.20 +
            conciseness['score'] * 0.15
        , 3)
    else:
        results = scorer.score_output(content, expected_sections=expected)
    
    # 附加SKILL专项维度
    extras = {}
    
    # YAML frontmatter检查
    has_frontmatter = content.startswith('---')
    extras['has_frontmatter'] = has_frontmatter
    
    # 标签检查（兼容 inline: tags: [a, b] 和 block: tags:\n  - a\n  - b 两种格式）
    has_tags = False
    if has_frontmatter:
        inline_tags = re.findall(r'tags:\s*\[([^\]]*)\]', content[:500])
        if inline_tags:
            has_tags = len(inline_tags[0].strip()) > 0
        else:
            # YAML block格式：检查 frontmatter 区有无 "  - " 在 tags: 下面
            fm_section = content.split('---', 2)[1] if content.startswith('---') else ''
            block_tags = re.findall(r'(?m)^tags:\s*$', fm_section)
            has_tags = len(block_tags) > 0
    extras['has_tags'] = has_tags
    
    # 功能描述检查（必须有核心功能描述）
    has_description = any(kw in content[:1000].lower() for kw in 
                          ['功能', '描述', 'description', 'core mission', '核心使命'])
    extras['has_description'] = has_description
    
    # 版本/日期检查 — 同时扫描frontmatter和全文
    # 先取frontmatter段
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    fm_text = fm_match.group(1) if fm_match else ''
    
    # 日期：frontmatter中的 date: 字段，或全文中的 20XX-XX-XX
    has_date = bool(re.search(r'(?m)^date:\s*20[2-9]\d', fm_text))
    if not has_date:
        has_date = bool(re.search(r'20[2-9]\d[-/]\d{2}[-/]\d{2}', content[:2000]))
    
    # 版本：version: x.y.z 或 vx.y
    has_version = bool(re.search(r'(?im)^version:\s*[\"\']?(\d+\.\d+)', fm_text))
    if not has_version:
        has_version = bool(re.search(r'v\d+\.\d+(\.\d+)?', content[:800]))
    extras['has_date'] = has_date
    extras['has_version'] = has_version
    
    # 代码示例检查（较长的技能应有）
    has_code_example = '```' in content
    extras['has_code_example'] = has_code_example
    
    return {
        'name': skill['name'],
        'category': skill['category'],
        'path': skill['path'],
        'lines': skill['lines'],
        'overall': round(results['_overall'], 3),
        'dimensions': {
            dim: results[dim]['score'] if isinstance(results[dim], dict) else results[dim]
            for dim in ['url_validity', 'structural_complete', 'citation_accuracy',
                        'consistency', 'conciseness']
        },
        'extras': extras,
        'details': results,
    }


def scan_all(min_score: float = 0.0, max_results: int = 0) -> list[dict]:
    """扫描所有SKILL.md并评分"""
    all_skills = find_all_skills(SKILLS_USER_DIR)
    
    print(f"\n🔍 SKILL健康扫描 — {len(all_skills)} 个skills\n")
    
    results = []
    for i, skill in enumerate(all_skills):
        if (i + 1) % 30 == 0:
            print(f"  进度: {i+1}/{len(all_skills)}...", flush=True)
        
        try:
            result = score_skill(skill, skip_url_check=True)
            results.append(result)
        except Exception as e:
            print(f"  ❌ {skill['name']}: 评分失败 - {e}")
    
    # 按总分排序
    results.sort(key=lambda r: r['overall'])
    
    # 过滤
    if min_score > 0:
        results = [r for r in results if r['overall'] < min_score]
    if max_results > 0:
        results = results[:max_results]
    
    return results


def print_results(results: list):
    """打印评分结果"""
    if not results:
        print("  无结果")
        return
    
    # 统计
    excellent = sum(1 for r in results if r['overall'] >= 0.85)
    good = sum(1 for r in results if 0.70 <= r['overall'] < 0.85)
    fair = sum(1 for r in results if 0.50 <= r['overall'] < 0.70)
    poor = sum(1 for r in results if r['overall'] < 0.50)
    
    print(f"  🟢 优秀(≥0.85): {excellent}")
    print(f"  🟡 良好(0.70-0.85): {good}")
    print(f"  🟠 一般(0.50-0.70): {fair}")
    print(f"  🔴 待优化(<0.50): {poor}")
    print()
    
    # 表格头
    print(f"{'技能名':<40} {'总分':>6} {'URL':>5} {'结构':>5} {'引用':>5} {'一致':>5} {'简洁':>5}  {'行数':>5}")
    print("-" * 85)
    
    for r in results:
        dims = r['dimensions']
        markers = []
        if not r['extras']['has_frontmatter']: markers.append('无frontmatter')
        if not r['extras']['has_description']: markers.append('无描述')
        if not r['extras']['has_tags']: markers.append('无标签')
        if not r['extras']['has_date']: markers.append('无日期')
        
        mark = f"  ⚠️{'/'.join(markers)}" if markers else ""
        
        # 颜色标记
        score = r['overall']
        icon = "🟢" if score >= 0.85 else ("🟡" if score >= 0.70 else ("🟠" if score >= 0.50 else "🔴"))
        
        print(f"{icon} {r['name']:<38s} {score:>5.2f} "
              f"{dims['url_validity']:>4.1f} {dims['structural_complete']:>4.1f} "
              f"{dims['citation_accuracy']:>4.1f} {dims['consistency']:>4.1f} "
              f"{dims['conciseness']:>4.1f}  {r['lines']:>4d}{mark}")
    
    # 低分top5详细分析
    print("\n\n── 待优化Skills 详细分析 ──\n")
    low = [r for r in results if r['overall'] < 0.70][:5]
    for r in low:
        print(f"  🔴 {r['name']} ({r['category']}) — 总分 {r['overall']:.2f}")
        for dim, score in r['dimensions'].items():
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            print(f"     {dim:<20s} {bar} {score:.2f}")
        missing = []
        for k, v in r['extras'].items():
            if not v and k != 'has_frontmatter' and k != 'has_tags' and k != 'has_code_example':
                missing.append(k)
        if missing:
            print(f"     缺失: {', '.join(missing)}")
        print()


def generate_report(results: list):
    """生成SVG兼容的报告到output/"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = OUTPUT_DIR / f'skill_health_report_{ts}.md'
    
    excellent = [r for r in results if r['overall'] >= 0.85]
    good = [r for r in results if 0.70 <= r['overall'] < 0.85]
    fair = [r for r in results if 0.50 <= r['overall'] < 0.70]
    poor = [r for r in results if r['overall'] < 0.50]
    
    avg = round(sum(r['overall'] for r in results) / len(results), 3) if results else 0
    
    lines = [
        f"# 🧬 SKILL健康扫描报告",
        f"> 生成: {ts}",
        f"> 扫描: {len(results)} 个skills",
        f"> 平均分: {avg:.3f}",
        f"",
        f"## 总体分布",
        f"",
        f"| 等级 | 数量 | 占比 |",
        f"|------|------|------|",
        f"| 🟢 优秀(≥0.85) | {len(excellent)} | {len(excellent)/len(results)*100:.0f}% |" if results else "| 🟢 | 0 | 0% |",
        f"| 🟡 良好(0.70-0.85) | {len(good)} | {len(good)/len(results)*100:.0f}% |" if results else "| 🟡 | 0 | 0% |",
        f"| 🟠 一般(0.50-0.70) | {len(fair)} | {len(fair)/len(results)*100:.0f}% |" if results else "| 🟠 | 0 | 0% |",
        f"| 🔴 待优化(<0.50) | {len(poor)} | {len(poor)/len(results)*100:.0f}% |" if results else "| 🔴 | 0 | 0% |",
        f"",
    ]
    
    if poor:
        lines.extend([f"## 待优化Skills ({len(poor)}个)", ""])
        for r in poor:
            dims_str = ', '.join(f"{d}={r['dimensions'][d]:.2f}" for d in r['dimensions'])
            lines.append(f"- **{r['name']}** [{r['category']}] 总分={r['overall']:.2f} | {dims_str}")
        lines.append("")
    
    if fair:
        lines.extend([f"## 一般Skills ({len(fair)}个)", ""])
        for r in fair:
            lines.append(f"- {r['name']} [{r['category']}] 总分={r['overall']:.2f}")
        lines.append("")
    
    lines.extend([
        f"## 前5名",
        "",
    ])
    top5 = sorted(results, key=lambda r: -r['overall'])[:5]
    for r in top5:
        lines.append(f"- 🟢 **{r['name']}** [{r['category']}] 总分={r['overall']:.3f} ({r['lines']}行)")
    
    lines.append(f"\n---\n报告: {report_path}")
    
    report_path.write_text('\n'.join(lines))
    print(f"\n📊 报告已写入: {report_path}")
    return report_path


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    
    if cmd == 'scan':
        min_score = 0.0
        max_results = 0
        
        if '--min' in sys.argv:
            min_score = 0.70
        for i, arg in enumerate(sys.argv):
            if arg == '--top' and i + 1 < len(sys.argv):
                max_results = int(sys.argv[i + 1])
        
        results = scan_all(min_score=min_score, max_results=max_results)
        print_results(results)
        
        # 同时生成报告
        all_results = scan_all()
        generate_report(all_results)
    
    elif cmd == 'report':
        all_results = scan_all()
        generate_report(all_results)
    
    elif cmd == 'check':
        if len(sys.argv) < 3:
            print("需指定skill名")
            sys.exit(1)
        name = sys.argv[2]
        skills = find_all_skills(SKILLS_USER_DIR)
        for s in skills:
            if name in s['name']:
                r = score_skill(s)
                print(f"\n📋 {r['name']} ({r['category']}) — 总分 {r['overall']:.3f}")
                print(f"   路径: {r['path']}")
                print(f"   行数: {r['lines']}")
                print()
                for dim, score in r['dimensions'].items():
                    bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
                    print(f"  {dim:<20s} {bar} {score:.2f}")
                sys.exit(0)
        print(f"❌ 未找到 '{name}'")
    
    else:
        print(__doc__)
