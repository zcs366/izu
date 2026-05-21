# 公众号发布工作流（个人订阅号 · 无API）

## 核心约束

- **個人订阅号没有发布 API**。`/cgi-bin/draft/add` 等接口需要服务号（服务号）的 AppID/Secret 授权。
- 与知乎等平台不同，公众号与微信登录账号绑定，不能复用知乎 Cookie + Playwright 方案。
- **必须手动** 或 **借助 Playwright 提取 QR 码后由用户扫码登录**。

## 完整工作流

### 阶段 0：内容准备（Agent 完成）
产出：标题 + 作者 + 正文 + 摘要 + 封面建议 + 原文链接

### 阶段 1：内容交付（Agent 完成）
通过 `send_message` 将完整内容发送到用户微信（home channel），格式为可直接复制粘贴的纯文本/HTML。

### 阶段 2：登录引导（Agent 辅助）
用户执行：打开 `https://mp.weixin.qq.com/` 扫码登录

**如果用户看不到二维码（浏览器插件屏蔽/缓存问题）：**
```python
from playwright.sync_api import sync_playwright
import time

def extract_wechat_qrcode(output_path="/tmp/login_qrcode.png"):
    """
    从 mp.weixin.qq.com 提取登录 QR 码，输出截图文件。
    返回路径，供 send_message 发送 MEDIA 到用户微信。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("https://mp.weixin.qq.com/")
        page.wait_for_timeout(5000)  # 等待 QR 码加载

        qr_box = page.eval_on_selector(
            ".login__type__container__scan__qrcode",
            "el => { const r = el.getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; }"
        )
        page.screenshot(
            path=output_path,
            clip={"x": qr_box["x"], "y": qr_box["y"], "width": qr_box["w"], "height": qr_box["h"]}
        )
        browser.close()
        return output_path
```

### 阶段 3：用户手动发布
告诉用户按以下步骤操作：

1. 左侧菜单 → **草稿箱** → **新建图文**
2. 填写字段：
   - **标题**：从交付内容复制
   - **作者**：张成市（或合作者名）
   - **正文**：从微信消息粘贴（支持 Markdown 格式）
   - **封面**：用户自选照片（孩子/活动相关）
   - **摘要**：已提供
3. 文末添加 **原文链接**（指向知乎或其他平台）
4. 预览 → 微调排版 → 发布

## 常见问题

### Q: 为什么不能像知乎那样自动发布？
因为公众号（个人订阅号）与知乎账号体系分离：知乎用手机号+Cookie登录，可通过 Playwright 绕开；公众号必须微信扫码验证，且无发布 API。

### Q: 出版内容已经在微信上，怎么贴？
用户打开电脑版微信（或手机微信传到电脑），在公众号编辑器中直接 Ctrl+V 粘贴即可。公众号编辑器支持富文本粘贴，基本保留格式。

### Q: 如果用户说"太长了，看不懂"？
在发完整文章的同时，先给三条核心步骤的摘要：
1. 打开 mp.weixin.qq.com → 扫码
2. 草稿箱 → 新建 → 贴进去
3. 预览 → 发布
