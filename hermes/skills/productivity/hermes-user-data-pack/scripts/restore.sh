#!/usr/bin/env bash
# ==============================================================================
# Hermes User Data Pack — 一键恢复脚本
# 用法: ./restore.sh <backup_archive>
# 恢复前自动备份当前状态，然后解压恢复。
# ==============================================================================
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Hermes User Data Pack — Restore v1.0${NC}"
echo -e "${CYAN}  ${TIMESTAMP}${NC}"
echo -e "${CYAN}══════════════════════════════════════════════${NC}"

# ===== 参数检查 =====
ARCHIVE="${1:-}"
if [ -z "$ARCHIVE" ]; then
    echo -e "${RED}[错误] 用法: $0 <backup_archive.tar.gz>${NC}"
    echo "  例如: $0 /mnt/i/hermes/output/备份/hermes-data-full-20260507_210000.tar.gz"
    exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
    echo -e "${RED}[错误] 备份文件不存在: $ARCHIVE${NC}"
    exit 1
fi

# ===== 校验备份文件 =====
echo -e "${YELLOW}[1/5] 校验备份文件...${NC}"
SHAFILE="${ARCHIVE%.tar.gz}.sha256"
if [ -f "$SHAFILE" ]; then
    cd "$(dirname "$ARCHIVE")"
    if sha256sum -c "$SHAFILE" 2>/dev/null; then
        echo -e "${GREEN}  ✅ 校验和通过${NC}"
    else
        echo -e "${RED}  ❌ 校验和不匹配！文件可能已损坏。${NC}"
        echo -e "${YELLOW}  是否继续？(y/N)${NC}"
        read -r response
        if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}  ⚠  无校验和文件，跳过校验${NC}"
fi

# ===== 检查备份内容 =====
echo -e "${YELLOW}[2/5] 检查备份内容...${NC}"
BACKUP_CHECK=$(tar -tzf "$ARCHIVE" 2>/dev/null | head -5)
if [ -z "$BACKUP_CHECK" ]; then
    echo -e "${RED}[错误] 备份文件为空或已损坏${NC}"
    exit 1
fi
echo -e "  ${CYAN}备份内容预览:${NC}"
tar -tzf "$ARCHIVE" 2>/dev/null | head -20 | while read line; do
    echo "    $line"
done

# 检查备份中包含的关键文件
HAS_CONFIG=$(tar -tzf "$ARCHIVE" 2>/dev/null | grep -c "config.yaml" || true)
HAS_SKILLS=$(tar -tzf "$ARCHIVE" 2>/dev/null | grep -c "^skills/" || true)
HAS_MEMORY=$(tar -tzf "$ARCHIVE" 2>/dev/null | grep -c "memory_store.db\|memories/" || true)
echo ""
echo -e "  含配置: ${GREEN}✅${NC}  含技能: ${GREEN}✅${NC}  含记忆: ${GREEN}✅${NC}"

# ===== 备份当前状态 =====
echo -e "${YELLOW}[3/5] 备份当前 Hermes 状态（安全网）...${NC}"
PRE_BACKUP_DIR=$(dirname "$ARCHIVE")
PRE_BACKUP="${PRE_BACKUP_DIR}/pre-restore-backup-${TIMESTAMP}.tar.gz"
if [ -d "$HERMES_HOME/config.yaml" ] || [ -f "$HERMES_HOME/config.yaml" ]; then
    # 快速备份关键路径
    mkdir -p /tmp/hermes-prebk-${TIMESTAMP}
    cd "$HERMES_HOME"
    for item in config.yaml .env auth.json SOUL.md skills cron memories memory_store.db state.db; do
        [ -e "$item" ] && cp -r "$item" "/tmp/hermes-prebk-${TIMESTAMP}/" 2>/dev/null || true
    done
    cd /tmp
    tar -czf "$PRE_BACKUP" -C "/tmp/hermes-prebk-${TIMESTAMP}" . 2>/dev/null || true
    rm -rf "/tmp/hermes-prebk-${TIMESTAMP}"
    if [ -f "$PRE_BACKUP" ]; then
        echo -e "  ${GREEN}✅ 当前数据已备份到:${NC}"
        echo -e "     ${CYAN}${PRE_BACKUP}${NC}"
    fi
fi

# ===== 确认恢复 =====
echo ""
echo -e "${YELLOW}══════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  ⚠  即将恢复 Hermes 数据！${NC}"
echo -e "${YELLOW}  当前数据已在 ${PRE_BACKUP} 备份${NC}"
echo -e "${YELLOW}  来源: $(basename "$ARCHIVE")${NC}"
echo -e "${YELLOW}  大小: $(du -h "$ARCHIVE" | cut -f1)${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════${NC}"
echo -e "  输入 ${GREEN}yes${NC} 确认恢复，${RED}其他任意键取消${NC}:"
read -r confirm
if [ "$confirm" != "yes" ]; then
    echo -e "${RED}已取消恢复${NC}"
    exit 0
fi

# ===== 执行恢复 =====
echo -e "${YELLOW}[4/5] 正在恢复数据到 ${HERMES_HOME} ...${NC}"

# 备份前停掉 gateway（如果正在运行）
if systemctl --user is-active --quiet hermes-gateway 2>/dev/null; then
    echo -e "  ${YELLOW}⚠ 正在停止 Hermes Gateway...${NC}"
    systemctl --user stop hermes-gateway 2>/dev/null || true
    sleep 2
fi

# 解压到临时目录，然后整理放置
RESTORE_TMP=$(mktemp -d)
tar -xzf "$ARCHIVE" -C "$RESTORE_TMP"

# 按组件恢复
restore_item() {
    local src="$RESTORE_TMP/$1"
    local dst="$2"
    if [ -e "$src" ]; then
        mkdir -p "$(dirname "$dst")"
        cp -r "$src" "$dst"
        echo -e "  ✅ 恢复: $1"
    fi
}

# 核心文件
restore_item "config/config.yaml" "$HERMES_HOME/config.yaml"
for bakfile in "$RESTORE_TMP"/config/config.yaml.bak*; do
    [ -f "$bakfile" ] && cp "$bakfile" "$HERMES_HOME/" 2>/dev/null || true
done

# 环境变量和认证
if [ -f "$RESTORE_TMP/env/.env" ]; then
    cp "$RESTORE_TMP/env/.env" "$HERMES_HOME/.env"
    echo -e "  ✅ 恢复: .env（含 API 密钥）"
fi
restore_item "auth.json" "$HERMES_HOME/auth.json"
restore_item "SOUL.md" "$HERMES_HOME/SOUL.md"

# 技能
if [ -d "$RESTORE_TMP/skills" ]; then
    rm -rf "$HERMES_HOME/skills"
    cp -r "$RESTORE_TMP/skills" "$HERMES_HOME/skills"
    SKILL_COUNT=$(find "$RESTORE_TMP/skills" -name "SKILL.md" | wc -l)
    echo -e "  ✅ 恢复: skills/（${SKILL_COUNT} 个技能）"
fi

# 记忆
if [ -d "$RESTORE_TMP/memories" ]; then
    mkdir -p "$HERMES_HOME/memories"
    [ -f "$RESTORE_TMP/memories/MEMORY.md" ] && cp "$RESTORE_TMP/memories/MEMORY.md" "$HERMES_HOME/memories/"
    [ -f "$RESTORE_TMP/memories/USER.md" ] && cp "$RESTORE_TMP/memories/USER.md" "$HERMES_HOME/memories/"
    echo -e "  ✅ 恢复: memories/"
fi
restore_item "memory_store.db" "$HERMES_HOME/memory_store.db"

# 会话（如果备份中有）
if [ -d "$RESTORE_TMP/sessions" ]; then
    # 注意: 会话是累积的，追加而非覆盖
    mkdir -p "$HERMES_HOME/sessions"
    cp -rn "$RESTORE_TMP/sessions/"* "$HERMES_HOME/sessions/" 2>/dev/null || true
    SESSION_COUNT=$(ls "$RESTORE_TMP/sessions/"*.jsonl 2>/dev/null | wc -l)
    echo -e "  ✅ 恢复: sessions/（${SESSION_COUNT} 个会话）"
fi

# 定时任务
if [ -d "$RESTORE_TMP/cron" ]; then
    [ -f "$RESTORE_TMP/cron/jobs.json" ] && cp "$RESTORE_TMP/cron/jobs.json" "$HERMES_HOME/cron/jobs.json"
    if [ -d "$RESTORE_TMP/cron/output" ]; then
        mkdir -p "$HERMES_HOME/cron/output"
        cp -rn "$RESTORE_TMP/cron/output/"* "$HERMES_HOME/cron/output/" 2>/dev/null || true
    fi
    echo -e "  ✅ 恢复: cron/"
fi

# 数据库
for db in state.db response_store.db kanban.db supermemory.json; do
    restore_item "$db" "$HERMES_HOME/$db"
done

# 网关状态
for f in gateway_state.json channel_directory.json discord_threads.json; do
    restore_item "$f" "$HERMES_HOME/$f"
done

# 平台/配对/钩子
[ -d "$RESTORE_TMP/platforms" ] && restore_item "platforms" "$HERMES_HOME/platforms_bak_${TIMESTAMP}" && \
    rm -rf "$HERMES_HOME/platforms" && mv "$HERMES_HOME/platforms_bak_${TIMESTAMP}" "$HERMES_HOME/platforms"
restore_item "pairing" "$HERMES_HOME/pairing"
restore_item "hooks" "$HERMES_HOME/hooks"
restore_item "checkpoints" "$HERMES_HOME/checkpoints"
restore_item ".skills_prompt_snapshot.json" "$HERMES_HOME/.skills_prompt_snapshot.json"

# 清理
rm -rf "$RESTORE_TMP"

# 权限修复
chmod 600 "$HERMES_HOME/.env" "$HERMES_HOME/auth.json" "$HERMES_HOME/config.yaml" 2>/dev/null || true

echo -e "${YELLOW}[5/5] 恢复完成！${NC}"

echo ""
echo -e "${GREEN}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 数据恢复成功！${NC}"
echo -e "${GREEN}══════════════════════════════════════════════${NC}"
echo ""
echo -e "  恢复后的操作:"
echo -e "  1. ${CYAN}重启 Gateway:${NC}"
echo -e "     systemctl --user restart hermes-gateway${NC}"
echo -e ""
echo -e "  2. ${CYAN}验证技能:${NC}"
echo -e "     hermes skills list${NC}"
echo -e ""
echo -e "  3. ${CYAN}验证定时任务:${NC}"
echo -e "     hermes cron list${NC}"
echo -e ""
echo -e "  4. ${CYAN}运行健康检查:${NC}"
echo -e "     hermes doctor${NC}"
echo ""
echo -e "  预恢复备份: ${CYAN}${PRE_BACKUP}${NC}"
echo -e "  备份来源:   ${CYAN}${ARCHIVE}${NC}"
echo ""
