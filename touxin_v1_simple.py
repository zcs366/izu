#!/usr/bin/env python3
"""透心 · 穿甲脚本 v1 — Playwright + Cookie注入"""
import json, sys, time, os
from playwright.sync_api import sync_playwright

COOKIE_FILE = "/mnt/i/hermes/input/md/知乎cookie.md"
TARGET_URL = "https://zhuanlan.zhihu.com/p/2036102958136419687"
OUTPUT_DIR = "/mnt/i/hermes/output/doc"

# 1. 读取cookie
with open(COOKIE_FILE, 'r') as f:
    cookies_raw = json.load(f)

# 转为Playwright格式
cookies = []
for c in cookies_raw:
    cookies.append({
        "name": c["name"],
        "value": c["value"],
        "domain": c["domain"],
        "path": c["path"],
        "httpOnly": c.get("httpOnly", False),
        "secure": c.get("secure", False),
        "sameSite": c.get("sameSite", "Lax").replace("unspecified", "Lax").replace("no_restriction", "None")
    })

print(f"加载 {len(cookies)} 条cookie")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )
    
    # 注入cookie
    context.add_cookies(cookies)
    
    page = context.new_page()
    
    print(f"访问: {TARGET_URL}")
    page.goto(TARGET_URL, wait_until="networkidle", timeout=30000)
    
    # 等渲染
    time.sleep(3)
    
    # 截图
    screenshot_path = f"{OUTPUT_DIR}/zhihu-article-screenshot.png"
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"✅ 截图: {screenshot_path}")
    
    # 提取标题
    try:
        title = page.title()
        print(f"标题: {title}")
    except:
        title = "未知标题"
    
    # 提取正文
    content_selector = ".RichText, .Post-RichText, article, .ArticleItem-content"
    try:
        content = page.locator(content_selector).first.inner_text()
    except:
        # 备选：整个body文字
        content = page.locator("body").inner_text()
        # 截取（去掉导航等）
        if len(content) > 10000:
            content = content[:10000]
    
    # 保存markdown
    md_path = f"{OUTPUT_DIR}/zhihu-article-{time.strftime('%Y%m%d-%H%M%S')}.md"
    with open(md_path, 'w') as f:
        f.write(f"# {title}\n\n")
        f.write(f"> 来源: {TARGET_URL}\n")
        f.write(f"> 抓取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> 工具: 透心 v1 (Playwright + Cookie)\n\n")
        f.write(content)
    
    print(f"✅ 文章: {md_path}")
    print(f"字数: {len(content)}")
    
    browser.close()

print("\n🎯 透心穿甲完成！")
