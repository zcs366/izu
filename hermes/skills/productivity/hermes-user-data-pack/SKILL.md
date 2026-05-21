---
name: hermes-user-data-pack
description: "一键备份/恢复 Hermes Agent 全部配置、记忆、技能、会话和数据库到 tar.gz 压缩包。"
version: 1.1.0
author: 军师祭酒
license: MIT
metadata:
  hermes:
    category: productivity
    tags: [backup, restore, data-export, data-import, migration, workspace]
    trigger_phrases: ["备份 Hermes", "恢复 Hermes", "导出配置", "导入配置", "数据打包", "迁移数据"]
---

# Hermes User Data Pack

> v1.1.0 · 2026-05-19

两层备份体系：① Hermes 系统数据（配置/技能/记忆/会话/状态）→ tar.gz 灾难恢复 ② Workspace 内容资产（wiki/scripts/output）→ tar.gz 内容保护 ③ GitHub 公开推送（精选文档）→ 公众认知。

## Workspace 输出目录结构（output/）

output/ 按项目归类，中文目录名，不按文件格式分：

```
output/
├── izu爱祝/          ← 战略规划 / 评估报告 / 研究产出
├── ita代码压缩/      ← 章程 / 研究报告 / 评审标注
├── hermes系统/       ← 手册指南 / 审计报告 / skills生态 / 架构设计
├── 军师体系/         ← 系统架构 / 裁决记录 / 核战队
├── 工具手册/         ← claude-code / obsidian / notion / comfyui / 其他工具
├── 研究成果/         ← agi研究 / 教育研究 / 育儿实践 / 品牌战略 / 论文评审
├── 每日产出/         ← 论文日报 / 乐团报告 / 前沿综述 / 周报
├── 运维监控/         ← 记忆健康 / skill健康 / 成本报告 / 进化报告
├── 待批准/           ← 军师出报告 → 用户批准，统一放这里
├── 设计稿/           ← logo / 架构图
├── 管线产物/         ← izu pipeline 原始产物
├── 备份/             ← 备份tar.gz
└── 其他/             ← 未分类
```

### 归类规则

1. **按项目分**：izu / ita / hermes / 军师 → 各自目录
2. **中文目录名**：一看就懂，不用猜缩写
3. **待批准目录**：所有需要用户批准的技术报告，军师出、用户批、统一放这里
4. **不按文件格式分**：同项目的 .md .html .pdf 放一起
5. **管线产物不动**：izu-pipeline 内部结构保持原样

### 批量整理脚本模式

当 output/ 再次变乱时，用 bash 脚本按文件名模式匹配批量归类：

```bash
cd /mnt/i/hermes/output
# 示例：按关键词匹配移动
for f in ita-* ITA-*; do mv "$f" "ita代码压缩/研究报告/"; done
for f in hermes-*; do mv "$f" "hermes系统/架构设计/"; done
```

## 用法

### 完整备份（两层一起跑）

```
请执行完整备份
```

**第一层·Hermes 系统数据** — 灾难恢复用（含密钥，不上传任何地方）

备份内容：
- `config.yaml` + 备份历史
- `.env`（环境变量/API密钥，⚠️ 含所有密钥）
- `auth.json`（OAuth凭据）
- `skills/`（全部技能）
- `memories/MEMORY.md` + `USER.md` + `memory_store.db`
- `sessions/`（全部会话历史）
- `cron/jobs.json` + `cron/output/`
- `state.db` + `response_store.db` + `kanban.db`
- `gateway_state.json` + `channel_directory.json`
- `platforms/` + `pairing/`
- `hooks/`
- `SOUL.md`
- `supermemory.json`
- `checkpoints/`（文件回滚快照）

**第二层·Workspace 内容资产** — 内容保护用（不含密钥，不含大二进制）

备份内容：
- `wiki/`（全量知识库）
- `scripts/`（所有自动化脚本）
- `output/`（全部产出，按项目归类）
- `izu-site/`（静态站点源码）
- `input/md/`（输入资料）
- `_workspace.md`（工作区配置）

排除：`output/backups/` `output/管线产物/` `state/` `work/` `data/` `.git/`

输出目录：`/mnt/i/hermes/output/备份/`

### 恢复

```
请恢复：hermes-data restore <archive_path>
```

恢复前会自动创建当前状态的备份。恢复后需重启：
```bash
systemctl --user restart hermes-gateway
```

## 手动 tar 命令

```bash
# 第一层：Hermes 系统
cd ~/.hermes && tar -czf /mnt/i/hermes/output/备份/hermes-data-full-$(date +%Y%m%d-%H%M).tar.gz config.yaml .env auth.json skills/ memories/ sessions/ cron/ state.db response_store.db kanban.db gateway_state.json channel_directory.json platforms/ pairing/ hooks/ SOUL.md supermemory.json checkpoints/

# 第二层：Workspace
cd /mnt/i/hermes && tar -czf /mnt/i/hermes/output/备份/izu-workspace-$(date +%Y%m%d-%H%M).tar.gz --exclude='output/备份' --exclude='output/管线产物' --exclude='state' --exclude='work' --exclude='data' wiki/ scripts/ output/ izu-site/ input/md/ _workspace.md
```

## 脚本参考

备份和恢复脚本存储在技能目录下：
- `scripts/backup.sh` — 完整备份脚本（两层一起跑）
- `scripts/restore.sh` — 恢复脚本

## 安全注意事项

1. `.env` 包含 API 密钥 — 备份文件必须妥善保管，不要上传到公开位置
2. `auth.json` 包含 OAuth 令牌 — 同样需要保密
3. 恢复会覆盖当前数据 — 恢复前会自动创建备份，但建议手动做一次完整备份

## 自动化备份

已部署 cron（每周六 22:00 自动执行）：
1. 备份 Hermes 系统数据 → `hermes-data-full-*.tar.gz`
2. 备份 Workspace 内容资产 → `izu-workspace-*.tar.gz`
3. 清理 30 天前的旧备份（保留至少最近 3 份）

## GitHub 推送

**推送内容**（精选，建公众认知用）：
- 白皮书、战略报告、公开长编 / 站点更新 / README

**永不上传**：`.env` / `auth.json` / `sessions/` / `state.db`

**Git 仓库**：`git@github.com:zcs366/izu.git` — 位于 `/mnt/i/hermes/izu-site/`

## 故障排除

### 备份时提示"空间不足"
使用 `backup-light` 模式排除 sessions 和 state.db。

### 恢复后技能不显示
运行 `hermes skills list` 检查。

### 恢复后 gateway 崩溃
```bash
systemctl --user reset-failed hermes-gateway
systemctl --user restart hermes-gateway
```
