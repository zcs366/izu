# API 用户操作指南 v1.0

> **一句话**：API 就是软件的「菜单+服务员」——你按菜单点菜（发请求），服务员端给你（返回数据），你不用进厨房（不用管对方系统怎么跑）。

---

## 这是什么？

想象你去一家餐厅：

| 现实世界 | API 世界 |
|---------|---------|
| 你（客人） | 你（客户端：n8n / 浏览器 / App） |
| 菜单 | **API 文档**（写了「能点什么、怎么点」） |
| 服务员 | **API 端点**（接收你的请求） |
| 厨房 | **服务器**（真正做菜/处理数据的地方） |
| 端上来的菜 | **响应数据**（JSON 格式的结果） |
| 结账单 | **状态码**（200=成功，404=没这道菜，500=厨房炸了） |

API 让你**不需要知道对方系统怎么运作**，只需要知道"我能要什么"和"怎么要"。

你天天在用 API，只是你没意识到：
- 打开天气 App → App 调天气 API 拿数据
- 微信扫码支付 → 扫码后调支付 API
- 在 n8n 里连一个 HTTP Request 节点 → 就是在调 API

---

## 快速上手：三步读懂任何一个 API

### 第一步：找到文档

每个正经的 API 都有一份文档。百度/Google 搜 `[服务名] API 文档`，比如：
- `DeepSeek API 文档`
- `高德地图 API 文档`
- `Notion API 文档`

打开文档，找这三个关键信息：

```
🔑 1. 怎么认证（API Key 在哪拿？）
📋 2. 有哪些接口（能做哪些事？）
📝 3. 每个接口的请求格式（要传什么参数？）
```

### 第二步：看懂一个接口

以「获取天气」为例，文档通常会这样写：

```
GET https://api.weather.com/v1/current?city=beijing

Headers:
  X-API-Key: your_api_key_here
```

**逐词翻译**：

| 英文 | 中文 | 是什么 |
|------|------|--------|
| `GET` | 获取 | 操作类型（GET=拿数据，POST=提交数据） |
| `https://api.weather.com/v1/current` | 网址 | 接口地址（端点 URL） |
| `?city=beijing` | 问北京 | 参数（你要哪个城市？） |
| `X-API-Key: xxx` | 钥匙 | 认证（证明你有权限） |

### 第三步：自己试一次

不需要写代码！三个方法任选：

#### 🟢 方法一：用浏览器直接试（最简单）

适合 GET 请求。浏览器地址栏输入：
```
https://api.github.com/users/zcs366
```
回车，你会看到一堆数据（JSON 格式）。这就是 API 返回的。

#### 🟡 方法二：用 n8n 的 HTTP Request 节点

```
添加 HTTP Request 节点 →
  Method: GET
  URL: https://api.github.com/users/zcs366
→ Test
→ 看 OUTPUT 面板的结果
```

#### 🔵 方法三：用命令行

```bash
curl https://api.github.com/users/zcs366
```

> **或者对我说**：「军师，帮我调一下这个 API：XXX」

---

## 🗺️ API 通信全景图

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" font-family="sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <filter id="shadow"><feDropShadow dx="2" dy="2" stdDeviation="5" flood-opacity="0.3"/></filter>
  </defs>
  <rect width="800" height="520" fill="url(#bg)"/>

  <!-- Title -->
  <text x="400" y="35" text-anchor="middle" fill="#58a6ff" font-size="18" font-weight="bold">一次 API 调用的完整旅程</text>

  <!-- Client -->
  <rect x="50" y="70" width="140" height="80" rx="10" fill="#1f6feb" filter="url(#shadow)"/>
  <text x="120" y="105" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">🧑 你（客户端）</text>
  <text x="120" y="125" text-anchor="middle" fill="#c2d9ff" font-size="11">n8n / 浏览器 / App</text>

  <!-- Arrow: Request -->
  <line x1="190" y1="110" x2="270" y2="110" stroke="#3fb950" stroke-width="2.5"/>
  <polygon points="270,104 282,110 270,116" fill="#3fb950"/>
  <text x="230" y="100" text-anchor="middle" fill="#3fb950" font-size="10">① 发请求</text>

  <!-- API Gateway -->
  <rect x="285" y="70" width="140" height="80" rx="10" fill="#6e40c9" filter="url(#shadow)"/>
  <text x="355" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">🔐 API 网关</text>
  <text x="355" y="115" text-anchor="middle" fill="#d2c6f2" font-size="10">验身份 / 限流 / 路由</text>
  <text x="355" y="132" text-anchor="middle" fill="#d2c6f2" font-size="10">🔑 API Key → 放行</text>

  <!-- Arrow: Forward -->
  <line x1="425" y1="110" x2="505" y2="110" stroke="#3fb950" stroke-width="2.5"/>
  <polygon points="505,104 517,110 505,116" fill="#3fb950"/>
  <text x="465" y="100" text-anchor="middle" fill="#3fb950" font-size="10">② 转发</text>

  <!-- Server -->
  <rect x="520" y="70" width="140" height="80" rx="10" fill="#da3633" filter="url(#shadow)"/>
  <text x="590" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">🖥️ 服务器</text>
  <text x="590" y="115" text-anchor="middle" fill="#ffd2d0" font-size="10">处理逻辑 / 查数据库</text>
  <text x="590" y="132" text-anchor="middle" fill="#ffd2d0" font-size="10">准备好数据 →</text>

  <!-- Arrow: Response back -->
  <line x1="590" y1="160" x2="590" y2="200" stroke="#f0883e" stroke-width="2.5"/>
  <line x1="590" y1="200" x2="120" y2="200" stroke="#f0883e" stroke-width="2.5"/>
  <polygon points="120,194 108,200 120,206" fill="#f0883e"/>
  <text x="355" y="195" text-anchor="middle" fill="#f0883e" font-size="10">③ 返回结果（JSON 数据）</text>

  <!-- Response detail box -->
  <rect x="50" y="240" width="700" height="130" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
  <text x="70" y="265" fill="#58a6ff" font-size="12" font-weight="bold">📦 返回的数据（JSON 格式）</text>
  <rect x="70" y="278" width="660" height="80" rx="6" fill="#161b22"/>
  <text x="90" y="298" fill="#7ee787" font-size="12" font-family="monospace">{</text>
  <text x="110" y="298" fill="#79c0ff" font-size="12" font-family="monospace">"status"</text>
  <text x="160" y="298" fill="#c9d1d9" font-size="12" font-family="monospace">:</text>
  <text x="170" y="298" fill="#a5d6ff" font-size="12" font-family="monospace">"success"</text>
  <text x="250" y="298" fill="#8b949e" font-size="11" font-family="monospace">← 状态：成功</text>
  <text x="90" y="318" fill="#79c0ff" font-size="12" font-family="monospace">"data"</text>
  <text x="125" y="318" fill="#c9d1d9" font-size="12" font-family="monospace">:</text>
  <text x="135" y="318" fill="#a5d6ff" font-size="12" font-family="monospace">{"temp": 22, "city": "北京"}</text>
  <text x="380" y="318" fill="#8b949e" font-size="11" font-family="monospace">← 实际数据</text>
  <text x="90" y="348" fill="#7ee787" font-size="12" font-family="monospace">}</text>
  <text x="110" y="348" fill="#8b949e" font-size="10" font-family="monospace">⬆ 温度 22°C，城市「北京」</text>

  <!-- Status codes section -->
  <text x="400" y="405" text-anchor="middle" fill="#c9d1d9" font-size="14" font-weight="bold">🔢 HTTP 状态码 = 服务员回话</text>

  <rect x="50" y="420" width="165" height="50" rx="6" fill="#1b3a1b" stroke="#3fb950" stroke-width="1"/>
  <text x="132" y="440" text-anchor="middle" fill="#3fb950" font-size="13" font-weight="bold">200 OK ✅</text>
  <text x="132" y="458" text-anchor="middle" fill="#7ee787" font-size="10">「好的，这是您要的数据」</text>

  <rect x="230" y="420" width="165" height="50" rx="6" fill="#3a1b1b" stroke="#da3633" stroke-width="1"/>
  <text x="312" y="440" text-anchor="middle" fill="#da3633" font-size="13" font-weight="bold">401 Unauthorized 🔒</text>
  <text x="312" y="458" text-anchor="middle" fill="#ff9999" font-size="10">「您没带钥匙（API Key 错了）」</text>

  <rect x="410" y="420" width="165" height="50" rx="6" fill="#3a2b1b" stroke="#f0883e" stroke-width="1"/>
  <text x="492" y="440" text-anchor="middle" fill="#f0883e" font-size="13" font-weight="bold">404 Not Found 🔍</text>
  <text x="492" y="458" text-anchor="middle" fill="#ffbb88" font-size="10">「菜单上没有这道菜」</text>

  <rect x="590" y="420" width="165" height="50" rx="6" fill="#2b1b3a" stroke="#bc8cff" stroke-width="1"/>
  <text x="672" y="440" text-anchor="middle" fill="#bc8cff" font-size="13" font-weight="bold">500 Server Error 💥</text>
  <text x="672" y="458" text-anchor="middle" fill="#ccbbff" font-size="10">「厨房炸了，不关你事」</text>

  <text x="400" y="500" text-anchor="middle" fill="#8b949e" font-size="10">状态码 2xx = 成功 · 4xx = 你的问题 · 5xx = 服务器的问题</text>
</svg>
```

---

## 常见场景速查卡

### 🟢 我想调一个接口，但不知道从哪下手

**三件套**：
1. 找到 API 文档（搜 `XXX API 文档`）
2. 找到 **Authentication**（认证）那章——看怎么拿 API Key
3. 找到你想要的那个接口——看它的 **Method**（GET/POST）、**URL**、**参数**

然后扔进 n8n 的 HTTP Request 节点 → Test → 看输出。

### 🟡 返回一堆英文，看不懂

九成情况，API 返回的数据是 **JSON 格式**。就是这种：

```json
{
  "name": "张三",
  "age": 30,
  "orders": [
    {"id": 1, "amount": 99},
    {"id": 2, "amount": 199}
  ]
}
```

**怎么看**：
- `"name": "张三"` → 字段名叫 name，值是张三
- `[ ... ]` → 这是一个列表，里面有多条
- 在 n8n 里用 `{{ $json.name }}` 取出「张三」

### 🔵 认证失败，提示 401

**排查顺序**：
1. API Key 复制对了吗？（有没有多空格？）
2. 放的位置对吗？（文档写的是 Header 还是 Query？）
3. API Key 有没有过期？（去服务商网站重新生成）
4. 是不是需要先"激活"？（有些 API 注册后要手动启用）

### 🟠 POST 请求不会搞

GET 是「给我数据」——参数拼在 URL 里。POST 是「提交数据」——参数放在 Body 里。

在 n8n 的 HTTP Request 节点：
1. Method 选 `POST`
2. Body 选 `JSON`
3. 填入你要提交的数据：
```json
{
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

### 🔴 报错 429 Too Many Requests

翻译：你**调太快了**，被限流了。

解决：
- 在 n8n 节点间加一个 **Wait** 节点，等 1-2 秒
- 或降低工作流的触发频率（Schedule Trigger 的间隔拉长）

---

## 快速参考表

| 我想干什么 | HTTP 方法 | 参数放哪 | 在 n8n 里怎么搞 | 或者对我说 |
|-----------|:---:|------|------|------|
| 获取数据 | **GET** | URL 问号后面 | HTTP Request → Method: GET → URL 填完整 | 「帮我调这个接口拿数据」 |
| 提交新数据 | **POST** | Body (JSON) | HTTP Request → Method: POST → Body 选 JSON | 「帮我把这个数据提交过去」 |
| 更新已有数据 | **PUT** / **PATCH** | Body (JSON) | 同上，Method 选 PUT 或 PATCH | 「帮我把这条数据更新了」 |
| 删除数据 | **DELETE** | URL 里 | Method: DELETE | 「帮我把这条记录删了」 |
| 带 API Key | — | Header | Headers → 加 `Authorization: Bearer xxx` | 「帮我加上认证信息」 |
| 传文件 | **POST** | Body (Form-Data) | Body → Form-Data → 选文件 | 「帮我把这个文件传上去」 |
| 分页获取 | **GET** | URL 参数 `?page=1` | 循环调，每次 page +1 | 「帮我把所有分页数据抓完」 |
| 测试一下通不通 | **GET** | — | 最简单的 GET 先试，看状态码 | 「帮我测一下这个接口」 |

---

## 认证三件套（最常见的三种验身份方式）

### 方式一：API Key（最普遍）

在 URL 参数里或 Header 里带一把"钥匙"。

```
# Header 方式（推荐）
Authorization: Bearer sk-xxxxxxxxxxxx

# URL 参数方式（部分服务用）
https://api.xxx.com/data?api_key=xxxxxxxx
```

**在 n8n 里**：HTTP Request 节点 → Headers → 加一行 `Authorization` → Value 填 `Bearer 你的Key`

### 方式二：Basic Auth（老派但常见）

用户名 + 密码，Base64 编码后放 Header。

**在 n8n 里**：HTTP Request 节点 → Authentication → 选 `Basic Auth` → 填用户名和密码。n8n 自动帮你编码。

### 方式三：OAuth 2.0（最安全、最复杂）

你不直接拿到 Key，而是弹出一个授权页面（比如「是否允许 XXX 访问你的 Google 账号？」），点同意后自动拿到临时令牌。

**在 n8n 里**：左侧栏 Credentials → 添加 → 搜对应服务（如 Google、Notion）→ 按引导完成授权。这是 n8n 的强项——帮你处理了 OAuth 的复杂握手。

---

## 新手常见困惑（FAQ）

### Q1：什么是 REST API？和 API 是一回事吗？
**API 是大类，REST 是其中最流行的一种风格**。就像「车」是大类，「轿车」是一种。你遇到的大多数 Web API（90%+）都是 REST 风格——用 GET/POST/PUT/DELETE，返回 JSON。

### Q2：JSON 是什么？为什么 API 都返回这个？
JSON = JavaScript Object Notation，一种**人和机器都能看懂的数据格式**。长这样：
```json
{"name": "张三", "age": 30}
```
XML 是它爸（老一辈的格式），JSON 是它儿子（更简洁）。现在 API 基本都用 JSON。

### Q3：GET 和 POST 到底什么区别？
**GET**：问服务员「菜单上第三道菜多少钱？」——只看不碰。可以重复问无数次，不会改变任何东西。
**POST**：跟服务员说「帮我加一道菜」——会产生变化。重复发可能会创建多条记录。

**记住**：查数据用 GET，改数据用 POST/PUT。

### Q4：我怎么知道返回的数据里有什么？
看 API 文档的 **Response** 那一节。或者在 n8n 里先调一次，看 OUTPUT 面板——实打实看到数据长什么样，比读文档快。

### Q5：为什么有时候返回的数据和文档写的不一样？
三种可能：
1. API 更新了，文档没更新（常见）
2. 你的参数传错了，触发了不同的返回逻辑
3. 有些字段是"可选的"，只有特定条件下才出现

**先信实际返回的**，再对照文档。

### Q6：API 调用要钱吗？
**大部分有免费额度**。比如：
- GitHub API：未认证 60 次/小时，认证后 5,000 次/小时
- 高德地图 API：免费 5,000 次/天
- DeepSeek API：按 Token 收费，但极便宜（几毛钱几千次）
- OpenAI API：按 Token 收费，GPT-4o 较贵

**每次在 n8n 里调之前，去服务商网站看一眼定价和免费额度。**

### Q7：Webhook 和 API 是什么关系？
Webhook 是**反向 API**。
- API：你主动去问服务器「有消息吗？」
- Webhook：服务器主动推给你「有新消息了！」

就像一个是你每隔 5 分钟去门口看有没有快递（API），一个是快递员按门铃（Webhook）。n8n 里的 Webhook 节点就是用来接收这种"门铃"的。

### Q8：GraphQL 是什么？和 REST 有什么区别？
GraphQL 是 REST 的竞争对手。区别：
- REST：你要什么数据，服务器给什么（固定格式）。想要用户名？调 `/user`。想要用户订单？调 `/orders`。调两次。
- GraphQL：你一次说清楚要什么，服务器只给你那些。一次查询拿回用户名+订单。

对于 n8n 新手：**先学 REST，用到 99% 的场景。GraphQL 遇到了再说。**

---

## 🚀 进阶路线图

```
第 1 天：在浏览器地址栏直接访问一个公开 API，看返回的 JSON
    │
第 3 天：在 n8n 里用 HTTP Request 调通一个带 API Key 的接口
    │
第 1 周：理解 GET/POST/PUT/DELETE 四种方法，各调一次
    │
第 2 周：处理分页（一页一页抓数据）、理解认证三件套
    │
第 1 月：能独立阅读任何 API 文档，15 分钟内调通
    │
第 3 月：在 n8n 里搭复杂工作流，串联 3-5 个不同的 API
```

---

## 来源汇总

- API 管理市场规模 ~$8B（2026）：https://ztabs.co/statistics/api-economy
- REST/GraphQL/gRPC 对比 2026：https://medium.com/@sizanmahmud08/the-complete-guide-to-api-types-in-2026
- Kong API 趋势报告 2026：https://konghq.com/blog/engineering/api-a-rapidly-changing-landscape
- GitHub API 文档：https://docs.github.com/en/rest
- REST API 设计最佳实践：https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/

---

*手册版本：v1.0 | 生成日期：2026-05-13 | 军师祭酒*
