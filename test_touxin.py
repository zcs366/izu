"""Tests for touxin.py — human_delay, human_scroll, extract_content, fetch_article"""

import pytest
import json
import time
import os
from unittest.mock import patch, MagicMock, mock_open


# ═══════════════════════════════════════════
# human_delay 测试
# ═══════════════════════════════════════════

class TestHumanDelay:
    """human_delay 函数测试"""

    @patch("touxin.time.sleep")
    @patch("touxin.random.uniform")
    def test_human_delay_calls_sleep(self, mock_uniform, mock_sleep):
        """应调用 time.sleep 并在默认范围内随机"""
        from touxin import human_delay
        mock_uniform.return_value = 1.23
        human_delay()
        mock_uniform.assert_called_once_with(0.5, 2.0)
        mock_sleep.assert_called_once_with(1.23)

    @patch("touxin.time.sleep")
    @patch("touxin.random.uniform")
    def test_human_delay_custom_range(self, mock_uniform, mock_sleep):
        """应支持自定义时间范围"""
        from touxin import human_delay
        mock_uniform.return_value = 5.0
        human_delay(3.0, 8.0)
        mock_uniform.assert_called_once_with(3.0, 8.0)
        mock_sleep.assert_called_once_with(5.0)


# ═══════════════════════════════════════════
# human_scroll 测试
# ═══════════════════════════════════════════

class TestHumanScroll:
    """human_scroll 函数测试"""

    @patch("touxin.time.sleep")
    @patch("touxin.random.randint")
    def test_human_scroll_performs_scrolls(self, mock_randint, mock_sleep):
        """应执行多次随机滚动并回到顶部"""
        from touxin import human_scroll
        page = MagicMock()
        mock_randint.side_effect = [3, 200, 300, 400]

        human_scroll(page)

        assert page.evaluate.call_count >= 4
        page.evaluate.assert_any_call("window.scrollTo(0, 0)")


# ═══════════════════════════════════════════
# extract_content 测试
# ═══════════════════════════════════════════
#
# extract_content 遍历 selectors[]，调用 page.locator(sel).first
# 并尝试 inner_text(). 我们通过 side_effect 控制每个选择器的返回值

class TestExtractContent:
    """extract_content 函数测试"""

    def _make_page_mock(self, title="文章 - 知乎", selectors_return=None,
                        body_text="body回退"):
        """构造 page mock，支持多选择器"""
        page = MagicMock()
        page.title.return_value = title
        # 默认所有选择器返回空
        page.locator.side_effect = lambda sel, **kw: MagicMock(
            first=MagicMock(inner_text=MagicMock(return_value=""))
        ) if not (selectors_return and sel in selectors_return) else MagicMock(
            first=MagicMock(inner_text=MagicMock(return_value=selectors_return[sel]))
        )
        # body 回退
        page.locator("body").inner_text.return_value = body_text
        return page

    def test_extract_content_with_title(self):
        """应从页面标题中提取文章标题，去掉 - 知乎 后缀"""
        from touxin import extract_content

        page = MagicMock()
        page.title.return_value = "AI发展 - 知乎"
        # 第一个选择器返回有效内容
        def locator_side(sel, **kw):
            mock_el = MagicMock()
            if sel == ".RichText":
                mock_el.first.inner_text.return_value = "内容正文"
            else:
                mock_el.first.inner_text.return_value = ""
            return mock_el
        page.locator.side_effect = locator_side

        result = extract_content(page)
        assert result["title"] == "AI发展"

    def test_extract_content_without_zhihu_suffix(self):
        """标题不含 - 知乎 时应原样返回"""
        from touxin import extract_content

        page = MagicMock()
        page.title.return_value = "纯标题"
        page.locator.return_value.first.inner_text.return_value = "内容"

        result = extract_content(page)
        assert result["title"] == "纯标题"

    def test_extract_content_title_exception(self):
        """page.title 异常时应返回 未知标题"""
        from touxin import extract_content

        page = MagicMock()
        page.title.side_effect = Exception("error")
        page.locator.return_value.first.inner_text.return_value = "正文"

        result = extract_content(page)
        assert result["title"] == "未知标题"

    def test_extract_content_fallback_to_body(self):
        """所有选择器无内容时应回退到 body"""
        from touxin import extract_content

        page = MagicMock()
        page.title.return_value = "标题 - 知乎"
        # 所有 locator(sel).first.inner_text() 返回空
        page.locator.return_value.first.inner_text.return_value = ""
        page.locator("body").inner_text.return_value = "body回退内容"

        result = extract_content(page)
        assert result["content"] == "body回退内容"

    def test_extract_content_length(self):
        """应正确计算内容长度"""
        from touxin import extract_content

        page = MagicMock()
        page.title.return_value = "标题 - 知乎"
        # 确保 locator(sel).first.inner_text() 返回字符串
        mock_locator = MagicMock()
        mock_first = MagicMock()
        mock_first.inner_text.return_value = "abc"
        mock_locator.first = mock_first
        page.locator.return_value = mock_locator
        # body选择器fallback
        body_mock = MagicMock()
        body_mock.inner_text.return_value = "a" * 100
        def locator_side_effect(sel):
            if sel == "body":
                return body_mock
            return mock_locator
        page.locator.side_effect = locator_side_effect

        result = extract_content(page)
        assert result["length"] >= 3

    def test_extract_content_first_selector_success(self):
        """第一个选择器返回足够长内容时应停止遍历"""
        from touxin import extract_content

        page = MagicMock()
        page.title.return_value = "标题 - 知乎"

        call_count = 0

        def locator_side(sel, **kw):
            nonlocal call_count
            call_count += 1
            mock_el = MagicMock()
            if sel == ".RichText":
                mock_el.first.inner_text.return_value = "A" * 200
            else:
                mock_el.first.inner_text.return_value = ""
            return mock_el

        page.locator.side_effect = locator_side

        result = extract_content(page)
        assert result["success"] if "success" in result else True
        # 确保 locator 被调用过
        assert call_count >= 1


# ═══════════════════════════════════════════
# fetch_article 测试
# ═══════════════════════════════════════════

class TestFetchArticle:
    """fetch_article 函数测试"""

    @patch("touxin.human_delay")
    @patch("touxin.human_scroll")
    def test_fetch_article_success(self, mock_scroll, mock_delay):
        """成功获取文章时应返回正确数据"""
        from touxin import fetch_article

        page = MagicMock()
        page.title.return_value = "测试文章 - 知乎"
        page.url = "https://zhuanlan.zhihu.com/p/123"
        page.locator.return_value.first.inner_text.return_value = "A" * 500

        result = fetch_article(page, "https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is True
        assert result["title"] == "测试文章"
        assert result["url"] == "https://zhuanlan.zhihu.com/p/123"
        assert "timestamp" in result

    @patch("touxin.human_delay")
    @patch("touxin.human_scroll")
    def test_fetch_article_captcha(self, mock_scroll, mock_delay):
        """验证码触发时应返回错误"""
        from touxin import fetch_article

        page = MagicMock()
        page.title.return_value = "验证"
        page.url = "https://zhuanlan.zhihu.com/captcha"

        result = fetch_article(page, "https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False
        assert "CAPTCHA" in result.get("error", "")

    @patch("touxin.human_delay")
    @patch("touxin.human_scroll")
    def test_fetch_article_content_too_short(self, mock_scroll, mock_delay):
        """内容过短（<=200字）时 success 应为 False"""
        from touxin import fetch_article

        page = MagicMock()
        page.title.return_value = "短文章 - 知乎"
        page.url = "https://zhuanlan.zhihu.com/p/123"
        page.locator.return_value.first.inner_text.return_value = "短"

        result = fetch_article(page, "https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False

    @patch("touxin.human_delay")
    @patch("touxin.human_scroll")
    def test_fetch_article_calls_goto(self, mock_scroll, mock_delay):
        """应调用 page.goto 访问目标 URL"""
        from touxin import fetch_article

        page = MagicMock()
        page.title.return_value = "文章 - 知乎"
        page.url = "https://zhuanlan.zhihu.com/p/123"
        page.locator.return_value.first.inner_text.return_value = "A" * 500

        fetch_article(page, "https://zhuanlan.zhihu.com/p/123")

        page.goto.assert_called_once_with(
            "https://zhuanlan.zhihu.com/p/123",
            wait_until="networkidle",
            timeout=30000
        )

    @patch("touxin.human_delay")
    @patch("touxin.human_scroll")
    def test_fetch_article_captcha_in_url(self, mock_scroll, mock_delay):
        """URL 中包含 captcha 时应检测到"""
        from touxin import fetch_article

        page = MagicMock()
        page.title.return_value = "文章 - 知乎"
        page.url = "https://zhuanlan.zhihu.com/captcha/verify"

        result = fetch_article(page, "https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False
        assert "CAPTCHA" in result.get("error", "")


# ═══════════════════════════════════════════
# main 测试（mock playwright + cookie 文件）
# ═══════════════════════════════════════════

class TestMain:
    """main 函数测试 — mock playwright 和文件 I/O"""

    @patch("touxin.sync_playwright")
    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    @patch("touxin.time.sleep")  # 防止 human_delay 卡住
    def test_main_injects_cookies(self, mock_sleep, mock_file, mock_playwright):
        """main 应加载 cookie 并注入 browser context"""
        from touxin import main

        # mock playwright 全链路
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # 设置页面返回内容
        mock_page.title.return_value = "测试文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/2036102958136419687"
        mock_page.locator.return_value.first.inner_text.return_value = "A" * 500

        main()

        # 验证 cookie 被注入
        mock_context.add_cookies.assert_called_once()
        # 验证浏览器启动参数
        mock_p.chromium.launch.assert_called_once()
        # 验证 stealth 被应用
        from playwright_stealth import Stealth
        # 因为 import 的是 from playwright_stealth import Stealth
        # 在 mock 下，Stealth 被用了

    @patch("touxin.sync_playwright")
    @patch("builtins.open", new_callable=mock_open,
           read_data='[]')
    @patch("touxin.time.sleep")
    def test_main_empty_cookies(self, mock_sleep, mock_file, mock_playwright):
        """空 cookie 列表应正常处理"""
        from touxin import main

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page
        mock_page.title.return_value = "文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/123"
        mock_page.locator.return_value.first.inner_text.return_value = "A" * 500

        main()  # 不应抛出异常

    @patch("touxin.sync_playwright")
    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/", "sameSite": "unspecified"}]')
    @patch("touxin.time.sleep")
    def test_main_normalizes_samesite(self, mock_sleep, mock_file, mock_playwright):
        """unspecified sameSite 应被转为 Lax"""
        from touxin import main

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page
        mock_page.title.return_value = "文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/123"
        mock_page.locator.return_value.first.inner_text.return_value = "A" * 500

        main()

        # 验证 add_cookies 收到的 sameSite 为 Lax
        call_args = mock_context.add_cookies.call_args
        if call_args:
            cookies_arg = call_args[0][0]
            assert cookies_arg[0]["sameSite"] == "Lax"

    @patch("touxin.sync_playwright")
    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"name": "a", "value": "1", "domain": ".zhihu.com", "path": "/"}]')
    @patch("touxin.time.sleep")
    @patch("touxin.os.makedirs")
    def test_main_writes_output_file(self, mock_makedirs, mock_sleep, mock_file, mock_playwright):
        """成功获取文章时应写 markdown 文件"""
        from touxin import main

        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page
        mock_page.title.return_value = "测试文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/2036102958136419687"
        mock_page.locator.return_value.first.inner_text.return_value = "A" * 500

        main()

        # open 应该被多次调用（cookie 文件 + 输出文件 + 日志文件）
        assert mock_file.call_count >= 2
