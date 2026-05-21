---
name: hermes-manual-upgrade
description: Hermes Agent 升级后更新完整功能手册的标准化流程。检测新版本→读取Release Notes→分路并行更新手册→生成HTML双版→同步到wiki。
version: 1.0.0
metadata:
  hermes:
    tags: [hermes, manual, upgrade, release, documentation]
    category: devops
---

# Hermes 手册版本升级流程

## 何时使用

当 Hermes Agent 有新版本发布时（由 cron 任务「Hermes版本升级追踪」触发，或用户主动告知）使用此流程。

## 前置条件

1. 确认当前已安装版本：`pip show hermes-agent | grep Version`
2. 确认新版本的 Release Notes 文件：`ls ~/.hermes/hermes-agent/RELEASE_*.md`
3. 确认手册文件路径：`/mnt/i/hermes/output/hermes系统/手册指南/Hermes_Agent_完整功能手册与操作指令集-v{旧版本}.md`

## 步骤

### 第1步：读取 Release Notes

读取 `~/.hermes/hermes-agent/RELEASE_v{新版本}.md` 文件，提取以下信息：
- 版本号/发布日期/代号
- 相较于上一版本的 commit/PR/issue 数量
- Highlights（亮点特性，通常前5-10条）
- 新工具/新命令/新平台/新提供商
- 安全修复
- 性能改进
- 破坏性变更
- 贡献者列表

### 第2步：复制基版

```bash
cp "/mnt/i/hermes/output/hermes系统/手册指南/Hermes_Agent_完整功能手册与操作指令集-v{旧版本}.md" \
   "/mnt/i/hermes/output/hermes系统/手册指南/Hermes_Agent_完整功能手册与操作指令集-v{新版本}.md"
```

### 第3步：并行更新

使用 delegate_task 并行执行以下三个修改流：

**流A：元数据 + 第2-6章（版本信息、亮点、安装、CLI、斜杠指令、工具集）**
- 替换版本号/代号/日期
- 重写第2章版本亮点
- 更新安装方法（如有变更）
- 更新 CLI 指令表（新增/删除命令）
- 更新斜杠指令表
- 更新工具集表

**流B：提供商 + Gateway + 安全 + Skills（第8-10、17章）**
- 更新提供商列表
- 更新 Gateway 平台数量和新平台
- 更新安全修复清单
- 更新 Skills 生态变更
- 更新 i18n 语言数量

**流C：Cron + Kanban + MCP + TUI + 工具生态图谱 + 附录（第12、15、18、20、21、24章）**
- 更新各章节的 v0.x 新增特性表格
- 更新工具生态图谱选择指南
- 更新附录术语表

### 第4步：验证

```bash
# 验证关键版本标识
grep -c "v{新版本}" "手册文件"
grep -c "{代号}" "手册文件"

# 验证各新特性关键词存在
grep -c "{特性1}" "手册文件"
grep -c "{特性2}" "手册文件"
# ... 列出所有核心新特性
```

### 第5步：生成 HTML

更新 `/tmp/gen_html.py` 中的文件路径为 v{新版本}，然后运行：

```bash
python3 /tmp/gen_html.py
```

### 第6步：同步到 wiki 和 doc

```bash
cp 手册.html /mnt/i/hermes/wiki/raw/祝成果/
cp 手册.md /mnt/i/hermes/wiki/raw/祝成果/
cp 手册.html /mnt/i/hermes/output/doc/
cp 手册.md /mnt/i/hermes/output/doc/
```

### 第7步：更新 cron 任务

更新「Hermes版本升级追踪」cron 任务中的版本号引用（如果有硬编码）。

## 陷阱

1. **文件路径用引号括起来** — 中文路径中有空格，patch 工具需要引号包裹
2. **不做全文件覆盖** — 用 patch 替换特定章节，不用 write_file 覆盖整个文件
3. **检查编号一致性** — 插入新章节后，后续章节编号要同步后移
4. **检查章节引用** — 工具生态图谱章节的服务名称可能随版本变化
5. **保留 v0.13.0 的工具生态图谱章节** — 它不受版本号影响，但新增工具要补充到选择指南表

## 验证清单

- [ ] 版本号和代号正确
- [ ] 所有新特性在手册中有对应章节
- [ ] 所有章节编号连续无跳号
- [ ] HTML 渲染无乱码
- [ ] 新旧手册同时保留在目录中
