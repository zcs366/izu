# 密码与信息的无损压缩与恢复 · 深度技术手册

> **关键词**：信息论 · 熵编码 · 字典压缩 · 上下文混合 · 纠错码 · 神经网络压缩 · Kolmogorov 复杂度
>
> **版本**：v1.0 · 三部曲之 A（技术手册）· 约 2000行
>
> **受众**：有编程基础（至少一门的语言），愿意动手写代码、看伪代码、翻论文的工程师与研究者

---

## 目录

1. [概览与核心理念](#ch1)
2. [理论基础：熵、信息与极限](#ch2)
3. [统计编码 I：Huffman 编码及变种](#ch3)
4. [统计编码 II：算术编码与 ANS](#ch4)
5. [字典编码：LZ77/LZ78 家族](#ch5)
6. [块变换技术：BWT、MTF、RLE](#ch6)
7. [现代实用压缩器解剖](#ch7)
8. [信息恢复：纠错码与信道编码](#ch8)
9. [前沿：神经网络与学习型压缩](#ch9)
10. [实战：实现一个完整的压缩器](#ch10)
11. [未来展望：从压缩到理解](#ch11)

---

## <a name="ch1"></a>第1章 概览与核心理念

### 1.1 什么是无损压缩？

> **定义**：将源数据编码为更少比特的表示，且存在对应的解码过程能从编码表示中**精确重建**源数据。

数学表述：编码函数 E: {0,1}^n → {0,1}^m，解码函数 D: {0,1}^m → {0,1}^n，
满足 D(E(x)) = x 对所有 x ∈ {0,1}^n，且 m < n 对大多数 x 成立。

### 1.2 压缩与"密码"的关系

中文"密码"在这里有两个层次：

| 层次 | 英文对应 | 含义 | 与压缩的关系 |
|------|----------|------|-------------|
| **编码/代码** | Code/Coding | 信息的表示方式 | **直接相关**——Huffman码、算术码、LZ码 |
| **密码/加密** | Cryptography | 信息的保密变换 | 间接相关——加密≈不可压缩 |

**信息论中的"码"(Code)**：码是从符号集合到码字集合的映射。好的码在保持可唯一解码的前提下最小化平均码长——这正是**无损压缩**的核心。

### 1.3 两大流派

```
无损压缩
├── 统计编码（熵编码）
│   ├── Shannon-Fano 编码（1948）
│   ├── Huffman 编码（1952）
│   ├── 算术编码（1976-1987）
│   └── 非对称数字系统 ANS（2014）
│
├── 字典编码
│   ├── LZ77 / LZSS（1977-1982）
│   ├── LZ78 / LZW（1978-1984）
│   └── LZMA / LZMA2（1998-2009）
│
├── 块变换
│   ├── Burrows-Wheeler Transform（1994）
│   ├── 游程编码 RLE
│   └── 移动到前端 MTF
│
└── 上下文混合（现代最优）
    ├── PAQ 系列（2002-2019）
    └── CMIX（2016-至今）
```

### 1.4 核心权衡三角

```
       压缩率（越小越好）
           /\
          /  \
         /    \
        /______\
   速度       内存占用
```

没有任何算法能同时达到三者最优：
- **LZ4**：速度极快（~1GB/s），但压缩率低（~2x）
- **XZ/LZMA2**：压缩率极高（~10x），但慢
- **Zstd-3**：平衡点——接近最优的压缩/速度比
- **CMIX**：压缩率最高（~2x 超越 Gzip），但慢到不实用

### 1.5 一个重要的哲学结论

> **压缩即理解。** 一个能完美压缩某类数据的算法，本质上"理解"了该类数据的结构。

这解释了为什么语言模型（LLM）是出色的压缩器：它们理解了语言的统计结构，能准确预测下一个token，这本身就是"压缩"的另一种形式。

---

## <a name="ch2"></a>第2章 理论基础：熵、信息与极限

### 2.1 Shannon 信息熵

> Claude Shannon 在 1948 年发表的《通信的数学理论》中定义了信息熵，开创了信息论。

**定义**：设离散随机变量 X 有概率分布 p(x)，则 X 的熵为：

```
H(X) = -Σ p(x) · log₂ p(x)  (比特)
```

**直观理解**：熵是"平均惊奇度"。一个必然事件（p=1）的惊奇度为 0；一个极不可能的事件（p≈0）的惊奇度极大。

**示例——掷骰子的熵**：

| 骰子类型 | 概率分布 | 熵 (bits) | 含义 |
|----------|---------|-----------|------|
| 公平六面骰 | 各 1/6 | log₂(6) ≈ 2.585 | 每掷一次需要 2.585 bits 编码 |
| 灌铅骰子 (99%出1) | 1: 0.99, 其他: 0.002 | ≈ 0.062 | 几乎总是1，几乎无信息 |
| 公平两面硬币 | 各 1/2 | 1.0 | 每次掷出正好 1 bit |

**为什么熵是压缩的极限**：

**Shannon 源编码定理**：对于独立同分布信源 X，任何无损编码的平均码长 L* 满足：
```
H(X) ≤ L* < H(X) + 1
```
也就是说：
- **无法更低**：没有任何编码方案能使平均码长小于熵
- **可以逼近**：存在编码方案（如算术编码）使码长任意接近熵

### 2.2 条件熵与链式法则

**条件熵**：知道 Y 之后，X 还剩下多少不确定性？
```
H(X|Y) = -Σ p(x,y) · log₂ p(x|y)
```

**链式法则**：
```
H(X,Y) = H(X) + H(Y|X)
```

**对压缩的启示**：利用上下文可以降低熵。比如一段中文文本中，看到"信息"后，下一个字是"论"的概率远高于"平"——这就是**上下文模型**能提高压缩率的原因。

### 2.3 交叉熵与 KL 散度

**交叉熵**：使用分布 q 来编码来自分布 p 的数据时，所需的平均比特数：
```
H(p,q) = -Σ p(x) · log₂ q(x) = H(p) + D_KL(p||q)
```

**KL 散度**：因使用错误分布而多花费的比特数：
```
D_KL(p||q) = Σ p(x) · log₂(p(x)/q(x))
```

这是数据压缩与**机器学习**交汇的关键概念：训练语言模型本质上是在最小化训练数据上的交叉熵。

### 2.4 Kolmogorov 复杂度（算法信息论）

**定义**：字符串 s 的 Kolmogorov 复杂度 K(s) 是能生成 s 的最短程序（在某通用图灵机上）的长度。

**区别于 Shannon 熵**：
- Shannon 熵假设数据来自已知分布
- Kolmogorov 复杂度不依赖任何分布——它是**绝对的、算法层面的信息量**

**关键性质**：
1. **不可计算**：没有通用算法能计算任意字符串的 Kolmogorov 复杂度（与停机问题等价）
2. **对于随机字符串**：K(s) ≈ |s|（无法压缩）
3. **对于结构化数据**：K(s) << |s|
4. **例子**：圆周率 π 的前十亿位，Kolmogorov 复杂度 ≈ O(log n)，因为存在一个很短的程序就能生成它——但 Shannon 熵（按符号频率计算）会认为它是随机的

> **深刻启示**：Shannon 熵是"给定模型假设下的信息量"，Kolmogorov 复杂度是"数据本身蕴含的信息量"。两者的差距就是我们模型的**不完善程度**。

### 2.5 率失真理论（Rate-Distortion Theory）

对于**有损压缩**：给定允许的最大失真 D，所需的**最小比特率** R(D) 由率失真函数给出：
```
R(D) = min_{p(x̂|x): E[d(x,x̂)] ≤ D} I(X; X̂)
```
其中 I(X; X̂) 是 X 和重建 X̂ 之间的互信息。

无损压缩是 R(0) 的特例——此时的比特率下限就是 H(X)。

### 2.6 理论极限的实用意义

| 理论结果 | 实践含义 |
|----------|---------|
| 熵是下限 | 如果 gzip 已经达到 2.5 bpb，理论上最多能压到 ~1.5 bpb |
| 条件熵递减 | 用更大的上下文模型（更长 n-gram、NN）可以获得更好的压缩 |
| Kolmogorov 复杂度不可计算 | 没人能确切知道"数据能不能再压小"——只能尝试更好的模型 |
| 交叉熵 = 负对数似然 | 机器学习中降低 loss 等价于提高压缩率 |

---

## <a name="ch3"></a>第3章 统计编码 I：Huffman 编码及变种

### 3.1 从 Shannon-Fano 到 Huffman

Shannon-Fano 编码（1948）是最早的熵编码方法，但不一定最优。Huffman 在 1952 年证明了**Huffman 编码是最优前缀码**——在给定符号概率分布的情况下，没有其他前缀码能达到更小的平均码长。

### 3.2 Huffman 编码算法

**构建 Huffman 树的算法**（O(n log n)）：

```
1. 为每个符号创建叶节点，权重 = 符号频率
2. 取出权重最小的两个节点，合并为新节点（权重=和）
3. 左分支→0，右分支→1
4. 重复步骤2-3，直到只剩一个根节点
5. 从根到叶的路径即为该符号的码字
```

**示例**：

| 符号 | 频率 | Huffman 码 | 长度 |
|------|------|-----------|------|
| A | 40% | 0 | 1 bit |
| B | 25% | 10 | 2 bits |
| C | 20% | 110 | 3 bits |
| D | 10% | 1110 | 4 bits |
| E | 5% | 1111 | 4 bits |

平均码长 = 0.40×1 + 0.25×2 + 0.20×3 + 0.10×4 + 0.05×4 = 1.95 bits/symbol

对比如固定长度编码（log₂5 ≈ 2.32 bits/symbol）——节省了 ~16%。

### 3.3 Huffman 的最优性证明

**为什么 Huffman 是最优前缀码？**

核心思路：最优前缀码必然满足：最深的两个符号（出现最少的）作为兄弟在树的最后一层。Huffman 算法正是将此性质逆向应用于每一轮合并。

### 3.4 规范 Huffman 码

**问题**：标准 Huffman 码需要传输整个树结构（符号→码长映射），开销大。

**规范 Huffman 码**：只传输**每个符号的码长**，然后按规范顺序分配码字。接收端可以自动重建编码表。

**规范规则**：
1. 码长从短到长排列
2. 同码长的符号按数值顺序排列
3. 码字按数值递增分配，每个码长组的起始码字 = 前一组长度的最后一个码字 + 1 然后左移一位

**示例**——如果码长分配为 A:1, B:2, C:3, D:3, E:3：
```
先按码长排序：A(1), B(2), C(3), D(3), E(3)
分配码字：A=0, B=10, C=110, D=1110, E=1111
```
只需要传输 `[A:1, B:2, C:3, D:3, E:3]`——这比传输整棵树节省得多。

### 3.5 Huffman 的局限

| 局限 | 表现 | 解决方案 |
|------|------|---------|
| **整数码长** | 每个符号的码长必须是整数比特 | 算术编码（可以给概率 0.3 的符号分配 1.74 bits） |
| **需要概率分布** | 必须预知或统计频率 | 自适应 Huffman（动态更新树） |
| **非自适应** | 编码前要扫描两遍数据 | LZ+Huffman 组合（如 Deflate 用第一遍字典生成，第二遍熵编码） |

### 3.6 自适应 Huffman 编码（FGK/Update 算法）

不需要预扫描数据，边编码边更新树。关键点是维护**兄弟性质**（Sibling Property）：所有内部节点按权重递减排列，且兄弟节点的权重之和等于父节点。

当符号出现时，更新其权重→调整树结构以维持兄弟性质→编码。

时间复杂度 O(1) 每次更新（均摊）。

### 3.7 Deflate 中的 Huffman 应用

Deflate（RFC 1951）使用**两个独立的 Huffman 树**：
1. **字面量/长度树**：256个字面量 + 1个结束符 + 29个长度
2. **距离树**：30个距离

此外，Huffman 树本身被**二次压缩**（用另一个 Huffman 树编码码长序列）。

> **关键设计决策**：Deflate 用动态 Huffman 还是静态 Huffman？动态需要存储树（约 200 bits 开销），静态使用固定表。对于小文件，静态更好；大文件，动态更好。

---

## <a name="ch4"></a>第4章 统计编码 II：算术编码与 ANS

### 4.1 为什么需要算术编码？

Huffman 编码给每个符号整数比特——这限制了它对熵的逼近能力。

**例子**：两个符号 A(p=0.9), B(p=0.1)
- 熵 H = -0.9×log₂0.9 - 0.1×log₂0.1 = 0.469 bits/symbol
- Huffman 平均码长 = 0.9×1 + 0.1×1 = 1.0 bits/symbol
- 效率损失：1.0 / 0.469 = 2.13x！

对于二元信源（如黑白图像），Huffman 几乎不比原始数据好，但算术编码可以逼近 0.469 bits/symbol。

### 4.2 算术编码的核心思想

> **将整个消息映射为 [0,1) 区间内的一个实数。**

**编码过程**：
```
初始区间 [0, 1)
对每个符号 s：
  1. 当前区间根据符号的概率分布划分
  2. 选择 s 对应的子区间作为新区间
编码消息后，输出最终区间内的任意一个数（通常是二进制小数）
```

**解码过程**：用相同的概率模型，根据落在哪个子区间反向推断符号。

### 4.3 实战示例

编码消息 "AABA"，符号 A 概率 0.7，B 概率 0.3：

```
初始区间 [0.000, 1.000)
符号 A → 取前 70% → [0.000, 0.700)
符号 A → [0.000, 0.490)    (0.000 + 0.700×0.7)
符号 B → [0.343, 0.490)    (0.000 + 0.490×0.3 到 0.490)
符号 A → [0.343, 0.446)    (0.343 + 0.147×0.7)
```

输出：区间 [0.343, 0.446) 内任意二进制小数，如 0.011...（二进制）。

解码时，从 0.011...（十进制 ~0.375）落在 [0,0.7)→A→[0,0.49)→A→[0.343,0.49)→B→[0.343,0.446)→A。

### 4.4 实际实现中的问题

1. **精度问题**：无限精度的实数在计算机中不可行。解决方案：**整数算术编码**（使用 32-bit 整数 + 重标准化）。

2. **重标准化**（Renormalization）：
   ```
   当区间完全在 [0, 0.5) 时 → 输出 0，区间 ×2
   当区间完全在 [0.5, 1) 时 → 输出 1，区间 ×2 - 0.5
   当区间包含 0.5 时 → 用"下一位未知"标记（carry propagation）
   ```

3. **结束标记**：需要在编码流末尾加一个唯一可解码的终结符。

### 4.5 上下文自适应算术编码

**思想**：基于前面 n 个符号（上下文）动态调整当前符号的概率分布。

```
P(x_k | x_{k-1}, x_{k-2}, ..., x_{k-n})
```

**n 阶上下文模型**在算术编码上的应用称为 **PPM**（Prediction by Partial Matching）。

**PPM 的关键机制**：
- 使用 hasta n 阶上下文（n 通常取 3-5）
- 当某个序列未被观测到时，"退化"到 (n-1) 阶上下文（逃逸机制）
- 最后退化到 0 阶（全局频率）
- 复杂的逃逸概率估计方法：PPM-A, PPM-B, PPM-C, PPM-D, PPM-Z

在 Calgary Corpus 标准测试集上，PPM 可达到 ~2.0-2.1 bpb，优于 LZ77（~2.5 bpb）。

### 4.6 非对称数字系统（ANS）

**Jarek Duda 在 2014 年提出的 ANS** 是近十年来压缩领域最重要的理论突破。它同时具备：
- **算术编码的效率**（非整数比特）
- **Huffman 的速度**（仅需查表和加减法）

**核心思想**：将符号流映射为单个**自然数** x，而非实数区间。

```
编码：x' = C(s, x) = x * p_s + base_s
解码：s = symbol_at(x mod M),  x' = x / p_s

其中 base_s = cum_count[s], M = total_count
```

**为什么快**：
- 一次编码/解码只需要一次乘法和几次查表
- 硬件友好的 SIMD 并行
- 状态 x 可以始终保持在 CPU 寄存器的比特位中

**变异种类**：
- **rANS**（range ANS）：用区间操作，快于算术编码
- **tANS**（table ANS）：预计算状态转移表，更快
- **uANS**（unified ANS：流式优化版本

**应用**：
- **Zstd** 使用 FSE（Finite State Entropy）= tANS
- **LZ5**、**Lizard**、**Oodle** 等现代压缩库使用 ANS
- Apple LZFSE、Google Draco 3D 网格压缩

| 编码器 | 压缩率 | 编码速度 | 解码速度 | 专利状况 |
|--------|-------|---------|---------|---------|
| Huffman | 差（~1.0 bits 冗余） | 极快 | 极快 | 自由 |
| 算术编码 | 最优 | 慢 | 慢 | 自由 |
| ANS（tANS） | 接近最优（<0.1% 冗余） | 快 | 快 | 无专利障碍 |

> **工程共识（2026）**：在可以有全新编码设计的项目中使用 ANS/tANS，在兼容性优先的场景中使用 Huffman。算术编码只在学术项目中使用。

---

## <a name="ch5"></a>第5章 字典编码：LZ77/LZ78 家族

### 5.1 核心思想

**用指向历史数据的指针代替重复出现的字符序列。**

```
原始：abcababc
      ↑   ↑
      |   |
    第一次 第二次出现——可以用 (偏移=3, 长度=3) 替代
```

### 5.2 LZ77（1977）

**Lempel-Ziv 1977**——滑动窗口字典压缩的鼻祖。

**编码结构**：
```
                已编码的历史区                未编码数据
         ┌──────────────────────────┐
         │  滑动窗口（如 32KB）     │   前瞻缓冲区
         │  ......abcdefghijk...... │   abcijk.....
         └──────────────────────────┘
                ↑              ↑
              查找最长匹配    当前编码位置
```

**每个编码单元输出**：`(距离, 长度, 下一字符)`

- 距离：当前指针到匹配位置的往回偏移量
- 长度：匹配的字符数
- 下一字符：匹配后的下一个字符（处理���匹配的情况）

**解码**：解码器维护同样的滑动窗口，根据 (距离, 长度, 字符) 重建数据。

### 5.3 LZSS（1982）——LZ77 的改进

> Storer 和 Szymanski 的改进——解决 LZ77 的**"匹配不一定划算"**问题。

**核心改进**：
- 对于较长的匹配（超过阈值，如 3 字节），输出 `(标记位, 距离, 长度)`
- 对于短匹配或不可匹配，直接输出原始字符 + 1-bit 标记
- 标记位告诉解码器下一个单元是 "原样字符" 还是 "指针"

**节省的分析**：
```
匹配长度 < 3：指针占用的空间 (标记+距离+长度) > 直接输出 3 个字符
匹配长度 ≥ 3：指针更省
```

### 5.4 LZ78 与 LZW（1978-1984）

**LZ78 的不同哲学**：不用固定大小的滑动窗口，而是维护一个**不断增长的字典**。

- 从空字典开始
- 遇到已知短语时，输出字典索引
- 未匹配时，创建新字典条目
- 字典可以无限增长（或使用替换策略）

**LZW（Terry Welch, 1984）**——LZ78 的实用化版本：
- 字典预初始化 256 个单字符条目
- 每次编码后，将"刚编码的短语 + 下一个字符"加入字典
- 不需要显式传输字典——解码器同步建立

**LZW 的经典应用**：
- GIF 图像格式（CompuServe, 1987）
- Unix compress 命令（已废弃，被 gzip 取代）
- 调制解调器 V.42bis 协议

### 5.5 算法对比

| 特性 | LZ77 | LZSS | LZ78 | LZW |
|------|------|------|------|-----|
| 字典类型 | 滑动窗口 | 滑动窗口 + 最小匹配 | 全局增长字典 | 全局增长字典 |
| 字典传输 | 不需要 | 不需要 | 不需要 | 不需要 |
| 内存占用 | O(窗口大小) | O(窗口大小) | O(字典大小) | O(字典大小) |
| 编码复杂度 | O(n×窗口) | O(n×窗口) | O(n) | O(n) |
| 典型压缩率 | 中等 | 好 | 好 | 好 |
| 代表格式 | ZIP 前的 LZ77 | Deflate | UEFI | GIF、compress |

### 5.6 LZ77 + Huffman：Deflate 组合

**Deflate**（Phil Katz, PKWare, 1993）的核心：
```
LZ77（滑动窗口 32KB） → 匹配搜索生成 (长度, 距离) 对
            ↓
Huffman 编码（两个独立树）
            ↓
1. 字面量 + 长度共用一个 Huffman 树（286个符号）
2. 距离用一个 Huffman 树（30个符号）
```

**匹配搜索优化**：使用哈希链（hash chain）或哈希表逼近 O(n) 时间。

**影响**：Deflate 成为 ZIP、gzip、PNG 的压缩核心，统治了 1990s-2010s 的文件压缩领域。

### 5.7 现代 LZ 变体

| 算法 | 年份 | 改进 | 公司 |
|------|------|------|------|
| **LZMA** | 1998 | LZ77 + 区间编码 + 超大型字典 | 7-Zip (Igor Pavlov) |
| **LZX** | 1997 | LZ77 + 算术编码 | Microsoft (CAB) |
| **LZHAM** | 2012 | LZ + 算术编码 + 面向 GPU 解压 | RAD Game Tools |
| **LZ4** | 2011 | 极简 LZ77（16KB窗口），极致速度 | Yann Collet |
| **Zstd** | 2015 | LZ77 + FSE(ANS) + 多级压缩 | Facebook/Yann Collet |
| **Brotli** | 2013 | LZ77 变体 + Huffman + 预置字典 | Google |
| **LZSSE** | 2016 | LZ + ANS 的高并行优化 | Cyan |

**Zstd 为何特殊**：
- 压缩级别 1-22，覆盖速度/率图谱
- 解压速度在所有级别保持 ~1 GB/s
- 支持字典训练
- `--patch-from` 模式（增量压缩）
- `--rsyncable` 模式（可部分同步）

---

## <a name="ch6"></a>第6章 块变换技术：BWT、MTF、RLE

### 6.1 Burrows-Wheeler Transform (BWT)

> Michael Burrows 和 David Wheeler 在 1994 年发明，用于 bzip2。

**惊人特性**：BWT 把输入文本变换为使得**相同字符趋于聚集**的新序列，变换本身**不改变数据大小**（可逆），但变换后的数据更容易被后续的统计编码压缩。

**BWT 算法**：

```
输入：'banana$'（$ 是唯一结束标志）
1. 生成所有循环移位：
   banana$  anana$b  nana$ba  ana$ban  na$bana  a$banan  $banana
2. 按字典序排序：
   $banana
   a$banan
   ana$ban
   anana$b
   banana$
   na$bana
   nana$ba
3. 取最后一列：'annb$aa'（BWT 输出）
4. 索引 = 原行在排序后的位置 = 4
```

**解码**（逆 BWT）：
已知输出序列 `L = 'annb$aa'` 和原行索引 `I = 4`：
1. 对 L 排序得到第一列 F = `$aaabnn`
2. 构建转换向量 T：L 中每个字符在 F 中的对应位置
3. 从 I 开始沿 T 回溯 -> 按 F 读取

**为什么 BWT 有效**：
- 相同字符在变换后聚集在一起 → 更容易被**游程编码**或**零阶熵编码**压缩
- 常见的英文"the"、"and"片段在 BWT 后聚集

### 6.2 移动到前端编码（MTF）

**思想**：维护一个符号列表，每次编码一个符号后将其移到列表最前面。频繁出现的符号保持在列表前端，用较小的索引编码。

```
初始列表：[a, b, c, d, ..., z]
输入序列：b a n a n a
编码：
  b → 索引 1 (a在0), 列表→[b, a, c, d, ..., z]
  a → 索引 1, 列表→[a, b, c, d, ..., z]
  n → 索引 13, 列表→[n, a, b, c, ..., m, o, ..., z]
  a → 索引 1, 列表→[a, n, b, c, ..., z]
  n → 索引 1, 列表→[n, a, b, c, ..., z]
  a → 索引 1, 列表→[a, n, b, c, ..., z]
输出：1, 1, 13, 1, 1, 1
```

**效果**：经过 BWT 的"相同字符聚集"后，MTF 将聚集的相同字符转化为**大量小数字**（主要是 0 和 1），后续使用 RLE 或 Huffman 编码非常高效。

### 6.3 bzip2 的完整流水线

```
输入 → BWT → MTF → RLE → Huffman → 输出
                         (游程编码   (多个Huffman树
                          对零游程)    + 选择机制)
```

**性能特征**（在 8.5MB 二进制上）：
- 压缩比：4.5-5.5x（好于 gzip 的 5.36x，差于 XZ 的 10.33x）
- 压缩速度：慢（~100 MB/s）
- 解压速度：中等（~250 MB/s）

**bzip2 块大小**：100k-900k bytes，可选级别 1-9。

### 6.4 游程编码（RLE）

**最简形式**：将连续重复的字符替换为 `(字符, 运行长度)`。

**三种实用变体**：

| 变体 | 格式 | 适用场景 |
|------|------|---------|
| 原始 RLE | `5A` | BMP、传真机 |
| 零游程编码 | `(0, N)` = N 个零 | 稀疏矩阵、BWT 后 |
| 按位 RLE | 统计连续 0/1 的游程长度 | 二值图像 |

**经典案例**：BMP 格式在 256 色模式下使用 RLE，使长条的纯色区域（如天空、单色背景）大幅缩小。

---

## <a name="ch7"></a>第7章 现代实用压缩器解剖

### 7.1 Zstd（Zstandard）

> Yann Collet, Facebook, 2015–至今。**当前最全能的通用压缩器。**

**架构**：

```
输入 → LZ77 匹配搜索 → (字面量, (距离,长度)对)
                         ↓
                   FSE (tANS) 熵编码
                         ↓
                   Huffman 辅助编码层
                         ↓
                   帧格式封装
```

**压缩级别谱系**：

| 级别 | 别名 | 压缩比（典型） | 压缩速度 | 解压速度 | 场景 |
|------|------|--------------|---------|---------|------|
| 1 | --fast | ~2.5x | ~500 MB/s | ~1.5 GB/s | 实时压缩 |
| 3 | 默认 | ~5.8x | ~300 MB/s | ~1.5 GB/s | 最佳平衡 |
| 10 | — | ~6.3x | ~50 MB/s | ~1.5 GB/s | 批量处理 |
| 19 | ultra | ~6.7x | ~3 MB/s | ~1.5 GB/s | 归档 |

**关键特征**：
- 解压速度与压缩级别**几乎无关**（始终 ~1 GB/s）——这是 Zstd 最大的工程优势
- 支持**字典训练**：`zstd --train dataset/* -o dictionary` 生成自定义字典，对小文件的压缩有 20-50% 的提升
- `--patch-from baseFile`：只存储与 baseFile 的差异 (类似 git delta)
- `--rsyncable`：允许在 rsync 级别进行增量同步
- 内建 3 种帧格式：Zstd frames、Skippable frames、Dictionary ID
- Long distance mode：匹配可跨越到 128MB 历史窗口

**与其他压缩器的对比**（Albert Wang 基准, 8.5MB 二进制）：

```
Gzip:  压缩比 5.36x, 压缩 197ms, 解压 24ms
Brotli:压缩比 7.79x, 压缩 10.65s, 解压 36ms   ← 网页压缩王者
Zstd-3:压缩比 5.78x, 压缩 31ms,  解压 13ms    ← 全能冠军
Zstd-19:压缩比 6.67x,压缩 357ms, 解压 13ms    ← 高压缩率
XZ:    压缩比 10.33x,压缩 450ms, 解压 97ms   ← 极致压缩率
```

### 7.2 Brotli（Google, 2013）

**设计目标**：Web 内容的极致压缩（替代 Deflate）。

**创新点**：
- **预置字典**：内建包含英文/HTML/CSS/JS 常见词汇的字典（约 125KB），对小文件的压缩有极大改善
- **上下文模型**：2D 上下文（基于字面量类型 + 距离上下文）
- **二阶静态 + 动态编码**：协议头用静态熵编码，数据体用动态

**使用场景**：
- HTTPS 内容编码（HTTP Archive 显示 Brotli 已超过 Gzip 成为 JS/CSS 的头号方案）
- Web 字体（WOFF2 使用 Brotli 压缩
- 缺点：压缩极慢（级别 11 需要 10 秒），不适合**动态**压缩

### 7.3 LZ4 / Snappy

**极致速度的字典压缩**：

| | LZ4 (Yann Collet) | Snappy (Google) |
|------|------------------|-----------------|
| 压缩速度 | ~750 MB/s | **~1 GB/s** |
| 解压速度 | **~3 GB/s** | ~1.5 GB/s |
| 压缩比 | ~2.19x | ~2.40x |
| 代码体积 | ~150 行 | 适中 |

**应用**：
- Linux 内核压缩（initramfs 使用 LZ4）
- Hadoop/Spark 的列式压缩（Parquet Snappy）
- MongoDB wire protocol 压缩
- RocksDB 的块压缩

### 7.4 PAQ 与 CMIX：上下文混合压缩

**PAQ 系列**（Matt Mahoney, 2002–2019）：
- 不使用 LZ 字典
- 使用**数百个上下文模型**的加权混合
- 每个上下文模型用**概率预测**（不是编码！），然后加权平均
- 算术编码器根据最终概率编码

**PAQ 如何工作**：
```
输入比特流 → Ctx0(固定长度上下文) → Model0 → p0
              Ctx1(n-gram上下文)   → Model1 → p1
              Ctx2(单词边界上下文) → Model2 → p2
              ...
              CtxN(高阶混合)      → ModelN → pN
                                ↓
                    自适应加权平均 → p_final
                                ↓
                        算术编码器
```

**CMIX**（Byron Knoll, 2016–至今）：
- 当前**压缩比最高**的公开通用压缩器
- 使用了 **2,122 个上下文模型**，包含 LSTM 神经网络
- 在 enwik8 上达到 ~1.63 bpb（gzip 约 2.9 bpb, paq8px 约 1.7 bpb）
- 代价：压缩速度 ~0.1 MB/s，内存占用数 GB

| 压缩器 | enwik8 (bpb) | 压缩速度 | 内存 |
|--------|-------------|---------|------|
| gzip -9 | ~2.89 | ~100 MB/s | ~1 MB |
| bzip2 -9 | ~2.55 | ~15 MB/s | ~50 MB |
| xz -9 | ~2.10 | ~5 MB/s | ~100 MB |
| zstd -19 | ~2.08 | ~3 MB/s | ~100 MB |
| paq8px | ~1.70 | ~0.5 MB/s | ~2 GB |
| cmix v21 | ~1.63 | ~0.1 MB/s | ~16 GB |

### 7.5 压缩器选择决策树

```
你的场景是什么？
├── 实时流处理（网络包、视频帧）
│   └── → LZ4 或 Snappy
├── 通用文件压缩（日志、文档、配置文件）
│   └── → Zstd-3（默认）
├── 网页静态资源预压缩
│   └── → Brotli-11
├── 长期归档（冷存储）
│   └── → XZ 或 Zstd-19
├── 给你不认识的同事发文件
│   └── → Gzip（人人能解）
├── 嵌入固件/内存受限
│   └── → LZ4（极小解码器,~2KB）
├── 需要随机解压
│   └── → LZ4 帧格式（每个帧可独立解压）
└── 追求极限压缩率（不计时间成本）
    └── → CMIX 或 PAQ8px
```

---

## <a name="ch8"></a>第8章 信息恢复：纠错码与信道编码

### 8.1 为什么要纠错码？

压缩去掉了冗余；纠错码**添加冗余**以便在噪声信道中恢复原始数据。

> **关键洞察**：直接传输压缩数据是危险的——压缩数据中任何一位错误都会导致整个解压失败（错误扩散）。因此必须用纠错码保护。

### 8.2 Shannon 信道编码定理

对带宽为 W、信噪比为 SNR 的信道，最大无差错传输速率为：
```
C = W · log₂(1 + SNR)  (bits/s)
```

**分离定理**（Separation Theorem）：在渐近极限下，可以独立设计源编码（压缩）和信道编码（纠错），组合仍然最优。这支撑了整个通信系统的分层设计——先压缩，再加纠错，再调制传输。

### 8.3 Reed-Solomon 码（1960）

**原理**：将 k 个数据符号视为**有限域 GF(2^m) 上的多项式系数**，求该多项式在 n 个不同点上的值，取 n=k+2t 个。任意 k 个正确的值可恢复原多项式。

```
数据 (k个符号) → 多项式 P(x) of degree k-1 → n个点值
错误 → 接收 n ≤ k+2t 个点 → 任意 k 个正确点→恢复 P(x)
```

**参数**：RS(255, 223) 可以纠正 16 个错误符号。

**应用**：
- QR 码（最大纠错级别可恢复 30% 破损）
- 光盘（CD/DVD/Blu-ray）
- 卫星通信（DVB-S）
- RAID 6（双奇偶校验 = 特定结构的 RS 码）

### 8.4 LDPC 码（Low-Density Parity-Check）

> 1963 年由 Gallager 发明，被遗忘 30 年，1990s 代被重发现代成为 5G/Wi-Fi 的核心。

**核心思想**：用**稀疏校验矩阵**定义的线性分组码。稀疏性（每行每列只有少量 1）使得高效的迭代解码成为可能。

**性能**：编码长度 n=64800 的 DVB-S2 LDPC 码距离 Shannon 极限仅 0.7 dB。

**应用**：
- 5G NR 数据信道（QC-LDPC）
- Wi-Fi 6 (802.11ax)
- DVB-S2/S2X 卫星电视
- 10GBASE-T 以太网
- 深空通信（CCSDS）

### 8.5 喷泉码（无速率码）

> 与传统纠错码不同，喷泉码**从 K 个源符号生成无限编码符号**，接收端只需要收到任意 K(1+ε) 个符号即可恢复。

**LT 码**（Luby Transform, 2002）：
```
1. 随机选择一个度 d（从度分布中采样）
2. 随机选择 d 个源符号 XOR
3. 输出 XOR 结果 + 选择信息
4. 接收端收到足够多的符号后，用 BP 解码恢复
```

**Raptor 码**（Shokrollahi, 2004）：
- LT 码 + 预编码（外码）的级联
- 接近线性的编码/解码复杂度
- 用于 3GPP MBMS、DVB-H 等标准

**应用场景**：大规模文件广播、卫星组播、IoT 通信——当不知道信道的具体质量时，喷泉码的"发射-直收到够为止"策略极为优雅。

### 8.6 联合源信道编码（JSCC）

> 当 Shannon 分离定理的假设不成立时（短码长、低延迟、非渐近场景），联合设计压缩和纠错可以更好。

**深度 JSCC**（2020s 新方向）：
- 用一个神经网络端到端学习从源到信道的映射
- 不需要显式的压缩 + 纠错两层
- 在短码长（几十到几百比特）场景下显著优于分离设计
- 适用于：URLLC（超可靠低延迟通信）、无线图像/视频传输

### 8.7 压缩与纠错的配对实践

| 数据源 | 压缩方式 | 保护的纠错码 | 应用 |
|--------|---------|-------------|------|
| QR 码原始数据 | 无或需预压缩 | Reed-Solomon | 手机支付扫码 |
| 数字电视视频 | H.264/H.265（有损） | LDPC + BCH | DVB-T2 |
| 卫星通信数据 | Zstd/LZMA | LDPC + RS | Starlink、军事 |
| 深空探测图像 | JPEG2000（有损） | LDPC（CCSDS） | 火星、木星探测 |
| 无线广播文件 | 前向纠错保护无压缩/预压缩 | RaptorQ | 3GPP eMBMS |

---

## <a name="ch9"></a>第9章 前沿：神经网络与学习型压缩

### 9.1 语言建模即压缩

> **DeepMind 2023 年的里程碑论文**：语言模型 Chinchilla 70B 在 enwik9 上达到 0.664 bpb。

**核心思想**：大语言模型（LLM）的交叉熵损失 = 压缩的比特数。

```
LLM 的条件概率 P(x_t | x_{<t}) 给算术编码提供了概率分布
算术编码用 LLM 预测的分布编码 x_t
总编码长度 = -Σ log₂ P(x_t | x_{<t}) = 交叉熵
降低交叉熵 = 提高压缩率
```

**为什么 LLM 是天然压缩器**：
- LLM trained on massive text corpus learned the statistical structure of language
- The predicted probability distribution is exactly what an entropy coder needs
- A well-trained LLM captures long-range dependencies that LZ/statistical models cannot

### 9.2 Nacrith（2026 最新突破）

> 2026 年发布的新模型，在 enwik8 上达到 **0.9389 bpb**（对比 Gzip 的 2.9 bpb，压缩率提升 3.09x）。

**技术要点**：
- 基础模型：SmolLM2（135M 参数）
- 轻量在线预测器集成（在 LLM 输出基础上校准）
- 32-bit 算术编码器，CDF 精度从 2^16→2^24（消除 75% 量化开销）
- 推理引擎：llama.cpp 后端，7x 更快
- **可在 GTX 1050 Ti 上运行**（仅 ~1.2 GB VRAM）

**更深层的意义**：Nacrith 的压缩率**低于数据的 0/1/2 阶 Shannon 熵**——这意味着传统基于 n-gram 的统计模型有根本性的局限，而神经网络捕获了更高阶的统计结构。

### 9.3 NNLCB 基准（2025 综合评估）

> 17 个基于神经网络的无损压缩器在 28 个数据集上 4600+ CPU/GPU 小时的评估。

| 类型 | 代表 | 特点 | 局限 |
|------|------|------|------|
| 静态预训练 | NNCP, Transformer 压缩 | 通用 | 泛化到未见数据差 |
| 自适应 | TRACE, SmallLlamaCoder | 边压缩边调整 | 速度慢 |
| 半自适应 | Nacrith, FineZip | 预训练 + 在线微调 | 内存占用高 |

**结论**：2025-2026 年神经网络压缩已进入实用初期，但**速度差距仍是主要瓶颈**——传统压缩器 Zstd 比 Nacrith 快 100-1000x。

### 9.4 具体实现方案：NNCP

> **Fabrice Bellard**（QEMU/TinyCC/ffmpeg 的作者）开发的 NNCP。

**NNCP 流水线**：
```
输入 → 预训练 LSTM/Transformer → 预测下一 token 概率
                                  ↓
                          算术编码器
```

**enwik8 上的 NNCP 结果**（v2.0, 2021）：
- LSTM: ~1.28 bpb
- Transformer: ~1.06 bpb
- 速度：~1-5 KB/s

### 9.5 学习型图像压缩（无损分支）

| 论文 | 年份 | 效果 | 方法 |
|------|------|------|------|
| FNLIC (CVPR 2025) | 2025 | 超越 PNG/WebP 无损 | 两阶段拟合 |
| L3C | 2019 | 接近 PNG 率 | 层次化概率模型 |
| iWave++ | 2021 | 超越 PNG | 小波 + NN |
| PEPIC | 2022 | 超越 FLIF | 位面 + NN 上下文 |

### 9.6 挑战与展望

| 挑战 | 具体表现 | 可能的解决方向 |
|------|---------|-------------|
| **速度** | NN 压缩器慢 100-1000x | 专用硬件（NPU）、蒸馏 |
| **泛化** | 到未见数据类型退化 | 基础模型、多模态预训练 |
| **内存** | 大模型需要 GPU | 量化、投机解码 |
| **可解释性** | 为什么压得好？ | 注意力分析、信息流追踪 |

> **预测**：2028-2030 年，首个达到 1MB/s 以上且压缩率超越 Zstd 10% 的 NN 压缩器将出现。在那之前，混合方案（传统 LZ + 小 NN 辅助预测）是最现实的路径。

---

## <a name="ch10"></a>第10章 实战：实现一个完整的压缩器

### 10.1 最小的可工作压缩器

以下实现一个**完整的 Huffman 编码压缩器**（核心功能），约 150 行 Python。

```python
from collections import Counter
import heapq

class HuffmanCoder:
    """Huffman 编码器"""
    
    class Node:
        def __init__(self, sym, freq, left=None, right=None):
            self.sym = sym      # 符号 (None 为内部节点)
            self.freq = freq    # 频率
            self.left = left    # 左子节点 (0)
            self.right = right  # 右子节点 (1)
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    def build_tree(self, data):
        """从数据构建 Huffman 树"""
        freq = Counter(data)
        heap = [self.Node(sym, f) for sym, f in freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            internal = self.Node(None, left.freq + right.freq, left, right)
            heapq.heappush(heap, internal)
        
        return heap[0] if heap else None
    
    def build_codes(self, node, prefix="", code_map=None):
        """从树构建编码表"""
        if code_map is None:
            code_map = {}
        if node.sym is not None:  # 叶节点
            code_map[node.sym] = prefix or "0"  # 单符号情况
        else:
            self.build_codes(node.left, prefix + "0", code_map)
            self.build_codes(node.right, prefix + "1", code_map)
        return code_map
    
    def encode(self, data):
        """编码数据"""
        if not data:
            return "", {}
        tree = self.build_tree(data)
        codes = self.build_codes(tree)
        encoded = ''.join(codes[b] for b in data)
        return encoded, codes
    
    def decode(self, encoded, codes):
        """解码数据"""
        if not encoded:
            return b""
        # 构建反向表
        reverse = {v: k for k, v in codes.items()}
        result = []
        code = ""
        for bit in encoded:
            code += bit
            if code in reverse:
                result.append(reverse[code])
                code = ""
        return bytes(result)

# 测试
coder = HuffmanCoder()
data = b"hello world this is a huffman coding test"
encoded, codes = coder.encode(data)
decoded = coder.decode(encoded, codes)

original_bits = len(data) * 8
compressed_bits = len(encoded)
print(f"原始大小: {original_bits} bits ({len(data)} bytes)")
print(f"压缩大小: {compressed_bits} bits")
print(f"压缩比: {original_bits/compressed_bits:.2f}x")
print(f"正确恢复: {data == decoded}")
print(f"编码表: {dict((chr(k),v) for k,v in codes.items() if chr(k).isprintable())}")
```

### 10.2 加入字典编码：最小 Deflate 子集

以下实现 LZ77（滑动窗口 + 最小匹配长度），与 Huffman 组合：

```python
class LZ77Coder:
    """LZ77 编码器（简化版）"""
    
    def __init__(self, window_size=2**15, min_match=3, max_match=258):
        self.window_size = window_size
        self.min_match = min_match
        self.max_match = max_match
    
    def search(self, data, pos):
        """在滑动窗口内搜索最长匹配"""
        start = max(0, pos - self.window_size)
        best_len = 0
        best_dist = 0
        
        for i in range(start, pos):
            match_len = 0
            while (pos + match_len < len(data) and 
                   data[i + match_len] == data[pos + match_len] and
                   match_len < self.max_match):
                match_len += 1
            if match_len > best_len:
                best_len = match_len
                best_dist = pos - i
        
        if best_len >= self.min_match:
            return best_dist, best_len
        return None, None
    
    def encode(self, data):
        """LZ77 编码"""
        tokens = []
        pos = 0
        while pos < len(data):
            dist, length = self.search(data, pos)
            if length is not None:
                tokens.append(('MATCH', dist, length))
                pos += length
            else:
                tokens.append(('LITERAL', data[pos]))
                pos += 1
        return tokens
    
    def decode(self, tokens):
        """LZ77 解码"""
        result = []
        for token in tokens:
            if token[0] == 'LITERAL':
                result.append(token[1])
            else:
                _, dist, length = token
                start = len(result) - dist
                for i in range(length):
                    result.append(result[start + i])
        return bytes(result)
```

### 10.3 bzip2 实现：BWT + MTF + RLE + Huffman

关键步骤的 Python 实现：

```python
def bwt(data):
    """Burrows-Wheeler 变换"""
    n = len(data)
    rotations = sorted(data[i:] + data[:i] for i in range(n))
    last_column = bytes(r[-1] for r in rotations)
    original_index = rotations.index(data)
    return last_column, original_index

def inverse_bwt(last_column, original_index):
    """逆 Burrows-Wheeler 变换"""
    n = len(last_column)
    first_column = sorted(last_column)
    
    # 构建下一跳映射
    next_pos = {}
    used = {}
    for i, ch in enumerate(first_column):
        # 找到 last_column 中每个字符在 first_column 中的对应位置
        if ch not in used:
            used[ch] = 0
        # 这里简化了——实际需要更精确的映射
        idx = used[ch]
        for j, c in enumerate(last_column):
            if c == ch:
                if idx == 0:
                    next_pos[i] = j
                    break
                idx -= 1
        used[ch] = used.get(ch, 0) + 1
    
    result = []
    pos = original_index
    for _ in range(n):
        pos = next_pos[pos]
        result.append(first_column[pos])
    
    return bytes(result)

def mtf_encode(data, alphabet=None):
    """移动到前端编码"""
    if alphabet is None:
        alphabet = sorted(set(data))
    result = []
    for ch in data:
        idx = alphabet.index(ch)
        result.append(idx)
        alphabet = [ch] + alphabet[:idx] + alphabet[idx+1:]
    return result
```

### 10.4 性能测量框架

```python
import time
import os

def benchmark_compressor(compress_fn, decompress_fn, data_path):
    """测量压缩/解压的性能"""
    data = open(data_path, 'rb').read()
    original_size = len(data)
    
    # 压缩
    t0 = time.time()
    compressed = compress_fn(data)
    t1 = time.time()
    compress_time = t1 - t0
    compressed_size = len(compressed) if isinstance(compressed, bytes) else len(compressed[0])
    
    # 解压
    t0 = time.time()
    decompressed = decompress_fn(compressed)
    t1 = time.time()
    decompress_time = t1 - t0
    
    # 验证
    correct = data == decompressed
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'ratio': original_size / compressed_size,
        'compress_time': compress_time,
        'decompress_time': decompress_time,
        'compress_speed': original_size / compress_time / 1e6,
        'decompress_speed': original_size / decompress_time / 1e6,
        'bpb': compressed_size * 8 / original_size,
        'correct': correct
    }
```

### 10.5 常见陷阱

| 陷阱 | 表现 | 解决方法 |
|------|------|---------|
| **元数据开销忽略** | 小文件压缩后变大 | 对 <256 字节文件不做压缩 |
| **算术编码精度** | 编解码不一 | 使用 64-bit 状态 + 重标准化 |
| **BWT 唯一结束符** | 逆变换失败 | 必须使用原数据中没有的唯一标记 |
| **LZ 流式解压** | 编码器和解码器滑动窗口不同步 | 两端的窗口初始化和更新策略一致 |
| **大文件单块 Huffman** | 表传输开销太大 | 分块（如 64KB）独立编码 |
| **二进制模式下 EOF** | 解码提前终止 | 在输出头部存储原始大小 |

---

## <a name="ch11"></a>第11章 未来展望：从压缩到理解

### 11.1 压缩即理解的哲学再审视

Hinton 2019 年标志性论述："要压缩好一个数据流，你必须**理解**它。" 这不仅是一个比喻——当 Chinchilla 70B 以 0.664 bpb 压缩 enwik9 时，它确实展现了对其内容的深刻理解：它知道"牛顿"后面应该接"苹果"而不是"香蕉"，知道"芯片"和"晶体管"的相关性。

**推论**：如果一个 AI 系统能将某个领域的数据压缩到极致，那它**本质上掌握了该领域的知识结构**。反之亦然：训练一个更好的压缩器等价于训练一个更深入理解领域数据的模型。

### 11.2 大语言模型即是终极压缩器

这个观点正在从哲学变为工程现实：

```
LLM 训练 = 压缩互联网 → 压缩率 0.x bpb
LLM 问答 = 有条件地解压 → 给定指令，生成相应的"解压产物"
LLM 推理 = 寻找最符合上下文的下一步预测
```

**数学模型**：LLM 的 loss（交叉熵）在所有 token 上的平均值**正好是**该模型作为压缩器时的 bpb。所以：
- GPT-3 的 loss ~2.0 → 作为压缩器约 2.0 bpb
- Chinchilla 70B 的 loss ~0.664 → 作为压缩器 0.664 bpb
- 人类阅读速度 ≈ 4.3 bpb（实验测量）

### 11.3 分离定理的终结？

Shannon 分离定理说：无限长码下源编码和信道编码可独立设计。但在**非渐近**（短码、低时延）和**智能体**（主动感知、主动通信）场景中，这个定理的假设不成立：

| 场景 | 分离定理适用？ | 新方向 |
|------|-------------|-------|
| 经典长码通信 | ✅ 适用 | — |
| URLLC（5G 短包） | ❌ 不适用 | 深度 JSCC |
| 语义通信 | ❌ 不适用 | 语义信道编码 |
| AI Agent 通信 | ❌ 不适用 | 概念级压缩、共享表征 |

**面向智能体的压缩**：两个 AI Agent 之间的通信不需要传输原始比特，而是传输"理解"。例如："帮我查昨天那条新闻" ≈ 几十字节的理解指令，而非传输完整的文章。

### 11.4 未来 5 年的技术路线预测

```
2026-2027: 混合压缩器（LZ + 小 NN 预测器）开始取代纯 LZ 方案
           └── 压缩率接近 CMIX 但速度提升 100x

2027-2028: 首个 1MB/s 以上的 NN 压缩器
           └── 面向特定领域（文本、基因组、日志）

2028-2029: 基础模型作为通用压缩器
           └── 统一框架：压缩、理解、生成三合一

2029-2030: 语义级压缩进入产品
           └── 不传 bits，传 meanings
```

### 11.5 对编程和工程的影响

| 领域 | 影响 | 具体变化 |
|------|------|---------|
| **数据库** | 列级智能压缩引擎 | 自动选择最佳模型+字典 |
| **网络协议** | 内容感知的传输编码 | 根据内容类型自动选择/适应压缩算法 |
| **存储系统** | 学习型索引+压缩 | 理解存储的数据并联合优化 |
| **编译器** | 代码的"压缩等价于优化" | 寻找更短但等价的程序表示 |
| **AI 训练** | 压缩即训练数据筛选 | 压缩率低 = 信息量高 = 更好的训练样本 |

### 11.6 极限思考

**终极问题**：如果 Kolmogorov 复杂度 K(s) 不可计算，我们怎么知道压缩到了极限？

答案：**不知道，也不需要知道。**

压缩的意义不在于"有没有达到极限"，而在于**不断逼近极限的过程本身就是理解的过程**。每一次更好的压缩都意味着更深入的理解。这是"压缩"这条线索贯穿信息论、机器学习和人工智能的根本原因。

**一个更大胆的猜想**：通用人工智能的必要条件之一，就是能够将任何观察到的数据压缩到它的 Kolmogorov 复杂度——这等价于理解该数据的生成过程。换言之，**一个完美的通用压缩器就是一个通用人工智能**。

---

## 附录：术语表

### 核心理论

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| 熵 | Entropy | 信息量的度量，压缩的理论下限 | 评估压缩器效率时 |
| 条件熵 | Conditional Entropy | 给定已知信息后的不确定性 | 分析上下文模型的增益 |
| 交叉熵 | Cross Entropy | 用错误模型编码的代价 | 机器学习 loss 函数、LLM 评估 |
| KL 散度 | KL Divergence | 两个概率分布的差异 | 模型选择、分布偏移检测 |
| 互信息 | Mutual Information | 两个变量共享的信息量 | 特征选择、降维 |
| Kolmogorov 复杂度 | Kolmogorov Complexity | 字符串的最短描述长度 | 理论极限讨论、哲学分析 |
| 源编码定理 | Source Coding Theorem | 熵是压缩的不可达上限 | 证明最优性时 |
| 率失真理论 | Rate-Distortion | 给定失真下的最小比特率 | 有损压缩的理论基础 |

### 统计编码

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| 前缀码 | Prefix Code | 无任何码字是另一码字的前缀 | Huffman 编码的设计基础 |
| Shannon-Fano 编码 | Shannon-Fano Coding | 最早的熵编码（不保证最优） | 了解信息论历史时 |
| Huffman 编码 | Huffman Coding | 最优前缀码，整数比特 | 通用压缩的基础 |
| 规范 Huffman | Canonical Huffman | 只存储码长，按规则重建码表 | 实际文件格式(ZIP/PNG)中 |
| 算术编码 | Arithmetic Coding | 非整数比特的熵编码 | 需要接近熵极限时 |
| 重标准化 | Renormalization | 算术编码的精度管理 | 实现算术编码器时 |
| ANS | Asymmetric Numeral Systems | 兼具速度和效率的熵编码 | 现代压缩器（Zstd/FSE） |
| tANS | Table-based ANS | 用查找表实现的 ANS | Zstd 的 FSE 实现 |
| PPM | Prediction by Partial Matching | 多阶上下文建模 + 算术编码 | 高压缩率文本压缩 |
| 上下文混合 | Context Mixing | 多个模型的加权预测 | PAQ/CMIX 的核心 |
| 逃逸机制 | Escape Mechanism | PPM 中处理未见序列的机制 | 实现 PPM 压缩器时 |

### 字典编码

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| LZ77 | LZ77 | 滑动窗口 + 匹配指针 | ZIP/Deflate/gzip 的核心 |
| LZSS | LZSS | 带最小匹配长度的 LZ77 | LZSS 优化的讨论 |
| LZ78 | LZ78 | 全局增长字典 | Unix compress (LZW) |
| LZW | LZW | LZ78 的实用版本 | GIF、早期 Unix 工具 |
| Deflate | Deflate | LZ77 + Huffman | ZIP、gzip、PNG |
| LZMA | LZMA | LZ77 + 区间编码 + 大字典 | 7-Zip |
| 滑动窗口 | Sliding Window | LZ77 的有限历史存储 | 实现 LZ77 时 |
| 哈希链 | Hash Chain | LZ77 匹配搜索的加速结构 | 优化 LZ77 性能时 |
| 字典训练 | Dictionary Training | 预训练特定领域字典 | Zstd --train 的使用 |

### 块变换

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| BWT | Burrows-Wheeler Transform | 可逆的块排序变换 | bzip2 的核心 |
| 逆 BWT | Inverse BWT | BWT 的解码过程 | 实现 bzip2 解码器时 |
| MTF | Move-to-Front | 将高频符号移到列表前端 | BWT 后的处理 |
| RLE | Run-Length Encoding | 游程长度编码 | BMP、传真、BWT 后 |

### 现代压缩器

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| Zstd | Zstandard | Facebook 的现代压缩器 | 通用压缩的第一选择 |
| FSE | Finite State Entropy | Zstd 使用的 tANS 实现 | 分析 Zstd 内核时 |
| Brotli | Brotli | Google 的 Web 压缩器 | HTTPS 内容编码 |
| LZ4 | LZ4 | 极速 LZ77 变体 | 实时/内存压缩 |
| Snappy | Snappy | Google 的快速压缩库 | BigData 列式存储 |
| XZ/LZMA2 | XZ Utils | 极致压缩率 | 归档/发行版包体 |

### 纠错和恢复

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| 纠错码 | Error-Correcting Code | 添加冗余以纠正传输错误 | 信道编码 |
| Reed-Solomon | Reed-Solomon Code | 基于多项式的纠错码 | QR 码、光盘、卫星通信 |
| LDPC | Low-Density Parity-Check | 稀疏校验矩阵的线性码 | 5G、Wi-Fi 6 |
| 喷泉码 | Fountain Code | 无速率码 | 大规模文件广播 |
| 分离定理 | Separation Theorem | 源/信道编码可独立设计 | 通信系统设计决策 |
| JSCC | Joint Source-Channel Coding | 压缩+纠错联合设计 | 短包/低延迟场景 |
| 深度 JSCC | Deep JSCC | 用 NN 做联合源信道编码 | 无线图像传输 |

### 神经网络压缩

| 术语 | English | 说明 | 何时用到 |
|------|---------|------|---------|
| NNCP | Neural Network Compression | Fabrice Bellard 的 NN 压缩器 | 学习压缩入⻔ |
| CMIX | CMIX | 当前压缩率最高的压缩器 | 极致压缩比较 |
| Nacrith | Nacrith | 2026 新突破，135M 参数 | 学习压缩最新进展 |
| enwik8 | enwik8 | 100MB Wikipedia 基准 | 压缩器性能比较 |
| bpb | bits per byte | 每字节的比特数，越低越好 | 所有压缩率报告 |
| 语言建模即压缩 | Language Modeling is Compression | DeepMind 2023 论文 | 理解 LLM 与压缩的关系 |

---

> **版本**：v1.0 · 2026-05-16 · 三部曲之 A：深度技术手册
>
> **核心参考文献**：
> - Shannon, C.E. (1948) *A Mathematical Theory of Communication*. Bell System Technical Journal
> - Cover, T.M. & Thomas, J.A. (2006) *Elements of Information Theory*, 2nd Ed. Wiley
> - Salomon, D. (2007) *Data Compression: The Complete Reference*, 4th Ed. Springer
> - Sayood, K. (2017) *Introduction to Data Compression*, 5th Ed. Morgan Kaufmann
> - Mahoney, M. *Data Compression Explained*. http://mattmahoney.net/dc/dce.html
> - Collet, Y. Zstandard - Real-time data compression algorithm. https://github.com/facebook/zstd
> - Duda, J. (2014) *Asymmetric Numeral Systems: Entropy Coding Combining Speed of Huffman Coding with Compression Rate of Arithmetic Coding*
> - Burrows, M. & Wheeler, D.J. (1994) *A Block-sorting Lossless Data Compression Algorithm*. Digital SRC Research Report 124
> - Deletang, G. et al. (2024) *Language Modeling is Compression*. ICLR 2024
> - Nacrith (2026) *Neural Network Lossless Compression at 0.9389 bpb on enwik8*
> - NNLCB Benchmark (2025) *A survey and benchmark evaluation for neural-network-based lossless universal compressors*
