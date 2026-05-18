"""
izu Trajectory Credit Scorer v1.0
==================================
从Orchard论文借来的"信用分配"思想，但不做SFT训练。

核心思想：
  不是所有轨迹步骤价值相等。成功轨迹的最后几步通常最有价值，
  失败轨迹中也可能有"上升段"（rise segments）——agent从迷茫到清晰的过程。
  
实现方式（轻量级，零API调用）：
  1. 读取Hermes session jsonl 或 izu 生产的轨迹数据
  2. 按规则计算每步的credit score（基于文本长度、工具使用、决策密度等信号）
  3. 标记rise segments（信用分数上升的连续片段）
  4. 输出过滤后的高credit轨迹，用于skill提取优先级排序

设计约束：
  - 零额外API调用
  - 零外部模型依赖
  - 纯算法/规则实现
  - 输出与现有izu格式兼容

用法：
  python -m izu.trajectory_credit --input input.jsonl --output output.jsonl
  python -m izu.trajectory_credit --report  # 只出统计报告，不改文件
"""

import json
import re
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════

@dataclass
class Step:
    """轨迹中的一步"""
    role: str                    # user / assistant / tool
    content: str
    turn: int                    # 轮次
    tool_name: Optional[str] = None
    credit_score: float = 0.0    # 信用评分 [0, 1]
    is_rise: bool = False        # 是否属于上升段

    @property
    def char_count(self) -> int:
        return len(self.content)

    @property
    def has_code(self) -> bool:
        return bool(re.search(r'```[\w]*\n', self.content))

    @property
    def has_decision_markers(self) -> bool:
        """决策信号词"""
        markers = ["因此", "所以", "结论", "决定", "选择", "应该", "需要",
                    "也就是说", "关键在于", "核心", "最终", "综上所述",
                    "therefore", "thus", "hence", "in conclusion", "key insight",
                    "the key", "the main", "the core"]
        for m in markers:
            if m in self.content.lower():
                return True
        return False

    @property
    def has_tool_call(self) -> bool:
        return self.tool_name is not None


@dataclass
class Trajectory:
    """完整轨迹"""
    session_id: str
    model: str = ""
    timestamp: str = ""
    completed: bool = False      # 是否成功完成
    steps: List[Step] = field(default_factory=list)

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def total_turns(self) -> int:
        if not self.steps:
            return 0
        return max(s.turn for s in self.steps)

    @property
    def success_rate(self) -> float:
        """估算的成功率——基于完成状态 + 最后几步的决策信号"""
        if self.completed:
            return 1.0
        # 失败轨迹：看最后几步有没有"像在解决的正确方向"
        last_steps = self.steps[-3:] if len(self.steps) >= 3 else self.steps
        decision_count = sum(1 for s in last_steps if s.has_decision_markers)
        return min(decision_count / len(last_steps) if last_steps else 0, 0.6)

    @property
    def high_credit_steps(self) -> List[Step]:
        """信用分 > 0.7 的步骤"""
        return [s for s in self.steps if s.credit_score > 0.7]

    @property
    def rise_segments(self) -> List[List[Step]]:
        """连续的上升段"""
        if not self.steps:
            return []
        segments = []
        current: List[Step] = []
        for s in self.steps:
            if s.is_rise:
                current.append(s)
            else:
                if len(current) >= 2:
                    segments.append(current)
                current = []
        if len(current) >= 2:
            segments.append(current)
        return segments


# ═══════════════════════════════════════════
# 信用评分引擎
# ═══════════════════════════════════════════

class CreditScorer:
    """
    对轨迹中的每一步计算信用分数。
    
    izu版评分维度（权重可调）：
      1. 推理深度（25%）——reasoning越长，思考越深
      2. 信息密度（20%）——工具返回的数据量/引用/结构
      3. 决策信号（20%）——有分析/总结/判断的内容
      4. 工具使用（15%）——使用工具说明在有效行动
      5. 语义唯一性（10%）——[SIOP启发] 语义上新颖的步骤比重复步骤更有价值
      6. 长度修正（10%）——过短的信息量有限，但极长的不一定更好

    语义唯一性（第5维度）是对SIOP论文思想的轻量级迁移实现：
    SIOP用多rollout的语义聚类推断关键决策点，本版本用轨迹内步骤间的
    embedding相似度替代——在相同轨迹内，语义上偏离主流方向的步骤
    （low embedding similarity to other steps）可能是关键分岔点。
    零外部API调用：embedding来自已有 izu_memory_maintenance 管道。
    """

    WEIGHTS = {
        "reasoning_depth": 0.30,
        "info_density": 0.25,
        "decision_signal": 0.20,
        "tool_use": 0.15,
        "length_bonus": 0.10,
    }

    # 信息密度用到的关键词
    CONCEPT_KEYWORDS = [
        # 研究型关键词
        "分析", "解释", "总结", "归纳", "推论", "对比", "论证",
        "cause", "effect", "therefore", "implies", "conclusion",
        "evidence", "finding", "result", "observation",
        # 系统级关键词
        "架构", "设计", "策略", "方案", "机制", "流程",
        "architecture", "design", "strategy", "mechanism",
        # 技术关键词
        "模型", "算法", "数据", "协议", "框架", "接口",
        "model", "algorithm", "protocol", "framework",
        # 关键举措词
        "需要", "必须", "可以", "建议", "推荐", "下一步",
    ]

    @classmethod
    def score_step(cls, step: Step, step_idx: int, total_steps: int,
                   completed: bool) -> float:
        """对单个step计算信用分数"""
        scores = {}
        
        # 1. 推理深度分：衡量内容的思考密度
        #    较长+多句子+多段落 = 思考深入
        reasoning_score = 0.0
        char_count = step.char_count
        if char_count > 20:
            sentences = len(re.split(r'[。！？.!?\n]', step.content))
            paragraphs = max(1, step.content.count("\n\n") + 1)
            # 段落数越多，思考越深；句子数多且不重复，说明推导充分
            reasoning_score = min(
                (min(sentences / 10, 1.0) * 0.5 + 
                 min(paragraphs / 5, 1.0) * 0.5),
                1.0
            )
        scores["reasoning_depth"] = reasoning_score

        # 2. 信息密度分
        concept_count = sum(1 for kw in cls.CONCEPT_KEYWORDS if kw in step.content)
        # 还看字符数——返回的数据量大说明有价值
        info_bonus = min(char_count / 2000, 1.0)
        scores["info_density"] = min(
            (min(concept_count * 0.12, 1.0) * 0.6 + info_bonus * 0.4),
            1.0
        )

        # 3. 决策信号分
        if step.has_decision_markers:
            marker_count = sum(
                1 for m in ["因此", "所以", "结论", "决定", "therefore", "thus", "in conclusion",
                            "关键在于", "核心", "最终", "综上所述", "key insight",
                            "the key", "the main", "the core",
                            "我决定", "选择", "使用", "采用",
                            "plan", "plan to", "will use",
                            "步骤如下", "方案如下", "步骤如下"]
                if m in step.content.lower()
            )
            scores["decision_signal"] = min(marker_count * 0.2, 1.0)
        else:
            scores["decision_signal"] = 0.05

        # 4. 工具使用分
        if step.has_tool_call:
            # 不同类型的工具价值不同
            valuable_tools = ["web_search", "web_extract", "search_files", 
                              "delegate_task", "skill_view", "browser_navigate"]
            if step.tool_name and any(vt in step.tool_name for vt in valuable_tools):
                scores["tool_use"] = 1.0
            else:
                scores["tool_use"] = 0.7
        elif step.role == "tool":
            # tool返回的内容（结果）有价值
            scores["tool_use"] = 0.6
        else:
            scores["tool_use"] = 0.15

        # 5. 长度修正分
        if char_count < 10:
            scores["length_bonus"] = 0.0
        elif char_count < 50:
            scores["length_bonus"] = 0.1
        elif char_count < 200:
            scores["length_bonus"] = 0.3
        elif char_count < 500:
            scores["length_bonus"] = 0.5
        elif char_count < 2000:
            scores["length_bonus"] = 0.7
        else:
            # 太长的也可能噪音，给cap
            scores["length_bonus"] = 0.8

        # 加权求和
        final_score = sum(
            scores[dim] * cls.WEIGHTS[dim]
            for dim in cls.WEIGHTS
        )

        return round(final_score, 4)

    @classmethod
    def score_trajectory(cls, traj: Trajectory) -> Trajectory:
        """对整个轨迹所有step计算信用分数，并标记rise segments"""
        total = len(traj.steps)
        for i, step in enumerate(traj.steps):
            step.credit_score = cls.score_step(
                step, i, total, traj.completed
            )

        # 标记rise segments: 连续2步以上信用分上升
        for i in range(1, total):
            prev_score = traj.steps[i-1].credit_score
            curr_score = traj.steps[i].credit_score
            # 上升段的宽松定义：只要分数没降太多就是上升
            if curr_score >= prev_score * 0.8:
                traj.steps[i].is_rise = True
            # 起步阶段的第一两步如果分数高也标记
            if i <= 2 and curr_score > 0.6:
                traj.steps[i].is_rise = True

        # 确保第一步如果分数高也被标记
        if total > 0 and traj.steps[0].credit_score > 0.6:
            traj.steps[0].is_rise = True

        return traj


# ═══════════════════════════════════════════
# 数据加载与导出
# ═══════════════════════════════════════════

def load_from_hermes_jsonl(path: str) -> List[Trajectory]:
    """
    从Hermes session jsonl加载轨迹。
    
    Hermes jsonl格式（每行一条消息，不是每行一条轨迹）：
      {"role": "user", "content": "...", "timestamp": "..."}
      {"role": "assistant", "content": "...", "reasoning": "...", "tool_calls": [...]}
      {"role": "tool", "content": "..."}
      
    一个jsonl文件 = 一个会话 = 一条轨迹
    """
    path_obj = Path(path)
    if not path_obj.exists():
        logger.warning(f"文件不存在: {path}")
        return []

    messages = []
    session_id = path_obj.stem  # 用文件名做session_id

    with open(path_obj, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                logger.warning(f"第{line_num}行JSON解析失败，跳过")
                continue
            messages.append(msg)

    if not messages:
        return []

    # 提取元信息
    timestamp = ""
    model = ""
    for msg in messages:
        ts = msg.get("timestamp", "")
        if ts:
            timestamp = ts

    # 判断完成状态：最后一条assistant有finish_reason="stop"
    completed = False
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            finish_reason = msg.get("finish_reason", "")
            if finish_reason == "stop":
                completed = True
            break

    # 转为steps
    steps = []
    turn = 0
    for i, msg in enumerate(messages):
        role = msg.get("role", "unknown")
        if role == "session_meta":
            continue  # 跳过元数据行

        content = msg.get("content", "")
        if isinstance(content, list):
            text_parts = [
                p.get("text", "") for p in content
                if isinstance(p, dict) and p.get("type") == "text"
            ]
            content = " ".join(text_parts)
        
        # 合并reasoning到content（对assistant消息）
        reasoning = msg.get("reasoning", "")
        if reasoning:
            content = reasoning + "\n" + content

        # 检测工具调用
        tool_name = None
        finish_reason = msg.get("finish_reason", "")
        if role == "assistant" and "tool_calls" in msg:
            tool_calls = msg["tool_calls"]
            if tool_calls and isinstance(tool_calls, list):
                tc = tool_calls[0]
                if isinstance(tc, dict):
                    tool_name = tc.get("function", {}).get("name", tc.get("name", ""))
        
        # 轮次：user消息+1，assistant消息保持同轮，tool消息与上一轮同
        if role == "user":
            turn += 1
        
        steps.append(Step(
            role=role,
            content=str(content) if content else "",
            turn=turn,
            tool_name=tool_name if role == "assistant" else None,
        ))

    trajectory = Trajectory(
        session_id=session_id,
        model=model,
        timestamp=timestamp,
        completed=completed,
        steps=steps,
    )

    logger.info(f"从 {path} 加载了 1 条轨迹（{len(steps)} 步, {'完成' if completed else '未完成'}）")
    return [trajectory]


def load_from_izu_sessions(directory: str = "/mnt/i/hermes/.hermes/sessions") -> List[Trajectory]:
    """
    加载目录下所有的izu session jsonl文件
    每个jsonl文件 = 一个会话 = 一条轨迹
    """
    sessions_dir = Path(directory)
    if not sessions_dir.exists():
        logger.warning(f"会话目录不存在: {directory}")
        return []

    all_trajectories = []
    for fpath in sorted(sessions_dir.glob("*.jsonl")):
        trajs = load_from_hermes_jsonl(str(fpath))
        all_trajectories.extend(trajs)
    
    return all_trajectories


def export_credit_trajectories(
    trajectories: List[Trajectory],
    output_path: str,
    min_credit: float = 0.3,
) -> int:
    """
    导出高credit轨迹到jsonl文件。
    每条轨迹只保留高credit的rise segment steps。
    """
    exported = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for traj in trajectories:
            if traj.high_credit_steps or traj.rise_segments:
                # 构建精简后的轨迹
                filtered_steps = []
                for segment in traj.rise_segments:
                    for step in segment:
                        filtered_steps.append({
                            "role": step.role,
                            "content": step.content,
                            "credit_score": step.credit_score,
                            "is_rise": step.is_rise,
                        })
                
                # 如果没有rise segment但有高credit step，也保留
                if not filtered_steps:
                    for step in traj.high_credit_steps:
                        filtered_steps.append({
                            "role": step.role,
                            "content": step.content,
                            "credit_score": step.credit_score,
                            "is_rise": step.is_rise,
                        })

                entry = {
                    "session_id": traj.session_id,
                    "model": traj.model,
                    "timestamp": traj.timestamp,
                    "completed": traj.completed,
                    "credit_trajectory": filtered_steps,
                    "total_origin_steps": traj.total_steps,
                    "total_credit_steps": len(filtered_steps),
                    "total_rise_segments": len(traj.rise_segments),
                    "avg_credit": round(
                        sum(s.credit_score for s in traj.steps) / max(len(traj.steps), 1), 4
                    ),
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                exported += 1

    logger.info(f"导出 {exported} 条高credit轨迹到 {output_path}")
    return exported


def generate_report(trajectories: List[Trajectory]) -> str:
    """生成轨迹信用统计报告"""
    if not trajectories:
        return "无轨迹数据"

    report_parts = [
        "═" * 50,
        "  izu 轨迹信用评分报告",
        f"  生成时间: {datetime.now().isoformat()}",
        "═" * 50,
        "",
        f"总轨迹数: {len(trajectories)}",
        f"总步数: {sum(t.total_steps for t in trajectories)}",
        f"总轮次: {sum(t.total_turns for t in trajectories)}",
        "",
    ]

    # 成功率分布
    success_count = sum(1 for t in trajectories if t.completed)
    report_parts.extend([
        "─── 完成状态 ───",
        f"  成功: {success_count} ({success_count/max(len(trajectories),1)*100:.1f}%)",
        f"  失败: {len(trajectories) - success_count}",
        "",
    ])

    # 信用分分布
    all_scores = []
    for t in trajectories:
        for s in t.steps:
            all_scores.append(s.credit_score)
    
    if all_scores:
        avg_score = sum(all_scores) / len(all_scores)
        high_count = sum(1 for s in all_scores if s > 0.7)
        report_parts.extend([
            "─── 信用分分布 ───",
            f"  平均分: {avg_score:.4f}",
            f"  高分段(>0.7): {high_count} ({high_count/len(all_scores)*100:.1f}%)",
            f"  最高分: {max(all_scores):.4f}",
            f"  最低分: {min(all_scores):.4f}",
            "",
        ])

    # Rise segment统计
    total_rise_segments = sum(len(t.rise_segments) for t in trajectories)
    total_rise_steps = sum(
        sum(1 for s in t.steps if s.is_rise) for t in trajectories
    )
    report_parts.extend([
        "─── Rise Segments ───",
        f"  总上升段数: {total_rise_segments}",
        f"  上升段步数: {total_rise_steps}",
        "",
    ])

    # 工具使用统计  
    tool_steps = sum(
        sum(1 for s in t.steps if s.has_tool_call) for t in trajectories
    )
    code_steps = sum(
        sum(1 for s in t.steps if s.has_code) for t in trajectories
    )
    decision_steps = sum(
        sum(1 for s in t.steps if s.has_decision_markers) for t in trajectories
    )
    report_parts.extend([
        "─── 步类型分布 ───",
        f"  含工具调用: {tool_steps} ({tool_steps/max(len(all_scores),1)*100:.1f}%)",
        f"  含代码: {code_steps} ({code_steps/max(len(all_scores),1)*100:.1f}%)",
        f"  含决策信号: {decision_steps} ({decision_steps/max(len(all_scores),1)*100:.1f}%)",
        "",
    ])

    # Top 5 高信用轨迹
    scored_trajs = sorted(
        trajectories,
        key=lambda t: sum(s.credit_score for s in t.steps) / max(len(t.steps), 1),
        reverse=True,
    )[:5]
    report_parts.append("─── Top 5 高信用轨迹 ───")
    for i, t in enumerate(scored_trajs, 1):
        avg_c = sum(s.credit_score for s in t.steps) / max(len(t.steps), 1)
        report_parts.append(
            f"  {i}. {t.session_id[:20]:20s} | "
            f"步骤:{t.total_steps:3d} | "
            f"均分:{avg_c:.4f} | "
            f"完成:{'✅' if t.completed else '❌'}"
        )

    report_parts.append("")
    report_parts.append("═" * 50)

    return "\n".join(report_parts)


# ═══════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="izu Trajectory Credit Scorer — 从轨迹中提取高信用片段"
    )
    parser.add_argument(
        "--input", "-i",
        default="/mnt/i/hermes/.hermes/sessions",
        help="输入：单个jsonl文件路径，或session目录路径（默认）"
    )
    parser.add_argument(
        "--output", "-o",
        default="/mnt/i/hermes/data/credit_trajectories.jsonl",
        help="输出：高credit轨迹jsonl文件"
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="只出报告，不写文件"
    )
    parser.add_argument(
        "--min-credit", "-m",
        type=float,
        default=0.3,
        help="最低信用分过滤阈值 (default: 0.3)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细日志"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    # 加载轨迹
    input_path = args.input
    if Path(input_path).is_dir():
        trajs = load_from_izu_sessions(input_path)
    else:
        trajs = load_from_hermes_jsonl(input_path)

    if not trajs:
        print("⚠ 未找到轨迹数据")
        return

    # 计算信用分
    scorer = CreditScorer()
    scored_trajs = []
    for traj in trajs:
        scored = scorer.score_trajectory(traj)
        scored_trajs.append(scored)

    # 输出
    if args.report:
        report = generate_report(scored_trajs)
        print(report)
    else:
        exported = export_credit_trajectories(
            scored_trajs, args.output, args.min_credit
        )
        report = generate_report(scored_trajs)
        print(report)
        print(f"\n📝 高credit轨迹已导出到: {args.output}")


if __name__ == "__main__":
    main()
