# any() and all()

这部分内容涉及到python非常重要的一个领域：
函数式编程思想和逻辑归约Reduction

这两个内置函数就像是逻辑门logical gates的集合版本

`any(iterable)`:只要可迭代对象中有一个元素为true，则返回结果为true

`all(iterable)`：只要当可迭代对象中所有的元素都为true，结果才为true

正常情况下的写法：
```py
has_negative = False
for x in numbers:
    if x < 0:
        has_negative = True
        break
```
在这种情况下，为了效率，用户必须手写一个break
这种逻辑看上去非常的啰嗦
你需要在维系一个外部状态变量has_negative的同时，
还需要手动处理一个break逻辑

在pythonic的写法（声明式编程）：
```py
has_negative = any(x < 0 for x in numbers)
```
这段代码直接告诉阅读者：
我在尝试检查numbers中是否存在任何一个小于0的书

在这行代码中，你在表答需要做什么，而不是应该怎么做

# 进阶版

## 短路逻辑short-circuiting

这是any()和all()最强大的地方，也是它们能够实现性能卓越的原因

* any() 会在遇到第一个true是立即停止，并返回true
* all() 会在遇到第一个false时立即停止，并发挥false

举一个栗子
```py
# 假设你有一个包含一百万个元素的列表
# 你想检查其中是否包含字符串"Error"

# 如果第一个元素就是"Error"，any()会直接返回True
# 而不会浪费不合理的内从和CPU遍历剩下的元素
found_error = any(is_error(item) for item in heavy_data)
```

## 生成器表达式 generator expression

这里需要注意的是，你在pythonic中使用的`(x < 0 for x in numbers)`
这并不是列表推导式（没有方括号），而是一个生成器表达式

这里就会有两个问题：

* 为什么不使用列表推导式？
`any([x < 0 for x in numbers])`：这个代码会先在内存中生成一个完整的布尔值列表，然后再交给any判断
这直接就是——浪费内存这一块...

* 为什么要使用生成器？
`any(x < 0 for x in numebrs)`: 这会一个一个的产生结果，any需要一个，生成器就会给它一个，一旦any觉得差不多了（即满足了短路的条件），剩下的数据就不会再被处理
这样能够省下大量的内容

## 必坑说明

掉坑了别说我没说...

* `any([])`结果是False：因为没有任何一个元素是True
* `all([])`结果是True: 这在数学上被称作“空真Vacuous Truth”，这意味着“在一个空集中，没有一个元素违反了我的规则，所以规则成立”

# 依旧是后日谈

在进行权限判断或者数据校验的时候
需要考虑到数据集为空的时候
```py
# 如果user_permissions是空的，all()会返回True
# 这可能会导致安全漏洞！！！
if user_permissions and all(p.is_active for p in user_permissions):
    pass
```

## 总结

嗯...

还是看看内容，别想着看总结了...

没时间就下次再看...
