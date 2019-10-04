---
title: git submodule操作
date: 2019-10-05 01:13:25
tags: git
---
如果你需要在一个项目中使用另一个项目，就需要用到submodule,[git](https://git-scm.com/book/zh/v1/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)
<!--more-->
#### 添加子项目
```shell
$ git submodule add git://github.com/chneukirchen/rack.git rack

$ git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#      new file:   .gitmodules
#      new file:   rack
会生成一个`.gitmodules`文件。很重要的一点是这个文件跟其他文件一样也是处于版本控制之下的，就像你的.gitignore文件一样。它跟项目里的其他文件一样可以被推送和拉取。这是其他克隆此项目的人获知子模块项目来源的途径。
```

#### 克隆子项目
如果你克隆一个带有子项目的项目，它将包含子项目的目录，但是里面没有文件。接下来你要运行这两个命令：
```shell
$ git submodule init
$ git submodule update
```

#### 删除子项目
```shell
$ rm -rf dir
$ rm .gitmodules
$ vim .git/config
修改submodule的配置信息。
$ git commit -a 'info'
```