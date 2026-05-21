#!/usr/bin/env bash
set -euo pipefail
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
H="${HERMES_HOME:-$HOME/.hermes}"
W="/mnt/i/hermes"
SD="$(cd "$(dirname "$0")" && pwd)"
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo -e "${CYAN}  天师道场 · 末日恢复${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo -e "\n${YELLOW}[1/4] Hermes...${NC}"
mkdir -p "$H/skills" "$H/memories" "$H/cron"
[ -f "$SD/hermes/config.yaml" ] && cp "$SD/hermes/config.yaml" "$H/"
[ -f "$SD/hermes/SOUL.md" ] && cp "$SD/hermes/SOUL.md" "$H/"
[ -d "$SD/hermes/skills" ] && cp -r "$SD/hermes/skills"/* "$H/skills/" 2>/dev/null
[ -d "$SD/hermes/memories" ] && cp -r "$SD/hermes/memories"/* "$H/memories/" 2>/dev/null
[ -f "$SD/hermes/memory_store.db" ] && cp "$SD/hermes/memory_store.db" "$H/"
echo -e "${GREEN}✅ Hermes 系统恢复${NC}"
echo -e "\n${YELLOW}[2/4] 工作区 wiki...${NC}"
[ -d "$SD/workspace/wiki" ] && mkdir -p "$W/wiki" && cp -r "$SD/workspace/wiki"/* "$W/wiki/" 2>/dev/null
echo -e "${GREEN}✅ 工作区恢复${NC}"
echo -e "\n${YELLOW}[3/4] 代码仓库...${NC}"
mkdir -p "$W"
for repo in izu ita; do
  [ ! -d "$W/$repo" ] && git clone --depth 1 "git@github.com:zcs366/$repo.git" "$W/$repo" 2>/dev/null && echo -e "  ${GREEN}✅ $repo${NC}" || echo -e "  ✅ $repo (已有)${NC}"
done
echo -e "\n${YELLOW}[4/4] 密钥提示...${NC}"
echo -e "  ${YELLOW}⚠  API 密钥已脱敏，需手动填入 config.yaml${NC}"
echo "    DeepSeek → https://platform.deepseek.com"
echo "    OpenRouter → https://openrouter.ai/keys"
echo "    MiniMax → https://platform.minimaxi.com"
echo -e "\n${GREEN}✅ 完成！重启: ${CYAN}systemctl --user restart hermes-gateway${NC}"
