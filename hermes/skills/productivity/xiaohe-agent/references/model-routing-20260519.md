# 模型路由配置 · 2026年5月19日

> 军师 zcs 确立 · 萧何执行

## 三层模型架构

| 层 | 谁在用 | 模型 | 时段 | 成本模式 |
|---|--------|------|------|---------|
| 战略层 | 军师（主AI） | DeepSeek V4 Flash | 全天 | 按量计费，$0.14/$0.28 per M |
| 攻坚层 | 全部子代理 | MiMo V2.5 Pro | 08:00→24:00 | Token Plan Max（659元/月，2x credits） |
| 优惠层 | 全部子代理 | MiMo V2.5 非Pro | 00:00→08:00 | Token Plan Max（1x credits × 0.8非高峰期系数） |

## 自动切换

两枚 no_agent cron 守护：
- `d4a0d4d50788` — 00:00 切到 non-Pro
- `be8644bd8d5d` — 08:00 切到 Pro

切换脚本：`~/.hermes/scripts/switch_delegation_model.py`
切换日志：`~/.hermes/logs/model_switch.log`

## 补充信息

- 非高峰期（00:00→08:00）全系列模型 0.8x 系数消耗
- TTS 系列模型限时免费使用
- AI Basecamp Claude 已彻底清除，不再使用

## config.yaml 关键配置

```yaml
model:
  default: deepseek-v4-flash           # 军师
  provider: deepseek

providers:
  xiaomi:                               # MiMo Token Plan
    base_url: https://token-plan-cn.xiaomimimo.com/v1
    api_key: tp-cff...v1si

delegation:
  model: mimo-v2.5-pro                  # 子代理（白天）
  provider: xiaomi
```
