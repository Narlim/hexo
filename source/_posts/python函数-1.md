---
title: python函数
date: 2020-05-26 22:03:18
tags: python
---

python函数总结。
<!--more-->

#### 匿名函数
lambda 关键字在 Python 表达式内创建匿名函数。

```python
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

除了作为参数传给高阶函数之外，Python 很少使用匿名函数。由于句法上的限制，非平凡的 lambda 表达式要么难以阅读，要么无法写出。


#### 可调用对象
>除了用户定义的函数，调用运算符(即 ())还可以应用到其他对象 上。如果想判断对象能否调用，可以使用内置的 callable() 函数。 Python 数据模型文档列出了 7 种可调用对象。
- 用户定义的函数:  
	使用def语句或lambda表达式创建

- 内置函数:  
	使用C语言（CPython）实现的函数，如len或者time.strftime
- 内置方法:  
	使用C语言实现的方法，如dict.get
- 方法:  
	在类的定义体中定义的函数
- 类:  
	调用类时会运行类的 `__new__` 方法创建一个实例，然后运行 `__init__` 方法，初始化实例，最后把实例返回给调用方。因为 Python 没有 new 运算符，所以调用类相当于调用函数。
- 类的实例:  
	如果类定义了 `__call__` 方法，那么它的实例可以作为函数调用。
- 生成器函数:  
	使用 yield 关键字的函数或方法。调用生成器函数返回的是生成 器对象。

可以使用内置的callable()函数来判断对象是否可调用。

### 用户定义的可调用类型
```python
import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)     # 在本地构建一个副本，防止列表意外副作用。
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def __call__(self):
        return self.pick()            # bingo.pick()的快捷方式是bingo()

>>> bingo = BingoCage(range(3))
>>> bingo.pick()
1
>>> bingo()
0
>> callable(bingo)
True
```

### 函数内省
dir函数可以查看函数具有的属性：
```python
>>> dir(factorial)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>>
```
下面是几个与把函数视为对象相关的几个属性：
#### __dict__

下面是函数专有而用户定义的一般对象没有的属性：
```python
In [18]: class C: pass

In [19]: obj = C()

In [20]: def func(): pass

In [21]: sorted(set(dir(func)) - set(dir(obj)))
Out[21]:
['__annotations__',
 '__call__',
 '__closure__',
 '__code__',
 '__defaults__',
 '__get__',
 '__globals__',
 '__kwdefaults__',
 '__name__',
 '__qualname__']
```

### 从定位参数到仅限关键字参数


### 获取关于参数的信息
```python
import bobo

@bobo.query('/')
def hello(person):
	return 'Hello %s!' % person
```
这里的关键是，Bobo 会内省 hello 函数，发现它需要一个名为 person 的参数，然后从请求中获取那个名称对应的参数，将其传给 hello 函 数，因此程序员根本不用触碰请求对象。

Bobo 是怎么知道函数需要哪个参数的呢?它又是怎么知道参数有没有 默认值呢?
函数对象有个 `__defaults__` 属性，它的值是一个元组，里面保存着定位参数和关键字参数的默认值。仅限关键字参数的默认值在 `__kwdefaults__` 属性中。然而，参数的名称在 `__code__` 属性中，它的值是一个 code 对象引用，自身也有很多属性。


再看下面的一个函数：
```python
def clip(text, max_len=80):
    """在max_len前面或后面的第一个空格处截断文本 """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rfind()
```
提取关于函数的信息：
```python
>>> from clip import clip
>>> clip.__defaults__
(80,)
>>> clip.__code__ # doctest: +ELLIPSIS <code object clip at 0x...>
>>> clip.__code__.co_varnames
('text', 'max_len', 'end', 'space_before', 'space_after') >>> clip.__code__.co_argcount
2
```

使用inspect模块更好地提取函数的信息：
```python
>>> from clip import clip
>>> from inspect import signature
>>> sig = signature(clip)
>>> sig # doctest: +ELLIPSIS
<inspect.Signature object at 0x...>
>>> str(sig)
'(text, max_len=80)'
>>> for name, param in sig.parameters.items():
... print(param.kind, ':', name, '=', param.default) ...
POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'> POSITIONAL_OR_KEYWORD : max_len = 80
```

kind 属性的值是 _ParameterKind 类中的 5 个值之一，列举如下：
- POSITIONAL_OR_KEYWORD: 可以通过定位参数和关键字参数传入的形参(多数 Python 函数的参 数属于此类)。
- VAR_POSITIONAL: 定位参数元组
- VAR_KEYWORD: 关键字参数字典
- KEYWORD_ONLY: 仅限关键字参数
- POSITIONAL_ONLY: 仅限定位参数;目前，Python 声明函数的句法不支持，但是有些使 用 C 语言实现且不接受关键字参数的函数(如 divmod)支持。

inspect.Signature 对象有个 bind 方法，它可以把任意个参数绑定 到签名中的形参上，所用的规则与实参到形参的匹配方式一样:
```python
>>> import inspect
>>> sig = inspect.signature(tag)  # 获取tag函数的签名
>>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
... 'src': 'sunset.jpg', 'cls': 'framed'}
>>> bound_args = sig.bind(**my_tag)  # 把一个字典参数传给.bind()方法
>>> bound_args
<inspect.BoundArguments object at 0x...> 
>>> for name, value in bound_args.arguments.items(): 
... print(name, '=', value)
...
name = img
cls = framed
attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'} >>> del my_tag['name'] 
>>> bound_args = sig.bind(**my_tag)   # 缺少name参数，报错
Traceback (most recent call last):
...
TypeError: 'name' parameter lacking default value
```
这个示例在 inspect 模块的帮助下，展示了 Python 数据模型把实参绑 定给函数调用中的形参的机制，这与解释器使用的机制相同。



### 函数注解
和上面的clip唯一的区别在于第一行
```python
def clip(text: str, max_len: 'int > 0' = 80) -> str:
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rfind()
```
注解不会做任何处理，只是存储在函数的 `__annotations__` 属性(一个字典)中:
```python
>>> from clip_annot import clip
>>> clip.__annotations__
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
```