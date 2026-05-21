# Batch DDGS Research Template

**当三个研究代理全部超时时使用**。此模板在单个 terminal 调用中运行 8 个查询，比逐个查询或重新委托代理快得多。

## 标准模板（8 查询）

```python
python3 << 'PYEOF'
from ddgs import DDGS

queries = [
    # --- 官方文档类 ---
    "Google AI Studio official documentation features",
    "Google AI Studio pricing free tier Gemini API 2025",

    # --- 竞品对比类 ---
    "Google AI Studio vs ChatGPT Claude comparison",

    # --- 技术教程类 ---
    "Google AI Studio prompt engineering guide",
    "Google AI Studio tutorial review developer experience",

    # --- 社区资源类 ---
    "Google AI Studio 使用教程 功能介绍",
    "Google AI Studio system instructions multimodal",

    # --- 专业评测类 ---
    "Google AI Studio review 2026 developer experience",
]

with DDGS() as ddgs:
    for q in queries:
        print(f"\n{'='*80}")
        print(f"QUERY: {q}")
        print(f"{'='*80}")
        try:
            for r in ddgs.text(q, max_results=6):
                print(f"TITLE: {r['title']}")
                print(f"URL: {r['href']}")
                print(f"BODY: {r['body'][:400]}")
                print("---")
        except Exception as e:
            print(f"ERROR: {e}")
PYEOF
```

## 自定义模板（替换 queries 列表）

```python
queries = [
    # 按类别组织，每类 2-3 个
    "XXX official documentation",
    "XXX pricing API 2025",
    "XXX tutorial beginner guide",
    "XXX vs competitor comparison",
    "XXX review experience pros cons",
    "site:zhihu.com XXX 教程",
    "site:youtube.com XXX tutorial",
    "XXX use case case study",
]
```

## 为什么这个模式有效

1. **效率**：8 个查询只需 1 个 terminal 调用（~30 秒完成），而不是 8 个独立的 web_search 调用
2. **鲁棒性**：每个查询有独立的 try/except，失败不影响后续查询
3. **完整上下文**：所有结果留在 conversation context 中，无需临时文件
4. **内容充足**：6 条结果 × 8 查询 = 48 个搜索结果片段，足够覆盖 Phase 1 需求

## 后续步骤：curl 深度提取

### 标准方式

DuckDuckGo 只返回搜索片段，对关键官方页面需用 curl 提取正文：

```bash
curl -sL "https://example.com/docs" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
print(text[:8000])
"
```

> ⚠️：某些网站会检测 curl（返回空/验证页面）。如遇此情况，尝试加 User-Agent header：
> `curl -sL -H "User-Agent: Mozilla/5.0" "https://example.com"`

### 增强版：脚本+样式剥离 + 去重去噪（2026-05-21 验证）

对于 mkdocs-material 等框架生成的文档站，HTML 中含有大量导航模板噪音。以下模式在 A2A 协议研究中验证有效：

```bash
curl -sL "https://docs.example.org/latest/" --max-time 10 | python3 -c "
import sys, re
html = sys.stdin.read()
# 先去除 script 和 style 块（它们含大量噪音）
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
# 所有标签换行符
text = re.sub(r'<[^>]+>', '\n', text)
# 合并空白行
text = re.sub(r'\n\s*\n', '\n\n', text)
# 去除非空行
lines = [l.strip() for l in text.split('\n') if l.strip()]
# 去重（页面模板产生大量重复片段）
seen = set()
for l in lines:
    if l not in seen and len(l) > 20:
        seen.add(l)
        print(l)
" 2>&1 | head -150
```

**版本对比**：

| 版本 | 步骤 | 产出质量 | 适用场景 |
|------|------|---------|---------|
| 基础版（空格法） | 去标签、去空白 | 2-3 段碎片 | 纯文本博客 |
| 增强版（换行+去重） | 去脚本+去样式+换行+合并+去重 | 可读段落流 | 框架文档站（mkdocs, readthedocs） |

### 当 ddgs 失败时的完整救援流程（2026-05-21 A2A 研究验证）

如果 ddgs 只返回了部分结果然后 ConnectError 死亡：

```
1. ddgs (8 queries) → 部分成功（5-6 个有用 URL）
2. curl GitHub raw README.md + specification.md → 完整协议规范的 70%
3. curl 官方首页 + 规范目录 → 文档结构的 80%
4. 跳过超时的页面（不追没有结果的来源）
5. 剩余内容从训练知识补充
```

**不追失败来源**的原则：如果一个站点超时/返回空，记下来跳过，继续下一个。时间用在有效来源上。

## 适用场景

- Firecrawl 额度用尽（返回 "Payment Required"）
- 三个研究代理全部超时
- 需要快速了解一个新产品/工具
- 在 terminal 可用但 web_search 工具不可用的情况下
