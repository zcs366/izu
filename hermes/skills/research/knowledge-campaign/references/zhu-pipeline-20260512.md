# 祝 CLI v0.4 实战调试记录

**日期**：2026-05-12
**主题**：张洁琼事业·抖音短视频与直播变现
**环境**：WSL (Ubuntu), Hermes Agent, DeepSeek API

---

## 会话概要

张洁琼在群聊中要求"用AI祝分析"她的事业如何利用抖音和直播变现。
刺史（张成市）要求跑 祝 流水线，但产出完全偏离目标：
- 长编正文写了美妆大主播"张洁琼"卖1.2亿的故事
- 认知地图批判直播带货的各种套路
- 完全没有涉及托管书法或国防基地业务

## 根因分析

1. **"搜"角色无真实搜索**：subagent.py 的"搜"只调 LLM 不做 web_search
2. **人名撞车**：训练数据中"张洁琼"关联美妆主播
3. **无业务上下文注入**：祝不知道张洁琼做托管和基地
4. **背景模式输出被缓冲**：log() 不用 sys.stdout.flush()

## 发现的问题清单

| # | 问题 | 严重度 | 状态 |
|---|------|--------|------|
| 1 | "搜"角色无联网搜索 | P0 | v0.4.1已修（DuckDuckGo集成） |
| 2 | log()输出缓冲 | P2 | 已修（加flush） |
| 3 | --focused不自动跳过交互 | P2 | 需显式加--silent |
| 4 | 无业务上下文注入 | P1 | 待修（--context参数规划中） |
| 5 | 模型用deepseek-v4-flash不稳定 | P2 | v0.4.1升为deepseek-chat |
| 6 | 图片/媒体不会自动从训练数据过滤 | P2 | 需人工确认 |

## 代码修复记录

### subagent.py v0.4.1

位置：knowledge-campaign skill 的 scripts/subagent.py

改动：
- 新增 ddgs_search()：DuckDuckGo 搜索
- 新增 fetch_url_text()：curl 爬页
- 新增 roll_collect()：搜→取→打包→AI总结
- "搜"角色先 roll_collect() 再调 API
- 模型从 deepseek-v4-flash 升为 deepseek-chat
- "写"角色 system prompt 增加人名业务描述规则
- "劈"角色 system prompt 增加"判断是否用刻板印象替代真实情况"

### 祝.py

位置：/mnt/i/hermes/scripts/祝.py

改动：
- log() 加 sys.stdout.flush()（已修）

### 需手工同步

`/mnt/i/hermes/scripts/subagent.py`（项目级）尚未更新为 v0.4.1。
理论上下次运行祝时会调 skill 下的 subagent，但需确认路径。
安全做法：`cp ~/.hermes/skills/research/knowledge-campaign/scripts/subagent.py /mnt/i/hermes/scripts/subagent.py`

## 运行参数备忘

```bash
# ✅ 正确的前台用法
timeout 480 python3 scripts/祝.py "主题" --focused --silent 2>&1

# ✅ 正确的后台用法（推荐）
python3 scripts/祝.py "主题" --focused --silent > /tmp/zhu_stdout.log 2>&1
tail -30 /tmp/zhu_stdout.log

# ❌ 错误用法（无--silent时后台卡死）
python3 scripts/祝.py "主题" --focused     # 卡在input()
```

## 升级规划（刺史说要私聊谈）

1. P0: 给"搜"角色绑定 web_search 工具 ✅（v0.4.1 已修）
2. P1: 把用户业务画像注入脚本（--context参数）
3. P2: 自动 --silent（focused/wild 模式默认跳过交互）
4. P3: 进度可视化（实时写入文件+轮询读取）
5. P4: 改走 delegate_task 而不是裸 subprocess
