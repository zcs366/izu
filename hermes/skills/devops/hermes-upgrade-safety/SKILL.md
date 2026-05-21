---
name: hermes-upgrade-safety
description: "Hermes Agent 升级安全检查清单 — 升级前审查release notes、备份、评估冲突；升级后自动补丁、验证。遵循「薄定制、紧跟上游、升级前必审、宁可慢半拍」策略。"
version: 1.1.0
metadata:
  hermes:
    category: devops
author: Hermes Agent
---

# Hermes 升级安全检查清单

## 升级防护盾（自动化替代方案）

除了手动执行下方分步清单外，**推荐先用升级防护盾工具自动化快照+diff**：

```bash
# Step 0a: 升级前拍快照（一次命令记录全部136+个skills和配置）
python3 /mnt/i/hermes/izu/izu_hermes_upgrade_guard.py snapshot

# 然后正常升级
pip install --upgrade hermes-agent

# Step 0b: 升级后检查diff
python3 /mnt/i/hermes/izu/izu_hermes_upgrade_guard.py check
```

`izu_hermes_upgrade_guard.py` 自动检测：
- Hermes版本变化（old → new）
- 全部skills的增减和内容变化（行数/frontmatter字段/hash）
- 配置文件修改时间变化

**防护盾不能替代下面完整清单的手动审查环节**（release notes审读、冲突评估），但能快速告诉你「哪些东西变了、要不要人工介入」。

---

## 核心策略

> **薄定制、紧跟上游、升级前必审、宁可慢半拍不跟残次品。**

- 不分家（fork），保持主线跟踪
- 定制最小化：新增文件不删上游文件，只做最少必要修改
- 节奏：一个版本稳定跑两周再考虑升级，不追周更
- **升级路径：v0.14.0+ 用 `pip install --upgrade hermes-agent`（PyPI 包）。v0.14.0 之前的老版本仍用 `git pull && pip install -e .`**
- 当前定制清单：`tools/bing_search_tool.py`(新增) + `toolsets.py`(两行补丁)

---

## 升级流程（按顺序执行）

### Phase 1: 升级前审查

**Step 1 — 查看当前状态**
```bash
hermes --version
pip show hermes-agent 2>/dev/null || echo "非 pip 安装"
git -C ~/.hermes/hermes-agent log --oneline -5 2>/dev/null || echo "非 git 安装"
git -C ~/.hermes/hermes-agent diff --stat 2>/dev/null
```

**Step 2 — 拉取官方最新 release notes**
```bash
# 如果从 pip 安装，直接搜 GitHub release
web_search "Hermes Agent v latest release 2026"

# 如果从 git 安装
git -C ~/.hermes/hermes-agent fetch --tags
LATEST_TAG=$(git -C ~/.hermes/hermes-agent tag --sort=-creatordate | grep '^v20' | head -1)
echo "Latest: $LATEST_TAG"

# 读取 release notes
curl -sL "https://raw.githubusercontent.com/NousResearch/hermes-agent/${LATEST_TAG}/RELEASE_${LATEST_TAG}.md" | head -300
```

**Step 3 — 冲突评估（重点检查项）**
- `toolsets.py` — `_HERMES_CORE_TOOLS` 列表结构是否变化？新增/删除工具？
- `tools/registry.py` — 工具注册机制是否改动？
- `config.yaml` schema — 是否有新增/废弃的配置项？
- 关键架构文件：`run_agent.py`、`model_tools.py`、`cli.py`

```bash
# Diff 关键文件（当前 vs 新版本）
git -C ~/.hermes/hermes-agent diff HEAD..."${LATEST_TAG}" -- toolsets.py tools/registry.py hermes_cli/config.py | head -100
```

**Step 4 — 全面备份**
```bash
# 使用 hermes-user-data-pack 一键备份
hermes-user-data-pack
# 或手动：
cp -r ~/.hermes/config.yaml ~/.hermes/.env ~/.hermes/skills/ ~/.hermes/sessions/ ~/.hermes/backups/pre-upgrade-$(date +%Y%m%d_%H%M%S)/
```

**Step 5 — 暂存本地改动**
```bash
cd ~/.hermes/hermes-agent
git stash push -m "pre-upgrade: $(date +%Y%m%d)" -- toolsets.py
# 注意: tools/bing_search_tool.py 是 untracked file，git stash 不影响它
```

### Phase 2: 执行升级

**Step 6 — 升级（根据安装方式选择）**

```bash
# 方式 A（推荐，v0.14.0+ PyPI 包）：
pip install --upgrade hermes-agent

# 方式 B（git 安装的老版本）：
cd ~/.hermes/hermes-agent && git pull && pip install -e .
```

**升级后验证新版本号：**
```bash
hermes --version
pip show hermes-agent 2>/dev/null | grep Version
```

### Phase 3: 升级后验证

**Step 7 — 运行自动补丁脚本**
```bash
bash ~/.hermes/scripts/post-update-patches.sh
```

**Step 8 — 验证核心功能**
```bash
# 1. 版本确认
hermes --version

# 2. 工具注册确认
grep -c "bing_search" ~/.hermes/hermes-agent/toolsets.py
# 预期输出: 2（两处都有）

# 3. 健康检查
hermes doctor

# 4. 确认 bing_search 工具可用
# 启动一个新 session，用 /skill bing-search 或直接调用 bing_search
```

**Step 9 — Gateway 重启（如果使用中）**
```bash
systemctl --user restart hermes-gateway
systemctl --user status hermes-gateway
```

**Step 10 — 最终确认**
```bash
# 检查无残留冲突
git -C ~/.hermes/hermes-agent status
# 预期: 只有 tools/bing_search_tool.py(untracked) 和 toolsets.py(modified)
```

### Phase 4: 回滚（仅在升级失败时）

```bash
# 恢复备份的配置
cp ~/.hermes/backups/pre-upgrade-*/config.yaml ~/.hermes/config.yaml
cp ~/.hermes/backups/pre-upgrade-*/.env ~/.hermes/.env

# pip 回滚
pip install hermes-agent==<旧版本号>

# Git 回滚（如是从 git 安装）
cd ~/.hermes/hermes-agent
git checkout <之前的commit>
pip install -e .

# 重新打补丁
bash ~/.hermes/scripts/post-update-patches.sh

# 重启 gateway
systemctl --user restart hermes-gateway
```

---

## 冲突风险矩阵

| 冲突类型 | 概率 | 影响 | 恢复难度 |
|---------|------|------|---------|
| toolsets.py 结构微调 | 中 | 低（一行补丁） | 极低 |
| toolsets.py 重构 | 低 | 中（需重写补丁逻辑） | 低 |
| tools/ 注册机制变更 | 极低 | 高（bing_search may break） | 中 |
| config.yaml schema 变更 | 中 | 低（hermes config migrate） | 低 |
| 依赖变更 | 中 | 中（pip install 可修） | 低 |
| 上游新增同名文件冲突 | 极低 | 高 | 中 |

---

## 定制约法

**铁律**：
1. 新增文件可以，不删上游文件
2. 修改上游文件只限于列表追加（如 toolsets.py），不重构逻辑
3. 所有定制改动必须有对应的自动补丁脚本（`post-update-patches.sh`）
4. 新增定制前评估：能不能用 skill/plugin/MCP 替代直接改源码？

**当前定制清单**：
| 文件 | 改动类型 | 补丁方式 |
|------|---------|---------|
| `tools/bing_search_tool.py` | 新增 | 无需补丁（untracked，pip install / git pull 不删） |
| `toolsets.py:33` | `_HERMES_CORE_TOOLS` 追加一项 | sed 自动补丁 |
| `toolsets.py:82` | `TOOLSETS[web][tools]` 追加一项 | sed 自动补丁 |

> 📖 **补丁脚本**：[`scripts/post-update-patches.sh`](./scripts/post-update-patches.sh) — 幂等、精准靶向、带验证。每次升级后运行。
> 🛡️ **升级防护盾**：[`izu_hermes_upgrade_guard.py`](../../../../../mnt/i/hermes/izu/izu_hermes_upgrade_guard.py) — 自动快照+diff+兼容检查，推荐升级前先拍快照。

---

## 补丁脚本编写陷阱

### sed 上下文锚定 —— 必须精准到缩进层级

**错误案例**（首次编写时踩坑）：
```bash
# ❌ 这个模式匹配了 4 个位置——_HERMES_CORE_TOOLS、TOOLSETS[web]、
# hermes-acp 和 hermes-api-server 全部被改
sed -i 's/"web_search", "web_extract",/"web_search", "web_extract", "bing_search",/' toolsets.py
```

`toolsets.py` 中有多处 `"web_search", "web_extract",` 出现（`_HERMES_CORE_TOOLS`、`TOOLSETS["web"]`、`hermes-acp`、`hermes-api-server`），无差别的全局替换会污染不该改的区块。

**正确做法**：用独一无二的上下文锚定目标行。

- **_HERMES_CORE_TOOLS**（4空格缩进 `# Web`，其他区块是12空格缩进）：
  ```bash
  sed -i '/^    # Web$/{n;s/"web_search", "web_extract",/"web_search", "web_extract", "bing_search",/}' toolsets.py
  ```

- **TOOLSETS["web"]**（工具集名 `"web": {` 唯一）：
  ```bash
  sed -i '/"web": {/,/"tools":/{s/"tools": \[\"web_search\", \"web_extract\"\]/"tools": ["web_search", "web_extract", "bing_search"]/}' toolsets.py
  ```

**通用原则**：sed 打补丁时，用缩进层级 + 块边界 + 相邻注释组合成唯一锚点，再用地址范围限制作用域。写完必须跑「破坏-恢复」测试验证只命中目标。
