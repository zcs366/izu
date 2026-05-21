# 🔀 路由与网关 · 深度技术手册 v1.0

> **从 IP 包转发的第一跳，到 BGP 骨干网的最后一公里。**
>
> 写给：开发者、运维工程师、网络学习者——不畏惧终端和路由表的人。

---

## 第一章 概览与核心理念

### 1.1 一个比喻，管一辈子

把互联网想象成**全世界的邮政系统**：

| 网络概念 | 邮政类比 |
|---------|---------|
| IP 数据包 | 一封信 |
| IP 地址 | 门牌号 |
| 子网掩码 | 街区范围（这条街从 1 号到 200 号） |
| 网关 | **城门**——你寄出所有信的唯一出口 |
| 路由表 | **邮递员脑子里的地图**——"去上海走京沪线，去广州走京广线" |
| 路由协议 | 邮递员之间交换路线信息（"京沪线塌了，改走沿海线"） |
| NAT | 传达室大爷——把你的内部门牌号翻译成临时外部编号 |
| TTL | 信封上的"最多转手次数"，到 0 就退回 |

**路由**回答的问题是：**"这封信，下一步交给谁？"**

**网关**回答的问题是：**"这封信怎么出这个网络？"**

> 💡 每一台连网的设备都有一个路由表。你的手机有，服务器有，连智能灯泡都有。只不过大多数设备的路由表只有一行：**"不知道去哪的，统统扔给网关"**。

### 1.2 路由的本质：逐跳转发

路由不是事先规划好整条路径，而是**每一跳独立决策**：

```
你 (192.168.1.10)
  │  查路由表：目的地不在本网段
  │  下一跳 = 192.168.1.1（网关）
  ▼
网关 (192.168.1.1 + 公网IP)
  │  查路由表：去 110.242.68.0/24 走运营商A
  │  下一跳 = 10.0.0.1（运营商接入路由器）
  ▼
运营商路由器 A
  │  查路由表：去 110.242.68.0/24 走骨干网
  │  下一跳 = BGP邻居
  ▼
  ... (经过 5-30 跳)
  ▼
目标服务器 (110.242.68.66)
```

每台路由器只看**目的IP地址**，查自己的路由表，决定扔给哪个邻居。这不叫"规划路线"，这叫**分布式协作**。

### 1.3 网关的三重身份

"网关"这个词在不同语境下指不同东西：

| 语境 | 含义 | 实例 |
|------|------|------|
| **默认网关** (Default Gateway) | 局域网内所有设备的出口路由器 | `192.168.1.1` |
| **协议网关** | 连接不同协议的网络（如 IPX↔TCP/IP） | 历史上常见，现在少见 |
| **应用网关** | 应用层的代理/转换 | API Gateway, 邮件网关, 短信网关 |

本手册主要讨论前两者。应用网关（API Gateway）将在云原生语境中涉及。

### 1.4 路由协议全景图

```
路由协议
├── 静态路由 —— 手工配置，简单但不灵活
└── 动态路由
    ├── 内部网关协议 (IGP) —— 同一个自治系统内部用
    │   ├── 距离矢量类
    │   │   ├── RIP (Routing Information Protocol) —— 古老，跳数定胜负
    │   │   └── EIGRP (Enhanced IGRP) —— Cisco专有，混合型
    │   └── 链路状态类
    │       ├── OSPF (Open Shortest Path First) —— 企业标配
    │       └── IS-IS (Intermediate System to IS) —— 运营商最爱
    └── 外部网关协议 (EGP) —— 自治系统之间用
        └── BGP (Border Gateway Protocol) —— 互联网的脊梁
```

**自治系统 (AS)** = 一个机构统一管理的网络集合。中国电信是一个 AS，阿里云是一个 AS，你公司也可以申请一个 AS。每个 AS 有一个唯一的 AS 号 (ASN)。

---

## 第二章 部署全指南

### 2.1 家用路由器部署

这是最简单也最常见的场景。现代家用路由器本质上是一个运行着 Linux 的小型计算机，集成了：
- **路由功能**（转发 IP 包）
- **NAT 功能**（私网↔公网地址转换）
- **DHCP 服务器**（自动分配 IP）
- **DNS 代理**（域名解析转发）
- **防火墙**（包过滤）
- **WiFi AP**（无线接入点）

**典型部署步骤**：

```bash
# 1. 物理连接
光猫 LAN口 ──网线── 路由器 WAN口
路由器 LAN口 ──网线── 电脑

# 2. 登录管理页
浏览器打开 http://192.168.1.1 （或 192.168.0.1）
# 登录凭据通常在路由器底部贴纸上

# 3. 基本设置
- WAN口设置：PPPoE拨号（输入宽带账号密码）/ DHCP自动获取
- LAN口设置：内网IP段 192.168.1.0/24，网关 192.168.1.1
- WiFi设置：SSID + WPA2密码
- DHCP设置：地址池 192.168.1.100 - 192.168.1.200
```

### 2.2 软路由（x86 路由器）

软路由 = 用普通 PC/工控机 + 路由操作系统，替代家用硬路由。

**为什么用软路由？**
- 性能：x86 CPU 远比家用路由器芯片强，NAT 吞吐量可达千兆甚至万兆
- 功能：插件生态丰富（去广告、科学上网、流量控制、Docker）
- 可控：完全掌控系统，不依赖厂商固件更新

**主流软路由系统**：

| 系统 | 特点 | 适合人群 |
|------|------|---------|
| **OpenWrt** | Linux内核，插件海量，社区活跃 | 喜欢折腾的玩家 |
| **pfSense** | FreeBSD，企业级防火墙功能 | 小型企业 |
| **OPNsense** | pfSense 的友好分支，界面更现代 | 中小团队 |
| **VyOS** | CLI 驱动，类 Cisco 命令 | 网络工程师 |
| **iKuai** (爱快) | 中文界面，流控见长 | 网吧/中小企业 |

**OpenWrt 安装示例**：

```bash
# 1. 下载固件（选 x86/64 版本）
# https://firmware-selector.openwrt.org/

# 2. 制作启动盘
dd if=openwrt-x86-64-generic-squashfs-combined.img of=/dev/sdX bs=4M

# 3. 启动后登录
ssh root@192.168.1.1
# 初始无密码，立即设置：
passwd

# 4. 基础配置
uci set network.lan.ipaddr='192.168.1.1'
uci commit network
/etc/init.d/network restart
```

### 2.3 企业路由器部署

企业路由器（Cisco IOS / IOS-XE、华为 VRP、Juniper JunOS）的核心部署模式：

```
                    ┌──────────┐
        ┌───────────┤ 核心路由器 ├──────────┐
        │           └──────────┘          │
   ┌────▼────┐                      ┌────▼────┐
   │ 汇聚交换机│                      │ 汇聚交换机│
   └────┬────┘                      └────┬────┘
   ┌────▼────────────────────────────────▼────┐
   │              接入层交换机                    │
   └────┬────────┬────────┬────────┬───────────┘
      [PC]    [PC]    [PC]    [打印机]
```

**Cisco IOS 基础配置示例**：

```cisco
! 进入特权模式
enable
configure terminal

! 配置接口IP
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 no shutdown

! 配置静态路由
ip route 0.0.0.0 0.0.0.0 203.0.113.2   ! 默认路由指向运营商
ip route 192.168.2.0 255.255.255.0 10.0.0.2  ! 去往分部网络

! 配置NAT
interface GigabitEthernet0/1
 ip nat outside
interface GigabitEthernet0/0
 ip nat inside
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

! 保存配置
write memory
```

### 2.4 云网关

在云环境中，"网关"的概念被抽象为服务：

| 云服务 | AWS | Azure | GCP |
|--------|-----|-------|-----|
| Internet 网关 | Internet Gateway | Azure Internet | Cloud NAT / IGW |
| NAT 网关 | NAT Gateway | NAT Gateway | Cloud NAT |
| VPN 网关 | VPN Gateway | VPN Gateway | Cloud VPN |
| 路由表 | Route Table | Route Table | Routes / VPC Network |
| 中转网关 | Transit Gateway | Virtual WAN | Network Connectivity Center |

**AWS VPC 路由表示例**：

```
目标              下一跳
10.0.0.0/16      local           ← VPC内部流量走本地
0.0.0.0/0        igw-xxxx       ← 所有出站流量走Internet Gateway
172.16.0.0/12    vgw-xxxx       ← 去往VPN的流量走虚拟私有网关
```

> 💡 云路由表的本质和物理路由器完全一样——都是"查目的地址 → 找下一跳"。只不过"下一跳"从物理接口变成了虚拟资源 ID。

### 2.5 Linux 作为路由器

任何一台 Linux 机器都可以变成路由器：

```bash
# 1. 开启IP转发（核心一步！）
echo 1 > /proc/sys/net/ipv4/ip_forward
# 永久生效：
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# 2. 配置接口
ip addr add 192.168.1.1/24 dev eth0    # 内网口
ip addr add 203.0.113.2/30 dev eth1    # 外网口

# 3. 配置NAT（MASQUERADE = 动态SNAT）
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
# nftables 等价写法：
nft add table ip nat
nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }
nft add rule ip nat postrouting oif eth1 masquerade

# 4. 添加静态路由
ip route add 10.0.0.0/8 via 203.0.113.1
```

---

## 第三章 路由表——核心数据结构

### 3.1 看懂路由表

```bash
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eno1
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eno1
169.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 eno1
```

解读每一行：

| 行 | 含义 |
|----|------|
| `0.0.0.0/0 → 192.168.1.1` | **默认路由**——不知道去哪的包，扔给网关 `192.168.1.1` |
| `192.168.1.0/24 → eno1` | **直连路由**——发给局域网内设备的包，直接从 `eno1` 网口出 |
| `169.254.0.0/16 → eno1` | **链路本地**——DHCP 失败时的自救地址，一般不用管 |

### 3.2 路由查找规则：最长前缀匹配

当路由表中有多条可能匹配的条目时，路由器选择**子网掩码最长**的那条：

```
路由表：
10.0.0.0/8      → 下一跳 A
10.1.0.0/16     → 下一跳 B
10.1.2.0/24     → 下一跳 C

目的地 10.1.2.5：
  ✓ 匹配 10.0.0.0/8  （掩码长度 8）
  ✓ 匹配 10.1.0.0/16 （掩码长度 16）
  ✓ 匹配 10.1.2.0/24 （掩码长度 24）← 最长，选这个 → 下一跳 C

目的地 10.1.3.5：
  ✓ 匹配 10.0.0.0/8  （掩码长度 8）
  ✓ 匹配 10.1.0.0/16 （掩码长度 16）
  ✗ 不匹配 10.1.2.0/24
  → 最长匹配 = 10.1.0.0/16 → 下一跳 B
```

> 🧠 **为什么是"最长匹配"而不是"精确匹配"？** 因为这允许路由聚合——用一条 `/16` 规则覆盖 256 个 `/24` 子网，同时又能为特殊子网写更精确的 `/24` 规则精准分流。这是互联网路由表能压缩到几十万条的核心原理。

### 3.3 Linux 路由操作

```bash
# 查看路由表
ip route show
ip route show table all    # 查看所有路由表（包括策略路由表）

# 添加/删除路由
ip route add 10.0.0.0/8 via 192.168.1.254
ip route add 10.0.0.0/8 via 192.168.1.254 dev eth0
ip route add 192.168.100.0/24 dev eth1        # 直连路由
ip route del 10.0.0.0/8

# 修改默认网关
ip route del default
ip route add default via 192.168.1.1
# 或者一行替换：
ip route replace default via 192.168.1.1

# 查看到某IP走什么路由
ip route get 8.8.8.8
# 输出：8.8.8.8 via 192.168.1.1 dev eno1 src 192.168.1.10
```

### 3.4 Windows 路由操作

```cmd
:: 查看路由表
route print
route print -4     :: 仅IPv4

:: 添加路由（需管理员权限）
route add 10.0.0.0 mask 255.0.0.0 192.168.1.254
route add 10.0.0.0 mask 255.0.0.0 192.168.1.254 -p    :: -p 表示永久路由

:: 删除路由
route delete 10.0.0.0

:: 查看追踪路径
tracert 8.8.8.8
```

---

## 第四章 实战：四个核心场景

### 场景1：双网卡——内网+外网同时通

**需求**：公司内网走网卡1，互联网走网卡2。

```
网卡1 (eth0)：10.0.0.100/24，网关 10.0.0.1  → 公司内网
网卡2 (eth1)：192.168.1.10/24，网关 192.168.1.1 → 互联网
```

**会出现的问题**：系统只有一个默认网关。如果默认网关设了 `10.0.0.1`，互联网走不通。如果默认网关设了 `192.168.1.1`，内网资源可能走公网绕一圈。

**解决方案**：

```bash
# 思路：默认网关走互联网，内网段用静态路由精确指向
ip route add default via 192.168.1.1 dev eth1
ip route add 10.0.0.0/8 via 10.0.0.1 dev eth0
ip route add 172.16.0.0/12 via 10.0.0.1 dev eth0
```

**验证**：
```bash
ip route get 10.100.1.5       # 应显示 via 10.0.0.1 dev eth0
ip route get 8.8.8.8          # 应显示 via 192.168.1.1 dev eth1
```

### 场景2：搭建软路由（OpenWrt on x86）

**硬件需求**：任何 x86 小主机/工控机，双网口（或单网口+VLAN）。

**步骤**：

```bash
# 1. 制作启动盘
wget https://downloads.openwrt.org/releases/23.05.0/targets/x86/64/openwrt-23.05.0-x86-64-generic-squashfs-combined.img.gz
gunzip openwrt-23.05.0-x86-64-generic-squashfs-combined.img.gz
sudo dd if=openwrt-23.05.0-x86-64-generic-squashfs-combined.img of=/dev/sdX bs=4M status=progress

# 2. 插电启动，串口或键盘显示器登录
# 默认 eth0=LAN(192.168.1.1)，eth1=WAN(DHCP)

# 3. 配置WAN口（PPPoE拨号）
uci set network.wan.proto='pppoe'
uci set network.wan.username='宽带账号'
uci set network.wan.password='宽带密码'
uci commit network
ifup wan

# 4. 安装LuCI网页管理
opkg update
opkg install luci

# 5. 安装常用插件
opkg install luci-app-upnp          # UPnP
opkg install luci-app-sqm           # 流量整形/QoS
opkg install luci-app-statistics    # 流量统计
opkg install luci-app-wireguard     # WireGuard VPN
```

### 场景3：服务器双线——电信+联通智能分流

**需求**：服务器有电信和联通两条线路，电信用户走电信，联通用户走联通，其他走电信（默认）。

```bash
# 思路：策略路由 (Policy Routing)
# 不按"目的IP"选路，而按"源IP属于哪个运营商"选路

# 1. 创建两个路由表
echo "100 ct" >> /etc/iproute2/rt_tables    # 电信路由表
echo "200 cu" >> /etc/iproute2/rt_tables    # 联通路由表

# 2. 各路由表设默认网关
ip route add default via 电信网关IP dev eth0 table ct
ip route add default via 联通网关IP dev eth1 table cu

# 3. 电信IP段走ct表，联通IP段走cu表
# 需要导入运营商IP地址库（可从APNIC获取）
ip rule add from 电信IP段 table ct
ip rule add from 联通IP段 table cu

# 4. 主路由表走电信（默认）
ip route add default via 电信网关IP

# 5. 自动导入运营商路由表（以电信为例）
curl -s http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest | \
  awk -F'|' '/CN\|ipv4/ {print $4, 32-log($5)/log(2)}' | \
  while read net mask; do
    ip route add $net/$mask via 电信网关 table ct
  done
```

### 场景4：API Gateway 部署（Kong / Nginx）

在现代微服务架构中，"网关"更多指 API Gateway——应用层的智能路由器。

```nginx
# Nginx 作为 API Gateway 的配置示例
upstream user_service {
    server 10.0.1.10:8080 weight=3;
    server 10.0.1.11:8080 weight=1;
}

upstream order_service {
    server 10.0.2.10:8080;
    server 10.0.2.11:8080 backup;  # 备用
}

server {
    listen 443 ssl;
    server_name api.example.com;

    # 路由：根据URL路径分发
    location /api/users/ {
        proxy_pass http://user_service/;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /api/orders/ {
        proxy_pass http://order_service/;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 限流
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # 认证
    auth_request /auth/verify;
}
```

这个场景说明：**路由的思想是通用的**——不管是IP包的路由，还是HTTP请求的路由，本质上都是"查规则 → 找下一跳"。

---

## 第五章 路由协议详解

### 5.1 静态路由 vs 动态路由

| 维度 | 静态路由 | 动态路由 |
|------|---------|---------|
| 配置方式 | 手工逐条添加 | 协议自动学习 |
| 收敛速度 | 不适用（不变） | 依赖协议（秒级到分钟级） |
| CPU/内存 | 几乎为零 | 有开销（OSPF需要SPF计算） |
| 适用规模 | 小型网络（<10条路由） | 中大型网络 |
| 可靠性 | 链路断了不知道 | 自动切换备用路径 |
| 安全性 | 不会被路由协议攻击 | 需要认证和过滤 |

**经验法则**：
- 默认路由 + 几条内部网络 → 静态路由即可
- 超过 3 台路由器互连 → 上 OSPF
- 连接互联网/多 AS → 上 BGP

### 5.2 RIP——最古老也最简单的动态路由

**原理**：每 30 秒广播整张路由表给邻居。跳数定胜负（最多 15 跳）。

```
路由器A的路由表：
  网络10.0.0.0/8, 跳数: 1, 下一跳: 直连

路由器A发广播 → 路由器B听到：
  "哦！A说它到 10.0.0.0/8 只需要1跳，那我经过A就是2跳"
  → 添加路由：10.0.0.0/8, 跳数: 2, 下一跳: A
```

**缺点**：收敛慢（等30秒才知道邻居挂了）、不支持 CIDR（默认不携带子网掩码，RIPv2 才支持）、最大 15 跳限制、广播浪费带宽。

**什么时候用**：现在几乎不用了。偶尔在极简单场景（2-3台路由器、不需要快速收敛）或教学场景中见到。

### 5.3 OSPF——企业网络的标配

**原理**：每台路由器画一张本地地图（链路状态），洪泛给整个区域，每台路由器用 Dijkstra 算法独立计算最短路径树。

```
类比：RIP = 问路（"去火车站怎么走？""往前两个路口左转"——只告诉你方向，不告诉你全貌）
     OSPF = 人手一份城市地图，各自规划最优路线
```

**核心概念**：

| 概念 | 解释 |
|------|------|
| **区域 (Area)** | 把网络分成多个区域，减少每台路由器需要掌握的信息量。Area 0 是骨干区域，所有区域必须连接 Area 0 |
| **DR/BDR** | 在广播网络（如以太网）中选出的指定路由器/备份指定路由器，减少邻接关系数量 |
| **LSA** (链路状态通告) | 路由器发的地图碎片 |
| **Cost** | 链路的开销，默认 = 100Mbps / 带宽。OSPF选路依据是路径总 Cost 最小 |
| **SPF算法** | Dijkstra 最短路径优先算法，每台路由器独立运行 |

**基本配置示例** (Cisco IOS)：

```cisco
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
!
! 修改接口Cost（越小越优先）
interface GigabitEthernet0/0
 ip ospf cost 10
```

**查看OSPF状态**：
```cisco
show ip ospf neighbor        ! 查看邻居关系
show ip ospf database        ! 查看链路状态数据库
show ip route ospf           ! 查看OSPF学到的路由
```

### 5.4 BGP——互联网的脊梁

**BGP 是唯一把互联网粘在一起的协议。** 全球 10 万+ 自治系统通过 BGP 交换路由信息。

**原理**：BGP 不是找"最短路径"，而是根据**策略**（路径属性）选路。BGP 交换的是**路径向量**——每一条路由都携带了完整的 AS 路径。

```
BGP 路由通告示例：
  网络: 8.8.8.0/24
  AS路径: 15169 (Google) → 指示这条路由来自Google的AS
  下一跳: 203.0.113.1
```

**核心概念**：

| 概念 | 解释 |
|------|------|
| **AS (自治系统)** | 一个管理域。AS号由IANA分配，16位(0-65535)或32位 |
| **eBGP** | 不同AS之间的BGP对等 |
| **iBGP** | 同一AS内部的BGP对等（全互联/路由反射器） |
| **AS_PATH** | 路由通告经过的AS列表，也是防环机制 |
| **LOCAL_PREF** | 本地优先级，控制出站流量走向 |
| **MED** (Multi-Exit Discriminator) | 向邻居建议入站路径 |
| **路由反射器 (RR)** | 解决iBGP全互联问题 |

**BGP 选路顺序（简化版）**：

1. 最高 LOCAL_PREF 优先
2. 最短 AS_PATH 优先
3. 最低 MED 优先
4. eBGP 优先于 iBGP
5. 最低 IGP Cost 到下一跳

**为什么互联网依赖 BGP？**
因为互联网不是一个集中管理的网络——它是成千上万个独立网络（AS）自愿互联而成的。BGP 是它们之间"协商路线"的共同语言。

### 5.5 协议选择速查

| 场景 | 推荐协议 | 原因 |
|------|---------|------|
| 家庭/小办公室 | 静态路由 | 没必要动态 |
| 企业内部（>3台路由器） | OSPF | 成熟、收敛快、厂商支持好 |
| 运营商骨干 | IS-IS 或 OSPF | IS-IS 在大型网络中更稳定 |
| 连接互联网（多ISP） | BGP | 唯一选择 |
| 数据中心 Spine-Leaf | BGP(带ECMP) 或 OSPF | BGP EVPN 已成趋势 |
| SD-WAN | 控制器驱动的 overlay 路由 | 超越传统协议 |

---

## 第六章 进阶技术

### 6.1 策略路由 (Policy-Based Routing)

传统路由：只看**目的IP**选路。
策略路由：可以按**源IP、协议类型、端口号、TOS字段**等选路。

```bash
# Linux 策略路由示例：
# 需求：来自 192.168.1.100 的流量走电信出口，其余走联通

# 1. 创建自定义路由表
echo "100 custom_table" >> /etc/iproute2/rt_tables

# 2. 该表走电信网关
ip route add default via 电信网关 dev eth0 table custom_table

# 3. 规则：来自 192.168.1.100 的流量查 custom_table
ip rule add from 192.168.1.100 table custom_table
ip rule add from 192.168.1.100 to 内网段 table main   # 内网流量正常走

# 查看策略路由规则
ip rule list
```

### 6.2 NAT 深度解析

NAT（网络地址转换）解决了 IPv4 地址枯竭问题，但也引入了复杂性。

| 类型 | 全称 | 行为 | 使用场景 |
|------|------|------|---------|
| **SNAT** | Source NAT | 改源IP | 内网访问公网（最常见的 NAT） |
| **DNAT** | Destination NAT | 改目的IP | 端口映射/负载均衡 |
| **MASQUERADE** | 动态SNAT | 源IP动态改为出接口IP | 家庭路由器（公网IP会变） |
| **Full-cone NAT** | 完全锥形 | 任何外部主机都能发包到你映射的端口 | NAT 类型中最宽松 |
| **Symmetric NAT** | 对称型 | 不同目标使用不同映射 | 最严格，P2P 难以穿透 |

**NAT 带来的问题**：
- 破坏了"端到端"原则（互联网最初设计是任何两台主机可直接通信）
- P2P 应用需要额外的 NAT 穿透技术（STUN/TURN/ICE）
- 服务端无法主动连接 NAT 后面的客户端
- 为 IPv6 的推广增加了阻力

### 6.3 VPN 与隧道

VPN 本质上是一条"逻辑上的直连线路"，通过加密隧道在不可信的网络上传输数据。

```bash
# WireGuard 配置示例（最简单高效的现代VPN）
# 服务器端 /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <服务器私钥>

[Peer]
PublicKey = <客户端公钥>
AllowedIPs = 10.0.0.2/32          # 只给这个客户端路由这个IP

# 客户端配置
[Interface]
Address = 10.0.0.2/24
PrivateKey = <客户端私钥>

[Peer]
PublicKey = <服务器公钥>
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0             # 所有流量走隧道 → 相当于"把网关搬到了服务器"
```

**`AllowedIPs` 是关键**：它不只是访问控制，更是**路由决策**。`AllowedIPs = 0.0.0.0/0` 就是告诉系统"所有流量通过这个隧道出去"。

### 6.4 SD-WAN——软件定义广域网

传统广域网：专线 + MPLS，运营商控制一切。
SD-WAN：用软件在普通互联网线路上建立智能 overlay 网络。

```
传统WAN：            SD-WAN：
[分支]──MPLS──[总部]      [分支]──互联网──[总部]
   + 专线                    \    /    \    /
                              [控制器：统一管理、智能选路]
```

**SD-WAN 的选路逻辑**超越了传统路由协议：
- 实时监测每条链路的质量（延迟、丢包、抖动）
- 关键应用自动走质量最好的链路
- 一条链路断了，毫秒级切换到另一条
- 甚至可以按应用类型分流（Office 365 直接走互联网，ERP 走专线）

### 6.5 Anycast——一个IP出现在多个地点

Anycast 是路由协议的"魔法"：同一个 IP 地址在多台服务器上同时宣告，用户自动连接到最近的一台。

```
DNS根服务器 8.8.8.8（Google DNS）的Anycast：
  东京数据中心: 宣告 8.8.8.0/24
  新加坡数据中心: 宣告 8.8.8.0/24
  伦敦数据中心: 宣告 8.8.8.0/24
  纽约数据中心: 宣告 8.8.8.0/24

用户的数据包：
  日本用户 → BGP看到东京的路径最短 → 连到东京
  英国用户 → BGP看到伦敦的路径最短 → 连到伦敦
```

**这是互联网基础设施的降维打击**——不需要DNS做地理调度，不需要应用层负载均衡，BGP 自动帮你把用户路由到最近节点。CDN 的底层就是 Anycast + BGP。

### 6.6 路由聚合（Route Aggregation / Summarization）

核心思想：用一条短掩码路由代表多条长掩码路由。

```
聚合前（4条路由）：
  192.168.1.0/24 → 下一跳 A
  192.168.2.0/24 → 下一跳 A
  192.168.3.0/24 → 下一跳 A
  192.168.4.0/24 → 下一跳 A（1280条路由）

聚合后（1条路由）：
  192.168.0.0/22 → 下一跳 A
  （192.168.0.0 到 192.168.3.255 共4个 /24）

聚合后（更大范围）：
  192.168.0.0/16 → 下一跳 A
```

路由聚合是互联网路由表能保持"仅"几十万条（而非几千万条）的关键。全球 BGP 路由表大小约 95万条（2024年数据），如果没有路由聚合，这个数字会膨胀数十倍。

---

## 第七章 社区资源精选

### 7.1 书籍

| 书名 | 适合人群 | 内容概览 | 一句话评价 |
|------|---------|---------|-----------|
| **《TCP/IP详解 卷1》** Stevens | 所有人 | 协议基础圣经，路由相关章节清晰透彻 | 三十年不过时的经典 |
| **《TCP/IP路由技术 卷1+卷2》** Doyle | 网络工程师 | OSPF/BGP/IS-IS的终极参考，Cisco视角 | CCIE备考者人手一套 |
| **《计算机网络：自顶向下》** Kurose/Ross | 学生/转行者 | 第4章讲网络层路由，有配套实验 | 最好的入门教材 |
| **《BGP设计与实现》** Zhang/Bartell | 运营商/云网络工程师 | BGP深度实战，包含大型ISP案例 | 互联网路由的真刀真枪 |
| **《SDN：软件定义网络》** Nadeau/Gray | 架构师 | OpenFlow到SD-WAN的演进全景 | 理解网络未来的必读 |

### 7.2 在线课程

| 课程 | 平台 | 适合人群 | 为什么值得看 |
|------|------|---------|-------------|
| CCNA 200-301 | Cisco/Udemy/B站 | 零基础 | 覆盖路由基础，实验多，认证含金量高 |
| Computer Networking (Kurose) | YouTube/B站 | 学生 | 原作者亲授，动画精美 |
| BGP 大师课 (INE/网络饭饭) | B站/INE | 进阶工程师 | 中文BGP讲得最好的系列 |
| AWS Networking Deep Dive | AWS/YouTube | 云工程师 | 理解云中路由与网关的实现 |

### 7.3 工具与实验平台

| 工具 | 用途 | 一句话 |
|------|------|--------|
| **GNS3** | 网络模拟器，跑真实路由OS镜像 | 比真机还方便 |
| **EVE-NG** | GNS3的高性能替代品 | 支持多厂商 |
| **Packet Tracer** | Cisco入门模拟器 | 零门槛，教学首选 |
| **Wireshark** | 抓包分析 | 看路由协议报文就靠它 |
| **Looking Glass** | 各ISP公开的BGP查询工具 | 在线看全球BGP路由 |
| **bgp.he.net** | Hurricane Electric的BGP工具 | 查AS、查路由、查前缀 |

### 7.4 社区与资讯

| 资源 | 平台 | 特点 |
|------|------|------|
| **r/networking** | Reddit | 英文网络工程师社区，问题质量高 |
| **V2EX / 宽带症候群** | V2EX | 中文软路由/家庭网络讨论活跃 |
| **Cisco Learning Network** | Cisco官方 | CCNA/CCIE备考社区 |
| **NANOG 邮件列表** | nanog.org | 北美运营商圈子，BGP真实运维讨论 |
| **BGP Stream** | bgpstream.com | BGP路由劫持/泄露实时监控 |

---

## 第八章 业内评价与案例

### 8.1 全球路由表规模演变

| 年份 | IPv4 路由表条目数 | 增长趋势 |
|------|------------------|---------|
| 2010 | ~33万 | — |
| 2015 | ~55万 | 67% 增长 |
| 2020 | ~82万 | 49% 增长 |
| 2024 | ~95万 | 16% 增长 |

> 来源：CIDR Report (cidr-report.org), 2024年数据

增长在放缓，部分原因是 IPv4 地址耗尽后不再有新的大块分配，另一部分是路由聚合策略的改进。

### 8.2 著名网络故障案例

**案例1：2008年巴基斯坦电信 YouTube 劫持**

巴基斯坦电信（AS17557）应政府要求封锁 YouTube，错误地将一条更具体的 YouTube IP 前缀的 BGP 路由通告给了其上游 PCCW（AS3491）。由于这条路由比 YouTube 自己宣告的更具体（`/24` vs `/22`），全球流量被重定向到巴基斯坦，YouTube 全球宕机约2小时。

**教训**：BGP 没有内建的内容验证机制——任何 AS 都可以宣告任意前缀。RPKI (Resource Public Key Infrastructure) 就是为了解决这类问题。

**案例2：2021年 Facebook 全球宕机**

Facebook 的 BGP 路由被意外撤回，导致其所有服务（Facebook、Instagram、WhatsApp）从互联网上"消失"了约6小时。根本原因是配置变更触发了骨干网故障，BGP 会话全部中断。

**教训**：即使是最顶级的互联网公司，一个 BGP 配置失误也能让所有服务不可达。运维上带外管理通道的重要性在此体现——Facebook 工程师甚至进不了机房，因为门禁系统也依赖同一网络。

**案例3：Cloudflare 的 Anycast 防御 DDoS**

Cloudflare 在全球 330+ 城市部署了 Anycast 网络。当遭遇 DDoS 攻击时，攻击流量被分散到所有节点，每个节点只需要承受一小部分。这使得 Cloudflare 可以吸收 TB 级别的攻击流量。

**教训**：Anycast 不仅是性能优化手段，更是安全防御手段。把 IP 地址"散布"到全球，攻击者打不到真正的服务器。

### 8.3 行业趋势信号

| 信号 | 说明 |
|------|------|
| **BGP 岗位薪资** | 国内 BGP 网络工程师年薪 30-80 万，资深可破百万（2024年数据，来源：Boss直聘/猎聘） |
| **云网络认证热度** | AWS/Azure 网络专项认证年增长率 40%+ |
| **eBPF 网络兴起** | Cilium/eBPF 正在替代 iptables/OVS，成为云原生网络的新基础 |
| **SRv6 替代 MPLS** | 中国三大运营商已在骨干网部署 SRv6，MPLS 的黄昏来临 |

---

## 第九章 避坑指南

### 9.1 常见故障排查

| 错误现象 | 原因分析 | 修复步骤 |
|---------|---------|---------|
| **能 ping IP 不能 ping 域名** | DNS配置错误 | 检查 `/etc/resolv.conf`，试 `nslookup baidu.com 8.8.8.8` |
| **内网互通但上不了外网** | NAT没配或网关不对 | 检查 `iptables -t nat -L`，确认 MASQUERADE 规则 |
| **路由器能上外网，内网设备不行** | IP转发没开 | `sysctl net.ipv4.ip_forward`，必须为1 |
| **部分网站打不开** | MTU 问题（常见于PPPoE） | `ping -M do -s 1472 8.8.8.8` 测试，调整 MTU 为 1492 或更小 |
| **路由表中有路由但还是不通** | 回程路由缺失 | 通信是双向的！检查对端是否有回来的路由 |
| **OSPF邻居起不来** | Hello/Dead 间隔不匹配、区域号不一致、认证密码错误 | `show ip ospf neighbor` 看状态，检查两端配置一致性 |
| **BGP路由收不到** | TTL问题（eBGP多跳）、AS号配置错误、路由策略拒绝 | `show ip bgp summary` 看邻居状态 |
| **NAT后面的服务器外网访问不了** | 没有端口映射（DNAT） | 添加端口转发规则 `iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to 192.168.1.100:80` |
| **双网关导致路由振荡** | 两个默认路由metric相同，ECMP导致包乱序 | 只保留一个默认网关，另一个用策略路由按需使用 |

### 9.2 路由环路问题

```
路由环路示例：
路由器A：去 10.0.0.0/8 → 下一跳 路由器B
路由器B：去 10.0.0.0/8 → 下一跳 路由器A

数据包在两台路由器之间来回弹，TTL递减直到归零丢弃。
```

**防环机制**：
- RIP：最大15跳（超过即丢弃）
- OSPF：SPF算法天然无环
- BGP：AS_PATH 属性（看到自己的AS号就丢弃）
- IP层：TTL字段（每经过一跳减1，归零即丢弃）

### 9.3 非对称路由

**现象**：出去的包走路径A，回来的包走路径B。TCP连接能建立，但状态防火墙可能拦回来包（因为它没看到出去的SYN）。

```
解决：
├── 状态防火墙设计成无状态模式（不推荐）
├── 确保来回路径一致（对称路由设计）
└── 使用多路径TCP (MPTCP) 或连接追踪同步（复杂）
```

### 9.4 性能优化

```bash
# 1. 增大 conntrack 表（NAT会话跟踪表）
sysctl -w net.netfilter.nf_conntrack_max=1048576

# 2. 减小 conntrack 超时（释放不活跃连接）
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established=3600

# 3. 开启 BBR 拥塞控制（谷歌声称吞吐量提升可达2700倍，来源：ACM Queue 2016）
sysctl -w net.core.default_qdisc=fq
sysctl -w net.ipv4.tcp_congestion_control=bbr

# 4. 调整接收/发送缓冲区
sysctl -w net.core.rmem_max=134217728
sysctl -w net.core.wmem_max=134217728

# 5. 开启网卡多队列 RSS
ethtool -L eth0 combined 8    # 将中断分布到8个CPU核心
```

---

## 第十章 进阶技巧与最佳实践

### 10.1 路由设计原则

| 原则 | 说明 |
|------|------|
| **KISS** (Keep It Simple, Stupid) | 能用静态路由的不用动态协议 |
| **层次化设计** | 核心层→汇聚层→接入层，路由条目逐层聚合 |
| **冗余但不冗余过度** | 备份链路要有，但不要让路由表膨胀到不可维护 |
| **路由聚合优先** | 每台路由器只应知道它需要的最小路由集 |
| **管理网络与业务网络分离** | 管理流量走独立的带外管理网 |

### 10.2 学习路线图

```
第一周：基础
├── OSI 七层模型、TCP/IP 四层模型
├── IP 地址、子网掩码、CIDR 计算
├── 路由表理解、默认网关概念
└── 实验：用两台Linux搭建简单路由器 + NAT

第二周：静态路由 + 基础动态路由
├── 静态路由实战（双网卡、多出口）
├── RIP 原理与配置（用GNS3模拟）
├── OSPF 基础（单区域）
└── 实验：3台路由器 + OSPF实现全网互通

第三周：高级路由
├── OSPF 多区域、虚链路
├── BGP 基础（eBGP/iBGP）
├── 策略路由
└── 实验：模拟多AS BGP互联

第四周：实战场景
├── 企业网络设计（VLAN间路由、NAT、ACL）
├── VPN部署（WireGuard/IPsec）
├── 排障方法论（自底向上：物理→链路→网络→传输→应用）
└── 实验：完整企业网络搭建 + 故障注入排障
```

### 10.3 自学方法

- **用 GNS3/EVE-NG 搭建拓扑**：比看书快 10 倍。先做，再看理论
- **抓包看协议交互**：Wireshark 抓 OSPF Hello 包、BGP UPDATE 包，比读 RFC 直观
- **看全球路由表**：`telnet route-views.routeviews.org`，执行 `show ip bgp`，感受互联网的脉搏
- **追踪真实路径**：`traceroute` 不同国家的网站，观察 AS_PATH 的变化
- **读故障报告**：Cloudflare、AWS、Azure 的事后分析博客是免费的网络架构课程

---

## 第十一章 未来展望

### 11.1 IPv6 的路由大迁徙

IPv6 部署已经走了二十多年，但真正的转折点正在到来。截至 2024 年，全球 IPv6 采用率约 42%（Google 统计），中国约 35%（APNIC 数据）。这不是一个"遥不可及的未来"——全球近一半的互联网流量已经是 IPv6。

IPv6 对路由的影响是根本性的：
- **不再需要 NAT**——每个设备有全球唯一地址，端到端原则回归
- **路由表更简洁**——IPv6 地址空间极大，可以采用严格的层次化分配，路由聚合效率远高于 IPv4
- **但 BGP 路由表仍在增长**——IPv6 BGP 表目前约 20 万条，增长速度快于 IPv4

预测：未来 5 年内，中国三大运营商的移动网络将实现 IPv6-only，家庭宽带进入双栈→IPv6 为主的过渡期。路由工程师需要掌握 IPv6 路由协议（OSPFv3、MP-BGP for IPv6）成为基本要求。

### 11.2 eBPF 重写网络栈

eBPF（extended Berkeley Packet Filter）正在从根本上改变 Linux 网络栈。传统上，数据包在内核中经过固定的处理路径（netfilter → iptables → 路由 → 转发）。eBPF 允许你在内核的任意钩子点注入自定义程序。

**Cilium**（基于 eBPF 的 CNI 插件）已经证明了这一点：
- 替代 kube-proxy（不再需要 iptables 规则海洋）
- 直接在内核层做服务网格（旁路 Sidecar）
- 路由决策可以在内核中以纳秒级完成

这意味着一台 Linux 服务器可以同时是：路由器、防火墙、负载均衡器、服务网格数据面——全在 eBPF 中完成。**路由不再是一个独立的"设备"功能，而是一个可编程的内核能力。**

### 11.3 云原生网关的暗战

API Gateway 市场正在经历一场"安静的革命"：

| 玩家 | 策略 |
|------|------|
| **Envoy** (CNCF) | 数据面事实标准，被 Istio/Contour/Ambassador 等使用 |
| **Kong** | 从 API Gateway 向全栈服务连接平台扩展 |
| **Traefik** | 容器原生，自动发现服务 |
| **云厂商原生网关** | AWS API Gateway、Azure Application Gateway、阿里云 MSE 云原生网关 |
| **NGINX/F5** | 老牌负载均衡厂商，收购/自研进入云原生 |

趋势判断：API Gateway 和 Service Mesh 的边界正在模糊。未来 3-5 年内，这两个品类可能合并为统一的"应用网络层"——既是南北向流量（外部↔内部）的网关，也是东西向流量（服务↔服务）的路由器。

### 11.4 太空互联网的路由挑战

SpaceX Starlink 已经证明了低轨卫星互联网的商业可行性。但这给路由协议带来了前所未有的挑战：

- **地面网络**：路由器之间是静态的物理线路，拓扑变化以"天"或"月"为周期
- **卫星网络**：卫星以 7.5 km/s 的速度移动，拓扑以**毫秒**为周期变化

传统的 IGP（OSPF/IS-IS）根本无法适应这种拓扑变化速度。Starlink 目前使用"太空弯管"架构（卫星只是中继，地面站做路由决策），但真正的星间激光链路（ISL）一旦全面部署，需要全新的路由协议——可能结合了 MANET（移动自组网）和传统 BGP 的混合方案。

### 11.5 量子网络的路由

量子互联网不是科幻。中国"墨子号"卫星和中国科学技术大学的量子京沪干线已经证明了量子密钥分发（QKD）的可行性。但量子信息的路由与传统 IP 路由有本质区别：

1. **量子不可克隆定理**——你不能"复制"一个量子态，所以在量子网络中不能像经典网络那样做"存储转发"
2. **纠缠交换**——量子路由需要预先建立纠缠链路，然后通过纠缠交换"转接"
3. **量子中继器**——替代经典路由器的设备，目前仍在实验室阶段

这是一个 10-20 年时间尺度的领域。但如果你现在 25 岁，你的职业生涯后半段可能就要面对量子网络的路由设计问题。

### 11.6 路由智能化的终极形态

我看到一个清晰的发展脉络：

```
静态路由 → 动态路由协议 → SDN集中控制 → AI驱动的自愈网络
   (手工)    (分布式算法)    (控制器)      (大模型预测+优化)
```

未来的路由器不只是"查表转发"。它可能：
- 实时分析流量模式，预测 5 分钟后的拥塞
- 自动调整路由策略，在用户感知到延迟之前就切换路径
- 自我诊断故障，不只是"链路 down"，而是"链路质量在劣化，提前切换"
- 多维度决策——不只是延迟，还有能耗、成本、合规（数据不出境）

这不是科幻。Google 的 B4 SD-WAN 已经基于流量预测做动态带宽分配。Juniper 的 Marvis（AI 运维助手）已经开始做故障预测。当大语言模型与网络遥测数据结合，路由决策将从"反应式"变成"预判式"。

**路由的终极形态，不是更快的查表，而是不需要查表——网络自己知道你要去哪，在你说出口之前。**

---

## 附录：术语表

| 中文 | 英文 | 使用场景 |
|------|------|---------|
| 自治系统 | Autonomous System (AS) | BGP 语境——"这个 AS 宣告了这段 IP" |
| 边界网关协议 | BGP | 连接不同 AS，互联网骨干路由协议 |
| 无类别域间路由 | CIDR | 表示IP段——`192.168.1.0/24` 这种写法就是 CIDR |
| 数据包 | Packet | IP 层的数据单位，包含源/目的 IP 地址 |
| 默认网关 | Default Gateway | 局域网设备的出口——几乎所有设备的路由表最后一行 |
| 动态主机配置协议 | DHCP | 自动分配 IP 地址的服务，路由器通常内置 |
| 域名系统 | DNS | 把域名翻译成 IP，不是路由协议但路由离不开它 |
| 等价多路径 | ECMP | 多条路径 cost 相同，流量负载分担 |
| 边界网关协议外部对等 | eBGP | 不同 AS 之间的 BGP，TTL=1 默认 |
| 内部网关协议 | IGP | AS 内部的路由协议（OSPF、IS-IS、RIP） |
| 边界网关协议内部对等 | iBGP | 同一 AS 内部的路由器运行 BGP |
| IP转发 | IP Forwarding | Linux 内核功能——收到不是发给自己的包时转发出去 |
| 链路状态通告 | LSA | OSPF 中路由器的"地图碎片" |
| 最长前缀匹配 | Longest Prefix Match | 路由表查找规则——掩码最长的那条命中 |
| 最大传输单元 | MTU | 一条链路能传输的最大包大小，超过则需要分片 |
| 网络地址转换 | NAT | 私网 IP ↔ 公网 IP 的翻译 |
| 下一跳 | Next Hop | 路由表中每条路由指定的"下一站"路由器 IP |
| 开放最短路径优先 | OSPF | 链路状态 IGP，企业网络标配 |
| 策略路由 | PBR (Policy-Based Routing) | 非目的地址驱动的路由选择 |
| 路由信息协议 | RIP | 古老的距离矢量路由协议，跳数制 |
| 路由聚合 | Route Aggregation | 多条路由合并为一条短掩码路由 |
| 路由表 | Routing Table | 每台路由器的核心数据结构——"去哪走哪"的地图 |
| 边界网关协议路由反射器 | Route Reflector | 解决 iBGP 全互联的机制 |
| 资源公钥基础设施 | RPKI | 防止 BGP 路由劫持的证书体系 |
| 软件定义广域网 | SD-WAN | 软件控制的智能广域网 |
| 生存时间 | TTL (Time To Live) | IP 包头中的防环字段，每跳减1 |
| 虚拟路由冗余协议 | VRRP | 多台路由器共享一个虚拟 IP，提供冗余 |
| 等价路由 | Equal-cost route | 到同一目的地有两条 cost 相同路径 |
| 虚拟局域网 | VLAN | 二层隔离技术，"虚拟局域网" |
| 出口/入口 | Egress/Ingress | 你发出的流量叫出口，进来的叫入口 |
| 隧道 | Tunnel | 把一种协议包在另一种协议里传输 |
| BGP 前缀劫持 | BGP Hijack | 恶意或误操作宣告不属于自己的 IP 段 |
| 云原生网络 | Cloud Native Networking | 以容器/K8s 为中心的网络架构 |
| 服务质量 | QoS | 给不同类型流量分配不同优先级 |

---

**路由与网关 · 深度技术手册 v1.0** | 2026-05-13 | 呈：张成市
