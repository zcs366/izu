---
name: junshi-code-standards
description: 军规——科学工程标准。严格严苛，马虎不得。所有代码、测试、文档、CI必须通过军规检查才能交付。
version: 1.1.0
author: 军师祭酒
tags:
  - 军规
  - 科学
  - 工程标准
  - 代码质量
  - 测试规范
  - 审计
  - 可复现
  - 不造假
  - izu案例
trigger: "军规|科学标准|工程标准|代码标准|质量检查|代码规范|科学态度|严格严苛|马虎不得|代码交付标准|能不能交付|整顿代码"
metadata:
  hermes:
    category: software-development
---

# 军规 · 科学工程标准

> 科学写作，严格严苛，马虎不得。
> 所有代码、测试、文档必须通过以下十条军规检查才能交付。

> **核心思想（一个公式）：**
>
> `真正完成 = 可运行 + 可复现 + 可审计 + 可传承`
>
> - **可运行**：代码活着（有入口、被集成、跑得通）
> - **可复现**：从头搭建环境能恢复（包管理 + 版本控制）
> - **可审计**：每项结论指向具体代码行，不笼统说"已优化"
> - **可传承**：下一任开发者3小时内能接手（README + CHANGELOG + 架构图）

## 十条军规（铁律，不可商量）

### 军规一：不造假——数据必须真实可复现

- **禁止**虚假指标、占位数据、恒等映射冒充验证结果
- 所有占位/模拟路径必须标注 `mock_mode=True`（字段名精确为 `mock_mode`，非 `is_mock`/`fake`/`simulated`）
- `round_trip` 类验证：如果解码器是恒等映射或空壳，其输出指标必须标红不可信
- 验证方法：去掉所有 mock，看还有几个测试能过。**mock去掉后如果核心逻辑没被测试覆盖，整条测试链不可信。**

**实战案例（izu v1.0.0审计发现）：**
```
encoder.py LatentCode.round_trip → 返回 edit_similarity=1.0, compression_ratio=0.3x
→ 实际解码器是恒等映射（lambda x: x），指标100%为假
→ 修复：输出加 mock_mode=True 字段，标注"解码器未实现，指标不可信"
```

### 军规二：可复现——包管理/版本控制必须完整

- **必须提供**：`requirements.txt` + `pyproject.toml`（或 `setup.py`）
- **版本控制**：每笔有意义变更单独 commit，禁止单次巨量 commit
- **README**：中英双语 + ASCII 架构图 + 可用命令
- **CHANGELOG**：每次版本变更记录 vX.Y + 日期 + 变更内容
- **Makefile**：提供 `test`/`lint`/`clean`/`all` 命令

**包管理成熟度阶梯：**

| 等级 | 特征 | 判定 |
|------|------|------|
| 🔴 不可复现 | 无 requirements / setup / pyproject | ❌ 卡死，不能交付 |
| 🟡 基本可复现 | 有 requirements.txt 但无版本锁定 | ⚠️ 未来可能断裂 |
| 🟢 良好 | requirements.txt + pyproject.toml | ✅ |
| 🟢 优秀 | + Makefile + CI (.github/workflows/) | ✅ 最佳实践 |

**版本控制健康检查：**
```
git status                    # 未跟踪文件超过30% = 🔴 工程崩溃预警
git log --oneline --graph     # 只有1次commit = ❌ 单次巨量commit不可追溯
git diff --stat origin/master..HEAD  # 新增 vs 删除比例是否合理
git ls-files | wc -l          # 真正被入版本的文件数
```

### 军规三：可审计——每项结论指向具体代码行

- 审计输出中**禁止**泛泛表述（"逻辑有问题""架构需优化"）
- 必须写：`[文件名:行号] — [具体问题] — [风险等级] — [修复方案]`
- 审计报告三种标记统一使用：

| 标记 | 含义 | 使用条件 |
|------|------|---------|
| ✅ 通过 | 功能正确，可直接推进 | 核心逻辑无问题，边界覆盖完整 |
| ⚠️ 有条件 | 有小问题但不阻塞 | 标注具体风险和修复建议，给出修复优先级 |
| ❌ 不通过 | 有硬伤必须修复 | 修复建议包含具体代码行号和替代写法 |

**实战案例（izu代码审计输出格式）：**
```
izu-pipeline.py L100-105 的 load_manifest 函数
  → ⚠️ 无 try/except 捕获 JSONDecodeError
  → 写入过程中 crash 会产生损坏文件
  → 修复：加 try/except，损坏时返回 {} 并记录日志
```

### 军规四：凭据安全——credentials 永远不在代码中

- `git remote -v` 必须为 SSH 或无凭据 HTTPS
- API key/token/password 使用环境变量或 `~/.hermes/auth.json` 凭证池
- 代码搜索凭据泄露：

```bash
grep -rn -E "(password|secret|api_key|token|key=|secret=)" \
  --include="*.py" --include="*.sh" --include="*.yaml" --include="*.json" \
  --include="*.yml" --include="*.toml" --include="*.env" . 2>/dev/null \
  | grep -v ".git/" | grep -v "node_modules" | grep -v "example\|sample\|template"
```

- 如果发现凭据泄露：**立即撤回 commit + 撤销远程 + 更换密钥**（不存档、不推送、不传播）

**实战案例（ITA v1.0.0审计——与izu同款凭据泄露，2026-05-19）：**
```
git remote -v → origin https://zcs366:PASSWORD@github.com/zcs366/ita.git
→ 🔴 ITA项目重蹈izu覆辙——同一个用户，不同项目，同样的问题！
→ 修复：git remote set-url origin git@github.com:zcs366/ita.git
→ 教训：军规四不是一次性动作。每开一个**新项目**，第一件事就是git remote -v检查。
   把凭据检查做成强制钩子：`echo 'git remote -v' >> ~/.bashrc` 或加入项目README启动步骤。
```

### 军规五：分批提交——禁止单次巨量 commit

- 每笔 commit 遵守 **「一个变更，一个 commit」** 原则
- 含义：一个逻辑变更 = 一个 commit。不是"一个文件一个 commit"，也不是"100个改同一件事的算一个"
- 巨量 commit 判定：单次 commit 修改 20+ 文件 或 超过 1000 行 → 🔴 需要拆分
- 真实案例：izu v1.0.0 首次 commit = 8 个文件 → 此后每轮测试补完独立 commit

**合格提交规范：**
```
✅ v1.0.0 — 工程基础设施修复    (8文件, +95行)     # 基础修复，范围可控
✅ v1.1.0 — pyproject + 测试补充  (3文件, +43行)     # 包管理，范围小
✅ v1.2.0 — 测试覆盖翻15倍         (13文件, +10661行) # 测试补充，虽大但全是同类变更
❌ 如果上述合并为一个 commit       (21文件, +10799行) # ➡ 不可追溯

判断标准：单次 commit + N个不同主题的变更 = 违反军规五
```

### 军规六：mock 有意识——mock 不是免检金牌

- mock 只屏蔽外部依赖（文件系统、网络、硬件），不屏蔽业务逻辑
- 每个使用 mock 的测试必须问：**去掉 mock 后，这个测试还能验证什么？**
- mock 密集模块必须至少有 1 个端到端测试走真实路径（即使慢、有外部依赖）
- 当 mock 边界偏差过多时，标记 `@pytest.mark.xfail(reason="原因")` + 记录预期修复时间，不阻塞整体交付

**Mock 质量分级：**

| 等级 | 特征 | 判定 |
|------|------|------|
| 🔴 虚假覆盖 | mock 了整个核心逻辑，测试等价于 assert True | ❌ 有测试等于没测试 |
| 🟡 浅覆盖 | mock 了外部依赖，验证了业务逻辑的 shape/type | ⚠️ 不验证数据正确性 |
| 🟢 深度覆盖 | mock 了外部依赖，验证了业务逻辑的正确性 | ✅ 真正的单元测试 |
| 🟢 实装覆盖 | 至少 1 个测试走真实依赖路径验证完整性 | ✅ 端到端可信 |

**实战案例（izu test_dep_parse_zh.py）：**
```
→ mock 了 spacy 分词器返回预设 token 列表
→ 测试验证了"分词→实体识别→关系抽取"三步骤流水线的逻辑正确性
→ 但 spacy 中文模型返回的 token 格式与实际有 7 处边界偏差
→ 修复：标记 7 项为 xfail（spacy mock 边界），保整体绿色
→ 教训：mock 能验证"骨架正确性"，但边界细节需真实模型验证
```

### 军规七：测试真实逻辑——不只测 wrapper

- 测试必须覆盖核心逻辑路径，不只是构造函数和正常路径
- 至少包含三类测试：**正常路径** + **边界条件** + **异常路径**
- 边界条件清单：空输入、None 输入、超大输入、损坏文件、重复值、循环依赖
- 如果模块有 `_process_item() _check() _validate()` 等内部逻辑方法，测试必须覆盖它们，不能只测 `run() run_all() process()` 等顶层方法

**测试质量检查清单：**
```
□ 正常路径：输入预期值，输出符合预期
□ 边界检查：空输入不崩溃
□ 边界检查：异常输入不崩溃（抛有意义异常）
□ 边界检查：超大输入性能底线
□ 异常路径：文件缺失优雅降级
□ 异常路径：写入失败回滚
□ 异常路径：数据损坏恢复
□ 集成验证：至少 1 端到端路径
```

### 军规八：代码活着——必须集成到管线/有入口

- 写完的代码如果未被集成到任何调用链条中 = 孤岛 = ❌ 未完成
- 检查方法：
  - `pipeline.py` 中是否存在 `run_xxx()` 方法引用该模块？
  - `health.py` 能否一键确认模块正常运行？
  - 是否存在端到端使用路径？（用户输入 → 模块处理 → 输出可感知）
- 最低集成标准：模块有自己的 `run()`/`run_all()` 入口方法，且被 `health.py` 或 `main.py` 引用

### 军规九：文档同步——README 跟不上代码 = 误导

- README 中声明的功能必须在代码中存在（反向验证）
- 代码中的新增功能必须在 README 中有记录
- 过时的 README 比没有更危险——它在主动误导
- CHANGELOG 必须与版本控制同步（每 commit 变更对应一条 changelog 记录）

**文档同步检查：**
```
# 正向验证：README写的功能在代码中是否存在
grep "def" README.md | while read line; do
  func=$(echo $line | grep -oP '(?<=`)[^`]+(?=`)')
  grep -r "$func" --include="*.py" . > /dev/null || echo "❌ $func 声明但不存在"
done

# 逆向验证：代码的关键功能是否在 README 中有记录
grep -r "def \|class " --include="*.py" . | head -20 | while read line; do
  name=$(echo $line | grep -oP '(?<=def |class )[^(:\s]+')
  grep -q "$name" README.md 2>/dev/null || echo "⚠️ $name 在代码中存在但 README 未记录"
done
```

### 军规十：交付三连检——自检→包拯→鲁班

每项代码交付物必须经过三级检查才能标记完成：

| 级别 | 检查人 | 检查内容 | 时间 | 产出 |
|------|--------|---------|------|------|
| L0 自检 | 写代码者 | 军规1-9基本检查 | 写完后立即 | 无（合规即可） |
| L1 包拯 | 审计官 | 五层深度核实（L1-L5）| 自检后 | 审计报告 + 推进建议 |
| L2 鲁班 | 工程导师 | 代码逐行 + 架构 + 测试质量 | 包拯通过后 | 代码审计报告 + 修复方案 |

**L0 自检清单（快速，3分钟内完成）：**
```
□ 军规一：无虚假数据？mock_mode 标注了？
□ 军规二：requirements + pyproject 存在？git 已提交？
□ 军规三：如果被审计，每项功能能指向具体代码行？
□ 军规四：git remote 无密码？代码中无硬编码 key？
□ 军规五：commit 拆分合理？
□ 军规六：mock 只屏蔽外部依赖，未遮蔽核心逻辑？
□ 军规七：测试覆盖正常+边界+异常三类？
□ 军规八：模块有入口且被集成？
□ 军规九：README 和 CHANGELOG 同步了？
□ 军规十：通过了 pytest 全量测试（绿色）？
```

**全军规验收模板（用于工程交付）：**
```
## 军规验收报告

| 军规 | 状态 | 证据 |
|------|------|------|
| 一、不造假 | ✅/⚠️/❌ | [证据：xxx] |
| 二、可复现 | ✅/⚠️/❌ | [证据：xxx] |
| 三、可审计 | ✅/⚠️/❌ | [证据：xxx] |
| 四、凭据安全 | ✅/⚠️/❌ | [证据：xxx] |
| 五、分批提交 | ✅/⚠️/❌ | [证据：xxx] |
| 六、mock有意识 | ✅/⚠️/❌ | [证据：xxx] |
| 七、真实逻辑 | ✅/⚠️/❌ | [证据：xxx] |
| 八、代码活着 | ✅/⚠️/❌ | [证据：xxx] |
| 九、文档同步 | ✅/⚠️/❌ | [证据：xxx] |
| 十、三连检 | ✅/⚠️/❌ | [证据：xxx] |

判定：全部 ✅ 方可交付。任意一条 ⚠️ 需标注改进计划。❌ 直接退回。
```

## 工程健康状态速查表

| 指标 | 🔴 崩溃 | 🟡 亚健康 | 🟢 健康 | 🟢 优秀 |
|------|---------|----------|---------|---------|
| 版本控制 | >30%文件未跟踪 | 10-30%未跟踪 | <10%未跟踪 | 0%未跟踪，分批commit |
| 测试 | 0个测试 | 1-10个测试 | >50个测试 | >模块数×10，全绿 |
| 包管理 | 无 | requirements.txt | + pyproject.toml | + Makefile + CI |
| 凭据 | 明文在remote/代码 | 环境变量 | 凭证池+SSH | 自动旋转+定期审计 |
| README | 无 | 存在但过时 | 同步代码 | 双语+架构图+命令 |
| CHANGELOG | 无 | 有但空 | 每版记录 | + 版本号 + 日期 + 变更说明 |
| 提交习惯 | 1次巨量commit | 3-4次大commit | 按模块commit | 按逻辑变更commit |

## 实战案例：izu 项目恢复全程（2026-05-19）

### 审计前状态（v1.0.0）

```
git status    → 21文件中仅9个被跟踪（57%未跟踪） → 🔴
git log       → 仅1次commit → 🔴
pytest        → 路径不存在 → 🔴（测试文件0个）
requirements  → 不存在 → 🔴
README        → 不存在 → 🔴
git remote    → HTTPS密码明文 → 🔴
```

**审计结论：** 5/5项军规（包管理/版本控制/凭据/文档/测试）全红 → 🔴 全局阻塞，必须先修基础设施才能审代码。

### 修复后状态（v1.5.0）

```
git status    → 21/21文件全部跟踪 → 🟢
git log       → 8次commit（按v1.0→v1.5版本拆分）→ 🟢
pytest        → 495+测试，全部绿色（21/21模块100%覆盖）→ 🟢
requirements  → requirements.txt + pyproject.toml + Makefile → 🟢
README        → 376行中英双语+ASCII架构图 → 🟢
git remote    → SSH无凭据 → 🟢
CHANGELOG     → v1.0→v1.5完整历史 → 🟢
CI            → .github/workflows/ci.yml → 🟢
```

**修复路径：** 包拯审计发现3项🔴阻塞问题 → 3路并行修复（README/requirements/测试）→ 逐轮提交 → 包拯复验 → 鲁班加固 → CHANGELOG归档。全程6小时（含中断）。

**关键决策记录：**
1. 12个 mock 边界偏差标记 xfail（不修，因真实 spacy 中文模型未装）
2. GitHub remote 直接切 SSH（不留过渡）
3. 测试按6轮分批写（2-3模块/轮），非一次性全写
4. 每轮写完立即 git commit + push，不做超大 commit

## 实战案例：ITA 项目基建修复（2026-05-19）

### 审计前状态（v1.0.0）

| 军规 | 状态 | 发现 |
|------|------|------|
| 一、不造假 | ⚠️ 有条件 | 解码器是恒等映射（已加mock_mode标注），不算造假但有意识标记 |
| 二、可复现 | 🔴 | 无requirements.txt、无pyproject.toml |
| 三、可审计 | ✅ | 代码结构清晰，但有解码器占位的TODO |
| **四、凭据安全** | **🔴 同izu一模一样的漏洞** | git remote HTTPS带明文密码——与izu v1.0.0的泄露完全一致 |
| 五、分批提交 | 🔴 | 仅2次commit，17个文件未跟踪（45%） |
| 六、mock有意识 | ✅ | mock_mode已标注 |
| 七、测试真实逻辑 | ✅ | 169测（1 flaky） |
| 八、代码活着 | ✅ | 集成在pipeline中 |
| 九、文档同步 | ⚠️ | README有但无使用方法 |
| 十、三连检 | ⚠️ | 自检有，但包拯审计未触发（人没叫审计） |

**核心教训：** ITA和izu是同一个用户、同一台机器、同一个开发习惯。izzu踩过的坑（凭证明文、无requirements、无pyproject），ITA一个不落全踩了。**军规不是一次性动作。每个新项目必须重新执行五步检查。**

### 修复后状态（v1.2.0）

```
git remote    → SSH无凭据 ✅（同izu修复方案）
requirements  → requirements.txt + pyproject.toml ✅
测试          → 191/191 ✅（新增22个解码器测试 + 1个flaky修复）
README        → 更新含使用方法+目录结构 ✅
CHANGELOG     → v1.0→v1.2 ✅
提交习惯      → 8次commit（v1.0→v1.1基建→v1.2解码器）✅
解码器        → 从恒等映射换成真实Transformer Decoder ✅
```

**修复路径：** 包拯审计（5步检查）→ 凭据切SSH → 创建requirements+pyproject → 提交全部文件 → 实现解码器（PythonTokenizer + CodeDecoder + ITADecoder）→ 写22测试 → 修复1个flaky → CHANGELOG+README更新 → git push。全程约2小时。

## 参考

- 包拯审计技能：`skills/dogfood/baozheng-audit/SKILL.md`
- 鲁班工程审计：`skills/software-development/luban-agent/SKILL.md`
- izu 审计报告：`docs/audit-report-izu-2026-05-19.md`（在 izu 项目目录下）
- izu CHANGELOG：项目根目录 CHANGELOG.md
