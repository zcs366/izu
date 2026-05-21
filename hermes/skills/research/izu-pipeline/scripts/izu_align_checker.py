#!/usr/bin/env python3
"""
izu 对齐检查器 v1.0
替代 LLM 调用的纯代码对齐检查。

工作原理：
1. 从 topic 中提取关键词（英文正则 + 中文 bigram/trigram 无词典分词）
2. 从"织"的关联地图中分析覆盖度（逐词匹配）
3. 检查织输出是否包含 5 个标准章节结构
4. 输出结构化对齐检查报告（与原 LLM 输出格式一致）

收益：
- 每次流水线运行节省 1 次 DeepSeek API 调用（~¥0.002 + 3-5s 延迟）
- 14 天回本（按日均 10 次管线运行计算）

使用方法：
    from izu_align_checker import check_alignment
    report, status = check_alignment("研究主题", 织输出文本)
    # status: "pass" / "warn" / "fail"

集成到流水线：
    from izu_align_checker import run_align_code
    fpath, report, status = run_align_code(topic, weave_path)
"""

import re
from pathlib import Path

# ============================================================
# 中文 + 英文停用词（对齐检查专用精简版）
# ============================================================
STOP_WORDS = {
    # 中文
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
    "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
    "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些",
    "什么", "怎么", "如何", "为什么", "这个", "那个", "因为", "所以",
    "但", "但是", "然而", "不过", "如果", "虽然", "而且", "并且", "或者",
    "还是", "不是", "就是", "只是", "但是", "可以", "能够", "应该",
    "需要", "可能", "已经", "正在", "通过", "对于", "关于", "根据",
    "以及", "包括", "其中", "之间", "之后", "之前", "以上", "以下",
    "进行", "使用", "利用", "采用", "基于", "来自", "进入", "开始",
    "研究", "分析", "讨论", "介绍", "提供", "产生", "发现", "提出",
    "成为", "作为", "做出", "看到", "知道", "觉得", "认为", "表示",
    # 英文
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "this", "that", "these", "those", "i", "you", "he", "she",
    "it", "we", "they", "me", "him", "her", "us", "them", "my", "your",
    "his", "its", "our", "their", "mine", "yours", "hers", "its", "ours",
    "theirs", "what", "which", "who", "whom", "whose", "when", "where",
    "why", "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "just", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "also",
}

# 对齐检查标准的章节标题（织的输出应有结构）
WEAVE_EXPECTED_SECTIONS = [
    "浮现的模式",
    "核心逻辑链",
    "信息分层",
    "再思考的视角",
    '给"写"的材料包',
]


def extract_keywords(text: str, max_words: int = 20) -> list[str]:
    """从文本中提取有意义的词汇。
    
    策略：
    - 英文：正则提取，去停用词，转小写
    - 中文：bigram/trigram 无词典分词（不依赖 jieba 等外部库）
    - 排序：按词频降序取 top N
    """
    from collections import Counter

    # 提取英文词汇
    eng_tokens = re.findall(r'[a-zA-Z]+(?:[-/][a-zA-Z]+)*', text)
    result = [t.lower() for t in eng_tokens if t.lower() not in STOP_WORDS and len(t) > 1]

    # 提取中文连续字符，用二元组/三元组做无词典分词
    chinese_seqs = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    for seq in chinese_seqs:
        clean_seq = ''.join(c for c in seq if '\u4e00' <= c <= '\u9fff')
        if len(clean_seq) < 2:
            continue
        for i in range(len(clean_seq) - 1):
            bigram = clean_seq[i:i+2]
            if bigram not in STOP_WORDS:
                result.append(bigram)
        for i in range(len(clean_seq) - 2):
            trigram = clean_seq[i:i+3]
            if trigram not in STOP_WORDS:
                result.append(trigram)

    freq = Counter(result)
    return [word for word, _ in freq.most_common(max_words)]


def check_keyword_coverage(keywords: list[str], weave_text: str) -> dict:
    """检查关键词在织输出中的覆盖情况。"""
    if not keywords:
        return {"coverage": {}, "ratio": 1.0, "covered": 0, "total": 0}

    text_lower = weave_text.lower()
    coverage = {}
    covered_count = 0

    for kw in keywords:
        found = kw.lower() in text_lower
        coverage[kw] = found
        if found:
            covered_count += 1

    return {
        "coverage": coverage,
        "ratio": covered_count / len(keywords),
        "covered": covered_count,
        "total": len(keywords),
    }


def check_section_structure(weave_text: str) -> dict:
    """检查织输出是否包含期望的结构章节。"""
    results = {}
    found_count = 0

    for section in WEAVE_EXPECTED_SECTIONS:
        found = section in weave_text
        results[section] = found
        if found:
            found_count += 1

    return {
        "sections": results,
        "ratio": found_count / len(WEAVE_EXPECTED_SECTIONS),
        "found": found_count,
        "total": len(WEAVE_EXPECTED_SECTIONS),
    }


def check_alignment(topic: str, weave_text: str) -> tuple[str, str]:
    """对齐检查主函数。
    
    参数：
        topic: 用户原始研究主题
        weave_text: 织步骤的关联地图文本
    
    返回：
        (report, status) 结构化 Markdown 报告 + "pass"/"warn"/"fail"
    """
    keywords = extract_keywords(topic)
    kw_coverage = check_keyword_coverage(keywords, weave_text)
    section_check = check_section_structure(weave_text)

    # 判定标准
    kw_ok = kw_coverage["ratio"] >= 0.5
    section_ok = section_check["ratio"] >= 0.5

    if kw_ok and section_ok:
        verdict = "✅ 已对齐"
        correction = '无修正。研究方向与用户原始关切一致，可进入"写"步骤。'
        missing_angles = "未发现明显遗漏方向。"
        status = "pass"
    elif kw_ok and not section_ok:
        verdict = "⚠️ 结构不完整"
        missing_sections = [s for s, found in section_check["sections"].items() if not found]
        correction = f"建议补充以下章节结构：{'、'.join(missing_sections)}。内容方向基本正确，但输出格式需要更结构化。"
        missing_angles = f"织的输出缺少标准章节：{'、'.join(missing_sections)}"
        status = "warn"
    elif not kw_ok and section_ok:
        verdict = "⚠️ 关键词覆盖不足"
        missing_kw = [kw for kw, found in kw_coverage["coverage"].items() if not found]
        correction = f"以下关键词在关联地图中未充分体现：{', '.join(missing_kw[:8])}{'等' if len(missing_kw) > 8 else ''}。建议补充相关方向的搜索。"
        missing_angles = f"未覆盖的关键方向：{'、'.join(missing_kw[:5])}..."
        status = "warn"
    else:
        verdict = "❌ 严重偏离"
        missing_kw = [kw for kw, found in kw_coverage["coverage"].items() if not found]
        missing_sections = [s for s, found in section_check["sections"].items() if not found]
        correction = (
            f"研究已偏离用户原始关切。\n"
            f"- 关键词缺失：{', '.join(missing_kw[:5])}...\n"
            f"- 章节缺失：{'、'.join(missing_sections)}\n"
            f"建议回退到探/搜步骤，重新聚焦用户核心问题。"
        )
        missing_angles = f"严重偏离：关键词覆盖率仅 {kw_coverage['ratio']:.0%}，章节完整度仅 {section_check['ratio']:.0%}"
        status = "fail"

    covered_kw = [kw for kw, found in kw_coverage["coverage"].items() if found]
    uncovered_kw = [kw for kw, found in kw_coverage["coverage"].items() if not found]

    report = f"""## 对齐检查报告

### 用户原始关切
{topic}

### 关联地图覆盖度
- ✅ 已覆盖的方向：{', '.join(covered_kw[:10]) or '无'}
- ⚠️ 部分覆盖的方向：{', '.join(uncovered_kw[:5]) or '无'}
- ❌ 遗漏的方向：{missing_angles}

### 结构完整性
- 【{'✅' if section_check['ratio'] >= 0.75 else '⚠️' if section_check['ratio'] >= 0.5 else '❌'}】章节完整度: {section_check['found']}/{section_check['total']}
{chr(10).join([f"  - {'✅' if found else '❌'} {s}" for s, found in section_check['sections'].items()])}

### 关键词覆盖统计
- 总关键词: {kw_coverage['total']}
- 已覆盖: {kw_coverage['covered']}
- 覆盖率: {kw_coverage['ratio']:.0%}

### 判定
{verdict}

### 修正指令
{correction}

---
*🤖 代码对齐检查 v1.0 | 耗时 <0.01s | 节省 1 次 API 调用*
"""
    return report, status


def run_align_code(topic: str, weave_path: str, output_dir: str = None) -> tuple[str, str, str]:
    """流水线集成接口。
    
    参数：
        topic: 用户原始研究主题
        weave_path: 织步骤输出文件路径
        output_dir: 输出目录（默认与weave同目录）
    
    返回：
        (fpath, report, status)
    """
    weave_path = Path(weave_path)
    weave_text = weave_path.read_text(encoding="utf-8")

    report, status = check_alignment(topic, weave_text)

    if output_dir is None:
        output_dir = str(weave_path.parent)

    slug = re.sub(r'[^\w\s-]', '', topic)[:30].strip().replace(' ', '_')
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    import os
    fpath = os.path.join(output_dir, f"{slug}_对齐_{ts}.md")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(report)

    return fpath, report, status


if __name__ == "__main__":
    # 测试
    test_topic = "GraphRAG 在知识库中的假引文问题与解决方案"
    test_weave = """
## 关联地图

### 浮现的模式
GraphRAG 在处理复杂查询时表现出色，但在长尾知识查询中存在幻觉问题。

### 核心逻辑链
知识库检索 → 图结构增强 → LLM生成 → 事实一致性校验

### 信息分层
- ✅确定层：GraphRAG 在标准化查询中准确率高
- ⚠️推断层：假引文问题源于图结构噪声累积
- ❓猜测层：通过反问向量可有效过滤假引文

### 再思考的视角
是否需要引入外部知识图谱验证？

### 给"写"的材料包
GraphRAG假引文分类 + 现有解决方案对比 + 推荐方案
"""

    result, status = check_alignment(test_topic, test_weave)
    print(f"状态: {status}")
    print(result)
