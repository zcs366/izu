#!/usr/bin/env bash
# md2html-batch.sh — Convert all .md files in a directory to .html
# Uses scripts/md2html.py from the same skill directory.
#
# Usage:
#   ./md2html-batch.sh /path/to/md/files
#
# Each .md file becomes .html in the same directory.
# Title is derived from the filename.
# Pairs well with multi-mode study (B->A->C) output.

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONVERTER="$SKILL_DIR/scripts/md2html.py"
TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: directory '$TARGET_DIR' not found"
    echo "Usage: $0 /path/to/md/files"
    exit 1
fi

if [ ! -f "$CONVERTER" ]; then
    echo "Error: md2html.py not found at $CONVERTER"
    exit 1
fi

count=0
for md_file in "$TARGET_DIR"/*.md; do
    [ -f "$md_file" ] || continue
    html_file="${md_file%.md}.html"
    base="$(basename "$md_file" .md)"

    # Skip existing HTML that's newer than the MD
    if [ -f "$html_file" ] && [ "$html_file" -nt "$md_file" ]; then
        echo "  skip $base.html (already current)"
        continue
    fi

    python3 "$CONVERTER" "$md_file" "$html_file" "$base"
    count=$((count + 1))
done

echo "Done: $count file(s) converted"
