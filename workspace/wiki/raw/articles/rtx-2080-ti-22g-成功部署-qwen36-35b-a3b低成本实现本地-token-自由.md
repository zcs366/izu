---
source_url: file:///mnt/i/hermes/wiki_dropbox/RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现本地 Token 自由.md
ingested: 2026-05-10
sha256: 4ce4af1c6697759c1e63ae6f55e0114411adf063ced7d3d1501013d247771664
source: wiki_dropbox
author: 用户提供
original_pub: 本地文件
title: RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现本地 Token 自由
---

# RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现本地 Token 自由

> 来源: RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现本地 Token 自由.md（用户存入 wiki_dropbox）

# RTX 2080 Ti 22G 成功部署 Qwen3.6-35B-A3B：低成本实现本地 Token 自由

[![mikesay](https://picx.zhimg.com/v2-abed1a8c04700ba7d72b45195223e0ff_l.jpg?source=32738c0c&needBackground=1)](https://www.zhihu.com/people/mikesay)

[mikesay](https://www.zhihu.com/people/mikesay)

关注

2 人赞同了该文章





当前，英伟达显卡价格居高不下，本地部署大模型门槛很高。我用便宜的老卡**[RTX 2080 Ti](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=RTX+2080+Ti&zhida_source=entity) 22G** 成功部署了通义千问最新的 Qwen3.6-35B-A3B 大模型，实测效果接近 4090，**43-45 tokens/s** 的生成速度，日常使用完全够用，低成本实现了本地 Token 自由。

这篇文章把我从部署到优化的完整过程和踩过的坑分享给大家，技术小白也能照着一步步来。

------

## 我的部署方法：AI 助 AI，效率翻倍

整个过程我是这么干的，不用你全懂，会提需求就行：

1. **部署阶段**：用本地 opencode 分析我的电脑配置，自动给出部署方案，我监督、确认就行
2. **优化阶段**：把测试速度和终端输出复制给在线 DeepSeek，让它帮分析问题、给出优化方案
3. **迭代验证**：我修改参数重新测试，反复几轮就找到了最佳配置

这种方法门槛很低，你不用记住所有细节，让 AI 帮你写命令，你只管验证结果就行。

------

## 部署：关键步骤和踩坑总结

## 我的硬件环境



| 组件 | 配置                       | 说明                                                         |
| ---- | -------------------------- | ------------------------------------------------------------ |
| GPU  | NVIDIA RTX 2080 Ti 22GB    | 刚好能放下 [Q4_K_M 量化版](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=Q4_K_M+量化版&zhida_source=entity) |
| CPU  | Intel i5-12400 (6核12线程) | 完全够用                                                     |
| 内存 | 64GB DDR4                  | 建议至少 32GB 以上                                           |
| 系统 | Windows 11                 | Windows 10 也完全支持                                        |



## ⚠️ 给小白的五个关键提醒（我踩过的坑）

## 1️⃣ 不要用 WSL2！直接原生 Windows

很多教程推荐 WSL2，**我实测结论：完全没必要**：

- WSL2 有虚拟化开销，性能损失 15-20%
- [CUDA](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=CUDA&zhida_source=entity) 配置更复杂，容易出兼容性问题
- 如果已经装了，直接删除释放空间：

```text
wsl --unregister Ubuntu-22.04
```

原生 Windows 比 WSL2 更快更简单，一步到位。

## 2️⃣ CUDA 必须降级到 12.8.2，13.x 会输出乱码

这是**血的教训**：llama.cpp 和 CUDA 13.x 兼容性不好，Qwen 会输出乱码，折腾半天发现是版本问题。

- 驱动**不用降级**，只需要卸载 CUDA 工具链重新安装即可
- 卸载后重启，再安装 12.8.2，驱动保留不影响
- 官方下载：CUDA 12.8.2 存档

## 3️⃣ 必须用 [Developer Command Prompt for VS 2022](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=Developer+Command+Prompt+for+VS+2022&zhida_source=entity) 编译

普通 CMD 或 PowerShell 找不到 MSVC 编译器，一定会编译失败。

- 开始菜单搜索 **"Developer Command Prompt for VS 2022"**
- 用这个打开，再执行编译命令

## 4️⃣ Visual Studio 必须装对组件

- 需要勾选 **"使用C++的桌面开发"** 工作负载
- 需要安装 **[CMake](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=CMake&zhida_source=entity) 工具**（在单个组件里找）
- 只装 BuildTools 就够了，不需要装完整 VS IDE，节省空间

## 5️⃣ CMAKE_CUDA_ARCHITECTURES 必须指定为 75

RTX 2080 Ti 是 Turing 架构，Compute Capability **7.5**：

- 不指定的话，默认会编译多种架构，浪费时间
- 按本文写的参数来，一步到位

## 完整部署命令

## 第一步：编译 llama.cpp（启用 CUDA）

```text
cmake -B build ^
  -DGGML_CUDA=ON ^
  -DCMAKE_CUDA_ARCHITECTURES=75 ^
  -DGGML_CUDA_F16=ON ^
  -DGGML_CUDA_DMMV=ON ^
  -DGGML_CUDA_MMQ=ON
cmake --build build --config Release -j
```

编译时间大约 5-15 分钟，取决于你的 CPU 速度。

## 第二步：下载模型

推荐选择：**Qwen3.6-35B-A3B-Instruct Q4_K_M**（19.71 GB）

- **[Hugging Face](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=Hugging+Face&zhida_source=entity)**：[https://huggingface.co/Qwen/Qwen3.6-35B-A3B-Instruct-GGUF](https://link.zhihu.com/?target=https%3A//huggingface.co/Qwen/Qwen3.6-35B-A3B-Instruct-GGUF)
- **[ModelScope](https://zhida.zhihu.com/search?content_id=274458776&content_type=Article&match_order=1&q=ModelScope&zhida_source=entity) 国内镜像**：[https://modelscope.cn/models/qwen/Qwen3.6-35B-A3B-Instruct-GGUF/summary](https://link.zhihu.com/?target=https%3A//modelscope.cn/models/qwen/Qwen3.6-35B-A3B-Instruct-GGUF/summary)

## 第三步：初始启动（可运行版）

```text
cd D:\llama.cpp\build\bin\Release
.\llama-server.exe `
  -m "D:\llama.cpp\models\qwen3.6-35b-a3b-instruct-Q4_K_M.gguf" `
  --jinja `
  -ngl 99 `
  -c 4096 `
  -fa on `
  -t 6 `
  -b 2048 `
  --cache-type-k q8_0 `
  --cache-type-v q8_0 `
  --host 0.0.0.0 `
  --port 8080 `
  --no-mmap `
  -np 1
```

## 第四步：访问测试

- 本地访问：http://localhost:8080
- 内网访问：http://你的IP:8080
- API 兼容 OpenAI，Hermes/opencode 可直接调用
- 防火墙记得放开 8080 端口

## 常见问题快速排查



| 问题           | 可能原因             | 解决方法                       |
| -------------- | -------------------- | ------------------------------ |
| 输出乱码       | CUDA 13.x 兼容性问题 | 降级到 12.8.2                  |
| 编译失败       | 没用对终端           | 用 Developer Command Prompt    |
| CMake 找不到   | VS 没装 CMake 组件   | VS Installer 里添加            |
| 启动就显存溢出 | 上下文开太大         | 减小 -c 参数，或部分卸载到 CPU |
| 速度很慢       | 部分专家卸载到 CPU   | 参考下文优化，全部放 GPU       |



------

## 优化：全部放 GPU 才是最快的

## 我的优化历程

这是三轮测试的结果：



| 阶段     | 配置策略                  | 生成速度       | 结论                     |
| -------- | ------------------------- | -------------- | ------------------------ |
| 初始版   | 6线程 + 部分专家卸载到CPU | 19.16 tokens/s | 显存友好但传输开销大     |
| 优化尝试 | 12线程 + 更多CPU卸载      | 16.50 tokens/s | ❌ 过度卸载，速度反而下降 |
| 最终最佳 | 8线程 + 全部放GPU         | 43-45 tokens/s | ✅ 消除传输瓶颈，速度翻倍 |



## 核心发现

**过度 CPU 卸载是速度杀手**：

CPU→GPU 数据传输开销，远大于把专家留在 CPU 节省的显存带来的收益。既然你的 22GB 显存刚好能放下整个模型，**就不要听信"专家放CPU"的经验**，全部放 GPU 才是真的快。

## 最终最佳配置（48K 上下文 + 全 GPU 加速）

这是经过反复测试验证的最佳配置：

```text
cd D:\llama.cpp\build\bin\Release
.\llama-server.exe `
  -m "D:\llama.cpp\models\qwen3.6-35b-a3b-instruct-Q4_K_M.gguf" `
  --jinja `
  -ngl 99 `
  -c 49152 `
  -fa on `
  -t 8 `
  -b 4096 `
  --cache-type-k q8_0 `
  --cache-type-v q8_0 `
  --host 0.0.0.0 `
  --port 8080 `
  --no-mmap `
  -np 1
```

## 参数说明（为什么这么设置）



| 参数                  | 值     | 原因                                                    |
| --------------------- | ------ | ------------------------------------------------------- |
| -ngl 99               | 99     | 所有层全部 offload 到 GPU，消除传输开销                 |
| -c 49152              | 48K    | 支持长文档分析，比初始 8K 扩展 6 倍，22GB 刚好放下      |
| -t 8                  | 8 线程 | 超线程利用，配合 MoE 架构并行计算（全 12 线程反而过载） |
| -b 4096               | 4096   | 增大批处理提升吞吐量，减少调度开销                      |
| --cache-type-k/v q8_0 | q8_0   | KV 缓存 8 位量化，精度损失可忽略，节省显存              |
| 无 -ot                | -      | 不卸载任何专家到 CPU，全部放 GPU                        |



## 连续任务稳定性测试

我连续跑了 8 个任务验证稳定性，结果如下：



| 任务ID | 输入tokens | Prompt速度 | 生成tokens | 生成速度 | 检查点        |
| ------ | ---------- | ---------- | ---------- | -------- | ------------- |
| 40     | 444        | 568 t/s    | 107        | 43.1 t/s | ✅ 命中31580   |
| 149    | 132        | 522 t/s    | 84         | 45.0 t/s | ✅ 命中32020   |
| 235    | 198        | 631 t/s    | 90         | 45.5 t/s | ✅ 连续        |
| 327    | 46         | 308 t/s    | 110        | 45.0 t/s | ✅ 连续        |
| 439    | 269        | 815 t/s    | 100        | 45.0 t/s | ✅ 连续        |
| 541    | 609        | 944 t/s    | 99         | 44.3 t/s | ✅ 连续        |
| 643    | 193        | 660 t/s    | 219        | 45.3 t/s | ✅ 连续        |
| 864    | 2380       | 1113 t/s   | 56         | 45.5 t/s | ⚠️ 回滚到32020 |



**测试结论**：

- 任务成功率：10/10（100%）
- 生成速度稳定在 43-45 tokens/s
- Prompt 速度最高突破 1113 tokens/s，创本地模型新纪录
- 即使最大 2380 tokens 输入，也只是回滚检查点，不会崩溃，稳定性很好

## 最终性能成果



| 指标        | 结果                                    |
| ----------- | --------------------------------------- |
| 生成速度    | 43-45 tokens/s（比初始提升 125%）       |
| Prompt 速度 | 568-1113 tokens/s（最高 1113 t/s）      |
| 显存占用    | 21.9 GB / 22 GB（97% 利用率，完美压榨） |
| 上下文长度  | 48K（支持长文档分析、长对话历史）       |
| 任务成功率  | 10/10 (100%)，从未 OOM                  |



## 给后来者的五条建议

1. **显存够就全部放 GPU**——传输开销比你想象的大得多
2. **线程不是越多越好**——6 核 12 线程用 8 线程比 12 线程更稳定
3. **Flash Attention 必须开**——实实在在提速，开了就知道好
4. **KV 缓存 q8_0 量化**——精度损失可忽略，显存节省明显
5. **Q4_K_M 量化足够用**——35B 模型效果已经很好，不必强求 Q5/Q6

------

## 使用感受：超出预期的惊喜

我在内网用 WorkBuddy 调用 API，本机用 opencode 调用 API，体验真的不错：

1. **工具调用成功率高**——以前部署的大模型只能聊天，AI Agent 调用工具经常失败。这次 Qwen3.6-35B-A3B 表现很好，网络搜索、本地工具都正常，完全可以作为本地 AI Agent 的智能底座。
2. **输出比在线模型还快**——在线模型经常要排队等待，本地部署稳定响应，高峰时段反而更快。
3. **稳定性好**——十几项任务全部成功完成，只有一次试了 80K 上下文爆了显存，降到 48K 就没问题了。

------

## 结论：这就是 RTX 2080 Ti 22GB 的理论极限

复杂任务交给在线大模型，这个本地配置已经把 RTX 2080 Ti 22GB 压榨到了极限：

✅ **生成速度**：43-45 tokens/s，日常对话流畅不卡 ✅ **上下文**：48K，满足绝大多数长文档分析需求 ✅ **显存利用率**：97%，一分显存一分货 ✅ **性价比**：老显卡废物利用，不用买高价新卡

**适用场景**：

- 日常对话聊天
- 短文本生成
- 长文档分析（48K 上下文）
- 长对话历史处理

如果你手里也有一块 RTX 2080 Ti 22GB，照着这个配置来，就能以极低的成本用上 35B 级别的大模型，实现本地 Token 自由。

**这就是 RTX 2080 Ti + Qwen3.6-35B-A3B Q4_K_M 的最佳配置！**
