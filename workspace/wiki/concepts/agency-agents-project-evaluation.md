---
title: agency-agents 项目深度评估
type: evaluation
evaluated: 2026-05-15
verdict: 值得研究，但需谨慎
priority: medium
related: [izu, 五人合议, agent-design-patterns, multi-agent-collaboration]
---

# agency-agents 项目深度评估

## 项目事实

| 项目 | 状态 | 数据 |
|------|------|------|
| 原仓库 `AI-Employer/ai-employees` | ❌ 404（已下架/重命名） | — |
| 现仓库 `msitarzewski/agency-agents` | ✅ 活跃 | 97k+ stars, 16k+ forks |
| 作者 | Michael Sitarzewski | 30+年经验builder, Techstars校友 |
| 当前规模 | 144 agents / 12 divisions | 远超文章所述的55个/9部门 |
| 许可证 | MIT | 完全开源可商用 |
| 集成工具 | Claude Code, Copilot, Cursor, Aider, Windsurf, Kimi, OpenCode, Antigravity, Gemini CLI | 覆盖主流AI编码工具 |

## 核实

| 文章声称 | 核实结果 | 证据 |
|---------|---------|------|
| GitHub项目地址为 AI-Employer/ai-employees | ❌ 已404 | GitHub返回404，项目已迁移至 msitarzewski/agency-agents |
| 55个AI员工，9个部门 | ⚠️ 过时 | 当前版本144个agent，12个division |
| 可以用OpenClaw/Dify/Coze加载 | ✅ 可行但不完整 | 项目自带install.sh支持Claude Code/Cursor/Copilot等，远超文章描述 |
| "几小时跑完8agent协作" | ⚠️ 夸大 | 这是理想场景，实际涉及多模型调用成本和编排复杂度 |

## 定论

⚠️ **项目本身有价值，但文章已严重过时。** 直接照文章做会踩到404。进入新仓库后，项目规模和质量远超文章所述。

**适合做什么：**
- 学习Agent角色定义的模板和思路
- 为特定场景挑选现成的agent定义（如WeChat Mini Program Developer, Feishu Integration Developer）
- 参考其多agent协作的工作流设计

**不适合做什么：**
- 直接照搬——144个agent的定义质量参差，很多是模板化填充
- 期望"一键部署数字公司"——本质是大量.md文件（system prompt模板），不是可运行的agent框架
- 替代真正的架构设计——每个agent是独立定义，缺乏统一的编排层和记忆系统

## 对张成市/izu的价值

**直接可用的：**
- 其 `WeChat Mini Program Developer` 和 `Feishu Integration Developer` agent定义可参考——如果izu需要这些集成
- `Autonomous Optimization Architect`（LLM路由和成本优化）的设计思路与我们已有方向一致，可交叉验证
- 多工具安装脚本 `install.sh` / `convert.sh` 的工程思路——我们的izu-agent pipeline可以参考

**已有的、不需要看它的：**
- 五人合议架构（子产/韩信/鲁班/萧何/子贡/军师）的设计深度远超agency-agents中任何单一agent
- 我们在agent间协作编排（长编→定本、CP检查点、聚合）上的实践走得更远

**建议：**
1. 浏览 /engineering/ 和 /research/ 分区的agent定义，看哪些角色我们还没覆盖
2. 重点看其 agent模板里的 `success metrics` 字段——我们agent定义里可以加这个
3. 研究其 install.sh 的多工具集成思路，看能否为izu-agent pipeline提供灵感
4. **不要**花时间逐一看144个agent——80%是模板化重复，价值集中在20%

## 军师的判断

这不是一个"数字员工操作系统"，而是一个"AI角色定义图书馆"——质量参差但覆盖面广。真正的价值不在于复制它的agent，而在于对比思考：它覆盖了哪些岗位、是怎么定义角色边界的、我们缺什么。

我们已有的架构深度远超它，但它在**广度**和**安装便利性**上做了文章。值得花30分钟浏览，但不值得深度研究。
