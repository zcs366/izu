# LSE代码辅助进化 v1.0 · 实验记录

**太阳神计划 · 2026-05-16**

## 问题

LSE论文 (arXiv 2603.18620) 使用RL训练4B进化策略模型，实现"学会自我进化"。我们无法复现（无GPU集群+RL训练设施）。尝试让单模型分析自己的错误并改写prompt → **失败**。模型能解AIME题，但无法可靠回答"我的prompt哪里不好"——元认知瓶颈。

## 突破：代码做决策，模型做生成

将进化过程拆为两层（匠石原则）：

```
代码层：错误分类(FORMAT/COMPUTE/OTHER) → 模板匹配 → 选择进化方向
模型层：接收修复方向 + 当前Skill → 生成改进版Skill文本
```

代码决定"改什么"，模型负责"怎么改"。

## 实验结果

- 初始弱Skill："请解答数学题。用 [答案: X] 格式输出。"
- 基线：训练集50%，测试集0%
- 5轮进化后：训练集75%，测试集75% (+25pp)
- 关键：第4轮回退被代码层正确捕获——防止"进化致死"

## 错误分类器

```python
def classify_errors(results):
    stats = {"FORMAT": 0, "COMPUTE": 0, "OTHER": 0}
    for q, exp, raw, ext, ok in results:
        if ok: stats["correct"] += 1; continue
        exp_norm = exp.replace(",", "").replace(" ", "").lower()
        raw_norm = raw.replace(",", "").replace(" ", "").lower()
        if exp_norm in raw_norm and ext != exp:
            stats["FORMAT"] += 1  # 答案在raw里但格式不对
        elif any(c.isdigit() for c in ext) and ext != exp:
            stats["COMPUTE"] += 1  # 计算错误
        else:
            stats["OTHER"] += 1
    return stats
```

## 模板选择器

```python
FIX_TEMPLATES = {
    "FORMAT":  "强化格式：答案必须用逗号分隔多个值，数字不加文字",
    "COMPUTE": "强化验算：每一步计算后立刻验证结果",
    "OTHER":   "强化理解：先分析已知条件和求解目标",
}
# 选择逻辑：FORMAT占比>40%→选FORMAT, COMPUTE>30%→选COMPUTE, 否则OTHER
```

## 已知上限

当前仅3种错误类型+3个模板。上限约80-85%。超过后需增加模板分支或引入RL训练。
