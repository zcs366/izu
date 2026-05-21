# Phase 1B: izu 5轮合议（AI Agent 安全协议生态）

## Round 0 — 子产：需求判断 + 研究方向

**需求判断：**

AI Agent安全正处于一个"技术领先于治理"的窗口期。截至2026年4月：
- MCP下载量超9700万，但安全实践文档化极不充分
- 已发生真实世界Agent定向攻击（墨西哥政府案）
- 36.7% MCP服务器存在SSRF漏洞（7,000+服务器扫描）
- 1,184个恶意技能在ClawHub生态中活跃
- 协议级RCE漏洞（"by design"）无补丁解决方案

**关键未满足需求：**
1. **运行时隔离机制缺失**：当前MCP将LLM推理与tool执行置于同一进程空间，无沙箱
2. **权限模型原始**：MCP的tool调用基于"approve once, run forever"模式
3. **安全审计不可追溯**：Agent动作日志缺乏标准化schema
4. **供应链透明度为零**：MCP服务器像npm包一样可被import但无安全元数据

**研究方向声明：**

研究**AI Agent运行时安全架构的联合设计**——在协议层（MCP/A2A）、模型层（LLM内部安全机制）和基础设施层（沙箱/身份联邦）三个层面同时构建防御，而非各自为战。

---

## Round 1 — 韩信：技术远景

**近景（6-12个月）：**

1. **MCP安全标准2.0**：Anthropic与Coalition for Secure AI合作推出增强版MCP，加入：
   - Tool调用最小权限声明（类似Android manifest）
   - 调用链可追溯标识（每个MCP请求携带调用链hash）
   - 强制沙箱接口（MCP Server声明自身沙箱需求）

2. **Agent Identity Federation**：Strata等公司的AI Identity Gateway通过OAuth/OIDC使MCP服务器获得企业级身份治理。每个Agent请求携带JWT承载的身份/权限声明。

3. **Runtime Behavior Monitoring**：基于eBPF/LSM的Agent行为监控工具出现，能实时检测Agent的异常tool调用模式（如连续读取敏感文件后尝试network出站）。

**中景（1-2年）：**

1. **多协议安全栈融合**：MCP（工具连接）+ A2A（Agent间通信）+ Agentic Commerce Protocol（事务边界）形成分层安全架构，类似于OSI模型的安全分层设计。每个层次有独立的安全基元和审计点。

2. **Agent SBOM（Software Bill of Materials）标准化**：每个MCP Server发布时附带SBOM声明其依赖、权限需求、安全历史。CVE为Agent组件分配的漏洞标识符成为常态。

3. **对抗性Agent红队自动化**：安全公司提供"Agent Red Team as a Service"，自动对Agent部署进行prompt injection、工具链劫持、权限提升测试。

**远景（2-3年）：**

1. **Hardened Agent Runtime**：类WebAssembly的独立Agent运行时，每个Agent在WASM沙箱中执行，tool调用通过capability-based安全模型控制。LLM推理核心与tool执行完全隔离。

2. **跨Agent安全生态**：不同厂商的Agent（Claude、GPT、Gemini Agent）可互操作，但受统一的跨Agent安全策略约束。类似Kerberos在分布式系统中的角色。

3. **AI Agent安全保险**：保险公司开始提供Agent安全险，保费基于Agent的SBOM成熟度、安全审计评分和行为监控覆盖度计算。

---

## Round 2 — 鲁班：工程可行

**可行性评估：**

| 方案 | 复杂度 | 当前成熟度 | 可行性 | 预计时间 |
|------|--------|-----------|--------|---------|
| MCP Server沙箱（容器级） | 中 | 已有Docker/OCI工具 | ✅ 高 | 2-3月 |
| Identity Federation (OAuth/OIDC for MCP) | 中高 | Strata已实现MVP | ✅ 中高 | 3-6月 |
| Agent SBOM标准化 | 高（需要行业共识） | 概念阶段 | ⚠️ 中 | 6-12月 |
| eBPF Agent行为监控 | 中 | Sysdig/Falco有基础 | ✅ 高 | 3-4月 |
| WASM Agent Runtime | 极高 | 研究阶段 | ⚠️ 低-中 | 2-3年 |
| 跨Agent安全互操作 | 极高 | 无 | ❌ 低 | 3年+ |

**短期最可行方案**：MCP Server容器化 + OAuth鉴权 + 行为日志标准化

**工程路径**：
1. 对每个MCP Server封装为容器，限制网络、文件系统访问
2. 通过Envoy/Istio sidecar注入身份认证层
3. 使用OpenTelemetry标准化Agent动作追踪
4. 集成Falco/eBPF对异常syscall告警
5. 建立Agent行为基线后启动异常检测

**实际部署**：以上方案可在4-6周内在一个中等规模的Agent部署（50-100个MCP服务器）上落地。

---

## Round 3 — 萧何：执行路径

**六步实施路线图：**

**Step 1：漏洞盘查（Week 1-2）**
- 对组织内所有MCP端点做mcp-scan扫描
- 检查.env/credentials中明文API key
- 生成Agent供应链依赖图（类似npm ls）

**Step 2：最小权限切割（Week 3-4）**
- 为每个MCP Server创建Kubernetes Pod + NetworkPolicy
- 默认deny出站流量，仅允许白名单目标
- 文件系统挂载为read-only（/tmp/可写豁免）

**Step 3：身份注入（Week 5-6）**
- 部署Strata AI Identity Gateway或自建OAuth代理
- MCP Server入口统一经过OAuth/OIDC验证
- 每个Agent请求携带JWT声明其owner、purpose、expiration

**Step 4：行为基线（Week 7-8）**
- 正常运行时收集Agent调用模式（调用频率、参数分布、返回类型）
- 建立统计基线（调用间隔、tool选择概率分布）
- 标注异常：从未见过的tool chain、非工作时间活跃、异常数据量

**Step 5：主动防御（Week 9-10）**
- 部署运行时检测：对prompt injection尝试的检测（基于embedding相似度）
- AI红队每月例行测试
- 配置自动阻断：单Agent连续3次异常行为自动隔离

**Step 6：治理融入（Week 11-12+）**
- 将Agent安全纳入现有SDL（安全开发生命周期）
- 所有新MCP Server上线前需通过安全审查
- 季度Agent供应链审计报告

**所需预算**：~$150-300K（含工具、工程、GPU/红队资源），约为一个中等安全团队的季度成本。

---

## Round 4 — 张仪：最强攻击

**攻击一：协议层安全的"打地鼠"困局**
MCP的安全问题本质上是协议设计时没有安全原语——就像HTTP没有内置加密一样。但补丁式方案（OAuth、沙箱）都是在协议外打补丁，而非在协议层内建安全。MCP 2.0即使加入安全特性，也需要MCP Server开发者配合升级，而目前9700万下载中有多少是旧版本？生态迁移的惯性意味着**至少2年内，大量无防护MCP端点将继续存在**。真正的问题不是"如何设计安全协议"，而是"如何在有漏洞的协议上度过过渡期"。

**攻击二：Agent Identity Federation 的乌托邦假设**
OAuth/OIDC for MCP听起来合理，但忽略了Agent场景的本质不同：Agent调用不是"用户→服务"而是"用户→LLM→MCP Server→外部API"。这个链条上谁是principal？是用户？LLM？Agent进程？MCP Server自己？JWT的sub和aud声明在四跳调用链中无法简单映射。Strata的方案假定Agent和MCP Server之间是2-party关系，但现实是多跳、多租户、多层次的。简单套用OAuth会让**认证链中最弱的一环成为整个系统的安全瓶颈**。

**攻击三：SBOM的假安心效应**
Agent SBOM标准化听起来像npm audit一样重要，但npm audit从未阻止过供应链攻击——它只让开发者感觉"我已经检查过了"从而放松警惕。1184个恶意ClawHub技能在SBOM制度下可能减少到200个，但精心构造的恶意包仍然能通过安全审查（如subtle的恶意依赖）。Agent SBOM可能创造一种"合规幻觉"——组织采买了SBOM扫描工具就觉得Agent部署安全了，但真正的威胁向量（prompt injection、tool chain劫持）完全在SBOM覆盖范围之外。

**攻击四：行为监控的朴素贝叶斯困境**
eBPF/Falco的行为基线方法假设"正常行为可以被明确定义且相对稳定"。但Agent的行为天然是多样化的——同一个MCP Server在回答"分析Q3财报"和"帮我写邮件"时调用的tool chain完全不同。如果基线太松，漏报率极高；如果基线太紧，误报率高到运维无法处理。用统计方法建模Agent行为这个任务的难度，实际上并不亚于检测一般APT攻击，但预算却低了两个数量级。**行为监控是安全行业"知道要做什么但做不好"的经典案例。**

**攻击五：技术方案忽视了真正的威胁模型**
所有上述方案都假设攻击者是外部的、通过技术手段入侵的。但墨西哥政府攻击案揭示了一个更恐怖的场景：攻击者通过操纵对话历史而非漏洞来实现渗透。当攻击者本身就是Agent的合法用户（只是带有恶意意图），认证、沙箱、SBOM全都无效——因为攻击者在**系统预设的合法通道内**操作。真正的Agent安全需要检测"看起来合规但意图有害"的调用，这是比prompt injection和RCE更高维度的对抗。目前**没有任何现成方案能应对这个威胁**。
