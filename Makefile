# =============================================================================
# izu — Makefile
#
# 使用说明：`make <target>`
# 默认目标：`make` 或 `make help`
# =============================================================================

.PHONY: help install install-dev test test-quick test-coverage lint clean format all

# ── 默认目标 ──────────────────────────────────────────────────────────────────
help:  ## 显示本帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── 安装 ──────────────────────────────────────────────────────────────────────
install:  ## pip install -e .（普通安装）
	pip install -e .

install-dev:  ## pip install -e ".[dev]"（包含开发依赖）
	pip install -e ".[dev]"

# ── 测试 ──────────────────────────────────────────────────────────────────────
test:  ## 运行全部测试（详细输出）
	pytest -v

test-quick:  ## 快速运行测试（简洁输出 + 短回溯）
	pytest -q --tb=short

test-coverage:  ## 运行测试并显示代码覆盖率
	pytest --cov=izu --cov-report=term

# ── 代码检查 ──────────────────────────────────────────────────────────────────
lint:  ## 检查所有 .py 文件的 Python 语法（py_compile）
	@echo "===== 语法检查 ====="
	@errors=0; \
	find . -name '*.py' ! -path './.*' -print0 | while IFS= read -r -d '' f; do \
		python -m py_compile "$$f" 2>&1 | grep -v "^$$" && errors=1; \
	done; \
	if [ "$$errors" -eq 0 ]; then \
		echo "所有文件语法正确。"; \
	fi

# ── 格式化（仅建议，不强制安装工具） ─────────────────────────────────────────
format:  ## 代码格式化（建议使用 ruff format 或 black）
	@echo "===== 格式化建议 ====="
	@echo "推荐使用以下工具之一格式化代码："
	@echo "  pip install ruff && ruff format ."
	@echo "  pip install black && black ."
	@echo ""
	@echo "当前未安装格式化工具，跳过格式化。"

# ── 清理 ──────────────────────────────────────────────────────────────────────
clean:  ## 删除 __pycache__、.pytest_cache、*.pyc
	@echo "===== 清理构建/缓存文件 ====="
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	@echo "清理完成。"

# ── 组合任务 ──────────────────────────────────────────────────────────────────
all: test lint  ## 运行全部测试 + 语法检查（CI 入口）
	@echo "===== all 完成 ====="
