---
title: ssh密钥登陆
date: 2019-09-13 11:57:09
tags: linux 
---
新买的vps一般都是配置密码登陆，如果想让自己的vps更安全一点，防止自己的密码被暴力破解，那么可以配置ssh，禁用密码登陆开启密钥登陆。
<!--more-->

#### 上传公钥
```sh
ssh-copy-id -i /home/username/.ssh/id_rsa.pub user@host -p port
```

#### 修改服务器sshd配置
```sh
vim /etc/ssh/sshd_config

#禁用密码验证
PasswordAuthentication no
#启用密钥验证
RSAAuthentication yes
PubkeyAuthentication yes
#指定公钥数据库文件
AuthorsizedKeysFile .ssh/authorized_keys

systemctl restart sshd
```

#### 验证是否生效
强制用密码登陆：
```sh
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no user@host
```
如果提示：Permission denied (publickey)
说明只能用密钥登陆，配置生效。也可以加`-v`参数查看具体连接的信息。