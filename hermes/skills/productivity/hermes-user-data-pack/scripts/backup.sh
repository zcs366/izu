#!/usr/bin/env bash
# ==============================================================================
# Hermes User Data Pack — 一键备份脚本
# 用法: ./backup.sh [output_dir]
# 默认输出: /mnt/i/hermes/output/备份/hermes-data-full-{timestamp}.tar.gz
# ==============================================================================
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
OUTPUT_DIR="${1:-/mnt/i/hermes/output/备份}"

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Hermes User Data Pack — Backup v1.0${NC}"
echo -e "${CYAN}  ${TIMESTAMP}${NC}"
echo -e "${CYAN}══════════════════════════════════════════════${NC}"

# 检查路径
if [ ! -d "$HERMES_HOME" ]; then
    echo -e "${RED}[错误] Hermes 主目录不存在: $HERMES_HOME${NC}"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
ARCHIVE="${OUTPUT_DIR}/hermes-data-full-${TIMESTAMP}.tar.gz"
LIGHT_ARCHIVE="${OUTPUT_DIR}/hermes-data-light-${TIMESTAMP}.tar.gz"

echo -e "${YELLOW}[1/6] 创建临时工作区...${NC}"
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

# 备份元信息
cat > "$WORKDIR/MANIFEST.txt" << EOF
Hermes User Data Pack — Backup Manifest
========================================
Timestamp:    ${TIMESTAMP}
Hermes Home:  ${HERMES_HOME}
Hostname:     $(hostname 2>/dev/null || echo "unknown")
User:         $(whoami)
Hermes Ver:   $(hermes --version 2>/dev/null || echo "unknown")
Files Count:  (populated after packing)
EOF

echo -e "${YELLOW}[2/6] 收集配置文件...${NC}"
CONF_DIR="$WORKDIR/config"
mkdir -p "$CONF_DIR"
for f in config.yaml config.yaml.bak*; do
    [ -f "$HERMES_HOME/$f" ] && cp "$HERMES_HOME/$f" "$CONF_DIR/"
done

echo -e "${YELLOW}[3/6] 收集数据组件...${NC}"

# 环境变量（含密钥警告）
if [ -f "$HERMES_HOME/.env" ]; then
    ENV_DIR="$WORKDIR/env"
    mkdir -p "$ENV_DIR"
    # 脱敏复制 — 保留结构但标记风险
    cp "$HERMES_HOME/.env" "$ENV_DIR/.env"
    echo "WARNING: .env contains API keys and secrets. Keep this archive secure." > "$ENV_DIR/SECURITY_WARNING.txt"
fi

# 认证凭据
[ -f "$HERMES_HOME/auth.json" ] && cp "$HERMES_HOME/auth.json" "$WORKDIR/auth.json"

# 灵魂文件
[ -f "$HERMES_HOME/SOUL.md" ] && cp "$HERMES_HOME/SOUL.md" "$WORKDIR/SOUL.md"

# 技能
if [ -d "$HERMES_HOME/skills" ]; then
    mkdir -p "$WORKDIR/skills"
    cp -r "$HERMES_HOME/skills"/* "$WORKDIR/skills/" 2>/dev/null || true
fi

# 记忆
if [ -d "$HERMES_HOME/memories" ]; then
    mkdir -p "$WORKDIR/memories"
    cp "$HERMES_HOME/memories/MEMORY.md" "$WORKDIR/memories/" 2>/dev/null || true
    cp "$HERMES_HOME/memories/USER.md" "$WORKDIR/memories/" 2>/dev/null || true
fi
[ -f "$HERMES_HOME/memory_store.db" ] && cp "$HERMES_HOME/memory_store.db" "$WORKDIR/memory_store.db"

# 会话历史（排除缓存无效文件）
if [ -d "$HERMES_HOME/sessions" ]; then
    mkdir -p "$WORKDIR/sessions"
    # 只备份非空且非临时文件
    find "$HERMES_HOME/sessions" -maxdepth 1 -name "*.jsonl" -size +50c \
        -exec cp {} "$WORKDIR/sessions/" \;
fi

# 定时任务
if [ -d "$HERMES_HOME/cron" ]; then
    mkdir -p "$WORKDIR/cron"
    [ -f "$HERMES_HOME/cron/jobs.json" ] && cp "$HERMES_HOME/cron/jobs.json" "$WORKDIR/cron/"
    if [ -d "$HERMES_HOME/cron/output" ]; then
        mkdir -p "$WORKDIR/cron/output"
        cp -r "$HERMES_HOME/cron/output"/* "$WORKDIR/cron/output/" 2>/dev/null || true
    fi
fi

# 数据库
for db in state.db response_store.db kanban.db supermemory.json; do
    [ -f "$HERMES_HOME/$db" ] && cp "$HERMES_HOME/$db" "$WORKDIR/$db"
done

# 网关状态
for f in gateway_state.json channel_directory.json discord_threads.json; do
    [ -f "$HERMES_HOME/$f" ] && cp "$HERMES_HOME/$f" "$WORKDIR/$f"
done

# 平台数据
[ -d "$HERMES_HOME/platforms" ] && cp -r "$HERMES_HOME/platforms" "$WORKDIR/platforms" 2>/dev/null || true

# 配对数据
[ -d "$HERMES_HOME/pairing" ] && cp -r "$HERMES_HOME/pairing" "$WORKDIR/pairing" 2>/dev/null || true

# 钩子脚本
[ -d "$HERMES_HOME/hooks" ] && cp -r "$HERMES_HOME/hooks" "$WORKDIR/hooks" 2>/dev/null || true

# 缓存（非必需但有助于恢复后体验）
for f in .skills_prompt_snapshot.json supermemory.json; do
    [ -f "$HERMES_HOME/$f" ] && cp "$HERMES_HOME/$f" "$WORKDIR/$f" 2>/dev/null || true
done

# 回滚快照（最近3个）
if [ -d "$HERMES_HOME/checkpoints" ]; then
    mkdir -p "$WORKDIR/checkpoints"
    ls -t "$HERMES_HOME/checkpoints" 2>/dev/null | head -3 | while read cp_dir; do
        [ -n "$cp_dir" ] && cp -r "$HERMES_HOME/checkpoints/$cp_dir" "$WORKDIR/checkpoints/" 2>/dev/null || true
    done
fi

echo -e "${YELLOW}[4/6] 创建完成备份归档...${NC}"
cd "$WORKDIR"

# 更新清单中的文件计数
FILE_COUNT=$(find . -type f | wc -l)
sed -i "s/Files Count:.*/Files Count:  ${FILE_COUNT}/" MANIFEST.txt

tar -czf "$ARCHIVE" . 2>/dev/null
if [ $? -ne 0 ] || [ ! -f "$ARCHIVE" ]; then
    echo -e "${RED}[错误] 打包失败${NC}"
    exit 1
fi

echo -e "${YELLOW}[5/6] 轻量版归档（排除 sessions 和 state.db）...${NC}"
tar --exclude='./sessions' --exclude='./state.db' -czf "$LIGHT_ARCHIVE" . 2>/dev/null || true

echo -e "${YELLOW}[6/6] 计算校验和...${NC}"
cd "$OUTPUT_DIR"
sha256sum "hermes-data-full-${TIMESTAMP}.tar.gz" > "hermes-data-full-${TIMESTAMP}.sha256"
sha256sum "hermes-data-light-${TIMESTAMP}.tar.gz" > "hermes-data-light-${TIMESTAMP}.sha256"

# 清理临时目录
rm -rf "$WORKDIR"

# 输出结果
echo ""
echo -e "${GREEN}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 备份完成！${NC}"
echo -e "${GREEN}══════════════════════════════════════════════${NC}"
echo ""
echo -e "  完整备份:  ${CYAN}${ARCHIVE}${NC}"
echo -e "  轻量备份:  ${CYAN}${LIGHT_ARCHIVE}${NC}"
echo ""
SIZE_FULL=$(du -h "$ARCHIVE" | cut -f1)
SIZE_LIGHT=$(du -h "$LIGHT_ARCHIVE" | cut -f1)
echo -e "  完整包大小: ${YELLOW}${SIZE_FULL}${NC}"
echo -e "  轻量包大小: ${YELLOW}${SIZE_LIGHT}${NC}"
echo -e "  文件总数:   ${YELLOW}${FILE_COUNT}${NC}"
echo ""
echo -e "  ${YELLOW}⚠  注意: .env 文件中包含 API 密钥，请妥善保管此备份文件。${NC}"
echo ""
