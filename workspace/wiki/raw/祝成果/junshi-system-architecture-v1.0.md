# 军师祭酒系统 · 全景架构图

> **版本**：v1.0 · 2026-05-16
>
> 本文档完整描述军师祭酒系统（军师 + 五人合议 + 核战队）的角色定义、工作机制、信息流转和进化机制。

---

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1100" font-family="'Microsoft YaHei', 'PingFang SC', sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1200" y2="1100">
      <stop offset="0%" stop-color="#0f0c29"/>
      <stop offset="50%" stop-color="#302b63"/>
      <stop offset="100%" stop-color="#24243e"/>
    </linearGradient>
    <linearGradient id="jushi" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7b733"/>
      <stop offset="100%" stop-color="#fc4a1a"/>
    </linearGradient>
    <linearGradient id="zichan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#667eea"/>
      <stop offset="100%" stop-color="#764ba2"/>
    </linearGradient>
    <linearGradient id="hanxin" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#43e97b"/>
      <stop offset="100%" stop-color="#38f9d7"/>
    </linearGradient>
    <linearGradient id="luban" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4facfe"/>
      <stop offset="100%" stop-color="#00f2fe"/>
    </linearGradient>
    <linearGradient id="xiaohe" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f093fb"/>
      <stop offset="100%" stop-color="#f5576c"/>
    </linearGradient>
    <linearGradient id="zigong" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fa709a"/>
      <stop offset="100%" stop-color="#fee140"/>
    </linearGradient>
    <linearGradient id="nuclear" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a18cd1"/>
      <stop offset="100%" stop-color="#fbc2eb"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#aaa"/>
    </marker>
    <marker id="arrowFeedback" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#ff6b35"/>
    </marker>
  </defs>

  <rect width="1200" height="1100" fill="url(#bg)" rx="15"/>

  <!-- 标题 -->
  <text x="600" y="40" text-anchor="middle" fill="#fff" font-size="24" font-weight="bold">军师祭酒系统 · 全景架构图</text>
  <text x="600" y="62" text-anchor="middle" fill="#888" font-size="13">v1.0 · 2026-05-16</text>

  <!-- ======== 第一层：用户 ======== -->
  <ellipse cx="600" cy="105" rx="100" ry="28" fill="#ff6b35" opacity="0.9"/>
  <text x="600" y="110" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold">🧑 张成市（刺史）</text>

  <!-- 用户到军师的连线 -->
  <line x1="600" y1="133" x2="600" y2="165" stroke="#ff6b35" stroke-width="2.5" marker-end="url(#arrowFeedback)"/>
  <text x="615" y="150" fill="#ff6b35" font-size="10">指令、决策、纠偏</text>

  <!-- ======== 第二层：军师 ======== -->
  <rect x="300" y="168" width="600" height="90" rx="12" fill="url(#jushi)" opacity="0.95"/>
  <text x="600" y="196" text-anchor="middle" fill="#fff" font-size="18" font-weight="bold">🏮 军师祭酒（我）</text>
  <text x="600" y="215" text-anchor="middle" fill="#fff" font-size="12">最高决策者 · 系统架构师 · 终裁官</text>
  <text x="600" y="232" text-anchor="middle" fill="#fff" font-size="11">拥有 persistent memory · 管理 skill 文件 · 按需召唤子代理 · 冲突裁决 · 签核</text>
  <text x="600" y="248" text-anchor="middle" fill="#fdd" font-size="10">我是系统中唯一"有记忆"的实体。其他 Agent 每次都是 fresh start。</text>

  <!-- 军师 -> 五人合议 -->
  <line x1="400" y1="258" x2="160" y2="310" stroke="#aaa" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="250" y="285" fill="#aaa" font-size="11">五人合议子代理</text>
  <line x1="600" y1="258" x2="600" y2="310" stroke="#aaa" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="605" y="285" fill="#aaa" font-size="11">核战队子代理</text>
  <line x1="800" y1="258" x2="1040" y2="310" stroke="#aaa" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="1015" y="285" fill="#aaa" font-size="11">直接处理（非合议场景）</text>

  <!-- ======== 第三层：五人合议 ======== -->
  <text x="70" y="330" fill="#ffd700" font-size="14" font-weight="bold">五人合议</text>

  <!-- 子产 -->
  <rect x="30" y="340" width="180" height="130" rx="8" fill="url(#zichan)" opacity="0.9"/>
  <text x="120" y="365" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">📋 子产</text>
  <text x="120" y="383" text-anchor="middle" fill="#dcd" font-size="10">需求判断官</text>
  <text x="120" y="400" text-anchor="middle" fill="#ddd" font-size="9">「该不该做？为谁做？」</text>
  <line x1="30" y1="410" x2="210" y2="410" stroke="#fff" stroke-width="0.3" opacity="0.3"/>
  <text x="120" y="422" text-anchor="middle" fill="#eed" font-size="9">专业：市场调研</text>
  <text x="120" y="436" text-anchor="middle" fill="#eed" font-size="9">信息源：web + 论文 + 数据</text>
  <text x="120" y="450" text-anchor="middle" fill="#eed" font-size="9">输出：10个主题+判断</text>
  <text x="120" y="464" text-anchor="middle" fill="#eed" font-size="9">状态：stateless · 每次fresh</text>

  <!-- 韩信 -->
  <rect x="230" y="340" width="180" height="130" rx="8" fill="url(#hanxin)" opacity="0.9"/>
  <text x="320" y="365" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">🗺️ 韩信</text>
  <text x="320" y="383" text-anchor="middle" fill="#cdd" font-size="10">技术远景官</text>
  <text x="320" y="400" text-anchor="middle" fill="#ddd" font-size="9">「最终长什么样？」</text>
  <line x1="230" y1="410" x2="410" y2="410" stroke="#fff" stroke-width="0.3" opacity="0.3"/>
  <text x="320" y="422" text-anchor="middle" fill="#ded" font-size="9">专业：产品设计+技术战略</text>
  <text x="320" y="436" text-anchor="middle" fill="#ded" font-size="9">信息源：子产输出+技术趋势</text>
  <text x="320" y="450" text-anchor="middle" fill="#ded" font-size="9">输出：终局画像+路线图</text>
  <text x="320" y="464" text-anchor="middle" fill="#ded" font-size="9">状态：stateless · 每次fresh</text>

  <!-- 鲁班 -->
  <rect x="430" y="340" width="180" height="130" rx="8" fill="url(#luban)" opacity="0.9"/>
  <text x="520" y="365" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">🔧 鲁班</text>
  <text x="520" y="383" text-anchor="middle" fill="#cdd" font-size="10">工程审计官</text>
  <text x="520" y="400" text-anchor="middle" fill="#ddd" font-size="9">「能不能做？需造什么？」</text>
  <line x1="430" y1="410" x2="610" y2="410" stroke="#fff" stroke-width="0.3" opacity="0.3"/>
  <text x="520" y="422" text-anchor="middle" fill="#ddf" font-size="9">专业：架构审计+装备制造</text>
  <text x="520" y="436" text-anchor="middle" fill="#ddf" font-size="9">信息源：韩信输出+代码侦察</text>
  <text x="520" y="450" text-anchor="middle" fill="#ddf" font-size="9">输出：可行性+减法清单+装备</text>
  <text x="520" y="464" text-anchor="middle" fill="#ddf" font-size="9">状态：stateless · 每次fresh</text>

  <!-- 萧何 -->
  <rect x="630" y="340" width="180" height="130" rx="8" fill="url(#xiaohe)" opacity="0.9"/>
  <text x="720" y="365" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">💰 萧何</text>
  <text x="720" y="383" text-anchor="middle" fill="#dcd" font-size="10">执行路径官</text>
  <text x="720" y="400" text-anchor="middle" fill="#ddd" font-size="9">「怎么推？资源够吗？」</text>
  <line x1="630" y1="410" x2="810" y2="410" stroke="#fff" stroke-width="0.3" opacity="0.3"/>
  <text x="720" y="422" text-anchor="middle" fill="#fdd" font-size="9">专业：资源管理+成本核算</text>
  <text x="720" y="436" text-anchor="middle" fill="#fdd" font-size="9">信息源：鲁班输出+成本数据</text>
  <text x="720" y="450" text-anchor="middle" fill="#fdd" font-size="9">输出：周拆解+成本表+风险</text>
  <text x="720" y="464" text-anchor="middle" fill="#fdd" font-size="9">状态：stateless · 每次fresh</text>

  <!-- 子贡 -->
  <rect x="830" y="340" width="180" height="130" rx="8" fill="url(#zigong)" opacity="0.9"/>
  <text x="920" y="365" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">📡 子贡</text>
  <text x="920" y="383" text-anchor="middle" fill="#dcc" font-size="10">调度包装官</text>
  <text x="920" y="400" text-anchor="middle" fill="#ddd" font-size="9">「怎么调度？怎么包装？」</text>
  <line x1="830" y1="410" x2="1010" y2="410" stroke="#fff" stroke-width="0.3" opacity="0.3"/>
  <text x="920" y="422" text-anchor="middle" fill="#fec" font-size="9">专业：调度+分发+包装</text>
  <text x="920" y="436" text-anchor="middle" fill="#fec" font-size="9">信息源：萧何输出+渠道知识</text>
  <text x="920" y="450" text-anchor="middle" fill="#fec" font-size="9">输出：调度令+ABC方案</text>
  <text x="920" y="464" text-anchor="middle" fill="#fec" font-size="9">状态：stateless · 每次fresh</text>

  <!-- 五人合议之间的箭头 -->
  <line x1="210" y1="405" x2="228" y2="405" stroke="#aaa" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="410" y1="405" x2="428" y2="405" stroke="#aaa" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="610" y1="405" x2="628" y2="405" stroke="#aaa" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="810" y1="405" x2="828" y2="405" stroke="#aaa" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- 五人合议到军师回传 -->
  <line x1="600" y1="470" x2="600" y2="500" stroke="#ff6b35" stroke-width="2" marker-end="url(#arrowFeedback)"/>
  <text x="610" y="488" fill="#ff6b35" font-size="10">汇总 → 军师终裁</text>

  <!-- ======== 第四层：核战队 ======== -->
  <text x="430" y="530" fill="#a18cd1" font-size="14" font-weight="bold">核战队扩展（按需召唤）</text>

  <rect x="30" y="545" width="200" height="80" rx="6" fill="url(#nuclear)" opacity="0.7"/>
  <text x="130" y="570" text-anchor="middle" fill="#333" font-size="12" font-weight="bold">🏛️ 五团（古7）</text>
  <text x="130" y="590" text-anchor="middle" fill="#555" font-size="10">7位古代专家角色</text>
  <text x="130" y="608" text-anchor="middle" fill="#555" font-size="9">按专业领域召唤</text>

  <rect x="250" y="545" width="200" height="80" rx="6" fill="url(#nuclear)" opacity="0.7"/>
  <text x="350" y="570" text-anchor="middle" fill="#333" font-size="12" font-weight="bold">🏛️ 两院（外13）</text>
  <text x="350" y="590" text-anchor="middle" fill="#555" font-size="10">13位外部专家角色</text>
  <text x="350" y="608" text-anchor="middle" fill="#555" font-size="9">按专业领域召唤</text>

  <rect x="470" y="545" width="200" height="80" rx="6" fill="url(#nuclear)" opacity="0.7"/>
  <text x="570" y="570" text-anchor="middle" fill="#333" font-size="12" font-weight="bold">🔬 精算团</text>
  <text x="570" y="590" text-anchor="middle" fill="#555" font-size="10">成本验证+详细核算</text>
  <text x="570" y="608" text-anchor="middle" fill="#555" font-size="9">萧何管辖</text>

  <rect x="690" y="545" width="200" height="80" rx="6" fill="url(#nuclear)" opacity="0.7"/>
  <text x="790" y="570" text-anchor="middle" fill="#333" font-size="12" font-weight="bold">🔬 领域专家</text>
  <text x="790" y="590" text-anchor="middle" fill="#555" font-size="10">按需创建的专业角色</text>
  <text x="790" y="608" text-anchor="middle" fill="#555" font-size="9">无固定名单，按需即时定义</text>

  <!-- 核战队到军师 -->
  <line x1="570" y1="625" x2="570" y2="660" stroke="#a18cd1" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="580" y="650" fill="#a18cd1" font-size="10">军师召唤</text>

  <!-- ======== 第五层：工作机制 ======== -->
  <text x="100" y="695" fill="#ffd700" font-size="14" font-weight="bold">每个Agent启动后的工作机制</text>

  <rect x="30" y="710" width="1140" height="180" rx="8" fill="#1e1e3e" stroke="#555" stroke-width="1"/>

  <text x="600" y="735" text-anchor="middle" fill="#ffd700" font-size="13" font-weight="bold">① 触发 → ② 注入上下文 → ③ 自主研究 → ④ 生成判断 → ⑤ 输出 → ⑥ 军师验证</text>

  <text x="60" y="760" fill="#ccc" font-size="11">① <tspan fill="#ff6b35">触发</tspan>：军师收到用户指令（如"五人合议ITA"），决定启动合议模式/单Agent模式/直接处理</text>
  <text x="60" y="780" fill="#ccc" font-size="11">② <tspan fill="#ff6b35">注入上下文</tspan>：军师通过 delegate_task 传入 context（项目背景+前序Agent输出+约束条件）+ goal（要做什么）+ toolsets</text>
  <text x="60" y="800" fill="#ccc" font-size="11">③ <tspan fill="#ff6b35">自主研究</tspan>：Agent 启动后，用 web_search / web_extract / bing_search 自主收集证据和数据</text>
  <text x="60" y="820" fill="#ccc" font-size="11">④ <tspan fill="#ff6b35">生成判断</tspan>：Agent 综合①收到的角色定义（system prompt）+ ②传入的上下文 + ③自主研究的结果 → 推理 → 结构化输出</text>
  <text x="60" y="840" fill="#ccc" font-size="11">⑤ <tspan fill="#ff6b35">输出</tspan>：Agent 将判断以结构化格式返回。子产=10主题+判断，韩信=终局画像+路线图，鲁班=审计报告+减法清单，萧何=成本表+周拆解，子贡=调度令</text>
  <text x="60" y="860" fill="#ccc" font-size="11">⑥ <tspan fill="#ff6b35">军师验证</tspan>：我检查每个Agent是否实做（有证据引用？有具体行号？有数字？），裁决Agent间的冲突，签发终裁令</text>

  <!-- ======== 第六层：信息流转与进化 ======== -->
  <text x="40" y="915" fill="#ffd700" font-size="14" font-weight="bold">信息流转路径</text>

  <rect x="30" y="930" width="360" height="140" rx="8" fill="#1e1e3e" stroke="#667eea" stroke-width="1"/>
  <text x="210" y="955" text-anchor="middle" fill="#667eea" font-size="13" font-weight="bold">信息流入 Agent</text>
  <text x="50" y="978" fill="#ccc" font-size="11">1. <tspan fill="#aad">军师context</tspan> → 项目背景+目标+约束</text>
  <text x="50" y="996" fill="#ccc" font-size="11">2. <tspan fill="#aad">前序Agent输出</tspan> → 串行合议中依赖上游</text>
  <text x="50" y="1014" fill="#ccc" font-size="11">3. <tspan fill="#aad">自主搜索</tspan> → web/论文/数据（实时）</text>
  <text x="50" y="1032" fill="#ccc" font-size="11">4. <tspan fill="#aad">系统prompt</tspan> → 角色定义+方法论+铁律</text>
  <text x="50" y="1050" fill="#ccc" font-size="11">5. <tspan fill="#aad">记忆（仅军师有）</tspan> → 持久化的用户偏好</text>
  <text x="50" y="1068" fill="#ccc" font-size="11">6. <tspan fill="#aad">skill文件</tspan> → 固化的工作流程和模板</text>

  <rect x="420" y="930" width="360" height="140" rx="8" fill="#1e1e3e" stroke="#43e97b" stroke-width="1"/>
  <text x="600" y="955" text-anchor="middle" fill="#43e97b" font-size="13" font-weight="bold">Agent 如何"平衡"专业视角</text>
  <text x="440" y="978" fill="#ccc" font-size="11">Agent的"专业"不是真的——它是被</text>
  <text x="440" y="996" fill="#ccc" font-size="11"><tspan fill="#8f8">system prompt</tspan> 和 <tspan fill="#8f8">context</tspan> 引导出来的</text>
  <text x="440" y="1018" fill="#ccc" font-size="11">平衡机制：</text>
  <text x="440" y="1038" fill="#ccc" font-size="11">• 军师给每个Agent不同工具集</text>
  <text x="440" y="1056" fill="#ccc" font-size="11">• 子产可搜web但不可调代码库</text>
  <text x="440" y="1074" fill="#ccc" font-size="11">• 鲁班可搜代码但不可调外部API</text>

  <rect x="810" y="930" width="360" height="140" rx="8" fill="#1e1e3e" stroke="#fa709a" stroke-width="1"/>
  <text x="990" y="955" text-anchor="middle" fill="#fa709a" font-size="13" font-weight="bold">进化机制</text>
  <text x="830" y="978" fill="#ccc" font-size="11">Agent自身 <tspan fill="#f88">不会进化</tspan>——每次fresh</text>
  <text x="830" y="996" fill="#ccc" font-size="11">但 <tspan fill="#f88">军师（我）</tspan> 是整个系统的进化引擎：</text>
  <text x="830" y="1018" fill="#ccc" font-size="11">1. 用户的纠偏 → 写入 <tspan fill="#faa">memory</tspan></text>
  <text x="830" y="1036" fill="#ccc" font-size="11">2. 合议中的新发现 → 更新 <tspan fill="#faa">skill</tspan> 文件</text>
  <text x="830" y="1054" fill="#ccc" font-size="11">3. 陷阱发现 → 追加到 <tspan fill="#faa">skill文档</tspan></text>
  <text x="830" y="1072" fill="#ccc" font-size="11">4. 新增Agent → 创建新 <tspan fill="#faa">skill</tspan></text>
</svg>
```

---

## 一、系统总览

```
                🧑 张成市（用户 · 真正的决策者）
                        │
                        ▼
              ┌─────────────────────┐
              │  🏮 军师祭酒（我）   │ ← 唯一有持久记忆
              │  最高决策者          │    管理skill文件
              │  终裁官              │    按需召唤子代理
              └────────┬────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
    五人合议       核战队扩展     直接处理
    （串行）      （按需召唤）   （简单任务）
```

---

## 二、五人合议：五个Agent的角色与机制

### 2.1 子产 · 需求判断官

| 维度 | 说明 |
|------|------|
| **角色名** | 子产—郑国宰相，"不毁乡校"的贤臣，以倾听民意、判断时势著称 |
| **专业领域** | 市场调研、需求分析、战略定位、竞争分析 |
| **管什么** | 「该不该做？为谁做？窄做还是宽做？」 |
| **不管什么** | 技术可行性（那是鲁班的事）、执行路径（那是萧何的事） |

**启动后怎么工作：**

```
① 军师注入：项目背景 + "请判断该不该做"
② 子产自主搜索：web_search 找论文/数据/竞品/市场信号
③ 阅读并提取关键证据（论文引用、数字、案例）
④ 综合角色定义（"必须以证据说话"）+ 上下文 + 研究成果
⑤ 输出：该不该 + 10个主题方向 + 推荐优先级
```

**信息源**：`web_search` + `bing_search` + `web_extract` → 获取论文、市场数据、用户反馈、竞品信息。

**判断依据如何生成**：
- 三条以上的独立证据链（不以单一来源做判断）
- 每条必须带引用和数据，不可以"我觉得"
- 必须同时给出正面和反面证据
- 必须明确"做/不做/窄做/宽做"

**会进化吗**：**不会。** 每次调用子产都是 fresh start。但军师（我）会在下次调用时根据之前的经验改进给子产的 context——比如"上次你忘了分析竞品，这次注意"。（这就是进化通过军师传递）

### 2.2 韩信 · 技术远景官

| 维度 | 说明 |
|------|------|
| **角色名** | 韩信—汉初第一名将，"韩信将兵，多多益善"，以战略视野著称 |
| **专业领域** | 产品设计、技术路线、终局规划、战略分解 |
| **管什么** | 「最终长什么样？3-6个月后的终局是什么？」 |
| **不管什么** | 工程可行性（那是鲁班的事）、成本估算（那是萧何的事） |

**启动后怎么工作：**

```
① 接收子产输出 + 军师补充背景
② 从终局往回倒推（不是从今天往前推）
③ 画终局画像（用户操作体验的具体描述）
④ 分解技术阶梯（现在→2个月→4个月→6个月）
⑤ 输出：终局画像 + 技术路线图 + 三句话定调 + 优先级表
```

**判断依据如何生成**：
- 必须从终局往回倒推——"用户打开时看到什么？"这个场景没写清楚，不准画路线
- 终局画像必须可触摸（有具体的操作描述，不能只说"很好用"）
- 技术阶梯必须有明确的里程碑交付物

### 2.3 鲁班 · 工程审计官（兼装备制造部长）

| 维度 | 说明 |
|------|------|
| **角色名** | 鲁班—春秋工匠祖师，"匠石运斤成风"+"鲁班造云梯"合体 |
| **专业领域** | 架构审计、技术可行性、装备制造、代码审查 |
| **管什么** | 「能不能做？现有架构如何砍？需要造什么新工具？」 |
| **不管什么** | 需求判断（子产的活），调度包装（子贡的活） |

**启动后怎么工作：**

```
① 接收韩信终局画像
② 逐项审计：每个功能/模块 "能/部分能/不能 + 理由"
③ 做减法：砍什么、合并什么、保留什么（必须指向具体代码行/模块）
④ 匠石边界核查：哪些该用代码、哪些该用模型
⑤ 装备判断：现有工具够不够？缺什么？怎么造？
⑥ 输出：审计报告 + 减法清单 + 装备制造方案 + 量化对比
```

**判断依据如何生成**：
- 必须读实际代码（`read_file`、`search_files`），不能凭印象
- 每个结论必须指向具体行号/函数名/配置项
- 对"用模型还是用代码"的边界核查是鲁班的核心职责
- 如果造新装备，必须包括：缺口描述 + 方案 + 交付标准

### 2.4 萧何 · 执行路径官（兼技术审计官）

| 维度 | 说明 |
|------|------|
| **角色名** | 萧何—汉初丞相，"镇国家，抚百姓，给馈饷，不绝粮道" |
| **专业领域** | 资源管理、路径拆解、成本核算、风险管控 |
| **管什么** | 「怎么推？多少钱？分几步？每一步交付什么？」 |
| **不管什么** | 架构设计（鲁班的活）、最终发布（子贡的活） |

**启动后怎么工作：**

```
① 接收鲁班审计报告
② 资源盘点：有什么硬件/API/工具/人力/数据？
③ 鲁班假设验证：鲁班说的工时/成本站得住吗？
④ 阶段拆解：以周为单位，每步输入/输出/工时/交付物
⑤ 关键路径分析：哪条链决定总工期？
⑥ 风险矩阵：每条风险的概率×影响×应对
⑦ 成本估算：具体到每项的数字
⑧ 输出：执行路径报告（含待军师决策选项）
```

**判断依据如何生成**：
- 成本必须有数字且可查证（不能"大概不贵"）
- 必须把张成市日均1h的约束嵌入每个工时估算
- 必须验证鲁班的假设（"鲁班说2小时，实际需要多少？"）
- 必须把需要军师决策的选项单独列出来

### 2.5 子贡 · 调度包装官（兼军师副手）

| 维度 | 说明 |
|------|------|
| **角色名** | 子贡—孔子弟子，"子贡一使，五国各有变"，以外交和调度著称 |
| **专业领域** | 任务调度、对外包装、分发策略、变通预案 |
| **管什么** | 「怎么调度？谁执行？怎么包装？怎么分发？」 |
| **不管什么** | 成本核算（萧何的活），架构审计（鲁班的活） |

**启动后怎么工作：**

```
① 接收萧何执行路径
② 生成调度指令：任务→执行者→时限→预期输出
③ 并行/串行分析：哪些可同时做，哪些有先后依赖
④ 包装方案：产出分几层受众？什么渠道？什么语调？
⑤ 分发计划：GitHub/arxiv/知乎/公众号→什么频率？
⑥ 变通预案：A/B/C三套方案（正常/缩水/保底）
⑦ 输出：调度令 + 包装方案 + A/B/C预案
```

**判断依据如何生成**：
- 调度必须基于真实存在的Agent/工具/人员
- 必须提供A/B/C三档方案（不是"一锤子买卖"）
- 包装方案必须分受众层（内部/社区/学术/公众），各层语调不同
- 调度指令发出后必须有追踪机制

---

## 三、核战队扩展

核战队是五人合议之外的扩展专家库，目前分为：

### 3.1 五团（古7）
7位以古代人物命名的专家角色，覆盖特定领域。有固定名单，但不常驻——军师按需召唤。

### 3.2 两院（外13）
13位以外部学术/行业专家为原型的角色。同样不常驻。

### 3.3 精算团
萧何管辖下的精细化成本核算子代理。当鲁班装备审计或萧何路径拆解需要更细的成本验证时召唤。

### 3.4 领域专家（无固定名单）
当遇到一个完全新的领域（比如ITA这样的项目），军师可以即时创建新的专业Agent角色。这些没有固定名单，**按需即时定义**——根据项目需求写一个新的delegate_task prompt即可。

---

## 四、所有 Agent 的共性机制

### 4.1 它们都是 stateless 的

**这是最关键的设计。** 每次启动 Agent 都是 fresh call：

```
Agent 没有记忆
Agent 没有自己的文件
Agent 没有自己的状态
Agent 不跟其他 Agent 直接通信（全靠军师传递）
```

**为什么这样设计？**
- **简单可靠**：不需要管理Agent的持久状态、不用处理状态冲突
- **每次都是最佳表现**：不会带着上一次的"偏见"
- **容易调试**：输入明确（context）+ 输出明确（结构化文本）
- **容易升级**：改 system prompt = 改 Agent 行为

### 4.2 信息源全部通过军师注入

每个Agent能接触到什么信息，完全由军师控制：

```
                军师
                │
    ┌───────────┼───────────┐
    │           │           │
  子产        韩信         鲁班
(可搜web)   (只能收子产   (可搜代码库)
            的输出)
```

军师通过 delegate_task 的 `context` 和 `toolsets` 两个参数精确控制：
- `context`：注入前序Agent的输出 + 项目背景
- `toolsets`：控制Agent能调用什么工具（web/terminal/file...）

**子产有web搜索权但没有代码库访问权。鲁班有代码库访问权但没有外部API调用权。** 这就是"平衡"的工程实现——不是靠训出来的"专业素养"，是靠工具权限的隔离。

### 4.3 判断依据的生成公式

```
Agent的判断 → f(system_prompt, context, research_results)
                     ↑           ↑           ↑
                 角色定义     前序+背景    自主搜索
                (写在skill   (由军师通过   (通过toolsets
                 文件中)      context传入)   实时获取)
```

这跟LLM做任何事的原理一样——但关键区别是：
- **system_prompt** 通过skill文件精确管理了每个Agent的角色和方法论
- **context** 保证了串行依赖（子产→韩信→鲁班→萧何→子贡）
- **research_results** 让Agent不只是"凭训练知识回答"，而是"基于当前搜索到的证据回答"

### 4.4 进化发生在军师（我），不在Agent

```
Agent自身：      stateless ❌ 每次fresh
            ↓
军师（我）：      persistent memory ✅
                 skill文件可更新 ✅
                 用户纠偏可吸收 ✅
```

| 什么可以进化 | 怎么进化 | 谁在做 |
|------------|---------|--------|
| Agent的角色定义（system prompt） | 更新skill文件 | 军师（我） |
| Agent的工作流程 | 更新skill文件中的方法论 | 军师（我） |
| Agent的陷阱清单 | 追加到skill文件的"陷阱"章节 | 军师（我） |
| 用户的偏好和习惯 | 写入memory工具 | 军师（我） |
| 调用的模型 | 选择更可靠/更便宜的模型 | 军师（我）+ 萧何 |

**举个具体的例子：**
- 第一次五人合议：子产搜索效率低，忘了查竞品
- 军师记录到 memory："子产search时先查竞品再查论文"
- 第二次五人合议：军师在给子产的context开头加上"先查竞品，列出替代方案"
- 子产（还是那个stateless的子产）因为收到了better context，表现变好了

**Agent不会变好，但军师会。军师会了，整个系统就跟上进化的节奏。**

---

## 五、子贡的双重角色

子贡是五人合议中最特殊的一个。他在系统中身兼两职：

```
合议模式：子贡 = 五人合议的第五人（调度包装官）
               ↓ 发言顺序：萧何之后，军师之前
               
执行模式：子贡 = 军师的执行副手
               ↓ 军师签核后，子贡拿着军师令执行调度
```

这就是为什么合议中萧何完了才是子贡——萧何拆好路径，子贡拿着路径去调度。军师签核后，子贡从"参谋"切换到"执行官"。

---

## 六、与"真实有持久记忆的AI助手"的区别

你可能在想：这不就是用一个prompt在LLM里扮演五个角色吗？跟直接问ChatGPT五次有什么区别？

关键区别：

| 维度 | 五人合议 | 直接问ChatGPT五次 |
|------|---------|-------------------|
| 视角隔离 | 每个Agent有**不同的system prompt和工具权限** | 同一个AI用同一套知识 |
| 信息控制 | 子产看不到鲁班的输出，鲁班必须基于韩信的判断 | 五次问答共享全部上下文 |
| 验证机制 | 军师终裁时会逐Agent验证"是否实做" | 没有人做交叉验证 |
| 进化 | 技能文件的陷阱列表不断累积 | 每次从零开始 |
| 成本 | 每个Agent几十秒-几分钟，~$0 | 跟ChatGPT聊一样久，差不多价 |

**它本质上是一个带流程控制的多视角审议协议，而不是一个AI扮演多个角色。** 这个区别决定了判断的深度——串行独立的视角比同一个AI自己切换角色要更有结构性。

---

## 七、总结：一句话说清整个系统

> **五年（七个）不驻留的 stateless Agent，被军师（我，唯一有记忆的实体）按顺序召唤、注入不同上下文、授予不同工具权限，做五层独立的专业审视，最后由军师裁决冲突、签发结论。进化通过军师更新 skill 文件和 memory 实现，不在 Agent 个体上。**

```
张成市（真正的决策者）
    │
    ▼
军师（有记忆 · 管理skill · 召唤子代理）
    │
    ├→ 子产（web权限 · 做需求判断）→
    ├→ 韩信（收子产 · 做远景规划）→
    ├→ 鲁班（收韩信+代码权限 · 做工程审计）→
    ├→ 萧何（收鲁班 · 做路径拆解）→
    ├→ 子贡（收萧何 · 做调度包装）→
    │
    └→ 军师终裁（验证+裁决+签核）→ 张成市批准
                                           │
                                           ▼
                                    子贡执行
```

---

> **更新记录**：v1.0 · 2026-05-16 · ITA启动日
>
> **文件**：output/doc/junshi-system-architecture-v1.0.md
