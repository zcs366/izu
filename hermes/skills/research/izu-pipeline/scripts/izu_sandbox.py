#!/usr/bin/env python3
"""
izu ProcessSandbox v1.0 —— 匠石方案落地
基于 OpenHands ProcessSandboxService 的设计模式，用 subprocess + tempfile 实现。
零 Docker 依赖，零 openhands-* 包引入，约 200 行纯 Python。

设计原则：
- 代码优先（匠石原则）：所有逻辑用代码，不调 LLM
- 最小依赖：只依赖 Python 标准库
- 自动清理：沙箱退出后不留痕迹
- 超时保护：死循环/恶意代码自动终止

用法：
    from izu_sandbox import Sandbox
    s = Sandbox()
    s.write_file("test.py", "print('hello')")
    result = s.exec("python3 test.py")
    print(result['stdout'])  # 'hello\n'
    s.cleanup()
"""

import subprocess
import tempfile
import os
import shutil
import time
from pathlib import Path
from datetime import datetime


# ── 安全配置 ──
DEFAULT_TIMEOUT = 30          # 默认超时（秒）
MAX_TIMEOUT = 300             # 最大超时
MAX_OUTPUT_BYTES = 1024 * 1024  # 最大输出 1MB
FORBIDDEN_COMMANDS = [        # 黑名单（前缀匹配）
    "rm -rf /", "mkfs.", "dd if=", ":(){ :|:& };:",
    "> /dev/sda", "chmod 777 /", "wget", "curl",
]


class Sandbox:
    """轻量进程沙箱。基于 tempfile + subprocess 实现隔离执行。"""

    def __init__(self, workdir: str = None, label: str = ""):
        """
        Args:
            workdir: 工作目录路径。None 则自动创建临时目录。
            label: 标签，用于日志。
        """
        self.label = label or f"sandbox_{int(time.time())}"
        self._own_workdir = workdir is None
        self.workdir = workdir or tempfile.mkdtemp(prefix="izu_sandbox_")
        self.created_at = datetime.now().isoformat()
        self.exec_count = 0
        self._cleaned = False
        Path(self.workdir).mkdir(parents=True, exist_ok=True)

    # ── 核心方法 ──

    def exec(self, cmd: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
        """在沙箱内执行命令。

        Returns:
            {"exit_code": int, "stdout": str, "stderr": str, "timed_out": bool, "duration_ms": int}
        """
        if self._cleaned:
            return {"exit_code": -1, "stdout": "", "stderr": "Sandbox已清理", "timed_out": False, "duration_ms": 0}

        self._check_forbidden(cmd)
        timeout = min(timeout, MAX_TIMEOUT)
        self.exec_count += 1

        t0 = time.time()
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=self.workdir,
                capture_output=True, text=True,
                timeout=timeout,
            )
            stdout = result.stdout[:MAX_OUTPUT_BYTES]
            stderr = result.stderr[:MAX_OUTPUT_BYTES]
            timed_out = False
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            stdout = ""
            stderr = f"命令超时（{timeout}秒）"
            timed_out = True
            exit_code = -1

        duration_ms = int((time.time() - t0) * 1000)

        return {
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": timed_out,
            "duration_ms": duration_ms,
        }

    def write_file(self, path: str, content: str):
        """在沙箱内写入文件。自动创建父目录。"""
        full_path = os.path.join(self.workdir, path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(self.workdir)):
            raise ValueError(f"路径逃逸: {path}")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    def read_file(self, path: str) -> str:
        """从沙箱内读取文件。"""
        full_path = os.path.join(self.workdir, path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(self.workdir)):
            raise ValueError(f"路径逃逸: {path}")
        if not os.path.exists(full_path):
            return ""
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def exists(self, path: str) -> bool:
        """检查沙箱内文件是否存在。"""
        return os.path.exists(os.path.join(self.workdir, path))

    def list_files(self, subdir: str = "") -> list:
        """列出沙箱内文件。"""
        target = os.path.join(self.workdir, subdir) if subdir else self.workdir
        if not os.path.exists(target):
            return []
        files = []
        for root, dirs, filenames in os.walk(target):
            for f in filenames:
                rel = os.path.relpath(os.path.join(root, f), self.workdir)
                size = os.path.getsize(os.path.join(root, f))
                files.append({"path": rel, "size": size})
        return files

    def exec_python(self, code: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
        """执行 Python 代码片段。自动写入临时文件后执行。"""
        tmp_file = f"_izu_tmp_{self.exec_count}.py"
        self.write_file(tmp_file, code)
        return self.exec(f"python3 {tmp_file}", timeout=timeout)

    def cleanup(self):
        """清理沙箱：删除临时目录及所有内容。"""
        if self._cleaned:
            return
        try:
            shutil.rmtree(self.workdir, ignore_errors=True)
            self._cleaned = True
        except Exception as e:
            print(f"[Sandbox] 清理警告: {e}")

    def stats(self) -> dict:
        """返回沙箱统计信息。"""
        total_size = 0
        file_count = 0
        if os.path.exists(self.workdir):
            for root, dirs, files in os.walk(self.workdir):
                for f in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except OSError:
                        pass
                    file_count += 1
        return {
            "label": self.label,
            "workdir": self.workdir,
            "created_at": self.created_at,
            "exec_count": self.exec_count,
            "file_count": file_count,
            "total_size_bytes": total_size,
            "cleaned": self._cleaned,
        }

    @staticmethod
    def extract_code_blocks(markdown_text: str) -> list:
        """从 Markdown 文本中提取所有代码块。"""
        import re
        blocks = []
        pattern = r"```(\w+)?\n(.*?)```"
        for m in re.finditer(pattern, markdown_text, re.DOTALL):
            lang = m.group(1) or "text"
            code = m.group(2).strip()
            line_start = markdown_text[:m.start()].count("\n") + 1
            if code:
                blocks.append({"language": lang, "code": code, "line_start": line_start})
        return blocks

    def _check_forbidden(self, cmd: str):
        """检查命令是否命中黑名单。"""
        cmd_lower = cmd.lower().replace(" ", "")
        for forbidden in FORBIDDEN_COMMANDS:
            if forbidden.lower().replace(" ", "") in cmd_lower:
                raise ValueError(f"禁止执行: {cmd[:80]}... (命中黑名单: {forbidden})")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()

    def __repr__(self):
        return f"Sandbox({self.label}, {self.workdir}, execs={self.exec_count})"


def quick_exec(code: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """一行式：创建沙箱 → 执行代码 → 清理 → 返回结果。"""
    with Sandbox() as s:
        return s.exec_python(code, timeout=timeout)


def validate_code_blocks(markdown_text: str, timeout: int = DEFAULT_TIMEOUT) -> list:
    """验证 Markdown 中的所有可执行代码块。"""
    results = []
    blocks = Sandbox.extract_code_blocks(markdown_text)
    executable_langs = {"python", "py", "python3", "bash", "sh", "shell"}

    with Sandbox() as s:
        for i, block in enumerate(blocks):
            if block["language"] not in executable_langs:
                continue
            if block["language"] in ("python", "py", "python3"):
                result = s.exec_python(block["code"], timeout=timeout)
            else:
                s.write_file(f"_script_{i}.sh", block["code"])
                result = s.exec(f"bash _script_{i}.sh", timeout=timeout)
            results.append({
                "block_index": i,
                "language": block["language"],
                "line_start": block["line_start"],
                "exit_code": result["exit_code"],
                "stdout": result["stdout"][:500],
                "stderr": result["stderr"][:500],
                "timed_out": result["timed_out"],
                "duration_ms": result["duration_ms"],
            })
    return results
