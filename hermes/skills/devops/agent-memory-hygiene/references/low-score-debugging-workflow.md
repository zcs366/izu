# 低分 Skill 调试工作流

## 场景

Skill生态健康扫描发现低分skill（<0.70或<0.65），需要分析原因并决定是否修复。

## 流程

### Step 1: 确认分数

看板列出「待关注」skills，但部分可能只是略低于0.75（属于0.70~0.85的🟡范围），真正需要关注的只有两个层级：

| 层级 | 分数 | 行动 |
|------|------|------|
| 🟠 关注级 | 0.50~0.70 | 分析原因，记录问题 |
| 🔴 异常级 | <0.65 | 触发告警报告 |

### Step 2: 逐项检查维度

```bash
python3 /mnt/i/hermes/izu/izu_skill_scorer.py check <skill_name>
```

输出格式：
```
📋 skill-name (category) — 总分 X.XXX
  url_validity         ████░░░░░░ 0.43    ← 外部链接失效
  structural_complete  ███░░░░░░░ 0.39    ← 结构松散/无frontmatter
  citation_accuracy    ██████████ 1.00
  consistency          ██████████ 1.00
  conciseness          ██████████ 1.00
```

### Step 3: 区分"外部skill"vs"用户skill"

核心规则（来自 `is_user_skill()`）：
- 有 `homepage:` 字段 → 外部skill，跳过自动修复
- 有 `metadata:hermes` 或 `author: Hermes Agent` → 外部skill
- 有 `compatibility:` 或 `plugin:` → 外部skill
- 无以上特征 → 用户skill，可自动修复

外部skill的问题通常只能手动修复，或者等待上游更新。

### Step 4: 常见病因与方案

| 低分维度 | 常见病因 | 方案 |
|----------|----------|------|
| url_validity | 引用外部链接已死 | ①用web_search确认；②若无必要则删链接；③换替代源 |
| structural_complete | 无frontmatter/缺节标题/缺代码块 | 用户skill可自动补frontmatter；外部skill需手动 |
| consistency | 数字/版本/时间混杂 | 通常为误报，需人工复查 |
| conciseness | skill过长(>300行) | 拆成references/目录下的支持文件，主skill保持精简 |

### Step 5: 决定报告格式

```python
if score < 0.65:
    if is_persistent_low:  # 昨日已在同区间
        report_level = "🟡 持续关注（简短报告）"
    else:  # 新增跌入低分
        report_level = "🔴 新增异常（详细报告）"
elif score < 0.75:
    report_level = "🟢 正常（一句话看板）"  # 持续的🟡属于已知
else:
    report_level = "🟢 正常（一句话看板）"
```

### 历史案例

| 日期 | Skill | 分数 | 病因 | 是否外部 | 处理 |
|------|-------|------|------|---------|------|
| 2026-05-21 | drawio-skill | 0.624 | url_validity=0.43, structural_complete=0.39 | 是（homepage+metadata+author:Hermes Agent） | 持续关注，无法自动修复 |
| 2026-05-21 | outlines | 0.662 | url_validity=0.50, consistency=0.60 | 是（metadata） | 持续关注 |
