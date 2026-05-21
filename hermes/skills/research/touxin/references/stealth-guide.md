# 透心隐身 · Playwright-Stealth 实现指南

> 日期：2026-05-14  
> 来源：透心项目隐身阶段实战验证（5/5知乎文章，零CAPTCHA）

## 一、安装

```bash
pip install playwright-stealth
```

## 二、API 正确用法（踩坑记录）

```python
# ❌ 错误（常见误导）
from playwright_stealth import stealth_sync
stealth_sync(page)  # ImportError

# ❌ 错误
from playwright_stealth import stealth
stealth(page)  # TypeError: 'module' object is not callable

# ✅ 正确
from playwright_stealth import Stealth
s = Stealth()
s.apply_stealth_sync(page)
```

**关键**：`stealth`是模块，不是函数。需要实例化`Stealth`类。

## 三、完整集成示例

```python
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(...)
    context.add_cookies(cookies)
    
    page = context.new_page()
    
    # 注入stealth
    s = Stealth()
    s.apply_stealth_sync(page)
    
    page.goto(url, wait_until="networkidle")
    # ... 提取内容
```

## 四、人类行为模拟（配合stealth使用）

```python
import random, time

def human_delay(min_s=0.5, max_s=2.0):
    time.sleep(random.uniform(min_s, max_s))

def human_scroll(page):
    for _ in range(random.randint(3, 8)):
        scroll_amount = random.randint(200, 600)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.3, 1.2))
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
```

调用顺序：
1. `page.goto(url)` → 等 `networkidle`
2. `human_delay(1.5, 3.0)` → 模拟阅读停顿
3. `human_scroll(page)` → 模拟滚动浏览
4. `human_delay(0.5, 1.5)` → 再停一下
5. 提取内容

**多篇文章之间**：`human_delay(3, 8)` 间隔，模拟人类在不同文章间的切换时间。

## 五、WSL Chromium 稳定性参数

WSL无头Chromium容易出现EPIPE管道断裂。添加以下启动参数：

```python
browser = p.chromium.launch(
    headless=True,
    args=[
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-first-run',
        '--no-zygote',
    ]
)
```

## 六、实测数据

| 测试 | 结果 |
|------|:--:|
| 目标站点 | 知乎专栏 (zhuanlan.zhihu.com) |
| 文章数 | 5篇 |
| 成功率 | 100% |
| CAPTCHA触发 | 0次 |
| 总文字量 | 25,268字 |
| 请求间隔 | 3-8秒随机 |

## 七、与v1（无stealth）的区别

| | v1 简单版 | v2 隐身版 |
|------|:--:|:--:|
| Stealth注入 | ❌ | ✅ |
| 人类行为模拟 | ❌ | ✅ |
| 多篇间隔 | 无 | 3-8秒随机 |
| 浏览器稳定性参数 | 无 | 全套WSL参数 |
| 特征日志 | 无 | JSON记录每次结果 |
| 适用场景 | 偶尔抓1篇 | 批量抓取、自动化入库 |
