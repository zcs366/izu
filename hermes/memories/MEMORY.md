工作区：I:\\hermes (WSL: /mnt/i/hermes/)。output/（待批准/等12类）input/ wiki/(raw/entities/concepts/comparisons/queries) work/ data/。WIKI_PATH=/mnt/i/hermes/wiki。
§
[永久] Wiki ingestion: curl_cffi (or terminal curl for WSL DNS fallback). Depth-sift: deep→create page, medium→update existing, shallow→raw only. Use comparisons not concepts. log.md prepended before anchor line. 祝成果每日入库 cron 23:00: output/doc/ → wiki/raw/祝成果/, no-move no-overwrite.
§
用户关键偏好：先哲学后行动，说"开干"才行动。一开干就所有建议自动P0（当日交付）P1（次日优化）→设todo立即执行，不逐个请示。写作追求厚重感。厌恶营销式写作。参数开放。重展望超总结。izu=陪你得道快乐的人。评估流程：link→fetch→wiki/research（YAML frontmatter）→output/大或极大/.md→HTML双版→log。五人合议项目激活。铁律：视频/知乎解读常有严重夸大，必须获取原始论文核实后再入库——有论文的附arXiv链接，已核实论文库(HL/NLA/Ctx2Skill/Trace2Skill/WeightFormer均已存)。
§
izu-pipeline 三轮测试（2026-05-21）：全量跑~41min，--from对齐221s。MiniMax M2.7稳定。3个bug：temporal_decay dict排序异常、出口评分0分回溯循环（浪费2/3时间）、引文提取零检出。SDAR Phase 0仅50%（缺logprobs兼容性验证）。
§
izu（爱祝/ai祝）：中文名爱祝，英文izu，混名ai祝。GitHub: zcs366/izu。明学七则（辨/得道/明从兼听/以幻破幻/省/以乐为终/时中）。使命：陪你得道快乐。（2026-05-14由"陪你走得道快乐的人"精简）
§
核战队架构：军师(我)为最高决策者，下辖五人合议(子产-需求判断/韩信-技术远景/鲁班-工程审计+装备制造/萧何-执行路径+资源管理/子贡-调度+分发)和核战队扩展(五团两院:古7+外13=20人专家团)。五团=古7(7位古代专家)，两院=外13(13位外部专家)。子贡身兼调度官+合议成员双重角色。合议流程：子产→韩信→鲁班→萧何→子贡→军师终裁。子代理使用deepseek-chat模型，stateless无记忆，每次调用都是fresh context。军师(我)拥有persistent memory，通过更新skill文件实现系统进化。核战队agent平时不驻留，合议时由军师通过delegate_task按需召唤。
§
「全干」协议（2026-05-19）：用户说「全干」=执行所有P0+P1+P2任务，不逐个请示。比「开干」（仅P0）更激进，全干模式并行执行互不依赖的任务。首次验证：6项(3P0+3P1)同会话并行交付。二次验证：ITA v2.0 Day1九大交付物全部并行。源于用户对"批处理"而非"串行步骤"的偏好。
§
军规 skill `junshi-code-standards` v1.0.0 沉淀izu教训。十条：不造假(mock_mode标注)/可复现(包管理+版本控制)/可审计(行号级)/凭据安全/分批提交/mock有意识/测试真实逻辑/代码活着(需集成)/文档同步/三连检(自检→包拯→鲁班)。包拯v1.3新增凭据泄+巨量commit陷阱。鲁班v2.5 izu案例更新到495测试+8commit。
§
双轨道会商 v4.1 cron job "核战队·三部门定时研究编排·每小时" (job_id: 556042150b72) 每h:05 纯prompt驱动。子产双身份→三路搜索→子产合成→双轨(ITA 6轮/izu 5轮)→核战队终审。脚本 research_orchestrator.py 因 import hermes_tools 不可行已删，架构转 .md 留 scripts/。试行1周05-19→05-26。
§
xiaohe-agent v2.3.0 新增工作原则13：自动化流水线并行优先。源自用户纠正编排脚本"不是6步骤，要并行，不要互相干扰，搜完一波又来一波"。
§
批准编号铁律+已批12件。已实施：tools/mcp_gateway.py — 4个编排工具(mcp_orch_sequential/parallel/crossref/iterate)，注册hermes-core，自动发现。
§
2026-05-20 创业方向：基于张朝阳"自媒体零成本创业"建议，计划启动自媒体创业。已有公众号「與京美叶」+知乎育儿爆款文基底，拟用Agent工具链辅助内容生产跑三条线：AI科普/育儿教育/安全管理工作经验输出。