# 知乎发布流水线深度参考

> 对应 `touxin` 技能的 "认证态发布" 章节。记录2026-05-16实战中踩过的坑和验证的方法。

## 页面结构（2026-05-16已验证）

```
写文章页: https://zhuanlan.zhihu.com/write
├── 标题: <TEXTAREA placeholder="请输入标题（最多 100 个字）">
├── 正文: <DIV class="notranslate public-DraftEditor-content" contenteditable="true">
│          (Draft.js驱动的React富文本编辑器)
├── 发布按钮: <button class="...">发布设置</button> (下拉菜单)
│   └── 菜单项: "发布文章" (点击后触发发布)
└── 二次确认弹窗: "确认发布" 按钮
```

## 发布脚本演化史

| 版本 | 策略 | 结果 |
|------|------|------|
| v0.1 | headless=False + keyboard.type | 需要显示桌面，WSL不可用 |
| v1.0 | headless=True + execCommand('insertHTML') | Draft.js不认，内容被清空 |
| v2.0 | innerHTML + input/compositionend事件 | Illegal invocation (textarea setter on div) |
| v3.0 | DataTransfer + ClipboardEvent('paste') | prevented=true，内容没进去 |
| v3.1 | Clipboard API write → Ctrl+V | 成功！14151字符填入Draft.js |
| v4.0 | 全流程自动发布 | 验证通过，发布到知乎 |

## Draft.js 内容注入——唯一可靠方式

**方案：Clipboard API 写入 HTML/纯文本 → Ctrl+V 粘贴**

### 为什么其他方案都失败

| 方案 | 失败原因 |
|------|---------|
| innerHTML = ... | Draft.js 监听自己的状态树，DOM直接修改会被render覆盖 |
| execCommand('insertHTML') | Draft.js 没有注册这个命令 |
| DataTransfer + paste event | headless Chromium 的 DataTransfer 在 eval 中行为异常 |
| keyboard.type(str) | 太慢（15000字符×delay=超时），且Draft.js可能合并事件 |

### Clipboard 方案的关键细节

**1. Browser Context 必须授权 clipboard 权限**
```python
context = browser.new_context(
    permissions=["clipboard-write", "clipboard-read"],
)
```

**2. page.evaluate 传多个值用对象，不是位置参数**
```python
# ❌ 错误
page.evaluate("(html, text) => {...}", html, text)
# TypeError: takes from 2 to 3 positional arguments but 4 were given

# ✅ 正确
page.evaluate("(data) => { const {html, text} = data; ...}", {"html": h, "text": t})
```

**3. 写入剪贴板后再粘贴**
```python
# 写入HTML + 纯文本（纯文本是fallback）
cb_result = page.evaluate("""(data) => {
    const {html, text} = data;
    const htmlBlob = new Blob([html], {type: 'text/html'});
    const textBlob = new Blob([text], {type: 'text/plain'});
    const item = new ClipboardItem({
        'text/html': htmlBlob,
        'text/plain': textBlob,
    });
    return navigator.clipboard.write([item])
        .then(() => 'ok').catch(e => 'err:' + e.message);
}""", {"html": html_content, "text": plain_text})

# 聚焦编辑器 + Ctrl+V
editor_loc = page.locator('[contenteditable="true"]')
editor_loc.click()
time.sleep(1)
page.keyboard.press("Control+v")
time.sleep(5)  # 等Draft.js解析完毕
```

## 发布按钮处理

注意事项：
- `button:has-text("发布")` 会匹配两个元素：`发布设置`(下拉按钮) 和 `发布`(实际按钮)
- 用 `get_by_role("button", name="发布设置").first` 做精确匹配
- 点击"发布设置"后，菜单出现，找 `get_by_text("发布文章", exact=True)`

```python
# 点击下拉按钮
page.get_by_role("button", name="发布设置").first.click()
time.sleep(1.5)

# 找菜单项
publish_item = page.get_by_text("发布文章", exact=True).first
if publish_item.is_visible(timeout=2000):
    publish_item.click()
    time.sleep(2)

# 二次确认
for confirm in ["确认发布", "发布", "确认"]:
    try:
        btn = page.get_by_role("button", name=confirm).first
        if btn.is_visible(timeout=1000):
            btn.click()
            break
    except:
        continue
```

## 内容校验

自动发布的前提是内容正确填充。发布前校验：

```python
editor_info = page.evaluate("""() => {
    const ed = document.querySelector('[contenteditable="true"]');
    if (!ed) return {error: "no_editor"};
    return {
        text_len: ed.textContent.length,
        text_preview: ed.textContent.slice(0, 100),
    };
}""")

if editor_info["text_len"] < 100:
    print("⚠️ 内容不足100字符，跳过发布")
else:
    # 执行发布
```

## Cookie 管理

- 来源：EditThisCookie 插件导出 → `I:\hermes\input\md\知乎cookie.md`
- 关键 cookie：`z_c0`(认证), `__zse_ck`(反爬), `_xsrf`(CSRF)
- `z_c0` 有效期约6个月（expirationDate）
- 首次验证后用 `context.cookies()` 缓存到 `~/.zhihu_cookies.json`
- sameSite 映射必须精确：`unspecified→Lax`, `no_restriction→None`

## 完整脚本

位于 `scripts/publish_zhihu.py`。调用方式：
```bash
cd /mnt/i/hermes && python3 scripts/publish_zhihu.py
```

执行流程：
1. 读取 cookie 并转换
2. Markdown → HTML 转换
3. 启动 headless Chromium
4. Cookie 注入 + Stealth 反检测
5. 登录验证 → 写文章页
6. page.fill 标题
7. Clipboard 写入 → Ctrl+V 粘贴正文
8. 内容校验
9. 点击发布 → 二次确认
10. 输出文章 URL
