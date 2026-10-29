# 序列解包（Unpacking）

## 1. 交换两个变量

```python
a, b = 1, 2
a, b = b, a
assert (a, b) == (2, 1)
```

在 C 语言中通常需要临时变量；Python 的赋值语法允许同时处理多个目标。可以从概念上将右侧理解为“先求值、再对左侧进行解包”，但**不应断言解释器一定在内存中创建临时元组**：具体优化由解释器决定。

不推荐使用异或交换来代替临时变量；它可读性较差，而且当两侧实际引用同一存储位置时可能破坏值。

## 2. 星号解包（Extended Iterable Unpacking）

```python
data = [1, 2, 3, 4, 5]
first, *middle, last = data
assert first == 1
assert middle == [2, 3, 4]
assert last == 5
```

被 `*` 捕获的剩余元素会组成**列表**，即使原输入是元组或生成器。

```python
first, *middle, last = [1, 2]
assert middle == []
```

如果只有一个元素，以上两个固定位置无法同时分配，会抛出 `ValueError`。

## 3. 忽略不关心的字段

```python
record = ["Alice", "student", "Taipei", "100"]
name, *_, post_code = record
assert name == "Alice"
assert post_code == "100"
```

`_` 是表示“不关注”的变量命名惯例，并不是特殊语法；它依然会接收列表。对于真实 CSV 文件，包含引号和逗号的字段需要使用标准库 `csv`，不宜直接调用 `split(",")`。

## 来源

- [Python 赋值语句](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)
- [PEP 3132：Extended Iterable Unpacking](https://peps.python.org/pep-3132/)
