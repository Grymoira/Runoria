## 列表推导式 Comprehensions

一般情况的写法
```py
temp = []
for i in range(10):
    if i % 2 == 0:
        temp.append(i**2)
```

列表推导式comprehensions写法
```py
temp = [i**2 for i in range(10) if i % 2 == 0]
```

这里会例举一个多重嵌套的写法
```py
temp = []
for i in range(10):
    if i % 2 == 0:
        temp.append(1**2)
    elif i == 1:
        temp.append(21)
    else:
        temp.append('fuck')
```

它的comprehension写法
```py
temp = [i**2 if i % 2 == 0 else 21 if i == 1 else 'fuck' for i in range(10)]
```
这种多重嵌套是不建议使用的，还有一种更易于理解的写法：
```py
def process_logic(i):
    if i % 2 == 0:
        return 1**2
    if i == 1:
        return 21
    return 'fuck'
temp = [process_logic(i) for i in range(10)]
```

列表推导式在性能上能够起到比一般的写法更快的速度\
在常规的写法中，普通的for循环的每次循环\
都需要调用List的append方法，在python字节码层面，\
这涉及到属性查找(LOAD_ATTR)和函数调用(CALL_FUNCTION)，开销较大\
而在编译推导式的时候，会将其优化为特定的字节码指令(LIST_APPEND)，\
这不仅减少了属性查找的开销，而且其循环逻辑实在c语言层面实现的，

同时，这种方法在Python 3中能够实现作用域的隔离，但是常规写法不能\
在python 3中，列表推导式有自己的闭包作用域，变量不再泄露\
但是，普通的for循环在python 3中依旧会泄露变量

拓展字典与集合推导式

字典推导dictionary comprehension
```py
temp_map = {x: x * x for x in range(5)}
```
result: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

这在做数据清洗的时候非常的有用\
比如将两个列表合并成一个字典\
{k: v for k, v in zip(keys, values)}

集合推导 set comprehension\
很多的人都会忘记这个内容\
如果你把中括号[]换成花括号{}并且没有键值对冒号\
它就是集合推导（自动去重）

```py
numbers = [1, 1, 2, 2, 3]
unique_squares = {x * x for x in numbers}
```
result: {1, 4, 9} （自动去重了）

## 相关说明


生成器表达式说明\
如果你的range不是10，而是100,000,000,000或者更大\
列表推导式会立刻创建一个包含这么多个元素的列表，瞬间撑爆你的电脑内存\
这个时候，把方括号[]换成圆括号()

这不是元组推导式（python没有元组推导式），这是生成器表达式
```py
squares_gen = (x * x for x in range(10000000000) if x % 2 == 0)
```

它不会立刻计算结果，而是返回一个生成器对象\
只有当你去遍历它（用for或者next()）的时候\
他才会一次吐出一个值\
这样能够省出大量的内存


## 容易混淆的地方
过滤Filter: if在for后面
```py
[x for x in data if x > 0] # 只保留大于0的数，列表变短
```

映射逻辑Map: if ... else在for前面
```py
[x if x > 0 else 0 for x in data] # 列表长度不变，小于0的变成0
```

这行代码的核心逻辑为原地修正Mapping / Transformation\
将这段话翻译成简单易懂的话为：\
便利data列表，如果遇到的数字大于0，就保留原样；\
否则就把他变成0，最后生成一个新的列表\
需要注意的是，列表的长度是不变的，变的是元素的值\
意思就是说，生成的新的列表中很可能会同时包含多个为0的元素

这行代码的语法涉及到了python中列表推导式的通用公式：\
[<表达式> for <变量> in <可迭代对象>]\
在这行代码中，最关键的<表达式>部分使用了Python的三元运算符Ternary operator\
为了方便理解，我在这里写出这行代码最初的循环写法：

```py
data = [-5, 3, -1, 10, 0]
result = []
for x in data:
    if x > 0:
        val = x
    else:
        val = 0
    result.append(val)
```

这里需要详细讲解两种情况：\
'if' before the 'for' AND 'if' behind the 'for'abs

if在for的前面，这是映射map的逻辑\
在这种情况下必须要带上else，因为你必须要告知python，\
如果不满足条件，需要填入的内容是什么，如果不写else，表达式就不完整

if在for的后面，这是过滤filter的逻辑\
这种情况下，是不能带else的\
这里只需要判断是否需要把x放进列表中\
结果就是导致列表的长度变短了（不满足条件的元素都会被遗弃）

嗯~ o(*￣▽￣*)o\
不要过度的使用推导式哦\
特别是两层及以上的循环嵌套\
Readability counts

这就是一个非常糟糕的代码
```py
result = [x * y for x in range(10) if x > 5 for y in range(5) if y < 2]
```

什么时候需要放弃推导式\
如果你的循环体中不仅仅是计算返回值\
还有副作用(比如print(), database.save(), 或者修改外部变量)\
这种情况下，请不要使用推导式

itertools模块\
当你发现生成器表达式变得极其复杂时\
此时你应该去查看python标准库itertools\
比如不要写(x for x in list1 for y in list2)来做笛卡尔积\
而是使用itertools.product
