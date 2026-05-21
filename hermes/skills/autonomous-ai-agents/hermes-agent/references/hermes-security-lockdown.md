# Hermes 安全加固检查单

> 适用场景：供应链攻击披露后、新安装 Hermes 后、定期安全审计。
> 来源：2026-05-15 MistralAI PyPI 投毒事件后的实战加固。

## 三步锁定

### 第一步：开启运行时脱敏（30秒）

```bash
hermes config set security.redact_secrets true
hermes config set privacy.redact_pii true
```

**验证：**
```bash
grep "redact" ~/.hermes/config.yaml
# 应显示：redact_secrets: true / redact_pii: true
```

**注意：** 需要重启 Hermes Gateway 或新开 CLI 会话才能生效。`redact_secrets` 在进程启动时快照，运行中修改不生效。

**为什么重要：** 关闭状态下，终端输出、日志、会话记录中可能泄露 API Key。2026-05-15 实测发现用户 config.yaml 中 `redact_secrets: false`，导致 grep 命令直接在终端回显中暴露了明文 Key。

---

### 第二步：锁定依赖版本（2分钟）

```bash
# 生成精确版本清单
pip freeze > ~/requirements-lock.txt

# 将清单复制到项目目录
cp ~/requirements-lock.txt /mnt/i/hermes/requirements-lock.txt
```

**进阶（可选）：加哈希校验**

```bash
# 用 pipx 安装 pip-tools（避免 PEP 668 限制）
pipx install pip-tools

# 生成带哈希的锁定文件
pip-compile --generate-hashes -o requirements-hash.txt requirements.in
```

**为什么重要：** Agent 自动化 `pip install` 不锁定版本，一旦恶意包撞上同名依赖，Agent 自动安装。精确版本锁定让攻击者无法通过版本号投毒。

**PEP 668 陷阱：** Ubuntu 系统 Python 阻止 `pip install pip-tools`。用 `pipx install pip-tools` 绕过。

---

### 第三步：清理密钥副本（1分钟）

Hermes 升级前自动备份 `~/.hermes/state-snapshots/`，每次备份包含完整 `.env` 文件。

```bash
# 查看快照数量
ls ~/.hermes/state-snapshots/

# 保留最近1份，删除其余
# 示例：保留 20260511-002959-pre-update
ls -t ~/.hermes/state-snappoints/ | tail -n +2 | xargs -I {} rm -rf ~/.hermes/state-snapshots/{}
```

**为什么重要：** 2026-05-15 实测发现 6 份快照各含 20KB 的完整 `.env` 文件（74 个 KEY/TOKEN/SECRET 变量）。一个供应链攻击的 credential stealer 可以遍历所有快照目录，一次窃取全部历史密钥。

---

## 补充检查

### 恶意包自查

```bash
# 检查指定恶意包
python -m pip show mistralai 2>/dev/null && echo "⚠️  INSTALLED" || echo "✅ clean"

# 检查恶意 payload 文件
ls -la /tmp/transformers.pyz 2>/dev/null && echo "⚠️  FOUND" || echo "✅ clean"

# 检查 C2 连接
sudo ss -tunap 2>/dev/null | grep '83.142.209.194' && echo "⚠️  CONNECTED" || echo "✅ clean"
```

### 环境变量暴露面审计

```bash
# 统计 .env 中的密钥数量
grep -c "KEY\|TOKEN\|SECRET" ~/.hermes/.env

# 检查 config.yaml 中的明文 Key（redact_secrets 开启后应被自动脱敏）
grep -n "api_key\|token\|secret" ~/.hermes/config.yaml | grep -v "^#" | grep -v "''" | wc -l
```

---

## 已知陷阱

1. **`hermes config set security.redact_secrets true` 写入成功但不生效** — 需要重启进程。这是设计特性，防止 LLM 运行时关闭自己的脱敏。
2. **快照删除后无法回滚到旧版本** — 保留最近 1 份作为回滚锚点。
3. **PEP 668 阻止系统 pip 安装包** — 用 `pipx` 或 `--break-system-packages`（不推荐）。
4. **`pip freeze --require-hashes` 不存在** — 需要 `pip-tools` 的 `pip-compile --generate-hashes`。
