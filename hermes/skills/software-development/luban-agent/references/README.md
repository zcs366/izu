本目录包含鲁班的参考文档：

- `paper-engineering-audit-methodology.md` — 论文→工程可行性审计方法（2026-05-16实战验证）。审计四步法、判断框架（能干/窄干/不能干）、量化模板、工时单位约定、能力要求、常见陷阱、实战案例。

该文件在 SKILL.md 的 2.8 节（论文→工程可行性审计）中有详细描述。

- `code-decoder-architecture.md` — 代码解码器架构模板：从隐空间重建代码。PythonTokenizer(4096词表) + CodeDecoder(Transformer 2层) + ITADecoder封装。含状态管理（mock/未训练/已训练三级）、自回归生成策略、loss下降验证、集成模式。
