# API 深度技术手册 v1.0

> **适用对象**：开发者、技术团队、n8n 进阶用户 | **预计阅读**：50 分钟

---

## 第一章 概览与核心理念

### 1.1 什么是 API

API（Application Programming Interface，应用程序编程接口）是软件之间通信的**契约**。它定义了一个系统可以向另一个系统"要什么"、"怎么要"和"得到什么"。

**三层理解**：
- **抽象层**：API 屏蔽了内部实现细节，只暴露需要的操作（你不知道厨房怎么炒菜，只知道菜单上有什么）
- **契约层**：API 是一份承诺——"你按这个格式请求，我按这个格式返回"（API 文档 = 合同）
- **产品层**：现代 API 本身即是产品（Twilio 卖短信能力、Stripe 卖支付能力、OpenAI 卖 AI 能力——全部通过 API 交付）

### 1.2 API 简史

| 年代 | 里程碑 | 意义 |
|------|--------|------|
| 1990s | CORBA / DCOM | 最早的企业级接口，复杂且绑定语言 |
| 2000 | SOAP + WSDL | XML 时代的标准化 API，重量级 |
| 2000 | **Roy Fielding 提出 REST** | 博士论文中定义了 REST 架构风格 |
| 2005-2010 | REST + JSON 兴起 | Web 2.0 浪潮，轻量级替代 SOAP |
| 2012 | Twilio/Stripe 将 API 作为产品 | "API 经济"概念诞生 |
| 2015 | **GraphQL**（Facebook 开源） | 客户端精确控制返回数据 |
| 2016 | **gRPC**（Google 开源） | 高性能微服务间通信 |
| 2020+ | OpenAPI 3.0 标准化 | API 描述语言统一 |
| 2023+ | AI API（OpenAI/Anthropic） | API 不止传递数据，还传递"智能" |

### 1.3 API 经济的规模

| 指标 | 数据 |
|------|------|
| API 管理市场规模（2026） | ~$8B，年增速 25%+ |
| 全球公开 API 数量 | 24,000+（ProgrammableWeb 统计） |
| API 调用占比（互联网流量） | 83% 的互联网流量来自 API 调用（Akamai） |
| 企业 API 化率 | 90% 的大型企业已有 API 战略 |

数据来源：ZTABS API Economy Statistics 2026、Kong API Landscape Report 2026。

### 1.4 核心理念

> **API First**：先设计接口，再实现功能。这不是技术偏好，是一种组织哲学——让不同团队通过契约协作，而非通过会议。

---

## 第二章 API 协议全解

### 2.1 REST（Representational State Transfer）

**地位**：Web API 的事实标准，市场份额 80%+。

**核心原则**：
| 原则 | 含义 | 示例 |
|------|------|------|
| **资源导向** | 一切皆资源，用 URL 标识 | `/users/123` 就是「ID 为 123 的用户」 |
| **无状态** | 每个请求自包含，服务器不记上下文 | 每次请求都得带上认证信息 |
| **统一接口** | 用标准 HTTP 方法操作资源 | GET 读、POST 建、PUT 改、DELETE 删 |
| **表现层分离** | 资源可以有多种表现（JSON/XML/HTML） | 请求头指定 `Accept: application/json` |

**RESTful URL 设计规则**：

```
✅ 好的 RESTful URL：
GET    /users           → 获取用户列表
GET    /users/123       → 获取 ID 123 的用户
POST   /users           → 创建新用户
PUT    /users/123       → 更新 ID 123 的用户
DELETE /users/123       → 删除
GET    /users/123/orders → 获取该用户的订单

❌ 不好的设计：
GET /getUser?id=123     → 动词不该出现在 URL 里
POST /users/create      → 同上
GET /users?action=delete → 用 HTTP 方法，不要用参数
```

### 2.2 GraphQL

**定位**：让客户端精确控制返回数据。Facebook 2012 年开发，2015 年开源。

**核心理念**："Ask for what you need, get exactly that."

```graphql
# 一次查询，精确获取
query {
  user(id: 123) {
    name
    email
    posts(last: 3) {
      title
      createdAt
    }
  }
}
```

| 维度 | REST | GraphQL |
|------|------|---------|
| 端点数量 | 多个（每个资源一个） | **一个**（`/graphql`） |
| 返回数据 | 服务器决定（可能过多或过少） | **客户端精确指定** |
| 缓存 | HTTP 缓存原生支持 | 需要额外处理 |
| 学习曲线 | 低 | 中 |
| 适用场景 | 简单 CRUD、公开 API | 复杂数据关系、移动端 |

### 2.3 gRPC

**定位**：高性能微服务间通信。Google 开源，用 Protocol Buffers 序列化。

| 维度 | REST | gRPC |
|------|------|------|
| 数据格式 | JSON（文本） | Protocol Buffers（二进制） |
| 速度 | 基准线 | **快 3-10 倍** |
| 可读性 | 人可读 | 需要工具 |
| 流式传输 | 不支持 | **原生支持双向流** |
| HTTP 版本 | HTTP/1.1 | **HTTP/2** |
| 浏览器支持 | ✅ 原生 | ❌ 需要 gRPC-Web |
| 适用场景 | Web API | 微服务内部通信 |

### 2.4 协议选型决策树

```
需要浏览器直接调用？
  ├── 是 → 数据关系复杂需要灵活查询？
  │         ├── 是 → GraphQL
  │         └── 否 → REST
  └── 否 → 需要极高吞吐/低延迟？
              ├── 是 → gRPC
              └── 否 → REST
```

---

## 第三章 HTTP 基础：API 的语言

### 3.1 URL 解剖

```
https://api.example.com:443/v2/users/123?fields=name,email&lang=zh
│      │               │   │       │       │
协议    主机             端口 版本    资源路径  查询参数
```

| 组成部分 | 说明 |
|---------|------|
| 协议 | `http` 或 `https`（永远用后者） |
| 主机 | 域名或 IP |
| 端口 | HTTP 默认 80，HTTPS 默认 443（可省略） |
| 路径 | 版本号 + 资源层级（`/v2/users/123`） |
| 查询参数 | `?key=value&key2=value2` |

### 3.2 HTTP 方法

| 方法 | 含义 | 幂等性 | 请求体 |
|:---:|------|:---:|:---:|
| **GET** | 获取资源 | ✅ 是 | ❌ 无 |
| **POST** | 创建资源 | ❌ 否（多次调用创建多个） | ✅ 有 |
| **PUT** | 全量替换资源 | ✅ 是 | ✅ 有 |
| **PATCH** | 部分更新资源 | ❌ 不一定 | ✅ 有 |
| **DELETE** | 删除资源 | ✅ 是 | ❌ 通常无 |
| **HEAD** | 同 GET 但只返回头 | ✅ 是 | ❌ 无 |
| **OPTIONS** | 查询支持的方法 | ✅ 是 | ❌ 无 |

**幂等性** = 同样的请求发 10 次，结果和发 1 次一样。

### 3.3 HTTP 状态码

#### 2xx — 成功
| 状态码 | 含义 | 何时返回 |
|:---:|------|---------|
| 200 | OK | GET/PUT/PATCH 成功 |
| 201 | Created | POST 创建资源成功 |
| 204 | No Content | DELETE 成功，响应体为空 |

#### 4xx — 客户端错误（你的问题）
| 状态码 | 含义 | 排查方向 |
|:---:|------|---------|
| 400 | Bad Request | 请求格式不对（JSON 语法错、参数类型错） |
| 401 | Unauthorized | 没认证或 API Key 错/过期 |
| 403 | Forbidden | 认证了但没权限（Key 对，但权限不够） |
| 404 | Not Found | URL 路径错或资源不存在 |
| 429 | Too Many Requests | 被限流了，降低调用频率 |

#### 5xx — 服务器错误（服务器的问题）
| 状态码 | 含义 | 排查方向 |
|:---:|------|---------|
| 500 | Internal Server Error | 服务器代码异常 |
| 502 | Bad Gateway | 上游服务挂了 |
| 503 | Service Unavailable | 服务器过载或维护 |
| 504 | Gateway Timeout | 上游响应太慢，超时了 |

### 3.4 HTTP Headers 速查

| Header | 用途 | 示例 |
|--------|------|------|
| `Authorization` | 认证 | `Bearer sk-xxx` |
| `Content-Type` | 请求体格式 | `application/json` |
| `Accept` | 期望的响应格式 | `application/json` |
| `User-Agent` | 标识客户端 | `n8n/2.21.0` |
| `X-RateLimit-Remaining` | 剩余调用次数（响应头） | `994` |

### 3.5 Content-Type 常见值

| 值 | 用途 |
|------|------|
| `application/json` | JSON 数据（最常用） |
| `application/x-www-form-urlencoded` | HTML 表单格式 |
| `multipart/form-data` | 文件上传 |
| `text/plain` | 纯文本 |
| `application/octet-stream` | 二进制文件 |

---

## 第四章 实战：从零调用、解析、集成

### 4.1 选择一个公开 API 练手

**推荐练手 API**（无需认证，直接能调）：

| API | URL | 返回什么 |
|-----|-----|---------|
| GitHub Users | `https://api.github.com/users/{用户名}` | 用户信息 |
| 公开狗狗图 | `https://dog.ceo/api/breeds/image/random` | 随机狗狗照片 |
| JSONPlaceholder | `https://jsonplaceholder.typicode.com/posts/1` | 假数据 |
| icanhazdadjoke | `https://icanhazdadjoke.com/` | 随机冷笑话 |

### 4.2 用 curl 快速测试

```bash
# 最简单的 GET
curl https://api.github.com/users/zcs366

# GET + 自定义头
curl -H "Accept: application/json" \
     https://icanhazdadjoke.com/

# POST + JSON Body
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"title":"测试","body":"内容"}' \
     https://jsonplaceholder.typicode.com/posts

# 只看状态码
curl -o /dev/null -s -w "%{http_code}" https://api.github.com

# 看完整响应头
curl -I https://api.github.com
```

### 4.3 在 n8n 中调用

```
[Webhook] → [HTTP Request] → [Set] → [响应/存储]
                │
          Method: GET
          URL: https://api.github.com/users/zcs366
          Response Format: JSON
```

**n8n 中的常见操作**：

```javascript
// 在 Code 节点中处理 API 返回
const data = items[0].json;
const name = data.login;           // GitHub 用户名
const repos = data.public_repos;   // 公开仓库数

items[0].json = {
  user: name,
  repoCount: repos,
  fetchedAt: new Date().toISOString()
};
return items;
```

### 4.4 解析 JSON 响应

```json
{
  "login": "zcs366",
  "id": 12345,
  "public_repos": 15,
  "followers": 20,
  "created_at": "2020-01-01T00:00:00Z"
}
```

| 在 n8n 中取出... | 用这个表达式 |
|-----------------|-------------|
| 用户名 | `{{ $json.login }}` |
| 公开仓库数 | `{{ $json.public_repos }}` |
| 创建日期 | `{{ $json.created_at }}` |

---

## 第五章 认证与授权详解

### 5.1 认证 vs 授权

| 概念 | 问题 | 比喻 |
|------|------|------|
| **认证** (Authentication) | 你是谁？ | 出示身份证 |
| **授权** (Authorization) | 你能干什么？ | 身份证验证你有 VIP 权限 |

### 5.2 API Key（最简单）

```
# 请求中带 API Key 的三种方式

# 方式 1：Header（推荐）
Authorization: Bearer sk-xxxxxxxxxxxxxxx

# 方式 2：Query 参数
GET /api/data?api_key=xxxxxxxxxxxxxxx

# 方式 3：自定义 Header
X-API-Key: xxxxxxxxxxxxxxx
```

**n8n 配置**：HTTP Request → Headers → `Authorization: Bearer {你的Key}`

### 5.3 Basic Auth

```
# 原理：Base64(username:password)
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

**n8n 配置**：HTTP Request → Authentication → Basic Auth → 填用户名密码

### 5.4 OAuth 2.0（企业标准）

**流程**：
```
用户 → 你的应用 → 授权服务器(如 Google)
        │              │
        └── 重定向用户去登录 ──→
                        ←── 返回授权码
        │              │
        └── 用授权码换 Access Token ──→
                        ←── 返回 Token
        │
        └── 用 Token 调 API
```

**n8n 的优势**：内置 OAuth 2.0 支持，Credentials 中直接选服务商，自动处理 token 刷新。

### 5.5 JWT（JSON Web Token）

**结构**：`Header.Payload.Signature`

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEyM30.abc123def456
│                    │                  │
算法信息             用户数据（可解码）    签名（防篡改）
```

特点：**无状态**——Token 自身携带用户信息，服务器不需要查数据库。广泛用于微服务间认证。

---

## 第六章 进阶技术

### 6.1 分页（Pagination）

API 返回大量数据时，不会一次全给，而是分页。

**三种主流分页方式**：

| 方式 | URL 示例 | 适用场景 |
|------|---------|---------|
| **Offset-based** | `?offset=0&limit=20` | 简单场景，但数据变动时可能重复/遗漏 |
| **Page-based** | `?page=1&per_page=20` | 最直观，同上缺点 |
| **Cursor-based** | `?cursor=abc123` | Twitter/GitHub 用，数据变动也不乱 |

**在 n8n 里循环抓取分页数据**：

```
[HTTP Request (page=1)]
    │
    ▼
[IF: 还有下一页?]
    ├─ true → [HTTP Request (page=2)] → 循环
    └─ false → [汇总]
```

### 6.2 限流（Rate Limiting）

API 服务商会限制调用频率，防止滥用。

**识别限流**：
```
HTTP 429 Too Many Requests
Retry-After: 60    ← 告诉你等 60 秒
X-RateLimit-Remaining: 0   ← 额度用完了
```

**应对策略**：
1. **服从**：看 `Retry-After` 头，等到了再调
2. **主动减速**：n8n 节点间加 Wait 节点
3. **缓存**：相同请求不重复调 API
4. **升级套餐**：付费提额

### 6.3 Webhook（反向 API）

```
传统 API：你主动问「有新数据吗？」每隔 5 分钟问一次
Webhook：「有新数据了！」服务主动推给你
```

**n8n Webhook 配置**：
1. 添加 **Webhook** 节点 → 生成 URL
2. 把这个 URL 填到第三方服务的 Webhook 设置页
3. 第三方有事件时，自动 POST 到这个 URL
4. n8n 收到后继续执行后续节点

### 6.4 API 版本控制

| 方式 | 示例 | 优缺点 |
|------|------|--------|
| **URL 路径** | `/v2/users` | 最直观，推荐 |
| **Header** | `Accept: application/vnd.api.v2+json` | URL 干净但不易发现 |
| **Query 参数** | `/users?version=2` | 简单但不够 RESTful |

### 6.5 缓存策略

| Header | 作用 |
|--------|------|
| `Cache-Control: max-age=3600` | 缓存 1 小时 |
| `ETag: "abc123"` | 数据指纹，没变返回 304 |
| `Last-Modified: Wed, 21 Oct 2025` | 上次修改时间 |

---

## 第七章 工具生态与社区资源

### 7.1 API 测试工具

| 工具 | 适合人群 | 特点 |
|------|---------|------|
| **curl** | 开发者 | 命令行，最灵活，脚本友好 |
| **Postman** | 所有用户 | 图形界面，集合管理，自动生成代码 |
| **Insomnia** | 开发者 | 轻量替代 Postman，支持 GraphQL/gRPC |
| **HTTPie** | 开发者 | 比 curl 更易读的命令行工具 |
| **n8n HTTP Request 节点** | n8n 用户 | 直接集成到自动化流程 |

### 7.2 API 文档工具

| 工具 | 说明 |
|------|------|
| **OpenAPI (Swagger)** | REST API 描述标准，.yaml/.json 定义接口 |
| **Swagger UI** | OpenAPI 定义 → 交互式文档页面 |
| **Redoc** | OpenAPI 的另一种精美渲染 |
| **Readme.io** | 托管 API 文档平台 |
| **Postman Collections** | 导出 Postman 的测试集作为文档 |

### 7.3 学习资源

| 资源 | 适合人群 | 内容 |
|------|---------|------|
| [MDN Web Docs - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) | 所有人 | HTTP 最权威中文/英文参考 |
| [REST API Tutorial](https://restfulapi.net/) | 开发者 | REST 设计指南 |
| [JSONPlaceholder](https://jsonplaceholder.typicode.com/) | 新手 | 免费假数据 API，练手用 |
| [Public APIs](https://github.com/public-apis/public-apis) | 所有人 | GitHub 上 300K+ Star 的公开 API 合集 |
| [HTTP Status Codes](https://httpstatuses.io/) | 所有人 | 每个状态码的详细解释 |

---

## 第八章 API 设计与最佳实践

### 8.1 设计原则

| 原则 | 说明 |
|------|------|
| **API First** | 先设计 API 契约，再写代码实现 |
| **资源命名用名词复数** | `/users` 而非 `/getUser` |
| **版本化** | `/v2/users`，避免 breaking change 影响老用户 |
| **错误信息要可操作** | 不只说"错了"，还要说"怎么改" |
| **分页默认开启** | 任何列表接口都应该分页 |
| **始终使用 HTTPS** | HTTP 明文传输敏感信息 = 裸奔 |

### 8.2 好的 API 错误响应

```json
// ✅ 好的错误响应
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "参数 'email' 格式不正确",
    "details": [
      {
        "field": "email",
        "reason": "缺少 @ 符号",
        "hint": "正确格式: user@example.com"
      }
    ],
    "doc_url": "https://docs.example.com/errors#invalid-parameter"
  }
}
```

### 8.3 OpenAPI 3.0 示例

```yaml
openapi: "3.0.0"
info:
  title: 用户管理 API
  version: "2.0.0"
paths:
  /users/{userId}:
    get:
      summary: 获取用户信息
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

---

## 第九章 避坑指南

### 9.1 请求层

| 问题 | 现象 | 原因 | 修复 |
|------|------|------|------|
| 404 但 URL 看着对 | 请求返回 404 | URL 缺少尾部 `/` 或多了一个 | 细看 API 文档的示例 URL，逐字符对照 |
| JSON 解析失败 | `Invalid JSON` | Body 里有中文引号、注释、尾部逗号 | 用 JSON 校验工具检查；删掉注释（JSON 不支持注释）|
| 中文乱码 | 返回 `????` | Content-Type 没设 charset | Header 加 `Content-Type: application/json; charset=utf-8` |
| 证书错误 | `SSL certificate problem` | 自签名证书或用 HTTP 调 HTTPS | 开发阶段可用 `curl -k`，生产必须用有效证书 |

### 9.2 认证层

| 问题 | 现象 | 修复 |
|------|------|------|
| 401 反复出现 | 刚拿的 Key 就报 401 | ①检查复制时有无多余空格 ②确认 Header 名称（`Authorization` 注意拼写） ③确认 Bearer 前有空格 |
| OAuth Token 过期 | 之前能用，突然 401 | 检查 Token 有效期。n8n 凭据中 OAuth 会自动刷新，自定义的需手动处理 |
| API Key 泄露 | 提交到 GitHub 了 | ①立即在服务商后台吊销旧 Key ②生成新的 ③用环境变量存 Key，永远不要硬编码 |

### 9.3 性能与稳定性

| 问题 | 现象 | 修复 |
|------|------|------|
| 被限流 | 429 | 降低频率，加 Wait 节点，读 `Retry-After` |
| 超时 | 请求一直转圈 | 调大超时（n8n 节点 Settings → Timeout），或换更快接口 |
| 网络问题重试 | 偶发失败 | 开启节点重试：`retryOnFail: true, maxTries: 3, waitBetweenTries: 5000` |
| 生产环境调测试 API | 扣了真钱 / 发了真邮件 | 用 Sandbox/Test 环境。Stripe/PayPal 等都有测试模式 |

---

## 第十章 API 安全

### 10.1 十大安全实践

1. **强制 HTTPS**：绝不通过 HTTP 传输敏感数据
2. **用 Token 而非密码**：API Key/OAuth Token，不要用用户密码做认证
3. **最小权限**：每个 API Key 只给必需的权限
4. **短期 Token + 刷新**：Access Token 有效期 15 分钟-1 小时
5. **限流防滥用**：防止单个客户端打垮服务
6. **输入校验**：永远不信任客户端传过来的数据
7. **日志但不记录敏感信息**：不要 log API Key 和密码
8. **CORS 配置**：只允许已知域名跨域访问
9. **API 网关**：统一认证、限流、路由
10. **定期轮换 Key**：每 90 天换一次

### 10.2 常见攻击与防御

| 攻击 | 原理 | 防御 |
|------|------|------|
| 中间人攻击 | HTTP 明文传输被截获 | **只用 HTTPS** |
| API Key 泄露 | Key 暴露在 URL/日志/Git | Header 传 Key + 环境变量 |
| 重放攻击 | 截获请求重发 | 加时间戳 + nonce |
| DDoS | 大量请求打死服务 | API 网关限流 + CDN 缓存 |

---

## 第十一章 未来展望

### 11.1 AI Native API 成为新范式

传统 API 返回数据。AI API 返回**判断、生成、推理**。

OpenAI 的 API 开创了一个新品类：输入自然语言，输出智能结果。这不是数据传输，是**能力传输**。2025 年，Anthropic、Google、DeepSeek、Meta 全部跟进——AI API 已经从"一个功能"变成"一个赛道"。

对 API 设计的影响：
- 传统 API 需要精确的参数和固定的返回格式
- AI API 接受模糊的自然语言输入，返回结构性输出（Function Calling / Structured Output）
- 这催生了 **MCP（Model Context Protocol）**——AI 调用 API 的标准化协议，让 AI 能动态发现和调用任何 API

### 11.2 API 即产品：从技术层到商业层

Stripe 证明了"API 可以是公司唯一的界面"。Twilio 证明了"你不需要做 App，只卖 API 就能值百亿"。

趋势：**每个 SaaS 都会成为 API 供应商**。Notion、Figma、Canva 都有了自己的 API——不是因为它们想做平台，而是因为用户要求。

2026 年，一个新的 SaaS 产品如果发布时没有 API，会被视为"不完整"。

### 11.3 GraphQL 与 REST 的长期共存

GraphQL 没有像一些人预测的那样"取代 REST"。二者的使用场景正在分化：
- REST：公开 API、简单 CRUD、缓存友好场景
- GraphQL：内部复杂数据查询、移动端 App（省流量）

预言：**REST 不会消失，但会退守到简单场景；GraphQL 会继续在复杂领域增长；gRPC 将统治微服务内部通信。**

### 11.4 "无 API"的悖论

AI Agent（如 n8n 的 AI Agent 节点）正在创造一种新可能：**用户不需要知道 API 存在，只需要描述意图**。

但这不意味着 API 在消失。恰恰相反——每个 AI Agent 的每一步操作，都在底层调用 API。只是用户层不再看到它们。

这是一个有趣的悖论：**API 总量在爆发式增长，而普通用户对 API 的感知在趋向于零。**

---

## 附录：术语表

| 中文 | English | 说明 |
|------|---------|------|
| 应用程序接口 | API | 软件间的通信契约 |
| 表述性状态传递 | REST | 最流行的 Web API 架构风格 |
| 端点 | Endpoint | API 的具体访问地址 |
| 请求 | Request | 客户端发给 API 的消息 |
| 响应 | Response | API 返回的消息 |
| 负载 | Payload | 请求/响应中携带的数据 |
| 状态码 | Status Code | 3 位数字表示请求结果（200/404/500 等） |
| 请求头 | Header | 请求/响应的元数据 |
| 认证 | Authentication | 验证调用者身份 |
| 授权 | Authorization | 控制调用者的操作权限 |
| API 密钥 | API Key | 一种简单的认证方式 |
| 开放授权 | OAuth 2.0 | 行业标准的授权协议 |
| JSON | JSON | API 最常用的数据格式 |
| GraphQL | GraphQL | 客户端精确控制返回数据的查询语言 |
| gRPC | gRPC | Google 的高性能 RPC 框架 |
| 开放 API 规范 | OpenAPI (Swagger) | API 描述标准 |
| 限流 | Rate Limiting | 限制单位时间内的请求次数 |
| 分页 | Pagination | 将大量结果分批返回 |
| Webhook | Webhook | 反向 API——服务器主动推送 |
| 幂等性 | Idempotency | 多次相同请求结果一致 |
| 跨域资源共享 | CORS | 控制跨域请求的安全机制 |
| 缓存 | Caching | 存储响应副本以减少重复请求 |
| 内容分发网络 | CDN | 加速静态内容分发的网络 |
| 协议缓冲区 | Protocol Buffers | gRPC 的二进制序列化格式 |
| 模型上下文协议 | MCP | AI 调用 API 的标准化发现协议 |
| 软删除 | Soft Delete | 标记删除而非物理删除 |

---

## 参考文献

1. Fielding, R. T. (2000). Architectural Styles and the Design of Network-based Software Architectures. (REST 博士论文)
2. ZTABS API Economy Statistics 2026: https://ztabs.co/statistics/api-economy
3. Kong API Landscape Report 2026: https://konghq.com/blog/engineering/api-a-rapidly-changing-landscape
4. MDN Web Docs - HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP
5. OpenAPI Specification 3.0: https://spec.openapis.org/oas/v3.0.3
6. REST/GraphQL/gRPC Comparison 2026: https://devstarsj.github.io/2026/03/17/graphql-vs-rest-vs-grpc-comparison-2026/
7. Google Cloud API Design Guide: https://cloud.google.com/apis/design
8. Stripe API Reference（API 设计的黄金标准）: https://stripe.com/docs/api
9. GitHub REST API: https://docs.github.com/en/rest
10. Public APIs List: https://github.com/public-apis/public-apis

---

*手册版本：v1.0 | 生成日期：2026-05-13 | 军师祭酒*
