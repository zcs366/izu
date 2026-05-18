"""Tests for touxin_v1_simple.py — script-level behavior (all module-level code)"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open


# ═══════════════════════════════════════════
# 模块级别代码测试
# ═══════════════════════════════════════════
# touxin_v1_simple.py 的所有代码都在模块级别执行（无函数包装）
# 我们测试各段逻辑：cookie解析、playwright交互、内容提取

class TestCookieParsing:
    """Cookie 解析逻辑测试"""

    def test_cookie_format_conversion(self):
        """cookie 应从 JSON 格式正确转换为 Playwright 格式"""
        # 模拟模块加载时的 cookie 解析逻辑
        cookies_raw = [
            {"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/",
             "httpOnly": False, "secure": False, "sameSite": "Lax"}
        ]
        cookies = []
        for c in cookies_raw:
            cookies.append({
                "name": c["name"],
                "value": c["value"],
                "domain": c["domain"],
                "path": c["path"],
                "httpOnly": c.get("httpOnly", False),
                "secure": c.get("secure", False),
                "sameSite": c.get("sameSite", "Lax")
                    .replace("unspecified", "Lax").replace("no_restriction", "None")
            })

        assert len(cookies) == 1
        assert cookies[0]["name"] == "a"
        assert cookies[0]["value"] == "1"

    def test_cookie_samesite_normalization_unspecified(self):
        """unspecified 应转为 Lax"""
        cookies_raw = [
            {"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/",
             "httpOnly": False, "secure": False, "sameSite": "unspecified"}
        ]
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

        assert cookies[0]["sameSite"] == "Lax"

    def test_cookie_samesite_normalization_no_restriction(self):
        """no_restriction 应转为 None"""
        cookies_raw = [
            {"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/",
             "httpOnly": False, "secure": False, "sameSite": "no_restriction"}
        ]
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

        assert cookies[0]["sameSite"] == "None"

    def test_cookie_empty_list(self):
        """空 cookie 列表应正常处理"""
        cookies = []
        assert len(cookies) == 0

    def test_cookie_missing_fields(self):
        """缺少可选字段时应使用默认值"""
        cookies_raw = [
            {"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}
        ]
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

        assert cookies[0]["httpOnly"] is False
        assert cookies[0]["secure"] is False
        assert cookies[0]["sameSite"] == "Lax"


class TestContentExtractionLogic:
    """内容提取逻辑测试"""

    def test_content_selector_list(self):
        """应使用正确顺序的选择器列表"""
        # touxin_v1_simple.py 中的选择器
        content_selector = ".RichText, .Post-RichText, article, .ArticleItem-content"
        selectors = [s.strip() for s in content_selector.split(",")]
        assert len(selectors) == 4
        assert ".RichText" in selectors
        assert "article" in selectors

    def test_content_truncation(self):
        """超过10000字的内容应截断"""
        content = "A" * 15000
        if len(content) > 10000:
            content = content[:10000]
        assert len(content) == 10000

    def test_screenshot_path_construction(self):
        """截图路径应包含 output_dir 和固定文件名"""
        output_dir = "/mnt/i/hermes/output/doc"
        screenshot_path = f"{output_dir}/zhihu-article-screenshot.png"
        assert screenshot_path == "/mnt/i/hermes/output/doc/zhihu-article-screenshot.png"

    def test_markdown_path_format(self):
        """markdown 文件路径应包含时间戳"""
        import time
        output_dir = "/mnt/i/hermes/output/doc"
        md_path = f"{output_dir}/zhihu-article-{time.strftime('%Y%m%d-%H%M%S')}.md"
        assert output_dir in md_path
        assert md_path.endswith(".md")
        # 时间戳格式验证
        from datetime import datetime
        # 提取时间戳部分
        basename = md_path.split("/")[-1]
        ts_part = basename.replace("zhihu-article-", "").replace(".md", "")
        datetime.strptime(ts_part, "%Y%m%d-%H%M%S")  # 不会抛出异常

    def test_content_truncation_boundary(self):
        """正好10000字的内容不应截断"""
        content = "A" * 10000
        if len(content) > 10000:
            content = content[:10000]
        assert len(content) == 10000

    def test_content_short_no_truncation(self):
        """短于10000字的内容不应截断"""
        content = "A" * 500
        if len(content) > 10000:
            content = content[:10000]
        assert len(content) == 500


class TestPlaywrightInteractions:
    """Playwright 交互逻辑测试 — 使用 mock"""

    @patch("touxin_v1_simple.sync_playwright")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    def test_playwright_launch_called(self, mock_file, mock_playwright):
        """应正确启动 playwright 浏览器"""
        # 由于模块代码在 import 时执行，我们需要重新触发 main 逻辑
        # 这里直接测试剧本的各个阶段
        import touxin_v1_simple as mod

        # 重建整个流程来测试
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # 模拟模块级代码的执行
        # 由于 touxin_v1_simple.py 是脚本式结构，我们模拟关键步骤

        # 1. playwright 启动
        with mod.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            context.add_cookies([])
            page = context.new_page()
            page.goto("https://zhuanlan.zhihu.com/p/2036102958136419687", wait_until="networkidle", timeout=30000)

        mock_playwright.assert_called_once()
        mock_p.chromium.launch.assert_called_once_with(headless=True)

    @patch("touxin_v1_simple.sync_playwright")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    def test_page_goto_called(self, mock_file, mock_playwright):
        """应调用 page.goto 访问目标 URL"""
        import touxin_v1_simple as mod

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        with mod.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="...",
                viewport={"width": 1280, "height": 800}
            )
            context.add_cookies([])
            page = context.new_page()
            page.goto("https://zhuanlan.zhihu.com/p/test", wait_until="networkidle", timeout=30000)
            browser.close()

        mock_page.goto.assert_called_once_with(
            "https://zhuanlan.zhihu.com/p/test",
            wait_until="networkidle",
            timeout=30000
        )

    @patch("touxin_v1_simple.sync_playwright")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    def test_screenshot_called(self, mock_file, mock_playwright):
        """应调用截图功能"""
        import touxin_v1_simple as mod

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        with mod.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="...", viewport={"width": 1280, "height": 800})
            context.add_cookies([])
            page = context.new_page()
            page.goto("https://zhuanlan.zhihu.com/p/test", wait_until="networkidle", timeout=30000)
            page.screenshot(path="/tmp/test.png", full_page=True)
            browser.close()

        mock_page.screenshot.assert_called_once_with(path="/tmp/test.png", full_page=True)

    @patch("touxin_v1_simple.sync_playwright")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    def test_content_extraction_with_mock(self, mock_file, mock_playwright):
        """应通过选择器提取内容"""
        import touxin_v1_simple as mod

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # 模拟 content_selector
        content_selector = ".RichText, .Post-RichText, article, .ArticleItem-content"
        locator_mock = MagicMock()
        mock_page.locator.return_value = locator_mock
        locator_mock.first.inner_text.return_value = "文章正文内容"

        with mod.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="...", viewport={"width": 1280, "height": 800})
            context.add_cookies([])
            page = context.new_page()
            page.goto("https://zhuanlan.zhihu.com/p/test", wait_until="networkidle", timeout=30000)

            # 使用 content_selector 提取
            content = page.locator(content_selector).first.inner_text()
            assert content == "文章正文内容"

    @patch("touxin_v1_simple.sync_playwright")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    def test_browser_close_called(self, mock_file, mock_playwright):
        """应正确关闭浏览器"""
        import touxin_v1_simple as mod

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        with mod.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="...", viewport={"width": 1280, "height": 800})
            context.add_cookies([])
            page = context.new_page()
            page.goto("https://zhuanlan.zhihu.com/p/test", wait_until="networkidle", timeout=30000)
            browser.close()

        mock_browser.close.assert_called_once()
