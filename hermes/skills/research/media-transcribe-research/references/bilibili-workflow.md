# B站视频转录 — 已验证的完整工作流

> 2026-05-13：BV1U35y6CEKP（17分25秒，有字幕可用）
> 2026-05-14：BV12wRzBdEhX（17分04秒，无字幕，走 Groq STT）
> 2026-05-16：BV1DB546wEb8（11分26秒，无字幕，走本地 faster-whisper medium，686秒音频用时~7min）

## 技术细节

### B站API三步确认法

必须查完下面3个端点再判无字幕：

1. **元数据API**：`api.bilibili.com/x/web-interface/view?bvid=BV号` → cid + 标题
2. **播放器API**：`api.bilibili.com/x/player/v2?bvid=...&cid=...` → `data.subtitle.subtitles[]`
3. **详情API**：`api.bilibili.com/x/web-interface/view/detail?bvid=...` → `data.View.subtitle.list[]`

### 本地 faster-whisper 速度实测

| 视频时长 | 模型 | 耗时 | CPU 占用 |
|---------|------|------|---------|
| 20min 28s | medium (int8) | ~12min | 400% (4核) |
| 11min 26s | medium (int8) | ~7min | 400% (4核) |
| 17min 04s | medium (int8) | ~10min | 400% (4核) |

**结论**：medium 模型缩放比例约 1:0.6（视频时长:转录耗时）。已缓存时约 0.6x 实时。

### 已修正的典型错误库（2026-05-16 更新）

以下是从多次转录中积累的常见Whisper错误，按风险等级排序：

#### 🔴 高危（公司名/产品名，必须校对所有出现位置）

| 原始Whisper | 修正 | 首次发现 |
|------------|------|---------|
| unthorpeak, unsorpic, sorpid, sorpre, sorpret, unthorpez | **Anthropic** | 2026-05-16 BV1DB546wEb8 |
| Cloud Code, cloudcode | **Claude Code** | 2026-05-13 BV1U35y6CEKP |
| cloud（单独使用时，指AI模型） | **Claude** | 2026-05-13 |
| gemnet | **Gemini** | 2026-05-14 |
| sunit, sornet, sornit, snut | **Sonnet** | 2026-05-14 |
| MAC（自动化平台语境） | **Make**（make.com） | 2026-05-14 |
| 蚵塞, 科塞, 库瑟 | **Cursor** | 2026-05-14 |
| Exit, Exter, Extor | **Axton**（UP主名） | 2026-05-15 |
| Methos, Cat Wu/Catwo/开图 | **Metheus, Kat Wu** | 2026-05-14 |

#### 🟡 中危（核心概念，影响理解）

| 原始Whisper | 修正 | 说明 |
|------------|------|------|
| 节偶, 结偶 | **解耦** | 核心架构概念，需确保全文统一 |
| 风群, 蜂群 | **集群** | Agent fleet/集群，非自然界的蜂群 |
| 沙河, 沙核 | **沙盒** | sandbox，非河流 |
| 小龙虾 | **小龙虾**（保留） | UP主对本地Agent的比喻，保留不修正 |
| folk（代码语境） | **fork** | 代码托管语义 |
| 烤取sandbox, 烤贝sandbox | **kube sandbox** | Kubernetes沙盒 |
| 理程式, 礼程式, 立成 | **历史** | 高发同音错 |

#### 🟢 低危（但不修正影响阅读体验）

| 原始Whisper | 修正 | 示例 |
|------------|------|------|
| 声称 | **生成** | "让AI给我声称HTML" |
| 内联注视 | **内联注释** | inline comment |
| 可释化 | **可视化** | visualization |
| 公单 | **工单** | ticket |
| AgentMD | **AGENTS.md** | 专有文件名 |
| pwt, pdt | **PPT** | 演示文稿 |
| EVOS | **Evals** | 评测集 |
| Cowork | **CodeWork** | 产品名 |
| SARS产品 | **SaaS产品** | 商业模式 |
| 塔利克 | **塔里克** | 人名 |

### 校对清单（硬性步骤，不可跳过）

1. **产品/人名排查**：用 `grep -i 'anthropic\|cloud\|gemnet\|sunit\|exit\|exter\|mac\|agentmd\|pwt' {file}` 快速定位所有疑似错误
2. **同音字三遍法**：读三遍——第一遍通读抓感觉，第二遍逐句校，第三遍"专有名词"模式查
3. **AI公司名必须统一**：Anthropic/OpenAI/Meta/Google 在整篇中保持一致
4. **中英混排检查**：`/` 前后是否有空格、英文术语大小写是否一致
5. **时间戳对齐**：每段时间戳递增，无跳跃或重叠

### 环境总结

| 组件 | 路径/值 |
|------|--------|
| yt-dlp | `/home/zcs/.hermes/hermes-agent/venv/bin/python3 -m yt_dlp` |
| faster-whisper | medium, cpu, int8, VAD 500ms |
| Groq key | `~/.hermes/.env` → `GROQ_API_KEY`（注意可能是`***`占位符） |
| Stable temp dir | `/mnt/i/hermes/tmp/bilibili_audio/`（不要用 `/tmp/`） |
| ffmpeg | `/usr/bin/ffmpeg` |
| Wiki 路径 | `/mnt/i/hermes/wiki/` |
