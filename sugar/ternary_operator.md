# 三元运算符 ternary operator

在很多的编程语言中，三元运算符基础的语法结构通常是
condition ? value_1 : value_2

但是在Python中的三元运算符则更加的接近自然语言的用法
结果 = 值为真的时候的输出 if 判断条件 else 值为假的时候的输出

它实际上是将传统的4行if-else结构压缩为一行

传统的写法为：

```py
if score > 60:
    status = 'Pass'
else:
    status = 'Fail'
```

这个Pythonic的写法：

```py
status = 'Pass' if score > 60 else 'Fail'
```

# 后日谈

这种方法只建议使用在简单的赋值上面，如果逻辑过于复杂，或者需要在if分支中执行多行的代码，依旧是建议回归到标准的写法中，否则很容易破坏代码的可读性；

千万不要像这样去写：
```py
res = "A" if x > 90 else "B" if x > 80 else "C"
```
这样的套娃，嗯，不想被同行殴打的话，还是不建议这样去写；

可以尝试在列表推导式中使用这种语法：
```py
# 将负数统一标记为0，整数保持不改变
processed_data = [x if x > 0 else 0 for x in raw_data]
```

