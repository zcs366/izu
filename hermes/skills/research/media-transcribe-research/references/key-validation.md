# Groq API Key 有效性检测与故障恢复

> 2026-05-16 实测记录：`.env` 中 `GROQ_API_KEY=***` 是占位符，非有效 Key。

## 检测方法

### Python 检测

```python
import os
env_path = os.path.expanduser("~/.hermes/.env")
with open(env_path) as f:
    for line in f:
        if line.startswith("GROQ_API_KEY"):
            val = line.split("=", 1)[1].strip()
            if val == "***":
                print("⚠️ 占位符，无效")
                # → 降级到本地 faster-whisper
            elif val:
                print(f"✅ 有效: {val[:10]}...")
                # → 尝试 Groq API
```

### Shell 检测

```bash
if grep -q 'GROQ_API_KEY=\*\*\*' ~/.hermes/.env; then
  echo "⚠️ Groq key 是占位符——降级到本地 faster-whisper"
fi
```

### Curl 探测

```bash
GROQ_KEY=$(grep GROQ_API_KEY ~/.hermes/.env | cut -d= -f2)
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_KEY" | head -100
# 返回: {"error":{"message":"Forbidden"}} → key 无效
# 返回: {"data":[{"id":"whisper-large-v3-turbo",...}]} → key 有效
```

## 已知状态

| Key 值 | 含义 | 行动 |
|--------|------|------|
| `***` | 占位符，从未设置过 | 降级到本地 faster-whisper |
| `gsk_xxx...` → curl 返回 403 Forbidden | Key 过期/被撤销 | 降级，通知用户换 key |
| `gsk_xxx...` → curl 返回正常 | Key 有效 | 正常使用 Groq STT |

## 恢复流程

1. Key 无效 → **直接降级**，不要重试
2. 降级目标：本地 faster-whisper medium 模型（已缓存，`~/.cache/huggingface/hub/models--Systran--faster-whisper-medium/`）
3. 工作目录：`/mnt/i/hermes/tmp/bilibili_audio/`（不用 `/tmp/`）
4. 预计耗时：20min 音频约 8-12min（CPU 4核 400%）
