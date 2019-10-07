---
title: python数组
date: 2019-10-07 15:02:06
tags: python
---

python数组总结。
如果我们需要一个只包含数字的列表,那么 array.array 比 list 更高效。数组支持所有跟可变序列有关的操作,包括 .pop、.insert 和.extend。另外,数组还提供从文件读取和存入文件的更快的方法,如.frombytes 和 .tofile。
<!--more-->
创建一个1000万个随机浮点数的数组：
```python
floats = array('d', (random() for i in range(10**7))) # 'd'是类型码，注意后面的生成器表达式写法
print(floats[-1])
with open('floats.bin', 'wb') as f:
    floats.tofile(f)
    
floats2 = array('d')
with open('floats.bin', 'rb') as f:
    floats2.fromfile(f, 10**7)
print(floats2[-1])
print(floats == floats2)

0.04699210455263536
0.04699210455263536
True
```

