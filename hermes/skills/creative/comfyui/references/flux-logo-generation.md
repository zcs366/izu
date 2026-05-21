# Flux FP8 Logo / Brand Concept Generation

> 基于 2026-05-10 会话验证。用 Comfy Org flux1-dev-fp8-with_clip_vae.safetensors (all-in-one) 生成品牌Logo概念图。
> **硬件**：RTX 2080 Ti (22G VRAM) | **ComfyUI**：Windows Portable 0.17.1

---

## 核心结论

- **Flux FP8 + CheckpointLoaderSimple 方案可行**，出图质量好，色彩表现力强
- **不适合精确Logo**——AI无法理解"左翼长城垛口、右翼山脉"这类结构性要求，适合出**氛围概念图**而非成品
- **最佳用途**：生成风格参考（调性/配色/氛围），然后让设计师手绘矢量稿

---

## 可用模型

```
/mnt/i/ComfyUI/ComfyUI_windows_portable/ComfyUI/models/checkpoints/
├── Comfy Org-flux1-dev-fp8-with_clip_vae.safetensors  ← 主要模型
└── sd3.5_large.safetensors                              ← 备选
```

---

## 工作流（已测试通过）

### 基础参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 模型节点 | `CheckpointLoaderSimple` | 不能用 `EmptySD3LatentImage`！要改用 `EmptyLatentImage` |
| 潜空间 | `EmptyLatentImage` (1024×1024) | Flux 不能用 SD3 的 latent 节点 |
| CFG | **1** | Flux 不使用传统 CFG，设 3.5 会过饱和 |
| 步数 | 20-30 | 30步效果稳定，20步也可以 |
| 调度器 | `simple` | 配合 euler 采样器 |
| 反面提示 | 留空 | Flux 不处理反面 CFG，填了也没用 |

### 标准 Workflow JSON（可直接用）

```json
{
  "3": {
    "class_type": "CheckpointLoaderSimple",
    "_meta": {"title": "Load Flux FP8 All-in-One"},
    "inputs": {"ckpt_name": "Comfy Org-flux1-dev-fp8-with_clip_vae.safetensors"}
  },
  "4": {
    "class_type": "CLIPTextEncode",
    "_meta": {"title": "CLIP Text Encode (Prompt)"},
    "inputs": {"text": "YOUR_PROMPT_HERE", "clip": ["3", 1]}
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {"title": "CLIP Text Encode (Negative)"},
    "inputs": {"text": "", "clip": ["3", 1]}
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {"title": "Empty Latent Image (Flux: NOT EmptySD3LatentImage)"},
    "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
  },
  "7": {
    "class_type": "KSampler",
    "_meta": {"title": "KSampler (Flux: cfg=1)"},
    "inputs": {
      "seed": -1,
      "steps": 30,
      "cfg": 1,
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": 1,
      "model": ["3", 0],
      "positive": ["4", 0],
      "negative": ["6", 0],
      "latent_image": ["5", 0]
    }
  },
  "8": {
    "class_type": "VAEDecode",
    "inputs": {"samples": ["7", 0], "vae": ["3", 2]}
  },
  "9": {
    "class_type": "SaveImage",
    "inputs": {"filename_prefix": "logo", "images": ["8", 0]}
  }
}
```

### 运行命令

```bash
# 单个生成（模型首次加载约30-90秒）
cd /home/zcs/.hermes/skills/creative/comfyui
python3 scripts/run_workflow.py \
  --workflow /tmp/your_workflow.json \
  --args '{"prompt": "your prompt", "seed": 12345, "steps": 30}' \
  --output-dir /tmp/logo_outputs \
  --host http://127.0.0.1:8188

# 模型已加载后，每张图约10-30秒（30步）
```

---

## 已验证的Logo Prompt模式

### 模式A：具象概念图（适合與京·大版）

**策略**：给出具体视觉元素 + 风格描述 + 颜色代码。Flux对颜色代码理解准确。

```
Chinese brand logo design, majestic phoenix spreading wings,
left wing shaped like Great Wall battlements,
right wing shaped like mountain ridges,
dark black background #1a1a1a,
phoenix in imperial gold #d4af37 with touches of cinnabar red,
traditional gongbi painting style, seal script feeling,
solemn and powerful, ancient Chinese aesthetic,
vector style, clean lines on dark background
```

**实际效果**：✅ 凤凰姿态舒展，质感好，中国风字符AI自行添加。❌ 长城/山脉融入翅膀的指令被忽略，翅膀没有分段。

### 模式B：几何极简（适合與京·小版/刺绣）

**策略**：强调线条数量 + 扁平 + 无渐变 + 可刺绣。

```
minimalist phoenix logo for embroidery, military style patch design,
phoenix formed by only 7 to 9 geometric angular lines,
olive green #4b5320 on white background,
gold #ffd700 accent lines,
flat vector style, no shadows no gradients,
clean simple silhouette, scalable to small size,
army badge style, bold simple shapes
```

**实际效果**：✅ 几何折线风格，配色准确（军绿+金），线条清晰，适合打样。❌ 线条数多于9条（约15条左右），离"7条折线"有距离。

### 模式C：水彩/自然风（适合美叶·大版）

**策略**：材质关键词（水彩）+ 意象描述 + 暖色调。

```
Chinese education brand logo, watercolor style ginkgo leaf spreading wide,
leaf veins doubling as open book pages,
warm yellow-green #9dc183 and light brown #d2b48c,
off-white paper background #faf0e6,
tiny seedling sprouting at leaf stem base,
soft rounded edges, watercolor paint texture,
warm nurturing atmosphere, gentle and welcoming,
children education brand feeling, organic natural shapes
```

**实际效果**：✅ 温暖柔和，有教育感。❌ AI将"叶+书"理解成了"花+书"，植物形态需要设计师修正。

### 模式D：极简矢量（适合美叶·小版/丝印）

**策略**：极简 + 纯色 + 丝印可行。

```
ultra minimal flat vector logo for children brand,
simple rounded leaf outline,
solid grass green #7cb342,
white interior with three white veins radiating from center,
one tiny dewdrop circle on leaf,
no shadows no gradients, clean crisp lines,
screen print ready design,
scalable from 3cm to 30cm,
pure white background, modern minimalist style
```

**实际效果**：✅ 干净简洁，叶子轮廓清晰，内部分支结构好。可以直接做丝印。❌ "三根叶脉"被理解成了内部分支+小叶子。

---

## 局限性

| 问题 | 说明 |
|------|------|
| **结构性要求不可控** | "左翼化为长城，右翼化为山脉"这类空间性指令，Flux无法精确执行 |
| **线条数不可控** | 指定"7-9条折线"会产出15-20条，AI无法数数 |
| **中文文字不稳定** | 要求生成"與京"二字的提示通常产出乱码字符，只能靠设计师后加 |
| **对称性凭运气** | Logo通常要求对称，但AI出图不一定对称 |

**最佳实践**：ComfyUI出概念氛围图 → 设计师根据规格书手绘矢量稿。不要试图让AI输出成品Logo。

---

## 输出管理

```bash
# 输出目录
/tmp/logo_outputs/   ← 每次运行临时文件
/mnt/i/hermes/output/logo_designs/   ← 持久存档 (Windows: I:\hermes\output\logo_designs\)

# 文件格式
logo_00001_.png  ← 第一张
logo_00002_.png  ← 第二张
# 按运行顺序递增
```
