"""
izu Trajectory Balance Sampler v1.0
====================================
从Orchard论文借来的"Balanced Adaptive Rollout"思想，但不做RL训练。

核心思想：
  BAR的核心是"不平衡就不提交"——正负奖励比例达标才结束采样。
  迁移到izu后：收集轨迹时主动平衡简单任务和困难任务的采样比例，
  避免batch_runner只收集简单任务的轨迹。

实现方式：
  1. 监控每个任务类型的成功率
  2. 当某类任务成功率>80%时降低采样权重，<20%时提高
  3. 目标：各任务类型采样数量大致均衡
  4. 使用目标比例[0.3, 0.7]：正难负易

用法：
  from izu.trajectory_balance import BalancedSampler
  
  sampler = BalancedSampler()
  sampler.record("web_search", success=True)  # 记录一次成功
  should_sample = sampler.should_sample("web_search")  # 是否应该采样
  weight = sampler.get_weight("research_write")  # 获取任务的采样权重
"""

import json
import logging
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class TaskClassifier:
    """
    将任务描述/查询分类为任务类型。
    
    规则简单：根据关键词匹配，不是机器学习。
    可扩展——子类化后覆盖CLASSIFY_RULES即可。
    """

    CLASSIFY_RULES = [
        # (关键词列表, 任务类型)
        (["研究", "分析", "调查", "对比", "研读", "research", "analyze",
          "study", "investigate", "literature", "survey"], "research"),
        (["搜索", "查找", "查", "查找资料", "search", "find", "look up",
          "google", "bing", "web"], "search"),
        (["写", "撰写", "生成", "总结", "整理", "write", "summarize",
          "generate", "draft", "compose", "produce"], "writing"),
        (["编程", "代码", "开发", "实现", "修", "debug", "code", "program",
          "implement", "fix", "bug", "feature", "refactor"], "coding"),
        (["审阅", "检查", "审", "review", "check", "inspect",
          "validate", "verify", "test"], "review"),
        (["设计", "架构", "规划", "设计模式", "design", "architect",
          "plan", "blueprint", "schema"], "design"),
        (["配置", "安装", "部署", "设置", "setup", "install",
          "configure", "deploy", "config"], "setup"),
        (["翻译", "translate", "convert", "transfer"], "translation"),
        (["对话", "聊天", "chat", "talk", "询问", "问", "ask"], "chat"),
    ]

    @classmethod
    def classify(cls, prompt: str) -> str:
        """根据prompt内容分类"""
        prompt_lower = prompt.lower()
        for keywords, task_type in cls.CLASSIFY_RULES:
            if any(kw in prompt_lower for kw in keywords):
                return task_type
        return "other"

    @classmethod
    def classify_from_trajectory(cls, steps: List) -> str:
        """从轨迹steps中推断任务类型"""
        if not steps:
            return "other"
        # 用user消息的prompt来判断
        for step in steps:
            if hasattr(step, 'role') and step.role == "user":
                return cls.classify(str(step.content)[:200])
            if isinstance(step, dict) and step.get("role") == "user":
                return cls.classify(str(step.get("content", ""))[:200])
        return "other"


class BalancedSampler:
    """
    平衡轨迹采样器。
    
    维护每个任务类型的成功率统计，
    自动调整采样权重，使各类任务采样数量趋向均衡。
    
    Orchard BAR思想迁移：
      - BAR的目标是正负奖励比例[0.375, 0.625]
      - 这里的目标是通过平衡采样防止数据偏斜
      - 不是RL，是采样策略
    """

    # 目标比例：成功率低（困难）的任务应该被更多采样
    # 成功率高（简单）的任务应该少采样
    TARGET_SUCCESS_WINDOW = (0.3, 0.7)  # [低, 高]
    
    # 采样权重范围
    MIN_WEIGHT = 0.2
    MAX_WEIGHT = 3.0
    DEFAULT_WEIGHT = 1.0

    # 平滑因子——新记录的权重
    SMOOTHING = 0.3

    def __init__(self, state_file: Optional[str] = None):
        self._stats: Dict[str, Dict] = defaultdict(lambda: {
            "total": 0,
            "success": 0,
            "fail": 0,
            "sampled": 0,  # 被采样的次数
            "last_updated": None,
        })
        self._task_queue: List[Tuple[str, float]] = []  # (task_type, priority)
        self._state_file = state_file or "/mnt/i/hermes/data/sampler_state.json"
        self._load_state()

    # ── 记录接口 ──

    def record(self, task_type: str, success: bool, details: str = ""):
        """记录一次任务执行结果"""
        stats = self._stats[task_type]
        stats["total"] += 1
        if success:
            stats["success"] += 1
        else:
            stats["fail"] += 1
        stats["sampled"] += 1
        stats["last_updated"] = datetime.now().isoformat()
        logger.debug(
            f"轨迹记录: {task_type} | {'✅' if success else '❌'} "
            f"| 总量:{stats['total']} | 成功率:{self.success_rate(task_type):.1%}"
        )

    def record_from_trajectory(self, steps: List, completed: bool):
        """从轨迹steps中自动提取任务类型并记录"""
        task_type = TaskClassifier.classify_from_trajectory(steps)
        self.record(task_type, success=completed)

    # ── 查询接口 ──

    def success_rate(self, task_type: str) -> float:
        """某类任务的成功率"""
        stats = self._stats[task_type]
        if stats["total"] == 0:
            return 0.5  # 初始不确定值
        return stats["success"] / stats["total"]

    def get_weight(self, task_type: str) -> float:
        """获取某类任务的采样权重。
        
        Orchard BAR思想转换：
          - 成功率低 → 权重高（困难任务多采样）
          - 成功率高 → 权重低（简单任务少采样）
          - 无数据 → 默认权重
        """
        rate = self.success_rate(task_type)
        if rate == 0.5:  # 无数据
            return self.DEFAULT_WEIGHT
        
        # 在TARGET窗口内 → 正常权重
        if self.TARGET_SUCCESS_WINDOW[0] <= rate <= self.TARGET_SUCCESS_WINDOW[1]:
            return self.DEFAULT_WEIGHT
        
        if rate < self.TARGET_SUCCESS_WINDOW[0]:
            # 成功率太低 → 困难任务 → 需要更多采样
            # rate=0→weight=2.0, rate=0.3→weight=1.0
            ratio = rate / self.TARGET_SUCCESS_WINDOW[0]
            return max(self.MIN_WEIGHT, self.DEFAULT_WEIGHT * (2.0 - ratio))
        else:
            # 成功率太高 → 简单任务 → 减少采样
            # rate=0.7→weight=1.0, rate=1.0→weight=0.3
            ratio = (rate - self.TARGET_SUCCESS_WINDOW[1]) / (1.0 - self.TARGET_SUCCESS_WINDOW[1])
            return max(self.MIN_WEIGHT, self.DEFAULT_WEIGHT * (1.0 - ratio * 0.7))

    def should_sample(self, task_type: str) -> bool:
        """是否应该采样此类任务"""
        weight = self.get_weight(task_type)
        if weight >= 1.0:
            return True
        # 权重<1.0时概率采样
        import random
        return random.random() < weight

    def get_priority(self, task_type: str) -> float:
        """获取任务的采样优先级（越高越优先）"""
        weight = self.get_weight(task_type)
        sampled = self._stats[task_type]["sampled"]
        total = self._stats[task_type]["total"]
        
        if total == 0:
            return 0.5  # 无数据，中等优先级
        
        # 权重高 + 采样比例低 = 高优先级
        sampling_ratio = sampled / max(total, 1)
        under_sampled_penalty = max(0, 1.0 - sampling_ratio)
        
        return weight * (0.5 + 0.5 * under_sampled_penalty)

    # ── 队列管理 ──

    def enqueue(self, task_type: str, base_priority: float = 1.0):
        """将任务类型加入队列"""
        priority = base_priority * self.get_priority(task_type)
        self._task_queue.append((task_type, priority))
        # 按优先级排序
        self._task_queue.sort(key=lambda x: -x[1])

    def dequeue(self, n: int = 1) -> List[str]:
        """从队列中取出最高优先级的n个任务"""
        result = []
        for _ in range(min(n, len(self._task_queue))):
            result.append(self._task_queue.pop(0)[0])
        return result

    def queue_empty(self) -> bool:
        return len(self._task_queue) == 0

    # ── 状态持久化 ──

    def _load_state(self):
        """从文件加载状态"""
        path = Path(self._state_file)
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for task_type, stats in data.get("stats", {}).items():
                    self._stats[task_type] = stats
                logger.info(f"从 {self._state_file} 加载了 {len(data.get('stats', {}))} 个任务类型的统计")
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"加载状态文件失败: {e}")

    def save_state(self):
        """保存状态到文件"""
        path = Path(self._state_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "stats": dict(self._stats),
            "updated_at": datetime.now().isoformat(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"平衡采样器状态已保存到 {self._state_file}")

    # ── 报告 ──

    def report(self) -> str:
        """生成统计报告"""
        lines = [
            "═" * 50,
            "  izu 轨迹平衡采样报告",
            f"  生成时间: {datetime.now().isoformat()}",
            "═" * 50,
            "",
        ]

        if not self._stats:
            lines.append("无任务记录")
            return "\n".join(lines)

        # 任务分布
        total_all = sum(s["total"] for s in self._stats.values())
        lines.append(f"总任务数: {total_all}")
        lines.append(f"任务类型数: {len(self._stats)}")
        lines.append("")

        # 各任务类型详情
        lines.append(f"{'任务类型':<15} {'总量':>6} {'成功':>6} {'成功%':>8} {'权重':>6} {'采样':>6}")
        lines.append("-" * 55)
        
        sorted_types = sorted(
            self._stats.items(),
            key=lambda x: self.get_weight(x[0]),
            reverse=True,
        )
        for task_type, stats in sorted_types:
            rate = self.success_rate(task_type)
            weight = self.get_weight(task_type)
            lines.append(
                f"{task_type:<15} {stats['total']:>6} {stats['success']:>6} "
                f"{rate:>7.1%} {weight:>6.2f} {stats['sampled']:>6}"
            )

        lines.append("")
        lines.append("─── 欠采样任务（高优先级） ───")
        for task_type, stats in sorted_types:
            weight = self.get_weight(task_type)
            if weight > 1.5:
                rate = self.success_rate(task_type)
                lines.append(f"  🔴 {task_type}: success={rate:.0%} → weight={weight:.2f}（需要更多采样）")
        
        lines.append("")
        lines.append("─── 过采样任务（低优先级） ───")
        for task_type, stats in sorted_types:
            weight = self.get_weight(task_type)
            if weight < 0.6:
                rate = self.success_rate(task_type)
                lines.append(f"  🟢 {task_type}: success={rate:.0%} → weight={weight:.2f}（减少采样）")

        lines.append("")
        lines.append("═" * 50)
        return "\n".join(lines)


# ── 辅助：从历史轨迹重建统计 ──

def bootstrap_from_trajectories(
    trajectories: List,
    sampler: Optional[BalancedSampler] = None,
) -> BalancedSampler:
    """
    从历史轨迹重建平衡采样器的初始状态。
    
    用法：
      from izu.trajectory_credit import load_from_izu_sessions
      trajs = load_from_izu_sessions("/mnt/i/hermes/.hermes/sessions")
      sampler = bootstrap_from_trajectories(trajs)
    """
    if sampler is None:
        sampler = BalancedSampler()
    
    for traj in trajectories:
        # 提取步骤
        steps = getattr(traj, 'steps', [])
        completed = getattr(traj, 'completed', False)
        sampler.record_from_trajectory(steps, completed)
    
    sampler.save_state()
    logger.info(
        f"从 {len(trajectories)} 条轨迹重建统计: {len(sampler._stats)} 个任务类型"
    )
    return sampler


# ── CLI入口 ──

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="izu Trajectory Balance Sampler — 平衡轨迹采样"
    )
    parser.add_argument(
        "--bootstrap", "-b",
        action="store_true",
        help="从已有轨迹重建统计"
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="输出报告"
    )
    parser.add_argument(
        "--state-file",
        default="/mnt/i/hermes/data/sampler_state.json",
        help="状态文件路径"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    sampler = BalancedSampler(state_file=args.state_file)

    if args.bootstrap:
        from izu.trajectory_credit import load_from_izu_sessions
        trajs = load_from_izu_sessions()
        if trajs:
            sampler = bootstrap_from_trajectories(trajs, sampler)
            print(f"✅ 从 {len(trajs)} 条轨迹重建统计完成")
        else:
            print("⚠ 未找到轨迹数据")
    
    if args.report:
        print(sampler.report())


if __name__ == "__main__":
    main()
