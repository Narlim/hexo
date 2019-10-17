---
title: python变量作用域和闭包
date: 2019-10-17 21:15:38
tags: python
---

摘录自《流畅的python》第七章。
<!--more-->

#### 变量作用域
```python
>>> def f1(a):
...     print(a)
...     print(b)
...
>>> f1(3)
3
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "<stdin>", line 3, in f1
NameError: global name 'b' is not defined

>>> b = 6
>>> f1(3)
3
6
```
再看一个示例：
```python
>>> b = 6
>>> def f2(a):
...     print(a)
...     print(b)
...     b = 9
...
>>> f2(3)
3
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment
```
Python 不要求声明变量,但是假定在函数定义体中赋值的变量是局部变量。这比 JavaScript 的行为好多了,JavaScript 也不要求声明变量,但是如果忘记把变量声明为局部变量(使用 var),可能会在不知情的情况下获取全局变量。

如果想让解释器把b当成全局变量，要使用global声明：
```python
>>> b = 6
>>> def f3(a):
        global b
        print(a)
        print(b)
        b = 9

>>> f3(3)
3
6
>>> b
9
>>> f3(3)
9
```
下面是闭包

#### 闭包
闭包指延伸了作用域的函数,其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系,关键是它能访问定义体之外定义的非全局变量。

下面一个例子可能有点晦涩：
是一个计算不断增加值的均值的函数。
```python
class Aerager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value)
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
```
```python
>>> avg = Averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
```
下面是函数的实现：
```python
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager
```
```python
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
```
Averager类的实例avg把值存储在self.series实例属性，但是第二个示例的avg函数呢？注意,series 是 make_averager 函数的局部变量,因为那个函数的定义体中初始化了 series:series = []。可是,调用 avg(10)时,make_averager 函数已经返回了,而它的本地作用域也一去不复返了。

在 averager 函数中,series 是自由变量(free variable)。这是一个技术术语,指未在本地作用域中绑定的变量。

综上,闭包是一种函数,它会保留定义函数时存在的自由变量的绑定,这样调用函数时,虽然定义作用域不可用了,但是仍能使用那些绑定。

**注意,只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。**

#### nonlocal声明
下面是一个有问题的示例：
```python
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager
```
错误的原因就是这句：`count += 1`，这句是一个赋值语句，这会把`count`当成局部变量，`total`也一样。前面没有遇到这个问题，是因为没有给series赋值，只是调用了方法，并把它传给sum和len，也就是说，我们利用了列表是可变的对象这一事实。
但是对数字、字符串、元组等不可变类型来说,只能读取,不能更新。如果尝试重新绑定,例如 count = count + 1,其实会隐式创建局部变量 count。这样,count 就不是自由变量了,因此不会保存在闭包中。

为了解决这个问题,Python 3 引入了 nonlocal 声明。它的作用是把变量标记为自由变量,即使在函数中为变量赋予新值了,也会变成自由变量。如果为 nonlocal 声明的变量赋予新值,闭包中保存的绑定会更新。
```python
def make_averager():
    count = 0
    total = 0
def averager(new_value):
    nonlocal count, total
    count += 1
    total += new_value
    return total / count
return averager
```

