"""
Agent关系拓扑 Python API v1.0
基于 agent-topology-schema-v1.json，提供 CRUD + 任务分配 + 进化数据接口
"""
import json, os, time
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict

SCHEMA_PATH = "/mnt/i/hermes/data/izu-agent-topology-schema-v1.json"
DATA_PATH = "/mnt/i/hermes/data/izu-agent-topology-data.json"

class AgentTopology:
    """Agent关系拓扑的读写接口"""
    
    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
        self.data = self._load()
    
    def _load(self) -> dict:
        if os.path.exists(self.data_path):
            with open(self.data_path) as f:
                return json.load(f)
        return {
            "topology_version": "1.0.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "agents": {},
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {
                "default_max_agents": 7,
                "exploration_rate": 0.15,
                "performance_decay_factor": 0.95,
                "min_interactions_for_trust": 5
            },
            "emergent_metrics": {
                "agent_load_distribution": {},
                "bottleneck_agents": [],
                "underutilized_agents": []
            }
        }
    
    def save(self):
        self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    # ── Agent CRUD ──
    def register_agent(self, agent_id: str, name: str, role: str, 
                       expertise_tags: list, capability_vector: dict = None):
        self.data["agents"][agent_id] = {
            "name": name,
            "role": role,
            "expertise_tags": expertise_tags,
            "capability_vector": capability_vector or {},
            "preferred_collaborators": [],
            "avoid_collaborators": [],
            "performance_history": {
                "avg_quality_score": 0.5,
                "avg_latency_seconds": 0,
                "avg_token_cost": 0,
                "success_rate": 1.0,
                "total_tasks_completed": 0
            },
            "evolution_state": {
                "current_generation": 0,
                "last_verified_at": None,
                "identified_weaknesses": [],
                "prompt_adjustments_applied": []
            }
        }
        self.save()
    
    def get_agent(self, agent_id: str) -> dict:
        return self.data["agents"].get(agent_id)
    
    def list_agents(self) -> list:
        return list(self.data["agents"].keys())
    
    # ── 关系管理 ──
    def add_relationship(self, source: str, target: str, rel_type: str,
                        weight: float = 0.5):
        # 避免重复
        for r in self.data["relationships"]:
            if r["source"] == source and r["target"] == target and r["type"] == rel_type:
                r["weight"] = weight
                r["interaction_count"] += 1
                r["last_interaction"] = datetime.now(timezone.utc).isoformat()
                self.save()
                return
        
        now = datetime.now(timezone.utc).isoformat()
        self.data["relationships"].append({
            "source": source, "target": target, "type": rel_type,
            "weight": weight, "interaction_count": 1,
            "avg_quality_delta": 0,
            "last_interaction": now, "established_at": now
        })
        self.save()
    
    def get_collaborators(self, agent_id: str, min_weight: float = 0.3) -> list:
        """获取某Agent的所有协作者"""
        result = []
        for r in self.data["relationships"]:
            if r["source"] == agent_id and r["weight"] >= min_weight:
                result.append(r)
            elif r["target"] == agent_id and r["weight"] >= min_weight:
                result.append(r)
        return sorted(result, key=lambda x: x["weight"], reverse=True)
    
    # ── 交互记录 ──
    def log_interaction(self, task_id: str, task_type: str,
                       agents_involved: list, allocation_strategy: str,
                       outcome: dict, evolution_triggered: bool = False):
        import uuid
        record = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": task_id, "task_type": task_type,
            "agents_involved": agents_involved,
            "allocation_strategy": allocation_strategy,
            "outcome": outcome,
            "evolution_triggered": evolution_triggered
        }
        self.data["interaction_log"].append(record)
        
        # 更新Agent表现
        for aid in agents_involved:
            agent = self.data["agents"].get(aid)
            if agent:
                ph = agent["performance_history"]
                n = ph["total_tasks_completed"]
                ph["avg_quality_score"] = (ph["avg_quality_score"] * n + outcome.get("quality_score", 0.5)) / (n + 1)
                ph["total_tasks_completed"] = n + 1
                ph["success_rate"] = (ph["success_rate"] * n + (0 if outcome.get("had_retry") else 1)) / (n + 1)
        
        # 更新关系权重
        for i, a1 in enumerate(agents_involved):
            for a2 in agents_involved[i+1:]:
                quality_delta = outcome.get("quality_score", 0.5) - 0.5
                self.add_relationship(a1, a2, "collaborates_with",
                    weight=0.5 + quality_delta * 0.5)
        
        self._update_emergent_metrics()
        self.save()
        return record["id"]
    
    # ── 任务分配 ──
    def allocate_agents(self, task_type: str, task_tags: list,
                       max_agents: int = None) -> list:
        """根据任务类型和标签，推荐最优Agent组合"""
        policy = self.data["task_allocation_policy"]
        max_a = max_agents or policy["default_max_agents"]
        
        import random
        # 探索：随机选
        if random.random() < policy["exploration_rate"]:
            candidates = list(self.data["agents"].keys())
            random.shuffle(candidates)
            return candidates[:max_a]
        
        # 利用：按匹配度排序
        scores = {}
        for aid, agent in self.data["agents"].items():
            tag_match = len(set(agent.get("expertise_tags", [])) & set(task_tags))
            perf = agent["performance_history"]["avg_quality_score"]
            scores[aid] = tag_match * 0.6 + perf * 0.4
        
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [aid for aid, _ in ranked[:max_a]]
    
    # ── 进化数据接口 ──
    def get_recent_scores(self, agent_id: str, n: int = 3) -> list:
        """获取Agent最近N次任务的质量评分"""
        scores = []
        for record in reversed(self.data["interaction_log"]):
            if agent_id in record["agents_involved"]:
                scores.append(record["outcome"].get("quality_score", 0.5))
                if len(scores) >= n:
                    break
        return list(reversed(scores))
    
    def update_weakness(self, agent_id: str, weakness: str):
        agent = self.data["agents"].get(agent_id)
        if agent:
            agent["evolution_state"]["identified_weaknesses"].append(weakness)
            agent["evolution_state"]["last_verified_at"] = datetime.now(timezone.utc).isoformat()
            self.save()
    
    def add_prompt_adjustment(self, agent_id: str, adjustment: str):
        agent = self.data["agents"].get(agent_id)
        if agent:
            agent["evolution_state"]["prompt_adjustments_applied"].append(adjustment)
            agent["evolution_state"]["current_generation"] += 1
            self.save()
    
    # ── 涌现指标 ──
    def _update_emergent_metrics(self):
        loads = defaultdict(int)
        for record in self.data["interaction_log"][-50:]:  # 最近50次
            for aid in record["agents_involved"]:
                loads[aid] += 1
        
        self.data["emergent_metrics"]["agent_load_distribution"] = dict(loads)
        
        if loads:
            avg_load = sum(loads.values()) / len(loads) if loads else 1
            self.data["emergent_metrics"]["bottleneck_agents"] = [
                aid for aid, count in loads.items() if count > avg_load * 1.5
            ]
            self.data["emergent_metrics"]["underutilized_agents"] = [
                aid for aid in self.data["agents"] if loads.get(aid, 0) < avg_load * 0.3
            ]
    
    # ── 统计 ──
    def stats(self) -> dict:
        return {
            "agent_count": len(self.data["agents"]),
            "relationship_count": len(self.data["relationships"]),
            "total_interactions": len(self.data["interaction_log"]),
            "bottlenecks": self.data["emergent_metrics"]["bottleneck_agents"],
            "underutilized": self.data["emergent_metrics"]["underutilized_agents"]
        }


# ── 自检 ──
if __name__ == "__main__":
    topo = AgentTopology()
    
    # 注册izu七个Agent
    agents = [
        ("tan", "探1", "聚合搜索", ["search", "aggregation", "web"]),
        ("tan2", "探2", "聚合搜索", ["search", "aggregation", "academic"]),
        ("sou", "搜1", "深度检索", ["deep_search", "extraction", "web"]),
        ("sou2", "搜2", "深度检索", ["deep_search", "extraction", "academic"]),
        ("zhi", "织", "编织合并", ["synthesis", "merge", "semantic"]),
        ("duiqi", "对齐", "对齐", ["alignment", "comparison"]),
        ("xie", "写", "终稿撰写", ["writing", "composition", "polish"]),
        ("pi", "劈", "分发", ["distribution", "formatting"]),
        ("he", "核验证", "质量核验", ["verification", "fact_check", "validation"]),
    ]
    
    for aid, name, role, tags in agents:
        if aid not in topo.data["agents"]:
            topo.register_agent(aid, name, role, tags)
    
    # 模拟一次交互
    rec_id = topo.log_interaction(
        task_id="test-001",
        task_type="research",
        agents_involved=["tan", "tan2", "sou", "zhi", "xie"],
        allocation_strategy="optimal",
        outcome={"quality_score": 0.82, "total_tokens": 45000,
                "duration_seconds": 120.5, "had_retry": False,
                "user_feedback": "positive"}
    )
    
    print(f"Agent数: {topo.stats()['agent_count']}")
    print(f"关系数: {topo.stats()['relationship_count']}")
    print(f"交互记录: {topo.stats()['total_interactions']}")
    
    # 测试任务分配
    alloc = topo.allocate_agents("research", ["search", "writing"], max_agents=4)
    print(f"推荐Agent: {alloc}")
    
    topo.save()
    print(f"✅ 数据写入 {DATA_PATH}")
