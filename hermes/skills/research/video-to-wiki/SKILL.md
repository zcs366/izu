---
name: video-to-wiki
description: "\"在线视频（YouTube/B站/其他）→ 音频提取 → 语音转文字 → 原文+译文交替排版 → wiki入库\""
category: research
author: Hermes Agent
---

# Video-to-Wiki — 视频转录入库管线

## When to Use

用户发送视频链接（B站/YouTube/其他）+ 「存入wiki」信号时触发。

目标：提取视频完整转录稿，按 **原文段 → 译文段** 交替格式输出 Markdown，含时间戳和术语行内注解，最终存入 `wiki/raw/`。

### 分支决策：转录 vs 评估

| 用户信号 | 路径 | 引用技能 |
|---------|------|---------|
| 「存入wiki」「转录」「转存」 | **转录路径**：字幕 → 格式化 → wiki | video-to-wiki（本技能） |
| 「评估分析」「评估」「极大」「评价」 | **评估路径**：元数据 → 评级 → 对齐度 → 入库 | render-eval-report（路径B） |
| 无明确信号 + 时长 < 10min | 默认转录 | video-to-wiki |
| 无明确信号 + 时长 > 20min | 优先评估路径 | render-eval-report |

> **核心原则**：35分钟+播客类视频，如果无字幕且用户没说「转录」，不要强行Whisper转录。评估分析 > 全量转录。

## 工作流总览

```
视频链接
  ├─ YouTube → youtube-content 技能（拉字幕）
  │   └─ 无字幕 → 降级到音频+STT
  ├─ B站 → 查字幕API（3个端点）
  │   ├─ 有字幕 → 直接下载JSON转文本
  │   └─ 无字幕 → yt-dlp下载音频 → faster-whisper转录
  └─ 其他平台 → yt-dlp下载音频 → faster-whisper转录
          │
          ▼
      格式化：时间戳 + 原文 + 译文（+术语注）
          │
          ▼
      存入 wiki/raw/（YAML frontmatter + sha256）
```

## Step 1: 获取视频元数据

### B站
```bash
python3 -c "
import urllib.request, json
url = 'https://api.bilibili.com/x/web-interface/view?bvid=BV号'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.bilibili.com/'
})
with urllib.request.urlopen(req, timeout=15) as r:
    d = json.loads(r.read())
print(d['data']['title'], d['data']['owner']['name'], d['data']['duration'], d['data']['cid'])
"
```

### YouTube
使用 `youtube-content` 技能中的 `fetch_transcript.py`。

## Step 2: 检查字幕可用性

### B站字幕检查（按顺序尝试）

1. **播放器API**：`https://api.bilibili.com/x/player/v2?bvid=...&cid=...`
   - 检查 `data.subtitle.subtitles` 数组是否非空
2. **详情API**：`https://api.bilibili.com/x/web-interface/view/detail?bvid=...`
   - 检查 `data.View.subtitle.list` 是否非空

如果两个端点都返回空 → 判定无字幕，进入 Step 3 音频转录。

### YouTube字幕检查
`fetch_transcript.py` 脚本会自动处理无字幕情况并报错。捕获错误后降级到 Step 3。

## Step 3: 音频下载 + 语音转文字

### 3a. 下载音频（yt-dlp）

⚠️ **调用路径**：Hermes venv 中 yt-dlp 不在 PATH，必须用模块调用：
```bash
AUDIO_DIR=/mnt/i/hermes/tmp/video_audio
mkdir -p $AUDIO_DIR
/home/zcs/.hermes/hermes-agent/venv/bin/python3 -m yt_dlp \
  -x --audio-format wav --audio-quality 0 \
  -o "$AUDIO_DIR/VIDEO_ID.%(ext)s" \
  '视频URL'
```

⚠️ **工作目录**：永远不用 `/tmp/` 做持久工作。WSL 的 `/tmp/` 在网关重启后会被系统清理。用 `/mnt/i/hermes/tmp/video_audio/`。

### 3b. 语音转文字（faster-whisper）

```python
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "/mnt/i/hermes/tmp/video_audio/audio.wav",
    language="zh",          # 或 "en" / "auto"
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
)
```

- 中文：`medium` 模型，CPU 约 3-5x 实时（17min视频 ≈ 5-8min处理）
- 英文：`small` 模型足够
- 结果存为 JSON：`{language, duration, segments: [{start, end, text}]}`
- 原始JSON保存到 `wiki/raw/{slug}-raw.json`

**后台运行**：17分钟以上音频用 `background: true` + `notify_on_complete: true`。转录完成后清理WAV文件。

## Step 4: 格式化输出

### 格式规范

```markdown
# 视频标题

**来源**：URL
**UP主/作者**：名称
**时长**：MM:SS
**转录方式**：字幕 / Whisper 语音识别

---

## 00:00:00

> 原文段落内容……

---

## 00:00:15

> 原文段落内容……
```

### 格式化规则

1. **按自然段分组**，不是按Whisper分段逐条输出——相邻同类内容合并（gap > 4.0s 或段长 > 250字时切分）
2. **时间戳**用 `## MM:SS` 格式，取该段起始时间
3. **原文**用 `>` 引用块
4. 段落间用 `---` 分隔
5. 中文视频：仅保留原文无需翻译，专有名词需修正（Claude Code、GStack、Opus等）

## Step 5: 存入 wiki

1. 计算 sha256：`sha256sum 文件.md`
2. 存入 `wiki/raw/{slug}-transcript.md`
3. YAML frontmatter：

```yaml
---
source_url: ...
title: 视频标题
author: UP主名称
platform: youtube
duration: 864
transcription: faster-whisper-medium
ingested: 2026-05-17T20:00:00
sha256: abc123...
---
```

4. 更新 `wiki/log.md`（置顶新记录）

## Step 5b: 双路径输出（用户信号驱动）

用户通过「大」或「极大」标记表达输出深度要求。判别后，转录稿和评估分析需要**成对输出**至 I 盘：

| 用户标记 | 输出目录（绝对路径） | 说明 |
|---------|-------------------|------|
| **大** | `/mnt/i/hermes/output/大/` | 标准评估，含转录原文+评估分析 |
| **极大** | `/mnt/i/hermes/output/极大/` | 含五人合议结论的深度分析+转录原文 |
| 无标记或「存入wiki」 | 仅wiki，不入output | 标准入库 |

**产出铁律：**
- 转录原文（带时间戳的完整版）和评估分析必须**成对出现**，缺一不可
- 原文文件名：`{slug}-transcript.md`
- 评估文件名：`{slug}-eval.md`
- 大和极大文件夹**严格分开放**，用户需要仔细研究的慢慢消化

## 清理

## Pitfalls

- **B站字幕API有多个端点**：必须全部查完再判无字幕。`player/v2` 为空不代表 `view/detail` 也为空。
- **yt-dlp 不在全局 PATH**：在 Hermes venv 中安装后必须用 `python3 -m yt_dlp`，直接敲 `yt-dlp` 会 command not found。
- **B站高清流需要会员cookie**：yt-dlp 会自动降级到可用的低码率音频流（m4a 格式就够了），不用纠结。
- **faster-whisper medium 模型较大**：首次使用需下载 ~3GB，确认磁盘空间。
- **WAV 文件很大**：17min = ~192MB，转录完成后记得删除释放空间
- **VAD（Voice Activity Detection）很重要**：不开的话分段太碎，开了 `min_silence_duration_ms=500` 能自然合并停顿处。
- **yt-dlp下载经常卡尾**：下载到99%后速度骤降是常态，等它完成即可，不要中断重试
- **YouTube连接WSL代理问题**：如果连接超时，重试一般可恢复
- **不要对播客类视频强行转录**：35分钟+播客无字幕时，Whisper转录耗时15-30分钟且产出大量噪音文本，不如走评估路径（`render-eval-report` 路径B）

## Related Skills

- `youtube-content`：YouTube 字幕提取（优先使用，无字幕时降级到本技能 Step 3）
- `wiki-drop`：通用文章 wiki 入库流程
- `media-transcribe-research`：高层次的评估分析skill（本技能聚焦纯转录管线）
- `render-eval-report`：视频元数据评估路径（路径B），当用户说「评估分析」时引用
