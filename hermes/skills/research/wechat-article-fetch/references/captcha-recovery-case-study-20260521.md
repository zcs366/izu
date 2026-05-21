# Captcha Recovery Case Study — 2026-05-21

## 场景

单会话批量抓取27篇微信公众号文章时，第25篇触发验证码。

| 属性 | 值 |
|------|-----|
| **文章URL** | `https://mp.weixin.qq.com/s/D7Udo__uUHentP742ytqiA` |
| **文章标题** | Claude Code 负责人：AI-native 工程组织怎么跑起来 |
| **文章作者** | Capihom |
| **文章长度** | ~5K chars |
| **前面已抓篇数** | 24篇（同一 session 复用） |

## 故障现象

```python
has_content = False
is_captcha = True  # resp.url 含 'appmsgcaptcha'
og:title = ""      # 空
```

## 恢复过程

| 尝试 | impersonate | 结果 | 说明 |
|------|-------------|------|------|
| 1 | chrome131 | ❌ captcha | 默认指纹，前面24篇都正常 |
| 2 | chrome124 | ✅ success | 新 session + chrome124 指纹 |

## 根因推测

同一 session 连续抓取24篇后，WAF 检测到请求模式并标记了该 session。重建 session + 换指纹可以绕过。

## 修复后的配置

```python
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    # 完整 Sec-Fetch-* 头
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
})
# 关键：先用 chrome124 预热
session.get("https://mp.weixin.qq.com/", impersonate="chrome124", timeout=10)
resp = session.get(url, impersonate="chrome124", timeout=30, allow_redirects=True)
```

## 经验教训

1. **连续抓取 6-8 篇后建议重建 session**（技能已有说明，验证有效）
2. **chrome131 → chrome124 是最高效的降级路径**，无需遍历全部指纹
3. 不要因为一篇 captcha 就放弃整个批次——恢复后继续即可
