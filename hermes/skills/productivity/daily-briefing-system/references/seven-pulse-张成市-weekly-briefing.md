# Seven-Pulse Weekly Briefing — 张成市 Implementation

> Concrete setup for 14-cron-job daily briefing system
> Created: 2026-05-05 | Updated: 2026-05-06 (dual-track delivery)
> Update note: Changed from "双推" (Telegram+WeChat both auto-push) to "双轨" (Telegram auto 09:00 + WeChat on-demand)

## User Profile

- Name: 张成市 (自称 蛊堂公/龙坝)
- Role: 诗人、奶爸（四孩）、安全管理员、妻子事业合伙人（国防军事教育基地）
- Platforms: Telegram (6512378453) + WeChat (o9cq80-A2QetTJisKNUphB70rxhs@im.wechat)
- Work dir: I:\hermes (WSL: /mnt/i/hermes/)
- Archive path: /mnt/i/hermes/output/weekly_reports/

## Delivery Architecture: Dual-Track (as of 2026-05-06)

| Platform | Delivery Model | Details |
|----------|---------------|---------|
| **Telegram** | Auto-push (cron) | Reports at 09:00, reminders at 18:00. Cron jobs unchanged. |
| **WeChat** | On-demand | User says "发周报" (or "周一的"/"周三的") → agent generates live in session. |

### Why Dual-Track?
The user wants Telegram as the "official push" channel (reliable, formatted, can be revisited) and WeChat as the "conversation" channel (where they can ask follow-ups and discuss after reading the report).

### On-Demand Generation Pattern (WeChat)
When user requests a report on WeChat:
1. Identify current day of week → determine topic from schedule
2. Web search latest news covering the 5 fixed points + flexible items
3. Compose full report (same format as cron-generated ones)
4. Deliver directly in the WeChat conversation
5. Save to archive at /mnt/i/hermes/output/weekly_reports/

## User Preferences (Embedded in Briefings)

- **Format**: 5 section blocks（每段60-150字）+ 灵活内容 + ending line
- **Order**: 从严肃到轻松排序（周一最严肃，周日最轻松）
- **Execution**: "开干" = 立即执行，不要过度解释
- **Tone**: 直接、有信息量、不废话、不鸡汤；技术类（周四）语气"像技术圈老友分享，专业但不晦涩，保持兴奋感"
- **Scope**: 覆盖要广（如AI周报不限于6家巨头，要覆盖美中主要厂商）
- **Delivery**: Telegram auto (09:00) + WeChat on-demand
- **Reminder**: Telegram 18:00 only (no WeChat reminder)
- **Ending**: 每篇报告末尾加一句「💡 军师的话」收尾

## Week Schedule

| Day | Topic | Cron Jobs (Telegram) | WeChat Trigger |
|-----|-------|---------------------|----------------|
| Mon | 诗歌与文学创作 | bf7309fa7a51 (report 09:00) + a6a683d48041 (reminder 18:00) | 用户说"周一的"或"发周报" |
| Tue | 父亲角色·家庭教育·英语 | 055c4d24f791 (report 09:00) + ce91f5de82bb (reminder 18:00) | 同上 |
| Wed | 军事热点·中国经济·世界经济 | e9b3730b5ff2 (report 09:00) + 406d93aec47a (reminder 18:00) | 同上 |
| Thu | 计算机与人工智能 | 5f7ad26d7a23 (report 09:00) + 909784d00d3e (reminder 18:00) | 同上 |
| Fri | 古代学术·新书·出版业 | 4494706feb8b (report 09:00) + 4ef824707c90 (reminder 18:00) | 同上 |
| Sat | 自我管理·短板修补 | 894e576ca00a (report 09:00) + 9e2a08e89577 (reminder 18:00) | 同上 |
| Sun | 生活趣味·身心安顿 | 6ab54d95b24f (report 09:00) + 347cb9de90ec (reminder 18:00) | 同上 |

## Cron Job Configuration Details

All report cron jobs:
- Schedule: `0 9 * * N` (N=1-7 for Mon-Sun)
- Model: default (deepseek-v4-flash)
- Deliver: `telegram:6512378453`
- No `send_message` to WeChat in prompts (Dual-Track)

All reminder cron jobs:
- Schedule: `0 18 * * N`
- Deliver: `telegram:6512378453`
- Simple nudge prompt, no WeChat delivery

## Report Fixed Points Detail

### Monday — 诗歌与文学创作
1. 本周诗坛要闻（活动/征稿/赛事/评奖）
2. 经典诗人/作品推荐（含简短赏析）
3. 当代新诗一读（完整贴出+解读）
4. 诗论/评论一篇（核心观点摘要）
5. 诗歌出版新讯（书名/作者/出版社）

### Tuesday — 父亲角色·家庭教育·英语
1. 教育新观点/研究
2. 父职参与方法（一个实操建议）
3. 英语学习本周推荐（App/频道/播客/网站）
4. 家庭实操小技巧（具体可执行）
5. 亲子共读/共学推荐

### Wednesday — 军事热点·宏观视野
1. 国内外军事热点（国防部官网）
2. 中国经济重要消息
3. 世界经济/金融市场
4. 国内政策新动向
5. 社会热点事件

### Thursday — 计算机与人工智能
覆盖范围：美国（OpenAI/Anthropic/Google/Microsoft/Apple/Meta/NVIDIA/xAI）+ 中国（阿里/DeepSeek/腾讯/Kimi/MiniMax/百川/智谱）+ 其他

**Format A（原始版本-公司维度）**：
1. 美国AI第一梯队（OpenAI+Anthropic+Google）
2. 美国AI第二梯队+NVIDIA（Microsoft/Apple/Meta/xAI）
3. 中国AI企业动态
4. AI产业与生态（融资/爆款/开源/政策）
5. 本周AI技术亮点（论文/突破/工具）

**Format B（2026年5月演化-主题维度）**：
1. AI行业重要动态：本周国内外AI领域最重要的消息
2. 新工具/新应用：一个值得关注的新AI工具或应用，说明有什么用
3. 技术趋势观察：当前AI领域值得关注的技术走向
4. 对个人的启发：这些技术发展对他的学习/写作有什么启发
5. 本周值得关注的话题：预告下周值得关注的方向
- 每段60-150字
- 语气：像技术圈老友分享，专业但不晦涩，保持兴奋感
- 纯知识兴趣阅读，不涉及企业经营
- 末尾加「💡 军师的话」收尾
- 格式开头：**日期：2026年X月X日（周四）** **呈：张成市**

### Friday — 古代学术·出版业
1. 古籍整理/考古新发现
2. 古代学术研究新论文
3. 国学/古代文化新书
4. 出版业重要新闻
5. 编辑/出版人动态

### Saturday — 自我管理·短板修补
1. 本周一个管理新思路
2. 本周一个新任务/挑战
3. 一个新机会推荐
4. 一个新方法/新工具
5. 本周践行指南（最小切口、最大收益）

### Sunday — 生活趣味·身心安顿
1. 健康/健身一条建议
2. 冥想/正念/心理调适
3. 园艺/种植技巧
4. 饮食/养生信息
5. 一个放松推荐（电影/音乐/书/风景）

## Initial Research Sources (七脉弹药库)

See file: `/mnt/i/hermes/output/doc/七脉弹药库-信息源清单.md`
Contains ~50 curated information sources across all 7 domains, including:
- 诗歌: 中国诗歌网/诗刊社/星星诗刊/这里有诗播客
- 家教: 爸爸真棒/憨爸在美国/父能量播客
- 军事: 国防部官网/中国军网/研学旅行网/全国国防教育平台
- AI: 量子位/机器之心/阮一峰周刊/PaperWeekly/硅谷101
- 学术: 奎章阁/书格/国学网/三联学术通讯/出版商务周报
- 自我管理: 电脑玩物/L先生说/warfalcon/Forest
- 生活: 踏花行/我爱菜园网/Keep/潮汐/朱兜兜花园

## Pitfall History

### 2026-05-06: Initial misinterpretation of delivery change
When user said "微信端以我要求周报时你随时发", I initially interpreted this as "cancel Telegram auto-push". Actually meant: keep Telegram auto-push unchanged, add WeChat on-demand as a parallel track. Always ask: "哪个端改哪个端不改" before assuming both.

### 2026-05-08: Search API failure in cron session
The Friday 学术出版 cron job ran with firecrawl API credits exhausted. web_search and web_extract both failed with "Payment Required". Successful fallback: bing-search skill (curl-based) + direct `curl -s -L` for page extraction. Xinhuanet.com content extracted cleanly. Gmw.cn returned gzipped binary (need `--compressed` flag).

### 2026-05-21: 周四AI周报搜索与格式迭代
**搜索策略**：本周四的AI周报使用Bing search作为主搜索工具（web_search因firecrawl额度失效）。并行跑4路Bing搜索（中美关键词各2路），从搜索结果摘要中提取有价值的文章URL，再用curl直取内容。关键发现：
- 36kr.com的Anthropic估值文章（1.2万亿）可用curl成功提取，内容质量高
- IT之家（ithome.com）的OpenAI新品报道同样可curl提取
- 中文Bing搜索"马斯克 OpenAI 败诉"时掉入"马"的百科陷阱——需要用更精确的引号包围关键词
- 英文Bing搜索比中文Bing的搜索质量高一个数量级，优先用英文关键词搜中文话题

**格式迭代**：本周用户明确要求了新的主题式5段结构（见Format B），替代了之前按公司划分的视角。记录在此供后续周四AI周报参考。

**执行提示**：对于周四AI周报的cron任务，由于这是纯知识兴趣阅读（不涉及企业经营），搜索范围可以更广——技术博客、开源社区、arXiv论文、Reddit/HN讨论都可以纳入，不限于企业动态。

### 2026-05-08: Bing query strategy lesson for report generation
- Broad queries ("古籍整理 考古新发现 2025年5月") returned encyclopedic pages (Baidu Baike, Zhihu) — nearly useless for weekly news.
- Specific queries ("2025年度全国十大考古新发现揭晓") returned rich news articles.
- Lesson: for report generation, prefer event-name/quote-anchored queries over date+noun queries.
- Multiple parallel bing_search calls (3-5 at once) efficiently gathered diverse topic data.
