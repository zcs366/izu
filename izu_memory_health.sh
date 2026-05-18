#!/bin/bash
# izu_memory_health.sh — 记忆系统健康检查一键报告
# 运行所有三个P0工具，输出统一报告
# 建议: 每天08:00运行一次

IZU_DIR="/mnt/i/hermes/izu"
REPORT_DIR="/mnt/i/hermes/output/doc/memory_health"
TIMESTAMP=$(date +%Y%m%d_%H%M)
REPORT_FILE="$REPORT_DIR/memory_health_$TIMESTAMP.md"

mkdir -p "$REPORT_DIR"

cat > "$REPORT_FILE" << EOF
# 🧠 记忆系统健康报告
> 生成: $(date '+%Y-%m-%d %H:%M')
> 工具: izu_session_memory + izu_working_memory + izu_self_model

---

EOF

echo "📊 Session记忆扫描..." >> "$REPORT_FILE"
cd "$IZU_DIR" && python3 izu_session_memory.py audit >> "$REPORT_FILE" 2>&1

echo "" >> "$REPORT_FILE"
echo "📉 衰减分析..." >> "$REPORT_FILE"
cd "$IZU_DIR" && python3 izu_session_memory.py decay >> "$REPORT_FILE" 2>&1

echo "" >> "$REPORT_FILE"
echo "🧬 Self Model 快照..." >> "$REPORT_FILE"
cd "$IZU_DIR" && python3 izu_self_model.py snapshot >> "$REPORT_FILE" 2>&1

echo "" >> "$REPORT_FILE"
echo "🧠 工作记忆快照..." >> "$REPORT_FILE"
cd "$IZU_DIR" && python3 izu_working_memory.py snapshot >> "$REPORT_FILE" 2>&1

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "报告: $REPORT_FILE" >> "$REPORT_FILE"

echo "✅ 记忆健康报告已生成: $REPORT_FILE"
wc -l "$REPORT_FILE"
