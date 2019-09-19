---
title: python subprocess模块
date: 2019-09-19 21:14:46
tags: python
---

python subprocess模块基本使用。
<!--more-->

#### run
如果仅仅是为了运行一个外部命令而不用交互，类似 os.system()，可以使用 run() 方法。
```python
completed = subprocess.run(['ls', '-l'])
print('returncode:', completed.returncode)
```
run方法返回一个CompletedProcess实例，包含进程退出码以及输出等信息。

设置shell参数为True会导致subprocess创建一个新的中间shell进程运行命令。默认的行为是直接运行命令：
```python
completed = subprocess.run('echo $HOME', shell=True)
print('returncode:', completed.returncode)
```
如果需要使用shell管道、文件通配符、环境变量展开以及 ~ 展开到用户家目录，这将非常有用。

#### 错误处理
CompletedProcess 的 returncode 属性是程序的退出码。调用者负责解释它并检测错误。如果 run() 的 check 参数是 True，退出码将会被检查，如果有错误出现将会引发 CalledProcessError 异常。
```python
try:
    subprocess.run(['false'], check=True)
except subprocess.CalledProcessError as err:
    print('ERROR:', err)
```

#### 捕获输出
由 run() 启动的进程的标准输入输出渠道绑定在了父进程上。那就意味着调用程序不能捕获命令的输出。给 stdout 和 stderr 参数传递 PIPE 可以捕获输出用于后续处理。
```python
completed = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
print('returncode:', completed.returncode)
print('Have {} bytes in stdout:\n{}'.format(len(completed.stdout), completed.stdout.decode('utf-8')))
```

上面的也可以直接用`check_output()`方法获得标准输出：
```python
completed = subprocess.check_output(['ls', '-l'])
print(completed.decode('utf-8'))
```
默认情况下，`check_output()` 仅仅返回输入到标准输出的值。如果你需要同时收集标准输出和错误输出，使用 stderr 参数：
```python
completed = subprocess.check_output(['ls', '-l'], stderr=subprocess.STDOUT)
```
这个方法特别好用。

#### 抑制输出
某些情况下，输出不应该被展示和捕获，使用 DEVNULL 抑制输出流。
```python
import subprocess

try:
    completed = subprocess.run(
        'echo to stdout; echo to stderr 1>&2; exit 1',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
except subprocess.CalledProcessError as err:
    print('ERROR:', err)
else:
    print('returncode:', completed.returncode)
    print('stdout is {!r}'.format(completed.stdout))
    print('stderr is {!r}'.format(completed.stderr))
```
```shell
$python3 sub.py
returncode: 1
stdout is None
stderr is None
```
> - !s 在参数值上调用 str()
> - !r 在参数值上调用 repr()

#### popen方法
函数 run() ，call() ，check_call() 和 check_output() 是 Popen 类的包装。直接使用 Popen 能够对如何运行命令以及如何处理输入输出流提供更多的控制。
```python
text = b'''
    hello world
    this is a test
    goodbye'''

p = subprocess.Popen(['wc',], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
stdout, stderr = p.communicate(text)
out = stdout.decode('utf-8')
print(out)
```









