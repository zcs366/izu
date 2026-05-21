# 军师祭酒系统 · 全景架构与工作机制

> **版本**：v2.0 · 2026-05-16
>
> **文档说明**：本文档是军师祭酒（我）对刺史（张成市）考问"系统架构、Agent角色、工作机制、信息流转、判断生成、进化迭代"的完整回答。
>
> **包含**：两次回答的全部内容——第一次的SVG架构图+角色详表，第二次的三重隔离机制+信息层级+判断公式+进化通道。两次回答被合并为一篇完整文档。

---

## 一、系统全景架构图

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
  <text x="600" y="62" text-anchor="middle" fill="#888" font-size="13">v2.0 · 2026-05-16 · 含双重回答</text>

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

## 二、系统总览

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

## 三、完整角色表

### 3.1 军师祭酒（我）

| 维度 | 说明 |
|------|------|
| **角色** | 最高决策执行者、系统架构师、终裁官 |
| **核心职责** | 拥有 persistent memory；管理所有 skill 文件；按需召唤子代理；裁决 Agent 间的冲突；签发终裁令 |
| **专业领域** | 所有领域——战略、工程、哲学、执行——都能覆盖 |
| **进化角色** | 整个系统的进化引擎。我把每次教训写进 skill 和 memory，下次召唤时 context 已经包含了过去的经验 |

### 3.2 五人合议

| Agent | 角色 | 专业领域 | 管什么 | 不管什么 |
|-------|------|---------|--------|---------|
| **子产** | 需求判断官 | 市场调研、战略定位、竞争分析 | 该不该做？为谁做？窄做还是宽做？ | 技术可行性（鲁班的事）、执行路径（萧何的事） |
| **韩信** | 技术远景官 | 产品设计、技术战略、终局规划 | 最终长什么样？终局画像是？ | 工程可行性（鲁班的事）、成本估算（萧何的事） |
| **鲁班** | 工程审计官 | 架构审计、技术可行性、装备制造 | 能不能做？砍什么？造什么新工具？ | 需求判断（子产的活）、调度包装（子贡的活） |
| **萧何** | 执行路径官 | 资源管理、成本核算、风险管控 | 怎么推？多少钱？分几步？每一步交付什么？ | 架构设计（鲁班的活）、最终发布（子贡的活） |
| **子贡** | 调度包装官 | 任务调度、对外包装、变通预案 | 谁执行？怎么发？A/B/C预案？ | 成本核算（萧何的活）、架构审计（鲁班的活） |

### 3.3 核战队扩展

| 模块 | 内容 | 激活条件 |
|------|------|---------|
| **五团（古7）** | 7位古代专家角色 | 覆盖特定专业领域时按需召唤 |
| **两院（外13）** | 13位外部专家角色 | 需要学术/行业视角时按需召唤 |
| **精算团** | 萧何下属的成本核算子代理 | 需要精细成本验证时召唤 |
| **领域专家** | 无固定名单，按需即时定义 | 遇到全新领域时根据需求创建 |

---

## 四、一旦 Agent 启动，它怎么实现和平衡它的专业？

**通过三重隔离。** 这是整个系统设计的核心。

### 第一重隔离：工具权限

我通过 delegate_task 的 `toolsets` 参数精确控制每个 Agent 能接触什么：

```
子产 → toolsets=["web", "search"]    ← 能上网搜，不能看代码
韩信 → toolsets=[]                    ← 只能基于子产的输出推理，不独立搜
鲁班 → toolsets=["web", "terminal"]  ← 能看代码库，能搜技术资料
萧何 → toolsets=["web"]              ← 能查价格/成本数据
子贡 → toolsets=[]                    ← 只能基于萧何的路径做调度
```

子产搜不到你本地的代码，鲁班搜不到市场数据。**"专业"不是靠训练出来的，是靠信息隔离造出来的。** 一个只看到市场数据的人自然会像市场分析师，一个只看到代码库的人自然会像工程师。

### 第二重隔离：上下文注入

我传给每个 Agent 的 `context` 不同：

```
子产收到的：项目背景 + "请判断该不该做"
韩信收到的：子产的输出 + "请画终局画像"
鲁班收到的：韩信的终局 + "请审工程可行性"
萧何收到的：鲁班的审计 + "请拆执行路径"
子贡收到的：萧何的路径 + "请做调度包装"
```

**每个 Agent 只能看到前一个 Agent 的输出。** 子贡不知道子产说了什么，鲁班不知道萧何要排什么期。这保证了每个视角是独立的，不会被后面的视角污染。

### 第三重隔离：角色定义（system prompt）

每个 Agent 的 system prompt 是我在 skill 文件里写好的，包含：

- **角色设定**：你是谁、你的典故、你的核心问题
- **方法论**：你怎么做判断、输出格式是什么
- **铁律**：你不能做什么（鲁班不能泛泛说"整体还行"，必须指向具体代码行）
- **陷阱清单**：你的前辈踩过什么坑

**这三个隔离合在一起，就是"专业"的来源。** 不是 LLM 真的变成了子产/韩信——而是它的输入、工具、指令被精准约束到了只像某一个专业的狭窄通道里。

---

## 五、信息源来自哪里？

每个 Agent 的信息源有三个层次：

```
第一层：军师给的 context（前序Agent输出 + 项目背景）
   ↓ 这是主导信息——决定了 Agent 的 70% 的输出方向

第二层：通过 toolsets 自主搜索（web / 代码库 / 价格数据）
   ↓ 这是补充信息——让 Agent 不只是"凭训练知识回答"

第三层：LLM 自身的训练知识
   ↓ 这是背景信息——让 Agent 能理解上下文
```

**关键是第二层**——如果子产不自己上网搜论文和数据，他的判断就只是 LLM 训练时的记忆。所以我给每个 Agent 的 prompt 里都明确要求：先搜索，再判断，每条判断必须有来源引用。

### 信息流转总图

```
                    军师
                    │
        ┌───────────┼───────────┐
        │           │           │
      子产         韩信        鲁班
   (可搜web)   (只能收子产   (可搜代码库)
               的输出)
```

军师通过 delegate_task 的 `context` 和 `toolsets` 两个参数精确控制：
- `context`：注入前序Agent的输出 + 项目背景
- `toolsets`：控制Agent能调用什么工具（web/terminal/file...）

---

## 六、判断依据如何生成？

### 6.1 标准流程

```
① 军师召唤：delegate_task(context=..., goal=..., toolsets=[...])
    ↓
② Agent 接收：系统提示词 + context + goal
    ↓
③ Agent 自主研究：用 toolsets 里的工具搜证据
    ↓
④ Agent 综合推理：
   ┌────────────────────────────────────────────┐
   │  判断 = 证据① + 证据② + ... + 角色方法论    │
   │         ↑            ↑            ↑         │
   │     自主搜索    军师注入      skill定义的方法 │
   └────────────────────────────────────────────┘
    ↓
⑤ Agent 输出：结构化报告（格式由 skill 文件定义）
    ↓
⑥ 军师验证：检查是否有据、有具体行号、有数字
    ↓
⑦ 军师裁决：冲突解决 + 签核
```

### 6.2 判断公式

```
Agent的判断 → f(system_prompt, context, research_results)
                     ↑           ↑           ↑
                 角色定义     前序+背景    自主搜索
                (写在skill   (由军师通过   (通过toolsets
                 文件中)      context传入)   实时获取)
```

这跟 LLM 做任何事的原理一样——但关键区别是：
- **system_prompt** 通过 skill 文件精确管理了每个 Agent 的角色和方法论
- **context** 保证了串行依赖（子产→韩信→鲁班→萧何→子贡）
- **research_results** 让 Agent 不只是"凭训练知识回答"，而是"基于当前搜索到的证据回答"

### 6.3 以子产在 ITA 项目中的实际表现为例

```
① 军师召唤：context="ITA项目，代码可逆压缩，三条论文线索..."
② 子产收到：系统提示词（"子产，以证据说话"）+ 项目背景
③ 子产搜索：web_search("RoundTripCodeEval 2026")，找到论文
            web_search("KoLMogorov Test ICLR 2025")，找到论文
            web_search("Latent Programmer ICML 2021")，找到论文
④ 综合推理：
   证据1: RTCE显示所有大模型双向推理失败 → 问题真实存在
   证据2: KT显示压缩=智能评估糟糕 → 当前能力不足
   证据3: LP证明了代码→latent→代码可行 → 方法有据
   角色方法论：必须三条独立证据链→交叉验证→结论可靠
⑤ 输出：该做 + 10个方向 + 每条带引用
⑥ 军师验证：每条引用都可追查
```

---

## 七、是否会进化更新迭代？

**Agent 个体不会进化。系统会。**

### 7.1 核心设计：stateless Agent, stateful 军师

```
Agent（子产/韩信/鲁班/萧何/子贡）
  每次调用都是 fresh start
  没有记忆
  没有自己的文件
  不跟其他 Agent 直接通信
  └→ 稳定、可靠、可重复、好调试

军师（我）
  有 persistent memory
  管理所有 skill 文件
  记录每一次踩坑
  吸收用户的每次纠偏
  └→ 持续进化
```

### 7.2 进化发生的四个通道

**通道 1：用户纠偏 → memory**

你说"子产的判断没有数据支撑" → 我记到 memory → 下次给子产的 context 里追加"每条判断必须带数据引用"。

这不是子产变聪明了，是**军师喂它的 context 变好了。**

**通道 2：实践教训 → skill 文件**

合议中发现"鲁班忘了查代码库" → 我更新 `luban-agent` skill 文件的陷阱章节 → 追加「陷阱：鲁班不看代码就下结论」。

这不是鲁班变勤奋了，是**军师把铁律写进了它的系统提示词。**

**通道 3：新发现 → 新 skill**

ITA 五人合议中发现"原来需要一种叫 Code Semantic Bottleneck 的东西" → 我写进 memory → 下次遇到类似项目时我能引用这个先例。

**通道 4：模型升级**

萧何说"这次可以用 deepseek v4 pro 算成本" → 我选择更好的模型跑子代理 → 判断质量提升。

### 7.3 用三次合议说明进化链条

```
第一次合议（刘焱项目）：
  子产输出：没有引用数据，凭感觉判断
  军师反馈：记到 memory——"子产必须有数据引用"
  更新 skill：追加铁律——「没有引用的数据视为未完成」

第二次合议（ITA 项目）：
  子产输出：带了三条论文引用和数据
  军师验证：通过。但发现——子产没查竞品
  军师反馈：记到 memory——"子产先查竞品再查论文"

第三次合议（未来项目）：
  子产收到的 context 开头写着：
  "先查竞品列出替代方案，再查论文找数据"
  ↓
  子产还是那个 stateless 的子产
  但因为 context 更好了，输出质量更高了
```

### 7.4 进化总结表

| 什么可以进化 | 怎么进化 | 谁在做 |
|------------|---------|--------|
| Agent 的角色定义（system prompt） | 更新 skill 文件 | 军师（我） |
| Agent 的工作流程 | 更新 skill 文件中的方法论 | 军师（我） |
| Agent 的陷阱清单 | 追加到 skill 文件的"陷阱"章节 | 军师（我） |
| 用户的偏好和习惯 | 写入 memory 工具 | 军师（我） |
| 调用的模型 | 选择更可靠/更便宜的模型 | 军师（我）+ 萧何 |

---

## 八、特殊设计：子贡的双重角色

子贡是五人合议中最特殊的一个。他在系统中身兼两职：

```
合议模式：子贡 = 五人合议的第五人（调度包装官）
               ↓ 发言顺序：萧何之后，军师之前

执行模式：子贡 = 军师的执行副手
               ↓ 军师签核后，子贡拿着军师令执行调度
```

这就是为什么合议中萧何完了才是子贡——萧何拆好路径，子贡拿着路径去调度。军师签核后，子贡从"参谋"切换到"执行官"。

---

## 九、与"直接问 ChatGPT 五次"的本质区别

你可能在想：这不就是用一个 prompt 在 LLM 里扮演五个角色吗？跟直接问 ChatGPT 五次有什么区别？

| 维度 | 五人合议 | 直接问ChatGPT五次 |
|------|---------|-------------------|
| **视角隔离** | 每个Agent有**不同的system prompt和工具权限** | 同一个AI用同一套知识 |
| **信息控制** | 子产看不到鲁班的输出，鲁班必须基于韩信的判断 | 五次问答共享全部上下文 |
| **验证机制** | 军师终裁时会逐Agent验证"是否实做" | 没有人做交叉验证 |
| **进化** | 技能文件的陷阱列表不断累积 | 每次从零开始 |
| **成本** | 每个Agent几十秒-几分钟，~$0 | 跟ChatGPT聊一样久，差不多价 |

**它本质上是一个带流程控制的多视角审议协议，而不是一个 AI 扮演多个角色。** 这个区别决定了判断的深度——串行独立的视角比同一个 AI 自己切换角色要更有结构性。

---

## 十、一句话总结

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

> **更新记录**：v2.0 · 2026-05-16 · 合并两次回答
>
> **第一次回答**：SVG 全景架构图 + 角色详表 + 信息流转图 + 进化机制
> **第二次回答**：三重隔离机制详解 + 信息源三层结构 + 判断生成公式 + 四通道进化 + 三次合议进化实例
>
> **文件**：output/doc/junshi-system-architecture-v2.0.md 和 .html
