# Model Switching via config.yaml

## Direct config edit (fastest)

When the user wants to switch models between providers that use the same `base_url`:

```bash
# Edit config.yaml directly
hermes config edit
# Change: model.default: deepseek-v4-flash → deepseek-v4-pro

# Or via patch tool:
# old: model:\n  default: <current-model>
# new: model:\n  default: <target-model>
```

**Critical timing rule**: Config changes to `model.default` take effect on the **next message / next session start**, NOT mid-conversation. The model is loaded once at conversation creation time. The current message still uses the old model.

**Provider consistency check**: When switching models, ensure `model.provider` and `model.base_url` remain valid. E.g., switching `deepseek-v4-flash` → `deepseek-v4-pro` with `provider: deepseek` and `base_url: https://api.deepseek.com/v1` is safe — both models live at the same endpoint.

## Interactive picker

```bash
hermes model          # Interactive model/provider browser
```

## CLI flags (per-invocation)

```bash
hermes chat -m deepseek-v4-pro --provider deepseek
```

## Caveats

- **Cross-provider switches**: If switching from DeepSeek to Anthropic, also update `model.provider` and `model.base_url`. Use `hermes model` interactive picker for safety.
- **API key validity**: Ensure the target model's API key is available (check `.env` or credential pool).
- **Auxiliary model independence**: `auxiliary.*.provider` settings are separate from `model.default` and must be updated independently if needed.
