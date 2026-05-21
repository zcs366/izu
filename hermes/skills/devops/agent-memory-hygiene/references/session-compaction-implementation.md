# Session Compaction 实现参考

> 从 `izu_session_memory.py` 提炼的规则压缩实现方案
> 零LLM成本，纯正则+关键词提取

## 核心数据结构

```python
# 从session中提取的关键内容
{
    'decisions': [],      # 决策/结论
    'intents': [],        # 用户意图/问题
    'code_blocks': [],    # 代码片段
    'urls': set(),        # 引用链接
    'key_facts': [],      # 关键事实
    'tool_actions': [],   # 工具调用（原始列表，可去重统计）
}
```

## 消息解析（支持两种session格式）

```python
def parse_session(path):
    """解析session文件为消息列表"""
    raw = path.read_text()
    msgs = []
    # 尝试JSON对象格式（含messages/conversation/history/turns键）
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            for key in ['messages', 'conversation', 'history', 'turns']:
                if key in data and isinstance(data[key], list):
                    msgs = data[key]; break
    except json.JSONDecodeError:
        # 尝试JSONL格式（每行一条消息）
        for line in raw.split('\n'):
            line = line.strip()
            if line:
                try: msgs.append(json.loads(line))
                except: pass
    return msgs
```

## 决策提取关键词

```python
DECISION_MARKERS = [
    '因此:', '所以:', '结论:', '决定:', '军师终裁:',
    '**结论**', '**决定**', '**方案**'
]

INTENT_MARKERS = [
    '开干', '启动', '开始', '创建', '写', '部署', '安装', '设置'
]

TOOL_EXTRACTOR = re.compile(r'https?://[^\s\)\]>]+')  # URL提取
CODE_EXTRACTOR = re.compile(r'```[\w]*\n.*?```', re.DOTALL)  # 代码块提取
```

## 压缩动作

1. 从session中提取关键内容
2. 生成结构化markdown摘要
3. 写入 `~/.hermes/memories/compacted/{name}_compact.md`
4. 原始session重命名为 `.archived`（保留但不再扫描）

> 5轮以上的待遗忘session走压缩归档路径
> 5轮以下的直接标记为 `.purged`（太短无压缩价值）
> request_dump等无法解析的文件直接移至 purged 目录

## 工作记忆评分关键词

```python
SCORE_WEIGHTS = {
    '决策信号': 30,   # 记住/重要/必须/决定/结论/因此
    '引用性': 15,     # 上次/之前/刚才/前面
    '动作': 10,        # 写入/创建/修改/部署/删除
    '疑问句': 8,       # 含?
    '用户消息': 5,     # role == 'user'
    '长回复': 3,       # assistant回复>200字
    '极短回复': -5,    # "好的"/"明白"/"嗯"/"ok"
}
```
