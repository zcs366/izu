---
name: touxin
description: 透心——知乎反爬穿透（抓取+发布）。发链接自动抓取全文→入库wiki；发文章自动发布到知乎。四阶段打穿（穿甲→隐身→破盾→透心），多方案容灾，自适应演进。日常使用：直接把知乎链接丢过来即可。
version: 4.1.0
tags:
  - scraping
  - anti-bot
  - zhihu
  - chinese-web
  - playwright
  - stealth
  - cookie
  - penetration
  - publishing
metadata:
  hermes:
    category: research
author: Hermes Agent
------

# 透心 · 认证态抓取与反爬穿透（含发布）

> "道高一尺，魔高一丈。但攻防异势的关键不是更强——是更愿意在同一个地方反复打。"
> 核心洞察：**不要破解反爬，复用用户的合法身份。**

## 适用场景

- 知乎专栏文章抓取（zse_ck + 多层反爬）
- 知乎文章自动发布（Draft.js编辑器 + 双向认证）
- 其他中文反爬站点：CSDN、简书、掘金、腾讯云社区
- 微信公众号、付费订阅站等需要登录态的站点
- 任何 curl/curl_cffi/CDP 均失败的高反爬站点
- 需要用户登录态才能访问的内容

## 通用认证态方法论（穿甲基座）

当第三方平台反爬强度极高且用户有合法登录态时，核心方法：**用户浏览器导出cookie → WSL内Playwright Chromium注入 → 服务器认为是同一用户**。

### 为什么有效

1. **服务器看到的是真实cookie**（z_c0、SESSIONID等认证token）
2. **反爬token在cookie里已存在**——不需要在请求时动态生成
3. **Playwright用的是真实Chromium**——TLS指纹与正常浏览器无差异
4. **运行在WSL本地**——没有跨系统网络隔离问题

### Cookie导出步骤（用户操作）

1. Chrome安装「EditThisCookie」插件
2. 打开目标站点（确保已登录）
3. 点击插件图标 → Export
4. 保存JSON文件，放到共享目录

### Cookie格式转换（EditThisCookie → Playwright）

```python
raw = json.loads(COOKIE_SOURCE.read_text(encoding='utf-8'))
cookies = []
for c in raw:
    if "zhihu.com" not in c.get("domain", ""):
        continue
    same = c.get("sameSite", "Lax")
        .replace("unspecified", "Lax")
        .replace("no_restriction", "None")
    cookies.append({
        "name": c["name"], "value": c["value"],
        "domain": c["domain"], "path": c.get("path", "/"),
        "httpOnly": c.get("httpOnly", False),
        "secure": c.get("secure", False),
        "sameSite": same,
    })
```

⚠️ `sameSite` 必须精确映射（unspecified→Lax, no_restriction→None），否则报 `cookies[0].sameSite: expected one of (Strict|Lax|None)`。

## 前置条件

1. **用户cookie文件**：用户需在Chrome中安装EditThisCookie插件 → 登录知乎 → 导出cookie为JSON → 放到 `I:\\hermes\\input\\md\\知乎cookie.md`
2. **Playwright + Chromium**：`pip install playwright && python3 -m playwright install chromium`
3. **playwright-stealth**：`pip install playwright-stealth`

## 四阶段抓取方法论

### 穿甲（MVP）：打通第一篇文章
- Playwright + Cookie注入 → 直接访问知乎
- 不需要CDP跨系统（WSL2无法连Windows Chrome）
- 在WSL中本地运行Chromium（python3 -m playwright install chromium）
- 验收：成功抓取1篇知乎文章→markdown

### 隐身（反检测）：不被识别为自动化
- `playwright-stealth`注入，隐藏webdriver等痕迹
- 人类行为模拟：随机延迟(0.5-3s)、随机滚动(3-8次)、文章间间隔(3-10s)
- 关键：`Stealth().apply_stealth_sync(page)` — 注意导入是 `from playwright_stealth import Stealth`
- 验收：连续5篇不同文章成功，零CAPTCHA触发
- 详细实现见 `references/stealth-guide.md`

### 破盾（容灾）：多方案自动切换
- 方案A（主力）：Cookie+Stealth
- 方案B（缓存）：Wayback Machine + CachedView
- 方案C（转载搜索）：Bing搜索文章标题找转载
- 策略路由器：A失败→B自动接管→C兜底

### 透心（自适应）：系统自己进化
- 对策矩阵：5种已知反爬模式
- 自适应引擎：失败→诊断→匹配对策→更新成功率

## 认证态发布（知乎文章自动发表）

透心不仅能抓取，还能**发布**到知乎。基于同一套 Cookie 注入 + Stealth 基础设施，实现全自动发布。

### 页面结构（2026-05-16确认）

```
写文章页: https://zhuanlan.zhihu.com/write
├── 标题: TEXTAREA[placeholder="请输入标题"]
├── 正文: DIV.public-DraftEditor-content[contenteditable] (Draft.js编辑器)
├── 发布按钮: button "发布设置" (下拉按钮)
│   └── 菜单项: "发布文章"
└── 二次确认: "确认发布" 弹窗按钮
```

### Draft.js 核心技法

**不能**用 innerHTML 或 execCommand('insertHTML')——Draft.js 接管了自己的状态管理，DOM修改会被覆盖。

**唯一可靠方式：Clipboard API 写入 HTML → Ctrl+V 粘贴。**

```python
# 关键：browser context 需要 clipboard 权限
context = browser.new_context(
    permissions=["clipboard-write", "clipboard-read"],
)

# page.evaluate 传多个值用对象，不能用多个位置参数
result = page.evaluate("""(data) => {
    const {html, text} = data;
    const htmlBlob = new Blob([html], {type: 'text/html'});
    const textBlob = new Blob([text], {type: 'text/plain'});
    const item = new ClipboardItem({'text/html': htmlBlob, 'text/plain': textBlob});
    return navigator.clipboard.write([item])
        .then(() => 'ok').catch(e => 'err:' + e.message);
}""", {"html": html_content, "text": plain_text})

# 聚焦编辑器 + Ctrl+V
page.keyboard.press("Control+v")
time.sleep(5)  # 等Draft.js解析
```

### 发布流水线

```
1. Cookie注入 → 免扫码登录
2. 验证登录（page.url不含signin/login）
3. 打开 https://zhuanlan.zhihu.com/write
4. page.fill("textarea[placeholder*='标题']", TITLE)
5. 聚焦编辑器 → Clipboard写入HTML+纯文本 → Ctrl+V → 等5秒
6. page.get_by_role("button", name="发布设置").click()
7. page.get_by_text("发布文章", exact=True).click()
8. 二次确认："确认发布"
9. 检查 URL —— 不含 "write" 则发布成功
```

### 发布流水线验证标准

- 编辑器内容长度 > 100 字符才执行发布步骤
- 发布后 page.url 不含 "write" 才算成功
- 成功时输出文章 URL（格式：https://zhuanlan.zhihu.com/p/{数字ID}）

### 已知陷阱

| 陷阱 | 表现 | 解决 |
|------|------|------|
| Clipboard写入headless失败 | clipboard_err | context加 permissions=["clipboard-write"] |
| Draft.js清空后再粘贴 | 粘贴不进去 | 不要预先clear innerHTML，直接Ctrl+V覆盖 |
| 两个"发布"按钮 | strict mode violation | 用exact=True，区分"发布设置"vs"发布" |
| headless=True等人 | 看不到浏览器 | 全自动流程，不设wait_for_timeout等人 |
| 文章太长keyboard type | 超时 | 用Clipboard paste替代 |
| sameSite格式错误 | expected one of (Strict\|Lax\|None) | 确保映射了no_restriction→None |

完整实现在 `scripts/publish_zhihu.py`，深度细节在 `references/zhihu-publishing.md`。

## 关键技术细节

### Playwright Chromium在WSL
```python
browser = p.chromium.launch(headless=True, args=[
    '--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
    '--disable-setuid-sandbox','--no-first-run','--no-zygote'
])
```

### 知乎内容选择器

**专栏文章** (zhuanlan.zhihu.com/p/...):
```python
selectors = [".RichText", ".Post-RichText", "article", ".css-376mun"]
```

**回答页面** (zhihu.com/question/.../answer/...):
```python
selectors = [".AnswerCard .RichContent", ".RichContent", ".AnswerItem-content"]
```
⚠️ 专栏和回答的HTML结构不同——用错选择器拿不到内容。详见 `references/zhihu-answer-page-selectors.md`。

### 反检测最佳实践
- User-Agent用Chrome 120 Windows
- viewport设置1280x800
- locale设为zh-CN

## 已部署脚本

| 脚本 | 用途 |
|------|------|
| `izu/touxin.py` | 日常单篇抓取 |
| `izu/touxin_shield.py` | 带A→B→C容灾 |
| `izu/touxin_adaptive.py` | 自适应演进+对策矩阵 |
| `scripts/publish_zhihu.py` | 知乎文章自动发布 |

## 用户标注规则

发知乎链接时可加标注控制分析深度：
- **"极大"** → 四子合议全上
- **"大"** → 军师深度评论
- **无标注** → 军师简要分析+入库

## 关联参考

- `references/zhihu-publishing.md` — 发布流水线深度细节
- `references/stealth-guide.md` — 反检测最佳实践
- `references/zhihu-answer-page-selectors.md` — 回答页选择器
- `references/countermeasure-matrix.md` — 反爬对策矩阵
