# 微信 iLink 机器人群聊限制

## 背景
2026-05-02 尝试为用户（张成市）妻子建立三人微信群（丈夫+妻子+Hermes机器人）时发现。

## 现象
设置 WEIXIN_GROUP_POLICY=open 并重启网关后，日志输出警告：
iLink bot identity (xxx@im.bot) cannot be invited into ordinary WeChat groups.

## 原因
Hermes 连接微信有两种方式：
1. **iLink Bot API**（当前配置）— 企业级接口，不支持被拉入普通微信群
2. **QR 扫码登录** — 模拟个人微信号，理论上支持群聊

## 替代方案
- Telegram 群聊（完全支持机器人入群）
- 微信各自私聊（用户妻子加机器人为好友）
- 转发模式
