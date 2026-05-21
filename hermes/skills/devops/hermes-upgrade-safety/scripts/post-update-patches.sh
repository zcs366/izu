#!/usr/bin/env bash
# ============================================================
# Hermes Post-Update Auto-Patch
# 在 hermes update 之后运行，自动恢复我们的定制改动
# 用法：bash ~/.hermes/scripts/post-update-patches.sh
# 安全：所有操作幂等，精准靶向，不误伤其他位置
# ============================================================
set -euo pipefail

HERMES_REPO="${HOME}/.hermes/hermes-agent"
TOOLSETS="${HERMES_REPO}/toolsets.py"
REPORT_FILE="${HOME}/.hermes/logs/post-update-patches.log"

mkdir -p "$(dirname "$REPORT_FILE")"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') Hermes Post-Update Patches ===" | tee -a "$REPORT_FILE"

PATCH_COUNT=0
SKIP_COUNT=0

# ── Patch 1: bing_search in _HERMES_CORE_TOOLS ──
# 锚点：4空格缩进的 "# Web" 注释（_HERMES_CORE_TOOLS 内唯一）
# sed: 匹配 "^    # Web$" 后下一行，替换 "web_search", "web_extract", → 追加 bing_search
if grep -q '"web_search", "web_extract", "bing_search",' "$TOOLSETS"; then
    echo "  ✓ bing_search already in _HERMES_CORE_TOOLS" | tee -a "$REPORT_FILE"
    SKIP_COUNT=$((SKIP_COUNT + 1))
else
    sed -i '/^    # Web$/{n;s/"web_search", "web_extract",/"web_search", "web_extract", "bing_search",/}' "$TOOLSETS"
    if grep -q '"web_search", "web_extract", "bing_search",' "$TOOLSETS"; then
        echo "  → Added bing_search to _HERMES_CORE_TOOLS" | tee -a "$REPORT_FILE"
        PATCH_COUNT=$((PATCH_COUNT + 1))
    else
        echo "  ✗ FAILED: could not add bing_search to _HERMES_CORE_TOOLS" | tee -a "$REPORT_FILE"
    fi
fi

# ── Patch 2: bing_search in TOOLSETS["web"]["tools"] ──
# 锚点："web": { → "tools": [...] 块内
if grep -q '"tools": \["web_search", "web_extract", "bing_search"\]' "$TOOLSETS"; then
    echo "  ✓ bing_search already in TOOLSETS[web][tools]" | tee -a "$REPORT_FILE"
    SKIP_COUNT=$((SKIP_COUNT + 1))
else
    sed -i '/"web": {/,/"tools":/{s/"tools": \["web_search", "web_extract"\]/"tools": ["web_search", "web_extract", "bing_search"]/}' "$TOOLSETS"
    if grep -q '"tools": \["web_search", "web_extract", "bing_search"\]' "$TOOLSETS"; then
        echo "  → Added bing_search to TOOLSETS[web][tools]" | tee -a "$REPORT_FILE"
        PATCH_COUNT=$((PATCH_COUNT + 1))
    else
        echo "  ✗ FAILED: could not add bing_search to TOOLSETS[web][tools]" | tee -a "$REPORT_FILE"
    fi
fi

# ── 汇总 ──
echo "=== Done: ${PATCH_COUNT} patches applied, ${SKIP_COUNT} skipped ===" | tee -a "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
