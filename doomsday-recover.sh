#!/usr/bin/env bash
# =============================================================================
# 天师道场 · 末日恢复脚本 v2.0
# 用法: bash <(curl -sL https://raw.githubusercontent.com/zcs366/izu/backup-20260618/doomsday-recover.sh)
# 功能: 从 GitHub 拉取 doomsday 备份 → 解压 → 恢复到 ~/.hermes 和 workspace
# =============================================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
WORKSPACE="${WORKSPACE:-/mnt/i/hermes}"
BRANCH="backup-20260618"
GITHUB="https://raw.githubusercontent.com/zcs366/izu/$BRANCH"

echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo -e "${CYAN}  天师道场 · 末日恢复 v2.0${NC}"
echo -e "${CYAN}  ${TIMESTAMP}${NC}"
echo -e "${CYAN}══════════════════════════════════════════════${NC}"

# ─── [1] 前置检查 ───
echo -e "\n${YELLOW}[1/6] 前置检查...${NC}"

# 检查必要工具
for cmd in curl tar git; do
  if ! command -v $cmd &>/dev/null; then
    echo -e "${RED}  ❌ 缺少 $cmd，请先安装${NC}"
    exit 1
  fi
done
echo -e "  ${GREEN}✅ 工具齐全${NC}"

# ─── [2] 下载备份 ───
echo -e "\n${YELLOW}[2/6] 下载 doomsday 备份...${NC}"
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

echo -e "  ${CYAN}从 ${GITHUB}/backup-20260618_200355.tar.gz 下载...${NC}"
if curl -sL "$GITHUB/backup-20260618_200355.tar.gz" -o backup.tar.gz; then
  ARCHIVE_SIZE=$(du -h backup.tar.gz | cut -f1)
  echo -e "  ${GREEN}✅ 下载完成 (${ARCHIVE_SIZE})${NC}"
else
  echo -e "  ${RED}❌ 下载失败${NC}"
  exit 1
fi

# ─── [3] 校验下载 ───
echo -e "\n${YELLOW}[3/6] 校验备份文件...${NC}"
if tar -tzf backup.tar.gz &>/dev/null; then
  FILE_COUNT=$(tar -tzf backup.tar.gz | wc -l)
  echo -e "  ${GREEN}✅ 备份有效 (${FILE_COUNT} 个文件)${NC}"
else
  echo -e "  ${RED}❌ 备份文件损坏${NC}"
  exit 1
fi

# ─── [4] 备份当前状态 ───
echo -e "\n${YELLOW}[4/6] 备份当前状态...${NC}"
if [ -d "$HERMES_HOME" ]; then
  CURRENT_BACKUP="/tmp/hermes-pre-restore-${TIMESTAMP}.tar.gz"
  tar -czf "$CURRENT_BACKUP" -C "$(dirname "$HERMES_HOME")" "$(basename "$HERMES_HOME")" 2>/dev/null || true
  echo -e "  ${GREEN}✅ 当前状态已备份到 ${CURRENT_BACKUP}${NC}"
fi

# ─── [5] 执行恢复 ───
echo -e "\n${YELLOW}[5/6] 执行恢复...${NC}"

# 解压到临时目录
tar -xzf backup.tar.gz

# 恢复 Hermes 系统数据
if [ -d "hermes" ]; then
  echo -e "  ${CYAN}恢复 Hermes 系统数据...${NC}"
  
  # config.yaml
  if [ -f "hermes/config.yaml" ]; then
    mkdir -p "$HERMES_HOME"
    cp hermes/config.yaml "$HERMES_HOME/config.yaml"
    echo -e "    ✅ config.yaml (已脱敏，需手动填入 API key)"
  fi
  
  # SOUL.md
  [ -f "hermes/SOUL.md" ] && cp hermes/SOUL.md "$HERMES_HOME/SOUL.md" && echo -e "    ✅ SOUL.md"
  
  # skills
  if [ -d "hermes/skills" ]; then
    rm -rf "$HERMES_HOME/skills"
    cp -r hermes/skills "$HERMES_HOME/skills"
    SKILL_COUNT=$(find hermes/skills -name "SKILL.md" | wc -l)
    echo -e "    ✅ skills/ (${SKILL_COUNT} 个技能)"
  fi
  
  # memories
  if [ -d "hermes/memories" ]; then
    mkdir -p "$HERMES_HOME/memories"
    [ -f "hermes/memories/MEMORY.md" ] && cp hermes/memories/MEMORY.md "$HERMES_HOME/memories/"
    [ -f "hermes/memories/USER.md" ] && cp hermes/memories/USER.md "$HERMES_HOME/memories/"
    echo -e "    ✅ memories/"
  fi
  [ -f "hermes/memory_store.db" ] && cp hermes/memory_store.db "$HERMES_HOME/memory_store.db" && echo -e "    ✅ memory_store.db"
  
  # cron
  if [ -d "hermes/cron" ]; then
    mkdir -p "$HERMES_HOME/cron"
    [ -f "hermes/cron/jobs.json" ] && cp hermes/cron/jobs.json "$HERMES_HOME/cron/"
    echo -e "    ✅ cron/"
  fi
fi

# 恢复 Workspace 数据
if [ -d "workspace" ]; then
  echo -e "  ${CYAN}恢复 Workspace 数据...${NC}"
  [ -d "workspace/wiki" ] && mkdir -p "$WORKSPACE" && cp -r workspace/wiki "$WORKSPACE/wiki" && echo -e "    ✅ wiki/"
  [ -d "workspace/scripts" ] && cp -r workspace/scripts "$WORKSPACE/scripts" && echo -e "    ✅ scripts/"
  [ -d "workspace/izu-site" ] && cp -r workspace/izu-site "$WORKSPACE/izu-site" && echo -e "    ✅ izu-site/"
fi

echo -e "  ${GREEN}✅ 恢复完成${NC}"

# ─── 密钥恢复提示 ───
echo ""
echo -e "${YELLOW}══════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  ⚠️  密钥恢复提示${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}.env 和 auth.json 未包含在公开备份中。${NC}"
echo -e "  请从以下位置恢复密钥:"
echo -e ""
echo -e "    ${CYAN}1. 本机备份: /mnt/i/hermes/output/备份/hermes-secrets-*.tar.gz${NC}"
echo -e "    ${CYAN}2. 密码管理器${NC}"
echo -e "    ${CYAN}3. 手工填入 ~/.hermes/.env${NC}"
echo ""

# ─── [6] 重启提示 ───
echo -e "\n${YELLOW}[6/6] 后续操作...${NC}"
echo "  恢复后建议执行:"
echo ""
echo -e "  1. ${CYAN}填入 API 密钥:${NC}"
echo -e "     vim ~/.hermes/.env"
echo -e "     vim ~/.hermes/config.yaml  # 填入 api_key"
echo ""
echo -e "  2. ${CYAN}重启 Gateway:${NC}"
echo -e "     systemctl --user restart hermes-gateway"
echo ""
echo -e "  3. ${CYAN}验证技能:${NC}"
echo -e "     hermes skills list"
echo ""
echo -e "  4. ${CYAN}健康检查:${NC}"
echo -e "     hermes doctor"
echo ""

# 清理临时目录（保留备份文件）
rm -rf "$TMPDIR"

echo -e "${GREEN}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 末日恢复脚本执行完毕！${NC}"
echo -e "${GREEN}══════════════════════════════════════════════${NC}"
