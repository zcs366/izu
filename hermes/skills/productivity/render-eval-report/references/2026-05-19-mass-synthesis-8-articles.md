# 2026-05-19 同主题火线合成案例：8篇极大级

## 场景
用户在单会话内连续发送8篇微信公众号文章，全部标记"极大"，主题高度一致——Agent基础设施层。

## 文章清单
1. Harness Engineering（OpenAI Ryan）—— 代码免费，工程分工已变
2. Agent Skills 系统性综述（127篇论文）—— 技能生命周期
3. Ralph（19.1k⭐）—— 自主编码循环
4. aweskill—— 47个Agent的中央Skill管理器
5. MIA（Memory Intelligence Agent）—— RL驱动自进化记忆
6. Ralph Loop不够用（Jarrod Watts）—— 长时间Agent缺3件事
7. Scientific Agent Skills（23k⭐）—— 135个科研技能包
8. take-root（6 Persona Harness）—— 评审+对抗+收敛工程化

## 处理流程

### 第1阶段：火线扫描（不挡道）
- 不逐篇写评估
- 不触发5-agent合议
- 仅做：web_extract → 快速扫读 + 级别判定 → 回复摘要

### 第2阶段：用户说"开始"→ 全流水线
**Parallel raw saving**: 8篇 raw 文件同时写入 wiki/raw/articles/（直接 write_file，8次调用，耗时<30秒）
**Synthesis writing**: 识别共同主题"Agent基础设施层"→ 写框架合成文档
  - 分7个维度（哲学/资产/执行/管理/记忆/科研/工程）
  - 每个维度做对照表：文章主张 ↔ 我们能力 ↔ 差距
  - ASCII 图景展示三层结构
**Action plan**: 产出 P0×3 + P1×3，带难度和价值评级
**HTML rendering**: python3 render_report.py → .html

## 关键决策

| 决定 | 逻辑 |
|------|------|
| 不做逐篇独立评估 | 8篇同一主题，独立评估会大量重复 |
| 不触发5-agent合议 | 8篇×5代理=40次delegate_task，火线场景100%被打断 |
| 直接write_file保存raw | 比delegate_task快10倍，不会被新消息打断 |
| 框架合成=主输出 | 核心数据提取出来作为合成素材，最终交付物是体系认知 |
| 加P0/P1行动计划 | 光有认知不够——需要告诉用户"接下来做什么" |

## 教训
- 同主题火线合成适合5-12篇。超过12篇需分批
- 异主题文章不要用此模式（框架合成会牵强附会）
- 保存raw时同步计算sha256（否则后续忘记补）
- log.md旧内容要完整保留