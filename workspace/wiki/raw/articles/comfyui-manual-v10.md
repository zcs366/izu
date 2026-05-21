---
source_url: file:///mnt/i/hermes/wiki_dropbox/comfyui-manual-v1.0.md
ingested: 2026-05-11
sha256: 23362e5da87f7ca32b52d63e2543cc65c9566784d142babd5b012930c869258f
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: ComfyUI 完全学习手册
---

# ComfyUI 完全学习手册

> 来源: comfyui-manual-v1.0.md（用户存入 wiki_dropbox）

# ComfyUI 完全学习手册

> **版本**: 2026-05 | **编译**: 军师祭酒
> 
> 术语约定：关键术语首次出现时标注英文原文（括号内），后续沿用中文。

---

# 第一章：ComfyUI 概览与核心理念

## 1.1 什么是 ComfyUI

ComfyUI 是一个**节点式（node-based）** 的 AI 生成界面，由开发者 **comfyanonymous** 于 2023 年初在 GitHub 上开源发布。它脱胎于 Stable Diffusion 社区，但如今已发展为支持图像、视频、音频、3D 等多种生成任务的统一平台。

**核心设计哲学**：用**可视化编程（visual programming）** 替代传统 WebUI 的固定面板。用户通过拖拽连接「节点（nodes）」来构建生成流水线，就像搭积木一样——每个节点负责一个特定功能（加载模型、编码文本、采样、解码、保存等），节点之间的「连线（links）」决定了数据的流动方向。

### 1.1.1 与其他工具的对比

| 维度 | ComfyUI | Automatic1111 (SD WebUI) | Forge | Fooocus | MidJourney |
|------|---------|--------------------------|-------|---------|------------|
| **易用性** | 陡峭 | 容易 | 容易 | 极简单 | 极简单 |
| **可控性** | 无上限 | 高 | 高 | 低 | 极低 |
| **速度** | 最快（图优化） | 基准线 | 比 A1111 快 10-30% | 中等 | 云端 |
| **VRAM 需求** | 最低（SDXL 仅 6GB） | 高（SDXL 需 8GB） | 较低 | 中等 | 云端 |
| **Flux 支持** | 首批支持 | 有限 | 支持 | 不支持 | 不支持 |
| **视频生成** | 支持 Wan/Hunyuan | 不支持 | 不支持 | 不支持 | 不支持 |
| **3D 生成** | 支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| **生产环境** | ✅ 适合 | ⚠️ 可行 | ⚠️ 可行 | ❌ | ❌ |
| **学习曲线** | 10-20 小时 | 1-2 小时 | 1-2 小时 | 10 分钟 | 0 |

**结论**：ComfyUI 面向**重度用户（power user）**——追求极致控制、希望第一时间使用最新模型、需要可复现工作流的用户。日常简单出图，Forge 或 Fooocus 更省心。

## 1.2 2026 年生态地位

- **估值 $5 亿**：2026 年 4 月完成 $3000 万融资（TechCrunch 报道），"ComfyUI 工程师/艺术家"已成为工作室招聘岗位
- **NVIDIA 官方合作**：GDC 2026 上 NVIDIA 宣布与 ComfyUI 深度合作，RTX 50 系列上实现 **2.5× 加速**和 **60% VRAM 降低**，并发布官方博客教程
- **VFX 行业采纳**：ActionVFX 推出首个 "Introduction to ComfyUI for VFX" 官方课程（15 模块）；Moment Factory 使用 ComfyUI 完成建筑级投影映射项目
- **Netflix 游戏生产**：ComfyUI 被用于 Netflix 游戏制作的 AI 管线

## 1.3 核心概念速览

| 概念 | 英文 | 说明 |
|------|------|------|
| 节点 | Node | 功能模块，每个节点执行一个操作 |
| 工作流 | Workflow | 节点构成的图（graph），保存为 JSON 或嵌入图像 |
| 连线 | Link | 节点之间的数据通道，颜色代表数据类型 |
| 检查点 | Checkpoint | 完整的基础模型文件（含模型+CLIP+VAE） |
| 潜空间 | Latent Space | 图像的压缩表示，VAE 在像素和潜空间之间转换 |
| 采样器 | Sampler | 从噪声生成图像的核心算法 |
| 调度器 | Scheduler | 控制采样过程中噪声衰减方式的策略 |
| 条件 | Conditioning | 指引生成方向的文本/图像输入（如 prompt） |
| LoRA | Low-Rank Adaptation | 轻量模型微调，注入风格/角色/概念 |
| ControlNet | — | 通过额外条件（姿势、深度、边缘等）精确控制生成 |

## 1.4 为什么要用 ComfyUI

1. **极致的模块化和可复用性**：工作流可保存为 JSON，分享即用。不同工作流可组合拼接
2. **最高的资源效率**：同模型下比 A1111 节省 20-30% VRAM，速度更快
3. **最先支持新模型**：Flux、Wan2.1、Hunyuan Video 都是 ComfyUI 首批支持
4. **生产级可靠性**：无 GUI 模式可运行在服务器上，通过 API 调用
5. **活性的社区生态**：Registry 上有数千个自定义节点（custom node），覆盖几乎所有需求

---

# 第二章：安装部署全指南

## 2.1 系统需求

### GPU 要求

| 目标 | 最低 VRAM | 推荐 VRAM | 说明 |
|------|-----------|-----------|------|
| SD 1.5 (512×512) | 4 GB | 6 GB | 基本可用 |
| SDXL (1024×1024) | 6 GB | 8 GB | 最常用的分辨率 |
| Flux Dev (1024×1024) | 12 GB | 16 GB | 需要显存较大 |
| Flux Pro / Wan2.1 视频 | 16 GB | 24 GB | 建议 24GB+ |
| 高清放大 + ControlNet | 8 GB | 12 GB | 组合使用时 |

### 操作系统

- **Windows**：NVIDIA GPU 支持最佳；AMD/Intel 也可用但性能较低
- **Linux**：NVIDIA（CUDA）、AMD（ROCm）均支持；服务器首选
- **macOS**：Apple Silicon（M1+）支持 MPS 加速，推荐 16GB+ 统一内存
- **Intel Mac**：不支持 GPU 加速，只能 CPU 运行（极慢）

### 其他依赖

- **Python**：3.10 - 3.13（推荐 3.12）
- **PyTorch**：CUDA 12.x / ROCm 7.x / MPS
- **磁盘空间**：基础安装约 2GB，一套常用模型约 30-80GB，专业配置可达 150GB+

## 2.2 安装方式概览

有 6 种安装方式，从最简单到最灵活：

```
难度排序：Desktop < 整合包 < Portable < comfy-cli < 手动 < Cloud
控制力：  Cloud < Desktop < 整合包 < Portable < comfy-cli = 手动
```

### 方式一：ComfyUI Desktop（推荐新手）

**适用**：Windows + NVIDIA / macOS Apple Silicon  
**难度**：⭐⭐（简单）

1. 访问 [https://www.comfy.org/download](https://www.comfy.org/download) 
2. 下载对应系统的安装包
3. 安装后打开，内置模型管理器、节点管理器

> ⚠️ 目前 Beta 阶段，Linux 暂不支持。

### 方式二：秋叶整合包（中文社区首选）

**适用**：Windows + NVIDIA  
**难度**：⭐（最简单）

秋叶（秋葉aaaki）制作的整合包是中文用户最流行的 ComfyUI 分发包：

1. 访问 [B站秋葉aaaki 主页](https://space.bilibili.com/12566101) 或百度网盘链接
2. 下载整合包（含 ComfyUI + 常用节点 + 基础模型）
3. 解压，双击 `A绘师启动器.exe`
4. 在启动器中点击「一键启动」

> ✅ 优点：自带 Python 环境、常用节点、一键更新  
> ⚠️ 注意：版本可能滞后官方 1-2 周

### 方式三：Portable 版（Windows）

**适用**：Windows + NVIDIA/AMD/Intel/CPU  
**难度**：⭐⭐

1. 访问 [GitHub Releases](https://github.com/comfyanonymous/ComfyUI/releases)
2. 下载 `ComfyUI_windows_portable_nvidia.7z`（或对应 GPU 版本）
3. 解压到目标目录（如 `D:\ComfyUI`）
4. 将模型文件放入 `ComfyUI\models\checkpoints\`
5. 运行 `run_nvidia_gpu.bat`（NVIDIA）或对应批处理文件

更新：运行 `update\update_comfyui_stable.bat`

### 方式四：comfy-cli（全平台推荐）

**适用**：所有平台，尤其是服务器/Headless 环境  
**难度**：⭐⭐⭐

```bash
# 1. 安装 comfy-cli
pip install comfy-cli

# 2. 关闭数据收集（可选但推荐）
comfy --skip-prompt tracking disable

# 3. 安装 ComfyUI（根据 GPU 选择）
comfy --skip-prompt install --nvidia    # NVIDIA CUDA
comfy --skip-prompt install --amd       # AMD ROCm
comfy --skip-prompt install --m-series  # Apple Silicon MPS
comfy --skip-prompt install --cpu       # CPU only

# 4. 启动
comfy launch --background               # 后台守护，默认端口 8188

# 5. 验证
curl http://127.0.0.1:8188/system_stats
```

**自定义端口和监听地址**：
```bash
comfy launch -- --listen 0.0.0.0 --port 8190
```

**指定工作目录**：
```bash
comfy --workspace /data/comfy install
comfy --workspace /data/comfy launch
```

### 方式五：手动 Git 安装（高级）

**适用**：需要完全控制、或使用非标准硬件  
**难度**：⭐⭐⭐⭐

```bash
# 1. 克隆仓库
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 2. 安装 PyTorch（选择对应 GPU 版本）
# NVIDIA CUDA 12.x:
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124

# AMD ROCm:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2

# Apple Silicon:
pip install torch torchvision torchaudio

# 3. 安装其他依赖
pip install -r requirements.txt

# 4. 启动
python main.py

# 带优化参数启动：
python main.py --lowvram --preview-method auto --use-flash-attention
```

### 方式六：Comfy Cloud（无需本地 GPU）

**适用**：没有 GPU、或不想折腾安装的用户  
**难度**：⭐

1. 访问 [https://www.comfy.org/cloud](https://www.comfy.org/cloud) 注册
2. 每月 400 免费积分（可运行少量工作流）
3. 付费套餐：Standard / Creator / Pro，并行任务数 1/3/5
4. 可通过网页端操作，也可通过 API 调用

> ⚠️ 免费套餐只能浏览模型，不能通过 API 运行工作流。

## 2.3 安装后配置

### 下载模型

```bash
# SDXL 基础模型（通用，~6.5 GB）
comfy model download \
  --url "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \
  --relative-path models/checkpoints

# Flux Dev fp8（较轻量的 Flux，~12 GB）
comfy model download \
  --url "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors" \
  --relative-path models/checkpoints

# SD 1.5（更轻量，~4 GB，6GB 显卡可用）
comfy model download \
  --url "https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" \
  --relative-path models/checkpoints
```

### 安装常用自定义节点

```bash
comfy node install comfyui-impact-pack         # 实用工具包
comfy node install comfyui-animatediff-evolved # 视频生成
comfy node install comfyui-controlnet-aux      # ControlNet 预处理器
comfy node install comfyui-essentials          # 常用辅助节点
comfy node install comfyui-manager             # 节点管理器（必装）
comfy node update all                          # 更新所有节点
```

### 使用 ComfyUI-Manager（推荐）

Manager 是 ComfyUI 的"应用商店"——直接在 WebUI 内搜索、安装、更新节点：

1. 安装：`comfy node install comfyui-manager`
2. 重启 ComfyUI
3. 在界面中点击 "Manager" 按钮
4. 浏览 "Install Custom Nodes" 目录

### 共享模型路径（多安装共存）

编辑 `extra_model_paths.yaml`（在 ComfyUI 根目录），可让 ComfyUI 读取其他目录中的模型：

```yaml
# 共享 A1111 的模型目录
a111:
  base_path: /path/to/stable-diffusion-webui/
  checkpoints: models/Stable-diffusion/
  loras: models/Lora/
  vae: models/VAE/
  controlnet: models/ControlNet/
```

## 2.4 验证安装

```bash
# 方式一：通过 system_stats 接口
curl http://127.0.0.1:8188/system_stats
# 应返回 JSON，包含设备信息、PyTorch 版本等

# 方式二：查看已安装模型
comfy model list

# 方式三：浏览器打开
# http://127.0.0.1:8188
# 看到 ComfyUI 界面（黑色画布 + 左侧节点面板）即为成功
```

## 2.5 更新 ComfyUI

```bash
# comfy-cli 方式
comfy update

# 手动安装方式
cd ComfyUI
git pull
pip install -r requirements.txt

# Portable 版
运行 update/update_comfyui_stable.bat

# Desktop 版
内置自动更新
```

> ⚠️ 更新后如果出现红色节点（missing nodes），说明自定义节点也需要更新：`comfy node update all`

---

# 第三章：界面与基础操作

## 3.1 界面总览

ComfyUI 的界面设计以 **极简高效** 为原则：

```
┌──────────────────────────────────────────────────────────┐
│  [菜单栏] Workflow  Edit  View  Queue  Manager  Settings │
├────────────┬─────────────────────────────────────────────┤
│ 左侧面板   │                                             │
│ ┌────────┐ │             画布 (Canvas)                   │
│ │ 搜索节点│ │                                             │
│ │  Add Node│ │   [Load Checkpoint] ───→ [CLIP Text]      │
│ │─────────│ │         │                      │           │
│ │ 最近使用 │ │         ▼                      ▼           │
│ │ 收藏节点 │ │   [Model] + [Conditioning]                │
│ │ 全部节点 │ │         │                      │           │
│ │─────────│ │         └──────┬───────────────┘           │
│ │ 队列状态 │ │                ▼                           │
│ │ 已生成   │ │            [KSampler]                      │
│ └────────┘ │                │                            │
│            │                ▼                            │
│            │          [VAE Decode]                       │
│            │                │                            │
│            │                ▼                            │
│            │          [Save Image]                       │
│            │                                             │
├────────────┴─────────────────────────────────────────────┤
│  [底部工具栏]  Queue Prompt  Extra Options  Node Count  │
└──────────────────────────────────────────────────────────┘
```

### 核心区域

| 区域 | 功能 |
|------|------|
| **画布（Canvas）** | 拖放节点、连接线路的主要工作区 |
| **左侧面板** | 节点浏览/搜索、最近使用、全部节点分类、队列信息 |
| **菜单栏** | Workflow（新建/加载/保存）、Edit（撤销/重做）、View（缩放/布局）、Queue（队列管理）、Manager（节点管理器）、Settings（设置） |
| **底部工具栏** | 排队生成按钮、额外选项（批次数量、种子控制等） |

## 3.2 节点操作基础

### 添加节点

四种方式：
1. **右键点击画布** → 弹出搜索框 → 输入节点名搜索
2. **双击画布** → 快速搜索
3. **左侧面板** → 浏览分类 → 拖拽到画布
4. **搜索栏**（顶部）→ 输入节点名

### 连接节点

- 从输出端口（右侧的圆点）**拖拽连线**到输入端口（左侧的圆点）
- 端口颜色代表数据类型（见下文）
- 无法连接不兼容的数据类型

### 数据类型颜色编码

| 颜色 | 数据类型 | 说明 |
|------|----------|------|
| 🟣 淡紫 | `MODEL` | 模型（checkpoint/UNet） |
| 🟡 黄色 | `CLIP` | 文本编码器 |
| 🌸 粉色 | `VAE` | VAE 模型 |
| 🟠 橙色 | `CONDITIONING` | 条件（prompt 编码结果） |
| 🩷 粉红 | `LATENT` | 潜空间张量 |
| 🔵 蓝色 | `IMAGE` | 图像张量 |
| 🟢 绿色 | `MASK` | 遮罩（黑白） |
| ⚪ 灰色 | `INT/STRING/FLOAT` | 基本数据类型 |

### 节点状态指示

| 状态 | 显示 | 含义 |
|------|------|------|
| **正常** | 默认 | 节点就绪 |
| **运行中** | 高亮/动画 | 正在执行 |
| **红色** | 红色边框 | 出错（节点报错） |
| **黄色** | 黄色边框 | 缺少输入或类型不匹配 |
| **绕过** | 灰化 + 虚线连线 | Bypass，该节点被临时禁用 |
| **静音** | 灰化 + 关闭图标 | Mute，和 Bypass 效果类似 |

### 节点操作快捷键

| 操作 | 方式 |
|------|------|
| 选择单个节点 | 点击 |
| 选择多个节点 | 框选（拖拽矩形）+ Ctrl+点击 |
| 移动节点 | 拖拽 |
| 删除节点 | 选中 → Delete / Backspace |
| 复制节点 | Ctrl+C / Ctrl+V |
| 绕过节点 | 选中 → Ctrl+B（保留输入输出直通） |
| 静音节点 | 右键 → Mute |
| 折叠/展开节点 | 双击节点标题栏（折叠后只显示输入输出） |
| 替换节点 | 右键 → Convert → 选择替换类型 |
| 注释 | 选中 → 右键 → Add Note / Ctrl+Shift+N |

## 3.3 队列与生成

### 排队机制

- 点击 **Queue Prompt**（排队生成）按钮或按 **Ctrl+Enter**
- 当前工作流被序列化并加入执行队列
- 可以设置 **batch count**（批次数量）一次性生成多张

### 种子控制

- **seed**: 随机种子，相同种子 + 相同参数 → 相同结果
- **control_after_generate**: 
  - `fixed`（固定）— 保留上次种子
  - `increment`（递增）— 每次 +1
  - `decrement`（递减）— 每次 -1
  - `randomize`（随机）— 每次都不同（默认）

### 图像查看

- 生成的图像显示在右侧的 **PreviewImage** 节点中
- 点击图像可放大查看
- 右键图像可保存到本地
- 图像元数据中嵌入了完整的 workflow JSON

## 3.4 工作流管理

### 保存工作流

- **Workflow → Save**（或 Ctrl+S）：保存为 `.json` 格式文件
- ⚠️ 默认**没有自动保存**！请在 Settings 中设置自动保存间隔（推荐 2-5 分钟）
- 生成的图像会自动嵌入 workflow JSON，拖入图像即可恢复

### 加载工作流

- **Workflow → Load**：选择 `.json` 文件
- **拖拽** `.json` 文件或图像到画布
- 从图像加载：会提示 "Load workflow from image?" → 确认

### 工作流格式

ComfyUI 有两种工作流格式：
- **Editor Format**：`nodes`（节点列表）+ `links`（连线列表），用于 UI 编辑
- **API Format**：每个节点是 `class_type` + `inputs`，用于通过 API 提交

### 工作流模板

ComfyUI 内置了多种工作流模板（Templates）：
- 文生图基础
- 图生图
- 局部重绘
- ControlNet 应用
- 视频生成 (Wan2.1, Hunyuan)

通过菜单栏 **Workflow → Templates** 或底部左侧面板访问。

## 3.5 高级界面特性

### 子图（Subgraph）

选中一组节点 → 右键 → **Convert to Subgraph** → 将多个节点折叠为一个可复用的子图（类似编程中的函数封装）。双击子图可展开编辑。

### App Mode

将工作流转换为一个简洁的单页应用——隐藏所有内部节点，只暴露可控参数（prompt、seed 等），生成分享链接。

**路径**：菜单 View → App Mode 或 Settings 中启用

### 设置面板

| 设置项 | 说明 |
|--------|------|
| Locale（语言）| 支持中文界面（部分翻译）|
| Menu Style | 经典 / 新版菜单 |
| Auto Save | 自动保存间隔（分钟），默认关闭 |
| Deprecated Nodes | 是否显示已弃用节点 |
| Node Suggestion Count | 搜索节点时的建议数量 |
| Selection Toolbox | 节点选择工具栏样式 |

---

# 第四章：工作流构建（基础）

## 4.1 文生图（Text-to-Image）— 最基础的工作流

这是 ComfyUI 的 "Hello World"，理解了这个就理解了核心原理：

### 节点结构

```
[Load Checkpoint] ──MODEL──→ [KSampler] ──LATENT──→ [VAE Decode] ──IMAGE──→ [Save Image]
       │                        ↑
       ├──CLIP──→ [CLIP Text Encode (正面prompt)] ──CONDITIONING──┘
       │              ↑
       │         (文本输入: "a cat")
       │
       └──CLIP──→ [CLIP Text Encode (负面prompt)] ──CONDITIONING──┘
                         ↑
                    (文本输入: "blurry, ugly")
```

### 分步详解

**步骤 1：加载检查点（Load Checkpoint）**

- 找到并加载一个基础模型文件（`.safetensors` 或 `.ckpt`）
- 输出三路：`MODEL`（生成模型）、`CLIP`（文本编码器）、`VAE`（图像编解码器）
- 这是每个工作流的起点

**步骤 2：编写提示词（CLIP Text Encode）**

- 正面 prompt（positive）：描述你想要的内容
- 负面 prompt（negative）：描述你不要的内容
- CLIP 将文本编码为模型能理解的 conditioning（条件）

**步骤 3：KSampler（核心采样）**

接收 `MODEL` + 正面 `CONDITIONING` + 负面 `CONDITIONING`，输出 `LATENT`

关键参数（后面有详解）：
- `seed`（种子）：随机数种子
- `steps`（步数）：采样步数，推荐 20-30
- `cfg`（CFG Scale）：引导强度，推荐 7-8
- `sampler_name`（采样器名）：如 `euler`, `dpmpp_2m`, `uni_pc`
- `scheduler`（调度器）：如 `normal`, `karras`, `exponential`
- `denoise`（去噪强度）：文生图中固定为 1.0

**步骤 4：VAE Decode（解码）**

将 `LATENT`（潜空间张量）解码为肉眼可见的 `IMAGE`（像素图像）

**步骤 5：Save Image（保存）**

将图像保存到 `ComfyUI/output/` 目录

### 动手构建

1. 右键画布 → 搜索并添加以下节点：
   - `CheckpointLoaderSimple`（或 `Load Checkpoint`）
   - `CLIPTextEncode` × 2
   - `KSampler`
   - `VAEDecode`
   - `SaveImage`（或 `PreviewImage`）
2. 按上文示意图连接
3. 在正面 CLIPTextEncode 中输入 prompt，如 `"a beautiful mountain landscape, photorealistic, 8k"`（美丽的山景，照片级逼真，8k）
4. 在负面 CLIPTextEncode 中输入：`"blurry, low quality, distorted, ugly"`（模糊、低质量、扭曲、丑陋）
5. 点击 **Queue Prompt** 或按 **Ctrl+Enter**
6. 等待几秒，图像生成！

## 4.2 图生图（Image-to-Image）

以一张现有图像为基础进行修改：

```
[Load Image] ──IMAGE──→ [VAE Encode] ──LATENT──→ [KSampler] ──LATENT──→ [VAE Decode] ──IMAGE──→ [Save Image]
                                                    ↑
[Load Checkpoint] ──MODEL───────────────────────────┘
       │
       └──CLIP──→ [CLIP Text Encode] ──CONDITIONING──┘
```

与文生图的区别：
- 多了 `Load Image`（加载图像）+ `VAE Encode`（编码到潜空间）
- KSampler 的 `denoise`（去噪强度）参数控制修改幅度：
  - `0.3`：微小改动（颜色、光照微调）
  - `0.5`：中等改动（改变风格、添加细节）
  - `0.7`：大幅改动（近乎重绘）

## 4.3 局部重绘（Inpainting）

只修改图像的特定区域：

```
[Load Image] ──IMAGE──→ [VAE Encode] ──LATENT──→ [KSampler] ──LATENT──→ [VAE Decode] ──IMAGE──→ [Save Image]
                                                     ↑
[Load Mask] ──MASK────→ [Set Latent Noise Mask] ────┘
[Load Checkpoint] ──MODEL────────────────────────────┘
```

- `Load Mask`：加载黑白遮罩图（白色→重绘区域，黑色→保留区域）
- `Set Latent Noise Mask`：告诉 KSampler 哪些区域需要重新生成
- 也可以用 ComfyUI 内置的 **Mask Editor** 直接在界面上绘制遮罩

## 4.4 工作流参数详解

### Steps（步数）

采样步数 = 去噪过程中的迭代次数。更多步数 ≈ 更精细 → 收敛至足够即可。

| 模型 | 推荐步数 | 说明 |
|------|---------|------|
| SD 1.5 | 20-30 | 20 步通常足够 |
| SDXL | 20-30 | 25 步平衡质量和速度 |
| Flux Dev | 20-30 | Flux 对步数不敏感，20 步即可 |
| Flux Pro | 30-50 | 更多步数提升细节 |
| LCM / Turbo | 1-4 | 极速模型，几步即可 |

### CFG（Classifier-Free Guidance，无分类器引导尺度）

控制生成图像对 prompt 的遵从程度。

| 值 | 效果 | 适用 |
|----|------|------|
| 1-3 | 弱引导 | 自由发挥，接近"无 prompt 生成" |
| 4-6 | 中等 | 创意性任务 |
| 7-8 | 标准（推荐）| SD 1.5 / SDXL 的平衡点 |
| 9-12 | 强引导 | 需要精确控制 prompt |
| 12+ | 过强 | 可能导致色彩饱和、伪影 |

> **⚠️ Flux 特殊**：Flux 使用 1.0-1.5 的 CFG 值！用 7-8 会得到完全损坏的输出。

### Seed（种子）

- **相同 seed + 相同参数 = 完全相同的结果**（可复现性）
- **-1 或 randomize**：每次随机
- 找好构图后固定 seed，微调其他参数

### Sampler（采样器）

| 采样器 | 速度 | 质量 | 推荐场景 |
|--------|------|------|----------|
| `euler` | 快 | 良好 | 快速预览 |
| `euler_ancestral` | 快 | 良好 | 更丰富的变化 |
| `dpmpp_2m` | 中等 | 优秀 | **日常推荐** |
| `dpmpp_2m_sde` | 慢 | 优秀 | 高质量，更长生成时间 |
| `dpmpp_3m_sde` | 慢 | 优秀 | 最高质量 |
| `uni_pc` | 快 | 良好 | 快速批量 |
| `lcm` | 极快 | 一般 | 几步出图（配合 LCM LoRA）|

### Scheduler（调度器）

| 调度器 | 效果 |
|--------|------|
| `normal` | 标准，通用 |
| `karras` | 在接近结束时分配更多步数，更锐利的细节 |
| `exponential` | 指数衰减，适合特定模型 |
| `sgm_uniform` | SDXL 推荐 |
| `simple` | 简单线性 |

> **经验组合**：`dpmpp_2m + karras` 是社区最常用的组合。

### Denoise（去噪强度）

仅用于图生图/重绘：

| 值 | 修改程度 |
|----|----------|
| 0.0 | 无变化 |
| 0.3-0.4 | 微调（颜色、光照、纹理） |
| 0.5-0.6 | 中等改动（保留构图，改变风格） |
| 0.7-0.8 | 大幅改动（保留模糊轮廓） |
| 0.9-1.0 | 几乎完全重绘 |

## 4.5 LoRA 的使用

LoRA（Low-Rank Adaptation，低秩适配）是一种轻量级的模型微调方法：

```
            ┌──────────────────────────────────────────┐
[Load Checkpoint] ──MODEL──→ [Load LoRA] ──MODEL──→ [KSampler]
       │                     model: 0.8
       ├──CLIP──→ [Load LoRA] ──CLIP──→ [CLIP Text Encode]
       │            clip: 0.8
       └──VAE─────────────────────────────────────────┘
```

- `Load LoRA` 节点接收 MODEL 和 CLIP，应用 LoRA 权重后输出调整后的 MODEL 和 CLIP
- `model_strength`（模型权重）：LoRA 对模型的影响强度
- `clip_strength`（CLIP 权重）：LoRA 对文本编码的影响强度
- 最常用的值：0.6-1.0，太大会过拟合导致图像扭曲

## 4.6 高清放大（Upscaling）

使用专门的放大模型（如 4x-UltraSharp）提升分辨率：

```
[原始图像] ──IMAGE──→ [Upscale Image (Model)] ──放大后图像──→ [Save Image]
                            │
                    [加载放大模型]
```

- `UpscaleImage`（使用算法）：速度快，用 LatentUpscale + 算法
- `Upscale Image (Model)`（使用模型）：质量高，需加载专门的放大模型

**推荐放大流程**：
1. 生成为较低分辨率（如 SDXL 的 1024×1024）
2. 使用 2× 放大模型放大
3. 可选择再做一次 2× 放大（总计 4×）

---

# 第五章：核心节点详解（中文翻译）

## 5.1 加载器（Loader）节点

### CheckpointLoaderSimple（简单检查点加载器）

**功能**：加载基础模型文件

| 参数 | 类型 | 说明 |
|------|------|------|
| `ckpt_name` | STRING | 检查点文件名（从 `models/checkpoints/` 中选择） |

**输出**：
- `MODEL`（模型）→ 连接 KSampler 等采样节点
- `CLIP`（文本编码器）→ 连接 CLIPTextEncode
- `VAE`（变分自编码器）→ 连接 VAEDecode

> 💡 如果你只需要单独加载模型的某一部分，可以使用：
> - `UNETLoader`：只加载 UNet 部分
> - `CLIPLoader`：只加载 CLIP 文本编码器
> - `VAELoader`：只加载 VAE

### Load LoRA（加载 LoRA）

**功能**：加载并应用 LoRA 模型

| 参数 | 说明 |
|------|------|
| `model` (MODEL) | 要应用 LoRA 的基础模型 |
| `clip` (CLIP) | 要应用 LoRA 的 CLIP |
| `lora_name` | LoRA 文件名（从 `models/loras/` 选择） |
| `strength_model` | 对模型的强度（0.0-1.0+） |
| `strength_clip` | 对 CLIP 的强度（0.0-1.0+） |

> 💡 多个 LoRA 可以串联使用，但总强度不宜超过 1.5-2.0

### Load ControlNet Model（加载 ControlNet）

**功能**：加载 ControlNet 模型

| 参数 | 说明 |
|------|------|
| `control_net_name` | ControlNet 文件名（从 `models/controlnet/` 选择） |

**输出**：`CONTROL_NET` → 连接 ControlNetApply 节点

### Load Image（加载图像）

**功能**：从本地或输入目录加载图像

| 参数 | 说明 |
|------|------|
| `image` | 图像路径（从 `input/` 目录选择） |

**输出**：`IMAGE`（张量形式）

## 5.2 条件（Conditioning）节点

### CLIPTextEncode（CLIP 文本编码）

**功能**：将文本 prompt 编码为模型可理解的 conditioning

| 参数 | 说明 |
|------|------|
| `text` | 输入文本 prompt |
| `clip` (CLIP) | 来自 CheckpointLoader 或 LoRA 的 CLIP |

**输出**：`CONDITIONING` → 连接 KSampler 的 positive/negative

> 💡 提示词技巧（prompt engineering）：
> - 正面 prompt + 负面 prompt 同等重要
> - 常见负面词：`blurry, low quality, distorted, ugly, bad anatomy, extra limbs, mutated hands`
> - 可使用 "embedding" 文件作为负面增强

### CLIPVisionEncode（CLIP 视觉编码）

**功能**：将图像编码为 conditioning，用于 IP-Adapter 等场景

| 参数 | 说明 |
|------|------|
| `clip_vision` (CLIP_VISION) | CLIP 视觉模型 |
| `image` (IMAGE) | 输入图像 |

### ControlNetApply（应用 ControlNet）

**功能**：将 ControlNet 条件应用到 conditioning 中

| 参数 | 说明 |
|------|------|
| `conditioning` (CONDITIONING) | 来自 CLIPTextEncode 的条件 |
| `control_net` (CONTROL_NET) | 来自 Load ControlNet Model |
| `image` (IMAGE) | ControlNet 的引导图像（如深度图、边缘图）|
| `strength` (FLOAT) | 控制强度 0.0-1.0，1.0=完全遵从 |
| `start_percent` (FLOAT) | 起效百分比（0.0-1.0） |
| `end_percent` (FLOAT) | 结束百分比（0.0-1.0） |

> 💡 通过 `start_percent` 和 `end_percent` 可以控制 ControlNet 在采样的哪个阶段起作用。例如 `start: 0.0, end: 0.5` 表示只在采样前半段应用 ControlNet。

## 5.3 采样（Sampling）节点

### KSampler（K 采样器）

ComfyUI 中最核心、最常用的节点。

**输入**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | MODEL | 生成模型 |
| `seed` | INT | 随机种子（-1=随机） |
| `control_after_generate` | STRING | 生成后种子策略 |
| `steps` | INT | 采样步数（推荐 20-30） |
| `cfg` | FLOAT | CFG 引导尺度（推荐 7-8） |
| `sampler_name` | STRING | 采样器算法 |
| `scheduler` | STRING | 调度器策略 |
| `positive` | CONDITIONING | 正面条件 |
| `negative` | CONDITIONING | 负面条件 |
| `latent_image` | LATENT | 潜空间图像（文生图时为空潜空间）|
| `denoise` | FLOAT | 去噪强度（文生图=1.0） |

**输出**：`LATENT` → 连接 VAEDecode

### KSamplerAdvanced（高级采样器）

拥有比 KSampler 更多的控制参数：
- `add_noise`：控制是否添加噪声到潜空间
- `noise_seed`：噪声的种子（与生成种子分离）
- `start_at_step` / `end_at_step`：精细控制采样起止步骤

### SamplerCustom（自定义采样器）

将采样过程拆解为更细粒度的组件，适合高级用户构建自定义采样管线。

## 5.4 图像操作节点

### SaveImage（保存图像）

**功能**：将图像保存到 `ComfyUI/output/` 目录

| 参数 | 说明 |
|------|------|
| `images` (IMAGE) | 要保存的图像 |

### PreviewImage（预览图像）

与 SaveImage 类似，但不保存文件，仅在界面中显示

### ImageResize / ImageScale（图像缩放）

- **ImageResize**：指定目标尺寸（宽×高）
- **ImageScale**：指定缩放倍数
- 支持多种缩放算法：`nearest-exact`, `bilinear`, `bicubic`, `lanczos`, `area`

### ImageBlend（图像混合）

将两张图像按透明比例混合：
- `blend_percentage`：前景透明度（0-100%）

## 5.5 潜空间操作节点

### VAEEncode（VAE 编码）

**功能**：将像素图像编码为潜空间表示

| 参数 | 说明 |
|------|------|
| `pixels` (IMAGE) | 像素图像 |
| `vae` (VAE) | VAE 模型 |

### VAEDecode（VAE 解码）

**功能**：将潜空间表示解码为像素图像（生成的最后一步）

| 参数 | 说明 |
|------|------|
| `samples` (LATENT) | 潜空间数据 |
| `vae` (VAE) | VAE 模型 |

# 第六章：进阶技术详解

## 6.1 ControlNet — 精确控制生成

ControlNet 是 ComfyUI 最重要的进阶技术之一，它通过额外条件（姿势、深度、边缘等）精确控制生成图像的构图和布局。

### 工作原理

```
[加载引导图像] ──→ [ControlNet 预处理器] ──→ [ControlNet 模型] ──→ [ControlNetApply]
                                                                         │
[CLIP Text Encode] ──CONDITIONING─────────────────────────────────────────┘
                                                                         │
                                                                    [修改后的 CONDITIONING]
```

### 常用 ControlNet 类型

| 类型 | 预处理器 | 效果 | 适用场景 |
|------|----------|------|----------|
| **Canny（边缘检测）** | `canny` | 提取线条边缘 | 保持构图结构 |
| **Depth（深度图）** | `depth_anything` / `miidas` | 提取景深信息 | 保持空间布局 |
| **OpenPose（姿态）** | `openpose` | 提取人物骨架 | 控制人物姿势 |
| **Scribble（涂鸦）** | `scribble` | 从手绘线稿生成 | 创意草图转图像 |
| **Lineart（线稿）** | `lineart` | 精确线条 | 动漫/漫画上色 |
| **SoftEdge（软边缘）** | `softedge` | 柔和边缘 | 自然风格控制 |
| **Tile（平铺）** | `tile` | 分块处理 | 高清放大 + 细节添加 |
| **IP-Adapter** | — | 图像风格迁移 | 以图生图的 prompt 替代方案 |

### 混合多个 ControlNet

```
[图像A] → [预处理器A] → [ControlNet A] → [ControlNetApply A] → 合并条件
                                                                    │
[图像B] → [预处理器B] → [ControlNet B] → [ControlNetApply B] ──────┘
                                                                    │
[CLIP Text Encode] ──────────────────────────────────────────────────┘
```

通过 `start_percent` / `end_percent` 控制每个 ControlNet 的作用阶段，可以实现更精细的控制。

## 6.2 IP-Adapter — 图像提示适配器

IP-Adapter 允许用"图像"作为 prompt，而非文字。它可以提取参考图像的风格、构图或角色特征：

```
[参考图像] → [CLIPVisionLoader] → [CLIPVisionEncode] → [IPAdapterApply] → 合并条件
                                                                              │
[CLIP Text Encode] ───────────────────────────────────────────────────────────┘
```

- **style transfer**（风格迁移）：提取参考图像的风格
- **composition**（构图参考）：提取构图布局

## 6.3 LoRA 进阶技巧

### 单工作流中使用多个 LoRA

```
[Checkpoint] → [Load LoRA A (strength: 0.8)] → [Load LoRA B (strength: 0.6)] → [KSampler]
```

- 多个 LoRA 的效果会叠加
- 推荐总强度不超过 1.5-2.0
- 顺序重要：先加载概念 LoRA，再加载风格 LoRA

### LyCORIS

LyCORIS 是 LoRA 的变体，提供更灵活的权重分解方式（LoRA, LoKr, LoHa, Diag-OFT 等），在保持模型容量的同时提供更好的效果。

## 6.4 视频生成（Wan2.1 / Hunyuan Video）

### Wan2.1 文生视频

```
[WanVideoTextToVideo] ──→ [VAEDecode (3D VAE)] ──→ [VideoCombine] ──→ 保存视频
```

- 支持 T2V（文生视频）、I2V（图生视频）
- 输出为视频文件（MP4）
- 需要 16GB+ VRAM

### Hunyuan Video

腾讯开源的视频生成模型，支持文生视频和图生视频。

## 6.5 3D 生成

ComfyUI 支持多种 3D 生成管线：

- **Hunyuan3D 2.0**：文本/图像 → 3D 模型
- **Tripo**：快速 3D 生成
- **Meshy**：AI 3D 内容平台集成

## 6.6 音频生成

- **Stable Audio**：文本 → 音乐/音效
- **ElevenLabs TTS**：文本 → 语音
- **ACE Step**：音频生成和处理

---

# 第七章：社区教程精选

## 7.1 B站顶级教程

### 排名 #1：Nenly同学 — ComfyUI 入门教程

- **播放量**：172.3 万
- **UP主**：Nenly同学（70.3 万关注）
- **链接**：[BV1D7421N7xN](https://www.bilibili.com/video/BV1D7421N7xN/)
- **系列**：共 11 课，约 3 小时
- **内容**：从"为什么 ComfyUI 是必须掌握的工具"讲起，覆盖：
  - 安装配置、界面操作、节点搭建
  - 自定义节点管理
  - 高清修复、ControlNet、LoRA
- **评价**：全网最知名的 AI 科普 UP 主，讲解通俗易懂，最适合零基础转 ComfyUI 的新手

### 排名 #2：ComfyUI UP主 — 2025最全面教程

- **播放量**：137.1 万
- **UP主**：comfyui（17.6 万关注）
- **链接**：[BV1ahJtzeEB1](https://www.bilibili.com/video/BV1ahJtzeEB1/)
- **系列**：22 节课，约 6 小时
- **四大模块**：
  1. 零基础入门（界面导览、文生图/图生图、ControlNet、IP-Adapter、老照片修复）
  2. FLUX 进阶（本地部署、去 AI 感、三视图、批量生成）
  3. LoRA 训练（从原理到实践）
  4. SD 设计篇（艺术字等）
- **特点**：含 FLUX 四大模型详解，当前最全面的 FLUX+ComfyUI 中文教程

### 其他推荐

| 标题 | UP主 | 播放量 | 链接 |
|------|------|--------|------|
| Comfyui工作流从零基础到精通（2026版） | comfyui工作流 | 35.4万 | [BV1dr3XzsEqP](https://www.bilibili.com/video/BV1dr3XzsEqP/) |
| 【秋叶最新Comfyui教程】2025B站最细保姆级教程（32集） | AI漫剧-- | 1.2万+ | [BV1RkXVYKEGL](https://www.bilibili.com/video/BV1RkXVYKEGL/) |

## 7.2 知乎高赞文章

| 标题 | 作者 | 说明 |
|------|------|------|
| **万字教程！奶奶看了都会的ComfyUI 入门教程** | 言川Artie | 知乎最知名的文字入门教程 |
| **万字教程丨从零开始：构建你的首个ComfyUI工作流** | — | 系统化入门 |
| **深入浅出完整解析主流AI绘画框架（ComfyUI/SD WebUI/Fooocus对比）** | Rocky | 深度对比分析 |
| **ComfyUI 完全入门：基本功能** | — | 系列教程 |

## 7.3 YouTube 英文教程（高推荐度）

| 频道 | 特点 |
|------|------|
| **Olivio Sarikas** | Reddit 社区最推荐的教程频道之一 |
| **Sebastian Kamph** | 大量 ComfyUI 入门教程，适合初学者 |
| **Latent Vision** | IP-Adapter 开发者，更深度的技术讲解 |
| **Nerdy Rodent** | 60+ 免费课程，适合从零开始 |
| **Max Novak** | "Ultimate Beginner Guide to Learning ComfyUI (2026)" — 登上 NVIDIA Studio 频道 |
| **Nico Erba** | VFX 工作室 Digital District 创新总监，专业 AI 工作流 |

## 7.4 系统化中文教程网站

| 网站 | 网址 | 特点 |
|------|------|------|
| **ComfyUI Wiki 中文百科** | https://comfyui-wiki.com/zh | 最系统化的中文文档，持续更新 |
| **Comflowy 中文版** | https://www.comflowy.com/zh-CN/basics | 手把手交互式教程，适合系统学习 |
| **飞书文档｜AI艺术家系列** | 微信公众号 | 微信生态的最佳资源，整理到飞书文档 |
| **WaytoAGI 知识库** | https://www.waytoagi.com | 社区驱动的 AI 学习平台 |

---

# 第八章：业内评价与案例分析

## 8.1 行业采纳情况

### NVIDIA 官方合作（2026年4月）

NVIDIA 在 GDC 2026 上宣布与 ComfyUI 深度合作：
- RTX 50 系列上实现 **2.5× 加速**，**60% VRAM 降低**
- 发布官方教程《How to Build, Run, and Scale High-Quality Creator Workflows in ComfyUI》
- 推荐配置：RTX GPU 24GB VRAM（Windows）/ 32GB（Linux）

> "ComfyUI provides the flexibility needed for architectural-scale generative workflows." — NVIDIA 官方博客

### VFX 行业

**ActionVFX**（2025年9月）：
> "行业内正在发生转变——不是用 AI 取代艺术家，而是用工具让他们的工作更快、更干净、更有创意。"

推出首个 "Introduction to ComfyUI for VFX" 官方课程（15 模块），涵盖：
- 清理画面（clean plates）
- 智能遮罩（smart mattes）使用 ControlNet
- 通过深度图实现 relighting（重新照明）
- 通过 inpainting 实现 set extensions（场景扩展）
- 导出分层 EXR

### Moment Factory 案例研究

Moment Factory（知名多媒体工作室）使用 ComfyUI 完成建筑级投影映射项目（25 Broadway）：
- **效率提升**：概念工作从 "数天" 缩短到 "数小时"
- **产出**：探索 20+ 艺术方向，每个 20-40 次迭代
- **高清输出**：提升至 18K 分辨率，约 20 分钟完成
- **团队**：1 名主艺术家 + 2 名团队成员

> "Achieving reliable architectural-scale generative workflows required a system flexible enough to be re-authored alongside the creative process. ComfyUI provided that flexibility." — Moment Factory

### 行业地位

- **TechCrunch 报道**（2026年4月）：ComfyUI 完成 $3000 万融资，估值 $5 亿
- **职位出现**："ComfyUI artist or engineer" 已成为工作室招聘职位
- **LinkedIn 案例**：Netflix 游戏生产、VFX 管线中已使用 ComfyUI

## 8.2 专业对比评测

### ComfyUI vs Forge vs A1111（2026年3月，offlinecreator.com）

| 维度 | ComfyUI | Forge | A1111 |
|------|---------|-------|-------|
| 易用性 | 陡峭学习曲线 | 容易 | 容易 |
| 速度 | 最快（图优化） | 比 A1111 快 10-30% | 基准 |
| VRAM | 最低 | 较低 | 高 |
| Flux 支持 | ✅ 首批 | ✅ | 有限 |
| 视频生成 | ✅ Wan/Hunyuan | ❌ | ❌ |

**结论**："ComfyUI for power users wanting bleeding-edge models and custom pipelines. Forge for most people."

### 性能基准测试（propelrc.com，300+小时测试）

| 基准 | ComfyUI | A1111 | Fooocus |
|------|---------|-------|---------|
| SD 1.5 512×512 | **2.1s** | 2.4s | 2.3s |
| SDXL 1024×1024 | **7.8s** | 9.2s | 8.5s |
| Batch of 4 | **28s** | 35s | 32s |
| VRAM min (SDXL) | **6GB** | 8GB | 8GB |

## 8.3 创作者评价

### Chase Jarvis（知名摄影师/创作者）

> "2026 年最高效的工作流不是 MidJourney vs ComfyUI，而是 **MidJourney → ComfyUI**"

- **ComfyUI 角色**："技师（Technician）"— 执行精确指令，通过 ControlNet 提供像素级控制
- **优势**：绝对的控制力、模块化、免费、隐私
- **劣势**：陡峭学习曲线、输出可能"呆板"
- **推荐混合工作流**：结构（ComfyUI）→ 风格（MidJourney）→ 组装（ComfyUI）

### Sider.ai 评测（2025年9月）

> "Capable and transparent way to run Stable Diffusion. Best for power users who value control over convenience."

**突出优势**：节点图系统、SDXL/LoRA/ControlNet 一等公民支持、性能与稳定性、生态

### Angry Shark Studio — 常见错误总结

10 大新手错误（详见第 9 章避坑指南），包括：未加载 VAE、忘记保存工作流、Flux 使用错误 CFG 等。

## 8.4 X（Twitter）舆论

| 声音 | 内容 |
|------|------|
| @vast_ai | ComfyUI 比同类界面快 2-3 倍 |
| @stepahin | 花一个月学习 ComfyUI + face models，正向评价 |
| IK3D.fr | "ComfyUI Just Killed the Node Graph Learning Curve — App Mode Changes Everything" |

---

# 第九章：避坑指南（常见错误与解决方案）

## 9.1 安装问题

### 错误：ComfyUI 启动报错，缺失依赖

**现象**：运行 `python main.py` 后出现 `ModuleNotFoundError`

**解决**：确保已安装所有依赖
```bash
pip install -r requirements.txt
```

### 错误：CUDA out of memory

**现象**：`RuntimeError: CUDA out of memory`

**原因**：显存不足

**解决**：
1. 使用 `--lowvram` 启动：`python main.py --lowvram`
2. 使用 `--normalvram` 启动
3. 使用 `--reserve-vram 2` 保留 2GB 余量
4. 关闭其他 GPU 应用（Chrome、游戏等）
5. 使用 fp8 精度的模型
6. 降低生成分辨率
7. 单批次 1 张

### 错误：Windows 上 Portable 版闪退

**解决**：
1. 确认 GPU 驱动已更新
2. 运行 `run_cpu.bat` 测试是否能启动（如能，说明 GPU 问题）
3. 确认 CUDA 版本匹配

### 错误：macOS 上提示 "damaged" 无法打开

**解决**：系统偏好设置 → 安全性与隐私 → 仍然打开

## 9.2 工作流问题

### ⭐ 错误 #1：不加载或加载错误的 VAE

**现象**：图像发灰、偏紫/绿色

**原因**：VAE（变分自编码器）对最终图像渲染至关重要，错误/缺失的 VAE 会导致颜色异常

**解决**：确保工作流中正确加载并连接了 VAE 模型

### ⭐ 错误 #2：忘记保存工作流

**现象**：辛苦搭建的工作流在关闭后丢失

**原因**：ComfyUI 默认没有自动保存

**解决**：
1. 频繁按 **Ctrl+S**（或 Cmd+S）
2. 在 Settings 中开启 **Auto Save**，设置 2-5 分钟间隔
3. 生成的图像会自动嵌入工作流，下次拖入图像可恢复

### ⭐ 错误 #3：Flux 使用错误的 CFG 值

**现象**：输出完全损坏、色彩异常

**原因**：Flux 使用与 SD/SDXL **完全不同**的 CFG 范围

**解决**：Flux 使用 **CFG 1.0-1.5**！绝对不要用 7-8

### ⭐ 错误 #4：分辨率不匹配

**现象**：图像扭曲、出现重复模式、无法生成

**原因**：模型有训练时的原生分辨率，偏离太远会导致问题

**解决**：
| 模型 | 推荐分辨率 |
|------|-----------|
| SD 1.5 | 512×512（或接近的倍数，如 768×512）|
| SDXL | 1024×1024 |
| Flux | 1024×1024（可灵活变化）|
| Wan2.1 视频 | 遵循模型文档 |

### ⭐ 错误 #5：盲目复制工作流

**现象**：下载的工作流不工作、出现红色节点

**原因**：缺少模型、自定义节点或配置

**解决**：
1. 使用 Manager 的 "Install Missing Custom Nodes" 功能
2. 运行 `comfy node install-deps --workflow=workflow.json`
3. 查看工作流依赖的模型并下载

### 错误 #6：自定义节点出现红色（Missing nodes）

**现象**：节点显示红色，提示 "class_type not found"

**原因**：缺少对应的自定义节点

**解决**：
```bash
# 方式一：Manager 自动安装
点击 Manager → Install Missing Custom Nodes

# 方式二：手动安装
comfy node install 节点名

# 方式三：查看依赖
comfy node install-deps --workflow=workflow.json
```

### 错误 #7：步数过多或过少

- **步数太少**：图像不精细、噪声明显
- **步数太多**：浪费时间，质量不会持续提升
- **建议**：SD 1.5/SDXL 用 20-30 步，Flux 用 20 步

### 错误 #8：CFG 设置不当

- **CFG 太高**（>12）：色彩饱和、伪影、物体变形
- **CFG 太低**（<4）：生成内容与 prompt 关联弱
- **建议**：从 7 开始，上下微调

### 错误 #9：种子管理混乱

- 想要可复现的结果，一定要固定 seed
- 使用 `control_after_generate: fixed` 或手动记录 seed 值

### 错误 #10：忽略模型特定设置

不同模型有不同的推荐参数（sampler、scheduler、CFG），检查模型卡（CivitAI / HuggingFace）上的说明。

## 9.3 性能问题

### 生成速度慢

1. 使用 `--use-flash-attention` 启动（显著加速）
2. 使用 fp8/fp16 精度模型（减少显存占用和计算量）
3. 使用更快的采样器（如 `euler` 或 `uni_pc`）
4. 降低图像分辨率
5. 使用更少的步数
6. 更新 GPU 驱动

### 显存管理

```bash
# 启动参数（按保守度升序）
python main.py                           # 默认，大显存
python main.py --normalvram              # 适中
python main.py --lowvram                 # 保守（6-8GB 显卡）
python main.py --novram                  # 极限（共享显存/CPU）
```

## 9.4 更新问题

### 更新后节点变红

**原因**：ComfyUI 版本更新可能改变内部 API，旧节点不兼容

**解决**：
```bash
comfy node update all   # 更新所有自定义节点
```

如果仍然红色，去节点 GitHub 主页查看是否兼容最新版本的 ComfyUI。

### 工作流版本不兼容

下载的旧工作流可能使用已弃用的节点。Settings → 开启 "Show Deprecated Nodes" 查看是否有替换方案。

---

# 第十章：进阶技巧与最佳实践

## 10.1 工作流组织

### 命名规范

- 给工作流取有意义的文件名：`portrait_sdxl_photorealistic_v3.json`
- 在画布中使用 **Note Node（注释节点）** 标记关键步骤

### 使用 Group（群组）

选中相关节点 → 右键 → **Add Group**（或按 Ctrl+G）→ 将逻辑相关的节点打包，便于识别和管理。

### 使用 Reroute（路由节点）

当连线过长或混乱时：
- 右键画布 → Add Node → Utils → **Reroute**（路由节点）
- 插入连线中间，整理线路走向
- 保持画布整洁

### 子图封装

将可复用的节点组合封装为 **Subgraph（子图）**，像函数一样复用：
- 选中节点 → 右键 → Convert to Subgraph
- 子图可保存为独立的 `.json` 文件
- 可定义输入/输出接口

## 10.2 测试与调试

### 5 分钟规则

在使用别人的工作流之前，花 5 分钟理解：
1. **使用什么模型**（checkpoint, LoRA, ControlNet）
2. **使用了哪些自定义节点**
3. **数据的流动路径**（从输入到输出）
4. **关键参数设置**（steps, CFG, sampler）

### 逐步增加复杂性

1. 从一个基础工作流开始（文生图）
2. 一次添加一个新节点（如 ControlNet）
3. 测试通过后再加下一个
4. 这样可以精确知道每个组件的效果

## 10.3 模型管理

### 磁盘空间管理

- 一套常用模型：30-80GB
- 专业配置可达 150GB+
- 使用 `extra_model_paths.yaml` 在不同驱动器之间共享
- 清理不需要的模型文件

### 整理模型目录

```
ComfyUI/models/
├── checkpoints/          # 完整模型文件（SDXL, Flux, SD1.5...）
├── loras/                # LoRA 文件
├── vae/                  # VAE 文件
├── controlnet/           # ControlNet 文件
├── upscale_models/       # 放大模型
├── clip/                 # CLIP 模型
├── clip_vision/          # CLIP Vision 模型
├── embeddings/           # Embedding 文件
├── ipadapter/            # IP-Adapter 文件
├── animatediff_models/   # AnimateDiff 模型
└── ultralytics/          # YOLO / 检测模型
```

### 模型选择策略

| 任务 | 推荐模型 | 理由 |
|------|----------|------|
| 通用高质量 | SDXL | 质量好、速度快、生态成熟 |
| 最前沿质量 | Flux Dev | 细节最多、构图最佳，但需要 12GB+ VRAM |
| 轻度使用 | SD 1.5 | 轻量、速度快、6GB 显卡可用 |
| 角色一致性 | SD 1.5 + LoRA | LoRA 生态最丰富 |
| 视频 | Wan2.1 / Hunyuan Video | 开源视频生成的首选 |

## 10.4 资源推荐

### 模型下载

| 平台 | 网址 | 特点 |
|------|------|------|
| **CivitAI** | https://civitai.com | 最大的模型社区，含预览图 |
| **HuggingFace** | https://huggingface.co | 最全的开源模型仓库 |

### 工作流下载

- **CivitAI**：模型页面通常附带工作流
- **Reddit r/comfyui**：社区分享工作流
- **OpenArt**：https://openart.ai
- **ComfyUI 官方示例**：GitHub 仓库的 `workflows/` 目录

### 学习路径建议

```
第 1 天： 安装 + 文生图工作流（本章第 1-2 章）
第 2-3 天：界面操作 + 图生图/重绘（本章第 3-4 章）
第 4-5 天：ControlNet + LoRA（本章第 5-6 章）
第 1 周：完成基础学习，能搭建自定义工作流
第 2 周：学习进阶技术（视频、IP-Adapter、高清放大）
第 3-4 周：深入特定领域（风格迁移、产品图、角色设计等）
```

---

# 附录：术语表（中英对照）

| 中文 | English | 说明 |
|------|---------|------|
| 节点 | Node | 功能模块，工作流的最小单位 |
| 工作流 | Workflow | 节点集合及连接的保存文件 |
| 连线/链接 | Link/Connection | 节点之间的数据通道 |
| 检查点 | Checkpoint | 完整的基础模型文件 |
| 潜空间 | Latent Space | 图像的压缩数学表示 |
| 采样器 | Sampler | 从噪声生成图像的核心算法 |
| 调度器 | Scheduler | 控制噪声衰减方式的策略 |
| 条件 | Conditioning | 指引生成方向的内容（文本/图像编码） |
| 提示词 | Prompt | 用户输入的文本描述 |
| 正面提示词 | Positive Prompt | 描述想要的内容 |
| 负面提示词 | Negative Prompt | 描述不想要的内容 |
| CFG 尺度 | CFG Scale | 控制对 prompt 的遵从程度 |
| 种子 | Seed | 随机数，用于复现生成结果 |
| 步数 | Steps | 采样迭代次数 |
| 去噪强度 | Denoise | 图生图中控制修改幅度 |
| VAE | Variational Autoencoder | 像素和潜空间之间的转换器 |
| LoRA | Low-Rank Adaptation | 轻量模型微调技术 |
| ControlNet | — | 通过额外条件控制生成的技术 |
| IP-Adapter | — | 用图像替代文本作为 prompt |
| 自定义节点 | Custom Node | 社区开发的扩展节点 |
| 子图 | Subgraph | 可复用的节点组封装 |
| 绕过 | Bypass | 临时禁用节点 |
| 队列 | Queue | 工作流的执行排队机制 |
| 批量 | Batch | 一次生成多张图像 |
| 放大 | Upscale | 提升图像分辨率 |
| 局部重绘 | Inpainting | 修改图像特定区域 |
| 外绘 | Outpainting | 超出原始边界扩展 |
| 预处理器 | Preprocessor | 提取 ControlNet 引导条件 |
| embedding | Textual Inversion | 通过文本文件定义的概念 |
| 调度 | Scheduler | 管理采样步数的策略 |
| 引导 | Guidance | 控制生成方向的机制 |
| 开源 | Open Source | 源代码公开可查看修改 |
| 集成包 | Integrated Package | 一站式安装包 |
| 管理器 | Manager | 管理自定义节点的工具 |

---

> **文档版本**: v1.0 | **最后更新**: 2026-05-06 | **编译**: 军师祭酒
>
> 本文档基于 ComfyUI 官方文档、社区资源、专业评测综合编译。官方文档以 [docs.comfy.org](https://docs.comfy.org/) 为准。

