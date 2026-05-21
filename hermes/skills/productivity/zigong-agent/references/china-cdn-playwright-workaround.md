# 中国网络环境·Playwright安装指南

## 问题

`playwright install chromium` 从 Google CDN (`storage.googleapis.com`) 下载 Chromium，在中国大陆超时。

## 解决方案

### 方法一：npm镜像（推荐）

```cmd
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

### 方法二：使用系统自带Edge

如果Chromium下载仍然失败，Playwright支持系统自带的Microsoft Edge（Chromium内核），无需额外下载：

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")  # 使用系统Edge
```

### 方法三：手动下载Chromium

1. 从 https://npmmirror.com/mirrors/playwright/ 下载对应版本的 chromium 压缩包
2. 解压到 `%LOCALAPPDATA%\ms-playwright\` 下对应版本目录

## 公众号/知乎发布

发布脚本位于 `I:\hermes\scripts\` 目录下，在Windows上运行（需要Chrome/Edge浏览器）。
- 知乎：`python publish_zhihu.py`（首次扫码登录，cookie持久化）
- 公众号：需公众号API凭证（AppID+AppSecret），个人订阅号无API权限，需Playwright模拟手动操作

## 已验证环境

- WSL → Windows 文件系统通过 `/mnt/i/` 挂载
- Python脚本在Windows上运行，读取WSL生成的内容
- 知乎cookie文件（`input/md/知乎cookie.md`）用于免登
