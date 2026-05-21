---
name: weekly-skills-hub-survey
description: 社区生态系统巡查与市场报告生成 — 每周扫描 agentskills.io、Hermes Agent GitHub、GitHub 社区 Skill 仓库，生成结构化的 MD+HTML 市场趋势报告。
version: 1.0.0
tags:
  - research
  - market-intelligence
  - cron
  - skills-ecosystem
  - weekly
metadata:
  hermes:
    category: research
author: Hermes Agent / 军师祭酒
---

# Skills Hub 每周市场巡查报告

## 概述

每周日自动执行的社区生态巡查任务。扫描 agentskills.io、Hermes Agent 官方仓库、GitHub 社区 Skill 仓库三大信息源，结合已有技能库做对比分析，输出结构化市场报告。

## 触发方式

- **Cron 自动**：每周日上午定时自动执行
- **手动触发**：说"跑技能市场巡查"或"Skills Hub 报告"

## 执行流程

### Phase 1：前置准备

**Step 1 — 确认版本号**
```bash
# 检查已有报告，取最大版本号+1
ls /mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v*.md 2>/dev/null
# 若无历史文件则从 v1 开始
```

**Step 2 — 读取当前技能库**
```
skills_list → 获取总数、分类分布、新技能
```

### Phase 2：数据采集（并行执行效率最高）

所有采集任务互不依赖，可并行启动：

**源 1：agentskills.io**
```bash
web_extract "https://agentskills.io"
# 获取总技能数、分类体系、特色功能
# 注意：主页是文档概述页，技能总数在分级页面
```

**源 2：Hermes Agent GitHub**
```bash
# 最新 release
web_extract "https://github.com/NousResearch/hermes-agent/releases"
# 或直接：
web_search "Hermes Agent v0.x.x release 2026"

# 最新 commits
web_extract "https://github.com/NousResearch/hermes-agent/commits/main"

# Star 数量
web_extract "https://github.com/NousResearch/hermes-agent"
```

**源 3：GitHub 社区 Skill 仓库**
```bash
# 通用搜索
web_search "GitHub agent skills SKILL.md new popular repository 2026"
web_search "addyosmani agent skills update"
web_search "mattpocock skills stars"
web_search "K-Dense-AI scientific-agent-skills"
web_search "VoltAgent awesome-agent-skills"

# 定向抓取热门仓库详情
web_extract "https://github.com/addyosmani/agent-skills"
web_extract "https://github.com/mattpocock/skills"  # 如果被发现
web_extract "https://github.com/VoltAgent/awesome-agent-skills"
```

**源 4：GitHub 趋势与博客（额外信号）**
```bash
web_search "github trending weekly agent skills"
web_search "gh skill GitHub CLI agent skills"
web_search "MicrosoftDocs Agent-Skills Azure"
```

### Phase 3：对比分析

**对比维度：**
1. 技能总数变化（自身 vs 市场）
2. 新晋高星仓库及其定位
3. 影响评估（可替代/可补充/护城河）
4. 趋势判断（市场走向）

**评估原则：**
- 自制 Skill 护城河（bing-search / wechat-article-fetch / wife-base / classic-to-fairy-tale / izu-pipeline / daily-rituals）通常不可替代
- 社区高星项目需要深读再判断，不盲目安装
- 关注哲学差异而非功能差异（如 mattpocock 轻量沟通 vs addyosmani 流程纪律）

### Phase 4：报告生成

**Step A — 写 Markdown**
```bash
write_file /mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v{N}.md
```

**报告结构（可参考历史报告）：**
```
# 🏛️ Skills Hub 每周巡查报告
## — 军师祭酒探市记 · 第N期

一、巡查快照（比上期数据对比表）
二、Hermes Agent 更新（新版本/新工具/关键修复）
三、社区生态（新发现仓库、趋势判断）
四、对你的影响评估（🟢可补充 🟡可参考 🔴护城河）
五、自上次行动清单回顾（✅已完成 ❌未完成）
六、本周 Top 5 推荐（🥇🥇🥇④⑤）
七、军师最后的话
```

**Step B — 生成 HTML**

```python
import markdown, os

with open(md_path, 'r') as f:
    text = f.read()

html = markdown.markdown(text, extensions=['extra', 'tables', 'fenced_code'])

# 包装完整 HTML（含 CSS 样式，参考已有 HTML 文件）
full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skills Hub 每周巡查报告 v{N}</title>
<style>
body {{ font-family: -apple-system, 'Noto Sans SC', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #e0e0e0; }}
h1, h2, h3, h4 {{ color: #f0c27f; }}
h1 {{ border-bottom: 2px solid #f0c27f; }}
h2 {{ border-bottom: 1px solid #333; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
th {{ background: #2a2a4a; color: #f0c27f; }}
tr:nth-child(even) {{ background: #222244; }}
blockquote {{ border-left: 3px solid #f0c27f; background: #222244; padding: 10px 15px; }}
code {{ background: #2a2a4a; padding: 2px 5px; border-radius: 3px; }}
pre {{ background: #0d0d1a; padding: 15px; border-radius: 5px; }}
pre code {{ background: none; padding: 0; }}
a {{ color: #7ec8e3; }}
hr {{ border: none; border-top: 1px solid #444; }}
</style>
</head>
<body>
{html}
</body>
</html>'''

with open(html_path, 'w') as f:
    f.write(full_html)
```

**Step C — 复制到 Wiki**
```bash
cp /mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v{N}.md /mnt/i/hermes/wiki/raw/祝成果/hermes-skills-hub-weekly-report-v{N}.md
```

#### 文件位置概览

| 文件 | 路径 |
|------|------|
| Markdown 报告 | `/mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v{N}.md` |
| HTML 报告 | `/mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v{N}.html` |
| Wiki 副本 | `/mnt/i/hermes/wiki/raw/祝成果/hermes-skills-hub-weekly-report-v{N}.md` |

## 已知陷阱

### 陷阱一：v0.14.0 后升级路径已变

v0.14.0（2026-05-16）引入 PyPI 包后，升级走 `pip install --upgrade hermes-agent` 而非 `git pull && pip install -e .`。检查报告中涉及 Hermes 版本的部分时，确认升级指令用 pip 版本。

### 陷阱二：web_extract 可能返回登录页

GitHub 页面在大批量请求后可能要求登录。此时退而使用 `web_search` 获取关键数据（如 star 数、最新 release 描述）。

### 陷阱三：报告版本号冲突

如果同一个周日 cron 跑了多次，先检查目标版本号是否存在，避免覆盖已有报告。确认方法：

```bash
ls /mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v{N}.md
# 存在 → 版本号+1；不存在 → 使用该版本号
```

### 陷阱四：mattpocock/skills 的星数可能异常高

该仓库在 2026年5月中旬爆发（77k→86.9k 一周内），可能包含不算入 GitHub Trending 的正常星外，还有社交媒体传播效应。不要将其星数与 addyosmani 直接对标，注重"哲学差异"而非"谁更火"。

### 陷阱五：不要依赖 bing_search 脚本做主要数据采集

本报告的主要数据源是 `web_extract`（agentskills.io、GitHub 页面）和 `web_search`（社区搜索）。`bing_search.sh` 脚本仅作为中国商业类搜索的备选，且中文搜索质量退化严重。优先使用英文搜索和英文 GitHub 页面提取。

## 参考历史报告

- v1.0 (2026-05-10): `/mnt/i/hermes/output/doc/hermes-skills-hub-market-report-v1.0.md`
- v2.0 (2026-05-16): `/mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v2.0.md`
- v3.0 (2026-05-17): `/mnt/i/hermes/output/doc/hermes-skills-hub-weekly-report-v3.0.md`
