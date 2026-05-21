# Curl HTML Rescue Pattern (2026-05-21)

**适用场景**: Firecrawl 额度用尽 + ddgs 间歇性失败时，用 curl 直接抓取页面内容。

## 原理

当 `web_search` / `web_extract` / ddgs 全部不可用时，curl 是最后的可靠武器。它绕过 API 限制，直接下载原始 HTML 或纯文本文件。

## 三类来源及对应策略

### 第一类：GitHub Raw（最可靠）

GitHub 的 `raw.githubusercontent.com` 提供纯文本 .md 文件，无任何反爬机制。

```bash
curl -sL "https://raw.githubusercontent.com/a2aproject/A2A/main/README.md" | head -300
```

**最长使用示意**（无管道，直接输出）：

```bash
curl -sL "https://raw.githubusercontent.com/{owner}/{repo}/main/{path}" --max-time 15
```

**优势**：纯文本，零噪音，直接可读。

### 第二类：官方文档页面（需 Python 洗数据）

标准 HTML 文档站（mkdocs-material, readthedocs 等），需要剥离标签。

```bash
curl -sL "https://example.org/docs" --max-time 10 | python3 -c "
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

**关键技巧**：
1. `--max-time 10` — 防止挂起（某些文档站响应慢）
2. `re.DOTALL` — 让 `.` 匹配换行符（否则 multiline script 块剥不干净）
3. `len(l) > 20` — 过滤短行噪音（导航文字、页码等）
4. `seen` 集合去重 — mkdocs 等框架在多个章节重复渲染相同导航模板

### 第三类：有反爬保护的网站

部分网站（知乎、技术博客）会检测 curl 的默认 User-Agent。

```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  "https://zhuanlan.zhihu.com/p/example" --max-time 10 | \
  python3 -c "...上述洗数据脚本..."
```

**如果还返回空**：尝试 `curl -sL -H "User-Agent: ..." -H "Accept: text/html,application/xhtml+xml"` 或改用 browser 工具。

## 实战案例：A2A 协议研究（2026-05-21）

| 目标 | 命令 | 结果 |
|------|------|------|
| 协议说明 | `curl -sL raw.githubusercontent.com/a2aproject/A2A/main/README.md` | ✅ 完整 README |
| 协议规范 | `curl -sL raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md` | ✅ 完整规范（前 400 行） |
| 官方首页 | `curl -sL a2a-protocol.org/latest/` | ✅ 首页文字内容提取 |
| 规范页面 | `curl -sL a2a-protocol.org/latest/specification/` | ✅ 规范目录结构 |
| 阿里云文章 | `curl -sL developer.aliyun.com/article/1661863` | ❌ 超时阻塞 |
| 公告页面 | `curl -sL a2a-protocol.org/latest/announcing-1.0/` | ❌ 超时阻塞 |

**成功约 66%**——足够覆盖研究需求。

## 注意事项

1. **超时是常态** — 设置 `--max-time 10-15`，失败就跳过。不超时的页面通常足够用。
2. **内容有损** — 洗数据后丢失列表标记、代码块格式、表格结构。换行方法 (`<[^>]+> → \n`) 比空格方法 (`→ ' '`) 更能保留下行结构。
3. **不适用于 SPA** — 单页应用（React/Vue 渲染）的 HTML 不含实质内容，curl 抓不到。此时必须用 browser 工具。
4. **GitHub 是最好朋友** — 如果主题在 GitHub 上有仓库，优先抓取 raw md 文件，它们比官方的 HTML 文档站更可靠。
5. **不要追多个失败** — 如果一个站点超时/返回空，记下来跳过，继续下一个。时间用在有效的来源上。
