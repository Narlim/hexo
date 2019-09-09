---
title: curl总结
date: 2019-09-09 22:55:11
tags: linux
---
所有的示例都来自与[Curl Cookbook](https://catonmat.net/cookbooks/curl)
<!--more-->

#### POST请求  
###### 发送一个post请求
```shell
$ curl -d 'login=emma&password=123' -X POST https://google.com/login
```
也可以直接不用写“-X POST”，因为有了“-d”，默认用post请求：
```shell
$ curl -d 'login=emma&password=123' https://google.com/login
```
或者可以这样：
```shell
$ curl -d 'login=emma' -d 'password=123' https://google.com/login
```

###### 追随重定向：
```shell
$ curl -L -d 'tweet=hi' https://api.twitter.com/tweet
```
###### 发送一个json数据：
```shell
$ curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' https://google.com/login
```
###### 发送文本格式数据：
```shell
$ curl -d 'hello world' -H 'Content-Type: text/plain' https://google.com/login
```

###### 从一个文件中发送数据：
```shell
$ curl -d '@data.txt' https://google.com/login
```
###### 发送一个二进制文件：
```shell
$ curl -F 'file=@photo.png' https://google.com/profile
```
###### 发送一个二进制文件，并设置mime类型：
```shell
$ curl -F 'file=@photo.png;type=image/png' https://google.com/profile
```

#### 添加http头

###### 添加一个简单的头
```shell
$ curl -H 'Accept-Language: en-US' https://google.com
```

###### 添加两个头
```shell
$ curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://google.com
```

###### 添加一个空头
```shell
$ curl -H 'Puppies;' https://google.com
```

#### 修改user agent
User-Agent 首部包含了一个特征字符串，用来让网络协议的对端来识别发起请求的用户代理软件的应用类型、操作系统、软件开发商以及版本号。
###### 改为firefox的useragent
```shell
$ curl -A 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0' https://google.com
```
###### 改为chrome的useragent
```shell
$ curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
```

###### 假装是Google bot
```shell
$ curl -A 'Googlebot/2.1 (+http://www.google.com/bot.html)' https://washingtonpost.com
```

###### 用-H参数修改useragent
```shell
$ curl -H 'User-Agent: php/1.0' https://google.com
```

#### 设置cookie
###### 添加一个cookie
```shell
$ curl -b 'session=abcdef' https://google.com
```

###### 添加两个cookie
```shell
$ curl -b 'session=abcdef' -b 'loggedin=true' https://google.com
```

###### 添加一个空的cookie
```shell
$ curl -b 'session=' https://google.com
```

###### 保存一个cookie到文件中
```shell
$ curl -c cookies.txt https://www.google.com
```

###### 加载一个cookie
```shell
$ curl -b cookies.txt https://www.google.com
```
#### 添加referrer
Referer 首部包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。服务端一般使用 Referer 首部识别访问来源，可能会以此进行统计分析、日志记录以及缓存优化等。

##### 添加一个referrer
```shell
$ curl -e 'https://google.com?q=cats' http://catonmat.net
```
When the owner of catonmat.net will look in his access.log files, he'll think that someone came from Google while searching for cats, but in reality, we'll have bamboozled the owner catonmat.net.

###### 发送一个空的referrer
```shell
$ curl -e '' http://catonmat.net
```

###### 用-H参数添加
```shell
$ curl -H 'Referer: https://digg.com' http://catonmat.net
```

#### 追踪重定向
```shell
$ curl -L http://catonmat.net
```

#### 设置basic HTTP Authentication
###### 设置用户名和密码
```shell
$ curl -u 'bob:12345' https://google.com/login
```

###### 在url中设置用户名和密码
```shell
$ curl https://bob:12345@google.com/login
```

###### 命令行提示密码
```shell
$ curl -u 'bob' https://google.com/login
```

#### 打印响应头
###### 打印头和体
```shell
$ curl -i https://catonmat.net
```

###### 仅打印头
```shell
$ curl -s -o /dev/null -D - https://catonmat.net
```
或者：
```shell
$ curl -I https://catonmat.net
```

#### 使用代理
###### 使用socks5代理
```shell
$ curl -x socks5://127.0.0.1:1080 https://google.com
```

###### 使用http代理
```shell
$ curl -x http://127.0.0.1:8001 https://google.com
```

#### 忽略ssl证书
```shell
$ curl -k https://catonmat.net
```

###### 用version 1 的ssl版本
```shell
$ curl -1 https://catonmat.net
```

#### 保存响应到文件
```shell
$ curl -o response.txt https://google.com?q=kitties
```

###### 用url的最后一段作为文件名
```shell
$ curl -O https://catonmat.net/ftp/digg.pm
```

#### 限制curl的速度
```shell
$ curl --limit-rate 200k https://google.com
```

#### debug curl request
###### make curl verbose
```shell
$ curl -v https://catonmat.net
```

###### 追踪细节
```shell
$ curl --trace - https://catonmat.net
```

###### 只打印响应码
```shell
$ curl -w '%{response_code}' -s -o /dev/null https://catonmat.net
```
