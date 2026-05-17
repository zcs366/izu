#!/usr/bin/env python3
"""
透心 v4 · 透心版（自适应演进）
- 对策矩阵驱动：失败→匹配模式→自动尝试对策
- 成功率追踪：每次尝试更新对策成功率
- 知识积累：新失败模式自动入库
- 通用化迁移框架：支持多站点
"""
import json, time, os, random, re, sys
import subprocess
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# ── 配置 ──
COOKIE_FILE = "/mnt/i/hermes/input/md/知乎cookie.md"
OUTPUT_DIR = "/mnt/i/hermes/output/doc"
MATRIX_FILE = "/mnt/i/hermes/data/touxin-countermeasure-matrix.json"
FAILURE_DB = "/mnt/i/hermes/data/touxin-failure-patterns.json"
LOG_FILE = "/mnt/i/hermes/data/touxin-adaptive-log.json"

# ── 方案A：主力 Stealth ──
def stealth_fetch(url: str, cookies: list, extra_wait: int = 2, stealth_level: str = "default") -> dict:
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
        
        s = Stealth(
            navigator_webdriver=True,
            navigator_hardware_concurrency=True,
            navigator_plugins=True,
            webgl_vendor=True,
            **({"navigator_webdriver": stealth_level == "aggressive"} if stealth_level != "default" else {})
        )
        s.apply_stealth_sync(page)
        
        page.goto(url, wait_until="networkidle", timeout=25000)
        time.sleep(extra_wait + random.uniform(1, 3))
        
        # 模拟人类行为
        for _ in range(random.randint(4, 10)):
            page.evaluate(f"window.scrollBy(0, {random.randint(100, 500)})")
            time.sleep(random.uniform(0.2, 0.8))
        
        if "验证" in page.title() or "captcha" in page.url.lower():
            browser.close()
            return {"success": False, "error": "captcha", "title": page.title()}
        
        title = page.title().replace(" - 知乎", "").strip()
        try:
            content = page.locator(".RichText, .Post-RichText, article").first.inner_text()
        except:
            content = page.locator("body").inner_text()[:8000]
        
        browser.close()
        
        if len(content) > 200:
            return {"success": True, "title": title, "content": content, "length": len(content)}
        return {"success": False, "error": "content_too_short", "title": title}

# ── 方案B：缓存 ──
def cache_fetch(url: str) -> dict:
    for source, cmd in [
        ("wayback", ["curl", "-sL", "--connect-timeout", "10", f"https://web.archive.org/web/2025/{url}"]),
        ("cachedview", ["curl", "-sL", "--connect-timeout", "8", f"https://cachedview.com/share/{url}"]),
    ]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and len(result.stdout) > 1000:
                text = re.sub(r'<[^>]+>', ' ', result.stdout)
                text = re.sub(r'\s+', ' ', text)
                if len(text) > 500:
                    return {"success": True, "content": text[:10000], "length": len(text), "source": source}
        except:
            continue
    return {"success": False, "error": "all_cache_failed"}

# ── 方案C：转载搜索 ──
def repost_fetch(url: str) -> dict:
    try:
        r = subprocess.run(["curl", "-sL", "--connect-timeout", "8", url], capture_output=True, text=True, timeout=15)
        title_match = re.search(r'<title>(.*?)</title>', r.stdout or "")
        title = title_match.group(1).replace(" - 知乎", "").strip() if title_match else ""
    except:
        title = ""
    
    if not title or len(title) < 5:
        return {"success": False, "error": "no_title"}
    
    try:
        search_url = f"https://www.bing.com/search?q={title}"
        r = subprocess.run(["curl", "-sL", "--connect-timeout", "8", "-H", "User-Agent: Mozilla/5.0", search_url],
                          capture_output=True, text=True, timeout=15)
        links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', r.stdout or "")
        for href, t in links[:10]:
            if "zhihu.com" not in href and "bing.com" not in href and len(t) > 10:
                try:
                    r2 = subprocess.run(["curl", "-sL", "--connect-timeout", "5", href], capture_output=True, text=True, timeout=10)
                    clean = re.sub(r'<[^>]+>', ' ', r2.stdout or "")
                    clean = re.sub(r'\s+', ' ', clean)
                    if len(clean) > 500:
                        return {"success": True, "content": clean[:10000], "length": len(clean), "source": href}
                except:
                    continue
    except:
        pass
    return {"success": False, "error": "no_repost_found"}

# ── 失败模式诊断 ──
def diagnose_failure(error: str, page_title: str = "") -> str:
    if "captcha" in error.lower() or "验证" in error or "CAPTCHA" in error:
        return "captcha_triggered"
    if "content_too_short" in error or "内容过短" in error:
        return "content_too_short"
    if "timeout" in error.lower() or "超时" in error:
        return "network_timeout"
    if "login" in error.lower() or "登录" in error:
        return "login_required"
    if "空白" in error or (page_title and len(page_title) < 5):
        return "zse_ck_upgraded"
    return f"unknown:{error[:30]}"

# ── 对策矩阵引擎 ──
class AdaptiveEngine:
    def __init__(self, matrix_path: str):
        self.matrix_path = matrix_path
        self.matrix = self._load()
    
    def _load(self) -> dict:
        with open(self.matrix_path) as f:
            return json.load(f)
    
    def _save(self):
        with open(self.matrix_path, 'w') as f:
            json.dump(self.matrix, f, indent=2, ensure_ascii=False)
    
    def get_countermeasures(self, pattern_id: str) -> list:
        for p in self.matrix["patterns"]:
            if p["id"] == pattern_id:
                return sorted(p["countermeasures"], key=lambda x: -x["success_rate"])
        return []
    
    def try_countermeasure(self, cm_id: str, pattern_id: str, url: str, cookies: list) -> dict:
        """尝试单个对策"""
        if cm_id == "wait_longer":
            return stealth_fetch(url, cookies, extra_wait=8)
        elif cm_id == "scroll_more":
            return stealth_fetch(url, cookies, extra_wait=5)
        elif cm_id == "switch_selector":
            return stealth_fetch(url, cookies)
        elif cm_id == "fallback_cache":
            return cache_fetch(url)
        elif cm_id == "stealth_upgrade":
            return stealth_fetch(url, cookies, stealth_level="aggressive")
        elif cm_id == "retry_with_backoff":
            for delay in [2, 4, 8]:
                time.sleep(delay)
                result = stealth_fetch(url, cookies)
                if result["success"]:
                    return result
            return {"success": False, "error": "retry_exhausted"}
        elif cm_id == "delay_longer":
            return stealth_fetch(url, cookies, extra_wait=15)
        elif cm_id == "use_vision":
            # 截图AI识别（需要CDP或playwright截图+外部OCR）
            return {"success": False, "error": "vision_not_yet_implemented"}
        else:
            return {"success": False, "error": f"unknown_cm:{cm_id}"}
    
    def update_success_rate(self, pattern_id: str, cm_id: str, success: bool):
        for p in self.matrix["patterns"]:
            if p["id"] == pattern_id:
                for cm in p["countermeasures"]:
                    if cm["id"] == cm_id:
                        old_rate = cm["success_rate"]
                        cm["tried"] += 1
                        # 指数移动平均更新成功率
                        alpha = 0.3
                        cm["success_rate"] = old_rate * (1 - alpha) + (1.0 if success else 0.0) * alpha
                        break
        self._save()
    
    def ensure_pattern_exists(self, pattern_id: str, error_msg: str):
        """新失败模式自动入库"""
        for p in self.matrix["patterns"]:
            if p["id"] == pattern_id:
                return  # 已存在
        
        self.matrix["patterns"].append({
            "id": pattern_id,
            "name": pattern_id.replace("_", " ").title(),
            "signals": [error_msg[:100]],
            "countermeasures": [
                {"id": "fallback_cache", "action": "切换到缓存方案", "success_rate": 0.0, "tried": 0},
                {"id": "stealth_upgrade", "action": "升级stealth配置", "success_rate": 0.0, "tried": 0},
            ]
        })
        self._save()
        print(f"     📝 新模式入库: {pattern_id}")
    
    def adapt(self, url: str, cookies: list, error: str, page_title: str = "") -> dict:
        """自适应主循环：诊断→匹配→尝试→更新"""
        pattern_id = diagnose_failure(error, page_title)
        
        self.ensure_pattern_exists(pattern_id, error)
        
        countermeasures = self.get_countermeasures(pattern_id)
        
        if not countermeasures:
            print(f"     ⚠ 无可用对策 for {pattern_id}")
            return {"success": False, "error": "no_countermeasures", "pattern": pattern_id}
        
        print(f"     🔍 模式: {pattern_id} | 对策: {len(countermeasures)}个")
        
        for cm in countermeasures:
            cm_id = cm["id"]
            print(f"        ▶ {cm_id} (成功率: {cm['success_rate']:.0%})")
            
            result = self.try_countermeasure(cm_id, pattern_id, url, cookies)
            
            self.update_success_rate(pattern_id, cm_id, result["success"])
            
            if result["success"]:
                print(f"        ✅ {cm_id} 成功!")
                return result
            else:
                print(f"        ❌ {cm_id} 失败: {result.get('error','')}")
        
        return {"success": False, "error": "all_countermeasures_exhausted", "pattern": pattern_id}

# ── 通用化迁移 ──
def generic_fetch(url: str, site_name: str, cookies: list) -> dict:
    """多站点通用抓取框架"""
    site_configs = {
        "csdn": {"selectors": [".article_content", "#content_views", "article"], "domain": "blog.csdn.net"},
        "jianshu": {"selectors": [".show-content-free", "article", "._2rhmJa"], "domain": "jianshu.com"},
    }
    
    config = site_configs.get(site_name, {"selectors": ["article", "body"], "domain": ""})
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
            '--no-first-run','--no-zygote'
        ])
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            viewport={"width":1280,"height":800}, locale="zh-CN"
        )
        Stealth().apply_stealth_sync(ctx.new_page())
        page = ctx.new_page()
        Stealth().apply_stealth_sync(page)
        
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(random.uniform(2, 4))
        
        content = ""
        for sel in config["selectors"]:
            try:
                content = page.locator(sel).first.inner_text()
                if len(content) > 200:
                    break
            except:
                continue
        
        if not content:
            content = page.locator("body").inner_text()[:8000]
        
        browser.close()
        
        if len(content) > 200:
            return {"success": True, "content": content, "length": len(content), "site": site_name}
        return {"success": False, "error": "content_too_short", "site": site_name}

# ── 主流程 ──
def main():
    # 加载cookie
    with open(COOKIE_FILE) as f:
        cookies_raw = json.load(f)
    cookies = [{
        "name": c["name"], "value": c["value"],
        "domain": c["domain"], "path": c["path"],
        "httpOnly": c.get("httpOnly", False),
        "secure": c.get("secure", False),
        "sameSite": c.get("sameSite", "Lax").replace("unspecified","Lax").replace("no_restriction","None")
    } for c in cookies_raw]
    
    engine = AdaptiveEngine(MATRIX_FILE)
    
    # 测试：正常URL + 异常URL
    test_cases = [
        {"url": "https://zhuanlan.zhihu.com/p/2036102958136419687", "expect": "success"},
        {"url": "https://zhuanlan.zhihu.com/p/9999999999999999999", "expect": "fallback"},  # 无效
    ]
    
    print(f"♟ 透心 v4 · 自适应演进")
    print(f"   对策矩阵: {len(engine.matrix['patterns'])}种模式\n")
    
    log = {"version": "4.0-adaptive", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "results": []}
    
    for i, tc in enumerate(test_cases):
        url = tc["url"]
        print(f"[{i+1}/{len(test_cases)}] {url.split('/')[-1][:30]}...")
        
        # 先试主力方案
        result = stealth_fetch(url, cookies)
        
        if result["success"]:
            print(f"     ✅ 主力方案直接成功 ({result['length']}字)")
            log["results"].append({"url": url, "route": "primary", "success": True, "length": result["length"]})
        else:
            # 主力失败→自适应引擎接管
            error = result.get("error", "unknown")
            print(f"     ❌ 主力失败: {error}")
            adapted = engine.adapt(url, cookies, error, result.get("title", ""))
            log["results"].append({
                "url": url, "route": "adaptive", "success": adapted["success"],
                "pattern": adapted.get("pattern", ""),
                "length": adapted.get("length", 0)
            })
            
            if adapted["success"]:
                result = adapted
            else:
                print(f"     💀 自适应引擎全部对策耗尽")
        
        # 保存成功结果
        if result["success"]:
            title = result.get("title", "未知标题")
            fname = re.sub(r'[^\w\-]', '_', title[:40])
            md_path = f"{OUTPUT_DIR}/zhihu-adaptive-{fname}-{time.strftime('%Y%m%d-%H%M%S')}.md"
            with open(md_path, 'w') as f:
                f.write(f"# {title}\n\n")
                f.write(f"> 来源: {url}\n")
                f.write(f"> 抓取方案: 透心 v4 · 自适应\n")
                f.write(f"> 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(result["content"])
        
        if i < len(test_cases) - 1:
            time.sleep(random.uniform(3, 8))
    
    # 通用化迁移测试
    print(f"\n🌐 通用化迁移测试...")
    migration_test = {"url": "https://blog.csdn.net/weixin_123456789/article/details/12345678", "site": "csdn"}
    try:
        m_result = generic_fetch(migration_test["url"], migration_test["site"], cookies)
        print(f"     {migration_test['site']}: {'✅' if m_result['success'] else '❌'} {m_result.get('length',0)}字")
        log["migration"] = m_result
    except Exception as e:
        print(f"     ❌ 迁移测试异常: {e}")
        log["migration"] = {"success": False, "error": str(e)}
    
    # 保存日志
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    
    successes = sum(1 for r in log["results"] if r["success"])
    print(f"\n{'='*50}")
    print(f"♟ 透心自适应: {successes}/{len(test_cases)} 成功")
    print(f"📊 对策矩阵: {len(engine.matrix['patterns'])}种模式")
    for p in engine.matrix["patterns"]:
        cms = [(cm["id"], f"{cm['success_rate']:.0%}") for cm in p["countermeasures"]]
        print(f"   {p['id']}: {cms}")
    print(f"💾 矩阵: {MATRIX_FILE}")
    print(f"📋 日志: {LOG_FILE}")

if __name__ == "__main__":
    main()
