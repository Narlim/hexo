---
title: magic trackpad2 支持gnome手势
date: 2021-06-13 17:39:57
tags: ['arch', 'linux', 'trackpad']
---

因为gnome40的触摸板手势是一大特色，而且在使用macbook的时候感觉苹果的触摸板确实挺好用的，于是就是入手了一个magic trackpad2，本来想着是直接蓝牙连接的我的arch上面就可以用了，没想的并没有开箱即用，这里就记录一下配置的过程，防止以后忘记。
<!--more-->

### 连接到蓝牙
很简单，打开trackpad上面的一个开关。默认就可以连接了，但是却有一个报错：  
`profiles/input/device.c:ioctl_is_connected() Can't open HIDP control socket`  
在网上查了半天，终于在['https://wiki.archlinux.org/title/Bluetooth_mouse'](https://wiki.archlinux.org/title/Bluetooth_mouse)里面找到一个关于hid的配置：  
```shell
# Configuration file for the input service
# This section contains options which are not specific to any
# particular interface
[General]

# Set idle timeout (in minutes) before the connection will
# be disconnect (defaults to 0 for no timeout)
IdleTimeout=0

#Enable HID protocol handling in userspace input profile
#Defaults to false(hidp handled in hidp kernel module)
UserspaceHID=true
```
把上面的配置写入或者创建文件：`/etc/bluetooth/input.conf`，重启bluetooth，终于连上了。按照这个配置的意思默认应该用的是内核模块的hidp,不知道为啥我这里用不了。

### 支持gnome40的手势
连上以后发现只有鼠标的点击能用，gnome手势并没有支持，虽然自带的`libinput`已经支持手势，但是gnome可能还没有实现用这个软件来控制，查看wiki后得知需要安装`libinput-gestures`，这个包是在`aur`仓库的：
```shell
yay -S libinput-gestures

libinput-gestures-setup service
libinput-gestures-setup autostart start
```
启动失败，查看失败的原因是权限，需要把当前用户加入到`input`这个用户组：
```shell
sudo usermod -aG input marlin
```
重启电脑。因为这个软件要读取/dev下的设备文件，所以要重启。

启动以后查看：
```shell
systemctl status libinput-gestures --user
```
其实前面的`libinput-gestures-setup service`就是创建了一个用户的systemd服务，`libinput-gestures-setup start`就等同于`systemctl start libinput-gestures --user`，我也不知道为啥他要自定义这些命令= =

### 总结
到手这个trackpad本来以为蓝牙连接上就能直接用了，其实买之前我也看了一篇文章，他用的fedora说是开箱即用的，没想到arch下面还是搞了好久，而且arch下面用trackpad的人好像也不太多，查资料也查了好久，不过最后还是搞定了，虽然过程曲折了一点。里面其实还有很多东西没有弄清楚，到时候有新的内容再来更新。

### 参考
- ['https://wiki.archlinux.org/title/Libinput_(%E7https://github.com/bulletmark/libinput-gestures/blob/master/README.md%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)'](https://wiki.archlinux.org/title/Libinput_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

- ['https://github.com/bulletmark/libinput-gestures/blob/master/README.md'](https://github.com/bulletmark/libinput-gestures/blob/master/README.md)