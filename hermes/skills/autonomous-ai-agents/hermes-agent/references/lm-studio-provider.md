# LM Studio Provider

LM Studio 是一个本地运行 LLM 的桌面应用（Windows/macOS/Linux），提供 OpenAI 兼容的 API 端点。可在 Hermes Agent 中作为自定义 provider 使用。

## Split API Paths（重要）

**⚠️ LM Studio v1.x 的 API 路径是分裂的，管理端点和推理端点路径不同！**

| 端点类型 | 路径 | 示例 |
|---------|------|------|
| 管理 API（模型列表） | `/api/v1/...` | `GET /api/v1/models` ✅ |
| OpenAI 兼容 API（推理） | `/v1/...`（标准） | `POST /v1/chat/completions` ✅ |
| /api/v1 路径的推理 | `/api/v1/...` | `POST /api/v1/chat/completions` ❌ |

**这意味着 Hermes 配置中的 `base_url` 必须使用标准 OpenAI 路径 `http://host:port/v1`，而不是 `http://host:port/api/v1`。**

## 基本配置

### 方式 A：直接设置 model（快速切换）

```bash
# 临时使用 LM Studio 会话
hermes chat --provider custom -m "your-model-name" \
  --provider-base-url http://localhost:1234/v1 \
  --provider-api-key "sk-lm-xxx"
```

### 方式 B：添加为命名 provider（推荐）

在 `~/.hermes/config.yaml` 的 `providers` 节添加：

```yaml
providers:
  lm-studio:
    base_url: http://192.168.1.7:11234/v1    # 注意：使用 /v1 而非 /api/v1
```

然后在 `.env` 中添加：

```bash
LM_STUDIO_API_KEY=sk-lm-xxx:yyyy
```

使用方式：

```bash
# CLI 启动时指定
hermes chat --provider lm-studio -m "mistralai/mistral-small-3.2"

# 会话内切换
/model mistralai/mistral-small-3.2
```

### 方式 C：配置为 auxiliary 任务

LM Studio 本地模型可以承担 Hermes 的辅助任务，尤其是 **vision（视觉）**——很多云端模型不支持看图，而本地模型如 Mistral Small 3.2 带视觉能力。

```yaml
auxiliary:
  vision:
    provider: lm-studio
    model: mistralai/mistral-small-3.2
    base_url: http://192.168.1.7:11234/v1
    api_key: sk-lm-JebJkxaS:Mz4nCplYzsFlTGFaR7OJ
    timeout: 120
```

配置后，所有图片分析请求自动走本地模型。

## API 认证

LM Studio 默认开启 API 认证。有三种处理方式：

### 方式 A：使用 Token（推荐）

在 LM Studio GUI → 设置 → API Tokens 中查看或创建 token。然后在 `.env` 中添加：

```bash
LM_STUDIO_API_KEY=sk-lm-xxx:yyyy
```

⚠ **Token 格式**：LM Studio 的 token 通常是 `sk-lm-` 开头，带冒号分隔（如 `sk-lm-xxx:yyyy`）。直接在 Bearer header 中使用即可。

### 方式 B：关闭认证

LM Studio GUI → 设置 → 关闭 "API Authentication"，然后不需要设置 api_key。

### 方式 C：启动时设置环境变量

```bash
# 在 LM Studio 启动前设置
set LM_STUDIO_API_TOKEN="your-token"   # Windows
export LM_STUDIO_API_TOKEN="your-token" # macOS/Linux
```

## 端口

默认端口是 `1234`，但 LM Studio 也可以配置为其他端口。通过 LM Studio GUI → 设置 → Server Port 修改。本环境的 LM Studio 使用端口 `11234`。

## 在 WSL 中使用

LM Studio 通常运行在 Windows 上。Hermes 运行在 WSL 中时：

- 用 `localhost`（Windows → WSL 自动桥接）—— 适用于同机
- 或用 Windows 主机的局域网 IP（如 `192.168.1.7`）—— 适用于跨机或明确路由

```yaml
# WSL 中访问 Windows 上的 LM Studio
model:
  base_url: http://192.168.1.7:11234/v1
```

## 验证连接

```bash
# 检查 LM Studio 是否运行（管理 API）
curl -s http://localhost:1234/api/v1/models \
  -H "Authorization: Bearer sk-lm-xxx"

# 测试对话（OpenAI 兼容 API — 注意路径不同）
curl -s http://localhost:1234/v1/chat/completions \
  -H "Authorization: Bearer sk-lm-xxx" \
  -H "Content-Type: application/json" \
  -d '{"model":"mistralai/mistral-small-3.2","messages":[{"role":"user","content":"你好"}]}'
```

## 模型选择参考

LM Studio 运行在本地 GPU 上，模型选择取决于显存大小：

| GPU 显存 | 推荐模型范围 | 示例 |
|----------|-------------|------|
| 6-8 GB | 7B Q4_K_M ~ 8B Q4_K_M | DeepSeek-R1-Distill-Qwen-7B, Gemma-2-9B |
| 8-12 GB | 8B Q8_0 ~ 12B Q4_K_M | Phi-4 14B Q4_K_M |
| 12-16 GB | 15B Q4_K_M ~ 24B Q4_K_M | Mistral Small 3.2 24B Q4_K_M |
| 16-22 GB | 24B Q6_K ~ 32B Q4_K_M | QwQ 32B Q4_K_M, Qwen3 32B Q4_K_M |
| 22-24 GB | 32B Q4_K_M + 32k ctx | Qwen3 32B ~131k ctx 需限制上下文 |

**本环境**：RTX 2080 Ti 22GB → Mistral Small 3.2 24B Q4_K_M (15.2GB) + 131k 上下文余量充足。

## 已知问题

- **冷启动延迟**：模型首次加载或空闲后重新推理时可能需要较长时间，建议热身一次。
- **模型名**：LM Studio 返回的模型名可能与文件名不完全一致。用 `curl /api/v1/models` 获取准确的标识符（如 `mistralai/mistral-small-3.2`）。
- **路径猜错**：如果你把 base_url 配成了 `/api/v1` 但 chat completions 报 "Unexpected endpoint or method"，说明此 LM Studio 版本的分裂路径与预期不同——先试 `/api/v1/models` 确认管理 API 通，再用 `/v1/chat/completions` 测推理。
