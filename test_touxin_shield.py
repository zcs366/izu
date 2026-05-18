"""Tests for touxin_shield.py — fetch_via_stealth, fetch_via_cache, fetch_via_repost, shield_fetch, load_failure_db, record_failure"""

import pytest
import json
import os
import time
from unittest.mock import patch, MagicMock, mock_open


# ═══════════════════════════════════════════
# fetch_via_stealth 测试
# ═══════════════════════════════════════════

class TestFetchViaStealth:
    """fetch_via_stealth 测试 — mock playwright"""

    @patch("touxin_shield.sync_playwright")
    @patch("touxin_shield.Stealth")
    @patch("touxin_shield.time.sleep")
    @patch("touxin_shield.random.uniform")
    def test_stealth_success(self, mock_uniform, mock_sleep, mock_stealth_cls, mock_playwright):
        """主力方案成功获取内容"""
        from touxin_shield import fetch_via_stealth

        mock_page = MagicMock()
        mock_page.title.return_value = "测试文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/123"
        locator = MagicMock()
        locator.inner_text.return_value = "正文内容" * 60
        mock_page.locator.return_value.first = locator

        mock_ctx = MagicMock()
        mock_ctx.new_page.return_value = mock_page
        mock_browser = MagicMock()
        mock_browser.new_context.return_value = mock_ctx
        mock_p = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_p

        result = fetch_via_stealth("https://zhuanlan.zhihu.com/p/123", [])

        assert result["success"] is True
        assert result["method"] == "stealth"
        assert result["title"] == "测试文章"

    @patch("touxin_shield.sync_playwright")
    @patch("touxin_shield.Stealth")
    @patch("touxin_shield.time.sleep")
    @patch("touxin_shield.random.uniform")
    def test_stealth_captcha(self, mock_uniform, mock_sleep, mock_stealth_cls, mock_playwright):
        """遇到验证码时应返回 CAPTCHA 错误"""
        from touxin_shield import fetch_via_stealth

        mock_page = MagicMock()
        mock_page.title.return_value = "验证"
        mock_page.url = "https://zhuanlan.zhihu.com/captcha"

        mock_ctx = MagicMock()
        mock_ctx.new_page.return_value = mock_page
        mock_browser = MagicMock()
        mock_browser.new_context.return_value = mock_ctx
        mock_p = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_p

        result = fetch_via_stealth("https://zhuanlan.zhihu.com/p/123", [])

        assert result["success"] is False
        assert result["error"] == "CAPTCHA"

    @patch("touxin_shield.sync_playwright")
    @patch("touxin_shield.Stealth")
    @patch("touxin_shield.time.sleep")
    @patch("touxin_shield.random.uniform")
    def test_stealth_content_too_short(self, mock_uniform, mock_sleep, mock_stealth_cls, mock_playwright):
        """内容过短时应返回错误"""
        from touxin_shield import fetch_via_stealth

        mock_page = MagicMock()
        mock_page.title.return_value = "短文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/123"
        locator = MagicMock()
        locator.inner_text.return_value = "短"
        mock_page.locator.return_value.first = locator

        mock_ctx = MagicMock()
        mock_ctx.new_page.return_value = mock_page
        mock_browser = MagicMock()
        mock_browser.new_context.return_value = mock_ctx
        mock_p = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_p

        result = fetch_via_stealth("https://zhuanlan.zhihu.com/p/123", [])

        assert result["success"] is False
        assert "内容过短" in result["error"]

    @patch("touxin_shield.sync_playwright")
    @patch("touxin_shield.Stealth")
    @patch("touxin_shield.time.sleep")
    @patch("touxin_shield.random.uniform")
    def test_stealth_fallback_to_body(self, mock_uniform, mock_sleep, mock_stealth_cls, mock_playwright):
        """选择器异常时应回退到 body 内容"""
        from touxin_shield import fetch_via_stealth

        mock_page = MagicMock()
        mock_page.title.return_value = "文章 - 知乎"
        mock_page.url = "https://zhuanlan.zhihu.com/p/123"

        # 第一个 locator 调用（.RichText,...）抛异常
        # page.locator("body") 应正常返回
        def locator_side(sel, **kw):
            if sel == ".RichText, .Post-RichText, article":
                raise Exception("not found")
            mock_loc = MagicMock()
            mock_loc.inner_text.return_value = "body回退" * 100
            return mock_loc
        mock_page.locator.side_effect = locator_side

        mock_ctx = MagicMock()
        mock_ctx.new_page.return_value = mock_page
        mock_browser = MagicMock()
        mock_browser.new_context.return_value = mock_ctx
        mock_p = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_p

        result = fetch_via_stealth("https://zhuanlan.zhihu.com/p/123", [])

        assert result["success"] is True
        assert "body回退" in result["content"]


# ═══════════════════════════════════════════
# fetch_via_cache 测试
# ═══════════════════════════════════════════

class TestFetchViaCache:
    """fetch_via_cache 测试 — mock subprocess"""

    @patch("touxin_shield.subprocess.run")
    def test_cache_cachedview_success(self, mock_run):
        """CachedView 返回有效内容"""
        from touxin_shield import fetch_via_cache

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "<html>" + "A" * 2000 + "</html>"
        mock_run.return_value = mock_result

        result = fetch_via_cache("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is True
        assert result["method"] == "cachedview"

    @patch("touxin_shield.subprocess.run")
    def test_cache_wayback_success(self, mock_run):
        """CachedView 失败但 Wayback 成功"""
        from touxin_shield import fetch_via_cache

        # 第一次失败（CachedView）
        fail_result = MagicMock()
        fail_result.returncode = 1
        fail_result.stdout = ""

        # 第二次成功（Wayback）
        ok_result = MagicMock()
        ok_result.returncode = 0
        ok_result.stdout = "<html>" + "B" * 3000 + "</html>"

        mock_run.side_effect = [fail_result, ok_result]

        result = fetch_via_cache("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is True
        assert result["method"] == "wayback"

    @patch("touxin_shield.subprocess.run")
    def test_cache_all_fail(self, mock_run):
        """所有缓存源都失败"""
        from touxin_shield import fetch_via_cache

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        result = fetch_via_cache("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False
        assert "所有缓存源不可用" in result["error"]

    @patch("touxin_shield.subprocess.run")
    def test_cache_exception_handling(self, mock_run):
        """subprocess 异常时应优雅跳过"""
        from touxin_shield import fetch_via_cache

        mock_run.side_effect = Exception("network error")

        result = fetch_via_cache("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False


# ═══════════════════════════════════════════
# fetch_via_repost 测试
# ═══════════════════════════════════════════

class TestFetchViaRepost:
    """fetch_via_repost 测试 — mock subprocess"""

    @patch("touxin_shield.subprocess.run")
    def test_repost_no_title(self, mock_run):
        """无法获取标题时应返回错误"""
        from touxin_shield import fetch_via_repost

        mock_result = MagicMock()
        mock_result.stdout = "<html>no title</html>"
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = fetch_via_repost("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False
        assert "无法获取标题" in result["error"]

    @patch("touxin_shield.subprocess.run")
    def test_repost_title_but_no_repost(self, mock_run):
        """有标题但找不到转载"""
        from touxin_shield import fetch_via_repost

        # 第一次：获取标题
        title_result = MagicMock()
        title_result.stdout = "<html><title>测试文章 - 知乎</title></html>"
        title_result.returncode = 0

        # 第二次：Bing搜索
        search_result = MagicMock()
        search_result.stdout = '<html><a href="https://bing.com">Bing</a></html>'
        search_result.returncode = 0

        mock_run.side_effect = [title_result, search_result]

        result = fetch_via_repost("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False
        assert "未找到转载" in result["error"]

    @patch("touxin_shield.subprocess.run")
    def test_repost_found(self, mock_run):
        """找到转载内容"""
        from touxin_shield import fetch_via_repost

        # 第一次：获取标题
        title_result = MagicMock()
        title_result.stdout = "<html><title>测试文章 - 知乎</title></html>"
        title_result.returncode = 0

        # 第二次：Bing搜索
        search_result = MagicMock()
        search_result.stdout = '<html><a href="https://example.com/repost">转载页面</a></html>'
        search_result.returncode = 0

        # 第三次：获取转载页
        repost_result = MagicMock()
        repost_result.stdout = "<html>" + "转载内容" * 200 + "</html>"
        repost_result.returncode = 0

        mock_run.side_effect = [title_result, search_result, repost_result]

        result = fetch_via_repost("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is True
        assert result["method"] == "repost_search"

    @patch("touxin_shield.subprocess.run")
    def test_repost_skip_zhihu_and_bing(self, mock_run):
        """转载搜索应跳过知乎和必应自身链接"""
        from touxin_shield import fetch_via_repost

        title_result = MagicMock()
        title_result.stdout = "<html><title>测试文章 - 知乎</title></html>"
        title_result.returncode = 0

        search_result = MagicMock()
        # 只有知乎和必应链接
        search_result.stdout = '<html><a href="https://zhihu.com/article">知乎</a><a href="https://bing.com">必应</a></html>'
        search_result.returncode = 0

        mock_run.side_effect = [title_result, search_result]

        result = fetch_via_repost("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False

    @patch("touxin_shield.subprocess.run")
    def test_repost_exception(self, mock_run):
        """异常时应优雅返回错误"""
        from touxin_shield import fetch_via_repost

        mock_run.side_effect = Exception("network error")

        result = fetch_via_repost("https://zhuanlan.zhihu.com/p/123")

        assert result["success"] is False


# ═══════════════════════════════════════════
# load_failure_db 测试
# ═══════════════════════════════════════════

class TestLoadFailureDb:
    """load_failure_db 测试"""

    @patch("touxin_shield.os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"patterns": [], "total_failures": 5, "last_updated": "2025-01-01"}')
    def test_load_existing_db(self, mock_file, mock_exists):
        """文件存在时应加载并返回内容"""
        from touxin_shield import load_failure_db

        mock_exists.return_value = True
        db = load_failure_db()

        assert db["total_failures"] == 5
        assert db["last_updated"] == "2025-01-01"

    @patch("touxin_shield.os.path.exists")
    def test_load_missing_db(self, mock_exists):
        """文件不存在时应返回默认结构"""
        from touxin_shield import load_failure_db

        mock_exists.return_value = False
        db = load_failure_db()

        assert db == {"patterns": [], "total_failures": 0, "last_updated": ""}

    @patch("touxin_shield.os.path.exists")
    def test_load_returns_new_dict_each_time(self, mock_exists):
        """多次调用应返回独立字典"""
        from touxin_shield import load_failure_db

        mock_exists.return_value = False
        db1 = load_failure_db()
        db2 = load_failure_db()

        assert db1 is not db2


# ═══════════════════════════════════════════
# record_failure 测试
# ═══════════════════════════════════════════

class TestRecordFailure:
    """record_failure 测试"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_increment_counter(self, mock_dump, mock_file):
        """应增加总失败计数"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "CAPTCHA", "https://zhuanlan.zhihu.com/p/123")

        assert db["total_failures"] == 1
        assert db["last_updated"] != ""

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_pattern_captcha(self, mock_dump, mock_file):
        """CAPTCHA 错误应匹配 captcha_triggered"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "CAPTCHA", "https://zhuanlan.zhihu.com/p/123")

        assert db["patterns"][0]["pattern"] == "captcha_triggered"

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_pattern_timeout(self, mock_dump, mock_file):
        """timeout 错误应匹配 network_timeout"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "timeout after 30s", "https://zhuanlan.zhihu.com/p/123")

        assert db["patterns"][0]["pattern"] == "network_timeout"

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_pattern_content_short(self, mock_dump, mock_file):
        """内容过短应匹配 content_too_short"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "内容过短", "https://zhuanlan.zhihu.com/p/123")

        assert db["patterns"][0]["pattern"] == "content_too_short"

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_pattern_404(self, mock_dump, mock_file):
        """404 错误应匹配 page_not_found"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "404 not found", "https://zhuanlan.zhihu.com/p/123")

        assert db["patterns"][0]["pattern"] == "page_not_found"

    @patch("builtins.open", new_callable=mock_open)
    @patch("touxin_shield.json.dump")
    def test_record_pattern_unknown(self, mock_dump, mock_file):
        """未知错误应截取前30字符作为 pattern"""
        from touxin_shield import record_failure

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        record_failure(db, "stealth", "some random error message", "https://zhuanlan.zhihu.com/p/123")

        assert db["patterns"][0]["pattern"] == "some random error message"


# ═══════════════════════════════════════════
# shield_fetch 测试
# ═══════════════════════════════════════════

class TestShieldFetch:
    """shield_fetch 测试 — A→B→C 策略路由"""

    @patch("touxin_shield.fetch_via_stealth")
    @patch("touxin_shield.fetch_via_cache")
    @patch("touxin_shield.fetch_via_repost")
    def test_route_a_success(self, mock_repost, mock_cache, mock_stealth):
        """A方案成功应直接返回"""
        from touxin_shield import shield_fetch

        mock_stealth.return_value = {"success": True, "method": "stealth", "content": "正文", "length": 1000}

        result = shield_fetch("https://zhuanlan.zhihu.com/p/123", [], {"patterns": [], "total_failures": 0, "last_updated": ""})

        assert result["success"] is True
        assert result["method"] == "stealth"
        mock_cache.assert_not_called()
        mock_repost.assert_not_called()

    @patch("touxin_shield.fetch_via_stealth")
    @patch("touxin_shield.fetch_via_cache")
    @patch("touxin_shield.fetch_via_repost")
    @patch("touxin_shield.record_failure")
    def test_route_a_fail_b_success(self, mock_record, mock_repost, mock_cache, mock_stealth):
        """A失败B成功"""
        from touxin_shield import shield_fetch

        mock_stealth.return_value = {"success": False, "method": "stealth", "error": "CAPTCHA"}
        mock_cache.return_value = {"success": True, "method": "cachedview", "content": "缓存正文", "length": 2000}

        result = shield_fetch("https://zhuanlan.zhihu.com/p/123", [], {"patterns": [], "total_failures": 0, "last_updated": ""})

        assert result["success"] is True
        assert result["method"] == "cachedview"
        mock_repost.assert_not_called()

    @patch("touxin_shield.fetch_via_stealth")
    @patch("touxin_shield.fetch_via_cache")
    @patch("touxin_shield.fetch_via_repost")
    @patch("touxin_shield.record_failure")
    def test_route_a_b_fail_c_success(self, mock_record, mock_repost, mock_cache, mock_stealth):
        """A和B都失败，C成功"""
        from touxin_shield import shield_fetch

        mock_stealth.return_value = {"success": False, "method": "stealth", "error": "CAPTCHA"}
        mock_cache.return_value = {"success": False, "method": "cache", "error": "所有缓存源不可用"}
        mock_repost.return_value = {"success": True, "method": "repost_search", "content": "转载正文", "length": 3000}

        result = shield_fetch("https://zhuanlan.zhihu.com/p/123", [], {"patterns": [], "total_failures": 0, "last_updated": ""})

        assert result["success"] is True
        assert result["method"] == "repost_search"

    @patch("touxin_shield.fetch_via_stealth")
    @patch("touxin_shield.fetch_via_cache")
    @patch("touxin_shield.fetch_via_repost")
    @patch("touxin_shield.record_failure")
    def test_route_all_fail(self, mock_record, mock_repost, mock_cache, mock_stealth):
        """所有方案都失败"""
        from touxin_shield import shield_fetch

        mock_stealth.return_value = {"success": False, "method": "stealth", "error": "CAPTCHA"}
        mock_cache.return_value = {"success": False, "method": "cache", "error": "所有缓存源不可用"}
        mock_repost.return_value = {"success": False, "method": "repost", "error": "未找到转载"}

        result = shield_fetch("https://zhuanlan.zhihu.com/p/123", [], {"patterns": [], "total_failures": 0, "last_updated": ""})

        assert result["success"] is False
        assert "所有方案均失败" in result["error"]

    @patch("touxin_shield.fetch_via_stealth")
    @patch("touxin_shield.fetch_via_cache")
    @patch("touxin_shield.fetch_via_repost")
    @patch("touxin_shield.record_failure")
    def test_route_records_failure_on_a(self, mock_record, mock_repost, mock_cache, mock_stealth):
        """A方案失败时应记录失败特征"""
        from touxin_shield import shield_fetch

        mock_stealth.return_value = {"success": False, "method": "stealth", "error": "CAPTCHA"}
        mock_cache.return_value = {"success": True, "method": "cachedview", "content": "正文", "length": 2000}

        db = {"patterns": [], "total_failures": 0, "last_updated": ""}
        shield_fetch("https://zhuanlan.zhihu.com/p/123", [], db)

        # record_failure 应被调用（A方案失败）
        mock_record.assert_called()
