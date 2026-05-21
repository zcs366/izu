---
sha256: 51b5ff445fea2002865d52b0649a0fa41b4796efe92141c3cef9109aa15b99b1
source_url: https://mp.weixin.qq.com/s/imRqprRoZkqAUHhrCYr3JA
ingested: 2026-05-12
title: 6步让Hermes在服务器上控制Chrome，点按钮、抓数据全自动
author: 肖冲
source: 微信公众号
content_type: article
description: 上周有朋友问我：Hermes能不能操作浏览器，自动登录账号、点按钮？能。但你得先给它一个浏览器。
---

# 6步让Hermes在服务器上控制Chrome，点按钮、抓数据全自动

上周有朋友问我：Hermes能不能操作浏览器，自动登录账号、点按钮？
能。但你得先给它一个浏览器。

这话听起来废话，但很多人卡在这里。服务器上没有桌面，没有图形界面，Chrome根本跑不起来。你让Hermes打开网页，它找不到任何可以操作的东西。

我花了一个下午把这套环境搭通了。6步配置完，Hermes就能通过CDP协议控制服务器上的Chrome，登录账号、点按钮、抓数据，全自动。

这篇文章把完整流程记录下来，你照着做就行。
先说清楚这套方案的逻辑
服务器上跑浏览器，需要三样东西：
1.虚拟显示器（VNC）：给Chrome一个"假屏幕"，让它以为自己在桌面上运行2.Chrome + CDP：Chrome开启远程调试端口9222，Hermes通过这个端口控制它3.Tailscale：把你的电脑和服务器组成私有网络，安全访问VNC和SSH，不暴露公网
三者缺一不可。
Step 1：服务器装 Tailscale
Tailscale是一个零配置的私有网络工具。装完之后，你的电脑和服务器就像在同一个局域网里，可以直接用内网IP互访。

给Hermes的指令：

帮我在服务器上装 Tailscale 并加入我的网络，完成后告诉我这台机器的 Tailscale IP。

Hermes实际在服务器上执行：

# 安装 Tailscale（2026年最新脚本）
curl-fsSL https://tailscale.com/install.sh |sh

tailscale up
# 它会给你一个授权链接，在浏览器里打开，登录你的Tailscale账号
# 授权完成后，服务器就加入你的私有网络了

tailscale ip-4# 查看服务器的 Tailscale IP，类似 100.x.x.x

注意：Tailscale需要你注册一个账号，注册后把服务器和你的电脑都加进去，两台设备就能直接通信。

第一次进来这个网站需要点击下方链接注册账号，注册过程会出现添加设备的引导，直接跳过。

让Hermes生成链接，点击新链接进来

通知Hermes已经完成，他会检查链路是否畅通。
Step 2：装虚拟桌面 + Chrome
Hermes指令：

帮我装 TigerVNC Server + fluxbox 轻量窗口管理器 + Google Chrome

Hermes实际执行：

# 装 TigerVNC + fluxbox（轻量级窗口管理器）+ 中文字体
sudoapt update
sudoaptinstall-y tigervnc-standalone-server tigervnc-common \
                    fluxbox xterm dbus-x11 \
                    fonts-noto-cjk fonts-noto-color-emoji

# 添加 Google Chrome 软件源
wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
|sudo gpg --dearmor-o /usr/share/keyrings/google-chrome.gpg

echo"deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] \
  http://dl.google.com/linux/chrome/deb/ stable main"\
|sudotee /etc/apt/sources.list.d/google-chrome.list

sudoapt update
sudoaptinstall-y google-chrome-stable
Step 3：设置 VNC 密码
Hermes会问你要不要设密码，直接设一个就行，后面连接VNC要用。
Step 4：配置 Chrome 随 VNC 启动，并开启 CDP
这是最关键的一步。我们要让VNC启动时自动拉起Chrome，并且Chrome开启9222端口供Hermes控制。

让Hermes执行：

cat> ~/.vnc/xstartup <<'EOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_SESSION_TYPE=x11

# 启动 Chrome，开启 CDP 端口 9222，供 Hermes 控制
/opt/google/chrome/chrome \
  --no-sandbox \
  --disable-gpu \
  --disable-software-rasterizer \
  --start-maximized \
  --no-first-run \
  --no-default-browser-check \
  --disable-sync \
  --disable-translate \
  --disable-default-apps \
  --user-data-dir=/root/.chrome-debug \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  >/root/.vnc/chrome.log 2>&1 &

# fluxbox 必须在前台运行，否则VNC会话直接退出
exec fluxbox
EOF

chmod +x ~/.vnc/xstartup
Step 5：防火墙只允许 Tailscale 访问
安全很重要。VNC端口不能对公网开放，只允许通过Tailscale内网访问。

打开CMD客户端，连接服务器后，手动执行以下命令

sudo ufw allow in on tailscale0 to any port 5901 proto tcp
sudo ufw allow in on tailscale0 to any port 22 proto tcp  # SSH也只走Tailscale
sudo ufw deny 5901/tcp        # 拒绝公网访问VNC
sudo ufw default deny incoming
sudo ufw --forceenable
sudo ufw status verbose |grep5901
Step 6：一键检查所有配置
配置完了，跑这个脚本验证一下：

echo"=== 1) Tailscale 状态 ==="
tailscale ip-4||echo"❌ Tailscale 没装"

echo"=== 2) VNC 监听 ==="
ss -tlnp|grep5901||echo"❌ VNC 没起"

echo"=== 3) Chrome CDP ==="
curl-s http://localhost:9222/json/version |grep-q"Chrome"\
&&echo"✅ CDP OK"||echo"❌ Chrome CDP 没起（先查 user-data-dir）"

echo"=== 4) Chrome 136+ user-data-dir 检查 ==="
ps-ef|grep chrome |grep-vgrep|grep-q"user-data-dir"\
&&echo"✅ 带了 user-data-dir"||echo"❌ Chrome 没带 user-data-dir，CDP 会静默失败"

echo"=== 5) 防火墙只对 Tailscale 开 5901 ==="
sudo ufw status |grep"5901"

echo"=== 6) xstartup 可执行 ==="
test-x ~/.vnc/xstartup &&echo"✅ OK"||echo"❌ xstartup 无执行权限"

6项全绿，配置完成。
在你的电脑上连接 VNC
打开链接：https://tailscale.com/download/windows，下载安装tailscale，登录同一个账号，让你的电脑也加入私有网络

出现这个界面时，直接关闭就行。

打开链接：https://sourceforge.net/projects/tigervnc/files/stable/1.16.2/，下载安装tigervnc

打开tigervnc，输入前面生成的IP地址和密码

如果出现这个界面不要慌，说明已经正常连接了，只是浏览器没有打开而已，让Hermes打开chrome浏览器。

正常情况下，能看到熟悉的chrome界面
让 Hermes 控制这个浏览器
现在告诉Hermes：

通过 CDP 连接 localhost:9222 的 Chrome，打开 https://x.com/home，然后点击登录按钮

Hermes会通过CDP协议接管Chrome，在VNC里你能实时看到它的操作。

在VNC界面手动登录账号，Hermes就行继续操作了。
几个容易踩的坑
Chrome 136+ 必须加 --user-data-dir

这是最常见的问题。不加这个参数，CDP连接会静默失败，没有任何报错，你以为是网络问题，其实是启动参数缺了一行。

VNC不能对公网开放

很多教程直接开放5901端口，这非常危险。Tailscale的作用就是把访问锁在私有网络里，公网完全看不到这个端口。

看到黑屏不要慌

VNC连上后如果只有黑屏，说明Chrome还没启动。让Hermes帮你打开Chrome就行，不是配置出了问题。

这套环境配一次，之后就一直能用。Hermes随时可以接管这个浏览器，你不需要再碰服务器。

我现在用它来做社媒账号的自动化操作，省了大量重复劳动。

你在用Hermes做什么？评论区说说。

