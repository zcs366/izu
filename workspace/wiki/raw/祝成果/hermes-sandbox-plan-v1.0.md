# Hermes 沙箱容器 · 设计与实现方案 v1.0

> 要想走得快，一个人走。要想走得远，一起走。要想敢走险路，得有另一匹马。
> —— 沙箱就是那匹替你先踩地雷的马。

## 一、为什么需要沙箱

### 1.1 痛点

Hermes 已在生产环境稳定运行。但 AGI 时代的 Agent 进化逻辑是：

```
Agent 写代码 → Agent 改自己的 prompt → Agent 改自己的 system → Agent 优化自己
```

这条链上的每一步，都有可能搞崩正在运行的系统。没有沙箱，你永远不敢让 Agent 动自己的配置。

### 1.2 价值

| 能力 | 没有沙箱 | 有沙箱 |
|------|---------|--------|
| Agent 自修改 | 不敢，怕崩 | 随便试，炸了重开 |
| prompt 优化闭环 | 手动改+测试 | Agent 自改自测 |
| 新技能训练 | 只能读文档 | 可以直接运行 |
| 多 Agent 通信协议测试 | 干扰生产 | 完全隔离 |
| 危险配置实验 | 绝对不能做 | 授权后可做 |

### 1.3 核心设计原则

```
┌─────────────────────────────────────────────┐
│              生产环境 Hermes                    │
│   ┌─────────────────────────────────────┐    │
│   │   config (R/W)  │  skills (R/W)    │    │
│   │   workspace (R/W) │  cron (R/W)    │    │
│   └─────────────────────────────────────┘    │
│                    ▲ 隔离层                    │
│                    │ 绝不交叉                   │
│   ┌─────────────────────────────────────┐    │
│   │         沙箱 Hermes (Docker)          │    │
│   │   sandbox-config (R/W)             │    │
│   │   sandbox-workspace (R/W)          │    │
│   │   生产代码 (RO mount 或 git clone)   │    │
│   └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## 二、实现方案

### 2.1 镜像构建

利用 Hermes 仓库自带的 Dockerfile 作为基底，添加沙箱专属层：

```dockerfile
FROM hermes-hermes-agent:latest  # 或从源码构建

# 沙箱专用配置注入
COPY sandbox-config.yaml /home/hermes/.hermes/config.yaml
COPY sandbox.env /home/hermes/.hermes/.env

# 沙箱工作区
RUN mkdir -p /home/hermes/sandbox/workspace \
             /home/hermes/sandbox/skills \
             /home/hermes/sandbox/logs

# 非 root 用户运行
USER hermes

# 默认入口：Hermes CLI 但不自动连接 gateway
CMD ["hermes", "chat", "--personality", "sandbox"]
```

### 2.2 沙箱配置（sandbox-config.yaml）

生产 config 的**安全子集**：

```yaml
model:
  default: deepseek-chat          # 用最便宜的模型做实验
  provider: deepseek
  base_url: https://api.deepseek.com/v1

agent:
  max_turns: 30                   # 减半，避免实验跑飞
  gateway_timeout: 300

toolsets:
  - hermes-cli
  - terminal                      # 允许执行命令，但受容器限制

# ❌ 不启用 gateway — 沙箱不连接外部分发渠道
# gateway:
#   enabled: false

# ❌ 不启用 cron — 沙箱不跑定时任务
# cron:
#   enabled: false

# 实验授权模式
sandbox:
  permissions:
    default: deny                 # 默认拒绝所有写操作
    approval_channel: weixin      # 授权走微信
    approval_timeout: 300         # 5分钟不回复则默认拒绝
    write_paths_whitelist:
      - /home/hermes/sandbox/*    # 只允许写沙箱目录
```

### 2.3 授权令牌机制

实验操作需要写权限时，沙箱 Agent 的行为：

```
沙箱尝试写入 /home/hermes/sandbox/experiment.py
  → 权限引擎拦截
  → 通过微信推送：「[[沙箱]] 请求授权：写入 experiment.py (1.2KB)，用途：测试 self-modify 能力」
  → 用户回复「允许」或「拒绝」或「允许本次」
  → 授权令牌有效期：1 分钟 / 仅本次 / 本次session
  → 超时不回复 = 默认拒绝
```

技术实现：用 Hermes Gateway 的 webhook 回传 + 微信通道做审批面板。

### 2.4 启动脚本

```bash
# 构建镜像
docker build -t hermes-sandbox ~/.hermes/hermes-agent/

# 启动沙箱
docker run -it --rm \
  --name hermes-sandbox \
  -v ~/.hermes/sandbox-config.yaml:/home/hermes/.hermes/config.yaml:ro \
  -v ~/.hermes/.env:/home/hermes/.hermes/.env:ro \
  -v /mnt/i/hermes/sandbox:/home/hermes/sandbox \
  --network host \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  hermes-sandbox

# 一键快速启动（别名化后）
alias hermes-sandbox='docker start -ai hermes-sandbox 2>/dev/null || docker run -it --rm --name hermes-sandbox ...'
```

### 2.5 搞崩恢复流程

```
1. Agent 自修改搞到连提示符都不出了
   → docker stop hermes-sandbox
   → docker rm hermes-sandbox
   → 重新运行启动命令（自动用干净配置和保留的 workspace）
   → 耗时 < 3 秒

2. workspace 里保留了上一次实验的产出
   → 可以复盘：炸之前做了什么？
   → 也可以：docker run 时挂载旧 workspace 到一个新容器里

3. 恢复后自动推送一条消息
   → 「沙箱已重生，上次实验因[原因]终止。保留的产物在 sandbox/experiment-20260516/」
```

## 三、实验场景规划

### 3.1 Agent 自我改写（核心场景）

```python
# 沙箱里的 Agent 想做的事情：
1. 读取自己的 system prompt
2. 分析哪些提示词效果不好
3. 修改 system prompt 并保存
4. 重启自己的 session 验证效果
5. 如此循环直到收敛
```

安全边界：只能改 sandbox 目录内的配置，改不了生产配置。

### 3.2 多 Agent 通信协议测试

在沙箱里启动多个 Hermes 实例（不同容器），测试：

- Agent 之间的消息路由
- 信息格式协议（JSON schema）
- 共识达成机制
- 冲突解决策略

### 3.3 Prompt 对抗训练

```
沙箱 A（攻击方）：试图绕过安全限制
沙箱 B（防御方）：试图守住安全限制
两人对抗 → 安全防线越来越强
```

### 3.4 Agent 技能自生成

- 给沙箱一个任务：「为 izu 系统创建一个数据分析技能」
- 沙箱自己写 SKILL.md 和实现代码
- 测试通过后，申请导出到生产环境

## 四、与现有系统关系

| 维度 | 生产 Hermes | 沙箱 Hermes |
|------|------------|------------|
| 代码 | 同一份 | 镜像内的同一份或 git clone |
| 配置 | ~/.hermes/config.yaml | ~/.hermes/sandbox-config.yaml |
| Gateway | 全平台连接 | 仅审批通道（微信） |
| Cron | 运行中 | 不启用 |
| Skills | 所有已安装技能 | 一个精简集 + 实验技能 |
| Workspace | I:/hermes/ | I:/hermes/sandbox/ |
| 搞崩代价 | 服务中断 | 重启容器 |

## 五、实施路径

### Phase 1（当日可完成）— MVP 沙箱

1. 基于现有 Dockerfile 构建 Hermes 镜像
2. 编写 sandbox-config.yaml（精简配置）
3. 编写启动脚本 + 别名
4. 验证：能在沙箱里跑 `hermes chat` 并正常调用 API

### Phase 2（1-2 天）— 授权机制

5. 在沙箱里实现权限拦截层
6. 对接微信通道做审批面板
7. 实现令牌超时自动回收

### Phase 3（3-5 天）— 实验工作流

8. Agent 自我改写闭环实验
9. 实验产物导出到生产的流程
10. 搞崩自恢复 + 日志复盘

## 六、成本估算

| 项目 | 成本 | 备注 |
|------|------|------|
| Docker 镜像 | ¥0 | 本地构建 |
| API 调用 | ~¥2-5/天 | 实验性质，用量远低于生产 |
| 存储 | ¥0 | 本地磁盘 |
| 人力 | 1-2 小时 Setup | 之后自动运行 |

---

> **军师按：** 沙箱做出来后，Hermes 系统就从「一架飞机」变成了「有人叫他开、他先试试、试好了再正式飞」。这是从工具到生命体的关键一步。
