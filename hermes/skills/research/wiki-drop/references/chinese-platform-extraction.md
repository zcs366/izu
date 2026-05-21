# Chinese Platform Content Extraction

> Proven recipes for extracting article content from JS-heavy Chinese platforms
> where `web_extract` (Firecrawl) fails due to credit limits, JS rendering, or anti-scraping measures.

## Why Standard Extraction Fails

| Platform | Failure Mode |
|---|---|
| **mp.weixin.qq.com** | JS-rendered content; Firecrawl runs out of credits for long articles; HTML has content hidden in `js_content` div |
| | 2026+ 新增：返回 200 + 腾讯验证码（"环境异常"），需全套浏览器头方可绕过 |
| **zhuanlan.zhihu.com** | Anti-scraping; login wall after 3-5 requests; content lazy-loaded |
| **bilibili.com** | SPA rendering; video pages don't expose article text |
| **toutiao.com** | JS injection; content fragmented across multiple script tags |

## Fallback Pipeline: curl + Python Extraction

### Step 1: Download raw HTML with curl

**⚠️ 微信反爬升级（2026）：** 仅设置 User-Agent 会触发"环境异常"验证码页面。必须模拟完整浏览器请求头：

```bash
curl -sL --compressed \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
  -H "Referer: https://mp.weixin.qq.com/" \
  -H "Sec-Fetch-Dest: document" \
  -H "Sec-Fetch-Mode: navigate" \
  -H "Sec-Fetch-Site: none" \
  -H "Sec-Fetch-User: ?1" \
  -H "Upgrade-Insecure-Requests: 1" \
  -c /tmp/wechat_cookies.txt \
  "https://mp.weixin.qq.com/s/ARTICLE_ID" > /tmp/article.html
```

**关键说明：**
- 所有 `Sec-Fetch-*` 头缺一不可 — 微信的腾讯验证码引擎（TCaptcha）会检测这些头是否匹配真实浏览器行为
- `--compressed` 处理 gzip/br 压缩
- `Referer: https://mp.weixin.qq.com/` 是必须的 — 微信拒绝没有来源的请求
- 如果仍遇到验证码，检查响应中是否包含 `window.cgiData.register_code` 或 `TCaptcha` — 有则需添加更多头
- 用 `grep -c "环境异常\|TCaptcha\|js_verify"` 检测是否触发了验证码

User-Agent must be modern Chrome — WeChat blocks bare curl.

### Step 2: Extract content for each platform

#### WeChat (mp.weixin.qq.com)

Content lives inside `<div id="js_content">...</div>`. **推荐使用 bundled 提取脚本**（处理了所有边界情况）：

```bash
cat /tmp/article.html | python3 <skill_path>/scripts/extract-wechat-article.py 2>/tmp/meta.json > /tmp/text.txt
```

脚本输出：stdout 为文章纯文本，stderr 为 JSON 元数据（title, author, nickname, description, length）。

如脚本不可用，手动提取方法如下：

```python
import sys, re

html = sys.stdin.read()

# Try js_content first
content_m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
if not content_m:
    # Fallback: rich_media_content class
    content_m = re.search(r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
if content_m:
    content = content_m.group(1)
    text = re.sub(r'<br\s*/?>', '\n', content)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Decode HTML entities
    for e, c in [('&nbsp;',' '),('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"')]:
        text = text.replace(e, c)
```

Also extract `title` (from `<title>` or `<meta property="og:title">`) and `author` (from `<meta name="author">` or `id="js_name"` or `js_profile_name`).

**Metadata extraction recipe (author + source):**

```python
# Author
author_m = re.search(
    r'<meta[^>]*name=["\']author["\'][^>]*content=["\'](.*?)["\']',
    html, re.DOTALL)
author = author_m.group(1).strip() if author_m else ''

# Nickname (公众号名称)
nickname_m = re.search(r'var\s+nickname\s*=\s*["\'](.*?)["\']', html)
if not nickname_m:
    nickname_m = re.search(r'"nickname"\s*:\s*"(.*?)"', html)
nickname = nickname_m.group(1).strip() if nickname_m else ''

# Description
desc_m = re.search(
    r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
    html, re.DOTALL)
description = desc_m.group(1).strip() if desc_m else ''
```

Use `author` for the `author:` field in YAML frontmatter, `nickname` for `source:`.

#### Zhihu (zhuanlan.zhihu.com / www.zhihu.com)

Anti-scraping is aggressive. **2026-05 实测：知乎全站已升级 zse-ck JS 挑战，自动化手段全灭。**

| URL 类型 | 反爬机制 | curl+头 | API | web_extract |
|---------|---------|---------|-----|-------------|
| `zhuanlan.zhihu.com/p/...` （专栏） | 登录墙（3-5次后触发） | ⚠️ 偶尔可行 | ❌ | ⚠️ 约50%成功率 |
| `www.zhihu.com/question/...` （问题页） | zse-ck JS 挑战 | ❌ 全灭 | ❌ 403 | ❌ 登录墙 |
| `www.zhihu.com/answer/...` （回答页） | zse-ck JS 挑战 | ❌ 全灭 | ❌ 40362 | ❌ 登录墙 |

**zse-ck 挑战特征：**
- HTML 大小仅 650 字节，包含 `<meta id="zh-zse-ck">` + SHA 加密内容
- 返回 HTTP 200，无错误码，但实际内容被 JS 加密隐藏
- API 端点返回 `{"error":{"code":40362,"message":"您当前请求存在异常..."}}`
- 检测机制：`grep -c "zh-zse-ck" <html>` 返回 >0 即触发

**已验证无解的手段：**
| 尝试 | 结果 |
|------|------|
| curl + 全套浏览器头 | ❌ |
| curl + Cookie 模拟 | ❌ |
| curl_cffi (chrome131) | ❌ |
| Zhihu API (/api/v4/answers/) | ❌ 40362 |
| bing_search 搜 syndicated 版本 | ⚠️ 偶尔有转载（澎湃新闻等） |

**可行手段：**
- 搜索是否有 syndicated 版本（澎湃新闻、什么值得买等经常转载知乎高赞回答）
- 如无转载 → 走 User-Help Fallback（请用户手动复制粘贴）

Best approach:

1. Try `web_extract` first (works for ~50% of zhuanlan articles, ~0% for answer/question pages)
2. Try searching for syndicated versions on 澎湃新闻/thepaper.cn, smzdm.com, 36kr.com
3. If still blocked, use User-Help Fallback

#### Bilibili (in video pages)

Bilibili articles (`www.bilibili.com/read/cv...`) are easier than video pages. Extract via:

```python
# Bilibili articles use class="article-content"
content_m = re.search(r'class="article-content"[^>]*>(.*?)</div>', html, re.DOTALL)
```

### Step 3: Save as markdown with YAML frontmatter

```yaml
---
source_url: https://mp.weixin.qq.com/s/...
ingested: YYYY-MM-DD
sha256: <hex digest of body>
source: 公众号名称
author: 作者名
original_pub: 原载出处（如适用）
---
```

Compute sha256 over the body only (everything after closing `---`):

```bash
sha256sum wiki/raw/articles/slug.md | cut -d' ' -f1
# Then insert into the frontmatter sha256: field
```

### Step 4: Verify content quality

- Read the extracted text: is it coherent? Are paragraphs intact?
- WeChat often has "end-of-article" noise (QR code prompts, "阅读原文" links, "在看" buttons)
- Strip trailing noise lines from the end

## Common Pitfalls

- **WeChat CAPTCHA（"环境异常"）**：现代微信返回 200 + 验证码页面而非 302 重定向。检测方法：`grep -c "环境异常\|TCaptcha"`。绕过方法不是等待，而是补充全套浏览器头（见 Step 1 中的完整 curl 命令）。响应体中若有 `window.cgiData` 对象，确认已触发验证码。
- **Encoding**: WeChat uses UTF-8 but some legacy articles use GBK — check `Content-Type` header, add `--header "Accept-Charset: utf-8"` if needed
- **Fake page**: Some WeChat articles return 200 but show only "此内容因违规无法查看" — check for that string in the response
- **Images**: WeChat images have expiring URLs (CDN tokens). Don't try to download them during ingestion — they'll break. Save the article text only.
- **Large articles**: WeChat allows very long articles (10K+ characters). curl may time out — add `--max-time 30`

## 2026 WeChat Anti-Scraping Reality

**2026-05-09 实战验证：微信反爬已升级到全栈级别，非仅 Header 可破。**

| 尝试过的方案 | 结果 |
|---|---|
| cURL + 全套浏览器头（Sec-Fetch-*、Referer） | ❌ appmsgcaptcha 验证码 |
| curl_cffi (chrome131 TLS 指纹模拟) | ❌ 同上 |
| Playwright (headless Chromium, 反检测 InitScript) | ❌ 重定向到 wappoc_appmsgcaptcha |
| Puppeteer (headless Chrome, stealth) | ❌ 同上 |
| MicroMessenger UA (微信内置浏览器) | ❌ 同上 |
| 搜狗微信搜索 → 跳转 | ❌ 搜狗也跳反爬页 |
| 搜狗微信搜索 → URL 拼接 → 直接访问 | ❌ 微信验证码 |

**根因：IP 信誉检测。** 非中国 IP / 数据中心 IP 直接被标记为高风险，无论如何模拟浏览器都无法绕过。

**检测是否触发：**
```bash
grep -c "环境异常\|TCaptcha\|appmsgcaptcha\|wappoc_appmsgcaptcha" <html>
# 返回 >0 则验证码已触发
```

**绕过此关卡的手段：**
- 中国 IP 代理/VPN 或许可行，但未验证
- 真实微信客户端的 Cookie（从用户浏览器导出）当前环境无法获得

## User-Help Fallback

当所有自动化手段失败时，**直接向用户说明情况并请求协助** —— 这是当前最可靠的兜底方案：

```
刺史，微信反爬墙太厚了，自动化方案全撞验证码（非中国 IP 信誉问题）。
最快解决方案：你在微信里打开文章→复制全文→粘贴到咱俩对话。
一篇大概花 2-3 分钟，我收到后立马入库分析。
```

收到底稿后照常走 wiki 入库流程（raw → entities → concepts → index + log）。

## Platform-Specific Extraction

### 163.com (网易订阅文章)

**结构说明：** `dy/article/` 路径下的网易订阅文章，内容在 `class="post_body"` 的 div 中。

```python
import re

post_body = re.search(
    r'class="post_body"[^>]*>(.*?)</div>\s*<div[^>]*class="post_',
    html, re.DOTALL)
if not post_body:
    post_body = re.search(
        r'class="post_body"[^>]*>(.*?)</div>\s*</div>',
        html, re.DOTALL)

if post_body:
    content = post_body.group(1)
    text = re.sub(r'<[^>]+>', '\n', content)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;', '', text)
    text = text.strip()
```

**curl 用法：**
```bash
curl -sL --compressed \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://www.163.com/dy/article/ARTICLE_ID.html" | \
  python3 -c "
import sys, re
html = sys.stdin.read()
m = re.search(r'class=\"post_body\"[^>]*>(.*?)</div>\s*<div[^>]*class=\"post_', html, re.DOTALL)
if m:
    t = re.sub(r'<[^>]+>', '\n', m.group(1))
    t = re.sub(r'\n{3,}', '\n\n', t)
    print(t.strip())
"
