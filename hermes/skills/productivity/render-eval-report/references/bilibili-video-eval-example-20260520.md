# Bilibili视频元数据评估案例

> 来源：2026-05-20 评估「硅谷温差 Ep2: Agent记忆系统=AGI ?」
> 视频URL：https://www.bilibili.com/video/BV13WRGBoEU3
> 无字幕，时长35:25，走路径B（元数据评估）

## 评估流程

1. 解析短链 `b23.tv` → 获取真实 URL（含 BVID）
2. 调用 B站API `x/web-interface/view?bvid=BV13WRGBoEU3` 获取元数据
3. 检查字幕可用性：`data.subtitle.list` 为空 → 判定无字幕
4. 用 `web_search` 补充检索（确认频道信息、相关讨论）
5. 基于 description + 元数据 + 背景知识完成评估

## Bilibili API 关键字段

```json
{
  "data": {
    "bvid": "BV13WRGBoEU3",
    "title": "2.Agent记忆系统 = AGI ?",
    "pubdate": 1777679480,          // Unix timestamp
    "duration": 2125,                // 秒
    "desc": "本期《硅谷温差》...",    // 完整描述
    "owner": { "name": "硅谷的温差" },
    "stat": {
      "view": 96, "danmaku": 1, "reply": 6,
      "favorite": 7, "coin": 2, "share": 3, "like": 3
    },
    "subtitle": { "allow_submit": false, "list": [] },
    "cid": 38023268579               // 用于字幕查询
  }
}
```

## B站字幕检查端点（按顺序）

1. `x/player/v2?bvid=BVxxx&cid=xxx` → `data.subtitle.subtitles`
2. `x/web-interface/view/detail?bvid=BVxxx` → `data.View.subtitle.list`

两者都空 = 无字幕。

## BVID获取

`b23.tv` 短链直接 GET 会返回 412，用 Python requests 拿到 `resp.url` 然后 regex 提取 BVID：
```python
import re
bvid_match = re.search(r'BV\w+', resp.url)
```

## 评估输出格式（路径B推荐结构）

1. **总评**：星级★ + 一句话定性
2. **核心论点摘要**：逐条列出
3. **对齐度分析**（如果评估对象与Hermes相关）：表格形式对比
4. **批判性评估**：亮点 / 不足 分列
5. **后续行动**：P0/P1/P2 优先级标记

## 保存路径

- wiki/raw/（status: raw, transcription: none 标记）
- 不入 output/ 除非用户要求 HTML 渲染

## 与视频-wiki 技能的关系

- 用户说「存入wiki」「转录」 → 走 `video-to-wiki` 全量转录
- 用户说「评估分析」「极大」 → 走本路径（元数据评估）
- 用户同时说两者 → 先评估（路径B），转录作为后台任务
