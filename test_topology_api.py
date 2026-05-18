"""Tests for topology_api.py — AgentTopology CRUD, relationships, allocation, evolution"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timezone

from topology_api import AgentTopology


# ═══════════════════════════════════════════
# AgentTopology CRUD 测试
# ═══════════════════════════════════════════

class TestAgentCRUD:
    """Agent 注册/查询/列表 测试"""

    @patch("topology_api.os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_register_agent_initializes_defaults(self, mock_dump, mock_open_file, mock_exists):
        """注册Agent后应包含完整的默认字段"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.register_agent("ag1", "Agent-A", "worker", ["code", "debug"])

        agent = topo.data["agents"]["ag1"]
        assert agent["name"] == "Agent-A"
        assert agent["role"] == "worker"
        assert agent["expertise_tags"] == ["code", "debug"]
        assert agent["capability_vector"] == {}
        assert agent["preferred_collaborators"] == []
        assert agent["avoid_collaborators"] == []
        assert agent["performance_history"]["avg_quality_score"] == 0.5
        assert agent["performance_history"]["success_rate"] == 1.0
        assert agent["performance_history"]["total_tasks_completed"] == 0
        assert agent["evolution_state"]["current_generation"] == 0
        assert agent["evolution_state"]["last_verified_at"] is None
        assert agent["evolution_state"]["identified_weaknesses"] == []
        assert agent["evolution_state"]["prompt_adjustments_applied"] == []

    @patch("topology_api.os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_register_agent_with_capability_vector(self, mock_dump, mock_open_file, mock_exists):
        """可以传入自定义 capability_vector"""
        topo = AgentTopology(data_path="/fake/path.json")
        cap = {"coding": 0.9, "reasoning": 0.8}
        topo.register_agent("ag2", "Agent-B", "coder", ["code"], capability_vector=cap)
        assert topo.data["agents"]["ag2"]["capability_vector"] == cap

    @patch("topology_api.os.path.exists", return_value=False)
    @patch("topology_api.json.dump")
    def test_get_agent_returns_none_for_missing(self, mock_dump, mock_exists):
        """不存在的Agent应返回 None"""
        topo = AgentTopology(data_path="/fake/path.json")
        assert topo.get_agent("nonexistent") is None

    @patch("topology_api.os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_list_agents_returns_registered_ids(self, mock_dump, mock_open_file, mock_exists):
        """list_agents 应返回所有注册的Agent ID"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.register_agent("a1", "A1", "dev", ["py"])
        topo.register_agent("a2", "A2", "ops", ["sh"])
        ids = topo.list_agents()
        assert "a1" in ids
        assert "a2" in ids
        assert len(ids) == 2


# ═══════════════════════════════════════════
# 关系管理 测试
# ═══════════════════════════════════════════

class TestRelationshipManagement:
    """add_relationship / get_collaborators 测试"""

    def setup_method(self):
        self.mock_data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {
                "alice": {
                    "name": "Alice", "role": "dev",
                    "expertise_tags": ["py"],
                    "capability_vector": {},
                    "preferred_collaborators": [],
                    "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                },
                "bob": {
                    "name": "Bob", "role": "ops",
                    "expertise_tags": ["sh"],
                    "capability_vector": {},
                    "preferred_collaborators": [],
                    "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                },
                "charlie": {
                    "name": "Charlie", "role": "qa",
                    "expertise_tags": ["test"],
                    "capability_vector": {},
                    "preferred_collaborators": [],
                    "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                }
            },
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_add_relationship_creates_new(self, mock_dump, mock_open_file):
        """新增关系应正确设置字段"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.add_relationship("alice", "bob", "collaborates_with", weight=0.8)
        assert len(topo.data["relationships"]) == 1
        rel = topo.data["relationships"][0]
        assert rel["source"] == "alice"
        assert rel["target"] == "bob"
        assert rel["type"] == "collaborates_with"
        assert rel["weight"] == 0.8
        assert rel["interaction_count"] == 1

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_add_relationship_updates_existing(self, mock_dump, mock_open_file):
        """已存在的关系应更新 weight 和 interaction_count"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.add_relationship("alice", "bob", "collaborates_with", weight=0.5)
        topo.add_relationship("alice", "bob", "collaborates_with", weight=0.9)
        assert len(topo.data["relationships"]) == 1
        rel = topo.data["relationships"][0]
        assert rel["weight"] == 0.9
        assert rel["interaction_count"] == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_get_collaborators_filters_by_weight(self, mock_dump, mock_open_file):
        """get_collaborators 应按 min_weight 过滤"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.add_relationship("alice", "bob", "collaborates_with", weight=0.9)
        topo.add_relationship("alice", "charlie", "collaborates_with", weight=0.2)

        high = topo.get_collaborators("alice", min_weight=0.5)
        assert len(high) == 1
        assert high[0]["target"] == "bob"

        all_rels = topo.get_collaborators("alice", min_weight=0.0)
        assert len(all_rels) == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_get_collaborators_finds_both_directions(self, mock_dump, mock_open_file):
        """作为 source 或 target 的关系都应被找到"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.add_relationship("alice", "bob", "collaborates_with", weight=0.7)
        topo.add_relationship("charlie", "alice", "collaborates_with", weight=0.6)
        cols = topo.get_collaborators("alice", min_weight=0.5)
        assert len(cols) == 2
        targets = {r["source"] + "->" + r["target"] for r in cols}
        assert "alice->bob" in targets
        assert "charlie->alice" in targets


# ═══════════════════════════════════════════
# 交互记录 & 表现更新 测试
# ═══════════════════════════════════════════

class TestInteractionLog:
    """log_interaction 及表现更新测试"""

    def setup_method(self):
        self.mock_data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {
                "alice": {
                    "name": "Alice", "role": "dev",
                    "expertise_tags": ["py"],
                    "capability_vector": {},
                    "preferred_collaborators": [],
                    "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                },
                "bob": {
                    "name": "Bob", "role": "ops",
                    "expertise_tags": ["sh"],
                    "capability_vector": {},
                    "preferred_collaborators": [],
                    "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                }
            },
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_log_interaction_updates_performance(self, mock_dump, mock_open_file):
        """log_interaction 应更新Agent的平均质量分和成功次数"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.log_interaction(
            task_id="t1", task_type="coding",
            agents_involved=["alice"],
            allocation_strategy="manual",
            outcome={"quality_score": 0.9, "had_retry": False}
        )
        alice = topo.data["agents"]["alice"]
        assert alice["performance_history"]["total_tasks_completed"] == 1
        assert alice["performance_history"]["avg_quality_score"] == pytest.approx(0.9)
        assert alice["performance_history"]["success_rate"] == 1.0

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_log_interaction_creates_relationships(self, mock_dump, mock_open_file):
        """log_interaction 应在涉及的Agent间自动创建关系"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        topo.log_interaction(
            task_id="t2", task_type="review",
            agents_involved=["alice", "bob"],
            allocation_strategy="auto",
            outcome={"quality_score": 0.8, "had_retry": False}
        )
        assert len(topo.data["relationships"]) == 1
        rel = topo.data["relationships"][0]
        assert rel["source"] == "alice"
        assert rel["target"] == "bob"
        assert rel["weight"] == pytest.approx(0.65)

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_log_interaction_returns_record_id(self, mock_dump, mock_open_file):
        """log_interaction 应返回记录ID"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data
        rid = topo.log_interaction(
            task_id="t3", task_type="test",
            agents_involved=["alice"],
            allocation_strategy="auto",
            outcome={"quality_score": 0.7}
        )
        assert isinstance(rid, str)
        assert len(rid) == 8


# ═══════════════════════════════════════════
# 任务分配 测试
# ═══════════════════════════════════════════

class TestTaskAllocation:
    """allocate_agents 测试"""

    def setup_method(self):
        self.agents = {
            "dev_a": {
                "name": "DevA", "role": "dev",
                "expertise_tags": ["py", "web"],
                "capability_vector": {},
                "preferred_collaborators": [], "avoid_collaborators": [],
                "performance_history": {"avg_quality_score": 0.9, "avg_latency_seconds": 0,
                                        "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 10},
                "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                    "identified_weaknesses": [], "prompt_adjustments_applied": []}
            },
            "dev_b": {
                "name": "DevB", "role": "dev",
                "expertise_tags": ["java", "db"],
                "capability_vector": {},
                "preferred_collaborators": [], "avoid_collaborators": [],
                "performance_history": {"avg_quality_score": 0.6, "avg_latency_seconds": 0,
                                        "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 5},
                "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                    "identified_weaknesses": [], "prompt_adjustments_applied": []}
            },
            "ops_c": {
                "name": "OpsC", "role": "ops",
                "expertise_tags": ["sh", "web"],
                "capability_vector": {},
                "preferred_collaborators": [], "avoid_collaborators": [],
                "performance_history": {"avg_quality_score": 0.7, "avg_latency_seconds": 0,
                                        "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 3},
                "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                    "identified_weaknesses": [], "prompt_adjustments_applied": []}
            }
        }
        self.mock_data_util = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": self.agents,
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.0,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }

    @patch("random.random", return_value=0.5)
    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_allocate_exploit_ranks_by_tag_and_perf(self, mock_dump, mock_open_file, mock_random):
        """利用模式下应按标签匹配度和表现排序"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data_util
        result = topo.allocate_agents("dev", ["py", "web"], max_agents=2)
        assert result == ["dev_a", "ops_c"]

    @patch("random.random", return_value=0.1)
    @patch("random.shuffle", side_effect=lambda x: x.reverse() or x)
    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_allocate_explore_random_selection(self, mock_dump, mock_open_file, mock_shuffle, mock_random):
        """探索模式下应随机选择Agent"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = self.mock_data_util
        topo.data["task_allocation_policy"]["exploration_rate"] = 0.15
        result = topo.allocate_agents("dev", ["py"], max_agents=2)
        assert len(result) <= 2


# ═══════════════════════════════════════════
# 进化数据接口 测试
# ═══════════════════════════════════════════

class TestEvolutionInterface:
    """get_recent_scores / update_weakness / add_prompt_adjustment 测试"""

    @patch("topology_api.json.dump")
    def test_get_recent_scores_returns_recent_n(self, mock_dump):
        """get_recent_scores 应返回最近的N个评分"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {
                "alice": {
                    "name": "Alice", "role": "dev",
                    "expertise_tags": ["py"],
                    "capability_vector": {},
                    "preferred_collaborators": [], "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                }
            },
            "relationships": [],
            "interaction_log": [
                {"agents_involved": ["alice"], "outcome": {"quality_score": 0.3}},
                {"agents_involved": ["alice"], "outcome": {"quality_score": 0.6}},
                {"agents_involved": ["alice"], "outcome": {"quality_score": 0.9}},
                {"agents_involved": ["bob"], "outcome": {"quality_score": 1.0}},
            ],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }
        scores = topo.get_recent_scores("alice", n=2)
        assert scores == [0.6, 0.9]

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_update_weakness_appends_and_saves(self, mock_dump, mock_open_file):
        """update_weakness 应追加弱点并更新时间戳"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {
                "alice": {
                    "name": "Alice", "role": "dev",
                    "expertise_tags": ["py"],
                    "capability_vector": {},
                    "preferred_collaborators": [], "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                }
            },
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }
        topo.update_weakness("alice", "缺乏单元测试能力")
        es = topo.data["agents"]["alice"]["evolution_state"]
        assert es["identified_weaknesses"] == ["缺乏单元测试能力"]
        assert es["last_verified_at"] is not None

    @patch("builtins.open", new_callable=mock_open)
    @patch("topology_api.json.dump")
    def test_add_prompt_adjustment_increments_generation(self, mock_dump, mock_open_file):
        """add_prompt_adjustment 应追加调整并增加代际"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {
                "alice": {
                    "name": "Alice", "role": "dev",
                    "expertise_tags": ["py"],
                    "capability_vector": {},
                    "preferred_collaborators": [], "avoid_collaborators": [],
                    "performance_history": {"avg_quality_score": 0.5, "avg_latency_seconds": 0,
                                            "avg_token_cost": 0, "success_rate": 1.0, "total_tasks_completed": 0},
                    "evolution_state": {"current_generation": 0, "last_verified_at": None,
                                        "identified_weaknesses": [], "prompt_adjustments_applied": []}
                }
            },
            "relationships": [],
            "interaction_log": [],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }
        topo.add_prompt_adjustment("alice", "增加 reasoning 步骤")
        es = topo.data["agents"]["alice"]["evolution_state"]
        assert es["prompt_adjustments_applied"] == ["增加 reasoning 步骤"]
        assert es["current_generation"] == 1


# ═══════════════════════════════════════════
# 涌现指标 & 统计 测试
# ═══════════════════════════════════════════

class TestEmergentMetrics:
    """_update_emergent_metrics / stats 测试"""

    @patch("topology_api.json.dump")
    def test_stats_returns_correct_counts(self, mock_dump):
        """stats() 应返回正确的计数和瓶颈信息"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {"a": {}, "b": {}},
            "relationships": [{"source": "a", "target": "b"}],
            "interaction_log": [{"id": "1"}, {"id": "2"}],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {"a": 10},
                                 "bottleneck_agents": ["a"],
                                 "underutilized_agents": ["b"]}
        }
        s = topo.stats()
        assert s["agent_count"] == 2
        assert s["relationship_count"] == 1
        assert s["total_interactions"] == 2
        assert s["bottlenecks"] == ["a"]
        assert s["underutilized"] == ["b"]

    @patch("topology_api.json.dump")
    def test_update_metrics_identifies_bottlenecks(self, mock_dump):
        """_update_emergent_metrics 应正确识别瓶颈和未充分利用Agent"""
        topo = AgentTopology(data_path="/fake/path.json")
        topo.data = {
            "topology_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00+00:00",
            "agents": {"a": {}, "b": {}, "c": {}},
            "relationships": [],
            "interaction_log": [
                {"agents_involved": ["a", "b"]},
                {"agents_involved": ["a"]},
                {"agents_involved": ["a"]},
                {"agents_involved": ["a"]},
            ],
            "task_allocation_policy": {"default_max_agents": 7, "exploration_rate": 0.15,
                                       "performance_decay_factor": 0.95, "min_interactions_for_trust": 5},
            "emergent_metrics": {"agent_load_distribution": {}, "bottleneck_agents": [], "underutilized_agents": []}
        }
        topo._update_emergent_metrics()
        em = topo.data["emergent_metrics"]
        assert "a" in em["bottleneck_agents"]
        assert "c" in em["underutilized_agents"]
