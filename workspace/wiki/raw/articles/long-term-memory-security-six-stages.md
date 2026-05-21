---
source_url: https://mp.weixin.qq.com/s/D_guPaSSroZgm-SxIjfGzw
ingested: 2026-05-19
sha256: pending
title: Agent 长期记忆安全六阶段框架与记忆主权
author: 模安局
source: arXiv:2604.16548
---

# 长期记忆安全六阶段框架 核心笔记

**论文**：A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty

## 六阶段

1. Write — 写入必须视为特权操作
2. Store — 压缩放大型毒素、记忆幻觉
3. Retrieve — 不能只靠相似度
4. Execute — 检索→行为劫持的连续链路
5. Share — 跨Agent/跨用户传播
6. Forget/Rollback — 最难最关键

## 记忆主权（Mnemonic Sovereignty）

治理原语：谁能写/读/共享 + 元数据 + 版本管理 + 删除语义 + 可验证遗忘

## 对izu的启示

- Write Gate 不足 → 需来源标记+信任等级
- 检索仅靠相似度 → 需叠加权限判断
- 遗忘只有衰减 → 需可验证删除
