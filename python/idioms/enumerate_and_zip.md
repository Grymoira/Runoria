# enumerate() 与 zip()

## 1. enumerate：同时取得索引与元素

```python
names = ["Alice", "Bob"]

for index, name in enumerate(names, start=1):
    print(index, name)
# 1 Alice
# 2 Bob
```

相比 `for index in range(len(names))`，直接遍历 `enumerate(names)` 可以避免重复索引。它返回 **enumerate 迭代器对象**，并不是“生成器对象”；它不会提前构造完整的索引列表。

## 2. zip：并行遍历多个可迭代对象

```python
names = ["Alice", "Bob"]
ages = [20, 21]

for name, age in zip(names, ages):
    print(f"{name}: {age}")
```

默认 `zip` 会在最短输入耗尽时停止。这个行为方便，但也会**静默丢弃较长输入剩余的元素**。

如果长度本来应该相等，Python 3.10+ 建议使用：

```python
names = ["Alice", "Bob"]
ages = [20]

try:
    list(zip(names, ages, strict=True))
except ValueError:
    print("Input lengths do not match")
```

如果你确实需要保留较长输入的所有元素，可使用：

```python
from itertools import zip_longest

pairs = list(zip_longest(["Alice", "Bob"], [20], fillvalue=None))
assert pairs == [("Alice", 20), ("Bob", None)]
```

## 3. 实用写法

```python
keys = ["name", "age"]
values = ["Alice", 20]
record = dict(zip(keys, values, strict=True))
assert record == {"name": "Alice", "age": 20}

matrix = [[1, 2], [3, 4], [5, 6]]
transposed = list(zip(*matrix, strict=True))
assert transposed == [(1, 3, 5), (2, 4, 6)]
```

矩阵转置示例要求每行长度一致，使用 `strict=True` 避免不规则矩阵静默截断；输出是由元组构成的列表。

遇到多个可迭代对象时，应先考虑不等长输入是错误、允许截断，还是需要填充，再选择 `zip(strict=True)`、普通 `zip()` 或 `zip_longest()`。

## 来源

- [Python 内置函数：enumerate](https://docs.python.org/3/library/functions.html#enumerate)
- [Python 内置函数：zip](https://docs.python.org/3/library/functions.html#zip)
- [PEP 618：zip strict=True](https://peps.python.org/pep-0618/)
