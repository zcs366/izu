# 知乎回答页 vs 专栏页 · 选择器差异

## 专栏文章 (zhuanlan.zhihu.com/p/...)

```python
selectors = [".RichText", ".Post-RichText", "article", ".css-376mun"]
```

- `.RichText` 是最可靠的（2026-05-14验证）
- 先用 `.RichText`，不行再试 `.Post-RichText`

## 回答页面 (zhihu.com/question/.../answer/...)

```python
selectors = [".AnswerCard .RichContent", ".RichContent", ".AnswerItem-content"]
```

- `.AnswerCard .RichContent` 是第一选择（最新版知乎）
- `.RichContent` 是通用备选
- ⚠️ 专栏选择器（`.RichText`）在回答页可能匹配到无关元素

## 验证方法

每次抓取后检查 `len(content) > 200`，不足则换下一个选择器。
