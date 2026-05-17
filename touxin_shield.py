#!/usr/bin/env python3
"""
透心 v3 · 破盾版
- 策略路由器：A(Cookie+Stealth) → B(缓存镜像) → C(标题搜索转载)
- 失败特征记录器：结构化日志+模式识别
- 信号：无论哪条路，都要拿到内容
"""
import json, time, os, random, re, sys
import subprocess
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

COOKIE_FILE = "/mnt/i/hermes/input/md/知乎cookie.md"
OUTPUT_DIR = "/mnt/i/hermes/output/doc"
LOG_FILE = "/mnt/i/hermes/data/touxin-shield-log.json"
FAILURE_DB = "/mnt/i/hermes/data/touxin-failure-patterns.json"

# ── 方案A：主力 Cookie+Stealth ──
def fetch_via_stealth(url: str, cookies: list) -> dict:
    """Playwright + Cookie + Stealth"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
            '--disable-setuid-sandbox','--no-first-run','--no-zygote'
        ])
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            viewport={"width":1280,"height":800}, locale="zh-CN"
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        Stealth().apply_stealth_sync(page)
        
        page.goto(url, wait_until="networkidle", timeout=25000)
        time.sleep(random.uniform(2, 4))
        
        if "验证" in page.title() or "captcha" in page.url.lower():
            browser.close()
            return {"success": False, "method": "stealth", "error": "CAPTCHA"}
        
        title = page.title().replace(" - 知乎", "").strip()
        try:
            content = page.locator(".RichText, .Post-RichText, article").first.inner_text()
        except:
            content = page.locator("body").inner_text()[:8000]
        
        browser.close()
        
        if len(content) > 200:
            return {"success": True, "method": "stealth", "title": title, "content": content, "length": len(content)}
        return {"success": False, "method": "stealth", "error": "内容过短"}

# ── 方案B：缓存镜像 ──
def fetch_via_cache(url: str) -> dict:
    """CachedView + Wayback Machine"""
    # 尝试1: CachedView
    try:
        result = subprocess.run(
            ["curl", "-sL", "--connect-timeout", "8", f"https://cachedview.com/share/{url}"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and len(result.stdout) > 1000:
            text = re.sub(r'<[^>]+>', ' ', result.stdout)
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 500:
                return {"success": True, "method": "cachedview", "content": text[:10000], "length": len(text)}
    except:
        pass
    
    # 尝试2: Wayback Machine
    try:
        result = subprocess.run(
            ["curl", "-sL", "--connect-timeout", "10", f"https://web.archive.org/web/2025/{url}"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and len(result.stdout) > 2000:
            text = re.sub(r'<[^>]+>', ' ', result.stdout)
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 500:
                return {"success": True, "method": "wayback", "content": text[:10000], "length": len(text)}
    except:
        pass
    
    return {"success": False, "method": "cache", "error": "所有缓存源不可用"}

# ── 方案C：转载搜索 ──
def fetch_via_repost(url: str) -> dict:
    """搜索文章标题找转载"""
    # 先用curl快速获取标题
    try:
        result = subprocess.run(
            ["curl", "-sL", "--connect-timeout", "8", url],
            capture_output=True, text=True, timeout=15
        )
        title_match = re.search(r'<title>(.*?)</title>', result.stdout or "")
        title = title_match.group(1).replace(" - 知乎", "").strip() if title_match else ""
    except:
        title = ""
    
    if not title or len(title) < 5:
        return {"success": False, "method": "repost", "error": "无法获取标题"}
    
    # 搜索转载（用curl搜Bing）
    try:
        search_url = f"https://www.bing.com/search?q={title}"
        result = subprocess.run(
            ["curl", "-sL", "--connect-timeout", "8", "-H", "User-Agent: Mozilla/5.0", search_url],
            capture_output=True, text=True, timeout=15
        )
        # 找非知乎的结果链接
        links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', result.stdout or "")
        for href, text in links[:10]:
            if "zhihu.com" not in href and "bing.com" not in href and len(text) > 10:
                # 尝试获取转载页
                try:
                    r2 = subprocess.run(
                        ["curl", "-sL", "--connect-timeout", "5", href],
                        capture_output=True, text=True, timeout=10
                    )
                    clean = re.sub(r'<[^>]+>', ' ', r2.stdout or "")
                    clean = re.sub(r'\s+', ' ', clean)
                    if len(clean) > 500:
                        return {"success": True, "method": "repost_search", "content": clean[:10000], "length": len(clean), "source_url": href}
                except:
                    continue
    except:
        pass
    
    return {"success": False, "method": "repost", "error": "未找到转载"}

# ── 策略路由器 ──
def shield_fetch(url: str, cookies: list, failure_db: dict) -> dict:
    """多方案容灾：A→B→C"""
    
    print(f"  🛡 策略路由启动...")
    
    # 方案A：主力
    print(f"     ▶ A: Cookie+Stealth")
    result = fetch_via_stealth(url, cookies)
    if result["success"]:
        print(f"     ✅ A方案成功 ({result['length']}字)")
        return result
    
    failure = result.get("error", "未知")
    print(f"     ❌ A方案失败: {failure}")
    record_failure(failure_db, "stealth", failure, url)
    
    # 方案B：缓存
    print(f"     ▶ B: 缓存镜像")
    result = fetch_via_cache(url)
    if result["success"]:
        print(f"     ✅ B方案成功 ({result['length']}字) [{result['method']}]")
        return result
    
    failure = result.get("error", "未知")
    print(f"     ❌ B方案失败: {failure}")
    record_failure(failure_db, "cache", failure, url)
    
    # 方案C：转载搜索
    print(f"     ▶ C: 转载搜索")
    result = fetch_via_repost(url)
    if result["success"]:
        print(f"     ✅ C方案成功 ({result['length']}字) [{result.get('source_url','')}]")
        return result
    
    failure = result.get("error", "未知")
    print(f"     ❌ C方案失败: {failure}")
    record_failure(failure_db, "repost", failure, url)
    
    return {"success": False, "method": "all_failed", "error": "所有方案均失败"}

# ── 失败特征记录器 ──
def load_failure_db() -> dict:
    if os.path.exists(FAILURE_DB):
        with open(FAILURE_DB) as f:
            return json.load(f)
    return {"patterns": [], "total_failures": 0, "last_updated": ""}

def record_failure(db: dict, method: str, error: str, url: str):
    db["total_failures"] += 1
    db["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 模式匹配
    pattern = None
    if "CAPTCHA" in error or "验证" in error:
        pattern = "captcha_triggered"
    elif "timeout" in error.lower():
        pattern = "network_timeout"
    elif "内容过短" in error:
        pattern = "content_too_short"
    elif "404" in error or "not found" in error.lower():
        pattern = "page_not_found"
    else:
        pattern = error[:30]
    
    db["patterns"].append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "method": method, "pattern": pattern, "error": error,
        "url_short": url.split("/")[-1][:20]
    })
    
    with open(FAILURE_DB, 'w') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

# ── 主流程 ──
def main():
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
                .replace("unspecified", "Lax").replace("no_restriction", "None")
        })
    
    failure_db = load_failure_db()
    
    test_urls = [
        "https://zhuanlan.zhihu.com/p/2036102958136419687",  # 已验证
        "https://zhuanlan.zhihu.com/p/2026621357476127133",  # Agent基础设施
        "https://zhuanlan.zhihu.com/p/9999999999999999999",  # 故意无效URL，测容灾
    ]
    
    print(f"🛡 透心 v3 · 破盾模式")
    print(f"   Cookie: {len(cookies)}条 | 方案: A→B→C\n")
    
    shield_log = {"version": "3.0-shield", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "results": []}
    
    for i, url in enumerate(test_urls):
        print(f"[{i+1}/{len(test_urls)}] {url.split('/')[-1][:30]}...")
        result = shield_fetch(url, cookies, failure_db)
        shield_log["results"].append(result)
        
        if result["success"]:
            # 保存
            title = result.get("title", "未知标题")
            fname = re.sub(r'[^\w\-]', '_', title[:40])
            md_path = f"{OUTPUT_DIR}/zhihu-shield-{fname}-{time.strftime('%Y%m%d-%H%M%S')}.md"
            with open(md_path, 'w') as f:
                f.write(f"# {title}\n\n")
                f.write(f"> 来源: {url}\n")
                f.write(f"> 抓取方案: {result['method']}\n")
                f.write(f"> 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(result["content"])
        else:
            print(f"     💀 全部失败")
        
        if i < len(test_urls) - 1:
            time.sleep(random.uniform(4, 10))
    
    with open(LOG_FILE, 'w') as f:
        json.dump(shield_log, f, indent=2, ensure_ascii=False)
    
    successes = sum(1 for r in shield_log["results"] if r["success"])
    print(f"\n{'='*50}")
    print(f"🛡 破盾测试: {successes}/{len(test_urls)} 成功")
    print(f"📋 失败记录: {failure_db['total_failures']}条 | 模式: {len(failure_db['patterns'])}种")
    print(f"💾 日志: {LOG_FILE} | {FAILURE_DB}")

if __name__ == "__main__":
    main()
