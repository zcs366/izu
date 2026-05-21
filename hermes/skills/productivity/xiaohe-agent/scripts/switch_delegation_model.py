#!/usr/bin/env python3
"""
萧何·模型切换守护 (v1.0)

职责：按时段切换delegation子代理模型
  00:00 → 08:00: MiMo V2.5 非Pro（非高峰期0.8x系数）
  08:00 → 24:00: MiMo V2.5 Pro（白天全量能力）

用法：
  python3 switch_delegation_model.py pro     # 切到Pro
  python3 switch_delegation_model.py nonpro  # 切到非Pro

日志写入 ~/.hermes/logs/model_switch.log

适用条件：当模型提供商提供非高峰期折扣/系数时，可以用两个no_agent cron
+ 本脚本实现自动化时段切换。零token成本，仅修改config.yaml的一行。
"""
import os, sys, re
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".hermes" / "config.yaml"
LOG_PATH = Path.home() / ".hermes" / "logs" / "model_switch.log"

TARGETS = {
    "pro": {
        "model": "mimo-v2.5-pro",
        "label": "MiMo V2.5 Pro",
        "desc": "白天全量模式"
    },
    "nonpro": {
        "model": "mimo-v2.5",
        "label": "MiMo V2.5 非Pro",
        "desc": "非高峰期模式（0.8x系数）"
    }
}

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def switch(target_key):
    if target_key not in TARGETS:
        log(f"❌ 未知目标: {target_key}，可选: pro / nonpro")
        return False

    target = TARGETS[target_key]

    with open(str(CONFIG_PATH)) as f:
        content = f.read()

    new_content = re.sub(
        r'(delegation:\n(?:\s+[^:]+:.*\n)*\s+model:\s*).*',
        f'\\1{target["model"]}                  # 子代理（{target["label"]}）：{target["desc"]}',
        content
    )

    if new_content == content:
        log(f"⚠️ 正则替换未命中，尝试直接替换模型名...")
        for old in ["mimo-v2.5-pro", "mimo-v2.5"]:
            if old in content:
                new_content = content.replace(old, target["model"])
                break

    if new_content == content:
        log(f"❌ 替换失败，未找到匹配的模型名")
        return False

    with open(str(CONFIG_PATH), "w") as f:
        f.write(new_content)

    log(f"✅ delegation.model → {target['label']}（{target['desc']}）")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 switch_delegation_model.py [pro|nonpro]")
        sys.exit(1)
    success = switch(sys.argv[1])
    sys.exit(0 if success else 1)
