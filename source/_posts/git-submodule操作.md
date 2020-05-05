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
上面的两条也可以合并成一步：
$ git submodule update --init

或者直接一条命令：
$ git clone --recurse-submodules https://github.com/chaconinc/MainProject
```

#### 删除子项目
```shell
$ rm -rf dir
$ rm .gitmodules
$ vim .git/config
修改submodule的配置信息。
$ git commit -a 'info'
```

#### 修改提交子项目
> 当我们运行 git submodule update 从子模块仓库中抓取修改时， Git 将会获得这些改动并更新子目录中的文件，但是会将子仓库留在一个称作“游离的 HEAD”的状态。 这意味着没有本地工作分支（例如 “master” ）跟踪改动。 如果没有工作分支跟踪更改，也就意味着即便你将更改提交到了子模块，这些更改也很可能会在下次运行 git submodule update 时丢失。

```bash
进入子项目修改：
cd sub
git checkout release
git submodule update --remote --merge
这时我们将会看到服务器上的这个子模块有一个改动并且它被合并了进来。
或者直接修改release分支，然后：
git add .
git commit -m 'change something'

如果我们对子模块做了一些改动，上游也对子模块做了改动，就需要用下面的命令了：
git submodule update --remote --rebase

提交：
cd ..
git add .
git commit -m 'change something'

下面的命令会把子项目的修改也提交到远程仓库：
git push --recurse-submodules=on-demand
```

### git改密钥登录（https改为git）

修改`.git`目录的`config`文件：

```bash
url = https://github.com/test/test.git
改为：
url = git@github.com:test/test.git
```
[](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)