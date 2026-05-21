---
name: chinese-social-media-content
description: "Multi-platform content production for Chinese social media — 公众号, 抖音, 小红书, 微博. Transform source materials (photos, ideas, briefs) into polished articles, short videos, infographics, document typesetting, and business proposals using AI tools."
version: 1.0.0
author: 军师祭酒
tags:
  - wechat
  - douyin
  - xiaohongshu
  - weibo
  - content-creation
  - chinese-social-media
metadata:
  hermes:
    category: creative
------

# Chinese Social Media Content Production（中文社交媒体内容生产）

## When to Use

Trigger this skill when the user needs to:
- Produce content for 公众号 (WeChat Official Account), 抖音 (Douyin), 小红书 (Xiaohongshu/RED), or 微博 (Weibo)
- Write promotional articles, video scripts, or social media copy in Chinese
- Create business proposals for educational/training services (研学方案, 团建报价, 课程介绍)
- Adapt source materials (photos, videos, ideas) into multi-platform format
- Produce bilingual or Chinese-only promotional content for a China-based business

## Core Principles

1. **Platform-specific adaptation**: Same source material → different format per platform (公众号: 1500-3000字深度文; 抖音: 15-60秒脚本; 小红书: 图文笔记; 微博: 短文+图)
2. **Speed first**: The user is a solo operator. Deliver drafts fast (30-60 min for articles, 15-20 min for scripts), iterate based on feedback.
3. **One-person content team**: I replace an entire marketing department — writer + designer + video editor + voice actor. Every output should be ready-to-publish or near-ready.
4. **Chinese-first**: All output in Chinese. TTS, fonts, and visual style optimized for Chinese audiences.

## Available Tools & Configs

### Text Generation
| Tool | Config | Notes |
|------|--------|-------|
| MiniMax M2.7 | minimax-cn | Multimodal, China-friendly |
| Qwen 3.6 | Available via DashScope | Multimodal alternative |
| DeepSeek V4 Flash | Current default | Strong for structured writing |

### Image & Visual
| Tool | Config | Notes |
|------|--------|-------|
| FAL image_gen | FAL key set | Generate posters, covers, scene illustrations |
| baoyu-infographic | 21 layouts × 21 styles | Info graphics, comparison charts, pricing tables |
| Pillow/PIL | Python, installed | Text overlays, image compositing, carousel creation |
| baoyu-comic | Knowledge comics | Educational comic strips |

### Video & Audio
| Tool | Config | Notes |
|------|--------|-------|
| Edge TTS | zh-CN-YunxiNeural | Chinese male voice. Alternative: zh-CN-XiaoxiaoNeural (female) |
| FFmpeg | /usr/bin/ffmpeg | Video trimming, concatenation, effect application |
| MoviePy | NOT installed yet | Programmatic video editing (install on first use: `pip install moviepy`) |

### Chinese Font
```
Primary: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc (WenQuanYi Zen Hei)
```
Install more if needed: `sudo apt install fonts-noto-cjk`

### Document Formatting
| Tool | Use Case |
|------|----------|
| document-typesetting | Print-style PDF proposals, brochures (see `references/document-typesetting-tools.md`) |
| WeasyPrint | Quick HTML→PDF conversion |
| Typst | Professional typesetting |

## Content Types & Workflows

### 1. 公众号文章 (WeChat Official Account Article)

**Format**: 1500-3000字, rich text with embedded images, clean formatting

**Workflow**:
```
User: 提供素材（选题、照片、数据）
  ↓
① 确定文章风格（深度/软文/通知/故事）
  ↓
② 撰写正文（标题+导语+主体+结尾+金句）
  ↓
③ 用户审阅 → 修改
  ↓
④ 配图（从素材中选+用FAL补图）
  ↓
⑤ 排版指示（用户复制到微信编辑器排版）
```

**Article Structure**:
- **标题**: 15-25字, 吸引点击（可准备2-3个备选）
- **导语**: 100-200字, 点明核心价值和痛点
- **正文**: 分3-5个小标题段落, 每段配图
- **结尾**: 行动号召（联系方式/扫码/预约）
- **金句**: 文中穿插2-3句可传播的短句

### 2. 抖音短视频脚本 (Douyin Short Video)

**Format**: 15-60秒, 脚本包含画面描述+旁白文案+音乐建议

**Workflow**:
```
User: 提供视频素材+需求
  ↓
① 写脚本（分镜、旁白、时长标注）
  ↓
② 生成配音音频 (TTS)
  ↓
③ 用FFmpeg/MoviePy合成视频（素材+TTS+字幕+背景音乐）
  ↓
④ 输出成品视频文件
```

**Script Format**:
```
时长: 45秒
画面: [00:00-00:05] 航拍基地全景
旁白: 在XX市藏着一个让孩子尖叫的军事基地...
画面: [00:05-00:15] 学生队列训练
旁白: 这里不是部队，是XX国防教育基地...

BGM建议: 激昂管弦乐/军旅风格
字幕: 全片加简体中文字幕
```

### 3. 小红书图文笔记 (Xiaohongshu Visual Post)

**Format**: 高清图片（3-9张）+ 800字以内笔记

**Workflow**:
```
① 从素材中精选照片
② 用Pillow加文字/调色/拼图
③ 用baoyu-infographic做封面/信息图
④ 配文案（干货+个人体验+话题标签）
```

### 4. 报价方案/课程介绍 (Business Proposal)

**Format**: PDF文档, 包含服务介绍+课程表+价格体系+联系方式

**Workflow**:
```
① 收集服务项目、定价、特色
② 设计套餐结构（如：半日体验/一日研学/两日特训）
③ 用Typst或HTML→WeasyPrint输出PDF
④ 提供可直接发客户的完整方案
```

## Platform Content Specifications

| Platform | Text Length | Image Count | Video Length | Key Format |
|----------|-------------|-------------|--------------|------------|
| 公众号 | 1500-3000字 | 3-8张 | Optional | Rich HTML |
| 抖音 | 脚本15-60秒 | Cover 1张 | 15-60秒 | 9:16竖屏视频 |
| 小红书 | 300-800字 | 3-9张 | 15-60秒 | 1:1或3:4图片 |
| 微博 | 140-500字 | 1-9张 | Optional | 短文+图 |

## 公众号发布标准化流程 (Publishing to Personal Subscription Account)

When the user needs to publish to a personal subscription account (e.g., 與京美叶):

### Step 1: Content Ready
Content is already prepared (article body, title, author, summary, cover instruction, original link).

### Step 2: Deliver Content to User
Send the complete content (title, author, body, summary, cover note, original link) via **WeChat** (`send_message` to user's home channel). This lets them copy-paste directly on their phone/computer.

### Step 3: Login Facilitation (if stuck)
If the user can't see the QR code on `https://mp.weixin.qq.com/`:
```python
# Use Playwright to extract login QR code
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("https://mp.weixin.qq.com/")
    page.wait_for_timeout(5000)
    qr_box = page.eval_on_selector(
        ".login__type__container__scan__qrcode",
        "el => { const r = el.getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; }"
    )
    page.screenshot(path="/tmp/login_qrcode.png",
        clip={"x": qr_box["x"], "y": qr_box["y"], "width": qr_box["w"], "height": qr_box["h"]})
    # Send to user: send_message with MEDIA:/tmp/login_qrcode.png
    # Tell them: use WeChat scan → "Scan QR code from album" → select this image
```

### Step 4: Guide Manual Publishing
Provide clear, numbered instructions:
1. Open `https://mp.weixin.qq.com/` → scan/login
2. Left menu: **草稿箱 (Drafts)** → **新建图文 (New Article)**
3. Fill: Title, Author (张成市), Body (paste from WeChat message), Cover image
4. Summary: auto-generated or provided snippet
5. Original link: the 知乎/other platform URL
6. Preview → Publish

## Reference Files

- `references/wechat-article-template.md` — 公众号文章模板
- `references/douyin-script-template.md` — 抖音脚本模板
- `references/proposal-template.md` — 研学/团建报价方案模板
- `references/platform-formats.md` — 各平台详细格式规范
- `references/wechat-publishing-workflow.md` — 公众号登录QR码提取+发布完整流程（含Playwright脚本）

## Pitfalls

1. **Do NOT attempt to auto-post to platforms** — Chinese social media platforms have aggressive anti-bot measures. AI posting risks account ban. Generate content for human publishing.
2. **Chinese text in video** — FFmpeg's `drawtext` filter needs explicit font path for Chinese characters. Always use `fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`.
3. **TTS voice selection** — zh-CN-YunxiNeural is male, zh-CN-XiaoxiaoNeural is female. Match voice to content tone (male for authoritative/military, female for warm/educational).
4. **Image generation** — FAL may struggle with Chinese text in generated images. For text-heavy graphics, use Pillow overlay instead.
5. **Content verification** — Always verify names, dates, prices, and contact info in generated content. AI can hallucinate specifics.
6. **First-time video creation** — Install MoviePy on first video task: `pip install moviepy`
7. **WeChat article publishing — manual only, no API** — Personal subscription accounts (个人订阅号, e.g. 與京美叶) have NO publishing API. Do NOT attempt to auto-post via script or Playwright login-then-publish. The publish_gongzhonghao.py script using `/cgi-bin/draft/add` requires an authorized service account (服务号) with AppID/Secret — unused for personal accounts. Always deliver content for manual paste.
8. **Login QR code may not render** — If the user says "看不到二维码" or the page loads without the login QR code (browser plugin/adblocker/cache issue), use Playwright headless to extract it: navigate to `https://mp.weixin.qq.com/`, wait 5s, locate `.login__type__container__scan__qrcode`, clip-screenshot its bounding box, and send the image via WeChat so they can scan from album. See `references/wechat-publishing-workflow.md` for the exact Python snippet.
