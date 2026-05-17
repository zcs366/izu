#!/usr/bin/env python3
"""
透心 v2 · 隐身版
- playwright-stealth 反检测
- 人类行为模拟（随机延迟、滚动、鼠标）
- 批量抓取 + 特征记录
"""
import json, time, os, random, re
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

COOKIE_FILE = "/mnt/i/hermes/input/md/知乎cookie.md"
OUTPUT_DIR = "/mnt/i/hermes/output/doc"
LOG_FILE = "/mnt/i/hermes/data/touxin-stealth-log.json"

# 测试文章列表（不同主题，验证通用性）
TEST_ARTICLES = [
    "https://zhuanlan.zhihu.com/p/2036102958136419687",  # 2080Ti部署Qwen
    "https://zhuanlan.zhihu.com/p/1990404048021652655",  # 2026 AI Agent学习计划
    "https://zhuanlan.zhihu.com/p/2026621357476127133",  # Agent基础设施层竞争
    "https://zhuanlan.zhihu.com/p/2017558472355496387",  # 企业级Agent选型指南
    "https://zhuanlan.zhihu.com/p/2010437035492664715",  # Agent工程化元年
]

def human_delay(min_s=0.5, max_s=2.0):
    """随机等待，模拟人类阅读速度"""
    time.sleep(random.uniform(min_s, max_s))

def human_scroll(page):
    """随机滚动，模拟人类浏览行为"""
    for _ in range(random.randint(3, 8)):
        scroll_amount = random.randint(200, 600)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.3, 1.2))
    # 回到顶部
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)

def extract_content(page) -> dict:
    """提取文章内容"""
    try:
        title = page.title()
        # 知乎标题格式："文章标题 - 知乎"，截取
        title = title.replace(" - 知乎", "").strip()
    except:
        title = "未知标题"
    
    # 主选择器
    selectors = [
        ".RichText",
        ".Post-RichText", 
        "article",
        ".ArticleItem-content",
        ".css-376mun"
    ]
    
    content = ""
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el:
                content = el.inner_text()
                if len(content) > 100:
                    break
        except:
            continue
    
    if not content or len(content) < 100:
        content = page.locator("body").inner_text()[:8000]
    
    return {"title": title, "content": content, "length": len(content)}

def fetch_article(page, url: str) -> dict:
    """抓取单篇文章"""
    print(f"  🌐 {url.split('/')[-1][:20]}...")
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    human_delay(1.5, 3.0)
    
    # 检查是否被拦截
    if "验证" in page.title() or "captcha" in page.url.lower():
        return {"success": False, "error": "CAPTCHA触发", "url": url}
    
    # 模拟人类浏览
    human_scroll(page)
    human_delay(0.5, 1.5)
    
    # 提取
    result = extract_content(page)
    result["success"] = len(result["content"]) > 200
    result["url"] = url
    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    return result

def main():
    # 加载cookie
    with open(COOKIE_FILE) as f:
        cookies_raw = json.load(f)
    
    cookies = []
    for c in cookies_raw:
        cookies.append({
            "name": c["name"], "value": c["value"],
            "domain": c["domain"], "path": c["path"],
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", False),
            "sameSite": c.get("sameSite", "Lax")
                .replace("unspecified", "Lax")
                .replace("no_restriction", "None")
        })
    
    log = {"version": "2.0-stealth", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "results": []}
    
    with sync_playwright() as p:
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
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="zh-CN"
        )
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # 注入stealth
        s = Stealth()
        s.apply_stealth_sync(page)
        
        print(f"🕶 透心 v2 · 隐身模式")
        print(f"   Cookie: {len(cookies)}条")
        print(f"   文章: {len(TEST_ARTICLES)}篇\n")
        
        success_count = 0
        for i, url in enumerate(TEST_ARTICLES):
            print(f"[{i+1}/{len(TEST_ARTICLES)}]", end=" ")
            try:
                result = fetch_article(page, url)
                log["results"].append(result)
                
                if result["success"]:
                    success_count += 1
                    # 保存文章
                    fname = re.sub(r'[^\w\-]', '_', result["title"][:40])
                    md_path = f"{OUTPUT_DIR}/zhihu-{fname}-{time.strftime('%Y%m%d-%H%M%S')}.md"
                    with open(md_path, 'w') as f:
                        f.write(f"# {result['title']}\n\n")
                        f.write(f"> 来源: {result['url']}\n")
                        f.write(f"> 抓取: {result['timestamp']}\n")
                        f.write(f"> 工具: 透心 v2 · 隐身模式\n\n")
                        f.write(result["content"])
                    print(f"  ✅ {result['length']}字 → {os.path.basename(md_path)}")
                else:
                    print(f"  ❌ {result.get('error', '内容过短')}")
                    
            except Exception as e:
                log["results"].append({"success": False, "url": url, "error": str(e)})
                print(f"  ❌ {type(e).__name__}: {e}")
            
            # 文章间随机间隔
            if i < len(TEST_ARTICLES) - 1:
                human_delay(3, 8)
        
        browser.close()
    
    # 写入日志
    log["summary"] = {
        "total": len(TEST_ARTICLES),
        "success": success_count,
        "rate": f"{success_count/len(TEST_ARTICLES)*100:.0f}%"
    }
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"🎯 隐身测试: {log['summary']['success']}/{log['summary']['total']} 成功 ({log['summary']['rate']})")
    print(f"📋 日志: {LOG_FILE}")

if __name__ == "__main__":
    main()
