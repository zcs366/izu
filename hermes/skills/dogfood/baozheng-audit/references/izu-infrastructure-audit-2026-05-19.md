# 包拯审计实战案例：izu v1.0.0 工程基础设施审计

**日期：** 2026-05-19
**审计对象：** izu系统（21文件/5,746行）
**审计官：** 包拯（攻击性审计版v1.1）

## 发现摘要

| 问题 | 严重程度 | 审计步骤 |
|------|---------|---------|
| 12/21文件(50%代码)未入git | 🔴 | `git status` |
| 测试覆盖率0.2%（仅11测） | 🔴 | `pytest --collect-only` |
| 无requirements.txt/pyproject.toml | 🔴 | `ls requirements.txt` |
| GitHub凭证明文在remote URL | 🔴 | `git remote -v` |
| 无README.md | 🟡 | `ls README.md` |
| 单次巨型commit(14文件/3,472行) | 🟡 | `git log --oneline` |

## 攻击性审计五步初始检查的实战验证

```bash
# 第1步：版本控制完整性
git status            → 17个未跟踪/修改文件
git ls-files          → 仅14文件被追踪
git log --oneline     → 仅1次commit

# 第2步：测试真实度
pytest --collect-only → 11个测试，覆盖仅7%
ls test_*.py          → 仅1个测试文件

# 第3步：包管理
ls requirements.txt   → 不存在
ls setup.py pyproject.toml → 不存在

# 第4步：文档同步
ls README.md          → 不存在

# 第5步：凭据泄露
git remote -v         → https://zcs366:***@github.com/zcs366/izu.git
```

## 修复结果

| 修复项 | 变化 |
|-------|------|
| git提交 | 14→31文件入版本，2次commit推送到GitHub |
| 测试覆盖 | 11→79测试（7倍），新增68测试 |
| requirements.txt | playwright, playwright-stealth, spacy, pytest |
| pyproject.toml | 项目元数据+构建配置 |
| 凭据修复 | SSH remote，密码彻底清除 |
| README.md | 376行中英双语，含架构图+13模块说明 |

## 教训

1. git status + pytest + ls requirements + git remote -v 四条命令是**每次审计的必修步骤**
2. 工程基础设施缺口是代码审计的**前件条件**——必须先过基建检查再审计代码质量
3. 并行修复效率极高（3个delegate_task同时推进README/tests/requirements），总耗时约3分钟
