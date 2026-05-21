# 替代抓取工具参考

当 web_extract → curl_cffi → 终端curl → Puppeteer 全部失败时：

## Scrapling（2026-05 发现）
- **GitHub**: D4Vinci/Scrapling (477+ stars)
- **安装**: `pip install "scrapling[all]" && scrapling install --force`
- **三层架构**: Fetcher(HTTP) → StealthyFetcher(过Cloudflare Turnstile) → Spider(并发爬取)
- **CLI**: `scrapling extract stealthy-fetch URL file.md`
- **特点**: 自带Hermes Agent SKILL.md，API兼容Playwright风格
- **适用**: 内容采集、高风控网站、批量爬取

## CloakBrowser（2026-05 发现，5000+ stars）
- **GitHub**: CloakHQ/CloakBrowser
- **安装**: `pip install -U cloakbrowser`
- **核心**: 49个Chromium源码级C++补丁，30/30反爬测试全过
- **reCAPTCHA v3评分**: 0.9（超真人级）
- **特点**: 改Chromium内核，非JS注入，Playwright API兼容
- **适用**: 需要浏览器渲染的高风控场景
- **缺点**: 首次运行下载~200MB预编译Chromium

## wx-cli（2026-05 发现，2400+ stars）
- **GitHub**: jackwener/wx-cli
- **安装**: `npm install -g @jackwener/wx-cli` 或 curl一键安装
- **核心**: 读取本地WeChat数据库（Rust编写，单二进制）
- **关键命令**: `wx biz-articles --account "公众号名" --limit 50`
- **特点**: 复用本地微信登录态，无验证码无反爬
- **输出**: Markdown格式，可直接对接wiki
- **适用**: 微信公众号文章批量获取（个人研究用途）
- **风险**: 灰色地带，不适合商业大规模使用
