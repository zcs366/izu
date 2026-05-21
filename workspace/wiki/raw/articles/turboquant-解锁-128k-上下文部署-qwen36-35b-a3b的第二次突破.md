---
source_url: file:///mnt/i/hermes/wiki_dropbox/TurboQuant 解锁 128K 上下文：部署 Qwen3.6-35B-A3B的第二次突破.md
ingested: 2026-05-10
sha256: 24b7056719b1f11bbfb6db7696c2a5ce78d73e4c0aaeb4e5025a9b792fe42302
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: TurboQuant 解锁 128K 上下文：部署 Qwen3.6-35B-A3B的第二次突破
---

# TurboQuant 解锁 128K 上下文：部署 Qwen3.6-35B-A3B的第二次突破

> 来源: TurboQuant 解锁 128K 上下文：部署 Qwen3.6-35B-A3B的第二次突破.md（用户存入 wiki_dropbox）

# TurboQuant 解锁 128K 上下文：部署 Qwen3.6-35B-A3B的第二次突破

[![mikesay](https://pic1.zhimg.com/v2-abed1a8c04700ba7d72b45195223e0ff_l.jpg?source=32738c0c&needBackground=1)](https://www.zhihu.com/people/mikesay)

[mikesay](https://www.zhihu.com/people/mikesay)

关注

2 人赞同了该文章





在上一篇文章中，我分享了在魔改 RTX 2080 Ti 22GB 上部署 Qwen3.6-35B-A3B 的经验：[RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现Token自由](https://link.zhihu.com/?target=https%3A//www.toutiao.com/article/7632874325510570523/%3Flog_from%3D24f14c8f3ab678_1777948772010)

文章很受欢迎！很多读者反馈 48K 上下文还是太小，不能满足日常使用。

为此，花了半天时间，使用开源技术 **[TurboQuant](https://zhida.zhihu.com/search?content_id=274459451&content_type=Article&match_order=1&q=TurboQuant&zhida_source=entity)**，我成功将上下文从 48K 扩展到了 128K（32 倍增长），更让人惊喜的是：**生成速度竟然没有变慢，依然维持在 48 tokens/s。**

这篇文章详细拆解win11上部署 TurboQuant 的方法，希望能帮助大家在老显卡上也能实现长文本自由。

------

## 什么是 TurboQuant？

TurboQuant 是 llama.cpp 的一个实验性分支，专门针对 **[KV Cache](https://zhida.zhihu.com/search?content_id=274459451&content_type=Article&match_order=1&q=KV+Cache&zhida_source=entity)（键值缓存）** 进行了动态量化优化。

## 核心原理：压缩显存的"草稿纸"

理解 KV Cache 是理解 TurboQuant 的关键：

- **KV Cache** 是大模型在处理长文本时，为了记住前文信息而保存在显存里的临时数据。
- **痛点**：传统的 KV Cache 使用 q8_0（8-bit 量化），占用显存极大。上下文越长，KV Cache 占用越多，直到显存溢出（OOM）。

**TurboQuant 的做法**：

它在推理过程中，动态地将 KV Cache 压缩为 **q4_1（4-bit 量化）**。

- **压缩率**：KV Cache 体积直接缩小 **50%**。
- **效果**：省下的显存空间，正好用来容纳更长的上下文。

这就像把笔记本的纸张厚度减半，就能写两倍多的字，而不需要买更大的笔记本。

------

## 部署实操：一键抄作业

## 1. 获取 TurboQuant 预编译包

TurboQuant 目前还在开发中，需要下载预编译版本。

- **GitHub 项目地址**：[https://github.com/TheTom/llama-cpp-turboquant](https://link.zhihu.com/?target=https%3A//github.com/TheTom/llama-cpp-turboquant)
- **下载页面（Releases）**：[https://github.com/TheTom/llama-cpp-turboquant/releases](https://link.zhihu.com/?target=https%3A//github.com/TheTom/llama-cpp-turboquant/releases)

**下载建议**：

在 Releases 页面下载 Windows 版本的压缩包。目前推荐版本是 tqp-v0.1.1，请寻找文件名包含 windows-x64-cuda12.4 的压缩包（例如
turboquant-plus-tqp-v0.1.1-windows-x64-cuda12.4.zip）。

## 2. 准备工作

- **模型**：使用你现有的模型即可（推荐 Qwen3.6-35B-A3B Q4_K_M）。
- **环境**：需要安装 CUDA 12.x。实测 CUDA 12.8 兼容 TurboQuant 的 CUDA 12.4 预编译版，无需降级。

## 3. 启动命令

将解压后的文件放在一个目录（如 D:\llama-turboquant\），然后使用以下命令启动：

```text
cd D:\llama-turboquant\bin

.\llama-server.exe `
  -m "..\models\qwen3.6-35b-a3b-instruct-Q4_K_M.gguf" `
  --jinja `
  -ngl 99 `
  -c 131072 `
  -fa on `
  -t 6 `
  -b 2048 `
  --cache-type-k q4_1 `
  --cache-type-v q4_1 `
  --host 0.0.0.0 `
  --port 8081 `
  --no-mmap `
  -np 1
```

**关键参数说明**：

- --cache-type-k q4_1：核心！设置 Key Cache 为 4-bit TurboQuant 压缩。
- --cache-type-v q4_1：核心！设置 Value Cache 为 4-bit TurboQuant 压缩。
- -c 131072：设置上下文长度为 128K。

## 4. 常见问题处理

**Q: 提示 DLL 缺失？**

A: TurboQuant 依赖 [OpenSSL](https://zhida.zhihu.com/search?content_id=274459451&content_type=Article&match_order=1&q=OpenSSL&zhida_source=entity) 等库。如果你安装了 Git for Windows，通常会自动解决。如果不行，可以尝试手动从 Git 目录复制 libssl-3-x64.dll 和 libcrypto-3-x64.dll 到程序同级目录。

------

## 性能实测：数据说话

我在魔改 RTX 2080 Ti 22GB 上，使用 Qwen3.6-35B-A3B 进行了详细对比：





| 指标          | 标准版 (48K) | TurboQuant (128K) | 变化           |
| ------------- | ------------ | ----------------- | -------------- |
| 最大上下文    | 48K          | 128K              | ⭐ 约3倍增长    |
| KV Cache 压缩 | q8_0 (8-bit) | q4_1 (4-bit)      | ⭐ 节省 50%     |
| 显存占用      | ~21.9 GB     | ~20.5 GB          | ⭐ 节省 1.4GB   |
| 生成速度      | 41-48 t/s    | ~48 t/s           | ✅ 持平甚至微快 |
| Prompt 速度   | ~550 t/s     | ~550 t/s          | ✅ 持平         |



## 几个关键发现

1. **速度零损耗甚至微快**：KV Cache 压缩降低了内存带宽压力，反而加速了数据读取。
2. **显存真的省了**：从 21.9GB 降到 20.5GB，对于 22GB 的卡，这 1.4GB 就是"能跑"和"不能跑"的生死线。

------

## 为什么我现在全用 TurboQuant？

因为 128K 的上下文足够应对绝大多数长文本场景，而且它的速度并没有因为上下文变长而变慢。这意味着我再也不用担心"文章太长读不完"的 Token 焦虑。

省心、快速、能装下更多内容，这就是老显卡折腾出 TurboQuant 最大的意义。

如果你也有一块 22GB 显存的老显卡，并且经常需要处理长文本，TurboQuant 是目前性价比最高的方案之一。不用换硬件，不用花一分钱，通过技术优化就能实现能力的跃迁。

**这就是魔改 RTX 2080 Ti 22GB + TurboQuant + Qwen3.6-35B-A3B 的最佳组合！**
