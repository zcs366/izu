# TRT答案提取 · 6次迭代完整记录

**太阳神计划 · 2026-05-16**

## 迭代历程

| 版本 | 方法 | 干净率 | 核心问题 |
|------|------|--------|---------|
| v0.1 | 基础正则 `[答案: X]` | ~70% | 模型输出格式多变，简单正则覆盖不全 |
| v0.2 | 三层fallback（标注→等号→最后数字） | ~75% | LaTeX残渣(`\boxed{}`)未清理；1位数字误提 |
| v0.3 | 鲁班修复：LaTeX清理 + 次佳fallback | ~75% | 过滤太保守，部分正确答案被丢弃 |
| v0.4 | 军师修复：激进过滤 | 69% | 过度过滤→"提取失败"增多，**反向优化** |
| v0.5 | `FINAL_ANSWER:` 强制格式 | 0% | **致命陷阱**：一次调用3个rollout用"---"分隔，`FINAL_ANSWER`只在末尾而非每个rollout内 |
| v0.6 | 回退鲁班v0.3 + 关键修复 | **100%** | 去掉单数字过滤 + LaTeX清理 + 次佳fallback |

## 关键教训

### 教训1：FINAL_ANSWER 在TRT中完全失败

**不推荐在任何多rollout场景中使用 `FINAL_ANSWER:` 格式。**

原因：TRT的 `generate_rollouts()` 在一次API调用中生成3个候选解答，用"---"分隔。指令"必须在最后输出FINAL_ANSWER"可能只在整个响应的末尾生效一次，而非在每个rollout中分别生效。简单正则提取到的是整个响应的最后一行，而非各个rollout的答案。

### 教训2：过滤比宽松更危险

v0.4的谨慎过滤（跳过1位数字、跳过说明行）使干净率从75%降到69%。过度防御比适度宽松更糟。

### 教训3：次佳fallback是救命稻草

v0.6的核心改进：当最佳rollout提取失败时，依次尝试次佳、第三佳rollout。这使AIME题目的最终答案提取从"X"（失败）变为"157, 472"（成功）。

## 稳定方案（v0.6最终版）

```python
def extract_answer(text):
    # 1. 清理LaTeX残渣
    cleaned = re.sub(r'\\[a-z]+\{|\}|\\\\[a-z]*\{|\\\[|\\\]|\\,', '', text)
    
    # 2. 标注格式优先
    for pat in [r'\[答案:\s*(.+?)\]', r'最终答案[:：]\s*(.+?)', ...]:
        m = re.search(pat, cleaned)
        if m: return m.group(1).strip()
    
    # 3. 最后几行等号后数字（跳过说明行）
    for line in reversed(lines[-5:]):
        if any(w in line for w in ['好的','方案','候选','因此']): continue
        m = re.search(r'=\s*([\d,\s\.]+)', line)
        if m: return m.group(1).strip()
    
    # 4. 最后非说明行数字序列兜底
    for line in reversed(lines):
        if any(w in line for w in ['好的','方案','候选']): continue
        nums = re.findall(r'\d+(?:\.\d+)?', line)
        if nums and len(nums) <= 4: return ', '.join(nums)
    
    return "FAIL"
```

## 匠石原则验证

这6次迭代完美验证了匠石原则：**代码做框架，模型做语义。** 答案提取是确定性任务（正则匹配），不应该交给模型。将提取逻辑留在代码层是正确决策——6次迭代后稳定。
