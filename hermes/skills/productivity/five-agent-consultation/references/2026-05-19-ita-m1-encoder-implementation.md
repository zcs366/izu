# 2026-05-19 ITA M1 编码器v0.1 第一阶段交付

> M1启动后的第一个开发冲刺：修复FSQ故障 → 实现编码器v0.1 → 编写42个测试 → 全量169通过。
> 关键模式：先扫清测试故障再建新代码，编码器mock模式先行再实装。

## 会话流程

1. **基线检查**：运行全量测试 → 发现4个FSQ测试故障 + 依赖缺失(einops)
2. **修复FSQ测试**：
   - `test_soft_round_ste_forward`：temperature太低(t=0.1)导致tanh饱和，改用t=1.0+小值输入
   - `test_fsq_forward_with_temperature`等3个：FSQ.forward()期待3D(b,n,d)输入，但测试传2D(b,d)
   - FSQ源码也需修改：forward签名增加 `temperature` 参数并透传给 `quantize()`
3. **实现编码器v0.1** (`src/encoder.py`, 21.6KB, 从1.4KB扩15倍)：
   - `HiddenStateExtractor`：延迟加载模型/mock双模式，device自动检测
   - `ProjectionLayer`：正投影 + 逆投影双通路，支持梯度传播
   - `FSQQuantizer`：包装原始FSQ，适配temperature参数，处理2D/3D自动转型
   - `ITAEncoder`：encode/decode/round_trip/eval_core_set四大方法
   - `LatentCode`：dataclass数据结构
4. **设备管理**：提取器(CUDA)→投影层(CPU)→量化器(CPU)的设备不一致问题，通过device参数串联修复
5. **FSQ量化器shape修复**：`encode_to_indices`返回1D索引，`decode_from_indices`的`indices_to_codes`返回3D，需squeeze seq dim
6. **更新立项书v1.0→文档添加版本号规则**
7. **全量测试**：169/169全部通过

## 关键发现

### FSQ.forward() 签名修正
原始FSQ源码 `forward(self, z: Tensor)` 不接受temperature参数。修改为：
```python
def forward(self, z: Tensor, temperature: float = 0.1) -> Tuple[Tensor, Tensor]:
```
同时 `codes = self.quantize(z)` → `codes = self.quantize(z, temperature=temperature)`
并在 import 中增加 `Tuple`。

### 3D输入要求
FSQ.forward() 期待 (batch, seq, dim) 3D输入。单函数编码需要 (1, 1, dim)。FSQQuantizer 封装时自动 unsqueeze/squeeze 适配。

### 设备传递链
多Module管线中，所有子Module必须同设备：
```
extractor(device) → projection(device) → quantizer(device)
```
在ITAM1Encoder的 `__init__` 中统一从 extractor 获取 device 后传递给下游。

### Mock模式实现
`HiddenStateExtractor._mock_extract()` 基于 `hash(code_text)` 生成确定性随机种子，保证相同代码→相同向量：
```python
seed = hash(code_text) & 0x7FFFFFFF
rng = torch.Generator(device=self.device)
rng.manual_seed(seed)
length_factor = min(1.0, len(code_text) / 1000.0)
vec = torch.randn(1, self.hidden_dim, generator=rng, device=self.device)
vec = vec * (0.5 + length_factor * 0.5)
```

### ITAEncoder架构
```
encode(): code → HiddenStateExtractor → ProjectionLayer → [FSQQuantizer] → LatentCode
decode(): LatentCode → [FSQQuantizer.decode_from_indices] → ProjectionLayer.inverse_forward → code
round_trip(): encode → decode → compare(edit_similarity, cosine_similarity, exact_match)
```

## 交付物清单

| 文件 | 大小 | 变化 |
|------|------|------|
| `src/encoder.py` | 21.6KB | 从1.4KB完全重写 |
| `src/fsq/fsq.py` | +3行 | forward加temperature参数+Tuple import |
| `tests/test_encoder.py` | 14.7KB / 42 tests | 新增 |
| `tests/test_fsq.py` | 4.9KB / 9 tests | 从5修到9(4修复+1新增) |
| `docs/ita-project-charter-v1.0.md` | — | 增加版本号+状态跟踪模板 |

## 测试结果

| 模块 | 测试数 | 结果 |
|------|--------|------|
| test_encoder.py | 42 | ✅ 全过 |
| test_fsq.py | 9 | ✅ 全过 |
| test_budget.py | 27 | ✅ 全过 |
| test_complexity.py | 33 | ✅ 全过 |
| test_pipeline.py | 7 | ✅ 全过 |
| test_regression.py | 45 | ✅ 全过 |
| test_config.py | 3 | ✅ 全过 |
| test_dataset.py | 4 | ✅ 全过 |
| **合计** | **169** | **✅ 全量通过** |

## 用户偏好记录

- **立项书必须版本跟踪**：用户明确要求"立项书要随着进展调整，记得写清版本号"。已转化为陷阱十八和模板更新。

## 待办（M1 Phase 2）

1. 500个核心函数数据集生成器
2. 真实模型加载（Qwen-Coder 0.5B ~3GB下载）
3. 训练管线 train.py
4. 第一次连续模式训练（需GPU）
