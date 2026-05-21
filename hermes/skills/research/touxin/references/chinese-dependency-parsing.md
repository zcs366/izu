# 中文spaCy依赖解析要点

- **模型**：zh_core_web_sm（spacy download，约48MB）
- **关键bug**：所有动词的lemma_返回空字符串！必须用token.text代替
- **中文句子特征**：Root常是名词，动词通过conj并列连接
- **cop系词模式**：中文"A是B"中，"是"是cop，root是B（名词）
- **noun_chunks不支持中文**：用连续NOUN/PROPN序列手动提取
- **停用词**：过滤"的/了/着/在/可以/需要/来/去"等低信息量动词
- **子树截断**：subtree限制≤20 token，防止整句当宾语

生产脚本：izu/dep_parse_zh.py
输出：data/wiki-graph-dep-parse-zh-v4.json（150篇→4016边→24568节点→密度0.163）
