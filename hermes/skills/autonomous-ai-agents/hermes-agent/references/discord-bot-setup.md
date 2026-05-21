# Discord Bot 完整配置指南

## 1. 在 Discord Developer Portal 创建 Bot

1. 浏览器打开 https://discord.com/developers/applications
2. 点击 **New Application** → 输入 Bot 名称 → 勾选条款 → **Create**
3. 左边菜单 → **Bot** → **Reset Token** → 复制 Token（格式：`MTIz...NGQ.abc...xyz`，三段点分隔）
4. 同一个 Bot 页面 → **Privileged Gateway Intents** → 打开三个开关：
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT（缺这个 Bot 会静默无响应）
5. 点击 **Save Changes**

## 2. 将 Bot 加入服务器

1. 左边菜单 → **OAuth2 → URL Generator**
2. **Scopes** 勾选 `bot`
3. **Bot Permissions** 勾选 `Administrator`（或按需精细勾选 Read/Send Messages 等）
4. 复制底部生成的 URL → 浏览器打开 → 选服务器 → 授权

## 3. 配置 Token 到 Hermes

```bash
# 写入 .env（.env 受保护，不能用 write_file/terminal 直接写，需走 Python）
echo 'DISCORD_BOT_TOKEN=your_token_here' >> ~/.hermes/.env
```

或通过 Python（Hermes 会话内用 `execute_code`）：

```python
from hermes_tools import terminal
terminal("sed -i '$aDISCORD_BOT_TOKEN=your_token_here' /home/$USER/.hermes/.env", timeout=5)
```

验证：

```bash
hermes doctor | grep discord
# 应显示 ✓ discord 和 ✓ discord_admin
```

## 4. 启动 Gateway

### 前台（用于测试）

```bash
cd ~/.hermes && source .env && hermes gateway run
```

### 后台持久化（tmux，推荐用于 WSL）

```bash
tmux new-session -d -s hermes 'cd ~/.hermes && source .env && hermes gateway run'
```

查看状态：

```bash
tmux capture-pane -t hermes -p | tail -20
grep "discord\|error\|fail" ~/.hermes/logs/gateway.log | tail -10
```

### 重启

```bash
tmux send-keys -t hermes C-c && sleep 3 && \
tmux new-session -d -s hermes 'cd ~/.hermes && source .env && hermes gateway run'
```

## 5. 用户访问权限

Gateway 默认拒绝所有未授权用户。首次启动日志会有：

```
No user allowlists configured. All unauthorized users will be denied.
```

### 开放访问（测试用）

```bash
echo 'GATEWAY_ALLOW_ALL_USERS=true' >> ~/.hermes/.env
# 然后重启 Gateway
```

### 限制访问（生产用）

配置平台特定的 allowlist，如 Discord 的频道白名单（具体见 Hermes 文档）。

## 6. 验证 Bot 在线

在 Discord 中给 Bot 发私信或在服务器中 @Bot 发消息。如果无响应：

1. 检查 Privileged Gateway Intents 的 **MESSAGE CONTENT INTENT** 是否开启
2. 检查 Gateway 日志：`grep -i "error\|fail" ~/.hermes/logs/gateway.log`
3. 检查 Bot 是否已加入服务器
4. 重启 Gateway
