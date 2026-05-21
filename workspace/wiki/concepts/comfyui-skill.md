---
name: ComfyUI Skill
type: concept
created: 2026-05-09
updated: 2026-05-09
status: active
confidence: medium
sources:
  - raw/articles/hermes-comfyui-skill-wechat.md
tags:
  - skill
  - comfyui
  - image-generation
  - video-generation
  - creative
---

# ComfyUI Skill

Hermes Agent 内置的多媒体生成 Skill，将 [[comfyui]] 的图像/视频/音频生成能力封装为 Agent 可直接调用的接口。

## 核心能力

- **生命周期管理**：通过 comfy-cli 自动安装、启动 ComfyUI 及自定义节点
- **原生 API 调用**：走 ComfyUI REST + WebSocket API，非截图/UI 模拟
- **工作流管理**：自动解析工作流 JSON 的可注入参数（prompt、seed、LoRA 权重、尺寸等），建立参数映射层
- **多实例路由**：支持注册多个 ComfyUI 实例（本地/远程/不同显卡），执行时指定路由

## 支持的操作

- 🖼️ 文生图、图生图
- 🎬 视频生成（配合 AnimateDiff、Wan、HunyuanVideo 等工作流）
- 🎵 音频生成（配合 AudioCraft 工作流）
- 🔄 批量处理（批量 prompt、批量 seed）
- ⛓️ 链式工作流（出图 → 放大 → 局部重绘，全自动编排）

## 安装位置

```
~/.hermes/skills/creative/comfyui/
```

通过 Hermes CLI 安装：
```
hermes skills install creative/comfyui
```

## 使用示例

直接对 Hermes 说：
> 使用 ComfyUI 帮我生成一张猫咪图片，ComfyUI 运行地址: http://192.168.33.106:8188/

Agent 自动执行：
1. 检查 ComfyUI 服务是否在线
2. 找到对应工作流 → 注入 prompt → 设置 seed
3. 调用 API 执行生成 → 返回结果

## 核心价值

将 ComfyUI 从"需要手动操作的工具"变为"Agent 可编排的能力"。写文章、做 PPT、生成配图——以前步骤是断开的，现在全部由 Agent 串起来。

## 相关页面

- [[hermes-agent]] — 宿主 Agent
- [[agent-skills-system]] — Hermes Agent 技能系统
- [[comfyui]] — 底层图像生成引擎
