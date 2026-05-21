# TinyFish — Free Search & Fetch MCP Server

> **官网**: https://agent.tinyfish.ai  
> **文档**: https://docs.tinyfish.ai  
> **MCP 端点**: `https://agent.tinyfish.ai/mcp@latest`  
> **注册**: 邮箱注册，无需绑信用卡，新用户赠 500 credits  
> **Search/Fetch 永久免费**: Search 5次/分钟，Fetch 25 URL/分钟

## 能力

| 功能 | 端点 | 免费限制 | 说明 |
|------|------|---------|------|
| **Search API** | `GET https://api.search.tinyfish.ai` | 5次/分钟 | 实时搜索，结构化结果 |
| **Fetch API** | `POST https://api.fetch.tinyfish.ai` | 25 URL/分钟 | 真实浏览器渲染 + stealth 反爬，返回干净 Markdown |
| **Agent API** | `POST https://agent.tinyfish.ai/v1/automation/...` | 消耗 credits | NLP 驱动浏览器自动化 |
| **Browser API** | `POST https://api.browser.tinyfish.ai` | 消耗 credits | 远程 CDP/Playwright 控制 |

## Hermes MCP 配置

在 `~/.hermes/config.yaml` 中添加：

```yaml
mcp_servers:
  tinyfish:
    url: "https://agent.tinyfish.ai/mcp@latest"
    headers:
      Authorization: "Bearer [REDACTED]-你的APIKEY"
    timeout: 60
```

API Key 也可以在 `~/.hermes/.env` 中保存：

```
TINYFISH_API_KEY=[REDACTED]-你的APIKEY
```

## 验证

重启 Hermes 后：

```bash
hermes mcp list
```

预期输出：

```
Name         Transport                          Tools    Status
──────────── ────────────────────────────────── ──────── ──────────
tinyfish     https://agent.tinyfish.ai/mcp...   all      ✓ enabled
```

工具将被注册为 `mcp_tinyfish_*` 前缀，可在任何会话中直接调用。

## 典型用法

在 Hermes 对话中，MCP 工具会自动可用：

- `mcp_tinyfish_search(query, max_results)` — 搜索网页
- `mcp_tinyfish_fetch(url)` — 抓取网页内容为 Markdown
- `mcp_tinyfish_agent(goal)` — 浏览器自动化

这些工具集成在 Shearch Fetch 上，无需额外配置。

## 注意

- API Key 以 `[REDACTED]-` 开头
- 不要在非交互环境（如 terminal tool）中使用 `hermes mcp add --auth header` 配置——交互式 getpass 提示会失败。应直接写入 `config.yaml`。
- Search 和 Fetch 永久免费，Agent 和 Browser 消耗 credits
