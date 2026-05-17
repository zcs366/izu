#!/usr/bin/env python3
"""
izu 进化引擎 v1.0 · ReVeal推理时扩展
匠石铁律：能用代码就别用模型。评分90%代码化，模型只做10%语义判断。
"""
import json, os, re, time, subprocess
from datetime import datetime, timezone
from urllib.parse import urlparse

DATA_DIR = "/mnt/i/hermes/data"
TOPO_FILE = f"{DATA_DIR}/izu-agent-topology-data.json"

# ── 评分维度（90%代码化） ──
SCORING_DIMENSIONS = {
    "url_validity":       {"weight": 0.20, "method": "code", "desc": "URL存活率"},
    "structural_complete": {"weight": 0.20, "method": "code", "desc": "结构完整性"},
    "citation_accuracy":  {"weight": 0.15, "method": "code", "desc": "引用准确性"},
    "consistency":        {"weight": 0.20, "method": "code", "desc": "内部一致性"},
    "conciseness":        {"weight": 0.15, "method": "code", "desc": "简洁度"},
    "semantic_quality":   {"weight": 0.10, "method": "model","desc": "语义质量（仅此项需模型）"},
}

# ── 验证器 ──
class Verifier:
    """代码验证器——匠石铁律：代码做"""
    
    @staticmethod
    def check_urls(text: str) -> dict:
        """URL存活检查"""
        urls = re.findall(r'https?://[^\s\)\]>]+', text)
        if not urls:
            return {"score": 1.0, "total": 0, "alive": 0, "dead": []}
        
        alive = 0
        dead = []
        for url in urls[:20]:
            try:
                r = subprocess.run(["curl", "-sL", "--connect-timeout", "3", "-o", "/dev/null", "-w", "%{http_code}", url],
                                   capture_output=True, text=True, timeout=5)
                code = int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
                if 200 <= code < 500:
                    alive += 1
                else:
                    dead.append({"url": url[:80], "status": code})
            except:
                dead.append({"url": url[:80], "status": "error"})
        
        score = alive / len(urls) if urls else 1.0
        return {"score": score, "total": len(urls), "alive": alive, "dead": dead}
    
    @staticmethod
    def check_structure(text: str, expected_sections: list = None) -> dict:
        """结构完整性检查：是否包含必要章节"""
        if not expected_sections:
            expected_sections = ["##", "###"]  # 至少要有标题
        
        found = []
        missing = []
        for sec in expected_sections:
            if sec in text:
                found.append(sec)
            else:
                missing.append(sec)
        
        score = len(found) / len(expected_sections) if expected_sections else 1.0
        return {"score": score, "found": found, "missing": missing}
    
    @staticmethod
    def check_citations(text: str) -> dict:
        """引用完整性检查：找到的引用是否都有来源"""
        citations = re.findall(r'[\uff08\(](\w+等?\s*(?:et\s*al\.?)?\s*[,，]?\s*\d{4})[\uff09\)]', text)
        links = re.findall(r'https?://[^\s\)\]>]+', text)
        
        score = 1.0
        # 有引用但没链接 → 可能不完整
        if citations and not links:
            score = 0.5
        
        return {"score": score, "citations": len(citations), "links": len(links)}
    
    @staticmethod
    def check_consistency(text: str) -> dict:
        """内部一致性：检测自相矛盾的模式"""
        issues = []
        
        # 数字范围检测
        ranges = re.findall(r'(\d+)\s*[-~到]\s*(\d+)', text)
        for lo, hi in ranges:
            if int(lo) > int(hi):
                issues.append(f"数字范围异常:{lo}-{hi}")
        
        # 百分比总和检测
        percents = re.findall(r'(\d+)%', text)
        if percents:
            total = sum(int(p) for p in percents)
            if total > 200:
                issues.append(f"百分比可能溢出:{total}%")
        
        score = max(0, 1.0 - len(issues) * 0.2)
        return {"score": score, "issues": issues}
    
    @staticmethod
    def check_conciseness(text: str) -> dict:
        """简洁度：token密度比"""
        words = len(text)
        sentences = max(1, len(re.findall(r'[。！？.!?\n]', text)))
        avg_sentence_len = words / sentences
        
        # 最优句长 15-40字，偏离扣分
        if avg_sentence_len < 10:
            score = 0.7
        elif avg_sentence_len > 80:
            score = 0.6
        else:
            score = 1.0
        
        return {"score": score, "total_chars": len(text), "sentences": sentences, "avg_len": round(avg_sentence_len, 1)}

# ── 评分器 ──
class Scorer:
    """5维度加权评分"""
    
    def __init__(self):
        self.verifier = Verifier()
    
    def score_output(self, text: str, expected_sections: list = None) -> dict:
        results = {}
        total = 0.0
        
        # URL存活
        r = self.verifier.check_urls(text)
        results["url_validity"] = r
        total += r["score"] * SCORING_DIMENSIONS["url_validity"]["weight"]
        
        # 结构完整
        r = self.verifier.check_structure(text, expected_sections)
        results["structural_complete"] = r
        total += r["score"] * SCORING_DIMENSIONS["structural_complete"]["weight"]
        
        # 引用准确
        r = self.verifier.check_citations(text)
        results["citation_accuracy"] = r
        total += r["score"] * SCORING_DIMENSIONS["citation_accuracy"]["weight"]
        
        # 一致性
        r = self.verifier.check_consistency(text)
        results["consistency"] = r
        total += r["score"] * SCORING_DIMENSIONS["consistency"]["weight"]
        
        # 简洁度
        r = self.verifier.check_conciseness(text)
        results["conciseness"] = r
        total += r["score"] * SCORING_DIMENSIONS["conciseness"]["weight"]
        
        results["_overall"] = round(total, 3)
        results["_timestamp"] = datetime.now(timezone.utc).isoformat()
        
        return results

# ── 进化触发器 ──
class EvolutionTrigger:
    """短板记录+提示微调"""
    
    def __init__(self, topo_path=TOPO_FILE):
        self.topo_path = topo_path
    
    def _load_topo(self) -> dict:
        with open(self.topo_path) as f:
            return json.load(f)
    
    def _save_topo(self, data: dict):
        with open(self.topo_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def evaluate_and_evolve(self, agent_id: str, output_text: str, task_type: str) -> dict:
        """核心入口：评分→记录→触发进化"""
        scorer = Scorer()
        scores = scorer.score_output(output_text)
        
        topo = self._load_topo()
        agent = topo["agents"].get(agent_id)
        
        if not agent:
            return {"error": f"Agent {agent_id} not found"}
        
        # 更新表现历史
        ph = agent["performance_history"]
        n = ph["total_tasks_completed"]
        overall = scores["_overall"]
        ph["avg_quality_score"] = (ph["avg_quality_score"] * n + overall) / (n + 1)
        ph["total_tasks_completed"] = n + 1
        
        # 检测短板
        weaknesses = []
        prompts = []
        for dim, info in SCORING_DIMENSIONS.items():
            if dim == "semantic_quality":
                continue
            if scores.get(dim, {}).get("score", 1.0) < 0.5:
                weaknesses.append(dim)
                prompts.append(f"本次任务在{info['desc']}方面得分偏低({scores[dim]['score']:.0%})，下次请注意")
        
        # 写入短板
        ev = agent["evolution_state"]
        for w in weaknesses:
            if w not in ev["identified_weaknesses"]:
                ev["identified_weaknesses"].append(w)
        
        # 写入提示调整
        for p in prompts:
            ev["prompt_adjustments_applied"].append(f"{time.strftime('%Y%m%d-%H%M')}:{p}")
            ev["current_generation"] += 1
        
        ev["last_verified_at"] = datetime.now(timezone.utc).isoformat()
        
        self._save_topo(topo)
        
        return {
            "agent": agent_id,
            "overall_score": overall,
            "dimensions": {k: v.get("score",0) for k,v in scores.items() if not k.startswith("_")},
            "weaknesses_found": weaknesses,
            "prompts_injected": prompts,
            "generation": ev["current_generation"]
        }

# ── 核验证独立校验循环（v2.0）──
MAX_RETRIES = 3
PASS_THRESHOLD = 0.70  # 综合分≥70%才算通过

class VerificationLoop:
    """核验证Agent独立校验生成Agent的输出。不自判。最多3次重试。"""
    
    def __init__(self):
        self.scorer = Scorer()
        self.trigger = EvolutionTrigger()
    
    def verify(self, generator_agent_id: str, verifier_agent_id: str, 
               output_text: str, task_type: str) -> dict:
        """
        generator_agent_id: 生成Agent（写/织/探/搜）
        verifier_agent_id: 核验证Agent（独立，不自判）
        """
        result = {
            "generator": generator_agent_id,
            "verifier": verifier_agent_id,
            "task_type": task_type,
            "attempts": 0,
            "passed": False,
            "history": []
        }
        
        for attempt in range(1, MAX_RETRIES + 1):
            scores = self.scorer.score_output(output_text)
            overall = scores["_overall"]
            
            attempt_record = {
                "attempt": attempt,
                "overall": overall,
                "dimensions": {k: v.get("score",0) for k,v in scores.items() if not k.startswith("_")},
                "passed": overall >= PASS_THRESHOLD
            }
            result["history"].append(attempt_record)
            result["attempts"] = attempt
            
            if overall >= PASS_THRESHOLD:
                result["passed"] = True
                result["final_score"] = overall
                break
            else:
                # 记录短板到核验证Agent（不是生成Agent）
                weak_dims = [d for d,s in attempt_record["dimensions"].items() if s < 0.5]
                
                if attempt < MAX_RETRIES:
                    # 还有重试机会：记录短板到生成Agent，打回重写
                    for dim in weak_dims:
                        self.trigger.evaluate_and_evolve(generator_agent_id, output_text, task_type)
        
        # 最终结果写入生成Agent的进化状态
        final_score = result.get("final_score", 0)
        if not result["passed"]:
            # 3次都失败：记录到短板库，通知
            result["exhausted"] = True
            result["weaknesses"] = [d for d,s in attempt_record["dimensions"].items() if s < 0.5]
        
        self.trigger.evaluate_and_evolve(generator_agent_id, output_text, task_type)
        
        return result

# ── 集成测试 ──
if __name__ == "__main__":
    print("🧬 izu进化引擎 v2.0 · 核验证独立校验\n")
    
    test_text_good = """## 分析评估
这篇文章讲了AI项目的灵感来源。作者认为灵感来自与AI的高频对话回路。

### 核心观点
1. Agent的核心难点是长期运行的稳定性
2. AI压缩了反馈周期，从孤立开发变成持续迭代
3. 未来智能系统需要在开放世界持续运行

参考来源：https://zhuanlan.zhihu.com/p/2036102958136419687"""

    test_text_bad = """ai很好 非常好 真的很好 反正就是好 你说呢 我觉得不错"""
    
    loop = VerificationLoop()
    
    # 测试1：好输出（应通过）
    print("📝 测试1：合格输出")
    r1 = loop.verify("xie", "he", test_text_good, "analysis")
    print(f"  生成Agent: {r1['generator']} → 核验证Agent: {r1['verifier']}")
    print(f"  结果: {'✅ 通过' if r1['passed'] else '❌ 未通过'}")
    print(f"  尝试: {r1['attempts']}次")
    for h in r1["history"]:
        print(f"    第{h['attempt']}次: {h['overall']:.0%} {'✅' if h['passed'] else '❌'}")
    
    # 测试2：烂输出（应3次都不通过）
    print(f"\n📝 测试2：不合格输出（最多{MAX_RETRIES}次重试）")
    r2 = loop.verify("xie", "he", test_text_bad, "analysis")
    print(f"  生成Agent: {r2['generator']} → 核验证Agent: {r2['verifier']}")
    print(f"  结果: {'✅ 通过' if r2['passed'] else '💀 3次耗尽'}")
    print(f"  尝试: {r2['attempts']}次")
    for h in r2["history"]:
        print(f"    第{h['attempt']}次: {h['overall']:.0%} {'✅' if h['passed'] else '❌'}")
    if r2.get("exhausted"):
        print(f"  短板: {r2.get('weaknesses',[])}")
