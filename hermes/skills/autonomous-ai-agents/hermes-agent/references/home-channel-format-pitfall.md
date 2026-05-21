# Home Channel 格式陷阱 — Gateway 崩溃排查

## 症状

`hermes gateway status` 显示 `activating (auto-restart)` 循环：

```
Active: activating (auto-restart) (Result: exit-code) since ...
Main PID: XXXX (code=exited, status=1/FAILURE)
```

journalctl/gateway.log 报 `TypeError: string indices must be integers, not 'str'`：

```
TypeError: string indices must be integers, not 'str'
  File ".../gateway/config.py", line 212, in from_dict
    platform=Platform(data["platform"]),
```

## 根因

Hermes Agent v0.13.0 起，`home_channel` 配置格式从**裸字符串**改为**字典结构**。

### ❌ 错误的格式（前代遗留/手动编辑导致）

```yaml
# platforms 下某平台
feishu:
  enabled: true
  extra:
    app_id: cli_xxx
    app_secret: xxx
  home_channel: oc_xxxxx    # ← 裸字符串导致 crash
```

### ✅ 正确的格式

```yaml
feishu:
  enabled: true
  extra:
    app_id: cli_xxx
    app_secret: xxx
  home_channel:
    platform: feishu        # 平台标识（字符串，小写）
    chat_id: oc_xxxxx       # 聊天/频道 ID（字符串）
```

## 排查命令

```bash
# 1. 检查所有 home_channel 条目
grep -n "home_channel" ~/.hermes/config.yaml

# 2. 确认哪些是裸字符串（无缩进 platform: / chat_id: 的子条目）
# 合法的条目应有 platform: 子字段

# 3. 检查 gateway 日志
grep "TypeError.*string indices" ~/.hermes/logs/gateway.log | tail -5

# 4. journalctl 完整回溯
journalctl --user -u hermes-gateway --no-pager -n 30 | grep -A 30 "Traceback"
```

## 修复 + 重启

```bash
# 修复 config.yaml 中对应条目后：
systemctl --user reset-failed hermes-gateway    # 清除失败状态
hermes gateway restart                           # 重启（会自动刷新 unit）
# 或：
systemctl --user restart hermes-gateway
```

## 验证

```bash
systemctl --user status hermes-gateway --no-pager -n 5
# 应显示:
#   Active: active (running) since ...
# 不再有 auto-restart 循环
```

## 常见变体

- 同报错、不同平台：检查 `discord.`、`telegram.`、`yuanbao.`、`weixin.` 下的 `home_channel`
- 如果某平台原本就没有 home_channel，可能是 gateway 升级后自动补了一个空串，也需要修正
- **升级后触发**：`hermes update` 后 config 格式变更未自动迁移，需手动检查 `home_channel` 字段
