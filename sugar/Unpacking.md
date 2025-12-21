## 序列解包 Unpacking

变量交换Variable Swapping
```py
a, b = b, a
```
这行代码是python中最为经典的写法之一，在其他的语言中通常需要引入一个中间变量
```c
int temp = a;
a = b;
b = temp;
```
* 这里特别讲解一下c语言中不使用中间变量的方法
```c
a = a ^ b;
b = a ^ b;
a = a ^ b;
```
需要注意的是：\
这个移除了中间变量的交换方案虽然在逻辑上是合理的，\
但是，在实际的c语言工程中，这段代码存在一个致命的地址别名问题Aliasing\
总的来说就是，不建议尝试这段代码内容

## 元组打包与解包Tuple Packing & Unpacking的底层逻辑

这行代码实际上发生了两个步骤的操作，顺序是先右后左：
1. 右侧打包Packing
python解释器首先计算等号右边的表达式b, a\
这时，python会在内存中创建一个临时的元组Tuple，\
内容是(b的值，a的值)
2. 左侧解包Unpacking
接着，解释器将这个临时元组中的元素，\
按照顺序分别赋值给左侧的变量a和b

## 提取部分元素 Extended Iterable Unpacking
```py
data = [1, 2, 3, 4, 5]
first, *middle, last = data
# first = 1, middle = [2, 3, 4], last = 5
```

这个语法特性是在python 3中引入的(PEP 3132)\
在python 2中，你必须通过切片来完成同样的工作

```py
# python 2老师写法
first = data[0]
middle = data[1: -1]
last = data[-1]
```
使用*操作符(通常称为Star Operator 或者 Splat Operator)\
我们可以动态地留住剩余的元素

*表示收集剩余的所有元素
这一点非常的关键，无论是右边的data是列表，元组，字符串还是生成器，带*的变量用永远会被赋值为一个列表List\
哪怕只捕获到一个元素，甚至捕获到元素（空列表），他也是列表

python解释器会自动根据左侧变量的坑位来计算*middle应该容纳多少个元素

* fist占了第一个
* last占了最后一个
* data总共有5个
* 所有middle自动获取中间的5 - 1 - 1 = 3 个元素

这种写法在处理非定长数据时非常的强大

1. 取头部，丢弃尾部
```py
rankings = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
winner, runner_up, *others = rankings
# winner='Alice', others=['Charlie', 'David', 'Eve']
```

2. 结合_(下划线)丢弃数据
在python惯例中，_表示我不关心的变量
```py
# 假设解析一个如 "name,email,phone,address,zip" 的CSV行
line = "John,john@example.com,12345,NY,10001"
name, email, *_, zip_code = line.split(',')
# 我们跳过了中间所有的字段，只拿头尾
```

3. 处理边界情况
考虑数据不够分的情况怎么解决？
```py
short_data = [1, 2]
first, *middle, last = short_data
# first = 1
# last = 2
# middle = []  <-- 注意这里是空列表，不会报错
```

注意：如果 short_data 只有 1 个元素，上述代码会抛出 ValueError，因为 first 和 last 至少需要两个元素来填充

