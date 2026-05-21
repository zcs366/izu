# Installing Optional Hermes Agent Submodules

Hermes Agent ships several optional submodules in the main repository. These are
not installed by default and must be explicitly built from source.

## Finding Available Submodules

The repo uses git submodules declared in `.gitmodules`:

```bash
cd ~/.hermes/hermes-agent
cat .gitmodules
```

Each submodule's `path` field tells you where it lives relative to the repo root.
Check whether a submodule is initialized:

```bash
git submodule status
# Leading `-` = not initialized, `+` = modified, ` ` = clean
```

## Installation Procedure

All submodules live inside the Hermes repo. Install them from the repo root
using the same venv Hermes uses:

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate    # or: source .venv/bin/activate
uv pip install -e ./<submodule-name>
```

### Key Details

- **Use `uv pip install`**, not `pip install` — the repo uses `uv` for dependency
  management and pinning. Plain `pip` may resolve different versions.
- **Editable install (`-e`)** — the submodule is symlinked, so the code stays
  inside the repo tree and any git updates are reflected immediately.
- **Long timeout needed** — transitive dependencies can be heavy (transformers,
  wandb, pyarrow, polars, etc.). Use a timeout of at least 300 seconds:
  ```bash
  uv pip install -e ./tinker-atropos   # expect ~2.5-3 minutes
  ```
- **Resolution is cached** — subsequent installs reuse resolved packages (seconds
  instead of minutes).

## Verification

Not all submodule packages define `__version__`. Verify by importing a module
rather than checking version:

```python
# ✅ Good — checks the package is importable
python -c "import <package>.config; print('OK')"

# ❌ May fail if __init__.py is empty
python -c "import <package>; print(<package>.__version__)"
```

For tinker-atropos specifically:

```bash
python -c "import tinker_atropos.config; print('OK')"
python -c "import tinker_atropos.types; print('OK')"
```

## Example: tinker-atropos

A Reinforcement Learning training framework that bridges Tinker (training API)
and Atropos (RL framework). Used for GRPO/RL fine-tuning of LLMs.

### Location

`/home/zcs/.hermes/hermes-agent/tinker-atropos/`

### Dependencies (transitive)

Installs 33+ packages including: atroposlib, tinker, transformers, datasets,
wandb, gymnasium, fastapi, uvicorn, pandas, polars, pyarrow, nltk, safetensors.

### CLI Entry Point

```bash
rl-server   # FastAPI RL API server (defined in pyproject.toml [project.scripts])
```

### Runtime Dependencies (NOT installed automatically)

PyTorch (`torch`) is imported by `tinker_atropos.trainer` at runtime but is
NOT listed as a dependency. Install it separately only if you intend to run
training:

```bash
uv pip install torch
```

Basic configuration and type imports work without torch.

### Package Structure

```
tinker-atropos/
├── pyproject.toml
├── configs/                  # YAML configs
├── launch_training.py        # Entry point for training runs
└── tinker_atropos/
    ├── __init__.py           # Empty — no __version__
    ├── config.py             # TinkerAtroposConfig (Pydantic-based)
    ├── types.py              # Request/response type definitions
    ├── trainer.py            # TinkerAtroposTrainer (requires torch)
    ├── environments/         # RL environments (GSM8K, etc.)
    └── utils/
        └── download_weights.py
```

## Pitfalls

- **`__version__` may not exist** — the `__init__.py` can be empty. Use a
  concrete submodule import for verification.
- **Timed out first install** — heavy downloads (wandb ~26 MB, pyarrow ~47 MB,
  transformers ~10 MB) through a proxy can exceed a default 120s timeout. Use
  300s.
- **`--progress-bar` flag unsupported by `uv`** — `uv pip install` does NOT
  accept `--progress-bar` (that's a `pip` flag). Using it will fail with
  `error: unexpected argument '--progress-bar' found`. Remove it if migrating
  from pip commands.
- **Proxy in China: expect long downloads** — through `http://127.0.0.1:7890`:
  initial submodule resolution ~2.5 min (96 packages), torch alone ~35 min
  (12 nvidia packages + 506 MB torch wheel). Use `terminal(background=True)`
  with `notify_on_complete=True` for hands-off installs rather than synchronous
  timeouts.
- **Verification tip: write a temp script** — in sandboxed environments,
  inline Python with `-c` can return empty output. Prefer writing a temp file
  and running it:
  ```bash
  cat > /tmp/check_mod.py << 'EOF'
  import tinker_atropos.config
  import tinker_atropos.types
  print('OK')
  EOF
  /home/zcs/.hermes/hermes-agent/venv/bin/python /tmp/check_mod.py
  ```
  Using the full venv Python path (`venv/bin/python`) is more reliable than
  `source venv/bin/activate && python` in restricted contexts.
- **trainer.py needs torch** — don't expect the trainer module to work without
  a separate `pip install torch`. Core config/types work fine.
- **Venv matters** — the submodule must be installed into the same venv as
  Hermes itself (`~/hermes/hermes-agent/venv/`), not a system Python or a
  different virtualenv.
- **`source venv/bin/activate` can be blocked** — in some agent sandbox
  environments, interactive shell commands like `source` trigger user
  confirmation prompts. Use full paths to the venv Python binary instead:
  `/home/zcs/.hermes/hermes-agent/venv/bin/python`.
