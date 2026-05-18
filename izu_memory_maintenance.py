#!/usr/bin/env python3
"""
izu_memory_maintenance.py — 记忆系统自动维护流水线

每6小时跑一次：
  1. 压缩超50轮的session
  2. 清理待遗忘session
  3. 生成记忆健康报告
  4. Self Model快照（只在凌晨运行）
"""
import sys, os, subprocess
from datetime import datetime
from pathlib import Path

IZU_DIR = Path("/mnt/i/hermes/izu")
HERMES_HOME = Path(os.getenv('HERMES_HOME', Path.home() / '.hermes'))
OUTPUT_DIR = Path("/mnt/i/hermes/output/doc/memory_health")

def run(*args):
    result = subprocess.run(
        [sys.executable, str(IZU_DIR / "izu_session_memory.py")] + list(args),
        capture_output=True, text=True, cwd=str(IZU_DIR)
    )
    return result.stdout + result.stderr

def main():
    now = datetime.now()
    is_midnight = now.hour in [0, 6]  # 0:00 or 6:00 also do self model
    
    print(f"🧹 记忆维护流水线 — {now.strftime('%Y-%m-%d %H:%M')}\n")
    
    # 1. 压缩需压缩的session
    print("=" * 50)
    print("📦 Step 1: 压缩...")
    compact_out = run("compact")
    print(compact_out)
    
    # 2. 遗忘清理
    print("=" * 50)
    print("🗑️  Step 2: 清理...")
    purge_out = run("purge")
    print(purge_out)
    
    # 3. 生成报告
    print("=" * 50)
    print("📊 Step 3: 报告...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIR / f"memory_health_{now.strftime('%Y%m%d_%H%M')}.md"
    
    report_out = subprocess.run(
        [sys.executable, str(IZU_DIR / "izu_session_memory.py"), "report"],
        capture_output=True, text=True, cwd=str(IZU_DIR)
    )
    
    report_text = report_out.stdout + report_out.stderr
    report_text = f"""# 🧠 记忆系统健康报告
> 生成: {now.strftime('%Y-%m-%d %H:%M')}
> 自动维护流水线

---

{report_text}

---

## 工作记忆快照

"""
    # 附加工作记忆
    wm_out = subprocess.run(
        [sys.executable, str(IZU_DIR / "izu_working_memory.py"), "snapshot"],
        capture_output=True, text=True, cwd=str(IZU_DIR)
    )
    report_text += wm_out.stdout
    report_text += f"\n报告: {report_path}\n"
    
    report_path.write_text(report_text)
    print(f"  报告已写入: {report_path}")
    
    # 4. Self Model快照（凌晨6点跑）
    if is_midnight:
        print("=" * 50)
        print("🧬 Step 4: Self Model快照...")
        sm_out = subprocess.run(
            [sys.executable, str(IZU_DIR / "izu_self_model.py"), "snapshot"],
            capture_output=True, text=True, cwd=str(IZU_DIR)
        )
        print(sm_out.stdout + sm_out.stderr)
    
    print("\n✅ 记忆维护完成")

if __name__ == '__main__':
    main()
