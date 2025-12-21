# enumerate and zip

如果你学过c语言，那么你一定会不习惯这一部分的内容

但是完全不需要担心

我讲的足够看得懂

## enumerate ： 优雅的计数器

在很多的语言中，如果你需要索引，你就需要首先定义一个变量i，然后每循环一次+1
但是在python中，我们选择更加直接的方式来解决这个问题

这里涉及一个问题：
为什么不使用range(len(...))?

普通的写法：
```py
names = ["alice", "bob"]
for i in range(len(names)):
    name = names[i]
    print(f"{i}: {name}")
```

pythonic的写法：
```py
for i, name in enumerate(names):
    print(f"{i}: {name}")
```

## 后日谈

一些好的tips

1. 自定义其实索引：这是很多人都会自己忽略的方式

如果你想让编号从1开始，不需要写成i+1：
```py
for i, name in enumerate(names, start = 1):
    print(f"{i}: {name}")
```

2. 解构Unpacking：enumerate每次迭代都会返回一个元组(index, element)
我们直接在for语句中使用i, name将其解构，让代码变得更加简洁

3. 性能方面：enumerate是一个生成器对象，他不会在内存中创建完整的索引列表，即使遍历超级多个元素，它也能够尽可能的省下内存

# zip
接下来我们来讲解一下zip这部分的内容

zip光是从命名上面就非常的形象，就像是拉链一样，将两部分的元素一对一的整合在一起

正常的写法：
```py
names = ['alice', 'bob']
ages = [24, 30]
for i in range(len(names)):
    name = names[i]
    age = ages[i]
    print(f"{name} is {age}")
```
这种写法很糟糕，因为很容易出现一些如果两个列表的长度不一致，
报错indexError

pythonic的写法：
```py
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
```

## 经验谈

1. zip有一个特性：如果两个列表的长度不相同，他会以短的那个列表为准，长的那个剩下的列表元素会被自动的忽略，这个特性叫做最短对齐原则

2. 处理不等长列表zip_longest： 当你需要以长的列表为准的话，缺失的元素位使用None填充，这个时候你需要调用itertools模块
```py
from itertools import zip_longest
for name, age in zip_longest(names, ages, fillvalue = "Unkonwn"):
    pass
```

3. 矩阵转置： 这是一个很不常见的操作，使用zip(*matrix)可以瞬间实现矩阵的转置操作
```py
matrix = [[1, 2], [3, 4], [5, 6]]
transposed = list(zip(*matrix))
```
这个代码的结果会输出：
[(1, 3, 5), (2, 4, 6)]

4. 生成字典： zip能够很方便的创建一个字典
```py
user_dict = dict(zip(names, ages))
```
