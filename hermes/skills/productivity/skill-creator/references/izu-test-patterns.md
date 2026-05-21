# IZU 测试模式 (Mock 陷阱 & 最佳实践)

从多次编写 izu 模块测试的迭代中沉淀的经验。

## 核心原则

1. **先看现有测试的写法** — `test_trajectory_credit.py` 是 izu 测试的样式锚。按那个风格写: pytest class-based, `tmp_path` 或 `@patch`, 中文 docstring。
2. **能不 mock 就不 mock** — 纯逻辑函数（`decay_score`, `state_str`, `TaskClassifier.classify`, `extract_key_content`）直接测，零 mock。
3. **模块级全局用 `patch.object(cls, ...)`** — 不要 `patch("some_module.Path.glob")`。

---

## Mock 陷阱速查表

### 1. `random.random` 在函数内部被 import

```python
# ❌ 错误 (mock 模块级):
with patch("trajectory_balance.random.random", return_value=0.1):
# → AttributeError: module 'trajectory_balance' has no attribute 'random'

# ✅ 正确 (mock 全局 random):
with patch("random.random", return_value=0.1):
```

**原因**: `should_sample()` 方法内部执行 `import random`（惰性导入），所以 `random` 不在模块命名空间里。必须 mock 全局 `random.random`。

### 2. `Path.read_text()` 而非 `builtins.open`

izu_session_memory.py 的 `parse_session()` 使用 `path.read_text(encoding='utf-8')`，不是 `open(path)`:

```python
# ❌ 错误:
with patch("builtins.open", mock_open(read_data=data)):

# ✅ 正确:
with patch.object(Path, "read_text", return_value=data):
```

同理 `count_turns()` 使用 `open(path)`，所以用 `patch("builtins.open")` 对它是可以的。看源码决定用哪个。

### 3. `Path.glob()` 是 C 级方法，不可直接 patch 实例

```python
# ❌ 错误:
with patch.object(Path, "glob", return_value=[Path("/fake.json")]):
# → AttributeError: 'PosixPath' object attribute 'glob' is read-only

# ✅ 正确方法 A: 用模块级引用的类
import izu_session_memory as ism
with patch.object(ism.SESSIONS.__class__, "glob", return_value=[]):

# ✅ 正确方法 B: mock 整个模块级的 sessions 变量
with patch("izu_session_memory.SESSIONS") as mock_sessions:
    mock_sessions.glob.return_value = []
```

### 4. `os.path.getmtime` 在 `sorted(... key=...)` 中

CLI 命令如 `cmd_compact()` 调用 `sorted(SESSIONS.glob('*.json'), key=os.path.getmtime)`。即使 mock 了 glob 返回的 Path 对象，`os.path.getmtime` 仍然会尝试 stat 真实路径:

```python
# ❌ 即便有 mock glob，这个依然会 FileNotFoundError:
mock_glob.return_value = [Path("/nonexistent/session.json")]

# ✅ 方案 A: 返回空列表（函数会快速退出）
mock_glob.return_value = []

# ✅ 方案 B: 用 tmp_path 创建真实文件
p = tmp_path / "session.json"
p.write_text(data)
mock_glob.return_value = [p]
```

### 5. compact JSON 与 `count_turns` 的兼容性

`count_turns()` 逐行扫描 `'"role":'` 出现次数并除以 2:

```python
with open(path) as f:
    return sum(1 for l in f if '"role":' in l) // 2
```

```python
# ❌ 单行 JSON → count_turns 可能不正确:
json.dumps({"messages": [...]})  # 所有内容在一行

# ✅ 多行 JSON → 每轮 role 在不同行:
json.dumps({"messages": [...]}, indent=2)
```

### 6. `extract_key_content` 的 tool role 过滤条件

tool role 消息只有同时满足 `len(content) > 50` 且含特定关键词才进入 key_facts:

```python
if role == 'tool' and len(content) > 50:
    if any(k in content for k in ['/mnt/', '.md', '.py',
                                  'success', 'completed', '写入']):
        result['key_facts'].append(content[:100])
```

测试时需要构造长度 > 50 字符的内容。

---

## 推荐的测试结构

### 模块级常量/函数

```python
import izu_session_memory as ism   # 注意 import 整个模块

# 这样 CLI 命令中的 SESSIONS、MEMORY_FILE 等全局变量
# 可以通过 ism.SESSIONS 访问，便于 patch
```

### 纯函数（零 mock）

```python
class TestDecayScore:
    def test_persistent_always_one(self):
        assert decay_score(1000, persistent=True) == 1.0

    def test_one_half_life(self):
        assert decay_score(DECAY_HALF_LIFE) == pytest.approx(0.5, abs=0.01)
```

### 带文件 IO 的函数

```python
class TestParseSession:
    def test_parse_json_dict(self):
        data = json.dumps({"messages": [{"role": "user", "content": "hi"}]})
        with patch.object(Path, "read_text", return_value=data):
            msgs = parse_session(Path("/f/s.json"))
        assert len(msgs) == 1
```

### 集成测试（tmp_path 真实文件）

```python
class TestIntegration:
    def test_compact_roundtrip(self, tmp_path):
        hermes_dir = tmp_path / "hermes"
        (hermes_dir / "memories" / "compacted").mkdir(parents=True)
        session_path = hermes_dir / "sessions" / "test.json"
        session_path.parent.mkdir(parents=True)
        session_path.write_text(json.dumps({...}, indent=2))

        with patch("izu_session_memory.HERMES", hermes_dir):
            compact_path = compact_session(session_path)

        assert compact_path.exists()
        assert "关键词" in compact_path.read_text()
```

---

## 运行命令

```bash
# 单文件
pytest test_trajectory_balance.py -v

# 多文件
pytest test_trajectory_balance.py test_izu_session_memory.py -v

# 全部
pytest . -v

# 用 Makefile
make test
```
