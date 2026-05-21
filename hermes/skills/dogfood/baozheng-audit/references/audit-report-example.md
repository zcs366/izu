# 包拯实战案例：ITA v1.0 → v1.1 编码器审计

> 日期：2026-05-19  
> 核心发现：Mock模式掩盖 + 指标虚高 + stats空功能  
> 修复：mock_mode标注 + stats分类修复

## 发现

| 项目 | 声明状态 | 审计结论 | 关键证据 |
|------|---------|---------|---------|
| 编码器 encode路径 | ✅ | ✅ 真正完成 | 隐状态提取→投影→量化→LatentCode全链路 |
| 编码器 decode路径 | ✅ | ⚠️ 有条件 | `_decode_hidden`恒等返回原文(TODO占位符) |
| round_trip指标 | ✅ | ❌ 虚假 | mock模式下edit_similarity=1.0是恒等映射结果 |
| 回归护城河 | ✅ | ✅ 真正完成 | 9个HL用例可构建/注册/执行 |
| 回归stats() | ✅ | ⚠️ 功能缺失 | categories字典永远硬编码为空 |
| FSQ量化器 | ✅ | ⚠️ 有条件 | 量化精度需训练数据验证 |

## 修复

1. `src/encoder.py`: LatentCode增加`mock_mode: bool`字段 → 非mock模式下调用方知道指标不可信
2. `src/regression.py`: `stats()`从硬编码空字典改为按用例名前缀分类

## 教训

- **Mock模式是最大的虚假完成源**——decode在mock下恒等映射，所有round-trip指标都是假数据
- **测试通过 ≠ 功能完整**——stats()返回了正确格式但内容是空的，测试不测内容
- **必须标注受限数据**——添加mock_mode字段让下游知道数据不可信
