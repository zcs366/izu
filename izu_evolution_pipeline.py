#!/usr/bin/env python3
"""
izu_evolution_pipeline.py — 进化循环集成管道

统一 trajectory_credit + trajectory_balance + evolution_engine 三个组件：
  1. 扫描最近session → 提取轨迹
  2. 计算credit score → 标记rise segments
  3. 更新balance采样统计
  4. 记录短板到顶级Agent拓扑数据
  5. 输出进化报告

用法:
  python3 izu_evolution_pipeline.py run           # 运行完整进化管道
  python3 izu_evolution_pipeline.py report        # 只输出当前拓扑状态
"""
import sys, json, os
from pathlib import Path
from datetime import datetime, timedelta

# ── 路径 ──
IZU_DIR = Path(__file__).parent
SESSION_DIR = Path.home() / '.hermes' / 'sessions'
DATA_DIR = Path('/mnt/i/hermes/data')
OUTPUT_DIR = Path('/mnt/i/hermes/output/doc/evolution')

# 导入各模块
sys.path.insert(0, str(IZU_DIR))
from trajectory_credit import (
    load_from_hermes_jsonl, CreditScorer, Trajectory
)
from trajectory_balance import BalancedSampler
from evolution_engine import Scorer, EvolutionTrigger


def get_latest_sessions(limit: int = 10) -> list[Path]:
    """获取最近的JSON/JSONL session文件"""
    sessions = sorted(SESSION_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
    sessions += sorted(SESSION_DIR.glob('*.jsonl'), key=os.path.getmtime, reverse=True)
    return sessions[:limit]


def run_pipeline() -> dict:
    """完整进化管道：轨迹→信用→平衡→进化记录"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"🧬 进化管道 — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    result = {
        'sessions_processed': 0,
        'total_steps': 0,
        'high_credit_steps': 0,
        'rise_segments': 0,
        'task_types': {},
        'weaknesses_recorded': [],
        'timestamp': datetime.now().isoformat(),
    }
    
    # Step 1: 加载最近session
    sessions = get_latest_sessions(limit=15)
    print(f"📥 Step 1: 加载 {len(sessions)} 个最近session...")
    
    all_trajectories = []
    for s in sessions:
        try:
            raw = json.loads(s.read_text(encoding='utf-8'))
            if isinstance(raw, dict) and 'messages' in raw:
                # 转换为trajectory_credit期望的jsonl格式
                from trajectory_credit import Step as TCStep, Trajectory as TCTrajectory
                steps = []
                for i, msg in enumerate(raw.get('messages', [])):
                    role = msg.get('role', '')
                    content = msg.get('content', '') or ''
                    if isinstance(content, list):
                        text_parts = [p.get('text','') for p in content if isinstance(p,dict)]
                        content = ' '.join(text_parts)
                    
                    tool_name = None
                    if role == 'assistant' and 'tool_calls' in msg:
                        for tc in msg['tool_calls']:
                            fn = tc.get('function',{}).get('name', tc.get('name',''))
                            if fn: tool_name = fn
                    
                    steps.append(TCStep(
                        role=role,
                        content=str(content) if content else '',
                        turn=i,
                        tool_name=tool_name if role == 'assistant' else None,
                    ))
                
                completed = any(m.get('finish_reason') == 'stop' for m in reversed(raw.get('messages',[])) if m.get('role') == 'assistant')
                
                traj = TCTrajectory(
                    session_id=raw.get('session_id', s.stem),
                    model=raw.get('model', ''),
                    completed=completed,
                    steps=steps,
                )
                all_trajectories.append(traj)
            else:
                # 退回到jsonl加载
                from trajectory_credit import load_from_hermes_jsonl
                trajs = load_from_hermes_jsonl(str(s))
                all_trajectories.extend(trajs)
        except Exception as e:
            print(f"  ⚠️ {s.name}: {e}")
    
    if not all_trajectories:
        print("  ❌ 无可解析的轨迹")
        return result
    
    result['sessions_processed'] = len(all_trajectories)
    print(f"  ✅ 解析 {len(all_trajectories)} 条轨迹")
    
    # Step 2: 信用评分
    print(f"\n📊 Step 2: 轨迹信用评分...")
    scorer = CreditScorer()
    high_credit = 0
    total_steps = 0
    
    for traj in all_trajectories:
        scored = scorer.score_trajectory(traj)
        total_steps += len(scored.steps)
        high_credit += len(scored.high_credit_steps)
        
        if scored.rise_segments:
            result['rise_segments'] += len(scored.rise_segments)
            for seg in scored.rise_segments[:3]:  # 只记录前3段
                print(f"  📈 Rise segment: {seg[0].role} → {seg[-1].role} ({len(seg)}步, credit={seg[-1].credit_score:.2f})")
    
    result['total_steps'] = total_steps
    result['high_credit_steps'] = high_credit
    print(f"  {total_steps} 步, {high_credit} 高信用步, {result['rise_segments']} 上升段")
    
    # 从高信用轨迹中提取有用模式
    patterns = []
    for traj in all_trajectories:
        scored = scorer.score_trajectory(traj)
        for seg in scored.rise_segments[:2]:  # 每轨迹最多2段
            tools_used = [s.tool_name for s in seg if s.tool_name]
            if tools_used:
                patterns.append({
                    'session_id': traj.session_id,
                    'rise_tools': tools_used,
                    'step_count': len(seg),
                    'avg_credit': round(sum(s.credit_score for s in seg) / len(seg), 3)
                })
    
    # Step 3: 平衡采样更新
    print(f"\n⚖️ Step 3: 平衡采样统计...")
    sampler = BalancedSampler()
    task_type_counts = {}
    
    for traj in all_trajectories:
        for step in traj.steps:
            if step.role == 'user' and step.content:
                # 简单分类
                c = step.content.lower()
                if any(w in c for w in ['研究', '分析', '搜索']):
                    tt = 'research'
                elif any(w in c for w in ['写', '创建', '生成']):
                    tt = 'writing'
                elif any(w in c for w in ['代码', '编程', '实现']):
                    tt = 'coding'
                elif '?':
                    tt = 'question'
                else:
                    tt = 'other'
                
                sampler.record(tt, success=traj.completed)
                task_type_counts[tt] = task_type_counts.get(tt, 0) + 1
    
    result['task_types'] = task_type_counts
    sampler.save_state()
    print(f"  {len(task_type_counts)} 种任务类型: {task_type_counts}")
    
    # Step 4: 记录到进化引擎
    print(f"\n🧬 Step 4: 进化状态记录...")
    
    # 构建/更新topology数据
    topo_file = DATA_DIR / 'izu-agent-topology-data.json'
    topo_path = str(topo_file)
    
    if topo_file.exists():
        with open(topo_path) as f:
            topo = json.load(f)
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        topo = {
            "agents": {},
            "last_evolution": None,
            "total_evolutions": 0
        }
    
    # 为每个session/task_type创建agent记录
    for traj in all_trajectories:
        agent_id = traj.session_id[:16]
        if agent_id not in topo['agents']:
            topo['agents'][agent_id] = {
                "performance_history": {
                    "total_tasks_completed": 0,
                    "avg_quality_score": 0.5,
                },
                "evolution_state": {
                    "current_generation": 0,
                    "identified_weaknesses": [],
                    "prompt_adjustments_applied": [],
                    "last_verified_at": None,
                },
                "credit_profile": {
                    "total_steps": 0,
                    "high_credit_steps": 0,
                    "avg_credit": 0.0,
                }
            }
        
        agent = topo['agents'][agent_id]
        ph = agent['performance_history']
        cp = agent['credit_profile']
        
        scored = scorer.score_trajectory(traj)
        avg_cr = round(sum(s.credit_score for s in scored.steps) / max(len(scored.steps), 1), 3)
        
        ph['total_tasks_completed'] += 1
        n = ph['total_tasks_completed']
        ph['avg_quality_score'] = (ph['avg_quality_score'] * (n-1) + (1.0 if traj.completed else 0.3)) / n
        
        cp['total_steps'] += len(scored.steps)
        cp['high_credit_steps'] += len(scored.high_credit_steps)
        # 滚动平均
        cp['avg_credit'] = (cp['avg_credit'] * (n-1) + avg_cr) / n
    
    # 记录进化
    topo['last_evolution'] = datetime.now().isoformat()
    topo['total_evolutions'] = topo.get('total_evolutions', 0) + 1
    
    # 识别循环中的短板
    all_weaknesses = []
    for agent_id, agent_data in topo['agents'].items():
        for w in agent_data['evolution_state']['identified_weaknesses']:
            all_weaknesses.append(w)
    
    weakness_summary = {}
    for w in all_weaknesses:
        weakness_summary[w] = weakness_summary.get(w, 0) + 1
    
    result['weaknesses_recorded'] = weakness_summary
    
    # 写入
    with open(topo_path, 'w') as f:
        json.dump(topo, f, indent=2, ensure_ascii=False)
    print(f"  ✅ 已更新 {len(topo['agents'])} 个agent记录")
    if weakness_summary:
        print(f"  短板分布: {weakness_summary}")
    
    # Step 5: 生成报告
    print(f"\n📋 Step 5: 生成进化报告...")
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = OUTPUT_DIR / f'evolution_report_{ts}.md'
    
    report_lines = [
        f"# 🧬 进化循环报告",
        f"> 生成: {ts}",
        f"",
        f"## 本次处理",
        f"",
        f"| 维度 | 数值 |",
        f"|------|------|",
        f"| 处理session数 | {result['sessions_processed']} |",
        f"| 总步数 | {result['total_steps']} |",
        f"| 高信用步 | {result['high_credit_steps']} |",
        f"| 上升段 | {result['rise_segments']} |",
        f"| 任务类型 | {len(result['task_types'])} |",
        f"| Agent记录 | {len(topo['agents'])} |",
        f"| 总进化次数 | {topo['total_evolutions']} |",
        f"",
    ]
    
    if patterns:
        report_lines.append("## 高价值模式 (rise segments工具序列)")
        report_lines.append("")
        for p in patterns[:5]:
            report_lines.append(f"- Session {p['session_id'][:20]}: {', '.join(p['rise_tools'][:4])} (avg credit {p['avg_credit']})")
        report_lines.append("")
    
    if result['task_types']:
        report_lines.append("## 任务分布")
        report_lines.append("")
        report_lines.append(f"| 类型 | 次数 | 占比 |")
        report_lines.append(f"|------|------|------|")
        total_tasks = sum(result['task_types'].values())
        for tt, count in sorted(result['task_types'].items(), key=lambda x: -x[1]):
            report_lines.append(f"| {tt} | {count} | {count/total_tasks*100:.0f}% |")
        report_lines.append("")
    
    if weakness_summary:
        report_lines.append("## 短板分布")
        report_lines.append("")
        for w, c in sorted(weakness_summary.items(), key=lambda x: -x[1]):
            report_lines.append(f"- {w}: {c}次")
        report_lines.append("")
    
    report_lines.append("---")
    report_lines.append(f"报告: {report_path}")
    
    report_path.write_text('\n'.join(report_lines))
    print(f"  ✅ 报告: {report_path}")
    print(f"\n✅ 进化管道完成")
    
    return result


def cmd_report():
    """输出当前拓扑状态"""
    topo_file = DATA_DIR / 'izu-agent-topology-data.json'
    if not topo_file.exists():
        return print("❌ 无拓扑数据")
    
    with open(topo_file) as f:
        topo = json.load(f)
    
    print(f"\n📊 进化引擎拓扑状态")
    print(f"   最后进化: {topo.get('last_evolution', 'N/A')}")
    print(f"   总进化次数: {topo.get('total_evolutions', 0)}")
    print(f"   Agent数: {len(topo['agents'])}")
    print()
    
    # 统计
    scores = [a['performance_history']['avg_quality_score'] for a in topo['agents'].values()]
    credits = [a['credit_profile']['avg_credit'] for a in topo['agents'].values() if a['credit_profile']['avg_credit'] > 0]
    
    if scores:
        print(f"   平均质量分: {sum(scores)/len(scores):.3f}")
    if credits:
        print(f"   平均信用分: {sum(credits)/len(credits):.3f}")
    
    # 短板排
    all_w = []
    for a in topo['agents'].values():
        all_w.extend(a['evolution_state']['identified_weaknesses'])
    if all_w:
        from collections import Counter
        print(f"\n   短板排行:")
        for w, c in Counter(all_w).most_common(5):
            print(f"     {w}: {c}次")
    
    print(f"\n   数据文件: {topo_file}")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'run'
    if cmd == 'run':
        run_pipeline()
    elif cmd == 'report':
        cmd_report()
    else:
        print(__doc__)
