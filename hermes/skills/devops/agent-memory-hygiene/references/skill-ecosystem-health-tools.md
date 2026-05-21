# Skill生态健康工具 — 参考文档

> 对接 `agent-ecosystem-health` 主线：三大支柱中的Skill健康 + 升级防护。

---

## 一、izu_skill_scorer.py

**位置**: `/mnt/i/hermes/izu/izu_skill_scorer.py`  
**功能**: 6维评分引擎，扫描所有SKILL.md

### 评分维度

| 维度 | 权重 | 检查方式 |
|------|------|----------|
| `url_validity` | 20% | curl检查前20个URL |
| `structural_complete` | 20% | 检测frontmatter/标题/代码块/表格/用法段，有加分 |
| `citation_accuracy` | 15% | 有引用无链接扣0.5 |
| `consistency` | 20% | 排除日期(2026-05-16)/版本(v1.0)/时间(6:30-7:00)后的数字范围异常 |
| `conciseness` | 15% | 平均句长10-40字=1.0，<10=0.7，>80=0.6 |

### 额外检查项（extras）

| 检查项 | 检测方式 |
|--------|----------|
| `has_frontmatter` | content.startswith('---') |
| `has_tags` | 兼容 inline `tags: [a,b]` 和 block `tags:\n  - a` |
| `has_date` | frontmatter `date:` 字段 或 全文 `20XX-XX-XX` |
| `has_version` | frontmatter `version: x.y` 或 全文 `vx.y.z` |
| `has_description` | 内容含 功能/description/core mission |

### 历史修复记录

- **consistency误报**：日期/版本号/时间格式被误判为数字范围异常 → 剥离后修复
- **structure过于简单**：只搜 `##` 字符串 → 改为SKILL专用结构检测+加分
- **has_version漏检**：只搜 `v1.0` → 兼容 `version: 1.0.0` YAML格式
- **has_tags漏检**：只认inline → 兼容YAML block `tags:\n  - a`

---

## 二、izu_skill_ecosystem_health.py

**位置**: `/mnt/i/hermes/izu/izu_skill_ecosystem_health.py`  
**功能**: 扫描 + 自动修正 + 看板 + 报告

### 命令

```bash
python3 izu_skill_ecosystem_health.py scan        # 扫描
python3 izu_skill_ecosystem_health.py fix          # 扫描+自动修正
python3 izu_skill_ecosystem_health.py dashboard    # 看板
python3 izu_skill_ecosystem_health.py full         # 全流程(含记忆维护)
```

### is_user_skill 保护逻辑

```python
def is_user_skill(content):
    """返回False表示跳过自动修正——这是Hermes官方/外部skill"""
    # 命中任一特征即判定为外部skill:
    # - homepage: 字段存在
    # - metadata: 含 hermes 或 openclaw
    # - author: 含 Hermes Agent
    # - plugin: 字段存在
    # - compatibility: 字段存在
```

### 看板格式

```markdown
## 🧬 Skill生态健康看板
> {timestamp} | {total}个skills

| 等级 | 数量 | 分布 |
|------|------|------|
| 🟢 ≥0.85 | {n} | {bar} |
| 🟡 0.70-0.85 | {n} | {bar} |
| 🟠 0.50-0.70 | {n} | {bar} |
| 🔴 <0.50 | {n} | {bar} |
| **平均** | **{avg}** |  |

### 📉 待关注
> 🟠 以下skills需要关注：
- `{name}`

### 📈 最佳实践
> 🟢 以下skills是质量标杆：
- `{name}`
```

---

## 三、izu_hermes_upgrade_guard.py

**位置**: `/mnt/i/hermes/izu/izu_hermes_upgrade_guard.py`  
**功能**: 升级前快照 + 升级后diff + 兼容检查

### 使用流程

```bash
# 升级前
python3 izu_hermes_upgrade_guard.py snapshot

# 执行升级
# pip install --upgrade hermes-agent

# 升级后
python3 izu_hermes_upgrade_guard.py check
```

### 快照内容

- Hermes版本号
- 全部136+个SKILL.md的：行数/大小/修改时间/frontmatter字段/content hash
- config.yaml的mtime和size

### 检查报告内容

- 版本变化: old → new
- skills增减: 新增/移除列表
- skills内容变化: 行数变化/字段增减/frontmatter变更
- 配置变化告警

---

## 四、cron配置参考

```yaml
# 记忆维护 — 每6小时（后台无LLM）
cronjob:
  action: create
  schedule: "0 */6 * * *"
  script: izu_memory_maintenance.py
  no_agent: true

# Skill健康 — 每日6:00（带报告）
cronjob:
  action: create
  schedule: "0 6 * * *"
  name: skill-ecosystem-health
  prompt: "每天清晨的Skill生态系统健康维护。安静维护，有异常才报告。"
```

---

## 五、初始修复的分数跃迁

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 低分skills(<0.70) | 108个 | 1个 |
| 平均分 | 0.66 | 0.774 |
| 最高分 | ~0.70 | 0.828 |
| 自动修正skills | — | 20个 |

唯一剩余低分: `drawio-skill` (0.698) — Hermes官方外部skill，不动。
