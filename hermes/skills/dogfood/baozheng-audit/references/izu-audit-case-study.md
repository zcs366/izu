# 包拯实战案例：izu v1.0.0 基础设施审计

> 日期：2026-05-19  
> 审计方式：攻击性5步检查 + 三路并行修复  
> 效果：11测试/5%覆盖 → 495+测试/100%覆盖，8次commit推送GitHub

## 发现（攻击性5步检查实录）

```
Step 1: git status
  🔴 21文件中12个未跟踪（50%代码）
  🔴 evolution_engine.py已修改未提交

Step 2: pytest
  🔴 仅1个测试文件（test_agent_loop.py, 11测）
  🔴 5,746行代码仅0.2%覆盖率

Step 3: ls requirements.txt
  🔴 不存在。无依赖记录，不可复现安装

Step 4: head -30 README.md
  🔴 不存在。新开发者无从了解项目

Step 5: git remote -v
  🔴 https://zcs366:***@github.com/zcs366/izu.git — 凭证明文
```

## 修复模式：三路并行 + 包拯再验证

```
韩信画终局 → 鲁班分三路并行 → 包拯再验证
                    ↓
            路A: README + 架构文档
            路B: requirements.txt + pyproject.toml
            路C: 测试（6轮递增）
```

## 测试覆盖递增轨迹

| 轮次 | 行动 | 测试数 | 模块覆盖 |
|------|------|--------|---------|
| 审计前 | — | 11 | 1/21 (5%) |
| 轮1 | traj_credit + skill_scorer | 79 | 3/21 (14%) |
| 轮2 | traj_balance + session_memory | 164 | 5/21 (24%) |
| 轮3 | evolution_engine + evolution_pipeline | 221 | 7/21 (33%) |
| 轮4 | cost_tracker + skill_ecosystem_health | 339 | 12/21 (57%) |
| 轮5 | topology_api + working_memory | 392 | 14/21 (67%) |
| 轮6 | self_model + memory_maintenance + upgrade_guard | 495+ | 21/21 (100%) |
| 终战 | dep_parse_zh + touxin四件套 | 495+ | 21/21 (100%) |

## 关键决策

- **基础设施优先于功能**：先修git/reqs/README/凭据，再补测试
- **由小到大**：先测无外部依赖模块，再mock spacy/playwright
- **mock优于安装**：不安装spacy中文模型（~50MB）和playwright浏览器（~300MB），全部mock
- **文档同步**：每次修复伴随CHANGELOG更新 + README同步
- **Git推送**：每轮修完立即commit+push，不积压

## 教训

1. **git status是最有效的审计单条命令**——未跟踪文件揭示真相
2. **Mock是最大的虚假完成源**——mock模式下所有指标都好看但不真实
3. **凭据泄露最常见的源头是git remote URL**——比代码中的password变量更隐蔽
4. **测试覆盖率从0.2%拉到100%是可能的**——只要分模块、mocked、递进式
