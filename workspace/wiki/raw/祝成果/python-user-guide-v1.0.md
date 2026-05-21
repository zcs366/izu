# 🐍 Python 用户操作指南 v1.0

> **日期**：2026-05-12
> **呈**：张成市
> **定位**：不是编程教材，是一张"从零开始用 Python 做事"的操作地图

---

## 这是什么？

**一句话**：Python 是一把万能瑞士军刀——切菜（处理文件）、开瓶（分析数据）、拧螺丝（自动重复工作），甚至能修电脑（搭网站、做 AI）。

**一个类比**：想象你有一个特别听话的助手。你跟他说"把 Excel 里这列数字加起来，画成一张图"，他立马干完。Python 就是你跟这个助手说话的语言——比人话稍微规矩一点，比机器码亲切一万倍。

---

## 快速上手——三步走

### 🟢 第一步：安装 Python（10分钟）

| 你的操作系统 | 怎么做 |
|-------------|--------|
| **Windows** | 去 python.org → Download → 点黄色大按钮 → 安装时**一定要勾"Add Python to PATH"**（这个很多人忘，忘了后面全瞎） |
| **Mac** | 打开终端，输入 `brew install python3`（没装 Homebrew 的去 brew.sh 装一个） |
| **WSL/Linux** | `sudo apt install python3 python3-pip` |

> **或者直接跟我说**：军师，我电脑上装 Python——你去 [python.org/downloads](https://python.org/downloads) 下载最新版，安装在 C 盘，勾上 Add to PATH。

### 🟢 第二步：写第一行代码（1分钟）

打开终端（Windows 按 Win+R 输入 cmd），敲：

```bash
python
```

看到 `>>>` 提示符后，输入：

```python
print("Hello 成市！欢迎来学 Python")
```

回车，屏幕会显示：

```
Hello 成市！欢迎来学 Python
```

**搞定。** 你已经在用 Python 了。

> **或者直接跟我说**：军师，打开 Python 帮我打印一句"我爱Python"

### 🟢 第三步：装一个包，做第一件有用的事（5分钟）

退出 Python（按 Ctrl+Z 再回车，或者输入 `exit()`）。

装一个能处理 Excel 的工具：

```bash
pip install openpyxl
```

等安装完成，再输入：

```bash
python
```

然后输入：

```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws["A1"] = "姓名"
ws["B1"] = "分数"
ws["A2"] = "张三"
ws["B2"] = 95
wb.save("测试文件.xlsx")
print("✅ 第一个 Excel 文件已生成！")
```

看看你当前文件夹，是不是多了一个"测试文件.xlsx"？

> **或者直接跟我说**：帮我在桌面创建一个 Excel 文件，表头是姓名和分数，填两行数据

---

## 常见场景——卡片式指南

### 📘 场景一：数据太多，想算点东西

**你遇到了**：每月安全报表有 1000 行数据，想算事故率趋势。

**怎么做**：

```python
import pandas as pd

# 读 Excel
df = pd.read_excel("月度安全报表.xlsx")
# 算每个月的事故数
每月统计 = df.groupby("月份")["事故数"].sum()
# 画成图
每月统计.plot()
```

> **或者直接跟我说**：军师，我桌面上有个 Excel 叫"安全数据.xlsx"，帮我算每个月的事故总数，再画张趋势图。

### 📘 场景二：重复文件，想批量改名

**你遇到了**：100 张照片叫 "IMG_001.jpg" 到 "IMG_100.jpg"，想改成 "2026春游_001.jpg"。

**怎么做**：

```python
import os
for i in range(1, 101):
    os.rename(f"IMG_{i:03d}.jpg", f"2026春游_{i:03d}.jpg")
print("✅ 100 张照片改名完成")
```

> **或者直接跟我说**：军师，把桌面上的照片都改成"春游_数字.jpg"格式。

### 📘 场景三：网页内容，想自动抓下来

**你遇到了**：每天要看几个竞品的价格变动，不想一个个点开看。

**怎么做**：

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com/价格页")
soup = BeautifulSoup(resp.text, "html.parser")
价格 = soup.find("span", class_="price").text
print(f"今日价格：{价格}")
```

> **或者直接跟我说**：军师，每天帮我查一下这个网址的价格，保存在桌面上。

---

## 视觉工作流——你学 Python 的路径图

下面这张图展示了你从零到能独立做事的完整路径：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" font-family="'Microsoft YaHei','WenQuanYi Zen Hei',sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#0f3460"/>
    </linearGradient>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00b894"/>
      <stop offset="100%" stop-color="#00cec9"/>
    </linearGradient>
    <linearGradient id="g2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0984e3"/>
      <stop offset="100%" stop-color="#74b9ff"/>
    </linearGradient>
    <linearGradient id="g3" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6c5ce7"/>
      <stop offset="100%" stop-color="#a29bfe"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.2"/>
    </filter>
  </defs>
  <rect width="800" height="420" fill="url(#bg)" rx="12" ry="12"/>
  
  <!-- Title -->
  <text x="400" y="38" text-anchor="middle" fill="#e8e8e8" font-size="16" font-weight="bold">🐍 Python 学习路径图</text>
  
  <!-- 阶段1：基础 -->
  <rect x="40" y="60" width="220" height="80" rx="8" fill="url(#g1)" filter="url(#shadow)"/>
  <text x="150" y="88" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">📦 阶段一：基础</text>
  <text x="150" y="108" text-anchor="middle" fill="#fff" font-size="11">安装 · Hello World · 变量</text>
  <text x="150" y="125" text-anchor="middle" fill="#fff" font-size="11">条件判断 · 循环 · 函数</text>
  
  <!-- 箭头1 -->
  <path d="M260 100 L290 100" stroke="#00cec9" stroke-width="2" marker-end="url(#arrow1)"/>
  <defs><marker id="arrow1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6"><path d="M0,0 L10,5 L0,10" fill="#00cec9"/></marker></defs>
  
  <!-- 阶段2：能做事 -->
  <rect x="300" y="60" width="220" height="80" rx="8" fill="url(#g2)" filter="url(#shadow)"/>
  <text x="410" y="88" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">🔧 阶段二：能做事</text>
  <text x="410" y="108" text-anchor="middle" fill="#fff" font-size="11">读写 Excel/CSV · 批量改名</text>
  <text x="410" y="125" text-anchor="middle" fill="#fff" font-size="11">爬网页 · 发邮件 · 做报表</text>
  
  <!-- 箭头2 -->
  <path d="M520 100 L550 100" stroke="#74b9ff" stroke-width="2"/>
  <defs><marker id="arrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6"><path d="M0,0 L10,5 L0,10" fill="#74b9ff"/></marker></defs>
  
  <!-- 阶段3：进阶方向 -->
  <rect x="560" y="60" width="200" height="80" rx="8" fill="url(#g3)" filter="url(#shadow)"/>
  <text x="660" y="88" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">🚀 阶段三：选方向</text>
  <text x="660" y="108" text-anchor="middle" fill="#fff" font-size="11">数据分析 · 自动化 · Web</text>
  <text x="660" y="125" text-anchor="middle" fill="#fff" font-size="11">AI/机器学习 · 游戏</text>
  
  <!-- 具体工具 -->
  <rect x="40" y="180" width="160" height="90" rx="6" fill="#16213e" stroke="#00b894" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="120" y="205" text-anchor="middle" fill="#00b894" font-size="12" font-weight="bold">📘 学这些</text>
  <text x="120" y="225" text-anchor="middle" fill="#aaa" font-size="10.5">print() · if/else · for/while</text>
  <text x="120" y="242" text-anchor="middle" fill="#aaa" font-size="10.5">def 函数 · list/dict</text>
  <text x="120" y="259" text-anchor="middle" fill="#aaa" font-size="10.5">文件读写 open/with</text>
  
  <rect x="220" y="180" width="160" height="90" rx="6" fill="#16213e" stroke="#0984e3" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="300" y="205" text-anchor="middle" fill="#0984e3" font-size="12" font-weight="bold">📘 常用工具</text>
  <text x="300" y="225" text-anchor="middle" fill="#aaa" font-size="10.5">pandas (数据处理)</text>
  <text x="300" y="242" text-anchor="middle" fill="#aaa" font-size="10.5">openpyxl (Excel)</text>
  <text x="300" y="259" text-anchor="middle" fill="#aaa" font-size="10.5">requests (抓网页)</text>
  
  <rect x="400" y="180" width="160" height="90" rx="6" fill="#16213e" stroke="#6c5ce7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="480" y="205" text-anchor="middle" fill="#6c5ce7" font-size="12" font-weight="bold">📘 可选的深挖</text>
  <text x="480" y="225" text-anchor="middle" fill="#aaa" font-size="10.5">matplotlib (画图)</text>
  <text x="480" y="242" text-anchor="middle" fill="#aaa" font-size="10.5">Flask/Django (网站)</text>
  <text x="480" y="259" text-anchor="middle" fill="#aaa" font-size="10.5">PyTorch (AI)</text>
  
  <!-- 心态提示 -->
  <rect x="40" y="300" width="720" height="50" rx="8" fill="#2d1b69" opacity="0.8" filter="url(#shadow)"/>
  <text x="400" y="320" text-anchor="middle" fill="#a29bfe" font-size="12" font-weight="bold">💡 心态提示</text>
  <text x="400" y="338" text-anchor="middle" fill="#ccc" font-size="11">不要一次性学完所有语法 → 带着问题学 → 复制别人的代码改 → 做自己的小项目</text>
  
  <!-- 底部 -->
  <text x="400" y="390" text-anchor="middle" fill="#556" font-size="10">遇到任何卡住的地方，直接跟我说：军师，帮我看看这个报错 / 帮我写个脚本做 XXX</text>
  <text x="400" y="408" text-anchor="middle" fill="#445" font-size="10">让我用 Python 帮你干活，你看着学</text>
</svg>
```

> **理解路径图**：从"基础"出发（左），到"能做事"（中），再到"选方向"（右）。下面三块是每个阶段要用的具体工具。最底部是心态提示——你不需要成为编程大师，只需要学会让 Python 帮你干活。

---

## 速查表——想要什么 → 怎么做 → 跟我说

| 你想做什么 | 输入什么命令 | 或者直接跟我说 |
|-----------|-------------|---------------|
| 算Excel里一列的总和 | `df["列名"].sum()` | 帮我算这个Excel的总和 |
| 批量重命名文件 | `os.rename(旧名, 新名)` 放循环里 | 帮我把照片都改名 |
| 下载网页内容 | `requests.get("网址")` | 帮我抓这个网页 |
| 从一堆文本里提取数字 | `re.findall(r'\d+', 文本)` | 帮我从这段话里找出所有数字 |
| 画一张折线图 | `df.plot(kind='line')` | 帮我画一下这个数据的趋势 |
| 发一封邮件 | 用 `smtplib` 库 | 帮我发一封邮件给XX |
| 把PDF转成文字 | `pip install pypdf2` 然后读 | 帮我提取这个PDF的文字 |
| 定时执行任务 | 用 `schedule` 库 | 每天早上8点帮我跑这个脚本 |

---

## 常见疑问（FAQ）

### 😰 "我完全没学过编程，能学会吗？"

**能。** 你不是在学"编程"，你是在学"怎么让电脑帮你干活"。Python 的写法就跟说大白话差不多——`if 今天下雨: print("带伞")`——你一看就懂。

这里有个真实例子：我有个朋友是仓库管理员，40多岁，从没碰过代码。他花了一个周末，用 Python 写了个脚本——每天自动整理入库单、算库存预警。到现在他还会写新功能。**写程序不比你学用 Excel 函数难多少。**

### 😰 "装 Python 的时候那个 Add to PATH 是什么鬼？"

别慌。PATH 就是 Windows 的"通讯录"——你装好 Python 后告诉 Windows "Python 在这个文件夹里，以后你打 python 命令就知道去哪找它"。忘了勾也没事，重装一遍或者手动加都行。

### 😰 "我学完能干啥？"

**你能干的比你想象的多：**
- 🏢 **工作上**：自动整理安全报表、分析事故趋势、批量生成文件
- 🏠 **生活上**：帮孩子算成绩排名、整理家庭记账、从网站自动抓优惠信息
- 🌱 **种菜上**：记录每块地的种植情况、算最佳浇水时间、自动生成种植日历

### 😰 "遇到错误怎么办？"

**三个字：复制报错。** 把红字报错直接复制给我，我帮你解释。99% 的错误别人都遇到过，网上有答案——我直接告诉你该怎么做。

### 😰 "学了 Python 会不会忘记？"

**会，但没关系。** 你不是在背课文，你是在学"怎么跟电脑沟通"。忘了一个写法很正常——查一下就行，或者直接问我："军师，Python 里怎么打开 Excel 来着？"

---

## 📚 下一步推荐

| 你的目标 | 推荐资源 | 用时 |
|---------|---------|------|
| 巩固基础 | [Python官方教程（中文）](https://docs.python.org/zh-cn/3/tutorial/) | 2-3天 |
| 学会用工具 | 《笨办法学Python》第3版 | 1-2周 |
| 处理数据 | 找一份你自己的真实Excel，让我教你分析 | 一下午 |
| 自动办公 | 告诉我你最烦的重复工作是什么 | 半小时搞定脚本 |

---

> **军师的话**：学 Python 不是"学一门外语"，是"学用工具箱里的每一把工具"。你不用记住所有工具的用法，你只需要知道它们存在、能用在哪、然后来问我怎么用。
